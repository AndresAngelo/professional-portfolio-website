---
name: stage-4b-local-execution
description: Stage 4b of the Modular AI Engineering Pipeline. Execution of the python orchestrator using Bonsai CoT planning and Gemma code execution.
---

# Stage 4b: Local Agentic Execution

## Purpose

Stage 4b executes the automated Python orchestrator harness created in Stage 4a across the 1,000-task backlog.

## Execution Division of Labor

1. **google/gemma-4-12b-qat (Reasoning / CoT Generator)**: Parses task requirements and generates concise step-by-step logic plans (`task_N_CoT.md`).
2. **google/gemma-4-e2b (Code Execution Workhorse)**: Ingests `task_N_CoT.md` and outputs clean, production-grade code directly into target files via local LM Studio stateless requests.

## Workflow Execution

Python handles task queuing, runs pre-flight AST checks, selects the active mode, dispatches stateless requests, verifies linter/compiler passes, and updates `docs/master/progress-tracker.md` after each task completion.