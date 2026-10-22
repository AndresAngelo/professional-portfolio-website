# M4.G6: Site Metadata and Root Layout

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure site metadata generator `buildSiteMetadata` in `src/app/site-metadata.ts` and the canonical Root Layout shell in `src/app/layout.tsx`. `buildSiteMetadata` derives standard Next.js metadata (`metadataBase`, `title.default`, `title.template = '%s | {siteName}'`, `description`, Open Graph defaults) strictly from `SiteConfig` without hardcoded site strings, rejecting non-absolute URLs with a descriptive error. `src/app/layout.tsx` serves as the top-level server-component shell wrapping every route with the required landmark hierarchy: `html[lang="en"]`, `SkipLink`, `SiteHeader`, `main#main-content[tabIndex={-1}]`, and `SiteFooter` in exact document order. It loads site data via `await getSiteConfig()` (allowing validation errors to bubble without suppressive `try/catch`), imports M1's global stylesheet, and documents the intentional `focus:outline-none` exception on the non-interactive `main` container. Validate metadata generation, layout landmarks, and Properties 12 and 13 using Vitest.

## Goal Success Criteria

- ✓ `src/app/site-metadata.ts` exports pure helper `buildSiteMetadata` mapping `SiteConfig` to Next.js `Metadata`
- ✓ `buildSiteMetadata` sets `title.template = '%s | {siteName}'` and `metadataBase = new URL(siteUrl)`
- ✓ `buildSiteMetadata` sets Open Graph `type: 'website'`, `siteName`, `title`, `description`, and `url` without images or Twitter image defaults (Req 10.5, 10.6)
- ✓ Invalid non-absolute `siteUrl` throws an `Error` explicitly naming `SiteConfig.siteUrl`
- ✓ `src/app/layout.tsx` implemented as an async server component without `'use client'`
- ✓ Root layout renders `<html lang="en">` and exactly one `<main id="main-content" tabIndex={-1}>`
- ✓ Landmark sequence strictly follows: `SkipLink` $\rightarrow$ `SiteHeader` $\rightarrow$ `main#main-content` $\rightarrow$ `SiteFooter`
- ✓ `layout.tsx` exports `generateMetadata` consuming `buildSiteMetadata(await getSiteConfig())`
- ✓ Corrupted site data causes `getSiteConfig()` error to surface directly, failing the build
- ✓ `tests/unit/app/site-metadata.test.ts` and `layout.test.tsx` pass with 100% assertions
- ✓ Property 12 and Property 13 tests pass $\ge 100$ runs with `fast-check`

## Prerequisites

- Goals M4.G1 through M4.G5 completed (`SkipLink`, `SiteHeader`, `SiteFooter` available)
- M2 loader `getSiteConfig` available at `src/content/loaders/site.ts`
- M1 stylesheet available at `src/app/globals.css`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M4.G6.T1: Implement Pure Metadata Builder (`src/app/site-metadata.ts`)

**Objective:** Author the pure function `buildSiteMetadata` in `src/app/site-metadata.ts` deriving Next.js `Metadata` strictly from `SiteConfig`.

**Acceptance Criteria:**
- ✓ File `src/app/site-metadata.ts` created
- ✓ Exports `buildSiteMetadata(site: Pick<SiteConfig, 'siteName' | 'siteUrl' | 'profile'>): Metadata`
- ✓ Constructs `metadataBase` from `new URL(site.siteUrl)`
- ✓ Sets `title.default = site.siteName` and `title.template = `%s | ${site.siteName}``
- ✓ Sets `description = site.profile.introduction`
- ✓ Configures `openGraph` with `type: 'website'`, `siteName`, `title`, `description`, and `url`
- ✓ Emits zero `images` array and zero `twitter` key (Req 10.6)
- ✓ Pure module without React or Next.js layout dependencies

**Prerequisites:**
- M4.G1 completed (`SiteConfig` type available)
- Target file: `src/app/site-metadata.ts`

**Implementation Details:**

Write `src/app/site-metadata.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import type { Metadata } from 'next';
import type { SiteConfig } from '@/types/content';

/**
 * Pure Metadata Construction Helper
 *
 * Derives site-wide Next.js metadata from SiteConfig.
 * TRD.md 2.1, AGENTS.md 4.2 & Requirement 10.
 */
export function buildSiteMetadata(
  site: Pick<SiteConfig, 'siteName' | 'siteUrl' | 'profile'>
): Metadata {
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(site.siteUrl);
  } catch {
    throw new Error(
      `[buildSiteMetadata] Invalid SiteConfig.siteUrl: expected a valid absolute HTTPS URL, received "${site.siteUrl.slice(0, 20)}...".`
    );
  }

  return {
    metadataBase: parsedUrl,
    title: {
      default: site.siteName,
      template: `%s | ${site.siteName}`,
    },
    description: site.profile.introduction,
    openGraph: {
      type: 'website',
      siteName: site.siteName,
      title: site.siteName,
      description: site.profile.introduction,
      url: parsedUrl.href,
    },
  };
}
'@ | Set-Content "src\app\site-metadata.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/app/site-metadata.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 10.6, Req 10.7, Req 10.8

---

### M4.G6.T2: Implement Root Layout Component (`src/app/layout.tsx`)

**Objective:** Author the server component `RootLayout` and `generateMetadata` in `src/app/layout.tsx` composing the full global shell around child pages.

**Acceptance Criteria:**
- ✓ File `src/app/layout.tsx` updated
- ✓ Imports `./globals.css` (M1 global stylesheet)
- ✓ Exports `async function generateMetadata(): Promise<Metadata>` calling `buildSiteMetadata(await getSiteConfig())`
- ✓ Exports `default async function RootLayout({ children }: { children: ReactNode }): Promise<JSX.Element>`
- ✓ Renders `<html lang="en">`
- ✓ Renders `<body className="flex min-h-screen flex-col bg-page text-text-primary">`
- ✓ Renders `<SkipLink />` as first focusable child
- ✓ Renders `<SiteHeader siteName={...} navigation={...} contactChannels={...} />`
- ✓ Renders `<main id="main-content" tabIndex={-1} className="flex-1 focus:outline-none">` containing `{children}`
- ✓ Renders `<SiteFooter profileName={...} navigation={...} socialLinks={...} contactChannels={...} />`
- ✓ Documents `focus:outline-none` on `main` as an intentional non-interactive focus target exception
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G6.T1 completed (`buildSiteMetadata` available)
- M4.G4 completed (`SkipLink`, `SiteHeader` available)
- M4.G5 completed (`SiteFooter` available)
- Target file: `src/app/layout.tsx`

**Implementation Details:**

Write `src/app/layout.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React, { type ReactNode } from 'react';
import type { Metadata } from 'next';
import './globals.css';
import { getSiteConfig } from '@/content/loaders/site';
import { SkipLink } from '@/components/layout/skip-link';
import { SiteHeader } from '@/components/layout/site-header';
import { SiteFooter } from '@/components/layout/site-footer';
import { MAIN_CONTENT_ID } from '@/components/layout/layout-text';
import { buildSiteMetadata } from './site-metadata';

/**
 * Generates site-wide default metadata from validated content.
 */
export async function generateMetadata(): Promise<Metadata> {
  const site = await getSiteConfig();
  return buildSiteMetadata(site);
}

/**
 * Root Layout Shell
 *
 * Wraps every page with consistent landmark regions and accessible navigation.
 * AGENTS.md Section 3, TRD.md 3.3 & Requirement 1. Server component by default (Req 1.7).
 */
export default async function RootLayout({
  children,
}: {
  children: ReactNode;
}): Promise<JSX.Element> {
  const site = await getSiteConfig();

  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col bg-page text-text-primary antialiased">
        <SkipLink />
        <SiteHeader
          siteName={site.siteName}
          navigation={site.navigation}
          contactChannels={site.contactChannels}
        />
        {/*
          main is given tabIndex={-1} to receive keyboard focus directly from SkipLink.
          focus:outline-none is applied here to prevent a full-page rectangular focus ring
          since main is a structural container rather than an interactive control (Req 7.3, 13.4).
        */}
        <main
          id={MAIN_CONTENT_ID}
          tabIndex={-1}
          className="flex-1 focus:outline-none"
        >
          {children}
        </main>
        <SiteFooter
          profileName={site.profile.name}
          navigation={site.navigation}
          socialLinks={site.socialLinks}
          contactChannels={site.contactChannels}
        />
      </body>
    </html>
  );
}
'@ | Set-Content "src\app\layout.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/app/layout.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 1.4, Req 1.6, Req 1.7, Req 2.1, Req 7.3, Req 10.1

---

### M4.G6.T3: Author Unit Tests for Metadata Builder (`tests/unit/app/site-metadata.test.ts`)

**Objective:** Create `tests/unit/app/site-metadata.test.ts` verifying title defaults, template interpolation, canonical `metadataBase`, and Open Graph parameters.

**Acceptance Criteria:**
- ✓ File `tests/unit/app/site-metadata.test.ts` created
- ✓ `metadataBase` equals `new URL(siteUrl)`
- ✓ `title.default` equals `siteName`
- ✓ `title.template` equals `%s | Angelo Andres`
- ✓ `description` equals `profile.introduction`
- ✓ Open Graph fields are correctly populated
- ✓ Asserts `images` key does NOT exist in Open Graph config (Req 10.6)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G6.T1 completed
- Target file: `tests/unit/app/site-metadata.test.ts`

**Implementation Details:**

Write `tests/unit/app/site-metadata.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "tests\unit\app")) {
    New-Item -ItemType Directory -Path "tests\unit\app" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { buildSiteMetadata } from '@/app/site-metadata';
import { validSiteConfig } from '../../fixtures/site-config';

describe('Site Metadata Builder (Req 10)', () => {
  it('constructs complete metadata from valid SiteConfig', () => {
    const meta = buildSiteMetadata(validSiteConfig);

    expect(meta.metadataBase?.href).toBe('https://example.vercel.app/');
    expect(meta.title).toEqual({
      default: 'Angelo Andres',
      template: '%s | Angelo Andres',
    });
    expect(meta.description).toBe(validSiteConfig.profile.introduction);

    expect(meta.openGraph).toEqual({
      type: 'website',
      siteName: 'Angelo Andres',
      title: 'Angelo Andres',
      description: validSiteConfig.profile.introduction,
      url: 'https://example.vercel.app/',
    });

    // Ensure zero unwanted image placeholders
    expect((meta.openGraph as any).images).toBeUndefined();
    expect(meta.twitter).toBeUndefined();
  });
});
'@ | Set-Content "tests\unit\app\site-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/site-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 10.6, Req 10.8

---

### M4.G6.T4: Author Property-Based Test for Metadata Builder (Property 12)

**Objective:** Append property-based test in `tests/unit/app/site-metadata.test.ts` using `fast-check` verifying Property 12: metadata values strictly derive from input config without hardcoded values or image keys.

**Acceptance Criteria:**
- ✓ Implements Property 12 test ($\ge 100$ runs with `fast-check`)
- ✓ Asserts `metadataBase.href` matches normalized `siteUrl`
- ✓ Asserts `title.default` matches `siteName`
- ✓ Asserts `title.template` equals `%s | ${siteName}`
- ✓ Asserts `openGraph.description` matches introduction
- ✓ Asserts `openGraph.images` and `twitter` remain undefined
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/app/site-metadata.test.ts`

**Implementation Details:**

Append Property 12 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 12)', () => {
    it('Feature: m4-global-layout-navigation, Property 12: site metadata is derived exclusively from SiteConfig for any valid input', () => {
      const fc = require('fast-check');
      const { absoluteUrlArbitrary } = require('../../fixtures/site-config-arbitraries');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 30 }).filter((s: string) => s.trim().length > 0 && !s.includes('<')),
          absoluteUrlArbitrary,
          fc.string({ minLength: 10, maxLength: 100 }).filter((s: string) => s.trim().length > 0 && !s.includes('<')),
          (siteName: string, siteUrl: string, intro: string) => {
            const config = {
              siteName,
              siteUrl,
              profile: { introduction: intro } as any,
            };

            const meta = buildSiteMetadata(config);
            const expectedUrl = new URL(siteUrl).href;

            expect(meta.metadataBase?.href).toBe(expectedUrl);
            expect(meta.title).toEqual({
              default: siteName,
              template: `%s | ${siteName}`,
            });
            expect(meta.description).toBe(intro);
            expect(meta.openGraph?.siteName).toBe(siteName);
            expect(meta.openGraph?.url).toBe(expectedUrl);
            expect((meta.openGraph as any)?.images).toBeUndefined();
            expect(meta.twitter).toBeUndefined();
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\app\site-metadata.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\site-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/site-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 10.6, Req 10.8

---

### M4.G6.T5: Author Property-Based Test for Invalid Site URL Rejection (Property 13)

**Objective:** Append property-based test in `tests/unit/app/site-metadata.test.ts` verifying Property 13: any non-absolute URL string throws an `Error` explicitly naming `SiteConfig.siteUrl`.

**Acceptance Criteria:**
- ✓ Implements Property 13 test ($\ge 100$ runs with `fast-check`)
- ✓ Generates invalid non-absolute URL strings using `invalidUrlArbitrary`
- ✓ Asserts `buildSiteMetadata` throws an Error
- ✓ Asserts error message contains `'SiteConfig.siteUrl'`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/app/site-metadata.test.ts`

**Implementation Details:**

Append Property 13 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 13)', () => {
    it('Feature: m4-global-layout-navigation, Property 13: invalid siteUrl is rejected with descriptive error naming SiteConfig.siteUrl', () => {
      const fc = require('fast-check');
      const { invalidUrlArbitrary } = require('../../fixtures/site-config-arbitraries');

      fc.assert(
        fc.property(
          invalidUrlArbitrary,
          (badUrl: string) => {
            const config = {
              siteName: 'Test',
              siteUrl: badUrl,
              profile: { introduction: 'Intro' } as any,
            };

            expect(() => buildSiteMetadata(config)).toThrow(/SiteConfig\.siteUrl/);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\app\site-metadata.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\site-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/site-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.7

---

### M4.G6.T6: Author Unit Tests for Root Layout Shell (`tests/unit/app/layout.test.tsx`)

**Objective:** Create `tests/unit/app/layout.test.tsx` verifying landmark hierarchy, `lang="en"`, single `<main>` element, and correct document order.

**Acceptance Criteria:**
- ✓ File `tests/unit/app/layout.test.tsx` created
- ✓ Mocks `getSiteConfig` returning `validSiteConfig`
- ✓ Verifies `<html>` contains `lang="en"`
- ✓ Verifies exactly one `<main>` landmark exists
- ✓ Verifies `<main>` has `id="main-content"` and `tabIndex={-1}`
- ✓ Verifies document order: `SkipLink` $\rightarrow$ `header` $\rightarrow$ `main` $\rightarrow$ `footer`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G6.T2 completed
- Target file: `tests/unit/app/layout.test.tsx`

**Implementation Details:**

Write `tests/unit/app/layout.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import RootLayout from '@/app/layout';
import { validSiteConfig } from '../../fixtures/site-config';

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn().mockResolvedValue(validSiteConfig),
}));

vi.mock('next/navigation', () => ({
  usePathname: () => '/',
}));

describe('RootLayout Component (Req 1, 7)', () => {
  it('renders standard landmark regions in exact required document order', async () => {
    const LayoutComponent = await RootLayout({
      children: <div data-testid="page-content">Home Content</div>,
    });

    const { container } = render(LayoutComponent);

    // 1. Verify single main landmark
    const mains = container.querySelectorAll('main');
    expect(mains.length).toBe(1);

    const main = mains[0];
    expect(main.getAttribute('id')).toBe('main-content');
    expect(main.getAttribute('tabindex')).toBe('-1');

    // 2. Verify header, main, and footer presence
    const header = container.querySelector('header');
    const footer = container.querySelector('footer');
    expect(header).not.toBeNull();
    expect(footer).not.toBeNull();

    // 3. Verify exact DOM order: skip link -> header -> main -> footer
    const skipLink = screen.getByRole('link', { name: 'Skip to main content' });
    expect(skipLink.compareDocumentPosition(header!)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    expect(header!.compareDocumentPosition(main)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    expect(main.compareDocumentPosition(footer!)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);

    // 4. Verify child content rendered inside main
    expect(screen.getByTestId('page-content')).toBeDefined();
  });
});
'@ | Set-Content "tests\unit\app\layout.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/layout.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 1.4, Req 7.1, Req 7.3, Req 15.1

---

### M4.G6.T7: Author Content Loader Rejection Test for Layout

**Objective:** Append a test in `tests/unit/app/layout.test.tsx` verifying that loader validation failures propagate directly without suppressive error boundaries, causing static build to fail per Requirement 2.5.

**Acceptance Criteria:**
- ✓ Mocks `getSiteConfig` to reject with a validation `Error`
- ✓ Confirms `RootLayout` rejects with the exact same error
- ✓ Proves zero try/catch blocks swallow content schema failures
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G6.T6 completed
- Target file: `tests/unit/app/layout.test.tsx`

**Implementation Details:**

Append loader rejection test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Loader Failure Propagation (Req 2.5)', () => {
    it('propagates getSiteConfig validation rejection directly to fail build', async () => {
      const { getSiteConfig } = await import('@/content/loaders/site');
      vi.mocked(getSiteConfig).mockRejectedValueOnce(
        new Error('Content schema validation failed: [site.json] missing profile.name')
      );

      await expect(
        RootLayout({ children: <div>Fail Test</div> })
      ).rejects.toThrow('Content schema validation failed: [site.json] missing profile.name');
    });
  });
'@

$content = Get-Content "tests\unit\app\layout.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\app\layout.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/app/layout.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.5

---

### M4.G6.T8: Audit Server-Component Status & Absence of Browser APIs

**Objective:** Audit `src/app/layout.tsx` and `src/app/site-metadata.ts` to confirm neither declares `'use client'` and neither accesses `window`, `document`, or `headers()` per Requirement 1.7 and 2.6.

**Acceptance Criteria:**
- ✓ Confirms zero `'use client'` statements in `layout.tsx` or `site-metadata.ts`
- ✓ Confirms zero occurrences of `headers()`, `cookies()`, `window`, or `document`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G6.T1 and M4.G6.T2 completed

**Implementation Details:**

Execute boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appFiles = @("src\app\layout.tsx", "src\app\site-metadata.ts")
$violations = @()

foreach ($f in $appFiles) {
    $content = Get-Content $f -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "$f must NOT declare 'use client'"
    }
    if ($content -match "\b(window|document|next\/headers)\b") {
        $violations += "$f accesses forbidden client or dynamic server APIs"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.7, Req 2.6, Req 14.8, Req 16.2

---

### M4.G6.T9: Verify Source Hygiene of Root Layout and Metadata Modules

**Objective:** Audit `layout.tsx` and `site-metadata.ts` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `any`, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Both files are under 300 lines

**Prerequisites:**
- M4.G6.T1 and M4.G6.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\app\layout.tsx", "src\app\site-metadata.ts")
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

### M4.G6.T10: Checkpoint — Root Layout and Metadata Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across Root Layout and Metadata modules.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all layout and metadata tests and passes with code 0
- ✓ Zero regressions introduced into upstream modules

**Prerequisites:**
- M4.G6.T1 through M4.G6.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/app/site-metadata.test.ts tests/unit/app/layout.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/app/site-metadata.test.ts tests/unit/app/layout.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\app\site-metadata.ts"
Test-Path "src\app\layout.tsx"
Test-Path "tests\unit\app\site-metadata.test.ts"
Test-Path "tests\unit\app\layout.test.tsx"
npm run typecheck
npm run test -- tests/unit/app/site-metadata.test.ts tests/unit/app/layout.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all site metadata and layout tests with return code 0.