---
name: stage-4b-local-execution
description: Stage 4b of the Modular AI Engineering Pipeline. Execution of the python orchestrator using Bonsai CoT planning and Gemma code execution.
---

# Stage 4b: Local Agentic Execution

## Purpose

Stage 4b executes the automated Python orchestrator harness created in Stage 4a across the 1,000-task backlog.

## Execution Division of Labor

1. **Bonsai 2 27B PTQ1 (Reasoning / CoT Generator)**: Parses task requirements and generates concise step-by-step logic plans (`task_N_CoT.md`).
2. **Gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF (Code Execution Workhorse)**: Ingests `task_N_CoT.md` and outputs clean, production-grade code directly into target files via local LM Studio stateless requests.

## Workflow Execution

Python handles task queuing, runs pre-flight AST checks, selects the active mode, dispatches stateless requests, verifies linter/compiler passes, and updates `docs/master/progress-tracker.md` after each task completion.