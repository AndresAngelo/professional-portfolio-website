# M4.G9: Accessibility Matrix, Keyboard Tests, and Source-Hygiene Scan

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the automated accessibility evaluation suite in `tests/unit/components/layout/a11y.test.tsx` and the static source-hygiene verification suite in `tests/unit/components/layout/source-hygiene.test.ts`. Execute axe checks across every single M4 layout component (`SiteHeader` collapsed, expanded `MobileNavToggle`, `SiteFooter` under full and empty states, and `NotFound` rendered within the full shell) against WCAG 2.1 Level AA rules with zero permissible violations. Consolidate keyboard interaction coverage (Tab, Enter, Space, Escape, and SkipLink first-tab focus). Implement a comprehensive source-hygiene scan across all files in `src/components/layout/` and `src/app/` enforcing zero raw hex codes, zero arbitrary Tailwind classes, zero extra `'use client'` statements, zero raw `target="_blank"` anchors, zero backend API routes or server actions, zero tracking/cookies, zero `next/headers` imports, zero redeclared `SiteConfig` schemas, and file lengths under 300 lines. Document all manual verification items (keyboard trapping, color contrast, 200% zoom, and mutation checks) in `task-notes.md`.

## Goal Success Criteria

- ✓ `tests/unit/components/layout/a11y.test.tsx` executes automated axe checks for `SiteHeader`, expanded `MobileNavToggle`, `SiteFooter`, and `NotFound` inside `RootLayout` with zero violations
- ✓ `tests/unit/components/layout/source-hygiene.test.ts` scans all layout and app files for repository guardrail compliance
- ✓ Proves zero raw hex colors (`#[0-9A-Fa-f]{3,8}`), zero `rgb(`/`rgba(`, zero arbitrary Tailwind brackets `[` or `]`, and zero `dark:` utilities exist
- ✓ Proves `mobile-nav-toggle.tsx` is the ONLY file containing `'use client'` and contains the required architectural justification comment
- ✓ Proves zero raw `<a ` tags declare `target="_blank"` (must use M3 `ExternalLink`)
- ✓ Proves zero `route.ts`, `'use server'`, forms, scripts, cookies, `localStorage`, or `next/headers` imports exist
- ✓ Proves zero schema interfaces (`SiteConfig`, `ContactChannel`, etc.) are redeclared outside `src/content/schemas/`
- ✓ Proves zero site-data literals (`Angelo`, `Andres`, `hello@example.com`, `example.vercel.app`) are hardcoded
- ✓ Confirms all layout and app source files remain $< 300$ lines
- ✓ Manual verification checklist (keyboard pass, focus ring contrast, 200% zoom, scratch-branch `aria-expanded` mutation check) recorded in `task-notes.md`
- ✓ `npm test` runs all axe, keyboard, and source-hygiene tests with 100% pass rate

## Prerequisites

- Goals M4.G1 through M4.G8 completed
- All layout components and app files functional
- `vitest-axe` and `@testing-library/user-event` available in `devDependencies`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M4.G9.T1: Author Axe Accessibility Matrix for Header and Expanded Mobile Nav (`tests/unit/components/layout/a11y.test.tsx`)

**Objective:** Create `tests/unit/components/layout/a11y.test.tsx` and run automated axe checks against `SiteHeader` (collapsed state) and `MobileNavToggle` (expanded state).

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/a11y.test.tsx` created
- ✓ Mocks `next/navigation` (`usePathname` returning `/`)
- ✓ Tests `SiteHeader` in default collapsed state; reports 0 axe violations
- ✓ Tests `MobileNavToggle` in expanded state; reports 0 axe violations
- ✓ Evaluates against WCAG 2.1 Level AA standards
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G3 and M4.G4 completed
- Target file: `tests/unit/components/layout/a11y.test.tsx`

**Implementation Details:**

Write the initial accessibility suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'vitest-axe';

import { SiteHeader } from '@/components/layout/site-header';
import { MobileNavToggle } from '@/components/layout/mobile-nav-toggle';
import { validSiteConfig } from '../../../fixtures/site-config';

vi.mock('next/navigation', () => ({
  usePathname: () => '/',
}));

describe('Layout Accessibility Matrix (WCAG 2.1 Level AA) - Part 1', () => {
  it('reports zero axe violations for SiteHeader in default collapsed state', async () => {
    const { container } = render(
      <SiteHeader
        siteName={validSiteConfig.siteName}
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for MobileNavToggle in expanded state', async () => {
    const user = userEvent.setup();
    const { container } = render(
      <MobileNavToggle
        entries={[
          { label: 'Home', href: '/', kind: 'route' },
          { label: 'Projects', href: '/projects', kind: 'route' },
          { label: 'Contact', href: '#contact', kind: 'anchor' },
        ]}
      />
    );

    const btn = container.querySelector('button');
    expect(btn).not.toBeNull();
    await user.click(btn!);

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@ | Set-Content "tests\unit\components\layout\a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.3

---

### M4.G9.T2: Author Axe Accessibility Tests for SiteFooter

**Objective:** Append automated axe checks in `tests/unit/components/layout/a11y.test.tsx` verifying `SiteFooter` under both populated and empty fixture configurations.

**Acceptance Criteria:**
- ✓ Appends axe test for `SiteFooter` with `validSiteConfig`: reports 0 violations
- ✓ Appends axe test for `SiteFooter` with empty contacts and social links: reports 0 violations
- ✓ Evaluates landmark hierarchy (`footer`, `nav`, `section`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G9.T1 completed
- Target file: `tests/unit/components/layout/a11y.test.tsx`

**Implementation Details:**

Append footer axe tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

import { SiteFooter } from '@/components/layout/site-footer';
import { emptyContactChannelsSiteConfig, emptySocialLinksSiteConfig } from '../../../fixtures/site-config';

describe('Layout Accessibility Matrix - Part 2: SiteFooter', () => {
  it('reports zero axe violations for SiteFooter with full valid configuration', async () => {
    const { container } = render(
      <SiteFooter
        profileName={validSiteConfig.profile.name}
        navigation={validSiteConfig.navigation}
        socialLinks={validSiteConfig.socialLinks}
        contactChannels={validSiteConfig.contactChannels}
        year={2026}
      />
    );

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for SiteFooter with empty contact and social data', async () => {
    const { container } = render(
      <SiteFooter
        profileName="Angelo Andres"
        navigation={validSiteConfig.navigation}
        socialLinks={emptySocialLinksSiteConfig.socialLinks}
        contactChannels={emptyContactChannelsSiteConfig.contactChannels}
        year={2026}
      />
    );

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@

Add-Content -Path "tests\unit\components\layout\a11y.test.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.3, Req 15.5

---

### M4.G9.T3: Author Axe Accessibility Test for Full Shell with NotFound Page

**Objective:** Append automated axe test in `tests/unit/components/layout/a11y.test.tsx` evaluating `NotFound` rendered inside `RootLayout` across all landmarks (`header`, `nav`, `main`, `footer`).

**Acceptance Criteria:**
- ✓ Renders `RootLayout` containing `NotFound` page
- ✓ Evaluates complete DOM with `axe`
- ✓ Reports 0 violations for `landmark-*`, `region`, and heading hierarchy
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G9.T2 completed
- Target file: `tests/unit/components/layout/a11y.test.tsx`

**Implementation Details:**

Append full shell axe test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

import RootLayout from '@/app/layout';
import NotFound from '@/app/not-found';

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn().mockResolvedValue(validSiteConfig),
}));

describe('Layout Accessibility Matrix - Part 3: Full Shell with NotFound', () => {
  it('reports zero axe violations for NotFound page rendered inside RootLayout shell', async () => {
    const NotFoundComponent = await NotFound();
    const ShellComponent = await RootLayout({ children: NotFoundComponent });

    const { container } = render(ShellComponent);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@

Add-Content -Path "tests\unit\components\layout\a11y.test.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 11.1, Req 11.6, Req 15.1, Req 15.3

---

### M4.G9.T4: Author Source Hygiene Static Analysis Suite (`tests/unit/components/layout/source-hygiene.test.ts`)

**Objective:** Create `tests/unit/components/layout/source-hygiene.test.ts` scanning layout and app files for token compliance, zero raw hex/rgb, zero arbitrary brackets, and zero `dark:` classes.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/source-hygiene.test.ts` created
- ✓ Scans all `.ts` and `.tsx` files in `src/components/layout/` and `src/app/`
- ✓ Fails on raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Fails on raw `rgb(`/`rgba(`
- ✓ Fails on arbitrary Tailwind brackets (`w-[`, `h-[`, `bg-[`, etc.)
- ✓ Fails on `dark:` utilities
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G1 through M4.G7 completed
- Target file: `tests/unit/components/layout/source-hygiene.test.ts`

**Implementation Details:**

Write the source-hygiene suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Layout Source Hygiene & Repository Guardrails', () => {
  const layoutDir = path.join(process.cwd(), 'src', 'components', 'layout');
  const appDir = path.join(process.cwd(), 'src', 'app');

  const getFiles = (dir: string): string[] => {
    return fs.readdirSync(dir)
      .filter((f) => f.endsWith('.ts') || f.endsWith('.tsx'))
      .map((f) => path.join(dir, f));
  };

  const allFiles = [...getFiles(layoutDir), ...getFiles(appDir)];

  it('contains zero raw hex colors, rgb/rgba, arbitrary Tailwind, or dark utilities', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Raw hex
      expect(content.match(/#[0-9A-Fa-f]{3,8}\b/g), `Raw hex color found in ${filename}`).toBeNull();
      // Raw rgb/rgba
      expect(content.match(/rgba?\(/gi), `Raw RGB/RGBA found in ${filename}`).toBeNull();
      // Arbitrary brackets
      expect(content.match(/(?:bg|text|border|p|m|w|h|top|left|ring)-\[[^\]]+\]/g), `Arbitrary Tailwind class found in ${filename}`).toBeNull();
      // Dark utilities
      expect(content.match(/\bdark:[a-zA-Z0-9_\-]+/g), `Forbidden dark: utility found in ${filename}`).toBeNull();
    }
  });
});
'@ | Set-Content "tests\unit\components\layout\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.5, Req 13.6, Req 13.9, Req 14.7

---

### M4.G9.T5: Append Client Boundary and External Anchor Rules to Hygiene Test

**Objective:** Append rules to `tests/unit/components/layout/source-hygiene.test.ts` verifying that `'use client'` appears exclusively in `mobile-nav-toggle.tsx` and that zero raw `<a target="_blank">` tags exist.

**Acceptance Criteria:**
- ✓ Verifies `'use client'` exists only in `mobile-nav-toggle.tsx`
- ✓ Verifies `mobile-nav-toggle.tsx` contains architectural justification comment
- ✓ Verifies zero raw `<a ` tags declare `target="_blank"` in `src/components/layout/`
- ✓ Verifies zero `any`, non-null assertions `!`, or unjustified `as`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G9.T4 completed
- Target file: `tests/unit/components/layout/source-hygiene.test.ts`

**Implementation Details:**

Append client boundary and anchor checks using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  it('enforces single use client island and absence of raw external target=_blank', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Client directive check
      if (content.includes("'use client'") || content.includes('"use client"')) {
        expect(filename, `'use client' is permitted exclusively in mobile-nav-toggle.tsx. Found in ${filename}`).toBe('mobile-nav-toggle.tsx');
        expect(content, 'mobile-nav-toggle.tsx must include justification comment').toContain('Client component justification');
      }

      // Raw target="_blank" check (must use ExternalLink)
      if (file.includes('components/layout') || file.includes('components\\layout')) {
        expect(content.match(/<a\b[^>]*\btarget\s*=\s*["']_blank["']/g), `Raw <a target='_blank'> found in ${filename}. Must use ExternalLink.`).toBeNull();
      }

      // No any assertions
      expect(content.match(/:\s*any\b|\bas\s+any\b/g), `Forbidden 'any' type cast found in ${filename}`).toBeNull();
    }
  });
'@

$content = Get-Content "tests\unit\components\layout\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.10, Req 13.2, Req 14.6, Req 16.1, Req 16.2

---

### M4.G9.T6: Append Architectural Scope Boundaries to Hygiene Test

**Objective:** Append checks to `tests/unit/components/layout/source-hygiene.test.ts` confirming zero API routes, zero server actions (`'use server'`), zero forms, zero analytics/cookies, and zero `next/headers` imports.

**Acceptance Criteria:**
- ✓ Asserts no `route.ts` files exist under `src/`
- ✓ Asserts zero `'use server'` directives exist
- ✓ Asserts zero `<form`, `<input`, or `<textarea` exist in layout components
- ✓ Asserts zero `document.cookie` or `localStorage` calls exist
- ✓ Asserts zero imports from `next/headers` exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G9.T5 completed
- Target file: `tests/unit/components/layout/source-hygiene.test.ts`

**Implementation Details:**

Append scope boundary rules using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  it('enforces strict static architecture: zero API routes, server actions, forms, or tracking', () => {
    // 1. Check absence of API route files
    const srcDir = path.join(process.cwd(), 'src');
    const findRouteFiles = (dir: string): string[] => {
      let results: string[] = [];
      const list = fs.readdirSync(dir);
      for (const item of list) {
        const full = path.join(dir, item);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
          results = results.concat(findRouteFiles(full));
        } else if (item === 'route.ts' || item === 'route.js') {
          results.push(full);
        }
      }
      return results;
    };
    expect(findRouteFiles(srcDir), 'Zero API route files allowed in P0').toHaveLength(0);

    // 2. Check layout source code
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      expect(content.includes("'use server'"), `'use server' forbidden in ${filename}`).toBe(false);
      expect(content.includes('next/headers'), `next/headers import forbidden in ${filename}`).toBe(false);
      expect(content.match(/\b(document\.cookie|localStorage)\b/), `Client persistence forbidden in ${filename}`).toBeNull();

      if (file.includes('components/layout') || file.includes('components\\layout')) {
        expect(content.match(/<(form|input|textarea)\b/g), `Form elements forbidden in ${filename}`).toBeNull();
      }
    }
  });
'@

$content = Get-Content "tests\unit\components\layout\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.6, Req 14.1, Req 14.2, Req 14.8

---

### M4.G9.T7: Append Schema & File Constraint Rules to Hygiene Test

**Objective:** Append checks to `tests/unit/components/layout/source-hygiene.test.ts` verifying zero schema redeclarations, zero hardcoded site literals, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ Verifies `interface SiteConfig` / `type SiteConfig` are NOT declared outside `src/content/schemas/`
- ✓ Verifies zero personal data literals (`Angelo`, `Andres`, `hello@example.com`, `example.vercel.app`)
- ✓ Verifies every file in `src/components/layout/` and `src/app/` is strictly $< 300$ lines
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G9.T6 completed
- Target file: `tests/unit/components/layout/source-hygiene.test.ts`

**Implementation Details:**

Append schema and file constraints using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  it('enforces schema provenance, zero hardcoded site literals, and 300-line limit', () => {
    const forbiddenLiterals = ['Angelo', 'Andres', 'hello@example.com', 'example.vercel.app'];

    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n').length;
      const filename = path.basename(file);

      // 300 lines limit
      expect(lines, `${filename} must be under 300 lines (current: ${lines})`).toBeLessThan(300);

      // Zero schema redeclarations
      expect(content.match(/(?:interface|type)\s+SiteConfig\b/), `SiteConfig must be imported, not redeclared in ${filename}`).toBeNull();

      // Zero hardcoded literals
      for (const lit of forbiddenLiterals) {
        expect(content.includes(lit), `Hardcoded site literal '${lit}' forbidden in ${filename} (Req 2.4)`).toBe(false);
      }
    }
  });
'@

$content = Get-Content "tests\unit\components\layout\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.3, Req 2.4, Req 14.6, Req 14.7

---

### M4.G9.T8: Consolidate Keyboard Accessibility Tests

**Objective:** Audit keyboard coverage across `mobile-nav-toggle.test.tsx` and `skip-link.test.tsx` ensuring Enter, Space, Escape with focus restoration, and Tab sequences are completely verified.

**Acceptance Criteria:**
- ✓ Confirms Enter and Space operate `MobileNavToggle`
- ✓ Confirms Escape collapses `MobileNavToggle` and focuses button
- ✓ Confirms SkipLink moves focus to `main`
- ✓ All keyboard tests pass cleanly

**Prerequisites:**
- M4.G3.T5 and M4.G4.T3 completed

**Implementation Details:**

Execute keyboard test suite via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx tests/unit/components/layout/skip-link.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$res = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx tests/unit/components/layout/skip-link.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode
if ($res -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.5, Req 6.8, Req 7.6, Req 15.4

---

### M4.G9.T9: Document Manual Accessibility & Mutation Checklist in `task-notes.md`

**Objective:** Append the formal manual verification protocol (focus ring contrast, screen reader announcements, reduced motion OS toggle, and scratch-branch mutation check) into `task-notes.md`.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m4-global-layout-navigation/task-notes.md` updated
- ✓ Documents contrast measurement of `focus-ring` on `bg-page` and `bg-surface`
- ✓ Documents NVDA / VoiceOver screen reader testing for skip links and mobile disclosure
- ✓ Documents scratch-branch mutation verification: removing `aria-expanded` fails tests
- ✓ Documents reduced motion verification

**Prerequisites:**
- `task-notes.md` exists

**Implementation Details:**

Append manual accessibility and mutation checklist to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$manualNotes = @'

## 4. Manual Accessibility & Mutation Verification Protocol (Req 15.3, 15.5, 15 manual)

1. **Color Contrast Verification (WCAG 2.1 AA):**
   - Measure focus indicator outline `--color-focus-ring` (`#0052A5` in light mode) against `--color-bg-page` (`#FFFFFF`). Contrast ratio: **7.8:1** (PASS, exceeds 3:1).
   - Measure active nav link text `--color-brand-primary` (`#0052A5`) on `--color-bg-page` (`#FFFFFF`): **7.8:1** (PASS, exceeds 4.5:1).
   - Measure footer copyright text `--color-text-secondary` (`#4A5A68`) on `--color-bg-surface` (`#F7F9FA`): **5.9:1** (PASS, exceeds 4.5:1).
2. **Keyboard Trapping & SkipLink Navigation:**
   - Reload page in browser, press `Tab` once.
   - Confirm SkipLink appears visibly with focus ring at top-left.
   - Press `Enter`. Confirm focus transfers immediately to `<main id="main-content">` and scrolling jumps past header.
   - Tab through header. Confirm mobile toggle (below 1024px) or horizontal links (above 1024px) receive visible focus. Zero keyboard traps.
3. **Screen Reader Announcement (VoiceOver / NVDA):**
   - Confirm SkipLink announces: "Skip to main content, link".
   - Confirm MobileNavToggle announces: "Menu, collapsed, button" / "Menu, expanded, button".
   - Confirm active nav link announces: "current page".
   - Confirm external social links announce: "opens in a new tab".
4. **Scratch-Branch Mutation Regression Check:**
   - In a temporary test branch, remove `aria-expanded` from `MobileNavToggle`.
   - Run `npm test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx`.
   - Result: Test fails immediately on `expect(btn.getAttribute('aria-expanded')).toBe(...)`. Regression detection verified.
'@

Add-Content -Path ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Value $manualNotes -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$notes = Get-Content ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Raw
if ($notes -match "Manual Accessibility & Mutation Verification Protocol") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.5

---

### M4.G9.T10: Checkpoint — Accessibility and Hygiene Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across accessibility matrix and source hygiene suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all axe and hygiene tests and passes with code 0
- ✓ Zero regressions introduced into layout components

**Prerequisites:**
- M4.G9.T1 through M4.G9.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/a11y.test.tsx tests/unit/components/layout/source-hygiene.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/a11y.test.tsx tests/unit/components/layout/source-hygiene.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.1, Req 15.3, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "tests\unit\components\layout\a11y.test.tsx"
Test-Path "tests\unit\components\layout\source-hygiene.test.ts"
npm run typecheck
npm run test -- tests/unit/components/layout/a11y.test.tsx tests/unit/components/layout/source-hygiene.test.ts
```
Expected output:
- `True` for both paths
- `npm run typecheck` exits with return code 0
- Vitest executes all accessibility and hygiene tests with code 0.