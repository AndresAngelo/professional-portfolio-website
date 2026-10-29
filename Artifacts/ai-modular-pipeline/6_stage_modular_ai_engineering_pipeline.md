---
name: six-stage-modular-ai-engineering-pipeline
description: Root architecture and operating guide for the 6-Stage Modular AI Engineering Pipeline. Governs deterministic handoffs from initial context gathering to local agentic execution and production QA.
---

# 6-Stage Modular AI Engineering Pipeline

## Purpose

This document defines the master operating framework for the **6-Stage Modular AI Engineering Pipeline**. It governs how specialized AI agents interact across six deterministic stages to deliver zero-hallucination, spec-driven engineering projects.

It enforces repository state as the single source of truth, eliminates context drift, avoids commercial paywalls through free-tier/local-first tools, and orchestrates local agentic code generation.

---

## Crew & Stage Overview Matrix

| Stage | Role / Name | Tool / Platform | Primary Responsibility | Key Deliverables & Output Location |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 0** | Context Gatherer & Orchestrator | Hermes Local AI + Obsidian Vault | Ingest user intent, maintain persistent second-brain context, and generate meta-prompts. | Meta-prompts & context directives (`docs/master/`) |
| **Stage 1** | Research & Specs Hub | Custom Gemini Gem (Web Grounded) | Deep web research and synthesis of the 6 core master specification files. | `master-files/` (PRD, TRD, APP_FLOW, design, AGENTS, ROADMAP) |
| **Stage 2** | Spec-Driven Development | Kiro IDE (Qwen Coder Next + Claude Haiku) | Transform master specs into a 3-layer ~1,000-task execution hierarchy ($10 \times 10 \times 10$). Produces `tasks.md` per milestone containing the 10-goals structure and Stage 3 delegation instructions only. | `specs/M[N]/` (`requirements.md`, `design.md`, `tasks.md`) |
| **Stage 3** | Scaffolding & Framework Architect | Google AI Studio API in VS Code Agent Chat | Ingest 1M+ token context (master-files, pipeline specs, all `tasks.md` files) to: (1) generate `goal1.md`–`goal10.md` per milestone, each with ~10 fully-detailed atomic tasks, then (2) produce zero-placeholder scaffolding. | `specs/M[N]/goal[1-10].md`, core directory tree, manifests, DDLs, and `HANDOFF.md` |
| **Stage 4a** | Orchestrator Pipeline Creator | Codex / Python | Construct the local, deterministic Python orchestrator harness using the Stateless Turn Pattern. | Python orchestrator scripts & 4 mode prompts (`local-ai/`) |
| **Stage 4b** | Local Agentic AI Workhorse | Python Harness + LM Studio (RTX 5070 8GB) | Four-pass pipeline over three resident models: nomic embeddings (retrieval), gemma-3-1b router and auditor, gemma-4-e2b executor. | Fully implemented codebase, `local-ai/program-states/progress-tracker.md` |
| **Stage 5** | Senior QA & Production Engineer | Cursor IDE + CodeRabbit | Static code inspection, unit/E2E testing, security audits, and production deployment. | Audit report, `.coderabbit.yaml`, verified test suite, deployment |

---

## Detailed Stage Definitions

### Stage 0: Hermes Local AI Setup & Context Gatherer
- **Engine**: Hermes Agent paired with a local Obsidian Vault (Second Brain).
- **Core Responsibilities**:
  - Index and retrieve persistent conversation history, architectural preferences, and domain constraints from Obsidian.
  - Translate raw, unformatted user intent into structured meta-prompts tailored for Stages 1 through 5.
  - Maintain zero-hallucination alignment with local engineering mandates.

---

### Stage 1: Research & Specs Hub (Gemini Gem)
- **Engine**: Custom Gemini Gem with Web Search Grounding.
- **Core Responsibilities**:
  - Perform live web-backed technical research for libraries, API contracts, and architectural best practices.
  - Synthesize the **6 Master Spec Files** and write them directly into the `master-files/` directory:
    1. `master-files/PRD.md`: Business goals, scope, and feature priorities.
    2. `master-files/TRD.md`: Tech stack, API endpoints, performance SLAs, and DB schema.
    3. `master-files/APP_FLOW.md`: User journeys, interaction maps, EARS acceptance criteria.
    4. `master-files/design.md`: Visual tokens, typography hierarchy, UI standards.
    5. `master-files/AGENTS.md`: SQL schemas, ERDs, non-negotiable boundaries.
    6. `master-files/ROADMAP.md`: Task execution roadmap and verification commands.

---

### Stage 2: Spec-Driven Development (Kiro)
- **Engine**: Kiro IDE utilizing Qwen Coder Next (planning) and Claude Haiku (spec drafting).
- **Core Responsibilities**:
  - Deconstruct `master-files/` into a deterministic **3-Layer Task Hierarchy (~1,000 tasks)**:
    - **Layer 1: Milestones (~10)** — Project macro phases.
    - **Layer 2: Goals (~10 per Milestone)** — Functional subsystems and modules.
    - **Layer 3: Tasks (~10 per Goal)** — Atomic, testable execution tasks.
  - Output spec artifacts directly into `specs/` (accessible directly by VS Code agents):
    - `specs/M[N]/requirements.md`
    - `specs/M[N]/design.md`
    - `specs/M[N]/tasks.md` — Contains the **10-goals skeleton only** (goal names, success criteria, task list stubs, and delegation instructions for Stage 3). Individual task detail is **not** authored in Kiro to avoid file size limits.
  - `tasks.md` includes an explicit instruction block telling Stage 3 (Google AI Studio) how to expand each goal into a separate `goal[N].md` file.

---

### Stage 3: Google AI Studio API on VS Code Agent Chat
- **Engine**: Google AI Studio API loaded inside VS Code Agent Chat.
- **Core Responsibilities**:
  - Leverage the **1,000,000+ Token Context Window** to absorb:
    1. All 6 files in `master-files/`.
    2. All control files inside `ai-modular-pipeline/`.
    3. All spec-driven files in `specs/` (`requirements.md`, `design.md`, `tasks.md` per milestone).
  - **Goal File Generation (pre-scaffolding step):** For each milestone, read `tasks.md` and generate 10 separate goal files (`goal1.md` through `goal10.md`) inside the milestone folder. Each goal file contains ~10 fully-detailed atomic tasks with: objective, acceptance criteria, prerequisites, implementation details with code, validation steps, and requirements traceability.
  - **Scaffolding:** After all goal files are generated, produce complete initial project scaffolding, package manifests (`package.json`, `tsconfig.json`), component stubs, and `HANDOFF.md` without placeholder code.

---

### Stage 4a: Stateless Turn Python Orchestrator Pipeline
- **Engine**: Python script harness created via Codex.
- **Core Responsibilities**:
  - Define a 4-mode conditional execution loop:
    1. `CoT-Task-mode.md` (~1,000 runs — 100% frequency): Primary task execution pass.
    2. `Scaffold-mode.md` (~30–50 runs — ~3–5% frequency): Triggered when creating brand-new files.
    3. `Aligner-mode.md` (~50–100 runs — ~5–10% frequency): Triggered on import/type contract mismatch.
    4. `Error-mode.md` (~20–50 runs — ~2–5% frequency): Triggered when linter or compiler stderr fails.

---

### Stage 4b: Local Agentic Execution & Resident Model Mesh
- **Hardware Baseline**: ASUS TUF A14/A16 (2025) | AMD Ryzen 9 | NVIDIA RTX 5070 Laptop GPU (8GB VRAM) | 32GB RAM.
- **VRAM Constraint & Solution**:
  - **gemma-3-1b-it-qat** (router and auditor): context 2048, output reserve 512 tokens.
  - **gemma-4-e2b-it-qat@q4_k_xl** (executor): context 4096, output reserve 1024 tokens. **text-embedding-nomic-embed-text-v1.5** (retrieval): context 2048.
  - All three models stay resident together. The speculative-decoding draft model and the vision projector must be off, and at least 700 MiB of VRAM must stay free.
  - The orchestrator never loads or unloads a model. It verifies the loaded models and context caps at startup and fails closed on a mismatch.

#### Resident Model Mesh Execution Flow
For every task $N$ in the execution queue:

```
┌─────────────────────────────────────────────────────────────┐
│                 PYTHON ORCHESTRATOR LOOP                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
       Pass 1-2: RETRIEVAL + ROUTING (nomic embeddings, gemma-3-1b router)
       ├── 1. Embed the task query and retrieve the top chunks from the local index
       ├── 2. Router returns a schema-valid plan (constraints, target paths, chunk IDs)
       └── 3. No model is loaded or unloaded; all three stay resident
                               │
                               ▼
       Pass 3-4: EXECUTION + AUDIT (gemma-4-e2b executor, gemma-3-1b auditor)
       ├── 1. Verify loaded models and context caps (fail closed)
       ├── 2. Perform pre-flight mode check (Scaffold / Aligner)
       ├── 3. Execute code generation pass (`CoT-Task-mode.md`)
       ├── 4. Run post-flight syntax linter (Trigger `Error-mode.md` on failure)
       └── 5. Update state tracker files
                               │
                               ▼
            [Advance to Task N+1 cleanly]
```

#### State Tracking Locations (Stage 4 Output)
All stage 4 execution states, logs, and tracking metrics reside in `local-ai/`:
- `local-ai/program-states/progress-tracker.md`
- `local-ai/program-states/current-issues.md`
- `local-ai/embeddings/index.json`

---

### Stage 5: Senior QA & Production Engineer (Cursor + CodeRabbit)
- **Engine**: Cursor IDE paired with CodeRabbit GitHub App integration.
- **Core Responsibilities**:
  - **CodeRabbit Automated Review**: Run static analysis on PRs, checking against `master-files/AGENTS.md` and `master-files/design.md`.
  - **Cursor Agent Remediation**: Consume CodeRabbit review comments via GitHub CLI (`gh pr view`) and automatically apply fixes.
  - Verify unit, integration, and E2E test suites before tagging release deployments.

---

## Operating Principles & Review Gates

1. **Specs Before Code**: No agent generates feature code without an active specification in `specs/`.
2. **Repository State as Source of Truth**: Conversation memory is ephemeral. Session progress MUST be written to `local-ai/program-states/progress-tracker.md`.
3. **Hard Review Gates**:
   - **Gate 1**: User approves `master-files/` before Stage 2 begins.
   - **Gate 2**: User approves Kiro `specs/` and Stage 3 scaffold before Stage 4 execution.
   - **Gate 3**: CodeRabbit PR sign-off and complete test suite verification before Stage 5 deployment.