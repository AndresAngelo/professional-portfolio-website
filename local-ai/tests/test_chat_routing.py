"""Role-routed chat requests: each role reaches its own model, and schema requests are constrained."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from orchestrator.config import LmStudioConfig, ModelRole, ModelRoles
from orchestrator.lm_studio import LmStudioAdapter, ModelRequestError, build_messages, reply_text

ROUTER_SCHEMA = {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}


@dataclass
class RecordingTransport:
    responses: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
        self.calls.append({"method": method, "url": url, "payload": payload})
        return self.responses.pop(0)


def lm_config() -> LmStudioConfig:
    return LmStudioConfig(
        base_url="http://127.0.0.1:1234/v1",
        request_timeout_seconds=12,
        allow_loopback_only=True,
        models=ModelRoles(
            embedding=ModelRole("text-embedding-nomic-embed-text-v1.5", 2048, 0, 8192),
            router=ModelRole("gemma-3-1b-it-qat", 2048, 512, 6144),
            executor=ModelRole("gemma-4-e2b-it-qat@q4_k_xl", 4096, 1024, 12288),
        ),
    )


def reply(content: str) -> dict[str, Any]:
    return {"choices": [{"message": {"role": "assistant", "content": content}}]}


def test_each_role_reaches_its_own_model(workspace: Path) -> None:
    transport = RecordingTransport(responses=[reply("{}"), reply("{}")])
    adapter = LmStudioAdapter(config=lm_config(), storage=workspace / "local-ai", transport=transport)

    adapter.chat("router", [{"role": "user", "content": "route"}], task_id="M5.G1.T1")
    adapter.chat("executor", [{"role": "user", "content": "code"}], task_id="M5.G1.T1")

    assert [call["payload"]["model"] for call in transport.calls] == [
        "gemma-3-1b-it-qat",
        "gemma-4-e2b-it-qat@q4_k_xl",
    ]
    assert adapter.last_model_id == "gemma-4-e2b-it-qat@q4_k_xl"


def test_schema_requests_are_constrained_with_a_strict_json_schema(workspace: Path) -> None:
    transport = RecordingTransport(responses=[reply('{"task_id": "M5.G1.T1"}')])
    adapter = LmStudioAdapter(config=lm_config(), storage=workspace / "local-ai", transport=transport)

    adapter.chat(
        "router",
        [{"role": "user", "content": "route"}],
        task_id="M5.G1.T1",
        response_schema=ROUTER_SCHEMA,
        schema_name="router_plan",
    )

    body = transport.calls[0]["payload"]
    assert body["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "router_plan", "strict": True, "schema": ROUTER_SCHEMA},
    }
    assert body["temperature"] == 0


def test_unconstrained_requests_send_no_response_format(workspace: Path) -> None:
    transport = RecordingTransport(responses=[reply("code")])
    adapter = LmStudioAdapter(config=lm_config(), storage=workspace / "local-ai", transport=transport)

    adapter.chat("executor", [{"role": "user", "content": "code"}], task_id="M5.G1.T1")

    assert "response_format" not in transport.calls[0]["payload"]


def test_request_shorthand_routes_to_the_executor_with_anchors_as_system_text(workspace: Path) -> None:
    transport = RecordingTransport(responses=[reply("ok")])
    adapter = LmStudioAdapter(config=lm_config(), storage=workspace / "local-ai", transport=transport)
    payload = {
        "context": {
            "system_rules": "RULES",
            "architecture_schema": "SCHEMA",
            "active_task_scope": {"task_id": "M5.G1.T1"},
        }
    }

    adapter.request(payload, task_id="M5.G1.T1")

    body = transport.calls[0]["payload"]
    assert body["model"] == "gemma-4-e2b-it-qat@q4_k_xl"
    assert body["messages"][0] == {"role": "system", "content": "RULES\n\nSCHEMA"}
    assert body["messages"][1]["role"] == "user"
    assert '"task_id": "M5.G1.T1"' in body["messages"][1]["content"]


def test_payloads_without_context_are_sent_as_one_json_user_message() -> None:
    assert build_messages({"a": 1}) == [{"role": "user", "content": '{"a": 1}'}]


def test_reply_text_extracts_the_content_or_fails_locally() -> None:
    assert reply_text(reply("hi")) == "hi"
    with pytest.raises(ModelRequestError, match="choices"):
        reply_text({"choices": []})


def test_a_reply_that_names_a_draft_model_is_refused_as_speculative_decoding(workspace: Path) -> None:
    """Draft-model fields mean speculative decoding is on, which the operator turned off. Fail closed."""
    from orchestrator.lm_studio import SpeculativeDecodingError

    drafted = {**reply("{}"), "draft_model": "unsloth/gemma-4-E2B-it-qat-GGUF/mtp-F16.gguf"}
    adapter = LmStudioAdapter(
        config=lm_config(), storage=workspace / "local-ai", transport=RecordingTransport(responses=[drafted])
    )

    with pytest.raises(SpeculativeDecodingError, match="speculative decoding is on"):
        adapter.chat("executor", [{"role": "user", "content": "code"}], task_id="M5.G1.T1")
    assert adapter.last_draft_model is not None


def test_a_draft_model_reported_only_in_stats_is_also_refused(workspace: Path) -> None:
    from orchestrator.lm_studio import SpeculativeDecodingError

    drafted = {**reply("{}"), "stats": {"draft_model": "x.gguf", "total_draft_tokens_count": 5}}
    adapter = LmStudioAdapter(
        config=lm_config(), storage=workspace / "local-ai", transport=RecordingTransport(responses=[drafted])
    )

    with pytest.raises(SpeculativeDecodingError):
        adapter.chat("router", [{"role": "user", "content": "route"}], task_id="M5.G1.T1")


def test_the_executor_reply_is_constrained_to_the_tool_protocol_schema() -> None:
    """The hand-written executor schema requires every protocol key and only the four known actions."""
    from orchestrator.schemas import TOOL_PROTOCOL_SCHEMA

    assert set(TOOL_PROTOCOL_SCHEMA["required"]) == set(TOOL_PROTOCOL_SCHEMA["properties"])
    assert TOOL_PROTOCOL_SCHEMA["properties"]["action"]["enum"] == ["mkdir", "write_file", "patch_file", "delete_file"]
    assert TOOL_PROTOCOL_SCHEMA["additionalProperties"] is False
    assert "$ref" not in str(TOOL_PROTOCOL_SCHEMA) and "pattern" not in TOOL_PROTOCOL_SCHEMA["properties"]["task_id"]
