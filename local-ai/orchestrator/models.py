"""Typed, JSON-safe domain records for the workspace-local orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal


class TaskStatus(StrEnum):
    """Durable lifecycle states for a queued task."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    QUARANTINED = "quarantined"


class ExecutionMode(StrEnum):
    """Observed execution classifications; models never choose these."""

    SCAFFOLD = "Scaffold"
    ALIGNER = "Aligner"
    COT_TASK = "CoT-Task"
    ERROR = "Error"


@dataclass(frozen=True, order=True)
class TaskId:
    milestone: int
    goal: int
    task: int

    def __post_init__(self) -> None:
        if min(self.milestone, self.goal, self.task) < 1:
            raise ValueError("TaskId coordinates must be positive")

    def __str__(self) -> str:
        return f"M{self.milestone}.G{self.goal}.T{self.task}"

    @classmethod
    def from_string(cls, value: str) -> TaskId:
        import re

        match = re.fullmatch(r"M(\d+)\.G(\d+)\.T(\d+)", value)
        if match is None:
            raise ValueError(f"Invalid task identifier: {value!r}")
        return cls(*(int(part) for part in match.groups()))

    def to_dict(self) -> dict[str, int]:
        return {"milestone": self.milestone, "goal": self.goal, "task": self.task}


@dataclass(frozen=True)
class DeclaredCommand:
    raw_text: str
    canonical_text: str
    ordinal: int

    def to_dict(self) -> dict[str, object]:
        return {"raw_text": self.raw_text, "canonical_text": self.canonical_text, "ordinal": self.ordinal}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> DeclaredCommand:
        return cls(str(value["raw_text"]), str(value["canonical_text"]), int(value["ordinal"]))


@dataclass(frozen=True)
class GoalTask:
    id: TaskId
    source_path: str
    source_hash: str
    heading: str
    objective: str
    acceptance_criteria: tuple[str, ...]
    prerequisites: tuple[str, ...]
    implementation_details: str
    validation_commands: tuple[DeclaredCommand, ...]
    active_target_hints: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "id": str(self.id), "source_path": self.source_path, "source_hash": self.source_hash,
            "heading": self.heading, "objective": self.objective,
            "acceptance_criteria": list(self.acceptance_criteria), "prerequisites": list(self.prerequisites),
            "implementation_details": self.implementation_details,
            "validation_commands": [command.to_dict() for command in self.validation_commands],
            "active_target_hints": list(self.active_target_hints),
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> GoalTask:
        return cls(
            id=TaskId.from_string(str(value["id"])), source_path=str(value["source_path"]),
            source_hash=str(value["source_hash"]), heading=str(value["heading"]),
            objective=str(value["objective"]),
            acceptance_criteria=tuple(str(item) for item in value["acceptance_criteria"]),
            prerequisites=tuple(str(item) for item in value["prerequisites"]),
            implementation_details=str(value["implementation_details"]),
            validation_commands=tuple(DeclaredCommand.from_dict(item) for item in value["validation_commands"]),
            active_target_hints=tuple(str(item) for item in value["active_target_hints"]),
        )


@dataclass(frozen=True)
class TaskQueueRecord:
    task: GoalTask
    ordinal: int

    def to_dict(self) -> dict[str, object]:
        return {"task": self.task.to_dict(), "ordinal": self.ordinal}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> TaskQueueRecord:
        return cls(task=GoalTask.from_dict(value["task"]), ordinal=int(value["ordinal"]))


ErrorHistoryDisposition = Literal["error_request_granted", "refused_retry_limit"]


@dataclass(frozen=True)
class ErrorHistoryEntry:
    """One nonzero validation result on the active task and the scheduler's decision about it.

    ``error_request_granted`` entries earned an Error-mode request and appear in ``mode_history``.
    ``refused_retry_limit`` entries were kept as evidence, but no Error-mode request was made.
    """

    attempt: int
    command: str
    exit_code: int
    artifact_path: str
    disposition: ErrorHistoryDisposition
    error_mode_request_number: int | None
    recorded_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "attempt": self.attempt, "command": self.command, "exit_code": self.exit_code,
            "artifact_path": self.artifact_path, "disposition": self.disposition,
            "error_mode_request_number": self.error_mode_request_number, "recorded_at": self.recorded_at,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ErrorHistoryEntry:
        disposition = str(value["disposition"])
        if disposition not in {"error_request_granted", "refused_retry_limit"}:
            raise ValueError(f"unknown error history disposition: {disposition}")
        request_number = value.get("error_mode_request_number")
        return cls(
            attempt=int(value["attempt"]),
            command=str(value["command"]),
            exit_code=int(value["exit_code"]),
            artifact_path=str(value["artifact_path"]),
            disposition=disposition,  # type: ignore[arg-type]
            error_mode_request_number=None if request_number is None else int(request_number),
            recorded_at=str(value["recorded_at"]),
        )


MODEL_TURN_PASSES = frozenset({"embedding", "router", "executor", "auditor"})
MODEL_TURN_ROLES = frozenset({"embedding", "router", "executor"})
MODEL_TURN_OUTCOMES = frozenset(
    {"accepted", "schema_rejected", "transport_failed", "validation_failed", "audit_rejected"}
)


@dataclass(frozen=True)
class ModelTurn:
    """One model request made for a task, with the exact model identifier that served it.

    Turns are provenance only. Scheduling never reads them, so a turn cannot change task state.
    """

    turn_id: int
    pass_name: str
    role: str
    model_id: str
    attempt: int
    mode: str | None
    request_id: str
    timestamp: str
    outcome: str

    def __post_init__(self) -> None:
        if self.turn_id < 1 or self.attempt < 1:
            raise ValueError("turn_id and attempt must be positive")
        if self.pass_name not in MODEL_TURN_PASSES:
            raise ValueError(f"unknown model turn pass: {self.pass_name}")
        if self.role not in MODEL_TURN_ROLES:
            raise ValueError(f"unknown model turn role: {self.role}")
        if self.outcome not in MODEL_TURN_OUTCOMES:
            raise ValueError(f"unknown model turn outcome: {self.outcome}")
        if not self.model_id or not self.request_id:
            raise ValueError("model turns need a model identifier and a request identifier")

    def to_dict(self) -> dict[str, object]:
        return {
            "turn_id": self.turn_id, "pass_name": self.pass_name, "role": self.role,
            "model_id": self.model_id, "attempt": self.attempt, "mode": self.mode,
            "request_id": self.request_id, "timestamp": self.timestamp, "outcome": self.outcome,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ModelTurn:
        mode = value.get("mode")
        return cls(
            turn_id=int(value["turn_id"]),
            pass_name=str(value["pass_name"]),
            role=str(value["role"]),
            model_id=str(value["model_id"]),
            attempt=int(value["attempt"]),
            mode=None if mode is None else str(mode),
            request_id=str(value["request_id"]),
            timestamp=str(value["timestamp"]),
            outcome=str(value["outcome"]),
        )


@dataclass
class TaskRunRecord:
    task_id: TaskId
    status: TaskStatus
    mode_history: list[ExecutionMode] = field(default_factory=list)
    error_mode_requests: int = 0
    started_at: str | None = None
    completed_at: str | None = None
    request_ids: list[str] = field(default_factory=list)
    validation_artifact_paths: list[str] = field(default_factory=list)
    changed_workspace_paths: list[str] = field(default_factory=list)
    quarantine_report_path: str | None = None
    error_history: list[ErrorHistoryEntry] = field(default_factory=list)
    model_turns: list[ModelTurn] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "task_id": str(self.task_id), "status": self.status.value,
            "mode_history": [mode.value for mode in self.mode_history],
            "error_mode_requests": self.error_mode_requests, "started_at": self.started_at,
            "completed_at": self.completed_at, "request_ids": self.request_ids,
            "validation_artifact_paths": self.validation_artifact_paths,
            "changed_workspace_paths": self.changed_workspace_paths,
            "quarantine_report_path": self.quarantine_report_path,
            "error_history": [entry.to_dict() for entry in self.error_history],
            "model_turns": [turn.to_dict() for turn in self.model_turns],
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> TaskRunRecord:
        return cls(
            task_id=TaskId.from_string(str(value["task_id"])), status=TaskStatus(str(value["status"])),
            mode_history=[ExecutionMode(str(mode)) for mode in value.get("mode_history", [])],
            error_mode_requests=int(value.get("error_mode_requests", 0)), started_at=value.get("started_at"),
            completed_at=value.get("completed_at"),
            request_ids=[str(item) for item in value.get("request_ids", [])]
            + ([str(value["planner_request_id"])] if value.get("planner_request_id") else [])
            + [str(item) for item in value.get("executor_request_ids", [])],
            validation_artifact_paths=[str(item) for item in value.get("validation_artifact_paths", [])],
            changed_workspace_paths=[str(item) for item in value.get("changed_workspace_paths", [])],
            quarantine_report_path=value.get("quarantine_report_path"),
            error_history=[ErrorHistoryEntry.from_dict(item) for item in value.get("error_history", [])],
            model_turns=[ModelTurn.from_dict(item) for item in value.get("model_turns", [])],
        )


@dataclass
class RunState:
    schema_version: int
    workspace_id: str
    queue: list[TaskQueueRecord]
    task_records: dict[str, TaskRunRecord]
    active_task_id: str | None
    updated_at: str

    def to_dict(self) -> dict[str, object]:
        return {"schema_version": self.schema_version, "workspace_id": self.workspace_id,
                "queue": [record.to_dict() for record in self.queue],
                "task_records": {key: record.to_dict() for key, record in self.task_records.items()},
                "active_task_id": self.active_task_id, "updated_at": self.updated_at}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> RunState:
        return cls(schema_version=int(value["schema_version"]), workspace_id=str(value["workspace_id"]),
                   queue=[TaskQueueRecord.from_dict(item) for item in value["queue"]],
                   task_records={str(key): TaskRunRecord.from_dict(item) for key, item in value["task_records"].items()},
                   active_task_id=value.get("active_task_id"), updated_at=str(value["updated_at"]))


@dataclass(frozen=True)
class ToolOperation:
    protocol_version: Literal["1.0"]
    task_id: str
    target_path: str
    action: Literal["mkdir", "write_file", "patch_file", "delete_file"]
    arguments: dict[str, Any]
    expected_result: str

    def to_dict(self) -> dict[str, object]:
        return {"protocol_version": self.protocol_version, "task_id": self.task_id,
                "target_path": self.target_path, "action": self.action, "arguments": self.arguments,
                "expected_result": self.expected_result}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ToolOperation:
        action = str(value["action"])
        if action not in {"mkdir", "write_file", "patch_file", "delete_file"}:
            raise ValueError(f"Unsupported tool action: {action}")
        version = str(value["protocol_version"])
        if version != "1.0":
            raise ValueError(f"Unsupported protocol version: {version}")
        return cls(protocol_version="1.0", task_id=str(value["task_id"]), target_path=str(value["target_path"]),
                   action=action, arguments=dict(value["arguments"]), expected_result=str(value["expected_result"]))


@dataclass(frozen=True)
class ToolResult:
    task_id: str
    action: str
    resolved_path: str
    status: Literal["completed", "rejected", "failed"]
    timestamp: str
    error_details: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {"task_id": self.task_id, "action": self.action, "resolved_path": self.resolved_path,
                "status": self.status, "timestamp": self.timestamp, "error_details": self.error_details}
