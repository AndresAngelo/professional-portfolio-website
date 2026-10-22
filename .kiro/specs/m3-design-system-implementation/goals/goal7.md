# M3.G7: Container and Responsive Verification

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the polymorphic server-component `Container` primitive in `src/components/ui/container.tsx` to standardize responsive layout boundaries across Mobile (375px–767px), Tablet (768px–1023px), Desktop (1024px–1439px), and Wide Desktop (1440px+). Enforce horizontal centering (`mx-auto`), responsive horizontal padding (`px-4 md:px-6 lg:px-8`), maximum readable width capping (`max-w-screen-xl`), and landmark polymorphism (`div`, `section`, `main`, `article`) without assertions. Document the responsive verification procedure across all target viewport widths in `task-notes.md` without modifying root configuration files.

## Goal Success Criteria

- ✓ `src/components/ui/container.tsx` implemented as a server component without `'use client'`
- ✓ Polymorphic `as` prop restricted to `ContainerElement = 'div' | 'section' | 'main' | 'article'` (defaults to `'div'`)
- ✓ Centers content with `mx-auto w-full max-w-screen-xl`
- ✓ Stepped horizontal padding: `px-4` on mobile (16px), `md:px-6` on tablet (24px), `lg:px-8` on desktop (32px)
- ✓ Prevents horizontal page scrolling at 375px mobile viewport width
- ✓ Capped at `max-w-screen-xl` (1280px) on wide desktop viewports (1440px+)
- ✓ Manual responsive check protocol documented in `task-notes.md`
- ✓ `git diff` confirms zero edits to `tailwind.config.ts` or `globals.css`
- ✓ `tests/unit/components/ui/container.test.tsx` passes with 100% assertions
- ✓ `npm run typecheck` passes with zero errors under strict mode

## Prerequisites

- Goals M3.G1 through M3.G6 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/components/ui/cx.ts` exists and compiles

---

## Tasks

### M3.G7.T1: Define Container Types and Component (`src/components/ui/container.tsx`)

**Objective:** Author the polymorphic `Container` component in `src/components/ui/container.tsx` constraining layout boundaries with semantic spacing tokens.

**Acceptance Criteria:**
- ✓ File `src/components/ui/container.tsx` created
- ✓ Exports `ContainerElement = 'div' | 'section' | 'main' | 'article'`
- ✓ Exports `ContainerProps` requiring `children: ReactNode` and optional `as?: ContainerElement`
- ✓ Defaults `as` to `'div'` cleanly without type assertions
- ✓ Applies `mx-auto w-full max-w-screen-xl px-4 md:px-6 lg:px-8`
- ✓ Zero hardcoded design values or arbitrary Tailwind brackets `[`
- ✓ Server component without `'use client'`

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/container.tsx`

**Implementation Details:**

Write `src/components/ui/container.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React, { type ReactNode } from 'react';
import { cx } from './cx';

export type ContainerElement = 'div' | 'section' | 'main' | 'article';

export interface ContainerProps {
  /** Polymorphic landmark tag (Req 13.5). Defaults to 'div'. */
  as?: ContainerElement;
  className?: string;
  children: ReactNode;
}

/**
 * Responsive Container Primitive
 *
 * Constrains layout width and applies responsive horizontal padding across
 * Mobile (375px), Tablet (768px), Desktop (1024px), and Wide Desktop (1440px).
 * design.md Section 5.1 & Requirement 13.
 */
export function Container({
  as: Component = 'div',
  className,
  children,
}: ContainerProps): JSX.Element {
  return (
    <Component
      className={cx(
        'mx-auto w-full max-w-screen-xl px-4 md:px-6 lg:px-8',
        className
      )}
    >
      {children}
    </Component>
  );
}
'@ | Set-Content "src\components\ui\container.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/container.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.5, Req 13.7, Req 16.8

---

### M3.G7.T2: Author Unit Tests for Container Defaults & Tokens (`tests/unit/components/ui/container.test.tsx`)

**Objective:** Create `tests/unit/components/ui/container.test.tsx` verifying default `<div>` rendering and canonical layout class tokens.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/container.test.tsx` created
- ✓ Verifies default element rendered is `<div>`
- ✓ Verifies presence of centering token `mx-auto`
- ✓ Verifies presence of full-width utility `w-full`
- ✓ Verifies presence of max-width cap `max-w-screen-xl`
- ✓ Verifies presence of responsive padding steps `px-4`, `md:px-6`, `lg:px-8`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G7.T1 completed
- Target file: `tests/unit/components/ui/container.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Container } from '@/components/ui/container';

describe('Container Primitive (Req 13)', () => {
  it('renders default div with canonical layout and responsive padding tokens', () => {
    const { container } = render(
      <Container>
        <p>Container inner content</p>
      </Container>
    );

    const el = container.firstElementChild as HTMLElement;
    expect(el).not.toBeNull();
    expect(el.tagName).toBe('DIV');
    expect(el.className).toContain('mx-auto');
    expect(el.className).toContain('w-full');
    expect(el.className).toContain('max-w-screen-xl');
    expect(el.className).toContain('px-4');
    expect(el.className).toContain('md:px-6');
    expect(el.className).toContain('lg:px-8');
    expect(screen.getByText('Container inner content')).toBeDefined();
  });
});
'@ | Set-Content "tests\unit\components\ui\container.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/container.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.3, Req 14.1

---

### M3.G7.T3: Author Unit Tests for Landmark Polymorphism

**Objective:** Append tests verifying that `as` correctly renders semantic landmarks (`section`, `main`, `article`) in `tests/unit/components/ui/container.test.tsx`.

**Acceptance Criteria:**
- ✓ `as="section"` renders `<section>` element
- ✓ `as="main"` renders `<main>` element
- ✓ `as="article"` renders `<article>` element
- ✓ Preserves layout classes regardless of rendered element tag
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G7.T2 completed
- Target file: `tests/unit/components/ui/container.test.tsx`

**Implementation Details:**

Append polymorphism tests to `tests/unit/components/ui/container.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Polymorphic Landmark Elements (Req 13.5)', () => {
    it.each([
      ['div', 'DIV'],
      ['section', 'SECTION'],
      ['main', 'MAIN'],
      ['article', 'ARTICLE'],
    ])('renders as="%s" yielding <%s> element with layout tokens', (asTag, expectedTagName) => {
      const { container } = render(
        <Container as={asTag as any}>
          <span>Content</span>
        </Container>
      );

      const el = container.firstElementChild as HTMLElement;
      expect(el.tagName).toBe(expectedTagName);
      expect(el.className).toContain('mx-auto');
      expect(el.className).toContain('max-w-screen-xl');
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\container.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\container.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/container.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.5, Req 14.1

---

### M3.G7.T4: Author Property-Based Test for Container Elements (Property 13)

**Objective:** Append property-based test in `tests/unit/components/ui/container.test.tsx` using `fast-check` to assert that for any element in `{div, section, main, article}`, Container renders exact tag with layout and max-width tokens.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Generates randomized element from `['div', 'section', 'main', 'article']`
- ✓ Asserts root tag equals upper-cased element string
- ✓ Asserts `mx-auto`, `max-w-screen-xl`, and `px-4` are always present
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/container.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/container.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: Element Invariants (Property 13)', () => {
    it('Feature: m3-design-system-implementation, Property 13: renders exact tag name and layout tokens for any element in {div, section, main, article}', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.constantFrom('div', 'section', 'main', 'article'),
          (tag: 'div' | 'section' | 'main' | 'article') => {
            cleanup();
            const { container } = render(<Container as={tag}>Text</Container>);
            const el = container.firstElementChild as HTMLElement;

            expect(el.tagName.toLowerCase()).toBe(tag);
            expect(el.className).toContain('mx-auto');
            expect(el.className).toContain('max-w-screen-xl');
            expect(el.className).toContain('px-4');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\container.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\container.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/container.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.3, Req 13.5, Req 14.1

---

### M3.G7.T5: Author Automated Axe Accessibility Tests for Container

**Objective:** Append automated accessibility checks for `Container` across all supported element landmarks using `vitest-axe`.

**Acceptance Criteria:**
- ✓ `div` container passes axe with 0 violations
- ✓ `section` container with accessible name passes axe with 0 violations
- ✓ `main` container passes axe with 0 violations
- ✓ `article` container passes axe with 0 violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target file: `tests/unit/components/ui/container.test.tsx`

**Implementation Details:**

Append axe checks to `tests/unit/components/ui/container.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Accessibility Verification (Req 15)', () => {
    it.each(['div', 'main', 'article'])('produces zero accessibility violations for as="%s"', async (asTag) => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <Container as={asTag as any}>
          <h1>Accessible Landmark</h1>
          <p>Landmark content.</p>
        </Container>
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });

    it('produces zero violations for section with accessible name', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <Container as="section" aria-label="Featured Section">
          <h2>Section Title</h2>
          <p>Section body.</p>
        </Container>
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\container.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\container.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/container.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G7.T6: Document Manual Responsive Check Protocol in `task-notes.md`

**Objective:** Append the formal step-by-step manual responsive verification protocol across the 4 canonical breakpoints (375px, 768px, 1024px, 1440px) into `task-notes.md` per Requirement 13.4 and 15.5.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m3-design-system-implementation/task-notes.md` updated
- ✓ Documents 375px mobile check: verifies fluid width and absence of horizontal document scrollbar
- ✓ Documents 768px tablet check: verifies `md:px-6` (24px) padding application
- ✓ Documents 1024px desktop check: verifies `lg:px-8` (32px) padding application
- ✓ Documents 1440px wide desktop check: verifies horizontal centering (`mx-auto`) and capping at `1280px` (`max-w-screen-xl`)

**Prerequisites:**
- `task-notes.md` exists (created in M3.G1.T7)

**Implementation Details:**

Append the protocol to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$protocolNotes = @'

## 3. Responsive Verification Protocol (Req 13.2, 13.4, 15.5)

The responsive behavior of `Container` and layout primitives must be manually verified across the 4 canonical breakpoints in Chromium and WebKit DevTools:

1. **Mobile Viewport (375px width):**
   - Emulate iPhone SE / 375px width in DevTools.
   - Confirm horizontal padding is exactly 16px (`px-4`).
   - Confirm `document.documentElement.scrollWidth <= document.documentElement.clientWidth`. No horizontal scrollbar appears.
2. **Tablet Viewport (768px width):**
   - Set viewport to 768px.
   - Confirm horizontal padding steps up to 24px (`md:px-6`).
   - Confirm layout remains fluid.
3. **Desktop Viewport (1024px width):**
   - Set viewport to 1024px.
   - Confirm horizontal padding steps up to 32px (`lg:px-8`).
   - Confirm content columns align neatly to the SGDS grid.
4. **Wide Desktop Viewport (1440px+ width):**
   - Set viewport to 1440px and 1920px.
   - Confirm container width is capped at 1280px (`max-w-screen-xl`).
   - Confirm outer margins are symmetrical (`mx-auto` centering).
'@

Add-Content -Path ".kiro\specs\m3-design-system-implementation\task-notes.md" -Value $protocolNotes -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$notes = Get-Content ".kiro\specs\m3-design-system-implementation\task-notes.md" -Raw
if ($notes -match "Responsive Verification Protocol") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.2, Req 13.4, Req 15.5

---

### M3.G7.T7: Verify Zero Modification to Root Tailwind Configuration

**Objective:** Run `git diff` against `tailwind.config.ts` and `globals.css` to confirm no custom screen overrides were introduced, adhering to `AGENTS.md` Section 6.2.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts` produces zero output
- ✓ `git diff src/app/globals.css` produces zero output
- ✓ Script asserts zero unapproved configuration drift

**Prerequisites:**
- Project root exists

**Implementation Details:**

Execute diff verification using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$diff = git diff tailwind.config.ts src/app/globals.css
if ($diff.Length -eq 0) {
    "PASS"
} else {
    Write-Host "Unexpected changes in root configs:`n$diff"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.3, Req 13.6

---

### M3.G7.T8: Verify Source Hygiene of `container.tsx`

**Objective:** Audit `src/components/ui/container.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind classes, zero `any`, and zero `'use client'`.

**Acceptance Criteria:**
- ✓ Zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or non-null assertions `!`
- ✓ Zero `'use client'` statements
- ✓ Total file length is below 300 lines

**Prerequisites:**
- M3.G7.T1 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$content = Get-Content "src\components\ui\container.tsx" -Raw
$lines = (Get-Content "src\components\ui\container.tsx").Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and $lines -lt 300) {
    "PASS"
} else {
    Write-Host "Violation in container.tsx: Hex=$hasHex, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient, Lines=$lines"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.8

---

### M3.G7.T9: Author Custom Class Extension Test for Container

**Objective:** Append a test in `tests/unit/components/ui/container.test.tsx` verifying that custom consumer classes merge cleanly without removing base layout tokens.

**Acceptance Criteria:**
- ✓ Container accepts `className="py-12 bg-surface"`
- ✓ Resulting element contains both base layout classes and custom classes
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G7.T1 completed
- Target file: `tests/unit/components/ui/container.test.tsx`

**Implementation Details:**

Append class merge test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Custom Class Extension', () => {
    it('merges consumer className cleanly with default layout tokens', () => {
      const { container } = render(
        <Container className="py-12 bg-surface">
          <span>Custom Spacing</span>
        </Container>
      );

      const el = container.firstElementChild as HTMLElement;
      expect(el.className).toContain('mx-auto');
      expect(el.className).toContain('max-w-screen-xl');
      expect(el.className).toContain('py-12');
      expect(el.className).toContain('bg-surface');
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\container.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\container.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/container.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 14.1

---

### M3.G7.T10: Checkpoint — Container Primitive Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the Container implementation.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all container tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G7.T1 through M3.G7.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/container.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/container.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\container.tsx"
Test-Path "tests\unit\components\ui\container.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/container.test.tsx
```
Expected output:
- `True` for both files
- `npm run typecheck` exits with return code 0
- Tests pass with exit code 0.