"""Property tests for stateless, task-bounded LM Studio requests."""

from __future__ import annotations

import json
from typing import Any

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.config import LmStudioConfig, ModelRole, ModelRoles
from orchestrator.context_packer import ContextPacker
from orchestrator.lm_studio import LmStudioAdapter
from orchestrator.models import DeclaredCommand, ExecutionMode, GoalTask, TaskId


# Feature: stateless-turn-python-orchestrator-pipeline, Property 5: Fresh model request isolation and routing
# Validates: Requirements 4.1, 4.2, 4.3, 4.4
_TEXT = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_ ",
    min_size=1,
    max_size=40,
)
_TASK_NUMBERS = st.tuples(
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=10),
    st.integers(min_value=1, max_value=99),
)
_MODES = st.sampled_from(tuple(ExecutionMode))
# Shared static anchors must be identical for every task, so they never embed task markers.
_SHARED_RULES = "Shared rules contract for every request"
_ARCHITECTURE = "Architecture contract"


def _lm_config() -> LmStudioConfig:
    """Bind the three configured roles; requests without a role use the executor model."""
    return LmStudioConfig(
        base_url="http://127.0.0.1:1234/v1",
        request_timeout_seconds=12,
        allow_loopback_only=True,
        models=ModelRoles(
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
        ),
    )


class _FakeLocalModel:
    """A model port that records requests without performing HTTP I/O."""

    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []

    def request(self, *, payload: dict[str, Any]) -> dict[str, str]:
        self.requests.append({"model": payload["model"], "payload": payload})
        return {"id": f"request-{len(self.requests)}", "content": "{}"}


def _envelope(marker: str) -> str:
    """Wrap a generated marker in angle brackets, which generated text never contains.

    A bare marker such as "0" is a substring of "00", so isolation is checked on envelopes.
    """
    return f"<{marker}>"


def _task(coordinates: tuple[int, int, int], marker: str) -> GoalTask:
    """Build a minimal task whose marker must never cross a request boundary."""
    milestone, goal, task = coordinates
    task_id = TaskId(milestone=milestone, goal=goal, task=task)
    command = f"python -m pytest local-ai/tests/{marker}.py -q"
    return GoalTask(
        id=task_id,
        source_path=f".kiro/specs/m{milestone}-generated/goals/goal{goal}.md",
        source_hash=f"hash-{marker}",
        heading=f"Task {_envelope(marker)}",
        objective=f"Complete {_envelope(marker)}",
        acceptance_criteria=(f"Criterion {_envelope(marker)}",),
        prerequisites=(),
        implementation_details=f"Implementation {_envelope(marker)}",
        validation_commands=(
            DeclaredCommand(raw_text=command, canonical_text=command, ordinal=1),
        ),
        active_target_hints=(f"src/{marker}.py",),
    )


def _serialized(payload: dict[str, Any]) -> str:
    """Use the protocol serializer so containment checks cover every nested field."""
    return json.dumps(payload, sort_keys=True)


@settings(max_examples=100, deadline=None)
@given(
    first_coordinates=_TASK_NUMBERS,
    second_coordinates=_TASK_NUMBERS,
    first_mode=_MODES,
    second_mode=_MODES,
    first_marker=_TEXT,
    second_marker=_TEXT,
)
def test_fresh_model_request_isolation_and_routing(
    tmp_path_factory: pytest.TempPathFactory,
    first_coordinates: tuple[int, int, int],
    second_coordinates: tuple[int, int, int],
    first_mode: ExecutionMode,
    second_mode: ExecutionMode,
    first_marker: str,
    second_marker: str,
) -> None:
    """Later mode-driven requests are new, bounded payloads for their active task only."""
    if first_coordinates == second_coordinates or first_marker == second_marker:
        return

    tmp_path = tmp_path_factory.mktemp("fresh-requests")
    first = _task(first_coordinates, first_marker)
    second = _task(second_coordinates, second_marker)
    first_path = tmp_path / "src" / f"{first_marker}.py"
    second_path = tmp_path / "src" / f"{second_marker}.py"
    first_path.parent.mkdir(exist_ok=True)
    first_path.write_text(f"# {first_marker}\n", encoding="utf-8")
    second_path.write_text(f"# {second_marker}\n", encoding="utf-8")

    packer = ContextPacker(
        workspace=tmp_path,
        rules_text=_SHARED_RULES,
        architecture_text=_ARCHITECTURE,
        prompt_budget_bytes=8_000,
        max_file_bytes=1_000,
        max_active_files=1,
    )
    model = _FakeLocalModel()
    adapter = LmStudioAdapter(config=_lm_config(), model_port=model)

    first_request = packer.build_payload(
        task=first,
        mode=first_mode,
        mode_evidence={"marker": first_marker},
        active_files=(first_path.relative_to(tmp_path),),
    )
    adapter.request(first_request)
    first_planned_request = packer.build_payload(
        task=first,
        mode=first_mode,
        mode_evidence={"marker": first_marker},
        active_files=(first_path.relative_to(tmp_path),),
        plan={"task": str(first.id)},
    )
    adapter.request(first_planned_request)
    second_request = packer.build_payload(
        task=second,
        mode=second_mode,
        mode_evidence={"marker": second_marker},
        active_files=(second_path.relative_to(tmp_path),),
    )
    adapter.request(second_request)
    second_planned_request = packer.build_payload(
        task=second,
        mode=second_mode,
        mode_evidence={"marker": second_marker},
        active_files=(second_path.relative_to(tmp_path),),
        plan={"task": str(second.id)},
    )
    adapter.request(second_planned_request)

    assert [request["model"] for request in model.requests] == ["1b-gemma-4-e2b-it-qat"] * 4

    for payload, task, mode, marker in (
        (first_request, first, first_mode, first_marker),
        (first_planned_request, first, first_mode, first_marker),
        (second_request, second, second_mode, second_marker),
        (second_planned_request, second, second_mode, second_marker),
    ):
        rendered = _serialized(payload)
        assert str(task.id) in rendered
        assert mode.value in rendered
        assert task.validation_commands[0].canonical_text in rendered
        assert _envelope(marker) in rendered
        assert _SHARED_RULES in rendered

    second_rendered = _serialized(second_request) + _serialized(second_planned_request)
    assert f'"{first.id}"' not in second_rendered
    assert f'"{first.validation_commands[0].canonical_text}"' not in second_rendered
    assert _envelope(first_marker) not in second_rendered
