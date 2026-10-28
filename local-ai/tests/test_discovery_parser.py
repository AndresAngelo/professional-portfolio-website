"""Examples defining configured goal discovery and faithful Markdown task parsing."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest

from orchestrator.config import load_configuration
from orchestrator.discovery import discover_goal_files
from orchestrator.markdown_parser import MarkdownParseError, parse_goal_file


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
M5_GOALS_SOURCE = (
    REPOSITORY_ROOT / ".kiro" / "specs" / "m5-homepage-experience" / "goals"
)


def write_config(workspace: Path) -> Path:
    """Write the configured M1–M5 discovery policy for a temporary workspace."""
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
model_id = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"
request_timeout_seconds = 120
allow_loopback_only = true

[context]
max_total_bytes = 120000
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


def write_goal_file(
    workspace: Path,
    *,
    milestone: int,
    goal: int,
    task: int,
    title: str = "Create a parser contract",
    validation_preamble: str = "",
) -> Path:
    """Create a complete synthetic M1–M4 goal task with all parser fields."""
    goal_path = (
        workspace
        / ".kiro"
        / "specs"
        / f"m{milestone}-synthetic"
        / "goals"
        / f"goal{goal}.md"
    )
    goal_path.parent.mkdir(parents=True, exist_ok=True)
    goal_path.write_text(
        f'''# M{milestone}.G{goal}: Synthetic Goal

### M{milestone}.G{goal}.T{task}: {title}

**Objective:**
Create the parser-facing module at `local-ai/orchestrator/example.py`.

**Acceptance Criteria:**
- The parser preserves each declared task field.
- The parser records canonical validation commands.

**Prerequisites:**
- The configuration contract is loaded.
- The workspace is available.

**Implementation Details:**
Update `local-ai/orchestrator/example.py` without network access.

**Validation:**
```powershell
{validation_preamble}python -m pytest local-ai/tests/test_example.py -q
```
''',
        encoding="utf-8",
    )
    return goal_path


def copy_populated_m5_goals(workspace: Path) -> list[Path]:
    """Copy the approved populated M5 source set into an isolated workspace."""
    copied: list[Path] = []
    destination = workspace / ".kiro" / "specs" / "m5-homepage-experience" / "goals"
    destination.mkdir(parents=True, exist_ok=True)
    for goal_number in range(1, 11):
        source = M5_GOALS_SOURCE / f"goal{goal_number}.md"
        target = destination / source.name
        shutil.copyfile(source, target)
        copied.append(target)
    return copied


def test_discovery_includes_only_non_empty_configured_goal_files(workspace: Path) -> None:
    """M1–M5 populated goal files are discoverable; empty and disabled files are not."""
    config = load_configuration(write_config(workspace))
    m5_goals = copy_populated_m5_goals(workspace)
    m1_goal = write_goal_file(workspace, milestone=1, goal=2, task=10)
    m4_goal = write_goal_file(workspace, milestone=4, goal=10, task=1)
    empty_goal = workspace / ".kiro" / "specs" / "m2-empty" / "goals" / "goal1.md"
    empty_goal.parent.mkdir(parents=True, exist_ok=True)
    empty_goal.write_text("  \n", encoding="utf-8")
    disabled_goal = write_goal_file(workspace, milestone=6, goal=1, task=1)

    discovered = discover_goal_files(config)

    assert discovered == [m1_goal, m4_goal, *m5_goals]
    assert empty_goal not in discovered
    assert disabled_goal not in discovered


def test_parser_preserves_all_task_fields_and_source_hash(workspace: Path) -> None:
    """A complete task becomes a typed record with a hash of the exact source bytes."""
    config = load_configuration(write_config(workspace))
    goal_path = write_goal_file(workspace, milestone=3, goal=2, task=7)
    source = goal_path.read_text(encoding="utf-8")

    parsed_tasks = parse_goal_file(goal_path, config)

    assert len(parsed_tasks) == 1
    parsed = parsed_tasks[0]
    assert str(parsed.id) == "M3.G2.T7"
    assert parsed.source_path == ".kiro/specs/m3-synthetic/goals/goal2.md"
    assert parsed.source_hash == hashlib.sha256(source.encode("utf-8")).hexdigest()
    assert parsed.heading == "Create a parser contract"
    assert parsed.objective == "Create the parser-facing module at `local-ai/orchestrator/example.py`."
    assert parsed.acceptance_criteria == (
        "The parser preserves each declared task field.",
        "The parser records canonical validation commands.",
    )
    assert parsed.prerequisites == (
        "The configuration contract is loaded.",
        "The workspace is available.",
    )
    assert parsed.implementation_details == "Update `local-ai/orchestrator/example.py` without network access."
    assert parsed.validation_commands[0].raw_text == "python -m pytest local-ai/tests/test_example.py -q"
    assert parsed.validation_commands[0].canonical_text == "python -m pytest local-ai/tests/test_example.py -q"
    assert parsed.validation_commands[0].ordinal == 1


def test_parser_canonicalizes_only_the_configured_leading_legacy_cd(workspace: Path) -> None:
    """Configured historical roots are retained as raw evidence and removed canonically."""
    config = load_configuration(write_config(workspace))
    alias = f'cd "{(workspace / "personal-website-portfolio-v2").as_posix()}"\n'
    goal_path = write_goal_file(
        workspace,
        milestone=2,
        goal=1,
        task=1,
        validation_preamble=alias,
    )

    parsed = parse_goal_file(goal_path, config)[0]
    command = parsed.validation_commands[0]

    assert command.raw_text == f'{alias}python -m pytest local-ai/tests/test_example.py -q'
    assert command.canonical_text == "python -m pytest local-ai/tests/test_example.py -q"


@pytest.mark.parametrize(
    "preamble",
    [
        'cd "C:/unrecognized/repository"\n',
        "cd ..\n",
    ],
)
def test_parser_rejects_unrecognized_validation_roots(workspace: Path, preamble: str) -> None:
    """Only exact configured aliases may be canonicalized; other roots are unsafe."""
    config = load_configuration(write_config(workspace))
    goal_path = write_goal_file(
        workspace,
        milestone=1,
        goal=1,
        task=1,
        validation_preamble=preamble,
    )

    with pytest.raises(MarkdownParseError, match="(?:unrecognized|legacy|root|cd)"):
        parse_goal_file(goal_path, config)
