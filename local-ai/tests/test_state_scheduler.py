"""Test-first examples for atomic run state and durable single-task scheduling.

These examples intentionally define the state_store and scheduler contracts that task 3.3
must implement. They exercise real temporary-workspace files; no model or network service
is contacted.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

import pytest

from orchestrator.models import (
    DeclaredCommand,
    GoalTask,
    RunState,
    TaskId,
    TaskQueueRecord,
    TaskRunRecord,
    TaskStatus,
)
from orchestrator.scheduler import Scheduler, StateExecutionRefused
from orchestrator.state_store import AtomicStateStore, StateLoadError, WorkspaceLockedError


WORKSPACE_ID = "test-workspace-v1"
SCHEMA_VERSION = 1


def make_task(*, task: int) -> GoalTask:
    """Build the smallest valid queued task used by scheduler examples."""
    task_id = TaskId(milestone=1, goal=1, task=task)
    return GoalTask(
        id=task_id,
        source_path=".kiro/specs/m1-example/goals/goal1.md",
        source_hash=f"source-{task}",
        heading=f"Task {task}",
        objective="Exercise durable scheduler behavior.",
        acceptance_criteria=("The state remains durable.",),
        prerequisites=(),
        implementation_details="Use the state store.",
        validation_commands=(
            DeclaredCommand(
                raw_text="python -m pytest local-ai/tests/test_state_scheduler.py -q",
                canonical_text="python -m pytest local-ai/tests/test_state_scheduler.py -q",
                ordinal=1,
            ),
        ),
        active_target_hints=("local-ai/orchestrator/scheduler.py",),
    )


def make_state(*, queued_task_numbers: tuple[int, ...] = (1, 2)) -> RunState:
    """Build a valid state with only queued task records."""
    queue = [
        TaskQueueRecord(task=make_task(task=number), ordinal=index)
        for index, number in enumerate(queued_task_numbers)
    ]
    return RunState(
        schema_version=SCHEMA_VERSION,
        workspace_id=WORKSPACE_ID,
        queue=queue,
        task_records={
            str(record.task.id): TaskRunRecord(
                task_id=record.task.id,
                status=TaskStatus.QUEUED,
            )
            for record in queue
        },
        active_task_id=None,
        updated_at="2026-01-01T00:00:00Z",
    )


def build_store(workspace: Path) -> AtomicStateStore:
    """Create the required workspace-contained atomic state store."""
    return AtomicStateStore(
        workspace=workspace,
        workspace_id=WORKSPACE_ID,
        schema_version=SCHEMA_VERSION,
    )


def test_commit_flushes_same_directory_temp_file_replaces_primary_and_keeps_backup(
    workspace: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A commit is durable only after flush, same-directory replace, and backup retention."""
    store = build_store(workspace)
    store.commit(make_state())

    calls: list[tuple[str, Path]] = []
    original_fsync = os.fsync
    original_replace = os.replace

    def record_fsync(file_descriptor: int) -> None:
        calls.append(("fsync", Path(str(file_descriptor))))
        original_fsync(file_descriptor)

    def record_replace(source: os.PathLike[str], destination: os.PathLike[str]) -> None:
        calls.append(("replace", Path(destination)))
        assert Path(source).parent == Path(destination).parent
        original_replace(source, destination)

    monkeypatch.setattr(os, "fsync", record_fsync)
    monkeypatch.setattr(os, "replace", record_replace)

    next_state = make_state(queued_task_numbers=(3,))
    store.commit(next_state)

    state_path = workspace / "local-ai" / "program-states" / "run-state.json"
    backup_path = workspace / "local-ai" / "program-states" / "run-state.previous.json"
    assert any(kind == "fsync" for kind, _ in calls)
    assert ("replace", state_path) in calls
    assert json.loads(state_path.read_text(encoding="utf-8")) == next_state.to_dict()
    assert json.loads(backup_path.read_text(encoding="utf-8")) == make_state().to_dict()


def test_load_rejects_wrong_workspace_or_schema_before_returning_state(workspace: Path) -> None:
    """State from another workspace or schema is never accepted as scheduling authority."""
    store = build_store(workspace)
    state_path = workspace / "local-ai" / "program-states" / "run-state.json"
    state_path.parent.mkdir(parents=True)

    wrong_workspace = make_state().to_dict()
    wrong_workspace["workspace_id"] = "another-workspace"
    state_path.write_text(json.dumps(wrong_workspace), encoding="utf-8")
    with pytest.raises(StateLoadError, match="workspace"):
        store.load()

    wrong_schema = make_state().to_dict()
    wrong_schema["schema_version"] = SCHEMA_VERSION + 1
    state_path.write_text(json.dumps(wrong_schema), encoding="utf-8")
    with pytest.raises(StateLoadError, match="schema"):
        store.load()


def test_workspace_lock_refuses_parallel_owner_and_recovers_only_stale_lock_with_evidence(
    workspace: Path,
) -> None:
    """A live lock prevents parallel scheduling; stale recovery writes local evidence."""
    first_store = build_store(workspace)
    second_store = build_store(workspace)

    first_store.acquire_lock()
    with pytest.raises(WorkspaceLockedError):
        second_store.acquire_lock()
    first_store.release_lock()

    lock_path = workspace / "local-ai" / "program-states" / "scheduler.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text('{"owner":"dead-process","created_at":"2025-01-01T00:00:00Z"}', encoding="utf-8")

    second_store.acquire_lock(recover_stale=True)
    recovery_reports = list((workspace / "local-ai" / "quarantine").glob("*stale-lock*.md"))
    assert recovery_reports, "stale-lock recovery must leave local audit evidence"
    assert "dead-process" in recovery_reports[0].read_text(encoding="utf-8")
    second_store.release_lock()


def test_scheduler_refuses_selection_and_records_report_for_missing_or_corrupt_state(
    workspace: Path,
) -> None:
    """A state failure quarantines evidence and blocks all task execution until recovery."""
    scheduler = Scheduler(build_store(workspace))

    with pytest.raises(StateExecutionRefused, match="state"):
        scheduler.select_next()

    reports = list((workspace / "local-ai" / "quarantine").glob("*state*.md"))
    assert reports
    assert "Run State" in reports[0].read_text(encoding="utf-8")


def test_selection_commits_in_progress_before_any_model_callback(workspace: Path) -> None:
    """The active record must already be durable when planning/execution is allowed to start."""
    store = build_store(workspace)
    store.commit(make_state())
    scheduler = Scheduler(store)
    observed_statuses: list[TaskStatus] = []

    def model_request(task: GoalTask) -> None:
        loaded = store.load()
        assert loaded.active_task_id == str(task.id)
        observed_statuses.append(loaded.task_records[str(task.id)].status)

    selected = scheduler.select_next(on_selected=model_request)

    assert str(selected.id) == "M1.G1.T1"
    assert observed_statuses == [TaskStatus.IN_PROGRESS]


def test_restart_resumes_existing_active_task_before_queued_task(workspace: Path) -> None:
    """Resume always returns the persisted active task rather than advancing the queue."""
    store = build_store(workspace)
    state = make_state()
    active_id = "M1.G1.T2"
    state.active_task_id = active_id
    state.task_records[active_id].status = TaskStatus.IN_PROGRESS
    store.commit(state)

    resumed = Scheduler(store).select_next()

    assert str(resumed.id) == active_id
    reloaded = store.load()
    assert reloaded.active_task_id == active_id
    assert reloaded.task_records["M1.G1.T1"].status is TaskStatus.QUEUED


def test_completion_requires_zero_exit_validation_artifacts_before_persisting_completed(
    workspace: Path,
) -> None:
    """Completion metadata is committed only after persisted artifacts prove zero-exit validation."""
    store = build_store(workspace)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    selected = scheduler.select_next()

    with pytest.raises(ValueError, match="validation"):
        scheduler.complete(task_id=selected.id, validation_results=[])
    assert store.load().task_records[str(selected.id)].status is TaskStatus.IN_PROGRESS

    artifact = "local-ai/validation/M1_G1_T1/attempt-1/result.json"
    scheduler.complete(
        task_id=selected.id,
        validation_results=[{"exit_code": 0, "artifact_path": artifact}],
    )

    completed = store.load().task_records[str(selected.id)]
    assert completed.status is TaskStatus.COMPLETED
    assert completed.validation_artifact_paths == [artifact]
    assert completed.completed_at is not None


def test_progress_tracker_is_an_optional_atomic_projection_never_scheduler_authority(
    workspace: Path,
) -> None:
    """Tracker output may be regenerated, but editing it cannot alter queue selection."""
    store = build_store(workspace)
    store.commit(make_state())
    scheduler = Scheduler(store)

    tracker_path = scheduler.regenerate_progress_tracker()
    assert tracker_path == workspace / "local-ai" / "program-states" / "progress-tracker.md"
    assert "M1.G1.T1" in tracker_path.read_text(encoding="utf-8")

    tracker_path.write_text("# forged tracker\nactive: M1.G1.T2\n", encoding="utf-8")
    selected = scheduler.select_next()

    assert str(selected.id) == "M1.G1.T1"
    assert store.load().active_task_id == "M1.G1.T1"
