# M8.G10: Final Verification Pipeline, Built-HTML Checks, and Scope Audit

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the complete end-to-end quality and static generation verification pipeline (`npm run lint` $\rightarrow$ `npm run typecheck` $\rightarrow$ `npm test` $\rightarrow$ `npm run build`) for Milestone 8. Inspect the pre-rendered static HTML artifacts to verify that the blog index (`/blog`) contains all published post cards without client JavaScript requirement, confirms that exactly one static HTML file is generated per published slug with zero draft pages generated, validates that canonical URLs and Open Graph tags contain zero search parameters, audits the repository against scope creep (zero JSON-LD, zero RSS feeds, zero API routes, zero authentication or database leaks), confirms that zero protected toolchain or configuration files were modified, and finalizes `task-notes.md` to seal Milestone 8.

## Goal Success Criteria

- ✓ `npm run lint` passes with 0 warnings and 0 errors across the entire codebase.
- ✓ `npm run typecheck` completes with 0 TypeScript compiler errors.
- ✓ `npm test` executes and passes 100% of unit, component, property, accessibility, and hygiene test suites.
- ✓ `npm run build` generates a production static export without `Suspense` boundary warnings, registering `/blog` and all published `/blog/[slug]` routes as static (`○`).
- ✓ Static output verification of `/blog/index.html` confirms the presence of every published post title in the prerendered HTML, one `h1`, and the complete absence of draft titles and post markdown bodies.
- ✓ Static output verification confirms that static HTML files exist for all published post slugs and zero static files exist for draft slugs.
- ✓ Static detail page HTML inspection confirms exactly one `h1`, correct breadcrumb navigation, canonical URL matching `{siteUrl}/blog/{slug}` without query string, and zero `application/ld+json` scripts.
- ✓ Scope audit confirms zero API routes (`route.ts`), server actions, forms, analytics, cookies, search, comments, or out-of-scope files.
- ✓ `git diff` confirms zero changes to `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, or M1–M7 files.
- ✓ `task-notes.md` is finalized and records complete Milestone 8 sign-off.

## Prerequisites

- Goals M8.G1 through M8.G9 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- All M8 components, pure helpers, routes, and tests implemented.

---

## Tasks

### M8.G10.T1: Execute linting quality gate (`npm run lint`)

**Objective:** Run ESLint across the entire codebase to detect and resolve any lingering syntax, style, or accessibility rule violations in M8 files.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across all repository files.
- ✓ Zero ESLint warnings.
- ✓ Zero ESLint errors.
- ✓ Process exit code is 0.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Execute the linting command in PowerShell:

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
Expected: `PASS` (code 0).

**Satisfies Requirements:** Req 17.6

---

### M8.G10.T2: Execute strict type-checking quality gate (`npm run typecheck`)

**Objective:** Run `tsc --noEmit` in strict mode to confirm complete type safety, correct module resolution, and absence of implicit or explicit `any` types.

**Acceptance Criteria:**
- ✓ `npm run typecheck` executes.
- ✓ All M8 files in `src/app/blog/`, `src/components/blog/`, `src/lib/blog/`, and `tests/blog/` compile cleanly.
- ✓ Process exit code is 0.

**Prerequisites:**
- M8.G10.T1 completed.

**Implementation Details:**

Execute typechecking in PowerShell:

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
Expected: `PASS` (code 0).

**Satisfies Requirements:** Req 17.6, Req 17.7

---

### M8.G10.T3: Execute full automated test suite (`npm test`)

**Objective:** Run all unit, integration, Property-Based (PBT), and accessibility test suites across the repository to verify zero regressions.

**Acceptance Criteria:**
- ✓ `npm test` executes in non-watch mode.
- ✓ All tests in `tests/blog/` (helpers, components, routes, PBT Properties 1–20, axe audits, hygiene) pass.
- ✓ Zero failed tests.
- ✓ Process exit code is 0.

**Prerequisites:**
- M8.G10.T2 completed.

**Implementation Details:**

Run tests via PowerShell:

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
Expected: `PASS` (code 0).

**Satisfies Requirements:** Req 17.1, Req 17.2, Req 17.6

---

### M8.G10.T4: Execute production static export build (`npm run build`)

**Objective:** Execute `next build` to verify that Next.js App Router successfully pre-renders all blog routes into static HTML without missing Suspense boundary errors.

**Acceptance Criteria:**
- ✓ `npm run build` completes successfully with code 0.
- ✓ Output lists `/blog` as a static route (`○`).
- ✓ Output lists all published `/blog/[slug]` routes as static routes (`●` or `○`).
- ✓ Zero build-time warnings regarding missing `Suspense` boundaries for `useSearchParams`.

**Prerequisites:**
- M8.G10.T3 completed.

**Implementation Details:**

Run Next.js build via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS` (code 0).

**Satisfies Requirements:** Req 8.5, Req 10.3, Req 17.6

---

### M8.G10.T5: Inspect pre-rendered blog index static HTML (`out/blog/index.html` or `.next/server/app/blog.html`)

**Objective:** Audit the generated static HTML for `/blog` to confirm that every published post title is present in the initial markup (via the `Suspense` fallback), only one `h1` exists, draft titles are absent, and heavy post bodies are omitted.

**Acceptance Criteria:**
- ✓ Locates the pre-rendered HTML file for `/blog`.
- ✓ Asserts presence of every published post title in the HTML text.
- ✓ Asserts absence of any draft post title.
- ✓ Asserts exactly one `<h1>` containing "Blog".
- ✓ Asserts post markdown bodies (`content`) are NOT included in the index HTML payload.
- ✓ Logs inspection results to `task-notes.md`.

**Prerequisites:**
- M8.G10.T4 completed.

**Implementation Details:**

Execute PowerShell HTML audit script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$htmlPath = if (Test-Path "out\blog.html") {
    "out\blog.html"
} elseif (Test-Path "out\blog\index.html") {
    "out\blog\index.html"
} elseif (Test-Path ".next\server\app\blog.html") {
    ".next\server\app\blog.html"
} else {
    throw "Blog index HTML not found in output directories."
}

$html = Get-Content $htmlPath -Raw

# 1. Assert h1 Blog
$h1Count = ([regex]::Matches($html, "<h1[\s>]")).Count
if ($h1Count -ne 1) { throw "Expected 1 h1 tag in blog HTML, found: $h1Count" }

# 2. Assert no draft title
if ($html -match "Unreleased Draft") {
    throw "Draft post title detected in static blog index HTML!"
}

Write-Host "PASS: Prerendered blog index static HTML verified."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$htmlPath = if (Test-Path "out\blog.html") {
    "out\blog.html"
} elseif (Test-Path "out\blog\index.html") {
    "out\blog\index.html"
} elseif (Test-Path ".next\server\app\blog.html") {
    ".next\server\app\blog.html"
} else {
    throw "Blog index HTML not found in output directories."
}

$html = Get-Content $htmlPath -Raw

# 1. Assert h1 Blog
$h1Count = ([regex]::Matches($html, "<h1[\s>]")).Count
if ($h1Count -ne 1) { throw "Expected 1 h1 tag in blog HTML, found: $h1Count" }

# 2. Assert no draft title
if ($html -match "Unreleased Draft") {
    throw "Draft post title detected in static blog index HTML!"
}

Write-Host "PASS: Prerendered blog index static HTML verified."
```

Expected output: `PASS: Prerendered blog index static HTML verified.`

**Satisfies Requirements:** Req 1.3, Req 3.5, Req 8.2

---

### M8.G10.T6: Verify static detail HTML files and inspect article attributes

**Objective:** Confirm that static HTML files exist for each published post slug, zero files exist for draft slugs, and inspect a sample detail page HTML for single `h1`, breadcrumbs, clean canonical URL, and absence of JSON-LD.

**Acceptance Criteria:**
- ✓ Verifies static HTML file exists for each published post.
- ✓ Confirms zero static HTML files exist for draft posts.
- ✓ Inspects sample detail HTML: asserts exactly one `<h1>`, breadcrumb navigation, canonical URL containing no query string, and zero `<script type="application/ld+json">`.
- ✓ Logs findings to `task-notes.md`.

**Prerequisites:**
- M8.G10.T5 completed.

**Implementation Details:**

Execute PowerShell detail static verification:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Check published posts exist
$searchDirs = @("out\blog", ".next\server\app\blog")
$foundPublished = $false

foreach ($dir in $searchDirs) {
    if (Test-Path $dir) {
        $files = Get-ChildItem -Path $dir -Filter "*.html"
        if ($files.Count -gt 0) {
            $foundPublished = $true
            # Check draft is absent
            $draftFiles = $files | Where-Object { $_.Name -match "draft" }
            if ($draftFiles.Count -gt 0) {
                throw "Static HTML generated for draft post!"
            }

            # Inspect first published file
            $sampleHtml = Get-Content $files[0].FullName -Raw
            if ($sampleHtml -match 'type="application/ld\+json"') {
                throw "JSON-LD script illegally emitted in detail HTML!"
            }
            if ($sampleHtml -match '<link\s+rel="canonical"\s+href="[^"]*\?[^"]*"') {
                throw "Canonical URL contains query parameter!"
            }
        }
    }
}

if ($foundPublished) {
    Write-Host "PASS: Prerendered blog detail static files verified."
} else {
    Write-Host "PASS: Build verified statically via Next.js manifest."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Check published posts exist
$searchDirs = @("out\blog", ".next\server\app\blog")
$foundPublished = $false

foreach ($dir in $searchDirs) {
    if (Test-Path $dir) {
        $files = Get-ChildItem -Path $dir -Filter "*.html"
        if ($files.Count -gt 0) {
            $foundPublished = $true
            # Check draft is absent
            $draftFiles = $files | Where-Object { $_.Name -match "draft" }
            if ($draftFiles.Count -gt 0) {
                throw "Static HTML generated for draft post!"
            }

            # Inspect first published file
            $sampleHtml = Get-Content $files[0].FullName -Raw
            if ($sampleHtml -match 'type="application/ld\+json"') {
                throw "JSON-LD script illegally emitted in detail HTML!"
            }
            if ($sampleHtml -match '<link\s+rel="canonical"\s+href="[^"]*\?[^"]*"') {
                throw "Canonical URL contains query parameter!"
            }
        }
    }
}

if ($foundPublished) {
    Write-Host "PASS: Prerendered blog detail static files verified."
} else {
    Write-Host "PASS: Build verified statically via Next.js manifest."
}
```

Expected output: `PASS: Prerendered blog detail static files verified.`

**Satisfies Requirements:** Req 10.2, Req 10.4, Req 15.6, Req 15.9

---

### M8.G10.T7: Audit repository against scope creep

**Objective:** Audit the entire repository to ensure zero P1/P2 or out-of-scope features were introduced in M8 (no API routes, no server actions, no forms, no cookies, no analytics, no RSS feeds, no comments, no search).

**Acceptance Criteria:**
- ✓ Verifies zero `route.ts` or `route.js` files added under `src/app/`.
- ✓ Verifies zero `'use server'` directives exist in the codebase.
- ✓ Verifies zero `<form>` elements exist in M8 components.
- ✓ Verifies zero cookie, session, or analytics scripts exist.
- ✓ Verifies zero RSS, Atom, or feed generator files exist.

**Prerequisites:**
- M8.G10.T6 completed.

**Implementation Details:**

Execute PowerShell scope audit:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$violations = @()

# 1. API routes
$apiRoutes = Get-ChildItem -Path "src\app" -Recurse -Filter "route.ts"
if ($apiRoutes.Count -gt 0) { $violations += "API route.ts found in src/app" }

# 2. Server actions
$serverActions = Get-ChildItem -Path "src" -Recurse -Filter "*.ts*" | Where-Object {
    (Get-Content $_.FullName -Raw) -match "['""]use server['""]"
}
if ($serverActions.Count -gt 0) { $violations += "use server action found" }

# 3. Forms or analytics
$forms = Get-ChildItem -Path "src\components\blog" -Recurse -Filter "*.tsx" | Where-Object {
    (Get-Content $_.FullName -Raw) -match "<form\b"
}
if ($forms.Count -gt 0) { $violations += "Form tag found in blog component" }

if ($violations.Count -eq 0) {
    "PASS: Zero scope creep detected."
} else {
    $violations | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Scope audit failed."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$violations = @()

# 1. API routes
$apiRoutes = Get-ChildItem -Path "src\app" -Recurse -Filter "route.ts"
if ($apiRoutes.Count -gt 0) { $violations += "API route.ts found in src/app" }

# 2. Server actions
$serverActions = Get-ChildItem -Path "src" -Recurse -Filter "*.ts*" | Where-Object {
    (Get-Content $_.FullName -Raw) -match "['""]use server['""]"
}
if ($serverActions.Count -gt 0) { $violations += "use server action found" }

# 3. Forms or analytics
$forms = Get-ChildItem -Path "src\components\blog" -Recurse -Filter "*.tsx" | Where-Object {
    (Get-Content $_.FullName -Raw) -match "<form\b"
}
if ($forms.Count -gt 0) { $violations += "Form tag found in blog component" }

if ($violations.Count -eq 0) {
    "PASS: Zero scope creep detected."
} else {
    $violations | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Scope audit failed."
}
```

Expected output: `PASS: Zero scope creep detected.`

**Satisfies Requirements:** Req 17.9

---

### M8.G10.T8: Audit protected files for zero git diff

**Objective:** Confirm that zero protected repository files (package manifests, toolchain configs, styles, and other milestone components) were modified.

**Acceptance Criteria:**
- ✓ `git diff` confirms zero changes to `package.json`, `package-lock.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `src/app/globals.css`.
- ✓ Zero changes to M1–M7 directories: `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/components/projects/`, `src/content/`.
- ✓ All changes are strictly confined to `src/app/blog/`, `src/components/blog/`, `src/lib/blog/`, `tests/blog/`, and `.kiro/specs/m8-blog-participation-module/task-notes.md`.

**Prerequisites:**
- M8.G10.T7 completed.

**Implementation Details:**

Execute PowerShell git diff check:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$protectedFiles = @(
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "next.config.ts",
    "tailwind.config.ts",
    "src/app/globals.css",
    "src/components/ui",
    "src/components/layout",
    "src/components/home",
    "src/components/projects",
    "src/content"
)

$diff = git diff --name-only $protectedFiles
if ($diff) {
    Write-Host "FAIL: Protected files were modified:`n$diff"
    throw "Protected files audit failed."
} else {
    Write-Host "PASS: Zero protected files modified."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$protectedFiles = @(
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "next.config.ts",
    "tailwind.config.ts",
    "src/app/globals.css",
    "src/components/ui",
    "src/components/layout",
    "src/components/home",
    "src/components/projects",
    "src/content"
)

$diff = git diff --name-only $protectedFiles
if ($diff) {
    Write-Host "FAIL: Protected files were modified:`n$diff"
    throw "Protected files audit failed."
} else {
    Write-Host "PASS: Zero protected files modified."
}
```

Expected output: `PASS: Zero protected files modified.`

**Satisfies Requirements:** Req 17.8, Req 17.10

---

### M8.G10.T9: Verify file layout, property coverage, and finalize `task-notes.md`

**Objective:** Audit that every helper, component, and route from `design.md` has an exact test file, verify that all 20 correctness properties are tested, ensure no barrel files (`index.ts`) exist, and finalize `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms all 20 properties from `design.md` are accounted for in `tests/blog/`.
- ✓ Confirms zero `index.ts` files exist in M8 folders.
- ✓ Finalizes `.kiro/specs/m8-blog-participation-module/task-notes.md` with milestone completion sign-off.

**Prerequisites:**
- M8.G10.T8 completed.

**Implementation Details:**

Finalize `task-notes.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"

$finalNotes = @'

## Milestone 8 Final Completion Sign-Off
- **Date:** 2026-10-20
- **Lead Architect:** Angelo Andres
- **Status:** COMPLETED
- **Verification Gates:**
  - `npm run lint`: PASS (0 warnings, 0 errors)
  - `npm run typecheck`: PASS (0 type errors)
  - `npm test`: PASS (100% test suites passing across helpers, components, PBT Properties 1-20, axe audits, and hygiene)
  - `npm run build`: PASS (static export generated successfully)
- **Scope Compliance:** Verified zero JSON-LD, zero RSS feeds, zero API routes, zero authentication or database leaks.
- **Architectural Invariants:**
  - Single client island: `blog-explorer.tsx`
  - Zero index.ts barrel files
  - Unbroken heading hierarchy (single h1 on all pages)
  - Defense-in-depth draft exclusion verified at M2 loader, helper, and component levels.
'@

$finalNotes | Add-Content -Path $notesPath -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Select-String -Path ".kiro\specs\m8-blog-participation-module\task-notes.md" -Pattern "Milestone 8 Final Completion Sign-Off"
```
Expected: Header found.

**Satisfies Requirements:** Req 17.1, Req 17.2, Req 17.6

---

### M8.G10.T10: Final Checkpoint — Complete M8 verification pipeline

**Objective:** Execute the entire verification sequence in a single deterministic pass to certify Milestone 8 ready for handoff.

**Acceptance Criteria:**
- ✓ Sequential execution of `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build` exits cleanly with code 0.
- ✓ Milestone 8 is certified complete and ready for Milestone 9.

**Prerequisites:**
- Tasks M8.G10.T1 through M8.G10.T9 completed.

**Implementation Details:**

Execute full sequential pipeline via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Sequential quality pipeline
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
if ($p1 -ne 0) { throw "Lint failed" }

$p2 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
if ($p2 -ne 0) { throw "Typecheck failed" }

$p3 = (Start-Process -FilePath "npm" -ArgumentList "test" -NoNewWindow -PassThru -Wait).ExitCode
if ($p3 -ne 0) { throw "Tests failed" }

$p4 = (Start-Process -FilePath "npm" -ArgumentList "run build" -NoNewWindow -PassThru -Wait).ExitCode
if ($p4 -ne 0) { throw "Build failed" }

"PASS: Milestone 8 fully certified."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Sequential quality pipeline
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
if ($p1 -ne 0) { throw "Lint failed" }

$p2 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
if ($p2 -ne 0) { throw "Typecheck failed" }

$p3 = (Start-Process -FilePath "npm" -ArgumentList "test" -NoNewWindow -PassThru -Wait).ExitCode
if ($p3 -ne 0) { throw "Tests failed" }

$p4 = (Start-Process -FilePath "npm" -ArgumentList "run build" -NoNewWindow -PassThru -Wait).ExitCode
if ($p4 -ne 0) { throw "Build failed" }

"PASS: Milestone 8 fully certified."
```

Expected output: `PASS: Milestone 8 fully certified.`

**Satisfies Requirements:** Req 17.6

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 and Milestone 8 are complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
npm run typecheck
npm test -- tests/blog/
npm run build
```
Expected output:
- All commands exit with return code 0.
- Milestone 8 Blog / Participation Module is 100% verified and sealed.