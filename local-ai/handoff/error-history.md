# Error history for higher-model review

Status: final for Tasks 1-12. Task 13 (live acceptance run) is blocked on the LM Studio reloads below.
Test suite: 171 passed, 1 skipped (symlink test needs a Windows privilege), Python 3.13 (project pins 3.12, not installed).

Scope: errors and wrong turns in the stateless turn orchestrator build, from the first
live check of the LM Studio model mesh onward. Each entry lists what happened, the cause,
the fix, and what remains open. Runtime errors recorded by the orchestrator itself live
in `local-ai/program-states/run-state.json` under `task_records[*].error_history`.

## Live environment findings

| # | Finding | Evidence | Status |
|---|---------|----------|--------|
| L1 | Screenshot labels are not LM Studio identifiers. `1b-gemma-3-1b-it-qat` and `embed-text-embedding-nomic-embed-text-v1.5` do not exist as written. | `GET /v1/models` lists `gemma-3-1b-it-qat`, `text-embedding-nomic-embed-text-v1.5`, and `gemma-4-e2b-it-qat@q4_k_xl` / `@f16` | Resolved in code. Startup binds each label to one loaded identifier. |
| L2 | The executor has two variants. Only `gemma-4-e2b-it-qat@q4_k_xl` is loaded. | Native `GET /api/v0/models` reports `state: loaded` for the q4 variant only | Resolved in code. Ambiguity blocks a role. |
| L3 | The router is loaded at context 16128, but the configured cap is 2048. | `verify-models` run, `run-verify-output.txt` | Open. Needs a reload in LM Studio with context length 2048. |
| L4 | The executor is loaded at context 65792, but the configured cap is 4096. | Same run | Open. Needs a reload in LM Studio with context length 4096. |
| L5 | The executor reports type `vlm`, which may mean the vision projector is still loaded. Speculative decoding state cannot be read from the API. | `GET /api/v0/models` shows `type: vlm` | Open. Confirm in LM Studio that the projector is unloaded and speculative decoding is off. |
| L6 | `/v1/models` lists downloaded models, not loaded ones. Load state must come from the native endpoint. | Compare both responses | Resolved in code. |

## Code and test errors

| # | Error | Cause | Fix | Status |
|---|-------|-------|-----|--------|
| C1 | Baseline: 12 test failures before Task 1 work. | Hypothesis health checks on function-scoped `tmp_path` fixtures (10), a tuple passed where a strategy was required, a source-hash test that read text instead of bytes. | Per-example directories from `tmp_path_factory`, `st.sampled_from`, byte hashing. | Fixed. |
| C2 | Quarantine reports lost evidence on Windows. A CRLF in captured text became `\r\r\n`. | `write_text` translated newlines again on already-CRLF text. | Captured text normalized to LF; reports written with `newline="\n"`. | Fixed. |
| C3 | Error-mode history over-counted. A fourth failure added an ERROR entry to `mode_history` even though no request was made. | The append happened before the retry-limit check. | Refused failures go to `error_history` with disposition `refused_retry_limit`. `mode_history` now records only granted requests. | Fixed. Covered by `tests/test_error_history.py`. |
| C4 | Scheduler test expected a fourth Error request to succeed silently. | Test expectation did not match the designed cap. | Test now expects `StateExecutionRefused` at the cap. | Fixed. |
| C5 | Telemetry snapshot test expected the wrong directory. | Artifact paths are task-scoped (`telemetry/runtime/`). | Test corrected. | Fixed. |
| C6 | Packaging-level test collection failed with `No module named 'orchestrator'`. | A background pytest run was started without `cwd` set to `local-ai`. | Runs now go through a script that sets the directory. | Fixed (process error, not a product defect). |

## Tooling and process errors (not product defects)

| # | Issue | Effect | Mitigation |
|---|-------|--------|-----------|
| P1 | The PowerShell tool often echoed long commands back in garbled form. | Output could not be trusted. | Results are written to files and read back in a separate step. |
| P2 | Reads issued in the same batch as a wait returned an empty file. | Several false "no output" results. | Waits and reads now run in separate steps. |
| P3 | A launcher that starts before its script file exists fails silently. | Missing output file. | Create the file first, then start the process. |

## Open decisions and risks

- Router and executor must be reloaded at their configured caps before any live run.
- The 6144-byte router budget may be smaller than the rules and architecture anchors. The
  size check is part of Task 9.
- The executor output reserve is 1024 tokens. Long files may need more, which would turn into
  invalid JSON and then Error-mode loops. The live acceptance run will show whether this matters.

## Tasks 7-13 additions

| # | Item | Detail | Status |
|---|------|--------|--------|
| C7 | Old packer test assumed the prompt budget bounded file bytes only. | Task 9 makes the budget cover the whole payload (anchors + scope + files). The 180-byte test now fails by design. | Test updated to 2000 bytes plus an explicit `PromptBudgetError` case. |
| D1 | Intermediate router schema failures are not ledgered as separate model turns. | `structured_call` returns the failures but not their request IDs, so only the final attempt gets a `ModelTurn` (with `attempt` = failures + 1). | Open. Acceptable for provenance; revisit if per-attempt IDs are needed. |
| D2 | The auditor reuses the router model (`gemma-3-1b`). A failed audit quarantines the task with no retry. | A 1B auditor may reject good work. | Open decision. Options: keep, make audit advisory, or add an audit-retry budget. |
| D3 | A task is quarantined on invalid executor output, unsafe tool operation, or an unexecutable declared command. | Matches the original design for invalid protocol output; added `Scheduler.quarantine_task`. | Done. |
| D4 | `build-index` produced 1681 chunks at 1500 chars. `local-ai/embeddings/index.json` is untracked and not git-ignored. | Generated file. | Open: decide whether to ignore it. |
| D5 | `run-once` needs `init-state` first (no code previously created `run-state.json`). | Added `init-state`; it refuses to overwrite existing state. | Done. Not yet run against the real workspace. |

## Task 13 status: blocked

`python -m orchestrator run-once --dry-run` stops at `verify-models` (exit 2):

- `gemma-3-1b-it-qat` is loaded at context 16128, cap 2048.
- `gemma-4-e2b-it-qat@q4_k_xl` is loaded at context 65792, cap 4096.
- The embedding model is correct (2048). `build-index` and `query` work live.

To unblock, in LM Studio:
1. Reload `gemma-3-1b-it-qat` with context length 2048.
2. Reload `gemma-4-e2b-it-qat@q4_k_xl` with context length 4096.
3. Turn off speculative decoding and unload the vision projector (the API cannot report either).
4. Run `verify-models`, `measure`, then `init-state` and `run-once --dry-run`.

The real `run-once` edits workspace files. Run it on a disposable copy of the repo, or approve the real workspace explicitly.

## Not verified

- Router and executor behavior on real tasks (only fake-model scenarios and the router probe were run).
- Whether the 1024-token executor reserve truncates long files.
- Whether the 6144-byte router budget leaves room for retrieved chunks on real tasks (anchors are about 1.9 KB total).
- Python 3.12.

## Task 13 attempt 1 (disposable copy at `%USERPROFILE%\portfolio-live-copy`)

Context caps were fixed by the operator (router 2048, executor 4096). `verify-models` and `measure` passed, 1386 MiB free.
`init-state` queued 10 tasks, next task `M1.G1.T1`. The first real `run-once` quarantined that task. Findings:

| # | Finding | Evidence | Status |
|---|---------|----------|--------|
| L7 | The executor has speculative decoding (MTP) ON. | Every executor reply carries `draft_model: ...mtp-gemma-4-E2B-it-F16.gguf` and draft-token stats. The router reply does not. | Open, operator action: turn speculative decoding off on the executor and reload it. `measure` and `run-once` now fail closed on any reply that names a draft model (`SpeculativeDecodingError`). |
| C8 | The executor invented its own `tool_call` format, so the Tool Protocol validator rejected it ("unknown top-level field"). | Quarantine report `invalid-protocol.md` in the copy. | Fixed in code: the executor request now carries a `json_schema` constraint (`TOOL_PROTOCOL_SCHEMA`). Not yet re-run live. |
| C9 | The anchor `pipeline-rules.md` still said "Use exactly one configured LM Studio model", and the model read it. | Executor reasoning trace quoted the line. | Fixed. The rules now describe the three-model mesh, the protocol keys, and that commands cannot be run. Index re-embedded 2 chunks. |
| C10 | My copy step overwrote `spec_root` (regex `root = "..."` also matched inside `spec_root = ...`), so discovery found no goal files. | `init-state: queued 0 tasks; 0 quarantine reports`. | Process error in the copy only. Config of the real workspace is unchanged. |
| L8 | 49 goal sections were rejected by the parser during `init-state`. | Reasons seen: "unrecognized legacy cd root" (M1 goal files) and "missing declared PowerShell validation block" (M4 goal files). | Open. The parser drops a whole goal file when any section fails, so only 10 of the available tasks were queued. Decide: fix the goal files, widen the accepted `cd` aliases, or parse per section. |
| L9 | The executor spent 691 of 735 completion tokens on reasoning (`reasoning_content`) for a trivial task. | Response artifact for `M1.G1.T1`. | Open. The 1024-token output reserve may truncate longer tasks. Watch the first successful runs. |
| D6 | Tasks that only check the environment (such as `M1.G1.T1`: `node -v`) have no file to change, and the executor cannot run commands. | The executor tried to run them. | Open decision. The rules now tell it to write a note to `local-ai/notes/<task_id>.md`. Alternative: let Python run the declared validation first and skip the executor when it already passes. |
| P4 | Some shell calls returned no output or ran from the wrong directory. | Several empty output files. | Mitigation: script files launched with `powershell -File`, and `Set-Location` inside the script. |

Next live steps once L7 is fixed: `measure`, then `run-once` on the copy (Task `M1.G1.T1`), then inspect the audit verdict for false positives (the 1B auditor quarantines on a failed verdict).
Test suite after these fixes: 174 passed, 1 skipped.

## Task 13 attempt 2 (speculative decoding off)

`measure` PASS (1583 MiB free, no draft model in any reply). `run-once` on the copy, task `M1.G1.T1`:
- Router and executor both returned schema-valid replies. The executor produced a valid `write_file` operation (C8 fixed live).
- The task was quarantined at validation: `package command activity is denied`.

| # | Finding | Evidence | Status |
|---|---------|----------|--------|
| C11 | `CommandGuard` denies every `npm`/`yarn`/`pnpm`/`pip` command, including `npm -v`, `npm test`, `npm run typecheck`. Design text says only package download/install commands are denied. | `protocol-records/M1_G1_T1/*-rejected.json`, `denylist_category: package` | Open decision. Nearly every goal task validates with an npm script, so none can complete while this stands. |
| L10 | For a check-only task the executor wrote a note claiming "Prerequisites verified successfully" although nothing was run. | `local-ai/notes/M1.G1.T1.md` | Open. The note is not evidence. Only Python-run validation counts. |
