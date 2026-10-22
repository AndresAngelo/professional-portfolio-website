---
name: stage-5-senior-qa-production-engineer
description: Stage 5 of the Modular AI Engineering Pipeline. Senior QA & Production Engineer using Cursor IDE and CodeRabbit integration.
---

# Stage 5: Senior QA & Production Engineer (Cursor + CodeRabbit)

## Purpose

Stage 5 represents the final verification, security audit, and deployment gateway using **Cursor IDE**. It ingests the fully implemented codebase from Stage 4b to conduct static code analysis, unit/E2E testing, accessibility checks, and production deployment.

## Enhanced Code Inspection with CodeRabbit

To maximize code quality and catch edge-case bugs before production deployment, Stage 5 includes an **automated walkthrough and installation guide for CodeRabbit**:

### CodeRabbit Integration & Walkthrough Steps

1. **Installation & Repository Binding**:
   - Install the CodeRabbit app via GitHub Marketplace on the target repository.
   - Add `.coderabbit.yaml` to the root directory with custom review guidelines aligned with `master-files/AGENTS.md` and `master-files/design.md`.

2. **Automated AI Code Reviews**:
   - CodeRabbit performs line-by-line static analysis on every pull request, flagging security vulnerabilities, type mismatches, and memory leaks.
   - Provides automated sequence diagram generation and summary walkthroughs for complex PRs.

3. **Cursor + CodeRabbit Collaborative QA Loop**:
   - Cursor IDE reads CodeRabbit PR review comments via GitHub CLI (`gh pr view`).
   - Senior QA Engineer uses Cursor Agent mode to apply targeted automated fixes for any issue flagged by CodeRabbit.

## Final Deliverables

- Complete QA audit report (lint, security, performance, accessibility).
- Verified test suite executions (Unit, Integration, E2E).
- CodeRabbit PR review sign-off.
- Production deployment configuration and live deployment logs.