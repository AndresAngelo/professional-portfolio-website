"""Property tests for durable single-task scheduler transitions."""

from __future__ import annotations

from pathlib import Path

from hypothesis import given, settings, strategies as st

from orchestrator.models import (
    DeclaredCommand,
    GoalTask,
    RunState,
    TaskId,
    TaskQueueRecord,
    TaskRunRecord,
    TaskStatus,
)
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore


# Feature: stateless-turn-python-orchestrator-pipeline, Property 4: Single active task and restart priority
# Validates: Requirements 3.2, 3.3
_WORKSPACE_ID = "property-scheduler-workspace"
_SCHEMA_VERSION = 1


def _task(number: int) -> GoalTask:
    """Build a minimal valid task with a numerically ordered identifier."""
    task_id = TaskId(milestone=1, goal=1, task=number)
    return GoalTask(
        id=task_id,
        source_path=".kiro/specs/m1-generated/goals/goal1.md",
        source_hash=f"source-{number}",
        heading=f"Generated task {number}",
        objective="Exercise durable scheduling.",
        acceptance_criteria=("Only one task is active.",),
        prerequisites=(),
        implementation_details="Use the scheduler.",
        validation_commands=(
            DeclaredCommand(
                raw_text="python -m pytest local-ai/tests/test_property_04_scheduler.py -q",
                canonical_text="python -m pytest local-ai/tests/test_property_04_scheduler.py -q",
                ordinal=1,
            ),
        ),
        active_target_hints=("local-ai/orchestrator/scheduler.py",),
    )


def _state(queue_size: int) -> RunState:
    """Create a queued-only durable state for one generated queue."""
    queue = [
        TaskQueueRecord(task=_task(number), ordinal=number - 1)
        for number in range(1, queue_size + 1)
    ]
    return RunState(
        schema_version=_SCHEMA_VERSION,
        workspace_id=_WORKSPACE_ID,
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


def _assert_single_active(state: RunState) -> None:
    """The persisted active pointer and record statuses agree exactly."""
    in_progress = [
        task_id
        for task_id, record in state.task_records.items()
        if record.status is TaskStatus.IN_PROGRESS
    ]
    assert len(in_progress) <= 1
    assert in_progress == ([] if state.active_task_id is None else [state.active_task_id])


@settings(max_examples=100, deadline=None)
@given(
    queue_size=st.integers(min_value=1, max_value=20),
    transitions=st.lists(st.booleans(), min_size=1, max_size=80),
)
def test_single_active_task_and_restart_priority(
    tmp_path: Path,
    queue_size: int,
    transitions: list[bool],
) -> None:
    """Every restart resumes durable active work before advancing the queue."""
    workspace = tmp_path / "workspace"
    workspace.mkdir(exist_ok=True)
    store = AtomicStateStore(
        workspace=workspace,
        workspace_id=_WORKSPACE_ID,
        schema_version=_SCHEMA_VERSION,
    )
    store.commit(_state(queue_size))
    scheduler = Scheduler(store)
    active = scheduler.select_next()
    _assert_single_active(store.load())

    for transition_index, restart in enumerate(transitions):
        persisted = store.load()
        _assert_single_active(persisted)

        if restart:
            queued_ids = [
                str(record.task.id)
                for record in persisted.queue
                if persisted.task_records[str(record.task.id)].status is TaskStatus.QUEUED
            ]
            resumed = Scheduler(store).select_next()
            assert resumed.id == active.id
            assert str(resumed.id) not in queued_ids
            _assert_single_active(store.load())
            continue

        scheduler.complete(
            task_id=active.id,
            validation_results=[
                {
                    "exit_code": 0,
                    "artifact_path": (
                        f"local-ai/validation/{active.id}/attempt-{transition_index}/result.json"
                    ),
                }
            ],
        )
        completed_state = store.load()
        _assert_single_active(completed_state)

        queued = [
            record.task
            for record in completed_state.queue
            if completed_state.task_records[str(record.task.id)].status is TaskStatus.QUEUED
        ]
        if not queued:
            return

        active = scheduler.select_next()
        assert active.id == queued[0].id
        _assert_single_active(store.load())
