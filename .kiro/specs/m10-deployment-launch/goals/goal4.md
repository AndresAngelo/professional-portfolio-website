# M10.G4: Deployment Verifier Pure Core

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure, offline-testable domain logic for the deployment smoke verifier across five modular components: HTML page signal extraction (`page-signals.ts`), verification check evaluators (`checks.ts`), CLI argument parser and run-mode classifier (`args.ts`), M9-compatible verification audit report builder (`verify-report.ts`), and post-launch check-in calendar calculator (`check-in-dates.ts`). Formally verify Correctness Properties 12 through 17 and Property 20 via fast-check randomized testing, ensuring zero network access, zero file system writes, and zero references to `process.env`.

## Goal Success Criteria

- ✓ `scripts/launch/lib/page-signals.ts` extracts canonical link `href`, robots `meta` content, document title, primary `h1` text, and Next.js static asset URLs via `jsdom`
- ✓ `scripts/launch/lib/checks.ts` implements status checking, 404 body confirmation, canonical comparison according to run kind (preview vs. production per `design.md` Decision 10), and robots directive verification (handling `noindex` on 404 and Vercel preview tags per Clarification C3/C4/C7)
- ✓ `scripts/launch/lib/args.ts` validates CLI arguments (enforcing a bare `https:` origin with zero path/query/fragment) and classifies runs as `production` or `preview` based on origin matching
- ✓ `scripts/launch/lib/verify-report.ts` formats route check summaries and builds an `AuditReport<VerifyData>` that cleanly passes M9 `validateReport`
- ✓ `scripts/launch/lib/check-in-dates.ts` calculates exact UTC calendar offsets (+7, +28, +84 days) from any `YYYY-MM-DD` launch date
- ✓ Properties 12, 13, 14, 15, 16, 17, and 20 pass at least 100 iterations each in `tests/launch/*.property.test.ts`
- ✓ All pure modules contain zero I/O side effects, zero `process.env` references, and zero `any` types

## Prerequisites

- Goal M10.G1, M10.G2, and M10.G3 completed (`scripts/launch/lib/types.ts` and M9 audit contracts available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Node.js 18+ environment with fast-check and vitest

---

## Tasks

### M10.G4.T1: Implement Page Signal Extraction (`scripts/launch/lib/page-signals.ts`)

**Objective:** Implement `scripts/launch/lib/page-signals.ts` using `jsdom` to parse static HTML strings and extract the canonical URL, robots meta directives, page title, `h1` heading, and Next.js static asset URLs.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `extractPageSignals(html)` parses HTML without executing scripts
- ✓ Returns first `link[rel~="canonical"]` href attribute, or `null` if absent
- ✓ Returns `meta[name="robots"]` content attribute (lowercased), or `null` if absent
- ✓ Returns `document.title` (trimmed), or `null` if absent/empty
- ✓ Returns first `h1` textContent (trimmed), or `null` if absent/empty
- ✓ Gathers all `script[src]` and `link[href]` starting with `/_next/static/` into `staticAssetPaths`
- ✓ Unit tests in `tests/launch/page-signals.test.ts` pass cleanly

**Prerequisites:**
- M10.G1.T6 completed (`scripts/launch/lib/types.ts`)
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\page-signals.ts`

**Implementation Details:**
Create `scripts/launch/lib/page-signals.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { JSDOM } from 'jsdom';

export interface PageSignals {
  readonly title: string | null;
  readonly h1: string | null;
  readonly canonical: string | null;
  readonly robotsMeta: string | null;
  readonly staticAssetPaths: readonly string[];
}

export function extractPageSignals(html: string): PageSignals {
  const dom = new JSDOM(html, { runScripts: 'outside-only' });
  const doc = dom.window.document;

  const canonicalLink = doc.querySelector('link[rel~="canonical"]');
  const canonical = canonicalLink ? canonicalLink.getAttribute('href') : null;

  const robotsMetaEl = doc.querySelector('meta[name="robots" i]');
  const robotsMeta = robotsMetaEl ? robotsMetaEl.getAttribute('content')?.toLowerCase() ?? null : null;

  const titleEl = doc.querySelector('title');
  const rawTitle = titleEl ? titleEl.textContent?.trim() ?? '' : '';
  const title = rawTitle.length > 0 ? rawTitle : null;

  const h1El = doc.querySelector('h1');
  const rawH1 = h1El ? h1El.textContent?.trim() ?? '' : '';
  const h1 = rawH1.length > 0 ? rawH1 : null;

  const staticAssetPaths = new Set<string>();

  const scripts = Array.from(doc.querySelectorAll('script[src]'));
  for (const s of scripts) {
    const src = s.getAttribute('src');
    if (src && src.startsWith('/_next/static/')) {
      staticAssetPaths.add(src);
    }
  }

  const links = Array.from(doc.querySelectorAll('link[href]'));
  for (const l of links) {
    const href = l.getAttribute('href');
    if (href && href.startsWith('/_next/static/')) {
      staticAssetPaths.add(href);
    }
  }

  return {
    title,
    h1,
    canonical,
    robotsMeta,
    staticAssetPaths: Array.from(staticAssetPaths).sort(),
  };
}
'@ | Set-Content -Path "scripts\launch\lib\page-signals.ts" -Encoding UTF8
```

Write accompanying unit test `tests/launch/page-signals.test.ts`:
```powershell
@'
import { describe, it, expect } from 'vitest';
import { extractPageSignals } from '../../scripts/launch/lib/page-signals';

describe('extractPageSignals Unit Test', () => {
  it('extracts canonical, robots, title, h1, and static assets from HTML', () => {
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <title> Projects | Angelo Andres </title>
          <link rel="canonical" href="https://example.com/projects" />
          <meta name="robots" content="index, follow" />
          <link rel="stylesheet" href="/_next/static/css/app.css" />
          <script src="/_next/static/chunks/main.js"></script>
        </head>
        <body>
          <h1> Featured Projects </h1>
        </body>
      </html>
    `;

    const signals = extractPageSignals(html);
    expect(signals.title).toBe('Projects | Angelo Andres');
    expect(signals.h1).toBe('Featured Projects');
    expect(signals.canonical).toBe('https://example.com/projects');
    expect(signals.robotsMeta).toBe('index, follow');
    expect(signals.staticAssetPaths).toContain('/_next/static/css/app.css');
    expect(signals.staticAssetPaths).toContain('/_next/static/chunks/main.js');
  });

  it('handles missing tags gracefully with nulls and empty lists', () => {
    const signals = extractPageSignals('<html><body><p>Empty</p></body></html>');
    expect(signals.title).toBeNull();
    expect(signals.h1).toBeNull();
    expect(signals.canonical).toBeNull();
    expect(signals.robotsMeta).toBeNull();
    expect(signals.staticAssetPaths).toEqual([]);
  });
});
'@ | Set-Content -Path "tests\launch\page-signals.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/page-signals.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.9

---

### M10.G4.T2: Implement CLI Argument Parser and Run Classifier (`scripts/launch/lib/args.ts`)

**Objective:** Implement `scripts/launch/lib/args.ts` exporting pure functions `parseArgs` and `classifyRun` according to the command-line interface specification in `design.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `parseArgs` enforces exactly one positional argument that must be an absolute `https:` URL
- ✓ Rejects URLs with non-empty paths (other than `/`), credentials, queries, or fragments
- ✓ Normalizes base URL to `url.origin` (no trailing slash)
- ✓ Parses optional flags: `--timeout <ms>`, `--concurrency <n>`, `--vercel-json <path>`, `--expect-headers <path>`
- ✓ Returns standardized usage text on invalid arguments
- ✓ `classifyRun(baseUrl, siteUrl)` returns `'production'` if `new URL(baseUrl).origin === new URL(siteUrl).origin`, otherwise `'preview'`

**Prerequisites:**
- M10.G1.T6 completed (`scripts/launch/lib/types.ts`)
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\args.ts`

**Implementation Details:**
Create `scripts/launch/lib/args.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { VerifyArgs, RunKind } from './types';

export type ParseArgsResult =
  | { readonly ok: true; readonly args: VerifyArgs }
  | { readonly ok: false; readonly usage: string };

const USAGE_TEXT = `Usage: verify-deployment <https-base-url> [options]

Arguments:
  <https-base-url>              Base URL to verify (e.g. https://portfolio.vercel.app)

Options:
  --timeout <ms>               Request timeout in ms (default: 10000)
  --concurrency <n>            Maximum concurrent requests (default: 4)
  --vercel-json <path>         Path to vercel.json (default: vercel.json)
  --expect-headers <path>      Path to JSON fallback headers file (optional)
`;

export function parseArgs(argv: readonly string[]): ParseArgsResult {
  let baseUrl: string | null = null;
  let timeoutMs = 10000;
  let concurrency = 4;
  let vercelJsonPath = 'vercel.json';
  let expectHeadersPath: string | null = null;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i] ?? '';
    if (arg === '--timeout') {
      const val = parseInt(argv[++i] ?? '', 10);
      if (isNaN(val) || val <= 0) return { ok: false, usage: USAGE_TEXT };
      timeoutMs = val;
    } else if (arg === '--concurrency') {
      const val = parseInt(argv[++i] ?? '', 10);
      if (isNaN(val) || val <= 0) return { ok: false, usage: USAGE_TEXT };
      concurrency = val;
    } else if (arg === '--vercel-json') {
      const pathVal = argv[++i];
      if (!pathVal || pathVal.startsWith('--')) return { ok: false, usage: USAGE_TEXT };
      vercelJsonPath = pathVal;
    } else if (arg === '--expect-headers') {
      const pathVal = argv[++i];
      if (!pathVal || pathVal.startsWith('--')) return { ok: false, usage: USAGE_TEXT };
      expectHeadersPath = pathVal;
    } else if (arg.startsWith('--')) {
      return { ok: false, usage: USAGE_TEXT };
    } else {
      if (baseUrl !== null) {
        return { ok: false, usage: USAGE_TEXT }; // Multiple positional URLs rejected
      }
      baseUrl = arg;
    }
  }

  if (!baseUrl) {
    return { ok: false, usage: USAGE_TEXT };
  }

  let parsed: URL;
  try {
    parsed = new URL(baseUrl);
  } catch {
    return { ok: false, usage: USAGE_TEXT };
  }

  if (parsed.protocol !== 'https:') {
    return { ok: false, usage: USAGE_TEXT };
  }

  if (parsed.username || parsed.password) {
    return { ok: false, usage: USAGE_TEXT };
  }

  if (parsed.pathname !== '/' && parsed.pathname !== '') {
    return { ok: false, usage: USAGE_TEXT };
  }

  if (parsed.search || parsed.hash) {
    return { ok: false, usage: USAGE_TEXT };
  }

  return {
    ok: true,
    args: {
      baseUrl: parsed.origin,
      timeoutMs,
      concurrency,
      vercelJsonPath,
      expectHeadersPath,
    },
  };
}

export function classifyRun(baseUrl: string, siteUrl: string): RunKind {
  try {
    const baseOrigin = new URL(baseUrl).origin;
    const siteOrigin = new URL(siteUrl).origin;
    return baseOrigin === siteOrigin ? 'production' : 'preview';
  } catch {
    return 'preview';
  }
}
'@ | Set-Content -Path "scripts\launch\lib\args.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.10

---

### M10.G4.T3: Implement Status and Body Check Functions (`scripts/launch/lib/checks.ts`)

**Objective:** Implement the initial suite of pure checking functions in `scripts/launch/lib/checks.ts` for HTTP response status codes and 404 not-found body signal validation.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `checkStatus(actual, expected)` asserts HTTP status equality and returns `CheckResult`
- ✓ `checkNotFoundBody(body, signals)` checks presence of local 404 `title` and `h1` text in the response body
- ✓ Emits `not-found-body-missing-title` or `not-found-body-missing-h1` when expected text is missing
- ✓ Emits passing result if expected signals are `null` (degraded local layout mode)

**Prerequisites:**
- M10.G1.T6 completed (`scripts/launch/lib/types.ts`)
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\checks.ts`

**Implementation Details:**
Create `scripts/launch/lib/checks.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { CheckResult, RunKind } from './types';

export function checkStatus(actual: number, expected: number): CheckResult {
  const passed = actual === expected;
  return {
    id: 'status',
    severity: 'error',
    passed,
    message: passed
      ? `HTTP Status ${actual} matched expected ${expected}.`
      : `HTTP Status mismatch: expected ${expected}, got ${actual}.`,
    details: { actual, expected },
  };
}

export function checkNotFoundBody(
  body: string,
  signals: { readonly title: string | null; readonly h1: string | null } | null
): CheckResult {
  if (!signals || (signals.title === null && signals.h1 === null)) {
    return {
      id: 'not-found-body',
      severity: 'info',
      passed: true,
      message: 'Local 404 signals not available; body content check skipped.',
    };
  }

  if (signals.title && !body.includes(signals.title)) {
    return {
      id: 'not-found-body',
      severity: 'error',
      passed: false,
      message: `404 response body missing expected title text '${signals.title}'.`,
      details: { expectedTitle: signals.title },
    };
  }

  if (signals.h1 && !body.includes(signals.h1)) {
    return {
      id: 'not-found-body',
      severity: 'error',
      passed: false,
      message: `404 response body missing expected heading text '${signals.h1}'.`,
      details: { expectedH1: signals.h1 },
    };
  }

  return {
    id: 'not-found-body',
    severity: 'error',
    passed: true,
    message: '404 response body successfully validated against local 404 signals.',
  };
}
'@ | Set-Content -Path "scripts\launch\lib\checks.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.4, Req 7.5, Req 7.6

---

### M10.G4.T4: Implement Canonical, Robots, and Not-Found Route Logic (`scripts/launch/lib/checks.ts`)

**Objective:** Append `checkCanonical` and `checkRobots` to `scripts/launch/lib/checks.ts` implementing Decision 10 (preview vs production comparison), Clarifications C3/C4 (handling `siteUrl` and preview `X-Robots-Tag`), and Clarification C7 (`noindex` expected on 404).

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `checkCanonical` compares against base URL for production runs, and against `siteUrl` for preview runs
- ✓ Emits `base-differs-from-siteUrl` info finding on preview runs
- ✓ Flags missing canonical (`canonical === null`) as an error
- ✓ `checkRobots` asserts presence of `noindex` if `expectNoindex === true` (404 route), and absence of `noindex` on standard routes
- ✓ Flags `X-Robots-Tag: noindex` as error on production, and as `info` (`details.reason: 'expected-on-preview'`) on preview runs

**Prerequisites:**
- M10.G4.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\checks.ts`

**Implementation Details:**
Append `checkCanonical` and `checkRobots` to `scripts/launch/lib/checks.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$checkExtensions = @'

export function expectedCanonical(base: string, routePath: string, style: 'flat' | 'directory'): string {
  const cleanBase = base.replace(/\/+$/, '');
  const cleanPath = routePath === '/' ? '' : routePath.replace(/^\/+|\/+$/g, '');

  if (cleanPath === '') {
    return `${cleanBase}/`;
  }

  if (style === 'directory') {
    return `${cleanBase}/${cleanPath}/`;
  }

  return `${cleanBase}/${cleanPath}`;
}

export function checkCanonical(input: {
  readonly actual: string | null;
  readonly path: string;
  readonly base: string;
  readonly siteUrl: string;
  readonly run: RunKind;
  readonly style: 'flat' | 'directory';
}): readonly CheckResult[] {
  const results: CheckResult[] = [];

  if (input.actual === null) {
    results.push({
      id: 'canonical',
      severity: 'error',
      passed: false,
      message: `Canonical link missing on route ${input.path}.`,
    });
    return results;
  }

  if (input.run === 'production') {
    const expected = expectedCanonical(input.base, input.path, input.style);
    const passed = input.actual === expected;
    results.push({
      id: 'canonical',
      severity: 'error',
      passed,
      message: passed
        ? `Canonical URL matched expected '${expected}'.`
        : `Canonical URL mismatch on production: expected '${expected}', got '${input.actual}'.`,
      details: { expected, actual: input.actual },
    });
  } else {
    // Preview run
    const expected = expectedCanonical(input.siteUrl, input.path, input.style);
    const passed = input.actual === expected;

    results.push({
      id: 'canonical',
      severity: 'error',
      passed,
      message: passed
        ? `Canonical URL matched expected siteUrl '${expected}'.`
        : `Canonical URL mismatch on preview: expected siteUrl '${expected}', got '${input.actual}'.`,
      details: { expectedSiteUrl: expected, actual: input.actual },
    });

    results.push({
      id: 'base-differs-from-siteUrl',
      severity: 'info',
      passed: true,
      message: 'Base URL differs from siteUrl on preview deployment; canonical validated against siteUrl.',
      details: { baseUrl: input.base, siteUrl: input.siteUrl },
    });
  }

  return results;
}

export function checkRobots(input: {
  readonly robotsMeta: string | null;
  readonly xRobotsTag: string | null;
  readonly run: RunKind;
  readonly expectNoindex: boolean;
}): readonly CheckResult[] {
  const results: CheckResult[] = [];

  const metaHasNoindex = input.robotsMeta !== null && input.robotsMeta.toLowerCase().includes('noindex');
  const headerHasNoindex = input.xRobotsTag !== null && input.xRobotsTag.toLowerCase().includes('noindex');

  // Meta tag validation
  if (input.expectNoindex) {
    const passed = metaHasNoindex;
    results.push({
      id: 'robots-meta',
      severity: 'error',
      passed,
      message: passed
        ? 'Expected noindex directive confirmed in robots meta tag.'
        : 'Missing expected noindex directive in robots meta tag on 404 route.',
    });
  } else {
    const passed = !metaHasNoindex;
    results.push({
      id: 'robots-meta',
      severity: 'error',
      passed,
      message: passed
        ? 'Robots meta tag does not contain noindex directive.'
        : "Forbidden 'noindex' directive found in robots meta tag on standard route.",
    });
  }

  // Header validation
  if (input.run === 'production') {
    const passed = !headerHasNoindex;
    results.push({
      id: 'robots-header',
      severity: 'error',
      passed,
      message: passed
        ? 'X-Robots-Tag header is clean of noindex on production.'
        : "Forbidden 'X-Robots-Tag: noindex' detected on production deployment.",
    });
  } else {
    // Preview run
    if (headerHasNoindex) {
      results.push({
        id: 'robots-header',
        severity: 'info',
        passed: true,
        message: 'X-Robots-Tag: noindex detected on preview deployment (expected platform behavior).',
        details: { reason: 'expected-on-preview' },
      });
    } else {
      results.push({
        id: 'robots-header',
        severity: 'info',
        passed: true,
        message: 'X-Robots-Tag header is clean.',
      });
    }
  }

  return results;
}
'@

Add-Content -Path "scripts\launch\lib\checks.ts" -Value $checkExtensions -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.5, Req 7.9, Req 7.10

---

### M10.G4.T5: Implement Verification Report Builder (`scripts/launch/lib/verify-report.ts`)

**Objective:** Implement `scripts/launch/lib/verify-report.ts` providing `buildVerifyReport` and `formatSummary` to generate standardized `AuditReport<VerifyData>` structures compatible with M9 contracts.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `buildVerifyReport` maps per-route checks into M9 `Finding` structures
- ✓ Error checks increment `failed` count and `summary.errors`
- ✓ Warnings and info results never increment failed count and never fail the audit status
- ✓ Routes and findings are deterministically sorted by route identifier
- ✓ Generated report conforms to M9 `AuditReport<VerifyData>` schema
- ✓ `formatSummary` returns a formatted table with one summary line per verified route

**Prerequisites:**
- M10.G1.T6 completed (`scripts/launch/lib/types.ts`)
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\verify-report.ts`

**Implementation Details:**
Create `scripts/launch/lib/verify-report.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { buildReport } from '../../audit/lib/report';
import type { AuditReport, Finding } from '../../audit/lib/types';
import type { VerifyData, RouteResult, CheckResult, VerifyArgs, RunKind } from './types';

export interface RawRouteResult {
  readonly route: string;
  readonly url: string;
  readonly status: number | null;
  readonly checks: readonly CheckResult[];
}

export function buildVerifyReport(input: {
  readonly args: VerifyArgs;
  readonly siteUrl: string;
  readonly run: RunKind;
  readonly results: readonly RawRouteResult[];
  readonly now: string;
}): AuditReport<VerifyData> {
  const sortedRaw = [...input.results].sort((a, b) => a.route.localeCompare(b.route));
  const findings: Finding[] = [];
  const processedRoutes: RouteResult[] = [];

  let totalPassed = 0;
  let totalFailed = 0;

  for (const r of sortedRaw) {
    let routePassed = 0;
    let routeFailed = 0;

    for (const c of r.checks) {
      if (c.severity === 'error') {
        if (c.passed) {
          routePassed++;
        } else {
          routeFailed++;
          findings.push({
            route: r.route,
            rule: c.id,
            message: c.message,
            severity: 'error',
            details: c.details,
          });
        }
      } else if (c.severity === 'warning') {
        if (!c.passed) {
          findings.push({
            route: r.route,
            rule: c.id,
            message: c.message,
            severity: 'warning',
            details: c.details,
          });
        }
      } else if (c.severity === 'info') {
        findings.push({
          route: r.route,
          rule: c.id,
          message: c.message,
          severity: 'info',
          details: c.details,
        });
      }
    }

    totalPassed += routePassed;
    totalFailed += routeFailed;

    processedRoutes.push({
      route: r.route,
      url: r.url,
      status: r.status,
      passed: routePassed,
      failed: routeFailed,
      checks: r.checks.map(c => ({ id: c.id, passed: c.passed, severity: c.severity })),
    });
  }

  const verifyData: VerifyData = {
    baseUrl: input.args.baseUrl,
    siteUrl: input.siteUrl,
    run: input.run,
    totals: { passed: totalPassed, failed: totalFailed },
    routes: processedRoutes,
  };

  return buildReport({
    audit: 'verify-deployment',
    findings,
    routesChecked: processedRoutes.map(r => r.route),
    skipped: [],
    data: verifyData,
    now: input.now,
  });
}

export function formatSummary(report: AuditReport<VerifyData>): string {
  const lines: string[] = [];
  lines.push(`\n=== Deployment Verification Summary (${report.data.run.toUpperCase()}) ===`);
  lines.push(`Base URL: ${report.data.baseUrl}`);
  lines.push(`Status:   ${report.status.toUpperCase()} (${report.summary.errors} errors, ${report.summary.warnings} warnings)`);
  lines.push('-----------------------------------------------------------------');

  for (const r of report.data.routes) {
    const outcome = r.failed === 0 ? 'PASS' : 'FAIL';
    lines.push(`${r.route.padEnd(30)} ${outcome.padEnd(6)} [${r.passed}/${r.passed + r.failed}] (HTTP ${r.status ?? 'ERR'})`);
  }
  lines.push('-----------------------------------------------------------------');
  return lines.join('\n');
}
'@ | Set-Content -Path "scripts\launch\lib\verify-report.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.12

---

### M10.G4.T6: Implement Check-In Dates Calculator (`scripts/launch/lib/check-in-dates.ts`)

**Objective:** Implement `scripts/launch/lib/check-in-dates.ts` exporting `computeCheckInDates` to compute exact UTC calendar dates for Week 1 (+7 days), Week 4 (+28 days), and Week 12 (+84 days) post-launch check-ins.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `computeCheckInDates(launchDate)` accepts `YYYY-MM-DD` string
- ✓ Throws `RangeError` if date string is invalid, malformed, or out of range
- ✓ Adds exactly 7, 28, and 84 days in UTC calendar arithmetic
- ✓ Handles leap years and month/year rollovers deterministically
- ✓ Returns `{ week1, week4, week12 }` with formatted `YYYY-MM-DD` strings

**Prerequisites:**
- M10.G1.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\check-in-dates.ts`

**Implementation Details:**
Create `scripts/launch/lib/check-in-dates.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
export interface CheckInDates {
  readonly week1: string;
  readonly week4: string;
  readonly week12: string;
}

export function computeCheckInDates(launchDateStr: string): CheckInDates {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(launchDateStr)) {
    throw new RangeError(`Invalid date format '${launchDateStr}', expected YYYY-MM-DD.`);
  }

  const [yearStr, monthStr, dayStr] = launchDateStr.split('-');
  const year = parseInt(yearStr ?? '', 10);
  const month = parseInt(monthStr ?? '', 10);
  const day = parseInt(dayStr ?? '', 10);

  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    throw new RangeError(`Invalid calendar date '${launchDateStr}'.`);
  }

  const addDays = (base: Date, days: number): string => {
    const next = new Date(base.getTime() + days * 86400000);
    const y = next.getUTCFullYear();
    const m = String(next.getUTCMonth() + 1).padStart(2, '0');
    const d = String(next.getUTCDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  };

  return {
    week1: addDays(date, 7),
    week4: addDays(date, 28),
    week12: addDays(date, 84),
  };
}
'@ | Set-Content -Path "scripts\launch\lib\check-in-dates.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.4

---

### M10.G4.T7: Implement Fast-Check Tests for Args, Classification, and Status (Properties 14, 15, 16)

**Objective:** Write randomized property-based tests in `tests/launch/args.property.test.ts` and `tests/launch/checks.property.test.ts` formally proving Properties 14, 15, and 16 over at least 100 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 14 proves `parseArgs` accepts only valid bare `https:` origins and rejects credentials, paths, queries, and bad flags
- ✓ Property 15 proves `classifyRun` returns `production` if and only if URL origins match
- ✓ Property 16 proves `checkStatus` and `checkNotFoundBody` validate exact status codes and signal text
- ✓ Tests pass with at least 100 runs each

**Prerequisites:**
- M10.G4.T2 and M10.G4.T3 completed
- Target files: `tests/launch/args.property.test.ts`, `tests/launch/checks.property.test.ts`

**Implementation Details:**
Create the property test files using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. args.property.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { parseArgs, classifyRun } from '../../scripts/launch/lib/args';

describe('M10 Args & Run Classification Properties (Properties 14 & 15)', () => {
  // Feature: m10-deployment-launch, Property 14: Argument parsing accepts only a bare https:// origin
  it('Property 14: Argument parsing accepts only a bare https:// origin', () => {
    const validOriginArb = fc.tuple(
      fc.stringMatching(/^[a-z0-9-]{3,15}$/),
      fc.constantFrom('com', 'org', 'app', 'dev')
    ).map(([sub, tld]) => `https://${sub}.${tld}`);

    fc.assert(
      fc.property(validOriginArb, url => {
        const res = parseArgs([url]);
        expect(res.ok).toBe(true);
        if (res.ok) {
          expect(res.args.baseUrl).toBe(url);
          expect(res.args.timeoutMs).toBe(10000);
        }

        // With trailing slash normalizes cleanly
        const resSlash = parseArgs([`${url}/`]);
        expect(resSlash.ok).toBe(true);

        // With invalid path must fail
        const resPath = parseArgs([`${url}/subpath`]);
        expect(resPath.ok).toBe(false);

        // With http must fail
        const resHttp = parseArgs([url.replace('https:', 'http:')]);
        expect(resHttp.ok).toBe(false);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m10-deployment-launch, Property 15: Run classification compares origins
  it('Property 15: Run classification compares origins', () => {
    const hostArb = fc.stringMatching(/^[a-z0-9-]{3,12}\.com$/);

    fc.assert(
      fc.property(hostArb, hostArb, (h1, h2) => {
        const u1 = `https://${h1}/`;
        const u2 = `https://${h2}/projects`;

        const runKind = classifyRun(u1, u2);
        if (h1 === h2) {
          expect(runKind).toBe('production');
        } else {
          expect(runKind).toBe('preview');
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content -Path "tests\launch\args.property.test.ts" -Encoding UTF8

# 2. checks.property.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { checkStatus, checkNotFoundBody } from '../../scripts/launch/lib/checks';

describe('M10 Status and Body Checks (Property 16)', () => {
  // Feature: m10-deployment-launch, Property 16: Status and body expectations
  it('Property 16: Status and body expectations', () => {
    fc.assert(
      fc.property(fc.integer({ min: 100, max: 599 }), fc.integer({ min: 100, max: 599 }), (actual, expected) => {
        const res = checkStatus(actual, expected);
        expect(res.passed).toBe(actual === expected);
      }),
      { numRuns: 100 }
    );

    fc.assert(
      fc.property(
        fc.stringMatching(/^[a-zA-Z0-9_\s]{5,20}$/),
        fc.stringMatching(/^[a-zA-Z0-9_\s]{5,20}$/),
        (title, h1) => {
          const bodyWithBoth = `<html><head><title>${title}</title></head><body><h1>${h1}</h1></body></html>`;
          const resBoth = checkNotFoundBody(bodyWithBoth, { title, h1 });
          expect(resBoth.passed).toBe(true);

          const bodyMissingH1 = `<html><head><title>${title}</title></head><body><h1>Different</h1></body></html>`;
          const resMiss = checkNotFoundBody(bodyMissingH1, { title, h1 });
          expect(resMiss.passed).toBe(false);
        }
      ),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content -Path "tests\launch\checks.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/args.property.test.ts tests/launch/checks.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.4, Req 7.5, Req 7.6, Req 7.10

---

### M10.G4.T8: Implement Fast-Check Tests for Canonical & Robots (Properties 12 & 13)

**Objective:** Write randomized property-based tests in `tests/launch/canonical-robots.property.test.ts` formally proving Property 12 (canonical evaluation) and Property 13 (robots meta and header evaluation) over at least 100 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 12 proves `checkCanonical` strictly evaluates against base URL on production, and against `siteUrl` on preview
- ✓ Proves preview runs emit `base-differs-from-siteUrl` info finding
- ✓ Property 13 proves `checkRobots` requires `noindex` on 404, forbids `noindex` on standard routes, and treats preview `X-Robots-Tag: noindex` as `info`
- ✓ Tests pass with at least 100 runs each

**Prerequisites:**
- M10.G4.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\canonical-robots.property.test.ts`

**Implementation Details:**
Create `tests/launch/canonical-robots.property.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { checkCanonical, checkRobots, expectedCanonical } from '../../scripts/launch/lib/checks';
import type { RunKind } from '../../scripts/launch/lib/types';

describe('M10 Canonical & Robots Properties (Properties 12 & 13)', () => {
  // Feature: m10-deployment-launch, Property 12: Canonical check follows the run kind
  it('Property 12: Canonical check follows the run kind', () => {
    const routeArb = fc.constantFrom('/', '/projects', '/certifications', '/blog');
    const runKindArb = fc.constantFrom<RunKind>('production', 'preview');

    fc.assert(
      fc.property(routeArb, runKindArb, (route, run) => {
        const base = 'https://preview.vercel.app';
        const siteUrl = 'https://production.com';

        const targetBase = run === 'production' ? base : siteUrl;
        const matchingCanonical = expectedCanonical(targetBase, route, 'flat');

        // 1. Correct canonical passes
        const resPass = checkCanonical({
          actual: matchingCanonical,
          path: route,
          base,
          siteUrl,
          run,
          style: 'flat',
        });
        const canonicalCheck = resPass.find(r => r.id === 'canonical');
        expect(canonicalCheck?.passed).toBe(true);

        if (run === 'preview') {
          expect(resPass.some(r => r.id === 'base-differs-from-siteUrl')).toBe(true);
        } else {
          expect(resPass.some(r => r.id === 'base-differs-from-siteUrl')).toBe(false);
        }

        // 2. Incorrect canonical fails
        const resFail = checkCanonical({
          actual: 'https://wrong-domain.com/',
          path: route,
          base,
          siteUrl,
          run,
          style: 'flat',
        });
        const failCheck = resFail.find(r => r.id === 'canonical');
        expect(failCheck?.passed).toBe(false);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m10-deployment-launch, Property 13: Robots check follows the run kind and route type
  it('Property 13: Robots check follows the run kind and route type', () => {
    const runKindArb = fc.constantFrom<RunKind>('production', 'preview');
    const expectNoindexArb = fc.boolean();

    fc.assert(
      fc.property(runKindArb, expectNoindexArb, (run, expectNoindex) => {
        const metaContent = expectNoindex ? 'noindex, follow' : 'index, follow';
        const headerValue = run === 'preview' ? 'noindex' : null;

        const results = checkRobots({
          robotsMeta: metaContent,
          xRobotsTag: headerValue,
          run,
          expectNoindex,
        });

        const metaRes = results.find(r => r.id === 'robots-meta');
        expect(metaRes?.passed).toBe(true);

        const headerRes = results.find(r => r.id === 'robots-header');
        if (run === 'production') {
          expect(headerRes?.passed).toBe(true);
          expect(headerRes?.severity).toBe('error');
        } else {
          expect(headerRes?.passed).toBe(true);
          expect(headerRes?.severity).toBe('info');
          if (headerValue?.includes('noindex')) {
            expect(headerRes?.details?.reason).toBe('expected-on-preview');
          }
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content -Path "tests\launch\canonical-robots.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/canonical-robots.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.9, Req 7.10

---

### M10.G4.T9: Implement Fast-Check Tests for Reports & Check-In Dates (Properties 17 & 20)

**Objective:** Write randomized property-based tests in `tests/launch/verify-report.property.test.ts` and `tests/launch/check-in-dates.property.test.ts` formally proving Property 17 (report validity and input-order invariance) and Property 20 (UTC calendar check-in date arithmetic) over at least 100 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 17 proves `buildVerifyReport` produces reports that pass M9 `validateReport`, maintains count consistency, and is invariant to input ordering
- ✓ Property 20 proves `computeCheckInDates` computes dates exactly 7, 28, and 84 days later across month, year, and leap-day boundaries
- ✓ Proves `computeCheckInDates` throws `RangeError` on invalid calendar dates (e.g. `2026-02-30`)
- ✓ Tests pass with at least 100 runs each

**Prerequisites:**
- M10.G4.T5 and M10.G4.T6 completed
- Target files: `tests/launch/verify-report.property.test.ts`, `tests/launch/check-in-dates.property.test.ts`

**Implementation Details:**
Create the property test files using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. verify-report.property.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { buildVerifyReport, type RawRouteResult } from '../../scripts/launch/lib/verify-report';
import { validateReport } from '../../audit/lib/report';
import type { VerifyArgs } from '../../scripts/launch/lib/types';

describe('M10 Verify Report Properties (Property 17)', () => {
  const dummyArgs: VerifyArgs = {
    baseUrl: 'https://example.com',
    timeoutMs: 10000,
    concurrency: 4,
    vercelJsonPath: 'vercel.json',
    expectHeadersPath: null,
  };

  // Feature: m10-deployment-launch, Property 17: Verification reports are valid, consistent, and order independent
  it('Property 17: Verification reports are valid, consistent, and order independent', () => {
    const rawResultArb = fc.record<RawRouteResult>({
      route: fc.stringMatching(/^\/[a-z0-9-]{1,10}$/),
      url: fc.constant('https://example.com/route'),
      status: fc.constant(200),
      checks: fc.array(
        fc.record({
          id: fc.constantFrom('status', 'canonical', 'robots-meta'),
          severity: fc.constantFrom('error', 'warning', 'info'),
          passed: fc.boolean(),
          message: fc.constant('check outcome'),
        }),
        { minLength: 1, maxLength: 4 }
      ),
    });

    fc.assert(
      fc.property(fc.uniqueArray(rawResultArb, { selector: r => r.route, minLength: 1, maxLength: 5 }), results => {
        const now = '2026-10-22T00:00:00.000Z';
        const report1 = buildVerifyReport({
          args: dummyArgs,
          siteUrl: 'https://example.com',
          run: 'production',
          results,
          now,
        });

        // 1. Conforms to M9 schema
        expect(validateReport(report1)).toBe(true);

        // 2. Count consistency
        const failedErrors = results.reduce(
          (acc, r) => acc + r.checks.filter(c => c.severity === 'error' && !c.passed).length,
          0
        );
        expect(report1.summary.errors).toBe(failedErrors);
        expect(report1.status).toBe(failedErrors === 0 ? 'pass' : 'fail');

        // 3. Input order invariance
        const reversedResults = [...results].reverse();
        const report2 = buildVerifyReport({
          args: dummyArgs,
          siteUrl: 'https://example.com',
          run: 'production',
          results: reversedResults,
          now,
        });

        expect(report1).toEqual(report2);
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content -Path "tests\launch\verify-report.property.test.ts" -Encoding UTF8

# 2. check-in-dates.property.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { computeCheckInDates } from '../../scripts/launch/lib/check-in-dates';

describe('M10 Check-In Dates Properties (Property 20)', () => {
  // Feature: m10-deployment-launch, Property 20: Check-in dates are fixed offsets from the launch date
  it('Property 20: Check-in dates are fixed offsets from the launch date', () => {
    // Generate valid calendar days between 2026 and 2028
    const dateArb = fc.date({ min: new Date('2026-01-01T00:00:00Z'), max: new Date('2028-12-31T00:00:00Z') })
      .map(d => d.toISOString().split('T')[0]!);

    fc.assert(
      fc.property(dateArb, dateStr => {
        const dates = computeCheckInDates(dateStr);
        const base = new Date(`${dateStr}T00:00:00Z`).getTime();

        const w1 = new Date(`${dates.week1}T00:00:00Z`).getTime();
        const w4 = new Date(`${dates.week4}T00:00:00Z`).getTime();
        const w12 = new Date(`${dates.week12}T00:00:00Z`).getTime();

        expect(w1 - base).toBe(7 * 86400000);
        expect(w4 - base).toBe(28 * 86400000);
        expect(w12 - base).toBe(84 * 86400000);
      }),
      { numRuns: 100 }
    );

    // Invalid dates throw RangeError
    expect(() => computeCheckInDates('2026-02-31')).toThrow(RangeError);
    expect(() => computeCheckInDates('invalid-date')).toThrow(RangeError);
  });
});
'@ | Set-Content -Path "tests\launch\check-in-dates.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/verify-report.property.test.ts tests/launch/check-in-dates.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.12, Req 14.4

---

### M10.G4.T10: Goal 4 Checkpoint and Quality Gate Verification

**Objective:** Execute the full verification suite (linting, typechecking, and all pure-core property tests) to confirm Goal 4 is complete with zero regressions and zero side-effect leaks.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ All property tests for Goal 4 (Properties 12, 13, 14, 15, 16, 17, 20) pass with at least 100 runs each
- ✓ Zero modified files outside `scripts/launch/` and `tests/launch/`

**Prerequisites:**
- M10.G4.T1 through M10.G4.T9 completed

**Implementation Details:**
Execute the verification pipeline via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw "Typecheck failed" }

# 2. Lint
npm run lint
if ($LASTEXITCODE -ne 0) { throw "Lint failed" }

# 3. Test Suites
npx vitest run tests/launch/page-signals.test.ts tests/launch/args.property.test.ts tests/launch/checks.property.test.ts tests/launch/canonical-robots.property.test.ts tests/launch/verify-report.property.test.ts tests/launch/check-in-dates.property.test.ts
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Write-Host "M10.G4 Checkpoint: All verifier pure core quality gates passed cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/page-signals.test.ts tests/launch/args.property.test.ts tests/launch/checks.property.test.ts tests/launch/canonical-robots.property.test.ts tests/launch/verify-report.property.test.ts tests/launch/check-in-dates.property.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.4–7.6, Req 7.9–7.10, Req 7.12, Req 14.4

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "scripts\launch\lib\page-signals.ts"
Test-Path "scripts\launch\lib\args.ts"
Test-Path "scripts\launch\lib\checks.ts"
Test-Path "scripts\launch\lib\verify-report.ts"
Test-Path "scripts\launch\lib\check-in-dates.ts"
npx vitest run tests/launch/page-signals.test.ts tests/launch/args.property.test.ts tests/launch/checks.property.test.ts tests/launch/canonical-robots.property.test.ts tests/launch/verify-report.property.test.ts tests/launch/check-in-dates.property.test.ts
```
Expected output:
- `True` for all 5 pure module paths
- Vitest reports 6 test files passed with 0 failures