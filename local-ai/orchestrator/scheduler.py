"""Durable one-at-a-time scheduling over workspace-local run state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from .models import ExecutionMode, GoalTask, TaskId, TaskStatus
from .quarantine import write_state_quarantine_report, write_validation_failure_quarantine_report
from .state_store import AtomicStateStore, StateLoadError


class StateExecutionRefused(RuntimeError):
    """Raised when the scheduler cannot safely use durable state as authority."""


@dataclass(frozen=True)
class ErrorModeContext:
    """Exact validation failure evidence included in the next Error-mode request."""

    mode: ExecutionMode
    command: str
    stdout: str
    stderr: str
    exit_code: int
    artifact_path: str


@dataclass(frozen=True)
class ErrorModeRequest:
    """A durably counted Error-mode request authorization."""

    mode: ExecutionMode
    request_number: int


class Scheduler:
    """Select, resume, complete, and recover exactly one durable task at a time."""

    def __init__(self, store: AtomicStateStore) -> None:
        self.store = store
        self._validation_failures: dict[str, list[dict[str, object]]] = {}

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(UTC).isoformat()

    def _load_or_refuse(self):
        try:
            return self.store.load()
        except StateLoadError as error:
            self._write_state_failure_report(str(error))
            raise StateExecutionRefused(f"state unavailable: {error}") from error

    def _write_state_failure_report(self, detail: str) -> None:
        write_state_quarantine_report(workspace=self.store.workspace, category="state-failure", detail=detail)

    def _active_record(self, task_id: TaskId):
        state = self._load_or_refuse()
        expected_id = str(task_id)
        if state.active_task_id != expected_id:
            raise ValueError("only the current active task can transition")
        record = state.task_records.get(expected_id)
        if record is None or record.status is not TaskStatus.IN_PROGRESS:
            raise ValueError("active task is not in progress")
        return state, record

    def select_next(self, *, on_selected: Callable[[GoalTask], None] | None = None) -> GoalTask:
        """Resume persisted active work or durably claim the first queued task."""
        state = self._load_or_refuse()
        if state.active_task_id is not None:
            active_id = state.active_task_id
            for queued in state.queue:
                if str(queued.task.id) == active_id:
                    return queued.task
            raise StateExecutionRefused("state active task is absent from the durable queue")

        for queued in state.queue:
            task_id = str(queued.task.id)
            record = state.task_records.get(task_id)
            if record is None:
                self._write_state_failure_report(f"queue record {task_id} has no task run record")
                raise StateExecutionRefused("state queue is incomplete")
            if record.status is not TaskStatus.QUEUED:
                continue
            record.status = TaskStatus.IN_PROGRESS
            record.started_at = self._timestamp()
            state.active_task_id = task_id
            state.updated_at = self._timestamp()
            self.store.commit(state)
            if on_selected is not None:
                on_selected(queued.task)
            return queued.task
        raise StateExecutionRefused("no queued task is available")

    def complete(self, *, task_id: TaskId, validation_results: list[dict[str, Any]]) -> None:
        """Mark the active task complete only with persisted zero-exit validation artifacts."""
        if not validation_results:
            raise ValueError("validation results are required before completion")
        artifact_paths: list[str] = []
        for result in validation_results:
            if result.get("exit_code") != 0 or not isinstance(result.get("artifact_path"), str):
                raise ValueError("validation requires zero-exit artifact paths")
            artifact_path = result["artifact_path"]
            if not artifact_path.startswith("local-ai/") or ".." in artifact_path.split("/"):
                raise ValueError("validation artifact path must be workspace-local")
            artifact_paths.append(artifact_path)

        state, record = self._active_record(task_id)
        record.status = TaskStatus.COMPLETED
        record.validation_artifact_paths = artifact_paths
        record.completed_at = self._timestamp()
        state.active_task_id = None
        state.updated_at = self._timestamp()
        self.store.commit(state)

    def record_validation_failure(
        self, *, task_id: TaskId, command: str, stdout: str, stderr: str, exit_code: int, artifact_path: str
    ) -> ErrorModeContext:
        """Persist Error mode and its exact nonzero validation evidence."""
        if exit_code == 0:
            raise ValueError("only nonzero validation failures select Error mode")
        if not artifact_path.startswith("local-ai/") or ".." in artifact_path.split("/"):
            raise ValueError("validation artifact path must be workspace-local")
        state, record = self._active_record(task_id)
        record.mode_history.append(ExecutionMode.ERROR)
        record.validation_artifact_paths.append(artifact_path)
        self._validation_failures.setdefault(str(task_id), []).append(
            {
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
                "artifact_path": artifact_path,
            }
        )
        state.updated_at = self._timestamp()
        self.store.commit(state)
        return ErrorModeContext(ExecutionMode.ERROR, command, stdout, stderr, exit_code, artifact_path)

    def begin_error_mode_request(self, *, task_id: TaskId) -> ErrorModeRequest:
        """Atomically increment the Error request count immediately before a fresh request."""
        state, record = self._active_record(task_id)
        if not record.mode_history or record.mode_history[-1] is not ExecutionMode.ERROR:
            raise ValueError("Error request requires a recorded Error-mode validation failure")
        if record.error_mode_requests >= 3:
            raise StateExecutionRefused("Error-mode request limit reached")
        record.error_mode_requests += 1
        state.updated_at = self._timestamp()
        self.store.commit(state)
        return ErrorModeRequest(ExecutionMode.ERROR, record.error_mode_requests)

    def record_error_mode_request(self, *, task_id: TaskId, validation_results: list[dict[str, Any]]) -> ErrorModeRequest:
        """Record a failed validation attempt and reserve its next Error-mode request."""
        if not validation_results:
            raise ValueError("validation results are required")
        failed = next((result for result in validation_results if result.get("exit_code") != 0), None)
        if failed is None:
            raise ValueError("Error-mode recovery requires a nonzero validation result")
        self.record_validation_failure(
            task_id=task_id,
            command=str(failed.get("command", "")),
            stdout=str(failed.get("stdout", "")),
            stderr=str(failed.get("stderr", "")),
            exit_code=int(failed["exit_code"]),
            artifact_path=str(failed.get("artifact_path", "")),
        )
        return self.begin_error_mode_request(task_id=task_id)

    def quarantine_after_retry_limit(self, *, task_id: TaskId, changed_workspace_paths: list[str]) -> Path:
        """Quarantine after exactly three Error requests without rolling back workspace edits."""
        state, record = self._active_record(task_id)
        if record.error_mode_requests < 3:
            raise ValueError("task has not reached the Error-mode retry limit")
        task = next((entry.task for entry in state.queue if entry.task.id == task_id), None)
        if task is None:
            raise StateExecutionRefused("active task is absent from the durable queue")
        record.changed_workspace_paths = list(changed_workspace_paths)
        report_path = write_validation_failure_quarantine_report(
            workspace=self.store.workspace,
            task_id=task_id,
            mode_history=record.mode_history,
            validation_artifact_paths=record.validation_artifact_paths,
            changed_workspace_paths=record.changed_workspace_paths,
            retry_count=record.error_mode_requests,
            validation_evidence=self._validation_failures.get(str(task_id)),
        )
        record.status = TaskStatus.QUARANTINED
        record.quarantine_report_path = report_path.relative_to(self.store.workspace).as_posix()
        state.active_task_id = None
        state.updated_at = self._timestamp()
        self.store.commit(state)
        return report_path

    def regenerate_progress_tracker(self):
        """Write a derived, non-authoritative human-readable queue projection."""
        state = self._load_or_refuse()
        target = self.store.state_directory / "progress-tracker.md"
        lines = ["# Orchestrator Progress Tracker", "", "This projection is not scheduling authority.", ""]
        for queued in state.queue:
            task_id = str(queued.task.id)
            record = state.task_records[task_id]
            marker = " ← active" if state.active_task_id == task_id else ""
            lines.append(f"- `{task_id}` — {record.status.value}{marker}")
        self.store._atomic_write_bytes(target, ("\n".join(lines) + "\n").encode("utf-8"))
        return target
