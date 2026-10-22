# M5.G10: Final Verification Pipeline, Static-Output Check, and Scope Audit

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end quality pipeline and strict architectural scope audit to finalize Milestone 5. Verify that all four canonical project quality gates (`npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`) pass cleanly with exit code 0. Conduct an exhaustive build inspection to confirm that Next.js statically generates the root route (`/`) into `out/index.html` without dynamic SSR, proving that prerendered HTML contains the exact landmark and heading hierarchy (single `<h1>`, ordered `<h2>` sections), the M4 shell (`<header>`, `<footer>`, `<main>`), correct canonical and Open Graph metadata, and zero draft blog post content. Execute an architectural scope audit confirming zero contamination from downstream milestones (no projects/certifications/blog index or detail routes, no filters, no search, no resume download, no API routes, no server actions, no forms, no analytics, no cookies, and no barrel files). Verify via `git diff` that `package.json`, lockfiles, `tsconfig.json`, `next.config.ts`, `src/components/ui/`, `src/components/layout/`, `src/content/`, `tailwind.config.ts`, and `globals.css` remain untouched. Finalize `task-notes.md`, commit all assets, tag the tree with `m5-baseline`, and update `local-ai/program-states/progress-tracker.md` to seal Milestone 5.

## Goal Success Criteria

- ✓ `npm run lint` passes with 0 errors and 0 warnings
- ✓ `npm run typecheck` passes with zero type errors in strict mode
- ✓ `npm test` runs all unit, property, axe accessibility, and source-hygiene test suites with 100% pass rate
- ✓ `npm run build` runs content validation and produces static export in `out/` with exit code 0
- ✓ Inspection of prerendered `out/index.html` confirms single `<h1>`, section ordering, M4 header and footer, canonical `<link rel="canonical">`, Open Graph tags, and complete absence of draft post content
- ✓ Scope audit confirms zero new files in `src/app/` other than `page.tsx`
- ✓ Scope audit confirms zero files created for M6–M8 pages (`projects`, `certifications`, `blog` route directories)
- ✓ Scope audit confirms zero barrel files (`index.ts`) in `src/components/home/` or `src/lib/home/`
- ✓ `git diff` confirms zero changes to `tailwind.config.ts`, `src/app/globals.css`, `src/components/ui/`, `src/components/layout/`, `src/content/`, or CI files
- ✓ Task notes file `.kiro/specs/m5-homepage-experience/task-notes.md` finalized with all gate logs, sign-offs, and deferred verification notes
- ✓ Working tree committed, tagged with `m5-baseline`, and `local-ai/program-states/progress-tracker.md` updated

## Prerequisites

- Goals M5.G1 through M5.G9 completed
- All homepage components, helpers, and test suites operational
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M5.G10.T1: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Run ESLint across the repository to verify zero linting errors, no unsafe type assignments, and no accessibility issues in M5 components, helpers, and tests.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across all project files
- ✓ Reports 0 errors and 0 warnings
- ✓ Process exit code is 0

**Prerequisites:**
- M5.G9 completed

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

**Satisfies Requirements:** Req 16.7, Req 16.8

---

### M5.G10.T2: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Run TypeScript strict compiler check (`tsc --noEmit`) to confirm complete type safety across all homepage components, view models, metadata builders, and tests.

**Acceptance Criteria:**
- ✓ `npm run typecheck` runs without errors
- ✓ Process exit code is 0
- ✓ Confirms zero `any` or implicit `any` violations

**Prerequisites:**
- M5.G10.T1 completed

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

**Satisfies Requirements:** Req 16.7

---

### M5.G10.T3: Execute Full Test Suite Quality Gate (`npm test`)

**Objective:** Run Vitest across all unit, property, accessibility, and hygiene test suites.

**Acceptance Criteria:**
- ✓ `npm test` runs all test suites in the project (M1 through M5)
- ✓ All 14 property tests execute with $\ge 100$ iterations each
- ✓ All tests pass with zero failures
- ✓ Process exit code is 0

**Prerequisites:**
- M5.G10.T2 completed

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

**Satisfies Requirements:** Req 16.6, Req 16.7

---

### M5.G10.T4: Execute Production Build Quality Gate (`npm run build`)

**Objective:** Run `npm run build` to confirm `validate:content` triggers and passes, and Next.js produces static HTML output in `out/` with `/` listed as static (`○ (Static)`).

**Acceptance Criteria:**
- ✓ `validate:content` executes and validates all schemas
- ✓ Next.js static build succeeds with exit code 0
- ✓ Route `/` indicated as statically prerendered
- ✓ Output directory `out/` contains static `index.html` asset

**Prerequisites:**
- M5.G10.T3 completed

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

**Satisfies Requirements:** Req 1.2, Req 14.8

---

### M5.G10.T5: Inspect Prerendered Static Homepage Output (`out/index.html`)

**Objective:** Inspect the generated static HTML export of the homepage (`out/index.html`) to verify that the M4 shell, single `<h1>`, section ordering, metadata, and draft post exclusion are preserved in production markup.

**Acceptance Criteria:**
- ✓ File `out/index.html` exists
- ✓ Contains `<header>` and `<footer>` from M4 shell
- ✓ Contains single `<main id="main-content">`
- ✓ Contains exactly one `<h1>` displaying the owner name
- ✓ Sections appear in order: hero $\rightarrow$ featured-projects $\rightarrow$ skills $\rightarrow$ certifications $\rightarrow$ recent-activity
- ✓ Contains `<link rel="canonical" href="https://example.vercel.app/">`
- ✓ Contains Open Graph title, description, and url meta tags
- ✓ Contains ZERO occurrences of draft post titles (e.g. 'Draft Post — Secret Feature Preview')
- ✓ PowerShell inspection script exits with PASS

**Prerequisites:**
- M5.G10.T4 completed

**Implementation Details:**

Execute build output inspection using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$indexHtml = "out\index.html"
if (-not (Test-Path $indexHtml)) {
    Write-Error "Static index.html not found in out/ directory"
    exit 1
}

$content = Get-Content $indexHtml -Raw
$violations = @()

# 1. Shell landmarks
if (-not ($content -match '<header\b')) { $violations += "Header landmark missing in index.html" }
if (-not ($content -match '<footer\b')) { $violations += "Footer landmark missing in index.html" }
if (-not ($content -match '<main\b[^>]*\bid="main-content"')) { $violations += "Main landmark missing in index.html" }

# 2. Heading hierarchy
$h1Matches = [regex]::Matches($content, '<h1\b')
if ($h1Matches.Count -ne 1) { $violations += "Expected exactly 1 <h1> in index.html, found $($h1Matches.Count)" }

# 3. Canonical and Open Graph
if (-not ($content -match '<link[^>]*rel="canonical"[^>]*href="https://example\.vercel\.app/"')) {
    $violations += "Canonical link missing or inaccurate in index.html"
}
if (-not ($content -match '<meta[^>]*property="og:url"[^>]*content="https://example\.vercel\.app/"')) {
    $violations += "Open Graph url meta tag missing or inaccurate"
}

# 4. Draft exclusion check
if ($content.Contains("Draft Post — Secret Feature Preview")) {
    $violations += "CRITICAL: Draft blog post content leaked into static index.html!"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.7, Req 2.1, Req 11.9, Req 13.1, Req 13.3, Req 14.1

---

### M5.G10.T6: Audit Architectural Scope Boundaries (Zero M6–M10 Contamination)

**Objective:** Verify that M5 remained strictly within its homepage boundary: no new pages under `src/app/` (other than `page.tsx`), no projects/certifications/blog route directories, no API routes, no server actions, no forms, no analytics, and no premature feature code for M6–M10.

**Acceptance Criteria:**
- ✓ Confirms `src/app/` contains ONLY `layout.tsx`, `not-found.tsx`, `site-metadata.ts`, `page.tsx`, and `globals.css`
- ✓ Confirms zero directories created for `src/app/projects/`, `src/app/certifications/`, or `src/app/blog/`
- ✓ Confirms zero `route.ts` or `'use server'` files exist
- ✓ Confirms zero `index.ts` barrel files exist in `src/components/home/` or `src/lib/home/`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G10.T5 completed

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

# 2. Check home directories for barrel files
if (Test-Path "src\components\home\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/components/home (AGENTS.md 7.2)"
}
if (Test-Path "src\lib\home\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/lib/home (AGENTS.md 7.2)"
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

**Satisfies Requirements:** Req 16.1, Req 16.3, Req 16.4, Req 16.8

---

### M5.G10.T7: Verify Upstream Foundations and Config Invariance (`git diff`)

**Objective:** Execute `git diff` on `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, `globals.css`, `src/components/ui/`, `src/components/layout/`, and `src/content/` to confirm zero unintended modifications occurred during Milestone 5.

**Acceptance Criteria:**
- ✓ `git diff` on all upstream files produces zero lines
- ✓ Script returns PASS

**Prerequisites:**
- M5.G10.T6 completed

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/content/ package.json package-lock.json next.config.ts tsconfig.json
if ($diff.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Upstream protected files modified!`n$diff"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.2, Req 16.4, Req 16.5

---

### M5.G10.T8: Audit Test Matrix Coverage for M5

**Objective:** Verify that every homepage component, pure helper, formatter, and route has a matching test file in `tests/home/` and that all 14 properties have dedicated property tests.

**Acceptance Criteria:**
- ✓ `compare.test.ts` exists
- ✓ `format-date.test.ts` exists (Property 13)
- ✓ `select-featured-projects.test.ts` exists (Property 1)
- ✓ `select-certification-preview.test.ts` exists (Property 2)
- ✓ `select-recent-posts.test.ts` exists (Property 3)
- ✓ `selection-purity.test.ts` exists (Property 4)
- ✓ `derive-skill-groups.test.ts` exists (Properties 5, 6)
- ✓ `select-hero-action.test.ts` exists (Property 7)
- ✓ `hero-section.test.tsx` exists (Property 8)
- ✓ `section-visibility.test.ts` exists (Property 9 helper)
- ✓ `featured-projects.test.tsx` exists (Property 10)
- ✓ `certifications-preview.test.tsx` and `recent-activity.test.tsx` exist (Property 11)
- ✓ `home-content.test.tsx` exists (Properties 9 render, 12)
- ✓ `home-metadata.test.ts` exists (Property 14)
- ✓ `page.test.tsx`, `a11y.test.tsx`, `source-hygiene.test.ts` exist

**Prerequisites:**
- M5.G10.T7 completed

**Implementation Details:**

Execute test matrix check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$expectedTests = @(
    "tests\home\compare.test.ts",
    "tests\home\format-date.test.ts",
    "tests\home\select-featured-projects.test.ts",
    "tests\home\select-certification-preview.test.ts",
    "tests\home\select-recent-posts.test.ts",
    "tests\home\selection-purity.test.ts",
    "tests\home\derive-skill-groups.test.ts",
    "tests\home\select-hero-action.test.ts",
    "tests\home\hero-section.test.tsx",
    "tests\home\section-visibility.test.ts",
    "tests\home\featured-projects.test.tsx",
    "tests\home\certifications-preview.test.tsx",
    "tests\home\recent-activity.test.tsx",
    "tests\home\home-content.test.tsx",
    "tests\home\home-metadata.test.ts",
    "tests\home\page.test.tsx",
    "tests\home\a11y.test.tsx",
    "tests\home\source-hygiene.test.ts"
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

**Satisfies Requirements:** Req 16.6, Req 16.7

---

### M5.G10.T9: Finalize `task-notes.md` with Execution Sign-Off

**Objective:** Finalize `.kiro/specs/m5-homepage-experience/task-notes.md` with all completed verification logs, gate results, and deferred verification notes.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m5-homepage-experience/task-notes.md` updated
- ✓ Records status: PASS across Lint, Types, Tests, Build, Static Output, Axe, and Source Hygiene
- ✓ Documents deferred verification note: link destinations (`/projects/{slug}`, `/certifications`, `/blog`, `/blog/{slug}`) resolve once M6–M8 are completed
- ✓ Confirms baseline tag `m5-baseline` designation

**Prerequisites:**
- M5.G10.T8 completed

**Implementation Details:**

Append sign-off to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$signOff = @'

## 4. Milestone 5 Final Sign-Off & Gate Summary

- **Lint Gate (`npm run lint`):** PASS (0 errors, 0 warnings)
- **Typecheck Gate (`npm run typecheck`):** PASS (0 errors, strict mode enforced)
- **Test Gate (`npm test`):** PASS (All M1–M5 test suites passing, all 14 property tests verified >= 100 iterations)
- **Build Gate (`npm run build`):** PASS (Static HTML export generated into `out/` with `/` listed as static)
- **Static Output Inspection:** PASS (`out/index.html` verified static with single `<h1>`, canonical tag, Open Graph metadata, and zero draft leaks)
- **Axe WCAG 2.1 AA Gate:** PASS (0 violations across full homepage in populated and empty states)
- **Source Hygiene Scan:** PASS (0 raw hex, 0 arbitrary Tailwind, 0 extra client components, 0 scope leaks)
- **Scope Audit:** PASS (Zero barrel files, zero files >= 300 lines, zero M6–M10 contamination)
- **Root Config Diff:** PASS (`git diff` clean across all protected upstream files)
- **Deferred Verification Note:** Link destinations (`/projects/{slug}`, `/certifications`, `/blog/{slug}`) are verified structurally as correct `href` attributes; active resolution of destination routes will complete during M6, M7, and M8 implementations.

**Baseline Designation:** `m5-baseline`
'@

Add-Content -Path ".kiro\specs\m5-homepage-experience\task-notes.md" -Value $signOff -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m5-homepage-experience\task-notes.md" -Raw
if ($notes -match "Milestone 5 Final Sign-Off") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

### M5.G10.T10: Commit and Tag Milestone 5 Baseline (`m5-baseline`) & Update Progress Tracker

**Objective:** Commit all Milestone 5 components, helpers, route files, and test suites to Git, apply the tag `m5-baseline`, and record completion in `local-ai/program-states/progress-tracker.md`.

**Acceptance Criteria:**
- ✓ All M5 assets staged and committed with standardized commit message
- ✓ Git tag `m5-baseline` created on HEAD
- ✓ `local-ai/program-states/progress-tracker.md` updated marking Milestone 5 as `COMPLETED`
- ✓ Working tree is clean

**Prerequisites:**
- M5.G10.T1 through M5.G10.T9 completed

**Implementation Details:**

Commit, tag, and update progress tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

git add .
git commit -m "feat(m5): homepage experience, hero, featured projects, skills snapshot, preview sections, and seo metadata"
git tag -a "m5-baseline" -m "Milestone 5 Homepage Experience Verified"

@'
# Orchestrator Progress Tracker

## Milestone Execution Status

| Milestone | Status | Gates Status | Baseline Tag | Completed Date |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Repository Foundation & Toolchain** | **COMPLETED** | PASS (Lint, Types, Tests, Build) | `m1-baseline` | 2026-10-20 |
| **M2: Content Architecture & Validation** | **COMPLETED** | PASS (Lint, Types, Tests >80%, Build) | `m2-baseline` | 2026-10-20 |
| **M3: Global Layout & Design System** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Axe) | `m3-baseline` | 2026-10-22 |
| **M4: Global Layout & Navigation** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Static Inspection, Axe) | `m4-baseline` | 2026-10-22 |
| **M5: Homepage Experience** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Static Output Inspection, Axe) | `m5-baseline` | 2026-10-23 |
| **M6: Projects Index & Case Studies** | NOT STARTED | PENDING | — | — |
| **M7: Certifications & Badges** | NOT STARTED | PENDING | — | — |
| **M8: Blog & Community Participation** | NOT STARTED | PENDING | — | — |
| **M9: Quality, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M10: Production Deployment & Launch** | NOT STARTED | PENDING | — | — |

## Milestone 5 Verification Log
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors, strict mode verified)
- `npm test`: PASS (All unit, property, axe, and hygiene test suites green)
- `npm run build`: PASS (static HTML export generated into `out/` with `/` static)
- Static Output Inspection: PASS (`out/index.html` verified static with single `<h1>`, canonical URL, Open Graph metadata, and zero draft leaks)
- Git Baseline: `m5-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m5): record milestone 5 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$tag = git tag -l "m5-baseline"
$status = git status --porcelain
if ($tag -eq "m5-baseline" -and $status.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git tag -l "m5-baseline"
git status
npm run lint
npm run typecheck
npm test
npm run build
```
Expected output:
- Git tag lists `m5-baseline`
- Working tree is clean
- All four verification commands exit with return code 0.

***

### Summary of Completed M5 Goals
All 10 Goal specification files for Milestone 5 (`m5-homepage-experience`) are now generated and fully detailed:
- `goal1.md`: Fixtures, Fixed UI Strings, Comparator, Date Formatter, and Gap Log
- `goal2.md`: Selection Helpers and Property Tests
- `goal3.md`: Skill Derivation, Hero Contact Action, and Property Tests
- `goal4.md`: View Model, Section Visibility, and Homepage Metadata
- `goal5.md`: HeroSection
- `goal6.md`: FeaturedProjects and SkillsSnapshot
- `goal7.md`: CertificationsPreview and RecentActivity
- `goal8.md`: HomeContent, Route, and Heading/Landmark Structure
- `goal9.md`: Responsive, Token, and Scope Compliance; Accessibility Matrix; Source Hygiene
- `goal10.md`: Final Verification Pipeline, Static-Output Check, and Scope Audit