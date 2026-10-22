Here is the complete, self-contained **`goal10.md`** file for Milestone 1, generated according to the Stage 3 Task Format Contract.

Save this content to:  
`.kiro/specs/m1-repository-foundation-toolchain/goal10.md`

***

# M1.G10: Final Validation & Baseline Commit

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end verification pipeline (`install` $\rightarrow$ `format:check` $\rightarrow$ `lint` $\rightarrow$ `typecheck` $\rightarrow$ `test` $\rightarrow$ `build`) across the entire scaffolded repository. Finalize all architectural documentation (`README.md`, `next.config.ts`, `next-env.d.ts`), audit dependencies, verify clean Git hooks, tag the repository with `m1-baseline`, and record completion in the progress tracker to seal Milestone 1 and prepare for M2 (Content Architecture & Validation).

## Goal Success Criteria

- ✓ `README.md` created with prerequisites, script documentation, directory structure, architectural constraints, and master specification references
- ✓ `next.config.ts` configured with `output: 'export'` and `images.unoptimized: true`
- ✓ `next-env.d.ts` present and valid for Next.js types
- ✓ Full sequential pipeline execution passes cleanly: `npm ci && npm run lint && npm run typecheck && npm run test && npm run build`
- ✓ Git working tree is clean and tagged with `m1-baseline`
- ✓ `local-ai/program-states/progress-tracker.md` updated with Milestone 1 sign-off status

## Prerequisites

- Goals M1.G1 through M1.G9 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- All configurations, tokens, scripts, and tests committed and clean

---

## Tasks

### M1.G10.T1: Finalize Next.js Configuration (`next.config.ts`)

**Objective:** Configure `next.config.ts` for static export compatibility (`output: 'export'`), unoptimized image export, strict mode, and zero build error suppression.

**Acceptance Criteria:**
- ✓ `next.config.ts` imports `NextConfig` type
- ✓ `reactStrictMode` is set to `true`
- ✓ `output` is set to `'export'`
- ✓ `images.unoptimized` is set to `true`
- ✓ `typescript.ignoreBuildErrors` is set to `false`
- ✓ `eslint.ignoreDuringBuilds` is set to `false`

**Prerequisites:**
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\next.config.ts`

**Implementation Details:**
Write the finalized configuration using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: {
    unoptimized: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;
'@ | Set-Content "next.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "next.config.ts" -Raw
if ($cfg -match "output:\s*'export'" -and $cfg -match "unoptimized:\s*true") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 1.6

---

### M1.G10.T2: Verify Next.js Type Declarations (`next-env.d.ts`)

**Objective:** Ensure `next-env.d.ts` exists and references Next.js and image types for TypeScript compiler recognition.

**Acceptance Criteria:**
- ✓ `next-env.d.ts` exists in project root
- ✓ Contains `/// <reference types="next" />`
- ✓ Contains `/// <reference types="next/image-types/global" />`

**Prerequisites:**
- M1.G10.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\next-env.d.ts`

**Implementation Details:**
Create or verify `next-env.d.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "next-env.d.ts")) {
@'
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/api-reference/config/typescript for more information.
'@ | Set-Content "next-env.d.ts" -Encoding UTF8
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$dts = Get-Content "next-env.d.ts" -Raw
if ($dts -match '<reference types="next" />') { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2

---

### M1.G10.T3: Generate Comprehensive `README.md`

**Objective:** Author the master repository `README.md` documenting installation, scripts, architecture, quality gates, constraints, and specification links.

**Acceptance Criteria:**
- ✓ `README.md` exists in project root
- ✓ Contains Prerequisites (Node 18+, npm 9+)
- ✓ Documents all npm scripts (`dev`, `build`, `lint`, `typecheck`, `test`, `format`, `format:check`)
- ✓ Outlines AGENTS.md directory taxonomy
- ✓ Documents architectural boundaries (zero database, zero auth, zero custom APIs)
- ✓ References master spec files (`PRD.md`, `TRD.md`, `AGENTS.md`, `design.md`)

**Prerequisites:**
- M1.G10.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\README.md`

**Implementation Details:**
Write `README.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
# personal-website-portfolio-v2

A specification-driven, statically generated developer portfolio built with Next.js 15+ App Router, TypeScript strict mode, and Tailwind CSS with Singapore Government Design System (SGDS) semantic tokens.

## Prerequisites

- **Node.js:** `>= 18.0.0`
- **npm:** `>= 9.0.0`

## Getting Started

### Installation
```bash
npm ci
```

### Development
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the application.

## Verification Pipeline

All changes must pass the complete quality gate sequence prior to merging or deployment:
```bash
npm run format:check && npm run lint && npm run typecheck && npm run test && npm run build
```

### Available Scripts

| Script | Command | Purpose |
| :--- | :--- | :--- |
| `dev` | `next dev` | Starts local Next.js development server |
| `build` | `next build` | Generates static export production output into `out/` |
| `lint` | `next lint` | Executes ESLint checking type-safety and accessibility |
| `typecheck` | `tsc --noEmit` | Validates TypeScript strict mode and module resolution |
| `test` | `vitest run` | Runs unit and integration test suites in non-watch mode |
| `test:coverage`| `vitest run --coverage` | Generates V8 test coverage report |
| `format` | `prettier --write .` | Formats all supported files |
| `format:check`| `prettier --check .` | Verifies code formatting compliance |

## Architectural Constraints (P0 Scope)

Per `AGENTS.md` and `TRD.md`, the following boundaries are non-negotiable:
- ❌ **No runtime database:** No ORM, SQL drivers, or external DB connections.
- ❌ **No authentication:** No session management, JWT, or OAuth.
- ❌ **No custom public APIs:** No route handlers, API routes, or server actions.
- ❌ **No visitor tracking:** Zero analytics, third-party trackers, or personal data collection.
- ✅ **Static-first:** 100% pre-rendered HTML/CSS/JS served via CDN.
- ✅ **Local Content:** All portfolio data loaded from `content/` Markdown/MDX and JSON files.
- ✅ **Strict Types:** Zero `any`, non-null assertions (`!`), or unsafe type casting.

## Master Specifications

- **Product Requirements Document (PRD):** `PRD.md`
- **Technical Requirement Document (TRD):** `TRD.md`
- **Background Schema & Repository Context:** `AGENTS.md`
- **Design Brief & System Specification:** `design.md`
- **App Flow & User Stories:** `APP_FLOW.md`
- **Implementation Plan & Roadmap:** `implementation_plan.md`
'@ | Set-Content "README.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$readme = Get-Content "README.md" -Raw
if ($readme -match "Architectural Constraints" -and $readme -match "Verification Pipeline") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.4, Req 9.6, Req 9.9, Req 9.12, Req 15.1

---

### M1.G10.T4: Audit Dependency Trees and Vulnerability Checks

**Objective:** Audit `package.json` dependencies and ensure zero high or critical security vulnerabilities exist.

**Acceptance Criteria:**
- ✓ `npm audit` executes
- ✓ Direct dependencies report zero high or critical severity vulnerabilities

**Prerequisites:**
- M1.G10.T3 completed

**Implementation Details:**
Execute the audit command using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm audit --audit-level=high
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm audit --audit-level=high
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.10

---

### M1.G10.T5: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Verify that the completed codebase satisfies all ESLint, TypeScript, and jsx-a11y rules.

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ Zero warnings or errors reported

**Prerequisites:**
- M1.G10.T4 completed

**Implementation Details:**
Run ESLint via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run lint
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run lint
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.13, Req 11.2

---

### M1.G10.T6: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Confirm strict TypeScript compilation across all application modules, utilities, and tests.

**Acceptance Criteria:**
- ✓ `npm run typecheck` completes with code 0
- ✓ No missing type declarations or implicit `any` errors

**Prerequisites:**
- M1.G10.T5 completed

**Implementation Details:**
Run the typecheck command via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.10, Req 11.3

---

### M1.G10.T7: Execute Testing Quality Gate (`npm run test`)

**Objective:** Run all unit and integration test suites in non-watch mode.

**Acceptance Criteria:**
- ✓ `npm run test` executes
- ✓ All tests pass
- ✓ Exit code is 0

**Prerequisites:**
- M1.G10.T6 completed

**Implementation Details:**
Run Vitest via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.11, Req 11.4

---

### M1.G10.T8: Execute Static Production Build Quality Gate (`npm run build`)

**Objective:** Execute `next build` to verify full compilation and static HTML export to the `out/` directory.

**Acceptance Criteria:**
- ✓ `npm run build` completes with exit code 0
- ✓ `out/` directory contains `index.html` and static assets
- ✓ Build completes in under 3 minutes

**Prerequisites:**
- M1.G10.T7 completed

**Implementation Details:**
Execute the build command via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
if ($LASTEXITCODE -eq 0 -and (Test-Path "out\index.html")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 7.10, Req 11.5, Req 11.7

---

### M1.G10.T9: Commit and Tag Milestone 1 Baseline (`m1-baseline`)

**Objective:** Stage all final assets, commit with a standardized conventional commit message, and create the immutable Git tag `m1-baseline`.

**Acceptance Criteria:**
- ✓ All modified files committed
- ✓ Working tree is clean
- ✓ Git tag `m1-baseline` created on HEAD

**Prerequisites:**
- M1.G10.T8 completed

**Implementation Details:**
Execute the Git commands using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git add .
git commit -m "feat(m1): repository foundation & toolchain baseline"
git tag -a "m1-baseline" -m "Milestone 1 Foundation and Toolchain Verified"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$tag = git tag -l "m1-baseline"
if ($tag -eq "m1-baseline") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 11.12

---

### M1.G10.T10: Update State Tracker for Milestone 1 Completion

**Objective:** Record the completion of Milestone 1 in the orchestration state tracking file.

**Acceptance Criteria:**
- ✓ Directory `local-ai/program-states/` exists
- ✓ `progress-tracker.md` exists and marks Milestone 1 as `COMPLETED`
- ✓ Quality gate outcomes recorded (lint: PASS, typecheck: PASS, test: PASS, build: PASS)

**Prerequisites:**
- M1.G10.T9 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\local-ai\program-states\progress-tracker.md`

**Implementation Details:**
Create and populate the state tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "local-ai\program-states")) {
    New-Item -ItemType Directory -Path "local-ai\program-states" -Force | Out-Null
}

@'
# Orchestrator Progress Tracker

## Milestone Execution Status

| Milestone | Status | Gates Status | Baseline Tag | Completed Date |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Repository Foundation & Toolchain** | **COMPLETED** | PASS (Lint, Types, Tests, Build) | `m1-baseline` | 2026-10-20 |
| **M2: Content Architecture & Validation** | NOT STARTED | PENDING | — | — |
| **M3: Global Layout & Design System** | NOT STARTED | PENDING | — | — |
| **M4: Core Routes & Experiences** | NOT STARTED | PENDING | — | — |
| **M5: QA, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M6: Production Deployment** | NOT STARTED | PENDING | — | — |

## Milestone 1 Verification Log
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors)
- `npm run test`: PASS (all unit/smoke tests passed)
- `npm run build`: PASS (static export generated in `out/`)
- Git Baseline: `m1-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m1): record milestone 1 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "local-ai\program-states\progress-tracker.md") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.6, Req 11.12

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "README.md"
Test-Path "out\index.html"
Test-Path "local-ai\program-states\progress-tracker.md"
git tag -l "m1-baseline"
git status
```
Expected output:
- `True` for `README.md`, `out\index.html`, and `progress-tracker.md`
- Output includes `m1-baseline`
- `git status` reports working tree clean.

***

### Summary of Completed M1 Goals
All 10 Goal specification files for Milestone 1 are now generated:
- `goal1.md`: Next.js Project Initialization
- `goal2.md`: TypeScript Strict Configuration
- `goal3.md`: Tailwind CSS & Design Token Configuration
- `goal4.md`: ESLint & Code Quality Configuration
- `goal5.md`: Vitest & Testing Infrastructure
- `goal6.md`: Prettier & Code Formatting
- `goal7.md`: Git & Husky Pre-commit Hooks
- `goal8.md`: Path Aliases & Module Resolution
- `goal9.md`: Directory Structure & Source Layout
- `goal10.md`: Final Validation & Baseline Commit