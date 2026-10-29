"""Property coverage for invalid executor Tool Protocol output."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.protocol import ProtocolProcessor


# Feature: stateless-turn-python-orchestrator-pipeline, Property 7: Invalid protocol safely preserves the task
# Validates: Requirements 5.4
_SAFE_TEXT = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 {}[],:\\\"`~!@#$%^&*()-_=+\\n\\t",
    min_size=0,
    max_size=160,
)
_NON_JSON = _SAFE_TEXT.filter(lambda text: not _is_json_object(text))
_FENCED_OR_PROSE = st.one_of(
    _SAFE_TEXT.map(lambda text: f"```json\\n{text}\\n```"),
    _SAFE_TEXT.map(lambda text: f"Here is the requested action: {text}"),
)
_MALFORMED = st.sampled_from(
    (
        "{",
        "[]",
        "null",
        '{"protocol_version":"1.0"}',
        '{"protocol_version":"1.0","task_id":"M5.G1.T1","target_path":"src/kept.txt"}',
    )
)
_MISMATCHED = st.sampled_from(
    (
        '{"protocol_version":"1.0","task_id":"M5.G1.T2","target_path":"src/kept.txt",'
        '"action":"write_file","arguments":{"content":"unsafe"},"expected_result":"changed"}',
        '{"protocol_version":"2.0","task_id":"M5.G1.T1","target_path":"src/kept.txt",'
        '"action":"write_file","arguments":{"content":"unsafe"},"expected_result":"changed"}',
        '{"protocol_version":"1.0","task_id":"M5.G1.T1","target_path":"src/kept.txt",'
        '"action":"shell","arguments":{},"expected_result":"changed"}',
    )
)
_INVALID_OUTPUTS = st.one_of(_NON_JSON, _FENCED_OR_PROSE, _MALFORMED, _MISMATCHED)


def _is_json_object(text: str) -> bool:
    """Return whether text is a JSON object, excluding valid protocol candidates."""
    import json

    try:
        return isinstance(json.loads(text), dict)
    except json.JSONDecodeError:
        return False


@dataclass
class _ActiveTaskState:
    """Minimal scheduler-owned state supplied to the protocol boundary."""

    active_task_id: str = "M5.G1.T1"
    status: str = "in_progress"


@dataclass
class _RecordingToolExecutor:
    """Fail the property immediately if invalid output reaches a tool operation."""

    calls: list[object] = field(default_factory=list)

    def execute(self, operation: object) -> None:
        self.calls.append(operation)
        raise AssertionError("invalid executor output must never invoke a tool operation")


@settings(max_examples=100, deadline=None)
@given(response_text=_INVALID_OUTPUTS)
def test_invalid_protocol_output_preserves_active_task_and_workspace(
    tmp_path_factory: pytest.TempPathFactory, response_text: str
) -> None:
    """Invalid executor output is quarantined without touching tools, state, or source files."""
    tmp_path = tmp_path_factory.mktemp("invalid-protocol")
    source = tmp_path / "src" / "kept.txt"
    source.parent.mkdir()
    original = "pre-existing workspace change\\n"
    source.write_text(original, encoding="utf-8")
    state = _ActiveTaskState()
    tools = _RecordingToolExecutor()

    result = ProtocolProcessor(
        workspace=tmp_path,
        active_task_state=state,
        tool_executor=tools,
    ).process_executor_output(response_text)

    assert tools.calls == []
    assert state.active_task_id == "M5.G1.T1"
    assert state.status == "in_progress"
    assert source.read_text(encoding="utf-8") == original
    assert result.status == "quarantined"
    assert result.report_path.is_file()
    report = result.report_path.read_text(encoding="utf-8")
    assert response_text in report
    assert result.parse_error in report
