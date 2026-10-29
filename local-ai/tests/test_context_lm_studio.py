"""Test-first examples for bounded fresh context and local LM Studio requests.

Task 4.3 must implement these contracts without contacting a real LM Studio server.  The
transport below is a deterministic local test double; production code must supply the
actual loopback HTTP boundary and artifact persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from orchestrator.config import ContextConfig, LmStudioConfig, ModelRole, ModelRoles
from orchestrator.context_packer import ContextPacker
from orchestrator.lm_studio import LmStudioAdapter, ModelRequestError
from orchestrator.models import DeclaredCommand, ExecutionMode, GoalTask, TaskId


@dataclass
class RecordingLocalTransport:
    """Local-only transport double that records HTTP contract calls."""

    responses: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    failure: Exception | None = None

    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
        self.calls.append({"method": method, "url": url, "payload": payload, "timeout": timeout})
        if self.failure is not None:
            raise self.failure
        if not self.responses:
            raise AssertionError("No local response was configured.")
        return self.responses.pop(0)


def make_task(*, target_hints: tuple[str, ...] = ("src/active.py",)) -> GoalTask:
    """Create the smallest task with active scope and declared validation."""
    return GoalTask(
        id=TaskId(5, 1, 1),
        source_path=".kiro/specs/m5-example/goals/goal1.md",
        source_hash="source-hash",
        heading="Build active scope",
        objective="Create bounded task context.",
        acceptance_criteria=("Only current-task scope is included.",),
        prerequisites=("Configuration is valid.",),
        implementation_details="Use the local adapter.",
        validation_commands=(
            DeclaredCommand("python -m pytest -q", "python -m pytest -q", 1),
        ),
        active_target_hints=target_hints,
    )


def make_context_config(workspace: Path, *, per_file: int = 64) -> ContextConfig:
    rules = workspace / "local-ai" / "context" / "pipeline-rules.md"
    architecture = workspace / "local-ai" / "context" / "architecture-schema.md"
    rules.parent.mkdir(parents=True, exist_ok=True)
    rules.write_text("Return strict protocol JSON.", encoding="utf-8")
    architecture.write_text("interface ActiveScope: bounded", encoding="utf-8")
    return ContextConfig(
        max_file_bytes=per_file,
        max_active_files=2,
        rules_path=rules,
        architecture_path=architecture,
    )


def make_model_roles() -> ModelRoles:
    return ModelRoles(
        embedding=ModelRole(
            model_id="embed-text-embedding-nomic-embed-text-v1.5",
            context_length=2048,
            output_reserve_tokens=0,
            max_prompt_bytes=8192,
        ),
        router=ModelRole(
            model_id="1b-gemma-3-1b-it-qat",
            context_length=2048,
            output_reserve_tokens=512,
            max_prompt_bytes=6144,
        ),
        executor=ModelRole(
            model_id="1b-gemma-4-e2b-it-qat",
            context_length=4096,
            output_reserve_tokens=1024,
            max_prompt_bytes=12288,
        ),
    )


def make_lm_config(*, base_url: str = "http://127.0.0.1:1234/v1") -> LmStudioConfig:
    return LmStudioConfig(
        base_url=base_url,
        request_timeout_seconds=12,
        allow_loopback_only=True,
        models=make_model_roles(),
    )


def test_packer_creates_deterministic_three_bucket_scope_from_current_task_only(workspace: Path) -> None:
    """Rules, architecture, and active scope are stable and exclude arbitrary workspace files."""
    config = make_context_config(workspace)
    (workspace / "src").mkdir()
    (workspace / "src" / "active.py").write_text("ACTIVE = True\n", encoding="utf-8")
    (workspace / "src" / "ignored.py").write_text("SECRET = 'not context'\n", encoding="utf-8")
    packer = ContextPacker(
        workspace=workspace,
        config=config,
        prompt_budget_bytes=make_model_roles().executor.max_prompt_bytes,
    )

    first = packer.pack(task=make_task(), mode=ExecutionMode.COT_TASK, evidence="healthy target")
    second = packer.pack(task=make_task(), mode=ExecutionMode.COT_TASK, evidence="healthy target")

    assert first.payload == second.payload
    assert tuple(first.payload["context"]) == ("system_rules", "architecture_schema", "active_task_scope")
    assert first.payload["context"]["system_rules"] == "Return strict protocol JSON."
    assert first.payload["context"]["architecture_schema"] == "interface ActiveScope: bounded"
    assert first.payload["context"]["active_task_scope"]["task_id"] == "M5.G1.T1"
    assert first.payload["context"]["active_task_scope"]["validation_commands"] == ["python -m pytest -q"]
    assert first.manifest.included_paths == ("src/active.py",)
    assert "ignored.py" not in str(first.payload)


def test_packer_enforces_per_file_and_total_byte_caps_with_manifest_markers(workspace: Path) -> None:
    """Oversized active files are deterministically truncated and accounted for in the manifest."""
    config = make_context_config(workspace, per_file=20)
    (workspace / "src").mkdir()
    (workspace / "src" / "a.py").write_text("a" * 80, encoding="utf-8")
    (workspace / "src" / "b.py").write_text("b" * 80, encoding="utf-8")
    packed = ContextPacker(workspace=workspace, config=config, prompt_budget_bytes=2000).pack(
        task=make_task(target_hints=("src/b.py", "src/a.py")),
        mode=ExecutionMode.SCAFFOLD,
        evidence="target absent before creation",
    )

    assert packed.manifest.included_paths == ("src/a.py", "src/b.py")
    assert packed.manifest.truncated_paths == ("src/a.py", "src/b.py")
    from orchestrator.context_packer import PromptBudgetError, messages_bytes

    assert messages_bytes(packed.payload) <= 2000
    with pytest.raises(PromptBudgetError):
        ContextPacker(workspace=workspace, config=config, prompt_budget_bytes=180).pack(
            task=make_task(target_hints=("src/b.py", "src/a.py")),
            mode=ExecutionMode.SCAFFOLD,
            evidence="target absent before creation",
        )
    files = packed.payload["context"]["active_task_scope"]["files"]
    assert all("[TRUNCATED" in item["content"] for item in files)


def test_adapter_routes_default_requests_to_executor_only(workspace: Path) -> None:
    """Requests without an explicit role use the executor binding and only the chat-completions endpoint."""
    model_id = make_model_roles().executor.model_id
    transport = RecordingLocalTransport(
        responses=[{"id": "first"}, {"id": "second"}]
    )
    adapter = LmStudioAdapter(config=make_lm_config(), storage=workspace / "local-ai", transport=transport)

    first = adapter.request({"request": "first", "mode": "Scaffold"}, task_id="M5.G1.T1")
    second = adapter.request({"request": "second", "mode": "CoT-Task"}, task_id="M5.G1.T1")

    assert first["id"] == "first"
    assert second["id"] == "second"
    assert [(call["method"], call["url"]) for call in transport.calls] == [
        ("POST", "http://127.0.0.1:1234/v1/chat/completions"),
        ("POST", "http://127.0.0.1:1234/v1/chat/completions"),
    ]
    assert all(call["payload"]["model"] == model_id for call in transport.calls)
    assert adapter.model_id_for("executor") == model_id


def test_adapter_rejects_non_loopback_endpoints_and_normalizes_capabilities(workspace: Path) -> None:
    """Only loopback service URLs are allowed and missing capability data is not invented."""
    with pytest.raises(ValueError, match="loopback"):
        LmStudioAdapter(
            config=make_lm_config(base_url="https://model.example/v1"),
            storage=workspace / "local-ai",
            transport=RecordingLocalTransport(),
        )

    transport = RecordingLocalTransport(responses=[{"flash_attention": True, "gpu_offload": False}])
    capabilities = LmStudioAdapter(
        config=make_lm_config(), storage=workspace / "local-ai", transport=transport
    ).capabilities()

    assert capabilities == {
        "flash_attention": "supported",
        "gpu_offload": "unsupported",
        "unified_kv": "not-reported",
        "kv_cache_type": "not-reported",
        "kv_offload": "not-reported",
    }


@pytest.mark.parametrize("failure", [ConnectionError("offline"), TimeoutError("slow"), RuntimeError("HTTP 503")])
def test_transport_failure_writes_error_artifact_without_mutating_workspace_or_active_state(
    workspace: Path, failure: Exception
) -> None:
    """Request failures preserve caller-managed in-progress state and existing workspace changes."""
    source = workspace / "src" / "partial.py"
    source.parent.mkdir()
    source.write_text("partial change\n", encoding="utf-8")
    active_state = {"active_task_id": "M5.G1.T1", "status": "in_progress"}
    adapter = LmStudioAdapter(
        config=make_lm_config(),
        storage=workspace / "local-ai",
        transport=RecordingLocalTransport(failure=failure),
    )

    with pytest.raises(ModelRequestError):
        adapter.request({"request": "mode-driven"}, task_id="M5.G1.T1")

    assert source.read_text(encoding="utf-8") == "partial change\n"
    assert active_state == {"active_task_id": "M5.G1.T1", "status": "in_progress"}
    errors = list((workspace / "local-ai" / "protocol-records" / "M5_G1_T1").glob("*request-error*.json"))
    assert len(errors) == 1
    record = errors[0].read_text(encoding="utf-8")
    assert make_model_roles().executor.model_id in record
    assert '"role": "executor"' in record
    assert "M5.G1.T1" in record
