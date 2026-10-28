# M6.G9: Responsive, Token, and Scope Compliance; Accessibility and Keyboard Matrix; Source Hygiene

> **Milestone:** M6 — Projects Module  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute an exhaustive responsive layout audit, design-token compliance verification, WCAG 2.1 AA automated accessibility evaluation, keyboard interaction pass, and strict static source-hygiene scan across all Milestone 6 components (`ProjectCard`, `ProjectGrid`, `ProjectFilterBar`, `ProjectsExplorer`, `ProjectsIndex`, `ProjectBreadcrumb`, `ProjectHeader`, `ProjectMetadata`, `ProjectLinks`, `BuildDocumentation`, `RelatedProjects`, and route files `src/app/projects/page.tsx` and `src/app/projects/[slug]/page.tsx`). Ensure all pages and card grids apply standard Tailwind responsive utilities (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`), that filter chips wrap on mobile without horizontal scrolling (`flex-wrap`), and that detail content widths are bounded by M3's `Container` primitive. Execute automated axe accessibility checks across both routes in all operational states (index default, index filtered, index empty, detail populated, and detail minimal) with zero permissible violations. Enforce strict keyboard operability verifying that Tab navigation reaches every chip and action, Enter and Space activate controls, and "Clear filters" returns focus to the first chip. Run static source-hygiene scans verifying zero raw hex colors, zero arbitrary Tailwind brackets, zero `dark:` utilities, zero `'use client'` statements outside `projects-explorer.tsx`, zero `useSearchParams` outside the Explorer, zero redeclared content types, zero hardcoded personal literals, zero API routes or server actions, zero forms or cookies, and file lengths strictly under 300 lines. Document the manual verification checklist in `task-notes.md`.

## Goal Success Criteria

- ✓ All M6 pages and sections compose M3's `Container` primitive for width constraint and horizontal padding
- ✓ `ProjectGrid` and `RelatedProjects` apply responsive column classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ `ProjectFilterBar` chips wrap onto multiple lines at mobile viewports via `flex-wrap` (Req 16.4)
- ✓ Confirms M3's `FOCUS_RING` is applied to every interactive link and button, and motion helpers respect `prefers-reduced-motion`
- ✓ `tests/projects/a11y.test.tsx` executes automated axe checks for both routes across all states (index default, filtered, empty; detail full, minimal) with 0 violations
- ✓ `tests/projects/keyboard.test.tsx` verifies full keyboard operation: Tab sequence, Enter/Space activation, and focus restoration to first chip upon clearing filters (Req 6.8, 6.9, 8.6)
- ✓ `tests/projects/source-hygiene.test.ts` scans all M6 files for repository guardrail compliance with 100% pass rate
- ✓ `git diff` confirms changes are strictly confined to `src/app/projects/`, `src/components/projects/`, `src/lib/projects/`, and `tests/`
- ✓ Manual responsive, touch-target ($\ge 44\text{px}$), and keyboard verification protocol documented in `task-notes.md`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 through M6.G8 completed (all components, helpers, and routes operational)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `vitest-axe` and `@testing-library/user-event` installed in `devDependencies`

---

## Tasks

### M6.G9.T1: Audit Breakpoint Utilities and Absence of Arbitrary Dimension Classes

**Objective:** Inspect all files in `src/components/projects/`, `src/app/projects/`, and `src/app/projects/[slug]/` ensuring responsive layout relies strictly on standard Tailwind breakpoints (`md:`, `lg:`) and contains zero arbitrary dimension brackets `[` or `]`.

**Acceptance Criteria:**
- ✓ Scans all M6 components and route files
- ✓ Confirms card grids apply `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Confirms filter bar applies `flex-wrap`
- ✓ Confirms zero occurrences of arbitrary dimension utilities (`w-[`, `min-w-[`, `h-[`, `min-h-[`, `p-[`, `px-[`, `py-[`, `gap-[`)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M6.G4 through M6.G8 completed

**Implementation Details:**

Execute breakpoint audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$targetDirs = @("src\components\projects", "src\app\projects")
$files = Get-ChildItem -Path "src\components\projects" -Include *.ts, *.tsx -Recurse
$files += Get-Item "src\app\projects\page.tsx"
$files += Get-Item "src\app\projects\[slug]\page.tsx"

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
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$targetDirs = @("src\components\projects", "src\app\projects")
$files = Get-ChildItem -Path "src\components\projects" -Include *.ts, *.tsx -Recurse
$files += Get-Item "src\app\projects\page.tsx"
$files += Get-Item "src\app\projects\[slug]\page.tsx"

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

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.2, Req 16.3, Req 16.4

---

### M6.G9.T2: Verify Client Boundaries & Framework Invariance in M6

**Objective:** Audit all M6 components and helpers to verify that `ProjectsExplorer` is the ONLY client component, the ONLY caller of `useSearchParams`, and that no browser globals or dynamic hooks exist elsewhere.

**Acceptance Criteria:**
- ✓ Scans all files in `src/components/projects/`, `src/lib/projects/`, and `src/app/projects/`
- ✓ Confirms `'use client'` appears in exactly one file: `projects-explorer.tsx` (Req 7.3)
- ✓ Confirms `useSearchParams` is called only in `projects-explorer.tsx`
- ✓ Confirms zero imports of `useState`, `useEffect`, or `matchMedia` outside `projects-explorer.tsx`
- ✓ Confirms zero occurrences of `window`, `document`, or `fetch(`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M6.G1 through M6.G8 completed

**Implementation Details:**

Execute client boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$allM6Files = Get-ChildItem -Path "src\components\projects", "src\lib\projects", "src\app\projects" -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($file in $allM6Files) {
    $content = Get-Content $file.FullName -Raw
    $isExplorer = $file.Name -eq "projects-explorer.tsx"

    if ($content -match "['""]use client['""]" -and -not $isExplorer) {
        $violations += "Forbidden 'use client' found in $($file.Name) (Explorer is only client module)"
    }
    if ($content -match "\buseSearchParams\b" -and -not $isExplorer) {
        $violations += "Forbidden useSearchParams call in $($file.Name)"
    }
    if ($content -match "\b(useState|useEffect|useReducer|matchMedia)\b" -and -not $isExplorer) {
        $violations += "Forbidden client hook in $($file.Name)"
    }
    if ($content -match "\b(window|document|fetch)\b") {
        $violations += "Forbidden browser global in $($file.Name)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$allM6Files = Get-ChildItem -Path "src\components\projects", "src\lib\projects", "src\app\projects" -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($file in $allM6Files) {
    $content = Get-Content $file.FullName -Raw
    $isExplorer = $file.Name -eq "projects-explorer.tsx"

    if ($content -match "['""]use client['""]" -and -not $isExplorer) {
        $violations += "Forbidden 'use client' found in $($file.Name) (Explorer is only client module)"
    }
    if ($content -match "\buseSearchParams\b" -and -not $isExplorer) {
        $violations += "Forbidden useSearchParams call in $($file.Name)"
    }
    if ($content -match "\b(useState|useEffect|useReducer|matchMedia)\b" -and -not $isExplorer) {
        $violations += "Forbidden client hook in $($file.Name)"
    }
    if ($content -match "\b(window|document|fetch)\b") {
        $violations += "Forbidden browser global in $($file.Name)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.3, Req 9.1, Req 17.3

---

### M6.G9.T3: Verify Composition of M3 UI Primitives & Focus Ring Helpers

**Objective:** Perform static analysis across M6 components to confirm mandatory composition of M3 primitives (`Container`, `Card`, `TagList`, `StatusBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Button`, `FOCUS_RING`) without local redefinition.

**Acceptance Criteria:**
- ✓ Confirms `Container` wraps `ProjectsIndex` and `ProjectDetailPage`
- ✓ Confirms `FOCUS_RING` is applied to all interactive links, chips, and buttons
- ✓ Confirms `ExternalLink` is used for all external destinations (zero raw `<a target="_blank">`)
- ✓ Confirms motion classes include `MOTION_FAST` (carrying `motion-reduce:transition-none`)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M6.G4 through M6.G8 completed

**Implementation Details:**

Execute primitive composition audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$componentFiles = Get-ChildItem -Path "src\components\projects", "src\app\projects" -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($f in $componentFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match '<a\b[^>]*\btarget\s*=\s*["'']_blank["'']') {
        $violations += "Raw <a target='_blank'> found in $($f.Name). Must use ExternalLink primitive (Req 12.6)"
    }
}

$pageFiles = @("src\components\projects\projects-index.tsx", "src\app\projects\[slug]\page.tsx")
foreach ($pf in $pageFiles) {
    $content = Get-Content $pf -Raw
    if (-not ($content -match '\bContainer\b')) {
        $violations += "$pf must import and render Container primitive (Req 15.1, 16.3)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$componentFiles = Get-ChildItem -Path "src\components\projects", "src\app\projects" -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($f in $componentFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match '<a\b[^>]*\btarget\s*=\s*["'']_blank["'']') {
        $violations += "Raw <a target='_blank'> found in $($f.Name). Must use ExternalLink primitive (Req 12.6)"
    }
}

$pageFiles = @("src\components\projects\projects-index.tsx", "src\app\projects\[slug]\page.tsx")
foreach ($pf in $pageFiles) {
    $content = Get-Content $pf -Raw
    if (-not ($content -match '\bContainer\b')) {
        $violations += "$pf must import and render Container primitive (Req 15.1, 16.3)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 12.6, Req 15.1, Req 16.1, Req 16.3, Req 16.8, Req 17.7

---

### M6.G9.T4: Author Automated Axe Accessibility Tests for Projects Index (`tests/projects/a11y-index.test.tsx`)

**Objective:** Create `tests/projects/a11y-index.test.tsx` executing automated axe accessibility tests on `ProjectsIndex` under default, filtered, and empty states with zero violations.

**Acceptance Criteria:**
- ✓ File `tests/projects/a11y-index.test.tsx` created
- ✓ Evaluates default `ProjectsIndex` (full collection): 0 axe violations
- ✓ Evaluates filtered `ProjectsExplorer` (technology active): 0 axe violations
- ✓ Evaluates empty-filtered `ProjectsExplorer` (zero matches): 0 axe violations
- ✓ Evaluates empty `ProjectsIndex` (zero projects in repo): 0 axe violations
- ✓ Evaluates against WCAG 2.1 Level AA standards
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G5 completed
- Target file: `tests/projects/a11y-index.test.tsx`

**Implementation Details:**

Write `tests/projects/a11y-index.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { ProjectsIndex } from '@/components/projects/projects-index';
import { ProjectsExplorer } from '@/components/projects/projects-explorer';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';
import { setInitialQuery, mockUseRouter, mockUseSearchParams } from './helpers/mock-navigation';

vi.mock('next/navigation', () => ({
  useRouter: () => mockUseRouter(),
  useSearchParams: () => mockUseSearchParams(),
}));

describe('Projects Index Axe Accessibility Matrix (Req 16.6)', () => {
  const cards = sampleProjectsList.map(toProjectCardData);

  it('reports zero axe violations for default ProjectsIndex', async () => {
    setInitialQuery('');
    const { container } = render(<ProjectsIndex projects={cards} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for filtered ProjectsExplorer', async () => {
    setInitialQuery('technology=TypeScript');
    const { container } = render(<ProjectsExplorer projects={cards} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for empty-filtered ProjectsExplorer', async () => {
    setInitialQuery('technology=TypeScript&status=archived'); // 0 matches
    const { container } = render(<ProjectsExplorer projects={cards} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for empty ProjectsIndex', async () => {
    const { container } = render(<ProjectsIndex projects={[]} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@ | Set-Content "tests\projects\a11y-index.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/a11y-index.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M6.G9.T5: Author Automated Axe Accessibility Tests for Project Detail Page (`tests/projects/a11y-detail.test.tsx`)

**Objective:** Create `tests/projects/a11y-detail.test.tsx` executing automated axe accessibility tests on `ProjectDetailPage` across fully populated and minimal configurations with zero violations.

**Acceptance Criteria:**
- ✓ File `tests/projects/a11y-detail.test.tsx` created
- ✓ Mocks loaders returning full project (with links, tags, metrics, and related projects)
- ✓ Evaluates full `ProjectDetailPage`: 0 axe violations
- ✓ Mocks loaders returning minimal project (no links, empty tags, empty metrics, no related projects)
- ✓ Evaluates minimal `ProjectDetailPage`: 0 axe violations
- ✓ Evaluates against WCAG 2.1 Level AA standards
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G8 completed
- Target file: `tests/projects/a11y-detail.test.tsx`

**Implementation Details:**

Write `tests/projects/a11y-detail.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import ProjectDetailPage from '@/app/projects/[slug]/page';
import {
  sampleProjectsList,
  noLinksProject,
  emptyTagsMetricsProject,
  isolatedTechProject,
} from '../fixtures/projects-data';
import { sampleSiteConfig } from '../fixtures/home-data';

vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
  getProjectBySlug: vi.fn(),
}));
vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(),
}));
vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(),
}));

describe('Project Detail Axe Accessibility Matrix (Req 16.6)', () => {
  beforeEach(async () => {
    const { getProjects } = await import('@/content/loaders/projects');
    const { getSiteConfig } = await import('@/content/loaders/site');
    const { renderMarkdown } = await import('@/content/markdown/renderer');

    vi.mocked(getProjects).mockResolvedValue(sampleProjectsList);
    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);
    vi.mocked(renderMarkdown).mockResolvedValue('<h2>Architecture</h2><p>Notes</p>');
  });

  it('reports zero axe violations for fully populated ProjectDetailPage', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    vi.mocked(getProjectBySlug).mockResolvedValue(sampleProjectsList[0]);

    const Page = await ProjectDetailPage({
      params: Promise.resolve({ slug: 'alpha-pipeline-core' }),
    });
    const { container } = render(Page);

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it('reports zero axe violations for minimal ProjectDetailPage (no links, empty tags/metrics/related)', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    const minimalProject = {
      ...noLinksProject,
      ...emptyTagsMetricsProject,
      ...isolatedTechProject,
    };
    vi.mocked(getProjectBySlug).mockResolvedValue(minimalProject);

    const Page = await ProjectDetailPage({
      params: Promise.resolve({ slug: minimalProject.slug }),
    });
    const { container } = render(Page);

    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
});
'@ | Set-Content "tests\projects\a11y-detail.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/a11y-detail.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M6.G9.T6: Author Comprehensive Keyboard Interaction Tests (`tests/projects/keyboard.test.tsx`)

**Objective:** Create `tests/projects/keyboard.test.tsx` verifying full keyboard accessibility: Tab sequence, Enter/Space activation, and focus restoration to first chip upon clearing filters.

**Acceptance Criteria:**
- ✓ File `tests/projects/keyboard.test.tsx` created
- ✓ Tests Tab key reaches every technology chip, status chip, and "Clear filters" button in document order
- ✓ Tests Enter and Space keys toggle chip activation
- ✓ Tests activating "Clear filters" in filter bar moves focus to first chip (Req 6.8)
- ✓ Tests activating "Clear filters" in empty state moves focus to first chip (Req 8.6)
- ✓ Uses `@testing-library/user-event`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G5 completed
- Target file: `tests/projects/keyboard.test.tsx`

**Implementation Details:**

Write `tests/projects/keyboard.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectsExplorer } from '@/components/projects/projects-explorer';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';
import { setInitialQuery, mockUseRouter, mockUseSearchParams } from './helpers/mock-navigation';

vi.mock('next/navigation', () => ({
  useRouter: () => mockUseRouter(),
  useSearchParams: () => mockUseSearchParams(),
}));

describe('Projects Keyboard Interaction Protocol (Req 6.8, 6.9, 8.6)', () => {
  const cards = sampleProjectsList.map(toProjectCardData);

  beforeEach(() => {
    setInitialQuery('');
  });

  it('allows full keyboard traversal and activation via Tab, Enter, and Space', async () => {
    const user = userEvent.setup();
    render(<ProjectsExplorer projects={cards} />);

    // 1. Tab to first technology chip (Docker)
    await user.tab();
    const firstChip = screen.getByRole('button', { name: 'Docker' });
    expect(firstChip).toHaveFocus();

    // 2. Activate via Enter
    await user.keyboard('{Enter}');
    expect(firstChip.getAttribute('aria-pressed')).toBe('true');

    // 3. Tab through remaining chips and activate Go via Space
    await user.tab(); // Go
    const goChip = screen.getByRole('button', { name: 'Go' });
    expect(goChip).toHaveFocus();
    await user.keyboard(' ');
    expect(goChip.getAttribute('aria-pressed')).toBe('true');
  });

  it('restores keyboard focus to first chip after activating Clear filters in filter bar', async () => {
    const user = userEvent.setup();
    setInitialQuery('technology=Docker');
    render(<ProjectsExplorer projects={cards} />);

    const clearBtn = screen.getByRole('button', { name: 'Clear filters' });
    clearBtn.focus();
    expect(clearBtn).toHaveFocus();

    await user.keyboard('{Enter}');

    const firstChip = screen.getByRole('button', { name: 'Docker' });
    expect(firstChip).toHaveFocus();
  });

  it('restores keyboard focus to first chip after activating Clear filters in EmptyState', async () => {
    const user = userEvent.setup();
    setInitialQuery('technology=Docker&status=archived'); // 0 matches
    render(<ProjectsExplorer projects={cards} />);

    const emptyClearBtn = screen.getByRole('button', { name: 'Clear filters' });
    emptyClearBtn.focus();
    expect(emptyClearBtn).toHaveFocus();

    await user.keyboard('{Enter}');

    const firstChip = screen.getByRole('button', { name: 'Docker' });
    expect(firstChip).toHaveFocus();
  });
});
'@ | Set-Content "tests\projects\keyboard.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/keyboard.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.8, Req 6.9, Req 8.6, Req 16.5, Req 17.1

---

### M6.G9.T7: Author Source Hygiene Static Analysis Suite (`tests/projects/source-hygiene.test.ts`)

**Objective:** Create `tests/projects/source-hygiene.test.ts` scanning all M6 files for token compliance, zero raw colors, zero arbitrary brackets, zero `dark:` classes, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ File `tests/projects/source-hygiene.test.ts` created
- ✓ Scans all `.ts` and `.tsx` files in `src/components/projects/`, `src/lib/projects/`, and `src/app/projects/`
- ✓ Fails on raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Fails on raw `rgb(`/`rgba(`
- ✓ Fails on arbitrary Tailwind brackets (`w-[`, `h-[`, `px-[`, etc.)
- ✓ Fails on `dark:` utilities
- ✓ Fails on any file exceeding 300 lines
- ✓ Tests pass under `npm test`

**Prerequisites:**
- Target file: `tests/projects/source-hygiene.test.ts`

**Implementation Details:**

Write the source-hygiene suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Projects Module Source Hygiene & Token Compliance (Req 16, 17)', () => {
  const compDir = path.join(process.cwd(), 'src', 'components', 'projects');
  const libDir = path.join(process.cwd(), 'src', 'lib', 'projects');
  const appDir = path.join(process.cwd(), 'src', 'app', 'projects');

  const getFiles = (dir: string): string[] => {
    let results: string[] = [];
    const list = fs.readdirSync(dir);
    for (const item of list) {
      const full = path.join(dir, item);
      const stat = fs.statSync(full);
      if (stat.isDirectory()) {
        results = results.concat(getFiles(full));
      } else if (item.endsWith('.ts') || item.endsWith('.tsx')) {
        results.push(full);
      }
    }
    return results;
  };

  const allFiles = [...getFiles(compDir), ...getFiles(libDir), ...getFiles(appDir)];

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

  it('strictly enforces the 300-line limit across all M6 files', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n').length;
      const filename = path.basename(file);
      expect(lines, `${filename} must be under 300 lines (current: ${lines})`).toBeLessThan(300);
    }
  });
});
'@ | Set-Content "tests\projects\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.1, Req 17.3, Req 17.4

---

### M6.G9.T8: Append Architectural Scope Boundaries to Hygiene Test

**Objective:** Append checks to `tests/projects/source-hygiene.test.ts` verifying zero API routes, zero server actions, zero forms, zero client persistence, zero schema redeclarations, zero client directives outside `projects-explorer.tsx`, and zero JSON-LD.

**Acceptance Criteria:**
- ✓ Fails if any `route.ts` file exists under `src/`
- ✓ Fails if `'use server'` appears in any file
- ✓ Fails if `'use client'` appears in any file other than `projects-explorer.tsx`
- ✓ Fails if `useSearchParams` appears outside `projects-explorer.tsx`
- ✓ Fails if `<form`, `<input`, or `<textarea` appear
- ✓ Fails if `document.cookie` or `localStorage` appear
- ✓ Fails if `interface Project` or `type ProjectFilters` are redeclared
- ✓ Fails if `application/ld+json` appears
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G9.T7 completed
- Target file: `tests/projects/source-hygiene.test.ts`

**Implementation Details:**

Append architectural scope checks using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  it('enforces architectural scope boundaries: zero extra client components, API routes, forms, or tracking', () => {
    // 1. Zero API routes in project
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

    // 2. Scan M6 files
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);
      const isExplorer = filename === 'projects-explorer.tsx';

      if (!isExplorer) {
        expect(content.includes("'use client'"), `'use client' forbidden in ${filename}`).toBe(false);
        expect(content.includes('useSearchParams'), `useSearchParams forbidden in ${filename}`).toBe(false);
      }

      expect(content.includes("'use server'"), `'use server' forbidden in ${filename}`).toBe(false);
      expect(content.includes('next/headers'), `next/headers forbidden in ${filename}`).toBe(false);
      expect(content.match(/\b(document\.cookie|localStorage)\b/), `Client persistence forbidden in ${filename}`).toBeNull();
      expect(content.includes('application/ld+json'), `JSON-LD structured data forbidden in ${filename} (Req 15.7)`).toBe(false);

      if (file.includes('components/projects') || file.includes('components\\projects')) {
        expect(content.match(/<(form|input|textarea)\b/g), `Form elements forbidden in ${filename}`).toBeNull();
      }

      // Zero schema redeclarations
      expect(
        content.match(/(?:interface|type)\s+(?:Project|ProjectFrontmatter|ProjectStatus|ProjectFilters)\b/),
        `Content contract redeclared in ${filename}. Must import from @/types/content (Req 1.5)`
      ).toBeNull();
    }
  });
'@

$content = Get-Content "tests\projects\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 7.3, Req 15.7, Req 17.3, Req 17.6, Req 17.8

---

### M6.G9.T9: Verify Protected Files Invariance and Record Manual Verification Protocol

**Objective:** Execute `git diff` against the M5 baseline to verify that modifications are strictly confined to `src/app/projects/`, `src/components/projects/`, `src/lib/projects/`, and `tests/projects/`, and document the manual responsive/keyboard verification checklist in `task-notes.md`.

**Acceptance Criteria:**
- ✓ `git diff` on `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, `src/content/`, `tailwind.config.ts`, `globals.css`, and `package.json` produces zero output
- ✓ Appends manual verification protocol to `.kiro/specs/m6-projects-module/task-notes.md`
- ✓ Documents 375px mobile inspection (overflow verification, chip wrapping, touch targets $\ge 44\text{px}$)
- ✓ Documents 768px tablet and 1024px desktop grid inspection
- ✓ Documents keyboard tab order through index and detail routes
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G9.T1 through M6.G8 completed

**Implementation Details:**

Execute diff check and append notes using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diffProtected = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json
if ($diffProtected.Length -gt 0) {
    Write-Error "CRITICAL: Upstream protected files modified!`n$diffProtected"
    exit 1
}

$manualNotes = @'

## 4. Manual Responsive, Touch Target & Keyboard Verification Protocol (Req 16.2-16.5)

1. **Responsive Viewport Inspection (375px to 1440px):**
   - **375px (Mobile):** Navigate to `/projects`. Confirm `ProjectFilterBar` chips wrap cleanly onto multiple rows via `flex-wrap`. Card grid renders 1 column (`grid-cols-1`). Execute in console: `document.documentElement.scrollWidth <= window.innerWidth`. Expected: `true` (zero horizontal overflow).
   - **375px Detail Page:** Navigate to `/projects/alpha-pipeline-core`. Confirm breadcrumb truncates cleanly, header tags wrap, and code blocks scroll horizontally without forcing page overflow.
   - **768px (Tablet):** Card grids transition into 2 columns (`md:grid-cols-2`).
   - **1024px+ (Desktop):** Card grids expand to 3 columns (`lg:grid-cols-3`). Content width is bounded by `Container`.
2. **Touch Target Size Compliance (WCAG 2.1 AA 2.5.5):**
   - Inspect FilterChips: verify computed height is at least 44px (including padding).
   - Inspect Card title links and breadcrumb links: verify tap area meets accessible dimensions.
3. **Keyboard Trapping & Tab Flow:**
   - On `/projects`: press `Tab` through skip link, header navigation, and enter `ProjectFilterBar`.
   - Confirm visible focus indicator (`FOCUS_RING`) on every technology chip and status chip.
   - Press `Enter` to select a technology filter. Confirm `ProjectGrid` filters instantly and polite live region updates text.
   - Tab to "Clear filters" button and press `Enter`. Confirm focus returns immediately to the first chip in the filter bar.
   - On detail page: tab through breadcrumb, external links, and back link. Confirm visible focus indicators.
'@

Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $manualNotes -Encoding UTF8
"PASS"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diffProtected = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json
if ($diffProtected.Length -gt 0) {
    Write-Error "CRITICAL: Upstream protected files modified!`n$diffProtected"
    exit 1
}

$manualNotes = @'

## 4. Manual Responsive, Touch Target & Keyboard Verification Protocol (Req 16.2-16.5)

1. **Responsive Viewport Inspection (375px to 1440px):**
   - **375px (Mobile):** Navigate to `/projects`. Confirm `ProjectFilterBar` chips wrap cleanly onto multiple rows via `flex-wrap`. Card grid renders 1 column (`grid-cols-1`). Execute in console: `document.documentElement.scrollWidth <= window.innerWidth`. Expected: `true` (zero horizontal overflow).
   - **375px Detail Page:** Navigate to `/projects/alpha-pipeline-core`. Confirm breadcrumb truncates cleanly, header tags wrap, and code blocks scroll horizontally without forcing page overflow.
   - **768px (Tablet):** Card grids transition into 2 columns (`md:grid-cols-2`).
   - **1024px+ (Desktop):** Card grids expand to 3 columns (`lg:grid-cols-3`). Content width is bounded by `Container`.
2. **Touch Target Size Compliance (WCAG 2.1 AA 2.5.5):**
   - Inspect FilterChips: verify computed height is at least 44px (including padding).
   - Inspect Card title links and breadcrumb links: verify tap area meets accessible dimensions.
3. **Keyboard Trapping & Tab Flow:**
   - On `/projects`: press `Tab` through skip link, header navigation, and enter `ProjectFilterBar`.
   - Confirm visible focus indicator (`FOCUS_RING`) on every technology chip and status chip.
   - Press `Enter` to select a technology filter. Confirm `ProjectGrid` filters instantly and polite live region updates text.
   - Tab to "Clear filters" button and press `Enter`. Confirm focus returns immediately to the first chip in the filter bar.
   - On detail page: tab through breadcrumb, external links, and back link. Confirm visible focus indicators.
'@

Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $manualNotes -Encoding UTF8
"PASS"
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 16.2, Req 16.3, Req 16.4, Req 16.5, Req 17.7

---

### M6.G9.T10: Checkpoint — Compliance, Accessibility, and Hygiene Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across compliance, accessibility, and hygiene suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all axe, keyboard, and hygiene test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G9.T1 through M6.G9.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/a11y-index.test.tsx tests/projects/a11y-detail.test.tsx tests/projects/keyboard.test.tsx tests/projects/source-hygiene.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/a11y-index.test.tsx tests/projects/a11y-detail.test.tsx tests/projects/keyboard.test.tsx tests/projects/source-hygiene.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1, Req 17.4, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\projects\a11y-index.test.tsx"
Test-Path "tests\projects\a11y-detail.test.tsx"
Test-Path "tests\projects\keyboard.test.tsx"
Test-Path "tests\projects\source-hygiene.test.ts"
npm run typecheck
npm run test -- tests/projects/a11y-index.test.tsx tests/projects/a11y-detail.test.tsx tests/projects/keyboard.test.tsx tests/projects/source-hygiene.test.ts
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all accessibility, keyboard, and hygiene tests with code 0.