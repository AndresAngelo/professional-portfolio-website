"""Strict executor-output parsing and invalid-protocol quarantine handling."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from .models import ToolOperation


class ProtocolValidationError(ValueError):
    """Raised when executor output does not exactly satisfy Tool Protocol v1.0."""


_ALLOWED_FIELDS = {
    "protocol_version",
    "task_id",
    "target_path",
    "action",
    "arguments",
    "expected_result",
}
_ACTIONS = {"mkdir", "write_file", "patch_file", "delete_file"}
_TASK_ID = re.compile(r"^M[1-9][0-9]*\.G[1-9][0-9]*\.T[1-9][0-9]*$")


class _ToolExecutor(Protocol):
    def execute(self, operation: ToolOperation) -> object: ...


@dataclass(frozen=True)
class ProtocolQuarantineResult:
    """Evidence emitted when an executor response cannot safely reach tools."""

    status: str
    report_path: Path
    parse_error: str


@dataclass(frozen=True)
class ProtocolValidator:
    """Parse exactly one versioned JSON protocol object for one active task."""

    active_task_id: str

    def parse(self, response_text: str) -> ToolOperation:
        try:
            document = json.loads(response_text)
        except (TypeError, json.JSONDecodeError) as error:
            raise ProtocolValidationError("response is not valid JSON") from error
        if not isinstance(document, dict):
            raise ProtocolValidationError("response must be a JSON object")
        unknown = set(document).difference(_ALLOWED_FIELDS)
        if unknown:
            raise ProtocolValidationError("unknown top-level field")
        missing = _ALLOWED_FIELDS.difference(document)
        if missing:
            raise ProtocolValidationError("required field is missing")
        if document["protocol_version"] != "1.0":
            raise ProtocolValidationError("unsupported protocol version")
        task_id = document["task_id"]
        if not isinstance(task_id, str) or not _TASK_ID.fullmatch(task_id):
            raise ProtocolValidationError("invalid task identifier")
        if task_id != self.active_task_id:
            raise ProtocolValidationError("task identifier does not match active task")
        target_path = document["target_path"]
        if not isinstance(target_path, str) or not target_path:
            raise ProtocolValidationError("target_path must be a non-empty string")
        action = document["action"]
        if action not in _ACTIONS:
            raise ProtocolValidationError("unsupported action")
        arguments = document["arguments"]
        if not isinstance(arguments, dict):
            raise ProtocolValidationError("arguments must be an object")
        expected_result = document["expected_result"]
        if not isinstance(expected_result, str) or not expected_result:
            raise ProtocolValidationError("expected_result must be a non-empty string")
        return ToolOperation(
            protocol_version="1.0",
            task_id=task_id,
            target_path=target_path,
            action=action,
            arguments=arguments,
            expected_result=expected_result,
        )


def parse_tool_operation(document: dict[str, Any], *, active_task_id: str) -> ToolOperation:
    """Validate an already-decoded protocol document through the same strict parser."""
    if not isinstance(document, dict):
        raise ProtocolValidationError("response must be a JSON object")
    return ProtocolValidator(active_task_id=active_task_id).parse(json.dumps(document, separators=(",", ":")))


@dataclass
class ProtocolProcessor:
    """Gate model output so invalid text cannot invoke filesystem operations."""

    workspace: Path
    active_task_state: Any
    tool_executor: _ToolExecutor

    def process_executor_output(self, response_text: str) -> object:
        """Dispatch valid output or quarantine invalid output without changing task state."""
        active_task_id = getattr(self.active_task_state, "active_task_id", None)
        if not isinstance(active_task_id, str) or not active_task_id:
            raise ProtocolValidationError("active task state has no task identifier")
        try:
            operation = ProtocolValidator(active_task_id=active_task_id).parse(response_text)
        except ProtocolValidationError as error:
            return self._quarantine(response_text=response_text, parse_error=str(error))
        return self.tool_executor.execute(operation)

    def _quarantine(self, *, response_text: str, parse_error: str) -> ProtocolQuarantineResult:
        root = self.workspace.resolve()
        quarantine = root / "local-ai" / "quarantine"
        quarantine.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        report_path = quarantine / f"{timestamp}-invalid-protocol.md"
        report_path.write_text(
            "# Quarantine: invalid Tool Protocol output\n\n"
            "- **Category:** invalid-protocol-output\n"
            f"- **Recorded:** `{datetime.now(UTC).isoformat()}`\n"
            f"- **Parse error:** {parse_error}\n"
            "- **Recovery:** workspace changes preserved; active task remains in progress\n\n"
            "## Executor response\n\n```text\n"
            f"{response_text}\n```\n",
            encoding="utf-8",
        )
        return ProtocolQuarantineResult(status="quarantined", report_path=report_path, parse_error=parse_error)
