"""Pydantic contracts for the JSON replies that the local router and auditor must produce.

The schemas are sent to LM Studio as ``json_schema`` constraints and are checked again here
after the reply arrives. Patterns are checked in Python rather than in the schema, because
constrained decoding supports a narrower set of JSON Schema keywords.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_TASK_ID = re.compile(r"M\d+\.G\d+\.T\d+")


def _check_task_id(value: str) -> str:
    if not _TASK_ID.fullmatch(value):
        raise ValueError("task_id must look like M5.G1.T1")
    return value


class RouterPlan(BaseModel):
    """Pass 2 reply: sanitized constraints and the context the executor may use."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    sanitized_constraints: list[str] = Field(min_length=1, max_length=20)
    target_paths: list[str] = Field(max_length=8)
    context_chunk_ids: list[str] = Field(max_length=10)

    @field_validator("task_id")
    @classmethod
    def _task_id(cls, value: str) -> str:
        return _check_task_id(value)


class AuditViolation(BaseModel):
    """One rule the auditor found broken, with the evidence that shows it."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, max_length=80)
    file_path: str = Field(max_length=260)
    evidence: str = Field(max_length=500)


class AuditReport(BaseModel):
    """Pass 4 reply: a verdict against the TRD rules, with evidence for every failure."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    verdict: Literal["pass", "fail"]
    violations: list[AuditViolation] = Field(max_length=20)

    @field_validator("task_id")
    @classmethod
    def _task_id(cls, value: str) -> str:
        return _check_task_id(value)

    @model_validator(mode="after")
    def _verdict_matches_violations(self) -> AuditReport:
        if self.verdict == "pass" and self.violations:
            raise ValueError("a pass verdict cannot list violations")
        if self.verdict == "fail" and not self.violations:
            raise ValueError("a fail verdict must list at least one violation")
        return self


# Executor reply schema sent as a json_schema constraint. Written by hand, without $ref or pattern, because
# constrained decoding supports a narrower set of keywords. ProtocolValidator still validates the reply.
TOOL_PROTOCOL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["protocol_version", "task_id", "target_path", "action", "arguments", "expected_result"],
    "properties": {
        "protocol_version": {"type": "string", "enum": ["1.0"]},
        "task_id": {"type": "string"},
        "target_path": {"type": "string"},
        "action": {"type": "string", "enum": ["mkdir", "write_file", "patch_file", "delete_file"]},
        "arguments": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "content": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
        },
        "expected_result": {"type": "string"},
    },
}
