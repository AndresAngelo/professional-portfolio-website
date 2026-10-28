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

    def to_dict(self) -> dict[str, object]:
        return {
            "task_id": str(self.task_id), "status": self.status.value,
            "mode_history": [mode.value for mode in self.mode_history],
            "error_mode_requests": self.error_mode_requests, "started_at": self.started_at,
            "completed_at": self.completed_at, "request_ids": self.request_ids,
            "validation_artifact_paths": self.validation_artifact_paths,
            "changed_workspace_paths": self.changed_workspace_paths,
            "quarantine_report_path": self.quarantine_report_path,
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
