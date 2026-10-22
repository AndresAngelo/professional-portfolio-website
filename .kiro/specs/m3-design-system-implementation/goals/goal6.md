# M3.G6: ExternalLink and EmptyState

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the `ExternalLink` primitive in `src/components/ui/external-link.tsx` and the `EmptyState` primitive in `src/components/ui/empty-state.tsx`. `ExternalLink` validates that destinations strictly use the secure absolute `https://` protocol via `resolveExternalHref`, rendering an anchor with `target="_blank"`, `rel="noopener noreferrer"`, visually hidden `(opens in a new tab)` text, and a decorative `aria-hidden` external icon while cleanly suppressing invalid/missing URLs per `AGENTS.md` Rule 5.1.8 and Requirement 8. `EmptyState` provides a standardized fallback container for zero-result filtering states and empty collections, rendering consumer-supplied copy, an optional action slot (Button or link), and an optional `role="status"` live-region mode per Requirement 9. Author comprehensive unit, property-based, and accessibility tests for both primitives.

## Goal Success Criteria

- ✓ `src/components/ui/external-link.tsx` implemented as a server component without `'use client'`
- ✓ `ExternalLink` renders an `<a>` with `target="_blank"`, `rel="noopener noreferrer"`, `FOCUS_RING`, and `text-brand-primary underline`
- ✓ `ExternalLink` embeds visually hidden `(opens in a new tab)` text and decorative SVG icon
- ✓ `ExternalLink` returns `null` when `href` is `null`, `undefined`, empty string, or non-HTTPS
- ✓ Development warning logged when non-HTTPS URL is supplied without leaking sensitive query strings
- ✓ `src/components/ui/empty-state.tsx` implemented with required `heading`, `message`, and `headingLevel` (`2 | 3 | 4`)
- ✓ `EmptyState` renders optional `action` slot inside an action container, omitting the container when absent
- ✓ `EmptyState` supports `announce?: boolean` adding `role="status"` for user-driven filter updates
- ✓ `tests/unit/components/ui/external-link.test.tsx` and `empty-state.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` passes with zero errors under strict mode

## Prerequisites

- Goals M3.G1 through M3.G5 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/components/ui/cx.ts`, `focus-ring.ts`, `heading-level.ts`, and `external-link-attrs.ts` exist and compile

---

## Tasks

### M3.G6.T1: Implement `ExternalLink` Primitive (`src/components/ui/external-link.tsx`)

**Objective:** Author the `ExternalLink` component in `src/components/ui/external-link.tsx` implementing safe external navigation and URL validation.

**Acceptance Criteria:**
- ✓ File `src/components/ui/external-link.tsx` created
- ✓ Exports `ExternalLinkProps` and `ExternalLink`
- ✓ Resolves `href` via `resolveExternalHref` from `./external-link-attrs`
- ✓ Returns `null` if resolved href is `null` (suppresses invalid or missing destinations)
- ✓ Renders an `<a>` tag with `EXTERNAL_LINK_ATTRS` (`target="_blank"`, `rel="noopener noreferrer"`)
- ✓ Embeds `<span className="sr-only">{NEW_TAB_TEXT}</span>`
- ✓ Embeds decorative inline SVG icon with `aria-hidden="true"` and `focusable="false"`
- ✓ Applies `text-brand-primary underline` and `FOCUS_RING`
- ✓ Logs dev-time error category when non-HTTPS URL is rejected

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/external-link.tsx`

**Implementation Details:**

Write `src/components/ui/external-link.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React, { type ReactNode } from 'react';
import { cx } from './cx';
import { FOCUS_RING } from './focus-ring';
import {
  resolveExternalHref,
  EXTERNAL_LINK_ATTRS,
  NEW_TAB_TEXT,
  type HttpsUrl,
} from './external-link-attrs';

export interface ExternalLinkProps {
  href: HttpsUrl | string | null | undefined;
  children: ReactNode;
  className?: string;
}

/**
 * ExternalLink Primitive
 *
 * Renders an accessible, secure link to an external destination.
 * Rejects non-HTTPS or absent URLs by rendering nothing per AGENTS.md Rule 5.1.8 & Requirement 8.
 */
export function ExternalLink({ href, children, className }: ExternalLinkProps): JSX.Element | null {
  const validHref = resolveExternalHref(href);

  if (!validHref) {
    if (process.env.NODE_ENV !== 'production' && typeof href === 'string' && href.trim().length > 0) {
      console.error(`[ExternalLink] Rejected invalid non-HTTPS protocol for href: "${href.slice(0, 15)}...".`);
    }
    return null;
  }

  return (
    <a
      href={validHref}
      className={cx(
        'inline-flex items-center gap-1 text-brand-primary underline hover:opacity-80 rounded-sm',
        FOCUS_RING,
        className
      )}
      {...EXTERNAL_LINK_ATTRS}
    >
      <span>{children}</span>
      <span className="sr-only">{NEW_TAB_TEXT}</span>
      <svg
        className="h-3.5 w-3.5 shrink-0 text-current inline-block"
        aria-hidden="true"
        focusable="false"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
        />
      </svg>
    </a>
  );
}
'@ | Set-Content "src\components\ui\external-link.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/external-link.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5, Req 8.6, Req 8.7, Req 16.8

---

### M3.G6.T2: Implement `EmptyState` Primitive (`src/components/ui/empty-state.tsx`)

**Objective:** Author the `EmptyState` component in `src/components/ui/empty-state.tsx` supporting consumer-provided messages, dynamic heading levels, and optional action slots.

**Acceptance Criteria:**
- ✓ File `src/components/ui/empty-state.tsx` created
- ✓ Exports `EmptyStateProps` and `EmptyState`
- ✓ Requires `heading: string`, `message: string`, and `headingLevel: HeadingLevel` (`2 | 3 | 4`)
- ✓ Supports optional `action?: ReactNode` and `announce?: boolean`
- ✓ Renders `<div className="rounded-lg border border-border-default bg-surface p-8 md:p-12 text-center">`
- ✓ Renders message using `text-body text-text-secondary`
- ✓ Renders action container `<div className="mt-6">` ONLY when `action` is provided (Req 9.4)
- ✓ Applies `role="status"` when `announce: true` (Req 9.6)
- ✓ Contains zero hardcoded copy

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/empty-state.tsx`

**Implementation Details:**

Write `src/components/ui/empty-state.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React, { type ReactNode } from 'react';
import { cx } from './cx';
import type { HeadingLevel } from './heading-level';

export interface EmptyStateProps {
  /** Consumer-supplied heading text (Req 9.5) */
  heading: string;
  /** Explanatory message text (Req 9.1) */
  message: string;
  /** Semantic heading level governing page hierarchy (Req 9.3) */
  headingLevel: HeadingLevel;
  /** Optional action slot (e.g. Button or link to clear filters) */
  action?: ReactNode;
  /** When true, attaches role="status" for live filter announcement (Req 9.6) */
  announce?: boolean;
  className?: string;
}

/**
 * EmptyState Primitive
 *
 * Displays a helpful fallback message when collections or filters yield no items.
 * design.md Section 4.3 & Requirement 9.
 */
export function EmptyState({
  heading,
  message,
  headingLevel,
  action,
  announce = false,
  className,
}: EmptyStateProps): JSX.Element {
  const Heading = `h${headingLevel}` as const;

  return (
    <div
      role={announce ? 'status' : undefined}
      className={cx(
        'rounded-lg border border-border-default bg-surface p-8 md:p-12 text-center',
        className
      )}
    >
      <Heading className="text-heading-3 font-semibold text-text-primary mb-2">
        {heading}
      </Heading>
      <p className="text-body text-text-secondary max-w-md mx-auto">
        {message}
      </p>
      {action && <div className="mt-6 inline-flex justify-center">{action}</div>}
    </div>
  );
}
'@ | Set-Content "src\components\ui\empty-state.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/empty-state.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3, Req 9.4, Req 9.5, Req 9.6, Req 9.7, Req 16.8

---

### M3.G6.T3: Author Unit Tests for `ExternalLink` (`tests/unit/components/ui/external-link.test.tsx`)

**Objective:** Create `tests/unit/components/ui/external-link.test.tsx` verifying anchor attributes, accessible text announcement, and link icon rendering.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/external-link.test.tsx` created
- ✓ Renders anchor with `target="_blank"` and `rel="noopener noreferrer"`
- ✓ Accessible name contains link text and `(opens in a new tab)`
- ✓ Decorative SVG icon is present with `aria-hidden="true"`
- ✓ Applies `text-brand-primary underline` and focus ring classes
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G6.T1 completed
- Target file: `tests/unit/components/ui/external-link.test.tsx`

**Implementation Details:**

Write `tests/unit/components/ui/external-link.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ExternalLink } from '@/components/ui/external-link';

describe('ExternalLink Primitive (Req 8)', () => {
  it('renders anchor with valid https URL, security attributes, and accessible label', () => {
    render(<ExternalLink href="https://example.com/spec">API Specification</ExternalLink>);
    const link = screen.getByRole('link', { name: /API Specification/ });

    expect(link.getAttribute('href')).toBe('https://example.com/spec');
    expect(link.getAttribute('target')).toBe('_blank');
    expect(link.getAttribute('rel')).toBe('noopener noreferrer');
    expect(link.textContent).toContain('(opens in a new tab)');

    const icon = link.querySelector('svg');
    expect(icon).not.toBeNull();
    expect(icon?.getAttribute('aria-hidden')).toBe('true');
  });

  it('applies brand-primary color token and focus ring', () => {
    render(<ExternalLink href="https://github.com">GitHub</ExternalLink>);
    const link = screen.getByRole('link', { name: /GitHub/ });

    expect(link.className).toContain('text-brand-primary');
    expect(link.className).toContain('underline');
    expect(link.className).toContain('focus-visible:ring-focus-ring');
  });
});
'@ | Set-Content "tests\unit\components\ui\external-link.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/external-link.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.7, Req 14.1

---

### M3.G6.T4: Author Rejection-Path Tests for `ExternalLink`

**Objective:** Append unit tests in `tests/unit/components/ui/external-link.test.tsx` verifying that missing, empty, or non-HTTPS `href` values render `null`.

**Acceptance Criteria:**
- ✓ Renders `null` when `href` is `null`
- ✓ Renders `null` when `href` is `undefined`
- ✓ Renders `null` when `href` is `""` (empty string)
- ✓ Renders `null` when `href` is `http://insecure.com`
- ✓ Renders `null` when `href` is `javascript:alert(1)`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G6.T3 completed
- Target file: `tests/unit/components/ui/external-link.test.tsx`

**Implementation Details:**

Append rejection tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Rejection Paths (Req 8.5, 8.6)', () => {
    it.each([
      [null, 'null'],
      [undefined, 'undefined'],
      ['', 'empty string'],
      ['   ', 'whitespace only'],
      ['http://example.com', 'insecure http'],
      ['ftp://files.example.com', 'ftp protocol'],
      ['javascript:void(0)', 'javascript protocol'],
      ['/internal/route', 'internal relative path'],
    ])('renders null and suppresses DOM output when href is %s (%s)', (invalidHref) => {
      const { container } = render(
        <ExternalLink href={invalidHref}>Test Link</ExternalLink>
      );
      expect(container.firstChild).toBeNull();
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\external-link.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\external-link.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/external-link.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.4, Req 8.5, Req 8.6, Req 14.6

---

### M3.G6.T5: Author Unit Tests for `EmptyState` (`tests/unit/components/ui/empty-state.test.tsx`)

**Objective:** Create `tests/unit/components/ui/empty-state.test.tsx` testing heading levels, copy presentation, optional action slot rendering, and live-region announcement.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/empty-state.test.tsx` created
- ✓ Renders required heading and message
- ✓ Renders dynamic heading level (`<h2>`, `<h3>`, `<h4>`)
- ✓ Omits action wrapper `<div>` when `action` prop is omitted (Req 9.4)
- ✓ Renders action wrapper and action component when `action` prop is provided
- ✓ Does not set `role="status"` when `announce: false` or omitted
- ✓ Sets `role="status"` when `announce: true` (Req 9.6)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G6.T2 completed
- Target file: `tests/unit/components/ui/empty-state.test.tsx`

**Implementation Details:**

Write `tests/unit/components/ui/empty-state.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { EmptyState } from '@/components/ui/empty-state';

describe('EmptyState Primitive (Req 9)', () => {
  it('renders required heading and descriptive message', () => {
    render(
      <EmptyState
        heading="No matching projects"
        message="Try adjusting your technology or status filters."
        headingLevel={2}
      />
    );

    const heading = screen.getByRole('heading', { level: 2, name: 'No matching projects' });
    expect(heading).toBeDefined();
    expect(screen.getByText('Try adjusting your technology or status filters.')).toBeDefined();
  });

  describe('Action Slot Omission (Req 9.2, 9.4)', () => {
    it('omits action container when action prop is not provided', () => {
      const { container } = render(
        <EmptyState
          heading="No results"
          message="Zero records found."
          headingLevel={3}
        />
      );

      const actionWrapper = container.querySelector('.mt-6');
      expect(actionWrapper).toBeNull();
    });

    it('renders action container when action prop is provided', () => {
      const { container } = render(
        <EmptyState
          heading="No results"
          message="Zero records found."
          headingLevel={3}
          action={<button type="button">Clear filters</button>}
        />
      );

      const actionWrapper = container.querySelector('.mt-6');
      expect(actionWrapper).not.toBeNull();
      expect(screen.getByRole('button', { name: 'Clear filters' })).toBeDefined();
    });
  });

  describe('Live-Region Announcement (Req 9.6)', () => {
    it('does not set role="status" by default', () => {
      const { container } = render(
        <EmptyState heading="Default" message="Quiet state" headingLevel={2} />
      );
      expect(container.firstChild).not.toHaveProperty('role', 'status');
      expect((container.firstChild as HTMLElement)?.getAttribute('role')).toBeNull();
    });

    it('attaches role="status" when announce=true', () => {
      const { container } = render(
        <EmptyState heading="Filtered" message="Dynamic state" headingLevel={2} announce={true} />
      );
      expect((container.firstChild as HTMLElement)?.getAttribute('role')).toBe('status');
    });
  });
});
'@ | Set-Content "tests\unit\components\ui\empty-state.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/empty-state.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3, Req 9.4, Req 9.6, Req 9.7, Req 14.1

---

### M3.G6.T6: Author Property-Based Test for `ExternalLink` Invariants (Property 8 & 9)

**Objective:** Append property-based test in `tests/unit/components/ui/external-link.test.tsx` using `fast-check` to assert that valid HTTPS URLs always render safe links, and non-HTTPS values render nothing.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Generates valid HTTPS web URLs and verifies `target="_blank"`, `rel="noopener noreferrer"`, and new tab text
- ✓ Generates non-HTTPS strings and verifies output is strictly `null`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/external-link.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/external-link.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: ExternalLink URL Invariants (Property 8 & 9)', () => {
    it('Feature: m3-design-system-implementation, Property 8: renders secure anchor with noopener noreferrer for any valid HTTPS URL', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.webUrl({ validSchemes: ['https'] }),
          fc.string({ minLength: 1, maxLength: 20 }).filter((s: string) => s.trim().length > 0),
          (httpsUrl: string, linkText: string) => {
            cleanup();
            render(<ExternalLink href={httpsUrl}>{linkText}</ExternalLink>);
            const link = screen.getByRole('link', { name: new RegExp(linkText) });

            expect(link.getAttribute('href')).toBe(httpsUrl);
            expect(link.getAttribute('target')).toBe('_blank');
            expect(link.getAttribute('rel')).toBe('noopener noreferrer');
            expect(link.textContent).toContain('(opens in a new tab)');
          }
        ),
        { numRuns: 100 }
      );
    });

    it('Feature: m3-design-system-implementation, Property 9: suppresses render and outputs null for any non-HTTPS URL', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.string().filter((s: string) => !s.startsWith('https://')),
          (nonHttpsUrl: string) => {
            cleanup();
            const { container } = render(<ExternalLink href={nonHttpsUrl}>Link</ExternalLink>);
            expect(container.firstChild).toBeNull();
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\external-link.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\external-link.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/external-link.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.4, Req 8.5, Req 14.1, Req 14.6

---

### M3.G6.T7: Author Property-Based Test for `EmptyState` Invariants (Property 10)

**Objective:** Append property-based test in `tests/unit/components/ui/empty-state.test.tsx` verifying Property 10: action container is rendered if and only if action is supplied, and `role="status"` is set if and only if `announce` is true.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Generates boolean for `announce` and boolean for `hasAction`
- ✓ Verifies action container `.mt-6` existence strictly matches `hasAction`
- ✓ Verifies `role="status"` strictly matches `announce`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/empty-state.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/empty-state.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: EmptyState Invariants (Property 10)', () => {
    it('Feature: m3-design-system-implementation, Property 10: action container presence strictly matches action prop, and role="status" strictly matches announce prop', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.boolean(),
          fc.boolean(),
          fc.constantFrom(2, 3, 4),
          (announce: boolean, hasAction: boolean, level: 2 | 3 | 4) => {
            cleanup();
            const actionNode = hasAction ? <button type="button">Action</button> : undefined;

            const { container } = render(
              <EmptyState
                heading="Heading"
                message="Message"
                headingLevel={level}
                action={actionNode}
                announce={announce}
              />
            );

            const actionContainer = container.querySelector('.mt-6');
            if (hasAction) {
              expect(actionContainer).not.toBeNull();
            } else {
              expect(actionContainer).toBeNull();
            }

            const rootElement = container.firstChild as HTMLElement;
            if (announce) {
              expect(rootElement.getAttribute('role')).toBe('status');
            } else {
              expect(rootElement.getAttribute('role')).toBeNull();
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\empty-state.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\empty-state.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/empty-state.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.2, Req 9.4, Req 9.6, Req 14.1

---

### M3.G6.T8: Author Automated Axe Accessibility Tests

**Objective:** Append automated accessibility checks for `ExternalLink` and `EmptyState` using `vitest-axe`.

**Acceptance Criteria:**
- ✓ `ExternalLink` passes axe with 0 violations
- ✓ `EmptyState` with action passes axe with 0 violations
- ✓ `EmptyState` without action passes axe with 0 violations
- ✓ `EmptyState` in live-region mode (`announce=true`) passes axe with 0 violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target files: `external-link.test.tsx` and `empty-state.test.tsx`

**Implementation Details:**

Append axe checks using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

# 1. Append to external-link.test.tsx
$appendExtAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it('produces zero accessibility violations for ExternalLink', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <ExternalLink href="https://example.com/accessible">Accessible Link</ExternalLink>
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@
$extContent = Get-Content "tests\unit\components\ui\external-link.test.tsx" -Raw
$extContent = $extContent -replace "\s*\}\);\s*$", "$appendExtAxe`n});`n"
$extContent | Set-Content "tests\unit\components\ui\external-link.test.tsx" -Encoding UTF8

# 2. Append to empty-state.test.tsx
$appendEmptyAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it('produces zero accessibility violations for EmptyState configurations', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <EmptyState
          heading="Accessible Zero State"
          message="Clear filters to view all projects."
          headingLevel={2}
          action={<button type="button">Reset</button>}
          announce={true}
        />
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@
$emptyContent = Get-Content "tests\unit\components\ui\empty-state.test.tsx" -Raw
$emptyContent = $emptyContent -replace "\s*\}\);\s*$", "$appendEmptyAxe`n});`n"
$emptyContent | Set-Content "tests\unit\components\ui\empty-state.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/external-link.test.tsx tests/unit/components/ui/empty-state.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G6.T9: Verify Source Hygiene of `external-link.tsx` and `empty-state.tsx`

**Objective:** Audit both component files for zero raw hex colors, zero arbitrary Tailwind classes, zero `any`, and zero `'use client'`.

**Acceptance Criteria:**
- ✓ Both files contain zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Both files contain zero `rgb(`/`rgba(`
- ✓ Both files contain zero arbitrary Tailwind brackets `[` or `]`
- ✓ Both files contain zero `any` or `!`
- ✓ Both files contain zero `'use client'` statements
- ✓ Both files are under 300 lines

**Prerequisites:**
- M3.G6.T1 and M3.G6.T2 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\ui\external-link.tsx", "src\components\ui\empty-state.tsx")
$allPass = $true

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    $lines = (Get-Content $file).Count

    $hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
    $hasRgb = $content -match 'rgba?\('
    $hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
    $hasAny = $content -match ':\s*any\b|\bas\s+any\b'
    $hasClient = $content -match "['""]use client['""]"

    if ($hasHex -or $hasRgb -or $hasArbitrary -or $hasAny -or $hasClient -or ($lines -ge 300)) {
        $allPass = $false
        Write-Host "Violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.8

---

### M3.G6.T10: Checkpoint — ExternalLink and EmptyState Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across ExternalLink and EmptyState.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all external link and empty state tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G6.T1 through M3.G6.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/external-link.test.tsx tests/unit/components/ui/empty-state.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/external-link.test.tsx tests/unit/components/ui/empty-state.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\external-link.tsx"
Test-Path "src\components\ui\empty-state.tsx"
Test-Path "tests\unit\components\ui\external-link.test.tsx"
Test-Path "tests\unit\components\ui\empty-state.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/external-link.test.tsx tests/unit/components/ui/empty-state.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Tests pass with exit code 0.