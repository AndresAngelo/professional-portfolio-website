"""Property contract for permanent validation-failure preservation."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.models import ExecutionMode, TaskStatus
from orchestrator.quarantine import normalize_markdown_text
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore

from test_state_scheduler import SCHEMA_VERSION, WORKSPACE_ID, make_state


# Feature: stateless-turn-python-orchestrator-pipeline, Property 13: Permanent validation failure preserves changes and evidence
# Validates: Requirements 8.4
_SAFE_SEGMENT = st.from_regex(r"[a-z][a-z0-9_-]{0,12}", fullmatch=True)
_CHANGED_PATH_SETS = st.lists(
    st.tuples(_SAFE_SEGMENT, _SAFE_SEGMENT).map(lambda parts: f"src/{parts[0]}/{parts[1]}.py"),
    min_size=0,
    max_size=5,
    unique=True,
)
_FAILURE_RESULTS = st.lists(
    st.tuples(
        st.integers(min_value=1, max_value=255),
        st.text(min_size=1, max_size=48),
        st.text(min_size=1, max_size=48),
    ),
    min_size=3,
    max_size=6,
)


def _store(workspace: Path) -> AtomicStateStore:
    return AtomicStateStore(
        workspace=workspace,
        workspace_id=WORKSPACE_ID,
        schema_version=SCHEMA_VERSION,
    )


@settings(max_examples=100, deadline=None)
@given(failures=_FAILURE_RESULTS, changed_paths=_CHANGED_PATH_SETS)
def test_permanent_validation_failure_preserves_changes_and_evidence(
    tmp_path_factory: pytest.TempPathFactory, failures: list[tuple[int, str, str]], changed_paths: list[str]
) -> None:
    """Three Error requests quarantine the task without changing its workspace files."""
    workspace = tmp_path_factory.mktemp("permanent-failure")
    (workspace / "local-ai").mkdir()
    snapshots: dict[str, str] = {}
    for index, relative_path in enumerate(changed_paths, start=1):
        target = workspace / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        content = f"PARTIAL_CHANGE_{index} = {index}\n"
        target.write_text(content, encoding="utf-8")
        snapshots[relative_path] = content

    store = _store(workspace)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    task = scheduler.select_next()

    for attempt, (exit_code, stdout, stderr) in enumerate(failures[:3], start=1):
        scheduler.record_validation_failure(
            task_id=task.id,
            command="python -m pytest local-ai/tests/test_example.py -q",
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            artifact_path=f"local-ai/validation/{task.id}/{attempt:03d}.json",
        )
        retry = scheduler.begin_error_mode_request(task_id=task.id)
        assert retry.mode is ExecutionMode.ERROR
        assert retry.request_number == attempt

    report_path = scheduler.quarantine_after_retry_limit(
        task_id=task.id,
        changed_workspace_paths=changed_paths,
    )

    persisted = store.load().task_records[str(task.id)]
    report = report_path.read_text(encoding="utf-8")
    assert persisted.status is TaskStatus.QUARANTINED
    assert persisted.error_mode_requests == 3
    assert persisted.mode_history == [ExecutionMode.ERROR, ExecutionMode.ERROR, ExecutionMode.ERROR]
    assert persisted.changed_workspace_paths == changed_paths
    assert persisted.quarantine_report_path == report_path.relative_to(workspace).as_posix()
    assert all((workspace / path).read_text(encoding="utf-8") == content for path, content in snapshots.items())
    assert str(task.id) in report
    assert "Error → Error → Error" in report
    assert "python -m pytest local-ai/tests/test_example.py -q" in report
    assert "Recovery" in report
    assert "3" in report
    for exit_code, stdout, stderr in failures[:3]:
        assert str(exit_code) in report
        assert normalize_markdown_text(stdout) in report
        assert normalize_markdown_text(stderr) in report
    for changed_path in changed_paths:
        assert changed_path in report
