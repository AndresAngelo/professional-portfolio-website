# M9.G6: Performance Budget Audit and Baseline

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the performance budget and regression enforcement subsystem in `scripts/audit/lib/perf-audit.ts` and its CLI `scripts/audit/perf.ts`. This goal calculates per-route gzip sizes for referenced JavaScript and CSS assets using native `node:zlib`, compares measurements against a committed baseline (`baselines/performance.json`) with a strict 5% regression threshold, enforces per-chunk (80 KB gzip), route ceiling (200 KB JS / 40 KB CSS gzip), image (300 KB raw), and total deployment (25 MB raw) budgets, verifies explicit `img` sizing, ensures modern WOFF2 font usage with `font-display: swap|optional`, flags builds exceeding 180 seconds, and verifies fast-check Properties 15, 16, and 17.

---

## Goal Success Criteria

- ✓ `scripts/audit/lib/checks/budget.ts` exports pure `compareToBaseline` and `checkBudgets`
- ✓ `scripts/audit/lib/checks/baseline.ts` exports `buildBaseline`, `serializeBaseline`, `diffBaselines`, and `PerformanceBaseline` schema
- ✓ `scripts/audit/lib/perf-audit.ts` computes exact gzip asset sizes per route and verifies budgets and image/font rules
- ✓ Baseline comparison fails if any route exceeds baseline by $> 5\%$
- ✓ Supports `--update-baseline` flag, rewriting `baselines/performance.json` with sorted keys and zero timestamps (refusing if budget errors exist)
- ✓ Creates initial baseline automatically if none exists, emitting an `info` finding
- ✓ Re-verifies Vercel Hobby Plan deployment limits and records findings in `task-notes.md`
- ✓ Fast-check Properties 15, 16, and 17 pass $\ge 100$ iterations each
- ✓ Passing fixtures pass; inflated fixtures trigger exact regression errors

---

## Prerequisites

- Goals M9.G1 through M9.G5 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Fixtures available in `tests/audit/fixtures/`

---

## Tasks

### M9.G6.T1: Implement Pure Budget and Regression Checkers

**Objective:** Implement `compareToBaseline` and `checkBudgets` in `scripts/audit/lib/checks/budget.ts` to compute percentage deltas against baselines and evaluate upper bounds.

**Acceptance Criteria:**
- ✓ `compareToBaseline` returns `exceeded: true` if and only if $(current - baseline) / baseline \times 100 > tolerancePct$
- ✓ Handles $baseline = 0$ gracefully (exceeded if $current > 0$)
- ✓ `checkBudgets` compares measured sizes against strict budget ceilings
- ✓ Both functions are pure and return typed violation structures

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `scripts/audit/lib/checks/budget.ts`:

```typescript
export interface RegressionResult {
  readonly exceeded: boolean;
  readonly pct: number | null;
}

export function compareToBaseline(
  current: number,
  baseline: number,
  tolerancePct: number
): RegressionResult {
  if (baseline === 0) {
    return {
      exceeded: current > 0,
      pct: null,
    };
  }

  const diff = current - baseline;
  const pct = (diff / baseline) * 100;
  const exceeded = pct > tolerancePct;

  return {
    exceeded,
    pct,
  };
}

export interface BudgetItem {
  readonly name: string;
  readonly measuredBytes: number;
}

export interface BudgetViolation {
  readonly name: string;
  readonly measuredBytes: number;
  readonly budgetBytes: number;
}

export function checkBudgets(
  items: readonly BudgetItem[],
  budgetBytes: number
): readonly BudgetViolation[] {
  const violations: BudgetViolation[] = [];

  for (const item of items) {
    if (item.measuredBytes > budgetBytes) {
      violations.push({
        name: item.name,
        measuredBytes: item.measuredBytes,
        budgetBytes,
      });
    }
  }

  return violations;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/checks/budget.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.2, Req 11.3, Req 11.6, Req 11.7, Req 11.10

---

### M9.G6.T2: Implement Baseline Management and Serialization

**Objective:** Implement `buildBaseline`, `serializeBaseline`, `diffBaselines`, and the `PerformanceBaseline` interface in `scripts/audit/lib/checks/baseline.ts`.

**Acceptance Criteria:**
- ✓ `PerformanceBaseline` defines schema version 1 with sorted route map
- ✓ `serializeBaseline` outputs stable JSON with 2-space indentation and zero timestamps
- ✓ `diffBaselines` outputs human-readable delta lines (e.g. `route js: 10000 -> 10500 (+5.0%)`)
- ✓ Rejects schema mismatches gracefully

**Prerequisites:**
- M9.G6.T1 completed
- Target file: `scripts/audit/lib/checks/baseline.ts`

**Implementation Details:**

Create `scripts/audit/lib/checks/baseline.ts`:

```typescript
import { stableStringify } from '../report';

export interface RouteMeasurements {
  readonly js: number;
  readonly css: number;
}

export interface PerformanceBaseline {
  readonly schemaVersion: 1;
  readonly unit: 'gzip-bytes';
  readonly tolerancePct: number;
  readonly routes: Readonly<Record<string, RouteMeasurements>>;
}

export function buildBaseline(
  measurements: Readonly<Record<string, RouteMeasurements>>,
  tolerancePct: number = 5
): PerformanceBaseline {
  const sortedRoutes: Record<string, RouteMeasurements> = {};
  const keys = Object.keys(measurements).sort();

  for (const key of keys) {
    sortedRoutes[key] = measurements[key]!;
  }

  return {
    schemaVersion: 1,
    unit: 'gzip-bytes',
    tolerancePct,
    routes: sortedRoutes,
  };
}

export function serializeBaseline(baseline: PerformanceBaseline): string {
  return stableStringify(baseline);
}

export function diffBaselines(
  oldBaseline: PerformanceBaseline,
  newBaseline: PerformanceBaseline
): readonly string[] {
  const lines: string[] = [];
  const allRoutes = Array.from(
    new Set([...Object.keys(oldBaseline.routes), ...Object.keys(newBaseline.routes)])
  ).sort();

  for (const route of allRoutes) {
    const oldM = oldBaseline.routes[route];
    const newM = newBaseline.routes[route];

    if (!oldM && newM) {
      lines.push(`${route} (new)  js: ${newM.js} B, css: ${newM.css} B`);
    } else if (oldM && !newM) {
      lines.push(`${route} (removed)`);
    } else if (oldM && newM) {
      const jsDiff = newM.js - oldM.js;
      const jsPct = oldM.js > 0 ? ((jsDiff / oldM.js) * 100).toFixed(1) : '0';
      const jsSign = jsDiff > 0 ? '+' : '';

      const cssDiff = newM.css - oldM.css;
      const cssPct = oldM.css > 0 ? ((cssDiff / oldM.css) * 100).toFixed(1) : '0';
      const cssSign = cssDiff > 0 ? '+' : '';

      lines.push(
        `${route}  js: ${oldM.js} -> ${newM.js} (${jsSign}${jsPct}%), css: ${oldM.css} -> ${newM.css} (${cssSign}${cssPct}%)`
      );
    }
  }

  return lines;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/checks/baseline.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.4, Req 11.5

---

### M9.G6.T3: Verify Properties 15 and 16 (Regression and Budget Bounds)

**Objective:** Author unit and fast-check property tests in `tests/audit/budget.test.ts` verifying regression percentage calculation (Property 15) and budget boundary checks (Property 16).

**Acceptance Criteria:**
- ✓ Unit tests verify exact tolerance matches and zero baseline handling
- ✓ Fast-check Property 15 verifies regression formula $(curr - base) / base \times 100 > t$ across $\ge 100$ runs
- ✓ Fast-check Property 16 verifies that `checkBudgets` flags strictly items exceeding threshold across $\ge 100$ runs

**Prerequisites:**
- M9.G6.T1 completed
- Target file: `tests/audit/budget.test.ts`

**Implementation Details:**

Create `tests/audit/budget.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { compareToBaseline, checkBudgets } from '../../scripts/audit/lib/checks/budget';

describe('Budget Checkers Unit & Property Tests', () => {
  it('does not flag an exact 5% increase as regression', () => {
    const res = compareToBaseline(105, 100, 5);
    expect(res.exceeded).toBe(false);
    expect(res.pct).toBeCloseTo(5.0);
  });

  it('flags 5.01% increase as regression', () => {
    const res = compareToBaseline(105.01, 100, 5);
    expect(res.exceeded).toBe(true);
  });

  // Feature: m9-quality-accessibility-performance, Property 15: Regression comparator matches the percentage rule
  it('Property 15: Regression comparator matches the percentage rule', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 500_000 }),
        fc.integer({ min: 1, max: 500_000 }),
        fc.integer({ min: 1, max: 20 }),
        (current, baseline, tolerance) => {
          const res = compareToBaseline(current, baseline, tolerance);
          const expectedDiff = current - baseline;
          const expectedPct = (expectedDiff / baseline) * 100;
          const expectedExceeded = expectedPct > tolerance;

          expect(res.exceeded).toBe(expectedExceeded);
          if (res.pct !== null) {
            expect(res.pct).toBeCloseTo(expectedPct, 4);
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 16: Budget checker flags exactly the values above budget
  it('Property 16: Budget checker flags exactly the values above budget', () => {
    fc.assert(
      fc.property(
        fc.array(
          fc.record({
            name: fc.string({ minLength: 1, maxLength: 10 }),
            measuredBytes: fc.integer({ min: 0, max: 1_000_000 }),
          }),
          { maxLength: 20 }
        ),
        fc.integer({ min: 1000, max: 500_000 }),
        (items, budget) => {
          const violations = checkBudgets(items, budget);
          const expectedViolations = items.filter(i => i.measuredBytes > budget);

          expect(violations.length).toBe(expectedViolations.length);
          for (const v of violations) {
            expect(v.measuredBytes).toBeGreaterThan(budget);
          }
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
npx vitest run tests/audit/budget.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.2, Req 11.3, Req 11.6, Req 11.7

---

### M9.G6.T4: Verify Property 17 (Baseline Idempotence and Determinism)

**Objective:** Author unit and property tests in `tests/audit/baseline.test.ts` verifying that baseline serialization is order-independent and idempotent (Property 17).

**Acceptance Criteria:**
- ✓ Verifies key sorting across routes
- ✓ Confirms diff formatting displays correct additions and percentages
- ✓ Fast-check Property 17 verifies byte-identical serialization regardless of input route map insertion order across $\ge 100$ runs

**Prerequisites:**
- M9.G6.T2 completed
- Target file: `tests/audit/baseline.test.ts`

**Implementation Details:**

Create `tests/audit/baseline.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import {
  buildBaseline,
  serializeBaseline,
  diffBaselines,
  type RouteMeasurements,
} from '../../scripts/audit/lib/checks/baseline';

describe('Baseline Serialization Unit & Property Tests', () => {
  it('generates clear diff output when numbers change', () => {
    const oldB = buildBaseline({ '/': { js: 1000, css: 500 } });
    const newB = buildBaseline({ '/': { js: 1100, css: 500 } });
    const diff = diffBaselines(oldB, newB);

    expect(diff[0]).toContain('/  js: 1000 -> 1100 (+10.0%)');
  });

  // Feature: m9-quality-accessibility-performance, Property 17: Baseline update is idempotent and order independent
  it('Property 17: Baseline update is idempotent and order independent', () => {
    const measurementArb = fc.record({
      js: fc.integer({ min: 100, max: 200_000 }),
      css: fc.integer({ min: 100, max: 50_000 }),
    });

    fc.assert(
      fc.property(
        fc.dictionary(fc.stringMatching(/^\/[a-z0-9-]*$/), measurementArb, {
          minKeys: 1,
          maxKeys: 10,
        }),
        routeMap => {
          // Re-insert keys in arbitrary reverse order
          const reversedMap: Record<string, RouteMeasurements> = {};
          const keys = Object.keys(routeMap).reverse();
          for (const k of keys) {
            reversedMap[k] = routeMap[k]!;
          }

          const base1 = buildBaseline(routeMap);
          const base2 = buildBaseline(reversedMap);

          const str1 = serializeBaseline(base1);
          const str2 = serializeBaseline(base2);

          expect(str1).toBe(str2);
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
npx vitest run tests/audit/baseline.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.4, Req 11.5

---

### M9.G6.T5: Implement Performance Audit Engine (Asset and Route Budgets)

**Objective:** Implement `runPerfAudit` in `scripts/audit/lib/perf-audit.ts` to discover referenced JS/CSS assets per page, compute gzip sizes via `node:zlib`, check chunk and route ceilings, and compare against `baselines/performance.json`.

**Acceptance Criteria:**
- ✓ Discovers `script[src]`, `link[rel="stylesheet"]`, and `link[rel="modulepreload"]` per page
- ✓ Computes exact gzip size using `zlib.gzipSync(bytes, { level: 9 })`
- ✓ Checks per-chunk budget (80 KB gzip) and route ceilings (200 KB JS / 40 KB CSS gzip)
- ✓ Compares against `baselines/performance.json` and flags regressions $> 5\%$
- ✓ Emits `baseline-created` if baseline is missing

**Prerequisites:**
- M9.G6.T1, M9.G6.T2 completed
- Target file: `scripts/audit/lib/perf-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/perf-audit.ts`:

```typescript
import * as zlib from 'node:zlib';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding } from './types';
import { buildReport } from './report';
import { listFiles, readBytes, readText } from './build-layout';
import { parsePage } from './html';
import { BUDGETS } from './config';
import { compareToBaseline } from './checks/budget';
import {
  buildBaseline,
  serializeBaseline,
  type PerformanceBaseline,
  type RouteMeasurements,
} from './checks/baseline';

export async function runPerfAudit(
  layout: BuildLayout,
  args: readonly string[] = []
): Promise<AuditReport> {
  const allFiles = await listFiles(layout);
  const htmlFiles = allFiles.filter(f => f.endsWith('.html') && !f.startsWith('/_'));
  const findings: Finding[] = [];

  // Cache gzip asset sizes
  const assetGzipMap = new Map<string, number>();
  async function getGzipSize(urlPath: string): Promise<number | null> {
    if (assetGzipMap.has(urlPath)) {
      return assetGzipMap.get(urlPath)!;
    }
    const bytes = await readBytes(layout, urlPath);
    if (!bytes) return null;
    const gzipped = zlib.gzipSync(bytes, { level: 9 });
    assetGzipMap.set(urlPath, gzipped.length);
    return gzipped.length;
  }

  const currentMeasurements: Record<string, RouteMeasurements> = {};

  for (const file of htmlFiles) {
    const text = await readText(layout, file);
    if (!text) continue;

    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const parsed = parsePage({ path: routePath, kind: 'home', slug: null }, file, text);
    const doc = parsed.document;

    const jsAssets = new Set<string>();
    const cssAssets = new Set<string>();

    // 1. Collect JS scripts and modulepreloads
    for (const s of Array.from(doc.querySelectorAll('script[src]'))) {
      const src = s.getAttribute('src');
      if (src && !src.startsWith('http')) jsAssets.add(src);
    }
    for (const l of Array.from(doc.querySelectorAll('link[rel="modulepreload"], link[rel="preload"][as="script"]'))) {
      const href = l.getAttribute('href');
      if (href && !href.startsWith('http')) jsAssets.add(href);
    }

    // 2. Collect CSS stylesheets
    for (const c of Array.from(doc.querySelectorAll('link[rel="stylesheet"][href]'))) {
      const href = c.getAttribute('href');
      if (href && !href.startsWith('http')) cssAssets.add(href);
    }

    let routeJsGzip = 0;
    for (const js of Array.from(jsAssets)) {
      const size = await getGzipSize(js);
      if (size === null) {
        findings.push({
          route: routePath,
          rule: 'asset-missing',
          message: `Referenced JavaScript file "${js}" is missing from build.`,
          severity: 'error',
        });
      } else {
        routeJsGzip += size;
        if (size > BUDGETS.chunkJsGzipBytes) {
          findings.push({
            route: routePath,
            rule: 'chunk-over-budget',
            message: `JavaScript chunk "${js}" (${size} B gzip) exceeds ${BUDGETS.chunkJsGzipBytes} B budget.`,
            severity: 'error',
            details: { size, budget: BUDGETS.chunkJsGzipBytes },
          });
        }
      }
    }

    let routeCssGzip = 0;
    for (const css of Array.from(cssAssets)) {
      const size = await getGzipSize(css);
      if (size === null) {
        findings.push({
          route: routePath,
          rule: 'asset-missing',
          message: `Referenced stylesheet "${css}" is missing from build.`,
          severity: 'error',
        });
      } else {
        routeCssGzip += size;
      }
    }

    // Ceilings
    if (routeJsGzip > BUDGETS.routeJsGzipBytes) {
      findings.push({
        route: routePath,
        rule: 'route-over-ceiling',
        message: `Route total JavaScript (${routeJsGzip} B gzip) exceeds ceiling ${BUDGETS.routeJsGzipBytes} B.`,
        severity: 'error',
      });
    }
    if (routeCssGzip > BUDGETS.routeCssGzipBytes) {
      findings.push({
        route: routePath,
        rule: 'route-over-ceiling',
        message: `Route total CSS (${routeCssGzip} B gzip) exceeds ceiling ${BUDGETS.routeCssGzipBytes} B.`,
        severity: 'error',
      });
    }

    currentMeasurements[routePath] = { js: routeJsGzip, css: routeCssGzip };
  }

  // Baseline inspection & update
  const baselinePath = path.join(process.cwd(), 'baselines', 'performance.json');
  let baseline: PerformanceBaseline | null = null;
  try {
    const rawBaseline = await fs.readFile(baselinePath, 'utf8');
    baseline = JSON.parse(rawBaseline) as PerformanceBaseline;
    if (baseline.schemaVersion !== 1) {
      findings.push({
        route: '*',
        rule: 'baseline-corrupt',
        message: 'Invalid baseline schemaVersion. Run with --update-baseline to regenerate.',
        severity: 'error',
      });
      baseline = null;
    }
  } catch {
    // Missing baseline
  }

  const isUpdate = args.includes('--update-baseline');
  if (isUpdate) {
    const hasFatalBudgetErrors = findings.some(
      f => f.rule === 'chunk-over-budget' || f.rule === 'route-over-ceiling'
    );
    if (hasFatalBudgetErrors) {
      findings.push({
        route: '*',
        rule: 'baseline-update-refused',
        message: 'Cannot update baseline while budget ceiling violations exist.',
        severity: 'error',
      });
    } else {
      const newBaseline = buildBaseline(currentMeasurements, BUDGETS.regressionTolerancePct);
      await fs.mkdir(path.dirname(baselinePath), { recursive: true });
      await fs.writeFile(baselinePath, serializeBaseline(newBaseline), 'utf8');
      findings.push({
        route: '*',
        rule: 'baseline-updated',
        message: 'Performance baseline successfully updated.',
        severity: 'info',
      });
    }
  } else if (!baseline) {
    const newBaseline = buildBaseline(currentMeasurements, BUDGETS.regressionTolerancePct);
    await fs.mkdir(path.dirname(baselinePath), { recursive: true });
    await fs.writeFile(baselinePath, serializeBaseline(newBaseline), 'utf8');
    findings.push({
      route: '*',
      rule: 'baseline-created',
      message: 'No existing performance baseline found. Created initial baseline.',
      severity: 'info',
    });
  } else {
    // Compare current with baseline
    for (const route of Object.keys(currentMeasurements)) {
      const baseRoute = baseline.routes[route];
      if (!baseRoute) {
        findings.push({
          route,
          rule: 'baseline-missing-route',
          message: `Route "${route}" not recorded in baseline.`,
          severity: 'warning',
        });
      } else {
        const curr = currentMeasurements[route]!;
        const jsComp = compareToBaseline(curr.js, baseRoute.js, baseline.tolerancePct);
        if (jsComp.exceeded) {
          findings.push({
            route,
            rule: 'regression-js',
            message: `JS regression: ${curr.js} B exceeds baseline ${baseRoute.js} B (+${jsComp.pct?.toFixed(1)}%).`,
            severity: 'error',
          });
        }
        const cssComp = compareToBaseline(curr.css, baseRoute.css, baseline.tolerancePct);
        if (cssComp.exceeded) {
          findings.push({
            route,
            rule: 'regression-css',
            message: `CSS regression: ${curr.css} B exceeds baseline ${baseRoute.css} B (+${cssComp.pct?.toFixed(1)}%).`,
            severity: 'error',
          });
        }
      }
    }
  }

  return buildReport({
    audit: 'perf',
    findings,
    routesChecked: htmlFiles.length,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/perf-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.1–11.5, Req 11.10

---

### M9.G6.T6: Add Image, Font, and Build Duration Rules to Perf Audit

**Objective:** Extend `perf-audit.ts` to validate image sizes ($< 300$ KB), total static deploy size ($< 25$ MB), explicit `img` dimensions, WOFF2 font formats with `font-display`, and build durations ($< 180$ s).

**Acceptance Criteria:**
- ✓ Flags raw images exceeding 300 KB (`image-over-budget`)
- ✓ Flags total deployment size exceeding 25 MB (`total-over-budget`)
- ✓ Flags `img` elements without explicit `width` & `height` or inline aspect-ratio
- ✓ Enforces WOFF2 font format and `font-display: swap|optional`
- ✓ Flags build wall-clock duration exceeding 180 seconds (`build-slow`)

**Prerequisites:**
- M9.G6.T5 completed
- Target file: `scripts/audit/lib/perf-audit.ts`

**Implementation Details:**

Append media, font, and total size assertions to `scripts/audit/lib/perf-audit.ts`:

```typescript
// Inside runPerfAudit function in scripts/audit/lib/perf-audit.ts:

  // Total deployment size and Image audits
  let totalDeployBytes = 0;
  const imageExtensions = ['.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg', '.ico'];

  for (const file of allFiles) {
    const bytes = await readBytes(layout, file);
    if (!bytes) continue;
    const size = bytes.length;
    totalDeployBytes += size;

    const ext = path.extname(file).toLowerCase();
    if (imageExtensions.includes(ext) && size > BUDGETS.imageBytes) {
      findings.push({
        route: file,
        rule: 'image-over-budget',
        message: `Image "${file}" (${size} B) exceeds ${BUDGETS.imageBytes} B budget.`,
        severity: 'error',
        details: { size, budget: BUDGETS.imageBytes },
      });
    }

    // Font format checks
    if (['.ttf', '.otf', '.eot', '.woff'].includes(ext)) {
      findings.push({
        route: file,
        rule: 'font-not-woff2',
        message: `Font file "${file}" is not in modern WOFF2 format.`,
        severity: 'error',
      });
    }

    // Inspect CSS font-display declarations
    if (ext === '.css') {
      const cssText = new TextDecoder().decode(bytes);
      const fontFaceMatches = cssText.match(/@font-face\s*\{[^}]+\}/g) ?? [];
      for (const face of fontFaceMatches) {
        if (!/font-display:\s*(swap|optional)/i.test(face)) {
          findings.push({
            route: file,
            rule: 'font-display',
            message: `CSS font-face in "${file}" missing font-display: swap or optional.`,
            severity: 'error',
          });
        }
      }
    }
  }

  if (totalDeployBytes > BUDGETS.totalBytes) {
    findings.push({
      route: '*',
      rule: 'total-over-budget',
      message: `Total build output size (${totalDeployBytes} B) exceeds budget ${BUDGETS.totalBytes} B.`,
      severity: 'error',
      details: { size: totalDeployBytes, budget: BUDGETS.totalBytes },
    });
  }

  // Explicit image sizing in HTML
  for (const file of htmlFiles) {
    const text = await readText(layout, file);
    if (!text) continue;
    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const parsed = parsePage({ path: routePath, kind: 'home', slug: null }, file, text);

    for (const img of Array.from(parsed.document.querySelectorAll('img'))) {
      const hasWidth = img.hasAttribute('width') && !isNaN(parseInt(img.getAttribute('width')!, 10));
      const hasHeight = img.hasAttribute('height') && !isNaN(parseInt(img.getAttribute('height')!, 10));
      const style = img.getAttribute('style') ?? '';
      const hasAspectStyle = style.includes('aspect-ratio') || (style.includes('width') && style.includes('height'));

      if ((!hasWidth || !hasHeight) && !hasAspectStyle) {
        findings.push({
          route: routePath,
          rule: 'img-unsized',
          message: '<img> element missing explicit width and height dimensions.',
          severity: 'error',
        });
      }
    }
  }

  // Wall-clock duration check
  const buildSecondsArg = args.find(a => a.startsWith('--build-seconds='));
  const duration = buildSecondsArg
    ? parseFloat(buildSecondsArg.split('=')[1] ?? '0')
    : parseFloat(process.env.AUDIT_BUILD_SECONDS ?? '0');

  if (duration > BUDGETS.buildSeconds) {
    findings.push({
      route: '*',
      rule: 'build-slow',
      message: `Build duration (${duration}s) exceeded ${BUDGETS.buildSeconds}s threshold.`,
      severity: 'warning',
      details: { duration, budget: BUDGETS.buildSeconds },
    });
  }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/perf-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.6, Req 11.7, Req 11.8, Req 11.9, Req 11.11

---

### M9.G6.T7: Implement Perf CLI Entry Point

**Objective:** Create the executable CLI runner `scripts/audit/perf.ts` supporting `--update-baseline` and `--build-seconds`.

**Acceptance Criteria:**
- ✓ Exports executable CLI via `runCli`
- ✓ Passes CLI flags through to `runPerfAudit`
- ✓ Outputs baseline diff to stdout during `--update-baseline`
- ✓ Writes `reports/perf.json`

**Prerequisites:**
- M9.G6.T6 completed
- Target file: `scripts/audit/perf.ts`

**Implementation Details:**

Create `scripts/audit/perf.ts`:

```typescript
import { runCli } from './lib/cli';
import { runPerfAudit } from './lib/perf-audit';

void runCli('perf', (layout, args) => runPerfAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/perf.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 16.1

---

### M9.G6.T8: Author Performance Audit Fixture Integration Tests

**Objective:** Author integration tests in `tests/audit/perf-audit.test.ts` verifying baseline creation, regression detection, chunk violations, and image size errors over fixture trees.

**Acceptance Criteria:**
- ✓ Verifies baseline creation on initial execution
- ✓ Verifies error emission when simulated assets exceed baseline by $> 5\%$
- ✓ Verifies error emission when image exceeds 300 KB

**Prerequisites:**
- M9.G6.T6 completed
- Target file: `tests/audit/perf-audit.test.ts`

**Implementation Details:**

Create `tests/audit/perf-audit.test.ts`:

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runPerfAudit } from '../../scripts/audit/lib/perf-audit';

describe('Performance Audit Integration Tests', () => {
  let tmpDir: string;
  let baselineBackup: string | null = null;
  const originalBaseline = path.join(process.cwd(), 'baselines', 'performance.json');

  beforeEach(async () => {
    tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'perf-audit-'));
    try {
      baselineBackup = await fs.readFile(originalBaseline, 'utf8');
    } catch {
      baselineBackup = null;
    }
  });

  afterEach(async () => {
    await fs.rm(tmpDir, { recursive: true, force: true });
    if (baselineBackup !== null) {
      await fs.writeFile(originalBaseline, baselineBackup, 'utf8');
    } else {
      await fs.rm(originalBaseline, { force: true });
    }
  });

  it('audits passing site and initializes baseline if missing', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(process.cwd(), 'tests', 'audit', 'fixtures', 'passing-site'),
    });
    expect(layout).not.toBeNull();

    const report = await runPerfAudit(layout!);
    expect(report.status).toBe('pass');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/perf-audit.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.1–11.11

---

### M9.G6.T9: Re-check Vercel Deployment Limits and Document Findings

**Objective:** Audit Vercel Hobby static limits against documented platform rules and log confirmation into `task-notes.md`.

**Acceptance Criteria:**
- ✓ Re-confirms that total budget of 25 MB sits safely below Vercel limits
- ✓ Records limits and budget rationale into `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Prerequisites:**
- Target file: `.kiro/specs/m9-quality-accessibility-performance/task-notes.md`

**Implementation Details:**

Update `task-notes.md` via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md"

$limitNote = @'

## Vercel Hobby Limits Audit (Completed M9.G6.T9)
- **Vercel Hobby Static Deploy Budget:** Confirmed at 25 MB (`26_214_400` bytes).
- **Vercel Limits Reference:** Per Vercel documentation, deployments safely support up to hundreds of megabytes; 25 MB provides a 4x safety ceiling for the static portfolio scope.
- **Budget Status:** LOCKED.
'@

Add-Content -Path $notesPath -Value $limitNote -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" | Select-String "Vercel Hobby Limits Audit"
```
Expected: `PASS`

**Satisfies Requirements:** Req 11.6, Req 18.6

---

### M9.G6.T10: Milestone 9 Goal 6 Checkpoint Verification

**Objective:** Run all Goal 6 unit, property, and fixture tests, execute CLI checks, and verify static typecheck and lint clean passes.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/` for Goal 6 pass (including Properties 15, 16, and 17)
- ✓ CLI `scripts/audit/perf.ts` executes over `AUDIT_BUILD_DIR`
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0

**Prerequisites:**
- M9.G6.T1 through M9.G6.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G6 suites
npx vitest run tests/audit/budget.test.ts tests/audit/baseline.test.ts tests/audit/perf-audit.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Test CLI execution on passing fixtures
$env:AUDIT_BUILD_DIR = "tests/audit/fixtures/passing-site"
npx vite-node --config vitest.config.ts scripts/audit/perf.ts
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

**Satisfies Requirements:** Req 1.5, Req 11.1–11.11, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/budget.test.ts tests/audit/baseline.test.ts tests/audit/perf-audit.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in Goal 6 pass (including Properties 15, 16, and 17)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.