# M9.G3: Structural Audit and Hygiene Checks

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the pure structural and privacy hygiene audit rules under `scripts/audit/lib/checks/` and the composite structural audit engine `scripts/audit/lib/structure-audit.ts` with its CLI `scripts/audit/structure.ts`. This goal evaluates all P0 built HTML pages against semantic document structure (HTML `lang`, single `h1`, single `main`, landmarks, heading hierarchies, skip link, accessible names, image `alt` attributes, ID uniqueness), privacy hygiene (external link security tokens, strict `https:`, forbidden input/embed elements, script origins, tracking markers per Decision 7, cookies, secrets), and JSON-LD syntax verification. It provides fast-check Property 10 (heading skips), Property 11 (duplicate detection), and Property 14 (rel security tokens).

---

## Goal Success Criteria

- ✓ `scripts/audit/lib/checks/headings.ts` exports pure `findHeadingOrderViolations` flagging downward heading skips
- ✓ `scripts/audit/lib/checks/uniqueness.ts` exports pure `findDuplicates` detecting non-unique identifiers
- ✓ `scripts/audit/lib/checks/accessible-name.ts` exports `computeAccessibleName` verifying labels for anchors and buttons
- ✓ `scripts/audit/lib/checks/hygiene.ts` exports `checkExternalRel`, `scanMarkers`, and `scanSecrets` implementing Decision 7
- ✓ `scripts/audit/lib/structure-audit.ts` aggregates all rules and produces typed findings with deterministic selectors
- ✓ `scripts/audit/structure.ts` executes via `runCli`, exiting 0 on clean builds and 1 on defects
- ✓ Fast-check Properties 10, 11, and 14 pass $\ge 100$ iterations each
- ✓ Passing fixture yields 0 errors; defective fixtures yield exactly their respective isolated errors
- ✓ Zero use of regular expressions for HTML document structure parsing

---

## Prerequisites

- Goals M9.G1 and M9.G2 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Static fixtures available in `tests/audit/fixtures/`

---

## Tasks

### M9.G3.T1: Implement Pure Heading Order and Duplicate Detection Checkers

**Objective:** Implement pure, isolated utility functions to detect heading downward skips (`findHeadingOrderViolations`) and duplicate array values (`findDuplicates`).

**Acceptance Criteria:**
- ✓ `scripts/audit/lib/checks/headings.ts` flags only indices $i \ge 1$ where $h_i > h_{i-1} + 1$
- ✓ First heading index (0) is never flagged as a skip
- ✓ `scripts/audit/lib/checks/uniqueness.ts` returns duplicate items once in first-seen order
- ✓ Both functions are pure with zero side-effects and zero external dependencies

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

1. Create directory `scripts/audit/lib/checks/` if missing.
2. Create `scripts/audit/lib/checks/headings.ts`:

```typescript
/**
 * Detects heading levels that skip downward by more than one level.
 * e.g., h2 followed by h4 is a violation. h3 followed by h1 or h2 is valid.
 * The first heading (index 0) is never a violation.
 * Returns array of indices in the input array where violations occur.
 */
export function findHeadingOrderViolations(levels: readonly number[]): readonly number[] {
  const violations: number[] = [];
  if (levels.length <= 1) {
    return violations;
  }

  for (let i = 1; i < levels.length; i++) {
    const prev = levels[i - 1]!;
    const curr = levels[i]!;
    if (curr > prev + 1) {
      violations.push(i);
    }
  }

  return violations;
}
```

3. Create `scripts/audit/lib/checks/uniqueness.ts`:

```typescript
/**
 * Detects duplicate entries in an array of strings.
 * Returns each duplicate value exactly once, in order of its first duplication.
 */
export function findDuplicates<T extends string | number>(items: readonly T[]): readonly T[] {
  const seen = new Set<T>();
  const duplicates = new Set<T>();

  for (const item of items) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }

  return Array.from(duplicates);
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/checks/headings.ts scripts/audit/lib/checks/uniqueness.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 3.4, Req 3.8

---

### M9.G3.T2: Implement Accessible Name Calculation Checker

**Objective:** Implement `computeAccessibleName` in `scripts/audit/lib/checks/accessible-name.ts` to compute accessible labels for interactive controls without heavy external libraries.

**Acceptance Criteria:**
- ✓ Checks `aria-label`, `aria-labelledby`, text content (excluding `aria-hidden` descendants), `img[alt]`, `svg > title`, and `title` attribute in order
- ✓ Strips whitespace and returns empty string if no accessible name exists
- ✓ Includes unit tests verifying all evaluation paths

**Prerequisites:**
- M9.G3.T1 completed
- Target files: `scripts/audit/lib/checks/accessible-name.ts`, `tests/audit/accessible-name.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/checks/accessible-name.ts`:

```typescript
export function computeAccessibleName(el: Element): string {
  // 1. aria-label
  const ariaLabel = el.getAttribute('aria-label');
  if (ariaLabel && ariaLabel.trim() !== '') {
    return ariaLabel.trim();
  }

  // 2. aria-labelledby
  const labelledBy = el.getAttribute('aria-labelledby');
  if (labelledBy && labelledBy.trim() !== '') {
    const doc = el.ownerDocument;
    if (doc) {
      const ids = labelledBy.trim().split(/\s+/);
      const textParts: string[] = [];
      for (const id of ids) {
        const target = doc.getElementById(id);
        if (target && target.textContent) {
          textParts.push(target.textContent.trim());
        }
      }
      const combined = textParts.join(' ').trim();
      if (combined !== '') {
        return combined;
      }
    }
  }

  // 3. Descendant image alt
  const imgDescendant = el.querySelector('img[alt]');
  if (imgDescendant) {
    const alt = imgDescendant.getAttribute('alt');
    if (alt && alt.trim() !== '') {
      return alt.trim();
    }
  }

  // 4. Descendant SVG title
  const svgTitle = el.querySelector('svg > title');
  if (svgTitle && svgTitle.textContent && svgTitle.textContent.trim() !== '') {
    return svgTitle.textContent.trim();
  }

  // 5. Direct and nested text content excluding aria-hidden
  function extractVisibleText(node: Node): string {
    if (node.nodeType === 3) {
      // Text node
      return node.textContent ?? '';
    }
    if (node.nodeType === 1) {
      // Element node
      const element = node as Element;
      if (element.getAttribute('aria-hidden') === 'true') {
        return '';
      }
      let acc = '';
      for (const child of Array.from(element.childNodes)) {
        acc += extractVisibleText(child);
      }
      return acc;
    }
    return '';
  }

  const textContent = extractVisibleText(el).trim();
  if (textContent !== '') {
    return textContent;
  }

  // 6. title attribute
  const titleAttr = el.getAttribute('title');
  if (titleAttr && titleAttr.trim() !== '') {
    return titleAttr.trim();
  }

  return '';
}
```

2. Create `tests/audit/accessible-name.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { JSDOM } from 'jsdom';
import { computeAccessibleName } from '../../scripts/audit/lib/checks/accessible-name';

describe('computeAccessibleName', () => {
  it('prefers aria-label over inner text', () => {
    const dom = new JSDOM('<button aria-label="Close modal">X</button>');
    const btn = dom.window.document.querySelector('button')!;
    expect(computeAccessibleName(btn)).toBe('Close modal');
  });

  it('resolves aria-labelledby references', () => {
    const dom = new JSDOM(`
      <span id="t1">Delete</span>
      <span id="t2">Item</span>
      <button aria-labelledby="t1 t2"></button>
    `);
    const btn = dom.window.document.querySelector('button')!;
    expect(computeAccessibleName(btn)).toBe('Delete Item');
  });

  it('ignores aria-hidden content', () => {
    const dom = new JSDOM('<a href="#">Home <span aria-hidden="true">&rarr;</span></a>');
    const a = dom.window.document.querySelector('a')!;
    expect(computeAccessibleName(a)).toBe('Home');
  });

  it('extracts alt text from child img', () => {
    const dom = new JSDOM('<a href="#"><img src="/logo.png" alt="Company Logo" /></a>');
    const a = dom.window.document.querySelector('a')!;
    expect(computeAccessibleName(a)).toBe('Company Logo');
  });

  it('extracts title from child svg', () => {
    const dom = new JSDOM('<button><svg><title>Search</title></svg></button>');
    const btn = dom.window.document.querySelector('button')!;
    expect(computeAccessibleName(btn)).toBe('Search');
  });

  it('returns empty string when no label exists', () => {
    const dom = new JSDOM('<button></button>');
    const btn = dom.window.document.querySelector('button')!;
    expect(computeAccessibleName(btn)).toBe('');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/accessible-name.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 3.6

---

### M9.G3.T3: Implement Security and Privacy Hygiene Checkers

**Objective:** Implement `checkExternalRel`, `scanMarkers`, and `scanSecrets` in `scripts/audit/lib/checks/hygiene.ts` implementing Decision 7.

**Acceptance Criteria:**
- ✓ `checkExternalRel` asserts that `rel` contains both `noopener` and `noreferrer` tokens (case-insensitive)
- ✓ `scanMarkers` evaluates attributes, inline non-payload scripts, and scripts/stylesheets against Decision 7 marker lists
- ✓ Ignores HTML text nodes and Next.js flight payload scripts (`__next_f`)
- ✓ `scanSecrets` detects private key headers, tokens, and `.env` references across text content

**Prerequisites:**
- M9.G3.T1 completed
- Target file: `scripts/audit/lib/checks/hygiene.ts`

**Implementation Details:**

Create `scripts/audit/lib/checks/hygiene.ts`:

```typescript
import { TRACKING_HOST_MARKERS, TRACKING_CALL_MARKERS, SECRET_PATTERNS } from '../config';

export function checkExternalRel(relValue: string | null | undefined): boolean {
  if (!relValue) {
    return false;
  }
  const tokens = relValue.toLowerCase().trim().split(/\s+/);
  return tokens.includes('noopener') && tokens.includes('noreferrer');
}

export interface MarkerMatch {
  readonly matched: string;
  readonly context: string;
}

export function scanMarkers(content: string): readonly MarkerMatch[] {
  const matches: MarkerMatch[] = [];

  for (const marker of TRACKING_HOST_MARKERS) {
    if (content.includes(marker)) {
      matches.push({ matched: marker, context: 'tracking-host' });
    }
  }

  for (const marker of TRACKING_CALL_MARKERS) {
    if (content.includes(marker)) {
      matches.push({ matched: marker, context: 'tracking-call' });
    }
  }

  return matches;
}

export function scanSecrets(content: string, filename: string): readonly MarkerMatch[] {
  const matches: MarkerMatch[] = [];

  // Check file name for environment secret file
  if (/\.env(\.|$)/i.test(filename)) {
    matches.push({ matched: filename, context: 'env-file' });
  }

  for (const pattern of SECRET_PATTERNS) {
    if (pattern.test(content)) {
      matches.push({ matched: pattern.source, context: 'secret-pattern' });
    }
  }

  return matches;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/checks/hygiene.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.5, Req 5.7

---

### M9.G3.T4: Implement Core Document Structure Rules in Structure Audit

**Objective:** Implement `scripts/audit/lib/structure-audit.ts` with checks for document language, `h1` count, `main` count, required landmarks, heading sequence, skip link, accessible control names, image alt attributes, and unique IDs.

**Acceptance Criteria:**
- ✓ Validates `html[lang]`, single `h1`, single `main`, and presence of `header`, `nav`, `main`, `footer`
- ✓ Applies `findHeadingOrderViolations` to heading sequences (`h1` through `h6`)
- ✓ Verifies skip link is the first focusable element targeting an existing ID in the DOM
- ✓ Verifies accessible names on all `a[href]` and `button` elements
- ✓ Verifies `img[alt]` and checks that empty `alt` is paired with presentation semantics
- ✓ Emits findings containing route, rule ID, and element selector

**Prerequisites:**
- M9.G3.T1, M9.G3.T2, M9.G3.T3 completed
- Target file: `scripts/audit/lib/structure-audit.ts`

**Implementation Details:**

Create `scripts/audit/lib/structure-audit.ts`:

```typescript
import type { BuildLayout } from './build-layout';
import type { AuditReport, Finding, RouteEntry } from './types';
import { buildReport } from './report';
import { readText, listFiles } from './build-layout';
import { parsePage, selectorFor, collectIds, type ParsedPage } from './html';
import { findHeadingOrderViolations } from './checks/headings';
import { findDuplicates } from './checks/uniqueness';
import { computeAccessibleName } from './checks/accessible-name';
import { checkExternalRel, scanMarkers, scanSecrets } from './checks/hygiene';
import { APPROVALS } from './config';

export async function runStructureAudit(
  layout: BuildLayout,
  _args: readonly string[] = []
): Promise<AuditReport> {
  const allFiles = await listFiles(layout);
  const htmlFiles = allFiles.filter(f => f.endsWith('.html') && !f.startsWith('/_'));
  const findings: Finding[] = [];

  for (const file of htmlFiles) {
    const html = await readText(layout, file);
    if (!html) {
      continue;
    }

    const routePath = file === '/index.html'
      ? '/'
      : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');

    const routeEntry: RouteEntry = {
      path: routePath,
      kind: routePath === '/' ? 'home' : 'projects-index',
      slug: null,
    };

    const parsed: ParsedPage = parsePage(routeEntry, file, html);
    const doc = parsed.document;

    // 1. html[lang]
    const htmlEl = doc.documentElement;
    const lang = htmlEl.getAttribute('lang');
    if (!lang || lang.trim() === '') {
      findings.push({
        route: routePath,
        rule: 'html-lang',
        message: 'Missing or empty lang attribute on <html> element.',
        severity: 'error',
        selector: 'html',
      });
    }

    // 2. Exactly one <h1>
    const h1s = doc.querySelectorAll('h1');
    if (h1s.length !== 1) {
      findings.push({
        route: routePath,
        rule: 'h1-count',
        message: `Page must have exactly one <h1> element, found ${h1s.length}.`,
        severity: 'error',
        selector: h1s.length > 0 ? selectorFor(h1s[0]!) : 'html > body',
      });
    }

    // 3. Exactly one <main>
    const mains = doc.querySelectorAll('main');
    if (mains.length !== 1) {
      findings.push({
        route: routePath,
        rule: 'main-count',
        message: `Page must have exactly one <main> element, found ${mains.length}.`,
        severity: 'error',
        selector: mains.length > 0 ? selectorFor(mains[0]!) : 'html > body',
      });
    }

    // 4. Landmarks: header, nav, main, footer
    for (const tag of ['header', 'nav', 'main', 'footer']) {
      if (!doc.querySelector(tag)) {
        findings.push({
          route: routePath,
          rule: 'landmark-missing',
          message: `Required landmark <${tag}> is missing.`,
          severity: 'error',
          selector: 'html > body',
        });
      }
    }

    // 5. Heading levels
    const headings = Array.from(doc.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    const levels = headings.map(h => parseInt(h.tagName.substring(1), 10));
    const skipIndices = findHeadingOrderViolations(levels);
    for (const idx of skipIndices) {
      const el = headings[idx]!;
      const prevEl = headings[idx - 1]!;
      findings.push({
        route: routePath,
        rule: 'heading-skip',
        message: `Heading level skipped downward from <${prevEl.tagName.toLowerCase()}> to <${el.tagName.toLowerCase()}>.`,
        severity: 'error',
        selector: selectorFor(el),
      });
    }

    // 6. Skip link is first focusable element
    const focusable = doc.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusable.length > 0) {
      const first = focusable[0]!;
      const href = first.getAttribute('href') ?? '';
      if (first.tagName.toLowerCase() !== 'a' || !href.startsWith('#')) {
        findings.push({
          route: routePath,
          rule: 'skip-link-first',
          message: 'First focusable element must be an in-page skip link (e.g. href="#main-content").',
          severity: 'error',
          selector: selectorFor(first),
        });
      } else {
        const targetId = href.substring(1);
        if (targetId && !doc.getElementById(targetId)) {
          findings.push({
            route: routePath,
            rule: 'skip-link-first',
            message: `Skip link targets "#${targetId}" which does not exist in the document.`,
            severity: 'error',
            selector: selectorFor(first),
          });
        }
      }
    }

    // 7. Accessible name for anchors and buttons
    const interactiveEls = doc.querySelectorAll('a[href], button');
    for (const el of Array.from(interactiveEls)) {
      const name = computeAccessibleName(el);
      const isButton = el.tagName.toLowerCase() === 'button';
      if (name === '') {
        findings.push({
          route: routePath,
          rule: isButton ? 'button-name' : 'link-name',
          message: `<${el.tagName.toLowerCase()}> must have a non-empty accessible name.`,
          severity: 'error',
          selector: selectorFor(el),
        });
      }
    }

    // 8. Image alt attributes
    const images = doc.querySelectorAll('img');
    for (const img of Array.from(images)) {
      if (!img.hasAttribute('alt')) {
        findings.push({
          route: routePath,
          rule: 'img-alt',
          message: '<img> element missing required alt attribute.',
          severity: 'error',
          selector: selectorFor(img),
        });
      } else {
        const alt = img.getAttribute('alt')!;
        const isPres = img.getAttribute('role') === 'presentation' || img.getAttribute('aria-hidden') === 'true';
        if (alt.trim() === '' && !isPres) {
          findings.push({
            route: routePath,
            rule: 'img-alt',
            message: '<img> with empty alt must have role="presentation" or aria-hidden="true".',
            severity: 'error',
            selector: selectorFor(img),
          });
        }
      }
    }

    // 9. ID uniqueness
    const allIdElements = doc.querySelectorAll('[id]');
    const rawIds = Array.from(allIdElements)
      .map(e => e.getAttribute('id')!.trim())
      .filter(id => id.length > 0);
    const duplicates = findDuplicates(rawIds);
    for (const dupId of duplicates) {
      findings.push({
        route: routePath,
        rule: 'id-duplicate',
        message: `Duplicate ID attribute found: "${dupId}".`,
        severity: 'error',
        selector: `[id="${CSS.escape(dupId)}"]`,
      });
    }
  }

  return buildReport({
    audit: 'structure',
    findings,
    routesChecked: htmlFiles.length,
  });
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/structure-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 3.1–3.9

---

### M9.G3.T5: Implement Hygiene and Privacy Audit Rules

**Objective:** Augment `structure-audit.ts` with external link security checks, script origin verification, forbidden element enforcement, tracking marker detection, cookie checks, and secret scans.

**Acceptance Criteria:**
- ✓ Verifies `rel="noopener noreferrer"` on all external `a[target="_blank"]`
- ✓ Enforces `https:` on all external links
- ✓ Forbids `form`, `input`, `textarea`, `iframe`, and third-party scripts/links
- ✓ Scans inline scripts, attributes, and JS/CSS files for tracking markers per Decision 7
- ✓ Flags any occurrence of `document.cookie` or `set-cookie`
- ✓ Executes `scanSecrets` on all build files

**Prerequisites:**
- M9.G3.T4 completed
- Target file: `scripts/audit/lib/structure-audit.ts`

**Implementation Details:**

Update `scripts/audit/lib/structure-audit.ts` to include hygiene inspection:

```typescript
// Add into loop for each HTML page in scripts/audit/lib/structure-audit.ts:

    // 10. External link rel and protocol
    const anchors = doc.querySelectorAll('a[href]');
    for (const a of Array.from(anchors)) {
      const href = a.getAttribute('href')!.trim();
      const isExternal = /^https?:\/\//i.test(href);

      if (isExternal) {
        if (!href.startsWith('https://')) {
          findings.push({
            route: routePath,
            rule: 'external-http',
            message: `External link "${href}" must use secure https: protocol.`,
            severity: 'error',
            selector: selectorFor(a),
          });
        }
        if (a.getAttribute('target') === '_blank') {
          const rel = a.getAttribute('rel');
          if (!checkExternalRel(rel)) {
            findings.push({
              route: routePath,
              rule: 'external-rel',
              message: 'External link with target="_blank" must contain rel="noopener noreferrer".',
              severity: 'error',
              selector: selectorFor(a),
            });
          }
        }
      }
    }

    // 11. Script origins and forbidden inline scripts
    const scripts = doc.querySelectorAll('script');
    for (const s of Array.from(scripts)) {
      const src = s.getAttribute('src');
      const type = s.getAttribute('type');

      if (src) {
        if (!src.startsWith('/_next/') && !src.startsWith('/') && !src.startsWith('./')) {
          findings.push({
            route: routePath,
            rule: 'script-origin',
            message: `External script origin forbidden: "${src}".`,
            severity: 'error',
            selector: selectorFor(s),
          });
        }
      } else {
        const text = s.textContent ?? '';
        const isJsonLd = type === 'application/ld+json';
        const isNextPayload = s.getAttribute('data-next-f') !== null || text.includes('__next_f') || text.includes('self.__next');

        if (!isJsonLd && !isNextPayload && text.trim().length > 0) {
          findings.push({
            route: routePath,
            rule: 'script-origin',
            message: 'Unrecognized inline script detected.',
            severity: 'error',
            selector: selectorFor(s),
          });
        }
      }
    }

    // 12. Forbidden elements
    const forbidden = doc.querySelectorAll('form, input, textarea, iframe');
    for (const el of Array.from(forbidden)) {
      findings.push({
        route: routePath,
        rule: 'forbidden-element',
        message: `Forbidden interactive element <${el.tagName.toLowerCase()}> found in P0 static output.`,
        severity: 'error',
        selector: selectorFor(el),
      });
    }

    // 13. Tracking markers in attributes and inline scripts (Decision 7)
    const markerMatches = scanMarkers(html);
    for (const m of markerMatches) {
      findings.push({
        route: routePath,
        rule: 'tracking-marker',
        message: `Disallowed tracking marker detected: "${m.matched}".`,
        severity: 'error',
        file,
      });
    }

    // 14. Cookie markers
    if (/document\.cookie/i.test(html) || /http-equiv=["']set-cookie["']/i.test(html)) {
      findings.push({
        route: routePath,
        rule: 'cookie-reference',
        message: 'Cookie access or Set-Cookie header detected in static document.',
        severity: 'error',
        file,
      });
    }

  // Outside the HTML loop: scan all build files for secrets and cookie references in JS chunks
  for (const f of allFiles) {
    const text = await readText(layout, f);
    if (!text) {
      continue;
    }

    if (f.endsWith('.js') && /document\.cookie/i.test(text)) {
      findings.push({
        route: '*',
        rule: 'cookie-reference',
        message: 'Reference to document.cookie detected in JavaScript bundle.',
        severity: 'error',
        file: f,
      });
    }

    const secrets = scanSecrets(text, f);
    for (const s of secrets) {
      findings.push({
        route: '*',
        rule: 'secret-marker',
        message: `Sensitive credential or secret pattern matched in file "${f}".`,
        severity: 'error',
        file: f,
      });
    }
  }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/structure-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 5.1–5.8

---

### M9.G3.T6: Verify Properties 10 and 11 (Headings and Duplicates)

**Objective:** Author unit and fast-check property tests for heading order violations (Property 10) and duplicate value detection (Property 11).

**Acceptance Criteria:**
- ✓ Unit tests verify heading edge cases (ascending, descending, single heading, multiple skips)
- ✓ Fast-check Property 10 verifies that `findHeadingOrderViolations` returns exactly the downward skips across $\ge 100$ runs
- ✓ Fast-check Property 11 verifies that `findDuplicates` returns repeated values once in first-seen order across $\ge 100$ runs

**Prerequisites:**
- M9.G3.T1 completed
- Target files: `tests/audit/headings.test.ts`, `tests/audit/uniqueness.test.ts`

**Implementation Details:**

1. Create `tests/audit/headings.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { findHeadingOrderViolations } from '../../scripts/audit/lib/checks/headings';

describe('Heading Sequence Checks', () => {
  it('passes on valid sequential headings', () => {
    expect(findHeadingOrderViolations([1, 2, 3, 2, 3, 4, 1])).toEqual([]);
  });

  it('detects downward skips', () => {
    expect(findHeadingOrderViolations([1, 3])).toEqual([1]);
    expect(findHeadingOrderViolations([1, 2, 4, 2, 5])).toEqual([2, 4]);
  });

  // Feature: m9-quality-accessibility-performance, Property 10: Heading order violations are exactly the downward skips
  it('Property 10: Heading order violations are exactly the downward skips', () => {
    fc.assert(
      fc.property(
        fc.array(fc.integer({ min: 1, max: 6 }), { minLength: 0, maxLength: 20 }),
        levels => {
          const violations = findHeadingOrderViolations(levels);

          for (let i = 1; i < levels.length; i++) {
            const isSkip = levels[i]! > levels[i - 1]! + 1;
            if (isSkip) {
              expect(violations).toContain(i);
            } else {
              expect(violations).not.toContain(i);
            }
          }
          expect(violations).not.toContain(0);
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

2. Create `tests/audit/uniqueness.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { findDuplicates } from '../../scripts/audit/lib/checks/uniqueness';

describe('Duplicate Detection Checks', () => {
  it('returns empty array when all elements are unique', () => {
    expect(findDuplicates(['a', 'b', 'c'])).toEqual([]);
  });

  it('identifies duplicate items once in first-seen order', () => {
    expect(findDuplicates(['a', 'b', 'a', 'c', 'b', 'a'])).toEqual(['a', 'b']);
  });

  // Feature: m9-quality-accessibility-performance, Property 11: Duplicate detection returns exactly the repeated values
  it('Property 11: Duplicate detection returns exactly the repeated values', () => {
    fc.assert(
      fc.property(
        fc.array(fc.string({ minLength: 1, maxLength: 10 }), { maxLength: 30 }),
        items => {
          const dups = findDuplicates(items);
          const seen = new Set<string>();
          const expectedDups = new Set<string>();

          for (const item of items) {
            if (seen.has(item)) {
              expectedDups.add(item);
            } else {
              seen.add(item);
            }
          }

          expect(new Set(dups)).toEqual(expectedDups);
          expect(dups.length).toBe(expectedDups.size);
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
npx vitest run tests/audit/headings.test.ts tests/audit/uniqueness.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 3.4, Req 3.8

---

### M9.G3.T7: Verify Property 14 (Rel Security Tokens) and Hygiene Tests

**Objective:** Author unit and fast-check property tests for `checkExternalRel` (Property 14) and privacy marker/secret scanning.

**Acceptance Criteria:**
- ✓ Unit tests verify scanning of tracking hosts, tracking call expressions, and secret tokens
- ✓ Confirms that benign router words like `"segment"` in router JS or `"gtag"` inside prose do not trigger false positives
- ✓ Fast-check Property 14 verifies that `checkExternalRel` passes if and only if both `noopener` and `noreferrer` are present across $\ge 100$ runs

**Prerequisites:**
- M9.G3.T3 completed
- Target file: `tests/audit/hygiene.test.ts`

**Implementation Details:**

Create `tests/audit/hygiene.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { checkExternalRel, scanMarkers, scanSecrets } from '../../scripts/audit/lib/checks/hygiene';

describe('Hygiene Checkers Unit Tests', () => {
  it('detects tracking host markers in URLs', () => {
    const html = '<script src="https://www.google-analytics.com/analytics.js"></script>';
    const matches = scanMarkers(html);
    expect(matches.some(m => m.matched === 'google-analytics.com')).toBe(true);
  });

  it('detects tracking call expressions', () => {
    const script = 'window.dataLayer = window.dataLayer || []; gtag("event", "click");';
    const matches = scanMarkers(script);
    expect(matches.some(m => m.matched === 'gtag(')).toBe(true);
    expect(matches.some(m => m.matched === 'window.dataLayer')).toBe(true);
  });

  it('detects AWS access keys and private key markers', () => {
    const secretContent = 'AKIAIOSFODNN7EXAMPLE and -----BEGIN RSA PRIVATE KEY-----';
    const matches = scanSecrets(secretContent, 'test.js');
    expect(matches.length).toBe(2);
  });
});

describe('Hygiene Properties', () => {
  // Feature: m9-quality-accessibility-performance, Property 14: External link rel check requires both tokens
  it('Property 14: External link rel check requires both tokens', () => {
    const tokenList = ['noopener', 'noreferrer', 'nofollow', 'external', 'ugc'];

    fc.assert(
      fc.property(
        fc.subarray(tokenList),
        tokens => {
          const shuffled = [...tokens].sort(() => Math.random() - 0.5);
          const relString = shuffled.join('   ');
          const result = checkExternalRel(relString);

          const lowerTokens = tokens.map(t => t.toLowerCase());
          const hasNoopener = lowerTokens.includes('noopener');
          const hasNoreferrer = lowerTokens.includes('noreferrer');

          expect(result).toBe(hasNoopener && hasNoreferrer);
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
npx vitest run tests/audit/hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.5, Req 5.7

---

### M9.G3.T8: Author Structure Audit Fixture Integration Tests

**Objective:** Validate `runStructureAudit` against static fixture trees in `tests/audit/fixtures/` to verify zero findings on passing trees and exact single findings on defect fixtures.

**Acceptance Criteria:**
- ✓ `passing-site/` produces 0 findings
- ✓ `two-h1.html` produces exactly one `h1-count` error
- ✓ `skipped-heading.html` produces exactly one `heading-skip` error
- ✓ `empty-link.html` produces exactly one `link-name` error
- ✓ `missing-alt.html` produces exactly one `img-alt` error
- ✓ `broken-hash.html` produces exactly one `skip-link-first` error
- ✓ `external-http.html` produces exactly one `external-http` error
- ✓ `blank-no-rel.html` produces exactly one `external-rel` error
- ✓ `duplicate-id.html` produces exactly one `id-duplicate` error

**Prerequisites:**
- M9.G3.T5 completed
- Target file: `tests/audit/structure-audit.test.ts`

**Implementation Details:**

Create `tests/audit/structure-audit.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as path from 'node:path';
import { resolveBuildLayout } from '../../scripts/audit/lib/build-layout';
import { runStructureAudit } from '../../scripts/audit/lib/structure-audit';

describe('Structure Audit Fixture Integration', () => {
  const fixturesRoot = path.join(process.cwd(), 'tests', 'audit', 'fixtures');

  it('produces zero errors on compliant passing-site fixture', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(fixturesRoot, 'passing-site'),
    });
    expect(layout).not.toBeNull();
    const report = await runStructureAudit(layout!);
    expect(report.summary.errors).toBe(0);
    expect(report.status).toBe('pass');
  });

  it('detects single isolated defects on defect fixtures', async () => {
    const layout = await resolveBuildLayout({
      AUDIT_BUILD_DIR: path.join(fixturesRoot, 'defects'),
    });
    expect(layout).not.toBeNull();
    const report = await runStructureAudit(layout!);

    const ruleNames = report.findings.map(f => f.rule);
    expect(ruleNames).toContain('h1-count');
    expect(ruleNames).toContain('heading-skip');
    expect(ruleNames).toContain('link-name');
    expect(ruleNames).toContain('img-alt');
    expect(ruleNames).toContain('skip-link-first');
    expect(ruleNames).toContain('external-http');
    expect(ruleNames).toContain('external-rel');
    expect(ruleNames).toContain('id-duplicate');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structure-audit.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 3.1–3.9, Req 5.1–5.8

---

### M9.G3.T9: Add JSON-LD Block Validation and CLI Entrypoint

**Objective:** Add schema.org JSON-LD parsing checks to `structure-audit.ts` and create the CLI entry point `scripts/audit/structure.ts`.

**Acceptance Criteria:**
- ✓ Parses every `<script type="application/ld+json">` as valid JSON
- ✓ Verifies `@context` equals `'https://schema.org'`
- ✓ Checks expected `@type` based on route kind (`home` $\rightarrow$ `Person`, `blog-detail` $\rightarrow$ `Article` & `BreadcrumbList`, `project-detail` $\rightarrow$ `BreadcrumbList`)
- ✓ Emits `jsonld-invalid`, `jsonld-type`, or `jsonld-unexpected` errors
- ✓ Creates executable CLI `scripts/audit/structure.ts` wired through `runCli`

**Prerequisites:**
- M9.G3.T8 completed
- Target files: `scripts/audit/lib/structure-audit.ts`, `scripts/audit/structure.ts`

**Implementation Details:**

1. Append JSON-LD script validation block inside HTML loop in `scripts/audit/lib/structure-audit.ts`:

```typescript
    // 15. JSON-LD validation (Approval A5 enabled)
    if (APPROVALS.jsonLdIntegration) {
      const jsonLdScripts = doc.querySelectorAll('script[type="application/ld+json"]');
      for (const s of Array.from(jsonLdScripts)) {
        const text = s.textContent ?? '';
        try {
          const parsedJson = JSON.parse(text) as Record<string, unknown>;
          if (parsedJson['@context'] !== 'https://schema.org') {
            findings.push({
              route: routePath,
              rule: 'jsonld-invalid',
              message: 'JSON-LD @context must equal "https://schema.org".',
              severity: 'error',
              selector: selectorFor(s),
            });
          }
          const type = parsedJson['@type'];
          if (routePath === '/' && type !== 'Person') {
            findings.push({
              route: routePath,
              rule: 'jsonld-type',
              message: `Expected JSON-LD @type "Person" on homepage, found "${String(type)}".`,
              severity: 'error',
              selector: selectorFor(s),
            });
          }
        } catch {
          findings.push({
            route: routePath,
            rule: 'jsonld-invalid',
            message: 'Invalid JSON inside application/ld+json script block.',
            severity: 'error',
            selector: selectorFor(s),
          });
        }
      }
    }
```

2. Create `scripts/audit/structure.ts`:

```typescript
import { runCli } from './lib/cli';
import { runStructureAudit } from './lib/structure-audit';

void runCli('structure', (layout, args) => runStructureAudit(layout, args));
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/structure.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.6, Req 16.1

---

### M9.G3.T10: Milestone 9 Goal 3 Checkpoint Verification

**Objective:** Execute all Goal 3 test suites, run CLI dry-run over fixtures, and confirm full type-checking and lint compliance.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/` pass (including Properties 10, 11, and 14)
- ✓ CLI `npx vite-node --config vitest.config.ts scripts/audit/structure.ts` executes over `AUDIT_BUILD_DIR`
- ✓ `npm run typecheck` exits with 0
- ✓ `npm run lint` exits with 0

**Prerequisites:**
- M9.G3.T1 through M9.G3.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G3 suites
npx vitest run tests/audit/headings.test.ts tests/audit/uniqueness.test.ts tests/audit/accessible-name.test.ts tests/audit/hygiene.test.ts tests/audit/structure-audit.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Run CLI against passing fixtures
$env:AUDIT_BUILD_DIR = "tests/audit/fixtures/passing-site"
npx vite-node --config vitest.config.ts scripts/audit/structure.ts
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item env:AUDIT_BUILD_DIR

# 3. Static type checking
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

**Satisfies Requirements:** Req 1.5, Req 3.1–3.9, Req 5.1–5.8, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/headings.test.ts tests/audit/uniqueness.test.ts tests/audit/hygiene.test.ts tests/audit/structure-audit.test.ts
npm run typecheck
npm run lint
```
Expected output:
- All test suites pass (including Properties 10, 11, and 14)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.