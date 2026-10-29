"""Atomic workspace-local persistence for scheduler state and immutable artifacts."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import RunState


class StateLoadError(RuntimeError):
    """Raised when durable scheduling state is missing, malformed, or incompatible."""


class WorkspaceLockedError(RuntimeError):
    """Raised when another live scheduler owns the workspace-local lock."""


class AtomicStateStore:
    """Store scheduler authority only below ``workspace/local-ai``."""

    def __init__(self, *, workspace: Path, workspace_id: str, schema_version: int) -> None:
        self.workspace = workspace.resolve()
        self.workspace_id = workspace_id
        self.schema_version = schema_version
        self.storage_root = (self.workspace / "local-ai").resolve()
        self.state_directory = self.storage_root / "program-states"
        self.state_path = self.state_directory / "run-state.json"
        self.previous_state_path = self.state_directory / "run-state.previous.json"
        self.lock_path = self.state_directory / "scheduler.lock"
        self._lock_token: str | None = None

    def _ensure_storage(self) -> None:
        self.state_directory.mkdir(parents=True, exist_ok=True)
        if not self.state_directory.resolve().is_relative_to(self.storage_root):
            raise StateLoadError("state storage escapes workspace-local storage")

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(UTC).isoformat()

    def _atomic_write_bytes(self, target: Path, content: bytes) -> None:
        """Flush a same-directory temporary file before replacing its target."""
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, target)
            # Persist the directory entry when the platform permits directory handles.
            try:
                directory_fd = os.open(target.parent, os.O_RDONLY)
            except OSError:
                return
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()

    def commit(self, state: RunState) -> None:
        """Atomically replace state while retaining the previous valid generation."""
        self._ensure_storage()
        self._validate_state(state)
        if self.state_path.exists():
            # The prior generation remains readable even if the new primary is interrupted.
            self._atomic_write_bytes(self.previous_state_path, self.state_path.read_bytes())
        payload = json.dumps(state.to_dict(), indent=2, sort_keys=True).encode("utf-8") + b"\n"
        self._atomic_write_bytes(self.state_path, payload)

    def _validate_state(self, state: RunState) -> None:
        if state.workspace_id != self.workspace_id:
            raise StateLoadError("state workspace identity does not match this workspace")
        if state.schema_version != self.schema_version:
            raise StateLoadError("state schema version does not match this scheduler")
        in_progress = [
            task_id for task_id, record in state.task_records.items() if record.status.value == "in_progress"
        ]
        if len(in_progress) > 1:
            raise StateLoadError("state contains more than one in-progress task")
        if (state.active_task_id is None) != (not in_progress):
            raise StateLoadError("state active task pointer disagrees with task records")
        if in_progress and state.active_task_id != in_progress[0]:
            raise StateLoadError("state active task pointer disagrees with in-progress task")

    def load(self) -> RunState:
        """Read and validate primary scheduler authority; never silently use a backup."""
        if not self.state_path.exists():
            raise StateLoadError("run state is absent")
        try:
            decoded = json.loads(self.state_path.read_text(encoding="utf-8"))
            if not isinstance(decoded, dict):
                raise ValueError("state document must be an object")
            # Version 1 documents lack model_turns. They load as version 2 with no turns, and the next
            # commit writes version 2.
            if decoded.get("schema_version") == 1 and self.schema_version == 2:
                decoded["schema_version"] = 2
            state = RunState.from_dict(decoded)
            self._validate_state(state)
            return state
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            if isinstance(error, StateLoadError):
                raise
            raise StateLoadError(f"run state is unreadable: {error}") from error

    def write_json_artifact(self, relative_path: str, value: dict[str, Any]) -> str:
        """Atomically persist an immutable JSON artifact beneath local storage."""
        candidate = Path(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts or "\\" in relative_path:
            raise ValueError("artifact path must be workspace-relative POSIX text")
        target = (self.storage_root / candidate).resolve()
        try:
            target.relative_to(self.storage_root)
        except ValueError as error:
            raise ValueError("artifact path escapes workspace-local storage") from error
        self._atomic_write_bytes(target, json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        return target.relative_to(self.workspace).as_posix()

    def acquire_lock(self, *, recover_stale: bool = False) -> None:
        """Acquire the exclusive local scheduler lock, recovering only a stale owner."""
        self._ensure_storage()
        token = f"{os.getpid()}-{datetime.now(UTC).timestamp()}"
        payload = {"owner": token, "pid": os.getpid(), "created_at": self._timestamp(), "workspace_id": self.workspace_id}
        try:
            descriptor = os.open(self.lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            if not recover_stale or not self._lock_is_stale():
                raise WorkspaceLockedError("workspace scheduler lock is already held")
            previous = self.lock_path.read_text(encoding="utf-8", errors="replace")
            self._write_stale_lock_report(previous)
            self.lock_path.unlink(missing_ok=True)
            return self.acquire_lock(recover_stale=False)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        self._lock_token = token

    def _lock_is_stale(self) -> bool:
        try:
            payload = json.loads(self.lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return True
        pid = payload.get("pid") if isinstance(payload, dict) else None
        if not isinstance(pid, int) or pid <= 0:
            return True
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            return False
        return False

    def _write_stale_lock_report(self, lock_evidence: str) -> None:
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        target = self.storage_root / "quarantine" / f"{timestamp}-stale-lock.md"
        body = (
            "# Quarantine: stale scheduler lock recovery\n\n"
            "- **Category:** stale-lock-recovery\n"
            f"- **Recorded:** `{self._timestamp()}`\n"
            "- **Recovery:** stale lock removed before local scheduler startup\n\n"
            "## Prior lock evidence\n\n```json\n"
            f"{lock_evidence}\n```\n"
        )
        self._atomic_write_bytes(target, body.encode("utf-8"))

    def release_lock(self) -> None:
        """Release only the lock acquired by this store instance."""
        if self._lock_token is None:
            return
        try:
            payload = json.loads(self.lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        if payload.get("owner") == self._lock_token:
            self.lock_path.unlink(missing_ok=True)
        self._lock_token = None
