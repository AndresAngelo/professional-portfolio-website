# M4.G7: Global Not-Found Page

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the global not-found boundary in `src/app/not-found.tsx` (`SCR-07`) as an async server component. The not-found page renders automatically within the `RootLayout` shell, ensuring the `SiteHeader`, primary navigation, skip link, and `SiteFooter` remain visible while containing its content strictly inside the single `<main>` landmark. The page presents exactly one `<h1>` stating that the page could not be found, an explanatory message paragraph using `NOT_FOUND_*` constants, a primary action `Button` linking back to `/`, and a list of section links dynamically derived from `SiteConfig.navigation` (omitting `/`) without hardcoded URLs. Guarantee complete server-component compliance (zero `'use client'`), zero duplicate `<main>` landmarks, zero arbitrary design values, and graceful handling of empty navigation arrays. Validate error boundary composition and Property 14 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/app/not-found.tsx` implemented as an async server component without `'use client'`
- ✓ Renders inside the `RootLayout` shell, preserving `SiteHeader` and `SiteFooter`
- ✓ Emits zero `<main>` elements of its own; wraps content in `<Container as="section" className="py-16">` inside the layout's `<main>` landmark
- ✓ Displays exactly one `<h1>` with text `NOT_FOUND_HEADING = 'Page not found'`
- ✓ Displays explanatory paragraph with `NOT_FOUND_MESSAGE`
- ✓ Renders a primary action using M3 `Button` (`variant="primary"`) linking to `/` with `NOT_FOUND_HOME_LABEL`
- ✓ Dynamically renders secondary section links from `SiteConfig.navigation` filtered to `href !== '/'`
- ✓ Contains zero hardcoded navigation labels, paths, or site-owner strings
- ✓ Tests in `tests/unit/app/not-found.test.tsx` verify single `<h1>`, home button, section links, and shell integration
- ✓ Property 14 test passes $\ge 100$ runs with `fast-check`

## Prerequisites

- Goals M4.G1 through M4.G6 completed (`layout-text.ts`, `SiteConfig` loader, M3 `Container`, `Button` available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Test fixtures available at `tests/fixtures/site-config.ts`

---

## Tasks

### M4.G7.T1: Implement `NotFound` Server Component (`src/app/not-found.tsx`)

**Objective:** Author the server component `NotFound` in `src/app/not-found.tsx` rendering the standardized 404 error boundary.

**Acceptance Criteria:**
- ✓ File `src/app/not-found.tsx` created
- ✓ Exports default async function `NotFound(): Promise<JSX.Element>`
- ✓ Obtains site configuration via `await getSiteConfig()`
- ✓ Filters section links from `site.navigation` where `href !== '/'`
- ✓ Wraps content in `<Container as="section" className="py-16">`
- ✓ Renders `<h1 className="text-heading-1 font-semibold text-text-primary">` with `NOT_FOUND_HEADING`
- ✓ Renders `<p className="mt-4 text-body text-text-secondary max-w-md">` with `NOT_FOUND_MESSAGE`
- ✓ Renders primary home action `<Button variant="primary" href="/">` with `NOT_FOUND_HOME_LABEL`
- ✓ Renders section links `<ul aria-label={NOT_FOUND_SECTIONS_LABEL}>` using Next.js `Link`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G1 completed (`layout-text.ts` exists)
- M3 `Container` and `Button` available
- Target file: `src/app/not-found.tsx`

**Implementation Details:**

Write `src/app/not-found.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import Link from 'next/link';
import { getSiteConfig } from '@/content/loaders/site';
import { Container } from '@/components/ui/container';
import { Button } from '@/components/ui/button';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import {
  NOT_FOUND_HEADING,
  NOT_FOUND_MESSAGE,
  NOT_FOUND_HOME_LABEL,
  NOT_FOUND_SECTIONS_LABEL,
} from '@/components/layout/layout-text';

/**
 * Global Not-Found Boundary Component
 *
 * Renders user-friendly recovery options inside the RootLayout shell (SCR-07).
 * Server component by default (Req 11.7).
 */
export default async function NotFound(): Promise<JSX.Element> {
  const site = await getSiteConfig();
  const sectionLinks = site.navigation.filter((item) => item.href !== '/');

  return (
    <Container as="section" className="py-16 text-center md:text-left">
      <h1 className="text-heading-1 font-semibold text-text-primary mb-4">
        {NOT_FOUND_HEADING}
      </h1>
      <p className="text-body text-text-secondary max-w-md mb-8">
        {NOT_FOUND_MESSAGE}
      </p>

      {/* Primary Recovery Action */}
      <div className="mb-10 inline-block">
        <Button variant="primary" size="lg" href="/">
          {NOT_FOUND_HOME_LABEL}
        </Button>
      </div>

      {/* Dynamic Section Directory */}
      {sectionLinks.length > 0 && (
        <div>
          <h2 className="text-small font-semibold text-text-primary uppercase tracking-wider mb-4">
            {NOT_FOUND_SECTIONS_LABEL}
          </h2>
          <ul
            aria-label={NOT_FOUND_SECTIONS_LABEL}
            className="flex flex-wrap gap-4 list-none p-0 m-0 justify-center md:justify-start"
          >
            {sectionLinks.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cx(
                    'text-body text-brand-primary underline hover:opacity-80 rounded-sm',
                    FOCUS_RING,
                    MOTION_FAST
                  )}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </Container>
  );
}
'@ | Set-Content "src\app\not-found.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/app/not-found.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.6, Req 11.7, Req 13.1, Req 13.3

---

### M4.G7.T2: Author Unit Tests for `NotFound` Component (`tests/unit/app/not-found.test.tsx`)

**Objective:** Create `tests/unit/app/not-found.test.tsx` verifying single `<h1>`, explanatory text, primary home link, and section link rendering.

**Acceptance Criteria:**
- ✓ File `tests/unit/app/not-found.test.tsx` created
- ✓ Mocks `getSiteConfig` returning `validSiteConfig`
- ✓ Verifies exactly one `<h1>` exists with text `Page not found`
- ✓ Verifies primary recovery link points to `/`
- ✓ Verifies section links list contains `Projects`, `Certifications`, and `Blog` (excluding `Home`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G7.T1 completed
- Target file: `tests/unit/app/not-found.test.tsx`

**Implementation Details:**

Write `tests/unit/app/not-found.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import NotFound from '@/app/not-found';
import { validSiteConfig } from '../../fixtures/site-config';

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn().mockResolvedValue(validSiteConfig),
}));

describe('NotFound Component (Req 11)', () => {
  it('renders single h1, message, home button, and section links', async () => {
    const Component = await NotFound();
    const { container } = render(Component);

    // 1. Single h1 assertion
    const headings = screen.getAllByRole('heading', { level: 1 });
    expect(headings.length).toBe(1);
    expect(headings[0].textContent).toBe('Page not found');

    // 2. Explanatory message
    expect(screen.getByText(/The page you followed does not exist/)).toBeDefined();

    // 3. Primary action button
    const homeLink = screen.getByRole('link', { name: 'Back to home' });
    expect(homeLink).toBeDefined();
    expect(homeLink.getAttribute('href')).toBe('/');

    // 4. Section links (excluding root /)
    const expectedSections = ['Projects', 'Certifications', 'Blog'];
    expectedSections.forEach((sec) => {
      const link = screen.getByRole('link', { name: sec });
      expect(link).toBeDefined();
    });

    // 5. Zero duplicate main elements in component output
    expect(container.querySelectorAll('main').length).toBe(0);
  });
});
'@ | Set-Content "tests\unit\app\not-found.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/not-found.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.2, Req 11.3, Req 11.4, Req 11.6, Req 15.1

---

### M4.G7.T3: Author Shell Integration Test for `NotFound` Inside Root Layout

**Objective:** Append an integration test in `tests/unit/app/not-found.test.tsx` verifying that `NotFound` renders inside `RootLayout` without breaking landmark structure or introducing duplicate `<main>` elements.

**Acceptance Criteria:**
- ✓ Renders `RootLayout` wrapping `await NotFound()`
- ✓ Verifies exactly one `<header>`, one `<main>`, and one `<footer>` in DOM
- ✓ Verifies `NotFound` `<h1>` resides inside the single `<main>` element
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G7.T2 completed
- Target file: `tests/unit/app/not-found.test.tsx`

**Implementation Details:**

Append shell integration test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Shell Integration (Req 11.1, 11.6)', () => {
    it('renders inside RootLayout with exactly one main landmark containing 404 content', async () => {
      const RootLayout = (await import('@/app/layout')).default;

      const NotFoundPage = await NotFound();
      const ShellWith404 = await RootLayout({ children: NotFoundPage });

      const { container } = render(ShellWith404);

      // Verify header, main, footer exist
      expect(container.querySelectorAll('header').length).toBe(1);
      expect(container.querySelectorAll('main').length).toBe(1);
      expect(container.querySelectorAll('footer').length).toBe(1);

      // Verify 404 h1 is inside the single main container
      const main = container.querySelector('main');
      const h1 = main?.querySelector('h1');
      expect(h1).not.toBeNull();
      expect(h1?.textContent).toBe('Page not found');
    });
  });
'@

$content = Get-Content "tests\unit\app\not-found.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\not-found.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/not-found.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 11.1, Req 11.6

---

### M4.G7.T4: Author Property-Based Test for Section Links (Property 14)

**Objective:** Append property-based test in `tests/unit/app/not-found.test.tsx` using `fast-check` to assert that across arbitrary navigation arrays, section links strictly equal all navigation items whose `href !== '/'`.

**Acceptance Criteria:**
- ✓ Implements Property 14 test ($\ge 100$ runs with `fast-check`)
- ✓ Generates randomized navigation items via `navItemArbitrary`
- ✓ Asserts rendered section links match navigation items with `href !== '/'` in exact config order
- ✓ Asserts `/` is never included in section links list
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/app/not-found.test.tsx`

**Implementation Details:**

Append Property 14 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 14)', () => {
    it('Feature: m4-global-layout-navigation, Property 14: section links strictly match navigation minus root / for any navigation config', async () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { navItemArbitrary } = require('../../fixtures/site-config-arbitraries');
      const { getSiteConfig } = await import('@/content/loaders/site');

      await fc.assert(
        fc.asyncProperty(
          fc.array(navItemArbitrary, { minLength: 1, maxLength: 8 }),
          async (navItems: any) => {
            cleanup();
            vi.mocked(getSiteConfig).mockResolvedValueOnce({
              ...validSiteConfig,
              navigation: navItems,
            });

            const Component = await NotFound();
            render(Component);

            const expectedSections = navItems.filter((item: any) => item.href !== '/');
            const sectionList = screen.queryByRole('list', { name: 'Browse a section' });

            if (expectedSections.length === 0) {
              expect(sectionList).toBeNull();
            } else {
              expect(sectionList).not.toBeNull();
              expectedSections.forEach((sec: any) => {
                expect(screen.getByRole('link', { name: sec.label })).toBeDefined();
              });
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\app\not-found.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\not-found.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/not-found.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.4, Req 15.1

---

### M4.G7.T5: Author Empty-Navigation Fallback Test for `NotFound`

**Objective:** Append a unit test in `tests/unit/app/not-found.test.tsx` verifying that if `site.navigation` contains only `/` or is empty, the section links directory is cleanly omitted without rendering empty lists or throwing errors.

**Acceptance Criteria:**
- ✓ Mocks `site.navigation = [{ label: 'Home', href: '/' }]`
- ✓ Renders `NotFound`
- ✓ Asserts primary home button is present
- ✓ Asserts section links list and heading are omitted
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G7.T4 completed
- Target file: `tests/unit/app/not-found.test.tsx`

**Implementation Details:**

Append empty navigation test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Empty Navigation Fallback', () => {
    it('cleanly omits section directory when navigation has no subpages', async () => {
      const { getSiteConfig } = await import('@/content/loaders/site');
      vi.mocked(getSiteConfig).mockResolvedValueOnce({
        ...validSiteConfig,
        navigation: [{ label: 'Home', href: '/' }],
      });

      const Component = await NotFound();
      const { container } = render(Component);

      expect(screen.getByRole('link', { name: 'Back to home' })).toBeDefined();
      expect(container.querySelector('ul')).toBeNull();
      expect(screen.queryByText('Browse a section')).toBeNull();
    });
  });
'@

$content = Get-Content "tests\unit\app\not-found.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\not-found.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/not-found.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.4, Req 15.5

---

### M4.G7.T6: Audit Hardcoded Site Literals in Not-Found Page

**Objective:** Audit `src/app/not-found.tsx` to ensure zero personal name, email, or site-owner literals are hardcoded per Requirement 2.4.

**Acceptance Criteria:**
- ✓ Searches file for `'Angelo'`, `'Andres'`, `'hello@example.com'`, and `'example.vercel.app'`
- ✓ Confirms zero string matches in source code
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G7.T1 completed

**Implementation Details:**

Execute literal audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$file = "src\app\not-found.tsx"
$forbiddenLiterals = @('Angelo', 'Andres', 'hello@example.com', 'example.vercel.app')
$violations = @()

$content = Get-Content $file -Raw
foreach ($lit in $forbiddenLiterals) {
    if ($content.Contains($lit)) {
        $violations += "Hardcoded site literal '$lit' found in $file (Req 2.4 violation)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 2.4, Req 14.5

---

### M4.G7.T7: Audit Server-Component Status of Not-Found Page

**Objective:** Audit `src/app/not-found.tsx` to guarantee it does not declare `'use client'` per Requirement 11.7.

**Acceptance Criteria:**
- ✓ Confirms zero `'use client'` statements in `src/app/not-found.tsx`
- ✓ PowerShell audit script exits with PASS

**Prerequisites:**
- M4.G7.T1 completed

**Implementation Details:**

Execute server boundary check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$file = "src\app\not-found.tsx"
$content = Get-Content $file -Raw

if ($content -match "['""]use client['""]") {
    Write-Host "Forbidden 'use client' directive found in $file (must be server component)"
    "FAIL"
} else {
    "PASS"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 11.7, Req 16.2

---

### M4.G7.T8: Verify Absence of `<main>` in `not-found.tsx`

**Objective:** Audit `src/app/not-found.tsx` to confirm it renders `<Container as="section">` and does not emit a duplicate `<main>` tag, preserving the single `<main>` invariant of `layout.tsx` (Req 1.3, 11.6).

**Acceptance Criteria:**
- ✓ Confirms `<main` does not appear in `src/app/not-found.tsx`
- ✓ Confirms root container renders as `section` or `div`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G7.T1 completed

**Implementation Details:**

Execute main landmark check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$file = "src\app\not-found.tsx"
$content = Get-Content $file -Raw

if ($content -match '<main\b') {
    Write-Host "Forbidden <main> tag found in $file (only layout.tsx may render <main>)"
    "FAIL"
} else {
    "PASS"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.3, Req 11.6

---

### M4.G7.T9: Verify Source Hygiene of `not-found.tsx`

**Objective:** Audit `src/app/not-found.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `any`, and file length under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ File length under 300 lines

**Prerequisites:**
- M4.G7.T1 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$file = "src\app\not-found.tsx"
$content = Get-Content $file -Raw
$lines = (Get-Content $file).Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and ($lines -lt 300)) {
    "PASS"
} else {
    Write-Host "Violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny)"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.5, Req 13.6, Req 14.6, Req 14.7

---

### M4.G7.T10: Checkpoint — Global Not-Found Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the Not-Found implementation.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all not-found tests and passes with code 0
- ✓ Zero regressions introduced into upstream modules

**Prerequisites:**
- M4.G7.T1 through M4.G7.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/app/not-found.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/app/not-found.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\app\not-found.tsx"
Test-Path "tests\unit\app\not-found.test.tsx"
npm run typecheck
npm run test -- tests/unit/app/not-found.test.tsx
```
Expected output:
- `True` for both paths
- `npm run typecheck` exits with return code 0
- Vitest executes all not-found test suites with code 0.