# Implementation Plan: Stateless Turn Python Orchestrator Pipeline

## Overview

Implement the local-first Python orchestrator under `local-ai/` as a durable, single-task pipeline. The implementation must treat `local-ai/config/orchestrator.toml` as the sole runtime authority, discover only enabled M1–M5 goals (including the populated M5 `goal1.md`–`goal10.md` set), and expose M6–M10 only as disabled, configuration-gated future milestones. All model traffic must be restricted to the configured loopback LM Studio endpoint; the pipeline must never automatically mutate Git, contact general outbound network endpoints, or process more than one active task per workspace.

## Tasks

- [x] 1. Establish the Python package, immutable configuration, and domain contracts
  - [x] 1.1 Create the local Python project and deterministic test tooling
    - Create `local-ai/pyproject.toml`, `local-ai/orchestrator/__init__.py`, and `local-ai/tests/conftest.py` with Python 3.12 settings and pinned development tools for `pytest`, `hypothesis`, `ruff`, and `mypy`.
    - Add test helpers for temporary workspaces, fake clocks, fake model/process ports, and no-network test isolation; do not create any runtime Git integration.
    - Validate with `python -m pytest local-ai/tests -q` (collection succeeds) and `python -m ruff check local-ai/orchestrator local-ai/tests`.
    - _Requirements: 3.1, 6.2, 9.1_
  - [x]* 1.2 Write test-first configuration and model-contract tests
    - In `local-ai/tests/test_config_models.py`, specify expected typed task/state/operation codecs, canonical workspace containment, configured repository-root precedence over the legacy nested alias, disabled M6–M10 defaults, and rejection of non-loopback LM Studio URLs or storage outside the workspace.
    - Validate with `python -m pytest local-ai/tests/test_config_models.py -q`.
    - _Requirements: 3.5, 4.1, 4.2, 6.2, 9.1_
  - [x]* 1.3 Write the workspace-scoped storage property test
    - In `local-ai/tests/test_property_11_storage_paths.py`, implement **Property 11: All local artifact paths remain workspace-scoped** using at least 100 generated workspace roots, artifact kinds, task IDs, and hostile relative names.
    - Assert state, plan, protocol, telemetry, validation, and quarantine paths never escape the canonical workspace.
    - Validate with `python -m pytest local-ai/tests/test_property_11_storage_paths.py -q --hypothesis-profile=ci`.
    - _Requirements: 9.1_
  - [x] 1.4 Implement configuration, typed records, and static runtime artifacts
    - Implement `config.py`, `models.py`, and service protocols; create `config/orchestrator.toml`, `config/tool-protocol.schema.json`, `context/pipeline-rules.md`, and `context/architecture-schema.md` as the code-consumed static artifacts described in the design.
    - Resolve and validate canonical paths, fixed planner/executor IDs, loopback-only endpoint policy, bounded-context limits, three-error retry cap, M1–M5 enabled milestones, M5 goal-number coverage, and M6–M10 disabled future milestones. Do not let goal content override configuration.
    - Validate with `python -m pytest local-ai/tests/test_config_models.py local-ai/tests/test_property_11_storage_paths.py -q` and `python -m mypy local-ai/orchestrator`.
    - _Requirements: 1.1, 3.5, 4.1, 4.2, 6.2, 9.1_

- [x] 2. Build numeric goal discovery, Markdown parsing, and malformed-input quarantine
  - [x]* 2.1 Write test-first discovery and Markdown parser examples
    - In `local-ai/tests/test_discovery_parser.py`, add fixtures copied from the populated M5 `goal1.md`–`goal10.md` source set plus synthetic M1–M4 goals. Specify non-empty-file discovery, source hashing, parsed headings/objectives/criteria/prerequisites/implementation details/validation commands, configured legacy-`cd` canonicalization, and rejection of unrecognized roots.
    - Validate with `python -m pytest local-ai/tests/test_discovery_parser.py -q`.
    - _Requirements: 1.1, 1.2, 1.4_
  - [x]* 2.2 Write the eligible-discovery and faithful-parsing property test
    - In `local-ai/tests/test_property_01_discovery_parsing.py`, implement **Property 1: Eligible goal discovery and faithful parsing** with at least 100 generated enabled M1–M5 layouts and valid task sections; assert stable/changed hashes and exact field preservation.
    - Validate with `python -m pytest local-ai/tests/test_property_01_discovery_parsing.py -q --hypothesis-profile=ci`.
    - _Requirements: 1.1, 1.2, 1.4, 2.1_
  - [x]* 2.3 Write the invalid/duplicate exclusion property test
    - In `local-ai/tests/test_property_02_invalid_duplicates.py`, implement **Property 2: Invalid and duplicate task exclusion** with malformed sections and global duplicate IDs; assert all affected records are unqueueable and reports contain raw evidence and source provenance.
    - Validate with `python -m pytest local-ai/tests/test_property_02_invalid_duplicates.py -q --hypothesis-profile=ci`.
    - _Requirements: 1.3, 2.4_
  - [x]* 2.4 Write the numeric-ordering property test
    - In `local-ai/tests/test_property_03_numeric_ordering.py`, implement **Property 3: Numeric queue ordering is independent of digit width** using at least 100 coordinate permutations, including 2-versus-10 cases.
    - Validate with `python -m pytest local-ai/tests/test_property_03_numeric_ordering.py -q --hypothesis-profile=ci`.
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 2.5 Implement discovery, parser, source hashing, and parse quarantine
    - Implement `discovery.py`, `markdown_parser.py`, and parser-facing functions in `quarantine.py`. Enumerate only configured enabled M1–M5 `goal{1..10}.md` files, sort all file/task coordinates numerically, canonicalize only configured leading legacy aliases, preserve raw sections, exclude malformed/duplicate tasks, and write local reports without halting unrelated valid work.
    - Persist successful source hashes and queue records only through the state/artifact interfaces; do not scan M6–M10 while disabled.
    - Validate with `python -m pytest local-ai/tests/test_discovery_parser.py local-ai/tests/test_property_01_discovery_parsing.py local-ai/tests/test_property_02_invalid_duplicates.py local-ai/tests/test_property_03_numeric_ordering.py -q --hypothesis-profile=ci`.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4_

- [x] 3. Add atomic run state, lock-controlled one-at-a-time scheduling, and tracker projection
  - [-]* 3.1 Write test-first atomic-state and scheduler examples
    - In `local-ai/tests/test_state_scheduler.py`, specify same-directory temporary-write/flush/replace behavior, backup generation, workspace identity/schema checks, lock acquisition/stale-lock recovery evidence, state-failure refusal, commit-before-model-call selection, resume priority, and completion only after zero-exit validation artifacts are persisted.
    - Cover an optional atomically regenerated `program-states/progress-tracker.md` projection that never becomes the scheduling authority.
    - Validate with `python -m pytest local-ai/tests/test_state_scheduler.py -q`.
    - _Requirements: 3.1, 3.3, 3.4, 3.5, 9.1_
  - [x]* 3.2 Write the single-active-task/restart property test
    - In `local-ai/tests/test_property_04_scheduler.py`, implement **Property 4: Single active task and restart priority** across at least 100 generated queues and valid transition sequences.
    - Assert at most one `in_progress` record and that a resumed active task always wins over a queued task.
    - Validate with `python -m pytest local-ai/tests/test_property_04_scheduler.py -q --hypothesis-profile=ci`.
    - _Requirements: 3.2, 3.3_
  - [x] 3.3 Implement atomic artifact persistence and the durable scheduler
    - Implement `state_store.py`, `scheduler.py`, and the report/projection portions of `quarantine.py`. Commit `in_progress` before any model request, enforce the single active task and workspace lock, resume safely, retain the prior valid generation, persist completion metadata after validation, and refuse execution on missing/corrupt state until recovery.
    - Keep run state small and refer to immutable local artifacts by workspace-relative path; never use the legacy tracker or task prose as an authority.
    - Validate with `python -m pytest local-ai/tests/test_state_scheduler.py local-ai/tests/test_property_04_scheduler.py -q --hypothesis-profile=ci`.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 9.1_

- [x] 4. Implement bounded fresh-turn context packing and the local LM Studio planner/executor adapter
  - [x]* 4.1 Write test-first context-packer and LM Studio adapter examples
    - In `local-ai/tests/test_context_lm_studio.py`, specify deterministic three-bucket packing, per-file/total byte truncation manifests, fixed planner/executor routing, explicit unload/switch lifecycle, loopback endpoint enforcement, capability query normalization, and artifacts for connection, timeout, or non-success failures that preserve `in_progress` state and workspace changes.
    - Validate with `python -m pytest local-ai/tests/test_context_lm_studio.py -q`.
    - _Requirements: 4.1, 4.2, 4.3, 4.5, 9.2_
  - [x]* 4.2 Write the fresh-request isolation property test
    - In `local-ai/tests/test_property_05_fresh_requests.py`, implement **Property 5: Fresh model request isolation and routing** with at least 100 generated task/mode pairs and fake local model responses.
    - Assert every request has only current-task bounded context and no prior task messages, routes to the correct fixed model ID, and includes rules, validation, and mode evidence.
    - Validate with `python -m pytest local-ai/tests/test_property_05_fresh_requests.py -q --hypothesis-profile=ci`.
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [x] 4.3 Implement the bounded packer and fresh local-model lifecycle adapter
    - Implement `context_packer.py` and `lm_studio.py`. Build immutable planner/executor payloads from only static rules, architecture, active task, selected mode/evidence, declared validation, relevant bounded files, and current plan; persist request/response/manifests with unique IDs.
    - Enforce loopback-only HTTP, fixed configured model IDs, configured timeouts, fail-closed local lifecycle loading/switching, and no concurrent planner/executor assumption. Retain `in_progress` plus an error artifact on transport failure.
    - Validate with `python -m pytest local-ai/tests/test_context_lm_studio.py local-ai/tests/test_property_05_fresh_requests.py -q --hypothesis-profile=ci`.
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 9.2_

- [x] 5. Implement JSON protocol workspace operations and the command/PowerShell safety boundary
  - [x]* 5.1 Write test-first Tool Protocol and workspace-operation examples
    - In `local-ai/tests/test_protocol_workspace.py`, specify strict versioned JSON parsing with no unknown top-level fields, active-task matching, allowlisted actions, canonical containment, symlink/device/binary/path-traversal rejection, configured-default-disabled deletion, atomic text writes, structured unique-context patching, and before/after hash audit records.
    - Validate with `python -m pytest local-ai/tests/test_protocol_workspace.py -q`.
    - _Requirements: 5.1, 5.2, 5.3_
  - [x]* 5.2 Write the protocol validation/confinement property test
    - In `local-ai/tests/test_property_06_protocol_confinement.py`, implement **Property 6: Protocol validation and workspace confinement** across at least 100 generated protocol documents, path inputs, and symlink layouts.
    - Validate with `python -m pytest local-ai/tests/test_property_06_protocol_confinement.py -q --hypothesis-profile=ci`.
    - _Requirements: 5.1, 5.2, 5.3_
  - [x]* 5.3 Write the invalid-protocol preservation property test
    - In `local-ai/tests/test_property_07_invalid_protocol.py`, implement **Property 7: Invalid protocol safely preserves the task** with non-JSON, fenced/prose, malformed, and mismatched executor outputs.
    - Assert no tool execution, retained `in_progress`, unchanged pre-existing workspace files, and a parse report with response text/error.
    - Validate with `python -m pytest local-ai/tests/test_property_07_invalid_protocol.py -q --hypothesis-profile=ci`.
    - _Requirements: 5.4_
  - [x]* 5.4 Write test-first command-guard, PowerShell, and ordered-validation examples
    - In `local-ai/tests/test_command_validation.py`, specify quoted-whitespace normalization, exact canonical declared-command matching, denylist rejections for Git mutation/remote/network/package-download forms, workspace `cwd`, no-profile/non-interactive PowerShell arguments, minimal environment, ordered execution, captured stdout/stderr/exit metadata, and rejection audit artifacts.
    - Use a fake runner only; tests must not launch real PowerShell or network-capable commands.
    - Validate with `python -m pytest local-ai/tests/test_command_validation.py -q`.
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.1_
  - [x]* 5.5 Write the command-authorization property test
    - In `local-ai/tests/test_property_08_command_guard.py`, implement **Property 8: Command authorization excludes unsafe activity** across at least 100 declared/candidate commands, whitespace variants, and Git/network denylist forms.
    - Validate with `python -m pytest local-ai/tests/test_property_08_command_guard.py -q --hypothesis-profile=ci`.
    - _Requirements: 6.1, 6.2, 6.3_
  - [x] 5.6 Implement strict JSON protocol validation and safe workspace mutations
    - Implement `protocol.py` and `workspace.py`. Validate the schema and active task, resolve real paths beneath the workspace, execute only `mkdir`, `write_file`, and `patch_file` without a shell, keep `delete_file` disabled unless explicitly configured, and persist proposed-action/result records with required audit fields.
    - Quarantine invalid protocol output while retaining partial workspace changes; reject unsafe operations before mutation.
    - Validate with `python -m pytest local-ai/tests/test_protocol_workspace.py local-ai/tests/test_property_06_protocol_confinement.py local-ai/tests/test_property_07_invalid_protocol.py -q --hypothesis-profile=ci`.
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [x] 5.7 Implement command authorization, PowerShell execution, and validation artifacts
    - Implement `command_guard.py`, `powershell.py`, and `validation.py`. Execute only canonical parser-derived commands that exactly match after allowed normalization and pass the denylist; reject all automatic Git mutations, remote operations, general outbound/network-capable commands, and undeclared shell text.
    - Run accepted commands non-interactively from `workspace.root`, record command results under `local-ai/validation/`, and stop ordered validation at the first non-zero exit while preserving output evidence.
    - Validate with `python -m pytest local-ai/tests/test_command_validation.py local-ai/tests/test_property_08_command_guard.py -q --hypothesis-profile=ci`.
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.1_

- [x] 6. Add observable execution modes, bounded Error recovery, and permanent-failure evidence
  - [x]* 6.1 Write test-first mode-selection and retry examples
    - In `local-ai/tests/test_modes_retries.py`, specify Scaffold for absent targets, Aligner for imports/dependencies/signatures, CoT-Task for healthy existing targets, Error only after non-zero validation, exact stderr/exit context propagation, transition persistence, and completion after retry with exact count.
    - Include three persistent failures and assert no workspace rollback plus a complete Markdown quarantine report.
    - Validate with `python -m pytest local-ai/tests/test_modes_retries.py -q`.
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4_
  - [x]* 6.2 Write the deterministic-mode-selection property test
    - In `local-ai/tests/test_property_09_mode_selection.py`, implement **Property 9: Observable preflight and validation evidence determines mode** across at least 100 generated preflight/validation observations.
    - Validate with `python -m pytest local-ai/tests/test_property_09_mode_selection.py -q --hypothesis-profile=ci`.
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  - [x]* 6.3 Write the ordered-validation/bounded-retry property test
    - In `local-ai/tests/test_property_10_validation_retries.py`, implement **Property 10: Ordered validation and bounded error recovery** with generated declared-command result sequences.
    - Assert declaration order, no more than three Error-mode executor requests, and exact completed retry counts on retry success.
    - Validate with `python -m pytest local-ai/tests/test_property_10_validation_retries.py -q --hypothesis-profile=ci`.
    - _Requirements: 8.1, 8.2, 8.3_
  - [x]* 6.4 Write the permanent-failure preservation property test
    - In `local-ai/tests/test_property_13_permanent_failure.py`, implement **Property 13: Permanent validation failure preserves changes and evidence** with at least 100 generated failing result sequences and changed-path sets.
    - Validate with `python -m pytest local-ai/tests/test_property_13_permanent_failure.py -q --hypothesis-profile=ci`.
    - _Requirements: 8.4_
  - [x] 6.5 Implement mode inspection and the bounded Error-mode state machine
    - Implement `mode_selector.py` and extend `scheduler.py`, `validation.py`, and `quarantine.py` to derive modes from observable evidence, commit mode history, increment Error requests immediately before each fresh request, and cap Error requests at three.
    - On terminal validation failure, atomically mark the task quarantined without rollback and emit a redacted report containing task ID, mode history, command/output/exit evidence, retries, changed paths, recovery timestamp, and relative artifact links.
    - Validate with `python -m pytest local-ai/tests/test_modes_retries.py local-ai/tests/test_property_09_mode_selection.py local-ai/tests/test_property_10_validation_retries.py local-ai/tests/test_property_13_permanent_failure.py -q --hypothesis-profile=ci`.
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4_

- [x] 7. Implement capability-gated low-VRAM telemetry
  - [x]* 7.1 Write test-first capability and telemetry examples
    - In `local-ai/tests/test_telemetry.py`, specify runtime-reported capability-state normalization (`supported`, `unsupported`, `not-reported`), default retention for unsupported settings, validation of effective applied values, one append-only NDJSON record per benchmarked request, and absent—not synthesized—memory telemetry.
    - Validate with `python -m pytest local-ai/tests/test_telemetry.py -q`.
    - _Requirements: 9.2, 9.3, 9.4, 9.5_
  - [x]* 7.2 Write the low-VRAM capability-gate property test
    - In `local-ai/tests/test_property_12_low_vram.py`, implement **Property 12: Capability-gated low-VRAM application and telemetry** across at least 100 generated support matrices, requested settings, and benchmark request sequences.
    - Validate with `python -m pytest local-ai/tests/test_property_12_low_vram.py -q --hypothesis-profile=ci`.
    - _Requirements: 9.3, 9.4, 9.5_
  - [x] 7.3 Implement capability gating and append-only telemetry
    - Implement `telemetry.py` and complete the capability/application interfaces in `lm_studio.py`. Query and record runtime support before initialization/benchmarks, apply only confirmed supported requested values, retain runtime defaults otherwise, and append one local telemetry record for each benchmark request.
    - Do not claim that Flash Attention, KV settings, or GPU offload are active unless the local runtime both reports and confirms them; never modify runtime settings outside explicit benchmark configuration.
    - Validate with `python -m pytest local-ai/tests/test_telemetry.py local-ai/tests/test_property_12_low_vram.py -q --hypothesis-profile=ci`.
    - _Requirements: 9.2, 9.3, 9.4, 9.5_

- [x] 8. Compose the CLI, fake-LM integration coverage, and an explicit controlled pilot path
  - [x]* 8.1 Write integration tests using a fake local LM Studio service
    - In `local-ai/tests/test_integration_fake_lm_studio.py`, run a temporary-workspace task through discovery, atomic selection, fresh fake planner/executor responses, real protocol validation/execution, fake PowerShell validation, completion/resume cases, protocol quarantine, and transport retry preservation.
    - Assert exactly one active task, no Git mutation, no non-loopback request, ordered validation, local artifact confinement, M5 discovery coverage, and M6–M10 exclusion unless the fixture changes configuration.
    - Validate with `python -m pytest local-ai/tests/test_integration_fake_lm_studio.py -q`.
    - _Requirements: 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.5, 5.1, 5.4, 6.2, 8.1, 9.1_
  - [x]* 8.2 Write CLI/pilot command tests without a real model
    - In `local-ai/tests/test_cli.py`, specify `discover`, `run-once`, `resume`, `benchmark`, and `pilot` argument handling, explicit `--enable-pilot` confirmation, loopback-only preflight, one-task limit, disabled-by-default benchmark settings, and a refusal when configuration, state, or capabilities are unsafe.
    - Use fake adapters only; the test suite must never start a real LM Studio request or alter model settings.
    - Validate with `python -m pytest local-ai/tests/test_cli.py -q`.
    - _Requirements: 3.2, 4.1, 6.2, 8.2, 9.2, 9.3, 9.4, 9.5_
  - [x] 8.3 Implement CLI composition, controlled pilot support, and local operator artifacts
    - Implement `__main__.py` and `services.py` to compose only the validated dependencies and provide `discover`, `run-once`, `resume`, `benchmark`, and a configuration-gated `pilot` command. Add a code-consumed `local-ai/context/pilot-procedure.md` that documents the exact local-only preflight and telemetry artifact locations.
    - The `pilot` path must require explicit opt-in, execute no more than one selected task, require a configured loopback LM Studio endpoint and valid capability record, retain the default runtime settings unless benchmark mode is separately enabled, and never issue Git mutations or general outbound network requests.
    - Validate with `python -m pytest local-ai/tests/test_integration_fake_lm_studio.py local-ai/tests/test_cli.py -q`, `python -m pytest local-ai/tests -q --hypothesis-profile=ci`, `python -m ruff check local-ai/orchestrator local-ai/tests`, and `python -m mypy local-ai/orchestrator`.
    - _Requirements: 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, 4.5, 5.1, 5.4, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4, 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional test tasks. They are intentionally listed before their corresponding implementation to support test-first development, but must not be implemented automatically when skipped.
- Each property task maps one-to-one to a numbered correctness property in `design.md` and must use at least 100 generated examples with fake I/O.
- All implementation and test artifacts remain under `local-ai/`; no task authorizes automatic commits, tags, branches, pushes, resets, cleans, or general outbound network access.
- The M1–M5 discovery range is enabled by configuration and includes the populated M5 goals. M6–M10 remain configuration-gated future scope and must not be discovered by default.
- The controlled pilot is code-supported and explicit-opt-in only. It is not an instruction to run a real model during this planning workflow.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["1.4"] },
    { "id": 3, "tasks": ["2.1", "2.2", "2.3", "2.4"] },
    { "id": 4, "tasks": ["2.5"] },
    { "id": 5, "tasks": ["3.1", "3.2"] },
    { "id": 6, "tasks": ["3.3"] },
    { "id": 7, "tasks": ["4.1", "4.2"] },
    { "id": 8, "tasks": ["4.3"] },
    { "id": 9, "tasks": ["5.1", "5.2", "5.3", "5.4", "5.5"] },
    { "id": 10, "tasks": ["5.6"] },
    { "id": 11, "tasks": ["5.7"] },
    { "id": 12, "tasks": ["6.1", "6.2", "6.3", "6.4"] },
    { "id": 13, "tasks": ["6.5"] },
    { "id": 14, "tasks": ["7.1", "7.2"] },
    { "id": 15, "tasks": ["7.3"] },
    { "id": 16, "tasks": ["8.1", "8.2"] },
    { "id": 17, "tasks": ["8.3"] }
  ]
}
```