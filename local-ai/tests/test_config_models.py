"""Contracts for immutable orchestrator configuration and JSON domain records."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.config import ConfigurationError, load_configuration
from orchestrator.models import (
    DeclaredCommand,
    ExecutionMode,
    GoalTask,
    RunState,
    TaskId,
    TaskQueueRecord,
    TaskRunRecord,
    TaskStatus,
    ToolOperation,
)


_EMBEDDING_ROLE = """[lm_studio.models.embedding]
model_id = "embed-text-embedding-nomic-embed-text-v1.5"
context_length = 2048
output_reserve_tokens = 0
max_prompt_bytes = 8192
"""
_EXECUTOR_ROLE = """[lm_studio.models.executor]
model_id = "1b-gemma-4-e2b-it-qat"
context_length = 4096
output_reserve_tokens = 1024
max_prompt_bytes = 12288
"""


def _router_role(
    *, context_length: int = 2048, output_reserve_tokens: int = 512, max_prompt_bytes: int = 6144
) -> str:
    """Render the router binding so budget tests can vary only the numbers under test."""
    return (
        "[lm_studio.models.router]\n"
        'model_id = "1b-gemma-3-1b-it-qat"\n'
        f"context_length = {context_length}\n"
        f"output_reserve_tokens = {output_reserve_tokens}\n"
        f"max_prompt_bytes = {max_prompt_bytes}\n"
    )


DEFAULT_MODEL_ROLES = "\n".join((_EMBEDDING_ROLE, _router_role(), _EXECUTOR_ROLE))
RETIRED_MODEL_ID = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"


def write_config(
    workspace: Path,
    *,
    base_url: str = "http://127.0.0.1:1234/v1",
    local_storage: str = "local-ai",
    lm_studio_extra: str = "",
    allow_loopback_only: str = "true",
    model_roles: str = DEFAULT_MODEL_ROLES,
) -> Path:
    """Write the smallest complete runtime configuration for a test workspace."""
    config_path = workspace / "local-ai" / "config" / "orchestrator.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        f'''[workspace]
root = "{workspace.as_posix()}"
spec_root = ".kiro/specs"
local_storage = "{local_storage}"

[discovery]
enabled_milestones = [1, 2, 3, 4, 5]
future_milestones = [6, 7, 8, 9, 10]
goal_glob = "m{{milestone}}-*/goals/goal{{goal}}.md"
required_goal_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

[legacy_instruction_migration]
accepted_root_aliases = ["{workspace.as_posix()}/personal-website-portfolio-v2"]
tracker_path = "local-ai/program-states/progress-tracker.md"
tracker_mode = "orchestrator-owned"

[lm_studio]
base_url = "{base_url}"
request_timeout_seconds = 120
allow_loopback_only = {allow_loopback_only}
{lm_studio_extra}
{model_roles}

[context]
max_file_bytes = 24000
max_active_files = 8
rules_path = "local-ai/context/pipeline-rules.md"
architecture_path = "local-ai/context/architecture-schema.md"

[retry]
max_error_mode_requests = 3

[low_vram]
benchmark_enabled = false
requested_flash_attention = "auto"
requested_unified_kv = "auto"
requested_kv_cache_type = "Q4_0"
requested_kv_offload = "auto"
requested_gpu_offload_layers = "auto"
''',
        encoding="utf-8",
    )
    return config_path


def test_configuration_uses_configured_root_and_preserves_legacy_alias(workspace: Path) -> None:
    """The real configured repository root wins over legacy task-instruction paths."""
    config = load_configuration(write_config(workspace))

    assert config.workspace.root == workspace.resolve()
    assert config.workspace.spec_root == (workspace / ".kiro" / "specs").resolve()
    assert config.workspace.local_storage == (workspace / "local-ai").resolve()
    assert config.legacy_instruction_migration.accepted_root_aliases == (
        (workspace / "personal-website-portfolio-v2").resolve(),
    )
    assert config.legacy_instruction_migration.tracker_path == (
        workspace / "local-ai" / "program-states" / "progress-tracker.md"
    ).resolve()
    assert config.legacy_instruction_migration.tracker_mode == "orchestrator-owned"


def test_configuration_keeps_m1_through_m5_enabled_and_m6_through_m10_disabled(
    workspace: Path,
) -> None:
    """Future milestones remain configuration-gated rather than discoverable by default."""
    config = load_configuration(write_config(workspace))

    assert config.discovery.enabled_milestones == (1, 2, 3, 4, 5)
    assert config.discovery.future_milestones == (6, 7, 8, 9, 10)
    assert set(config.discovery.enabled_milestones).isdisjoint(config.discovery.future_milestones)
    assert config.discovery.required_goal_numbers == tuple(range(1, 11))


@pytest.mark.parametrize(
    "base_url",
    [
        "https://example.test/v1",
        "http://192.168.1.10:1234/v1",
        "http://[::1]:1234/v1",
        "http://localhost:1234/v1",
    ],
)
def test_configuration_rejects_non_loopback_model_endpoints(workspace: Path, base_url: str) -> None:
    """Only explicitly configured IPv4 loopback LM Studio endpoints are valid."""
    config_path = write_config(workspace, base_url=base_url)

    with pytest.raises(ConfigurationError, match="loopback"):
        load_configuration(config_path)


def test_configuration_rejects_storage_outside_the_canonical_workspace(workspace: Path) -> None:
    """State and artifacts cannot be redirected outside the selected workspace."""
    outside_storage = workspace.parent / "outside-local-ai"
    config_path = write_config(workspace, local_storage=outside_storage.as_posix())

    with pytest.raises(ConfigurationError, match="storage.*workspace"):
        load_configuration(config_path)


def test_task_state_and_operation_codecs_preserve_the_typed_contract() -> None:
    """Domain records round-trip through JSON-safe dictionaries without losing state."""
    task_id = TaskId(milestone=5, goal=1, task=2)
    task = GoalTask(
        id=task_id,
        source_path=".kiro/specs/m5-demo/goals/goal1.md",
        source_hash="a" * 64,
        heading="Build a typed contract",
        objective="Create immutable model records.",
        acceptance_criteria=("Records are JSON-safe.",),
        prerequisites=("Python 3.12",),
        implementation_details="Use frozen dataclasses.",
        validation_commands=(
            DeclaredCommand(
                raw_text="python -m pytest local-ai/tests -q",
                canonical_text="python -m pytest local-ai/tests -q",
                ordinal=1,
            ),
        ),
        active_target_hints=("local-ai/orchestrator/models.py",),
    )
    state = RunState(
        schema_version=1,
        workspace_id="workspace-sha256",
        queue=[TaskQueueRecord(task=task, ordinal=0)],
        task_records={
            str(task_id): TaskRunRecord(
                task_id=task_id,
                status=TaskStatus.IN_PROGRESS,
                mode_history=[ExecutionMode.COT_TASK],
                request_ids=["plan-001", "execute-001"],
            )
        },
        active_task_id=str(task_id),
        updated_at="2026-01-01T00:00:00Z",
    )
    operation = ToolOperation(
        protocol_version="1.0",
        task_id=str(task_id),
        target_path="local-ai/orchestrator/models.py",
        action="write_file",
        arguments={"content": "# generated\n"},
        expected_result="The model module exists.",
    )

    encoded_state = state.to_dict()
    encoded_operation = operation.to_dict()

    assert json.loads(json.dumps(encoded_state)) == encoded_state
    assert json.loads(json.dumps(encoded_operation)) == encoded_operation
    assert RunState.from_dict(encoded_state) == state
    assert ToolOperation.from_dict(encoded_operation) == operation
    assert TaskId.from_string(str(task_id)) == task_id


def test_configuration_loads_three_named_model_roles(workspace: Path) -> None:
    """Embedding, router, and executor bindings load with their exact IDs and context caps."""
    config = load_configuration(write_config(workspace))
    roles = config.lm_studio.models

    assert config.lm_studio.base_url == "http://127.0.0.1:1234/v1"
    assert (roles.embedding.model_id, roles.embedding.context_length) == (
        "embed-text-embedding-nomic-embed-text-v1.5",
        2048,
    )
    assert (roles.router.model_id, roles.router.context_length) == ("1b-gemma-3-1b-it-qat", 2048)
    assert (roles.executor.model_id, roles.executor.context_length) == ("1b-gemma-4-e2b-it-qat", 4096)
    assert roles.for_role("router") == roles.router


def test_configuration_rejects_legacy_single_model_key(workspace: Path) -> None:
    """The retired single [lm_studio] model_id key fails closed instead of selecting a model."""
    config_path = write_config(workspace, lm_studio_extra='model_id = "1b-gemma-4-e2b-it-qat"')

    with pytest.raises(ConfigurationError, match="model_id is retired"):
        load_configuration(config_path)


def test_configuration_rejects_retired_pinned_model_identifier(workspace: Path) -> None:
    """The pinned 12B identifier cannot be bound to any role."""
    roles = DEFAULT_MODEL_ROLES.replace('"1b-gemma-3-1b-it-qat"', f'"{RETIRED_MODEL_ID}"')
    config_path = write_config(workspace, model_roles=roles)

    with pytest.raises(ConfigurationError, match="retired pinned"):
        load_configuration(config_path)


def test_configuration_requires_three_distinct_model_identifiers(workspace: Path) -> None:
    """Two roles cannot share one LM Studio model identifier."""
    roles = DEFAULT_MODEL_ROLES.replace(
        '"1b-gemma-3-1b-it-qat"', '"embed-text-embedding-nomic-embed-text-v1.5"'
    )
    config_path = write_config(workspace, model_roles=roles)

    with pytest.raises(ConfigurationError, match="distinct"):
        load_configuration(config_path)


def test_configuration_rejects_disabling_the_loopback_guard(workspace: Path) -> None:
    """A remote endpoint cannot be enabled by turning off allow_loopback_only."""
    config_path = write_config(
        workspace, base_url="https://model.example/v1", allow_loopback_only="false"
    )

    with pytest.raises(ConfigurationError, match="loopback"):
        load_configuration(config_path)


def test_configuration_derives_prompt_budgets_from_usable_context(workspace: Path) -> None:
    """Each prompt budget is at most (context_length - output_reserve_tokens) x 4 bytes."""
    roles = load_configuration(write_config(workspace)).lm_studio.models

    assert (roles.embedding.output_reserve_tokens, roles.embedding.max_prompt_bytes) == (0, 8192)
    assert (roles.router.output_reserve_tokens, roles.router.max_prompt_bytes) == (512, 6144)
    assert (roles.executor.output_reserve_tokens, roles.executor.max_prompt_bytes) == (1024, 12288)


def test_configuration_rejects_budget_above_usable_context(workspace: Path) -> None:
    """A router budget one byte above (2048 - 512) x 4 is refused before any request is built."""
    roles = "\n".join((_EMBEDDING_ROLE, _router_role(max_prompt_bytes=6145), _EXECUTOR_ROLE))

    with pytest.raises(ConfigurationError, match="max_prompt_bytes"):
        load_configuration(write_config(workspace, model_roles=roles))


def test_configuration_rejects_output_reserve_that_consumes_the_context(workspace: Path) -> None:
    """An output reserve equal to the context length leaves no room for any prompt."""
    router = _router_role(output_reserve_tokens=2048, max_prompt_bytes=1)
    roles = "\n".join((_EMBEDDING_ROLE, router, _EXECUTOR_ROLE))

    with pytest.raises(ConfigurationError, match="output_reserve_tokens"):
        load_configuration(write_config(workspace, model_roles=roles))


def test_configuration_rejects_the_retired_global_context_budget(workspace: Path) -> None:
    """The global [context] max_total_bytes key is replaced by per-role prompt budgets."""
    config_path = write_config(workspace)
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace(
            "max_file_bytes = 24000", "max_total_bytes = 120000\nmax_file_bytes = 24000"
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="max_total_bytes is retired"):
        load_configuration(config_path)


@settings(max_examples=100, deadline=None)
@given(
    context_length=st.integers(min_value=1, max_value=8192),
    output_reserve_tokens=st.integers(min_value=0, max_value=8192),
    max_prompt_bytes=st.integers(min_value=1, max_value=40_000),
)
def test_every_declared_budget_leaves_room_for_the_output_reserve(
    tmp_path_factory: pytest.TempPathFactory,
    context_length: int,
    output_reserve_tokens: int,
    max_prompt_bytes: int,
) -> None:
    """The router budget loads exactly when it fits context minus the output reserve."""
    workspace = tmp_path_factory.mktemp("budget")
    roles = "\n".join(
        (
            _EMBEDDING_ROLE,
            _router_role(
                context_length=context_length,
                output_reserve_tokens=output_reserve_tokens,
                max_prompt_bytes=max_prompt_bytes,
            ),
            _EXECUTOR_ROLE,
        )
    )
    config_path = write_config(workspace, model_roles=roles)
    usable_bytes = (context_length - output_reserve_tokens) * 4
    fits = output_reserve_tokens < context_length and 1 <= max_prompt_bytes <= usable_bytes

    if fits:
        assert load_configuration(config_path).lm_studio.models.router.max_prompt_bytes == max_prompt_bytes
    else:
        with pytest.raises(ConfigurationError):
            load_configuration(config_path)
