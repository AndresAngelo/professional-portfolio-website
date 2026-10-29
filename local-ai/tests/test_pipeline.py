"""Four-pass pipeline scenarios with a scripted fake model. No network, no real model."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orchestrator.context_packer import ContextPacker, PromptBudgetError, pack_router_prompt
from orchestrator.models import TaskStatus
from orchestrator.pipeline import PipelineDeps, Retrieval, run_task
from orchestrator.scheduler import Scheduler
from orchestrator.validation import ValidationRecord
from orchestrator.workspace import WorkspaceToolExecutor

from test_state_scheduler import build_store, make_state

TASK = "M1.G1.T1"
ROUTER_OK = json.dumps(
    {"task_id": TASK, "sanitized_constraints": ["keep it small"], "target_paths": ["out.txt"], "context_chunk_ids": ["a#1"]}
)
AUDIT_PASS = json.dumps({"task_id": TASK, "verdict": "pass", "violations": []})
AUDIT_FAIL = json.dumps(
    {"task_id": TASK, "verdict": "fail", "violations": [{"rule_id": "R1", "file_path": "out.txt", "evidence": "bad"}]}
)
WRITE_OP = json.dumps(
    {
        "protocol_version": "1.0", "task_id": TASK, "target_path": "out.txt", "action": "write_file",
        "arguments": {"content": "hello"}, "expected_result": "out.txt exists",
    }
)


def _reply(text: str) -> dict:
    return {"choices": [{"message": {"content": text}}]}


class FakeAdapter:
    """Pops scripted replies per role. The router role also serves the auditor."""

    def __init__(self, router: list[str], executor: list[str]) -> None:
        self.queues = {"router": list(router), "executor": list(executor)}
        self.calls: list[str] = []
        self.schemas: list[tuple[str, str, bool]] = []
        self.last_request_id: str | None = None
        self.last_model_id: str | None = None

    def chat(self, role, messages, *, task_id=None, response_schema=None, schema_name="x"):
        self.calls.append(role)
        self.schemas.append((role, schema_name, response_schema is not None))
        self.last_request_id = f"req_{len(self.calls)}"
        self.last_model_id = {"router": "gemma-3-1b-it-qat", "executor": "gemma-4-e2b-it-qat@q4_k_xl"}[role]
        return _reply(self.queues[role].pop(0))


def _deps(workspace: Path, adapter: FakeAdapter, exit_codes: list[int]):
    scheduler = Scheduler(build_store(workspace))
    scheduler.store.commit(make_state(queued_task_numbers=(1,)))
    task = scheduler.select_next()
    codes = list(exit_codes)

    def validate(_task):
        code = codes.pop(0)
        return [
            ValidationRecord("python -m pytest -q", 1, "", "boom" if code else "", code, "t",
                             f"local-ai/validation/M1_G1_T1/{len(codes)}.json")
        ]

    deps = PipelineDeps(
        scheduler=scheduler, adapter=adapter, workspace=workspace,
        packer=ContextPacker(workspace=workspace, rules_text="rules", architecture_text="arch",
                             prompt_budget_bytes=12288, max_file_bytes=24000, max_active_files=8),
        router_budget=6144, router_system_text="route", auditor_system_text="audit",
        retrieve=lambda _q: Retrieval([{"chunk_id": "a#1", "text": "context"}], "req_embed", "nomic"),
        tool_executor=WorkspaceToolExecutor(workspace=workspace, storage=workspace / "local-ai"),
        validate=validate,
    )
    return deps, task, scheduler


def test_happy_path_completes_and_ledgers_every_pass(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK, AUDIT_PASS], [WRITE_OP])
    deps, task, scheduler = _deps(workspace, adapter, [0])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "completed" and record.status is TaskStatus.COMPLETED
    assert [t.pass_name for t in record.model_turns] == ["embedding", "router", "executor", "auditor"]
    assert [t.model_id for t in record.model_turns][1:] == [
        "gemma-3-1b-it-qat", "gemma-4-e2b-it-qat@q4_k_xl", "gemma-3-1b-it-qat"
    ]
    assert (workspace / "out.txt").read_text(encoding="utf-8") == "hello"
    # Every pass is schema-constrained, including the executor.
    assert adapter.schemas == [
        ("router", "router_plan", True),
        ("executor", "x", False),
        ("router", "audit_report", True),
    ]


def test_router_schema_retries_do_not_spend_error_mode_requests(workspace: Path) -> None:
    adapter = FakeAdapter(["not json", "{}", ROUTER_OK, AUDIT_PASS], [WRITE_OP])
    deps, task, scheduler = _deps(workspace, adapter, [0])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "completed" and record.error_mode_requests == 0
    assert adapter.calls.count("router") == 4  # 3 router attempts + 1 audit


def test_router_exhausting_schema_attempts_quarantines(workspace: Path) -> None:
    adapter = FakeAdapter(["x", "y", "z"], [])
    deps, task, scheduler = _deps(workspace, adapter, [])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "quarantined" and record.status is TaskStatus.QUARANTINED
    assert adapter.calls == ["router"] * 3 and record.error_mode_requests == 0


def test_validation_failures_stop_after_exactly_three_error_requests(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK], [WRITE_OP] * 4)
    deps, task, scheduler = _deps(workspace, adapter, [1, 1, 1, 1])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "quarantined" and record.status is TaskStatus.QUARANTINED
    assert adapter.calls.count("executor") == 4  # first attempt + 3 Error-mode requests
    assert record.error_mode_requests == 3
    assert [e.disposition for e in record.error_history] == ["error_request_granted"] * 3 + ["refused_retry_limit"]


def test_recovery_in_error_mode_completes_and_counts_the_request(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK, AUDIT_PASS], [WRITE_OP, WRITE_OP])
    deps, task, scheduler = _deps(workspace, adapter, [1, 0])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "completed" and result.error_mode_requests == 1
    assert [t.outcome for t in record.model_turns if t.pass_name == "executor"] == ["validation_failed", "accepted"]


def test_empty_executor_reply_is_quarantined_without_validation(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK], ["   "])
    deps, task, scheduler = _deps(workspace, adapter, [])

    result = run_task(deps, task)

    assert result.status == "quarantined" and "empty" in result.detail
    assert scheduler.store.load().task_records[TASK].status is TaskStatus.QUARANTINED


def test_free_text_executor_reply_is_written_as_a_note_and_validated(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK, AUDIT_PASS], ["Checked the prerequisites. Versions are fine."])
    deps, task, scheduler = _deps(workspace, adapter, [0])

    result = run_task(deps, task)

    assert result.status == "completed"
    note = (workspace / "local-ai" / "notes" / f"{TASK}.md").read_text(encoding="utf-8")
    assert "Checked the prerequisites" in note


def test_failed_audit_quarantines_and_keeps_the_edit(workspace: Path) -> None:
    adapter = FakeAdapter([ROUTER_OK, AUDIT_FAIL], [WRITE_OP])
    deps, task, scheduler = _deps(workspace, adapter, [0])

    result = run_task(deps, task)

    record = scheduler.store.load().task_records[TASK]
    assert result.status == "quarantined" and (workspace / "out.txt").exists()
    assert record.model_turns[-1].outcome == "audit_rejected"


def test_router_prompt_drops_lowest_ranked_chunks_first_and_refuses_oversized_anchors() -> None:
    chunks = [{"chunk_id": f"c{i}", "text": "x" * 400} for i in range(5)]
    prompt = pack_router_prompt(system_text="s" * 100, scope={"task_id": TASK}, chunks=chunks, budget=1200)
    assert prompt.included_chunk_ids == ("c0", "c1")
    assert prompt.dropped_chunk_ids == ("c2", "c3", "c4")
    assert prompt.prompt_bytes <= 1200
    with pytest.raises(PromptBudgetError):
        pack_router_prompt(system_text="s" * 2000, scope={"task_id": TASK}, chunks=chunks, budget=1200)
