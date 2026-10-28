"""Property tests for stateless, task-bounded LM Studio requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hypothesis import given, settings, strategies as st

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


class _FakeLocalModel:
    """A model port that records requests without performing HTTP I/O."""

    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []

    def request(self, *, payload: dict[str, Any]) -> dict[str, str]:
        self.requests.append({"model": payload["model"], "payload": payload})
        return {"id": f"request-{len(self.requests)}", "content": "{}"}


def _task(coordinates: tuple[int, int, int], marker: str) -> GoalTask:
    """Build a minimal task whose marker must never cross a request boundary."""
    milestone, goal, task = coordinates
    task_id = TaskId(milestone=milestone, goal=goal, task=task)
    command = f"python -m pytest local-ai/tests/{marker}.py -q"
    return GoalTask(
        id=task_id,
        source_path=f".kiro/specs/m{milestone}-generated/goals/goal{goal}.md",
        source_hash=f"hash-{marker}",
        heading=f"Task {marker}",
        objective=f"Complete {marker}",
        acceptance_criteria=(f"Criterion {marker}",),
        prerequisites=(),
        implementation_details=f"Implementation {marker}",
        validation_commands=(
            DeclaredCommand(raw_text=command, canonical_text=command, ordinal=1),
        ),
        active_target_hints=(f"src/{marker}.py",),
    )


def _serialized(payload: dict[str, Any]) -> str:
    """Use the protocol serializer so containment checks cover every nested field."""
    import json

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
    tmp_path: Path,
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

    rules = f"Rules for {first_marker} and {second_marker}"
    architecture = "Architecture contract"
    first = _task(first_coordinates, first_marker)
    second = _task(second_coordinates, second_marker)
    first_path = tmp_path / "src" / f"{first_marker}.py"
    second_path = tmp_path / "src" / f"{second_marker}.py"
    first_path.parent.mkdir(exist_ok=True)
    first_path.write_text(f"# {first_marker}\n", encoding="utf-8")
    second_path.write_text(f"# {second_marker}\n", encoding="utf-8")

    packer = ContextPacker(
        workspace=tmp_path,
        rules_text=rules,
        architecture_text=architecture,
        max_total_bytes=8_000,
        max_file_bytes=1_000,
        max_active_files=1,
    )
    model = _FakeLocalModel()
    adapter = LmStudioAdapter(model_port=model)

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

    assert [request["model"] for request in model.requests] == [
        "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
        "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
        "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
        "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
    ]

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
        assert marker in rendered
        assert rules in rendered

    second_rendered = _serialized(second_request) + _serialized(second_planned_request)
    assert str(first.id) not in second_rendered
    assert first.validation_commands[0].canonical_text not in second_rendered
    assert first_marker not in second_rendered
