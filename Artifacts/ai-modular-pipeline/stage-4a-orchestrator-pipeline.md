---
name: stage-4a-orchestrator-pipeline
description: Stage 4a of the Modular AI Engineering Pipeline. Creation of the Stateless Turn Python Orchestrator Pipeline using Codex and execution math analysis.
---

# Stage 4a: Stateless Turn Python Orchestrator Pipeline

## Architecture Overview

Stage 4a defines the creation of a deterministic Python orchestrator script using **Codex**. The orchestrator manages task execution wave-by-wave, running locally on an RTX 5070 (8GB VRAM) under the **Stateless Turn Pattern**.

## The 4-Mode Orchestrator Logic & Real-World Execution Math

When evaluating the 4 operational modes across ~1,000 tasks, **modes do NOT run sequentially for every single task**. They are conditional fallback branches, not a linear 4-pass checklist.

### Real-World Session Execution Breakdown (~1,050–1,200 Total Turns):

1. **`CoT-Task-mode.md` (~1,000 Runs — 100% Frequency)**
   - Core implementation pass. Every task runs this baseline mode once it reaches the front of the execution queue.
2. **`Scaffold-mode.md` (~30–50 Runs — ~3–5% Frequency)**
   - Pre-flight file system check. Triggers *only* when starting a brand new file path on disk to generate initial scaffolding stubs.
3. **`Aligner-mode.md` (~50–100 Runs — ~5–10% Frequency)**
   - Corrective pre-flight pass. Triggers *only* if Python AST or linter detects missing imports, interface drift, or broken type contracts before coding.
4. **`Error-mode.md` (~20–50 Runs — ~2–5% Frequency)**
   - Post-flight retry loop. Triggers *only* if compiler stderr or linter returns an error after execution, injecting logs for a targeted syntax fix.

### Memory & VRAM Efficiency
Total pipeline calls range between **1,050 to 1,200 stateless turns** (rather than 4,000). Because every turn is completely stateless, VRAM automatically flushes after each API call, locking memory usage safely below the 8GB VRAM limit.