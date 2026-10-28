"""Deterministic, task-bounded payload construction for fresh model turns."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping, Sequence

from .config import ContextConfig
from .models import ExecutionMode, GoalTask


@dataclass(frozen=True)
class ContextManifest:
    """Auditable description of the bounded active-file contribution."""

    included_paths: tuple[str, ...]
    file_hashes: dict[str, str]
    truncated_paths: tuple[str, ...]
    payload_bytes: int


@dataclass(frozen=True)
class PackedContext:
    """One immutable request context and its manifest."""

    payload: dict[str, Any]
    manifest: ContextManifest


class ContextPacker:
    """Build fresh contexts from static anchors and the currently active task only."""

    def __init__(
        self,
        *,
        workspace: Path,
        config: ContextConfig | None = None,
        rules_text: str | None = None,
        architecture_text: str | None = None,
        max_total_bytes: int | None = None,
        max_file_bytes: int | None = None,
        max_active_files: int | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        if config is not None:
            self.rules_text = config.rules_path.read_text(encoding="utf-8")
            self.architecture_text = config.architecture_path.read_text(encoding="utf-8")
            self.max_total_bytes = config.max_total_bytes
            self.max_file_bytes = config.max_file_bytes
            self.max_active_files = config.max_active_files
        else:
            if None in (rules_text, architecture_text, max_total_bytes, max_file_bytes, max_active_files):
                raise ValueError("packer needs ContextConfig or every explicit context setting")
            self.rules_text = str(rules_text)
            self.architecture_text = str(architecture_text)
            self.max_total_bytes = int(max_total_bytes)
            self.max_file_bytes = int(max_file_bytes)
            self.max_active_files = int(max_active_files)
        if min(self.max_total_bytes, self.max_file_bytes, self.max_active_files) < 1:
            raise ValueError("context limits must be positive")

    def pack(self, *, task: GoalTask, mode: ExecutionMode, evidence: Any) -> PackedContext:
        """Pack target hints as the only workspace file candidates."""
        return self._build(task=task, mode=mode, evidence=evidence, active_files=task.active_target_hints, plan=None)

    def build_payload(
        self,
        *,
        task: GoalTask,
        mode: ExecutionMode,
        mode_evidence: Any,
        active_files: Sequence[Path],
        plan: Any = None,
    ) -> dict[str, Any]:
        """Build one fresh request payload, optionally carrying the current plan."""
        return self._build(task=task, mode=mode, evidence=mode_evidence, active_files=active_files, plan=plan).payload

    def _build(
        self, *, task: GoalTask, mode: ExecutionMode, evidence: Any, active_files: Sequence[Path | str], plan: Any
    ) -> PackedContext:
        files, manifest = self._files(active_files)
        scope: dict[str, Any] = {
            "task_id": str(task.id),
            "heading": task.heading,
            "objective": task.objective,
            "acceptance_criteria": list(task.acceptance_criteria),
            "prerequisites": list(task.prerequisites),
            "implementation_details": task.implementation_details,
            "execution_mode": mode.value,
            "mode_evidence": evidence,
            "validation_commands": [command.canonical_text for command in task.validation_commands],
            "files": files,
        }
        if plan is not None:
            scope["plan"] = plan
        payload = {
            "context": {
                "system_rules": self.rules_text,
                "architecture_schema": self.architecture_text,
                "active_task_scope": scope,
            }
        }
        return PackedContext(payload=payload, manifest=manifest)

    def _files(self, candidates: Sequence[Path | str]) -> tuple[list[dict[str, str]], ContextManifest]:
        normalized: list[tuple[str, Path]] = []
        for candidate in candidates:
            raw = Path(candidate)
            target = raw.resolve() if raw.is_absolute() else (self.workspace / raw).resolve()
            try:
                relative = target.relative_to(self.workspace).as_posix()
            except ValueError:
                continue
            if target.is_file():
                normalized.append((relative, target))
        selected = sorted(dict(normalized).items())[: self.max_active_files]
        files: list[dict[str, str]] = []
        hashes: dict[str, str] = {}
        truncated: list[str] = []
        consumed = 0
        for relative, target in selected:
            raw = target.read_bytes()
            hashes[relative] = sha256(raw).hexdigest()
            available = max(0, self.max_total_bytes - consumed)
            limit = min(self.max_file_bytes, available)
            content = raw[:limit].decode("utf-8", errors="replace")
            was_truncated = len(raw) > limit
            if was_truncated:
                marker = "\n[TRUNCATED]"
                marker_bytes = len(marker.encode("utf-8"))
                retained = raw[: max(0, limit - marker_bytes)].decode("utf-8", errors="replace")
                content = retained + marker
                truncated.append(relative)
            consumed += min(len(raw), limit)
            files.append({"path": relative, "content": content, "sha256": hashes[relative]})
        return files, ContextManifest(tuple(path for path, _ in selected), hashes, tuple(truncated), consumed)
