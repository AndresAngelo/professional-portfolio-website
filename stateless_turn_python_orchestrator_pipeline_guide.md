# Stateless Turn Python Orchestrator Pipeline Guide

## Overview & Hardware Boundaries
This architecture guide details the setup for a deterministic, local-first multi-AI development pipeline optimized for an **8GB VRAM RTX 5070 laptop GPU**. 

When executing a ~1,000-task software project derived from 6 Master Artifacts (PRD, TRD, App Flow, Design Brief, Background Schema, Implementation Plan) and Kiro spec documents, continuous long-context chat sessions degrade speed, consume excessive VRAM, and cause instruction drift. This setup uses a **Stateless Turn Pattern** managed by a **Deterministic Python Orchestrator** to guarantee stable VRAM allocation, high generation speed, and zero context poisoning.

---

## 1. Model & Hardware Division of Labor

The hardware footprint relies on strict separation between high-level cloud planning, local reasoning, and low-latency local execution:

```
┌─────────────────────────────────────────────────────────────┐
│ Google AI Studio (Cloud - 1M Context Window)                │
│ Role: Macro-Scaffolding Architect                           │
│ Task: Ingests 6 Master Artifacts & Kiro specs to generate  │
│       initial project file trees and interface stubs.       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ gemma-3-1b-it-qat (Local GPU, context 2048)                 │
│ Role: Router and Auditor                                    │
│ Task: Turns retrieved chunks into a schema-valid plan, then │
│       audits the executor's change against the TRD rules.   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ gemma-4-e2b-it-qat@q4_k_xl (Local GPU, context 4096)        │
│ Role: Execution Workhorse                                   │
│ Task: Ingests the router plan and active context files;     │
│       outputs clean, syntax-compliant code via LM Studio.   │
└─────────────────────────────────────────────────────────────┘
```

### Why a Resident Three-Model Mesh Fits 8GB VRAM:
1. **`gemma-3-1b-it-qat` (Router and Auditor):** Small enough to stay loaded next to the executor. Its replies are constrained to JSON schemas and validated with Pydantic, so a weak reply is rejected and retried instead of trusted.
2. **`gemma-4-e2b-it-qat@q4_k_xl` (Execution Workhorse):** Fast and small. It receives a pre-filtered plan and retrieved context, so it can focus on syntax generation and file manipulation.
3. **`text-embedding-nomic-embed-text-v1.5` (Retrieval):** Ranks spec and context chunks so only the relevant ones reach the router.

No model is swapped during the run. The orchestrator verifies loaded identifiers and context caps at startup and fails closed.

---

## 2. The Stateless Turn Pattern

The core principle of this architecture is **Stateless Context Management**. Instead of maintaining a running conversation across tasks, every interaction with the local inference server (LM Studio / Ollama) is a single, isolated turn.

### Core Mechanics:
- **Zero KV Cache Bloat:** Closing and resetting the HTTP request after each task flushes the KV Cache completely. VRAM usage resets back to baseline, preventing GPU memory exhaustion across 1,000 tasks.
- **Immunity to Context Poisoning:** Errors or invalid assumptions made during Task #42 are automatically discarded when the session closes. Task #43 starts in a completely clean environment and cannot inherit context corruption.
- **The 3-Bucket Context Structure:** Every request constructs a context payload adhering to three distinct layers:
  1. *System Rules (Static Top Anchor):* Coding standards and output constraints (`6modular_pipeline_rules.md`).
  2. *Architecture Schema (Static Middle Anchor):* Types, DB schemas, and interfaces (`architecture_schema.md`).
  3. *Active Task Scope (Dynamic Bottom Anchor):* The router plan, retrieved chunks, and target source file stubs.

---

## 3. The Community-Backed 4-State Python Orchestrator

Rather than allowing the LLM to manage its own execution loop (which leads to off-by-one errors and broken file paths), a **deterministic Python script** manages execution state.

### The 4 Interceptor Modes

The orchestrator dynamically selects one of four specialized mode drivers based on pre-flight file system checks and post-flight linter validation:

```
                            [Python Script Task Loop]
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
       [Pre-Flight Checks]                        [Post-Flight Checks]
                  │                                         │
     ┌────────────┴────────────┐                            │
     ▼                         ▼                            ▼
[Target Missing?]    [Dependencies Broken?]         [Linter Failed?]
     │                         │                            │
     ▼                         ▼                            ▼
Scaffold-mode.md        Aligner-mode.md               Error-mode.md
(Creates file template) (Generates interface stubs) (Injects compiler stderr)
     │                         │                            │
     └────────────────────┬────┘                            │
                          │                                 │
                          ▼                                 │
                 CoT-Task-mode.md ◄─────────────────────────┘
                 (Standard Execution)
```

| Execution Mode | Trigger Condition | Operational Function |
| :--- | :--- | :--- |
| **`CoT-Task-mode.md`** | **Default.** Pre-flight pass: target file exists and interfaces align. | Standard code generation following the router plan. |
| **`Scaffold-mode.md`** | Pre-flight check fails: target file path does not exist on disk. | Generates directory paths and creates initial boilerplate file templates. |
| **`Aligner-mode.md`** | Pre-flight check fails: missing imports or mismatched AST signatures detected. | Generates missing interface contracts, type stubs, or imports before coding. |
| **`Error-mode.md`** | Post-flight check fails: Python linter/compiler returns non-zero error trace. | Injects `stderr` error logs into context to force a targeted syntax fix. |

---

## 4. Real-World Execution Math & Frequency Analysis

Modes do **NOT** run sequentially for every task. They represent conditional branches in a state machine. Across ~1,000 tasks, execution breaks down as follows:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ TOTAL PIPELINE EXECUTION: ~1,050 to 1,200 Stateless Turns                │
├──────────────────────────────────────────────────────────────────────────┤
│ 1. CoT-Task-mode.md : ~1,000 Turns (100% Frequency - 1 per task)          │
│ 2. Scaffold-mode.md : ~30 to 50 Turns (~3–5% Frequency - per new file)   │
│ 3. Aligner-mode.md  : ~50 to 100 Turns (~5–10% Frequency - on drift)    │
│ 4. Error-mode.md    : ~20 to 50 Turns (~2–5% Frequency - linter retry)   │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Total Network Turns:** ~1,050–1,200 stateless HTTP POST calls (NOT 4,000 calls).
- **VRAM Lifecycle:** Memory is flushed 1,000+ times, maintaining a constant ~2GB–7GB VRAM profile on your RTX 5070 without memory leakage.

---

## 5. Direct Instructions for GPT 5.6 Luna

When instructing **GPT 5.6 Luna** (or any advanced meta-prompting orchestrator) to write or modify the Python runner script for this pipeline, feed it the following specification block:

```markdown
### SYSTEM INSTRUCTION FOR GPT 5.6 LUNA: BUILD STATELESS ORCHESTRATOR SCRIPT

You are tasked with generating a production-grade Python Orchestrator Script for a 1,000-task AI engineering pipeline.

#### Hardware & Model Target:
- GPU VRAM: 8GB (RTX 5070 Laptop GPU)
- Local Server Endpoint: LM Studio REST API (`http://127.0.0.1:1234/v1`)
- Embedding Model: `text-embedding-nomic-embed-text-v1.5`
- Router and Auditor Model: `gemma-3-1b-it-qat`
- Code Execution Model: `gemma-4-e2b-it-qat@q4_k_xl`

#### Structural Requirements for the Generated Python Script:
1. **Stateless Request Loop:**
   - Must use standard `requests.post` or `OpenAI()` client pointing to LM Studio.
   - Must NOT persist messages array across task iterations. Each task must send a fresh payload containing:
     `[Rules Markdown] + [Architecture Schema Markdown] + [Mode Driver] + [Router Plan] + [Active Source File]`
   
2. **Resident Model Mesh:**
   - Do not load or unload models. Verify the loaded identifiers and context caps through LM Studio's model endpoints and fail closed on a mismatch.
   - Pass 1-2: retrieve chunks with the embedding model, then get a schema-valid plan from the router.
   - Pass 3-4: run the executor and declared validation, then audit with the router.

3. **4-State Interceptor Machine:**
   - **Scaffold Interceptor:** Check if target file path exists. If not, load `Scaffold-mode.md`, write empty file stub.
   - **Aligner Interceptor:** Run an AST/import check on target file. If dependencies are missing, load `Aligner-mode.md`.
   - **CoT-Task Mode:** Standard execution using `CoT-Task-mode.md`.
   - **Error Interceptor:** Post-execution, run `subprocess.run(["python3", "-m", "py_compile", target_file])` (or equivalent syntax check). If `returncode != 0`, trigger `Error-mode.md` with `stderr` log. Cap retries at 3 attempts per task.

4. **Response Cleaning & Output Validation:**
   - Programmatically strip markdown code fences (```python ... ```) from model response strings before writing output files to disk.
   - Maintain a `failures.log` file for any task that exceeds maximum error retries.

Ensure the script is completely modular, fully commented, and includes robust exception handling for HTTP 429 and connection timeout errors.
```