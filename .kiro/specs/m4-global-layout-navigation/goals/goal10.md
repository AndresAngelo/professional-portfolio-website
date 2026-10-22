# M4.G10: Final Verification Pipeline, Scope Audit, and Static-Output Check

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end quality pipeline and strict architectural scope audit to finalize Milestone 4. Verify that all four canonical project quality gates (`npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`) pass cleanly with exit code 0. Conduct an exhaustive build inspection to confirm that Next.js statically generates the layout shell routes and the `/_not-found` page without falling back to dynamic SSR, proving that prerendered `/_not-found` HTML contains the full navigation structure with zero entries marked `aria-current`. Execute an architectural scope audit confirming zero contamination from downstream milestones (no homepage content, no projects/certifications/blog routes, no API routes or server actions, no forms, no analytics, no cookies, and no barrel files). Verify via `git diff` that `package.json`, lockfiles, `tsconfig.json`, `next.config.ts`, `src/components/ui/`, `tailwind.config.ts`, and `globals.css` remain untouched (aside from pre-approved dev-dependencies). Finalize `task-notes.md`, commit all assets, tag the tree with `m4-baseline`, and update `local-ai/program-states/progress-tracker.md` to seal Milestone 4.

## Goal Success Criteria

- ✓ `npm run lint` passes with 0 errors and 0 warnings
- ✓ `npm run typecheck` passes with zero type errors in strict mode
- ✓ `npm test` runs all unit, property, axe accessibility, and source-hygiene test suites with 100% pass rate
- ✓ `npm run build` runs content validation and produces static export in `out/` with exit code 0
- ✓ Inspection of prerendered `out/404.html` (or `out/_not-found.html`) confirms navigation links exist and zero links carry `aria-current="page"`
- ✓ Scope audit confirms zero new files in `src/app/` other than `layout.tsx`, `not-found.tsx`, and `site-metadata.ts`
- ✓ Scope audit confirms zero files created for M5–M8 pages (`projects`, `certifications`, `blog`, homepage content)
- ✓ Scope audit confirms zero barrel files (`index.ts`) in `src/components/layout/`
- ✓ `git diff` confirms zero changes to `tailwind.config.ts`, `src/app/globals.css`, `src/components/ui/`, or CI files
- ✓ Task notes file `.kiro/specs/m4-global-layout-navigation/task-notes.md` finalized with all gate logs, sign-offs, and deferred verification notes
- ✓ Working tree committed, tagged with `m4-baseline`, and `local-ai/program-states/progress-tracker.md` updated

## Prerequisites

- Goals M4.G1 through M4.G9 completed
- All layout components, app shell files, and test suites functional
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M4.G10.T1: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Run ESLint across the repository to verify zero linting errors, no unsafe type assignments, and no accessibility issues in M4 components, app files, and tests.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across all project files
- ✓ Reports 0 errors and 0 warnings
- ✓ Process exit code is 0

**Prerequisites:**
- M4.G9 completed

**Implementation Details:**

Run linting via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.6, Req 14.7, Req 15.8, Req 16.1

---

### M4.G10.T2: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Run TypeScript strict compiler check (`tsc --noEmit`) to confirm complete type safety across all layout components, metadata generators, app shell files, and tests.

**Acceptance Criteria:**
- ✓ `npm run typecheck` runs without errors
- ✓ Process exit code is 0
- ✓ Confirms zero `any` or implicit `any` violations

**Prerequisites:**
- M4.G10.T1 completed

**Implementation Details:**

Run type checking via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.6, Req 15.8, Req 16.1

---

### M4.G10.T3: Execute Full Test Suite Quality Gate (`npm test`)

**Objective:** Run Vitest across all unit, property, accessibility, and hygiene test suites.

**Acceptance Criteria:**
- ✓ `npm test` runs all test suites in the project (M1 through M4)
- ✓ All tests pass with zero failures
- ✓ Process exit code is 0

**Prerequisites:**
- M4.G10.T2 completed

**Implementation Details:**

Run test suite via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.8

---

### M4.G10.T4: Execute Production Build Quality Gate (`npm run build`)

**Objective:** Run `npm run build` to confirm `validate:content` triggers and passes, and Next.js produces static HTML output in `out/` with zero dynamic runtime dependencies.

**Acceptance Criteria:**
- ✓ `validate:content` executes and validates all schemas
- ✓ Next.js static build succeeds with exit code 0
- ✓ Build output indicates static route generation (`○ (Static)`)
- ✓ Output directory `out/` contains static HTML assets

**Prerequisites:**
- M4.G10.T3 completed

**Implementation Details:**

Run production build via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
if ($LASTEXITCODE -eq 0 -and (Test-Path "out\index.html")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.8, Req 15.8

---

### M4.G10.T5: Inspect Prerendered Static Not-Found Output (`out/404.html`)

**Objective:** Inspect the generated static HTML export of the not-found boundary (`out/404.html` or `out/_not-found.html`) to verify that navigation is present and no link is mistakenly marked current.

**Acceptance Criteria:**
- ✓ Static file `out/404.html` or `out/_not-found.html` exists
- ✓ Contains `<header>` and `<footer>` markup
- ✓ Contains navigation links (`Projects`, `Certifications`, `Blog`)
- ✓ Contains zero occurrences of `aria-current="page"`
- ✓ PowerShell inspection script exits with PASS

**Prerequisites:**
- M4.G10.T4 completed

**Implementation Details:**

Execute build output inspection using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$targetHtml = "out\404.html"
if (-not (Test-Path $targetHtml)) {
    $targetHtml = "out\_not-found.html"
}

if (-not (Test-Path $targetHtml)) {
    Write-Error "Static 404 HTML not found in out/ directory"
    exit 1
}

$content = Get-Content $targetHtml -Raw
$violations = @()

if (-not ($content -match '<header\b')) {
    $violations += "Header landmark missing in static 404 output"
}
if (-not ($content -match '<footer\b')) {
    $violations += "Footer landmark missing in static 404 output"
}
if (-not ($content -match 'Projects')) {
    $violations += "Navigation links missing in static 404 output"
}
if ($content -match 'aria-current="page"') {
    $violations += "Forbidden aria-current='page' found in static 404 output (no route should be marked active on 404)"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.5, Req 14.8

---

### M4.G10.T6: Audit Architectural Scope Boundaries (Zero M5–M8 Contamination)

**Objective:** Verify that M4 remained strictly within its layout boundary: no new pages under `src/app/` (other than `layout.tsx`, `not-found.tsx`, `site-metadata.ts`), no API routes, no server actions, no forms, no analytics, and no premature feature code for M5–M8.

**Acceptance Criteria:**
- ✓ Confirms `src/app/` contains ONLY `layout.tsx`, `not-found.tsx`, `site-metadata.ts`, `page.tsx` (M1 stub), and `globals.css`
- ✓ Confirms zero directories created for `src/app/projects/`, `src/app/certifications/`, or `src/app/blog/`
- ✓ Confirms zero `route.ts` or `'use server'` files exist
- ✓ Confirms zero `index.ts` barrel files exist in `src/components/layout/`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G10.T5 completed

**Implementation Details:**

Execute scope boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$violations = @()

# 1. Check premature route directories
$forbiddenDirs = @(
    "src\app\projects",
    "src\app\certifications",
    "src\app\blog"
)
foreach ($d in $forbiddenDirs) {
    if (Test-Path $d) {
        $violations += "Premature milestone route directory found: $d (reserved for M6-M8)"
    }
}

# 2. Check layout directory for barrel files
if (Test-Path "src\components\layout\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/components/layout (AGENTS.md 7.2)"
}

# 3. Check for API routes or server actions
$srcFiles = Get-ChildItem -Path "src" -Include *.ts, *.tsx -Recurse
foreach ($f in $srcFiles) {
    if ($f.Name -eq "route.ts") {
        $violations += "Forbidden API route file found: $($f.FullName)"
    }
    $content = Get-Content $f.FullName -Raw
    if ($content -match "['""]use server['""]") {
        $violations += "Forbidden 'use server' action found in $($f.FullName)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.5, Req 14.7

---

### M4.G10.T7: Verify Root Styling and Primitives Invariance (`git diff`)

**Objective:** Execute `git diff` on `tailwind.config.ts`, `globals.css`, and `src/components/ui/` to confirm zero unintended modifications occurred during Milestone 4.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts` produces zero lines
- ✓ `git diff src/app/globals.css` produces zero lines
- ✓ `git diff src/components/ui/` produces zero lines
- ✓ Script returns PASS

**Prerequisites:**
- M4.G10.T6 completed

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diffTailwind = git diff tailwind.config.ts
$diffCss = git diff src/app/globals.css
$diffUi = git diff src/components/ui/

if ($diffTailwind.Length -eq 0 -and $diffCss.Length -eq 0 -and $diffUi.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Protected files modified!`n$diffTailwind`n$diffCss`n$diffUi"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.6, Req 13.7, Req 14.4

---

### M4.G10.T8: Audit Test Matrix Coverage for M4

**Objective:** Verify that every layout component, pure module, and app shell file has a matching, dedicated test file in `tests/`.

**Acceptance Criteria:**
- ✓ `current-route.test.ts` exists
- ✓ `nav-entries.test.ts` exists
- ✓ `disclosure.test.ts` exists
- ✓ `contact-channels.test.ts` exists
- ✓ `mobile-nav-toggle.test.tsx` exists
- ✓ `primary-nav.test.tsx` exists
- ✓ `skip-link.test.tsx` exists
- ✓ `site-header.test.tsx` exists
- ✓ `contact-links.test.tsx` exists
- ✓ `site-footer.test.tsx` exists
- ✓ `site-metadata.test.ts` exists
- ✓ `layout.test.tsx` exists
- ✓ `not-found.test.tsx` exists
- ✓ `compliance.test.ts`, `a11y.test.tsx`, `source-hygiene.test.ts` exist

**Prerequisites:**
- M4.G10.T7 completed

**Implementation Details:**

Execute test matrix check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$expectedTests = @(
    "tests\unit\components\layout\current-route.test.ts",
    "tests\unit\components\layout\nav-entries.test.ts",
    "tests\unit\components\layout\disclosure.test.ts",
    "tests\unit\components\layout\contact-channels.test.ts",
    "tests\unit\components\layout\mobile-nav-toggle.test.tsx",
    "tests\unit\components\layout\primary-nav.test.tsx",
    "tests\unit\components\layout\skip-link.test.tsx",
    "tests\unit\components\layout\site-header.test.tsx",
    "tests\unit\components\layout\contact-links.test.tsx",
    "tests\unit\components\layout\site-footer.test.tsx",
    "tests\unit\app\site-metadata.test.ts",
    "tests\unit\app\layout.test.tsx",
    "tests\unit\app\not-found.test.tsx",
    "tests\unit\components\layout\compliance.test.ts",
    "tests\unit\components\layout\a11y.test.tsx",
    "tests\unit\components\layout\source-hygiene.test.ts"
)

$missing = @()
foreach ($t in $expectedTests) {
    if (-not (Test-Path $t)) {
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

**Satisfies Requirements:** Req 15.1, Req 15.8

---

### M4.G10.T9: Finalize `task-notes.md` with Execution Sign-Off

**Objective:** Finalize `.kiro/specs/m4-global-layout-navigation/task-notes.md` with all completed verification logs, gate results, and deferred verification notes.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m4-global-layout-navigation/task-notes.md` updated
- ✓ Records status: PASS across Lint, Types, Tests, Build, Static Output, Axe, and Source Hygiene
- ✓ Documents deferred verification note: slug `notFound()` integration will be verified in M6–M8
- ✓ Confirms baseline tag `m4-baseline` designation

**Prerequisites:**
- M4.G10.T8 completed

**Implementation Details:**

Append sign-off to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$signOff = @'

## 5. Milestone 4 Final Sign-Off & Gate Summary

- **Lint Gate (`npm run lint`):** PASS (0 errors, 0 warnings)
- **Typecheck Gate (`npm run typecheck`):** PASS (0 errors, strict mode enforced)
- **Test Gate (`npm test`):** PASS (All M1–M4 test suites passing with 100% assertions)
- **Build Gate (`npm run build`):** PASS (Static HTML export generated in `out/`)
- **Static Output Inspection:** PASS (`out/404.html` contains navigation structure with zero `aria-current="page"`)
- **Axe WCAG 2.1 AA Gate:** PASS (0 violations across header, expanded nav, footer, and not-found inside shell)
- **Source Hygiene Scan:** PASS (0 raw hex, 0 arbitrary Tailwind, 0 extra client components, 0 scope leaks)
- **Scope Audit:** PASS (Zero barrel files, zero files >= 300 lines, zero M5–M8 contamination)
- **Root Config Diff:** PASS (`git diff` on `tailwind.config.ts`, `globals.css`, `src/components/ui/` clean)
- **Deferred Verification Note:** Requirement 11.5 (`notFound()` triggered by invalid project/blog slugs) is verified structurally via unit test and will receive end-to-end route verification once dynamic slug routes are implemented in M6 and M8.

**Baseline Designation:** `m4-baseline`
'@

Add-Content -Path ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Value $signOff -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Raw
if ($notes -match "Milestone 4 Final Sign-Off") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.5, Req 15.8

---

### M4.G10.T10: Commit and Tag Milestone 4 Baseline (`m4-baseline`) & Update Progress Tracker

**Objective:** Commit all Milestone 4 layout components, app shell files, and test suites to Git, apply the tag `m4-baseline`, and record completion in `local-ai/program-states/progress-tracker.md`.

**Acceptance Criteria:**
- ✓ All M4 assets staged and committed with standardized commit message
- ✓ Git tag `m4-baseline` created on HEAD
- ✓ `local-ai/program-states/progress-tracker.md` updated marking Milestone 4 as `COMPLETED`
- ✓ Working tree is clean

**Prerequisites:**
- M4.G10.T1 through M4.G10.T9 completed

**Implementation Details:**

Commit, tag, and update progress tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

git add .
git commit -m "feat(m4): global layout shell, navigation, header, footer, not-found, and a11y matrix"
git tag -a "m4-baseline" -m "Milestone 4 Global Layout and Navigation Verified"

@'
# Orchestrator Progress Tracker

## Milestone Execution Status

| Milestone | Status | Gates Status | Baseline Tag | Completed Date |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Repository Foundation & Toolchain** | **COMPLETED** | PASS (Lint, Types, Tests, Build) | `m1-baseline` | 2026-10-20 |
| **M2: Content Architecture & Validation** | **COMPLETED** | PASS (Lint, Types, Tests >80%, Build) | `m2-baseline` | 2026-10-20 |
| **M3: Global Layout & Design System** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Axe) | `m3-baseline` | 2026-10-22 |
| **M4: Global Layout & Navigation** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Static Inspection, Axe) | `m4-baseline` | 2026-10-22 |
| **M5: Homepage Experience** | NOT STARTED | PENDING | — | — |
| **M6: Projects Index & Case Studies** | NOT STARTED | PENDING | — | — |
| **M7: Certifications & Badges** | NOT STARTED | PENDING | — | — |
| **M8: Blog & Community Participation** | NOT STARTED | PENDING | — | — |
| **M9: Quality, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M10: Production Deployment & Launch** | NOT STARTED | PENDING | — | — |

## Milestone 4 Verification Log
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors, strict mode verified)
- `npm test`: PASS (All unit, property, axe, and hygiene test suites green)
- `npm run build`: PASS (static HTML export generated into `out/`)
- Static 404 Inspection: PASS (`out/404.html` verified static with zero active current cues)
- Git Baseline: `m4-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m4): record milestone 4 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$tag = git tag -l "m4-baseline"
$status = git status --porcelain
if ($tag -eq "m4-baseline" -and $status.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git tag -l "m4-baseline"
git status
npm run lint
npm run typecheck
npm test
npm run build
```
Expected output:
- Git tag lists `m4-baseline`
- Working tree is clean
- All four verification commands exit with return code 0.

***

### Summary of Completed M4 Goals
All 10 Goal specification files for Milestone 4 (`m4-global-layout-navigation`) are now generated and fully detailed:
- `goal1.md`: Fixtures, Fixed UI Strings, Dependency Approval, and Gap Log
- `goal2.md`: Pure Logic Modules and Property Tests
- `goal3.md`: MobileNavToggle Client Island and PrimaryNav
- `goal4.md`: SkipLink and SiteHeader
- `goal5.md`: ContactLinks and SiteFooter
- `goal6.md`: Site Metadata and Root Layout
- `goal7.md`: Global Not-Found Page
- `goal8.md`: Responsive Verification and Token/Scope Compliance
- `goal9.md`: Accessibility Matrix, Keyboard Tests, and Source-Hygiene Scan
- `goal10.md`: Final Verification Pipeline, Scope Audit, and Static-Output Check