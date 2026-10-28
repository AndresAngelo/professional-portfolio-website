"""Test-first examples for observable execution modes and bounded Error recovery.

Task 6.5 must provide the mode selector and scheduler retry APIs exercised here. These
examples use temporary workspace files and durable state only; they never invoke a
model, PowerShell, Git, or network service.
"""

from __future__ import annotations

from pathlib import Path

from orchestrator.mode_selector import ModeEvidence, select_execution_mode
from orchestrator.models import ExecutionMode, TaskStatus
from orchestrator.scheduler import Scheduler
from orchestrator.state_store import AtomicStateStore

from test_state_scheduler import SCHEMA_VERSION, WORKSPACE_ID, make_state


def build_store(workspace: Path) -> AtomicStateStore:
    """Create the state store used to verify persisted mode transitions."""
    return AtomicStateStore(
        workspace=workspace,
        workspace_id=WORKSPACE_ID,
        schema_version=SCHEMA_VERSION,
    )


def test_preflight_selects_scaffold_for_an_absent_target(workspace: Path) -> None:
    """A missing active target selects Scaffold and carries its path as evidence."""
    target = workspace / "src" / "missing_module.py"

    decision = select_execution_mode(
        ModeEvidence(target_path=target, missing_imports=(), unresolved_dependencies=(), signature_mismatches=())
    )

    assert decision.mode is ExecutionMode.SCAFFOLD
    assert decision.evidence == f"target path is absent: {target.relative_to(workspace).as_posix()}"


def test_preflight_selects_aligner_for_import_dependency_or_signature_mismatch(
    workspace: Path,
) -> None:
    """Any observed import, dependency, or signature mismatch selects Aligner."""
    target = workspace / "src" / "existing.py"
    target.parent.mkdir()
    target.write_text("def current(value: str) -> str:\n    return value\n", encoding="utf-8")

    for evidence in (
        ModeEvidence(target_path=target, missing_imports=("from app.types import Missing",)),
        ModeEvidence(target_path=target, unresolved_dependencies=("declared dependency: httpx",)),
        ModeEvidence(target_path=target, signature_mismatches=("expected render(data: Data)",)),
    ):
        decision = select_execution_mode(evidence)
        assert decision.mode is ExecutionMode.ALIGNER
        assert decision.evidence


def test_preflight_selects_cot_task_for_a_healthy_existing_target(workspace: Path) -> None:
    """An existing target with no observed mismatch selects CoT-Task."""
    target = workspace / "src" / "healthy.py"
    target.parent.mkdir()
    target.write_text("VALUE = 'healthy'\n", encoding="utf-8")

    decision = select_execution_mode(ModeEvidence(target_path=target))

    assert decision.mode is ExecutionMode.COT_TASK
    assert decision.evidence == "existing target has no observed alignment mismatch"


def test_nonzero_validation_selects_error_and_persists_exact_failure_context(
    workspace: Path,
) -> None:
    """Only non-zero validation creates Error mode with unmodified stderr and exit code."""
    store = build_store(workspace)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    task = scheduler.select_next()
    stderr = "tests/test_example.py:42: assertion failed\nexpected: 0\nactual: 1\n"

    error_context = scheduler.record_validation_failure(
        task_id=task.id,
        command="python -m pytest tests/test_example.py -q",
        stdout="one failed\n",
        stderr=stderr,
        exit_code=1,
        artifact_path="local-ai/validation/M1_G1_T1/001.json",
    )

    record = store.load().task_records[str(task.id)]
    assert error_context.mode is ExecutionMode.ERROR
    assert error_context.stderr == stderr
    assert error_context.exit_code == 1
    assert record.status is TaskStatus.IN_PROGRESS
    assert record.mode_history == [ExecutionMode.ERROR]
    assert record.error_mode_requests == 0


def test_retry_success_completes_with_exact_error_request_count(workspace: Path) -> None:
    """The Error request count increments before each retry and remains exact on success."""
    store = build_store(workspace)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    task = scheduler.select_next()
    scheduler.record_validation_failure(
        task_id=task.id,
        command="python -m pytest tests/test_example.py -q",
        stdout="",
        stderr="first failure",
        exit_code=1,
        artifact_path="local-ai/validation/M1_G1_T1/001.json",
    )

    retry = scheduler.begin_error_mode_request(task_id=task.id)
    assert retry.mode is ExecutionMode.ERROR
    assert retry.request_number == 1
    assert store.load().task_records[str(task.id)].error_mode_requests == 1

    scheduler.complete(
        task_id=task.id,
        validation_results=[{"exit_code": 0, "artifact_path": "local-ai/validation/M1_G1_T1/002.json"}],
    )
    record = store.load().task_records[str(task.id)]
    assert record.status is TaskStatus.COMPLETED
    assert record.error_mode_requests == 1


def test_three_persistent_failures_preserve_workspace_and_create_complete_report(
    workspace: Path,
) -> None:
    """A third Error-mode failure quarantines with evidence and never rolls back edits."""
    source = workspace / "src" / "preserved.py"
    source.parent.mkdir()
    source.write_text("PARTIAL_CHANGE = True\n", encoding="utf-8")
    store = build_store(workspace)
    store.commit(make_state(queued_task_numbers=(1,)))
    scheduler = Scheduler(store)
    task = scheduler.select_next()

    for attempt in range(1, 4):
        scheduler.record_validation_failure(
            task_id=task.id,
            command="python -m pytest tests/test_example.py -q",
            stdout=f"attempt {attempt} stdout",
            stderr=f"attempt {attempt} stderr",
            exit_code=attempt,
            artifact_path=f"local-ai/validation/M1_G1_T1/{attempt:03d}.json",
        )
        scheduler.begin_error_mode_request(task_id=task.id)

    report_path = scheduler.quarantine_after_retry_limit(
        task_id=task.id,
        changed_workspace_paths=["src/preserved.py"],
    )

    record = store.load().task_records[str(task.id)]
    report = report_path.read_text(encoding="utf-8")
    assert source.read_text(encoding="utf-8") == "PARTIAL_CHANGE = True\n"
    assert record.status is TaskStatus.QUARANTINED
    assert record.error_mode_requests == 3
    assert record.changed_workspace_paths == ["src/preserved.py"]
    assert record.quarantine_report_path == report_path.relative_to(workspace).as_posix()
    assert "M1.G1.T1" in report
    assert "Error → Error → Error" in report
    assert "python -m pytest tests/test_example.py -q" in report
    assert "attempt 3 stdout" in report
    assert "attempt 3 stderr" in report
    assert "3" in report
    assert "src/preserved.py" in report
    assert "Recovery" in report
