"""Property tests for malformed and duplicate goal-task exclusion."""

from __future__ import annotations

from pathlib import Path

from hypothesis import given, settings, strategies as st

from orchestrator.config import load_configuration
from orchestrator.markdown_parser import parse_goal_files


# Feature: stateless-turn-python-orchestrator-pipeline, Property 2: Invalid and duplicate task exclusion
# Validates: Requirements 1.3, 2.4
_MISSING_ELEMENTS = st.sampled_from(
    ("identifier", "objective", "acceptance criteria", "validation")
)
_COORDINATE = st.tuples(
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=10),
    st.integers(min_value=1, max_value=99),
)


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


def _valid_section(milestone: int, goal: int, task: int) -> str:
    return f'''### M{milestone}.G{goal}.T{task}: Valid task

**Objective:**
Create `local-ai/orchestrator/example.py`.

**Acceptance Criteria:**
- The task can be parsed.

**Prerequisites:**
- The workspace is configured.

**Implementation Details:**
Keep the implementation local.

**Validation:**
```powershell
python -m pytest local-ai/tests/test_example.py -q
```
'''


def _malformed_section(milestone: int, goal: int, task: int, missing: str) -> str:
    section = _valid_section(milestone, goal, task)
    if missing == "identifier":
        return section.replace(f"M{milestone}.G{goal}.T{task}", "not-a-task-identifier", 1)
    if missing == "objective":
        return section.replace("Create `local-ai/orchestrator/example.py`.", "", 1)
    if missing == "acceptance criteria":
        return section.replace("- The task can be parsed.", "", 1)
    return section.replace(
        "```powershell\npython -m pytest local-ai/tests/test_example.py -q\n```",
        "",
        1,
    )


@settings(max_examples=100, deadline=None)
@given(
    malformed=_MISSING_ELEMENTS,
    duplicate_id=_COORDINATE,
)
def test_invalid_and_duplicate_task_exclusion(
    tmp_path: Path,
    malformed: str,
    duplicate_id: tuple[int, int, int],
) -> None:
    """Malformed and globally duplicated tasks are never returned as queue records."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    config = load_configuration(_write_config(workspace))
    milestone, goal, task = duplicate_id
    malformed_path = workspace / ".kiro" / "specs" / "m1-invalid" / "goals" / "goal1.md"
    first_duplicate_path = workspace / ".kiro" / "specs" / f"m{milestone}-first" / "goals" / f"goal{goal}.md"
    second_duplicate_path = workspace / ".kiro" / "specs" / f"m{milestone}-second" / "goals" / f"goal{goal}.md"
    for path in (malformed_path, first_duplicate_path, second_duplicate_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    malformed_section = _malformed_section(1, 1, 1, malformed)
    first_duplicate_section = _valid_section(milestone, goal, task)
    second_duplicate_section = _valid_section(milestone, goal, task)
    malformed_path.write_text(f"# Invalid Goal\n\n{malformed_section}", encoding="utf-8")
    first_duplicate_path.write_text(f"# First Duplicate\n\n{first_duplicate_section}", encoding="utf-8")
    second_duplicate_path.write_text(f"# Second Duplicate\n\n{second_duplicate_section}", encoding="utf-8")

    outcome = parse_goal_files(
        (malformed_path, first_duplicate_path, second_duplicate_path), config
    )

    excluded_id = f"M{milestone}.G{goal}.T{task}"
    assert all(str(record.task.id) != excluded_id for record in outcome.queue)
    assert all(record.task.source_path != malformed_path.relative_to(workspace).as_posix() for record in outcome.queue)

    reports = "\n".join(path.read_text(encoding="utf-8") for path in outcome.quarantine_reports)
    assert malformed_path.relative_to(workspace).as_posix() in reports
    assert malformed_section in reports
    assert malformed in reports.lower()
    assert excluded_id in reports
    assert first_duplicate_path.relative_to(workspace).as_posix() in reports
    assert second_duplicate_path.relative_to(workspace).as_posix() in reports
    assert first_duplicate_section in reports
    assert second_duplicate_section in reports
