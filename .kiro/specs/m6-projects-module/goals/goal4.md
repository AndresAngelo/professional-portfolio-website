# M6.G4: ProjectCard and ProjectGrid

> **Milestone:** M6 — Projects Module  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the reusable, presentational UI components `ProjectCard` in `src/components/projects/project-card.tsx` and `ProjectGrid` in `src/components/projects/project-grid.tsx`. `ProjectCard` renders an individual project summary card using M3's `Card` primitive, supporting configurable heading levels (`headingLevel: 2 | 3`) to ensure heading hierarchy integrity on both the Projects Index (`<h2>`) and Related Projects (`<h3>`) sections without skipping levels. It renders the project title as a single primary link (`/projects/{slug}`), concise summary copy, role, M3 `StatusBadge`, and at most 4 technologies through M3 `TagList` in stored order, accompanied by a `+{n} more` text indicator when technologies exceed 4. It displays "Completed {date}" when `completedAt !== null` or "Started {date}" when `completedAt === null` inside `<time dateTime={iso}>` elements formatted deterministically via M5's `formatDisplayDate`. It strictly omits repository, live demo, and documentation links. `ProjectGrid` renders an unordered list (`<ul>`) styled as a responsive CSS grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`) containing `ProjectCard` components while strictly preserving input order. Ensure both components are pure presentational components without `'use client'`, using Semantic_Tokens exclusively, with file lengths under 300 lines. Validate all rendering, heading levels, and Property 14 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/projects/project-card.tsx` implemented as a server-safe component without `'use client'`
- ✓ `ProjectCard` accepts `project: ProjectCardData` and `headingLevel: 2 | 3`
- ✓ Renders exactly one anchor tag linking to `/projects/${project.slug}` with the project title as accessible name
- ✓ Displays summary, `StatusBadge`, role, and at most `MAX_CARD_TECHNOLOGIES` (4) tags in stored order
- ✓ Displays text `+{n - 4} more` if and only if `project.technologies.length > 4`
- ✓ Renders completion metadata inside `<time dateTime={iso}>` using `formatDisplayDate` ("Completed {date}" vs "Started {date}")
- ✓ Strictly omits repository, live demo, and documentation links (Req 2.7)
- ✓ `src/components/projects/project-grid.tsx` renders responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`) preserving input order
- ✓ Unit, property (Property 14), and axe accessibility tests in `tests/projects/project-card.test.tsx` and `project-grid.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1, M6.G2, and M6.G3 completed (`card-data.ts`, `projects-text.ts`, and M5's `formatDisplayDate` available)
- M3 primitives (`Card`, `TagList`, `StatusBadge`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available in `src/components/ui/`
- Target files: `src/components/projects/project-card.tsx` and `src/components/projects/project-grid.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G4.T1: Implement `ProjectCard` Component Skeleton & Heading Title Link (`src/components/projects/project-card.tsx`)

**Objective:** Author the initial skeleton of `src/components/projects/project-card.tsx` accepting `ProjectCardData` and dynamic `headingLevel` (`2 | 3`), rendering the primary title link inside M3 `Card`.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-card.tsx` created
- ✓ Exports `interface ProjectCardProps { readonly project: ProjectCardData; readonly headingLevel: 2 | 3; }`
- ✓ Exports `ProjectCard({ project, headingLevel }: ProjectCardProps): JSX.Element`
- ✓ Renders outer wrapper M3 `<Card className="flex flex-col justify-between h-full p-6">`
- ✓ Dynamically renders heading tag (`h2` or `h3` according to `headingLevel`)
- ✓ Heading contains single `<Link href={`/projects/${project.slug}`}>` with M3 `FOCUS_RING` and motion classes
- ✓ Accessible name of the link equals `project.title`
- ✓ Component contains zero `'use client'` directives

**Prerequisites:**
- M6.G1 completed (`ProjectCardData` in `src/lib/projects/card-data.ts`)
- M3 `Card`, `FOCUS_RING`, `MOTION_FAST`, `cx` available
- Target file: `src/components/projects/project-card.tsx`

**Implementation Details:**

Write `src/components/projects/project-card.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectCardProps {
  readonly project: ProjectCardData;
  readonly headingLevel: 2 | 3;
}

/**
 * ProjectCard Component
 *
 * Renders project summary card with dynamic heading level (h2 on index, h3 in related).
 * design.md Section 6.2 & Requirement 2. Server component by default (Req 1.1, 7.3).
 */
export function ProjectCard({ project, headingLevel }: ProjectCardProps): JSX.Element {
  const HeadingTag = `h${headingLevel}` as const;

  return (
    <Card className="flex flex-col justify-between h-full p-6">
      <div>
        <HeadingTag className="text-heading-4 font-semibold text-text-primary mb-2">
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
        </HeadingTag>
      </div>
    </Card>
  );
}
'@ | Set-Content "src\components\projects\project-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.8, Req 16.7, Req 17.3

---

### M6.G4.T2: Append Summary, StatusBadge, and Role Metadata to `ProjectCard`

**Objective:** Append status badge header, role, and summary copy to `ProjectCard` using semantic typography tokens.

**Acceptance Criteria:**
- ✓ Renders M3 `StatusBadge` for `project.status` above or alongside the title
- ✓ Renders `project.role` as visible secondary text
- ✓ Renders `project.summary` with semantic body text tokens and multi-line clamping
- ✓ Zero hardcoded design values or inline styles

**Prerequisites:**
- M6.G4.T1 completed
- Target file: `src/components/projects/project-card.tsx`

**Implementation Details:**

Update `src/components/projects/project-card.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$code = @'
import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/status-badge';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectCardProps {
  readonly project: ProjectCardData;
  readonly headingLevel: 2 | 3;
}

/**
 * ProjectCard Component
 *
 * Renders project summary card with dynamic heading level (h2 on index, h3 in related).
 * design.md Section 6.2 & Requirement 2. Server component by default (Req 1.1, 7.3).
 */
export function ProjectCard({ project, headingLevel }: ProjectCardProps): JSX.Element {
  const HeadingTag = `h${headingLevel}` as const;

  return (
    <Card className="flex flex-col justify-between h-full p-6">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <StatusBadge status={project.status} />
          <span className="text-caption font-medium text-text-secondary">
            {project.role}
          </span>
        </div>

        <HeadingTag className="text-heading-4 font-semibold text-text-primary mb-2">
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
        </HeadingTag>

        <p className="text-body text-text-secondary mb-4 line-clamp-3">
          {project.summary}
        </p>
      </div>
    </Card>
  );
}
'@ | Set-Content "src\components\projects\project-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 16.1

---

### M6.G4.T3: Append Technology Tags & Overflow Count to `ProjectCard`

**Objective:** Append technology tags rendering using M3 `TagList` capped at `MAX_CARD_TECHNOLOGIES` (4) with `+{n} more` text indicator.

**Acceptance Criteria:**
- ✓ Imports `MAX_CARD_TECHNOLOGIES` from `@/components/projects/projects-text`
- ✓ Renders first `min(4, technologies.length)` technologies in stored order via M3 `TagList`
- ✓ If `project.technologies.length > 4`, renders `<span className="text-caption font-medium text-text-secondary">+{n} more</span>` where $n = \text{length} - 4$
- ✓ If `project.technologies.length <= 4`, renders zero overflow text
- ✓ Does NOT make the `+{n} more` indicator an interactive element

**Prerequisites:**
- M6.G4.T2 completed
- M3 `TagList` available
- Target file: `src/components/projects/project-card.tsx`

**Implementation Details:**

Update `src/components/projects/project-card.tsx` to include technology tags and overflow indicator:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$code = @'
import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/status-badge';
import { TagList } from '@/components/ui/tag-list';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { MAX_CARD_TECHNOLOGIES } from './projects-text';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectCardProps {
  readonly project: ProjectCardData;
  readonly headingLevel: 2 | 3;
}

/**
 * ProjectCard Component
 *
 * Renders project summary card with dynamic heading level (h2 on index, h3 in related).
 * design.md Section 6.2 & Requirement 2. Server component by default (Req 1.1, 7.3).
 */
export function ProjectCard({ project, headingLevel }: ProjectCardProps): JSX.Element {
  const HeadingTag = `h${headingLevel}` as const;

  const totalTechs = project.technologies || [];
  const visibleTechs = totalTechs.slice(0, MAX_CARD_TECHNOLOGIES);
  const overflowCount = totalTechs.length - MAX_CARD_TECHNOLOGIES;

  return (
    <Card className="flex flex-col justify-between h-full p-6">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <StatusBadge status={project.status} />
          <span className="text-caption font-medium text-text-secondary">
            {project.role}
          </span>
        </div>

        <HeadingTag className="text-heading-4 font-semibold text-text-primary mb-2">
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
        </HeadingTag>

        <p className="text-body text-text-secondary mb-4 line-clamp-3">
          {project.summary}
        </p>
      </div>

      <div className="pt-2 border-t border-border-default/50">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <TagList items={visibleTechs} />
          {overflowCount > 0 && (
            <span className="text-caption font-medium text-text-secondary">
              +{overflowCount} more
            </span>
          )}
        </div>
      </div>
    </Card>
  );
}
'@ | Set-Content "src\components\projects\project-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.3, Req 2.4

---

### M6.G4.T4: Append Deterministic Date Timeline to `ProjectCard`

**Objective:** Append date timeline to `ProjectCard` displaying "Completed {date}" or "Started {date}" inside `<time dateTime={iso}>` formatted via M5's `formatDisplayDate`.

**Acceptance Criteria:**
- ✓ Imports `formatDisplayDate` from `@/lib/format-date`
- ✓ Imports `PROJECTS_TEXT` from `./projects-text`
- ✓ When `project.completedAt !== null`: renders "Completed <time dateTime={project.completedAt}>{formatDisplayDate(project.completedAt)}</time>"
- ✓ When `project.completedAt === null`: renders "Started <time dateTime={project.startedAt}>{formatDisplayDate(project.startedAt)}</time>"
- ✓ Strictly omits repository, live demo, and documentation links from card markup (Req 2.7)
- ✓ Contains zero other anchor tags

**Prerequisites:**
- M6.G4.T3 completed
- M5 `formatDisplayDate` available in `src/lib/format-date.ts`
- Target file: `src/components/projects/project-card.tsx`

**Implementation Details:**

Write the completed `src/components/projects/project-card.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/status-badge';
import { TagList } from '@/components/ui/tag-list';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { MAX_CARD_TECHNOLOGIES, PROJECTS_TEXT } from './projects-text';
import { formatDisplayDate } from '@/lib/format-date';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectCardProps {
  readonly project: ProjectCardData;
  readonly headingLevel: 2 | 3;
}

/**
 * ProjectCard Component
 *
 * Renders project summary card with dynamic heading level (h2 on index, h3 in related).
 * Displays role, status badge, summary, capped tags, and deterministic date timeline.
 * Strictly omits external repository, live demo, and docs links (Req 2.1-2.8).
 * Server component by default (Req 1.1, 7.3).
 */
export function ProjectCard({ project, headingLevel }: ProjectCardProps): JSX.Element {
  const HeadingTag = `h${headingLevel}` as const;

  const totalTechs = project.technologies || [];
  const visibleTechs = totalTechs.slice(0, MAX_CARD_TECHNOLOGIES);
  const overflowCount = totalTechs.length - MAX_CARD_TECHNOLOGIES;

  const isCompleted = project.completedAt !== null;
  const displayDateIso = isCompleted ? project.completedAt! : project.startedAt;
  const datePrefix = isCompleted
    ? PROJECTS_TEXT.completedPrefix
    : PROJECTS_TEXT.startedPrefix;

  return (
    <Card className="flex flex-col justify-between h-full p-6">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <StatusBadge status={project.status} />
          <span className="text-caption font-medium text-text-secondary">
            {project.role}
          </span>
        </div>

        <HeadingTag className="text-heading-4 font-semibold text-text-primary mb-2">
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
        </HeadingTag>

        <p className="text-body text-text-secondary mb-4 line-clamp-3">
          {project.summary}
        </p>
      </div>

      <div className="pt-4 border-t border-border-default/50">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <TagList items={visibleTechs} />
          {overflowCount > 0 && (
            <span className="text-caption font-medium text-text-secondary">
              +{overflowCount} more
            </span>
          )}
        </div>

        <p className="text-small text-text-secondary">
          {datePrefix}{' '}
          <time dateTime={displayDateIso}>
            {formatDisplayDate(displayDateIso)}
          </time>
        </p>
      </div>
    </Card>
  );
}
'@ | Set-Content "src\components\projects\project-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-card.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.5, Req 2.6, Req 2.7, Req 10.6

---

### M6.G4.T5: Implement `ProjectGrid` Component (`src/components/projects/project-grid.tsx`)

**Objective:** Author the presentational component `ProjectGrid` in `src/components/projects/project-grid.tsx` rendering an unordered list with responsive grid classes and propagating `headingLevel`.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-grid.tsx` created
- ✓ Exports `interface ProjectGridProps { readonly projects: readonly ProjectCardData[]; readonly headingLevel: 2 | 3; }`
- ✓ Exports `ProjectGrid({ projects, headingLevel }: ProjectGridProps): JSX.Element`
- ✓ Renders `<ul className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 list-none p-0 m-0">`
- ✓ Renders `<li key={project.slug} className="flex">` wrapping `<ProjectCard project={project} headingLevel={headingLevel} />`
- ✓ Preserves exact input array order without re-sorting
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G4.T4 completed
- Target file: `src/components/projects/project-grid.tsx`

**Implementation Details:**

Write `src/components/projects/project-grid.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { ProjectCard } from './project-card';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectGridProps {
  readonly projects: readonly ProjectCardData[];
  readonly headingLevel: 2 | 3;
}

/**
 * ProjectGrid Component
 *
 * Renders responsive CSS grid of project cards in given order.
 * design.md Section 6.2 & Requirement 2.9, 16.2. Server component by default (Req 1.1, 7.3).
 */
export function ProjectGrid({ projects, headingLevel }: ProjectGridProps): JSX.Element {
  return (
    <ul className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 list-none p-0 m-0">
      {projects.map((project) => (
        <li key={project.slug} className="flex flex-col">
          <ProjectCard project={project} headingLevel={headingLevel} />
        </li>
      ))}
    </ul>
  );
}
'@ | Set-Content "src\components\projects\project-grid.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-grid.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.9, Req 16.2, Req 16.7, Req 17.3

---

### M6.G4.T6: Author Concrete Unit Scenarios for `ProjectCard` (`tests/projects/project-card.test.tsx`)

**Objective:** Create `tests/projects/project-card.test.tsx` verifying card heading levels, single link destination, technology tags cap, overflow count, and timeline display.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-card.test.tsx` created
- ✓ Tests `headingLevel={2}` renders `<h2>` containing title link
- ✓ Tests `headingLevel={3}` renders `<h3>` containing title link
- ✓ Tests single link in card points to `/projects/${slug}`
- ✓ Tests 6 technologies render first 4 tags and `"+2 more"` text
- ✓ Tests 3 technologies render 3 tags and zero overflow indicator
- ✓ Tests `completedAt !== null` renders "Completed" with formatted date
- ✓ Tests `completedAt === null` renders "Started" with formatted date
- ✓ Tests zero repository, demo, or external anchors exist in card markup (Req 2.7)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G4.T4 completed
- Fixtures available in `tests/fixtures/projects-data.ts`
- Target file: `tests/projects/project-card.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/projects/project-card.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProjectCard } from '@/components/projects/project-card';
import { toProjectCardData } from '@/lib/projects/card-data';
import {
  sampleProjectsList,
  inProgressProject,
  overflowTechProject,
} from '../fixtures/projects-data';

describe('ProjectCard Component (Req 2)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('renders headingLevel 2 for index cards and headingLevel 3 for related cards', () => {
      const cardData = toProjectCardData(sampleProjectsList[0]);

      const { rerender } = render(<ProjectCard project={cardData} headingLevel={2} />);
      expect(screen.getByRole('heading', { level: 2, name: cardData.title })).toBeDefined();

      rerender(<ProjectCard project={cardData} headingLevel={3} />);
      expect(screen.getByRole('heading', { level: 3, name: cardData.title })).toBeDefined();
    });

    it('renders exactly one link in card pointing to /projects/{slug}', () => {
      const cardData = toProjectCardData(sampleProjectsList[0]);
      render(<ProjectCard project={cardData} headingLevel={2} />);

      const links = screen.getAllByRole('link');
      expect(links.length).toBe(1);
      expect(links[0].getAttribute('href')).toBe(`/projects/${cardData.slug}`);
      expect(links[0].textContent).toBe(cardData.title);
    });

    it('renders at most 4 technologies and indicates overflow count for 5+ technologies', () => {
      const overflowData = toProjectCardData(overflowTechProject); // 6 technologies
      render(<ProjectCard project={overflowData} headingLevel={2} />);

      // First 4 technologies: TypeScript, Go, Docker, Next.js
      expect(screen.getByText('TypeScript')).toBeDefined();
      expect(screen.getByText('Go')).toBeDefined();
      expect(screen.getByText('Docker')).toBeDefined();
      expect(screen.getByText('Next.js')).toBeDefined();

      // 5th and 6th omitted from tags
      expect(screen.queryByText('Python')).toBeNull();
      expect(screen.queryByText('PostgreSQL')).toBeNull();

      // Overflow indicator
      expect(screen.getByText('+2 more')).toBeDefined();
    });

    it('renders Started date when completedAt is null and Completed date when non-null', () => {
      const completedData = toProjectCardData(sampleProjectsList[0]); // completedAt: '2025-06-15'
      const { rerender } = render(<ProjectCard project={completedData} headingLevel={2} />);
      expect(screen.getByText(/Completed/)).toBeDefined();
      expect(screen.getByText('June 15, 2025')).toBeDefined();

      const inProgressData = toProjectCardData(inProgressProject); // completedAt: null, startedAt: '2025-07-01'
      rerender(<ProjectCard project={inProgressData} headingLevel={2} />);
      expect(screen.getByText(/Started/)).toBeDefined();
      expect(screen.getByText('July 1, 2025')).toBeDefined();
    });

    it('strictly omits repository, live demo, and external links from card', () => {
      const cardData = toProjectCardData(sampleProjectsList[0]);
      const { container } = render(<ProjectCard project={cardData} headingLevel={2} />);

      expect(container.querySelectorAll('a[target="_blank"]').length).toBe(0);
      expect(screen.queryByText(/Repository/i)).toBeNull();
      expect(screen.queryByText(/Live demo/i)).toBeNull();
    });
  });
});
'@ | Set-Content "tests\projects\project-card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 2.5, Req 2.6, Req 2.7, Req 2.8, Req 16.7

---

### M6.G4.T7: Author Property-Based Test for `ProjectCard` (Property 14)

**Objective:** Append property-based test in `tests/projects/project-card.test.tsx` validating Property 14 across generated `ProjectCardData` objects.

**Acceptance Criteria:**
- ✓ Implements Property 14 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 14: project cards show the required facts and a single internal link`
- ✓ Asserts heading level equals supplied `headingLevel` prop
- ✓ Asserts single anchor tag with `href="/projects/${slug}"`
- ✓ Asserts summary, role, and status badge present
- ✓ Asserts tag count is $\le 4$ and `+{n - 4} more` text present iff $n > 4$
- ✓ Asserts time element datetime equals expected ISO date
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G4.T6 completed
- Arbitraries in `tests/fixtures/projects-arbitraries.ts`
- Target file: `tests/projects/project-card.test.tsx`

**Implementation Details:**

Append Property 14 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 14)', () => {
    it('Feature: m6-projects-module, Property 14: project cards show required facts and single internal link for any ProjectCardData', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProjectCardData } = require('../fixtures/projects-arbitraries');

      fc.assert(
        fc.property(
          arbProjectCardData,
          fc.constantFrom(2, 3),
          (cardData: any, headingLevel: any) => {
            cleanup();
            render(<ProjectCard project={cardData} headingLevel={headingLevel} />);

            // 1. Single heading of specified level
            const headings = screen.getAllByRole('heading', { level: headingLevel });
            expect(headings.length).toBe(1);
            expect(headings[0].textContent).toBe(cardData.title);

            // 2. Exactly one link to /projects/{slug}
            const links = screen.getAllByRole('link');
            expect(links.length).toBe(1);
            expect(links[0].getAttribute('href')).toBe(`/projects/${cardData.slug}`);

            // 3. Facts: summary, role
            expect(screen.getByText(cardData.summary)).toBeDefined();
            expect(screen.getByText(cardData.role)).toBeDefined();

            // 4. Technologies tag cap and overflow indicator
            const n = cardData.technologies.length;
            if (n > 4) {
              expect(screen.getByText(`+${n - 4} more`)).toBeDefined();
            } else {
              expect(screen.queryByText(/more/)).toBeNull();
            }

            // 5. Time element datetime
            const expectedIso = cardData.completedAt !== null ? cardData.completedAt : cardData.startedAt;
            const timeElem = document.querySelector('time');
            expect(timeElem).not.toBeNull();
            expect(timeElem?.getAttribute('datetime')).toBe(expectedIso);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\project-card.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\project-card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-card.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 2.5, Req 2.6, Req 2.7, Req 2.8, Req 17.2

---

### M6.G4.T8: Author Unit Tests for `ProjectGrid` (`tests/projects/project-grid.test.tsx`)

**Objective:** Create `tests/projects/project-grid.test.tsx` verifying DOM order, responsive column classes, and pass-through of `headingLevel`.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-grid.test.tsx` created
- ✓ Tests renders cards in exact input array order
- ✓ Tests applies `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Tests passes `headingLevel` through to child cards
- ✓ Tests empty array renders empty `<ul>` without throwing
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G4.T5 completed
- Target file: `tests/projects/project-grid.test.tsx`

**Implementation Details:**

Write `tests/projects/project-grid.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProjectGrid } from '@/components/projects/project-grid';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';

describe('ProjectGrid Component (Req 2.9, 16.2)', () => {
  const cards = sampleProjectsList.slice(0, 3).map(toProjectCardData);

  it('renders project cards in exact given order', () => {
    render(<ProjectGrid projects={cards} headingLevel={2} />);

    const headings = screen.getAllByRole('heading', { level: 2 });
    expect(headings.length).toBe(3);
    expect(headings[0].textContent).toBe(cards[0].title);
    expect(headings[1].textContent).toBe(cards[1].title);
    expect(headings[2].textContent).toBe(cards[2].title);
  });

  it('applies responsive column classes to ul grid container', () => {
    const { container } = render(<ProjectGrid projects={cards} headingLevel={2} />);
    const ul = container.querySelector('ul');

    expect(ul).not.toBeNull();
    expect(ul?.className).toContain('grid');
    expect(ul?.className).toContain('grid-cols-1');
    expect(ul?.className).toContain('md:grid-cols-2');
    expect(ul?.className).toContain('lg:grid-cols-3');
  });

  it('renders an empty list without throwing when projects is empty', () => {
    const { container } = render(<ProjectGrid projects={[]} headingLevel={2} />);
    const ul = container.querySelector('ul');
    expect(ul).not.toBeNull();
    expect(ul?.children.length).toBe(0);
  });
});
'@ | Set-Content "tests\projects\project-grid.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-grid.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.9, Req 16.2, Req 17.1

---

### M6.G4.T9: Author Automated Axe Accessibility Tests for `ProjectCard` and `ProjectGrid`

**Objective:** Append axe accessibility tests in `tests/projects/project-card.test.tsx` and `project-grid.test.tsx` verifying zero WCAG 2.1 AA violations.

**Acceptance Criteria:**
- ✓ Evaluates `ProjectCard` at `headingLevel={2}`: 0 axe violations
- ✓ Evaluates `ProjectCard` at `headingLevel={3}`: 0 axe violations
- ✓ Evaluates `ProjectGrid`: 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G4.T7 and M6.G4.T8 completed

**Implementation Details:**

Append axe tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Append to project-card.test.tsx
$appendCardAxe = @'

  describe('Axe Accessibility Matrix (Req 16.6)', () => {
    it('reports zero axe violations for ProjectCard at headingLevel 2 and 3', async () => {
      const { axe } = require('vitest-axe');
      const cardData = toProjectCardData(sampleProjectsList[0]);

      const { container: c2 } = render(<ProjectCard project={cardData} headingLevel={2} />);
      expect((await axe(c2)).violations).toHaveLength(0);

      const { container: c3 } = render(<ProjectCard project={cardData} headingLevel={3} />);
      expect((await axe(c3)).violations).toHaveLength(0);
    });
  });
'@

$contentCard = Get-Content "tests\projects\project-card.test.tsx" -Raw
$contentCard = $contentCard -replace "\s*\}\);\s*$", "$appendCardAxe`n});`n"
$contentCard | Set-Content "tests\projects\project-card.test.tsx" -Encoding UTF8

# Append to project-grid.test.tsx
$appendGridAxe = @'

  it('reports zero axe violations for ProjectGrid', async () => {
    const { axe } = require('vitest-axe');
    const { container } = render(<ProjectGrid projects={cards} headingLevel={2} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@

$contentGrid = Get-Content "tests\projects\project-grid.test.tsx" -Raw
$contentGrid = $contentGrid -replace "\s*\}\);\s*$", "$appendGridAxe`n});`n"
$contentGrid | Set-Content "tests\projects\project-grid.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-card.test.tsx tests/projects/project-grid.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M6.G4.T10: Checkpoint — ProjectCard & ProjectGrid Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `ProjectCard` and `ProjectGrid`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs card and grid tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G4.T1 through M6.G4.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/project-card.test.tsx tests/projects/project-grid.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/project-card.test.tsx tests/projects/project-grid.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.4, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\projects\project-card.tsx"
Test-Path "src\components\projects\project-grid.tsx"
Test-Path "tests\projects\project-card.test.tsx"
Test-Path "tests\projects\project-grid.test.tsx"
npm run typecheck
npm run test -- tests/projects/project-card.test.tsx tests/projects/project-grid.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all card and grid tests with return code 0.