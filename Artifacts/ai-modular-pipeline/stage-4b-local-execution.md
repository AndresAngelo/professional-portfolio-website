---
name: stage-4b-local-execution
description: Stage 4b of the Modular AI Engineering Pipeline. Execution of the python orchestrator over a resident three-model LM Studio mesh (embedding, router, executor).
---

# Stage 4b: Local Agentic Execution

## Purpose

Stage 4b executes the automated Python orchestrator harness created in Stage 4a across the 1,000-task backlog.

## Execution Division of Labor

1. **text-embedding-nomic-embed-text-v1.5 (Retrieval)**: Embeds spec and context chunks into `local-ai/embeddings/index.json` and ranks them for each task.
2. **gemma-3-1b-it-qat (Router and Auditor)**: Returns a schema-valid plan (constraints, target paths, chunk IDs), then audits the executor's change against the TRD rules.
3. **gemma-4-e2b-it-qat@q4_k_xl (Code Execution Workhorse)**: Receives the router plan and active files and returns one strict Tool Protocol JSON operation via local LM Studio stateless requests.

All three stay resident. The orchestrator never loads or unloads a model; it verifies loaded identifiers and context caps at startup and fails closed.

## Workflow Execution

Python handles task queuing, runs pre-flight AST checks, selects the active mode, dispatches stateless requests, verifies linter/compiler passes, and updates `docs/master/progress-tracker.md` after each task completion.