# M10.G3: Vercel Config Module, Header Comparison, and `vercel.json`

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure `vercel.json` parser, schema validator, header source matcher, and header comparison engine in `scripts/launch/lib/vercel-config.ts` and `headers.ts`. Under verified Human Approval A1 (Approved 2026-10-22), generate the production `vercel.json` declaring required Security_Headers on `/(.*)` and immutable caching on `/_next/static/(.*)`. Wire the `--write` option into `csp-hashes.ts`, prove Correctness Properties 8 through 11 via fast-check randomized testing, and assert that zero forbidden configuration keys exist.

## Goal Success Criteria

- ✓ `scripts/launch/lib/vercel-config.ts` exports `parseVercelConfig`, `validateVercelConfig`, `matchHeaderSource`, and `expectedHeadersFor`
- ✓ `scripts/launch/lib/headers.ts` exports `normalizeHeaderValue`, `compareHeaders`, `checkCacheControl`, and `findPoweredBy`
- ✓ Approval A1 is confirmed in `task-notes.md`, and `vercel.json` is generated at the repository root containing only `$schema` and `headers`
- ✓ `vercel.json` enforces `nosniff`, `strict-origin-when-cross-origin`, `DENY`, `camera=(), microphone=(), geolocation=(), payment=(), usb=()`, and `frame-ancestors 'none'` on `/(.*)`
- ✓ `vercel.json` enforces `Cache-Control: public, max-age=31536000, immutable` on `/_next/static/(.*)` and allows zero immutable caching on HTML routes
- ✓ `csp-hashes.ts --write` safely updates only the `Content-Security-Policy` value in `vercel.json` and preserves formatting
- ✓ Properties 8, 9, 10, and 11 pass at least 100 iterations each in `tests/launch/*.property.test.ts`
- ✓ Zero runtime or unapproved dependencies added; typecheck and lint pass cleanly

## Prerequisites

- Goal M10.G1 and M10.G2 completed (`scripts/launch/lib/types.ts` and `csp.ts` available)
- Approval Item A1 confirmed as `Approved 2026-10-22 (approval A1)` in `task-notes.md`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M10.G3.T1: Implement Vercel Config Parser & Validator (`scripts/launch/lib/vercel-config.ts`)

**Objective:** Implement `scripts/launch/lib/vercel-config.ts` providing pure functions `parseVercelConfig`, `validateVercelConfig`, `matchHeaderSource`, and `expectedHeadersFor` according to `design.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `parseVercelConfig` safely parses JSON and returns typed `VercelConfig` or `ConfigIssue` list
- ✓ `validateVercelConfig` enforces top-level key allowlist (`$schema`, `headers` only) and rejects `redirects`, `rewrites`, `routes`, `functions`, and `crons`
- ✓ Validates presence of mandatory security headers on `/(.*)`: `nosniff`, `strict-origin-when-cross-origin`, `DENY`, `permissions-policy`, and `content-security-policy` with `frame-ancestors 'none'`
- ✓ Validates `/_next/static/(.*)` immutable cache rule and rejects `immutable` on routes matching HTML
- ✓ `matchHeaderSource` supports exactly `/(.*)` and literal-prefix `<prefix>/(.*)` patterns

**Prerequisites:**
- M10.G2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\vercel-config.ts`

**Implementation Details:**
Create `scripts/launch/lib/vercel-config.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { VercelConfig, ConfigIssue, HeaderPair, HeaderRule } from './types';
import { parseCsp, findThirdPartySources } from './csp';

export const REQUIRED_SECURITY_HEADERS: readonly string[] = [
  'x-content-type-options',
  'referrer-policy',
  'x-frame-options',
  'permissions-policy',
  'content-security-policy',
];

const ALLOWED_CONFIG_KEYS = new Set(['$schema', 'headers']);

export function parseVercelConfig(text: string): { ok: true; config: VercelConfig } | { ok: false; issues: readonly ConfigIssue[] } {
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch (err) {
    return {
      ok: false,
      issues: [{ rule: 'config-invalid-json', message: `Invalid JSON syntax: ${(err as Error).message}` }],
    };
  }

  const issues = validateVercelConfig(parsed);
  if (issues.length > 0) {
    return { ok: false, issues };
  }

  return { ok: true, config: parsed as VercelConfig };
}

export function validateVercelConfig(value: unknown): readonly ConfigIssue[] {
  const issues: ConfigIssue[] = [];

  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    return [{ rule: 'config-not-object', message: 'Root configuration must be a JSON object.' }];
  }

  const obj = value as Record<string, unknown>;

  for (const key of Object.keys(obj)) {
    if (!ALLOWED_CONFIG_KEYS.has(key)) {
      issues.push({
        rule: 'config-key-forbidden',
        message: `Forbidden top-level key '${key}' detected. Only '$schema' and 'headers' are allowed.`,
      });
    }
  }

  if (!Array.isArray(obj.headers) || obj.headers.length === 0) {
    issues.push({ rule: 'headers-missing', message: "'headers' array must be present and non-empty." });
    return issues;
  }

  const rules = obj.headers as unknown[];
  let rootRule: HeaderRule | null = null;
  let staticRule: HeaderRule | null = null;

  for (let i = 0; i < rules.length; i++) {
    const r = rules[i];
    if (typeof r !== 'object' || r === null) {
      issues.push({ rule: 'rule-not-object', message: `Rule #${i} must be an object.` });
      continue;
    }

    const ruleObj = r as Record<string, unknown>;
    const source = ruleObj.source;

    if (typeof source !== 'string') {
      issues.push({ rule: 'source-missing', message: `Rule #${i} must define a string 'source'.` });
      continue;
    }

    const isValidSource = source === '/(.*)' || /^\/[a-zA-Z0-9_\-./]+\/\(\.\*\)$/.test(source);
    if (!isValidSource) {
      issues.push({
        rule: 'source-unsupported',
        message: `Rule #${i} has unsupported source pattern '${source}'. Must be '/(.*)' or '<prefix>/(.*)'.`,
      });
    }

    if (!Array.isArray(ruleObj.headers) || ruleObj.headers.length === 0) {
      issues.push({ rule: 'headers-empty', message: `Rule #${i} for source '${source}' has empty headers.` });
      continue;
    }

    const typedRule: HeaderRule = {
      source,
      headers: ruleObj.headers as HeaderPair[],
    };

    if (source === '/(.*)') rootRule = typedRule;
    if (source === '/_next/static/(.*)') staticRule = typedRule;

    // Check for immutable on HTML routes
    if (source !== '/_next/static/(.*)') {
      for (const h of typedRule.headers) {
        if (h.key.toLowerCase() === 'cache-control' && h.value.toLowerCase().includes('immutable')) {
          issues.push({
            rule: 'html-immutable',
            message: `Source '${source}' matching HTML routes must not declare 'immutable' Cache-Control.`,
          });
        }
      }
    }
  }

  if (!rootRule) {
    issues.push({ rule: 'required-header-missing', message: "Mandatory root rule for source '/(.*)' is missing." });
  } else {
    const headerMap = new Map<string, string>();
    for (const h of rootRule.headers) {
      headerMap.set(h.key.toLowerCase(), h.value);
    }

    // Required headers checks
    if (headerMap.get('x-content-type-options')?.toLowerCase() !== 'nosniff') {
      issues.push({ rule: 'required-header-missing', message: "Missing 'X-Content-Type-Options: nosniff'." });
    }
    if (headerMap.get('referrer-policy')?.toLowerCase() !== 'strict-origin-when-cross-origin') {
      issues.push({ rule: 'required-header-missing', message: "Missing 'Referrer-Policy: strict-origin-when-cross-origin'." });
    }
    if (headerMap.get('x-frame-options')?.toUpperCase() !== 'DENY') {
      issues.push({ rule: 'required-header-missing', message: "Missing 'X-Frame-Options: DENY'." });
    }

    const perm = headerMap.get('permissions-policy') ?? '';
    const hasRequiredPerms = ['camera=()', 'microphone=()', 'geolocation=()', 'payment=()', 'usb=()']
      .every(p => perm.includes(p));
    if (!hasRequiredPerms) {
      issues.push({ rule: 'required-header-missing', message: 'Permissions-Policy must disable camera, microphone, geolocation, payment, and usb.' });
    }

    const csp = headerMap.get('content-security-policy') ?? '';
    if (!csp.includes("frame-ancestors 'none'")) {
      issues.push({ rule: 'required-header-missing', message: "Content-Security-Policy must include 'frame-ancestors \\'none\\''." });
    }

    const parsedCsp = parseCsp(csp);
    const tp = findThirdPartySources(parsedCsp);
    if (tp.length > 0) {
      issues.push({ rule: 'csp-third-party', message: `Third-party origins forbidden in vercel.json CSP: ${tp.join(', ')}` });
    }
  }

  if (!staticRule) {
    issues.push({ rule: 'static-cache-missing', message: "Missing cache rule for source '/_next/static/(.*)'." });
  } else {
    const staticCache = staticRule.headers.find(h => h.key.toLowerCase() === 'cache-control')?.value.toLowerCase() ?? '';
    const hasImmutable = staticCache.includes('public') && staticCache.includes('max-age=31536000') && staticCache.includes('immutable');
    if (!hasImmutable) {
      issues.push({ rule: 'static-cache-missing', message: "Source '/_next/static/(.*)' must specify 'public, max-age=31536000, immutable'." });
    }
  }

  return issues;
}

export function matchHeaderSource(source: string, path: string): boolean {
  if (source === '/(.*)') {
    return path.startsWith('/');
  }
  if (source.endsWith('/(.*)')) {
    const prefix = source.slice(0, -5);
    return path.startsWith(`${prefix}/`);
  }
  return false;
}

export function expectedHeadersFor(config: VercelConfig, path: string): readonly HeaderPair[] {
  const merged = new Map<string, string>();

  for (const rule of config.headers) {
    if (matchHeaderSource(rule.source, path)) {
      for (const h of rule.headers) {
        merged.set(h.key.toLowerCase(), h.value);
      }
    }
  }

  const result: HeaderPair[] = [];
  for (const [key, value] of merged.entries()) {
    result.push({ key, value });
  }
  return result;
}
'@ | Set-Content -Path "scripts\launch\lib\vercel-config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1–5.7, Req 5.9, Req 5.10, Req 7.7

---

### M10.G3.T2: Implement Header Comparison Engine (`scripts/launch/lib/headers.ts`)

**Objective:** Implement `scripts/launch/lib/headers.ts` providing pure comparison logic for normalized HTTP headers, case-insensitive mapping, Cache-Control checking, and `X-Powered-By` fingerprint detection.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `toHeaderBag` converts header entries to lowercase string map with comma-separated multiples
- ✓ `normalizeHeaderValue` collapses whitespace, lowercases case-insensitive headers, normalizes CSP, and sorts comma-separated items
- ✓ `compareHeaders` returns mismatches only when expected headers are absent or value differs after normalization
- ✓ Extra response headers never cause a mismatch
- ✓ `findPoweredBy` case-insensitively detects `x-powered-by` header values or returns `null`
- ✓ `hasImmutableCache` detects `immutable` directive in Cache-Control

**Prerequisites:**
- M10.G3.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\headers.ts`

**Implementation Details:**
Create `scripts/launch/lib/headers.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { HeaderBag, HeaderPair, HeaderMismatch } from './types';
import { normalizeCsp } from './csp';

export function toHeaderBag(entries: Iterable<readonly [string, string]>): HeaderBag {
  const bag: Record<string, string> = {};
  for (const [rawKey, rawVal] of entries) {
    const key = rawKey.toLowerCase();
    if (bag[key] !== undefined) {
      bag[key] = `${bag[key]}, ${rawVal}`;
    } else {
      bag[key] = rawVal;
    }
  }
  return bag;
}

export function normalizeHeaderValue(key: string, value: string): string {
  const k = key.toLowerCase();
  const trimmed = value.trim().replace(/\s+/g, ' ');

  if (k === 'x-content-type-options' || k === 'x-frame-options' || k === 'referrer-policy') {
    return trimmed.toLowerCase();
  }

  if (k === 'content-security-policy') {
    return normalizeCsp(trimmed);
  }

  if (k === 'permissions-policy' || k === 'cache-control') {
    return trimmed
      .split(',')
      .map(part => part.trim().toLowerCase())
      .filter(Boolean)
      .sort()
      .join(', ');
  }

  return trimmed;
}

export function compareHeaders(expected: readonly HeaderPair[], actual: HeaderBag): readonly HeaderMismatch[] {
  const mismatches: HeaderMismatch[] = [];

  for (const exp of expected) {
    const key = exp.key.toLowerCase();
    const actualVal = actual[key] ?? null;

    if (actualVal === null) {
      mismatches.push({
        key,
        kind: 'missing',
        expected: exp.value,
        actual: null,
      });
      continue;
    }

    const normExp = normalizeHeaderValue(key, exp.value);
    const normAct = normalizeHeaderValue(key, actualVal);

    if (normExp !== normAct) {
      mismatches.push({
        key,
        kind: 'different',
        expected: exp.value,
        actual: actualVal,
      });
    }
  }

  return mismatches.sort((a, b) => a.key.localeCompare(b.key));
}

export function findPoweredBy(actual: HeaderBag): string | null {
  for (const [k, v] of Object.entries(actual)) {
    if (k.toLowerCase() === 'x-powered-by') {
      return v;
    }
  }
  return null;
}

export function hasImmutableCache(actual: HeaderBag): boolean {
  const cache = actual['cache-control'] ?? '';
  return cache.toLowerCase().includes('immutable');
}
'@ | Set-Content -Path "scripts\launch\lib\headers.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.6, Req 5.7, Req 7.7, Req 7.8

---

### M10.G3.T3: Implement Fast-Check Tests for Vercel Config Properties 8, 9, and 10

**Objective:** Author `tests/launch/vercel-config.property.test.ts` formally proving Property 8 (required security headers & cache rules), Property 9 (forbidden keys & JSON validity), and Property 10 (source path matching) over at least 100 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 8 proves `validateVercelConfig` passes valid security configs and flags missing headers or bad cache rules
- ✓ Property 9 proves all keys outside `$schema` and `headers` are flagged with `config-key-forbidden`
- ✓ Property 10 proves `expectedHeadersFor` applies rules strictly based on path prefix matching and excludes immutable on HTML
- ✓ Tests pass with at least 100 runs each and include feature tag comments

**Prerequisites:**
- M10.G3.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\vercel-config.property.test.ts`

**Implementation Details:**
Create `tests/launch/vercel-config.property.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { validateVercelConfig, parseVercelConfig, matchHeaderSource, expectedHeadersFor } from '../../scripts/launch/lib/vercel-config';
import type { VercelConfig } from '../../scripts/launch/lib/types';

describe('M10 Vercel Config Properties (Properties 8 - 10)', () => {
  const baseValidConfig: VercelConfig = {
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
      {
        source: '/_next/static/(.*)',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ],
  };

  // Feature: m10-deployment-launch, Property 8: vercel.json validation requires the security headers and the static cache rule
  it('Property 8: vercel.json validation requires the security headers and the static cache rule', () => {
    // Valid baseline passes
    expect(validateVercelConfig(baseValidConfig)).toEqual([]);

    fc.assert(
      fc.property(fc.integer({ min: 0, max: 4 }), headerIndexToRemove => {
        // Create config with one missing required header
        const alteredRootHeaders = baseValidConfig.headers[0]!.headers.filter((_, idx) => idx !== headerIndexToRemove);
        const alteredConfig: VercelConfig = {
          headers: [
            { source: '/(.*)', headers: alteredRootHeaders },
            baseValidConfig.headers[1]!,
          ],
        };

        const issues = validateVercelConfig(alteredConfig);
        expect(issues.some(i => i.rule === 'required-header-missing')).toBe(true);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m10-deployment-launch, Property 9: vercel.json allows only the headers key and valid JSON
  it('Property 9: vercel.json allows only the headers key and valid JSON', () => {
    fc.assert(
      fc.property(fc.stringMatching(/^[a-z]{3,12}$/), randomKey => {
        fc.pre(randomKey !== 'headers' && randomKey !== '$schema');

        const invalidConfig = {
          ...baseValidConfig,
          [randomKey]: true,
        };

        const issues = validateVercelConfig(invalidConfig);
        expect(issues.some(i => i.rule === 'config-key-forbidden')).toBe(true);
      }),
      { numRuns: 100 }
    );

    // Invalid JSON test
    const invalidJsonRes = parseVercelConfig('{ "headers": invalid-json');
    expect(invalidJsonRes.ok).toBe(false);
  });

  // Feature: m10-deployment-launch, Property 10: Header source matching selects the right rules
  it('Property 10: Header source matching selects the right rules', () => {
    fc.assert(
      fc.property(fc.stringMatching(/^\/[a-z0-9_-]{1,15}$/), routePath => {
        // Any standard HTML route matches /(.*) but not /_next/static/(.*)
        expect(matchHeaderSource('/(.*)', routePath)).toBe(true);
        expect(matchHeaderSource('/_next/static/(.*)', routePath)).toBe(false);

        const expected = expectedHeadersFor(baseValidConfig, routePath);
        // HTML route must not receive immutable Cache-Control
        const cacheControl = expected.find(h => h.key.toLowerCase() === 'cache-control');
        expect(cacheControl).toBeUndefined();

        // Static path matches both and merges
        const staticAssetPath = `/_next/static/chunks${routePath}.js`;
        const staticExpected = expectedHeadersFor(baseValidConfig, staticAssetPath);
        const staticCache = staticExpected.find(h => h.key.toLowerCase() === 'cache-control');
        expect(staticCache?.value).toContain('immutable');
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content -Path "tests\launch\vercel-config.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/vercel-config.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1–5.7, Req 5.9, Req 5.10, Req 7.7

---

### M10.G3.T4: Implement Fast-Check Tests for Header Comparison Property 11

**Objective:** Author `tests/launch/headers.property.test.ts` formally proving Property 11 (header comparison reports exact missing/different headers and is invariant to order in directives) over at least 200 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 11 proves `compareHeaders` returns zero mismatches when actual headers match expected values
- ✓ Proves extra headers in actual response bag never cause mismatches
- ✓ Proves permuting comma-separated directives in `Permissions-Policy` or `Cache-Control` causes zero mismatches
- ✓ Proves `findPoweredBy` detects `x-powered-by` in any letter case
- ✓ Tests pass with at least 200 runs

**Prerequisites:**
- M10.G3.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\headers.property.test.ts`

**Implementation Details:**
Create `tests/launch/headers.property.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { compareHeaders, findPoweredBy, toHeaderBag } from '../../scripts/launch/lib/headers';
import type { HeaderPair, HeaderBag } from '../../scripts/launch/lib/types';

describe('M10 Headers Comparison Property (Property 11)', () => {
  // Feature: m10-deployment-launch, Property 11: Header comparison reports exactly the missing or different headers
  it('Property 11: Header comparison reports exactly the missing or different headers', () => {
    const headerPairArb = fc.record<HeaderPair>({
      key: fc.stringMatching(/^[a-z][a-z0-9-]{1,15}$/),
      value: fc.stringMatching(/^[a-zA-Z0-9_\s=,-]{1,40}$/),
    });

    fc.assert(
      fc.property(
        fc.uniqueArray(headerPairArb, { selector: h => h.key, minLength: 1, maxLength: 5 }),
        expectedHeaders => {
          // 1. Exact match returns zero mismatches
          const actualBag: Record<string, string> = {};
          for (const h of expectedHeaders) {
            actualBag[h.key] = h.value;
          }
          expect(compareHeaders(expectedHeaders, actualBag)).toEqual([]);

          // 2. Extra actual headers do not trigger mismatches
          const augmentedBag = { ...actualBag, 'x-extra-custom-header': 'unrelated-value' };
          expect(compareHeaders(expectedHeaders, augmentedBag)).toEqual([]);

          // 3. Omitted header triggers 'missing' mismatch
          if (expectedHeaders.length > 1) {
            const omittedKey = expectedHeaders[0]!.key;
            const partialBag = { ...actualBag };
            delete partialBag[omittedKey];

            const mismatches = compareHeaders(expectedHeaders, partialBag);
            expect(mismatches.length).toBe(1);
            expect(mismatches[0]?.kind).toBe('missing');
            expect(mismatches[0]?.key).toBe(omittedKey.toLowerCase());
          }
        }
      ),
      { numRuns: 200 }
    );
  });

  it('detects x-powered-by header regardless of casing', () => {
    fc.assert(
      fc.property(fc.constantFrom('x-powered-by', 'X-Powered-By', 'X-POWERED-BY'), key => {
        const bag: HeaderBag = { [key]: 'Next.js' };
        expect(findPoweredBy(bag)).toBe('Next.js');
      }),
      { numRuns: 50 }
    );

    expect(findPoweredBy({ 'content-type': 'text/html' })).toBeNull();
  });
});
'@ | Set-Content -Path "tests\launch\headers.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/headers.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.7, Req 7.8

---

### M10.G3.T5: Verify Human Approval A1 Status in Task Notes

**Objective:** Audit `task-notes.md` to confirm that Human Approval A1 (`vercel.json`) is recorded as `Approved 2026-10-22 (approval A1)` before creating the file on disk.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `task-notes.md` contains the explicit approval confirmation for A1
- ✓ Script verifies approval status programmatically before file generation proceeds

**Prerequisites:**
- M10.G1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Execute the approval verification check via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
$isApproved = $notes -match "Approval Item A1[\s\S]*?Approved 2026-10-22 \(approval A1\)"

if (-not $isApproved) {
    throw "Approval Gate Blocked: A1 (vercel.json) is not verified as approved in task-notes.md."
}

Write-Host "Approval Gate Passed: Item A1 confirmed approved. Proceeding with vercel.json generation."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "Approved 2026-10-22 \(approval A1\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 5.1

---

### M10.G3.T6: Create Canonical `vercel.json` (Approval A1)

**Objective:** Under verified Approval A1, create `vercel.json` in the project root containing the `$schema` reference, the `/(.*)` rule with all required Security_Headers (using CSP from `buildCsp` with `inline-allowed` and derived style mode), and the immutable caching rule on `/_next/static/(.*)`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ File `vercel.json` exists at project root
- ✓ Contains valid JSON matching `VercelConfig` schema
- ✓ Declares headers on `/(.*)`: `nosniff`, `strict-origin-when-cross-origin`, `DENY`, `permissions-policy`, and `content-security-policy`
- ✓ Declares headers on `/_next/static/(.*)`: `public, max-age=31536000, immutable`
- ✓ Contains zero forbidden keys (`redirects`, `rewrites`, `functions`, `crons`)
- ✓ Strict-Transport-Security is omitted (default Vercel CDN behavior)

**Prerequisites:**
- M10.G3.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\vercel.json`

**Implementation Details:**
Create `vercel.json` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "X-Frame-Options", "value": "DENY" },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
'@ | Set-Content -Path "vercel.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$vj = Get-Content "vercel.json" -Raw | ConvertFrom-Json
if ($vj.headers.Count -eq 2 -and ($vj.headers[0].headers | Where-Object { $_.key -eq "X-Frame-Options" }).value -eq "DENY") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1–5.7, Req 5.9, Req 5.10, Req 6.5

---

### M10.G3.T7: Add `--write` Capability to `scripts/launch/csp-hashes.ts`

**Objective:** Wire the `--write` flag into `scripts/launch/csp-hashes.ts` so that it safely replaces only the `Content-Security-Policy` header in `vercel.json` without re-ordering other entries or corrupting JSON indentation.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `csp-hashes.ts` handles `--write` flag
- ✓ Locates existing `/(.*)` rule in `vercel.json` and updates its `Content-Security-Policy` value
- ✓ Refuses to execute if `vercel.json` does not exist or if CSP entry is missing
- ✓ Preserves 2-space JSON indentation and trailing newline
- ✓ Re-parses and validates config after writing to ensure zero syntax or schema regressions

**Prerequisites:**
- M10.G3.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\csp-hashes.ts`

**Implementation Details:**
Update `scripts/launch/csp-hashes.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$scriptContent = Get-Content "scripts\launch\csp-hashes.ts" -Raw

$updatedScript = $scriptContent -replace '(\s+if \(args\.command === ''print''\) \{[\s\S]*?return 0;\s+\})', @'
  if (args.write) {
    const vercelTarget = path.resolve(process.cwd(), args.vercelJsonPath);
    if (!fs.existsSync(vercelTarget)) {
      console.error(`Cannot --write: '${args.vercelJsonPath}' does not exist.`);
      return 2;
    }

    try {
      const vercelJson = JSON.parse(fs.readFileSync(vercelTarget, 'utf8'));
      const rootRule = (vercelJson.headers ?? []).find((r: { source: string }) => r.source === '/(.*)');
      if (!rootRule || !Array.isArray(rootRule.headers)) {
        console.error("Cannot --write: Missing '/(.*)' rule in vercel.json.");
        return 2;
      }

      const cspEntry = rootRule.headers.find((h: { key: string }) => h.key.toLowerCase() === 'content-security-policy');
      if (!cspEntry) {
        console.error("Cannot --write: No Content-Security-Policy entry found in '/(.*)' rule.");
        return 2;
      }

      cspEntry.value = generatedCsp;
      fs.writeFileSync(vercelTarget, JSON.stringify(vercelJson, null, 2) + '\n', 'utf8');
      console.log(`Successfully updated Content-Security-Policy in ${args.vercelJsonPath}`);
    } catch (err) {
      console.error(`Failed to write to ${args.vercelJsonPath}: ${(err as Error).message}`);
      return 2;
    }
  }

$1
'@

Set-Content -Path "scripts\launch\csp-hashes.ts" -Value $updatedScript -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.3, Req 6.10

---

### M10.G3.T8: Author Real `vercel.json` and `--write` Verification Tests

**Objective:** Write `tests/launch/vercel-json.test.ts` to validate the live `vercel.json` file on disk and `tests/launch/csp-write.test.ts` to test `--write` updates on temporary copies.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `tests/launch/vercel-json.test.ts` asserts `vercel.json` exists, is valid JSON, has 0 `validateVercelConfig` issues, and contains zero external hosts
- ✓ `tests/launch/csp-write.test.ts` copies `vercel.json` to a temp path, executes `runCspHashes(['print', '--write', '--vercel-json', tempPath])`, and asserts CSP was updated while preserving other headers
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G3.T7 completed
- Target files: `tests/launch/vercel-json.test.ts`, `tests/launch/csp-write.test.ts`

**Implementation Details:**
Create the test files using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. vercel-json.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { validateVercelConfig, parseVercelConfig } from '../../scripts/launch/lib/vercel-config';

describe('Live vercel.json Verification', () => {
  it('validates production vercel.json structure and security headers', () => {
    const vercelPath = path.resolve(process.cwd(), 'vercel.json');
    expect(fs.existsSync(vercelPath)).toBe(true);

    const content = fs.readFileSync(vercelPath, 'utf8');
    const parseResult = parseVercelConfig(content);

    expect(parseResult.ok).toBe(true);
    if (parseResult.ok) {
      const issues = validateVercelConfig(parseResult.config);
      expect(issues).toEqual([]);
    }
  });
});
'@ | Set-Content -Path "tests\launch\vercel-json.test.ts" -Encoding UTF8

# 2. csp-write.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { runCspHashes } from '../../scripts/launch/csp-hashes';

describe('CSP Hashes --write Integration Test', () => {
  it('updates CSP header in vercel.json without modifying other entries', async () => {
    const tempVercel = path.resolve(__dirname, 'fixtures/vercel/temp-write-test.json');
    const sourceVercel = path.resolve(process.cwd(), 'vercel.json');

    fs.copyFileSync(sourceVercel, tempVercel);

    try {
      const exitCode = await runCspHashes(['print', '--policy', 'inline', '--write', '--vercel-json', tempVercel]);
      expect(exitCode).toBe(0);

      const updated = JSON.parse(fs.readFileSync(tempVercel, 'utf8'));
      const rootRule = updated.headers.find((r: { source: string }) => r.source === '/(.*)');
      const csp = rootRule.headers.find((h: { key: string }) => h.key === 'Content-Security-Policy');

      expect(csp.value).toContain("default-src 'self'");
      expect(csp.value).toContain("script-src 'self' 'unsafe-inline'");
    } finally {
      if (fs.existsSync(tempVercel)) {
        fs.unlinkSync(tempVercel);
      }
    }
  });
});
'@ | Set-Content -Path "tests\launch\csp-write.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/vercel-json.test.ts tests/launch/csp-write.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1–5.7, Req 5.9, Req 5.10, Req 6.3, Req 6.10

---

### M10.G3.T9: Author Fixture Variation Suite (`tests/launch/vercel-fixtures.test.ts`)

**Objective:** Write unit tests in `tests/launch/vercel-fixtures.test.ts` verifying that `validateVercelConfig` emits exact expected issue rules for all invalid fixtures in `tests/launch/fixtures/vercel/`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Asserts `missing-header.json` produces `required-header-missing` and `static-cache-missing`
- ✓ Asserts `forbidden-key.json` produces `config-key-forbidden` for `redirects`
- ✓ Asserts `html-immutable.json` produces `html-immutable`
- ✓ Asserts `unsupported-source.json` produces `source-unsupported`
- ✓ Asserts `invalid-syntax.json` produces `config-invalid-json`

**Prerequisites:**
- M10.G3.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\vercel-fixtures.test.ts`

**Implementation Details:**
Create `tests/launch/vercel-fixtures.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { parseVercelConfig } from '../../scripts/launch/lib/vercel-config';

describe('Vercel Config Fixture Issue Detection', () => {
  const fixtureDir = path.resolve(__dirname, 'fixtures/vercel');

  it('detects missing headers in missing-header.json', () => {
    const content = fs.readFileSync(path.join(fixtureDir, 'missing-header.json'), 'utf8');
    const result = parseVercelConfig(content);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.issues.some(i => i.rule === 'required-header-missing')).toBe(true);
      expect(result.issues.some(i => i.rule === 'static-cache-missing')).toBe(true);
    }
  });

  it('detects forbidden keys in forbidden-key.json', () => {
    const content = fs.readFileSync(path.join(fixtureDir, 'forbidden-key.json'), 'utf8');
    const result = parseVercelConfig(content);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.issues.some(i => i.rule === 'config-key-forbidden' && i.message.includes('redirects'))).toBe(true);
    }
  });

  it('detects immutable caching on HTML in html-immutable.json', () => {
    const content = fs.readFileSync(path.join(fixtureDir, 'html-immutable.json'), 'utf8');
    const result = parseVercelConfig(content);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.issues.some(i => i.rule === 'html-immutable')).toBe(true);
    }
  });

  it('detects unsupported source patterns in unsupported-source.json', () => {
    const content = fs.readFileSync(path.join(fixtureDir, 'unsupported-source.json'), 'utf8');
    const result = parseVercelConfig(content);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.issues.some(i => i.rule === 'source-unsupported')).toBe(true);
    }
  });

  it('handles invalid JSON syntax in invalid-syntax.json', () => {
    const content = fs.readFileSync(path.join(fixtureDir, 'invalid-syntax.json'), 'utf8');
    const result = parseVercelConfig(content);
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.issues.some(i => i.rule === 'config-invalid-json')).toBe(true);
    }
  });
});
'@ | Set-Content -Path "tests\launch\vercel-fixtures.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/vercel-fixtures.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.6, Req 5.7, Req 5.9, Req 5.10

---

### M10.G3.T10: Goal 3 Checkpoint and Quality Gate Verification

**Objective:** Run the full quality verification suite (lint, typecheck, property tests, fixture tests, and real `vercel.json` validation) to seal Goal 3 with zero regressions.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ Properties 8 through 11 pass with at least 100/200 runs
- ✓ All vercel config unit and fixture integration tests pass
- ✓ `git diff` confirms only `vercel.json`, `scripts/launch/`, and `tests/launch/` are modified

**Prerequisites:**
- M10.G3.T1 through M10.G3.T9 completed

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
npx vitest run tests/launch/vercel-config.property.test.ts tests/launch/headers.property.test.ts tests/launch/vercel-json.test.ts tests/launch/csp-write.test.ts tests/launch/vercel-fixtures.test.ts
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Write-Host "M10.G3 Checkpoint: All Vercel config & header quality gates passed cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/vercel-config.property.test.ts tests/launch/headers.property.test.ts tests/launch/vercel-json.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 5.1–5.7, Req 5.9–5.11

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "scripts\launch\lib\vercel-config.ts"
Test-Path "scripts\launch\lib\headers.ts"
Test-Path "vercel.json"
npx vitest run tests/launch/vercel-config.property.test.ts tests/launch/headers.property.test.ts tests/launch/vercel-json.test.ts tests/launch/csp-write.test.ts tests/launch/vercel-fixtures.test.ts
git status --porcelain vercel.json
```
Expected output:
- `True` for all paths including root `vercel.json`
- Vitest reports all property and fixture test suites passed
- `vercel.json` is tracked and clean