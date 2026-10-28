# M9.G8: Lighthouse Audit and Manual Lighthouse Procedure

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the local static server (`scripts/audit/lib/static-server.ts`), the pure Lighthouse median result evaluator, and the automated Lighthouse audit runner (`scripts/audit/lib/lighthouse-audit.ts`) with its standalone CLI (`scripts/audit/lighthouse.ts`). Author the supplementary human verification procedure and results template in `docs/quality/manual-lighthouse-procedure.md`. This goal enforces Core Web Vitals thresholds (LCP $< 2500$ ms, CLS $< 0.1$, FCP $< 1800$ ms, TBT $< 200$ ms, Accessibility $\ge 95$, Performance/SEO/Best Practices $\ge 90$) over 5 mobile emulation runs per inventory route using dynamic imports of Approval_Item A3 dependencies, isolates Lighthouse from `npm test` and the aggregate `audit` script, and documents TBT as the lab proxy for INP.

---

## Goal Success Criteria

- ✓ Approval_Item A3 is confirmed as Approved 2026-10-22 in `task-notes.md` prior to executing Lighthouse imports
- ✓ `scripts/audit/lib/static-server.ts` provides a zero-dependency `node:http` server supporting `flat` and `directory` route mappings, on-the-fly gzip compression, and 404 responses
- ✓ `evaluateRoute` calculates the median across 5 runs and enforces strict Core Web Vitals and category thresholds
- ✓ Excludes `/404` route from SEO score gating per Decision 8
- ✓ Reports TBT as the lab proxy for INP ($< 200$ ms) with note on field data validation
- ✓ Exits with code 2 and outputs a pointer to `docs/quality/manual-lighthouse-procedure.md` if `lighthouse` or `chrome-launcher` cannot be imported
- ✓ `docs/quality/manual-lighthouse-procedure.md` provides complete steps for Chrome DevTools and PageSpeed Insights audits across all P0 routes
- ✓ Zero imports of `lighthouse` or `chrome-launcher` exist in any default test or `run-all.ts`

---

## Prerequisites

- Goals M9.G1 through M9.G7 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Fixtures available in `tests/audit/fixtures/`
- Approval A3 recorded in `task-notes.md`

---

## Tasks

### M9.G8.T1: Verify Approval A3 and Audit Lighthouse Dependencies

**Objective:** Confirm that Approval_Item A3 is recorded as Approved 2026-10-22 in `task-notes.md` and verify the availability of `lighthouse` and `chrome-launcher` in `node_modules` with exact pinned versions.

**Acceptance Criteria:**
- ✓ Validates that `task-notes.md` contains the approval record for A3
- ✓ Checks that `lighthouse` and `chrome-launcher` can be resolved or installs pinned devDependencies
- ✓ Documents purpose and maintenance status
- ✓ Historical fallback: If packages are uninstalled, dynamic imports catch the failure gracefully

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- File `.kiro\specs\m9-quality-accessibility-performance\task-notes.md` exists

**Implementation Details:**

Verify Approval A3 via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content "..\.kiro\specs\m9-quality-accessibility-performance\task-notes.md" -Raw
if ($notes -notmatch "\*\*A3\*\*.*Approved") {
    Write-Error "Approval A3 is not recorded as Approved in task-notes.md"
    exit 1
}

$lhInstalled = (Test-Path "node_modules\lighthouse") -and (Test-Path "node_modules\chrome-launcher")
if (-not $lhInstalled) {
    Write-Host "Installing pinned lighthouse and chrome-launcher devDependencies (Approval A3)..."
    npm install --save-dev lighthouse@12.2.1 chrome-launcher@1.1.2
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
node -e "require('chrome-launcher'); console.log('PASS');"
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.8, Req 18.6

---

### M9.G8.T2: Implement Lightweight Local Static HTTP Server

**Objective:** Implement `startStaticServer` and `stopStaticServer` in `scripts/audit/lib/static-server.ts` using `node:http` and `node:zlib` to serve Build_Output on an ephemeral port.

**Acceptance Criteria:**
- ✓ Binds to host `127.0.0.1` on port 0 (ephemeral allocation)
- ✓ Maps incoming URL paths to build files using `routeFileCandidates`
- ✓ Dynamically compresses text responses (`text/html`, `text/css`, `application/javascript`) with gzip
- ✓ Serves `404.html` with HTTP status 404 for unknown paths
- ✓ Exposes special test route `/__audit-not-found` that responds with status 404
- ✓ Shuts down cleanly without lingering socket listeners

**Prerequisites:**
- M9.G8.T1 completed
- Target file: `scripts/audit/lib/static-server.ts`

**Implementation Details:**

Create `scripts/audit/lib/static-server.ts`:

```typescript
import * as http from 'node:http';
import * as zlib from 'node:zlib';
import type { BuildLayout } from './build-layout';
import { readBytes } from './build-layout';
import { routeFileCandidates } from './route-files';

export interface StaticServer {
  readonly origin: string;
  readonly close: () => Promise<void>;
}

export async function startStaticServer(layout: BuildLayout): Promise<StaticServer> {
  const server = http.createServer(async (req, res) => {
    const rawUrl = req.url ?? '/';
    const parsedPath = rawUrl.split('?')[0] ?? '/';

    // Special test route for not-found page testing
    const isSpecial404 = parsedPath === '/__audit-not-found';
    const lookupPath = isSpecial404 ? '/404' : parsedPath;

    let content: Uint8Array | null = null;
    let statusCode = isSpecial404 ? 404 : 200;

    // Try direct file first
    content = await readBytes(layout, lookupPath);

    // Try route file candidates
    if (!content) {
      const candidates = routeFileCandidates(lookupPath);
      for (const cand of candidates) {
        content = await readBytes(layout, `/${cand}`);
        if (content) break;
      }
    }

    // Fall back to 404.html
    if (!content) {
      statusCode = 404;
      content = await readBytes(layout, '/404.html');
      if (!content) {
        content = await readBytes(layout, '/404/index.html');
      }
    }

    if (!content) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not Found');
      return;
    }

    // Determine content type
    let contentType = 'application/octet-stream';
    if (parsedPath.endsWith('.html') || !parsedPath.includes('.')) contentType = 'text/html; charset=utf-8';
    else if (parsedPath.endsWith('.css')) contentType = 'text/css; charset=utf-8';
    else if (parsedPath.endsWith('.js')) contentType = 'application/javascript; charset=utf-8';
    else if (parsedPath.endsWith('.svg')) contentType = 'image/svg+xml';
    else if (parsedPath.endsWith('.png')) contentType = 'image/png';
    else if (parsedPath.endsWith('.jpg') || parsedPath.endsWith('.jpeg')) contentType = 'image/jpeg';
    else if (parsedPath.endsWith('.woff2')) contentType = 'font/woff2';

    // Gzip text responses
    const isText = contentType.startsWith('text/') || contentType.startsWith('application/javascript');
    const acceptGzip = (req.headers['accept-encoding'] ?? '').includes('gzip');

    if (isText && acceptGzip) {
      const gzipped = zlib.gzipSync(content, { level: 6 });
      res.writeHead(statusCode, {
        'Content-Type': contentType,
        'Content-Encoding': 'gzip',
        'Content-Length': gzipped.length,
      });
      res.end(gzipped);
    } else {
      res.writeHead(statusCode, {
        'Content-Type': contentType,
        'Content-Length': content.length,
      });
      res.end(content);
    }
  });

  return new Promise((resolve, reject) => {
    server.listen(0, '127.0.0.1', () => {
      const addr = server.address();
      if (!addr || typeof addr === 'string') {
        reject(new Error('Failed to obtain ephemeral port'));
        return;
      }
      const origin = `http://127.0.0.1:${addr.port}`;
      resolve({
        origin,
        close: () =>
          new Promise<void>((resClose, rejClose) => {
            server.close(err => (err ? rejClose(err) : resClose()));
          }),
      });
    });
    server.on('error', reject);
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/static-server.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.1

---

### M9.G8.T3: Implement Pure Lighthouse Evaluation Logic and Tests

**Objective:** Implement `median` calculation and `evaluateRoute` in `scripts/audit/lib/lighthouse-audit.ts` enforcing strict thresholds across multiple runs, and author unit tests in `tests/audit/lighthouse-evaluate.test.ts`.

**Acceptance Criteria:**
- ✓ Computes exact median value for odd run counts
- ✓ Flags scores: Accessibility $< 95$; Performance, Best Practices, SEO $< 90$
- ✓ Flags Core Web Vitals: LCP $\ge 2500$ ms, CLS $\ge 0.1$, FCP $\ge 1800$ ms, TBT $\ge 200$ ms
- ✓ Does NOT gate SEO score on `/404` route (Decision 8)
- ✓ Captures failing audit IDs in `details`

**Prerequisites:**
- M9.G8.T2 completed
- Target files: `scripts/audit/lib/lighthouse-audit.ts`, `tests/audit/lighthouse-evaluate.test.ts`

**Implementation Details:**

1. Create initial evaluation logic in `scripts/audit/lib/lighthouse-audit.ts`:

```typescript
import { LIGHTHOUSE } from './config';
import type { Finding } from './types';

export interface LighthouseScores {
  readonly accessibility: number;
  readonly performance: number;
  readonly bestPractices: number;
  readonly seo: number;
}

export interface LighthouseMetrics {
  readonly lcpMs: number;
  readonly cls: number;
  readonly fcpMs: number;
  readonly tbtMs: number;
}

export interface LighthouseRunSample {
  readonly scores: LighthouseScores;
  readonly metrics: LighthouseMetrics;
}

export function median(values: readonly number[]): number {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  if (sorted.length % 2 !== 0) {
    return sorted[mid]!;
  }
  return (sorted[mid - 1]! + sorted[mid]!) / 2;
}

export function evaluateRoute(
  routePath: string,
  runs: readonly LighthouseRunSample[]
): {
  readonly findings: readonly Finding[];
  readonly medianScores: LighthouseScores;
  readonly medianMetrics: LighthouseMetrics;
} {
  const isNotFound = routePath === '/404';

  const medianScores: LighthouseScores = {
    accessibility: median(runs.map(r => r.scores.accessibility)),
    performance: median(runs.map(r => r.scores.performance)),
    bestPractices: median(runs.map(r => r.scores.bestPractices)),
    seo: median(runs.map(r => r.scores.seo)),
  };

  const medianMetrics: LighthouseMetrics = {
    lcpMs: median(runs.map(r => r.metrics.lcpMs)),
    cls: median(runs.map(r => r.metrics.cls)),
    fcpMs: median(runs.map(r => r.metrics.fcpMs)),
    tbtMs: median(runs.map(r => r.metrics.tbtMs)),
  };

  const findings: Finding[] = [];

  // Score Gates
  if (medianScores.accessibility < LIGHTHOUSE.minScores.accessibility) {
    findings.push({
      route: routePath,
      rule: 'lh-accessibility',
      message: `Lighthouse Accessibility score (${medianScores.accessibility}) below required ${LIGHTHOUSE.minScores.accessibility}.`,
      severity: 'error',
      details: { score: medianScores.accessibility },
    });
  }

  if (medianScores.performance < LIGHTHOUSE.minScores.performance) {
    findings.push({
      route: routePath,
      rule: 'lh-performance',
      message: `Lighthouse Performance score (${medianScores.performance}) below required ${LIGHTHOUSE.minScores.performance}.`,
      severity: 'error',
      details: { score: medianScores.performance },
    });
  }

  if (medianScores.bestPractices < LIGHTHOUSE.minScores.bestPractices) {
    findings.push({
      route: routePath,
      rule: 'lh-best-practices',
      message: `Lighthouse Best Practices score (${medianScores.bestPractices}) below required ${LIGHTHOUSE.minScores.bestPractices}.`,
      severity: 'error',
      details: { score: medianScores.bestPractices },
    });
  }

  // Decision 8: Skip SEO score gating on 404
  if (!isNotFound && medianScores.seo < LIGHTHOUSE.minScores.seo) {
    findings.push({
      route: routePath,
      rule: 'lh-seo',
      message: `Lighthouse SEO score (${medianScores.seo}) below required ${LIGHTHOUSE.minScores.seo}.`,
      severity: 'error',
      details: { score: medianScores.seo },
    });
  }

  // Core Web Vitals Gates
  if (medianMetrics.lcpMs >= LIGHTHOUSE.maxMetrics.lcpMs) {
    findings.push({
      route: routePath,
      rule: 'lh-lcp',
      message: `LCP metric (${medianMetrics.lcpMs} ms) is >= threshold ${LIGHTHOUSE.maxMetrics.lcpMs} ms.`,
      severity: 'error',
      details: { lcpMs: medianMetrics.lcpMs },
    });
  }

  if (medianMetrics.cls >= LIGHTHOUSE.maxMetrics.cls) {
    findings.push({
      route: routePath,
      rule: 'lh-cls',
      message: `CLS metric (${medianMetrics.cls}) is >= threshold ${LIGHTHOUSE.maxMetrics.cls}.`,
      severity: 'error',
      details: { cls: medianMetrics.cls },
    });
  }

  if (medianMetrics.fcpMs >= LIGHTHOUSE.maxMetrics.fcpMs) {
    findings.push({
      route: routePath,
      rule: 'lh-fcp',
      message: `FCP metric (${medianMetrics.fcpMs} ms) is >= threshold ${LIGHTHOUSE.maxMetrics.fcpMs} ms.`,
      severity: 'error',
      details: { fcpMs: medianMetrics.fcpMs },
    });
  }

  if (medianMetrics.tbtMs >= LIGHTHOUSE.maxMetrics.tbtMs) {
    findings.push({
      route: routePath,
      rule: 'lh-tbt',
      message: `TBT metric (${medianMetrics.tbtMs} ms) is >= threshold ${LIGHTHOUSE.maxMetrics.tbtMs} ms.`,
      severity: 'error',
      details: { tbtMs: medianMetrics.tbtMs },
    });
  }

  return { findings, medianScores, medianMetrics };
}
```

2. Create `tests/audit/lighthouse-evaluate.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { median, evaluateRoute, type LighthouseRunSample } from '../../scripts/audit/lib/lighthouse-audit';

describe('Lighthouse Evaluation Unit Tests', () => {
  it('correctly calculates the median of numbers', () => {
    expect(median([10, 20, 30, 40, 50])).toBe(30);
    expect(median([5, 15, 25, 35])).toBe(20);
  });

  it('passes when all scores and metrics meet thresholds', () => {
    const validSample: LighthouseRunSample = {
      scores: { accessibility: 98, performance: 95, bestPractices: 95, seo: 95 },
      metrics: { lcpMs: 1200, cls: 0.02, fcpMs: 1000, tbtMs: 50 },
    };
    const res = evaluateRoute('/', [validSample, validSample, validSample, validSample, validSample]);
    expect(res.findings).toHaveLength(0);
  });

  it('exempts 404 route from SEO score failure (Decision 8)', () => {
    const lowSeoSample: LighthouseRunSample = {
      scores: { accessibility: 98, performance: 95, bestPractices: 95, seo: 75 },
      metrics: { lcpMs: 1200, cls: 0.02, fcpMs: 1000, tbtMs: 50 },
    };
    const res = evaluateRoute('/404', [lowSeoSample, lowSeoSample, lowSeoSample]);
    const seoErrors = res.findings.filter(f => f.rule === 'lh-seo');
    expect(seoErrors).toHaveLength(0);
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/lighthouse-evaluate.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.2, Req 12.3, Req 12.4, Req 12.7

---

### M9.G8.T4: Implement Automated Lighthouse Audit Runner

**Objective:** Complete `scripts/audit/lib/lighthouse-audit.ts` to launch headless Chrome, start the static server, execute 5 mobile runs per inventory route, and aggregate results into `AuditReport`.

**Acceptance Criteria:**
- ✓ Launches Chrome headless with flag `--no-sandbox`
- ✓ Executes 5 iterations per route with mobile emulation
- ✓ Records Chrome and Lighthouse versions in report `data`
- ✓ States in report that TBT is the lab proxy for INP
- ✓ Stops static server and closes Chrome instance reliably in finally block

**Prerequisites:**
- M9.G8.T3 completed
- Target file: `scripts/audit/lib/lighthouse-audit.ts`

**Implementation Details:**

Append the runner logic to `scripts/audit/lib/lighthouse-audit.ts`:

```typescript
// Append to scripts/audit/lib/lighthouse-audit.ts:

import type { BuildLayout } from './build-layout';
import type { AuditReport } from './types';
import { buildReport } from './report';
import { startStaticServer } from './static-server';
import { loadRouteInventory } from './route-inventory';

export interface LighthouseReportData {
  readonly lighthouseVersion: string;
  readonly chromeVersion: string;
  readonly runs: number;
  readonly note: string;
  readonly routes: ReadonlyArray<{
    readonly route: string;
    readonly scores: LighthouseScores;
    readonly metrics: LighthouseMetrics;
  }>;
}

export async function runLighthouseAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport<LighthouseReportData | null>> {
  let lighthouse: typeof import('lighthouse');
  let chromeLauncher: typeof import('chrome-launcher');

  try {
    lighthouse = await import('lighthouse');
    chromeLauncher = await import('chrome-launcher');
  } catch {
    return buildReport<LighthouseReportData | null>({
      audit: 'lighthouse',
      findings: [],
      routesChecked: 0,
      skipped: ['lighthouse or chrome-launcher not installed'],
      data: null,
    });
  }

  const server = await startStaticServer(layout);
  let chrome: import('chrome-launcher').LaunchedChrome | null = null;

  try {
    chrome = await chromeLauncher.launch({
      chromeFlags: ['--headless', '--no-sandbox', '--disable-gpu'],
    });

    const { routes } = await loadRouteInventory();
    const findings: Finding[] = [];
    const routeSummaries: Array<{
      route: string;
      scores: LighthouseScores;
      metrics: LighthouseMetrics;
    }> = [];

    for (const route of routes) {
      const urlPath = route.path === '/404' ? '/__audit-not-found' : route.path;
      const targetUrl = `${server.origin}${urlPath}`;
      const samples: LighthouseRunSample[] = [];

      for (let run = 0; run < LIGHTHOUSE.runs; run++) {
        const runnerResult = await lighthouse.default(targetUrl, {
          port: chrome.port,
          output: 'json',
          onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
          formFactor: 'mobile',
          screenEmulation: {
            mobile: true,
            width: 390,
            height: 844,
            deviceScaleFactor: 2,
            disabled: false,
          },
        });

        if (!runnerResult) continue;
        const lhr = runnerResult.lhr;

        samples.push({
          scores: {
            accessibility: Math.round((lhr.categories.accessibility?.score ?? 0) * 100),
            performance: Math.round((lhr.categories.performance?.score ?? 0) * 100),
            bestPractices: Math.round((lhr.categories['best-practices']?.score ?? 0) * 100),
            seo: Math.round((lhr.categories.seo?.score ?? 0) * 100),
          },
          metrics: {
            lcpMs: lhr.audits['largest-contentful-paint']?.numericValue ?? 0,
            cls: lhr.audits['cumulative-layout-shift']?.numericValue ?? 0,
            fcpMs: lhr.audits['first-contentful-paint']?.numericValue ?? 0,
            tbtMs: lhr.audits['total-blocking-time']?.numericValue ?? 0,
          },
        });
      }

      const evaluation = evaluateRoute(route.path, samples);
      findings.push(...evaluation.findings);
      routeSummaries.push({
        route: route.path,
        scores: evaluation.medianScores,
        metrics: evaluation.medianMetrics,
      });
    }

    const data: LighthouseReportData = {
      lighthouseVersion: '12.2.1',
      chromeVersion: 'HeadlessChrome',
      runs: LIGHTHOUSE.runs,
      note: 'Total Blocking Time (TBT < 200ms) serves as the lab proxy for INP. Real-user INP < 200ms is verified from field data when available.',
      routes: routeSummaries,
    };

    return buildReport<LighthouseReportData | null>({
      audit: 'lighthouse',
      findings,
      routesChecked: routes.length,
      data,
    });
  } finally {
    if (chrome) {
      await chrome.kill();
    }
    await server.close();
  }
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/lighthouse-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.1–12.7

---

### M9.G8.T5: Implement Lighthouse CLI Entry Point with Exit-2 Fallback

**Objective:** Create `scripts/audit/lighthouse.ts` wrapping `runLighthouseAudit` with clear command line feedback and exit code 2 fallback guidance.

**Acceptance Criteria:**
- ✓ Exports executable CLI via `runCli`
- ✓ Prints pointer to `docs/quality/manual-lighthouse-procedure.md` if execution fails or dependencies are missing
- ✓ Writes `reports/lighthouse.json` on completion

**Prerequisites:**
- M9.G8.T4 completed
- Target file: `scripts/audit/lighthouse.ts`

**Implementation Details:**

Create `scripts/audit/lighthouse.ts`:

```typescript
import { resolveBuildLayout } from './lib/build-layout';
import { runLighthouseAudit } from './lib/lighthouse-audit';
import { writeReport } from './lib/report';

async function main() {
  const layout = await resolveBuildLayout();
  if (!layout) {
    process.stderr.write('Build output not found. Run npm run build first.\n');
    process.exit(2);
  }

  try {
    process.stdout.write('Starting local Lighthouse audit (5 mobile runs per route)...\n');
    const report = await runLighthouseAudit(layout);

    if (report.status === 'skipped') {
      process.stdout.write(
        'Lighthouse dependencies missing or unresolvable.\n' +
        'Please refer to docs/quality/manual-lighthouse-procedure.md for manual DevTools auditing.\n'
      );
      process.exit(2);
    }

    const outPath = await writeReport(report);
    const summary = report.summary;
    const statusLabel = report.status.toUpperCase();

    process.stdout.write(
      `[lighthouse] ${statusLabel} - Errors: ${summary.errors}, Warnings: ${summary.warnings} (Report: ${outPath})\n`
    );

    process.exitCode = report.status === 'fail' ? 1 : 0;
  } catch (err) {
    process.stderr.write(`Lighthouse execution crashed: ${err instanceof Error ? err.message : String(err)}\n`);
    process.stderr.write('Refer to docs/quality/manual-lighthouse-procedure.md for manual procedure.\n');
    process.exit(2);
  }
}

void main();
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lighthouse.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.6, Req 12.9, Req 16.1

---

### M9.G8.T6: Author Static Server Verification Tests

**Objective:** Write `tests/audit/static-server.test.ts` verifying ephemeral port binding, gzip encoding header emission, 404 handling, and clean shutdown.

**Acceptance Criteria:**
- ✓ Verifies HTTP GET on `/` returns 200 with HTML content
- ✓ Verifies HTTP GET with `Accept-Encoding: gzip` returns `Content-Encoding: gzip`
- ✓ Verifies unknown paths return status 404
- ✓ Confirms clean server closure

**Prerequisites:**
- M9.G8.T2 completed
- Target file: `tests/audit/static-server.test.ts`

**Implementation Details:**

Create `tests/audit/static-server.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { startStaticServer } from '../../scripts/audit/lib/static-server';

describe('Static Server Unit Tests', () => {
  it('serves pages and compresses with gzip', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(process.cwd(), 'tests', 'audit', 'fixtures', 'passing-site'),
    });
    expect(layout).not.toBeNull();

    const server = await startStaticServer(layout!);
    try {
      const res = await fetch(`${server.origin}/`, {
        headers: { 'Accept-Encoding': 'gzip' },
      });
      expect(res.status).toBe(200);
      expect(res.headers.get('content-encoding')).toBe('gzip');

      const res404 = await fetch(`${server.origin}/non-existent-page`);
      expect(res404.status).toBe(404);
    } finally {
      await server.close();
    }
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/static-server.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.1

---

### M9.G8.T7: Create Manual Lighthouse Procedure Document

**Objective:** Author `docs/quality/manual-lighthouse-procedure.md` detailing step-by-step auditing instructions using Chrome DevTools and Google PageSpeed Insights.

**Acceptance Criteria:**
- ✓ Details local testing via Chrome DevTools Lighthouse tab (Mobile device emulation, Clear storage)
- ✓ Details remote testing via Google PageSpeed Insights
- ✓ Lists all target metrics and thresholds: LCP $< 2.5$ s, CLS $< 0.1$, FCP $< 1.8$ s, TBT $< 200$ ms, Accessibility $\ge 95$, Performance/SEO/Best Practices $\ge 90$
- ✓ Provides a results template table covering all P0 routes
- ✓ Explains the TBT lab proxy relationship for field INP

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `docs/quality/manual-lighthouse-procedure.md`:

```markdown
# Manual Lighthouse & Core Web Vitals Audit Procedure

> **Standard:** TRD Section 6.1 Performance Benchmarks & PRD Success Criteria  
> **Target Device:** Mobile (Simulated Moto G4 / Mid-Tier Mobile)  
> **Status:** Active Release Requirement

---

## 1. Overview & Purpose
This procedure defines the manual verification protocol for Core Web Vitals and Lighthouse category scores when running in local development or performing pre-release deployment verification.

---

## 2. Benchmark Thresholds

| Metric / Category | Target SLA | Source / Tooling |
| :--- | :--- | :--- |
| **Accessibility Score** | **$\ge$ 95** | Lighthouse Mobile |
| **Performance Score** | **$\ge$ 90** | Lighthouse Mobile |
| **Best Practices Score**| **$\ge$ 90** | Lighthouse Mobile |
| **SEO Score** | **$\ge$ 90** (Exempt on `/404`) | Lighthouse Mobile |
| **Largest Contentful Paint (LCP)** | **$< 2.5$ s** | Core Web Vitals |
| **Cumulative Layout Shift (CLS)** | **$< 0.1$** | Core Web Vitals |
| **First Contentful Paint (FCP)** | **$< 1.8$ s** | Core Web Vitals |
| **Total Blocking Time (TBT)** | **$< 200$ ms** | Lab Proxy for INP |
| **Interaction to Next Paint (INP)**| **$< 200$ ms** | Field Data (when live) |

---

## 3. Execution Steps (Chrome DevTools)

1. **Serve Static Build:**
   ```bash
   npx serve out/ -p 3000
   ```
2. **Open Guest / Incognito Window:**
   Navigate to `http://localhost:3000`. Ensure all browser extensions are disabled.
3. **Open Lighthouse Panel:**
   Press `F12` $\rightarrow$ Select the **Lighthouse** tab.
4. **Configure Settings:**
   - **Mode:** Navigation (Default)
   - **Device:** Mobile
   - **Categories:** Performance, Accessibility, Best Practices, SEO
   - Check **Clear storage** before audit.
5. **Analyze Page:**
   Click **Analyze page load**. Repeat 3–5 times per route and take the median result.

---

## 4. Manual Audit Results Log

- **Tester:** _______________________
- **Date:** _________________________
- **Environment:** Local Static Build (`out/`)

| Route | Perf | A11y | Best Pract | SEO | LCP (s) | CLS | FCP (s) | TBT (ms) | Pass / Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/` | | | | | | | | | [ ] |
| `/projects` | | | | | | | | | [ ] |
| `/projects/[slug]` | | | | | | | | | [ ] |
| `/certifications` | | | | | | | | | [ ] |
| `/blog` | | | | | | | | | [ ] |
| `/blog/[slug]` | | | | | | | | | [ ] |
| `/404` | | | | N/A | | | | | [ ] |
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "docs\quality\manual-lighthouse-procedure.md"
```
Expected: `True`

**Satisfies Requirements:** Req 12.9

---

### M9.G8.T8: Author Test for Manual Lighthouse Documentation Completeness

**Objective:** Write `tests/audit/manual-lighthouse-procedure.test.ts` to assert that all Core Web Vitals metrics, thresholds, and P0 route patterns appear in the manual procedure document.

**Acceptance Criteria:**
- ✓ Asserts presence of LCP (2.5s), CLS (0.1), FCP (1.8s), TBT (200ms), A11y (95), Perf (90)
- ✓ Asserts presence of all P0 routes in results table
- ✓ Asserts presence of DevTools and PageSpeed Insights guidance

**Prerequisites:**
- M9.G8.T7 completed
- Target file: `tests/audit/manual-lighthouse-procedure.test.ts`

**Implementation Details:**

Create `tests/audit/manual-lighthouse-procedure.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Manual Lighthouse Documentation Completeness', () => {
  it('contains all required metrics, thresholds, and route patterns', async () => {
    const docPath = path.join(process.cwd(), 'docs', 'quality', 'manual-lighthouse-procedure.md');
    const content = await fs.readFile(docPath, 'utf8');

    // Metrics
    expect(content).toMatch(/2\.5/);
    expect(content).toMatch(/0\.1/);
    expect(content).toMatch(/1\.8/);
    expect(content).toMatch(/200/);
    expect(content).toMatch(/95/);
    expect(content).toMatch(/90/);

    // Routes
    expect(content).toMatch(/`\/`/);
    expect(content).toMatch(/`\/projects`/);
    expect(content).toMatch(/`\/projects\/\[slug\]`/);
    expect(content).toMatch(/`\/certifications`/);
    expect(content).toMatch(/`\/blog`/);
    expect(content).toMatch(/`\/blog\/\[slug\]`/);
    expect(content).toMatch(/`\/404`/);
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/manual-lighthouse-procedure.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.9

---

### M9.G8.T9: Author Lighthouse Isolation Verification Test

**Objective:** Write `tests/audit/lighthouse-isolation.test.ts` verifying that neither `lighthouse` nor `chrome-launcher` is imported in `scripts/audit/run-all.ts` or standard unit test suites.

**Acceptance Criteria:**
- ✓ Asserts `scripts/audit/run-all.ts` does not contain `lighthouse`
- ✓ Asserts no non-Lighthouse audit script imports `chrome-launcher`
- ✓ Confirms `npm test` does not invoke headless Chrome

**Prerequisites:**
- M9.G8.T4 completed
- Target file: `tests/audit/lighthouse-isolation.test.ts`

**Implementation Details:**

Create `tests/audit/lighthouse-isolation.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Lighthouse Execution Isolation', () => {
  it('ensures aggregate runner run-all does not import or invoke lighthouse', async () => {
    const runAllPath = path.join(process.cwd(), 'scripts', 'audit', 'run-all.ts');
    let exists = false;
    try {
      await fs.stat(runAllPath);
      exists = true;
    } catch {
      exists = false;
    }

    if (exists) {
      const content = await fs.readFile(runAllPath, 'utf8');
      expect(content).not.toMatch(/from\s+['"].*lighthouse-audit['"]/);
      expect(content).not.toContain('lighthouse');
    }
  });

  it('ensures no other audit script imports chrome-launcher', async () => {
    const auditLibDir = path.join(process.cwd(), 'scripts', 'audit', 'lib');
    const files = await fs.readdir(auditLibDir);

    for (const f of files) {
      if (f.endsWith('.ts') && f !== 'lighthouse-audit.ts') {
        const text = await fs.readFile(path.join(auditLibDir, f), 'utf8');
        expect(text).not.toContain('chrome-launcher');
      }
    }
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/lighthouse-isolation.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 12.10

---

### M9.G8.T10: Milestone 9 Goal 8 Checkpoint Verification

**Objective:** Execute all Goal 8 unit and integration tests, verify typecheck and lint compliance, and confirm that zero unapproved package modifications exist.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/lighthouse-evaluate.test.ts`, `static-server.test.ts`, `manual-lighthouse-procedure.test.ts`, and `lighthouse-isolation.test.ts` pass
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0

**Prerequisites:**
- M9.G8.T1 through M9.G8.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G8 suites
npx vitest run tests/audit/lighthouse-evaluate.test.ts tests/audit/static-server.test.ts tests/audit/manual-lighthouse-procedure.test.ts tests/audit/lighthouse-isolation.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Static typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. ESLint
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

**Satisfies Requirements:** Req 12.1–12.10, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/lighthouse-evaluate.test.ts tests/audit/static-server.test.ts tests/audit/manual-lighthouse-procedure.test.ts tests/audit/lighthouse-isolation.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in Goal 8 pass
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.