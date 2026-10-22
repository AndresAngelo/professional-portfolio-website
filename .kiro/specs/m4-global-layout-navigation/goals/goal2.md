# M4.G2: Pure Logic Modules and Property Tests

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the four core, directive-free, React-free pure logic modules underpinning layout and navigation: `current-route.ts`, `contact-channels.ts`, `nav-entries.ts`, and `disclosure.ts`. Ensure route matching strictly respects segment boundaries (preventing false positives such as `/projectsfoo` matching `/projects`), resolves longest-prefix ties deterministically, and marks at most one active navigation entry. Guarantee that navigation entries are derived in canonical order (`/`, `/projects`, `/certifications`, `/blog`) and dynamically append a `#contact` anchor if and only if renderable contact channels exist. Enforce disclosure state machine transitions as an exhaustive reducer, and implement non-mutating contact channel ordering (placing primary channels first and dropping unrenderable or non-HTTPS URLs). Cover all four modules with comprehensive Vitest unit tests and fast-check property tests validating Properties 1, 2, 3, 4, 5, and 7.

## Goal Success Criteria

- ✓ `src/components/layout/current-route.ts` implements `isCurrentRoute` and `getCurrentEntryIndex` with segment-boundary precision and zero React/Next.js dependencies
- ✓ `src/components/layout/contact-channels.ts` implements `getRenderableChannels` and `orderContactChannels` without mutating input arrays
- ✓ `src/components/layout/nav-entries.ts` implements `buildNavEntries` with canonical rank ordering and dynamic derived Contact entry appending
- ✓ `src/components/layout/disclosure.ts` implements `disclosureReducer` as an exhaustive pure state machine
- ✓ All four modules contain zero `'use client'` statements and zero React imports
- ✓ Unit tests in `tests/unit/components/layout/current-route.test.ts` pass, verifying exact matches, nested slugs, root path exclusivity, and prefix isolation
- ✓ Property-based tests for Property 1 and Property 2 execute $\ge 100$ iterations with `fast-check`
- ✓ Unit and property tests in `tests/unit/components/layout/nav-entries.test.ts` validate Properties 3 and 4
- ✓ Model-based property tests in `tests/unit/components/layout/disclosure.test.ts` validate Property 5
- ✓ Unit and property tests in `tests/unit/components/layout/contact-channels.test.ts` validate Property 7
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goal M4.G1 completed successfully
- Test fixtures available at `tests/fixtures/site-config.ts`
- Arbitraries available at `tests/fixtures/site-config-arbitraries.ts`
- M3 URL validation helper `resolveExternalHref` available at `src/components/ui/external-link-attrs.ts`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M4.G2.T1: Implement Current-Route Matching Logic (`src/components/layout/current-route.ts`)

**Objective:** Author the pure, directive-free route matching functions `isCurrentRoute` and `getCurrentEntryIndex` in `src/components/layout/current-route.ts`.

**Acceptance Criteria:**
- ✓ File `src/components/layout/current-route.ts` created
- ✓ Exports `isCurrentRoute(pathname: string | null, href: string): boolean`
- ✓ Normalizes trailing slashes (except root `/`)
- ✓ Treats `/` as exact-only match (`'/'` does NOT match `'/projects'`)
- ✓ Matches exact path or path followed immediately by `/` segment boundary (`'/projects/my-app'` matches `'/projects'`, but `'/projectsfoo'` does NOT)
- ✓ Exports `getCurrentEntryIndex(pathname: string | null, hrefs: readonly (string | null)[]): number | null`
- ✓ Resolves longest matching href; resolves ties by first matching index
- ✓ Returns `null` when `pathname` is `null` or matches no href
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M4.G1 completed
- Target file: `src/components/layout/current-route.ts`

**Implementation Details:**

Write `src/components/layout/current-route.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Route Matching Logic
 *
 * Provides segment-boundary aware current-route matching and active index resolution.
 * Contains no React, Next.js, or browser dependencies (Req 5.7).
 */

/**
 * Normalizes trailing slashes, preserving the root slash.
 */
function normalize(path: string): string {
  return path.length > 1 && path.endsWith('/') ? path.slice(0, -1) : path;
}

/**
 * Determines whether the active pathname corresponds to the given navigation href.
 * - Root path ('/') matches only exact root.
 * - Subpaths match exact href or href followed by a segment slash ('/projects/slug').
 * - Partial segment prefixes do NOT match ('/projectsfoo' does not match '/projects').
 */
export function isCurrentRoute(pathname: string | null, href: string): boolean {
  if (pathname === null) {
    return false;
  }
  const path = normalize(pathname);
  const target = normalize(href);

  if (target === '/') {
    return path === '/';
  }

  return path === target || path.startsWith(`${target}/`);
}

/**
 * Resolves the index of the single active navigation entry.
 * Selects the longest matching href (deepest route match); on equal lengths, the first index wins.
 * Returns null if no entry matches (Req 5.4).
 */
export function getCurrentEntryIndex(
  pathname: string | null,
  hrefs: readonly (string | null)[]
): number | null {
  if (pathname === null) {
    return null;
  }

  let bestIndex: number | null = null;
  let bestLength = -1;

  hrefs.forEach((href, index) => {
    if (href === null || !isCurrentRoute(pathname, href)) {
      return;
    }
    if (href.length > bestLength) {
      bestIndex = index;
      bestLength = href.length;
    }
  });

  return bestIndex;
}
'@ | Set-Content "src\components\layout\current-route.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/current-route.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.4, Req 5.5, Req 5.6, Req 5.7

---

### M4.G2.T2: Implement Contact Channels Filtering & Ordering (`src/components/layout/contact-channels.ts`)

**Objective:** Author pure helper functions `getRenderableChannels` and `orderContactChannels` in `src/components/layout/contact-channels.ts`.

**Acceptance Criteria:**
- ✓ File `src/components/layout/contact-channels.ts` created
- ✓ Exports `getRenderableChannels(channels: readonly ContactChannel[]): ContactChannel[]`
- ✓ Filters out email channels that do not start with `mailto:` or have empty addresses
- ✓ Filters out non-email channels that fail `resolveExternalHref` (non-HTTPS or malformed)
- ✓ Exports `orderContactChannels(channels: readonly ContactChannel[]): ContactChannel[]`
- ✓ Places `isPrimary: true` channels before non-primary channels while preserving relative order
- ✓ Never mutates input arrays (pure function)
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M4.G1 completed
- `src/components/ui/external-link-attrs.ts` exists (exports `resolveExternalHref`)
- Target file: `src/components/layout/contact-channels.ts`

**Implementation Details:**

Write `src/components/layout/contact-channels.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Contact Channel Utilities
 *
 * Manages protocol filtering and stable priority sorting for public contact links.
 * Contains no React, Next.js, or browser dependencies (Req 9.4, 9.7).
 */
import type { ContactChannel } from '@/types/content';
import { resolveExternalHref } from '@/components/ui/external-link-attrs';

/**
 * Filters out unrenderable or invalid channels.
 * - Email channels must have a valid mailto: URL with a recipient address.
 * - All other channels must be valid absolute HTTPS URLs.
 */
export function getRenderableChannels(
  channels: readonly ContactChannel[]
): ContactChannel[] {
  return channels.filter((channel) => {
    if (typeof channel.url !== 'string') {
      return false;
    }
    const trimmedUrl = channel.url.trim();
    if (channel.type === 'email') {
      return trimmedUrl.startsWith('mailto:') && trimmedUrl.length > 'mailto:'.length;
    }
    return resolveExternalHref(trimmedUrl) !== null;
  });
}

/**
 * Returns a stable permutation of contact channels with primary channels listed first.
 * Does not mutate the input array (Req 9.4).
 */
export function orderContactChannels(
  channels: readonly ContactChannel[]
): ContactChannel[] {
  const primaries: ContactChannel[] = [];
  const nonPrimaries: ContactChannel[] = [];

  for (const channel of channels) {
    if (channel.isPrimary) {
      primaries.push(channel);
    } else {
      nonPrimaries.push(channel);
    }
  }

  return [...primaries, ...nonPrimaries];
}
'@ | Set-Content "src\components\layout\contact-channels.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/contact-channels.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 8.6, Req 9.1, Req 9.2, Req 9.4, Req 9.7

---

### M4.G2.T3: Implement Navigation Entry Derivation (`src/components/layout/nav-entries.ts`)

**Objective:** Author pure helper function `buildNavEntries` in `src/components/layout/nav-entries.ts` sorting entries by canonical rank and dynamically deriving the `#contact` anchor.

**Acceptance Criteria:**
- ✓ File `src/components/layout/nav-entries.ts` created
- ✓ Exports `NavEntry` interface: `{ label: string; href: string; kind: 'route' | 'anchor' }`
- ✓ Exports `buildNavEntries(navigation: readonly SiteNavigationItem[], contactChannels: readonly ContactChannel[]): NavEntry[]`
- ✓ Canonical rank order enforced: `/` $\rightarrow$ `/projects` $\rightarrow$ `/certifications` $\rightarrow$ `/blog`
- ✓ Unknown navigation hrefs follow canonical entries, maintaining their original relative config order
- ✓ Appends `{ label: 'Contact', href: '#contact', kind: 'anchor' }` if and only if `getRenderableChannels(contactChannels).length > 0`
- ✓ Omits Contact entry if no renderable contact channels exist
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M4.G2.T2 completed
- `src/components/layout/layout-text.ts` exists (exports `CONTACT_NAV_LABEL`, `CONTACT_REGION_ID`)
- Target file: `src/components/layout/nav-entries.ts`

**Implementation Details:**

Write `src/components/layout/nav-entries.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Navigation Entry Derivation Logic
 *
 * Enforces canonical navigation sequence and dynamically generates the anchor Contact link.
 * Contains no React, Next.js, or browser dependencies (Req 4.2, 4.4, 4.5).
 */
import type { ContactChannel, SiteNavigationItem } from '@/types/content';
import { CONTACT_NAV_LABEL, CONTACT_REGION_ID } from './layout-text';
import { getRenderableChannels } from './contact-channels';

export interface NavEntry {
  label: string;
  href: string;
  /**
   * 'route' entries participate in path matching.
   * 'anchor' entries are same-page hash jumps and never match pathnames.
   */
  kind: 'route' | 'anchor';
}

const CANONICAL_ORDER: readonly string[] = [
  '/',
  '/projects',
  '/certifications',
  '/blog',
];

/**
 * Builds the ordered navigation entries list for SiteHeader and MobileNavToggle.
 */
export function buildNavEntries(
  navigation: readonly SiteNavigationItem[],
  contactChannels: readonly ContactChannel[]
): NavEntry[] {
  // 1. Map config items to route entries
  const routeEntries: NavEntry[] = navigation.map((item) => ({
    label: item.label,
    href: item.href,
    kind: 'route',
  }));

  // 2. Stable sort by canonical rank
  routeEntries.sort((a, b) => {
    const rankA = CANONICAL_ORDER.indexOf(a.href);
    const rankB = CANONICAL_ORDER.indexOf(b.href);

    const effectiveRankA = rankA === -1 ? CANONICAL_ORDER.length : rankA;
    const effectiveRankB = rankB === -1 ? CANONICAL_ORDER.length : rankB;

    return effectiveRankA - effectiveRankB;
  });

  // 3. Dynamically append Contact anchor if renderable contact channels exist
  const renderableContacts = getRenderableChannels(contactChannels);
  if (renderableContacts.length > 0) {
    routeEntries.push({
      label: CONTACT_NAV_LABEL,
      href: `#${CONTACT_REGION_ID}`,
      kind: 'anchor',
    });
  }

  return routeEntries;
}
'@ | Set-Content "src\components\layout\nav-entries.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/nav-entries.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 4.5, Req 4.7

---

### M4.G2.T4: Implement Disclosure State Machine (`src/components/layout/disclosure.ts`)

**Objective:** Author the pure state reducer `disclosureReducer` in `src/components/layout/disclosure.ts` governing mobile menu disclosure transitions.

**Acceptance Criteria:**
- ✓ File `src/components/layout/disclosure.ts` created
- ✓ Exports `DisclosureState = 'collapsed' | 'expanded'`
- ✓ Exports `DisclosureEvent = 'TOGGLE' | 'ESCAPE' | 'LINK_ACTIVATED' | 'ROUTE_CHANGED'`
- ✓ Exports `disclosureReducer(state: DisclosureState, event: DisclosureEvent): DisclosureState`
- ✓ `TOGGLE` inverts state (`collapsed` $\rightarrow$ `expanded`, `expanded` $\rightarrow$ `collapsed`)
- ✓ `ESCAPE`, `LINK_ACTIVATED`, and `ROUTE_CHANGED` always return `collapsed`
- ✓ Switch statement is compile-time exhaustive across `DisclosureEvent`
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M4.G1 completed
- Target file: `src/components/layout/disclosure.ts`

**Implementation Details:**

Write `src/components/layout/disclosure.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Disclosure State Machine
 *
 * Governs MobileNavToggle visibility transitions with zero side effects.
 * Contains no React, Next.js, or browser dependencies (Req 6.4, 6.5, 6.6, 6.7).
 */

export type DisclosureState = 'collapsed' | 'expanded';

export type DisclosureEvent =
  | 'TOGGLE'
  | 'ESCAPE'
  | 'LINK_ACTIVATED'
  | 'ROUTE_CHANGED';

/**
 * Pure reducer function for mobile navigation disclosure state.
 */
export function disclosureReducer(
  state: DisclosureState,
  event: DisclosureEvent
): DisclosureState {
  switch (event) {
    case 'TOGGLE':
      return state === 'collapsed' ? 'expanded' : 'collapsed';
    case 'ESCAPE':
    case 'LINK_ACTIVATED':
    case 'ROUTE_CHANGED':
      return 'collapsed';
    default: {
      const _exhaustiveCheck: never = event;
      return _exhaustiveCheck;
    }
  }
}
'@ | Set-Content "src\components\layout\disclosure.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/disclosure.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.4, Req 6.5, Req 6.6, Req 6.7

---

### M4.G2.T5: Audit Pure Modules for Zero React/Next.js Directives

**Objective:** Inspect all 4 pure modules (`current-route.ts`, `contact-channels.ts`, `nav-entries.ts`, `disclosure.ts`) to ensure zero `'use client'` statements and zero runtime framework dependencies exist.

**Acceptance Criteria:**
- ✓ Confirms zero occurrences of `'use client'` or `"use client"` in the four files
- ✓ Confirms zero imports from `'react'` or `'next/*'` in the four files
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G2.T1 through M4.G2.T4 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$pureFiles = @(
    "src\components\layout\current-route.ts",
    "src\components\layout\contact-channels.ts",
    "src\components\layout\nav-entries.ts",
    "src\components\layout\disclosure.ts"
)

$violations = @()

foreach ($file in $pureFiles) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' directive found in $file"
    }
    if ($content -match "\bfrom\s+['""](react|next|next\/[^'""]+)['""]") {
        $violations += "Forbidden React/Next import found in $file"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 5.7, Req 6.10, Req 14.1, Req 14.8

---

### M4.G2.T6: Author Unit & Property-Based Tests for Current-Route Matching (`tests/unit/components/layout/current-route.test.ts`)

**Objective:** Implement comprehensive unit and property-based tests for `isCurrentRoute` and `getCurrentEntryIndex` in `tests/unit/components/layout/current-route.test.ts` validating Properties 1 and 2.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/current-route.test.ts` created
- ✓ Tests exact path matching (`/` matches `/`, `/projects` matches `/projects`)
- ✓ Tests nested route matching (`/projects/example-project` matches `/projects`)
- ✓ Tests segment-boundary enforcement (`/projectsfoo` does NOT match `/projects`)
- ✓ Tests trailing slash normalization (`/projects/` matches `/projects`)
- ✓ Tests `null` pathname returns `false` / `null`
- ✓ Implements Property 1 test ($\ge 100$ runs with `fast-check`): route matching respects segment boundaries
- ✓ Implements Property 2 test ($\ge 100$ runs with `fast-check`): at most one entry is current; root marks only `/`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G2.T1 completed
- `fast-check` installed
- Target file: `tests/unit/components/layout/current-route.test.ts`

**Implementation Details:**

Write `tests/unit/components/layout/current-route.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { isCurrentRoute, getCurrentEntryIndex } from '@/components/layout/current-route';

describe('Current Route Matching Logic (Req 5)', () => {
  describe('Unit Scenarios', () => {
    it('matches exact root path and rejects root on subpaths', () => {
      expect(isCurrentRoute('/', '/')).toBe(true);
      expect(isCurrentRoute('/projects', '/')).toBe(false);
      expect(isCurrentRoute('/certifications', '/')).toBe(false);
    });

    it('matches exact and nested segment paths', () => {
      expect(isCurrentRoute('/projects', '/projects')).toBe(true);
      expect(isCurrentRoute('/projects/portfolio-v2', '/projects')).toBe(true);
      expect(isCurrentRoute('/blog/first-meetup', '/blog')).toBe(true);
    });

    it('enforces strict segment boundary matching without partial prefixes', () => {
      expect(isCurrentRoute('/projectsfoo', '/projects')).toBe(false);
      expect(isCurrentRoute('/blog-post', '/blog')).toBe(false);
      expect(isCurrentRoute('/certificates', '/certifications')).toBe(false);
    });

    it('normalizes trailing slashes safely', () => {
      expect(isCurrentRoute('/projects/', '/projects')).toBe(true);
      expect(isCurrentRoute('/projects', '/projects/')).toBe(true);
      expect(isCurrentRoute('/projects/app/', '/projects')).toBe(true);
    });

    it('handles null pathnames gracefully', () => {
      expect(isCurrentRoute(null, '/projects')).toBe(false);
      expect(getCurrentEntryIndex(null, ['/', '/projects'])).toBeNull();
    });

    it('resolves the longest matching href and handles ties by first index', () => {
      const hrefs = ['/', '/projects', '/projects/special'];
      expect(getCurrentEntryIndex('/projects/special/details', hrefs)).toBe(2);
      expect(getCurrentEntryIndex('/projects/other', hrefs)).toBe(1);
      expect(getCurrentEntryIndex('/', hrefs)).toBe(0);
      expect(getCurrentEntryIndex('/unknown', hrefs)).toBeNull();
    });
  });

  describe('Property-Based Invariants (Property 1 & 2)', () => {
    it('Feature: m4-global-layout-navigation, Property 1: route matching respects segment boundaries for any path and segment', () => {
      fc.assert(
        fc.property(
          fc.constantFrom('/projects', '/certifications', '/blog', '/docs'),
          fc.string({ minLength: 1, maxLength: 15 }).filter((s) => /^[a-z0-9-]+$/.test(s)),
          fc.char().filter((c) => c !== '/' && c !== ''),
          (baseHref, segment, nonSlashChar) => {
            // Exact match
            expect(isCurrentRoute(baseHref, baseHref)).toBe(true);
            // Nested valid segment match
            expect(isCurrentRoute(`${baseHref}/${segment}`, baseHref)).toBe(true);
            // Partial segment prefix mismatch
            expect(isCurrentRoute(`${baseHref}${nonSlashChar}${segment}`, baseHref)).toBe(false);
            // Null pathname safety
            expect(isCurrentRoute(null, baseHref)).toBe(false);
          }
        ),
        { numRuns: 100 }
      );
    });

    it('Feature: m4-global-layout-navigation, Property 2: at most one entry is marked current, and root marks only Home', () => {
      fc.assert(
        fc.property(
          fc.oneof(
            fc.constant('/'),
            fc.constant('/projects'),
            fc.constant('/projects/item-1'),
            fc.constant('/blog'),
            fc.constant('/unknown-route')
          ),
          fc.shuffledSubarray(['/', '/projects', '/certifications', '/blog', null, '/custom']),
          (pathname, hrefs) => {
            const index = getCurrentEntryIndex(pathname, hrefs);

            if (index !== null) {
              expect(index).toBeGreaterThanOrEqual(0);
              expect(index).toBeLessThan(hrefs.length);
              const matchedHref = hrefs[index];
              expect(matchedHref).not.toBeNull();
              if (pathname === '/') {
                expect(matchedHref).toBe('/');
              }
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\unit\components\layout\current-route.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/current-route.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.4, Req 5.5, Req 5.6, Req 5.7, Req 15.2, Req 15.6

---

### M4.G2.T7: Author Unit & Property-Based Tests for Navigation Entries (`tests/unit/components/layout/nav-entries.test.ts`)

**Objective:** Implement unit and property-based tests for `buildNavEntries` in `tests/unit/components/layout/nav-entries.test.ts` validating Properties 3 and 4.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/nav-entries.test.ts` created
- ✓ Tests canonical ordering (`/`, `/projects`, `/certifications`, `/blog`) regardless of config ordering
- ✓ Tests Contact entry is appended when renderable contact channels exist
- ✓ Tests Contact entry is omitted when contact channels are empty or invalid
- ✓ Implements Property 3 test ($\ge 100$ runs with `fast-check`): entries are canonically ordered and sourced from config
- ✓ Implements Property 4 test ($\ge 100$ runs with `fast-check`): Contact entry appended iff renderable channel exists
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G2.T3 completed
- Arbitraries available at `tests/fixtures/site-config-arbitraries.ts`
- Target file: `tests/unit/components/layout/nav-entries.test.ts`

**Implementation Details:**

Write `tests/unit/components/layout/nav-entries.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { buildNavEntries } from '@/components/layout/nav-entries';
import { getRenderableChannels } from '@/components/layout/contact-channels';
import {
  validSiteConfig,
  emptyContactChannelsSiteConfig,
  reorderedNavSiteConfig,
} from '../../../fixtures/site-config';
import {
  navItemArbitrary,
  contactChannelArbitrary,
} from '../../../fixtures/site-config-arbitraries';

describe('Navigation Entries Derivation (Req 4)', () => {
  describe('Unit Scenarios', () => {
    it('orders standard navigation items into canonical sequence and appends Contact', () => {
      const entries = buildNavEntries(
        reorderedNavSiteConfig.navigation,
        validSiteConfig.contactChannels
      );

      expect(entries.map((e) => e.href)).toEqual([
        '/',
        '/projects',
        '/certifications',
        '/blog',
        '/docs',
        '#contact',
      ]);

      const contactEntry = entries[entries.length - 1];
      expect(contactEntry.label).toBe('Contact');
      expect(contactEntry.kind).toBe('anchor');
    });

    it('omits Contact entry when contactChannels is empty', () => {
      const entries = buildNavEntries(
        validSiteConfig.navigation,
        emptyContactChannelsSiteConfig.contactChannels
      );

      expect(entries.map((e) => e.href)).toEqual([
        '/',
        '/projects',
        '/certifications',
        '/blog',
      ]);
      expect(entries.some((e) => e.kind === 'anchor')).toBe(false);
    });
  });

  describe('Property-Based Invariants (Property 3 & 4)', () => {
    it('Feature: m4-global-layout-navigation, Property 3: route entries are sourced from config and canonically sorted for any navigation permutation', () => {
      fc.assert(
        fc.property(
          fc.array(navItemArbitrary, { minLength: 1, maxLength: 8 }),
          (navItems) => {
            const entries = buildNavEntries(navItems, []);
            expect(entries.every((e) => e.kind === 'route')).toBe(true);

            // Canonical rank ordering check
            const canonicalOrder = ['/', '/projects', '/certifications', '/blog'];
            const seenRanks = entries
              .map((e) => canonicalOrder.indexOf(e.href))
              .filter((rank) => rank !== -1);

            for (let i = 1; i < seenRanks.length; i++) {
              expect(seenRanks[i]).toBeGreaterThanOrEqual(seenRanks[i - 1]);
            }
          }
        ),
        { numRuns: 100 }
      );
    });

    it('Feature: m4-global-layout-navigation, Property 4: Contact entry is appended if and only if renderable channels exist', () => {
      fc.assert(
        fc.property(
          fc.array(navItemArbitrary, { minLength: 1, maxLength: 4 }),
          fc.array(contactChannelArbitrary, { maxLength: 5 }),
          (navItems, contactChannels) => {
            const entries = buildNavEntries(navItems, contactChannels);
            const hasRenderable = getRenderableChannels(contactChannels).length > 0;
            const lastEntry = entries[entries.length - 1];

            if (hasRenderable) {
              expect(lastEntry).toBeDefined();
              expect(lastEntry.href).toBe('#contact');
              expect(lastEntry.kind).toBe('anchor');
              expect(lastEntry.label).toBe('Contact');
            } else {
              expect(entries.every((e) => e.kind === 'route')).toBe(true);
              expect(entries.some((e) => e.href === '#contact')).toBe(false);
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\unit\components\layout\nav-entries.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/nav-entries.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.2, Req 4.3, Req 4.4, Req 4.5, Req 4.7

---

### M4.G2.T8: Author Unit & Model-Based Tests for Disclosure Reducer (`tests/unit/components/layout/disclosure.test.ts`)

**Objective:** Implement unit and model-based property tests for `disclosureReducer` in `tests/unit/components/layout/disclosure.test.ts` validating Property 5.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/disclosure.test.ts` created
- ✓ Tests `TOGGLE` inverts `collapsed` $\leftrightarrow$ `expanded`
- ✓ Tests `ESCAPE` always yields `collapsed`
- ✓ Tests `LINK_ACTIVATED` always yields `collapsed`
- ✓ Tests `ROUTE_CHANGED` always yields `collapsed`
- ✓ Implements Property 5 test ($\ge 100$ runs with `fast-check`): final state matches parity of `TOGGLE` events after last collapse
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G2.T4 completed
- Target file: `tests/unit/components/layout/disclosure.test.ts`

**Implementation Details:**

Write `tests/unit/components/layout/disclosure.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import {
  disclosureReducer,
  type DisclosureState,
  type DisclosureEvent,
} from '@/components/layout/disclosure';

describe('Disclosure Reducer (Req 6)', () => {
  describe('Unit Transitions', () => {
    it('toggles between collapsed and expanded states', () => {
      expect(disclosureReducer('collapsed', 'TOGGLE')).toBe('expanded');
      expect(disclosureReducer('expanded', 'TOGGLE')).toBe('collapsed');
    });

    it('collapses on ESCAPE from any state', () => {
      expect(disclosureReducer('expanded', 'ESCAPE')).toBe('collapsed');
      expect(disclosureReducer('collapsed', 'ESCAPE')).toBe('collapsed');
    });

    it('collapses on LINK_ACTIVATED and ROUTE_CHANGED', () => {
      expect(disclosureReducer('expanded', 'LINK_ACTIVATED')).toBe('collapsed');
      expect(disclosureReducer('expanded', 'ROUTE_CHANGED')).toBe('collapsed');
      expect(disclosureReducer('collapsed', 'LINK_ACTIVATED')).toBe('collapsed');
      expect(disclosureReducer('collapsed', 'ROUTE_CHANGED')).toBe('collapsed');
    });
  });

  describe('Property-Based Invariants (Property 5)', () => {
    it('Feature: m4-global-layout-navigation, Property 5: disclosure reducer transitions correctly for any sequence of events', () => {
      fc.assert(
        fc.property(
          fc.array(
            fc.constantFrom<DisclosureEvent>('TOGGLE', 'ESCAPE', 'LINK_ACTIVATED', 'ROUTE_CHANGED'),
            { minLength: 1, maxLength: 50 }
          ),
          (events) => {
            let state: DisclosureState = 'collapsed';
            for (const event of events) {
              state = disclosureReducer(state, event);
            }

            // Reference model check: find index of last collapsing event
            let modelState: DisclosureState = 'collapsed';
            for (const ev of events) {
              if (ev === 'TOGGLE') {
                modelState = modelState === 'collapsed' ? 'expanded' : 'collapsed';
              } else {
                modelState = 'collapsed';
              }
            }

            expect(state).toBe(modelState);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\unit\components\layout\disclosure.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/disclosure.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.4, Req 6.5, Req 6.6, Req 6.7

---

### M4.G2.T9: Author Unit & Property-Based Tests for Contact Channels (`tests/unit/components/layout/contact-channels.test.ts`)

**Objective:** Implement unit and property-based tests for `getRenderableChannels` and `orderContactChannels` in `tests/unit/components/layout/contact-channels.test.ts` validating Property 7.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/contact-channels.test.ts` created
- ✓ Tests email without `mailto:` prefix is dropped
- ✓ Tests external link without `https://` prefix is dropped
- ✓ Tests `orderContactChannels` places all primary channels ahead of non-primary channels
- ✓ Tests input array immutability during ordering
- ✓ Implements Property 7 test ($\ge 100$ runs with `fast-check`): primary channels precede non-primary, relative order preserved, no mutation
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G2.T2 completed
- Target file: `tests/unit/components/layout/contact-channels.test.ts`

**Implementation Details:**

Write `tests/unit/components/layout/contact-channels.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import {
  getRenderableChannels,
  orderContactChannels,
} from '@/components/layout/contact-channels';
import type { ContactChannel } from '@/types/content';
import { contactChannelArbitrary } from '../../../fixtures/site-config-arbitraries';

describe('Contact Channels Utilities (Req 9)', () => {
  describe('Unit Scenarios', () => {
    it('drops invalid emails and non-HTTPS external channels', () => {
      const mixed: ContactChannel[] = [
        { type: 'email', label: 'Bad Email', url: 'hello@example.com', isPrimary: false },
        { type: 'email', label: 'Good Email', url: 'mailto:hello@example.com', isPrimary: true },
        { type: 'linkedin', label: 'Bad Link', url: 'http://insecure.linkedin.com', isPrimary: false },
        { type: 'github', label: 'Good GitHub', url: 'https://github.com/example', isPrimary: false },
      ];

      const renderable = getRenderableChannels(mixed);
      expect(renderable.length).toBe(2);
      expect(renderable[0].label).toBe('Good Email');
      expect(renderable[1].label).toBe('Good GitHub');
    });

    it('orders primary channels first without mutating input array', () => {
      const channels: ContactChannel[] = [
        { type: 'github', label: 'GitHub', url: 'https://github.com/a', isPrimary: false },
        { type: 'email', label: 'Email', url: 'mailto:a@b.com', isPrimary: true },
        { type: 'linkedin', label: 'LinkedIn', url: 'https://linkedin.com/a', isPrimary: false },
      ];

      const copyBefore = [...channels];
      const ordered = orderContactChannels(channels);

      expect(ordered[0].label).toBe('Email');
      expect(ordered[1].label).toBe('GitHub');
      expect(ordered[2].label).toBe('LinkedIn');
      expect(channels).toEqual(copyBefore);
    });
  });

  describe('Property-Based Invariants (Property 7)', () => {
    it('Feature: m4-global-layout-navigation, Property 7: primary channels precede non-primary, relative order is preserved, and input is never mutated', () => {
      fc.assert(
        fc.property(
          fc.array(contactChannelArbitrary, { minLength: 1, maxLength: 10 }),
          (channels) => {
            const copyBefore = channels.map((c) => ({ ...c }));
            const ordered = orderContactChannels(channels);

            // 1. Length preserved
            expect(ordered.length).toBe(channels.length);

            // 2. Primary channels precede non-primary
            let seenNonPrimary = false;
            for (const ch of ordered) {
              if (ch.isPrimary) {
                expect(seenNonPrimary).toBe(false);
              } else {
                seenNonPrimary = true;
              }
            }

            // 3. Relative order within primary group preserved
            const inputPrimaries = channels.filter((c) => c.isPrimary);
            const orderedPrimaries = ordered.filter((c) => c.isPrimary);
            expect(orderedPrimaries.map((c) => c.label)).toEqual(inputPrimaries.map((c) => c.label));

            // 4. Relative order within non-primary group preserved
            const inputNonPrimaries = channels.filter((c) => !c.isPrimary);
            const orderedNonPrimaries = ordered.filter((c) => !c.isPrimary);
            expect(orderedNonPrimaries.map((c) => c.label)).toEqual(inputNonPrimaries.map((c) => c.label));

            // 5. Input not mutated
            expect(channels).toEqual(copyBefore);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\unit\components\layout\contact-channels.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/contact-channels.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.4, Req 9.7

---

### M4.G2.T10: Checkpoint — Pure Logic Modules and Property Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across all four pure logic modules and their corresponding unit and property test suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all pure logic test suites and passes with code 0
- ✓ Zero regressions introduced into upstream modules

**Prerequisites:**
- M4.G2.T1 through M4.G2.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/current-route.test.ts tests/unit/components/layout/nav-entries.test.ts tests/unit/components/layout/disclosure.test.ts tests/unit/components/layout/contact-channels.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/current-route.test.ts tests/unit/components/layout/nav-entries.test.ts tests/unit/components/layout/disclosure.test.ts tests/unit/components/layout/contact-channels.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.2, Req 15.6, Req 15.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\layout\current-route.ts"
Test-Path "src\components\layout\contact-channels.ts"
Test-Path "src\components\layout\nav-entries.ts"
Test-Path "src\components\layout\disclosure.ts"
Test-Path "tests\unit\components\layout\current-route.test.ts"
Test-Path "tests\unit\components\layout\nav-entries.test.ts"
Test-Path "tests\unit\components\layout\disclosure.test.ts"
Test-Path "tests\unit\components\layout\contact-channels.test.ts"
npm run typecheck
npm run test -- tests/unit/components/layout/current-route.test.ts tests/unit/components/layout/nav-entries.test.ts tests/unit/components/layout/disclosure.test.ts tests/unit/components/layout/contact-channels.test.ts
```
Expected output:
- `True` for all 8 file existence checks
- `npm run typecheck` exits with return code 0
- Vitest executes all 4 pure logic test suites with return code 0.