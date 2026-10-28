"""Offline integration coverage for the fake local LM Studio pipeline.

**Validates: Requirements 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.5, 5.1, 5.4, 6.2, 8.1, 9.1**

The tests compose real discovery, state, protocol, workspace, and validation code with
in-memory model/process seams. They never start a model, shell, network connection, Git
command, or dependency installation.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from orchestrator.config import load_configuration
from orchestrator.discovery import discover_goal_files
from orchestrator.lm_studio import LmStudioAdapter, ModelRequestError
from orchestrator.markdown_parser import parse_goal_files
from orchestrator.models import RunState, TaskRunRecord, TaskStatus
from orchestrator.powershell import CommandResult, PowerShellRunner
from orchestrator.protocol import ProtocolProcessor, ProtocolQuarantineResult
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore
from orchestrator.validation import OrderedValidator
from orchestrator.workspace import WorkspaceToolExecutor


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ID = "fake-lm-integration"
SCHEMA_VERSION = 1


@dataclass
class FakeLocalModel:
    """Records mode-driven local model requests without opening a network connection."""

    responses: list[Any]
    calls: list[dict[str, Any]]

    def request(self, *, payload: dict[str, Any]) -> Any:
        self.calls.append({"model": payload["model"], "payload": payload})
        if not self.responses:
            raise AssertionError("No fake LM response was configured.")
        return self.responses.pop(0)


@dataclass
class FakeProcess:
    """A process seam that records validation but never launches PowerShell."""

    results: list[CommandResult]
    calls: list[dict[str, Any]]

    def run(self, *, argv: list[str], cwd: Path, environment: dict[str, str]) -> CommandResult:
        self.calls.append({"argv": argv, "cwd": cwd, "environment": environment})
        return self.results.pop(0)


def write_config(workspace: Path) -> Path:
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
accepted_root_aliases = ["{(workspace / 'legacy-root').as_posix()}"]
tracker_path = "local-ai/program-states/progress-tracker.md"
tracker_mode = "orchestrator-owned"

[lm_studio]
base_url = "http://127.0.0.1:1234/v1"
model_id = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"
request_timeout_seconds = 1
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


def write_goal(workspace: Path, *, milestone: int = 1, task: int = 1) -> Path:
    path = workspace / ".kiro" / "specs" / f"m{milestone}-fixture" / "goals" / "goal1.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'''### M{milestone}.G1.T{task}: Create integration output

**Objective:**
Create `src/generated.txt` using the protocol.

**Acceptance Criteria:**
- The generated file contains the fake executor output.

**Prerequisites:**
- The fake LM is available.

**Implementation Details:**
Write `src/generated.txt` without a shell.

**Validation:**
```powershell
python -m pytest local-ai/tests/test_integration_fake_lm_studio.py -q
```
''',
        encoding="utf-8",
    )
    return path


def copy_m5_goals(workspace: Path) -> None:
    source = REPOSITORY_ROOT / ".kiro" / "specs" / "m5-homepage-experience" / "goals"
    destination = workspace / ".kiro" / "specs" / "m5-homepage-experience" / "goals"
    destination.mkdir(parents=True, exist_ok=True)
    for number in range(1, 11):
        shutil.copyfile(source / f"goal{number}.md", destination / f"goal{number}.md")


def initialized_pipeline(workspace: Path) -> tuple[object, AtomicStateStore, Scheduler]:
    config = load_configuration(write_config(workspace))
    copy_m5_goals(workspace)
    write_goal(workspace)
    write_goal(workspace, milestone=6)
    discovered = discover_goal_files(config)
    assert len([path for path in discovered if "m5-homepage-experience" in path.as_posix()]) == 10
    assert all("m6-" not in path.as_posix() for path in discovered)
    parsed = parse_goal_files([path for path in discovered if "m1-fixture" in path.as_posix()], config)
    queue = list(parsed.queue)
    state = RunState(
        schema_version=SCHEMA_VERSION,
        workspace_id=WORKSPACE_ID,
        queue=queue,
        task_records={str(record.task.id): TaskRunRecord(task_id=record.task.id, status=TaskStatus.QUEUED) for record in queue},
        active_task_id=None,
        updated_at="2026-01-01T00:00:00Z",
    )
    store = AtomicStateStore(workspace=workspace, workspace_id=WORKSPACE_ID, schema_version=SCHEMA_VERSION)
    store.commit(state)
    return config, store, Scheduler(store)


def operation(task_id: str) -> str:
    return json.dumps({"protocol_version": "1.0", "task_id": task_id, "target_path": "src/generated.txt", "action": "write_file", "arguments": {"content": "created by fake executor\n"}, "expected_result": "generated output exists"})


def test_fake_lm_completes_discovered_task_with_ordered_validation_and_confined_artifacts(workspace: Path) -> None:
    """Fresh mode-driven turns mutate locally and complete only after validation."""
    config, store, scheduler = initialized_pipeline(workspace)
    selected = scheduler.select_next()
    fake_lm = FakeLocalModel(responses=[{"plan": "write output"}, operation(str(selected.id))], calls=[])
    adapter = LmStudioAdapter(model_port=fake_lm)

    assert adapter.request({"task_id": str(selected.id), "mode": "Scaffold"}) == {"plan": "write output"}
    executor_response = adapter.request({"task_id": str(selected.id), "mode": "CoT-Task"})
    result = ProtocolProcessor(workspace, store.load(), WorkspaceToolExecutor(workspace, workspace / "local-ai")).process_executor_output(executor_response)
    assert result.status == "completed"

    fake_process = FakeProcess(results=[CommandResult("first\n", "", 0)], calls=[])
    records = OrderedValidator(task_id=selected.id, workspace=workspace, runner=PowerShellRunner(process_runner=fake_process, workspace=workspace)).run(selected.validation_commands)
    scheduler.complete(task_id=selected.id, validation_results=[{"exit_code": record.exit_code, "artifact_path": record.artifact_path} for record in records])

    completed = store.load()
    assert completed.active_task_id is None
    assert completed.task_records[str(selected.id)].status is TaskStatus.COMPLETED
    assert [call["model"] for call in fake_lm.calls] == [config.lm_studio.model_id, config.lm_studio.model_id]
    assert [call["argv"][-1] for call in fake_process.calls] == [selected.validation_commands[0].canonical_text]
    assert (workspace / "src" / "generated.txt").read_text(encoding="utf-8") == "created by fake executor\n"
    assert not list(workspace.rglob(".git"))
    assert all(path.resolve().is_relative_to(workspace.resolve()) for path in (workspace / "local-ai").rglob("*"))


def test_resume_protocol_quarantine_and_transport_failure_preserve_active_task_and_changes(workspace: Path) -> None:
    """Resume wins over queued work while invalid protocol and offline fake transport retain evidence."""
    config, store, scheduler = initialized_pipeline(workspace)
    selected = scheduler.select_next()
    assert Scheduler(store).select_next().id == selected.id
    preserved = workspace / "src" / "partial.txt"
    preserved.parent.mkdir()
    preserved.write_text("keep me\n", encoding="utf-8")

    quarantine = ProtocolProcessor(workspace, store.load(), WorkspaceToolExecutor(workspace, workspace / "local-ai")).process_executor_output("not protocol JSON")
    assert isinstance(quarantine, ProtocolQuarantineResult)
    assert store.load().task_records[str(selected.id)].status is TaskStatus.IN_PROGRESS
    assert preserved.read_text(encoding="utf-8") == "keep me\n"

    class OfflineTransport:
        def request(self, **_kwargs: Any) -> dict[str, Any]:
            raise ConnectionError("offline fake LM")

    offline = LmStudioAdapter(config=config.lm_studio, storage=workspace / "local-ai", transport=OfflineTransport())
    with pytest.raises(ModelRequestError):
        offline.request({"context": {"active_task_scope": {"task_id": str(selected.id)}}})

    assert store.load().active_task_id == str(selected.id)
    assert preserved.read_text(encoding="utf-8") == "keep me\n"
    assert list((workspace / "local-ai" / "quarantine").glob("*invalid-protocol.md"))
    assert list((workspace / "local-ai" / "protocol-records" / "M1_G1_T1").glob("*request-error*.json"))
