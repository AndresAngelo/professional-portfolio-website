# M5.G9: Responsive, Token, and Scope Compliance; Accessibility Matrix; Source Hygiene

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute an exhaustive responsive design audit, design-token compliance verification, WCAG 2.1 AA automated accessibility evaluation, and strict static source-hygiene scan across all Milestone 5 components (`HeroSection`, `FeaturedProjects`, `SkillsSnapshot`, `CertificationsPreview`, `RecentActivity`, `HomeContent`, and `src/app/page.tsx`). Ensure all sections constrain horizontal width via M3's `Container` primitive, and verify that project and certification card grids transition smoothly from 1 column on mobile (`grid-cols-1`) to 2 columns on tablet (`md:grid-cols-2`) and up to 3 columns on desktop (`lg:grid-cols-3`) without client-side JavaScript or arbitrary Tailwind dimension brackets (`w-[`, `h-[`). Execute axe accessibility tests across the entire homepage in both fully populated and empty-data states with zero permissible violations. Enforce source-hygiene rules verifying zero `'use client'` statements, zero raw hex colors, zero `rgb(`/`rgba(`, zero `dark:` utilities, zero raw `target="_blank"` anchors, zero API routes or server actions, zero forms, cookies, or tracking scripts, zero redeclared `SiteConfig` or content interfaces, zero hardcoded personal literals, and file lengths strictly under 300 lines. Formally document the manual responsive and keyboard verification checklist in `task-notes.md`.

## Goal Success Criteria

- ✓ All M5 section components compose M3's `Container` primitive for width and horizontal padding
- ✓ FeaturedProjects and CertificationsPreview grids apply responsive column classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ RecentActivity applies single-column styling across all viewports (`flex flex-col`)
- ✓ Confirms zero occurrences of `useState`, `useEffect`, `matchMedia`, `fetch(`, `window`, or `document` in M5 source files (Req 15.3, 15.6)
- ✓ Confirms M3's `FOCUS_RING` is applied to every interactive control and motion classes respect `prefers-reduced-motion`
- ✓ `tests/home/a11y.test.tsx` executes automated axe checks for the full homepage in both populated and empty-data states with zero violations
- ✓ `tests/home/source-hygiene.test.ts` scans all M5 layout and app files for repository guardrail compliance with 100% pass rate
- ✓ `git diff` confirms changes are strictly confined to `src/app/page.tsx`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, and `tests/`
- ✓ Manual responsive and keyboard testing protocol documented in `task-notes.md`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1 through M5.G8 completed (all components, helpers, and route files operational)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `vitest-axe` installed in `devDependencies`

---

## Tasks

### M5.G9.T1: Audit Breakpoint Utilities and Absence of Arbitrary Dimension Classes

**Objective:** Inspect all files in `src/components/home/` and `src/app/page.tsx` ensuring responsive layout relies strictly on standard Tailwind breakpoints (`md:`, `lg:`) and contains zero arbitrary dimension brackets `[` or `]`.

**Acceptance Criteria:**
- ✓ Scans all M5 components and route files
- ✓ Confirms card grids apply `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Confirms zero occurrences of arbitrary dimension utilities (`w-[`, `min-w-[`, `h-[`, `min-h-[`, `p-[`, `px-[`, `py-[`, `gap-[`)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M5.G5 through M5.G8 completed

**Implementation Details:**

Execute breakpoint audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$targetDirs = @("src\components\home", "src\app\page.tsx")
$files = Get-ChildItem -Path "src\components\home" -Include *.ts, *.tsx -Recurse
$files += Get-Item "src\app\page.tsx"

$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $arbitraryMatches = [regex]::Matches($content, '(?:w|min-w|max-w|h|min-h|p|px|py|m|mx|my|gap)-\[[^\]]+\]')
    foreach ($m in $arbitraryMatches) {
        $violations += "Arbitrary dimension class found in $($file.Name): $($m.Value)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 14.8, Req 15.2, Req 15.3, Req 15.4, Req 15.6

---

### M5.G9.T2: Verify Zero Client State and Framework Invariance in M5

**Objective:** Audit all M5 components and helpers to verify that zero client components exist and no React client hooks (`useState`, `useEffect`) or browser globals (`matchMedia`, `window`, `document`) are imported.

**Acceptance Criteria:**
- ✓ Scans all files in `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, and `src/app/page.tsx`
- ✓ Confirms zero occurrences of `'use client'`
- ✓ Confirms zero imports of `useState`, `useEffect`, `useReducer`, or `matchMedia`
- ✓ Confirms zero occurrences of `window`, `document`, or `fetch(`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M5.G1 through M5.G8 completed

**Implementation Details:**

Execute client boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$targetDirs = @("src\components\home", "src\lib\home", "src\lib\format-date.ts", "src\app\page.tsx")
$files = Get-ChildItem -Path "src\components\home", "src\lib\home" -Include *.ts, *.tsx -Recurse
$files += Get-Item "src\lib\format-date.ts"
$files += Get-Item "src\app\page.tsx"

$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' found in $($file.Name)"
    }
    if ($content -match "\b(useState|useEffect|useReducer|matchMedia)\b") {
        $violations += "Forbidden client hook/API found in $($file.Name)"
    }
    if ($content -match "\b(window|document|fetch)\b") {
        $violations += "Forbidden browser global found in $($file.Name)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 1.6, Req 15.3, Req 15.6

---

### M5.G9.T3: Verify Composition of M3 UI Primitives & Focus Ring Helpers

**Objective:** Perform static analysis across M5 components to confirm mandatory composition of M3 primitives (`Container`, `Card`, `TagList`, `StatusBadge`, `EventTypeBadge`, `EmptyState`, `Button`, `ExternalLink`, `FOCUS_RING`) without local redefinition.

**Acceptance Criteria:**
- ✓ Confirms `Container` wraps `HeroSection`, `FeaturedProjects`, `SkillsSnapshot`, `CertificationsPreview`, and `RecentActivity`
- ✓ Confirms `FOCUS_RING` is applied to all interactive links and buttons
- ✓ Confirms `ExternalLink` is used for external destinations (zero raw `<a target="_blank">`)
- ✓ Confirms motion classes include `MOTION_FAST` (carrying `motion-reduce:transition-none`)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M5.G5 through M5.G7 completed

**Implementation Details:**

Execute primitive composition audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$componentFiles = @(
    "src\components\home\hero-section.tsx",
    "src\components\home\featured-projects.tsx",
    "src\components\home\skills-snapshot.tsx",
    "src\components\home\certifications-preview.tsx",
    "src\components\home\recent-activity.tsx"
)
$violations = @()

foreach ($f in $componentFiles) {
    $content = Get-Content $f -Raw
    if (-not ($content -match '\bContainer\b')) {
        $violations += "$f must import and render Container primitive (Req 15.1)"
    }
    if (-not ($content -match '\bFOCUS_RING\b')) {
        # skills-snapshot contains no links, others do
        if ($f -notmatch 'skills-snapshot') {
            $violations += "$f must import and apply FOCUS_RING helper (Req 14.4)"
        }
    }
    if ($content -match '<a\b[^>]*\btarget\s*=\s*["'']_blank["'']') {
        $violations += "Raw <a target='_blank'> found in $f. Must use ExternalLink primitive (Req 3.5)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 3.5, Req 14.4, Req 14.6, Req 15.1, Req 16.1

---

### M5.G9.T4: Author Automated Axe Accessibility Tests for Full Homepage (`tests/home/a11y.test.tsx`)

**Objective:** Create `tests/home/a11y.test.tsx` executing automated axe accessibility tests on the full Homepage under populated and empty-data states with zero violations.

**Acceptance Criteria:**
- ✓ File `tests/home/a11y.test.tsx` created
- ✓ Mocks loaders returning full sample fixtures
- ✓ Evaluates full Homepage via `axe`: 0 violations
- ✓ Mocks loaders returning empty projects, empty certs, and drafts-only posts
- ✓ Evaluates empty-state Homepage via `axe`: 0 violations
- ✓ Evaluates against WCAG 2.1 Level AA standards
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8 completed
- Target file: `tests/home/a11y.test.tsx`

**Implementation Details:**

Write `tests/home/a11y.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import HomePage from '@/app/page';
import {
  sampleSiteConfig,
  sampleProjects,
  sampleCertifications,
  sampleBlogPosts,
  emptyProjects,
  emptyCertifications,
  draftsOnlyBlogPosts,
  emptyContactChannelsSiteConfig,
  unavailableSiteConfig,
} from '../fixtures/home-data';

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(),
}));
vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
}));
vi.mock('@/content/loaders/certifications', () => ({
  getCertifications: vi.fn(),
}));
vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(),
}));

describe('Homepage Axe Accessibility Matrix (Req 14)', () => {
  it('reports zero axe violations for fully populated Homepage', async () => {
    const { getSiteConfig } = await import('@/content/loaders/site');
    const { getProjects } = await import('@/content/loaders/projects');
    const { getCertifications } = await import('@/content/loaders/certifications');
    const { getBlogPosts } = await import('@/content/loaders/blog');

    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);
    vi.mocked(getProjects).mockResolvedValue(sampleProjects);
    vi.mocked(getCertifications).mockResolvedValue(sampleCertifications);
    vi.mocked(getBlogPosts).mockResolvedValue(sampleBlogPosts);

    const Component = await HomePage();
    const { container } = render(Component);

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for Homepage in empty-data states', async () => {
    const { getSiteConfig } = await import('@/content/loaders/site');
    const { getProjects } = await import('@/content/loaders/projects');
    const { getCertifications } = await import('@/content/loaders/certifications');
    const { getBlogPosts } = await import('@/content/loaders/blog');

    vi.mocked(getSiteConfig).mockResolvedValue({
      ...unavailableSiteConfig,
      ...emptyContactChannelsSiteConfig,
    });
    vi.mocked(getProjects).mockResolvedValue(emptyProjects);
    vi.mocked(getCertifications).mockResolvedValue(emptyCertifications);
    vi.mocked(getBlogPosts).mockResolvedValue(draftsOnlyBlogPosts);

    const Component = await HomePage();
    const { container } = render(Component);

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@ | Set-Content "tests\home\a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.4, Req 14.7

---

### M5.G9.T5: Author Source Hygiene Static Analysis Suite (`tests/home/source-hygiene.test.ts`)

**Objective:** Create `tests/home/source-hygiene.test.ts` scanning all M5 files for repository guardrail compliance, token compliance, zero raw colors, zero arbitrary brackets, and zero `dark:` classes.

**Acceptance Criteria:**
- ✓ File `tests/home/source-hygiene.test.ts` created
- ✓ Scans all `.ts` and `.tsx` files in `src/components/home/`, `src/lib/home/`, and `src/app/page.tsx`
- ✓ Fails on raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Fails on raw `rgb(`/`rgba(`
- ✓ Fails on arbitrary Tailwind brackets (`w-[`, `h-[`, `bg-[`, etc.)
- ✓ Fails on `dark:` utilities
- ✓ Tests pass under `npm test`

**Prerequisites:**
- Target file: `tests/home/source-hygiene.test.ts`

**Implementation Details:**

Write the source-hygiene suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Homepage Source Hygiene & Design Token Compliance (Req 14, 16)', () => {
  const homeDir = path.join(process.cwd(), 'src', 'components', 'home');
  const libHomeDir = path.join(process.cwd(), 'src', 'lib', 'home');
  const pageFile = path.join(process.cwd(), 'src', 'app', 'page.tsx');

  const getFiles = (dir: string): string[] => {
    return fs.readdirSync(dir)
      .filter((f) => f.endsWith('.ts') || f.endsWith('.tsx'))
      .map((f) => path.join(dir, f));
  };

  const allFiles = [...getFiles(homeDir), ...getFiles(libHomeDir), pageFile];

  it('contains zero raw hex colors, rgb/rgba, arbitrary Tailwind, or dark utilities', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Raw hex
      expect(content.match(/#[0-9A-Fa-f]{3,8}\b/g), `Raw hex color found in ${filename}`).toBeNull();
      // Raw rgb/rgba
      expect(content.match(/rgba?\(/gi), `Raw RGB/RGBA found in ${filename}`).toBeNull();
      // Arbitrary brackets
      expect(content.match(/(?:bg|text|border|p|m|w|h|top|left|ring|gap)-\[[^\]]+\]/g), `Arbitrary Tailwind class found in ${filename}`).toBeNull();
      // Dark utilities
      expect(content.match(/\bdark:[a-zA-Z0-9_\-]+/g), `Forbidden dark: utility found in ${filename}`).toBeNull();
    }
  });
});
'@ | Set-Content "tests\home\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.4, Req 9.6, Req 14.7, Req 14.8, Req 16.7

---

### M5.G9.T6: Append Architectural Scope Boundaries to Hygiene Test

**Objective:** Append rules to `tests/home/source-hygiene.test.ts` verifying that zero `'use client'` statements, zero API routes, zero server actions, zero forms, and zero tracking scripts exist in M5.

**Acceptance Criteria:**
- ✓ Asserts `'use client'` is completely absent in M5 files
- ✓ Asserts zero `route.ts` files exist under `src/`
- ✓ Asserts zero `'use server'` directives exist
- ✓ Asserts zero `<form`, `<input`, or `<textarea` exist in home components
- ✓ Asserts zero `document.cookie` or `localStorage` calls exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G9.T5 completed
- Target file: `tests/home/source-hygiene.test.ts`

**Implementation Details:**

Append architectural scope checks using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  it('enforces strict static architecture: zero client components, API routes, server actions, forms, or tracking', () => {
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

    // 2. Check M5 source files
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      expect(content.includes("'use client'"), `'use client' forbidden in ${filename}`).toBe(false);
      expect(content.includes("'use server'"), `'use server' forbidden in ${filename}`).toBe(false);
      expect(content.includes('next/headers'), `next/headers import forbidden in ${filename}`).toBe(false);
      expect(content.match(/\b(document\.cookie|localStorage)\b/), `Client persistence forbidden in ${filename}`).toBeNull();

      if (file.includes('components/home') || file.includes('components\\home')) {
        expect(content.match(/<(form|input|textarea)\b/g), `Form elements forbidden in ${filename}`).toBeNull();
      }
    }
  });
'@

$content = Get-Content "tests\home\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 16.3, Req 16.4

---

### M5.G9.T7: Append Schema & File Constraint Rules to Hygiene Test

**Objective:** Append checks to `tests/home/source-hygiene.test.ts` verifying zero schema redeclarations, zero hardcoded personal literals, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ Verifies `interface SiteConfig`, `interface Project`, `interface Certification`, `interface BlogPost` are NOT redeclared in M5
- ✓ Verifies zero personal data literals (`Angelo`, `Andres`, `hello@example.com`, `example.vercel.app`) in Home components
- ✓ Verifies every file in `src/components/home/` and `src/lib/home/` is strictly $< 300$ lines
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G9.T6 completed
- Target file: `tests/home/source-hygiene.test.ts`

**Implementation Details:**

Append schema and file constraints using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  it('enforces schema provenance, zero hardcoded personal literals, and 300-line limit', () => {
    const forbiddenLiterals = ['Angelo', 'Andres', 'hello@example.com', 'example.vercel.app'];

    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n').length;
      const filename = path.basename(file);

      // 300 lines limit
      expect(lines, `${filename} must be under 300 lines (current: ${lines})`).toBeLessThan(300);

      // Zero schema redeclarations
      expect(content.match(/(?:interface|type)\s+(?:SiteConfig|Project|Certification|BlogPost)\b/), `Content contracts must be imported, not redeclared in ${filename}`).toBeNull();

      // Zero hardcoded literals in component files
      if (file.includes('components/home') || file.includes('components\\home')) {
        for (const lit of forbiddenLiterals) {
          expect(content.includes(lit), `Hardcoded site literal '${lit}' forbidden in ${filename} (Req 2.5)`).toBe(false);
        }
      }
    }
  });
'@

$content = Get-Content "tests\home\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 2.5, Req 16.7, Req 16.8

---

### M5.G9.T8: Verify Protected Files Invariance via `git diff`

**Objective:** Execute `git diff` against the M4 baseline to verify that modifications are strictly confined to `src/app/page.tsx`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, and `tests/`.

**Acceptance Criteria:**
- ✓ `git diff src/components/ui/` produces zero output
- ✓ `git diff src/components/layout/` produces zero output
- ✓ `git diff src/content/` produces zero output
- ✓ `git diff tailwind.config.ts src/app/globals.css` produces zero output
- ✓ `git diff package.json` produces zero output
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G1 through M5.G8 completed

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diffProtected = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/content/ package.json
if ($diffProtected.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Protected files modified!`n$diffProtected"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.2, Req 16.4, Req 16.5

---

### M5.G9.T9: Document Manual Responsive & Keyboard Protocol in `task-notes.md`

**Objective:** Append the formal manual verification protocol (breakpoint inspection at 375px, 768px, 1024px, 1440px, tab sequence, and 200% zoom) into `task-notes.md`.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m5-homepage-experience/task-notes.md` updated
- ✓ Documents 375px mobile test: verify single-column stacking, zero horizontal overflow (`scrollWidth <= innerWidth`)
- ✓ Documents 768px tablet test: verify 2-column project and certification grids
- ✓ Documents 1024px desktop test: verify 3-column project and certification grids
- ✓ Documents 1440px wide desktop test: verify `Container` width capping
- ✓ Documents keyboard pass: verify tab order through hero, featured cards, and section links with visible focus rings

**Prerequisites:**
- `task-notes.md` exists

**Implementation Details:**

Append manual verification protocol to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$manualNotes = @'

## 3. Manual Responsive & Keyboard Verification Protocol (Req 14.4, 15.5, 16 manual)

1. **Responsive Viewport Inspection (375px to 1440px):**
   - **375px (Mobile):** Verify Hero CTA wraps cleanly, FeaturedProjects and CertificationsPreview render in a single column (`grid-cols-1`). Execute in console: `document.documentElement.scrollWidth <= window.innerWidth`. Expected: `true` (zero horizontal overflow).
   - **768px (Tablet):** FeaturedProjects and CertificationsPreview transition into 2-column grid (`md:grid-cols-2`). RecentActivity remains single column.
   - **1024px (Desktop):** FeaturedProjects and CertificationsPreview expand to 3-column grid (`lg:grid-cols-3`).
   - **1440px (Wide Desktop):** Verify all sections remain horizontally centered within the max width of `Container`.
2. **Keyboard Trapping & Tab Flow:**
   - Reload homepage at `/`.
   - Press `Tab` through SkipLink, header navigation, and enter HeroSection.
   - Confirm visible focus ring on "View Projects" primary button.
   - Confirm focus lands cleanly on secondary contact link (if present).
   - Tab through Featured project title links. Confirm each card link receives visible focus.
   - Tab through "View all projects", "View all certifications", and "View all posts" links. Zero keyboard trapping.
3. **200% Text Scaling (WCAG 2.1 AA 1.4.4):**
   - At 1024px width, increase browser zoom to 200%.
   - Verify HeroSection buttons wrap without clipping or overlapping.
   - Verify card text wraps naturally without horizontal container blowouts.
'@

Add-Content -Path ".kiro\specs\m5-homepage-experience\task-notes.md" -Value $manualNotes -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m5-homepage-experience\task-notes.md" -Raw
if ($notes -match "Manual Responsive & Keyboard Verification Protocol") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.4, Req 15.5

---

### M5.G9.T10: Checkpoint — Responsive, Accessibility, and Hygiene Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across accessibility matrix and source hygiene suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all axe and hygiene tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G9.T1 through M5.G9.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/a11y.test.tsx tests/home/source-hygiene.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/a11y.test.tsx tests/home/source-hygiene.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\home\a11y.test.tsx"
Test-Path "tests\home\source-hygiene.test.ts"
npm run typecheck
npm run test -- tests/home/a11y.test.tsx tests/home/source-hygiene.test.ts
```
Expected output:
- `True` for both paths
- `npm run typecheck` exits with return code 0
- Vitest executes all accessibility and hygiene tests with code 0.