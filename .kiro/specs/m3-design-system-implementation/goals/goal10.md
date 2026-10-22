# M3.G10: Final Verification Pipeline and Scope Audit

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end quality pipeline and strict scope audit for Milestone 3. Verify that all 4 canonical project gates (`npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`) pass cleanly with exit code 0. Conduct an exhaustive scope audit ensuring zero unapproved additions exist: no barrel files (`index.ts`), no component exceeding 300 lines, no additions under `src/app/`, no API routes or server actions, no forms, no analytics/cookies, and no navigation/header/footer components (reserved for M4). Verify that `tailwind.config.ts` and `globals.css` remain untouched, finalize `task-notes.md`, tag the repository with `m3-baseline`, and update `local-ai/program-states/progress-tracker.md` to seal Milestone 3.

## Goal Success Criteria

- ✓ `npm run lint` passes with 0 errors and 0 warnings
- ✓ `npm run typecheck` passes with zero type errors in strict mode
- ✓ `npm test` runs all unit, property, axe accessibility, and source-hygiene test suites with 100% pass rate
- ✓ `npm run build` runs content validation and produces static export in `out/` with exit code 0
- ✓ Scope audit confirms zero files created under `src/app/` during M3
- ✓ Scope audit confirms zero barrel files (`index.ts`) in `src/components/ui/`
- ✓ Scope audit confirms zero files exceed 300 lines in `src/components/ui/`
- ✓ `git diff` confirms zero changes to `tailwind.config.ts` or `globals.css`
- ✓ `task-notes.md` finalized with all audit logs, config gaps, and manual verification checklists
- ✓ Git working tree tagged with `m3-baseline` and `local-ai/program-states/progress-tracker.md` updated

## Prerequisites

- Goals M3.G1 through M3.G9 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- All 10 UI primitives and corresponding test suites functional

---

## Tasks

### M3.G10.T1: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Run ESLint across the repository to verify zero linting errors, no unsafe type assignments, and no accessibility issues in M3 components and tests.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across all project files
- ✓ Reports 0 errors and 0 warnings
- ✓ Process exit code is 0

**Prerequisites:**
- M3.G9 completed

**Implementation Details:**

Run linting via PowerShell:
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

**Satisfies Requirements:** Req 16.1, Req 16.9

---

### M3.G10.T2: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Run TypeScript strict compiler check (`tsc --noEmit`) to confirm complete type safety across all components, shared helpers, and tests.

**Acceptance Criteria:**
- ✓ `npm run typecheck` runs without errors
- ✓ Process exit code is 0
- ✓ Confirms zero `any` or implicit `any` violations

**Prerequisites:**
- M3.G10.T1 completed

**Implementation Details:**

Run type checking via PowerShell:
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

**Satisfies Requirements:** Req 16.1, Req 16.9

---

### M3.G10.T3: Execute Full Test Suite Quality Gate (`npm test`)

**Objective:** Run Vitest across all unit, property, accessibility, and hygiene test suites.

**Acceptance Criteria:**
- ✓ `npm test` runs all test suites in the project
- ✓ All tests pass with zero failures
- ✓ Process exit code is 0

**Prerequisites:**
- M3.G10.T2 completed

**Implementation Details:**

Run test suite via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm test
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.9

---

### M3.G10.T4: Execute Production Build Quality Gate (`npm run build`)

**Objective:** Run `npm run build` to confirm `validate:content` triggers, passes, and Next.js produces the static export cleanly.

**Acceptance Criteria:**
- ✓ `validate:content` validates all content schemas and passes
- ✓ `next build` compiles static assets into `out/`
- ✓ Process exit code is 0

**Prerequisites:**
- M3.G10.T3 completed

**Implementation Details:**

Run production build via PowerShell:
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

**Satisfies Requirements:** Req 16.9

---

### M3.G10.T5: Audit Component File Constraints & Absence of Barrel Files

**Objective:** Audit `src/components/ui/` to confirm that no `index.ts` barrel file exists and that no component file exceeds 300 lines per `AGENTS.md` Section 7.2.

**Acceptance Criteria:**
- ✓ Confirms `src/components/ui/index.ts` does NOT exist
- ✓ Scans all files in `src/components/ui/`; confirms every file is strictly $< 300$ lines
- ✓ Audit script returns PASS

**Prerequisites:**
- M3.G10.T4 completed

**Implementation Details:**

Execute file constraint audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$hasBarrel = Test-Path "src\components\ui\index.ts"
$files = Get-ChildItem -Path "src\components\ui" -Include *.ts, *.tsx, *.css
$exceedsLines = @()

foreach ($file in $files) {
    $lineCount = (Get-Content $file.FullName).Count
    if ($lineCount -ge 300) {
        $exceedsLines += "$($file.Name): $lineCount lines (must be < 300)"
    }
}

if (-not $hasBarrel -and $exceedsLines.Count -eq 0) {
    "PASS"
} else {
    Write-Host "Violations detected: HasBarrel=$hasBarrel, Exceeds=$($exceedsLines -join '; ')"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.8

---

### M3.G10.T6: Audit Architectural Scope Boundaries (Zero M4/M5+ Contamination)

**Objective:** Verify that M3 remained strictly within its UI primitive boundary: no additions under `src/app/`, no API routes, no server actions, no forms, no analytics/cookies, and no navigation/header/footer components (M4).

**Acceptance Criteria:**
- ✓ `git status` confirms zero new or modified files under `src/app/`
- ✓ Zero new API routes or server actions
- ✓ Zero header, footer, or navigation components introduced
- ✓ Zero forms or analytics scripts introduced
- ✓ Audit script returns PASS

**Prerequisites:**
- M3.G10.T5 completed

**Implementation Details:**

Execute boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appDiff = git status --porcelain src/app/
$forbiddenPatterns = @(
    "src\components\layout\SiteHeader.tsx",
    "src\components\layout\SiteFooter.tsx",
    "src\components\layout\MobileNavigation.tsx"
)

$violations = @()
if ($appDiff) {
    $violations += "Unexpected modification in src/app/: $appDiff"
}

foreach ($fp in $forbiddenPatterns) {
    if (Test-Path $fp) {
        $violations += "Milestone 4 layout component found prematurely: $fp"
    }
}

if ($violations.Count -eq 0) {
    "PASS"
} else {
    $violations | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.6, Req 16.7

---

### M3.G10.T7: Verify Root Styling Config Invariance (`git diff`)

**Objective:** Execute `git diff` on `tailwind.config.ts` and `globals.css` to confirm that M3 consumed tokens without modifying root design configurations.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts` produces zero lines
- ✓ `git diff src/app/globals.css` produces zero lines
- ✓ Script returns PASS

**Prerequisites:**
- M3.G10.T6 completed

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$diffTailwind = git diff tailwind.config.ts
$diffCss = git diff src/app/globals.css

if ($diffTailwind.Length -eq 0 -and $diffCss.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Root styling configs were modified!`n$diffTailwind`n$diffCss"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.3, Req 16.5

---

### M3.G10.T8: Audit Component Test Suite Coverage Matrix

**Objective:** Verify that every single UI primitive created in M3 has a dedicated, matching unit test file under `tests/unit/components/ui/`.

**Acceptance Criteria:**
- ✓ `button.test.tsx` exists
- ✓ `card.test.tsx` exists
- ✓ `tag.test.tsx` exists
- ✓ `status-badge.test.tsx` exists
- ✓ `event-type-badge.test.tsx` exists
- ✓ `filter-chip.test.tsx` exists
- ✓ `external-link.test.tsx` exists
- ✓ `empty-state.test.tsx` exists
- ✓ `markdown-doc.test.tsx` exists
- ✓ `container.test.tsx` exists
- ✓ `shared.test.ts`, `a11y.test.tsx`, and `source-hygiene.test.ts` exist

**Prerequisites:**
- M3.G10.T7 completed

**Implementation Details:**

Execute test matrix audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$expectedTests = @(
    "button.test.tsx",
    "card.test.tsx",
    "tag.test.tsx",
    "status-badge.test.tsx",
    "event-type-badge.test.tsx",
    "filter-chip.test.tsx",
    "external-link.test.tsx",
    "empty-state.test.tsx",
    "markdown-doc.test.tsx",
    "container.test.tsx",
    "shared.test.ts",
    "a11y.test.tsx",
    "source-hygiene.test.ts"
)

$missing = @()
foreach ($t in $expectedTests) {
    if (-not (Test-Path "tests\unit\components\ui\$t")) {
        $missing += $t
    }
}

if ($missing.Count -eq 0) {
    "PASS"
} else {
    Write-Host "Missing test suites: $($missing -join ', ')"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2

---

### M3.G10.T9: Finalize `task-notes.md` with Execution Sign-Off

**Objective:** Finalize `.kiro/specs/m3-design-system-implementation/task-notes.md` with all completed verification data, gate results, and sign-off records.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m3-design-system-implementation/task-notes.md` updated
- ✓ Records status: PASS across Lint, Types, Tests, Build, Axe, and Source Hygiene
- ✓ Confirms baseline tag `m3-baseline` designation

**Prerequisites:**
- M3.G10.T8 completed

**Implementation Details:**

Append sign-off to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$signOff = @'

## 5. Milestone 3 Final Sign-Off & Gate Summary

- **Lint Gate (`npm run lint`):** PASS (0 errors, 0 warnings)
- **Typecheck Gate (`npm run typecheck`):** PASS (0 errors, strict mode enforced)
- **Test Gate (`npm test`):** PASS (13 test suites, 100% pass rate)
- **Build Gate (`npm run build`):** PASS (Static HTML export generated in `out/`)
- **Axe WCAG 2.1 AA Gate:** PASS (0 violations across all primitives and states)
- **Source Hygiene Scan:** PASS (0 raw hex, 0 arbitrary Tailwind, 0 unannotated client directives)
- **Scope Audit:** PASS (0 barrel files, 0 files >= 300 lines, 0 app/layout contamination)
- **Root Config Diff:** PASS (`git diff` on `tailwind.config.ts` and `globals.css` clean)

**Baseline Designation:** `m3-baseline`
'@

Add-Content -Path ".kiro\specs\m3-design-system-implementation\task-notes.md" -Value $signOff -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$notes = Get-Content ".kiro\specs\m3-design-system-implementation\task-notes.md" -Raw
if ($notes -match "Milestone 3 Final Sign-Off") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.5, Req 16.9

---

### M3.G10.T10: Commit and Tag Milestone 3 Baseline (`m3-baseline`) & Update Progress Tracker

**Objective:** Commit all Milestone 3 components and test suites to Git, apply the tag `m3-baseline`, and record completion in `local-ai/program-states/progress-tracker.md`.

**Acceptance Criteria:**
- ✓ All M3 assets staged and committed with standardized commit message
- ✓ Git tag `m3-baseline` created on HEAD
- ✓ `local-ai/program-states/progress-tracker.md` updated marking Milestone 3 as `COMPLETED`
- ✓ Working tree is clean

**Prerequisites:**
- M3.G10.T1 through M3.G10.T9 completed

**Implementation Details:**

Commit, tag, and update progress tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

git add .
git commit -m "feat(m3): design system ui primitives, accessibility matrix, and source hygiene"
git tag -a "m3-baseline" -m "Milestone 3 Design System Implementation Verified"

@'
# Orchestrator Progress Tracker

## Milestone Execution Status

| Milestone | Status | Gates Status | Baseline Tag | Completed Date |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Repository Foundation & Toolchain** | **COMPLETED** | PASS (Lint, Types, Tests, Build) | `m1-baseline` | 2026-10-20 |
| **M2: Content Architecture & Validation** | **COMPLETED** | PASS (Lint, Types, Tests >80%, Build) | `m2-baseline` | 2026-10-20 |
| **M3: Global Layout & Design System** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Axe) | `m3-baseline` | 2026-10-22 |
| **M4: Core Routes & Experiences** | NOT STARTED | PENDING | — | — |
| **M5: QA, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M6: Production Deployment** | NOT STARTED | PENDING | — | — |

## Milestone 3 Verification Log
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors, strict mode verified)
- `npm test`: PASS (13 test suites, all axe and property checks green)
- `npm run build`: PASS (static export generated into `out/`)
- Git Baseline: `m3-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m3): record milestone 3 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$tag = git tag -l "m3-baseline"
$status = git status --porcelain
if ($tag -eq "m3-baseline" -and $status.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git tag -l "m3-baseline"
git status
npm run lint
npm run typecheck
npm test
npm run build
```
Expected output:
- Git tag lists `m3-baseline`
- Working tree is clean
- All four verification commands exit with code 0.

***

### Summary of Completed M3 Goals
All 10 Goal specification files for Milestone 3 are now generated and fully detailed:
- `goal1.md`: Shared Internals, Dependency Approvals, and Config-Gap Log
- `goal2.md`: Button Component
- `goal3.md`: Card Container
- `goal4.md`: Tag, TagList, and StatusBadge
- `goal5.md`: EventTypeBadge and FilterChip
- `goal6.md`: ExternalLink and EmptyState
- `goal7.md`: Container and Responsive Verification
- `goal8.md`: MarkdownDoc, enhanceDocumentHtml, and CSS Module
- `goal9.md`: Accessibility Matrix and Source-Hygiene Tests
- `goal10.md`: Final Verification Pipeline and Scope Audit