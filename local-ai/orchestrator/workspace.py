"""Shell-free, workspace-confined filesystem operations for Tool Protocol actions."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .models import ToolOperation, ToolResult


class WorkspacePathError(ValueError):
    """Raised when a target path is not a canonical workspace descendant."""


class WorkspaceOperationError(RuntimeError):
    """Raised when a validated operation cannot be performed safely."""


_DRIVE_PATH = re.compile(r"^[A-Za-z]:")


def resolve_workspace_path(*, workspace: Path, target_path: str) -> Path:
    """Resolve one strictly canonical POSIX path beneath *workspace*.

    Lexical checks reject alternate separators, device/absolute forms, and traversal
    before resolving links.  Resolving the prospective target then prevents an
    existing symlink from redirecting a mutation outside the workspace.
    """
    root = workspace.resolve()
    candidate = Path(target_path)
    if (
        not target_path
        or "\\" in target_path
        or _DRIVE_PATH.match(target_path)
        or candidate.is_absolute()
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        raise WorkspacePathError("invalid workspace path")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise WorkspacePathError("path resolves outside workspace") from error
    return resolved


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_text_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.is_dir():
        raise WorkspaceOperationError("target is a directory")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise WorkspaceOperationError("binary target cannot be mutated") from error


@dataclass
class WorkspaceToolExecutor:
    """Safely execute the tiny allowlisted set of local filesystem mutations."""

    workspace: Path
    storage: Path
    delete_enabled: bool = False
    clock: Callable[[], str] | None = None

    def __post_init__(self) -> None:
        self.workspace = self.workspace.resolve()
        self.storage = self.storage.resolve()
        try:
            self.storage.relative_to(self.workspace)
        except ValueError as error:
            raise WorkspaceOperationError("storage must be inside workspace") from error

    def execute(self, operation: ToolOperation) -> ToolResult:
        """Apply a validated operation without launching a shell and record its result."""
        try:
            target = resolve_workspace_path(workspace=self.workspace, target_path=operation.target_path)
        except WorkspacePathError as error:
            raise WorkspaceOperationError(str(error)) from error
        before = _read_text_if_exists(target)
        if operation.action == "mkdir":
            target.mkdir(parents=True, exist_ok=True)
        elif operation.action == "write_file":
            content = operation.arguments.get("content")
            if not isinstance(content, str):
                raise WorkspaceOperationError("write_file requires string content")
            self._reject_package_script_change(target, before, content)
            self._atomic_write(target, content)
        elif operation.action == "patch_file":
            old_text = operation.arguments.get("old_text")
            new_text = operation.arguments.get("new_text")
            if not isinstance(old_text, str) or not isinstance(new_text, str):
                raise WorkspaceOperationError("patch_file requires old_text and new_text strings")
            if before is None:
                raise WorkspaceOperationError("patch target does not exist")
            if not old_text or before.count(old_text) != 1:
                raise WorkspaceOperationError("patch context must have one unique match")
            patched = before.replace(old_text, new_text, 1)
            self._reject_package_script_change(target, before, patched)
            self._atomic_write(target, patched)
        elif operation.action == "delete_file":
            if not self.delete_enabled:
                raise WorkspaceOperationError("delete_file is disabled")
            if before is None:
                raise WorkspaceOperationError("delete target does not exist")
            target.unlink()
        else:  # ToolOperation protects this; retain a safe boundary for callers.
            raise WorkspaceOperationError("unsupported action")

        after = _read_text_if_exists(target)
        result = ToolResult(
            task_id=operation.task_id,
            action=operation.action,
            resolved_path=target.relative_to(self.workspace).as_posix(),
            status="completed",
            timestamp=self._timestamp(),
        )
        self._record(operation=operation, result=result, before=before, after=after)
        return result

    @staticmethod
    def _package_scripts(text: str | None) -> object:
        """Return the ``scripts`` value of a package.json text, ``{}`` if absent or the file is new."""
        if text is None:
            return {}
        try:
            document = json.loads(text)
        except json.JSONDecodeError as error:
            raise WorkspaceOperationError("package.json is not valid JSON, so its scripts cannot be checked") from error
        return document.get("scripts", {}) if isinstance(document, dict) else {}

    def _reject_package_script_change(self, target: Path, before: str | None, after: str) -> None:
        """The executor may not add or change ``scripts`` in package.json: ``npm run`` would execute them."""
        if target.name != "package.json":
            return
        if self._package_scripts(before) != self._package_scripts(after):
            raise WorkspaceOperationError("package.json scripts may not be changed by the executor")

    def _atomic_write(self, target: Path, content: str) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent, text=True)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise

    def _record(self, *, operation: ToolOperation, result: ToolResult, before: str | None, after: str | None) -> None:
        task_directory = self.storage / "protocol-records" / operation.task_id.replace(".", "_")
        task_directory.mkdir(parents=True, exist_ok=True)
        timestamp = self._timestamp().replace(":", "-")
        payload = {
            **result.to_dict(),
            "before_hash": _hash_text(before) if before is not None else None,
            "after_hash": _hash_text(after) if after is not None else None,
            "expected_result": operation.expected_result,
        }
        self._atomic_write(task_directory / f"{timestamp}-result.json", json.dumps(payload, indent=2) + "\n")

    def _timestamp(self) -> str:
        if self.clock is not None:
            return self.clock()
        from datetime import UTC, datetime

        return datetime.now(UTC).isoformat()
