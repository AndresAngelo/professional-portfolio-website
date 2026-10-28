# M6.G7: BuildDocumentation and RelatedProjects

> **Milestone:** M6 — Projects Module  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complex case-study content sections for the Project Detail page (`SCR-03`): `BuildDocumentation` in `src/components/projects/build-documentation.tsx` and `RelatedProjects` in `src/components/projects/related-projects.tsx`. `BuildDocumentation` wraps already-rendered, sanitized Markdown documentation in an accessible section landmark (`<section aria-labelledby="build-docs-heading">`) preceded by an `<h2 id="build-docs-heading">` titled "Build documentation". It pipes the HTML through `demoteHeadings` to guarantee that any `<h1>` inside the documentation is demoted, preventing heading level collisions with the page's primary title, while passing the resulting HTML to M3's `MarkdownDoc` primitive without re-sanitizing or introducing raw HTML bypasses. `RelatedProjects` accepts an array of `ProjectCardData` (resolved by `selectRelatedProjects`); if the array is non-empty, it renders an `<section aria-labelledby="related-projects-heading">` with an `<h2 id="related-projects-heading">` titled "Related projects" and renders the cards using `ProjectCard` configured with `headingLevel={3}` in a responsive CSS grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`). If the related projects array is empty, it returns `null`, omitting the section and heading entirely. Ensure both components are pure server-safe components without `'use client'`, using Semantic_Tokens exclusively, with file lengths under 300 lines. Validate rendering, heading hierarchy integration, responsive styling, and accessibility using Vitest, RTL, and axe.

## Goal Success Criteria

- ✓ `src/components/projects/build-documentation.tsx` renders `<section aria-labelledby="build-docs-heading">` with `<h2 id="build-docs-heading">Build documentation</h2>`
- ✓ `BuildDocumentation` applies `demoteHeadings` to input HTML, rendering documentation headings starting at `<h2>` or lower, leaving no `<h1>` inside documentation (Req 13.3, 13.4)
- ✓ `BuildDocumentation` delegates rendering to M3's `MarkdownDoc` primitive and adds zero raw-HTML paths (Req 13.1, 13.5)
- ✓ `src/components/projects/related-projects.tsx` renders `<section aria-labelledby="related-projects-heading">` with `<h2 id="related-projects-heading">Related projects</h2>`
- ✓ `RelatedProjects` renders cards in given order with `headingLevel={3}` inside a responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)
- ✓ When `projects.length === 0`, `RelatedProjects` returns `null` (renders zero elements, including heading, per Req 14.7)
- ✓ Both components run as server components without `'use client'` statements and use Semantic_Tokens exclusively
- ✓ Unit, heading hierarchy, and axe accessibility tests in `tests/projects/build-documentation.test.tsx` and `related-projects.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 through M6.G6 completed (`demoteHeadings`, `ProjectCard`, and `projects-text.ts` available)
- M3 primitives (`MarkdownDoc`, `Container`, `Card`) available in `src/components/ui/`
- Target files: `src/components/projects/build-documentation.tsx` and `src/components/projects/related-projects.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G7.T1: Implement `BuildDocumentation` Component (`src/components/projects/build-documentation.tsx`)

**Objective:** Author the server component `BuildDocumentation` in `src/components/projects/build-documentation.tsx` rendering the section landmark, `<h2>` heading, and `MarkdownDoc` primitive with demoted headings.

**Acceptance Criteria:**
- ✓ File `src/components/projects/build-documentation.tsx` created
- ✓ Exports `interface BuildDocumentationProps { readonly html: string; }`
- ✓ Exports `BuildDocumentation({ html }: BuildDocumentationProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="build-docs-heading" className="mb-12">`
- ✓ Renders `<h2 id="build-docs-heading" className="text-heading-2 font-bold tracking-tight text-text-primary mb-6">{PROJECTS_TEXT.buildDocsHeading}</h2>`
- ✓ Applies `demoteHeadings(html)` and passes resulting string to M3 `<MarkdownDoc html={safeHtml} />`
- ✓ Relies on upstream M2 sanitization; introduces zero custom `dangerouslySetInnerHTML` bypasses (Req 13.5)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- M6.G3 completed (`demoteHeadings` in `src/lib/projects/demote-headings.ts`)
- M3 `MarkdownDoc` available in `src/components/ui/markdown-doc.tsx`
- Target file: `src/components/projects/build-documentation.tsx`

**Implementation Details:**

Write `src/components/projects/build-documentation.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { MarkdownDoc } from '@/components/ui/markdown-doc';
import { PROJECTS_TEXT } from './projects-text';
import { demoteHeadings } from '@/lib/projects/demote-headings';

export interface BuildDocumentationProps {
  readonly html: string;
}

/**
 * BuildDocumentation Section Component
 *
 * Renders verified technical case-study documentation Markdown.
 * Demotes any inner h1 tags to guarantee single page h1 hierarchy (Req 13.1-13.6).
 * Server component by default (Req 9.1).
 */
export function BuildDocumentation({ html }: BuildDocumentationProps): JSX.Element {
  const safeHtml = demoteHeadings(html);

  return (
    <section aria-labelledby="build-docs-heading" className="mb-12">
      <h2
        id="build-docs-heading"
        className="text-heading-2 font-bold tracking-tight text-text-primary mb-6"
      >
        {PROJECTS_TEXT.buildDocsHeading}
      </h2>

      <MarkdownDoc html={safeHtml} />
    </section>
  );
}
'@ | Set-Content "src\components\projects\build-documentation.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/build-documentation.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 13.5, Req 13.6, Req 16.7

---

### M6.G7.T2: Implement `RelatedProjects` Component (`src/components/projects/related-projects.tsx`)

**Objective:** Author the server component `RelatedProjects` in `src/components/projects/related-projects.tsx` rendering related project cards at heading level 3, returning `null` when the list is empty.

**Acceptance Criteria:**
- ✓ File `src/components/projects/related-projects.tsx` created
- ✓ Exports `interface RelatedProjectsProps { readonly projects: readonly ProjectCardData[]; }`
- ✓ Exports `RelatedProjects({ projects }: RelatedProjectsProps): JSX.Element | null`
- ✓ If `projects.length === 0`: returns `null` (renders zero elements, including heading, per Req 14.7)
- ✓ If `projects.length > 0`: renders `<section aria-labelledby="related-projects-heading" className="mt-16 pt-12 border-t border-border-default">`
- ✓ Renders `<h2 id="related-projects-heading" className="text-heading-2 font-bold tracking-tight text-text-primary mb-8">{PROJECTS_TEXT.relatedHeading}</h2>`
- ✓ Renders `<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">`
- ✓ Renders one `ProjectCard` per project with `headingLevel={3}` to prevent heading level jumps (Req 14.6, 16.7)
- ✓ Preserves exact input array order
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`, `ProjectCardData` in `card-data.ts`)
- M6.G4 completed (`ProjectCard` in `src/components/projects/project-card.tsx`)
- Target file: `src/components/projects/related-projects.tsx`

**Implementation Details:**

Write `src/components/projects/related-projects.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { ProjectCard } from './project-card';
import { PROJECTS_TEXT } from './projects-text';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface RelatedProjectsProps {
  readonly projects: readonly ProjectCardData[];
}

/**
 * RelatedProjects Section Component
 *
 * Displays up to 3 similar projects sharing technologies with current case study.
 * Configures ProjectCard with headingLevel=3 under the section h2 (Req 14.6, 14.7, 16.7).
 * Server component by default (Req 9.1).
 */
export function RelatedProjects({ projects }: RelatedProjectsProps): JSX.Element | null {
  if (!projects || projects.length === 0) {
    return null; // Omit completely per Req 14.7
  }

  return (
    <section
      aria-labelledby="related-projects-heading"
      className="mt-16 pt-12 border-t border-border-default"
    >
      <h2
        id="related-projects-heading"
        className="text-heading-2 font-bold tracking-tight text-text-primary mb-8"
      >
        {PROJECTS_TEXT.relatedHeading}
      </h2>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <div key={project.slug} className="flex flex-col">
            <ProjectCard project={project} headingLevel={3} />
          </div>
        ))}
      </div>
    </section>
  );
}
'@ | Set-Content "src\components\projects\related-projects.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/related-projects.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.6, Req 14.7, Req 16.2, Req 16.7, Req 17.3

---

### M6.G7.T3: Author Unit Tests for `BuildDocumentation` (`tests/projects/build-documentation.test.tsx`)

**Objective:** Create `tests/projects/build-documentation.test.tsx` verifying section labelling, heading demotion integration, and omission of script tags.

**Acceptance Criteria:**
- ✓ File `tests/projects/build-documentation.test.tsx` created
- ✓ Tests `<section>` is labelled by `h2#build-docs-heading` titled "Build documentation"
- ✓ Tests input containing `<h1>` is demoted to `<h2>` inside the rendered document
- ✓ Tests input containing `<h2>` and `<h3>` maintains appropriate levels without `<h1>`
- ✓ Tests malicious `<script>` tags in input HTML are excluded or inert
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G7.T1 completed
- Target file: `tests/projects/build-documentation.test.tsx`

**Implementation Details:**

Write `tests/projects/build-documentation.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BuildDocumentation } from '@/components/projects/build-documentation';

describe('BuildDocumentation Component (Req 13)', () => {
  it('renders section labelled by h2 Build documentation', () => {
    const html = '<h2 id="arch">Architecture</h2><p>Engine pipeline details.</p>';
    render(<BuildDocumentation html={html} />);

    const sectionHeading = screen.getByRole('heading', { level: 2, name: 'Build documentation' });
    expect(sectionHeading).toBeDefined();

    const section = sectionHeading.closest('section');
    expect(section?.getAttribute('aria-labelledby')).toBe('build-docs-heading');
  });

  it('demotes h1 in markdown documentation so no h1 appears inside the section', () => {
    // If documentation author included # Title in Markdown
    const htmlWithH1 = '<h1 id="title">Doc Title</h1><p>Body copy.</p><h2>Section</h2>';
    render(<BuildDocumentation html={htmlWithH1} />);

    // Zero h1 elements inside documentation
    expect(screen.queryByRole('heading', { level: 1 })).toBeNull();

    // The h1 was demoted to h2, and h2 demoted to h3
    expect(screen.getByRole('heading', { level: 2, name: 'Doc Title' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 3, name: 'Section' })).toBeDefined();
  });
});
'@ | Set-Content "tests\projects\build-documentation.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/build-documentation.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 17.1

---

### M6.G7.T4: Author Unit Tests for `RelatedProjects` (`tests/projects/related-projects.test.tsx`)

**Objective:** Create `tests/projects/related-projects.test.tsx` verifying card count, `headingLevel={3}` rendering, section heading, and null return on empty inputs.

**Acceptance Criteria:**
- ✓ File `tests/projects/related-projects.test.tsx` created
- ✓ Tests renders `h2` "Related projects" when array is non-empty
- ✓ Tests renders project cards with `<h3>` title headings (Req 14.6, 16.7)
- ✓ Tests cards are rendered in exact input array order
- ✓ Tests returns `null` and renders zero elements when array is empty (Req 14.7)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G7.T2 completed
- Fixtures available in `tests/fixtures/projects-data.ts`
- Target file: `tests/projects/related-projects.test.tsx`

**Implementation Details:**

Write `tests/projects/related-projects.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RelatedProjects } from '@/components/projects/related-projects';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';

describe('RelatedProjects Component (Req 14.6, 14.7)', () => {
  const cards = sampleProjectsList.slice(1, 4).map(toProjectCardData);

  it('renders section h2 Related projects and project cards with h3 headings', () => {
    render(<RelatedProjects projects={cards} />);

    expect(screen.getByRole('heading', { level: 2, name: 'Related projects' })).toBeDefined();

    const cardHeadings = screen.getAllByRole('heading', { level: 3 });
    expect(cardHeadings.length).toBe(3);
    expect(cardHeadings[0].textContent).toBe(cards[0].title);
    expect(cardHeadings[1].textContent).toBe(cards[1].title);
    expect(cardHeadings[2].textContent).toBe(cards[2].title);
  });

  it('returns null and renders zero elements when projects array is empty', () => {
    const { container } = render(<RelatedProjects projects={[]} />);
    expect(container.firstChild).toBeNull();
    expect(screen.queryByRole('heading', { level: 2, name: 'Related projects' })).toBeNull();
  });
});
'@ | Set-Content "tests\projects\related-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/related-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.6, Req 14.7, Req 16.7, Req 17.1

---

### M6.G7.T5: Verify Responsive Grid Utilities on `RelatedProjects`

**Objective:** Append test cases in `tests/projects/related-projects.test.tsx` verifying that responsive column utilities (`grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`) are strictly applied to the card grid.

**Acceptance Criteria:**
- ✓ Asserts card container element has `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G7.T4 completed
- Target file: `tests/projects/related-projects.test.tsx`

**Implementation Details:**

Append grid assertions using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Responsive Utilities (Req 16.2)', () => {
    it('applies 1-col on mobile, 2-col on tablet, and 3-col on desktop breakpoints', () => {
      const { container } = render(<RelatedProjects projects={cards} />);
      const grid = container.querySelector('.grid');

      expect(grid).not.toBeNull();
      expect(grid?.className).toContain('grid-cols-1');
      expect(grid?.className).toContain('md:grid-cols-2');
      expect(grid?.className).toContain('lg:grid-cols-3');
    });
  });
'@

$content = Get-Content "tests\projects\related-projects.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\related-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/related-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.2

---

### M6.G7.T6: Verify Full Heading Order Hierarchy in Composite Test

**Objective:** Create a composite test in `tests/projects/build-documentation.test.tsx` asserting that `ProjectHeader` (`h1`), `BuildDocumentation` (`h2`), and demoted documentation headings (`h3`) form an unbroken heading chain without skipped levels.

**Acceptance Criteria:**
- ✓ Renders a simulated case study layout containing `h1` Title, `h2` Build documentation, and demoted Markdown headings
- ✓ Verifies heading level sequence does not jump (e.g. `h1` $\rightarrow$ `h2` $\rightarrow$ `h3`, never `h1` $\rightarrow$ `h3`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G7.T3 completed
- Target file: `tests/projects/build-documentation.test.tsx`

**Implementation Details:**

Append composite hierarchy test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Heading Hierarchy Continuity (Req 16.7)', () => {
    it('forms an unbroken heading sequence without skipping levels', () => {
      const docHtml = '<h1 id="intro">Overview</h1><p>Text</p><h2>Pipeline</h2><p>Text</p>';
      const { container } = render(
        <div>
          <h1>Alpha Pipeline Core</h1>
          <BuildDocumentation html={docHtml} />
        </div>
      );

      const headings = Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6'));
      expect(headings.length).toBe(4);

      // Sequence: h1 (Project Title) -> h2 (Build documentation) -> h2 (Overview) -> h3 (Pipeline)
      expect(headings[0].tagName.toLowerCase()).toBe('h1');
      expect(headings[1].tagName.toLowerCase()).toBe('h2');
      expect(headings[2].tagName.toLowerCase()).toBe('h2');
      expect(headings[3].tagName.toLowerCase()).toBe('h3');
    });
  });
'@

$content = Get-Content "tests\projects\build-documentation.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\build-documentation.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/build-documentation.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.3, Req 16.7

---

### M6.G7.T7: Author Automated Axe Accessibility Tests for Documentation & Related Projects

**Objective:** Append automated axe tests in `tests/projects/build-documentation.test.tsx` and `related-projects.test.tsx` verifying WCAG 2.1 AA compliance with zero violations.

**Acceptance Criteria:**
- ✓ Evaluates `BuildDocumentation` with standard headings: 0 axe violations
- ✓ Evaluates `BuildDocumentation` with demoted `h1` headings: 0 axe violations
- ✓ Evaluates `RelatedProjects`: 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G7.T5 and M6.G7.T6 completed

**Implementation Details:**

Append axe tests across both test files using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. BuildDocumentation axe
$appendDocAxe = @'

  describe('Axe Accessibility Matrix (Req 16.6)', () => {
    it('reports zero axe violations for BuildDocumentation', async () => {
      const { axe } = require('vitest-axe');
      const html = '<h2 id="arch">Architecture</h2><p>Notes</p><h3>Details</h3>';
      const { container } = render(<BuildDocumentation html={html} />);
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
'@
$contentDoc = Get-Content "tests\projects\build-documentation.test.tsx" -Raw
$contentDoc = $contentDoc -replace "\s*\}\);\s*$", "$appendDocAxe`n});`n"
$contentDoc | Set-Content "tests\projects\build-documentation.test.tsx" -Encoding UTF8

# 2. RelatedProjects axe
$appendRelAxe = @'

  describe('Axe Accessibility Matrix (Req 16.6)', () => {
    it('reports zero axe violations for RelatedProjects', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(<RelatedProjects projects={cards} />);
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
'@
$contentRel = Get-Content "tests\projects\related-projects.test.tsx" -Raw
$contentRel = $contentRel -replace "\s*\}\);\s*$", "$appendRelAxe`n});`n"
$contentRel | Set-Content "tests\projects\related-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/build-documentation.test.tsx tests/projects/related-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M6.G7.T8: Audit Absence of Client Directives and Hardcoded Design Tokens

**Objective:** Audit `src/components/projects/build-documentation.tsx` and `related-projects.tsx` ensuring zero `'use client'`, zero raw hex colors, zero arbitrary Tailwind brackets, and file lengths strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ Both files strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G7.T1 and M6.G7.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @(
    "src\components\projects\build-documentation.tsx",
    "src\components\projects\related-projects.tsx"
)
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
        Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @(
    "src\components\projects\build-documentation.tsx",
    "src\components\projects\related-projects.tsx"
)
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
        Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.6, Req 16.1, Req 17.3, Req 17.4

---

### M6.G7.T9: Verify Zero Custom Dangerous HTML Sanitization Bypasses

**Objective:** Inspect `src/components/projects/build-documentation.tsx` ensuring that `dangerouslySetInnerHTML` is never called directly and rendering is handled exclusively by M3's `MarkdownDoc`.

**Acceptance Criteria:**
- ✓ Searches `build-documentation.tsx` for `dangerouslySetInnerHTML`
- ✓ Confirms zero occurrences
- ✓ Confirms `MarkdownDoc` is used to render HTML safely
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G7.T1 completed

**Implementation Details:**

Execute check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\components\projects\build-documentation.tsx"
$content = Get-Content $file -Raw

if ($content.Contains("dangerouslySetInnerHTML")) {
    Write-Host "CRITICAL: Direct dangerouslySetInnerHTML bypass found in $file. Must use MarkdownDoc (Req 13.5)"
    "FAIL"
} else {
    "PASS"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\components\projects\build-documentation.tsx"
$content = Get-Content $file -Raw

if ($content.Contains("dangerouslySetInnerHTML")) {
    Write-Host "CRITICAL: Direct dangerouslySetInnerHTML bypass found in $file. Must use MarkdownDoc (Req 13.5)"
    "FAIL"
} else {
    "PASS"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.5

---

### M6.G7.T10: Checkpoint — BuildDocumentation & RelatedProjects Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `BuildDocumentation` and `RelatedProjects`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all documentation and related projects test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G7.T1 through M6.G7.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/build-documentation.test.tsx tests/projects/related-projects.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/build-documentation.test.tsx tests/projects/related-projects.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.4, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\projects\build-documentation.tsx"
Test-Path "src\components\projects\related-projects.tsx"
Test-Path "tests\projects\build-documentation.test.tsx"
Test-Path "tests\projects\related-projects.test.tsx"
npm run typecheck
npm run test -- tests/projects/build-documentation.test.tsx tests/projects/related-projects.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all documentation and related projects tests with return code 0.