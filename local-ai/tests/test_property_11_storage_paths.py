"""Property tests for workspace-scoped Local AI Storage paths."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.config import derive_artifact_path


# Feature: stateless-turn-python-orchestrator-pipeline, Property 11: All local artifact paths remain workspace-scoped
# Validates: Requirements 9.1
_ARTIFACT_KINDS = st.sampled_from(
    ("state", "plan", "protocol", "telemetry", "validation", "quarantine")
)
_COMPONENT = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_",
    min_size=1,
    max_size=20,
)
_TASK_ID = st.builds(
    lambda milestone, goal, task: f"M{milestone}.G{goal}.T{task}",
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=10),
    st.integers(min_value=1, max_value=99),
)
_HOSTILE_RELATIVE_NAME = st.one_of(
    _COMPONENT.map(lambda component: f"{component}.json"),
    st.sampled_from(
        (
            "../outside.json",
            "nested/../../outside.json",
            "/absolute/outside.json",
            r"C:\\outside.json",
            r"..\\outside.json",
            "./nested/../record.json",
        )
    ),
)


def _is_descendant(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


@settings(max_examples=100)
@given(
    workspace_name=_COMPONENT,
    artifact_kind=_ARTIFACT_KINDS,
    task_id=_TASK_ID,
    relative_name=_HOSTILE_RELATIVE_NAME,
)
def test_all_local_artifact_paths_remain_workspace_scoped(
    tmp_path_factory: pytest.TempPathFactory,
    workspace_name: str,
    artifact_kind: str,
    task_id: str,
    relative_name: str,
) -> None:
    """Every accepted artifact path resolves below the canonical workspace."""
    tmp_path = tmp_path_factory.mktemp("storage-paths")
    workspace = tmp_path / workspace_name
    workspace.mkdir()
    canonical_workspace = workspace.resolve()

    try:
        artifact_path = derive_artifact_path(
            workspace=workspace,
            artifact_kind=artifact_kind,
            task_id=task_id,
            relative_name=relative_name,
        )
    except ValueError:
        return

    assert _is_descendant(artifact_path.resolve(), canonical_workspace)
    assert _is_descendant(artifact_path.resolve(), (canonical_workspace / "local-ai").resolve())
