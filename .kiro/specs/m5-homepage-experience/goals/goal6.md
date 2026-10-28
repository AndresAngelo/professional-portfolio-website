# M5.G6: FeaturedProjects and SkillsSnapshot

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component sections `FeaturedProjects` in `src/components/home/featured-projects.tsx` and `SkillsSnapshot` in `src/components/home/skills-snapshot.tsx`. `FeaturedProjects` renders a section landmark (`<section aria-labelledby="featured-projects-heading">`) with an `h2` heading, a responsive card grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`), one M3 `Card` per project containing an `h3` title link to `/projects/{slug}`, project summary, M3 `StatusBadge`, and M3 `TagList` of technologies. When no projects are featured, it presents the Section_Heading, an M3 `EmptyState` component with `HOME_TEXT.featuredEmpty`, and retains the "View all projects" link to `/projects`. It strictly omits repository, demo, and documentation links. `SkillsSnapshot` renders a section landmark (`<section aria-labelledby="skills-heading">`) with an `h2` heading, an `h3` group label (`Technologies`), and an M3 `TagList` displaying derived technology tags without fabricating skills, percentages, or proficiency ratings. Both components execute as pure server components (zero `'use client'`), use semantic tokens exclusively, and maintain file lengths under 300 lines. Validate rendering, empty states, and Property 10 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/home/featured-projects.tsx` implemented as a server component without `'use client'`
- ✓ `FeaturedProjects` renders `<section aria-labelledby="featured-projects-heading">` with `h2#featured-projects-heading`
- ✓ Renders one M3 `Card` per featured project with `h3` title linking to `/projects/{slug}`, summary, `StatusBadge`, and `TagList`
- ✓ Retains "View all projects" link to `/projects` in both populated and empty states
- ✓ Empty state renders M3 `EmptyState` with `HOME_TEXT.featuredEmpty` text within the section
- ✓ Strictly omits repository, live demo, and documentation links from project cards (Req 6.7)
- ✓ `src/components/home/skills-snapshot.tsx` implemented as a server component without `'use client'`
- ✓ `SkillsSnapshot` renders `<section aria-labelledby="skills-heading">` with `h2#skills-heading`, `h3` group label, and M3 `TagList`
- ✓ Applies standard responsive grid classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Unit, property (Property 10), and axe accessibility tests in `tests/home/featured-projects.test.tsx` and `skills-snapshot.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1 through M5.G5 completed
- `home-text.ts` available at `src/components/home/home-text.ts`
- M3 primitives (`Container`, `Card`, `TagList`, `StatusBadge`, `EmptyState`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available at `src/components/ui/`
- Target files: `src/components/home/featured-projects.tsx` and `src/components/home/skills-snapshot.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M5.G6.T1: Implement `FeaturedProjects` Component (`src/components/home/featured-projects.tsx`)

**Objective:** Author the server component `FeaturedProjects` in `src/components/home/featured-projects.tsx` rendering project cards or an empty state with navigation links.

**Acceptance Criteria:**
- ✓ File `src/components/home/featured-projects.tsx` created
- ✓ Exports `FeaturedProjectsProps` requiring `projects: readonly Project[]`
- ✓ Exports `FeaturedProjects(props: FeaturedProjectsProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="featured-projects-heading" className="py-12 md:py-16 bg-surface border-b border-border-default">`
- ✓ Wraps content in M3 `<Container>`
- ✓ Renders `<h2 id="featured-projects-heading" className="text-heading-2 font-bold text-text-primary mb-8">`
- ✓ If `projects.length > 0`: renders responsive grid `<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">`
- ✓ Each card renders an `h3` containing a `Link` to `/projects/${project.slug}`, summary, `StatusBadge`, and `TagList`
- ✓ If `projects.length === 0`: renders M3 `EmptyState` with `message={HOME_TEXT.featuredEmpty}`
- ✓ Renders bottom link to `/projects` with text `HOME_TEXT.viewAllProjects`
- ✓ Omits repository, live demo, and documentation links (Req 6.7)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5.G1 completed (`home-text.ts` exists)
- M3 primitives available
- Target file: `src/components/home/featured-projects.tsx`

**Implementation Details:**

Write `src/components/home/featured-projects.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import type { Project } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Card } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/status-badge';
import { TagList } from '@/components/ui/tag-list';
import { EmptyState } from '@/components/ui/empty-state';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';

export interface FeaturedProjectsProps {
  projects: readonly Project[];
}

/**
 * Featured Projects Section Component
 *
 * Displays curated engineering work with build documentation summaries.
 * design.md Section 6.1 & Requirements 6, 7. Server component by default (Req 1.2).
 */
export function FeaturedProjects({ projects }: FeaturedProjectsProps): JSX.Element {
  const hasProjects = projects.length > 0;

  return (
    <section
      aria-labelledby="featured-projects-heading"
      className="border-b border-border-default bg-surface py-12 md:py-16"
    >
      <Container>
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <h2
              id="featured-projects-heading"
              className="text-heading-2 font-bold tracking-tight text-text-primary"
            >
              {HOME_TEXT.featuredHeading}
            </h2>
          </div>
          <Link
            href="/projects"
            className={cx(
              'inline-flex items-center text-body font-medium text-brand-primary underline hover:opacity-80 rounded-sm self-start md:self-auto',
              FOCUS_RING,
              MOTION_FAST
            )}
          >
            {HOME_TEXT.viewAllProjects} &rarr;
          </Link>
        </div>

        {hasProjects ? (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <Card
                key={project.slug}
                className="flex flex-col justify-between h-full p-6"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <StatusBadge status={project.status} />
                  </div>
                  <h3 className="text-heading-4 font-semibold text-text-primary mb-2">
                    <Link
                      href={`/projects/${project.slug}`}
                      className={cx(
                        'hover:text-brand-primary underline-offset-4 hover:underline rounded-sm',
                        FOCUS_RING,
                        MOTION_FAST
                      )}
                    >
                      {project.title}
                    </Link>
                  </h3>
                  <p className="text-body text-text-secondary mb-4 line-clamp-3">
                    {project.summary}
                  </p>
                </div>
                <div>
                  <TagList items={project.technologies} />
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <div className="py-6">
            <EmptyState message={HOME_TEXT.featuredEmpty} />
          </div>
        )}
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\featured-projects.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/featured-projects.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.3, Req 6.4, Req 6.5, Req 6.6, Req 6.7, Req 7.1, Req 7.2, Req 7.4, Req 15.2, Req 15.3, Req 15.4

---

### M5.G6.T2: Implement `SkillsSnapshot` Component (`src/components/home/skills-snapshot.tsx`)

**Objective:** Author the server component `SkillsSnapshot` in `src/components/home/skills-snapshot.tsx` rendering compact technology groups derived from project evidence.

**Acceptance Criteria:**
- ✓ File `src/components/home/skills-snapshot.tsx` created
- ✓ Exports `SkillsSnapshotProps` requiring `groups: readonly SkillGroup[]`
- ✓ Exports `SkillsSnapshot(props: SkillsSnapshotProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="skills-heading" className="py-12 md:py-16 bg-page border-b border-border-default">`
- ✓ Wraps content in M3 `<Container>`
- ✓ Renders `<h2 id="skills-heading" className="text-heading-2 font-bold text-text-primary mb-6">` with `HOME_TEXT.skillsHeading`
- ✓ Iterates `groups`, rendering `h3` for group label (`Technologies`) and M3 `TagList` for skill names
- ✓ Contains zero hardcoded technology names or fabricated ratings (Req 9.5)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5.G1 completed (`home-text.ts` exists)
- M5.G3 completed (`SkillGroup` interface available)
- Target file: `src/components/home/skills-snapshot.tsx`

**Implementation Details:**

Write `src/components/home/skills-snapshot.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { Container } from '@/components/ui/container';
import { TagList } from '@/components/ui/tag-list';
import { HOME_TEXT } from './home-text';
import type { SkillGroup } from '@/lib/home/derive-skill-groups';

export interface SkillsSnapshotProps {
  groups: readonly SkillGroup[];
}

/**
 * Skills Snapshot Section Component
 *
 * Presents verified technology capabilities derived strictly from project documentation.
 * design.md Section 6.1 & Requirement 9. Server component by default (Req 1.2).
 */
export function SkillsSnapshot({ groups }: SkillsSnapshotProps): JSX.Element {
  return (
    <section
      aria-labelledby="skills-heading"
      className="border-b border-border-default bg-page py-12 md:py-16"
    >
      <Container>
        <h2
          id="skills-heading"
          className="text-heading-2 font-bold tracking-tight text-text-primary mb-6"
        >
          {HOME_TEXT.skillsHeading}
        </h2>

        <div className="flex flex-col gap-6 max-w-3xl">
          {groups.map((group) => (
            <div key={group.label} className="flex flex-col gap-3">
              <h3 className="text-heading-4 font-semibold text-text-secondary">
                {group.label}
              </h3>
              <TagList items={group.technologies.map((t) => t.name)} />
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\skills-snapshot.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/skills-snapshot.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.5, Req 9.6, Req 14.1, Req 14.2

---

### M5.G6.T3: Author Unit Scenarios for `FeaturedProjects` (`tests/home/featured-projects.test.tsx`)

**Objective:** Create `tests/home/featured-projects.test.tsx` verifying card rendering, slug link destinations, tag lists, status badges, empty states, and absence of repository/demo links.

**Acceptance Criteria:**
- ✓ File `tests/home/featured-projects.test.tsx` created
- ✓ Renders populated projects: verifies cards, title links to `/projects/{slug}`, status badge, and tags
- ✓ Verifies zero repository, demo, or documentation links appear in cards (Req 6.7)
- ✓ Verifies link to `/projects` with text "View all projects" is present
- ✓ Renders empty projects: verifies `EmptyState` text and presence of "View all projects" link
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G6.T1 completed
- Fixtures available in `tests/fixtures/home-data.ts`
- Target file: `tests/home/featured-projects.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/featured-projects.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FeaturedProjects } from '@/components/home/featured-projects';
import { sampleProjects } from '../fixtures/home-data';

describe('FeaturedProjects Component (Req 6, 7)', () => {
  const threeFeatured = sampleProjects.filter((p) => p.featured).slice(0, 3);

  describe('Concrete Unit Scenarios', () => {
    it('renders project cards with heading hierarchy, title links, badges, and tags', () => {
      render(<FeaturedProjects projects={threeFeatured} />);

      // Section heading h2
      const sectionHeading = screen.getByRole('heading', { level: 2, name: 'Featured Projects' });
      expect(sectionHeading).toBeDefined();

      // Card titles as h3 links
      const titleLinks = screen.getAllByRole('heading', { level: 3 });
      expect(titleLinks.length).toBe(3);

      threeFeatured.forEach((project) => {
        const link = screen.getByRole('link', { name: project.title });
        expect(link.getAttribute('href')).toBe(`/projects/${project.slug}`);
        expect(screen.getByText(project.summary)).toBeDefined();
      });

      // View all projects link
      const viewAllLink = screen.getByRole('link', { name: /View all projects/ });
      expect(viewAllLink.getAttribute('href')).toBe('/projects');
    });

    it('omits repository, demo, and documentation links from project cards', () => {
      render(<FeaturedProjects projects={threeFeatured} />);

      expect(screen.queryByText(/GitHub/i)).toBeNull();
      expect(screen.queryByText(/Live Demo/i)).toBeNull();
      expect(screen.queryByText(/Documentation/i)).toBeNull();

      // Ensure no external anchors exist in this section
      const anchors = screen.getAllByRole('link');
      anchors.forEach((a) => {
        const href = a.getAttribute('href') || '';
        expect(href.startsWith('https://')).toBe(false);
      });
    });

    it('renders accessible empty state and retains View all projects link when array is empty', () => {
      render(<FeaturedProjects projects={[]} />);

      expect(screen.getByRole('heading', { level: 2, name: 'Featured Projects' })).toBeDefined();
      expect(screen.getByText('No featured projects yet. Browse all projects instead.')).toBeDefined();

      const viewAllLink = screen.getByRole('link', { name: /View all projects/ });
      expect(viewAllLink.getAttribute('href')).toBe('/projects');
    });
  });
});
'@ | Set-Content "tests\home\featured-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/featured-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.3, Req 6.4, Req 6.6, Req 6.7, Req 7.1, Req 7.2, Req 7.4

---

### M5.G6.T4: Author Property-Based Test for FeaturedProjects (Property 10)

**Objective:** Append property-based test in `tests/home/featured-projects.test.tsx` validating Property 10 across generated project arrays of up to 3 items.

**Acceptance Criteria:**
- ✓ Implements Property 10 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 10: featured project cards show required fields and links`
- ✓ Asserts one card per project in identical order
- ✓ Asserts each card contains title link `/projects/{slug}`, summary, status, and tags
- ✓ Asserts zero repository, demo, or external links exist in the cards
- ✓ Asserts "View all projects" link is present
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G6.T3 completed
- Arbitraries in `tests/fixtures/home-arbitraries.ts`
- Target file: `tests/home/featured-projects.test.tsx`

**Implementation Details:**

Append Property 10 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 10)', () => {
    it('Feature: m5-homepage-experience, Property 10: featured project cards show required fields and links for any valid projects array', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProject } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          fc.array(arbProject, { minLength: 1, maxLength: 3 }),
          (projects: any) => {
            cleanup();
            render(<FeaturedProjects projects={projects} />);

            // 1. One h3 title link per project in order
            const h3Elements = screen.getAllByRole('heading', { level: 3 });
            expect(h3Elements.length).toBe(projects.length);

            for (let i = 0; i < projects.length; i++) {
              const p = projects[i];
              const link = screen.getByRole('link', { name: p.title });
              expect(link.getAttribute('href')).toBe(`/projects/${p.slug}`);
              expect(h3Elements[i].textContent).toBe(p.title);
            }

            // 2. View all link invariant
            const viewAll = screen.getByRole('link', { name: /View all projects/ });
            expect(viewAll.getAttribute('href')).toBe('/projects');

            // 3. No external repository/demo links
            const allLinks = screen.getAllByRole('link');
            allLinks.forEach((a) => {
              const href = a.getAttribute('href') || '';
              expect(href.startsWith('https://')).toBe(false);
            });
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\featured-projects.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\featured-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/featured-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.2, Req 6.3, Req 6.4, Req 6.5, Req 6.7

---

### M5.G6.T5: Author Unit Tests for `SkillsSnapshot` (`tests/home/skills-snapshot.test.tsx`)

**Objective:** Create `tests/home/skills-snapshot.test.tsx` verifying section heading, group label, and tag rendering from derived skill groups.

**Acceptance Criteria:**
- ✓ File `tests/home/skills-snapshot.test.tsx` created
- ✓ Verifies `h2` heading with "Skills Snapshot"
- ✓ Verifies `h3` heading with "Technologies"
- ✓ Verifies technology tags match fixture data
- ✓ Verifies zero hardcoded technology strings in component source code (Req 9.5)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G6.T2 completed
- Target file: `tests/home/skills-snapshot.test.tsx`

**Implementation Details:**

Write unit tests in `tests/home/skills-snapshot.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SkillsSnapshot } from '@/components/home/skills-snapshot';
import type { SkillGroup } from '@/lib/home/derive-skill-groups';

describe('SkillsSnapshot Component (Req 9)', () => {
  const sampleGroups: SkillGroup[] = [
    {
      label: 'Technologies',
      technologies: [
        { name: 'TypeScript', count: 3 },
        { name: 'Next.js', count: 2 },
        { name: 'Docker', count: 2 },
      ],
    },
  ];

  it('renders section heading h2, group heading h3, and technology tags', () => {
    render(<SkillsSnapshot groups={sampleGroups} />);

    expect(screen.getByRole('heading', { level: 2, name: 'Skills Snapshot' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 3, name: 'Technologies' })).toBeDefined();

    expect(screen.getByText('TypeScript')).toBeDefined();
    expect(screen.getByText('Next.js')).toBeDefined();
    expect(screen.getByText('Docker')).toBeDefined();
  });
});
'@ | Set-Content "tests\home\skills-snapshot.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/skills-snapshot.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.5, Req 9.6

---

### M5.G6.T6: Author Responsive Grid Class Verification Tests

**Objective:** Append test cases in `tests/home/featured-projects.test.tsx` verifying that responsive column utilities (`grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`) are strictly applied.

**Acceptance Criteria:**
- ✓ Asserts `FeaturedProjects` card container has `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Asserts `Container` primitive is rendered
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G6.T4 completed
- Target file: `tests/home/featured-projects.test.tsx`

**Implementation Details:**

Append grid class assertions using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Responsive Utilities (Req 15)', () => {
    it('applies 1-col on mobile, 2-col on tablet, and 3-col on desktop breakpoints', () => {
      const { container } = render(<FeaturedProjects projects={threeFeatured} />);
      const grid = container.querySelector('.grid');

      expect(grid).not.toBeNull();
      expect(grid?.className).toContain('grid-cols-1');
      expect(grid?.className).toContain('md:grid-cols-2');
      expect(grid?.className).toContain('lg:grid-cols-3');
    });
  });
'@

$content = Get-Content "tests\home\featured-projects.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\featured-projects.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/featured-projects.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 15.4

---

### M5.G6.T7: Author Automated Axe Accessibility Tests for FeaturedProjects & SkillsSnapshot

**Objective:** Append automated axe tests in `tests/home/featured-projects.test.tsx` and `skills-snapshot.test.tsx` verifying WCAG 2.1 AA compliance with zero violations.

**Acceptance Criteria:**
- ✓ Evaluates `FeaturedProjects` (populated): 0 axe violations
- ✓ Evaluates `FeaturedProjects` (empty): 0 axe violations
- ✓ Evaluates `SkillsSnapshot`: 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G6.T6 and M5.G6.T5 completed

**Implementation Details:**

Append axe tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Append to featured-projects.test.tsx
$appendFeaturedAxe = @'

  describe('Axe Accessibility Matrix (Req 14)', () => {
    it('reports zero axe violations for populated and empty featured projects', async () => {
      const { axe } = require('vitest-axe');

      const { container: c1 } = render(<FeaturedProjects projects={threeFeatured} />);
      expect((await axe(c1)).violations).toHaveLength(0);

      const { container: c2 } = render(<FeaturedProjects projects={[]} />);
      expect((await axe(c2)).violations).toHaveLength(0);
    });
  });
'@

$contentFP = Get-Content "tests\home\featured-projects.test.tsx" -Raw
$contentFP = $contentFP -replace "\s*\}\);\s*$", "$appendFeaturedAxe`n});`n"
$contentFP | Set-Content "tests\home\featured-projects.test.tsx" -Encoding UTF8

# Append to skills-snapshot.test.tsx
$appendSkillsAxe = @'

  it('reports zero axe violations for skills snapshot', async () => {
    const { axe } = require('vitest-axe');
    const { container } = render(<SkillsSnapshot groups={sampleGroups} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@

$contentSS = Get-Content "tests\home\skills-snapshot.test.tsx" -Raw
$contentSS = $contentSS -replace "\s*\}\);\s*$", "$appendSkillsAxe`n});`n"
$contentSS | Set-Content "tests\home\skills-snapshot.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/featured-projects.test.tsx tests/home/skills-snapshot.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.7

---

### M5.G6.T8: Audit Absence of Fabricated Skills & Hardcoded Literals

**Objective:** Audit `src/components/home/skills-snapshot.tsx` ensuring zero technology names (`'React'`, `'TypeScript'`, etc.) are hardcoded in the component per Requirement 9.5.

**Acceptance Criteria:**
- ✓ Searches `skills-snapshot.tsx` for technology name literals
- ✓ Confirms component receives all skill tags strictly via `groups` prop
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G6.T2 completed

**Implementation Details:**

Execute literal check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\components\home\skills-snapshot.tsx"
$content = Get-Content $file -Raw

$bannedNames = @('TypeScript', 'React', 'Next.js', 'Docker', 'Python', 'Go', 'PostgreSQL')
$violations = @()

foreach ($b in $bannedNames) {
    if ($content.Contains("'$b'") -or $content.Contains("""$b""")) {
        $violations += "Hardcoded technology literal '$b' found in $file (Req 9.5 violation)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 9.5

---

### M5.G6.T9: Verify Source Hygiene of `FeaturedProjects` and `SkillsSnapshot`

**Objective:** Audit `featured-projects.tsx` and `skills-snapshot.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file lengths strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ Both files are strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G6.T1 and M5.G6.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\components\home\featured-projects.tsx", "src\components\home\skills-snapshot.tsx")
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
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 9.6, Req 14.8, Req 16.7, Req 16.8

---

### M5.G6.T10: Checkpoint — FeaturedProjects and SkillsSnapshot Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `FeaturedProjects` and `SkillsSnapshot`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs featured projects and skills tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G6.T1 through M5.G6.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/featured-projects.test.tsx tests/home/skills-snapshot.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/featured-projects.test.tsx tests/home/skills-snapshot.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\home\featured-projects.tsx"
Test-Path "src\components\home\skills-snapshot.tsx"
Test-Path "tests\home\featured-projects.test.tsx"
Test-Path "tests\home\skills-snapshot.test.tsx"
npm run typecheck
npm run test -- tests/home/featured-projects.test.tsx tests/home/skills-snapshot.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all featured projects and skills snapshot tests with return code 0.