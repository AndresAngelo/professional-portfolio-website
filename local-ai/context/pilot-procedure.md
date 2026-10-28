# Controlled local pilot procedure

This document is consumed by the CLI composition as the operator procedure for the
explicit `pilot --enable-pilot` path. A pilot is deliberately limited to one selected
task and must not be used to process a queue.

## Required preflight

1. Confirm `local-ai/config/orchestrator.toml` resolves the intended workspace and
   keeps `local-ai/` beneath it.
2. Confirm the persisted `local-ai/program-states/run-state.json` is valid for that
   workspace. Do not repair or replace it automatically.
3. Confirm the configured LM Studio URL uses `127.0.0.1` or `localhost` only.
4. Query and retain a local runtime capability record before pilot work. Refuse the
   pilot when configuration, state, endpoint locality, or capability evidence is
   unsafe.
5. Invoke `python -m orchestrator pilot --enable-pilot` only after completing the
   checks above.

The pilot retains default runtime settings. Benchmark settings are considered only by
an explicitly enabled `benchmark --enable-benchmark` command. Neither command may
perform Git mutations, access general outbound endpoints, install dependencies, or
run undeclared commands.

## Local artifact locations

All evidence remains below `local-ai/` in the configured workspace:

- `program-states/run-state.json` and `program-states/scheduler.lock` hold durable
  selection and local lock evidence.
- `plans/` holds planner output.
- `protocol-records/` holds request, response, and protocol execution evidence.
- `validation/` holds declared-command stdout, stderr, and exit metadata.
- `telemetry/requests.ndjson` holds benchmark request telemetry and runtime
  capability records are written below `telemetry/runtime/`.
- `quarantine/` holds unsafe input, state, transport, and permanent-failure reports.

Stop after the one selected task. Preserve partial changes and review local artifacts
instead of automatically retrying beyond the configured policy.
