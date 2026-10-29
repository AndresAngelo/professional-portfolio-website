"""Four-pass task pipeline: retrieval, router, executor with declared validation, auditor.

Each pass is a fresh, history-free request. Pydantic retries (router, auditor) and Error-mode
executor requests use separate budgets. Every model request is ledgered as a ModelTurn.

The executor is not schema-constrained. Its reply is free text, and Python turns it into
Tool Protocol operations (see ``ingest_executor_reply``). Python checks every file path, and
validation and audit still decide whether the task passes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import Any

from .command_guard import CommandAuthorizationError
from .context_packer import ContextPacker, PromptBudgetError, build_messages, pack_router_prompt
from .lm_studio import ModelRequestError
from .mode_selector import ModeSelector, PreflightEvidence
from .models import ExecutionMode, GoalTask
from .protocol import ProtocolProcessor, ProtocolQuarantineResult
from .quarantine import write_state_quarantine_report
from .scheduler import Scheduler, StateExecutionRefused
from .schemas import AuditReport, RouterPlan
from .structured import StructuredOutputError, structured_call
from .validation import ValidationRecord
from .workspace import WorkspaceOperationError

STDERR_EXCERPT_BYTES = 1000
AUDIT_FILE_BYTES = 2000
MAX_FILES_PER_REPLY = 5
NOTE_PATH_TEMPLATE = "local-ai/notes/{task_id}.md"

# A FILE block: a header line ``FILE: <path>`` (backticks around the path are optional), then one
# fenced block whose body is the complete file content.
FILE_BLOCK = re.compile(
    r"^FILE:[ \t]*`?(?P<path>[^\s`]+)`?[ \t]*\r?\n```[^\n]*\r?\n(?P<body>.*?)\r?\n```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


class ExecutorReplyError(ValueError):
    """The executor reply cannot be turned into file operations, so the task must be quarantined."""


@dataclass(frozen=True)
class Retrieval:
    """Pass 1 result: ranked chunks (best first) and the embedding request that produced them."""

    chunks: list[dict[str, str]]
    request_id: str | None = None
    model_id: str | None = None


@dataclass
class PipelineDeps:
    scheduler: Scheduler
    adapter: Any  # chat(), last_request_id, last_model_id
    workspace: Path
    packer: ContextPacker  # executor-budget packer
    router_budget: int
    router_system_text: str
    auditor_system_text: str
    retrieve: Callable[[str], Retrieval]
    tool_executor: Any
    validate: Callable[[GoalTask], list[ValidationRecord]]


@dataclass(frozen=True)
class PipelineResult:
    task_id: str
    status: str  # "completed" | "quarantined"
    detail: str
    error_mode_requests: int = 0
    notes: tuple[str, ...] = field(default_factory=tuple)


def _scope(task: GoalTask) -> dict[str, Any]:
    return {
        "task_id": str(task.id),
        "heading": task.heading,
        "objective": task.objective,
        "acceptance_criteria": list(task.acceptance_criteria),
        "implementation_details": task.implementation_details,
        "validation_commands": [c.canonical_text for c in task.validation_commands],
    }


def _write_operation(task_id: str, target_path: str, content: str) -> dict[str, Any]:
    return {
        "protocol_version": "1.0",
        "task_id": task_id,
        "target_path": target_path,
        "action": "write_file",
        "arguments": {"content": content},
        "expected_result": f"{target_path} written with the executor's content.",
    }


def ingest_executor_reply(raw_text: str, task_id: str) -> list[dict[str, Any]]:
    """Turn one free-text executor reply into Tool Protocol operations, in the order they appear.

    Accepted forms, checked in this order:

    1. The whole reply is one Tool Protocol JSON object (has an ``action`` key). It is used as-is,
       and ProtocolValidator still checks its fields.
    2. One or more ``FILE: <path>`` headers, each followed by a fenced block with the full file body.
       Each block becomes its own write_file operation. Prose outside the blocks is discarded.
    3. Free text with no ``FILE:`` header. It is written as a note at ``local-ai/notes/<task_id>.md``.

    Raises :class:`ExecutorReplyError` for an empty reply, a ``FILE:`` header with no complete
    fenced block, or more than ``MAX_FILES_PER_REPLY`` blocks. Reasoning text is not part of
    ``raw_text`` and is never written.
    """
    text = raw_text.replace("\xa0", " ").strip()
    if not text:
        raise ExecutorReplyError("executor reply is empty")

    if text.startswith("{"):
        try:
            document = json.loads(text, strict=False)
        except ValueError:
            document = None
        if isinstance(document, dict) and "action" in document:
            return [document]

    blocks = list(FILE_BLOCK.finditer(text))
    if blocks:
        if len(blocks) > MAX_FILES_PER_REPLY:
            raise ExecutorReplyError(
                f"executor reply has {len(blocks)} FILE blocks; the limit is {MAX_FILES_PER_REPLY}"
            )
        return [_write_operation(task_id, match.group("path"), match.group("body") + "\n") for match in blocks]

    if "FILE:" in text:
        raise ExecutorReplyError("a FILE: header has no complete fenced block after it")

    return [
        _write_operation(
            task_id,
            NOTE_PATH_TEMPLATE.format(task_id=task_id),
            f"# Execution note for {task_id}\n\n{text}\n",
        )
    ]


def run_task(deps: PipelineDeps, task: GoalTask) -> PipelineResult:
    """Run one already-selected active task to completion or quarantine.

    Transport failures propagate and leave the task in progress so a later resume reuses it.
    """
    scheduler, adapter = deps.scheduler, deps.adapter
    changed: list[str] = []

    def ledger(pass_name: str, role: str, model_id: str | None, request_id: str | None, attempt: int,
               mode: str | None, outcome: str) -> None:
        if model_id and request_id:
            scheduler.record_model_turn(
                task_id=task.id, pass_name=pass_name, role=role, model_id=model_id, attempt=attempt,
                mode=mode, request_id=request_id, outcome=outcome,
            )

    def quarantine(category: str, detail: str, evidence: str | None = None) -> PipelineResult:
        report = write_state_quarantine_report(
            workspace=deps.workspace, category=category, detail=f"{task.id}: {detail}", evidence=evidence
        )
        scheduler.quarantine_task(task_id=task.id, report_path=report, changed_workspace_paths=changed)
        return PipelineResult(str(task.id), "quarantined", detail)

    def structured(role: str, messages: list[dict[str, str]], model_cls: Any, pass_name: str, schema_name: str):
        try:
            value, failures = structured_call(
                adapter, role=role, messages=messages, model_cls=model_cls, task_id=str(task.id),
                schema_name=schema_name,
            )
        except StructuredOutputError as error:
            ledger(pass_name, "router", adapter.last_model_id, adapter.last_request_id, len(error.attempts),
                   None, "schema_rejected")
            detail = f"{pass_name} reply failed schema validation on every attempt"
            evidence = "\n".join(f"attempt {a.attempt}: {a.error}\nreply: {a.reply_excerpt}" for a in error.attempts)
            return None, quarantine(f"{pass_name}-schema-failure", detail, evidence)
        except ModelRequestError:
            ledger(pass_name, "router", adapter.last_model_id, adapter.last_request_id, 1, None, "transport_failed")
            raise
        ledger(pass_name, "router", adapter.last_model_id, adapter.last_request_id, len(failures) + 1, None,
               "accepted")
        return value, None

    # Pass 1: retrieval.
    retrieval = deps.retrieve(f"{task.heading}\n{task.objective}")
    ledger("embedding", "embedding", retrieval.model_id, retrieval.request_id, 1, None, "accepted")

    # Pass 2: router.
    prompt = pack_router_prompt(
        system_text=deps.router_system_text, scope=_scope(task), chunks=retrieval.chunks, budget=deps.router_budget
    )
    plan, stop = structured("router", prompt.messages, RouterPlan, "router", "router_plan")
    if stop is not None:
        return stop
    if plan.task_id != str(task.id):
        return quarantine("router-task-mismatch", f"router answered for {plan.task_id}")
    by_id = {c["chunk_id"]: c for c in retrieval.chunks}
    selected_chunks = [by_id[i] for i in plan.context_chunk_ids if i in by_id]
    target_paths = [p for p in plan.target_paths if p] or list(task.active_target_hints)

    # Pass 3: executor with declared validation and bounded Error-mode retries.
    selector = ModeSelector()
    exists = bool(target_paths) and all((deps.workspace / p).exists() for p in target_paths)
    decision = selector.select_preflight(PreflightEvidence(target_exists=exists))
    mode, evidence = decision.mode, decision.evidence
    processor = ProtocolProcessor(deps.workspace, SimpleNamespace(active_task_id=str(task.id)), deps.tool_executor)
    attempt = 0
    while True:
        attempt += 1
        chunks = list(selected_chunks)
        while True:
            executor_plan = {
                "sanitized_constraints": plan.sanitized_constraints,
                "context_chunks": [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in chunks],
            }
            try:
                payload = deps.packer.build_payload(
                    task=task, mode=mode, mode_evidence=evidence if isinstance(evidence, str) else str(evidence),
                    active_files=[Path(p) for p in target_paths], plan=executor_plan,
                )
                break
            except PromptBudgetError as error:
                if not chunks:
                    return quarantine("executor-prompt-budget", str(error))
                chunks.pop()
        try:
            # Free text: no response_schema. Python validates what comes back.
            reply = adapter.chat("executor", build_messages(payload), task_id=str(task.id))
            text = reply["choices"][0]["message"]["content"]
        except (ModelRequestError, KeyError, IndexError, TypeError):
            ledger("executor", "executor", adapter.last_model_id, adapter.last_request_id, attempt, mode.value,
                   "transport_failed")
            raise
        request_id, model_id = adapter.last_request_id, adapter.last_model_id

        try:
            operations = ingest_executor_reply(text, str(task.id))
        except ExecutorReplyError as error:
            ledger("executor", "executor", model_id, request_id, attempt, mode.value, "schema_rejected")
            return quarantine("executor-reply-rejected", str(error), evidence=text[:4000])

        for operation in operations:
            try:
                outcome = processor.process_executor_output(json.dumps(operation))
            except WorkspaceOperationError as error:
                ledger("executor", "executor", model_id, request_id, attempt, mode.value, "schema_rejected")
                return quarantine("unsafe-tool-operation", str(error))
            if isinstance(outcome, ProtocolQuarantineResult):
                ledger("executor", "executor", model_id, request_id, attempt, mode.value, "schema_rejected")
                scheduler.quarantine_task(
                    task_id=task.id, report_path=outcome.report_path, changed_workspace_paths=changed
                )
                return PipelineResult(str(task.id), "quarantined", f"invalid protocol output: {outcome.parse_error}")
            if getattr(outcome, "status", "completed") != "completed":
                ledger("executor", "executor", model_id, request_id, attempt, mode.value, "schema_rejected")
                return quarantine("tool-operation-not-completed", str(getattr(outcome, "error_details", "")))
            resolved = getattr(outcome, "resolved_path", None)
            if isinstance(resolved, str) and resolved not in changed:
                changed.append(resolved)

        try:
            records = deps.validate(task)
        except CommandAuthorizationError as error:
            ledger("executor", "executor", model_id, request_id, attempt, mode.value, "validation_failed")
            return quarantine("unexecutable-validation-command", str(error))
        failed = next((r for r in records if r.exit_code != 0), None)
        if failed is None:
            ledger("executor", "executor", model_id, request_id, attempt, mode.value, "accepted")
            break
        ledger("executor", "executor", model_id, request_id, attempt, mode.value, "validation_failed")
        scheduler.record_validation_failure(
            task_id=task.id, command=failed.command, stdout=failed.stdout, stderr=failed.stderr,
            exit_code=failed.exit_code, artifact_path=failed.artifact_path,
        )
        try:
            request = scheduler.begin_error_mode_request(task_id=task.id)
        except StateExecutionRefused:
            report = scheduler.quarantine_after_retry_limit(task_id=task.id, changed_workspace_paths=changed)
            return PipelineResult(str(task.id), "quarantined", f"validation failed after 3 Error-mode requests: {report.name}",
                                  error_mode_requests=3)
        mode = request.mode
        evidence = (
            f"command: {failed.command}\nexit_code: {failed.exit_code}\n"
            f"stderr: {failed.stderr[:STDERR_EXCERPT_BYTES]}"
        )

    # Pass 4: auditor.
    files: list[dict[str, str]] = []
    for relative in changed:
        path = deps.workspace / relative
        if path.is_file():
            files.append({"chunk_id": path.name, "text": path.read_text(encoding="utf-8", errors="replace")[:AUDIT_FILE_BYTES]})
    audit_prompt = pack_router_prompt(
        system_text=deps.auditor_system_text, scope=_scope(task), chunks=files, budget=deps.router_budget,
        chunks_key="changed_files",
    )
    audit, stop = structured("router", audit_prompt.messages, AuditReport, "auditor", "audit_report")
    if stop is not None:
        return stop
    if audit.verdict == "fail":
        scheduler_turn_note = "; ".join(f"{v.rule_id} in {v.file_path}" for v in audit.violations)
        _record_audit_rejection(scheduler, task, adapter)
        return quarantine("audit-rejected", scheduler_turn_note, audit.model_dump_json(indent=2))

    results = [
        {"exit_code": r.exit_code, "artifact_path": r.artifact_path, "command": r.command}
        for r in records
    ]
    used = scheduler.store.load().task_records[str(task.id)].error_mode_requests
    scheduler.complete(task_id=task.id, validation_results=results)
    return PipelineResult(str(task.id), "completed", "validation and audit passed", error_mode_requests=used)


def _record_audit_rejection(scheduler: Scheduler, task: GoalTask, adapter: Any) -> None:
    """Ledger the failed verdict as its own turn; the schema-valid reply turn stays as written."""
    scheduler.record_model_turn(
        task_id=task.id, pass_name="auditor", role="router", model_id=adapter.last_model_id,
        attempt=1, mode=None, request_id=f"{adapter.last_request_id}-verdict", outcome="audit_rejected",
    )
