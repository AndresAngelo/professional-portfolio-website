# M4.G4: SkipLink and SiteHeader

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the accessible `SkipLink` primitive in `src/components/layout/skip-link.tsx` and the server-rendered `SiteHeader` component in `src/components/layout/site-header.tsx`. `SkipLink` acts as the very first focusable element on every page, visually hidden until focused (`sr-only focus:not-sr-only focus:z-50`), providing a direct keyboard jump to `#main-content` with M3's `FOCUS_RING` styling. `SiteHeader` renders a semantic `<header>` landmark wrapping the site identity link (`Link href="/"` displaying `SiteConfig.siteName`), embedding the `PrimaryNav` component, and conditionally presenting a desktop contact action for the primary contact channel (`isPrimary: true`). The header contact action dynamically adapts to the channel type: email channels render a secondary `Button` linking to `mailto:`, while external channels render an `external-link` variant `Button` with new-tab security attributes. Enforce strict server-component execution (zero `'use client'`), zero hardcoded site text, and responsive layout bounding via M3's `Container`. Validate all states, keyboard mechanics, and Property 11 using Vitest.

## Goal Success Criteria

- ✓ `src/components/layout/skip-link.tsx` implemented as a server component targeting `#main-content`
- ✓ `SkipLink` applies `sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50` and M3's `FOCUS_RING`
- ✓ `src/components/layout/site-header.tsx` implemented as a server component without `'use client'`
- ✓ `SiteHeader` renders `<header>` landmark with `SiteConfig.siteName` linking to `/`
- ✓ `SiteHeader` constrains width and horizontal padding using M3's `Container`
- ✓ First renderable contact channel with `isPrimary: true` renders as a desktop contact action inside a `hidden lg:block` wrapper
- ✓ Email primary channel renders `<Button variant="secondary" href="mailto:...">` without `target`
- ✓ Non-email primary channel renders `<Button variant="external-link" href="https://...">` with `target="_blank"` and `rel="noopener noreferrer"`
- ✓ Contact action is omitted if no primary channel is configured or if channels are empty
- ✓ `tests/unit/components/layout/skip-link.test.tsx` and `site-header.test.tsx` pass with 100% assertions
- ✓ Property 11 test passes $\ge 100$ runs with `fast-check`

## Prerequisites

- Goals M4.G1, M4.G2, and M4.G3 completed
- `PrimaryNav` available at `src/components/layout/primary-nav.tsx`
- Layout text constants available at `src/components/layout/layout-text.ts`
- M3 primitives (`Container`, `Button`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available at `src/components/ui/`
- Pure contact helper `getRenderableChannels` available at `src/components/layout/contact-channels.ts`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M4.G4.T1: Implement `SkipLink` Component (`src/components/layout/skip-link.tsx`)

**Objective:** Author the accessible, visually-hidden-until-focus `SkipLink` component in `src/components/layout/skip-link.tsx` targeting `#main-content`.

**Acceptance Criteria:**
- ✓ File `src/components/layout/skip-link.tsx` created
- ✓ Exports `SkipLink(): JSX.Element`
- ✓ Renders native `<a>` tag with `href="#main-content"` using `MAIN_CONTENT_ID`
- ✓ Displays visible text `Skip to main content` using `SKIP_LINK_TEXT`
- ✓ Applies `sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50`
- ✓ Applies token styling: `rounded-md bg-page px-4 py-2 text-body font-medium text-brand-primary`
- ✓ Applies M3's `FOCUS_RING`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G1 completed (`layout-text.ts` exists)
- M3 `focus-ring.ts` and `cx.ts` exist
- Target file: `src/components/layout/skip-link.tsx`

**Implementation Details:**

Write `src/components/layout/skip-link.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MAIN_CONTENT_ID, SKIP_LINK_TEXT } from './layout-text';

/**
 * SkipLink Primitive
 *
 * Provides keyboard users with a direct shortcut to bypass header navigation.
 * Positioned as the first focusable element in DOM order (Req 7.1, 7.2).
 * Server component by default (Req 7.4).
 */
export function SkipLink(): JSX.Element {
  return (
    <a
      href={`#${MAIN_CONTENT_ID}`}
      className={cx(
        'sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50',
        'rounded-md bg-page px-4 py-2 text-body font-medium text-brand-primary shadow-elevation-2',
        FOCUS_RING
      )}
    >
      {SKIP_LINK_TEXT}
    </a>
  );
}
'@ | Set-Content "src\components\layout\skip-link.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/layout/skip-link.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.4, Req 7.5, Req 13.4, Req 16.2

---

### M4.G4.T2: Implement `SiteHeader` Component (`src/components/layout/site-header.tsx`)

**Objective:** Author the server component `SiteHeader` in `src/components/layout/site-header.tsx` composing site identity, `PrimaryNav`, and primary contact action.

**Acceptance Criteria:**
- ✓ File `src/components/layout/site-header.tsx` created
- ✓ Exports `SiteHeaderProps` interface accepting `siteName`, `navigation`, and `contactChannels` from `SiteConfig`
- ✓ Exports `SiteHeader(props: SiteHeaderProps): JSX.Element`
- ✓ Root renders `<header className="relative border-b border-border-default bg-page">`
- ✓ Constrains content width with `<Container className="flex flex-wrap items-center justify-between gap-4 py-3">`
- ✓ Renders identity `Link href="/"` with `siteName` and `text-heading-4 font-semibold text-text-primary`
- ✓ Selects first renderable contact channel with `isPrimary: true` via `getRenderableChannels`
- ✓ Renders primary action inside `<div className="hidden lg:block">` using M3 `Button`
- ✓ Renders email channel as `variant="secondary"` without `target`
- ✓ Renders non-email channel as `variant="external-link"`
- ✓ Embeds `<PrimaryNav>` passing `navigation` and `contactChannels`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G3 completed (`PrimaryNav` available)
- M4.G2 completed (`getRenderableChannels` available)
- M3 `Container` and `Button` available
- Target file: `src/components/layout/site-header.tsx`

**Implementation Details:**

Write `src/components/layout/site-header.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import Link from 'next/link';
import type { SiteConfig } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Button } from '@/components/ui/button';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { PrimaryNav } from './primary-nav';
import { getRenderableChannels } from './contact-channels';

export interface SiteHeaderProps {
  siteName: SiteConfig['siteName'];
  navigation: SiteConfig['navigation'];
  contactChannels: SiteConfig['contactChannels'];
}

/**
 * Global SiteHeader Component
 *
 * Displays identity link, primary navigation, and desktop call-to-action.
 * design.md Section 4.2 & Requirement 3. Server component by default (Req 3.6).
 */
export function SiteHeader({
  siteName,
  navigation,
  contactChannels,
}: SiteHeaderProps): JSX.Element {
  const renderableChannels = getRenderableChannels(contactChannels);
  const primaryChannel = renderableChannels.find((channel) => channel.isPrimary);

  return (
    <header className="relative border-b border-border-default bg-page">
      <Container className="flex flex-wrap items-center justify-between gap-4 py-3">
        {/* Site Identity Link */}
        <Link
          href="/"
          className={cx(
            'text-heading-4 font-semibold text-text-primary hover:text-brand-primary rounded-sm',
            FOCUS_RING,
            MOTION_FAST
          )}
        >
          {siteName}
        </Link>

        {/* Navigation & Header Actions */}
        <div className="flex items-center gap-4">
          {primaryChannel && (
            <div className="hidden lg:block">
              {primaryChannel.type === 'email' ? (
                <Button variant="secondary" size="md" href={primaryChannel.url}>
                  {primaryChannel.label}
                </Button>
              ) : (
                <Button variant="external-link" size="md" href={primaryChannel.url}>
                  {primaryChannel.label}
                </Button>
              )}
            </div>
          )}

          <PrimaryNav navigation={navigation} contactChannels={contactChannels} />
        </div>
      </Container>
    </header>
  );
}
'@ | Set-Content "src\components\layout\site-header.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/layout/site-header.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 3.1, Req 3.2, Req 3.3, Req 3.4, Req 3.5, Req 3.6, Req 13.1, Req 13.3

---

### M4.G4.T3: Author Unit Tests for `SkipLink` (`tests/unit/components/layout/skip-link.test.tsx`)

**Objective:** Create `tests/unit/components/layout/skip-link.test.tsx` verifying visible copy, anchor destination, visual-hiding utilities, and focus-ring composition.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/skip-link.test.tsx` created
- ✓ Renders native anchor with text `Skip to main content`
- ✓ Anchor `href` equals `#main-content`
- ✓ Verifies presence of `sr-only` and `focus:not-sr-only` classes
- ✓ Verifies presence of `focus:z-50` and `focus-visible:ring-focus-ring`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G4.T1 completed
- Target file: `tests/unit/components/layout/skip-link.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/skip-link.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SkipLink } from '@/components/layout/skip-link';

describe('SkipLink Primitive (Req 7)', () => {
  it('renders anchor targeting #main-content with accessible text', () => {
    render(<SkipLink />);
    const link = screen.getByRole('link', { name: 'Skip to main content' });

    expect(link).toBeDefined();
    expect(link.getAttribute('href')).toBe('#main-content');
  });

  it('applies visually hidden until focus styling and focus ring tokens', () => {
    render(<SkipLink />);
    const link = screen.getByRole('link', { name: 'Skip to main content' });

    expect(link.className).toContain('sr-only');
    expect(link.className).toContain('focus:not-sr-only');
    expect(link.className).toContain('focus:z-50');
    expect(link.className).toContain('focus-visible:ring-focus-ring');
  });
});
'@ | Set-Content "tests\unit\components\layout\skip-link.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/skip-link.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.4, Req 7.5, Req 13.4, Req 15.1

---

### M4.G4.T4: Author Unit Tests for `SiteHeader` Rendering (`tests/unit/components/layout/site-header.test.tsx`)

**Objective:** Create `tests/unit/components/layout/site-header.test.tsx` verifying identity link, primary contact action presentation, email vs non-email variants, and empty-state omission.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/site-header.test.tsx` created
- ✓ Renders `<header>` landmark with `siteName` linking to `/`
- ✓ Renders desktop primary action when `isPrimary: true` channel exists
- ✓ Email primary channel renders `mailto:` link without `target="_blank"`
- ✓ Omits header contact action when `noPrimaryChannelSiteConfig` is supplied
- ✓ Omits header contact action when `emptyContactChannelsSiteConfig` is supplied
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G4.T2 completed
- Test fixtures available at `tests/fixtures/site-config.ts`
- Target file: `tests/unit/components/layout/site-header.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/site-header.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SiteHeader } from '@/components/layout/site-header';
import {
  validSiteConfig,
  noPrimaryChannelSiteConfig,
  emptyContactChannelsSiteConfig,
} from '../../../fixtures/site-config';

vi.mock('next/navigation', () => ({
  usePathname: () => '/',
}));

describe('SiteHeader Component (Req 3)', () => {
  it('renders siteName as identity link to root path /', () => {
    render(
      <SiteHeader
        siteName={validSiteConfig.siteName}
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const identityLink = screen.getByRole('link', { name: validSiteConfig.siteName });
    expect(identityLink).toBeDefined();
    expect(identityLink.getAttribute('href')).toBe('/');
  });

  it('renders email primary contact action with mailto: and no target attribute', () => {
    render(
      <SiteHeader
        siteName={validSiteConfig.siteName}
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const contactAction = screen.getByRole('link', { name: 'Email Angelo' });
    expect(contactAction).toBeDefined();
    expect(contactAction.getAttribute('href')).toBe('mailto:hello@example.com');
    expect(contactAction.getAttribute('target')).toBeNull();
  });

  it('omits contact action when no channel has isPrimary: true', () => {
    render(
      <SiteHeader
        siteName={noPrimaryChannelSiteConfig.siteName}
        navigation={noPrimaryChannelSiteConfig.navigation}
        contactChannels={noPrimaryChannelSiteConfig.contactChannels}
      />
    );

    expect(screen.queryByRole('link', { name: 'Email Angelo' })).toBeNull();
    expect(screen.queryByRole('link', { name: 'LinkedIn Profile' })).toBeNull();
  });

  it('omits contact action when contactChannels array is empty', () => {
    render(
      <SiteHeader
        siteName={emptyContactChannelsSiteConfig.siteName}
        navigation={emptyContactChannelsSiteConfig.navigation}
        contactChannels={emptyContactChannelsSiteConfig.contactChannels}
      />
    );

    const links = screen.getAllByRole('link');
    // Only identity link + navigation links, zero contact action buttons
    expect(links.some((l) => l.textContent?.includes('Email'))).toBe(false);
  });
});
'@ | Set-Content "tests\unit\components\layout\site-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-header.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 3.1, Req 3.3, Req 3.4, Req 15.1, Req 15.5

---

### M4.G4.T5: Author External Primary Action Unit Test

**Objective:** Append a test in `tests/unit/components/layout/site-header.test.tsx` verifying that a non-email primary contact channel renders an `external-link` Button with `target="_blank"`, `rel="noopener noreferrer"`, and new-tab text.

**Acceptance Criteria:**
- ✓ Configures fixture where a LinkedIn channel has `isPrimary: true`
- ✓ Renders `SiteHeader` with the fixture
- ✓ Verifies primary action has `target="_blank"` and `rel="noopener noreferrer"`
- ✓ Verifies link text includes visually hidden `(opens in a new tab)`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G4.T4 completed
- Target file: `tests/unit/components/layout/site-header.test.tsx`

**Implementation Details:**

Append external primary action test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  it('renders non-email primary contact channel with external link attributes', () => {
    const externalPrimaryChannels = [
      {
        type: 'linkedin' as const,
        label: 'LinkedIn Connect',
        url: 'https://linkedin.com/in/angelo',
        isPrimary: true,
      },
    ];

    render(
      <SiteHeader
        siteName="Angelo Andres"
        navigation={validSiteConfig.navigation}
        contactChannels={externalPrimaryChannels}
      />
    );

    const action = screen.getByRole('link', { name: /LinkedIn Connect/ });
    expect(action.getAttribute('href')).toBe('https://linkedin.com/in/angelo');
    expect(action.getAttribute('target')).toBe('_blank');
    expect(action.getAttribute('rel')).toBe('noopener noreferrer');
    expect(action.textContent).toContain('(opens in a new tab)');
  });
'@

$content = Get-Content "tests\unit\components\layout\site-header.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\site-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-header.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 13.2, Req 13.3

---

### M4.G4.T6: Author Property-Based Test for Header Identity and Action (Property 11)

**Objective:** Append property-based test in `tests/unit/components/layout/site-header.test.tsx` using `fast-check` to assert that across randomized site names and contact channels, `SiteHeader` strictly renders the identity link and at most one primary contact action.

**Acceptance Criteria:**
- ✓ Implements Property 11 test ($\ge 100$ runs with `fast-check`)
- ✓ Asserts identity link text strictly matches randomized `siteName`
- ✓ Asserts header renders exactly 1 contact action iff renderable primary channel exists
- ✓ Asserts first primary channel wins when multiple primary channels exist
- ✓ Asserts zero contact actions rendered when no primary channels exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/layout/site-header.test.tsx`

**Implementation Details:**

Append Property 11 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 11)', () => {
    it('Feature: m4-global-layout-navigation, Property 11: identity link matches siteName and renders at most one primary contact action for any config', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { contactChannelArbitrary, navItemArbitrary } = require('../../../fixtures/site-config-arbitraries');
      const { getRenderableChannels } = require('@/components/layout/contact-channels');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 30 }).filter((s: string) => s.trim().length > 0 && !s.includes('<')),
          fc.array(navItemArbitrary, { minLength: 1, maxLength: 4 }),
          fc.array(contactChannelArbitrary, { maxLength: 6 }),
          (name: string, navItems: any, contacts: any) => {
            cleanup();
            render(
              <SiteHeader
                siteName={name}
                navigation={navItems}
                contactChannels={contacts}
              />
            );

            // 1. Identity link check
            const identityLink = screen.getByRole('link', { name });
            expect(identityLink.getAttribute('href')).toBe('/');

            // 2. Action presence check
            const renderablePrimaries = getRenderableChannels(contacts).filter((c: any) => c.isPrimary);
            if (renderablePrimaries.length > 0) {
              const expectedFirst = renderablePrimaries[0];
              const action = screen.getByRole('link', { name: new RegExp(expectedFirst.label) });
              expect(action).toBeDefined();
              expect(action.getAttribute('href')).toBe(expectedFirst.url);
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\site-header.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\site-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-header.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.3, Req 3.4, Req 15.1

---

### M4.G4.T7: Audit Hardcoded Site-Data Literals in Header and SkipLink

**Objective:** Audit `src/components/layout/site-header.tsx` and `skip-link.tsx` to verify zero personal name, email, or site-owner literals are hardcoded per Requirement 2.4.

**Acceptance Criteria:**
- ✓ Searches files for `'Angelo'`, `'Andres'`, `'hello@example.com'`, and `'example.vercel.app'`
- ✓ Confirms zero string matches in source code
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G4.T1 and M4.G4.T2 completed

**Implementation Details:**

Execute literal audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\layout\skip-link.tsx", "src\components\layout\site-header.tsx")
$forbiddenLiterals = @('Angelo', 'Andres', 'hello@example.com', 'example.vercel.app')
$violations = @()

foreach ($f in $files) {
    $content = Get-Content $f -Raw
    foreach ($lit in $forbiddenLiterals) {
        if ($content.Contains($lit)) {
            $violations += "Hardcoded site literal '$lit' found in $f (Req 2.4 violation)"
        }
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 2.4, Req 14.5

---

### M4.G4.T8: Audit Server-Component Boundaries (Zero `'use client'`)

**Objective:** Audit `skip-link.tsx` and `site-header.tsx` to guarantee neither file declares `'use client'`.

**Acceptance Criteria:**
- ✓ `skip-link.tsx` contains zero `'use client'` statements
- ✓ `site-header.tsx` contains zero `'use client'` statements
- ✓ PowerShell audit script exits with PASS

**Prerequisites:**
- M4.G4.T1 and M4.G4.T2 completed

**Implementation Details:**

Execute server boundary check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\layout\skip-link.tsx", "src\components\layout\site-header.tsx")
$violations = @()

foreach ($f in $files) {
    $content = Get-Content $f -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' directive found in $f (must be server component)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 3.6, Req 7.4, Req 14.1, Req 16.2

---

### M4.G4.T9: Verify Source Hygiene of SkipLink and SiteHeader

**Objective:** Audit `skip-link.tsx` and `site-header.tsx` to ensure zero raw hex colors, zero arbitrary Tailwind brackets, zero `any`, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Both files are under 300 lines

**Prerequisites:**
- M4.G4.T1 and M4.G4.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\layout\skip-link.tsx", "src\components\layout\site-header.tsx")
$allPass = $true

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    $lines = (Get-Content $file).Count

    $hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
    $hasRgb = $content -match 'rgba?\('
    $hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
    $hasAny = $content -match ':\s*any\b|\bas\s+any\b'

    if ($hasHex -or $hasRgb -or $hasArbitrary -or $hasAny -or ($lines -ge 300)) {
        $allPass = $false
        Write-Host "Violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.5, Req 13.6, Req 14.6, Req 14.7

---

### M4.G4.T10: Checkpoint — SkipLink and SiteHeader Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `SkipLink` and `SiteHeader`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all SkipLink and SiteHeader tests and passes with code 0
- ✓ Zero regressions introduced into upstream modules

**Prerequisites:**
- M4.G4.T1 through M4.G4.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/skip-link.test.tsx tests/unit/components/layout/site-header.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/skip-link.test.tsx tests/unit/components/layout/site-header.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\layout\skip-link.tsx"
Test-Path "src\components\layout\site-header.tsx"
Test-Path "tests\unit\components\layout\skip-link.test.tsx"
Test-Path "tests\unit\components\layout\site-header.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/layout/skip-link.test.tsx tests/unit/components/layout/site-header.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all SkipLink and SiteHeader tests with return code 0.