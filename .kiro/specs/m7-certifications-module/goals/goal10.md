# M7.G10: Final Verification Pipeline, Built-HTML Check, and Scope Audit

> **Milestone:** M7 — Certifications Module  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks (M7.G10.T1 – M7.G10.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 13.1, 13.4, 13.7, 15.7–15.8), `design.md` (Static Generation, Testing Strategy, Quality Gates), `tasks.md` (M7.G10)

---

## Goal Objective

Execute the terminal integration and verification gate for Milestone 7:
1. Strict Quality Pipeline: Run `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`, ensuring all four commands complete with exit code 0.
2. Built-HTML Prerender Verification: Inspect the statically generated HTML output for route `/certifications` to confirm that all credential cards, verification links (`target="_blank"`, `rel="noopener noreferrer"`), plain badge images (`alt`, `width="64"`, `height="64"`), category headers, canonical tags, and Open Graph tags are fully present in static HTML with client JavaScript completely disabled.
3. Zero JSON-LD & Scope Boundary Audit: Assert that no `application/ld+json` script is emitted, no API routes or server actions were added, no dynamic `[slug]` route was generated, and no protected files (`package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, `globals.css`, or upstream directories `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/components/projects/`, `src/lib/home/`, `src/lib/projects/`, `src/content/`) were modified.
4. Final Milestone Handoff: Verify that all 15 correctness properties and 15 requirement areas are 100% covered, finalize `task-notes.md`, and declare Milestone 7 complete.

---

## Goal Success Criteria

- ✓ `npm run lint` completes with zero warnings/errors (exit code 0).
- ✓ `npm run typecheck` completes with zero errors (exit code 0).
- ✓ `npm test` runs the complete project test suite and all tests pass with exit code 0.
- ✓ `npm run build` completes with exit code 0 and lists `/certifications` as a static route (`○` / static prerender).
- ✓ Prerendered HTML file `.next/server/app/certifications.html` (or `.next/server/app/certifications/page.html`) contains the page `<h1>Certifications</h1>`, every valid verification link, every badge image, and valid canonical/Open Graph metadata.
- ✓ Zero `<script type="application/ld+json">` tags in the built HTML.
- ✓ `git diff` against the M6 baseline shows changes restricted strictly to permitted M7 locations:
  - `src/app/certifications/`
  - `src/components/certifications/`
  - `src/lib/certifications/`
  - `tests/certifications/`
  - `tests/fixtures/`
  - `.kiro/specs/m7-certifications-module/`
- ✓ `package.json` and the lockfile remain 100% byte-for-byte unmodified.
- ✓ Final verification report appended to `.kiro/specs/m7-certifications-module/task-notes.md`.

---

## Prerequisites

- Goals 1 through 9 completed.
- Node.js and project dependencies installed.
- Execution shell: Windows PowerShell.

---

## Tasks

### M7.G10.T1: Run ESLint Quality Gate and Resolve All Issues

**Objective:** Execute project linter across all M7 source and test files and resolve any lint warnings or errors.

**Acceptance Criteria:**
- ✓ `npm run lint` executes across the entire repository.
- ✓ Zero ESLint errors or warnings in M7 files.
- ✓ Clean exit with code 0.

**Prerequisites:**
- Tasks M7.G1 through M7.G9 completed.

**Implementation Details:**
Run the lint script in Windows PowerShell and fix any syntax or styling violations.

**Validation:**
Execute in Windows PowerShell:
```powershell
npm run lint
```
Expected output: No ESLint warnings or errors reported; exits with code 0.

**Satisfies Requirements:** Req 15.8

---

### M7.G10.T2: Run TypeScript Strict Mode Compilation Check

**Objective:** Execute `npm run typecheck` to confirm zero type errors across the workspace.

**Acceptance Criteria:**
- ✓ `npm run typecheck` (or `npx tsc --noEmit`) executes under strict mode.
- ✓ Zero type errors reported across all `.ts` and `.tsx` files.
- ✓ Exits with code 0.

**Prerequisites:**
- M7.G10.T1 completed.

**Implementation Details:**
Run typechecker in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npm run typecheck
```
Expected output: Zero errors; exits with code 0.

**Satisfies Requirements:** Req 15.5, 15.8

---

### M7.G10.T3: Run Full Vitest Test Suite

**Objective:** Run `npm test` across all unit, component, property, and accessibility test suites to verify complete green status.

**Acceptance Criteria:**
- ✓ Executes all test suites across the repository.
- ✓ All M7 test files pass:
  - `category-label.test.ts`
  - `group-certifications.test.ts`
  - `certification-status.test.ts`
  - `verification-href.test.ts`
  - `badge-source.test.ts`
  - `shift-headings.test.ts`
  - `load-supporting-content.test.ts`
  - `expired-indicator.test.tsx`
  - `verification-link.test.tsx`
  - `badge-image.test.tsx`
  - `atomic-components-a11y.test.tsx`
  - `certification-card.test.tsx`
  - `certification-card-a11y.test.tsx`
  - `certification-category-section.test.tsx`
  - `certifications-index.test.tsx`
  - `certifications-index-a11y.test.tsx`
  - `certifications-metadata.test.ts`
  - `page.test.tsx`
  - `static-checks.test.ts`
  - `a11y.test.tsx`
  - `keyboard.test.tsx`
  - `source-hygiene.test.ts`
  - `title-uniqueness.test.ts`
- ✓ All 15 fast-check properties execute $\ge 100$ runs and pass.
- ✓ Exits with code 0.

**Prerequisites:**
- M7.G10.T2 completed.

**Implementation Details:**
Execute test command in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npm test
```
Expected output: All test suites pass; 100% green; exits with code 0.

**Satisfies Requirements:** Req 15.1, 15.2, 15.3, 15.4, 15.8

---

### M7.G10.T4: Execute Next.js Production Build and Verify Static Route Listing

**Objective:** Run `npm run build` and confirm that Next.js static compilation generates route `/certifications` as static prerendered HTML without server execution errors.

**Acceptance Criteria:**
- ✓ `npm run build` completes with exit code 0.
- ✓ Build output table includes `/certifications`.
- ✓ Route type indicator for `/certifications` is `○ (Static)` prerendered HTML.
- ✓ Build time stays well within performance budgets.

**Prerequisites:**
- M7.G10.T3 completed.

**Implementation Details:**
Run build command in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npm run build
```
Expected output:
- Build output logs:
  ```
  Route (app)                              Size     First Load JS
  ┌ ○ /certifications                      ... kB         ... kB
  ```
- Exits with code 0.

**Satisfies Requirements:** Req 13.1, 15.8

---

### M7.G10.T5: Prerendered HTML Content and Accessibility Elements Inspection

**Objective:** Parse the generated static HTML for `/certifications` to verify that all credential titles, verification links, and badge images exist in the static markup without requiring JavaScript execution.

**Acceptance Criteria:**
- ✓ Locates the prerendered HTML file in `.next/server/app/certifications.html` (or `.next/server/app/certifications/page.html` or `out/certifications.html`).
- ✓ Confirms HTML contains `<h1...` with text `"Certifications"`.
- ✓ Confirms HTML contains all category section `<h2>` tags.
- ✓ Confirms all verification links are present with `target="_blank"` and `rel="noopener noreferrer"`.
- ✓ Confirms all badge images are present with `alt`, `width="64"`, and `height="64"`.
- ✓ Logs findings in `task-notes.md`.

**Prerequisites:**
- `npm run build` completed in M7.G10.T4.

**Implementation Details:**
Create and execute a node script `scripts/inspect-built-certifications.ts` or run PowerShell inspection:

```powershell
$htmlPath = Get-ChildItem -Path .next\server\app -Filter "*certifications*.html" -Recurse | Select-Object -First 1 -ExpandProperty FullName
if (-not $htmlPath) {
    $htmlPath = Get-ChildItem -Path out -Filter "certifications.html" -Recurse | Select-Object -First 1 -ExpandProperty FullName
}

if ($htmlPath) {
    $html = Get-Content $htmlPath -Raw
    $hasH1 = $html -match "<h1[^>]*>Certifications</h1>"
    $hasLinks = $html -match 'rel="noopener noreferrer"'
    $hasImages = $html -match 'width="64"'
    Write-Host "HTML Prerender Verification:"
    Write-Host "  H1 Present: $hasH1"
    Write-Host "  Links Present: $hasLinks"
    Write-Host "  Images Present: $hasImages"
} else {
    Write-Warning "Could not find certifications HTML file in .next or out directory"
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
# Run the inspection script block above
```
Expected output: All elements reported as `True`.

**Satisfies Requirements:** Req 13.1, 13.4

---

### M7.G10.T6: Prerendered HTML Metadata and Zero JSON-LD Verification

**Objective:** Inspect the static HTML of `/certifications` to confirm canonical URL and Open Graph tags are present without query parameters, and that no JSON-LD script exists.

**Acceptance Criteria:**
- ✓ HTML contains `<link rel="canonical" href=".../certifications">` with no query parameters.
- ✓ HTML contains `<meta property="og:title" content="Certifications">`.
- ✓ HTML contains `<meta property="og:url" content=".../certifications">`.
- ✓ HTML contains zero instances of `<script type="application/ld+json">`.
- ✓ Logs findings in `task-notes.md`.

**Prerequisites:**
- Built HTML file available from M7.G10.T4.

**Implementation Details:**
Inspect HTML file using PowerShell:

```powershell
$htmlPath = Get-ChildItem -Path .next\server\app, out -Filter "*certifications*.html" -Recurse | Select-Object -First 1 -ExpandProperty FullName
$html = Get-Content $htmlPath -Raw

$hasCanonical = $html -match 'rel="canonical" href="[^"?]+\/certifications"'
$hasOgTitle = $html -match 'property="og:title" content="Certifications"'
$hasNoJsonLd = -not ($html -match 'application\/ld\+json')

Write-Host "Metadata Verification:"
Write-Host "  Canonical Valid: $hasCanonical"
Write-Host "  OG Title Valid: $hasOgTitle"
Write-Host "  No JSON-LD: $hasNoJsonLd"
```

**Validation:**
Execute in Windows PowerShell:
```powershell
# Run the metadata inspection script block above
```
Expected output: All items report `True`.

**Satisfies Requirements:** Req 12.1, 12.3, 12.4, 12.5, 12.6, 13.4

---

### M7.G10.T7: Scope Boundary and Prohibited Files Audit

**Objective:** Audit the codebase to ensure zero forbidden files, routes, or backend components were created during Milestone 7.

**Acceptance Criteria:**
- ✓ Zero API routes or route handlers exist (`src/app/**/route.ts` or `src/pages/api/`).
- ✓ Zero `'use server'` actions exist in the repository.
- ✓ Zero middleware files exist (`middleware.ts`).
- ✓ Directory `src/app/certifications/` contains only `page.tsx` (and no `[slug]` folder).
- ✓ No blog files or other future milestone files were created.

**Prerequisites:**
- Source tree in completed state.

**Implementation Details:**
Run file tree scan in Windows PowerShell:

```powershell
$apiRoutes = Get-ChildItem -Path src -Filter "route.ts" -Recurse
$slugFolder = Test-Path "src\app\certifications\[slug]"
$middleware = Test-Path "src\middleware.ts"

if ($apiRoutes.Count -gt 0 -or $slugFolder -or $middleware) {
    Write-Error "Scope boundary violation detected!"
} else {
    Write-Host "Scope boundary audit clean."
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
# Run the scope boundary check above
```
Expected output: `Scope boundary audit clean.`

**Satisfies Requirements:** Req 1.7, 13.5

---

### M7.G10.T8: Protected Files and Package Manifest Diff Check

**Objective:** Run `git diff` against root configuration and protected files to confirm that `package.json`, lockfiles, and upstream directories remain 100% untouched.

**Acceptance Criteria:**
- ✓ `git diff package.json` is empty.
- ✓ `git diff package-lock.json` (or `pnpm-lock.yaml`) is empty.
- ✓ `git diff next.config.ts tsconfig.json tailwind.config.ts src/app/globals.css` is empty.
- ✓ `git status` confirms zero modified files in `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/components/projects/`, `src/lib/home/`, `src/lib/projects/`, or `src/content/`.
- ✓ Zero unapproved image assets added to `public/images/certifications/`.

**Prerequisites:**
- Git repository available.

**Implementation Details:**
Execute git status checks in Windows PowerShell:

```powershell
git diff --name-only package.json package-lock.json next.config.ts tsconfig.json tailwind.config.ts src\app\globals.css
git diff --name-only src\components\ui src\components\layout src\components\home src\components\projects src\lib\home src\lib\projects src\content
```

**Validation:**
Execute in Windows PowerShell:
```powershell
# Run the git diff checks above
```
Expected output: Completely empty output (zero modified files in protected paths).

**Satisfies Requirements:** Req 9.8, 13.7, 15.7

---

### M7.G10.T9: Verify Architectural Layout and Finalize Task Notes

**Objective:** Verify that every source file in `src/components/certifications/` and `src/lib/certifications/` has an exact 1:1 matching test file in `tests/certifications/` conforming to `design.md`, and finalize `.kiro/specs/m7-certifications-module/task-notes.md`.

**Acceptance Criteria:**
- ✓ 1:1 mapping confirmed between M7 components/helpers and tests:
  - `category-order.ts` & `category-label.ts` $\rightarrow$ `category-label.test.ts`
  - `group-certifications.ts` $\rightarrow$ `group-certifications.test.ts`
  - `certification-status.ts` $\rightarrow$ `certification-status.test.ts`
  - `verification-href.ts` $\rightarrow$ `verification-href.test.ts`
  - `badge-source.ts` $\rightarrow$ `badge-source.test.ts`
  - `shift-headings.ts` $\rightarrow$ `shift-headings.test.ts`
  - `load-supporting-content.ts` $\rightarrow$ `load-supporting-content.test.ts`
  - `expired-indicator.tsx` $\rightarrow$ `expired-indicator.test.tsx`
  - `verification-link.tsx` $\rightarrow$ `verification-link.test.tsx`
  - `badge-image.tsx` $\rightarrow$ `badge-image.test.tsx`
  - `certification-card.tsx` $\rightarrow$ `certification-card.test.tsx`
  - `certification-category-section.tsx` $\rightarrow$ `certification-category-section.test.tsx`
  - `certifications-index.tsx` $\rightarrow$ `certifications-index.test.tsx`
  - `certifications-metadata.ts` $\rightarrow$ `certifications-metadata.test.ts`
  - `page.tsx` $\rightarrow$ `page.test.tsx`
- ✓ All 15 fast-check properties confirmed present and passing.
- ✓ Final summary recorded in `.kiro/specs/m7-certifications-module/task-notes.md`.

**Prerequisites:**
- Tasks M7.G10.T1 through M7.G10.T8 completed.

**Implementation Details:**
Append final verification summary to `.kiro/specs/m7-certifications-module/task-notes.md`:

```markdown
## Milestone 7 Verification & Completion Report

- **Date:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **Milestone:** M7 — Certifications Module (`m7-certifications-module`)
- **Status:** COMPLETE / 100% GREEN

### Verification Pipeline Results:
1. `npm run lint`: PASS (0 errors, 0 warnings)
2. `npm run typecheck`: PASS (0 errors)
3. `npm test`: PASS (All unit, property, and accessibility suites green)
4. `npm run build`: PASS (Route `/certifications` prerendered statically)

### Properties Covered (15 / 15):
- Property 1: Partition and no loss (G2)
- Property 2: Groups and members ordered (G2)
- Property 3: Input-order independence (G2)
- Property 4: Idempotence under flatten (G2)
- Property 5: Immutability under deep freeze (G2)
- Property 6: Expiry classification matches date order (G3)
- Property 7: Category labels total and distinct (G1)
- Property 8: Card shows exactly fields given (G6)
- Property 9: Expired indicator iff expired (G6)
- Property 10: Verification link HTTPS rule (G3 helper, G6 render)
- Property 11: Badge image pair and source rule (G3 helper, G6 render)
- Property 12: Heading shift caps below h3 (G4)
- Property 13: Supporting content iff non-empty (G4 loader, G6 render)
- Property 14: Page structure ordered, labelled, level-correct (G7)
- Property 15: Metadata derived from site URL (G8)

### Architectural Invariants Maintained:
- Zero Client JavaScript (`'use client'` count: 0)
- Single Clock Read in `page.tsx`
- Plain `<img>` for badges with explicit dimensions
- Unbroken heading hierarchy (`h1` -> `h2` -> `h3` -> `h4+`)
- Zero changes to `package.json`, lockfiles, or upstream modules
```

**Validation:**
Execute in Windows PowerShell:
```powershell
Get-Content .kiro\specs\m7-certifications-module\task-notes.md | Select-String "Milestone 7 Verification & Completion Report"
```
Expected output: Header logged.

**Satisfies Requirements:** Req 15.7, 15.8

---

### M7.G10.T10: Confirm Milestone 7 Completion and Final Sign-Off

**Objective:** Final gate execution: confirm that all 10 goals of Milestone 7 have completed, all quality gates are green, scope boundaries are intact, and hand off to the next pipeline stage.

**Acceptance Criteria:**
- ✓ All 10 Goal files (`goal1.md` – `goal10.md`) are complete and verified.
- ✓ All 100 atomic tasks are implemented without placeholders or TBDs.
- ✓ The 4 quality gates pass consecutively:
  ```powershell
  npm run lint
  npm run typecheck
  npm test
  npm run build
  ```
- ✓ Terminal handoff status marked as complete.

**Prerequisites:**
- Tasks M7.G10.T1 through M7.G10.T9 completed.

**Implementation Details:**
Execute the full terminal quality gate pipeline in Windows PowerShell:

```powershell
npm run lint; if ($LASTEXITCODE -eq 0) { npm run typecheck }; if ($LASTEXITCODE -eq 0) { npm test }; if ($LASTEXITCODE -eq 0) { npm run build }
```

**Validation:**
Execute in Windows PowerShell:
```powershell
# Run the pipeline command above
```
Expected output: All 4 commands exit with code 0.

**Satisfies Requirements:** Req 13.1, 13.4, 13.7, 15.7, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 10 and Milestone 7 are complete:
```powershell
npm run lint
npm run typecheck
npm test
npm run build
```
Expected output: All four verification gates exit with code 0. Route `/certifications` is statically prerendered. Milestone 7 is officially complete.