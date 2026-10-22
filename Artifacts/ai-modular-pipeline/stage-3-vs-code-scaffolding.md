---
name: stage-3-vs-code-scaffolding
description: Stage 3 of the Modular AI Engineering Pipeline. Uses Google AI Studio API inside VS Code Agent Chat (1M+ token context) to: (1) generate goal1.md–goal10.md per milestone with ~10 fully-detailed atomic tasks each, then (2) produce zero-placeholder project scaffolding and HANDOFF.md.
---

# Stage 3: Google AI Studio API on VS Code Agent Chat

## Purpose

Stage 3 uses the **Google AI Studio API directly within VS Code Agent Chat** to perform two sequential responsibilities:

1. **Goal File Generation** — Expand each milestone's `tasks.md` skeleton into 10 separate `goal[N].md` files, each containing ~10 fully-detailed atomic tasks ready for stateless orchestrator execution.
2. **Project Scaffolding** — Generate the complete initial repository structure, package manifests, component stubs, and `HANDOFF.md` without any placeholder code.

Both steps leverage the **1,000,000+ token context window** to maintain full architectural fidelity across all milestones simultaneously.

---

## Context Absorption

Before beginning either step, the Stage 3 session absorbs the following in order:

| # | Source | Contents |
| :--- | :--- | :--- |
| 1 | `master-files/` | PRD, TRD, APP_FLOW, design.md, AGENTS.md, ROADMAP.md (6 files) |
| 2 | `ai-modular-pipeline/` | All pipeline control files including this document |
| 3 | `.kiro/specs/M[N]/requirements.md` | EARS requirements per milestone |
| 4 | `.kiro/specs/M[N]/design.md` | Technical architecture per milestone |
| 5 | `.kiro/specs/M[N]/tasks.md` | 10-goals skeleton + Stage 3 Delegation Instructions per milestone |

---

## Responsibility 1: Goal File Generation

This step runs **before scaffolding** and must complete for all milestones before any scaffolding code is written.

### Input

For each milestone M[N], read `tasks.md` and extract:
- The 10 goal names and success criteria
- The stub task list (T1–T10 titles) per goal
- The **Stage 3 Delegation Block** at the bottom of `tasks.md` (contains the Task Format Contract)

### Output

For each milestone M[N] and each goal G[X] (1–10), write one file:

```
.kiro/specs/M[N]-[kebab-name]/goal[X].md
```

Example for M2:
```
.kiro/specs/m2-content-architecture-validation/
├── goal1.md    ← M2.G1: Zod Schema Infrastructure Setup (10 tasks)
├── goal2.md    ← M2.G2: Enum Schemas (10 tasks)
├── goal3.md    ← M2.G3: SiteConfig Schema & Loader (10 tasks)
├── goal4.md    ← M2.G4: Project Schemas & Loaders (10 tasks)
├── goal5.md    ← M2.G5: Certification Schemas & Loaders (10 tasks)
├── goal6.md    ← M2.G6: BlogPost Schemas & Loaders (10 tasks)
├── goal7.md    ← M2.G7: Markdown Rendering Pipeline (10 tasks)
├── goal8.md    ← M2.G8: Type Inference & Type Safety (10 tasks)
├── goal9.md    ← M2.G9: Build-Time Validation Integration (10 tasks)
└── goal10.md   ← M2.G10: Testing & Documentation (10 tasks)
```

### Goal File Structure

Each `goal[X].md` must follow this exact structure:

```markdown
# M[N].G[X]: <Goal Name>

> **Milestone:** M[N] — <Milestone Name>
> **Goal:** G[X] of 10
> **Tasks:** ~10 atomic tasks
> **Status:** NOT STARTED

## Goal Objective

<One paragraph describing what this goal accomplishes and why it matters.>

## Goal Success Criteria

- ✓ <Observable criterion 1>
- ✓ <Observable criterion 2>
- ...

## Prerequisites

- <What must be complete before this goal begins (goal-level, not task-level)>

---

## Tasks

### M[N].G[X].T1: <Action-Oriented Task Name>

**Objective:** <One sentence.>

**Acceptance Criteria:**
- ✓ <Testable outcome 1>
- ✓ <Testable outcome 2>
- ...

**Prerequisites:**
- <Full file paths, installed deps, state assumptions — no "see previous task">

**Implementation Details:**

<Step-by-step instructions with actual TypeScript/shell/config code blocks.>

**Validation:**
```bash
# Exact command(s) to confirm task completion
npm run typecheck
```
Expected: <what success looks like>

**Satisfies Requirements:** Req X.Y, X.Z

---

### M[N].G[X].T2: <Next Task Name>
...

(repeat for T3–T10)

---

## Goal Checkpoint

Run the following to confirm all tasks in this goal are complete:
```bash
<goal-level verification command>
```
Expected: <success output>
```

### Task Format Contract (from tasks.md Delegation Block)

Every task inside a goal file must be **fully self-contained**:

| Section | Requirement |
| :--- | :--- |
| **Title** | `M[N].G[X].T[Y]: <Action-Oriented Name>` |
| **Objective** | One sentence: what this task accomplishes |
| **Acceptance Criteria** | 4–8 bullet points, observable and testable |
| **Prerequisites** | Full file paths, installed deps, state assumptions — no "see previous task" |
| **Implementation Details** | Step-by-step with actual TypeScript/shell code |
| **Validation** | Exact commands + expected output |
| **Satisfies Requirements** | Requirement numbers from `requirements.md` |

A stateless LLM with no conversation history must be able to execute each task from the task text alone. No placeholder text, no "TBD", no bare references to other documents without quoting the relevant excerpt inline.

---

## Responsibility 2: Project Scaffolding

After all goal files are generated and verified, Stage 3 produces the complete initial repository structure.

### Scaffolding Outputs

| Output | Description |
| :--- | :--- |
| `src/` directory tree | All source directories per AGENTS.md taxonomy |
| `package.json` | All dependencies pinned to exact versions |
| `tsconfig.json` | TypeScript strict mode config |
| `next.config.ts` | Next.js configuration with content validation hook stubs |
| `tailwind.config.ts` | Tailwind config with design token bindings from `design.md` |
| Component stubs | One stub per component defined in `design.md` / `APP_FLOW.md` |
| `content/` seed files | Minimal valid seed files for each content type |
| `HANDOFF.md` | Stage 3 → Stage 4a handoff document (see below) |

### Scaffolding Constraints

- **Zero placeholder code** — no `// TODO`, no `throw new Error('not implemented')`, no empty function bodies unless the function is intentionally a stub with a comment explaining what Stage 4b will fill in.
- All imports must resolve — no dangling import paths.
- `npm run typecheck` must pass on the scaffolded codebase before `HANDOFF.md` is written.
- Design tokens, color palette, and typography must come directly from `master-files/design.md`, not invented.

---

## HANDOFF.md Structure

`HANDOFF.md` is written at the repo root and contains:

```markdown
# Stage 3 → Stage 4a Handoff

## Scaffold Summary
- Total files created: N
- npm run typecheck: PASS / FAIL (with error list if FAIL)

## Goal File Index
| Milestone | Goal Files | Location |
| :--- | :--- | :--- |
| M1 | goal1.md – goal10.md | .kiro/specs/m1-.../  |
| M2 | goal1.md – goal10.md | .kiro/specs/m2-.../  |
| ...

## Stage 4a Entry Point
- Python orchestrator reads goal files in order: M1/goal1.md → M1/goal10.md → M2/goal1.md → ...
- Each task in each goal file is one stateless orchestrator turn
- State tracker: local-ai/program-states/progress-tracker.md

## Environment Config
- Node version: X.X.X
- Package manager: npm / pnpm
- Key scripts: npm run dev | build | typecheck | lint | test
```

---

## Stage 3 Execution Order

```
1. Absorb all context files (master-files, pipeline docs, all specs)
        ↓
2. For each milestone M1–M10:
   a. Read tasks.md → extract 10 goals + delegation instructions
   b. Generate goal1.md through goal10.md
   c. Verify each goal file has ~10 fully-detailed tasks
        ↓
3. Generate project scaffolding (zero-placeholder)
        ↓
4. Run npm run typecheck on scaffolded codebase
        ↓
5. Write HANDOFF.md
        ↓
6. Stage 3 complete → hand off to Stage 4a
```

---

## Review Gate

**Gate 2 (end of Stage 3):** User reviews:
- All `goal[1-10].md` files across all milestones (spot-check task detail quality)
- Scaffolded codebase passes `npm run typecheck`
- `HANDOFF.md` is accurate and complete

User approval required before Stage 4a (Python orchestrator construction) begins.
