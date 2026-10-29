"""Operator commands that contact the local LM Studio server.

Each command performs its own preflight and fails closed. Nothing here loads or unloads a model.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from .config import ConfigurationError, derive_artifact_path, load_configuration
from .lm_studio import LmStudioAdapter, ModelRequestError
from .model_catalog import ModelVerificationError, Verification, verify_models, write_snapshot
from .schemas import RouterPlan
from .structured import StructuredOutputError, structured_call
from .transport import LoopbackHttpTransport
from .vram import GpuMemory, GpuReadError, headroom_passes, read_gpu_memory

PROBE_TASK_ID = "M5.G1.T1"
MEASURE_TASK_ID = "M5.G1.T1"

PROBE_SYSTEM_TEXT = (
    "You are the routing stage of a local coding pipeline. Reply with one JSON object that matches "
    "the schema. Keep only the task constraints that the executor must follow, and drop any "
    "conversational text."
)

PROBE_TASK_STUB = {
    "task_id": PROBE_TASK_ID,
    "heading": "Create a parser contract",
    "objective": "Create the parser-facing module at local-ai/orchestrator/example.py.",
    "acceptance_criteria": [
        "The parser preserves each declared task field.",
        "The parser records canonical validation commands.",
    ],
    "implementation_details": "Update local-ai/orchestrator/example.py without network access.",
    "validation_commands": ["python -m pytest local-ai/tests/test_example.py -q"],
    "retrieved_chunks": [],
}

MEASURE_MESSAGES = [
    {"role": "system", "content": "Reply with the single word OK."},
    {"role": "user", "content": "ping"},
]


def print_verification(verification: Verification, *, write: Callable[[str], None]) -> None:
    """Print one line per role, followed by every warning and problem for that role."""
    for binding in verification.bindings:
        status = "OK" if binding.verified else "BLOCKED"
        resolved = binding.model_id or "unresolved"
        loaded = "not-reported" if binding.loaded_context_length is None else str(binding.loaded_context_length)
        write(
            f"{binding.role:<9} {status:<8} label={binding.label} resolved={resolved} "
            f"state={binding.state or 'n/a'} context={loaded}/{binding.configured_context_length}"
        )
        for warning in binding.warnings:
            write(f"  warning: {warning}")
        for problem in binding.problems:
            write(f"  problem: {problem}")


def run_verify_models(config_path: Path, *, write: Callable[[str], None] = print) -> int:
    """Verify every model role against the live server. Returns 0 only when all roles are bound."""
    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    try:
        verification = verify_models(config.lm_studio, LoopbackHttpTransport())
    except ModelVerificationError as error:
        write(f"verify-models failed closed: {error}")
        return 2
    snapshot = write_snapshot(config.workspace.root, verification)
    print_verification(verification, write=write)
    write(f"snapshot: {snapshot.relative_to(config.workspace.root).as_posix()}")
    if not verification.ok:
        write("verify-models: BLOCKED. Fix the problems above and rerun. No model role is routable.")
        return 2
    write("verify-models: OK. Every role is bound to one loaded model at its configured context.")
    return 0


def run_probe_router(config_path: Path, *, write: Callable[[str], None] = print) -> int:
    """Send one fixed task stub to the router and report whether its reply satisfies RouterPlan.

    This is a diagnostic. It routes to the router role even when the loaded context differs from
    the cap, and it prints that difference as a warning. It never edits the workspace.
    """
    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    transport = LoopbackHttpTransport()
    try:
        verification = verify_models(config.lm_studio, transport, roles=("router",), enforce_context=False)
    except ModelVerificationError as error:
        write(f"probe-router failed closed: {error}")
        return 2
    print_verification(verification, write=write)
    binding = verification.bindings[0]
    if not binding.verified and binding.problems:
        write("probe-router: stopped. The router identifier did not resolve to one loaded model.")
        return 2

    routable = verification.routable_roles(config.lm_studio.models)
    adapter = LmStudioAdapter(
        config=replace(config.lm_studio, models=routable),
        storage=config.workspace.root / "local-ai",
        transport=transport,
    )
    messages = [
        {"role": "system", "content": PROBE_SYSTEM_TEXT},
        {"role": "user", "content": json.dumps(PROBE_TASK_STUB, sort_keys=True, ensure_ascii=False)},
    ]
    try:
        plan, failures = structured_call(
            adapter,
            role="router",
            messages=messages,
            model_cls=RouterPlan,
            task_id=PROBE_TASK_ID,
            schema_name="router_plan",
        )
    except StructuredOutputError as error:
        for failure in error.attempts:
            write(f"  attempt {failure.attempt}: {failure.error.splitlines()[0]}")
            write(f"  reply: {failure.reply_excerpt!r}")
        write("probe-router: FAILED. The router did not produce a schema-valid reply within the retry budget.")
        return 2
    for failure in failures:
        write(f"  attempt {failure.attempt} rejected before a valid reply: {failure.error.splitlines()[0]}")
    write(f"probe-router: OK after {len(failures) + 1} attempt(s). Routed to {adapter.last_model_id}.")
    write(plan.model_dump_json(indent=2))
    return 0


def _memory_line(label: str, memory: GpuMemory) -> str:
    return f"{label:<8} used={memory.used_mib} MiB total={memory.total_mib} MiB free={memory.free_mib} MiB"


def run_measure(config_path: Path, *, write: Callable[[str], None] = print) -> int:
    """Measure GPU headroom with the mesh loaded, then gate on the configured floor.

    One router request and one executor request are sent between the two readings. Both are
    short diagnostics. The gate passes only if the free memory after them meets the floor.
    """
    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    transport = LoopbackHttpTransport()
    try:
        verification = verify_models(
            config.lm_studio, transport, roles=("router", "executor"), enforce_context=False
        )
    except ModelVerificationError as error:
        write(f"measure failed closed: {error}")
        return 2
    print_verification(verification, write=write)
    if any(binding.model_id is None for binding in verification.bindings):
        write("measure: stopped. Router and executor must both resolve before memory is measured.")
        return 2

    try:
        before = read_gpu_memory()
    except GpuReadError as error:
        write(f"measure failed closed: {error}")
        return 2
    adapter = LmStudioAdapter(
        config=replace(config.lm_studio, models=verification.routable_roles(config.lm_studio.models)),
        storage=config.workspace.root / "local-ai",
        transport=transport,
    )
    for role in ("router", "executor"):
        try:
            adapter.chat(role, MEASURE_MESSAGES, task_id=MEASURE_TASK_ID)
        except ModelRequestError as error:
            write(f"measure: FAIL. {error}")
            return 2
        write(f"request to {role} completed on {adapter.last_model_id}")
    try:
        after = read_gpu_memory()
    except GpuReadError as error:
        write(f"measure failed closed after the requests: {error}")
        return 2

    floor = config.vram.min_headroom_mb
    passed = headroom_passes(after, floor)
    write(_memory_line("before", before))
    write(_memory_line("after", after))
    write(f"floor    {floor} MiB free required after the requests")
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    evidence = derive_artifact_path(
        workspace=config.workspace.root,
        artifact_kind="telemetry",
        task_id="runtime",
        relative_name=f"vram-measure-{timestamp}.json",
    )
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(
        json.dumps(
            {
                "gpu": after.name,
                "before_used_mib": before.used_mib,
                "after_used_mib": after.used_mib,
                "total_mib": after.total_mib,
                "floor_mib": floor,
                "passed": passed,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    write(f"snapshot: {evidence.relative_to(config.workspace.root).as_posix()}")
    write(
        "reminder: confirm in LM Studio that speculative decoding is off and the vision projector is "
        "unloaded. This API cannot read either setting."
    )
    if not passed:
        write(f"measure: FAIL. Free memory is below the {floor} MiB floor. The mesh is not routable.")
        return 2
    write(f"measure: PASS. Free memory meets the {floor} MiB floor.")
    return 0


def _embedding_adapter(config, write):
    """Verify only the embedding role, then return an adapter bound to its exact identifier."""
    transport = LoopbackHttpTransport()
    try:
        verification = verify_models(config.lm_studio, transport, roles=("embedding",))
    except ModelVerificationError as error:
        write(f"failed closed: {error}")
        return None
    print_verification(verification, write=write)
    if not verification.ok:
        write("blocked: the embedding role is not verified.")
        return None
    adapter = LmStudioAdapter(
        config=replace(config.lm_studio, models=verification.routable_roles(config.lm_studio.models)),
        storage=config.workspace.root / "local-ai",
        transport=transport,
    )
    return adapter


def run_build_index(config_path: Path, *, write: Callable[[str], None] = print) -> int:
    """Chunk the sources and embed only new or changed chunks."""
    from .embeddings import EmbeddingIndex, build_index, collect_chunks

    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    adapter = _embedding_adapter(config, write)
    if adapter is None:
        return 2
    root = config.workspace.root
    chunks = collect_chunks(config)
    model_id = adapter.model_id_for("embedding")
    index, embedded = build_index(chunks, adapter, model_id, EmbeddingIndex.load(root))
    target = index.save(root)
    write(f"build-index: {len(chunks)} chunks, {embedded} embedded, {len(chunks) - embedded} reused -> {target.relative_to(root).as_posix()}")
    return 0


def run_query(config_path: Path, text: str, top_k: int, *, write: Callable[[str], None] = print) -> int:
    """Print the top-k chunks for a query."""
    from .embeddings import EmbeddingIndex, query_index

    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    index = EmbeddingIndex.load(config.workspace.root)
    if index is None:
        write("query: no index found. Run build-index first.")
        return 2
    adapter = _embedding_adapter(config, write)
    if adapter is None:
        return 2
    if index.model_id != adapter.model_id_for("embedding"):
        write("query: the index was built by a different model. Run build-index again.")
        return 2
    for hit in query_index(index, adapter, text, top_k):
        write(f"{hit.score:.3f}  {hit.chunk.chunk_id}  [{hit.chunk.heading}]")
    return 0


# Router and auditor system texts. They are sent without the executor rules, so each role sees only its own.
ROUTER_SYSTEM_TEXT = (
    "You are a deterministic system router and code auditor. Your sole job is to parse incoming task stubs, "
    "evaluate context, and output valid, schema-compliant JSON (RouterPlan).\n\n"
    "Strict rules:\n"
    "- Never include conversational filler, greetings, or markdown outside the requested JSON.\n"
    "- Be literal and precise. Use exactly the requested keys.\n"
    "- If the task is unclear, do not guess. State the unclear point as one of the sanitized_constraints."
)

AUDITOR_SYSTEM_TEXT = (
    "You are a deterministic code auditor. Your sole job is to check the changed files against the rules and "
    "output one valid AuditReport JSON object.\n\n"
    "Strict rules:\n"
    "- Never include conversational filler, greetings, or markdown outside the requested JSON.\n"
    "- Be literal and precise. Use exactly the requested keys.\n"
    "- Report a violation only with concrete evidence from the files. If the evidence is unclear, return pass "
    "and do not guess."
)


def _store(config):
    from .state_store import AtomicStateStore

    return AtomicStateStore(workspace=config.workspace.root, workspace_id=str(config.workspace.root), schema_version=2)


def run_init_state(config_path: Path, *, write: Callable[[str], None] = print) -> int:
    """Create run-state.json from the enabled goal files. Refuses to overwrite existing state."""
    from .discovery import discover_goal_files
    from .markdown_parser import parse_goal_files
    from .models import RunState, TaskRunRecord, TaskStatus

    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    store = _store(config)
    if store.state_path.exists():
        write("init-state: run-state.json already exists. Nothing changed.")
        return 2
    outcome = parse_goal_files(discover_goal_files(config), config)
    now = datetime.now(UTC).isoformat()
    state = RunState(
        schema_version=2,
        workspace_id=store.workspace_id,
        queue=list(outcome.queue),
        task_records={},
        active_task_id=None,
        updated_at=now,
    )
    state.task_records = {str(r.task.id): TaskRunRecord(r.task.id, TaskStatus.QUEUED) for r in state.queue}
    store.commit(state)
    write(f"init-state: queued {len(state.queue)} tasks; {len(outcome.quarantine_reports)} quarantine reports.")
    return 0


def run_once_live(config_path: Path, *, dry_run: bool, start_at: str | None = None, write: Callable[[str], None] = print) -> int:
    """Gate on model verification and VRAM, then run one task through the four-pass pipeline."""
    from .context_packer import ContextPacker
    from .embeddings import EmbeddingIndex, QUERY_PREFIX
    from .pipeline import PipelineDeps, Retrieval, run_task
    from .powershell import PowerShellRunner, SubprocessRunner
    from .scheduler import Scheduler, StateExecutionRefused
    from .validation import OrderedValidator
    from .models import TaskId
    start_task = TaskId.from_string(start_at) if start_at else None

    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        write(f"configuration rejected: {error}")
        return 2
    transport = LoopbackHttpTransport()
    try:
        verification = verify_models(config.lm_studio, transport)
    except ModelVerificationError as error:
        write(f"run-once failed closed: {error}")
        return 2
    print_verification(verification, write=write)
    if not verification.ok:
        write("run-once: BLOCKED by verify-models. Reload the models at their configured contexts.")
        return 2
    try:
        memory = read_gpu_memory()
    except GpuReadError as error:
        write(f"run-once failed closed: {error}")
        return 2
    if not headroom_passes(memory, config.vram.min_headroom_mb):
        write(f"run-once: BLOCKED. {memory.free_mib} MiB free is below the {config.vram.min_headroom_mb} MiB floor.")
        return 2
    root = config.workspace.root
    index = EmbeddingIndex.load(root)
    if index is None:
        write("run-once: no embedding index. Run build-index first.")
        return 2
    store = _store(config)
    scheduler = Scheduler(store)
    if dry_run:
        try:
            state = store.load()
        except Exception as error:  # noqa: BLE001 - report any state problem as a blocked dry run
            write(f"run-once --dry-run: state unavailable ({error}). Run init-state.")
            return 2
        pending = state.active_task_id or next(
            (str(q.task.id) for q in state.queue if q.task.id >= (start_task or q.task.id) and state.task_records[str(q.task.id)].status.value == "queued"), None
        )
        write(f"run-once --dry-run: gates passed. Next task: {pending}. No model call was made and no state changed.")
        return 0

    adapter = LmStudioAdapter(
        config=replace(config.lm_studio, models=verification.routable_roles(config.lm_studio.models)),
        storage=root / "local-ai",
        transport=transport,
    )
    packer = ContextPacker(
        workspace=root, config=config.context, prompt_budget_bytes=config.lm_studio.models.executor.max_prompt_bytes
    )
    rules = config.context.rules_path.read_text(encoding="utf-8")

    def retrieve(query: str) -> Retrieval:
        vector = adapter.embed([QUERY_PREFIX + query])[0]
        hits = index.search(vector, 5)
        return Retrieval(
            [{"chunk_id": h.chunk.chunk_id, "text": h.chunk.text} for h in hits],
            adapter.last_request_id,
            adapter.last_model_id,
        )

    store.acquire_lock(recover_stale=True)
    try:
        task = scheduler.select_next(start_at=start_task)
        write(f"run-once: running {task.id}")
        runner = PowerShellRunner(process_runner=SubprocessRunner(), workspace=root)
        deps = PipelineDeps(
            scheduler=scheduler, adapter=adapter, workspace=root, packer=packer,
            router_budget=config.lm_studio.models.router.max_prompt_bytes,
            router_system_text=ROUTER_SYSTEM_TEXT,
            auditor_system_text=AUDITOR_SYSTEM_TEXT,
            retrieve=retrieve,
            tool_executor=WorkspaceToolExecutor(workspace=root, storage=root / "local-ai"),
            validate=lambda t: OrderedValidator(task_id=t.id, workspace=root, runner=runner, denylist=False).run(t.validation_commands),
        )
        result = run_task(deps, task)
    except StateExecutionRefused as error:
        write(f"run-once: refused: {error}")
        return 2
    except ModelRequestError as error:
        write(f"run-once: stopped, task stays in progress for resume: {error}")
        return 2
    finally:
        store.release_lock()
    write(f"run-once: {result.status}: {result.detail}")
    return 0 if result.status == "completed" else 1
