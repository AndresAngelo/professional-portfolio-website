---
name: stage-1-research-and-specs-hub
description: Stage 1 of the Modular AI Engineering Pipeline. Research & Specs Hub using Gemini Custom Gem to perform deep research and synthesize the 6 master spec files inside the "master-files" directory.
---

# Stage 1: Research & Specs Hub (Gemini Gem)

## Purpose

Stage 1 is the Research & Specs Hub powered by a Custom Gemini Gem. Its responsibility is to conduct web-backed research and synthesize the 6 foundational master spec files that govern the entire pipeline. All 6 master files are created, organized, and stored inside the designated `master-files/` folder in the repository root.

## Directory Structure

All outputs from Stage 1 must reside within:

master-files/
├── PRD.md (Product Requirements Document)
├── TRD.md (Technical Requirement Document)
├── APP_FLOW.md (App Flow & User Story Specification)
├── design.md (Design Brief & System Specification)
├── AGENTS.md (Background Schema & Repository Context)
└── ROADMAP.md (Implementation Plan & Agentic Execution Roadmap)

## Inputs

- Stage 0 meta-prompt and Obsidian context retrieval directives.
- Project domain requirements, technical constraints, UI preferences, and API schemas.

## Outputs & Master Spec Files (`master-files/`)

1. **PRD (Product Requirements Document)** (`master-files/PRD.md`): Core business goals, product vision, user personas, and P0/P1 feature priorities.
2. **TRD (Technical Requirement Document)** (`master-files/TRD.md`): Architecture stack, API endpoint contracts, SLAs, performance metrics, and database requirements.
3. **App Flow & User Story Specification** (`master-files/APP_FLOW.md`): User journey maps, UX interaction tables, and EARS-formatted acceptance criteria.
4. **Design Brief & System Specification** (`master-files/design.md`): Color tokens, typography hierarchy, spacing grid, and UI component standards.
5. **Background Schema & Repository Context** (`master-files/AGENTS.md`): ERDs, SQL definitions, non-negotiable guardrails, and tool permission boundaries.
6. **Implementation Plan & Agentic Execution Roadmap** (`master-files/ROADMAP.md`): Dependency matrix, task sequences, and verification check commands.

## Allowed Actions

- Conduct deep live web research using Gemini's search grounding.
- Create and incrementally refine all 6 master files within `master-files/`.
- Ensure zero-hallucination consistency across all 6 documents before handing off.

## Forbidden Actions

- No implementation code generation.
- No placing master files outside of the `master-files/` directory.
- No silent assumptions or unverified architectural claims.