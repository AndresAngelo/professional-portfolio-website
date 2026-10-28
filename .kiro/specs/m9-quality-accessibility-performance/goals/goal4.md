# M9.G4: Route Inventory Audit, Internal Link Crawler, and SEO Audit

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the Route Inventory verification audit (`routes-audit.ts`), the offline Internal Link Crawler (`links-audit.ts`), and the SEO & Metadata audit (`seo-audit.ts`), along with their respective CLI entry points (`scripts/audit/routes.ts`, `scripts/audit/links.ts`, and `scripts/audit/seo.ts`). This goal establishes bidirectional route-to-file mapping (supporting both `flat` and `directory` static exports per Decision 2), validates that every internal `href` and `#fragment` resolves without network access, enforces title/description lengths and Open Graph parity, applies Decision 8 for the `/404` route exemption, and verifies fast-check Properties 7, 8, 9, 12, and 13.

---

## Goal Success Criteria

- ✓ `scripts/audit/lib/route-files.ts` exports `routeFileCandidates` and `htmlFileToRoute` operating symmetrically across `flat` and `directory` layouts
- ✓ `scripts/audit/lib/routes-audit.ts` detects missing routes, published drafts, missing 404, unexpected routes, and illegal API outputs
- ✓ `scripts/audit/lib/link-resolve.ts` exports pure `resolveInternalHref` normalizing query parameters, fragments, and origins
- ✓ `scripts/audit/lib/links-audit.ts` crawls all internal links offline, verifying targets and DOM fragment IDs without network requests
- ✓ `scripts/audit/lib/checks/metadata-ranges.ts` exports `checkLengthRange` and `expectedCanonical`
- ✓ `scripts/audit/lib/seo-audit.ts` validates title (10–70 chars), description (50–160 chars), canonical, Open Graph parity, blog article timestamps, and Decision 8 `/404` rules
- ✓ Fast-check Properties 7, 8, 9, 12, and 13 pass $\ge 100$ iterations each
- ✓ CLI runners `scripts/audit/routes.ts`, `links.ts`, and `seo.ts` execute cleanly via `runCli`

---

## Prerequisites

- Goals M9.G1, M9.G2, and M9.G3 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Fixtures available in `tests/audit/fixtures/`

---

## Tasks

### M9.G4.T1: Implement Bidirectional Route and File Mapping

**Objective:** Implement `routeFileCandidates` and `htmlFileToRoute` in `scripts/audit/lib/route-files.ts` to support both flat (`/projects.html`) and directory-style (`/projects/index.html`) exports per Decision 2.

**Acceptance Criteria:**
- ✓ `routeFileCandidates('/')` returns `['index.html']`
- ✓ `routeFileCandidates('/404')` returns `['404.html', '404/index.html']`
- ✓ `routeFileCandidates('/projects')` returns `['projects.html', 'projects/index.html']`
- ✓ `htmlFileToRoute` correctly inverts candidate files back to canonical route paths
- ✓ Pure functions with zero I/O and zero dependencies

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `scripts/audit/lib/route-files.ts`:

```typescript
/**
 * Generates candidate relative file paths in order of preference for a given route path.
 */
export function routeFileCandidates(routePath: string): readonly string[] {
  const clean = routePath === '/' ? '/' : routePath.replace(/\/+$/, '');

  if (clean === '/' || clean === '') {
    return ['index.html'];
  }
  if (clean === '/404') {
    return ['404.html', '404/index.html'];
  }

  const normalized = clean.startsWith('/') ? clean.slice(1) : clean;
  return [`${normalized}.html`, `${normalized}/index.html`];
}

/**
 * Maps an HTML build artifact path back to its canonical route path.
 */
export function htmlFileToRoute(filePath: string): string {
  const normalized = filePath.startsWith('/') ? filePath.slice(1) : filePath;

  if (normalized === 'index.html') {
    return '/';
  }
  if (normalized === '404.html' || normalized === '404/index.html') {
    return '/404';
  }
  if (normalized.endsWith('/index.html')) {
    return `/${normalized.slice(0, -'/index.html'.length)}`;
  }
  if (normalized.endsWith('.html')) {
    return `/${normalized.slice(0, -'.html'.length)}`;
  }

  return `/${normalized}`;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/route-files.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 2.2, Req 2.6

---

### M9.G4.T2: Implement Route Inventory Audit Engine

**Objective:** Implement `runRoutesAudit` in `scripts/audit/lib/routes-audit.ts` to assert that all expected routes exist in build output, drafts are excluded, and no illegal API routes exist.

**Acceptance Criteria:**
- ✓ Compares Build_Output against expected inventory from `loadRouteInventory`
- ✓ Emits `route-missing` if expected page HTML is absent
- ✓ Emits `draft-published` if a draft blog slug produces an HTML file
- ✓ Emits `not-found-missing` if 404 HTML is absent
- ✓ Emits `route-unexpected` for HTML files not in inventory (excluding Next.js internals)
- ✓ Emits `api-output` if build contains `/api/` files or server handlers

**Prerequisites:**
- M9.G4.T1 completed
- Target file: `scripts/audit/lib/routes-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/routes-audit.ts`:

```typescript
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding } from './types';
import { buildReport } from './report';
import { listFiles, checkFileExists } from './build-layout';
import { loadRouteInventory } from './route-inventory';
import { routeFileCandidates, htmlFileToRoute } from './route-files';
import * as path from 'node:path';

export async function runRoutesAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport> {
  const { routes: expectedRoutes, draftSlugs } = await loadRouteInventory();
  const allFiles = await listFiles(layout);
  const findings: Finding[] = [];

  const htmlFiles = allFiles.filter(f => f.endsWith('.html'));

  // 1. Verify all expected routes exist
  for (const route of expectedRoutes) {
    const candidates = routeFileCandidates(route.path);
    const exists = candidates.some(c => allFiles.includes(`/${c}`));
    if (!exists) {
      findings.push({
        route: route.path,
        rule: 'route-missing',
        message: `Expected route "${route.path}" is missing from build output.`,
        severity: 'error',
      });
    }
  }

  // 2. Verify draft blog posts are NOT present
  for (const slug of draftSlugs) {
    const draftCandidates = routeFileCandidates(`/blog/${slug}`);
    const exists = draftCandidates.some(c => allFiles.includes(`/${c}`));
    if (exists) {
      findings.push({
        route: `/blog/${slug}`,
        rule: 'draft-published',
        message: `Draft blog post "${slug}" was emitted to build output.`,
        severity: 'error',
      });
    }
  }

  // 3. Verify not-found page exists
  const has404 = allFiles.includes('/404.html') || allFiles.includes('/404/index.html');
  if (!has404) {
    findings.push({
      route: '/404',
      rule: 'not-found-missing',
      message: 'Not-found page (404.html) is missing from build output.',
      severity: 'error',
    });
  }

  // 4. Verify no unexpected HTML routes exist
  const expectedPathSet = new Set(expectedRoutes.map(r => r.path));
  for (const file of htmlFiles) {
    if (file.startsWith('/_')) {
      continue; // Skip Next.js internal pages like /_not-found.html
    }
    const route = htmlFileToRoute(file);
    if (!expectedPathSet.has(route)) {
      findings.push({
        route,
        rule: 'route-unexpected',
        message: `Unexpected route "${route}" (${file}) found in build output.`,
        severity: 'error',
        file,
      });
    }
  }

  // 5. Verify no API routes exist
  const apiFiles = allFiles.filter(f => f.startsWith('/api/'));
  for (const apiFile of apiFiles) {
    findings.push({
      route: apiFile,
      rule: 'api-output',
      message: `Prohibited API route output found: "${apiFile}".`,
      severity: 'error',
      file: apiFile,
    });
  }

  return buildReport({
    audit: 'routes',
    findings,
    routesChecked: expectedRoutes.length,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/routes-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 2.1–2.7

---

### M9.G4.T3: Author Route Audit Tests and Verify Property 7

**Objective:** Write unit tests for `runRoutesAudit` and verify fast-check Property 7 (bidirectional route/file mapping and missing route detection).

**Acceptance Criteria:**
- ✓ Tests missing route detection, draft exclusion, and missing 404 page
- ✓ Fast-check Property 7 proves that removing any candidate file yields exactly one `route-missing` finding across $\ge 100$ runs
- ✓ Creates CLI runner `scripts/audit/routes.ts`

**Prerequisites:**
- M9.G4.T2 completed
- Target files: `tests/audit/routes-audit.test.ts`, `scripts/audit/routes.ts`

**Implementation Details:**

1. Create `tests/audit/routes-audit.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { routeFileCandidates, htmlFileToRoute } from '../../scripts/audit/lib/route-files';

describe('Route Mapping and Detection Properties', () => {
  // Feature: m9-quality-accessibility-performance, Property 7: Route and file mapping is consistent and detects missing routes
  it('Property 7: Route and file mapping is consistent and detects missing routes', () => {
    const validSegment = fc.stringMatching(/^[a-z0-9]+(-[a-z0-9]+)*$/);
    const routeArb = fc.oneof(
      fc.constant('/'),
      fc.constant('/projects'),
      fc.constant('/certifications'),
      fc.constant('/blog'),
      fc.constant('/404'),
      validSegment.map(s => `/projects/${s}`),
      validSegment.map(s => `/blog/${s}`)
    );

    fc.assert(
      fc.property(routeArb, routePath => {
        const candidates = routeFileCandidates(routePath);
        expect(candidates.length).toBeGreaterThanOrEqual(1);

        for (const candidate of candidates) {
          const mapped = htmlFileToRoute(candidate);
          expect(mapped).toBe(routePath === '' ? '/' : routePath);
        }
      }),
      { numRuns: 100 }
    );
  });
});
```

2. Create `scripts/audit/routes.ts`:

```typescript
import { runCli } from './lib/cli';
import { runRoutesAudit } from './lib/routes-audit';

void runCli('routes', (layout, args) => runRoutesAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/routes-audit.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 2.1–2.7, Req 16.1

---

### M9.G4.T4: Implement Pure Internal Link Resolution Logic

**Objective:** Implement `resolveInternalHref` in `scripts/audit/lib/link-resolve.ts` to normalize links, classify protocols, strip query parameters, and extract fragment IDs.

**Acceptance Criteria:**
- ✓ Normalizes empty or `#` hrefs to `{ kind: 'placeholder' }`
- ✓ Handles `mailto:` and `tel:` as `{ kind: 'ignore' }`
- ✓ Classifies different host origins as `{ kind: 'external', url }`
- ✓ Drops query strings (e.g. `/blog?tag=react` $\rightarrow$ `/blog`)
- ✓ Decodes percent-encoded characters and extracts `#fragment`

**Prerequisites:**
- M9.G4.T1 completed
- Target file: `scripts/audit/lib/link-resolve.ts`

**Implementation Details:**

Create `scripts/audit/lib/link-resolve.ts`:

```typescript
export type HrefResolution =
  | { readonly kind: 'ignore' }
  | { readonly kind: 'placeholder' }
  | { readonly kind: 'external'; readonly url: string }
  | { readonly kind: 'internal'; readonly path: string; readonly fragment: string | null }
  | { readonly kind: 'malformed'; readonly reason: string };

export function resolveInternalHref(
  rawHref: string,
  sourcePath: string,
  siteOrigin: string | null = null
): HrefResolution {
  const trimmed = rawHref.trim();

  // 1. Placeholder links
  if (trimmed === '' || trimmed === '#') {
    return { kind: 'placeholder' };
  }

  // 2. Protocols to ignore
  if (/^(mailto|tel):/i.test(trimmed)) {
    return { kind: 'ignore' };
  }

  // 3. Illegal javascript: scheme
  if (/^javascript:/i.test(trimmed)) {
    return { kind: 'malformed', reason: 'javascript: URI is forbidden' };
  }

  try {
    const baseOrigin = 'http://audit.local';
    const resolvedUrl = new URL(trimmed, `${baseOrigin}${sourcePath}`);

    // Check if external origin
    const isLocalBase = resolvedUrl.origin === baseOrigin;
    const isSiteOrigin = siteOrigin !== null && resolvedUrl.origin === new URL(siteOrigin).origin;

    if (!isLocalBase && !isSiteOrigin) {
      return { kind: 'external', url: trimmed };
    }

    // Process internal path
    let pathname = decodeURIComponent(resolvedUrl.pathname);
    if (pathname.length > 1 && pathname.endsWith('/')) {
      pathname = pathname.slice(0, -1);
    }

    const fragment = resolvedUrl.hash ? decodeURIComponent(resolvedUrl.hash.slice(1)) : null;

    return {
      kind: 'internal',
      path: pathname,
      fragment: fragment === '' ? null : fragment,
    };
  } catch (err) {
    return {
      kind: 'malformed',
      reason: err instanceof Error ? err.message : String(err),
    };
  }
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/link-resolve.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.3, Req 4.4, Req 4.5

---

### M9.G4.T5: Implement Offline Internal Link Crawler Audit

**Objective:** Implement `runLinksAudit` in `scripts/audit/lib/links-audit.ts` to crawl all HTML pages, resolve internal targets, verify fragment anchors in DOM, and emit broken link findings without making network calls.

**Acceptance Criteria:**
- ✓ Crawls every anchor `a[href]` across all built HTML pages
- ✓ Uses `resolveInternalHref` to inspect links offline
- ✓ Resolves page targets and validates `#fragment` exists in target document ID set
- ✓ Emits `link-broken` or `link-placeholder` with route and selector
- ✓ Makes zero network requests

**Prerequisites:**
- M9.G4.T4 completed
- Target file: `scripts/audit/lib/links-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/links-audit.ts`:

```typescript
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding, RouteEntry } from './types';
import { buildReport } from './report';
import { listFiles, readText } from './build-layout';
import { parsePage, selectorFor, collectIds } from './html';
import { resolveInternalHref } from './link-resolve';
import { routeFileCandidates } from './route-files';

export async function runLinksAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport> {
  const allFiles = await listFiles(layout);
  const htmlFiles = allFiles.filter(f => f.endsWith('.html') && !f.startsWith('/_'));
  const findings: Finding[] = [];

  // Pre-load and parse all pages
  const pageDomMap = new Map<string, Document>();
  for (const file of htmlFiles) {
    const text = await readText(layout, file);
    if (text) {
      const parsed = parsePage({ path: file, kind: 'home', slug: null }, file, text);
      pageDomMap.set(file, parsed.document);
    }
  }

  for (const file of htmlFiles) {
    const doc = pageDomMap.get(file);
    if (!doc) continue;

    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const anchors = doc.querySelectorAll('a[href]');

    for (const a of Array.from(anchors)) {
      const rawHref = a.getAttribute('href')!;
      const resolution = resolveInternalHref(rawHref, routePath);

      if (resolution.kind === 'placeholder') {
        findings.push({
          route: routePath,
          rule: 'link-placeholder',
          message: `Placeholder link "${rawHref}" detected.`,
          severity: 'error',
          selector: selectorFor(a),
        });
      } else if (resolution.kind === 'malformed') {
        findings.push({
          route: routePath,
          rule: 'link-broken',
          message: `Malformed link "${rawHref}": ${resolution.reason}`,
          severity: 'error',
          selector: selectorFor(a),
        });
      } else if (resolution.kind === 'internal') {
        // Resolve internal target file
        const candidates = routeFileCandidates(resolution.path);
        const targetFile = candidates.find(c => allFiles.includes(`/${c}`));

        if (!targetFile && !allFiles.includes(resolution.path)) {
          findings.push({
            route: routePath,
            rule: 'link-broken',
            message: `Internal link "${rawHref}" targets non-existent path "${resolution.path}".`,
            severity: 'error',
            selector: selectorFor(a),
          });
        } else if (resolution.fragment && targetFile) {
          // Check fragment ID exists in target document
          const targetDoc = pageDomMap.get(`/${targetFile}`);
          if (targetDoc) {
            const ids = collectIds(targetDoc);
            const fragment = resolution.fragment;
            if (fragment !== 'top' && !ids.has(fragment) && !targetDoc.querySelector(`a[name="${CSS.escape(fragment)}"]`)) {
              findings.push({
                route: routePath,
                rule: 'link-broken',
                message: `Fragment target "#${fragment}" does not exist in target page "${resolution.path}".`,
                severity: 'error',
                selector: selectorFor(a),
              });
            }
          }
        }
      }
    }
  }

  return buildReport({
    audit: 'links',
    findings,
    routesChecked: htmlFiles.length,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/links-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 4.1–4.7

---

### M9.G4.T6: Verify Properties 8 and 9 (Link Resolution and Placeholders)

**Objective:** Author unit and property tests verifying link normalization (Property 8) and placeholder detection (Property 9), and create `scripts/audit/links.ts`.

**Acceptance Criteria:**
- ✓ Property 8 confirms query parameters and trailing slashes normalize identically
- ✓ Property 9 confirms empty or `#` hrefs always yield `placeholder` across $\ge 100$ runs
- ✓ Creates executable CLI `scripts/audit/links.ts`

**Prerequisites:**
- M9.G4.T5 completed
- Target files: `tests/audit/link-resolve.test.ts`, `scripts/audit/links.ts`

**Implementation Details:**

1. Create `tests/audit/link-resolve.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { resolveInternalHref } from '../../scripts/audit/lib/link-resolve';

describe('Link Resolution Unit & Property Tests', () => {
  it('ignores mailto and tel links', () => {
    expect(resolveInternalHref('mailto:test@example.com', '/').kind).toBe('ignore');
    expect(resolveInternalHref('tel:+1234567890', '/').kind).toBe('ignore');
  });

  // Feature: m9-quality-accessibility-performance, Property 8: Internal link resolution normalizes query, trailing slash, and fragment
  it('Property 8: Internal link resolution normalizes query, trailing slash, and fragment', () => {
    const pathSegment = fc.stringMatching(/^[a-z0-9-]+$/);
    const queryArb = fc.oneof(fc.constant(''), fc.constant('?tag=nextjs&page=1'));
    const fragmentArb = fc.oneof(fc.constant(''), fc.constant('#section-1'));

    fc.assert(
      fc.property(
        fc.array(pathSegment, { minLength: 1, maxLength: 3 }),
        queryArb,
        fragmentArb,
        (segments, query, fragment) => {
          const basePath = '/' + segments.join('/');
          const fullHref = `${basePath}/${query}${fragment}`;

          const res = resolveInternalHref(fullHref, '/');
          expect(res.kind).toBe('internal');
          if (res.kind === 'internal') {
            expect(res.path).toBe(basePath);
            if (fragment) {
              expect(res.fragment).toBe(fragment.slice(1));
            } else {
              expect(res.fragment).toBeNull();
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 9: Placeholder hrefs are detected regardless of padding
  it('Property 9: Placeholder hrefs are detected regardless of padding', () => {
    const whitespace = fc.constantFrom('', ' ', '  ', '\t', '\n');

    fc.assert(
      fc.property(
        whitespace,
        fc.constantFrom('', '#'),
        whitespace,
        (w1, val, w2) => {
          const padded = `${w1}${val}${w2}`;
          const res = resolveInternalHref(padded, '/');
          expect(res.kind).toBe('placeholder');
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

2. Create `scripts/audit/links.ts`:

```typescript
import { runCli } from './lib/cli';
import { runLinksAudit } from './lib/links-audit';

void runCli('links', (layout, args) => runLinksAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/link-resolve.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 4.1–4.7, Req 16.1

---

### M9.G4.T7: Implement Metadata Ranges and Canonical Calculators

**Objective:** Implement `checkLengthRange` and `expectedCanonical` in `scripts/audit/lib/checks/metadata-ranges.ts` and verify Properties 12 and 13.

**Acceptance Criteria:**
- ✓ `checkLengthRange` checks min and max bounds on trimmed strings
- ✓ `expectedCanonical` calculates canonical URL based on `flat` or `directory` export styles
- ✓ Property 12 verifies length range validation consistency
- ✓ Property 13 verifies expected canonical URL format

**Prerequisites:**
- M9.G4.T1 completed
- Target files: `scripts/audit/lib/checks/metadata-ranges.ts`, `tests/audit/metadata-ranges.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/checks/metadata-ranges.ts`:

```typescript
export type LengthCheckResult = 'ok' | 'too-short' | 'too-long';

export function checkLengthRange(length: number, min: number, max: number): LengthCheckResult {
  if (length < min) {
    return 'too-short';
  }
  if (length > max) {
    return 'too-long';
  }
  return 'ok';
}

export function expectedCanonical(
  siteUrl: string,
  routePath: string,
  style: 'flat' | 'directory' = 'flat'
): string {
  const base = siteUrl.replace(/\/+$/, '');
  const cleanPath = routePath === '/' ? '/' : routePath.replace(/\/+$/, '');

  if (cleanPath === '/') {
    return `${base}/`;
  }

  if (style === 'directory') {
    return `${base}${cleanPath}/`;
  }
  return `${base}${cleanPath}`;
}
```

2. Create `tests/audit/metadata-ranges.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { checkLengthRange, expectedCanonical } from '../../scripts/audit/lib/checks/metadata-ranges';

describe('Metadata Ranges and Canonical Properties', () => {
  // Feature: m9-quality-accessibility-performance, Property 12: Length range checker is consistent with its bounds
  it('Property 12: Length range checker is consistent with its bounds', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 200 }),
        fc.integer({ min: 10, max: 50 }),
        fc.integer({ min: 60, max: 150 }),
        (length, min, max) => {
          const res = checkLengthRange(length, min, max);
          if (length < min) {
            expect(res).toBe('too-short');
          } else if (length > max) {
            expect(res).toBe('too-long');
          } else {
            expect(res).toBe('ok');
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 13: Expected canonical URL is the normalized site URL plus the route path
  it('Property 13: Expected canonical URL is the normalized site URL plus the route path', () => {
    fc.assert(
      fc.property(
        fc.webUrl(),
        fc.stringMatching(/^\/[a-z0-9-/]*$/),
        fc.constantFrom<'flat' | 'directory'>('flat', 'directory'),
        (siteUrl, routePath, style) => {
          const res = expectedCanonical(siteUrl, routePath, style);
          const normalizedBase = siteUrl.replace(/\/+$/, '');
          expect(res.startsWith(normalizedBase)).toBe(true);

          if (routePath === '/' || routePath === '') {
            expect(res).toBe(`${normalizedBase}/`);
          } else if (style === 'directory') {
            expect(res.endsWith('/')).toBe(true);
          } else {
            expect(res.endsWith('/')).toBe(false);
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
npx vitest run tests/audit/metadata-ranges.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.7

---

### M9.G4.T8: Implement SEO and Metadata Audit Engine

**Objective:** Implement `runSeoAudit` in `scripts/audit/lib/seo-audit.ts` enforcing title/description length limits, canonical correctness, Open Graph consistency, and Decision 8 `/404` rules.

**Acceptance Criteria:**
- ✓ Enforces title (10–70) and description (50–160) limits across indexable routes
- ✓ Enforces uniqueness of titles and descriptions across routes
- ✓ Validates canonical and Open Graph parity (`og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`)
- ✓ Validates article metadata for `/blog/{slug}` pages
- ✓ Applies Decision 8: `/404` requires title, viewport, and `noindex`, skipping canonical/OG rules
- ✓ Reports warning if `siteUrl` uses placeholder hosts (`example.com`, `example.vercel.app`)

**Prerequisites:**
- M9.G4.T7 completed
- Target file: `scripts/audit/lib/seo-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/seo-audit.ts`:

```typescript
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding } from './types';
import { buildReport } from './report';
import { listFiles, readText } from './build-layout';
import { parsePage } from './html';
import { checkLengthRange, expectedCanonical } from './checks/metadata-ranges';
import { findDuplicates } from './checks/uniqueness';
import { SEO_LIMITS } from './config';
import { getSiteConfig } from '../../src/content/loaders/site';

export async function runSeoAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport> {
  const siteConfig = await getSiteConfig();
  const siteUrl = siteConfig.siteUrl;
  const allFiles = await listFiles(layout);
  const htmlFiles = allFiles.filter(f => f.endsWith('.html') && !f.startsWith('/_'));
  const findings: Finding[] = [];

  // Check placeholder siteUrl
  if (/example\.(com|vercel\.app)/i.test(siteUrl)) {
    findings.push({
      route: '*',
      rule: 'site-url-placeholder',
      message: `Site URL is configured with placeholder host "${siteUrl}".`,
      severity: 'warning',
      details: { releaseBlocker: true },
    });
  }

  const titles: Array<{ route: string; text: string }> = [];
  const descriptions: Array<{ route: string; text: string }> = [];

  for (const file of htmlFiles) {
    const text = await readText(layout, file);
    if (!text) continue;

    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const isNotFound = routePath === '/404';
    const parsed = parsePage({ path: routePath, kind: isNotFound ? 'not-found' : 'home', slug: null }, file, text);
    const doc = parsed.document;

    // Viewport meta (mandatory on all pages)
    const viewport = doc.querySelector('meta[name="viewport"]');
    if (!viewport) {
      findings.push({
        route: routePath,
        rule: 'seo-viewport',
        message: 'Missing required <meta name="viewport"> tag.',
        severity: 'error',
      });
    }

    // Title tag
    const titleEl = doc.querySelector('title');
    const titleText = titleEl?.textContent?.trim() ?? '';
    if (titleText === '') {
      findings.push({
        route: routePath,
        rule: 'seo-title',
        message: 'Missing or empty <title> element.',
        severity: 'error',
      });
    } else {
      titles.push({ route: routePath, text: titleText });
      if (!isNotFound) {
        const titleRange = checkLengthRange(titleText.length, SEO_LIMITS.title.min, SEO_LIMITS.title.max);
        if (titleRange !== 'ok') {
          findings.push({
            route: routePath,
            rule: 'seo-title-length',
            message: `Title length (${titleText.length}) is ${titleRange} [${SEO_LIMITS.title.min}-${SEO_LIMITS.title.max}].`,
            severity: 'error',
            details: { length: titleText.length },
          });
        }
      }
    }

    // Decision 8: Special handling for 404 route
    if (isNotFound) {
      const robots = doc.querySelector('meta[name="robots"]');
      const robotsContent = robots?.getAttribute('content') ?? '';
      if (!/noindex/i.test(robotsContent)) {
        findings.push({
          route: '/404',
          rule: 'seo-404-noindex',
          message: 'Not-found page must declare <meta name="robots" content="noindex">.',
          severity: 'error',
        });
      }
      continue; // Skip canonical and OG checks for /404
    }

    // Non-404 pages: noindex is strictly forbidden
    const robots = doc.querySelector('meta[name="robots"]');
    if (robots && /noindex/i.test(robots.getAttribute('content') ?? '')) {
      findings.push({
        route: routePath,
        rule: 'seo-noindex',
        message: `Indexable route "${routePath}" declares unexpected noindex directive.`,
        severity: 'error',
      });
    }

    // Description meta
    const descEl = doc.querySelector('meta[name="description"]');
    const descText = descEl?.getAttribute('content')?.trim() ?? '';
    if (descText === '') {
      findings.push({
        route: routePath,
        rule: 'seo-description',
        message: 'Missing or empty <meta name="description"> tag.',
        severity: 'error',
      });
    } else {
      descriptions.push({ route: routePath, text: descText });
      const descRange = checkLengthRange(descText.length, SEO_LIMITS.description.min, SEO_LIMITS.description.max);
      if (descRange !== 'ok') {
        findings.push({
          route: routePath,
          rule: 'seo-description-length',
          message: `Description length (${descText.length}) is ${descRange} [${SEO_LIMITS.description.min}-${SEO_LIMITS.description.max}].`,
          severity: 'error',
          details: { length: descText.length },
        });
      }
    }

    // Canonical link
    const canonical = doc.querySelector('link[rel="canonical"]');
    const canonicalHref = canonical?.getAttribute('href')?.trim() ?? '';
    const expected = expectedCanonical(siteUrl, routePath, layout.style);
    if (canonicalHref !== expected) {
      findings.push({
        route: routePath,
        rule: 'seo-canonical',
        message: `Canonical link "${canonicalHref}" does not match expected "${expected}".`,
        severity: 'error',
      });
    }

    // Open Graph tags
    const ogProps = ['og:title', 'og:description', 'og:url', 'og:type', 'og:site_name'];
    for (const prop of ogProps) {
      const el = doc.querySelector(`meta[property="${prop}"]`);
      if (!el || !el.getAttribute('content')) {
        findings.push({
          route: routePath,
          rule: 'seo-og',
          message: `Missing required Open Graph tag "${prop}".`,
          severity: 'error',
        });
      }
    }
  }

  // Duplicate titles and descriptions
  const dupTitles = findDuplicates(titles.map(t => t.text));
  for (const dup of dupTitles) {
    findings.push({
      route: '*',
      rule: 'seo-duplicate-title',
      message: `Duplicate title across pages: "${dup}".`,
      severity: 'error',
    });
  }

  const dupDescs = findDuplicates(descriptions.map(d => d.text));
  for (const dup of dupDescs) {
    findings.push({
      route: '*',
      rule: 'seo-duplicate-description',
      message: `Duplicate meta description across pages: "${dup}".`,
      severity: 'error',
    });
  }

  return buildReport({
    audit: 'seo',
    findings,
    routesChecked: htmlFiles.length,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/seo-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 8.1–8.8

---

### M9.G4.T9: Author SEO Audit Tests and CLI Runner

**Objective:** Write unit and fixture tests for `runSeoAudit` and create the CLI runner `scripts/audit/seo.ts`.

**Acceptance Criteria:**
- ✓ Validates clean passing report over compliant fixtures
- ✓ Verifies Decision 8: `/404` passes with `noindex` and requires no canonical
- ✓ Verifies length error reporting carries `{ length: N }` in details
- ✓ Creates executable CLI `scripts/audit/seo.ts`

**Prerequisites:**
- M9.G4.T8 completed
- Target files: `tests/audit/seo-audit.test.ts`, `scripts/audit/seo.ts`

**Implementation Details:**

1. Create `tests/audit/seo-audit.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runSeoAudit } from '../../scripts/audit/lib/seo-audit';

describe('SEO Audit Fixture Tests', () => {
  const fixturesRoot = path.join(process.cwd(), 'tests', 'audit', 'fixtures');

  it('runs cleanly on passing site fixture', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(fixturesRoot, 'passing-site'),
    });
    expect(layout).not.toBeNull();
    const report = await runSeoAudit(layout!);

    // Should only have warning for placeholder host if site.json uses example.com
    const errors = report.findings.filter(f => f.severity === 'error');
    expect(errors).toHaveLength(0);
  });
});
```

2. Create `scripts/audit/seo.ts`:

```typescript
import { runCli } from './lib/cli';
import { runSeoAudit } from './lib/seo-audit';

void runCli('seo', (layout, args) => runSeoAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/seo-audit.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 8.1–8.8, Req 16.1

---

### M9.G4.T10: Milestone 9 Goal 4 Checkpoint Verification

**Objective:** Run the full test suite for Goal 4, verify TypeScript and ESLint compliance, and test all three CLI runners against static fixtures.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/` pass (including Properties 7, 8, 9, 12, and 13)
- ✓ CLIs `routes.ts`, `links.ts`, and `seo.ts` execute cleanly
- ✓ `npm run typecheck` exits with 0
- ✓ `npm run lint` exits with 0

**Prerequisites:**
- M9.G4.T1 through M9.G4.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G4 suites
npx vitest run tests/audit/routes-audit.test.ts tests/audit/link-resolve.test.ts tests/audit/metadata-ranges.test.ts tests/audit/seo-audit.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Test CLI execution on passing fixtures
$env:AUDIT_BUILD_DIR = "tests/audit/fixtures/passing-site"
npx vite-node --config vitest.config.ts scripts/audit/routes.ts
if ($LASTEXITCODE -ne 0) { exit 1 }
npx vite-node --config vitest.config.ts scripts/audit/links.ts
if ($LASTEXITCODE -ne 0) { exit 1 }
npx vite-node --config vitest.config.ts scripts/audit/seo.ts
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

**Satisfies Requirements:** Req 1.5, Req 2.1–2.7, Req 4.1–4.7, Req 8.1–8.8, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/routes-audit.test.ts tests/audit/link-resolve.test.ts tests/audit/metadata-ranges.test.ts tests/audit/seo-audit.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in Goal 4 pass (including Properties 7, 8, 9, 12, and 13)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.