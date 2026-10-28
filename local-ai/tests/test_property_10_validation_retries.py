"""Property contract for ordered validation and bounded Error-mode recovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hypothesis import given, settings, strategies as st

from orchestrator.models import DeclaredCommand, GoalTask, RunState, TaskId, TaskQueueRecord, TaskRunRecord, TaskStatus
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore


# Feature: stateless-turn-python-orchestrator-pipeline, Property 10: Ordered validation and bounded error recovery
# Validates: Requirements 8.1, 8.2, 8.3
_COMMAND_COUNT = st.integers(min_value=1, max_value=5)
# A False result represents a failed validation attempt.  The final True, when
# present, represents successful validation after the given number of Error requests.
_RETRY_OUTCOMES = st.one_of(
    st.lists(st.just(False), min_size=3, max_size=8),
    st.lists(st.just(False), min_size=0, max_size=2).map(lambda failures: [*failures, True]),
)


def _task(command_count: int) -> GoalTask:
    task_id = TaskId(5, 1, 10)
    commands = tuple(
        DeclaredCommand(
            raw_text=f"python -m pytest local-ai/tests/command-{ordinal}.py -q",
            canonical_text=f"python -m pytest local-ai/tests/command-{ordinal}.py -q",
            ordinal=ordinal,
        )
        for ordinal in range(1, command_count + 1)
    )
    return GoalTask(
        id=task_id,
        source_path=".kiro/specs/m5-generated/goals/goal10.md",
        source_hash="generated-source",
        heading="Generated retry task",
        objective="Validate bounded Error-mode recovery.",
        acceptance_criteria=("Validation is ordered.",),
        prerequisites=(),
        implementation_details="Generated for Property 10.",
        validation_commands=commands,
        active_target_hints=("local-ai/orchestrator/validation.py",),
    )


def _active_scheduler(tmp_path: Path, task: GoalTask) -> tuple[Scheduler, AtomicStateStore]:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    record = TaskRunRecord(task_id=task.id, status=TaskStatus.QUEUED)
    state = RunState(
        schema_version=1,
        workspace_id="property-10-workspace",
        queue=[TaskQueueRecord(task=task, ordinal=0)],
        task_records={str(task.id): record},
        active_task_id=None,
        updated_at="2026-01-01T00:00:00Z",
    )
    store = AtomicStateStore(workspace=workspace, workspace_id="property-10-workspace", schema_version=1)
    store.commit(state)
    scheduler = Scheduler(store)
    assert scheduler.select_next().id == task.id
    return scheduler, store


@settings(max_examples=100, deadline=None)
@given(command_count=_COMMAND_COUNT, outcomes=_RETRY_OUTCOMES)
def test_ordered_validation_and_bounded_error_recovery(
    tmp_path: Path, command_count: int, outcomes: list[bool]
) -> None:
    """Validation retries remain ordered, capped at three, and persist exact success counts."""
    task = _task(command_count)
    scheduler, store = _active_scheduler(tmp_path, task)
    expected_commands = [command.canonical_text for command in task.validation_commands]

    for outcome in outcomes:
        commands_run = expected_commands if outcome else expected_commands[:1]
        validation_results: list[dict[str, Any]] = [
            {
                "command": command,
                "exit_code": 0 if outcome else 1,
                "artifact_path": f"local-ai/validation/{task.id}/attempt-{index}/result.json",
            }
            for index, command in enumerate(commands_run, start=1)
        ]
        assert [result["command"] for result in validation_results] == commands_run

        if outcome:
            scheduler.complete(task_id=task.id, validation_results=validation_results)
            persisted = store.load().task_records[str(task.id)]
            assert persisted.status is TaskStatus.COMPLETED
            assert persisted.error_mode_requests == outcomes.index(True)
            assert [result["command"] for result in validation_results] == expected_commands
            return

        scheduler.record_error_mode_request(task_id=task.id, validation_results=validation_results)
        persisted = store.load().task_records[str(task.id)]
        assert persisted.error_mode_requests <= 3

    persisted = store.load().task_records[str(task.id)]
    assert persisted.error_mode_requests == 3
