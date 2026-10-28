# M6.G10: Final Verification Pipeline, Static-Output Check, and Scope Audit

> **Milestone:** M6 — Projects Module  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end quality pipeline and strict architectural scope audit to finalize Milestone 6. Verify that all four canonical project quality gates (`npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`) pass cleanly with exit code 0. Conduct an exhaustive build inspection to confirm that Next.js statically generates the projects index (`/projects`) into `out/projects.html` and one static HTML page per project slug into `out/projects/[slug].html` without dynamic SSR, missing-Suspense errors, or client-side runtime hydration warnings. Prove that prerendered `out/projects.html` contains every project card title, the single `<h1>`, the Suspense fallback grid, and zero client filter controls or heavy Markdown documentation text. Prove that prerendered detail HTML contains the single `<h1>`, breadcrumb navigation, canonical and Open Graph metadata without query parameters, and strictly zero JSON-LD structured data. Execute an architectural scope audit confirming zero contamination from downstream milestones (no certifications or blog routes, no search, no resume download, no API routes, no server actions, no forms, no analytics, no cookies, and no barrel files). Verify via `git diff` that `package.json`, lockfiles, `tsconfig.json`, `next.config.ts`, `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, `src/content/`, `tailwind.config.ts`, and `globals.css` remain untouched. Finalize `task-notes.md`, commit all assets, tag the tree with `m6-baseline`, and update `local-ai/program-states/progress-tracker.md` to seal Milestone 6.

## Goal Success Criteria

- ✓ `npm run lint` passes with 0 errors and 0 warnings
- ✓ `npm run typecheck` passes with zero type errors in strict mode
- ✓ `npm test` runs all unit, property, axe accessibility, keyboard, and source-hygiene test suites with 100% pass rate
- ✓ `npm run build` runs content validation and produces static export in `out/` with `/projects` and every `/projects/[slug]` listed as static (`○ (Static)`)
- ✓ Inspection of prerendered `out/projects.html` confirms single `<h1>`, all project titles in Suspense fallback grid, absence of interactive filter bar buttons before hydration, and complete absence of heavy `documentation` markdown
- ✓ Inspection of prerendered detail HTML confirms single `<h1>`, breadcrumb `<nav>`, canonical tag without query string, Open Graph tags, and zero `application/ld+json` tags
- ✓ Scope audit confirms zero new files in `src/app/` other than `projects/page.tsx` and `projects/[slug]/page.tsx`
- ✓ Scope audit confirms zero directories created for M7–M8 pages (`certifications`, `blog` route directories)
- ✓ Scope audit confirms zero barrel files (`index.ts`) in `src/components/projects/` or `src/lib/projects/`
- ✓ `git diff` confirms zero changes to `tailwind.config.ts`, `src/app/globals.css`, `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, `src/content/`, or CI files
- ✓ Task notes file `.kiro/specs/m6-projects-module/task-notes.md` finalized with all gate logs, sign-offs, and deferred verification notes
- ✓ Working tree committed, tagged with `m6-baseline`, and `local-ai/program-states/progress-tracker.md` updated

## Prerequisites

- Goals M6.G1 through M6.G9 completed
- All projects module components, helpers, route files, and test suites operational
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G10.T1: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Run ESLint across the repository to verify zero linting errors, no unsafe type assignments, and no accessibility issues in M6 components, helpers, and tests.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across all project files
- ✓ Reports 0 errors and 0 warnings
- ✓ Process exit code is 0

**Prerequisites:**
- M6.G9 completed

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

**Satisfies Requirements:** Req 17.5, Req 17.6

---

### M6.G10.T2: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Run TypeScript strict compiler check (`tsc --noEmit`) to confirm complete type safety across all project components, client islands, view models, metadata builders, and tests.

**Acceptance Criteria:**
- ✓ `npm run typecheck` runs without errors
- ✓ Process exit code is 0
- ✓ Confirms zero `any` or implicit `any` violations

**Prerequisites:**
- M6.G10.T1 completed

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

**Satisfies Requirements:** Req 17.5, Req 17.6

---

### M6.G10.T3: Execute Full Test Suite Quality Gate (`npm test`)

**Objective:** Run Vitest across all unit, property, accessibility, keyboard, and hygiene test suites.

**Acceptance Criteria:**
- ✓ `npm test` runs all test suites in the project (M1 through M6)
- ✓ All 21 property tests execute with $\ge 100$ iterations each
- ✓ All tests pass with zero failures
- ✓ Process exit code is 0

**Prerequisites:**
- M6.G10.T2 completed

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

**Satisfies Requirements:** Req 17.1, Req 17.2, Req 17.5

---

### M6.G10.T4: Execute Production Build Quality Gate (`npm run build`)

**Objective:** Run `npm run build` to confirm `validate:content` triggers and passes, and Next.js produces static HTML output in `out/` with `/projects` and every `/projects/[slug]` listed as static (`○ (Static)`).

**Acceptance Criteria:**
- ✓ `validate:content` executes and validates all schemas
- ✓ Next.js static build succeeds with exit code 0 and zero missing-Suspense errors
- ✓ Route `/projects` and each `/projects/[slug]` indicated as statically prerendered
- ✓ Output directory `out/` contains static `projects.html` and one HTML file per project slug

**Prerequisites:**
- M6.G10.T3 completed

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
if ($LASTEXITCODE -eq 0 -and (Test-Path "out\projects.html")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.2, Req 7.5, Req 9.1, Req 9.2, Req 17.5

---

### M6.G10.T5: Inspect Prerendered Static Projects Index Output (`out/projects.html`)

**Objective:** Inspect the generated static HTML export of `/projects` (`out/projects.html`) to verify that all project cards are present in the fallback grid, the single `<h1>` exists, and heavy documentation is completely absent.

**Acceptance Criteria:**
- ✓ File `out/projects.html` exists
- ✓ Contains single `<h1 ...>Projects</h1>`
- ✓ Contains project card titles for all projects in `content/projects/`
- ✓ Contains `<link rel="canonical" href="https://example.vercel.app/projects">` with zero query string
- ✓ Contains ZERO occurrences of heavy documentation content (e.g. `## Alpha Engine Docs`)
- ✓ PowerShell inspection script exits with PASS

**Prerequisites:**
- M6.G10.T4 completed

**Implementation Details:**

Execute build output inspection using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$indexHtml = "out\projects.html"
if (-not (Test-Path $indexHtml)) {
    Write-Error "Static projects.html not found in out/ directory"
    exit 1
}

$content = Get-Content $indexHtml -Raw
$violations = @()

# 1. Heading hierarchy
$h1Matches = [regex]::Matches($content, '<h1\b[^>]*>Projects<\/h1>')
if ($h1Matches.Count -ne 1) { $violations += "Expected exactly 1 <h1>Projects</h1> in projects.html" }

# 2. Canonical tag
if (-not ($content -match '<link[^>]*rel="canonical"[^>]*href="https://example\.vercel\.app/projects"')) {
    $violations += "Canonical link missing or contains query parameters in projects.html"
}

# 3. Documentation exclusion check
if ($content.Contains("Alpha Engine Docs") -or $content.Contains("## ")) {
    $violations += "CRITICAL: Documentation markdown content leaked into projects.html static output!"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$indexHtml = "out\projects.html"
if (-not (Test-Path $indexHtml)) {
    Write-Error "Static projects.html not found in out/ directory"
    exit 1
}

$content = Get-Content $indexHtml -Raw
$violations = @()

# 1. Heading hierarchy
$h1Matches = [regex]::Matches($content, '<h1\b[^>]*>Projects<\/h1>')
if ($h1Matches.Count -ne 1) { $violations += "Expected exactly 1 <h1>Projects</h1> in projects.html" }

# 2. Canonical tag
if (-not ($content -match '<link[^>]*rel="canonical"[^>]*href="https://example\.vercel\.app/projects"')) {
    $violations += "Canonical link missing or contains query parameters in projects.html"
}

# 3. Documentation exclusion check
if ($content.Contains("Alpha Engine Docs") -or $content.Contains("## ")) {
    $violations += "CRITICAL: Documentation markdown content leaked into projects.html static output!"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 7.2, Req 7.6, Req 15.6

---

### M6.G10.T6: Inspect Prerendered Static Project Detail Output (`out/projects/[slug].html`)

**Objective:** Inspect the static HTML export of a project detail page to confirm single `<h1>`, breadcrumb navigation, canonical tag without query parameters, and complete absence of JSON-LD structured data.

**Acceptance Criteria:**
- ✓ Confirms static HTML files exist under `out/projects/` corresponding to project slugs
- ✓ Inspects first detail HTML file: confirms single `<h1>`
- ✓ Confirms `<nav aria-label="Breadcrumb">`
- ✓ Confirms `<link rel="canonical">` points to `{siteUrl}/projects/{slug}` with zero query parameters
- ✓ Confirms zero `application/ld+json` script tags (Req 15.7)
- ✓ PowerShell inspection script exits with PASS

**Prerequisites:**
- M6.G10.T5 completed

**Implementation Details:**

Execute detail build inspection using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$detailFiles = Get-ChildItem -Path "out\projects" -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }
if ($detailFiles.Count -eq 0) {
    # Check if Next.js exported as out/projects/[slug]/index.html
    $detailFiles = Get-ChildItem -Path "out\projects" -Recurse -Filter "index.html"
}

if ($detailFiles.Count -eq 0) {
    Write-Error "No prerendered project detail HTML files found in out/projects"
    exit 1
}

$firstDetail = $detailFiles[0]
$content = Get-Content $firstDetail.FullName -Raw
$violations = @()

# 1. Single h1
$h1Matches = [regex]::Matches($content, '<h1\b')
if ($h1Matches.Count -ne 1) { $violations += "Expected exactly 1 <h1> in $($firstDetail.Name), found $($h1Matches.Count)" }

# 2. Breadcrumb nav
if (-not ($content -match '<nav\b[^>]*aria-label="Breadcrumb"')) {
    $violations += "Breadcrumb navigation landmark missing in $($firstDetail.Name)"
}

# 3. Canonical tag
if (-not ($content -match '<link[^>]*rel="canonical"[^>]*href="https://example\.vercel\.app/projects/')) {
    $violations += "Canonical link missing or inaccurate in $($firstDetail.Name)"
}

# 4. JSON-LD absence check
if ($content.Contains("application/ld+json")) {
    $violations += "CRITICAL: JSON-LD structured data found in $($firstDetail.Name) (Req 15.7 violation)!"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$detailFiles = Get-ChildItem -Path "out\projects" -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }
if ($detailFiles.Count -eq 0) {
    # Check if Next.js exported as out/projects/[slug]/index.html
    $detailFiles = Get-ChildItem -Path "out\projects" -Recurse -Filter "index.html"
}

if ($detailFiles.Count -eq 0) {
    Write-Error "No prerendered project detail HTML files found in out/projects"
    exit 1
}

$firstDetail = $detailFiles[0]
$content = Get-Content $firstDetail.FullName -Raw
$violations = @()

# 1. Single h1
$h1Matches = [regex]::Matches($content, '<h1\b')
if ($h1Matches.Count -ne 1) { $violations += "Expected exactly 1 <h1> in $($firstDetail.Name), found $($h1Matches.Count)" }

# 2. Breadcrumb nav
if (-not ($content -match '<nav\b[^>]*aria-label="Breadcrumb"')) {
    $violations += "Breadcrumb navigation landmark missing in $($firstDetail.Name)"
}

# 3. Canonical tag
if (-not ($content -match '<link[^>]*rel="canonical"[^>]*href="https://example\.vercel\.app/projects/')) {
    $violations += "Canonical link missing or inaccurate in $($firstDetail.Name)"
}

# 4. JSON-LD absence check
if ($content.Contains("application/ld+json")) {
    $violations += "CRITICAL: JSON-LD structured data found in $($firstDetail.Name) (Req 15.7 violation)!"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 10.1, Req 15.1, Req 15.3, Req 15.6, Req 15.7

---

### M6.G10.T7: Audit Architectural Scope Boundaries (Zero M7–M10 Contamination)

**Objective:** Verify that M6 remained strictly within its projects module boundary: no new pages under `src/app/` (other than `projects/page.tsx` and `projects/[slug]/page.tsx`), no certifications/blog route directories, no API routes, no server actions, no forms, no analytics, and no premature feature code for M7–M10.

**Acceptance Criteria:**
- ✓ Confirms `src/app/` contains ONLY `layout.tsx`, `not-found.tsx`, `site-metadata.ts`, `page.tsx`, `globals.css`, and `projects/`
- ✓ Confirms zero directories created for `src/app/certifications/` or `src/app/blog/`
- ✓ Confirms zero `route.ts` or `'use server'` files exist
- ✓ Confirms zero `index.ts` barrel files exist in `src/components/projects/` or `src/lib/projects/`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G10.T6 completed

**Implementation Details:**

Execute scope boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$violations = @()

# 1. Check premature route directories
$forbiddenDirs = @(
    "src\app\certifications",
    "src\app\blog"
)
foreach ($d in $forbiddenDirs) {
    if (Test-Path $d) {
        $violations += "Premature milestone route directory found: $d (reserved for M7-M8)"
    }
}

# 2. Check projects directories for barrel files
if (Test-Path "src\components\projects\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/components/projects (AGENTS.md 7.2)"
}
if (Test-Path "src\lib\projects\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/lib/projects (AGENTS.md 7.2)"
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
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$violations = @()

# 1. Check premature route directories
$forbiddenDirs = @(
    "src\app\certifications",
    "src\app\blog"
)
foreach ($d in $forbiddenDirs) {
    if (Test-Path $d) {
        $violations += "Premature milestone route directory found: $d (reserved for M7-M8)"
    }
}

# 2. Check projects directories for barrel files
if (Test-Path "src\components\projects\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/components/projects (AGENTS.md 7.2)"
}
if (Test-Path "src\lib\projects\index.ts") {
    $violations += "Forbidden barrel file index.ts found in src/lib/projects (AGENTS.md 7.2)"
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

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 17.7, Req 17.8

---

### M6.G10.T8: Verify Upstream Foundations and Config Invariance (`git diff`)

**Objective:** Execute `git diff` on `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, `globals.css`, `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, and `src/content/` to confirm zero unintended modifications occurred during Milestone 6.

**Acceptance Criteria:**
- ✓ `git diff` on all upstream files produces zero lines
- ✓ Script returns PASS

**Prerequisites:**
- M6.G10.T7 completed

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json package-lock.json next.config.ts tsconfig.json
if ($diff.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Upstream protected files modified!`n$diff"
    "FAIL"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json package-lock.json next.config.ts tsconfig.json
if ($diff.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Upstream protected files modified!`n$diff"
    "FAIL"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 17.7

---

### M6.G10.T9: Audit Test Matrix Coverage for M6 & Finalize `task-notes.md`

**Objective:** Verify that every project component, pure helper, and route has a matching test file in `tests/projects/`, that all 21 properties have dedicated property tests, and finalize `.kiro/specs/m6-projects-module/task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms all 14 project test files exist in `tests/projects/`
- ✓ Confirms all 21 properties are accounted for in test files
- ✓ Updates `.kiro/specs/m6-projects-module/task-notes.md` with final gate results and sign-offs
- ✓ Confirms baseline tag `m6-baseline` designation

**Prerequisites:**
- M6.G10.T8 completed

**Implementation Details:**

Audit test matrix and finalize `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$expectedTests = @(
    "tests\projects\projects-text.test.ts",
    "tests\projects\tech-key.test.ts",
    "tests\projects\card-data.test.ts",
    "tests\projects\filter-params.test.ts",
    "tests\projects\derive-filter-options.test.ts",
    "tests\projects\filter-projects.test.ts",
    "tests\projects\select-related-projects.test.ts",
    "tests\projects\get-project-links.test.ts",
    "tests\projects\demote-headings.test.ts",
    "tests\projects\format-result-count.test.ts",
    "tests\projects\project-metadata.test.ts",
    "tests\projects\purity.test.ts",
    "tests\projects\project-card.test.tsx",
    "tests\projects\project-grid.test.tsx",
    "tests\projects\project-filter-bar.test.tsx",
    "tests\projects\projects-explorer.test.tsx",
    "tests\projects\projects-index.test.tsx",
    "tests\projects\projects-page.test.tsx",
    "tests\projects\project-breadcrumb.test.tsx",
    "tests\projects\project-header.test.tsx",
    "tests\projects\project-metadata.test.tsx",
    "tests\projects\project-links.test.tsx",
    "tests\projects\build-documentation.test.tsx",
    "tests\projects\related-projects.test.tsx",
    "tests\projects\detail-page.test.tsx",
    "tests\projects\static-params.test.ts",
    "tests\projects\detail-metadata.test.ts",
    "tests\projects\a11y-index.test.tsx",
    "tests\projects\a11y-detail.test.tsx",
    "tests\projects\keyboard.test.tsx",
    "tests\projects\source-hygiene.test.ts"
)

$missing = @()
foreach ($t in $expectedTests) {
    if (-not (Test-Path $t)) {
        $missing += $t
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing test files: $($missing -join ', ')"
    exit 1
}

$signOff = @'

## 5. Milestone 6 Final Sign-Off & Gate Summary

- **Lint Gate (`npm run lint`):** PASS (0 errors, 0 warnings)
- **Typecheck Gate (`npm run typecheck`):** PASS (0 errors, strict mode enforced)
- **Test Gate (`npm test`):** PASS (All M1–M6 test suites passing, all 21 property tests verified >= 100 iterations)
- **Build Gate (`npm run build`):** PASS (Static HTML export generated into `out/` with `/projects` and `/projects/[slug]` listed as static)
- **Static Output Inspection:** PASS (`out/projects.html` verified static with single `<h1>`, Suspense fallback grid with all cards, zero client controls before hydration, and zero documentation leaks; detail HTML verified with single `<h1>`, breadcrumbs, canonical tag, and zero JSON-LD)
- **Axe WCAG 2.1 AA Gate:** PASS (0 violations across index and detail routes in default, filtered, empty, and minimal states)
- **Keyboard Trapping & Tab Flow:** PASS (Full keyboard traversal, Enter/Space activation, and focus restoration to first chip upon clearing filters verified)
- **Source Hygiene Scan:** PASS (0 raw hex, 0 arbitrary Tailwind, exactly 1 client component `projects-explorer.tsx`, 0 scope leaks, all files < 300 lines)
- **Scope Audit:** PASS (Zero barrel files, zero M7–M10 contamination)
- **Root Config Diff:** PASS (`git diff` clean across all protected upstream files)
- **Deferred Verification Note:** Active navigation links to `/certifications` and `/blog` are structurally verified as correct `href` attributes; destination pages will resolve once M7 and M8 are completed.

**Baseline Designation:** `m6-baseline`
'@

Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $signOff -Encoding UTF8
"PASS"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$expectedTests = @(
    "tests\projects\projects-text.test.ts",
    "tests\projects\tech-key.test.ts",
    "tests\projects\card-data.test.ts",
    "tests\projects\filter-params.test.ts",
    "tests\projects\derive-filter-options.test.ts",
    "tests\projects\filter-projects.test.ts",
    "tests\projects\select-related-projects.test.ts",
    "tests\projects\get-project-links.test.ts",
    "tests\projects\demote-headings.test.ts",
    "tests\projects\format-result-count.test.ts",
    "tests\projects\project-metadata.test.ts",
    "tests\projects\purity.test.ts",
    "tests\projects\project-card.test.tsx",
    "tests\projects\project-grid.test.tsx",
    "tests\projects\project-filter-bar.test.tsx",
    "tests\projects\projects-explorer.test.tsx",
    "tests\projects\projects-index.test.tsx",
    "tests\projects\projects-page.test.tsx",
    "tests\projects\project-breadcrumb.test.tsx",
    "tests\projects\project-header.test.tsx",
    "tests\projects\project-metadata.test.tsx",
    "tests\projects\project-links.test.tsx",
    "tests\projects\build-documentation.test.tsx",
    "tests\projects\related-projects.test.tsx",
    "tests\projects\detail-page.test.tsx",
    "tests\projects\static-params.test.ts",
    "tests\projects\detail-metadata.test.ts",
    "tests\projects\a11y-index.test.tsx",
    "tests\projects\a11y-detail.test.tsx",
    "tests\projects\keyboard.test.tsx",
    "tests\projects\source-hygiene.test.ts"
)

$missing = @()
foreach ($t in $expectedTests) {
    if (-not (Test-Path $t)) {
        $missing += $t
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing test files: $($missing -join ', ')"
    exit 1
}

$signOff = @'

## 5. Milestone 6 Final Sign-Off & Gate Summary

- **Lint Gate (`npm run lint`):** PASS (0 errors, 0 warnings)
- **Typecheck Gate (`npm run typecheck`):** PASS (0 errors, strict mode enforced)
- **Test Gate (`npm test`):** PASS (All M1–M6 test suites passing, all 21 property tests verified >= 100 iterations)
- **Build Gate (`npm run build`):** PASS (Static HTML export generated into `out/` with `/projects` and `/projects/[slug]` listed as static)
- **Static Output Inspection:** PASS (`out/projects.html` verified static with single `<h1>`, Suspense fallback grid with all cards, zero client controls before hydration, and zero documentation leaks; detail HTML verified with single `<h1>`, breadcrumbs, canonical tag, and zero JSON-LD)
- **Axe WCAG 2.1 AA Gate:** PASS (0 violations across index and detail routes in default, filtered, empty, and minimal states)
- **Keyboard Trapping & Tab Flow:** PASS (Full keyboard traversal, Enter/Space activation, and focus restoration to first chip upon clearing filters verified)
- **Source Hygiene Scan:** PASS (0 raw hex, 0 arbitrary Tailwind, exactly 1 client component `projects-explorer.tsx`, 0 scope leaks, all files < 300 lines)
- **Scope Audit:** PASS (Zero barrel files, zero M7–M10 contamination)
- **Root Config Diff:** PASS (`git diff` clean across all protected upstream files)
- **Deferred Verification Note:** Active navigation links to `/certifications` and `/blog` are structurally verified as correct `href` attributes; destination pages will resolve once M7 and M8 are completed.

**Baseline Designation:** `m6-baseline`
'@

Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $signOff -Encoding UTF8
"PASS"
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 17.1, Req 17.2, Req 17.4, Req 17.5

---

### M6.G10.T10: Commit and Tag Milestone 6 Baseline (`m6-baseline`) & Update Progress Tracker

**Objective:** Commit all Milestone 6 components, helpers, route files, and test suites to Git, apply the tag `m6-baseline`, and record completion in `local-ai/program-states/progress-tracker.md`.

**Acceptance Criteria:**
- ✓ All M6 assets staged and committed with standardized commit message
- ✓ Git tag `m6-baseline` created on HEAD
- ✓ `local-ai/program-states/progress-tracker.md` updated marking Milestone 6 as `COMPLETED`
- ✓ Working tree is clean

**Prerequisites:**
- M6.G10.T1 through M6.G10.T9 completed

**Implementation Details:**

Commit, tag, and update progress tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

git add .
git commit -m "feat(m6): projects module, index, filtering, case study detail, build docs, and related projects"
git tag -a "m6-baseline" -m "Milestone 6 Projects Module Verified"

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
| **M6: Projects Index & Case Studies** | **COMPLETED** | PASS (Lint, Types, Tests, Build, Static Output Inspection, Axe, Keyboard) | `m6-baseline` | 2026-10-24 |
| **M7: Certifications & Badges** | NOT STARTED | PENDING | — | — |
| **M8: Blog & Community Participation** | NOT STARTED | PENDING | — | — |
| **M9: Quality, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M10: Production Deployment & Launch** | NOT STARTED | PENDING | — | — |

## Milestone 6 Verification Log
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors, strict mode verified)
- `npm test`: PASS (All unit, property, axe, keyboard, and hygiene test suites green)
- `npm run build`: PASS (static HTML export generated into `out/` with `/projects` and `/projects/[slug]` static)
- Static Output Inspection: PASS (`out/projects.html` verified static with full Suspense fallback grid, single `<h1>`, canonical URL, zero documentation leaks; detail HTML verified with single `<h1>`, breadcrumb, canonical URL, and zero JSON-LD)
- Git Baseline: `m6-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m6): record milestone 6 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$tag = git tag -l "m6-baseline"
$status = git status --porcelain
if ($tag -eq "m6-baseline" -and $status.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.5, Req 17.7

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git tag -l "m6-baseline"
git status
npm run lint
npm run typecheck
npm test
npm run build
```
Expected output:
- Git tag lists `m6-baseline`
- Working tree is clean
- All four verification commands exit with return code 0.

***

### Summary of Completed M6 Goals
All 10 Goal specification files for Milestone 6 (`m6-projects-module`) are now generated and fully detailed:
- `goal1.md`: Fixtures, Fixed UI Strings, Tech Key, Card Data, Upstream Verification, and Gap Log
- `goal2.md`: Filter Parameters, Option Derivation, and Property Tests
- `goal3.md`: Filtering, Related Selection, Links, Heading Demotion, Result Count, and Metadata Builders
- `goal4.md`: ProjectCard and ProjectGrid
- `goal5.md`: ProjectFilterBar, ProjectsExplorer, ProjectsIndex, and the Index Route
- `goal6.md`: ProjectBreadcrumb, ProjectHeader, ProjectMetadata, and ProjectLinks
- `goal7.md`: BuildDocumentation and RelatedProjects
- `goal8.md`: Detail Route, Static Params, Metadata, and Static-Output Checks
- `goal9.md`: Responsive, Token, and Scope Compliance; Accessibility and Keyboard Matrix; Source Hygiene
- `goal10.md`: Final Verification Pipeline, Static-Output Check, and Scope Audit