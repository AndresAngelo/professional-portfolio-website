"""Error history contracts: every nonzero validation result is kept, and only granted failures count."""

from __future__ import annotations

from pathlib import Path

import pytest

from orchestrator.models import ExecutionMode, TaskRunRecord
from orchestrator.scheduler import ERROR_MODE_LIMIT, Scheduler, StateExecutionRefused
from orchestrator.state_store import AtomicStateStore

from test_state_scheduler import SCHEMA_VERSION, WORKSPACE_ID, make_state


def _active_scheduler(workspace: Path):
    store = AtomicStateStore(workspace=workspace, workspace_id=WORKSPACE_ID, schema_version=SCHEMA_VERSION)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    task = scheduler.select_next()
    return scheduler, store, task


def _record_failure(scheduler: Scheduler, task, attempt: int) -> None:
    scheduler.record_validation_failure(
        task_id=task.id,
        command="python -m pytest local-ai/tests/test_example.py -q",
        stdout=f"stdout {attempt}",
        stderr=f"stderr {attempt}",
        exit_code=1,
        artifact_path=f"local-ai/validation/{task.id}/{attempt:03d}.json",
    )


def test_granted_failures_are_recorded_with_their_request_numbers(workspace: Path) -> None:
    """Each failure that earns a request is kept with its request number and disposition."""
    scheduler, store, task = _active_scheduler(workspace)
    for attempt in range(1, ERROR_MODE_LIMIT + 1):
        _record_failure(scheduler, task, attempt)
        scheduler.begin_error_mode_request(task_id=task.id)

    record = store.load().task_records[str(task.id)]
    assert [entry.attempt for entry in record.error_history] == [1, 2, 3]
    assert [entry.disposition for entry in record.error_history] == ["error_request_granted"] * 3
    assert [entry.error_mode_request_number for entry in record.error_history] == [1, 2, 3]
    assert record.mode_history == [ExecutionMode.ERROR] * ERROR_MODE_LIMIT


def test_refused_failure_is_kept_as_evidence_without_counting_a_request(workspace: Path) -> None:
    """A fourth failure is recorded as refused, leaves mode_history unchanged, and grants no request."""
    scheduler, store, task = _active_scheduler(workspace)
    for attempt in range(1, ERROR_MODE_LIMIT + 1):
        _record_failure(scheduler, task, attempt)
        scheduler.begin_error_mode_request(task_id=task.id)

    _record_failure(scheduler, task, ERROR_MODE_LIMIT + 1)

    record = store.load().task_records[str(task.id)]
    refused = record.error_history[-1]
    assert record.error_mode_requests == ERROR_MODE_LIMIT
    assert record.mode_history == [ExecutionMode.ERROR] * ERROR_MODE_LIMIT
    assert refused.disposition == "refused_retry_limit"
    assert refused.error_mode_request_number is None
    assert refused.artifact_path.endswith("004.json")
    with pytest.raises(StateExecutionRefused, match="limit"):
        scheduler.begin_error_mode_request(task_id=task.id)


def test_request_without_a_granted_failure_is_refused(workspace: Path) -> None:
    """An Error-mode request cannot be counted unless a granted failure is waiting for it."""
    scheduler, store, task = _active_scheduler(workspace)

    with pytest.raises(ValueError, match="granted"):
        scheduler.begin_error_mode_request(task_id=task.id)
    assert store.load().task_records[str(task.id)].error_mode_requests == 0


def test_error_history_round_trips_and_defaults_for_records_written_before_it_existed(workspace: Path) -> None:
    """The history survives a reload, and older run-state records without the field still load."""
    scheduler, store, task = _active_scheduler(workspace)
    _record_failure(scheduler, task, 1)
    scheduler.begin_error_mode_request(task_id=task.id)

    reloaded = store.load().task_records[str(task.id)]
    assert reloaded.error_history[0].disposition == "error_request_granted"
    assert reloaded.error_history[0].exit_code == 1

    legacy = reloaded.to_dict()
    legacy.pop("error_history")
    assert TaskRunRecord.from_dict(legacy).error_history == []
