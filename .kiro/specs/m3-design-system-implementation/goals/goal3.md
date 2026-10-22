# M3.G3: Card Container

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component `Card` primitive in `src/components/ui/card.tsx` as the standardized surface container for portfolio project cards, certification credentials, and blog entries. The component strictly consumes M1 semantic tokens (`radius-lg`, `elevation-1`, `bg-surface`, `border-border-default`, `space-6`), supports consumer-controlled heading levels (`2 | 3 | 4`), offers a full-card link mode using a stretched pseudo-element anchor with `elevation-2` hover transitions and focus ring indicators, and enforces an invariant against nested interactive children inside the link. Author comprehensive unit, accessibility, and property-based tests in `tests/unit/components/ui/card.test.tsx`.

## Goal Success Criteria

- ✓ `src/components/ui/card.tsx` implemented as a server component without `'use client'`
- ✓ Root `<article>` element applies `relative rounded-lg border border-border-default bg-surface p-6 shadow-elevation-1`
- ✓ Heading element dynamically rendered based on `headingLevel` (`2 | 3 | 4`)
- ✓ Linked mode (`href` provided) renders exactly one anchor element covering the entire card via `after:absolute after:inset-0`
- ✓ Linked mode transitions to `shadow-elevation-2` on pointer hover using `MOTION_SHADOW_FAST`
- ✓ Linked anchor applies `FOCUS_RING` on keyboard focus (:focus-visible)
- ✓ Static mode (`href` undefined) renders clean text/heading content with no hover elevation changes
- ✓ DOM checks verify no nested interactive elements (`button`, `a`, `input`, `select`) are placed inside linked cards
- ✓ Property-based testing validates heading level fidelity across all allowed levels
- ✓ Vitest test suite passes with 100% assertions; `npm run typecheck` exits 0

## Prerequisites

- Goals M3.G1 and M3.G2 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/components/ui/cx.ts`, `focus-ring.ts`, `motion.ts`, and `heading-level.ts` exist and compile

---

## Tasks

### M3.G3.T1: Define Card Interfaces and Types (`src/components/ui/card.tsx`)

**Objective:** Author the TypeScript prop contracts for static and linked cards in `src/components/ui/card.tsx`.

**Acceptance Criteria:**
- ✓ File `src/components/ui/card.tsx` created
- ✓ Imports `HeadingLevel` and `HeadingTag` from `./heading-level`
- ✓ `StaticCardProps` defines `href?: undefined`
- ✓ `LinkedCardProps` defines `href: string` and optional `linkLabel?: string`
- ✓ Discriminated union `CardProps = StaticCardProps | LinkedCardProps` exported
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/card.tsx`

**Implementation Details:**

Write the type definitions in `src/components/ui/card.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React, { type ReactNode } from 'react';
import { cx } from './cx';
import { FOCUS_RING } from './focus-ring';
import { MOTION_SHADOW_FAST } from './motion';
import type { HeadingLevel } from './heading-level';

interface CardBaseProps {
  /** Consumer governs document heading hierarchy (Req 3.6) */
  headingLevel: HeadingLevel;
  title: ReactNode;
  className?: string;
  children?: ReactNode;
}

export interface StaticCardProps extends CardBaseProps {
  href?: undefined;
}

/**
 * Full-card link configuration.
 * When title alone is not descriptive, linkLabel serves as the accessible name.
 */
export interface LinkedCardProps extends CardBaseProps {
  href: string;
  linkLabel?: string;
}

export type CardProps = StaticCardProps | LinkedCardProps;
'@ | Set-Content "src\components\ui\card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 16.1, Req 16.8

---

### M3.G3.T2: Implement Static Card Surface

**Objective:** Implement the base functional component rendering static cards with token-based surface styling in `src/components/ui/card.tsx`.

**Acceptance Criteria:**
- ✓ Exports `function Card(props: CardProps): JSX.Element`
- ✓ Root renders semantic `<article>` element
- ✓ Applies `relative rounded-lg border border-border-default bg-surface p-6 shadow-elevation-1`
- ✓ Renders heading with dynamic tag (`h2`, `h3`, `h4`) and `text-heading-4 text-text-primary font-semibold`
- ✓ Renders children inside body container below the heading
- ✓ Zero hardcoded design values or arbitrary classes

**Prerequisites:**
- M3.G3.T1 completed
- Target file: `src/components/ui/card.tsx`

**Implementation Details:**

Append the component implementation to `src/components/ui/card.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

/**
 * Card Container Primitive
 *
 * Provides a standardized surface container for portfolio case studies,
 * credentials, and blog entries per design.md Section 4.3 and Requirement 3.
 * Server component by default (Req 3.7).
 */
export function Card(props: CardProps): JSX.Element {
  const { headingLevel, title, className, children } = props;
  const Heading = `h${headingLevel}` as const;

  const isLinked = typeof props.href === 'string' && props.href.length > 0;

  const cardClasses = cx(
    'relative rounded-lg border border-border-default bg-surface p-6 shadow-elevation-1',
    isLinked && cx('hover:shadow-elevation-2', MOTION_SHADOW_FAST),
    className
  );

  return (
    <article className={cardClasses}>
      <Heading className="text-heading-4 font-semibold text-text-primary mb-2">
        {isLinked ? (
          <a
            href={props.href}
            aria-label={props.linkLabel}
            className={cx(
              'text-text-primary hover:text-brand-primary after:absolute after:inset-0 after:content-[""] rounded-lg',
              FOCUS_RING
            )}
          >
            {title}
          </a>
        ) : (
          title
        )}
      </Heading>
      {children && <div className="text-body text-text-secondary">{children}</div>}
    </article>
  );
}
'@

Add-Content -Path "src\components\ui\card.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.3, Req 3.4, Req 3.6, Req 3.7

---

### M3.G3.T3: Author Unit Tests for Static Card Rendering

**Objective:** Create `tests/unit/components/ui/card.test.tsx` verifying static Card surface tokens, padding, and heading rendering.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/card.test.tsx` created
- ✓ Renders `<article>` container
- ✓ Validates presence of `rounded-lg`, `border-border-default`, `bg-surface`, `p-6`, and `shadow-elevation-1`
- ✓ Confirms static Card does NOT have `hover:shadow-elevation-2` class
- ✓ Confirms static Card contains no anchor tags
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G3.T2 completed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Write static Card tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Card } from '@/components/ui/card';

describe('Card Primitive', () => {
  describe('Static Card Rendering (Req 3.1, 3.2)', () => {
    it('renders an article element with canonical surface tokens', () => {
      const { container } = render(
        <Card headingLevel={2} title="Static Card Title">
          <p>Body content description.</p>
        </Card>
      );

      const article = container.querySelector('article');
      expect(article).not.toBeNull();
      expect(article?.className).toContain('rounded-lg');
      expect(article?.className).toContain('border-border-default');
      expect(article?.className).toContain('bg-surface');
      expect(article?.className).toContain('p-6');
      expect(article?.className).toContain('shadow-elevation-1');
      expect(article?.className).not.toContain('hover:shadow-elevation-2');
    });

    it('renders heading with requested heading level', () => {
      render(
        <Card headingLevel={3} title="Heading Three Project">
          <span>Project details</span>
        </Card>
      );

      const heading = screen.getByRole('heading', { level: 3, name: 'Heading Three Project' });
      expect(heading).toBeDefined();
      expect(heading.tagName).toBe('H3');
    });
  });
});
'@ | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.6, Req 14.1

---

### M3.G3.T4: Author Unit Tests for Full-Card Link Mode

**Objective:** Append tests verifying full-card link anchor generation, single anchor constraint, hover elevation transition, and focus ring application.

**Acceptance Criteria:**
- ✓ Renders exactly one anchor tag when `href` is supplied
- ✓ Anchor contains stretched pseudo-element class `after:absolute after:inset-0`
- ✓ Card container applies `hover:shadow-elevation-2` and `duration-fast`
- ✓ Anchor element applies `focus-visible:ring-focus-ring`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G3.T3 completed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Append full-card link tests to `tests/unit/components/ui/card.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Full-Card Link Mode (Req 3.3, 3.4)', () => {
    it('renders a single full-card anchor covering the card surface', () => {
      const { container } = render(
        <Card headingLevel={2} title="Linked Project" href="/projects/sample">
          <p>Clickable project summary.</p>
        </Card>
      );

      const article = container.querySelector('article');
      expect(article?.className).toContain('hover:shadow-elevation-2');
      expect(article?.className).toContain('duration-fast');

      const links = screen.getAllByRole('link');
      expect(links.length).toBe(1);

      const anchor = links[0];
      expect(anchor?.getAttribute('href')).toBe('/projects/sample');
      expect(anchor?.className).toContain('after:absolute');
      expect(anchor?.className).toContain('after:inset-0');
      expect(anchor?.className).toContain('focus-visible:ring-focus-ring');
    });

    it('uses linkLabel as accessible name when provided', () => {
      render(
        <Card
          headingLevel={3}
          title="Project Delta"
          linkLabel="View Project Delta case study"
          href="/projects/delta"
        />
      );

      const link = screen.getByRole('link', { name: 'View Project Delta case study' });
      expect(link).toBeDefined();
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.4, Req 11.4, Req 14.1

---

### M3.G3.T5: Author Guard Test for Nested Interactive Elements

**Objective:** Append a test in `tests/unit/components/ui/card.test.tsx` that inspects the DOM of a linked Card to detect and flag any illicit nested interactive elements (`button`, extra `a`, `input`, `select`).

**Acceptance Criteria:**
- ✓ Validates that a compliant linked Card contains exactly 1 focusable/interactive element
- ✓ Asserts that attempting to embed an interactive child creates an invalid DOM structure containing multiple focusables
- ✓ Test passes and serves as an automated regression guard for Requirement 3.5

**Prerequisites:**
- M3.G3.T4 completed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Append nested interactive guard test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Nested Interactive Guard (Req 3.5)', () => {
    it('ensures a compliant linked Card contains exactly one focusable element', () => {
      const { container } = render(
        <Card headingLevel={2} title="Valid Linked Card" href="/projects/1">
          <p>Text only content.</p>
        </Card>
      );

      const interactives = container.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
      expect(interactives.length).toBe(1);
    });

    it('detects violations when interactive elements are nested inside children', () => {
      const { container } = render(
        <Card headingLevel={2} title="Card With Violation" href="/projects/bad">
          <div>
            <button type="button">Nested Action</button>
          </div>
        </Card>
      );

      const interactives = container.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
      // Violation detected: more than 1 interactive element inside full-card link container
      expect(interactives.length).toBeGreaterThan(1);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.5, Req 14.1

---

### M3.G3.T6: Author Property-Based Test for Heading Level Fidelity

**Objective:** Append property-based test in `tests/unit/components/ui/card.test.tsx` using `fast-check` asserting heading level fidelity across any randomized heading level (`2 | 3 | 4`) and title string.

**Acceptance Criteria:**
- ✓ Executes at least 100 runs with `fast-check`
- ✓ Asserts Card renders exact heading tag `<h2`, `<h3`, or `<h4` matching `headingLevel`
- ✓ Asserts heading text equals input title
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/card.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Test: Heading Level Fidelity (Property 4)', () => {
    it('Feature: m3-design-system-implementation, Property 4: renders exact heading level matching prop for any level in {2, 3, 4}', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.constantFrom(2, 3, 4),
          fc.string({ minLength: 1, maxLength: 30 }).filter((s: string) => s.trim().length > 0),
          (level: 2 | 3 | 4, titleText: string) => {
            cleanup();
            const { container } = render(<Card headingLevel={level} title={titleText} />);
            const heading = container.querySelector(`h${level}`);

            expect(heading).not.toBeNull();
            expect(heading?.textContent).toBe(titleText);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 14.1

---

### M3.G3.T7: Author Accessibility Tests with `vitest-axe`

**Objective:** Append automated WCAG 2.1 AA accessibility checks for both static and linked Cards using `vitest-axe`.

**Acceptance Criteria:**
- ✓ Static Card tested with axe; reports 0 accessibility violations
- ✓ Linked Card tested with axe; reports 0 accessibility violations
- ✓ Verified against WCAG 2.1 AA rules
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Append axe tests to `tests/unit/components/ui/card.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Accessibility Verification (Req 15)', () => {
    it('produces zero WCAG violations for static Card', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <Card headingLevel={2} title="Accessible Static Card">
          <p>Body copy description.</p>
        </Card>
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });

    it('produces zero WCAG violations for linked Card', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <Card headingLevel={2} title="Accessible Linked Card" href="/projects/accessible">
          <p>Linked body copy description.</p>
        </Card>
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G3.T8: Verify Source Hygiene of `card.tsx`

**Objective:** Audit `src/components/ui/card.tsx` ensuring strict conformance to zero raw hex codes, zero arbitrary classes, zero `any`, and zero `'use client'`.

**Acceptance Criteria:**
- ✓ Contains zero matches for `#[0-9A-Fa-f]{3,8}`, `rgb(`, or `rgba(`
- ✓ Contains zero arbitrary Tailwind brackets `[` or `]` (excluding `after:content-[""]`)
- ✓ Contains zero `any` or non-null assertions `!`
- ✓ Contains zero `'use client'` statements
- ✓ Total file length is below 300 lines per `AGENTS.md` 7.2

**Prerequisites:**
- M3.G3.T2 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$content = Get-Content "src\components\ui\card.tsx" -Raw
$lines = (Get-Content "src\components\ui\card.tsx").Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and $lines -lt 300) {
    "PASS"
} else {
    Write-Host "Violations detected: Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient, Lines=$lines"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.8

---

### M3.G3.T9: Test Card Rendering Across Breakpoint Container Contexts

**Objective:** Author integration tests verifying Card renders cleanly with flexible wrapping inside constrained layouts without layout shifts.

**Acceptance Criteria:**
- ✓ Renders inside 375px mobile wrapper without horizontal overflow
- ✓ Renders inside multi-column desktop grid wrapper
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G3.T4 completed
- Target file: `tests/unit/components/ui/card.test.tsx`

**Implementation Details:**

Append responsive layout test to `tests/unit/components/ui/card.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Layout Context Integration (Req 13.4)', () => {
    it('renders inside a mobile-width constrained container cleanly', () => {
      const { container } = render(
        <div style={{ width: '375px' }}>
          <Card headingLevel={2} title="Mobile View Project" href="/projects/mobile">
            <p>Summary text that comfortably wraps within 375px bounds.</p>
          </Card>
        </div>
      );

      const article = container.querySelector('article');
      expect(article).not.toBeNull();
      expect(article?.clientWidth).toBeLessThanOrEqual(375);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.4, Req 14.1

---

### M3.G3.T10: Checkpoint — Card Primitive Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the Card implementation.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all card tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G3.T1 through M3.G3.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/card.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/card.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\ui\card.tsx"
Test-Path "tests\unit\components\ui\card.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/card.test.tsx
```
Expected output:
- `True` for both files
- `npm run typecheck` exits with code 0
- Vitest executes all Card test cases with code 0.