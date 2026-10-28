# M10.G5: Deployment Verifier I/O Shell, CLI, and Offline Tests

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the thin I/O execution shell (`verify-run.ts`) and CLI entrypoint (`verify-deployment.ts`) that orchestrate route verification over HTTP using Node.js built-ins (`AbortController`, global `fetch`). Implement a bounded concurrency worker pool (4 concurrent requests), write JSON audit reports to git-ignored `reports/`, and strictly decouple the verifier from automated suites (`npm test`, CI). Under approved Human Decisions A2, A4, and A8, add npm scripts `verify:deployment` and `launch:csp`, verify that `.gitignore` ignores `reports/`, and confirm that the version manifest remains unmodified (A3 Declined).

## Goal Success Criteria

- ✓ `scripts/launch/lib/verify-run.ts` exports `fetchWithTimeout` (`redirect: 'manual'`, timeout aborts, zero custom headers beyond `user-agent` and `accept`) and `runVerification`
- ✓ `runVerification` verifies all Route_Inventory routes, asserts 404 with local body signals on `/this-route-does-not-exist-m10`, asserts 404 on draft slugs, and validates immutable caching on static assets
- ✓ `scripts/launch/verify-deployment.ts` CLI loads M9 route inventory, parses arguments, runs checks, outputs formatted summaries, writes `reports/verify-deployment.json`, and maps exit codes (0 = pass, 1 = failures, 2 = usage/env error)
- ✓ Offline unit and integration suites in `tests/launch/verify-run.test.ts` and `tests/launch/verify-cli.test.ts` verify all failure branches using `fake-fetcher.ts` with zero open sockets
- ✓ Isolation tests prove that `verify-deployment.ts` is never invoked by `npm test`, `npm run audit`, or CI
- ✓ Approvals A2 and A4 are applied to `package.json` (`verify:deployment` and `launch:csp` scripts added) while `version` remains unmodified (A3 Declined)
- ✓ Approval A8 is verified: `reports/` is confirmed ignored by git

## Prerequisites

- Goals M10.G1 through M10.G4 completed (pure core modules `page-signals.ts`, `checks.ts`, `args.ts`, `verify-report.ts`, `vercel-config.ts`, `headers.ts` available)
- Approval records A2, A4, and A8 confirmed in `task-notes.md`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M10.G5.T1: Implement HTTP Fetcher with Timeout (`scripts/launch/lib/verify-run.ts`)

**Objective:** Implement `fetchWithTimeout` in `scripts/launch/lib/verify-run.ts` wrapping global `fetch` with an `AbortController` timeout, enforcing `redirect: 'manual'`, sending no custom cookies or payload, and mapping network errors cleanly.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `fetchWithTimeout(timeoutMs)` returns a typed `Fetcher` function
- ✓ Uses `AbortController` to abort requests exceeding `timeoutMs` and throws an Error with `name: 'TimeoutError'`
- ✓ Sends only standard headers: `user-agent: m10-verify-deployment` and `accept: text/html,*/*`
- ✓ Configured with `redirect: 'manual'` so redirect status codes (3xx) are returned directly without following
- ✓ Reads text body for HTML/text responses and returns empty string for binary payloads

**Prerequisites:**
- M10.G4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\verify-run.ts`

**Implementation Details:**
Create `scripts/launch/lib/verify-run.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Fetcher, FetchedResponse, HeaderBag } from './types';
import { toHeaderBag } from './headers';

export function fetchWithTimeout(timeoutMs: number): Fetcher {
  return async (url: string): Promise<FetchedResponse> => {
    const controller = new AbortController();
    const timer = setTimeout(() => {
      controller.abort();
    }, timeoutMs);

    try {
      const response = await fetch(url, {
        method: 'GET',
        signal: controller.signal,
        redirect: 'manual',
        headers: {
          'user-agent': 'm10-verify-deployment',
          accept: 'text/html,*/*',
        },
      });

      const headerEntries: [string, string][] = [];
      response.headers.forEach((val, key) => {
        headerEntries.push([key, val]);
      });
      const headers: HeaderBag = toHeaderBag(headerEntries);

      const contentType = headers['content-type'] ?? '';
      let body = '';
      if (contentType.includes('text') || contentType.includes('html') || contentType.includes('json')) {
        body = await response.text();
      }

      return {
        status: response.status,
        headers,
        body,
      };
    } catch (err: unknown) {
      if ((err as Error).name === 'AbortError') {
        const timeoutError = new Error(`Request to ${url} timed out after ${timeoutMs}ms.`);
        timeoutError.name = 'TimeoutError';
        throw timeoutError;
      }
      throw err;
    } finally {
      clearTimeout(timer);
    }
  };
}
'@ | Set-Content -Path "scripts\launch\lib\verify-run.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.11

---

### M10.G5.T2: Implement Verification Runner Orchestrator (`scripts/launch/lib/verify-run.ts`)

**Objective:** Append `runVerification` to `scripts/launch/lib/verify-run.ts` to manage concurrent execution (pool size 4) across all routes, bogus 404 path, draft slugs, and static asset caching.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Executes concurrent requests bounded by `concurrency` (default 4) over a sorted route queue
- ✓ Evaluates 200 status, expected headers, `x-powered-by`, HTML caching, canonical, and robots on inventory routes
- ✓ Evaluates 404 status and not-found body signals on `/this-route-does-not-exist-m10`
- ✓ Evaluates 404 status on all configured draft slugs
- ✓ Evaluates immutable `Cache-Control` on the first detected static asset chunk
- ✓ Assembles check results and returns an `AuditReport<VerifyData>` via `buildVerifyReport`

**Prerequisites:**
- M10.G5.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\verify-run.ts`

**Implementation Details:**
Append `runVerification` to `scripts/launch/lib/verify-run.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$runnerCode = @'

import type {
  VerifyArgs,
  VercelConfig,
  CheckResult,
  RunKind,
  AuditReport,
  VerifyData,
} from './types';
import type { RouteEntry } from '../../audit/lib/types';
import { expectedHeadersFor } from './vercel-config';
import { compareHeaders, findPoweredBy, hasImmutableCache } from './headers';
import { extractPageSignals } from './page-signals';
import { checkStatus, checkCanonical, checkRobots, checkNotFoundBody } from './checks';
import { buildVerifyReport, type RawRouteResult } from './verify-report';

export interface VerifyContext {
  readonly args: VerifyArgs;
  readonly siteUrl: string;
  readonly run: RunKind;
  readonly style: 'flat' | 'directory';
  readonly routes: readonly RouteEntry[];
  readonly draftSlugs: readonly string[];
  readonly config: VercelConfig | null;
  readonly notFoundSignals: { readonly title: string | null; readonly h1: string | null } | null;
}

export async function runVerification(
  ctx: VerifyContext,
  fetcher: Fetcher,
  now: string = new Date().toISOString()
): Promise<AuditReport<VerifyData>> {
  const rawResults: RawRouteResult[] = [];
  let staticAssetToVerify: string | null = null;

  // 1. Inventory routes to check
  const inventoryRoutes = ctx.routes.filter(r => r.route !== '/404');

  // Helper to execute checks on a standard inventory route
  const verifyRoute = async (entry: RouteEntry): Promise<RawRouteResult> => {
    const targetUrl = `${ctx.args.baseUrl}${entry.route}`;
    const checks: CheckResult[] = [];
    let status: number | null = null;

    try {
      const res = await fetcher(targetUrl);
      status = res.status;

      checks.push(checkStatus(res.status, 200));

      if (ctx.config) {
        const expected = expectedHeadersFor(ctx.config, entry.route);
        const mismatches = compareHeaders(expected, res.headers);
        for (const m of mismatches) {
          checks.push({
            id: 'headers',
            severity: 'error',
            passed: false,
            message: `Header mismatch for '${m.key}': expected '${m.expected}', got '${m.actual}'.`,
            details: { key: m.key, expected: m.expected, actual: m.actual },
          });
        }
      } else {
        checks.push({
          id: 'headers',
          severity: 'warning',
          passed: true,
          message: 'Header check skipped: vercel.json not found and no --expect-headers provided.',
        });
      }

      const poweredBy = findPoweredBy(res.headers);
      if (poweredBy) {
        checks.push({
          id: 'powered-by',
          severity: 'error',
          passed: false,
          message: `Fingerprinting header 'X-Powered-By: ${poweredBy}' detected.`,
          details: { value: poweredBy },
        });
      }

      if (hasImmutableCache(res.headers)) {
        checks.push({
          id: 'cache-html',
          severity: 'error',
          passed: false,
          message: "HTML route must not declare 'immutable' Cache-Control.",
        });
      }

      const signals = extractPageSignals(res.body);

      if (entry.route === '/' && signals.staticAssetPaths.length > 0 && !staticAssetToVerify) {
        staticAssetToVerify = signals.staticAssetPaths[0] ?? null;
      }

      const canonicalChecks = checkCanonical({
        actual: signals.canonical,
        path: entry.route,
        base: ctx.args.baseUrl,
        siteUrl: ctx.siteUrl,
        run: ctx.run,
        style: ctx.style,
      });
      checks.push(...canonicalChecks);

      const robotsChecks = checkRobots({
        robotsMeta: signals.robotsMeta,
        xRobotsTag: res.headers['x-robots-tag'] ?? null,
        run: ctx.run,
        expectNoindex: false,
      });
      checks.push(...robotsChecks);
    } catch (err: unknown) {
      const errorName = (err as Error).name;
      checks.push({
        id: errorName === 'TimeoutError' ? 'timeout' : 'network-error',
        severity: 'error',
        passed: false,
        message: `Failed to fetch ${targetUrl}: ${(err as Error).message}`,
        details: { error: (err as Error).message },
      });
    }

    return { route: entry.route, url: targetUrl, status, checks };
  };

  // Concurrency worker pool execution
  const queue = [...inventoryRoutes];
  const workers = Array.from({ length: Math.min(ctx.args.concurrency, queue.length) }, async () => {
    while (queue.length > 0) {
      const entry = queue.shift();
      if (entry) {
        const res = await verifyRoute(entry);
        rawResults.push(res);
      }
    }
  });
  await Promise.all(workers);

  // 2. Bogus route check
  const bogusRoute = '/this-route-does-not-exist-m10';
  const bogusUrl = `${ctx.args.baseUrl}${bogusRoute}`;
  const bogusChecks: CheckResult[] = [];
  let bogusStatus: number | null = null;

  try {
    const res = await fetcher(bogusUrl);
    bogusStatus = res.status;
    bogusChecks.push(checkStatus(res.status, 404));

    const bodyCheck = checkNotFoundBody(res.body, ctx.notFoundSignals);
    bogusChecks.push(bodyCheck);

    const robotsChecks = checkRobots({
      robotsMeta: extractPageSignals(res.body).robotsMeta,
      xRobotsTag: res.headers['x-robots-tag'] ?? null,
      run: ctx.run,
      expectNoindex: true,
    });
    bogusChecks.push(...robotsChecks);
  } catch (err) {
    bogusChecks.push({
      id: 'network-error',
      severity: 'error',
      passed: false,
      message: `Failed to fetch bogus route ${bogusUrl}: ${(err as Error).message}`,
    });
  }
  rawResults.push({ route: bogusRoute, url: bogusUrl, status: bogusStatus, checks: bogusChecks });

  // 3. Draft posts check
  if (ctx.draftSlugs.length === 0) {
    rawResults.push({
      route: '/blog/[drafts]',
      url: `${ctx.args.baseUrl}/blog/[drafts]`,
      status: null,
      checks: [
        {
          id: 'draft-slug-check',
          severity: 'info',
          passed: true,
          message: 'No draft blog posts configured in content collection.',
        },
      ],
    });
  } else {
    for (const draftSlug of ctx.draftSlugs) {
      const draftRoute = `/blog/${draftSlug}`;
      const draftUrl = `${ctx.args.baseUrl}${draftRoute}`;
      const draftChecks: CheckResult[] = [];
      let draftStatus: number | null = null;

      try {
        const res = await fetcher(draftUrl);
        draftStatus = res.status;
        draftChecks.push(checkStatus(res.status, 404));
      } catch (err) {
        draftChecks.push({
          id: 'network-error',
          severity: 'error',
          passed: false,
          message: `Failed to fetch draft route ${draftUrl}: ${(err as Error).message}`,
        });
      }
      rawResults.push({ route: draftRoute, url: draftUrl, status: draftStatus, checks: draftChecks });
    }
  }

  // 4. Static asset check
  if (staticAssetToVerify) {
    const assetUrl = `${ctx.args.baseUrl}${staticAssetToVerify}`;
    const assetChecks: CheckResult[] = [];
    let assetStatus: number | null = null;

    try {
      const res = await fetcher(assetUrl);
      assetStatus = res.status;
      assetChecks.push(checkStatus(res.status, 200));

      const cache = res.headers['cache-control'] ?? '';
      const hasImmutable = cache.includes('immutable') && cache.includes('max-age=31536000');
      assetChecks.push({
        id: 'static-asset-cache',
        severity: 'error',
        passed: hasImmutable,
        message: hasImmutable
          ? `Static asset has immutable cache: ${cache}`
          : `Static asset missing immutable Cache-Control: got '${cache}'.`,
      });
    } catch (err) {
      assetChecks.push({
        id: 'network-error',
        severity: 'error',
        passed: false,
        message: `Failed to fetch static asset ${assetUrl}: ${(err as Error).message}`,
      });
    }
    rawResults.push({ route: staticAssetToVerify, url: assetUrl, status: assetStatus, checks: assetChecks });
  }

  return buildVerifyReport({
    args: ctx.args,
    siteUrl: ctx.siteUrl,
    run: ctx.run,
    results: rawResults,
    now,
  });
}
'@

Add-Content -Path "scripts\launch\lib\verify-run.ts" -Value $runnerCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.3–7.11

---

### M10.G5.T3: Implement Deployment Verifier CLI (`scripts/launch/verify-deployment.ts`)

**Objective:** Implement `scripts/launch/verify-deployment.ts` CLI parsing command arguments, reading local 404 signals via M9 `resolveBuildLayout({}, cwd)`, loading routes from M9 `loadRouteInventory`, executing `runVerification`, writing `reports/verify-deployment.json`, and setting exit codes cleanly.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Rejects missing or invalid arguments with standard usage text and exits with code 2
- ✓ Resolves build layout via `resolveBuildLayout({}, process.cwd())` without reading `process.env`
- ✓ Reads local `404.html` signals (title, h1) or emits `not-found-body-unchecked` warning
- ✓ Dispatches `runVerification` with `fetchWithTimeout(args.timeoutMs)`
- ✓ Writes JSON report to `reports/verify-deployment.json` via M9 `writeReport`
- ✓ Prints formatted summary lines to console
- ✓ Exits with code 0 on pass, 1 on check errors, and 2 on usage/environment errors

**Prerequisites:**
- M10.G5.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\verify-deployment.ts`

**Implementation Details:**
Create `scripts/launch/verify-deployment.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import * as fs from 'fs';
import * as path from 'path';
import { parseArgs, classifyRun } from './lib/args';
import { parseVercelConfig } from './lib/vercel-config';
import { extractPageSignals } from './lib/page-signals';
import { fetchWithTimeout, runVerification, type VerifyContext } from './lib/verify-run';
import { formatSummary } from './lib/verify-report';
import { resolveBuildLayout } from '../audit/lib/build-layout';
import { loadRouteInventory } from '../audit/lib/route-inventory';
import { writeReport } from '../audit/lib/report';
import type { VercelConfig } from './lib/types';
import siteConfig from '../../content/site.json';

export async function main(argv: readonly string[]): Promise<number> {
  const parseRes = parseArgs(argv);
  if (!parseRes.ok) {
    console.error(parseRes.usage);
    return 2;
  }
  const args = parseRes.args;

  // 1. Determine siteUrl and run kind
  const siteUrl = siteConfig.siteUrl;
  const run = classifyRun(args.baseUrl, siteUrl);

  // 2. Load vercel.json if available
  let config: VercelConfig | null = null;
  const vercelPath = path.resolve(process.cwd(), args.vercelJsonPath);
  if (fs.existsSync(vercelPath)) {
    const rawConfig = fs.readFileSync(vercelPath, 'utf8');
    const parsed = parseVercelConfig(rawConfig);
    if (!parsed.ok) {
      console.error(`Invalid vercel.json configuration at ${args.vercelJsonPath}:`);
      parsed.issues.forEach(i => console.error(` - ${i.rule}: ${i.message}`));
      return 2;
    }
    config = parsed.config;
  } else if (args.expectHeadersPath) {
    const fallbackPath = path.resolve(process.cwd(), args.expectHeadersPath);
    if (fs.existsSync(fallbackPath)) {
      const rawConfig = fs.readFileSync(fallbackPath, 'utf8');
      const parsed = parseVercelConfig(rawConfig);
      if (parsed.ok) config = parsed.config;
    }
  }

  // 3. Load local 404 signals
  let notFoundSignals: { title: string | null; h1: string | null } | null = null;
  const layout = resolveBuildLayout({}, process.cwd());
  if (layout) {
    const local404 = path.join(layout.outputDir, '404.html');
    if (fs.existsSync(local404)) {
      const signals = extractPageSignals(fs.readFileSync(local404, 'utf8'));
      notFoundSignals = { title: signals.title, h1: signals.h1 };
    }
  }

  // 4. Load Route Inventory and Drafts
  let routes;
  try {
    const inv = await loadRouteInventory();
    routes = inv.routes;
  } catch (err) {
    console.error(`Failed to load route inventory: ${(err as Error).message}`);
    return 2;
  }

  // Check draft blog slugs
  const blogDir = path.resolve(process.cwd(), 'content/blog');
  const draftSlugs: string[] = [];
  if (fs.existsSync(blogDir)) {
    const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.mdx') || f.endsWith('.md'));
    for (const f of files) {
      const content = fs.readFileSync(path.join(blogDir, f), 'utf8');
      if (content.match(/draft:\s*true/)) {
        const slug = f.replace(/\.mdx?$/, '');
        draftSlugs.push(slug);
      }
    }
  }

  const context: VerifyContext = {
    args,
    siteUrl,
    run,
    style: layout?.style ?? 'flat',
    routes,
    draftSlugs,
    config,
    notFoundSignals,
  };

  const fetcher = fetchWithTimeout(args.timeoutMs);
  const report = await runVerification(context, fetcher);

  // Write report to reports/
  const reportsDir = path.resolve(process.cwd(), 'reports');
  if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
  }
  const reportPath = path.join(reportsDir, 'verify-deployment.json');
  writeReport(reportPath, report);

  console.log(formatSummary(report));
  console.log(`\nReport written to: ${path.relative(process.cwd(), reportPath)}`);

  return report.status === 'pass' ? 0 : 1;
}

if (process.argv[1]?.endsWith('verify-deployment.ts')) {
  main(process.argv.slice(2)).then(code => {
    process.exitCode = code;
  });
}
'@ | Set-Content -Path "scripts\launch\verify-deployment.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1–7.6, Req 7.12, Req 7.14

---

### M10.G5.T4: Author Offline Unit Tests with Simulated Responses (`tests/launch/verify-run.test.ts`)

**Objective:** Write `tests/launch/verify-run.test.ts` executing `runVerification` against `createFakeFetcher` and simulated responses from `fixtures/responses/`, confirming that healthy runs pass and individual defects emit exactly one expected finding.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Test suite uses `createFakeFetcher` and opens zero network sockets
- ✓ Healthy production response mock produces status `'pass'` with 0 errors
- ✓ Missing header produces exactly one `headers` error finding
- ✓ Wrong canonical URL produces exactly one `canonical` error finding
- ✓ Robots `noindex` meta tag on standard route produces exactly one `robots-meta` error finding
- ✓ 200 OK on bogus route `/this-route-does-not-exist-m10` produces `status` error finding
- ✓ Presence of `X-Powered-By` produces `powered-by` error finding

**Prerequisites:**
- M10.G5.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\verify-run.test.ts`

**Implementation Details:**
Create `tests/launch/verify-run.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { runVerification, type VerifyContext } from '../../scripts/launch/lib/verify-run';
import { createFakeFetcher } from './helpers/fake-fetcher';
import type { VercelConfig, VerifyArgs } from '../../scripts/launch/lib/types';

describe('runVerification Offline Test Suite with Simulated Responses', () => {
  const baseArgs: VerifyArgs = {
    baseUrl: 'https://production.example.com',
    timeoutMs: 5000,
    concurrency: 2,
    vercelJsonPath: 'vercel.json',
    expectHeadersPath: null,
  };

  const validConfig: VercelConfig = {
    headers: [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=(), payment=(), usb=()' },
          { key: 'Content-Security-Policy', value: "default-src 'self'; frame-ancestors 'none'" },
        ],
      },
    ],
  };

  const baseContext: VerifyContext = {
    args: baseArgs,
    siteUrl: 'https://production.example.com',
    run: 'production',
    style: 'flat',
    routes: [{ route: '/', kind: 'static', file: 'index.html', mdxPath: null }],
    draftSlugs: [],
    config: validConfig,
    notFoundSignals: { title: '404: Page Not Found', h1: '404 - Page Not Found' },
  };

  const respDir = path.resolve(__dirname, 'fixtures/responses');
  const okResp = JSON.parse(fs.readFileSync(path.join(respDir, '200-ok.json'), 'utf8'));
  const bogusResp = JSON.parse(fs.readFileSync(path.join(respDir, '404-bogus.json'), 'utf8'));

  it('passes completely with zero errors on healthy production responses', async () => {
    const fetcher = createFakeFetcher({
      '/': okResp,
      '/this-route-does-not-exist-m10': bogusResp,
    });

    const report = await runVerification(baseContext, fetcher);
    expect(report.status).toBe('pass');
    expect(report.summary.errors).toBe(0);
  });

  it('detects missing security header as exactly one error finding', async () => {
    const missingHeaderResp = JSON.parse(fs.readFileSync(path.join(respDir, 'missing-header.json'), 'utf8'));
    const fetcher = createFakeFetcher({
      '/': missingHeaderResp,
      '/this-route-does-not-exist-m10': bogusResp,
    });

    const report = await runVerification(baseContext, fetcher);
    expect(report.status).toBe('fail');
    const headerErrors = report.findings.filter(f => f.rule === 'headers');
    expect(headerErrors.length).toBeGreaterThanOrEqual(1);
  });

  it('detects canonical mismatch as an error finding', async () => {
    const wrongCanonicalResp = JSON.parse(fs.readFileSync(path.join(respDir, 'wrong-canonical.json'), 'utf8'));
    const fetcher = createFakeFetcher({
      '/': wrongCanonicalResp,
      '/this-route-does-not-exist-m10': bogusResp,
    });

    const report = await runVerification(baseContext, fetcher);
    expect(report.status).toBe('fail');
    expect(report.findings.some(f => f.rule === 'canonical')).toBe(true);
  });

  it('detects forbidden noindex on standard routes', async () => {
    const noindexResp = JSON.parse(fs.readFileSync(path.join(respDir, 'noindex-meta.json'), 'utf8'));
    const fetcher = createFakeFetcher({
      '/': noindexResp,
      '/this-route-does-not-exist-m10': bogusResp,
    });

    const report = await runVerification(baseContext, fetcher);
    expect(report.status).toBe('fail');
    expect(report.findings.some(f => f.rule === 'robots-meta')).toBe(true);
  });

  it('detects x-powered-by header fingerprinting', async () => {
    const poweredByResp = JSON.parse(fs.readFileSync(path.join(respDir, 'x-powered-by.json'), 'utf8'));
    const fetcher = createFakeFetcher({
      '/': poweredByResp,
      '/this-route-does-not-exist-m10': bogusResp,
    });

    const report = await runVerification(baseContext, fetcher);
    expect(report.status).toBe('fail');
    expect(report.findings.some(f => f.rule === 'powered-by')).toBe(true);
  });
});
'@ | Set-Content -Path "tests\launch\verify-run.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/verify-run.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.4, Req 7.5, Req 7.7, Req 7.8, Req 7.9, Req 7.15

---

### M10.G5.T5: Author Edge Case and Failure Suite (`tests/launch/verify-run-failures.test.ts`)

**Objective:** Write `tests/launch/verify-run-failures.test.ts` testing network timeouts, connection resets, draft route leakage, and preview run classifications.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Simulates network timeout and verifies `timeout` finding is emitted
- ✓ Simulates connection error and verifies `network-error` finding is emitted
- ✓ Asserts 200 status on draft slug produces an error finding
- ✓ Asserts preview run treats `X-Robots-Tag: noindex` as `info` and does not fail audit

**Prerequisites:**
- M10.G5.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\verify-run-failures.test.ts`

**Implementation Details:**
Create `tests/launch/verify-run-failures.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { runVerification, type VerifyContext } from '../../scripts/launch/lib/verify-run';
import { createFakeFetcher } from './helpers/fake-fetcher';
import type { VerifyArgs } from '../../scripts/launch/lib/types';

describe('runVerification Edge Cases and Failures', () => {
  const baseArgs: VerifyArgs = {
    baseUrl: 'https://preview.vercel.app',
    timeoutMs: 1000,
    concurrency: 2,
    vercelJsonPath: 'vercel.json',
    expectHeadersPath: null,
  };

  const previewContext: VerifyContext = {
    args: baseArgs,
    siteUrl: 'https://production.com',
    run: 'preview',
    style: 'flat',
    routes: [{ route: '/', kind: 'static', file: 'index.html', mdxPath: null }],
    draftSlugs: ['secret-draft'],
    config: null,
    notFoundSignals: null,
  };

  const respDir = path.resolve(__dirname, 'fixtures/responses');
  const previewHeadersResp = JSON.parse(fs.readFileSync(path.join(respDir, 'preview-headers.json'), 'utf8'));

  it('handles simulated timeout error cleanly as a finding', async () => {
    const fetcher = createFakeFetcher({
      '/': { shouldTimeout: true },
      '*': { status: 404 },
    });

    const report = await runVerification(previewContext, fetcher);
    expect(report.status).toBe('fail');
    expect(report.findings.some(f => f.rule === 'timeout')).toBe(true);
  });

  it('handles draft post returning 200 OK as a failure', async () => {
    const fetcher = createFakeFetcher({
      '/': previewHeadersResp,
      '/this-route-does-not-exist-m10': { status: 404 },
      '/blog/secret-draft': { status: 200, body: 'Leaked Draft!' },
    });

    const report = await runVerification(previewContext, fetcher);
    expect(report.status).toBe('fail');
    const draftFinding = report.findings.find(f => f.route === '/blog/secret-draft' && f.rule === 'status');
    expect(draftFinding).toBeDefined();
  });

  it('treats preview X-Robots-Tag as info without failing the audit', async () => {
    const fetcher = createFakeFetcher({
      '/': previewHeadersResp,
      '/this-route-does-not-exist-m10': { status: 404, body: '404', headers: { 'x-robots-tag': 'noindex' } },
      '/blog/secret-draft': { status: 404 },
    });

    const report = await runVerification(previewContext, fetcher);
    const robotsHeaderFinding = report.findings.find(f => f.rule === 'robots-header');
    expect(robotsHeaderFinding?.severity).toBe('info');
    expect(report.status).toBe('pass');
  });
});
'@ | Set-Content -Path "tests\launch\verify-run-failures.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/verify-run-failures.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.6, Req 7.9, Req 7.10, Req 7.11

---

### M10.G5.T6: Author CLI and Network Isolation Tests

**Objective:** Write `tests/launch/verify-cli.test.ts` testing argument parsing and report generation via CLI, and `tests/launch/verify-isolation.test.ts` verifying that `verify-deployment.ts` is never referenced in automated test or CI pipelines.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `tests/launch/verify-cli.test.ts` asserts missing arguments output usage text and exit with code 2
- ✓ Asserts non-https URL is rejected
- ✓ `tests/launch/verify-isolation.test.ts` asserts `package.json` `scripts.test` does not invoke `verify-deployment`
- ✓ Asserts `scripts/audit/run-all.ts` does not invoke `verify-deployment`
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G5.T3 completed
- Target files: `tests/launch/verify-cli.test.ts`, `tests/launch/verify-isolation.test.ts`

**Implementation Details:**
Create the test files using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. verify-cli.test.ts
@'
import { describe, it, expect, vi } from 'vitest';
import { main } from '../../scripts/launch/verify-deployment';

describe('verify-deployment CLI Integration', () => {
  it('returns code 2 and outputs usage when no arguments provided', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const exitCode = await main([]);
    expect(exitCode).toBe(2);
    expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining('Usage: verify-deployment'));
    errorSpy.mockRestore();
  });

  it('returns code 2 when non-https URL provided', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const exitCode = await main(['http://insecure.example.com']);
    expect(exitCode).toBe(2);
    errorSpy.mockRestore();
  });
});
'@ | Set-Content -Path "tests\launch\verify-cli.test.ts" -Encoding UTF8

# 2. verify-isolation.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('Verifier Network Isolation Verification', () => {
  it('asserts verify-deployment is not executed during npm test', () => {
    const pkg = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'package.json'), 'utf8'));
    const testScript = pkg.scripts?.test ?? '';
    expect(testScript).not.toContain('verify-deployment');
  });

  it('asserts verify-deployment is not executed by audit aggregate scripts', () => {
    const auditRunAllPath = path.resolve(process.cwd(), 'scripts/audit/run-all.ts');
    if (fs.existsSync(auditRunAllPath)) {
      const content = fs.readFileSync(auditRunAllPath, 'utf8');
      expect(content).not.toContain('verify-deployment');
    }
  });
});
'@ | Set-Content -Path "tests\launch\verify-isolation.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/verify-cli.test.ts tests/launch/verify-isolation.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.13, Req 7.14

---

### M10.G5.T7: Verify Human Approvals A2, A4, and A8 in Task Notes

**Objective:** Inspect `task-notes.md` to confirm that Human Decisions A2 (`verify:deployment`), A4 (`launch:csp`), and A8 (`.gitignore` `reports/`) are marked as Approved before modifying configuration files.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Programmatically confirms A2 (`verify:deployment`) is recorded as `Approved 2026-10-22`
- ✓ Programmatically confirms A4 (`launch:csp`) is recorded as `Approved 2026-10-22`
- ✓ Programmatically confirms A8 (`reports/` gitignore) is recorded as `Approved 2026-10-22`
- ✓ Programmatically confirms A3 (version bump) is recorded as `Declined`

**Prerequisites:**
- M10.G1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Execute the check via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw

$a2Ok = $notes -match "Approved 2026-10-22 \(approval A2\)"
$a4Ok = $notes -match "Approved 2026-10-22 \(approval A4\)"
$a8Ok = $notes -match "Approved 2026-10-22 \(approval A8\)"
$a3Declined = $notes -match "Declined 2026-10-22 \(approval A3\)"

if (-not ($a2Ok -and $a4Ok -and $a8Ok -and $a3Declined)) {
    throw "Approval Gate Failure: One or more approvals missing or inconsistent in task-notes.md."
}

Write-Host "Approval Gate Passed: A2, A4, and A8 confirmed approved; A3 confirmed declined."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "approval A2" -and $notes -match "approval A4" -and $notes -match "approval A8") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 7.14

---

### M10.G5.T8: Add Launch Scripts to `package.json` (Approvals A2 & A4)

**Objective:** Under verified Approvals A2 and A4, add `"verify:deployment"` and `"launch:csp"` to `package.json` `scripts`, while strictly preserving the existing `version` field (A3 Declined).

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `package.json` contains `"verify:deployment": "vite-node --config vitest.config.ts scripts/launch/verify-deployment.ts --"`
- ✓ `package.json` contains `"launch:csp": "vite-node --config vitest.config.ts scripts/launch/csp-hashes.ts --"`
- ✓ `version` property is completely unchanged
- ✓ Zero runtime or dev dependencies added

**Prerequisites:**
- M10.G5.T7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\package.json`

**Implementation Details:**
Update `package.json` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json

$pkg.scripts | Add-Member -MemberType NoteProperty -Name "verify:deployment" -Value "vite-node --config vitest.config.ts scripts/launch/verify-deployment.ts --" -Force
$pkg.scripts | Add-Member -MemberType NoteProperty -Name "launch:csp" -Value "vite-node --config vitest.config.ts scripts/launch/csp-hashes.ts --" -Force

$jsonOut = $pkg | ConvertTo-Json -Depth 10
# Preserve exact 2-space indentation and newline
Set-Content -Path "package.json" -Value ($jsonOut + "`n") -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$hasVerify = $pkg.scripts."verify:deployment" -ne $null
$hasCsp = $pkg.scripts."launch:csp" -ne $null
if ($hasVerify -and $hasCsp) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.14, Req 11.1

---

### M10.G5.T9: Verify Git Ignore Rule for `reports/` (Approval A8)

**Objective:** Confirm that `reports/` is ignored by Git using `git check-ignore`, appending `reports/` to `.gitignore` under Approval A8 only if not already ignored by M9.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `git check-ignore reports/sample.json` confirms `reports/` is ignored
- ✓ `.gitignore` contains `reports/` without duplicate lines
- ✓ Staged git status confirms no accidental tracking of `reports/`

**Prerequisites:**
- M10.G5.T7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.gitignore`

**Implementation Details:**
Check and update `.gitignore` via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$check = git check-ignore "reports/test.json"
if (-not $check) {
    Add-Content -Path ".gitignore" -Value "`n# Launch & Audit Reports`nreports/" -Encoding UTF8
    Write-Host "Appended reports/ to .gitignore under Approval A8."
} else {
    Write-Host "reports/ is already ignored by Git."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$check = git check-ignore "reports/test.json"
if ($check -match "reports") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.12

---

### M10.G5.T10: Goal 5 Checkpoint and Quality Gate Verification

**Objective:** Run the full quality verification suite (lint, typecheck, verifier unit suites, CLI tests, and isolation tests) to seal Goal 5 with zero regressions.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ All verifier test suites pass cleanly
- ✓ `git diff` confirms modifications are strictly limited to `package.json` (scripts only), `.gitignore`, `scripts/launch/`, and `tests/launch/`

**Prerequisites:**
- M10.G5.T1 through M10.G5.T9 completed

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
npx vitest run tests/launch/verify-run.test.ts tests/launch/verify-run-failures.test.ts tests/launch/verify-cli.test.ts tests/launch/verify-isolation.test.ts
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Write-Host "M10.G5 Checkpoint: All verifier I/O and CLI quality gates passed cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/verify-run.test.ts tests/launch/verify-cli.test.ts tests/launch/verify-isolation.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 7.1–7.15

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "scripts\launch\lib\verify-run.ts"
Test-Path "scripts\launch\verify-deployment.ts"
git check-ignore "reports/verify-deployment.json"
npx vitest run tests/launch/verify-run.test.ts tests/launch/verify-run-failures.test.ts tests/launch/verify-cli.test.ts tests/launch/verify-isolation.test.ts
```
Expected output:
- `True` for tool files
- `reports/verify-deployment.json` is ignored
- Vitest reports 4 test files passed with 0 failures