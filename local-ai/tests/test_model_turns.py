"""Provenance contracts: each model request is recorded with the exact model that served it.

Turns are an audit trail. They must survive a reload, be numbered per task, refuse a reused
request identifier, and leave scheduling untouched. Version 1 state loads under a version 2
store with no turns.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from orchestrator.models import ExecutionMode, ModelTurn, TaskId, TaskStatus
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore

from test_state_scheduler import WORKSPACE_ID, build_store, make_state


def _active_scheduler(workspace: Path, *, queued_task_numbers: tuple[int, ...] = (1,)):
    store = build_store(workspace)
    store.commit(make_state(queued_task_numbers=queued_task_numbers))
    scheduler = Scheduler(store)
    task = scheduler.select_next()
    return scheduler, store, task


def _record(
    scheduler: Scheduler,
    task_id: TaskId,
    *,
    request_id: str,
    pass_name: str = "executor",
    role: str = "executor",
    model_id: str = "gemma-4-e2b-it-qat@q4_k_xl",
    outcome: str = "accepted",
) -> ModelTurn:
    return scheduler.record_model_turn(
        task_id=task_id,
        pass_name=pass_name,
        role=role,
        model_id=model_id,
        attempt=1,
        mode=ExecutionMode.SCAFFOLD.value,
        request_id=request_id,
        outcome=outcome,
    )


def test_turns_survive_reload_with_the_model_identifier_that_served_them(workspace: Path) -> None:
    """Each turn keeps its exact model identifier, its sequence number, and its outcome after a reload."""
    scheduler, store, task = _active_scheduler(workspace)
    router = _record(
        scheduler,
        task.id,
        request_id="req_router",
        pass_name="router",
        role="router",
        model_id="gemma-3-1b-it-qat",
    )
    executor = _record(scheduler, task.id, request_id="req_executor", outcome="validation_failed")

    reloaded = store.load().task_records[str(task.id)]
    assert reloaded.model_turns == [router, executor]
    assert [turn.turn_id for turn in reloaded.model_turns] == [1, 2]
    assert [turn.model_id for turn in reloaded.model_turns] == [
        "gemma-3-1b-it-qat",
        "gemma-4-e2b-it-qat@q4_k_xl",
    ]
    assert reloaded.request_ids == ["req_router", "req_executor"]


def test_turns_never_change_status_mode_history_or_retry_count(workspace: Path) -> None:
    """Recording provenance leaves every scheduling field as it was, even for a failed turn."""
    scheduler, store, task = _active_scheduler(workspace)

    _record(scheduler, task.id, request_id="req_failed", outcome="validation_failed")

    record = store.load().task_records[str(task.id)]
    assert record.status is TaskStatus.IN_PROGRESS
    assert record.mode_history == []
    assert record.error_mode_requests == 0
    assert record.error_history == []


def test_a_reused_request_identifier_is_refused_and_the_ledger_stays_unchanged(workspace: Path) -> None:
    """Each request identifier appears once per task, so one request cannot be recorded twice."""
    scheduler, store, task = _active_scheduler(workspace)
    _record(scheduler, task.id, request_id="req_1")

    with pytest.raises(ValueError, match="unique"):
        _record(scheduler, task.id, request_id="req_1")

    assert len(store.load().task_records[str(task.id)].model_turns) == 1


def test_turns_are_refused_for_any_task_other_than_the_active_one(workspace: Path) -> None:
    """A queued task has no provenance until it becomes the active task."""
    scheduler, store, _ = _active_scheduler(workspace, queued_task_numbers=(1, 2))
    queued_id = TaskId(milestone=1, goal=1, task=2)

    with pytest.raises(ValueError, match="active task"):
        _record(scheduler, queued_id, request_id="req_queued")

    assert store.load().task_records[str(queued_id)].model_turns == []


def test_an_invalid_turn_is_rejected_before_anything_is_written(workspace: Path) -> None:
    """A turn with an unknown pass never reaches the durable ledger."""
    scheduler, store, task = _active_scheduler(workspace)

    with pytest.raises(ValueError, match="pass"):
        _record(scheduler, task.id, request_id="req_bad", pass_name="planner")

    record = store.load().task_records[str(task.id)]
    assert record.model_turns == []
    assert record.request_ids == []


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"pass_name": "planner"}, "pass"),
        ({"role": "auditor"}, "role"),
        ({"outcome": "maybe"}, "outcome"),
        ({"turn_id": 0}, "positive"),
        ({"attempt": 0}, "positive"),
        ({"model_id": ""}, "identifier"),
        ({"request_id": ""}, "identifier"),
    ],
)
def test_model_turn_rejects_unknown_or_incomplete_provenance(overrides: dict[str, Any], message: str) -> None:
    """A turn needs a known pass, role, and outcome, positive numbering, and both identifiers."""
    fields: dict[str, Any] = {
        "turn_id": 1,
        "pass_name": "executor",
        "role": "executor",
        "model_id": "gemma-4-e2b-it-qat@q4_k_xl",
        "attempt": 1,
        "mode": None,
        "request_id": "req_1",
        "timestamp": "2026-01-01T00:00:00Z",
        "outcome": "accepted",
    }
    fields.update(overrides)

    with pytest.raises(ValueError, match=message):
        ModelTurn.from_dict(fields)


def test_version_one_state_loads_under_a_version_two_store_with_no_turns(workspace: Path) -> None:
    """Version 1 state loads as version 2 with empty provenance, and the next commit writes version 2."""
    state_path = workspace / "local-ai" / "program-states" / "run-state.json"
    state_path.parent.mkdir(parents=True)
    legacy = make_state(queued_task_numbers=(1,)).to_dict()
    legacy["schema_version"] = 1
    for record in legacy["task_records"].values():
        record.pop("model_turns")
        record.pop("error_history")
    state_path.write_text(json.dumps(legacy), encoding="utf-8")

    store = AtomicStateStore(workspace=workspace, workspace_id=WORKSPACE_ID, schema_version=2)
    loaded = store.load()
    assert loaded.schema_version == 2
    assert all(record.model_turns == [] for record in loaded.task_records.values())

    store.commit(loaded)
    assert json.loads(state_path.read_text(encoding="utf-8"))["schema_version"] == 2


def test_version_one_state_accepts_provenance_after_migration(workspace: Path) -> None:
    """A migrated queue can start a task and record its first turn as turn 1 under version 2."""
    state_path = workspace / "local-ai" / "program-states" / "run-state.json"
    state_path.parent.mkdir(parents=True)
    legacy = make_state(queued_task_numbers=(1,)).to_dict()
    legacy["schema_version"] = 1
    for record in legacy["task_records"].values():
        record.pop("model_turns")
        record.pop("error_history")
    state_path.write_text(json.dumps(legacy), encoding="utf-8")

    store = AtomicStateStore(workspace=workspace, workspace_id=WORKSPACE_ID, schema_version=2)
    scheduler = Scheduler(store)
    task = scheduler.select_next()
    turn = _record(scheduler, task.id, request_id="req_after_migration")

    assert turn.turn_id == 1
    persisted = json.loads(state_path.read_text(encoding="utf-8"))
    assert persisted["schema_version"] == 2
    assert persisted["task_records"][str(task.id)]["model_turns"][0]["request_id"] == "req_after_migration"
