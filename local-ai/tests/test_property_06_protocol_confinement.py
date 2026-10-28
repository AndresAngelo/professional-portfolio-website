"""Property tests for strict Tool Protocol validation and workspace confinement."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.models import ToolResult
from orchestrator.protocol import ProtocolValidationError, parse_tool_operation
from orchestrator.workspace import WorkspacePathError, resolve_workspace_path


# Feature: stateless-turn-python-orchestrator-pipeline, Property 6: Protocol validation and workspace confinement
# Validates: Requirements 5.1, 5.2, 5.3
_COMPONENT = st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789_-", min_size=1, max_size=12)
_TASK_ID = st.builds(
    lambda milestone, goal, task: f"M{milestone}.G{goal}.T{task}",
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=10),
    st.integers(min_value=1, max_value=99),
)
_SAFE_PATH = st.lists(_COMPONENT, min_size=1, max_size=3).map(lambda parts: "/".join(parts))
_HOSTILE_PATH = st.sampled_from(
    (
        "../outside.txt",
        "nested/../../outside.txt",
        "/absolute/outside.txt",
        r"C:\\outside.txt",
        r"..\\outside.txt",
        "link-outside/escape.txt",
    )
)
_ACTION = st.sampled_from(("mkdir", "write_file", "patch_file"))
_INVALID_VARIANT = st.sampled_from(
    ("unknown_field", "wrong_version", "wrong_task", "unknown_action", "missing_result")
)


def _document(*, task_id: str, target_path: str, action: str, variant: str | None) -> dict[str, Any]:
    document: dict[str, Any] = {
        "protocol_version": "1.0",
        "task_id": task_id,
        "target_path": target_path,
        "action": action,
        "arguments": {},
        "expected_result": "The requested workspace change is complete.",
    }
    if variant == "unknown_field":
        document["untrusted"] = True
    elif variant == "wrong_version":
        document["protocol_version"] = "2.0"
    elif variant == "wrong_task":
        document["task_id"] = "M9.G9.T9"
    elif variant == "unknown_action":
        document["action"] = "run_shell"
    elif variant == "missing_result":
        del document["expected_result"]
    return document


def _is_descendant(path: Path, workspace: Path) -> bool:
    try:
        path.relative_to(workspace)
    except ValueError:
        return False
    return True


@settings(max_examples=100)
@given(
    active_task_id=_TASK_ID,
    target_path=st.one_of(_SAFE_PATH, _HOSTILE_PATH),
    action=_ACTION,
    variant=st.one_of(st.none(), _INVALID_VARIANT),
)
def test_protocol_validation_and_workspace_confinement(
    tmp_path: Path,
    active_task_id: str,
    target_path: str,
    action: str,
    variant: str | None,
) -> None:
    """Only complete active-task documents may resolve to canonical workspace targets."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    link = workspace / "link-outside"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        # Platforms without symlink permission still cover lexical hostile paths.
        pass

    document = _document(
        task_id=active_task_id,
        target_path=target_path,
        action=action,
        variant=variant,
    )
    document_is_valid = variant is None

    if not document_is_valid:
        with pytest.raises(ProtocolValidationError):
            parse_tool_operation(document, active_task_id=active_task_id)
        return

    operation = parse_tool_operation(document, active_task_id=active_task_id)
    try:
        resolved_path = resolve_workspace_path(workspace=workspace, target_path=operation.target_path)
    except WorkspacePathError:
        assert target_path in _HOSTILE_PATH
        return

    canonical_workspace = workspace.resolve()
    assert _is_descendant(resolved_path, canonical_workspace)
    result = ToolResult(
        task_id=operation.task_id,
        action=operation.action,
        resolved_path=resolved_path.relative_to(canonical_workspace).as_posix(),
        status="completed",
        timestamp="2026-01-01T00:00:00Z",
    ).to_dict()
    assert set(result) == {
        "task_id",
        "action",
        "resolved_path",
        "status",
        "timestamp",
        "error_details",
    }
    assert result["task_id"] == active_task_id
    assert result["action"] == action
    assert result["status"] == "completed"
