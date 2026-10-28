# M6.G8: Detail Route, Static Params, Metadata, and Static-Output Checks

> **Milestone:** M6 — Projects Module  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete Project Detail route entry point `src/app/projects/[slug]/page.tsx` (`SCR-03`) with static route generation, strict dynamic route disabling, 404 boundary handling, and route metadata derivation. Specifically, export `dynamicParams = false` to guarantee that only known project slugs are rendered at runtime. Export `generateStaticParams()` returning one `{ slug }` entry per project returned by `getProjects()`. Export `generateMetadata` resolving route metadata through `buildProjectDetailMetadata`, invoking `notFound()` if an unknown slug is requested. Implement `ProjectDetailPage` as an async server component loading project data via `getProjectBySlug(slug)` (triggering `notFound()` on falsy returns), fetching all projects via `getProjects()` to resolve related case studies via `selectRelatedProjects`, rendering documentation Markdown through `renderMarkdown`, and orchestrating the case study layout inside M3's `Container` in canonical sequence: `ProjectBreadcrumb` $\rightarrow$ `ProjectHeader` $\rightarrow$ visible summary $\rightarrow$ `ProjectMetadata` $\rightarrow$ `ProjectLinks` (if present) $\rightarrow$ `BuildDocumentation` $\rightarrow$ "Back to projects" link $\rightarrow$ `RelatedProjects` (if present). Enforce zero client components, zero JSON-LD emissions, zero browser APIs or cookies, and zero try/catch blocks swallowing schema validation failures. Validate static route parameters, heading continuities, and Properties 19 and 20 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/app/projects/[slug]/page.tsx` exports `dynamicParams = false` and `generateStaticParams()` returning one `{ slug }` per project from `getProjects()`
- ✓ `generateMetadata` exports route metadata via `buildProjectDetailMetadata(project, site.siteUrl)`, invoking `notFound()` on missing slugs (Req 15.3, 15.8)
- ✓ `ProjectDetailPage` invokes `getProjectBySlug(slug)`, calling `notFound()` if falsy, and resolves related projects via `selectRelatedProjects`
- ✓ Composes components inside M3 `Container` in exact canonical order: `ProjectBreadcrumb`, `ProjectHeader`, summary paragraph, `ProjectMetadata`, `ProjectLinks` (if any), `BuildDocumentation`, "Back to projects" link, and `RelatedProjects` (if any)
- ✓ Renders exactly one `<h1>` (in `ProjectHeader`), all section headings as `<h2>`, card headings as `<h3>`, and zero skipped levels (Req 16.7)
- ✓ Strictly omits JSON-LD structured data script tags (Req 15.7)
- ✓ Renders zero `<header>`, `<footer>`, or `<main>` elements in page markup (M4 RootLayout owns these landmarks per Req 9.8)
- ✓ Unit, structure, and property tests in `tests/projects/detail-page.test.tsx`, `static-params.test.ts`, and `detail-metadata.test.ts` satisfy Properties 19 and 20 ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 through M6.G7 completed (all helpers, components, and M2 loaders available)
- M2 loaders: `getProjects`, `getProjectBySlug`, `getSiteConfig`, `renderMarkdown`
- Target file: `src/app/projects/[slug]/page.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G8.T1: Implement Static Route Scaffold with `generateStaticParams` (`src/app/projects/[slug]/page.tsx`)

**Objective:** Author the initial scaffold of `src/app/projects/[slug]/page.tsx` exporting `dynamicParams = false` and `generateStaticParams`.

**Acceptance Criteria:**
- ✓ Directory `src/app/projects/[slug]/` exists or is created
- ✓ File `src/app/projects/[slug]/page.tsx` created
- ✓ Exports `const dynamicParams = false` (Req 9.3)
- ✓ Exports async function `generateStaticParams(): Promise<{ slug: string }[]>`
- ✓ Calls `getProjects()` and maps to `{ slug: project.slug }` for every returned project (Req 9.2)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M2 `getProjects` available in `src/content/loaders/projects.ts`
- Target file: `src/app/projects/[slug]/page.tsx`

**Implementation Details:**

Write the scaffold of `src/app/projects/[slug]/page.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\app\projects\[slug]")) {
    New-Item -ItemType Directory -Path "src\app\projects\[slug]" -Force | Out-Null
}

@'
import React from 'react';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import Link from 'next/link';
import { getProjects, getProjectBySlug } from '@/content/loaders/projects';
import { getSiteConfig } from '@/content/loaders/site';
import { renderMarkdown } from '@/content/markdown/renderer';
import { Container } from '@/components/ui/container';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { PROJECTS_PATH, PROJECTS_TEXT } from '@/components/projects/projects-text';
import { toProjectCardData } from '@/lib/projects/card-data';
import { selectRelatedProjects } from '@/lib/projects/select-related-projects';
import { buildProjectDetailMetadata } from '@/lib/projects/project-metadata';
import { ProjectBreadcrumb } from '@/components/projects/project-breadcrumb';
import { ProjectHeader } from '@/components/projects/project-header';
import { ProjectMetadata } from '@/components/projects/project-metadata';
import { ProjectLinks } from '@/components/projects/project-links';
import { BuildDocumentation } from '@/components/projects/build-documentation';
import { RelatedProjects } from '@/components/projects/related-projects';

/**
 * Strict static route generation: disallow on-demand dynamic generation (Req 9.3).
 */
export const dynamicParams = false;

/**
 * Prerender all project slugs at build time (Req 9.2).
 */
export async function generateStaticParams(): Promise<{ slug: string }[]> {
  const projects = await getProjects();
  return projects.map((p) => ({
    slug: p.slug,
  }));
}
'@ | Set-Content "src\app\projects\[slug]\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/app/projects/[slug]/page.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3

---

### M6.G8.T2: Implement `generateMetadata` for Project Detail Page

**Objective:** Append `generateMetadata` to `src/app/projects/[slug]/page.tsx` producing route-specific SEO metadata and calling `notFound()` on missing slugs.

**Acceptance Criteria:**
- ✓ Exports `generateMetadata(props: { params: Promise<{ slug: string }> | { slug: string } }): Promise<Metadata>`
- ✓ Awaits `params` to resolve `slug`
- ✓ Calls `getProjectBySlug(slug)` and `getSiteConfig()`
- ✓ If project is falsy, calls `notFound()` (Req 15.8)
- ✓ Returns metadata object formatted via `buildProjectDetailMetadata(project, site.siteUrl)`
- ✓ Derives canonical URL without query string or hash (Req 15.6)
- ✓ Does NOT include JSON-LD structured data (Req 15.7)

**Prerequisites:**
- M6.G8.T1 completed
- Target file: `src/app/projects/[slug]/page.tsx`

**Implementation Details:**

Append `generateMetadata` to `src/app/projects/[slug]/page.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendMeta = @'

interface PageProps {
  params: Promise<{ slug: string }> | { slug: string };
}

/**
 * Generates route-specific metadata for individual project detail page.
 * Triggers notFound() if requested slug does not exist (Req 15.3, 15.6, 15.8).
 */
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const resolvedParams = await params;
  const [project, site] = await Promise.all([
    getProjectBySlug(resolvedParams.slug),
    getSiteConfig(),
  ]);

  if (!project) {
    notFound();
  }

  return buildProjectDetailMetadata(project, site.siteUrl);
}
'@

Add-Content -Path "src\app\projects\[slug]\page.tsx" -Value $appendMeta -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/app/projects/[slug]/page.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.5, Req 15.6, Req 15.7, Req 15.8

---

### M6.G8.T3: Implement `ProjectDetailPage` Component Composition

**Objective:** Complete `src/app/projects/[slug]/page.tsx` with default export `ProjectDetailPage` orchestrating detail sections inside `Container`.

**Acceptance Criteria:**
- ✓ Exports default async function `ProjectDetailPage({ params }: PageProps): Promise<JSX.Element>`
- ✓ Awaits `params.slug` and calls `getProjectBySlug(slug)`
- ✓ If project is falsy, calls `notFound()` so M4 `not-found` renders (Req 9.5)
- ✓ Awaits `allProjects = getProjects()` and derives `relatedProjects = selectRelatedProjects(project, allProjects).map(toProjectCardData)`
- ✓ Awaits `docHtml = renderMarkdown(project.documentation)`
- ✓ Wraps layout in `<Container className="py-12 md:py-16 max-w-4xl">`
- ✓ Renders in strict canonical order: `ProjectBreadcrumb`, `ProjectHeader`, visible summary paragraph, `ProjectMetadata`, `ProjectLinks`, `BuildDocumentation`, "Back to projects" link, and `RelatedProjects`
- ✓ Renders "Back to projects" link with `href="/projects"` and text `HOME_TEXT.backToProjects`
- ✓ Renders zero `<header>`, `<footer>`, or `<main>` elements in markup (Req 9.8)

**Prerequisites:**
- M6.G8.T2 completed
- Target file: `src/app/projects/[slug]/page.tsx`

**Implementation Details:**

Append `ProjectDetailPage` component using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendPage = @'

/**
 * Project Detail Page Route (SCR-03)
 *
 * Full engineering case study layout. Server component by default (Req 9.1).
 */
export default async function ProjectDetailPage({ params }: PageProps): Promise<JSX.Element> {
  const resolvedParams = await params;
  const project = await getProjectBySlug(resolvedParams.slug);

  if (!project) {
    notFound();
  }

  // Load all projects for related project derivation and render documentation
  const [allProjects, docHtml] = await Promise.all([
    getProjects(),
    renderMarkdown(project.documentation),
  ]);

  const relatedCards = selectRelatedProjects(project, allProjects).map(toProjectCardData);

  return (
    <Container className="py-12 md:py-16 max-w-4xl">
      {/* 1. Breadcrumb navigation */}
      <ProjectBreadcrumb title={project.title} />

      {/* 2. Project Header (single h1) */}
      <ProjectHeader
        title={project.title}
        status={project.status}
        role={project.role}
        startedAt={project.startedAt}
        completedAt={project.completedAt}
      />

      {/* 3. Summary positioning paragraph */}
      <p className="text-lead text-text-secondary leading-relaxed mb-8">
        {project.summary}
      </p>

      {/* 4. Project Metadata (Technologies, Tags, Metrics) */}
      <ProjectMetadata
        technologies={project.technologies}
        tags={project.tags}
        metrics={project.metrics}
      />

      {/* 5. Project Links (Repository, Live demo, Docs - omitted if empty) */}
      <ProjectLinks project={project} />

      {/* 6. Build Documentation Markdown */}
      <BuildDocumentation html={docHtml} />

      {/* 7. Back to projects link */}
      <div className="my-10 pt-6 border-t border-border-default">
        <Link
          href={PROJECTS_PATH}
          className={cx(
            'inline-flex items-center text-body font-medium text-brand-primary underline hover:opacity-80 rounded-sm',
            FOCUS_RING,
            MOTION_FAST
          )}
        >
          &larr; {PROJECTS_TEXT.backToProjects}
        </Link>
      </div>

      {/* 8. Related Projects (omitted if empty) */}
      <RelatedProjects projects={relatedCards} />
    </Container>
  );
}
'@

Add-Content -Path "src\app\projects\[slug]\page.tsx" -Value $appendPage -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/app/projects/[slug]/page.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.4, Req 9.5, Req 9.6, Req 9.7, Req 9.8, Req 15.1, Req 15.2, Req 16.3

---

### M6.G8.T4: Audit Detail Route for Zero Client Directives and Prohibited APIs

**Objective:** Audit `src/app/projects/[slug]/page.tsx` ensuring zero `'use client'` statements, zero dynamic headers/cookies, zero `fetch(`, zero browser globals, and zero JSON-LD script tags.

**Acceptance Criteria:**
- ✓ Scans `page.tsx` for `'use client'`
- ✓ Scans `page.tsx` for `headers()`, `cookies()`, `useSearchParams`, `window`, `document`
- ✓ Scans `page.tsx` for `application/ld+json` (Req 15.7)
- ✓ Scans `page.tsx` for `<header`, `<footer`, `<main` (Req 9.8)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G8.T3 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\app\projects\[slug]\page.tsx"
$content = Get-Content $file -Raw
$violations = @()

if ($content -match "['""]use client['""]") { $violations += "Forbidden 'use client' found in $file" }
if ($content -match "\b(headers|cookies|useSearchParams|window|document)\b") { $violations += "Forbidden dynamic/browser API in $file" }
if ($content -match "application\/ld\+json") { $violations += "Forbidden JSON-LD structured data in $file (Req 15.7)" }
if ($content -match "<(header|footer|main)\b") { $violations += "Forbidden shell landmark rendered in $file (Req 9.8)" }

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\app\projects\[slug]\page.tsx"
$content = Get-Content $file -Raw
$violations = @()

if ($content -match "['""]use client['""]") { $violations += "Forbidden 'use client' found in $file" }
if ($content -match "\b(headers|cookies|useSearchParams|window|document)\b") { $violations += "Forbidden dynamic/browser API in $file" }
if ($content -match "application\/ld\+json") { $violations += "Forbidden JSON-LD structured data in $file (Req 15.7)" }
if ($content -match "<(header|footer|main)\b") { $violations += "Forbidden shell landmark rendered in $file (Req 9.8)" }

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.8, Req 15.7, Req 17.3

---

### M6.G8.T5: Author Unit Tests for `ProjectDetailPage` (`tests/projects/detail-page.test.tsx`)

**Objective:** Create `tests/projects/detail-page.test.tsx` verifying route rendering with mocked loaders, 404 behavior, and section ordering.

**Acceptance Criteria:**
- ✓ File `tests/projects/detail-page.test.tsx` created
- ✓ Mocks `getProjects`, `getProjectBySlug`, `getSiteConfig`, `renderMarkdown`
- ✓ Tests rendering populated project: verifies breadcrumb, `<h1>` title, summary, metadata, links, documentation, back link, and related projects
- ✓ Tests unknown slug invokes `notFound()`
- ✓ Tests project with zero related projects omits "Related projects" section
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G8.T3 completed
- Target file: `tests/projects/detail-page.test.tsx`

**Implementation Details:**

Write `tests/projects/detail-page.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import ProjectDetailPage from '@/app/projects/[slug]/page';
import { sampleProjectsList, isolatedTechProject } from '../fixtures/projects-data';
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
vi.mock('next/navigation', () => ({
  notFound: vi.fn(() => {
    throw new Error('NEXT_NOT_FOUND');
  }),
}));

describe('ProjectDetailPage Route (Req 9, 15)', () => {
  beforeEach(async () => {
    const { getProjects, getProjectBySlug } = await import('@/content/loaders/projects');
    const { getSiteConfig } = await import('@/content/loaders/site');
    const { renderMarkdown } = await import('@/content/markdown/renderer');

    vi.mocked(getProjects).mockResolvedValue(sampleProjectsList);
    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);
    vi.mocked(renderMarkdown).mockResolvedValue('<h2>Architecture</h2><p>Notes</p>');
  });

  it('renders complete case study layout in canonical sequence', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    vi.mocked(getProjectBySlug).mockResolvedValue(sampleProjectsList[0]);

    const Page = await ProjectDetailPage({ params: Promise.resolve({ slug: 'alpha-pipeline-core' }) });
    render(Page);

    // 1. Breadcrumb
    expect(screen.getByRole('navigation', { name: 'Breadcrumb' })).toBeDefined();

    // 2. Single h1
    const h1s = screen.getAllByRole('heading', { level: 1 });
    expect(h1s.length).toBe(1);
    expect(h1s[0].textContent).toBe('Alpha Pipeline Core');

    // 3. Summary
    expect(screen.getByText(/High performance specification-driven pipeline/)).toBeDefined();

    // 4. Metadata
    expect(screen.getByRole('heading', { level: 2, name: 'Project details' })).toBeDefined();

    // 5. Links
    expect(screen.getByRole('heading', { level: 2, name: 'Project links' })).toBeDefined();

    // 6. Build docs
    expect(screen.getByRole('heading', { level: 2, name: 'Build documentation' })).toBeDefined();

    // 7. Back to projects link
    expect(screen.getByRole('link', { name: /Back to projects/ })).toBeDefined();

    // 8. Related projects
    expect(screen.getByRole('heading', { level: 2, name: 'Related projects' })).toBeDefined();
  });

  it('calls notFound when project slug does not exist', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    vi.mocked(getProjectBySlug).mockResolvedValue(null);

    await expect(
      ProjectDetailPage({ params: Promise.resolve({ slug: 'non-existent-slug' }) })
    ).rejects.toThrow('NEXT_NOT_FOUND');
  });

  it('omits Related projects section when project shares zero technologies', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    vi.mocked(getProjectBySlug).mockResolvedValue(isolatedTechProject);

    const Page = await ProjectDetailPage({ params: Promise.resolve({ slug: isolatedTechProject.slug }) });
    render(Page);

    expect(screen.queryByRole('heading', { level: 2, name: 'Related projects' })).toBeNull();
  });
});
'@ | Set-Content "tests\projects\detail-page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/detail-page.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.4, Req 9.5, Req 9.6, Req 9.7, Req 14.7, Req 15.1, Req 15.2, Req 17.1

---

### M6.G8.T6: Author Property-Based Test for Detail Page Structure & Heading Hierarchy (Property 19)

**Objective:** Append Property 19 test in `tests/projects/detail-page.test.tsx` validating unbroken heading hierarchy, landmark boundaries, and component sequence.

**Acceptance Criteria:**
- ✓ Implements Property 19 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 19: detail page structure and heading hierarchy`
- ✓ Asserts exactly one `<h1>` in rendered output
- ✓ Asserts zero `<header>`, `<footer>`, or `<main>` elements in page markup
- ✓ Asserts heading hierarchy never skips levels (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`)
- ✓ Asserts "Related projects" `<h2>` is present iff related cards exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G8.T5 completed
- Target file: `tests/projects/detail-page.test.tsx`

**Implementation Details:**

Append Property 19 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendProp19 = @'

  describe('Property-Based Invariants (Property 19)', () => {
    it('Feature: m6-projects-module, Property 19: detail page structure and heading hierarchy unbroken for any project', async () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProject, arbProjectsList } = require('../fixtures/projects-arbitraries');
      const { getProjectBySlug, getProjects } = await import('@/content/loaders/projects');
      const { renderMarkdown } = await import('@/content/markdown/renderer');

      fc.assert(
        fc.asyncProperty(arbProject, arbProjectsList, async (project: any, allProjects: any) => {
          cleanup();
          vi.mocked(getProjectBySlug).mockResolvedValue(project);
          vi.mocked(getProjects).mockResolvedValue(allProjects);
          vi.mocked(renderMarkdown).mockResolvedValue('<h2 id="intro">Intro</h2><p>Body</p>');

          const Page = await ProjectDetailPage({ params: Promise.resolve({ slug: project.slug }) });
          const { container } = render(Page);

          // 1. Single h1
          const h1s = container.querySelectorAll('h1');
          expect(h1s.length).toBe(1);

          // 2. Zero shell landmarks inside page
          expect(container.querySelectorAll('header, footer, main').length).toBe(0);

          // 3. Heading level hierarchy continuity
          const headings = Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6'));
          let currentLevel = 0;
          for (const h of headings) {
            const level = parseInt(h.tagName.substring(1), 10);
            if (currentLevel > 0) {
              expect(level).toBeLessThanOrEqual(currentLevel + 1);
            }
            currentLevel = level;
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\detail-page.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendProp19`n});`n"
$content | Set-Content "tests\projects\detail-page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/detail-page.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.6, Req 9.7, Req 9.8, Req 13.2, Req 14.6, Req 14.7, Req 15.1, Req 15.2, Req 16.7, Req 17.2

---

### M6.G8.T7: Author Unit & Property-Based Tests for Static Params (Property 20)

**Objective:** Create `tests/projects/static-params.test.ts` verifying that `generateStaticParams()` returns exact slugs for all projects and asserts `dynamicParams === false`.

**Acceptance Criteria:**
- ✓ File `tests/projects/static-params.test.ts` created
- ✓ Imports `generateStaticParams` and `dynamicParams` from `@/app/projects/[slug]/page`
- ✓ Asserts `dynamicParams === false` (Req 9.3)
- ✓ Implements Property 20 test ($\ge 100$ runs with `fast-check`): `generateStaticParams()` returns an array whose slugs equal input slugs exactly, with one entry per project
- ✓ Tagged: `Feature: m6-projects-module, Property 20: static params cover every project`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G8.T1 completed
- Target file: `tests/projects/static-params.test.ts`

**Implementation Details:**

Write `tests/projects/static-params.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect, vi } from 'vitest';
import fc from 'fast-check';
import { generateStaticParams, dynamicParams } from '@/app/projects/[slug]/page';
import { arbProjectsList } from '../fixtures/projects-arbitraries';

vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
  getProjectBySlug: vi.fn(),
}));

describe('generateStaticParams & dynamicParams Contract (Req 9.2, 9.3)', () => {
  it('dynamicParams is strictly false to prevent on-demand SSR', () => {
    expect(dynamicParams).toBe(false);
  });

  describe('Property-Based Invariants (Property 20)', () => {
    it('Feature: m6-projects-module, Property 20: static params cover every project for any project collection', async () => {
      const { getProjects } = await import('@/content/loaders/projects');

      await fc.assert(
        fc.asyncProperty(arbProjectsList, async (projects) => {
          vi.mocked(getProjects).mockResolvedValue(projects);

          const params = await generateStaticParams();
          expect(params.length).toBe(projects.length);

          const expectedSlugs = projects.map((p) => p.slug);
          const actualSlugs = params.map((param) => param.slug);
          expect(actualSlugs).toEqual(expectedSlugs);
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\static-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/static-params.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.2, Req 9.3, Req 17.2

---

### M6.G8.T8: Author Unit Tests for Detail Route Metadata (`tests/projects/detail-metadata.test.ts`)

**Objective:** Create `tests/projects/detail-metadata.test.ts` verifying `generateMetadata` output for project detail routes, canonical URL construction without queries, and 404 invocation on invalid slugs.

**Acceptance Criteria:**
- ✓ File `tests/projects/detail-metadata.test.ts` created
- ✓ Tests `generateMetadata` produces expected title, summary description, and article Open Graph type
- ✓ Tests canonical URL matches `https://example.vercel.app/projects/{slug}` with zero query parameters
- ✓ Tests unknown slug invokes `notFound()` (Req 15.8)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G8.T2 completed
- Target file: `tests/projects/detail-metadata.test.ts`

**Implementation Details:**

Write `tests/projects/detail-metadata.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { generateMetadata } from '@/app/projects/[slug]/page';
import { sampleProjectsList } from '../fixtures/projects-data';
import { sampleSiteConfig } from '../fixtures/home-data';

vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
  getProjectBySlug: vi.fn(),
}));
vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(),
}));
vi.mock('next/navigation', () => ({
  notFound: vi.fn(() => {
    throw new Error('NEXT_NOT_FOUND');
  }),
}));

describe('Project Detail generateMetadata (Req 15)', () => {
  beforeEach(async () => {
    const { getSiteConfig } = await import('@/content/loaders/site');
    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);
  });

  it('derives metadata from project and siteUrl without query string', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    const p = sampleProjectsList[0];
    vi.mocked(getProjectBySlug).mockResolvedValue(p);

    const meta = await generateMetadata({ params: Promise.resolve({ slug: p.slug }) });

    expect(meta.title).toBe(p.title);
    expect(meta.description).toBe(p.summary);
    expect(meta.alternates?.canonical).toBe(`https://example.vercel.app/projects/${p.slug}`);
    expect(meta.openGraph?.type).toBe('article');
  });

  it('calls notFound when generating metadata for an unknown slug', async () => {
    const { getProjectBySlug } = await import('@/content/loaders/projects');
    vi.mocked(getProjectBySlug).mockResolvedValue(null);

    await expect(
      generateMetadata({ params: Promise.resolve({ slug: 'unknown-slug' }) })
    ).rejects.toThrow('NEXT_NOT_FOUND');
  });
});
'@ | Set-Content "tests\projects\detail-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/detail-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.5, Req 15.6, Req 15.8

---

### M6.G8.T9: Verify Source Hygiene of `[slug]/page.tsx`

**Objective:** Audit `src/app/projects/[slug]/page.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file length strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ File strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G8.T3 completed

**Implementation Details:**

Execute hygiene check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\app\projects\[slug]\page.tsx"
$content = Get-Content $file -Raw
$lines = (Get-Content $file).Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and ($lines -lt 300)) {
    "PASS"
} else {
    Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    "FAIL"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\app\projects\[slug]\page.tsx"
$content = Get-Content $file -Raw
$lines = (Get-Content $file).Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and ($lines -lt 300)) {
    "PASS"
} else {
    Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    "FAIL"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 9.1, Req 16.1, Req 17.3, Req 17.4

---

### M6.G8.T10: Checkpoint — Detail Route Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across detail route components, static params, and metadata modules.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all G8 test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G8.T1 through M6.G8.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/detail-page.test.tsx tests/projects/static-params.test.ts tests/projects/detail-metadata.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/detail-page.test.tsx tests/projects/static-params.test.ts tests/projects/detail-metadata.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.4, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\app\projects\[slug]\page.tsx"
Test-Path "tests\projects\detail-page.test.tsx"
Test-Path "tests\projects\static-params.test.ts"
Test-Path "tests\projects\detail-metadata.test.ts"
npm run typecheck
npm run test -- tests/projects/detail-page.test.tsx tests/projects/static-params.test.ts tests/projects/detail-metadata.test.ts
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all detail route test suites with return code 0.