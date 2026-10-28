# M9.G1: Shared Audit Library, HTML Fixtures, Prerequisite Verification, and Approval Requests

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Establish the core audit infrastructure layer for Milestone 9. This goal creates the shared audit library (`scripts/audit/lib/types.ts`, `scripts/audit/lib/config.ts`, `scripts/audit/lib/report.ts`, `scripts/audit/lib/build-layout.ts`, `scripts/audit/lib/cli.ts`, `scripts/audit/lib/html.ts`, and `scripts/audit/lib/route-inventory.ts`), constructs comprehensive offline HTML fixtures under `tests/audit/fixtures/`, implements property tests for report stability, schema validity, and inventory derivation (Properties 6, 19, and 20), verifies all upstream M1/M2 prerequisites, and logs the approved Approval_Items A1–A6 into `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`.

---

## Goal Success Criteria

- ✓ `scripts/audit/lib/types.ts` exports `Severity`, `Status`, `Finding`, `AuditSummary`, `AuditReport`, `RouteKind`, and `RouteEntry` strictly typed without `any`
- ✓ `scripts/audit/lib/config.ts` exports `BUDGETS`, `SEO_LIMITS`, `LIGHTHOUSE`, `LINKS_ONLINE`, `MIN_CONTENT`, `APPROVALS` (flags defaulting to `true`), tracking and secret markers, and `DISABLED_AXE_RULES`
- ✓ `scripts/audit/lib/report.ts` provides pure comparison, stable serialization, report assembly, and filesystem export
- ✓ `scripts/audit/lib/build-layout.ts` and `scripts/audit/lib/cli.ts` resolve static build directories (`out/`, `.next/server/app/`, or `AUDIT_BUILD_DIR`) and handle standardized process exit codes (0, 1, 2)
- ✓ `scripts/audit/lib/html.ts` parses HTML via `jsdom` with scripts disabled (`outside-only`) and extracts deterministic selectors
- ✓ `tests/audit/fixtures/` contains a valid passing site tree and isolated single-defect HTML fixtures
- ✓ `scripts/audit/lib/route-inventory.ts` implements pure `buildRouteInventory` and loader-backed `loadRouteInventory`
- ✓ Fast-check Property 6 (route inventory), Property 19 (report schema validity), and Property 20 (report determinism) pass $\ge 100$ iterations
- ✓ `task-notes.md` records verified toolchain prerequisites and documents approvals A1 through A6
- ✓ Zero imports from `src/components/` exist inside `scripts/audit/` or `tests/audit/`

---

## Prerequisites

- Milestones M1 through M8 completed
- Node.js 18+ and npm installed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Existing `vitest.config.ts`, `tsconfig.json`, and M2 content loaders in `src/content/loaders/`

---

## Tasks

### M9.G1.T1: Create Shared Audit Types and Configuration

**Objective:** Define canonical TypeScript types for audit findings, summaries, and reports, and declare frozen audit configuration constants including budgets, marker patterns, and approval flags.

**Acceptance Criteria:**
- ✓ `scripts/audit/lib/types.ts` exports `Severity`, `Status`, `Finding`, `AuditSummary`, `AuditReport`, `RouteKind`, and `RouteEntry`
- ✓ `scripts/audit/lib/config.ts` exports `BUDGETS`, `SEO_LIMITS`, `LIGHTHOUSE`, `LINKS_ONLINE`, `MIN_CONTENT`, `APPROVALS`, tracking markers, secret regexes, and `DISABLED_AXE_RULES`
- ✓ All config objects are declared with `as const`
- ✓ Zero use of `any`, non-null assertions, or barrel re-exports

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

1. Create directory `scripts/audit/lib/` if missing.
2. Create `scripts/audit/lib/types.ts`:

```typescript
export type Severity = 'error' | 'warning' | 'info';
export type Status = 'pass' | 'fail' | 'skipped';

export interface Finding {
  readonly route: string;
  readonly rule: string;
  readonly message: string;
  readonly severity: Severity;
  readonly selector?: string;
  readonly file?: string;
  readonly details?: Readonly<Record<string, string | number | boolean | null>>;
}

export interface AuditSummary {
  readonly routesChecked: number;
  readonly errors: number;
  readonly warnings: number;
  readonly infos: number;
  readonly skipped: readonly string[];
}

export interface AuditReport<TData = null> {
  readonly audit: string;
  readonly generatedAt: string;
  readonly status: Status;
  readonly summary: AuditSummary;
  readonly findings: readonly Finding[];
  readonly data: TData;
}

export type RouteKind =
  | 'home'
  | 'projects-index'
  | 'project-detail'
  | 'certifications'
  | 'blog-index'
  | 'blog-detail'
  | 'not-found';

export interface RouteEntry {
  readonly path: string;
  readonly kind: RouteKind;
  readonly slug: string | null;
}
```

3. Create `scripts/audit/lib/config.ts`:

```typescript
export const BUDGETS = {
  chunkJsGzipBytes: 81_920,
  routeJsGzipBytes: 204_800,
  routeCssGzipBytes: 40_960,
  imageBytes: 307_200,
  totalBytes: 26_214_400,
  regressionTolerancePct: 5,
  buildSeconds: 180,
} as const;

export const SEO_LIMITS = {
  title: { min: 10, max: 70 },
  description: { min: 50, max: 160 },
} as const;

export const LIGHTHOUSE = {
  runs: 5,
  minScores: { accessibility: 95, performance: 90, bestPractices: 90, seo: 90 },
  maxMetrics: { lcpMs: 2500, cls: 0.1, fcpMs: 1800, tbtMs: 200 },
} as const;

export const LINKS_ONLINE = {
  timeoutMs: 10_000,
  concurrency: 4,
} as const;

export const MIN_CONTENT = {
  projects: 3,
  certifications: 1,
  publishedPosts: 1,
} as const;

export const APPROVALS = {
  jsonLdIntegration: true,
  lighthouseDependencies: true,
} as const;

export const TRACKING_HOST_MARKERS: readonly string[] = [
  'googletagmanager.com',
  'google-analytics.com',
  'analytics.google.com',
  'static.hotjar.com',
  'hotjar.com',
  'segment.com',
  'segment.io',
  'plausible.io',
  '/_vercel/insights',
  '/_vercel/speed-insights',
  'connect.facebook.net',
] as const;

export const TRACKING_CALL_MARKERS: readonly string[] = [
  'gtag(',
  'fbq(',
  'window.dataLayer',
  '_hjSettings',
] as const;

export const SECRET_PATTERNS: readonly RegExp[] = [
  /-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /ghp_[A-Za-z0-9]{36}/,
  /github_pat_[A-Za-z0-9_]{22,}/,
  /AKIA[0-9A-Z]{16}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /sk_live_[A-Za-z0-9]{16,}/,
  /AIza[0-9A-Za-z_-]{35}/,
] as const;

export const DISABLED_AXE_RULES: Readonly<Record<string, string>> = {
  'color-contrast': 'jsdom has no layout engine; verified via manual accessibility checklist',
} as const;
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/types.ts scripts/audit/lib/config.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.5, Req 1.6, Req 5.5, Req 5.7, Req 6.5, Req 11.6, Req 12.2, Req 12.3

---

### M9.G1.T2: Implement Report Generation, Sorting, and Stable Serialization

**Objective:** Implement deterministic report sorting, schema validation, stable JSON serialization, and filesystem persistence.

**Acceptance Criteria:**
- ✓ `compareFindings` enforces strict deterministic ordering by `route`, `rule`, `selector`, `file`, `message`
- ✓ `buildReport` computes correct summary counts, assigns status, and accepts an injected `now` timestamp
- ✓ `stableStringify` sorts object keys recursively with two-space indentation and trailing newline
- ✓ `validateReport` validates required report properties and confirms counts match findings
- ✓ `writeReport` creates target directory (e.g. `reports/`) automatically if missing

**Prerequisites:**
- M9.G1.T1 completed
- Target file: `scripts/audit/lib/report.ts`

**Implementation Details:**

Create `scripts/audit/lib/report.ts`:

```typescript
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import type { AuditReport, AuditSummary, Finding, Status } from './types';

export function compareFindings(a: Finding, b: Finding): number {
  if (a.route !== b.route) {
    return a.route < b.route ? -1 : 1;
  }
  if (a.rule !== b.rule) {
    return a.rule < b.rule ? -1 : 1;
  }
  const selA = a.selector ?? '';
  const selB = b.selector ?? '';
  if (selA !== selB) {
    return selA < selB ? -1 : 1;
  }
  const fileA = a.file ?? '';
  const fileB = b.file ?? '';
  if (fileA !== fileB) {
    return fileA < fileB ? -1 : 1;
  }
  if (a.message !== b.message) {
    return a.message < b.message ? -1 : 1;
  }
  return 0;
}

export function sortFindings(list: readonly Finding[]): readonly Finding[] {
  return [...list].sort(compareFindings);
}

export function stableStringify(value: unknown): string {
  function sortKeys(obj: unknown): unknown {
    if (obj === null || typeof obj !== 'object') {
      return obj;
    }
    if (Array.isArray(obj)) {
      return obj.map(sortKeys);
    }
    const record = obj as Record<string, unknown>;
    const sortedKeys = Object.keys(record).sort();
    const result: Record<string, unknown> = {};
    for (const key of sortedKeys) {
      result[key] = sortKeys(record[key]);
    }
    return result;
  }

  return JSON.stringify(sortKeys(value), null, 2) + '\n';
}

export interface BuildReportOptions<TData = null> {
  readonly audit: string;
  readonly findings: readonly Finding[];
  readonly routesChecked: number;
  readonly skipped?: readonly string[];
  readonly data?: TData;
  readonly now?: string;
}

export function buildReport<TData = null>(options: BuildReportOptions<TData>): AuditReport<TData> {
  const sorted = sortFindings(options.findings);
  let errors = 0;
  let warnings = 0;
  let infos = 0;

  for (const item of sorted) {
    if (item.severity === 'error') {
      errors++;
    } else if (item.severity === 'warning') {
      warnings++;
    } else if (item.severity === 'info') {
      infos++;
    }
  }

  const skippedList = options.skipped ?? [];
  let status: Status = 'pass';
  if (skippedList.length > 0 && options.findings.length === 0 && options.routesChecked === 0) {
    status = 'skipped';
  } else if (errors > 0) {
    status = 'fail';
  }

  const summary: AuditSummary = {
    routesChecked: options.routesChecked,
    errors,
    warnings,
    infos,
    skipped: skippedList,
  };

  return {
    audit: options.audit,
    generatedAt: options.now ?? new Date().toISOString(),
    status,
    summary,
    findings: sorted,
    data: (options.data !== undefined ? options.data : null) as TData,
  };
}

export function validateReport(value: unknown): { ok: true } | { ok: false; errors: string[] } {
  const errors: string[] = [];
  if (value === null || typeof value !== 'object') {
    return { ok: false, errors: ['Report must be a non-null object'] };
  }

  const report = value as Partial<AuditReport<unknown>>;
  if (typeof report.audit !== 'string' || report.audit.trim() === '') {
    errors.push('Missing or invalid "audit" field');
  }
  if (typeof report.generatedAt !== 'string' || isNaN(Date.parse(report.generatedAt))) {
    errors.push('Missing or invalid ISO "generatedAt" string');
  }
  if (report.status !== 'pass' && report.status !== 'fail' && report.status !== 'skipped') {
    errors.push('Invalid "status" value');
  }

  if (!report.summary || typeof report.summary !== 'object') {
    errors.push('Missing "summary" object');
  } else {
    const s = report.summary;
    if (typeof s.routesChecked !== 'number' || s.routesChecked < 0) {
      errors.push('Invalid summary.routesChecked');
    }
    if (typeof s.errors !== 'number' || s.errors < 0) {
      errors.push('Invalid summary.errors');
    }
    if (typeof s.warnings !== 'number' || s.warnings < 0) {
      errors.push('Invalid summary.warnings');
    }
    if (typeof s.infos !== 'number' || s.infos < 0) {
      errors.push('Invalid summary.infos');
    }
    if (!Array.isArray(s.skipped)) {
      errors.push('summary.skipped must be an array');
    }
  }

  if (!Array.isArray(report.findings)) {
    errors.push('findings must be an array');
  } else {
    let errCount = 0;
    let warnCount = 0;
    let infoCount = 0;

    for (let i = 0; i < report.findings.length; i++) {
      const f = report.findings[i] as Partial<Finding>;
      if (typeof f.route !== 'string' || f.route.trim() === '') {
        errors.push(`findings[${i}].route must be non-empty string`);
      }
      if (typeof f.rule !== 'string' || f.rule.trim() === '') {
        errors.push(`findings[${i}].rule must be non-empty string`);
      }
      if (typeof f.message !== 'string' || f.message.trim() === '') {
        errors.push(`findings[${i}].message must be non-empty string`);
      }
      if (f.severity === 'error') {
        errCount++;
      } else if (f.severity === 'warning') {
        warnCount++;
      } else if (f.severity === 'info') {
        infoCount++;
      } else {
        errors.push(`findings[${i}].severity must be error, warning, or info`);
      }
    }

    if (report.summary) {
      if (report.summary.errors !== errCount) {
        errors.push(`summary.errors (${report.summary.errors}) does not match findings count (${errCount})`);
      }
      if (report.summary.warnings !== warnCount) {
        errors.push(`summary.warnings (${report.summary.warnings}) does not match findings count (${warnCount})`);
      }
      if (report.summary.infos !== infoCount) {
        errors.push(`summary.infos (${report.summary.infos}) does not match findings count (${infoCount})`);
      }
      if (errCount > 0 && report.status !== 'fail') {
        errors.push('Report with error findings must have status="fail"');
      }
    }
  }

  return errors.length === 0 ? { ok: true } : { ok: false, errors };
}

export async function writeReport<TData>(report: AuditReport<TData>, dir: string = 'reports'): Promise<string> {
  await fs.mkdir(dir, { recursive: true });
  const filename = `${report.audit}.json`;
  const targetPath = path.join(dir, filename);
  const json = stableStringify(report);
  await fs.writeFile(targetPath, json, 'utf8');
  return targetPath;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/report.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.5, Req 1.6, Req 16.4, Req 16.6

---

### M9.G1.T3: Author Unit and Property Tests for Report Pipeline

**Objective:** Verify report formatting, summary computation, directory creation, and execute fast-check Property 19 and Property 20.

**Acceptance Criteria:**
- ✓ Unit tests verify status calculation (`pass`, `fail`, `skipped`)
- ✓ Unit tests confirm summary count consistency and invalid report schema rejection
- ✓ Fast-check Property 19 validates report structure across $\ge 100$ randomized finding sets
- ✓ Fast-check Property 20 validates that `buildReport` produces byte-identical serialized output regardless of finding input order

**Prerequisites:**
- M9.G1.T2 completed
- Target file: `tests/audit/report.test.ts`

**Implementation Details:**

Create `tests/audit/report.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';
import {
  compareFindings,
  sortFindings,
  stableStringify,
  buildReport,
  validateReport,
  writeReport,
} from '../../scripts/audit/lib/report';
import type { Finding, Severity } from '../../scripts/audit/lib/types';

describe('Report Helpers Unit Tests', () => {
  it('correctly assigns status fail when errors are present', () => {
    const findings: Finding[] = [
      { route: '/', rule: 'test-rule', message: 'Fail msg', severity: 'error' },
    ];
    const report = buildReport({ audit: 'unit-test', findings, routesChecked: 1, now: '2026-10-20T00:00:00.000Z' });
    expect(report.status).toBe('fail');
    expect(report.summary.errors).toBe(1);
    expect(report.summary.warnings).toBe(0);
  });

  it('correctly assigns status pass when only warnings or infos are present', () => {
    const findings: Finding[] = [
      { route: '/', rule: 'test-warn', message: 'Warn msg', severity: 'warning' },
      { route: '/', rule: 'test-info', message: 'Info msg', severity: 'info' },
    ];
    const report = buildReport({ audit: 'unit-test', findings, routesChecked: 1, now: '2026-10-20T00:00:00.000Z' });
    expect(report.status).toBe('pass');
    expect(report.summary.errors).toBe(0);
    expect(report.summary.warnings).toBe(1);
    expect(report.summary.infos).toBe(1);
  });

  it('correctly assigns status skipped when explicitly skipped without routes or findings', () => {
    const report = buildReport({
      audit: 'unit-test',
      findings: [],
      routesChecked: 0,
      skipped: ['axe-core not installed'],
      now: '2026-10-20T00:00:00.000Z',
    });
    expect(report.status).toBe('skipped');
    expect(report.summary.skipped).toContain('axe-core not installed');
  });

  it('rejects malformed reports in validateReport', () => {
    expect(validateReport(null).ok).toBe(false);
    expect(validateReport({}).ok).toBe(false);
    expect(
      validateReport({
        audit: 'test',
        generatedAt: 'invalid-date',
        status: 'pass',
        summary: { routesChecked: 1, errors: 0, warnings: 0, infos: 0, skipped: [] },
        findings: [],
        data: null,
      }).ok
    ).toBe(false);
  });

  it('creates directory and writes file in writeReport', async () => {
    const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'audit-report-'));
    try {
      const targetDir = path.join(tmpDir, 'nested', 'reports');
      const report = buildReport({ audit: 'file-test', findings: [], routesChecked: 1, now: '2026-10-20T00:00:00.000Z' });
      const filepath = await writeReport(report, targetDir);
      const content = await fs.readFile(filepath, 'utf8');
      expect(JSON.parse(content)).toEqual(report);
    } finally {
      await fs.rm(tmpDir, { recursive: true, force: true });
    }
  });
});

describe('Report Properties', () => {
  const findingArbitrary = fc.record({
    route: fc.constantFrom('/', '/projects', '/projects/test-proj', '/blog', '/404'),
    rule: fc.stringMatching(/^[a-z]+(-[a-z]+)*$/),
    message: fc.string({ minLength: 1, maxLength: 100 }),
    severity: fc.constantFrom<Severity>('error', 'warning', 'info'),
    selector: fc.option(fc.string({ minLength: 1, maxLength: 50 }), { nil: undefined }),
    file: fc.option(fc.string({ minLength: 1, maxLength: 50 }), { nil: undefined }),
  });

  // Feature: m9-quality-accessibility-performance, Property 19: Reports built from any findings are schema valid and self consistent
  it('Property 19: Reports built from any findings are schema valid and self consistent', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 20 }),
        fc.array(findingArbitrary, { maxLength: 20 }),
        fc.integer({ min: 0, max: 50 }),
        (auditName, findings, routesChecked) => {
          const report = buildReport({
            audit: auditName,
            findings,
            routesChecked,
            now: '2026-10-20T12:00:00.000Z',
          });

          const validation = validateReport(report);
          expect(validation.ok).toBe(true);

          const expectedErrors = findings.filter(f => f.severity === 'error').length;
          const expectedWarnings = findings.filter(f => f.severity === 'warning').length;
          const expectedInfos = findings.filter(f => f.severity === 'info').length;

          expect(report.summary.errors).toBe(expectedErrors);
          expect(report.summary.warnings).toBe(expectedWarnings);
          expect(report.summary.infos).toBe(expectedInfos);

          if (expectedErrors > 0) {
            expect(report.status).toBe('fail');
          } else {
            expect(report.status).toBe('pass');
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 20: Report content is deterministic and independent of finding order
  it('Property 20: Report content is deterministic and independent of finding order', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 20 }),
        fc.array(findingArbitrary, { minLength: 1, maxLength: 15 }),
        (auditName, findings) => {
          const fixedNow = '2026-10-20T12:00:00.000Z';
          const report1 = buildReport({ audit: auditName, findings, routesChecked: 5, now: fixedNow });

          // Shuffle findings
          const shuffled = [...findings].reverse();
          const report2 = buildReport({ audit: auditName, findings: shuffled, routesChecked: 5, now: fixedNow });

          expect(stableStringify(report1)).toBe(stableStringify(report2));
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/report.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS` (all unit and property tests passing)

**Satisfies Requirements:** Req 1.5, Req 16.4, Req 16.6

---

### M9.G1.T4: Implement Build Layout Detection and CLI Harness

**Objective:** Implement static layout detection (`resolveBuildLayout`), asset path resolution, filesystem reading utilities, and the standardized CLI execution harness (`runCli`).

**Acceptance Criteria:**
- ✓ `resolveBuildLayout` prioritizes `AUDIT_BUILD_DIR`, then `out/`, then `.next/server/app/`, or returns `null`
- ✓ Detects whether build uses `flat` (e.g. `blog.html`) or `directory` (e.g. `blog/index.html`) layout
- ✓ `listFiles` returns a sorted array of URL-relative paths
- ✓ `runCli` handles argument parsing, runs the audit, persists reports, outputs console summaries, and manages exit codes (0, 1, 2)
- ✓ Fails cleanly with code 2 if build layout is absent

**Prerequisites:**
- M9.G1.T2 completed
- Target files: `scripts/audit/lib/build-layout.ts`, `scripts/audit/lib/cli.ts`, `tests/audit/build-layout.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/build-layout.ts`:

```typescript
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

export interface BuildLayout {
  readonly kind: 'export' | 'next-prerender';
  readonly style: 'flat' | 'directory';
  readonly roots: ReadonlyArray<{ urlPrefix: string; dir: string }>;
}

export async function checkFileExists(filepath: string): Promise<boolean> {
  try {
    const stat = await fs.stat(filepath);
    return stat.isFile();
  } catch {
    return false;
  }
}

export async function checkDirExists(dirpath: string): Promise<boolean> {
  try {
    const stat = await fs.stat(dirpath);
    return stat.isDirectory();
  } catch {
    return false;
  }
}

export async function resolveBuildLayout(
  env: NodeJS.ProcessEnv = process.env,
  cwd: string = process.cwd()
): Promise<BuildLayout | null> {
  // 1. Explicit environment override
  if (env.AUDIT_BUILD_DIR) {
    const customDir = path.isAbsolute(env.AUDIT_BUILD_DIR)
      ? env.AUDIT_BUILD_DIR
      : path.join(cwd, env.AUDIT_BUILD_DIR);
    if (await checkDirExists(customDir)) {
      const hasFlat = await checkFileExists(path.join(customDir, 'projects.html'));
      const hasDir = await checkFileExists(path.join(customDir, 'projects', 'index.html'));
      const style = hasDir && !hasFlat ? 'directory' : 'flat';
      return {
        kind: 'export',
        style,
        roots: [{ urlPrefix: '', dir: customDir }],
      };
    }
  }

  // 2. Standard next export directory (out/)
  const outDir = path.join(cwd, 'out');
  if (await checkFileExists(path.join(outDir, 'index.html'))) {
    const hasFlat = await checkFileExists(path.join(outDir, 'projects.html'));
    const hasDir = await checkFileExists(path.join(outDir, 'projects', 'index.html'));
    const style = hasDir && !hasFlat ? 'directory' : 'flat';
    return {
      kind: 'export',
      style,
      roots: [{ urlPrefix: '', dir: outDir }],
    };
  }

  // 3. Next.js prerender server fallback
  const nextAppServer = path.join(cwd, '.next', 'server', 'app');
  const nextStatic = path.join(cwd, '.next', 'static');
  const publicDir = path.join(cwd, 'public');

  if ((await checkFileExists(path.join(nextAppServer, 'index.html'))) && (await checkDirExists(nextStatic))) {
    return {
      kind: 'next-prerender',
      style: 'flat',
      roots: [
        { urlPrefix: '/_next/static', dir: nextStatic },
        { urlPrefix: '/images', dir: path.join(publicDir, 'images') },
        { urlPrefix: '/files', dir: path.join(publicDir, 'files') },
        { urlPrefix: '', dir: nextAppServer },
      ],
    };
  }

  return null;
}

export async function listFiles(layout: BuildLayout): Promise<readonly string[]> {
  const result = new Set<string>();

  for (const root of layout.roots) {
    if (!(await checkDirExists(root.dir))) {
      continue;
    }
    const stack = [''];
    while (stack.length > 0) {
      const relative = stack.pop()!;
      const currentDir = path.join(root.dir, relative);
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const entryRelative = relative === '' ? entry.name : `${relative}/${entry.name}`;
        if (entry.isDirectory()) {
          stack.push(entryRelative);
        } else if (entry.isFile()) {
          const urlPath = root.urlPrefix === ''
            ? `/${entryRelative.replace(/\\/g, '/')}`
            : `${root.urlPrefix}/${entryRelative.replace(/\\/g, '/')}`;
          result.add(urlPath);
        }
      }
    }
  }

  return [...result].sort();
}

export async function readBytes(layout: BuildLayout, urlPath: string): Promise<Uint8Array | null> {
  const cleanUrl = urlPath.startsWith('/') ? urlPath : `/${urlPath}`;
  for (const root of layout.roots) {
    if (root.urlPrefix === '' || cleanUrl.startsWith(`${root.urlPrefix}/`)) {
      const relPart = root.urlPrefix === ''
        ? cleanUrl.slice(1)
        : cleanUrl.slice(root.urlPrefix.length + 1);
      const filePath = path.join(root.dir, path.normalize(relPart));
      try {
        const buf = await fs.readFile(filePath);
        return new Uint8Array(buf);
      } catch {
        continue;
      }
    }
  }
  return null;
}

export async function readText(layout: BuildLayout, urlPath: string): Promise<string | null> {
  const bytes = await readBytes(layout, urlPath);
  if (!bytes) {
    return null;
  }
  return new TextDecoder('utf-8').decode(bytes);
}
```

2. Create `scripts/audit/lib/cli.ts`:

```typescript
import { resolveBuildLayout, type BuildLayout } from './build-layout';
import { writeReport } from './report';
import type { AuditReport } from './types';

export type AuditRunner<TData = null> = (layout: BuildLayout, args: readonly string[]) => Promise<AuditReport<TData>>;

export async function runCli<TData = null>(auditName: string, runner: AuditRunner<TData>): Promise<void> {
  const args = process.argv.slice(2);
  const layout = await resolveBuildLayout();

  if (!layout) {
    process.stderr.write('Build output not found. Run npm run build first.\n');
    process.exit(2);
  }

  try {
    const report = await runner(layout, args);
    const reportPath = await writeReport(report);
    const summary = report.summary;

    const statusLabel = report.status.toUpperCase();
    const message = `[${auditName}] ${statusLabel} - Errors: ${summary.errors}, Warnings: ${summary.warnings}, Infos: ${summary.infos} (Report: ${reportPath})\n`;
    process.stdout.write(message);

    if (report.status === 'fail') {
      process.exitCode = 1;
    } else {
      process.exitCode = 0;
    }
  } catch (error) {
    process.stderr.write(`Error running audit ${auditName}: ${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(2);
  }
}
```

3. Create `tests/audit/build-layout.test.ts`:

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';
import { resolveBuildLayout, listFiles, readText } from '../../scripts/audit/lib/build-layout';

describe('Build Layout Detection Tests', () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'build-layout-'));
  });

  afterEach(async () => {
    await fs.rm(tmpDir, { recursive: true, force: true });
  });

  it('resolves layout from AUDIT_BUILD_DIR override', async () => {
    const exportDir = path.join(tmpDir, 'custom-out');
    await fs.mkdir(exportDir, { recursive: true });
    await fs.writeFile(path.join(exportDir, 'index.html'), '<html></html>', 'utf8');
    await fs.writeFile(path.join(exportDir, 'projects.html'), '<html></html>', 'utf8');

    const layout = await resolveBuildLayout({ AUDIT_BUILD_DIR: exportDir }, tmpDir);
    expect(layout).not.toBeNull();
    expect(layout?.kind).toBe('export');
    expect(layout?.style).toBe('flat');

    const files = await listFiles(layout!);
    expect(files).toContain('/index.html');
    expect(files).toContain('/projects.html');

    const content = await readText(layout!, '/index.html');
    expect(content).toBe('<html></html>');
  });

  it('detects directory style when subpages are inside index folders', async () => {
    const exportDir = path.join(tmpDir, 'dir-out');
    await fs.mkdir(path.join(exportDir, 'projects'), { recursive: true });
    await fs.writeFile(path.join(exportDir, 'index.html'), '<html></html>', 'utf8');
    await fs.writeFile(path.join(exportDir, 'projects', 'index.html'), '<html></html>', 'utf8');

    const layout = await resolveBuildLayout({ AUDIT_BUILD_DIR: exportDir }, tmpDir);
    expect(layout?.style).toBe('directory');
  });

  it('returns null when no build output exists', async () => {
    const layout = await resolveBuildLayout({}, tmpDir);
    expect(layout).toBeNull();
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/build-layout.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.5, Req 16.4

---

### M9.G1.T5: Implement JSDOM Page Parser and Stable Selector Extraction

**Objective:** Create pure HTML parsing utilities leveraging `jsdom` with script execution strictly disabled (`runScripts: 'outside-only'`), extracting deterministic CSS selectors and element ID collections.

**Acceptance Criteria:**
- ✓ `parsePage` constructs `ParsedPage` with isolated JSDOM instance
- ✓ Document scripts are never executed
- ✓ `selectorFor` returns stable structural selectors (utilizing unique `#id` shortcut or tag nth-of-type chains)
- ✓ `collectIds` extracts a set of all unique ID attributes from the document

**Prerequisites:**
- M9.G1.T4 completed
- Target files: `scripts/audit/lib/html.ts`, `tests/audit/html.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/html.ts`:

```typescript
import { JSDOM } from 'jsdom';
import type { RouteEntry } from './types';

export interface ParsedPage {
  readonly route: RouteEntry;
  readonly file: string;
  readonly html: string;
  readonly document: Document;
  readonly dom: JSDOM;
}

export function parsePage(route: RouteEntry, file: string, html: string): ParsedPage {
  const dom = new JSDOM(html, {
    url: `http://audit.local${route.path}`,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
  });

  return {
    route,
    file,
    html,
    document: dom.window.document,
    dom,
  };
}

export function collectIds(document: Document): ReadonlySet<string> {
  const elements = document.querySelectorAll('[id]');
  const ids = new Set<string>();
  for (const el of Array.from(elements)) {
    const id = el.getAttribute('id');
    if (id && id.trim() !== '') {
      ids.add(id.trim());
    }
  }
  return ids;
}

export function selectorFor(el: Element): string {
  if (el.tagName.toLowerCase() === 'html') {
    return 'html';
  }
  if (el.tagName.toLowerCase() === 'body') {
    return 'html > body';
  }

  const id = el.getAttribute('id');
  if (id && id.trim() !== '') {
    const doc = el.ownerDocument;
    if (doc) {
      const matches = doc.querySelectorAll(`[id="${CSS.escape(id.trim())}"]`);
      if (matches.length === 1) {
        return `#${id.trim()}`;
      }
    }
  }

  const parent = el.parentElement;
  if (!parent) {
    return el.tagName.toLowerCase();
  }

  const siblings = Array.from(parent.children).filter(
    sibling => sibling.tagName.toLowerCase() === el.tagName.toLowerCase()
  );

  const tagName = el.tagName.toLowerCase();
  if (siblings.length === 1) {
    return `${selectorFor(parent)} > ${tagName}`;
  }

  const index = siblings.indexOf(el) + 1;
  return `${selectorFor(parent)} > ${tagName}:nth-of-type(${index})`;
}
```

2. Create `tests/audit/html.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { parsePage, selectorFor, collectIds } from '../../scripts/audit/lib/html';
import type { RouteEntry } from '../../scripts/audit/lib/types';

describe('HTML Parsing and Selector Utilities', () => {
  const dummyRoute: RouteEntry = { path: '/', kind: 'home', slug: null };

  it('does not execute scripts when parsing page', () => {
    const html = `
      <!DOCTYPE html>
      <html>
        <body>
          <script>window.pwned = true;</script>
          <div id="target">Content</div>
        </body>
      </html>
    `;
    const parsed = parsePage(dummyRoute, 'index.html', html);
    const win = parsed.dom.window as unknown as { pwned?: boolean };
    expect(win.pwned).toBeUndefined();
    expect(parsed.document.getElementById('target')?.textContent).toBe('Content');
  });

  it('collects all element IDs', () => {
    const html = `
      <html>
        <body>
          <h1 id="title">Header</h1>
          <section id="main-content">
            <p id="para">Text</p>
          </section>
        </body>
      </html>
    `;
    const parsed = parsePage(dummyRoute, 'index.html', html);
    const ids = collectIds(parsed.document);
    expect(ids.has('title')).toBe(true);
    expect(ids.has('main-content')).toBe(true);
    expect(ids.has('para')).toBe(true);
    expect(ids.size).toBe(3);
  });

  it('generates unique #id selector when ID is unique', () => {
    const html = `
      <html>
        <body>
          <div id="unique-box"><span>Hello</span></div>
        </body>
      </html>
    `;
    const parsed = parsePage(dummyRoute, 'index.html', html);
    const el = parsed.document.getElementById('unique-box')!;
    expect(selectorFor(el)).toBe('#unique-box');
  });

  it('generates tag and nth-of-type selector when ID is duplicated or absent', () => {
    const html = `
      <html>
        <body>
          <div id="dup">First</div>
          <div id="dup">Second</div>
        </body>
      </html>
    `;
    const parsed = parsePage(dummyRoute, 'index.html', html);
    const divs = parsed.document.querySelectorAll('#dup');
    expect(selectorFor(divs[0]!)).toBe('html > body > div:nth-of-type(1)');
    expect(selectorFor(divs[1]!)).toBe('html > body > div:nth-of-type(2)');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/html.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.5, Req 3.1, Req 3.8, Req 3.9

---

### M9.G1.T6: Scaffold Offline Static HTML Audit Fixture Trees

**Objective:** Create self-contained, offline static HTML fixtures under `tests/audit/fixtures/` representing both a valid compliant build and individual defective variants.

**Acceptance Criteria:**
- ✓ `tests/audit/fixtures/passing-site/` contains `index.html`, `projects.html`, `projects/sample.html`, `certifications.html`, `blog.html`, `blog/sample.html`, and `404.html`
- ✓ `tests/audit/fixtures/defects/` contains single-issue HTML fixtures: `two-h1.html`, `skipped-heading.html`, `empty-link.html`, `missing-alt.html`, `broken-hash.html`, `tracking-gtag.html`, `external-http.html`, `blank-no-rel.html`, `duplicate-id.html`, and `unlabeled-button.html`
- ✓ All fixtures are completely static with no remote network assets

**Prerequisites:**
- M9.G1.T5 completed
- Target folder: `tests/audit/fixtures/`

**Implementation Details:**

Run PowerShell script to populate fixture trees:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$passingDir = "tests\audit\fixtures\passing-site"
$defectsDir = "tests\audit\fixtures\defects"
New-Item -ItemType Directory -Force -Path $passingDir | Out-Null
New-Item -ItemType Directory -Force -Path $defectsDir | Out-Null
New-Item -ItemType Directory -Force -Path "$passingDir\projects" | Out-Null
New-Item -ItemType Directory -Force -Path "$passingDir\blog" | Out-Null

# 1. Base passing template
$passHome = @'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Angelo Andres | Software Architect & Systems Lead</title>
    <meta name="description" content="Personal portfolio and verified technical documentation of Angelo Andres." />
    <link rel="canonical" href="https://example.com/" />
    <meta property="og:title" content="Angelo Andres | Software Architect" />
    <meta property="og:description" content="Personal portfolio and verified technical documentation of Angelo Andres." />
    <meta property="og:url" content="https://example.com/" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Angelo Andres" />
  </head>
  <body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header><nav><a href="/">Home</a><a href="/projects">Projects</a><a href="/blog">Blog</a></nav></header>
    <main id="main-content">
      <h1>Angelo Andres</h1>
      <h2>Profile Overview</h2>
      <p>Engineering systems and technical specifications.</p>
      <a href="https://github.com/example" target="_blank" rel="noopener noreferrer">GitHub Profile</a>
    </main>
    <footer><p>&copy; 2026 Angelo Andres</p></footer>
  </body>
</html>
'@
Set-Content -Path "$passingDir\index.html" -Value $passHome -Encoding UTF8
Set-Content -Path "$passingDir\projects.html" -Value ($passHome -replace "<h1>Angelo Andres</h1>", "<h1>Projects</h1>") -Encoding UTF8
Set-Content -Path "$passingDir\projects\sample.html" -Value ($passHome -replace "<h1>Angelo Andres</h1>", "<h1>Sample Project</h1>") -Encoding UTF8
Set-Content -Path "$passingDir\certifications.html" -Value ($passHome -replace "<h1>Angelo Andres</h1>", "<h1>Certifications</h1>") -Encoding UTF8
Set-Content -Path "$passingDir\blog.html" -Value ($passHome -replace "<h1>Angelo Andres</h1>", "<h1>Blog</h1>") -Encoding UTF8
Set-Content -Path "$passingDir\blog\sample.html" -Value ($passHome -replace "<h1>Angelo Andres</h1>", "<h1>Sample Post</h1>") -Encoding UTF8

$notfoundHtml = @'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Page Not Found | 404</title>
    <meta name="robots" content="noindex" />
  </head>
  <body>
    <header><nav><a href="/">Home</a></nav></header>
    <main><h1>404 - Not Found</h1><p>Page could not be located.</p></main>
    <footer><p>&copy; 2026</p></footer>
  </body>
</html>
'@
Set-Content -Path "$passingDir\404.html" -Value $notfoundHtml -Encoding UTF8

# 2. Defect Fixtures
Set-Content -Path "$defectsDir\two-h1.html" -Value ($passHome -replace "<h2>Profile Overview</h2>", "<h1>Second H1</h1>") -Encoding UTF8
Set-Content -Path "$defectsDir\skipped-heading.html" -Value ($passHome -replace "<h2>Profile Overview</h2>", "<h4>Skipped Heading</h4>") -Encoding UTF8
Set-Content -Path "$defectsDir\empty-link.html" -Value ($passHome -replace '>GitHub Profile<', '><') -Encoding UTF8
Set-Content -Path "$defectsDir\missing-alt.html" -Value ($passHome -replace '<p>Engineering', '<img src="/test.png" /><p>Engineering') -Encoding UTF8
Set-Content -Path "$defectsDir\broken-hash.html" -Value ($passHome -replace 'href="#main-content"', 'href="#missing-target"') -Encoding UTF8
Set-Content -Path "$defectsDir\tracking-gtag.html" -Value ($passHome -replace '</head>', '<script src="https://www.googletagmanager.com/gtag.js"></script></head>') -Encoding UTF8
Set-Content -Path "$defectsDir\external-http.html" -Value ($passHome -replace 'https://github.com', 'http://github.com') -Encoding UTF8
Set-Content -Path "$defectsDir\blank-no-rel.html" -Value ($passHome -replace 'rel="noopener noreferrer"', '') -Encoding UTF8
Set-Content -Path "$defectsDir\duplicate-id.html" -Value ($passHome -replace '<footer>', '<footer id="main-content">') -Encoding UTF8
Set-Content -Path "$defectsDir\unlabeled-button.html" -Value ($passHome -replace '</main>', '<button></button></main>') -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$passFiles = Get-ChildItem "tests\audit\fixtures\passing-site" -Recurse -File
$defectFiles = Get-ChildItem "tests\audit\fixtures\defects" -File
if ($passFiles.Count -ge 7 -and $defectFiles.Count -ge 10) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.4, Req 1.5, Req 3.2, Req 3.4, Req 3.6, Req 3.7, Req 3.8, Req 4.3, Req 5.1, Req 5.2, Req 5.5

---

### M9.G1.T7: Implement Route Inventory Builder and Verify Property 6

**Objective:** Implement the pure route inventory builder and runtime loader, and verify fast-check Property 6 (route inventory matches content derivation and excludes drafts).

**Acceptance Criteria:**
- ✓ `buildRouteInventory` generates exact canonical P0 routes (`/`, `/projects`, `/certifications`, `/blog`, `/404`, and slugs)
- ✓ Draft blog posts are strictly excluded from generated routes
- ✓ Result is lexicographically sorted and contains zero duplicate routes
- ✓ `loadRouteInventory` connects to M2 content loaders
- ✓ Fast-check Property 6 passes with $\ge 100$ runs

**Prerequisites:**
- M9.G1.T5 completed
- Target files: `scripts/audit/lib/route-inventory.ts`, `tests/audit/route-inventory.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/route-inventory.ts`:

```typescript
import type { RouteEntry } from './types';
import { getProjects } from '../../src/content/loaders/projects';
import { getBlogPosts } from '../../src/content/loaders/blog';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

export interface InventorySource {
  readonly projects: readonly { readonly slug: string }[];
  readonly posts: readonly { readonly slug: string; readonly draft: boolean }[];
}

export function buildRouteInventory(source: InventorySource): readonly RouteEntry[] {
  const routes: RouteEntry[] = [
    { path: '/', kind: 'home', slug: null },
    { path: '/projects', kind: 'projects-index', slug: null },
    { path: '/certifications', kind: 'certifications', slug: null },
    { path: '/blog', kind: 'blog-index', slug: null },
    { path: '/404', kind: 'not-found', slug: null },
  ];

  for (const proj of source.projects) {
    routes.push({
      path: `/projects/${proj.slug}`,
      kind: 'project-detail',
      slug: proj.slug,
    });
  }

  for (const post of source.posts) {
    if (!post.draft) {
      routes.push({
        path: `/blog/${post.slug}`,
        kind: 'blog-detail',
        slug: post.slug,
      });
    }
  }

  // Deduplicate and sort by path code-unit order
  const uniqueMap = new Map<string, RouteEntry>();
  for (const r of routes) {
    if (!uniqueMap.has(r.path)) {
      uniqueMap.set(r.path, r);
    }
  }

  return Array.from(uniqueMap.values()).sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
}

export async function loadRouteInventory(): Promise<{ routes: readonly RouteEntry[]; draftSlugs: readonly string[] }> {
  const projects = await getProjects();
  const publishedPosts = await getBlogPosts();

  // Read draft blog posts directly from content files
  const blogDir = path.join(process.cwd(), 'content', 'blog');
  const draftSlugs: string[] = [];

  try {
    const files = await fs.readdir(blogDir);
    for (const file of files) {
      if (file.endsWith('.mdx') || file.endsWith('.md')) {
        const fullPath = path.join(blogDir, file);
        const text = await fs.readFile(fullPath, 'utf8');
        if (/draft:\s*true/i.test(text)) {
          const slugMatch = text.match(/slug:\s*["']?([a-z0-9-]+)["']?/i);
          if (slugMatch && slugMatch[1]) {
            draftSlugs.push(slugMatch[1]);
          } else {
            const fallbackSlug = file.replace(/\.(mdx|md)$/, '');
            draftSlugs.push(fallbackSlug);
          }
        }
      }
    }
  } catch {
    // If directory not present or unreadable, drafts list remains empty
  }

  const postsSource: Array<{ slug: string; draft: boolean }> = [
    ...publishedPosts.map(p => ({ slug: p.slug, draft: false })),
    ...draftSlugs.map(slug => ({ slug, draft: true })),
  ];

  const routes = buildRouteInventory({
    projects: projects.map(p => ({ slug: p.slug })),
    posts: postsSource,
  });

  return { routes, draftSlugs };
}
```

2. Create `tests/audit/route-inventory.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { buildRouteInventory, type InventorySource } from '../../scripts/audit/lib/route-inventory';

describe('Route Inventory Builder Properties', () => {
  // Feature: m9-quality-accessibility-performance, Property 6: Route inventory equals the content it was derived from
  it('Property 6: Route inventory equals the content it was derived from', () => {
    const slugArb = fc.stringMatching(/^[a-z0-9]+(-[a-z0-9]+)*$/);

    fc.assert(
      fc.property(
        fc.uniqueArray(slugArb, { minLength: 0, maxLength: 10 }),
        fc.uniqueArray(
          fc.record({
            slug: slugArb,
            draft: fc.boolean(),
          }),
          { comparator: (a, b) => a.slug === b.slug, minLength: 0, maxLength: 10 }
        ),
        (projectSlugs, posts) => {
          const source: InventorySource = {
            projects: projectSlugs.map(s => ({ slug: s })),
            posts,
          };

          const inventory = buildRouteInventory(source);
          const paths = inventory.map(r => r.path);

          // 1. Mandatory core routes
          expect(paths).toContain('/');
          expect(paths).toContain('/projects');
          expect(paths).toContain('/certifications');
          expect(paths).toContain('/blog');
          expect(paths).toContain('/404');

          // 2. All projects present
          for (const s of projectSlugs) {
            expect(paths).toContain(`/projects/${s}`);
          }

          // 3. Only non-draft posts present
          for (const post of posts) {
            if (post.draft) {
              expect(paths).not.toContain(`/blog/${post.slug}`);
            } else {
              expect(paths).toContain(`/blog/${post.slug}`);
            }
          }

          // 4. Sorted and unique
          const sortedPaths = [...paths].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
          expect(paths).toEqual(sortedPaths);
          expect(new Set(paths).size).toBe(paths.length);
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/route-inventory.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.4

---

### M9.G1.T8: Audit and Document Upstream Toolchain Prerequisites

**Objective:** Inspect and verify local development environment prerequisites (Vite node execution, TypeScript aliases, static export settings in Next.js config) and record outcomes in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Checks if `vite-node` is executable via `npx vite-node -v`
- ✓ Confirms `jsdom` and `fast-check` are available in `node_modules`
- ✓ Validates that Next.js configuration specifies `output: 'export'`
- ✓ Documents all checked prerequisite states in `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Prerequisites:**
- M9.G1.T7 completed
- Target file: `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Implementation Details:**

Execute prerequisite audit script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notesPath = "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md"
if (-not (Test-Path "..\.kiro\specs\m9-quality-accessibility-performance")) {
    New-Item -ItemType Directory -Force -Path "..\.kiro\specs\m9-quality-accessibility-performance" | Out-Null
}

$viteNodeVer = (npx vite-node -v) 2>&1
$jsdomExists = Test-Path "node_modules\jsdom"
$fastCheckExists = Test-Path "node_modules\fast-check"

$nextCfg = Get-Content "next.config.ts" -Raw
$isExport = $nextCfg -match "output:\s*['""]export['""]"

$prereqLog = @"
# Task Notes & Prerequisite Audit Log - Milestone 9

## Prerequisite Audit Check (Completed M9.G1.T8)
- **vite-node status:** Available ($viteNodeVer)
- **jsdom installed:** $jsdomExists
- **fast-check installed:** $fastCheckExists
- **Next.js static export (output: 'export'):** $isExport (Build output directory: `out/`)
- **Node Environment:** $(node -v)
- **npm Version:** $(npm -v)

"@

Set-Content -Path $notesPath -Value $prereqLog -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" | Select-String "Prerequisite Audit Check"
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 18.6

---

### M9.G1.T9: Record Approvals A1 Through A6 in Task Notes

**Objective:** Formally log the recorded Approvals A1 through A6 (Approved 2026-10-22) into `task-notes.md`, including dependency specs, diff limits, and architectural decisions.

**Acceptance Criteria:**
- ✓ Appends documentation for approvals A1 through A6 to `task-notes.md`
- ✓ Documents purpose, maintenance status, and exact version requirements for dependencies
- ✓ Confirms Decision 8 (not-found robots meta exemption) and Decision 5b (Build output is `out/`)
- ✓ Confirms total deploy budget of 25 MB with planned re-check

**Prerequisites:**
- M9.G1.T8 completed
- Target file: `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Implementation Details:**

Append the approval record to `task-notes.md`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md"

$approvalsLog = @'

## Approval Items Log (Approved 2026-10-22)

| Approval ID | Scope | Status | Notes & Constraints |
| :--- | :--- | :--- | :--- |
| **A1** | Add `audit:*` scripts to `package.json` | Approved | Uses `vite-node --config vitest.config.ts` |
| **A2** | Add `axe-core` devDependency | Approved | Exact pin; used exclusively in jsdom audit |
| **A3** | Add `lighthouse` & `chrome-launcher` devDeps | Approved | Exact pin; runs against local static server |
| **A4** | Add `reports/` to `.gitignore` | Approved | Keeps audit JSON reports out of git history |
| **A5** | Minimal JSON-LD integration in 3 pages | Approved | Limited strictly to imports and `<JsonLd />` tag |
| **A6** | Update `package-lock.json` | Approved | Deterministic lockfile update for A2/A3 |

### Architectural Confirmations:
- **Decision 8:** Not-found page (`/404`) requires title, viewport, and `noindex`. It is exempt from canonical, Open Graph, and description uniqueness.
- **Decision 5b:** Build output directory is `out/` based on M1 `output: 'export'`.
- **Decision 7:** Bare tracking words matched as hosts or call expressions to prevent false positives.
- **Budget Decision:** Total deployment budget confirmed at 25 MB.
'@

Add-Content -Path $notesPath -Value $approvalsLog -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$content = Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" -Raw
if ($content -match "Approval Items Log \(Approved 2026-10-22\)" -and $content -match "Decision 8") { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.7, Req 12.8, Req 16.8, Req 18.6

---

### M9.G1.T10: Milestone 9 Goal 1 Checkpoint Verification

**Objective:** Execute the entire test suite for Goal 1, confirm type-safety, and verify that no unauthorized component imports or configuration edits were made.

**Acceptance Criteria:**
- ✓ All unit and property tests in `tests/audit/` pass cleanly
- ✓ `npm run typecheck` passes with zero errors
- ✓ `npm run lint` passes with zero errors
- ✓ Zero imports from `src/components/` exist inside `scripts/audit/` or `tests/audit/`
- ✓ Git status confirms zero unapproved modifications to `package.json`, lockfile, or `next.config.ts`

**Prerequisites:**
- M9.G1.T1 through M9.G1.T9 completed

**Implementation Details:**

Execute checkpoint validation script:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Check for illegal component imports
$illegalImports = Get-ChildItem -Path scripts/audit, tests/audit -Recurse -Include *.ts, *.tsx |
  Select-String -Pattern "from\s+['""].*components/"

if ($illegalImports) {
    Write-Error "Illegal import from components found: $illegalImports"
    exit 1
}

# 2. Run Vitest on M9.G1 suites
npx vitest run tests/audit/report.test.ts tests/audit/build-layout.test.ts tests/audit/html.test.ts tests/audit/route-inventory.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. Static typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Linter
npm run lint
if ($LASTEXITCODE -ne 0) { exit 1 }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git status --porcelain package.json package-lock.json next.config.ts .gitignore
if ($diff.Length -eq 0) { "PASS" } else { "FAIL: Unapproved modified files detected" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.6, Req 16.9, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in `tests/audit/` pass (including Properties 6, 19, and 20)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.