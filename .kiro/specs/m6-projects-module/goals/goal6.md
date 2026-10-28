# M6.G6: ProjectBreadcrumb, ProjectHeader, ProjectMetadata, and ProjectLinks

> **Milestone:** M6 — Projects Module  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the four presentational server components for the Project Detail page (`SCR-03`): `ProjectBreadcrumb` in `src/components/projects/project-breadcrumb.tsx`, `ProjectHeader` in `src/components/projects/project-header.tsx`, `ProjectMetadata` in `src/components/projects/project-metadata.tsx`, and `ProjectLinks` in `src/components/projects/project-links.tsx`. `ProjectBreadcrumb` renders an accessible `<nav aria-label="Breadcrumb">` containing an ordered list (`<ol>`) with a link to `/projects` and the current project title as non-link text with `aria-current="page"`. `ProjectHeader` renders the page's single `<h1>` tag containing the project title, the M3 `StatusBadge`, the role, and the project timeline (always showing the start date in a `<time dateTime={startedAt}>` element formatted via M5's `formatDisplayDate`, accompanied by a "Completed" time element iff `completedAt !== null`, and omitting any end date while in progress without fabricated dates). `ProjectMetadata` renders an `<h2 id="project-details-heading">` titled "Project details", an `h3` "Technologies" section rendering all technologies via M3 `TagList`, a conditional "Tags" section (omitted when empty), and a conditional "Metrics" `<dl>` rendering `<dt>`/`<dd>` pairs for each measured outcome (omitted when empty) as supplied without rounding or fabrication. `ProjectLinks` renders M3 `ExternalLink` components for valid repository, demo, and documentation URLs under an `<h2>` titled "Project links", rendering `null` when all links are empty and never rendering `#` or disabled placeholders. Enforce zero client components, complete design-token compliance, and file lengths strictly under 300 lines. Validate all components and fast-check Properties 15, 16, and 17 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/projects/project-breadcrumb.tsx` renders `<nav aria-label="Breadcrumb">` with `<ol>`, `<a href="/projects">`, and `<li aria-current="page">{title}</li>`
- ✓ `src/components/projects/project-header.tsx` renders single `<h1>`, `StatusBadge`, role, start date `<time>`, and completion date `<time>` iff `completedAt !== null`
- ✓ While `completedAt === null`, `ProjectHeader` renders "Started {date}" with zero fabricated completion dates (Req 10.5)
- ✓ `src/components/projects/project-metadata.tsx` renders `<h2>Project details</h2>`, all technologies, conditional tags, and conditional metrics `<dl>` in stored order (Req 11.1–11.6)
- ✓ `src/components/projects/project-links.tsx` renders `ExternalLink` items from `getProjectLinks` under `<h2>Project links</h2>`; renders `null` when all URLs are absent or empty (Req 12.1–12.5)
- ✓ `ProjectLinks` never renders an anchor with `href="#"` and assigns unique accessible names (Req 12.4, 12.7)
- ✓ All four components run as server-safe components without `'use client'` and use Semantic_Tokens exclusively
- ✓ Unit, property (Properties 15, 16, 17), and axe accessibility tests in `tests/projects/project-breadcrumb.test.tsx`, `project-header.test.tsx`, `project-metadata.test.tsx`, and `project-links.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 through M6.G5 completed (`projects-text.ts`, `getProjectLinks`, and M5's `formatDisplayDate` available)
- M3 primitives (`StatusBadge`, `TagList`, `ExternalLink`, `Container`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available in `src/components/ui/`
- Target files: `src/components/projects/project-breadcrumb.tsx`, `project-header.tsx`, `project-metadata.tsx`, and `project-links.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G6.T1: Implement `ProjectBreadcrumb` Component (`src/components/projects/project-breadcrumb.tsx`)

**Objective:** Author the accessible breadcrumb navigation component `ProjectBreadcrumb` in `src/components/projects/project-breadcrumb.tsx`.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-breadcrumb.tsx` created
- ✓ Exports `interface ProjectBreadcrumbProps { readonly title: string; }`
- ✓ Exports `ProjectBreadcrumb({ title }: ProjectBreadcrumbProps): JSX.Element`
- ✓ Renders `<nav aria-label={PROJECTS_TEXT.breadcrumbLabel} className="mb-8">`
- ✓ Renders `<ol className="flex flex-wrap items-center gap-2 list-none p-0 m-0 text-small text-text-secondary">`
- ✓ First breadcrumb item is `<Link href="/projects">` labeled `PROJECTS_TEXT.breadcrumbRoot` ("Projects") with `FOCUS_RING`
- ✓ Separator between items is decorative with `aria-hidden="true"`
- ✓ Final breadcrumb item is `<li aria-current="page" className="font-semibold text-text-primary truncate max-w-xs md:max-w-md">{title}</li>`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- Target file: `src/components/projects/project-breadcrumb.tsx`

**Implementation Details:**

Write `src/components/projects/project-breadcrumb.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import { PROJECTS_PATH, PROJECTS_TEXT } from './projects-text';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';

export interface ProjectBreadcrumbProps {
  readonly title: string;
}

/**
 * ProjectBreadcrumb Component
 *
 * Accessible breadcrumb navigation trail with aria-current="page".
 * design.md Section 6.2 & Requirement 15.1. Server component by default (Req 9.1).
 */
export function ProjectBreadcrumb({ title }: ProjectBreadcrumbProps): JSX.Element {
  return (
    <nav aria-label={PROJECTS_TEXT.breadcrumbLabel} className="mb-6">
      <ol className="flex flex-wrap items-center gap-2 list-none p-0 m-0 text-small text-text-secondary">
        <li>
          <Link
            href={PROJECTS_PATH}
            className={cx(
              'hover:text-brand-primary underline-offset-4 hover:underline rounded-sm',
              FOCUS_RING,
              MOTION_FAST
            )}
          >
            {PROJECTS_TEXT.breadcrumbRoot}
          </Link>
        </li>
        <li aria-hidden="true" className="select-none text-border-default">
          /
        </li>
        <li
          aria-current="page"
          className="font-medium text-text-primary truncate max-w-xs md:max-w-md"
        >
          {title}
        </li>
      </ol>
    </nav>
  );
}
'@ | Set-Content "src\components\projects\project-breadcrumb.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-breadcrumb.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 16.7, Req 17.3

---

### M6.G6.T2: Implement `ProjectHeader` Component (`src/components/projects/project-header.tsx`)

**Objective:** Author `ProjectHeader` in `src/components/projects/project-header.tsx` rendering the page's single `<h1>`, status badge, role, and timeline.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-header.tsx` created
- ✓ Exports `interface ProjectHeaderProps` requiring `title`, `status`, `role`, `startedAt`, and `completedAt`
- ✓ Exports `ProjectHeader(props: ProjectHeaderProps): JSX.Element`
- ✓ Renders `<header className="mb-8 pb-8 border-b border-border-default">`
- ✓ Renders `<h1 className="text-heading-1 font-bold text-text-primary tracking-tight mb-4">{title}</h1>` (only `<h1>` on detail page per Req 10.1, 16.7)
- ✓ Renders status badge (`<StatusBadge status={status} />`) and role text
- ✓ Always renders start date inside `<time dateTime={startedAt}>{formatDisplayDate(startedAt)}</time>` labeled "Started"
- ✓ When `completedAt !== null`: renders completion date inside `<time dateTime={completedAt}>{formatDisplayDate(completedAt)}</time>` labeled "Completed"
- ✓ When `completedAt === null`: strictly omits completion element without fabricated end date (Req 10.5)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5 `formatDisplayDate` available in `src/lib/format-date.ts`
- M3 `StatusBadge` available
- Target file: `src/components/projects/project-header.tsx`

**Implementation Details:**

Write `src/components/projects/project-header.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { ProjectStatus, IsoDateString } from '@/types/content';
import { StatusBadge } from '@/components/ui/status-badge';
import { PROJECTS_TEXT } from './projects-text';
import { formatDisplayDate } from '@/lib/format-date';

export interface ProjectHeaderProps {
  readonly title: string;
  readonly status: ProjectStatus;
  readonly role: string;
  readonly startedAt: IsoDateString;
  readonly completedAt: IsoDateString | null;
}

/**
 * ProjectHeader Component
 *
 * Renders the primary case study title, status badge, role, and verified timeline.
 * Contains the only h1 on the detail page (Req 10.1, 16.7).
 * Server component by default (Req 9.1).
 */
export function ProjectHeader({
  title,
  status,
  role,
  startedAt,
  completedAt,
}: ProjectHeaderProps): JSX.Element {
  return (
    <div className="mb-6 pb-6 border-b border-border-default">
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <StatusBadge status={status} />
        <span className="text-small font-medium text-text-secondary">
          Role: {role}
        </span>
      </div>

      <h1 className="text-heading-1 font-bold tracking-tight text-text-primary mb-4">
        {title}
      </h1>

      <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-small text-text-secondary">
        <p>
          <span className="font-medium text-text-primary">
            {PROJECTS_TEXT.startedPrefix}:
          </span>{' '}
          <time dateTime={startedAt}>{formatDisplayDate(startedAt)}</time>
        </p>

        {completedAt !== null && (
          <p>
            <span className="font-medium text-text-primary">
              {PROJECTS_TEXT.completedPrefix}:
            </span>{' '}
            <time dateTime={completedAt}>{formatDisplayDate(completedAt)}</time>
          </p>
        )}
      </div>
    </div>
  );
}
'@ | Set-Content "src\components\projects\project-header.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-header.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 10.6, Req 16.7

---

### M6.G6.T3: Implement `ProjectMetadata` Component (`src/components/projects/project-metadata.tsx`)

**Objective:** Author `ProjectMetadata` in `src/components/projects/project-metadata.tsx` rendering all technologies, conditional tags, and conditional measured outcomes (`<dl>`).

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-metadata.tsx` created
- ✓ Exports `interface ProjectMetadataProps` requiring `technologies: readonly string[]`, `tags: readonly string[]`, `metrics: readonly { label: string; value: string }[]`
- ✓ Exports `ProjectMetadata(props: ProjectMetadataProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="project-details-heading" className="mb-10 p-6 rounded-lg bg-surface border border-border-default">`
- ✓ Renders `<h2 id="project-details-heading" className="text-heading-3 font-semibold text-text-primary mb-6">{PROJECTS_TEXT.detailsHeading}</h2>`
- ✓ Always renders `h3` "Technologies" and M3 `TagList` displaying all project technologies (Req 11.1)
- ✓ Renders `h3` "Tags" and M3 `TagList` iff `tags.length > 0`; omitted completely when empty (Req 11.2, 11.3)
- ✓ Renders `h3` "Metrics" and `<dl>` iff `metrics.length > 0`; omitted completely when empty (Req 11.4, 11.5)
- ✓ Renders metrics as `<dt>{metric.label}</dt>` and `<dd>{metric.value}</dd>` in stored order without value modification (Req 11.6)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- M3 `TagList` available
- Target file: `src/components/projects/project-metadata.tsx`

**Implementation Details:**

Write `src/components/projects/project-metadata.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { TagList } from '@/components/ui/tag-list';
import { PROJECTS_TEXT } from './projects-text';

export interface ProjectMetadataProps {
  readonly technologies: readonly string[];
  readonly tags: readonly string[];
  readonly metrics: readonly { label: string; value: string }[];
}

/**
 * ProjectMetadata Section Component
 *
 * Renders technical stack tags, categorization tags, and measured metrics.
 * design.md Section 6.2 & Requirement 11. Server component by default (Req 9.1).
 */
export function ProjectMetadata({
  technologies,
  tags,
  metrics,
}: ProjectMetadataProps): JSX.Element {
  const hasTags = tags && tags.length > 0;
  const hasMetrics = metrics && metrics.length > 0;

  return (
    <section
      aria-labelledby="project-details-heading"
      className="mb-10 p-6 rounded-lg bg-surface border border-border-default"
    >
      <h2
        id="project-details-heading"
        className="text-heading-3 font-semibold text-text-primary mb-6"
      >
        {PROJECTS_TEXT.detailsHeading}
      </h2>

      <div className="flex flex-col gap-6">
        {/* Technologies (Always present per Req 11.1) */}
        <div>
          <h3 className="text-small font-semibold text-text-secondary uppercase tracking-wider mb-2">
            {PROJECTS_TEXT.technologiesLabel}
          </h3>
          <TagList items={technologies} />
        </div>

        {/* Tags (Conditional per Req 11.2, 11.3) */}
        {hasTags && (
          <div>
            <h3 className="text-small font-semibold text-text-secondary uppercase tracking-wider mb-2">
              {PROJECTS_TEXT.tagsLabel}
            </h3>
            <TagList items={tags} />
          </div>
        )}

        {/* Metrics (Conditional per Req 11.4, 11.5, 11.6) */}
        {hasMetrics && (
          <div>
            <h3 className="text-small font-semibold text-text-secondary uppercase tracking-wider mb-3">
              {PROJECTS_TEXT.metricsLabel}
            </h3>
            <dl className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {metrics.map((metric) => (
                <div
                  key={metric.label}
                  className="p-3 rounded-md bg-page border border-border-default"
                >
                  <dt className="text-caption text-text-secondary mb-1">
                    {metric.label}
                  </dt>
                  <dd className="text-heading-4 font-bold text-brand-primary">
                    {metric.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        )}
      </div>
    </section>
  );
}
'@ | Set-Content "src\components\projects\project-metadata.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-metadata.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.5, Req 11.6, Req 16.7

---

### M6.G6.T4: Implement `ProjectLinks` Component (`src/components/projects/project-links.tsx`)

**Objective:** Author `ProjectLinks` in `src/components/projects/project-links.tsx` rendering external repository, demo, and docs links, returning `null` when all URLs are absent.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-links.tsx` created
- ✓ Exports `interface ProjectLinksProps { readonly project: Pick<Project, 'repositoryUrl' | 'liveDemoUrl' | 'documentationUrl'>; }`
- ✓ Exports `ProjectLinks({ project }: ProjectLinksProps): JSX.Element | null`
- ✓ Calls `getProjectLinks(project)` to extract valid link items
- ✓ If `links.length === 0`: returns `null` (renders zero elements, including heading, per Req 12.5)
- ✓ If `links.length > 0`: renders `<section aria-labelledby="project-links-heading" className="mb-10">`
- ✓ Renders `<h2 id="project-links-heading" className="text-heading-3 font-semibold text-text-primary mb-4">{PROJECTS_TEXT.linksHeading}</h2>`
- ✓ Renders each item using M3 `ExternalLink` (`target="_blank"`, `rel="noopener noreferrer"`)
- ✓ Strictly omits anchors with `href="#"` or disabled placeholder buttons (Req 12.4)
- ✓ Assigns unique accessible link names within the section (Req 12.7)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G3 completed (`getProjectLinks` in `src/lib/projects/get-project-links.ts`)
- M3 `ExternalLink` available
- Target file: `src/components/projects/project-links.tsx`

**Implementation Details:**

Write `src/components/projects/project-links.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { Project } from '@/types/content';
import { ExternalLink } from '@/components/ui/external-link';
import { PROJECTS_TEXT } from './projects-text';
import { getProjectLinks } from '@/lib/projects/get-project-links';

export interface ProjectLinksProps {
  readonly project: Pick<Project, 'repositoryUrl' | 'liveDemoUrl' | 'documentationUrl'>;
}

/**
 * ProjectLinks Section Component
 *
 * Renders verified external links (Repository, Live demo, Documentation).
 * Returns null if no links are configured (Req 12.1-12.7).
 * Server component by default (Req 9.1).
 */
export function ProjectLinks({ project }: ProjectLinksProps): JSX.Element | null {
  const links = getProjectLinks(project);

  if (links.length === 0) {
    return null; // Omit completely per Req 12.5
  }

  return (
    <section aria-labelledby="project-links-heading" className="mb-10">
      <h2
        id="project-links-heading"
        className="text-heading-3 font-semibold text-text-primary mb-4"
      >
        {PROJECTS_TEXT.linksHeading}
      </h2>

      <div className="flex flex-wrap items-center gap-4">
        {links.map((link) => (
          <ExternalLink
            key={link.key}
            href={link.href}
            className="text-body font-medium"
          >
            {link.label}
          </ExternalLink>
        ))}
      </div>
    </section>
  );
}
'@ | Set-Content "src\components\projects\project-links.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-links.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.3, Req 12.4, Req 12.5, Req 12.6, Req 12.7

---

### M6.G6.T5: Author Unit Tests for `ProjectBreadcrumb` (`tests/projects/project-breadcrumb.test.tsx`)

**Objective:** Create `tests/projects/project-breadcrumb.test.tsx` verifying accessible `nav`, link destination to `/projects`, and current page item.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-breadcrumb.test.tsx` created
- ✓ Tests `<nav>` has accessible label "Breadcrumb"
- ✓ Tests first item links to `/projects` with text "Projects"
- ✓ Tests final item has `aria-current="page"` and matches project title
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G6.T1 completed
- Target file: `tests/projects/project-breadcrumb.test.tsx`

**Implementation Details:**

Write `tests/projects/project-breadcrumb.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProjectBreadcrumb } from '@/components/projects/project-breadcrumb';

describe('ProjectBreadcrumb Component (Req 15.1)', () => {
  it('renders accessible breadcrumb nav with link to /projects and current title', () => {
    render(<ProjectBreadcrumb title="Alpha Pipeline Core" />);

    const nav = screen.getByRole('navigation', { name: 'Breadcrumb' });
    expect(nav).toBeDefined();

    const rootLink = screen.getByRole('link', { name: 'Projects' });
    expect(rootLink.getAttribute('href')).toBe('/projects');

    const currentItem = screen.getByText('Alpha Pipeline Core');
    expect(currentItem.getAttribute('aria-current')).toBe('page');
  });
});
'@ | Set-Content "tests\projects\project-breadcrumb.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-breadcrumb.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 17.1

---

### M6.G6.T6: Author Unit & Property-Based Tests for `ProjectHeader` (Property 15)

**Objective:** Create `tests/projects/project-header.test.tsx` verifying single `<h1>`, role, and timeline display across completed and in-progress states, accompanied by Property 15 test.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-header.test.tsx` created
- ✓ Tests single `<h1>` strictly equals title
- ✓ Tests in-progress project displays "Started" date and zero completion date
- ✓ Tests completed project displays both "Started" and "Completed" dates
- ✓ Implements Property 15 test ($\ge 100$ runs with `fast-check`): single `<h1>`, role present, started `<time>` always present, completed `<time>` present iff `completedAt !== null`
- ✓ Tagged: `Feature: m6-projects-module, Property 15: header timeline reflects completion`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G6.T2 completed
- Arbitraries in `tests/fixtures/projects-arbitraries.ts`
- Target file: `tests/projects/project-header.test.tsx`

**Implementation Details:**

Write `tests/projects/project-header.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import fc from 'fast-check';
import { ProjectHeader } from '@/components/projects/project-header';
import { sampleProjectsList, inProgressProject } from '../fixtures/projects-data';
import { arbProject } from '../fixtures/projects-arbitraries';

describe('ProjectHeader Component (Req 10)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('renders single h1, role, and both Started/Completed dates when completed', () => {
      const p = sampleProjectsList[0];
      render(
        <ProjectHeader
          title={p.title}
          status={p.status}
          role={p.role}
          startedAt={p.startedAt}
          completedAt={p.completedAt}
        />
      );

      const headings = screen.getAllByRole('heading', { level: 1 });
      expect(headings.length).toBe(1);
      expect(headings[0].textContent).toBe(p.title);

      expect(screen.getByText(/Role: Lead Architect/)).toBeDefined();
      expect(screen.getByText(/Started:/)).toBeDefined();
      expect(screen.getByText('January 10, 2025')).toBeDefined();
      expect(screen.getByText(/Completed:/)).toBeDefined();
      expect(screen.getByText('June 15, 2025')).toBeDefined();
    });

    it('renders only Started date and zero Completed date when completedAt is null', () => {
      const p = inProgressProject;
      render(
        <ProjectHeader
          title={p.title}
          status={p.status}
          role={p.role}
          startedAt={p.startedAt}
          completedAt={p.completedAt}
        />
      );

      expect(screen.getByText(/Started:/)).toBeDefined();
      expect(screen.queryByText(/Completed:/)).toBeNull();
    });
  });

  describe('Property-Based Invariants (Property 15)', () => {
    it('Feature: m6-projects-module, Property 15: header timeline reflects completion for any project', () => {
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(arbProject, (p) => {
          cleanup();
          render(
            <ProjectHeader
              title={p.title}
              status={p.status}
              role={p.role}
              startedAt={p.startedAt}
              completedAt={p.completedAt}
            />
          );

          // 1. Single h1
          const h1s = screen.getAllByRole('heading', { level: 1 });
          expect(h1s.length).toBe(1);
          expect(h1s[0].textContent).toBe(p.title);

          // 2. Started time element always present
          const startedTime = document.querySelector(`time[datetime="${p.startedAt}"]`);
          expect(startedTime).not.toBeNull();

          // 3. Completed time element present iff completedAt is non-null
          if (p.completedAt !== null) {
            const completedTime = document.querySelector(`time[datetime="${p.completedAt}"]`);
            expect(completedTime).not.toBeNull();
            expect(screen.getByText(/Completed:/)).toBeDefined();
          } else {
            expect(screen.queryByText(/Completed:/)).toBeNull();
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\project-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-header.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 16.7, Req 17.2

---

### M6.G6.T7: Author Unit & Property-Based Tests for `ProjectMetadata` (Property 16)

**Objective:** Create `tests/projects/project-metadata.test.tsx` verifying conditional tags and metrics rendering, accompanied by Property 16 test.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-metadata.test.tsx` created
- ✓ Tests all technologies are rendered
- ✓ Tests tags section is rendered when non-empty, omitted when empty
- ✓ Tests metrics `<dl>` is rendered when non-empty, omitted when empty
- ✓ Implements Property 16 test ($\ge 100$ runs with `fast-check`): technologies always present, tags present iff non-empty, metrics present iff non-empty
- ✓ Tagged: `Feature: m6-projects-module, Property 16: metadata sections render all data and omit empty groups`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G6.T3 completed
- Target file: `tests/projects/project-metadata.test.tsx`

**Implementation Details:**

Write `tests/projects/project-metadata.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import fc from 'fast-check';
import { ProjectMetadata } from '@/components/projects/project-metadata';
import { sampleProjectsList, emptyTagsMetricsProject } from '../fixtures/projects-data';

describe('ProjectMetadata Component (Req 11)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('renders section heading h2, technologies, tags, and metrics dl', () => {
      const p = sampleProjectsList[0];
      render(
        <ProjectMetadata
          technologies={p.technologies}
          tags={p.tags}
          metrics={p.metrics}
        />
      );

      expect(screen.getByRole('heading', { level: 2, name: 'Project details' })).toBeDefined();
      expect(screen.getByText('Technologies')).toBeDefined();
      expect(screen.getByText('Tags')).toBeDefined();
      expect(screen.getByText('Metrics')).toBeDefined();

      expect(screen.getByText('Latency')).toBeDefined();
      expect(screen.getByText('<5ms')).toBeDefined();
    });

    it('omits Tags and Metrics sections when arrays are empty', () => {
      const p = emptyTagsMetricsProject;
      render(
        <ProjectMetadata
          technologies={p.technologies}
          tags={p.tags}
          metrics={p.metrics}
        />
      );

      expect(screen.getByText('Technologies')).toBeDefined();
      expect(screen.queryByText('Tags')).toBeNull();
      expect(screen.queryByText('Metrics')).toBeNull();
    });
  });

  describe('Property-Based Invariants (Property 16)', () => {
    it('Feature: m6-projects-module, Property 16: metadata sections render all data and omit empty groups for any props', () => {
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.array(fc.string({ minLength: 2, maxLength: 10 }), { minLength: 1, maxLength: 5 }),
          fc.array(fc.string({ minLength: 2, maxLength: 10 }), { maxLength: 3 }),
          fc.array(
            fc.record({
              label: fc.string({ minLength: 2, maxLength: 10 }),
              value: fc.string({ minLength: 2, maxLength: 10 }),
            }),
            { maxLength: 3 }
          ),
          (technologies, tags, metrics) => {
            cleanup();
            render(
              <ProjectMetadata
                technologies={technologies}
                tags={tags}
                metrics={metrics}
              />
            );

            // 1. Technologies always present
            expect(screen.getByText('Technologies')).toBeDefined();

            // 2. Tags conditional
            if (tags.length > 0) {
              expect(screen.getByText('Tags')).toBeDefined();
            } else {
              expect(screen.queryByText('Tags')).toBeNull();
            }

            // 3. Metrics conditional
            if (metrics.length > 0) {
              expect(screen.getByText('Metrics')).toBeDefined();
            } else {
              expect(screen.queryByText('Metrics')).toBeNull();
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\project-metadata.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-metadata.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.5, Req 11.6, Req 17.2

---

### M6.G6.T8: Author Unit & Property-Based Tests for `ProjectLinks` (Property 17)

**Objective:** Create `tests/projects/project-links.test.tsx` verifying external link rendering and null return on empty URLs, accompanied by Property 17 test.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-links.test.tsx` created
- ✓ Tests renders Repository, Live demo, and Documentation links with correct `href`
- ✓ Tests returns `null` when all link URLs are null or empty (Req 12.5)
- ✓ Tests never renders an anchor with `href="#"` (Req 12.4)
- ✓ Implements Property 17 test ($\ge 100$ runs with `fast-check`): links appear only for real URLs, no `#` anchors, null render on empty
- ✓ Tagged: `Feature: m6-projects-module, Property 17: project links appear only for real URLs`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G6.T4 completed
- Target file: `tests/projects/project-links.test.tsx`

**Implementation Details:**

Write `tests/projects/project-links.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import fc from 'fast-check';
import { ProjectLinks } from '@/components/projects/project-links';
import { sampleProjectsList, noLinksProject } from '../fixtures/projects-data';

describe('ProjectLinks Component (Req 12)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('renders ExternalLink for each configured URL under h2 Project links', () => {
      const p = sampleProjectsList[0];
      render(<ProjectLinks project={p} />);

      expect(screen.getByRole('heading', { level: 2, name: 'Project links' })).toBeDefined();

      const repoLink = screen.getByRole('link', { name: /Repository/ });
      expect(repoLink.getAttribute('href')).toBe(p.repositoryUrl);
      expect(repoLink.getAttribute('target')).toBe('_blank');

      const demoLink = screen.getByRole('link', { name: /Live demo/ });
      expect(demoLink.getAttribute('href')).toBe(p.liveDemoUrl);

      const docsLink = screen.getByRole('link', { name: /Documentation/ });
      expect(docsLink.getAttribute('href')).toBe(p.documentationUrl);
    });

    it('returns null and renders zero elements when all links are null or empty', () => {
      const { container } = render(<ProjectLinks project={noLinksProject} />);
      expect(container.firstChild).toBeNull();
      expect(screen.queryByRole('heading', { level: 2, name: 'Project links' })).toBeNull();
    });
  });

  describe('Property-Based Invariants (Property 17)', () => {
    it('Feature: m6-projects-module, Property 17: project links appear only for real URLs and never render # anchors', () => {
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.constantFrom('https://github.com/repo', '   ', null),
          fc.constantFrom('https://demo.example.com', null),
          fc.constantFrom('https://docs.example.com', null),
          (repoUrl, demoUrl, docsUrl) => {
            cleanup();
            const { container } = render(
              <ProjectLinks
                project={{
                  repositoryUrl: repoUrl,
                  liveDemoUrl: demoUrl,
                  documentationUrl: docsUrl,
                }}
              />
            );

            const hasValidRepo = typeof repoUrl === 'string' && repoUrl.trim().length > 0;
            const hasValidDemo = typeof demoUrl === 'string' && demoUrl.trim().length > 0;
            const hasValidDocs = typeof docsUrl === 'string' && docsUrl.trim().length > 0;
            const expectedCount = [hasValidRepo, hasValidDemo, hasValidDocs].filter(Boolean).length;

            if (expectedCount === 0) {
              expect(container.firstChild).toBeNull();
            } else {
              const anchors = container.querySelectorAll('a');
              expect(anchors.length).toBe(expectedCount);
              anchors.forEach((a) => {
                expect(a.getAttribute('href')).not.toBe('#');
                expect(a.getAttribute('href')?.startsWith('https://')).toBe(true);
              });
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\project-links.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-links.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.3, Req 12.4, Req 12.5, Req 12.6, Req 12.7, Req 17.2

---

### M6.G6.T9: Author Axe Accessibility Tests for Detail Components

**Objective:** Append automated axe tests verifying WCAG 2.1 AA compliance across all four detail presentation components.

**Acceptance Criteria:**
- ✓ Evaluates `ProjectBreadcrumb`: 0 axe violations
- ✓ Evaluates `ProjectHeader`: 0 axe violations
- ✓ Evaluates `ProjectMetadata` (populated and empty variants): 0 axe violations
- ✓ Evaluates `ProjectLinks`: 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G6.T5 through M6.G6.T8 completed

**Implementation Details:**

Append axe tests across all 4 test files using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. ProjectBreadcrumb axe
$appendBcAxe = @'

  it('reports zero axe violations for ProjectBreadcrumb', async () => {
    const { axe } = require('vitest-axe');
    const { container } = render(<ProjectBreadcrumb title="Alpha Pipeline Core" />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@
$contentBc = Get-Content "tests\projects\project-breadcrumb.test.tsx" -Raw
$contentBc = $contentBc -replace "\s*\}\);\s*$", "$appendBcAxe`n});`n"
$contentBc | Set-Content "tests\projects\project-breadcrumb.test.tsx" -Encoding UTF8

# 2. ProjectHeader axe
$appendHdAxe = @'

  it('reports zero axe violations for ProjectHeader', async () => {
    const { axe } = require('vitest-axe');
    const p = sampleProjectsList[0];
    const { container } = render(
      <ProjectHeader
        title={p.title}
        status={p.status}
        role={p.role}
        startedAt={p.startedAt}
        completedAt={p.completedAt}
      />
    );
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@
$contentHd = Get-Content "tests\projects\project-header.test.tsx" -Raw
$contentHd = $contentHd -replace "\s*\}\);\s*$", "$appendHdAxe`n});`n"
$contentHd | Set-Content "tests\projects\project-header.test.tsx" -Encoding UTF8

# 3. ProjectMetadata axe
$appendMdAxe = @'

  it('reports zero axe violations for ProjectMetadata', async () => {
    const { axe } = require('vitest-axe');
    const p = sampleProjectsList[0];
    const { container } = render(
      <ProjectMetadata
        technologies={p.technologies}
        tags={p.tags}
        metrics={p.metrics}
      />
    );
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@
$contentMd = Get-Content "tests\projects\project-metadata.test.tsx" -Raw
$contentMd = $contentMd -replace "\s*\}\);\s*$", "$appendMdAxe`n});`n"
$contentMd | Set-Content "tests\projects\project-metadata.test.tsx" -Encoding UTF8

# 4. ProjectLinks axe
$appendLkAxe = @'

  it('reports zero axe violations for ProjectLinks', async () => {
    const { axe } = require('vitest-axe');
    const { container } = render(<ProjectLinks project={sampleProjectsList[0]} />);
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });
'@
$contentLk = Get-Content "tests\projects\project-links.test.tsx" -Raw
$contentLk = $contentLk -replace "\s*\}\);\s*$", "$appendLkAxe`n});`n"
$contentLk | Set-Content "tests\projects\project-links.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-breadcrumb.test.tsx tests/projects/project-header.test.tsx tests/projects/project-metadata.test.tsx tests/projects/project-links.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M6.G6.T10: Checkpoint — Detail Components Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `ProjectBreadcrumb`, `ProjectHeader`, `ProjectMetadata`, and `ProjectLinks`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all four G6 test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G6.T1 through M6.G6.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/project-breadcrumb.test.tsx tests/projects/project-header.test.tsx tests/projects/project-metadata.test.tsx tests/projects/project-links.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/project-breadcrumb.test.tsx tests/projects/project-header.test.tsx tests/projects/project-metadata.test.tsx tests/projects/project-links.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.4, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\projects\project-breadcrumb.tsx"
Test-Path "src\components\projects\project-header.tsx"
Test-Path "src\components\projects\project-metadata.tsx"
Test-Path "src\components\projects\project-links.tsx"
npm run typecheck
npm run test -- tests/projects/project-breadcrumb.test.tsx tests/projects/project-header.test.tsx tests/projects/project-metadata.test.tsx tests/projects/project-links.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all four detail component test suites with return code 0.