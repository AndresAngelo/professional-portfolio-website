"""Free-text executor replies become Tool Protocol operations. Python checks every path."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orchestrator.pipeline import MAX_FILES_PER_REPLY, ExecutorReplyError, ingest_executor_reply
from orchestrator.protocol import ProtocolValidator
from orchestrator.workspace import WorkspaceOperationError, WorkspaceToolExecutor

TASK = "M5.G1.T1"


def _file(path: str, body: str) -> str:
    return f"FILE: {path}\n```ts\n{body}\n```\n"


def test_fenced_block_becomes_one_write_file_with_its_exact_body() -> None:
    operations = ingest_executor_reply(_file("tests/fixtures/home-data.ts", "export const x = 1;"), TASK)

    assert len(operations) == 1
    assert operations[0]["action"] == "write_file"
    assert operations[0]["target_path"] == "tests/fixtures/home-data.ts"
    assert operations[0]["arguments"]["content"] == "export const x = 1;\n"


def test_several_blocks_become_several_operations_in_order() -> None:
    reply = "Notes first.\n" + _file("src/a.ts", "a") + "\n" + _file("src/b.ts", "b")

    targets = [op["target_path"] for op in ingest_executor_reply(reply, TASK)]

    assert targets == ["src/a.ts", "src/b.ts"]


def test_backticked_path_and_latex_and_raw_newlines_survive_untouched() -> None:
    body = "/** $\\ge$ 18.0.0 */\nconst s = `template`;"
    reply = "FILE: `src/lib/x.ts`\n```ts\n" + body + "\n```"

    operations = ingest_executor_reply(reply, TASK)

    assert operations[0]["target_path"] == "src/lib/x.ts"
    assert operations[0]["arguments"]["content"] == body + "\n"


def test_whole_text_protocol_json_is_used_as_is() -> None:
    document = {
        "protocol_version": "1.0", "task_id": TASK, "target_path": "src/a.ts", "action": "write_file",
        "arguments": {"content": "a"}, "expected_result": "done",
    }

    assert ingest_executor_reply(json.dumps(document), TASK) == [document]


def test_free_text_becomes_a_note_at_the_task_notes_path() -> None:
    operations = ingest_executor_reply("Versions verified.", TASK)

    assert operations[0]["target_path"] == f"local-ai/notes/{TASK}.md"
    assert "Versions verified." in operations[0]["arguments"]["content"]


def test_reasoning_or_prose_outside_blocks_is_discarded() -> None:
    reply = "Thinking: the user wants X.\n" + _file("src/a.ts", "a") + "\nClosing remark."

    operations = ingest_executor_reply(reply, TASK)

    assert len(operations) == 1
    assert "Thinking" not in operations[0]["arguments"]["content"]
    assert "Closing remark" not in operations[0]["arguments"]["content"]


@pytest.mark.parametrize("reply", ["", "   \n\t  ", "\xa0"])
def test_empty_reply_is_refused(reply: str) -> None:
    with pytest.raises(ExecutorReplyError, match="empty"):
        ingest_executor_reply(reply, TASK)


def test_file_header_without_a_complete_fenced_block_is_refused() -> None:
    with pytest.raises(ExecutorReplyError, match="FILE"):
        ingest_executor_reply("FILE: src/a.ts\nexport const a = 1;", TASK)


def test_more_than_the_file_limit_is_refused() -> None:
    reply = "".join(_file(f"src/f{i}.ts", str(i)) for i in range(MAX_FILES_PER_REPLY + 1))

    with pytest.raises(ExecutorReplyError, match="limit"):
        ingest_executor_reply(reply, TASK)


def test_exactly_the_file_limit_is_accepted() -> None:
    reply = "".join(_file(f"src/f{i}.ts", str(i)) for i in range(MAX_FILES_PER_REPLY))

    assert len(ingest_executor_reply(reply, TASK)) == MAX_FILES_PER_REPLY


def test_each_ingested_operation_passes_the_strict_protocol_validator() -> None:
    for operation in ingest_executor_reply(_file("src/a.ts", "a") + _file("src/b.ts", "b"), TASK):
        ProtocolValidator(active_task_id=TASK).parse(json.dumps(operation))


@pytest.mark.parametrize("escape", ["../outside.ts", "/etc/passwd", "C:/Windows/system.ini"])
def test_paths_that_leave_the_workspace_are_refused_by_the_tool_executor(workspace: Path, escape: str) -> None:
    executor = WorkspaceToolExecutor(workspace=workspace, storage=workspace / "local-ai")
    operation = ingest_executor_reply(_file(escape, "x"), TASK)[0]

    with pytest.raises(WorkspaceOperationError):
        executor.execute(ProtocolValidator(active_task_id=TASK).parse(json.dumps(operation)))
    assert not (workspace.parent / "outside.ts").exists()


def test_package_json_scripts_cannot_be_changed_through_a_file_block(workspace: Path) -> None:
    (workspace / "package.json").write_text(json.dumps({"scripts": {"test": "vitest"}}), encoding="utf-8")
    executor = WorkspaceToolExecutor(workspace=workspace, storage=workspace / "local-ai")
    tampered = json.dumps({"scripts": {"test": "curl evil"}})

    operation = ingest_executor_reply(_file("package.json", tampered), TASK)[0]
    with pytest.raises(WorkspaceOperationError, match="scripts"):
        executor.execute(ProtocolValidator(active_task_id=TASK).parse(json.dumps(operation)))
