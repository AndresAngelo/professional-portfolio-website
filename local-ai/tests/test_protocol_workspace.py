"""Test-first examples for strict Tool Protocol parsing and workspace operations.

Task 5.6 must implement these contracts without invoking a shell.  The examples use a
real temporary workspace and define the validation, containment, mutation, and audit
boundaries required by Requirements 5.1–5.3.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from orchestrator.protocol import ProtocolValidationError, ProtocolValidator
from orchestrator.workspace import WorkspaceOperationError, WorkspaceToolExecutor


TASK_ID = "M5.G1.T1"


def operation_document(**overrides: Any) -> dict[str, Any]:
    """Build the smallest valid versioned tool operation document."""
    document: dict[str, Any] = {
        "protocol_version": "1.0",
        "task_id": TASK_ID,
        "target_path": "src/example.txt",
        "action": "write_file",
        "arguments": {"content": "created by the executor\n"},
        "expected_result": "The text fixture exists.",
    }
    document.update(overrides)
    return document


def parse(document: dict[str, Any]) -> object:
    """Parse an executor response against the active task identity."""
    return ProtocolValidator(active_task_id=TASK_ID).parse(json.dumps(document))


def executor(workspace: Path) -> WorkspaceToolExecutor:
    """Create a workspace-local executor with deletion disabled by default."""
    return WorkspaceToolExecutor(
        workspace=workspace,
        storage=workspace / "local-ai",
        delete_enabled=False,
        clock=lambda: "2026-01-01T00:00:00Z",
    )


def test_validator_accepts_only_exact_versioned_json_for_the_active_task() -> None:
    """A valid JSON object becomes a typed operation only for the selected task."""
    operation = parse(operation_document())

    assert operation.protocol_version == "1.0"
    assert operation.task_id == TASK_ID
    assert operation.target_path == "src/example.txt"
    assert operation.action == "write_file"


@pytest.mark.parametrize(
    ("document", "message"),
    [
        (operation_document(protocol_version="2.0"), "version"),
        (operation_document(task_id="M5.G1.T2"), "active task"),
        (operation_document(action="run_shell"), "action"),
        (operation_document(extra="not allowed"), "unknown"),
        ({"task_id": TASK_ID}, "required"),
    ],
)
def test_validator_rejects_wrong_version_task_action_unknown_or_missing_fields(
    document: dict[str, Any], message: str
) -> None:
    """Schema validation is strict before any workspace operation can be attempted."""
    with pytest.raises(ProtocolValidationError, match=message):
        parse(document)


@pytest.mark.parametrize("response", ["not json", "```json\n{}\n```", "[]", '"text"'])
def test_validator_rejects_non_object_or_non_json_executor_output(response: str) -> None:
    """Protocol parsing accepts exactly one JSON object and no explanatory envelope."""
    with pytest.raises(ProtocolValidationError):
        ProtocolValidator(active_task_id=TASK_ID).parse(response)


@pytest.mark.parametrize(
    "target_path",
    ["../outside.txt", "/absolute.txt", "C:/device.txt", "src/../outside.txt", "src\\windows.txt"],
)
def test_executor_rejects_noncanonical_paths_before_mutation(workspace: Path, target_path: str) -> None:
    """Traversal, absolute, device-style, and non-POSIX paths cannot escape the workspace."""
    outside = workspace.parent / "outside.txt"

    with pytest.raises(WorkspaceOperationError, match="path"):
        executor(workspace).execute(parse(operation_document(target_path=target_path)))

    assert not outside.exists()


def test_executor_rejects_symlink_target_that_resolves_outside_workspace(workspace: Path) -> None:
    """Real-path containment rejects a workspace symlink whose destination is external."""
    outside = workspace.parent / "outside"
    outside.mkdir()
    link = workspace / "linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"symlinks are unavailable in this environment: {error}")

    with pytest.raises(WorkspaceOperationError, match="workspace"):
        executor(workspace).execute(parse(operation_document(target_path="linked/escape.txt")))

    assert not (outside / "escape.txt").exists()


def test_executor_rejects_binary_existing_file_before_text_mutation(workspace: Path) -> None:
    """Text actions never overwrite bytes that are not valid UTF-8 text."""
    target = workspace / "src" / "binary.bin"
    target.parent.mkdir()
    target.write_bytes(b"\xff\x00\xfe")

    with pytest.raises(WorkspaceOperationError, match="binary"):
        executor(workspace).execute(parse(operation_document(target_path="src/binary.bin")))

    assert target.read_bytes() == b"\xff\x00\xfe"


def test_delete_action_is_rejected_when_not_explicitly_enabled(workspace: Path) -> None:
    """The schema may name delete_file, but configuration disables it by default."""
    target = workspace / "src" / "keep.txt"
    target.parent.mkdir()
    target.write_text("keep\n", encoding="utf-8")

    with pytest.raises(WorkspaceOperationError, match="delete"):
        executor(workspace).execute(
            parse(operation_document(target_path="src/keep.txt", action="delete_file", arguments={}))
        )

    assert target.read_text(encoding="utf-8") == "keep\n"


def test_write_file_is_atomic_and_records_before_after_hash_audit(workspace: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Text writes replace atomically and persist the mutation result with both hashes."""
    target = workspace / "src" / "example.txt"
    target.parent.mkdir()
    target.write_text("before\n", encoding="utf-8")
    replacements: list[tuple[Path, Path]] = []
    original_replace = os.replace

    def record_replace(source: os.PathLike[str], destination: os.PathLike[str]) -> None:
        replacements.append((Path(source), Path(destination)))
        original_replace(source, destination)

    monkeypatch.setattr(os, "replace", record_replace)
    result = executor(workspace).execute(parse(operation_document()))

    assert result.status == "completed"
    assert target.read_text(encoding="utf-8") == "created by the executor\n"
    assert any(source.parent == target.parent and destination == target for source, destination in replacements)
    records = list((workspace / "local-ai" / "protocol-records" / "M5_G1_T1").glob("*result*.json"))
    assert len(records) == 1
    audit = json.loads(records[0].read_text(encoding="utf-8"))
    assert audit["task_id"] == TASK_ID
    assert audit["action"] == "write_file"
    assert audit["resolved_path"] == "src/example.txt"
    assert audit["status"] == "completed"
    assert audit["before_hash"] is not None
    assert audit["after_hash"] is not None
    assert audit["before_hash"] != audit["after_hash"]


def test_patch_file_requires_one_unique_context_match_and_records_result(workspace: Path) -> None:
    """Patches update exactly one matching text context and reject ambiguous occurrences."""
    target = workspace / "src" / "example.txt"
    target.parent.mkdir()
    target.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    result = executor(workspace).execute(
        parse(
            operation_document(
                action="patch_file",
                arguments={"old_text": "beta", "new_text": "updated"},
            )
        )
    )

    assert result.status == "completed"
    assert target.read_text(encoding="utf-8") == "alpha\nupdated\ngamma\n"

    target.write_text("repeat\nrepeat\n", encoding="utf-8")
    with pytest.raises(WorkspaceOperationError, match="unique"):
        executor(workspace).execute(
            parse(
                operation_document(
                    action="patch_file",
                    arguments={"old_text": "repeat", "new_text": "changed"},
                )
            )
        )
    assert target.read_text(encoding="utf-8") == "repeat\nrepeat\n"


def _run(workspace: Path, **overrides: Any) -> object:
    executor = WorkspaceToolExecutor(workspace=workspace, storage=workspace / "local-ai")
    return executor.execute(parse(operation_document(**overrides)))


def test_executor_may_not_add_or_change_package_json_scripts(workspace: Path) -> None:
    """npm run executes package.json scripts, so the executor cannot create or edit them."""
    with pytest.raises(WorkspaceOperationError, match="scripts"):
        _run(
            workspace,
            target_path="package.json",
            arguments={"content": json.dumps({"name": "x", "scripts": {"test": "curl evil"}})},
        )
    assert not (workspace / "package.json").exists()

    (workspace / "package.json").write_text(json.dumps({"name": "x", "scripts": {"test": "vitest"}}), encoding="utf-8")
    with pytest.raises(WorkspaceOperationError, match="scripts"):
        _run(
            workspace,
            target_path="package.json",
            action="patch_file",
            arguments={"old_text": '"vitest"', "new_text": '"curl evil"'},
        )
    assert json.loads((workspace / "package.json").read_text(encoding="utf-8"))["scripts"] == {"test": "vitest"}


def test_executor_may_edit_other_package_json_fields_and_keep_scripts(workspace: Path) -> None:
    """Dependencies and metadata stay editable as long as the scripts block is unchanged."""
    original = {"name": "x", "scripts": {"test": "vitest"}}
    (workspace / "package.json").write_text(json.dumps(original), encoding="utf-8")

    _run(
        workspace,
        target_path="package.json",
        arguments={"content": json.dumps({**original, "description": "changed"})},
    )

    assert json.loads((workspace / "package.json").read_text(encoding="utf-8"))["description"] == "changed"


def test_package_json_with_invalid_json_is_refused_because_scripts_cannot_be_checked(workspace: Path) -> None:
    with pytest.raises(WorkspaceOperationError, match="valid JSON"):
        _run(workspace, target_path="package.json", arguments={"content": "{not json"})
