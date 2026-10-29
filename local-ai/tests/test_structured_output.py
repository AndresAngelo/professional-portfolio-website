"""Schema-constrained replies: Pydantic checks, three attempts, and failure evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
from hypothesis import given, settings, strategies as st
from pydantic import ValidationError

from orchestrator.schemas import AuditReport, RouterPlan
from orchestrator.structured import MAX_SCHEMA_ATTEMPTS, StructuredOutputError, structured_call

VALID_PLAN = (
    '{"task_id": "M5.G1.T1", "sanitized_constraints": ["Keep the parser pure."], '
    '"target_paths": ["local-ai/orchestrator/example.py"], "context_chunk_ids": []}'
)
MESSAGES = [{"role": "user", "content": "route this task"}]


@dataclass
class ScriptedAdapter:
    replies: list[str]
    calls: list[dict[str, Any]] = field(default_factory=list)

    def chat(
        self,
        role: str,
        messages: list[dict[str, str]],
        *,
        task_id: str | None = None,
        response_schema: dict[str, Any] | None = None,
        schema_name: str = "structured_reply",
    ) -> dict[str, Any]:
        self.calls.append(
            {"role": role, "task_id": task_id, "schema": response_schema, "schema_name": schema_name, "messages": messages}
        )
        if not self.replies:
            raise AssertionError("the scripted adapter has no reply left")
        return {"choices": [{"message": {"content": self.replies.pop(0)}}]}


def route(adapter: ScriptedAdapter):
    return structured_call(
        adapter,
        role="router",
        messages=MESSAGES,
        model_cls=RouterPlan,
        task_id="M5.G1.T1",
        schema_name="router_plan",
    )


def test_a_valid_first_reply_is_accepted_without_retries() -> None:
    adapter = ScriptedAdapter([VALID_PLAN])

    plan, failures = route(adapter)

    assert plan.task_id == "M5.G1.T1"
    assert failures == ()
    assert len(adapter.calls) == 1
    assert adapter.calls[0]["schema"] == RouterPlan.model_json_schema()
    assert adapter.calls[0]["schema_name"] == "router_plan"
    assert adapter.calls[0]["role"] == "router"


def test_a_valid_second_reply_uses_one_retry_and_keeps_the_first_failure_as_evidence() -> None:
    adapter = ScriptedAdapter(["Sure! Here is the plan:", VALID_PLAN])

    plan, failures = route(adapter)

    assert plan.task_id == "M5.G1.T1"
    assert len(adapter.calls) == 2
    assert [failure.attempt for failure in failures] == [1]
    assert failures[0].reply_excerpt.startswith("Sure!")


def test_three_invalid_replies_quarantine_after_exactly_three_requests() -> None:
    adapter = ScriptedAdapter(["not json", "{}", '{"task_id": "bad"}'])

    with pytest.raises(StructuredOutputError) as caught:
        route(adapter)

    assert MAX_SCHEMA_ATTEMPTS == 3
    assert len(adapter.calls) == 3
    assert [failure.attempt for failure in caught.value.attempts] == [1, 2, 3]
    assert caught.value.model_name == "RouterPlan"


def test_every_retry_is_a_fresh_request_with_the_same_messages_and_no_history() -> None:
    adapter = ScriptedAdapter(["not json", VALID_PLAN])

    route(adapter)

    assert adapter.calls[0]["messages"] == MESSAGES
    assert adapter.calls[1]["messages"] == MESSAGES


def test_router_plan_refuses_unknown_fields_and_malformed_task_identifiers() -> None:
    valid = {
        "task_id": "M5.G1.T1",
        "sanitized_constraints": ["Keep the parser pure."],
        "target_paths": [],
        "context_chunk_ids": [],
    }
    RouterPlan.model_validate(valid)

    with pytest.raises(ValidationError):
        RouterPlan.model_validate({**valid, "untrusted": True})
    with pytest.raises(ValidationError, match="M5.G1.T1"):
        RouterPlan.model_validate({**valid, "task_id": "5.1.1"})


def test_audit_verdict_must_agree_with_its_violations() -> None:
    passing = {"task_id": "M5.G1.T1", "verdict": "pass", "violations": []}
    AuditReport.model_validate(passing)

    with pytest.raises(ValidationError, match="pass verdict cannot list violations"):
        AuditReport.model_validate(
            {**passing, "violations": [{"rule_id": "TRD-1", "file_path": "a.py", "evidence": "x"}]}
        )
    with pytest.raises(ValidationError, match="fail verdict must list"):
        AuditReport.model_validate({**passing, "verdict": "fail"})


@settings(max_examples=100, deadline=None)
@given(replies=st.lists(st.sampled_from(["not json", "{}", VALID_PLAN]), min_size=1, max_size=5))
def test_request_count_stops_at_the_first_valid_reply_or_the_three_attempt_budget(replies: list[str]) -> None:
    adapter = ScriptedAdapter([*replies, "{}", "{}", "{}"])
    first_valid = next((index for index, reply in enumerate(replies) if reply == VALID_PLAN), None)

    if first_valid is not None and first_valid < MAX_SCHEMA_ATTEMPTS:
        plan, _ = route(adapter)
        assert plan.task_id == "M5.G1.T1"
        assert len(adapter.calls) == first_valid + 1
    else:
        with pytest.raises(StructuredOutputError):
            route(adapter)
        assert len(adapter.calls) == MAX_SCHEMA_ATTEMPTS
