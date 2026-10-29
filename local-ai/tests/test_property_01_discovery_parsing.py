"""Property tests for eligible goal discovery and faithful Markdown parsing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.config import load_configuration
from orchestrator.discovery import discover_goal_files
from orchestrator.markdown_parser import parse_goal_file


# Feature: stateless-turn-python-orchestrator-pipeline, Property 1: Eligible goal discovery and faithful parsing
# Validates: Requirements 1.1, 1.2, 1.4, 2.1
_IDENTIFIER = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-",
    min_size=1,
    max_size=16,
)
_COORDINATE = st.tuples(
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=10),
)


@dataclass(frozen=True)
class ExpectedTask:
    """The source fields a successful parser must preserve exactly."""

    task_number: int
    title: str
    objective: str
    acceptance_criteria: tuple[str, ...]
    prerequisites: tuple[str, ...]
    implementation_details: str
    validation_command: str


@dataclass(frozen=True)
class ExpectedGoalFile:
    """A generated eligible goal file and its expected parsed tasks."""

    milestone: int
    goal: int
    tasks: tuple[ExpectedTask, ...]


@st.composite
def _eligible_goal_layouts(draw: st.DrawFn) -> tuple[ExpectedGoalFile, ...]:
    coordinates = draw(
        st.lists(_COORDINATE, min_size=1, max_size=12, unique=True)
    )
    goal_files: list[ExpectedGoalFile] = []

    for milestone, goal in coordinates:
        task_count = draw(st.integers(min_value=1, max_value=4))
        task_numbers = draw(
            st.lists(
                st.integers(min_value=1, max_value=99),
                min_size=task_count,
                max_size=task_count,
                unique=True,
            )
        )
        tasks: list[ExpectedTask] = []
        for task_number in task_numbers:
            title = draw(_IDENTIFIER)
            objective = draw(_IDENTIFIER)
            criterion = draw(_IDENTIFIER)
            prerequisite = draw(_IDENTIFIER)
            implementation = draw(_IDENTIFIER)
            command_target = draw(_IDENTIFIER)
            tasks.append(
                ExpectedTask(
                    task_number=task_number,
                    title=title,
                    objective=objective,
                    acceptance_criteria=(criterion,),
                    prerequisites=(prerequisite,),
                    implementation_details=implementation,
                    validation_command=f"python -m pytest local-ai/tests/{command_target}.py -q",
                )
            )
        goal_files.append(ExpectedGoalFile(milestone, goal, tuple(tasks)))

    return tuple(goal_files)


def _write_config(workspace: Path) -> Path:
    config_path = workspace / "local-ai" / "config" / "orchestrator.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        f'''[workspace]
root = "{workspace.as_posix()}"
spec_root = ".kiro/specs"
local_storage = "local-ai"

[discovery]
enabled_milestones = [1, 2, 3, 4, 5]
future_milestones = [6, 7, 8, 9, 10]
goal_glob = "m{{milestone}}-*/goals/goal{{goal}}.md"
required_goal_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

[legacy_instruction_migration]
accepted_root_aliases = ["{(workspace / 'personal-website-portfolio-v2').as_posix()}"]
tracker_path = "local-ai/program-states/progress-tracker.md"
tracker_mode = "orchestrator-owned"

[lm_studio]
base_url = "http://127.0.0.1:1234/v1"
request_timeout_seconds = 120
allow_loopback_only = true

[lm_studio.models.embedding]
model_id = "embed-text-embedding-nomic-embed-text-v1.5"
context_length = 2048
output_reserve_tokens = 0
max_prompt_bytes = 8192

[lm_studio.models.router]
model_id = "1b-gemma-3-1b-it-qat"
context_length = 2048
output_reserve_tokens = 512
max_prompt_bytes = 6144

[lm_studio.models.executor]
model_id = "1b-gemma-4-e2b-it-qat"
context_length = 4096
output_reserve_tokens = 1024
max_prompt_bytes = 12288

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


def _goal_markdown(goal_file: ExpectedGoalFile) -> str:
    sections = [f"# M{goal_file.milestone}.G{goal_file.goal}: Generated Goal"]
    for task in goal_file.tasks:
        sections.append(
            f'''### M{goal_file.milestone}.G{goal_file.goal}.T{task.task_number}: {task.title}

**Objective:** {task.objective}

**Acceptance Criteria:**
- {task.acceptance_criteria[0]}

**Prerequisites:**
- {task.prerequisites[0]}

**Implementation Details:**
{task.implementation_details}

**Validation:**
```powershell
{task.validation_command}
```
'''
        )
    return "\n".join(sections)


@settings(max_examples=100, deadline=None)
@given(goal_files=_eligible_goal_layouts())
def test_eligible_goal_discovery_and_faithful_parsing(
    tmp_path_factory: pytest.TempPathFactory,
    goal_files: tuple[ExpectedGoalFile, ...],
) -> None:
    """Discover valid M1–M5 files numerically and preserve all task source fields."""
    tmp_path = tmp_path_factory.mktemp("discovery")
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    config = load_configuration(_write_config(workspace))
    expected_by_path: dict[Path, ExpectedGoalFile] = {}

    for goal_file in goal_files:
        path = (
            workspace
            / ".kiro"
            / "specs"
            / f"m{goal_file.milestone}-generated"
            / "goals"
            / f"goal{goal_file.goal}.md"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_goal_markdown(goal_file), encoding="utf-8")
        expected_by_path[path.resolve()] = goal_file

    discovered = discover_goal_files(config)
    assert discovered == sorted(
        expected_by_path,
        key=lambda path: (
            expected_by_path[path].milestone,
            expected_by_path[path].goal,
            path.as_posix(),
        ),
    )

    first_hashes: dict[Path, str] = {}
    for source_path in discovered:
        expected_file = expected_by_path[source_path]
        parsed_once = parse_goal_file(source_path, config)
        parsed_twice = parse_goal_file(source_path, config)
        expected_tasks = sorted(expected_file.tasks, key=lambda task: task.task_number)

        assert [task.id.task for task in parsed_once] == [task.task_number for task in expected_tasks]
        assert [task.id.milestone for task in parsed_once] == [expected_file.milestone] * len(expected_tasks)
        assert [task.id.goal for task in parsed_once] == [expected_file.goal] * len(expected_tasks)
        assert [task.source_path for task in parsed_once] == [
            source_path.relative_to(workspace).as_posix()
        ] * len(expected_tasks)
        assert [task.source_hash for task in parsed_once] == [
            task.source_hash for task in parsed_twice
        ]

        for parsed, expected_task in zip(parsed_once, expected_tasks, strict=True):
            assert parsed.heading == expected_task.title
            assert parsed.objective == expected_task.objective
            assert parsed.acceptance_criteria == expected_task.acceptance_criteria
            assert parsed.prerequisites == expected_task.prerequisites
            assert parsed.implementation_details == expected_task.implementation_details
            assert tuple(command.raw_text for command in parsed.validation_commands) == (
                expected_task.validation_command,
            )
            assert tuple(command.canonical_text for command in parsed.validation_commands) == (
                expected_task.validation_command,
            )
        first_hashes[source_path] = parsed_once[0].source_hash

    changed_source = discovered[0]
    changed_source.write_text(changed_source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    changed_hashes = [task.source_hash for task in parse_goal_file(changed_source, config)]
    assert changed_hashes
    assert all(source_hash != first_hashes[changed_source] for source_hash in changed_hashes)
