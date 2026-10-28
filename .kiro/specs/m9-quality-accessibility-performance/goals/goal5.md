# M9.G5: Automated Accessibility Audit (axe-core) and Manual Accessibility Checklist

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the automated accessibility verification layer using `axe-core` in `scripts/audit/lib/a11y-audit.ts` and author the comprehensive human assistive-technology verification procedure in `docs/quality/manual-accessibility-checklist.md`. This goal executes automated WCAG 2.1 Level A and AA audits across every statically built P0 HTML page (including `/404`), records disabled layout rules (such as `color-contrast`) with written architectural justifications, captures `incomplete` findings without masking them as passes, provides graceful fallback execution, and establishes clear manual auditing steps for screen readers, keyboard navigation, high zoom, and reflow.

---

## Goal Success Criteria

- ✓ Approval_Item A2 is confirmed as Approved 2026-10-22 in `task-notes.md` prior to executing `axe-core` imports
- ✓ `scripts/audit/lib/a11y-audit.ts` runs `axe.run` against JSDOM windows across all inventory routes using tags `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa`
- ✓ `color-contrast` is disabled in automated DOM analysis due to JSDOM layout limitations and explicitly documented in `DISABLED_AXE_RULES`
- ✓ Incomplete results are logged as `warning` findings and never treated as passing checks
- ✓ Any thrown axe execution exception is captured as an `axe-run-failed` error finding
- ✓ `scripts/audit/a11y.ts` provides the CLI entry point running through `runCli`
- ✓ `docs/quality/manual-accessibility-checklist.md` provides complete human verification steps covering NVDA, VoiceOver, keyboard traversal, focus rings, contrast (4.5:1 / 3:1), and breakpoints (375px, 768px, 1024px, 1440px)
- ✓ Integration tests verify deterministic offline runs with zero network activity

---

## Prerequisites

- Goals M9.G1 through M9.G4 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Fixtures available in `tests/audit/fixtures/`
- Approval A2 recorded in `task-notes.md`

---

## Tasks

### M9.G5.T1: Verify Approval A2 and Audit axe-core Installation

**Objective:** Confirm that Approval_Item A2 is recorded as Approved 2026-10-22 in `task-notes.md` and verify that `axe-core` is available in `node_modules` with exact pinned versioning.

**Acceptance Criteria:**
- ✓ Validates that `task-notes.md` contains the approval record for A2
- ✓ Checks that `axe-core` can be resolved by Node.js
- ✓ Confirms purpose and maintenance status are recorded
- ✓ Historical fallback: If `axe-core` is absent, dynamic import handles it gracefully

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- File `.kiro\specs\m9-quality-accessibility-performance\task-notes.md` exists

**Implementation Details:**

Verify Approval A2 via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" -Raw
if ($notes -notmatch "\*\*A2\*\*.*Approved") {
    Write-Error "Approval A2 is not recorded as Approved in task-notes.md"
    exit 1
}

# Verify npm package presence
$axeInstalled = Test-Path "node_modules\axe-core"
if (-not $axeInstalled) {
    Write-Host "Installing pinned axe-core devDependency (Approval A2)..."
    npm install --save-dev axe-core@4.10.2
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
node -e "require('axe-core'); console.log('PASS');"
```
Expected: `PASS`

**Satisfies Requirements:** Req 6.1, Req 12.8, Req 18.6

---

### M9.G5.T2: Implement Automated axe-core Accessibility Audit Engine

**Objective:** Implement `runA11yAudit` in `scripts/audit/lib/a11y-audit.ts` to evaluate all statically generated HTML pages against WCAG 2.1 A/AA rules using JSDOM.

**Acceptance Criteria:**
- ✓ Dynamically imports `axe-core` and injects `axe.source` into JSDOM window
- ✓ Evaluates rules with tags `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa`
- ✓ Disables `color-contrast` rule with reason documented in report data
- ✓ Formats each violation into a typed `Finding` with route, rule, selector, and helpUrl
- ✓ Captures unexpected runtime exceptions as `axe-run-failed` error findings

**Prerequisites:**
- M9.G5.T1 completed
- Target file: `scripts/audit/lib/a11y-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/a11y-audit.ts`:

```typescript
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding, RouteEntry } from './types';
import { buildReport } from './report';
import { listFiles, readText } from './build-layout';
import { parsePage } from './html';
import { DISABLED_AXE_RULES } from './config';

export interface AxeReportData {
  readonly axeVersion: string;
  readonly tags: readonly string[];
  readonly disabledRules: readonly string[];
  readonly routes: ReadonlyArray<{
    readonly route: string;
    readonly violations: number;
    readonly incomplete: number;
  }>;
}

export async function runA11yAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport<AxeReportData | null>> {
  let axe: typeof import('axe-core');
  try {
    axe = await import('axe-core');
  } catch {
    return buildReport<AxeReportData | null>({
      audit: 'a11y',
      findings: [],
      routesChecked: 0,
      skipped: ['axe-core is not installed or unresolvable'],
      data: null,
    });
  }

  const allFiles = await listFiles(layout);
  const htmlFiles = allFiles.filter(f => f.endsWith('.html') && !f.startsWith('/_'));
  const findings: Finding[] = [];
  const routeStats: Array<{ route: string; violations: number; incomplete: number }> = [];

  const disabledRuleKeys = Object.keys(DISABLED_AXE_RULES);
  const axeRulesConfig: Record<string, { enabled: boolean }> = {};
  for (const ruleKey of disabledRuleKeys) {
    axeRulesConfig[ruleKey] = { enabled: false };
  }

  const tags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];

  for (const file of htmlFiles) {
    const text = await readText(layout, file);
    if (!text) continue;

    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const isNotFound = routePath === '/404';
    const routeEntry: RouteEntry = {
      path: routePath,
      kind: isNotFound ? 'not-found' : 'home',
      slug: null,
    };

    const parsed = parsePage(routeEntry, file, text);
    const win = parsed.dom.window;

    try {
      // Evaluate axe inside JSDOM window context
      win.eval(axe.source);

      // Run accessibility inspection
      const axeResult = await (win as unknown as { axe: typeof import('axe-core') }).axe.run(
        parsed.document,
        {
          runOnly: {
            type: 'tag',
            values: tags,
          },
          rules: axeRulesConfig,
        }
      );

      // Process violations
      for (const v of axeResult.violations) {
        for (const node of v.nodes) {
          findings.push({
            route: routePath,
            rule: v.id,
            message: `${v.help} (${v.description})`,
            severity: 'error',
            selector: node.target.join(' '),
            details: {
              impact: v.impact ?? null,
              helpUrl: v.helpUrl,
            },
          });
        }
      }

      // Process incomplete findings as warnings (never counted as passes)
      for (const inc of axeResult.incomplete) {
        findings.push({
          route: routePath,
          rule: `axe-incomplete:${inc.id}`,
          message: `Incomplete automated check: ${inc.help}`,
          severity: 'warning',
          details: {
            helpUrl: inc.helpUrl,
          },
        });
      }

      routeStats.push({
        route: routePath,
        violations: axeResult.violations.length,
        incomplete: axeResult.incomplete.length,
      });
    } catch (err) {
      findings.push({
        route: routePath,
        rule: 'axe-run-failed',
        message: `axe inspection crashed on page: ${err instanceof Error ? err.message : String(err)}`,
        severity: 'error',
      });
    }
  }

  const data: AxeReportData = {
    axeVersion: axe.version,
    tags,
    disabledRules: disabledRuleKeys,
    routes: routeStats,
  };

  return buildReport<AxeReportData | null>({
    audit: 'a11y',
    findings,
    routesChecked: htmlFiles.length,
    data,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/a11y-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 6.1–6.7

---

### M9.G5.T3: Implement A11y CLI Entry Point

**Objective:** Create the standalone executable CLI runner `scripts/audit/a11y.ts` connected to `runCli`.

**Acceptance Criteria:**
- ✓ Exports executable CLI via `runCli`
- ✓ Writes `reports/a11y.json` containing `AxeReportData` payload
- ✓ Returns exit code 1 on rule violations, 0 on clean pass

**Prerequisites:**
- M9.G5.T2 completed
- Target file: `scripts/audit/a11y.ts`

**Implementation Details:**

Create `scripts/audit/a11y.ts`:

```typescript
import { runCli } from './lib/cli';
import { runA11yAudit } from './lib/a11y-audit';

void runCli('a11y', (layout, args) => runA11yAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/a11y.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.1

---

### M9.G5.T4: Verify Inclusion of Not-Found Page and Incomplete Handling

**Objective:** Ensure that `runA11yAudit` executes against `/404.html` and properly converts `incomplete` axe checks into warnings rather than passes.

**Acceptance Criteria:**
- ✓ `/404.html` is parsed and evaluated by axe
- ✓ Incomplete results emit `severity: 'warning'` with rule ID prefixed with `axe-incomplete:`
- ✓ Summary reflects correct warning counts

**Prerequisites:**
- M9.G5.T2 completed
- Target file: `tests/audit/a11y-audit.test.ts`

**Implementation Details:**

Create `tests/audit/a11y-audit.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runA11yAudit } from '../../scripts/audit/lib/a11y-audit';

describe('axe-core Accessibility Audit Integration', () => {
  const fixturesRoot = path.join(process.cwd(), 'tests', 'audit', 'fixtures');

  it('audits passing site fixture and includes 404 page', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(fixturesRoot, 'passing-site'),
    });
    expect(layout).not.toBeNull();

    const report = await runA11yAudit(layout!);
    expect(report.status).toBe('pass');
    expect(report.summary.errors).toBe(0);

    const routesChecked = report.data?.routes.map(r => r.route);
    expect(routesChecked).toContain('/404');
    expect(routesChecked).toContain('/');
    expect(report.data?.disabledRules).toContain('color-contrast');
  });

  it('flags accessibility violations on defect fixture', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(fixturesRoot, 'defects'),
    });
    expect(layout).not.toBeNull();

    const report = await runA11yAudit(layout!);
    const buttonErrors = report.findings.filter(f => f.rule === 'button-name');
    expect(buttonErrors.length).toBeGreaterThanOrEqual(1);
    expect(report.status).toBe('fail');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/a11y-audit.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 6.2, Req 6.4, Req 6.6

---

### M9.G5.T5: Implement Skipped Execution Coverage Test

**Objective:** Write unit tests covering the graceful `skipped` fallback behavior of `runA11yAudit` if `axe-core` cannot be resolved.

**Acceptance Criteria:**
- ✓ Simulates missing `axe-core` module
- ✓ Returns report with `status: 'skipped'` and `routesChecked: 0`
- ✓ Records reason in `summary.skipped`

**Prerequisites:**
- M9.G5.T2 completed
- Target file: `tests/audit/a11y-audit-skipped.test.ts`

**Implementation Details:**

Create `tests/audit/a11y-audit-skipped.test.ts`:

```typescript
import { describe, it, expect, vi } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runA11yAudit } from '../../scripts/audit/lib/a11y-audit';

describe('axe-core Skipped Execution Fallback', () => {
  it('returns skipped status when axe-core resolution fails', async () => {
    vi.doMock('axe-core', () => {
      throw new Error('Module not found');
    });

    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(process.cwd(), 'tests', 'audit', 'fixtures', 'passing-site'),
    });

    // Run audit with mocked failure
    const report = await runA11yAudit(layout!);
    expect(report.status).toBe('skipped');
    expect(report.summary.skipped.length).toBeGreaterThan(0);

    vi.doUnmock('axe-core');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/a11y-audit-skipped.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 6.5, Req 12.8

---

### M9.G5.T6: Create Manual Accessibility Checklist Document

**Objective:** Author `docs/quality/manual-accessibility-checklist.md` documenting human verification procedures for WCAG criteria that cannot be validated in automated headless environments.

**Acceptance Criteria:**
- ✓ Contains sections for keyboard traversal, visible focus, screen readers (NVDA, VoiceOver), 200% zoom and 320 CSS px reflow, `prefers-reduced-motion`, and color contrast
- ✓ Lists standard contrast ratios: 4.5:1 for normal text, 3:1 for large text / UI borders
- ✓ Explicitly enumerates all P0 route patterns in a structured test table
- ✓ Includes required breakpoints: 375px, 768px, 1024px, and 1440px
- ✓ Clearly states that automated tools alone do not constitute WCAG conformance

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

1. Create directory `docs/quality/` if missing.
2. Create `docs/quality/manual-accessibility-checklist.md`:

```markdown
# Manual Accessibility (a11y) Verification Checklist

> **Standard:** WCAG 2.1 Level AA Compliance  
> **Status:** Active Release Requirement  
> **Reference:** TRD Section 6.5, design.md Section 5.2

---

## 1. Executive Notice
Automated accessibility checks (e.g., `axe-core`) detect approximately 30–50% of WCAG defects. Automated testing alone does NOT establish WCAG conformance. All manual inspection steps in this checklist must be performed prior to production releases.

---

## 2. Test Environment & Header Details
- **Tester Name:** _______________________
- **Date Conducted:** ____________________
- **Browser & Version:** _________________
- **Screen Reader Software & Version:**
  - [ ] NVDA (tested with Chrome or Firefox on Windows)
  - [ ] VoiceOver (tested with Safari on macOS/iOS)

---

## 3. Responsive Breakpoints Inspection
Verify responsive layout, menu disclosure, and typography measures across:
- **Mobile:** `375px`
- **Tablet:** `768px`
- **Desktop:** `1024px`
- **Wide Desktop:** `1440px`

---

## 4. Evaluation Criteria

### 4.1 Keyboard Traversal & Visible Focus
- [ ] Every interactive control (links, buttons, filter chips) is reachable using `Tab` and operable via `Enter` / `Space`.
- [ ] No keyboard traps exist. Modal/drawer states trap focus correctly when opened and release on `Escape`.
- [ ] Focus indicator is distinctly visible on every focused element using the `--color-focus-ring` token. Focus outlines are never suppressed with `outline: none` without an equivalent visual replacement.

### 4.2 Screen Reader Traversal
- [ ] Landmark navigation correctly identifies `<header>`, `<nav>`, `<main>`, and `<footer>`.
- [ ] Headings form a logical semantic tree (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`) without skips.
- [ ] Visual icons and external link indicators provide clear accessible names (e.g., "opens in new window").

### 4.3 Visual Presentation, Zoom & Reflow
- [ ] **Contrast:** Normal text satisfies at least **4.5:1** contrast ratio against its background.
- [ ] **Contrast:** Large text (18pt+ or 14pt bold) and active UI boundaries satisfy at least **3:1** contrast ratio.
- [ ] **200% Zoom:** Content remains legible and functional without loss of content when zoomed to 200%.
- [ ] **320 CSS px Reflow:** Page scrolls vertically in a single column without horizontal scrollbars at 320px viewport width.

### 4.4 Motion & Animation
- [ ] Enabling `prefers-reduced-motion` in OS/browser preferences immediately disables non-essential animations and transitions.

---

## 5. Per-Route Verification Matrix

| Route Pattern | Tested Breakpoints | Screen Reader Checked | Keyboard Focus Verified | Contrast Verified | Pass / Fail | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/` (Homepage) | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/projects` (Index) | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/projects/[slug]` | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/certifications` | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/blog` (Index) | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/blog/[slug]` | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
| `/404` (Not Found) | 375, 768, 1024, 1440 | [ ] NVDA / [ ] VoiceOver | [ ] | [ ] | [ ] PASS | |
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "docs\quality\manual-accessibility-checklist.md"
```
Expected: `True`

**Satisfies Requirements:** Req 7.1–7.5

---

### M9.G5.T7: Author Test for Manual Accessibility Checklist Completeness

**Objective:** Write `tests/audit/manual-accessibility-checklist.test.ts` to assert that all required WCAG sections, routes, breakpoints, and conformance statements are present in the documentation.

**Acceptance Criteria:**
- ✓ Verifies presence of keyboard, focus, NVDA, VoiceOver, zoom, contrast, and motion headings
- ✓ Verifies presence of all 7 P0 route patterns
- ✓ Verifies presence of 375, 768, 1024, 1440 px breakpoints
- ✓ Asserts presence of the WCAG disclaimer statement

**Prerequisites:**
- M9.G5.T6 completed
- Target file: `tests/audit/manual-accessibility-checklist.test.ts`

**Implementation Details:**

Create `tests/audit/manual-accessibility-checklist.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Manual Accessibility Checklist Documentation', () => {
  it('contains all required sections, breakpoints, and routes', async () => {
    const docPath = path.join(process.cwd(), 'docs', 'quality', 'manual-accessibility-checklist.md');
    const content = await fs.readFile(docPath, 'utf8');

    // Headings and criteria
    expect(content).toMatch(/Keyboard Traversal/i);
    expect(content).toMatch(/Visible Focus/i);
    expect(content).toMatch(/NVDA/i);
    expect(content).toMatch(/VoiceOver/i);
    expect(content).toMatch(/200% Zoom/i);
    expect(content).toMatch(/320 CSS px Reflow/i);
    expect(content).toMatch(/prefers-reduced-motion/i);
    expect(content).toMatch(/4\.5:1/);
    expect(content).toMatch(/3:1/);

    // Breakpoints
    expect(content).toMatch(/375px/);
    expect(content).toMatch(/768px/);
    expect(content).toMatch(/1024px/);
    expect(content).toMatch(/1440px/);

    // Routes
    expect(content).toMatch(/`\/`/);
    expect(content).toMatch(/`\/projects`/);
    expect(content).toMatch(/`\/projects\/\[slug\]`/);
    expect(content).toMatch(/`\/certifications`/);
    expect(content).toMatch(/`\/blog`/);
    expect(content).toMatch(/`\/blog\/\[slug\]`/);
    expect(content).toMatch(/`\/404`/);

    // Disclaimer statement
    expect(content).toMatch(/Automated testing alone does NOT establish WCAG conformance/i);
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/manual-accessibility-checklist.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 7.1–7.5

---

### M9.G5.T8: Author A11y Audit Integration and Offline Verification Test

**Objective:** Write `tests/audit/a11y-audit.integration.test.ts` proving that running `runA11yAudit` twice produces identical output and makes zero network requests.

**Acceptance Criteria:**
- ✓ Two runs over identical fixtures yield byte-identical reports (excluding `generatedAt`)
- ✓ Replaces `globalThis.fetch` with an throwing stub to prove zero network activity
- ✓ Confirms deterministic behavior across consecutive executions

**Prerequisites:**
- M9.G5.T2 completed
- Target file: `tests/audit/a11y-audit.integration.test.ts`

**Implementation Details:**

Create `tests/audit/a11y-audit.integration.test.ts`:

```typescript
import { describe, it, expect, vi } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runA11yAudit } from '../../scripts/audit/lib/a11y-audit';

describe('a11y Audit Offline & Determinism Integration', () => {
  it('executes completely offline and produces deterministic results', async () => {
    // Intercept fetch to guarantee zero network I/O
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockImplementation(() => {
      throw new Error('Network request forbidden during offline a11y audit');
    });

    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(process.cwd(), 'tests', 'audit', 'fixtures', 'passing-site'),
    });

    const run1 = await runA11yAudit(layout!);
    const run2 = await runA11yAudit(layout!);

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(run1.findings).toEqual(run2.findings);
    expect(run1.summary).toEqual(run2.summary);

    fetchSpy.mockRestore();
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/a11y-audit.integration.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.4, Req 1.5, Req 6.1

---

### M9.G5.T9: Audit and Verify Absence of Rule Suppression

**Objective:** Inspect `a11y-audit.ts` to ensure no accessibility rule is disabled without being formally declared in `DISABLED_AXE_RULES`.

**Acceptance Criteria:**
- ✓ Asserts that only `color-contrast` is disabled in the axe configuration
- ✓ Asserts that `DISABLED_AXE_RULES` contains a written justification for each disabled rule
- ✓ Ensures no route-specific rule suppression or silent ignoring exists

**Prerequisites:**
- M9.G5.T2 completed
- Target file: `scripts/audit/lib/a11y-audit.ts`

**Implementation Details:**

Create test `tests/audit/a11y-rules-integrity.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { DISABLED_AXE_RULES } from '../../scripts/audit/lib/config';

describe('A11y Rules Integrity', () => {
  it('strictly limits disabled axe rules to justified layout-engine limitations', () => {
    const keys = Object.keys(DISABLED_AXE_RULES);
    expect(keys).toEqual(['color-contrast']);

    for (const key of keys) {
      const reason = DISABLED_AXE_RULES[key];
      expect(typeof reason).toBe('string');
      expect(reason?.length).toBeGreaterThan(10);
    }
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/a11y-rules-integrity.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 6.5, Req 6.7

---

### M9.G5.T10: Milestone 9 Goal 5 Checkpoint Verification

**Objective:** Run all Goal 5 test suites, verify CLI execution over static fixtures, and confirm TypeScript and ESLint compliance with zero unapproved file modifications.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/` for Goal 5 pass cleanly
- ✓ CLI `scripts/audit/a11y.ts` executes cleanly over `AUDIT_BUILD_DIR`
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0
- ✓ `git status` verifies no modifications to `package.json` outside approved `axe-core`

**Prerequisites:**
- M9.G5.T1 through M9.G5.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G5 suites
npx vitest run tests/audit/a11y-audit.test.ts tests/audit/a11y-audit-skipped.test.ts tests/audit/manual-accessibility-checklist.test.ts tests/audit/a11y-audit.integration.test.ts tests/audit/a11y-rules-integrity.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Test CLI execution on passing fixtures
$env:AUDIT_BUILD_DIR = "tests/audit/fixtures/passing-site"
npx vite-node --config vitest.config.ts scripts/audit/a11y.ts
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

**Satisfies Requirements:** Req 1.5, Req 6.1–6.7, Req 7.1–7.5, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/a11y-audit.test.ts tests/audit/manual-accessibility-checklist.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in Goal 5 pass
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.