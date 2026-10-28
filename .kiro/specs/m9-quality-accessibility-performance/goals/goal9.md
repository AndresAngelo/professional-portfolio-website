# M9.G9: Approval-Gated Integration, Aggregate Audit Command, and Quality Documentation

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Execute the approved repository integrations under Approvals A1 through A6 (Approved 2026-10-22). This goal appends `reports/` to `.gitignore` (A4), updates `package.json` with the canonical audit scripts (`audit:*` and `audit`) and pinned devDependencies (A1, A2, A3, A6), implements the multi-audit aggregate runner `scripts/audit/run-all.ts`, wires minimal JSON-LD rendering lines into `src/app/page.tsx`, `src/app/blog/[slug]/page.tsx`, and `src/app/projects/[slug]/page.tsx` (A5), authoring the comprehensive quality pipeline guide `docs/quality/verification-pipeline.md`, and compiling the requirements traceability matrix `docs/quality/traceability-matrix.md`.

---

## Goal Success Criteria

- ✓ Approvals A1, A4, A5, and A6 are re-confirmed from `task-notes.md` prior to executing modifications
- ✓ `.gitignore` ignores `reports/` and `git check-ignore reports/test.json` outputs a clean match
- ✓ `package.json` contains scripts for `audit:routes`, `audit:structure`, `audit:a11y`, `audit:seo`, `audit:perf`, `audit:links`, `audit:links:online`, `audit:lighthouse`, and `audit`
- ✓ `scripts/audit/run-all.ts` executes all offline audits sequentially without stopping on initial failures, emits a one-line summary per audit, and aggregates exit codes
- ✓ `src/app/page.tsx`, `src/app/blog/[slug]/page.tsx`, and `src/app/projects/[slug]/page.tsx` integrate `<JsonLd />` blocks with minimal diffs
- ✓ `docs/quality/verification-pipeline.md` defines the 6-step release verification order, audit contracts, and DOD mappings
- ✓ `docs/quality/traceability-matrix.md` maps every PRD success metric to an audit and classification
- ✓ Zero modifications to `next.config.ts`, `tsconfig.json`, or CI configurations

---

## Prerequisites

- Goals M9.G1 through M9.G8 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Approvals A1–A6 recorded in `task-notes.md`

---

## Tasks

### M9.G9.T1: Re-confirm Recorded Approvals A1, A4, A5, and A6

**Objective:** Audit `task-notes.md` to ensure Approvals A1, A4, A5, and A6 are actively marked as Approved 2026-10-22 before modifying any restricted files.

**Acceptance Criteria:**
- ✓ Validates presence of approval markers for A1, A4, A5, and A6
- ✓ Logs confirmation to console before proceeding to file writes
- ✓ Asserts that proposed diffs strictly conform to the approved scopes

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- File `.kiro\specs\m9-quality-accessibility-performance\task-notes.md` exists

**Implementation Details:**

Verify approvals via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" -Raw
$required = @('**A1**', '**A4**', '**A5**', '**A6**')
foreach ($item in $required) {
    if ($notes -notmatch "$item.*Approved") {
        Write-Error "Approval $item is missing or not marked Approved in task-notes.md"
        exit 1
    }
}
Write-Host "All approvals (A1, A4, A5, A6) verified. Proceeding with gated tasks."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" -Raw
if ($notes -match "\*\*A1\*\*.*Approved" -and $notes -match "\*\*A4\*\*.*Approved") { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.7, Req 16.8, Req 18.6

---

### M9.G9.T2: Update `.gitignore` to Ignore Audit Reports Directory (Approval A4)

**Objective:** Append `reports/` to `.gitignore` under Approval A4 so generated audit JSON/Markdown reports are not tracked by version control.

**Acceptance Criteria:**
- ✓ `reports/` is present in `.gitignore`
- ✓ `git check-ignore reports/test.json` succeeds
- ✓ `baselines/` remains tracked by Git

**Prerequisites:**
- M9.G9.T1 completed
- Target file: `.gitignore`

**Implementation Details:**

Append `reports/` to `.gitignore` via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$gi = Get-Content ".gitignore" -Raw
if ($gi -notmatch "(^|\n)reports/") {
    Add-Content -Path ".gitignore" -Value "`n# Audit Reports`nreports/`n" -Encoding UTF8
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git check-ignore reports/sample.json
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.5, Req 16.8

---

### M9.G9.T3: Add Audit Scripts and DevDependencies to `package.json` (Approvals A1, A6)

**Objective:** Register all canonical audit scripts in `package.json` utilizing `vite-node --config vitest.config.ts`, verify devDependencies, and regenerate the lockfile cleanly.

**Acceptance Criteria:**
- ✓ Registers scripts: `audit:routes`, `audit:structure`, `audit:a11y`, `audit:seo`, `audit:perf`, `audit:links`, `audit:links:online`, `audit:lighthouse`, and `audit`
- ✓ Runs `npm install` to update `package-lock.json`
- ✓ Zero runtime dependencies added

**Prerequisites:**
- M9.G9.T1 completed
- Target files: `package.json`, `package-lock.json`

**Implementation Details:**

Update `package.json` scripts using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$scripts = $pkg.scripts

$scripts | Add-Member -MemberType NoteProperty -Name "audit:routes" -Value "vite-node --config vitest.config.ts scripts/audit/routes.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:structure" -Value "vite-node --config vitest.config.ts scripts/audit/structure.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:a11y" -Value "vite-node --config vitest.config.ts scripts/audit/a11y.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:seo" -Value "vite-node --config vitest.config.ts scripts/audit/seo.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:perf" -Value "vite-node --config vitest.config.ts scripts/audit/perf.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:links" -Value "vite-node --config vitest.config.ts scripts/audit/links.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:links:online" -Value "vite-node --config vitest.config.ts scripts/audit/links-online.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit:lighthouse" -Value "vite-node --config vitest.config.ts scripts/audit/lighthouse.ts" -Force
$scripts | Add-Member -MemberType NoteProperty -Name "audit" -Value "vite-node --config vitest.config.ts scripts/audit/run-all.ts" -Force

$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8

# Clean lockfile update
npm install --package-lock-only
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.scripts.audit -and $pkg.scripts."audit:routes") { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.8

---

### M9.G9.T4: Implement Aggregate Audit Runner (`scripts/audit/run-all.ts`)

**Objective:** Implement `scripts/audit/run-all.ts` to sequentially execute all offline audits (`routes`, `structure`, `a11y`, `seo`, `perf`, `links`), run to completion without early termination, print summary lines, and aggregate exit codes.

**Acceptance Criteria:**
- ✓ Sequentially runs the 6 offline audits in fixed order
- ✓ Never terminates on initial failure; runs all audits to completion
- ✓ Excludes `audit:lighthouse` and `audit:links:online`
- ✓ Prints summary line per audit (e.g. `[routes] PASS - Errors: 0, Warnings: 0`)
- ✓ Exits with 1 if any audit has errors, 2 if any has environmental failures, else 0

**Prerequisites:**
- M9.G9.T3 completed
- Target file: `scripts/audit/run-all.ts`

**Implementation Details:**

Create `scripts/audit/run-all.ts`:

```typescript
import { resolveBuildLayout } from './lib/build-layout';
import { runRoutesAudit } from './lib/routes-audit';
import { runStructureAudit } from './lib/structure-audit';
import { runA11yAudit } from './lib/a11y-audit';
import { runSeoAudit } from './lib/seo-audit';
import { runPerfAudit } from './lib/perf-audit';
import { runLinksAudit } from './lib/links-audit';
import { writeReport } from './lib/report';
import type { AuditReport } from './lib/types';

interface AuditDefinition {
  readonly name: string;
  readonly run: (layout: any, args: readonly string[]) => Promise<AuditReport<any>>;
}

async function main() {
  const args = process.argv.slice(2);
  const layout = await resolveBuildLayout();

  if (!layout) {
    process.stderr.write('Build output not found. Run npm run build first.\n');
    process.exit(2);
  }

  const audits: readonly AuditDefinition[] = [
    { name: 'routes', run: runRoutesAudit },
    { name: 'structure', run: runStructureAudit },
    { name: 'a11y', run: runA11yAudit },
    { name: 'seo', run: runSeoAudit },
    { name: 'perf', run: runPerfAudit },
    { name: 'links', run: runLinksAudit },
  ];

  process.stdout.write('Executing Quality Verification Pipeline Audits...\n\n');

  let hasError = false;
  let hasEnvFailure = false;

  for (const a of audits) {
    try {
      const report = await a.run(layout, args);
      const reportPath = await writeReport(report);
      const s = report.summary;

      const statusTag = report.status.toUpperCase().padEnd(7);
      process.stdout.write(
        `[${statusTag}] ${a.name.padEnd(10)} - Errors: ${String(s.errors).padStart(2)}, Warnings: ${String(s.warnings).padStart(2)} -> ${reportPath}\n`
      );

      if (report.status === 'fail') {
        hasError = true;
      }
    } catch (err) {
      hasEnvFailure = true;
      process.stderr.write(`[CRASH]   ${a.name.padEnd(10)} - Execution failed: ${err instanceof Error ? err.message : String(err)}\n`);
    }
  }

  process.stdout.write('\n');

  if (hasError) {
    process.exitCode = 1;
  } else if (hasEnvFailure) {
    process.exitCode = 2;
  } else {
    process.exitCode = 0;
  }
}

void main();
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/run-all.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.2, Req 16.3, Req 16.7

---

### M9.G9.T5: Author Unit Tests for Aggregate Audit Runner

**Objective:** Write `tests/audit/run-all.test.ts` to assert that `run-all` executes all audits to completion, aggregates exit codes according to Decision 10, and excludes Lighthouse and online links.

**Acceptance Criteria:**
- ✓ Asserts all audits execute even when an earlier audit fails
- ✓ Asserts exit code 1 if any audit has an error
- ✓ Asserts exit code 2 if none have errors but an environment failure occurs
- ✓ Asserts `audit:lighthouse` and `audit:links:online` are omitted from the list

**Prerequisites:**
- M9.G9.T4 completed
- Target file: `tests/audit/run-all.test.ts`

**Implementation Details:**

Create `tests/audit/run-all.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Aggregate Audit Runner (run-all)', () => {
  it('strictly excludes lighthouse and links-online from aggregate list', async () => {
    const runAllCode = await fs.readFile(
      path.join(process.cwd(), 'scripts', 'audit', 'run-all.ts'),
      'utf8'
    );

    expect(runAllCode).not.toContain('runLighthouseAudit');
    expect(runAllCode).not.toContain('links-online');
    expect(runAllCode).toContain('runRoutesAudit');
    expect(runAllCode).toContain('runStructureAudit');
    expect(runAllCode).toContain('runA11yAudit');
    expect(runAllCode).toContain('runSeoAudit');
    expect(runAllCode).toContain('runPerfAudit');
    expect(runAllCode).toContain('runLinksAudit');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/run-all.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.2, Req 16.3

---

### M9.G9.T6: Wire Minimal JSON-LD Blocks into Page Routes (Approval A5)

**Objective:** Inject minimal, approved import and render lines for `<JsonLd />` into `src/app/page.tsx` (Person), `src/app/blog/[slug]/page.tsx` (Article & BreadcrumbList), and `src/app/projects/[slug]/page.tsx` (BreadcrumbList) under Approval A5.

**Acceptance Criteria:**
- ✓ Injects `<JsonLd data={buildPersonJsonLd(site)} />` on homepage
- ✓ Injects `<JsonLd data={buildArticleJsonLd(post, site)} />` and `<JsonLd data={buildBreadcrumbJsonLd(...)} />` on blog detail
- ✓ Injects `<JsonLd data={buildBreadcrumbJsonLd(...)} />` on project detail
- ✓ Existing component markup, hooks, and props remain completely unchanged
- ✓ Uses data already loaded by the page Server Components

**Prerequisites:**
- M9.G9.T1 completed
- Existing pages in `src/app/`

**Implementation Details:**

1. In `src/app/page.tsx`, import `JsonLd` and `buildPersonJsonLd`, rendering `<JsonLd data={buildPersonJsonLd(siteConfig)} />` inside the root `<main>`.
2. In `src/app/blog/[slug]/page.tsx`, import `JsonLd`, `buildArticleJsonLd`, and `buildBreadcrumbJsonLd`, rendering both blocks.
3. In `src/app/projects/[slug]/page.tsx`, import `JsonLd` and `buildBreadcrumbJsonLd`, rendering the breadcrumb block.

Apply the modifications carefully via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Example validation check of page files
$home = Get-Content "src/app/page.tsx" -Raw
if ($home -notmatch "buildPersonJsonLd") {
    # Prepend import
    $home = "import { JsonLd } from '@/components/structured-data/json-ld';`nimport { buildPersonJsonLd } from '@/lib/structured-data/person';`n" + $home
    # Inject component inside main
    $home = $home -replace "(<main[^>]*>)", "`$1`n      <JsonLd data={buildPersonJsonLd(siteConfig)} />"
    Set-Content -Path "src/app/page.tsx" -Value $home -Encoding UTF8
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.5

---

### M9.G9.T7: Author Test for JSON-LD Integration Diff Guard

**Objective:** Create `tests/audit/jsonld-integration-diff.test.ts` to assert that modifications to `src/app/` are restricted strictly to the approved `<JsonLd>` imports and tags.

**Acceptance Criteria:**
- ✓ Verifies that `src/app/page.tsx`, `blog/[slug]/page.tsx`, and `projects/[slug]/page.tsx` contain `JsonLd`
- ✓ Asserts no unauthorized component markup or client directives were introduced

**Prerequisites:**
- M9.G9.T6 completed
- Target file: `tests/audit/jsonld-integration-diff.test.ts`

**Implementation Details:**

Create `tests/audit/jsonld-integration-diff.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('JSON-LD Page Integration Guard', () => {
  it('confirms presence of JsonLd components on approved pages', async () => {
    const home = await fs.readFile(path.join(process.cwd(), 'src/app/page.tsx'), 'utf8');
    expect(home).toContain('buildPersonJsonLd');
    expect(home).toContain('<JsonLd');

    const blog = await fs.readFile(path.join(process.cwd(), 'src/app/blog/[slug]/page.tsx'), 'utf8');
    expect(blog).toContain('buildArticleJsonLd');
    expect(blog).toContain('<JsonLd');

    const project = await fs.readFile(path.join(process.cwd(), 'src/app/projects/[slug]/page.tsx'), 'utf8');
    expect(project).toContain('buildBreadcrumbJsonLd');
    expect(project).toContain('<JsonLd');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/jsonld-integration-diff.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.5, Req 18.5

---

### M9.G9.T8: Create Verification Pipeline Guide Document

**Objective:** Author `docs/quality/verification-pipeline.md` detailing the 6-stage release verification sequence, audit descriptions, report schemas, and DOD mappings.

**Acceptance Criteria:**
- ✓ Documents the exact command sequence: `npm ci` $\rightarrow$ `npm run lint` $\rightarrow$ `npm run typecheck` $\rightarrow$ `npm test` $\rightarrow$ `npm run build` $\rightarrow$ `npm run audit`
- ✓ Lists all audit scripts with their respective Quality Gates and report outputs
- ✓ Maps TRD Section 9 Definition of Done items to the audits that enforce them
- ✓ Documents Approvals A1–A6 status and states that deployment verification is owned by M10

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `docs/quality/verification-pipeline.md`:

```markdown
# Verification Pipeline & Release Quality Gates

> **Standard:** TRD Section 8.1 & Section 9 Definition of Done  
> **Milestone:** M9 Quality, Accessibility & Performance  
> **Status:** Active Release Requirement

---

## 1. Pipeline Execution Sequence
Before any deployment or release candidate sign-off, the following commands must execute cleanly in order:

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run audit
```

---

## 2. Audit Suite Catalog & Quality Gates

| Script Name | Scope / Responsibility | Quality Gate Criteria | Output Report |
| :--- | :--- | :--- | :--- |
| `npm run audit:routes` | Route Inventory | 100% of P0 routes exist; 0 drafts published; 404 present | `reports/routes.json` |
| `npm run audit:structure` | HTML Structure & Hygiene | Valid semantic HTML; 0 heading skips; no tracking/secrets | `reports/structure.json` |
| `npm run audit:a11y` | axe-core WCAG 2.1 AA | 0 automated violations across tags `wcag2a`, `wcag2aa`, etc. | `reports/a11y.json` |
| `npm run audit:seo` | Metadata & Open Graph | Title (10–70), Description (50–160), Canonical, OG tags | `reports/seo.json` |
| `npm run audit:perf` | Performance Budgets | Max 5% delta over baseline; chunk $< 80$KB; total $< 25$MB | `reports/perf.json` |
| `npm run audit:links` | Link Crawler & Inventory | 0 broken internal links or fragment IDs; exports inventory | `reports/links.json` |
| `npm run audit:lighthouse`| Lighthouse Mobile CWV | LCP $< 2.5$s, CLS $< 0.1$, FCP $< 1.8$s, TBT $< 200$ms, A11y $\ge 95$ | `reports/lighthouse.json` |
| `npm run audit:links:online`| Online Link Status | Manual check; sends bounded HEAD requests (10s timeout) | `reports/links-online.json` |

---

## 3. Definition of Done (TRD Section 9) Mapping

- **Automated WCAG 2.1 AA:** Enforced via `npm run audit:a11y` and verified with `docs/quality/manual-accessibility-checklist.md`.
- **Core Web Vitals:** Enforced via `npm run audit:lighthouse` and verified with `docs/quality/manual-lighthouse-procedure.md`.
- **Zero API Routes / Zero Tracking:** Enforced via `npm run audit:structure` and `npm run audit:routes`.
- **P0 Repository Links 100%:** Enforced via `tests/audit/content/p0-completeness.test.ts`.

---

## 4. Operational Boundaries
- **Deployment Verification:** Vercel Hobby Plan hosting and live URL verification are exclusively owned by **Milestone 10 (M10)**.
- **Approvals A1–A6:** All six approval items were formally Approved on 2026-10-22.
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "docs\quality\verification-pipeline.md"
```
Expected: `True`

**Satisfies Requirements:** Req 17.1–17.7

---

### M9.G9.T9: Create PRD Requirements Traceability Matrix

**Objective:** Author `docs/quality/traceability-matrix.md` mapping all PRD success metrics to automated and manual quality checks, and create `tests/audit/quality-docs.test.ts`.

**Acceptance Criteria:**
- ✓ Maps every PRD success metric to an audit and quality gate
- ✓ Categorizes verification method as `automated`, `manual`, or `automated + manual`
- ✓ Author unit test in `tests/audit/quality-docs.test.ts` verifying document integrity

**Prerequisites:**
- M9.G9.T8 completed
- Target files: `docs/quality/traceability-matrix.md`, `tests/audit/quality-docs.test.ts`

**Implementation Details:**

1. Create `docs/quality/traceability-matrix.md`:

```markdown
# Requirements & Success Metrics Traceability Matrix

| PRD Success Metric | Target SLA | Enforcing Audit / Test | Verification Mode |
| :--- | :--- | :--- | :--- |
| **Lighthouse Accessibility Score** | $\ge 95$ | `scripts/audit/lighthouse.ts` | `automated + manual` |
| **Automated WCAG 2.1 AA Compliance** | 0 violations on all P0 pages | `scripts/audit/a11y.ts` | `automated` |
| **Core Web Vitals (LCP, CLS, FCP, TBT)** | LCP $< 2.5$s, CLS $< 0.1$, FCP $< 1.8$s, TBT $< 200$ms | `scripts/audit/lighthouse.ts` | `automated + manual` |
| **P0 Route Availability** | 100% of expected routes present | `scripts/audit/routes.ts` | `automated` |
| **Content-Only Publishing** | Zero code changes for new content | `tests/audit/content/validation-rules.test.ts` | `automated` |
| **P0 Project Repository Links** | 100% coverage with valid URLs | `tests/audit/content/p0-completeness.test.ts` | `automated` |
| **Privacy & Zero Visitor Tracking** | No cookies, analytics, or trackers | `scripts/audit/structure.ts` | `automated` |
| **Manual Assistive Tech & Reflow** | NVDA/VoiceOver, 200% zoom, 320px | `docs/quality/manual-accessibility-checklist.md` | `manual` |
```

2. Create `tests/audit/quality-docs.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Quality Documentation Integrity', () => {
  it('verifies verification-pipeline.md contains all required pipeline commands', async () => {
    const pipelineDoc = await fs.readFile(
      path.join(process.cwd(), 'docs', 'quality', 'verification-pipeline.md'),
      'utf8'
    );
    expect(pipelineDoc).toContain('npm ci');
    expect(pipelineDoc).toContain('npm run lint');
    expect(pipelineDoc).toContain('npm run typecheck');
    expect(pipelineDoc).toContain('npm test');
    expect(pipelineDoc).toContain('npm run build');
    expect(pipelineDoc).toContain('npm run audit');
  });

  it('verifies traceability-matrix.md contains all PRD success metrics', async () => {
    const matrixDoc = await fs.readFile(
      path.join(process.cwd(), 'docs', 'quality', 'traceability-matrix.md'),
      'utf8'
    );
    expect(matrixDoc).toContain('Lighthouse Accessibility Score');
    expect(matrixDoc).toContain('Automated WCAG 2.1 AA Compliance');
    expect(matrixDoc).toContain('Core Web Vitals');
    expect(matrixDoc).toContain('P0 Route Availability');
    expect(matrixDoc).toContain('Content-Only Publishing');
    expect(matrixDoc).toContain('P0 Project Repository Links');
    expect(matrixDoc).toContain('Privacy & Zero Visitor Tracking');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/quality-docs.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 18.1–18.3

---

### M9.G9.T10: Milestone 9 Goal 9 Checkpoint Verification

**Objective:** Execute all documentation tests, run aggregate runner over passing fixture, and confirm typecheck and lint compliance with zero unapproved file modifications.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/run-all.test.ts`, `jsonld-integration-diff.test.ts`, and `quality-docs.test.ts` pass
- ✓ CLI `npm run audit` executes cleanly over `AUDIT_BUILD_DIR`
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0

**Prerequisites:**
- M9.G9.T1 through M9.G9.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G9 suites
npx vitest run tests/audit/run-all.test.ts tests/audit/jsonld-integration-diff.test.ts tests/audit/quality-docs.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Test aggregate runner over fixtures
$env:AUDIT_BUILD_DIR = "tests/audit/fixtures/passing-site"
npm run audit
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item env:AUDIT_BUILD_DIR

# 3. Static typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. ESLint
npm run lint
if ($LASTEXITCODE -ne 0) { exit 1 }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.1–16.9, Req 17.1–17.7, Req 18.1–18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/run-all.test.ts tests/audit/jsonld-integration-diff.test.ts tests/audit/quality-docs.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in Goal 9 pass
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.