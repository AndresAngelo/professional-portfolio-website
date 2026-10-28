# M9.G10: Final Verification Pipeline, Real-Build Audit Run, and Scope Audit

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Execute the complete end-to-end quality pipeline (`lint` $\rightarrow$ `typecheck` $\rightarrow$ `test` $\rightarrow$ `build` $\rightarrow$ `audit`) against the real, statically generated site output (`out/`), generate and freeze the production performance baseline (`baselines/performance.json`), run the automated Lighthouse Core Web Vitals audit (or log manual results), perform an exhaustive architectural scope audit, and record milestone completion in `task-notes.md`. This goal confirms that 100% of P0 routes are error-free, all 20 fast-check properties pass, zero unapproved files or dependencies exist, and no release blockers remain.

---

## Goal Success Criteria

- ✓ `npm run lint` completes with 0 errors and 0 warnings
- ✓ `npm run typecheck` completes with 0 errors
- ✓ `npm test` executes and passes all test suites completely offline without triggering network requests or Lighthouse
- ✓ `npm run build` completes with exit code 0 within the 180-second wall-clock performance SLA
- ✓ `npm run audit` runs all six offline audits against real `out/` build output and passes with 0 error findings
- ✓ `baselines/performance.json` is generated from the real build output and committed to Git
- ✓ `npm run audit:lighthouse` executes and evaluates all P0 routes against target SLAs
- ✓ Scope audit verifies that no `vercel.json`, custom API routes, analytics, forms, dark mode, or runtime dependencies exist
- ✓ All 20 fast-check properties across Goals 1–9 have passing verification
- ✓ Milestone 9 sign-off is documented in `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

---

## Prerequisites

- Goals M9.G1 through M9.G9 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Static export enabled in `next.config.ts` (`output: 'export'`)
- All audit libraries, fixtures, and documentation in place

---

## Tasks

### M9.G10.T1: Execute Static Linter Quality Gate (`npm run lint`)

**Objective:** Run the full project linter across all source, script, and test files to guarantee zero ESLint, TypeScript, or JSX accessibility violations.

**Acceptance Criteria:**
- ✓ `npm run lint` completes with exit code 0
- ✓ Zero warnings or errors reported across `scripts/`, `src/`, and `tests/`
- ✓ Prohibits explicit `any`, unescaped entities, and invalid accessible names

**Prerequisites:**
- M9.G9.T10 completed

**Implementation Details:**

Execute the linter via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
if ($LASTEXITCODE -ne 0) {
    Write-Error "Lint quality gate failed."
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.6, Req 18.8

---

### M9.G10.T2: Execute Strict Typecheck Quality Gate (`npm run typecheck`)

**Objective:** Run `tsc --noEmit` across the repository to confirm complete TypeScript strict mode compliance and alias resolution.

**Acceptance Criteria:**
- ✓ `npm run typecheck` completes with exit code 0
- ✓ Zero type inference failures or missing declaration errors
- ✓ `@/*` path aliases resolve without error

**Prerequisites:**
- M9.G10.T1 completed

**Implementation Details:**

Execute typechecking via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -ne 0) {
    Write-Error "Typecheck quality gate failed."
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.6, Req 18.8

---

### M9.G10.T3: Execute Test Suite Quality Gate (`npm test`)

**Objective:** Execute all unit, integration, content-gate, and property test suites via Vitest, verifying completely offline execution and zero Lighthouse invocation.

**Acceptance Criteria:**
- ✓ `npm test` runs in non-watch mode and passes all test suites
- ✓ All 20 fast-check properties execute with $\ge 100$ iterations each
- ✓ Zero network calls occur during the run
- ✓ Lighthouse is not executed

**Prerequisites:**
- M9.G10.T2 completed

**Implementation Details:**

Run the test suite via PowerShell with network isolation test:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test
if ($LASTEXITCODE -ne 0) {
    Write-Error "Vitest test suite execution failed."
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.4, Req 1.5, Req 12.10, Req 18.8

---

### M9.G10.T4: Execute Static Production Build and Measure Duration

**Objective:** Execute `npm run build` to generate static output in `out/`, measure wall-clock build time, and confirm it completes in $< 180$ seconds.

**Acceptance Criteria:**
- ✓ `npm run build` completes with exit code 0
- ✓ Output directory `out/` is populated with static HTML, CSS, JS, and image assets
- ✓ Build time is measured and logged to `task-notes.md`
- ✓ Wall-clock time is strictly below 180 seconds

**Prerequisites:**
- M9.G10.T3 completed

**Implementation Details:**

Measure and execute static build via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$sw = [System.Diagnostics.Stopwatch]::StartNew()
npm run build
$sw.Stop()

$buildSeconds = [Math]::Round($sw.Elapsed.TotalSeconds, 2)
Write-Host "Build completed in $buildSeconds seconds."

if ($buildSeconds -gt 180) {
    Write-Error "Build duration ($buildSeconds s) exceeded 180s SLA."
    exit 1
}

$notesPath = "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md"
Add-Content -Path $notesPath -Value "`n- **Production Build Duration:** $buildSeconds seconds (SLA: < 180s)" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "out\index.html"
```
Expected: `True`

**Satisfies Requirements:** Req 1.3, Req 11.11, Req 18.8

---

### M9.G10.T5: Execute Aggregate Audit Against Real Build Output

**Objective:** Execute `npm run audit` against the real `out/` directory, running all six offline audits to completion and ensuring zero error findings.

**Acceptance Criteria:**
- ✓ `npm run audit` executes without environment overrides
- ✓ All 6 audits (`routes`, `structure`, `a11y`, `seo`, `perf`, `links`) complete
- ✓ Zero `error` severity findings are emitted
- ✓ Summary reports 100% pass across all audits

**Prerequisites:**
- M9.G10.T4 completed

**Implementation Details:**

Run the aggregate audit runner via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run audit
if ($LASTEXITCODE -ne 0) {
    Write-Error "Aggregate audit failed on real build output."
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run audit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.5, Req 16.2, Req 16.3, Req 18.8

---

### M9.G10.T6: Generate and Commit Production Performance Baseline

**Objective:** Generate the official production performance baseline using `npm run audit:perf -- --update-baseline` and verify subsequent audit passes without regression.

**Acceptance Criteria:**
- ✓ `baselines/performance.json` is generated with real gzip measurements
- ✓ Re-running `npm run audit:perf` passes with zero regressions
- ✓ Baseline file is formatted stably with no volatile timestamps

**Prerequisites:**
- M9.G10.T5 completed
- Target file: `baselines/performance.json`

**Implementation Details:**

Generate and verify baseline via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Update baseline from real build
npm run audit:perf -- --update-baseline
if ($LASTEXITCODE -ne 0) { exit 1 }

# Confirm subsequent audit passes cleanly
npm run audit:perf
if ($LASTEXITCODE -ne 0) { exit 1 }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "baselines\performance.json"
```
Expected: `True`

**Satisfies Requirements:** Req 11.4, Req 11.5, Req 16.5

---

### M9.G10.T7: Execute Automated Lighthouse Audit

**Objective:** Run `npm run audit:lighthouse` against the locally served static output to verify Core Web Vitals and category scores across all P0 routes.

**Acceptance Criteria:**
- ✓ Launches static server and headless Chrome
- ✓ Evaluates 5 mobile emulation runs per route
- ✓ Validates Accessibility $\ge 95$, Performance/SEO/Best Practices $\ge 90$
- ✓ Validates LCP $< 2.5$ s, CLS $< 0.1$, FCP $< 1.8$ s, TBT $< 200$ ms
- ✓ Writes `reports/lighthouse.json`

**Prerequisites:**
- M9.G10.T6 completed

**Implementation Details:**

Run Lighthouse audit via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run audit:lighthouse
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Automated Lighthouse audit reported issues or was run in headless container."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "reports\lighthouse.json"
```
Expected: `True`

**Satisfies Requirements:** Req 12.1–12.7

---

### M9.G10.T8: Execute Architectural Scope and Boundaries Audit

**Objective:** Audit Git diff and filesystem to ensure strict adherence to M9 architectural boundaries (no runtime dependencies, no API routes, no forms, no analytics, no M10 deployment files).

**Acceptance Criteria:**
- ✓ Asserts zero occurrences of `app/api`, `route.ts`, `"use server"`, or `vercel.json`
- ✓ Asserts zero cookie references or third-party analytics in repository diff
- ✓ Confirms no modifications outside approved paths
- ✓ Confirms zero `index.ts` barrel files were created

**Prerequisites:**
- M9.G10.T7 completed

**Implementation Details:**

Execute scope audit via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Check for illegal server routes or actions
$serverHits = Get-ChildItem -Path src/ -Recurse -Include *.ts, *.tsx |
  Select-String -Pattern "['""]use server['""]|from ['""]next/server['""]"
if ($serverHits) {
    Write-Error "Illegal server action or next/server import found: $serverHits"
    exit 1
}

# 2. Check for illegal API routes
$apiRoutes = Get-ChildItem -Path src/app -Recurse -Include route.ts, route.js
if ($apiRoutes) {
    Write-Error "Illegal API route file found: $apiRoutes"
    exit 1
}

# 3. Check for vercel.json
if (Test-Path "vercel.json") {
    Write-Error "vercel.json is M10 scope and must not exist in M9."
    exit 1
}

# 4. Check for forbidden barrel files
$barrels = Get-ChildItem -Path scripts/audit, src/lib/structured-data -Recurse -Filter "index.ts"
if ($barrels) {
    Write-Error "Forbidden index.ts barrel file found: $barrels"
    exit 1
}

Write-Host "Scope audit PASS: Zero unauthorized files, boundaries, or server constructs."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src/app/api"
```
Expected: `False`

**Satisfies Requirements:** Req 1.1, Req 18.4, Req 18.5, Req 18.7

---

### M9.G10.T9: Document Release Blockers and Finalize Task Notes

**Objective:** Record all release-blocking requirements for Milestone 10 (such as replacing example content hosts with the production custom domain) in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Documents requirement to replace `example.com` with real production domain in M10
- ✓ Summarizes all verified quality metrics and test counts
- ✓ Marks Milestone 9 as COMPLETED in `task-notes.md`

**Prerequisites:**
- M9.G10.T8 completed
- Target file: `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Implementation Details:**

Update `task-notes.md` via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md"

$summaryNote = @'

## Milestone 9 Verification Summary & Release Sign-off (Completed M9.G10)

- **Verification Pipeline Status:** 100% PASS
  - `npm run lint`: PASS (0 errors, 0 warnings)
  - `npm run typecheck`: PASS (0 errors)
  - `npm test`: PASS (100% offline, all 20 fast-check properties passing)
  - `npm run build`: PASS (static export generated in `out/`)
  - `npm run audit`: PASS (routes, structure, a11y, seo, perf, links passing)
- **Baseline:** `baselines/performance.json` initialized and verified.
- **M10 Hand-off Release Blockers:**
  - `content/site.json`: Update `siteUrl` from placeholder (`example.com`) to official production domain.
  - Vercel Deployment & Security Headers: Deferred to Milestone 10 (M10).

### Status: MILESTONE 9 COMPLETED
'@

Add-Content -Path $notesPath -Value $summaryNote -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" | Select-String "MILESTONE 9 COMPLETED"
```
Expected: `PASS`

**Satisfies Requirements:** Req 8.8, Req 14.5, Req 17.6, Req 18.1

---

### M9.G10.T10: Final Milestone 9 Completion Checkpoint

**Objective:** Execute the entire verification sequence in strict order to confirm that the entire repository is in a clean, reproducible, and verifiable state.

**Acceptance Criteria:**
- ✓ `npm run lint` exits 0
- ✓ `npm run typecheck` exits 0
- ✓ `npm test` exits 0
- ✓ `npm run build` exits 0
- ✓ `npm run audit` exits 0

**Prerequisites:**
- M9.G10.T1 through M9.G10.T9 completed

**Implementation Details:**

Run master verification pipeline via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run lint
if ($LASTEXITCODE -ne 0) { exit 1 }

npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

npm test
if ($LASTEXITCODE -ne 0) { exit 1 }

npm run build
if ($LASTEXITCODE -ne 0) { exit 1 }

npm run audit
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "=========================================================="
Write-Host "   MILESTONE 9 QUALITY PIPELINE FULLY VERIFIED (PASS)    "
Write-Host "=========================================================="
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run audit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 and Milestone 9 are complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint && npm run typecheck && npm test && npm run build && npm run audit
```
Expected output:
- `npm run lint` passes with 0 warnings/errors
- `npm run typecheck` exits with 0
- `npm test` passes all test suites and properties
- `npm run build` completes in $< 180$ seconds and exports `out/`
- `npm run audit` completes with status PASS across all 6 audits.