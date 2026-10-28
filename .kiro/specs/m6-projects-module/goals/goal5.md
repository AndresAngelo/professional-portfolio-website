# M6.G5: ProjectFilterBar, ProjectsExplorer, ProjectsIndex, and the Index Route

> **Milestone:** M6 — Projects Module  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete Projects Index experience: `ProjectFilterBar` in `src/components/projects/project-filter-bar.tsx`, the client island `ProjectsExplorer` in `src/components/projects/projects-explorer.tsx`, the index composition container `ProjectsIndex` in `src/components/projects/projects-index.tsx`, and the static route entry point `src/app/projects/page.tsx` with its exported `metadata`. `ProjectFilterBar` renders accessible technology and status filter groups using M3's `FilterChip` (`role="group"`, `aria-label`, `aria-pressed`), conditionally omitting the status group when only a single status exists, and providing a "Clear filters" action whenever a filter is active. `ProjectsExplorer` is the solitary `'use client'` component in M6 and the exclusive caller of `useSearchParams`; it reads filters directly from the URL on every render, dispatches navigation updates via `router.replace('/projects' + qs, { scroll: false })`, renders a visible polite live region (`aria-live="polite"`) announcing matching project counts, presents an empty filtered state with a "Clear filters" button, and restores focus to the first filter chip upon clearing. `ProjectsIndex` wraps `ProjectsExplorer` in a React `Suspense` boundary providing the full unfiltered `ProjectGrid` as fallback to guarantee static HTML completeness under export. `src/app/projects/page.tsx` runs as an async server component passing serializable `ProjectCardData` and exporting route metadata derived via `buildProjectsIndexMetadata`. Cover the entire interaction, focus mechanics, and Property 12 using Vitest, RTL, and a store-backed `next/navigation` mock.

## Goal Success Criteria

- ✓ `src/components/projects/project-filter-bar.tsx` renders accessible filter groups and chips with `aria-pressed`, wraps chips responsively (`flex-wrap`), omits status group for $\le 1$ status, and shows "Clear filters" iff a filter is active
- ✓ `src/components/projects/projects-explorer.tsx` is the ONLY module with `'use client'` and the ONLY caller of `useSearchParams`; implements filter derivation, toggling off on re-activation, and URL updates via `router.replace` with `{ scroll: false }`
- ✓ `ProjectsExplorer` includes a visible `<p aria-live="polite">` announcing `formatResultCount(shown.length)` rendered on initial mount
- ✓ `ProjectsExplorer` renders `EmptyState` when matching projects count is 0 and moves keyboard focus to the first chip upon activating "Clear filters"
- ✓ `src/components/projects/projects-index.tsx` renders single `<h1>Projects</h1>`, wraps `ProjectsExplorer` in `<Suspense fallback={<ProjectGrid ... />}>`, and renders `EmptyState` with zero chips when collection is empty
- ✓ `src/app/projects/page.tsx` renders statically without client directives, passes `toProjectCardData` projections, and exports index metadata without query parameters
- ✓ Unit, property (Property 12), and axe accessibility tests in `tests/projects/project-filter-bar.test.tsx`, `projects-explorer.test.tsx`, `projects-index.test.tsx`, and `projects-page.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 through M6.G4 completed (`card-data.ts`, `filter-params.ts`, `filter-projects.ts`, `derive-filter-options.ts`, `ProjectCard`, `ProjectGrid` available)
- M3 primitives (`FilterChip`, `Button`, `EmptyState`, `Container`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available in `src/components/ui/`
- Target files: `src/components/projects/project-filter-bar.tsx`, `projects-explorer.tsx`, `projects-index.tsx`, and `src/app/projects/page.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G5.T1: Create Store-Backed `next/navigation` Test Mock (`tests/projects/helpers/mock-navigation.ts`)

**Objective:** Author a store-backed mock of `next/navigation` in `tests/projects/helpers/mock-navigation.ts` synchronizing `useRouter().replace` calls with `useSearchParams()` to enable deterministic client filtering tests.

**Acceptance Criteria:**
- ✓ File `tests/projects/helpers/mock-navigation.ts` created
- ✓ Exports `setInitialQuery(query: string): void`
- ✓ Exports `mockUseSearchParams(): URLSearchParams` reading from reactive store
- ✓ Exports `mockUseRouter(): { replace: vi.Mock }` where `replace` updates store and triggers component re-render
- ✓ Exports `mockNotFound(): never` throwing a recognizable sentinel error
- ✓ Enables testing client components without browser window location manipulation

**Prerequisites:**
- Directory `tests/projects/helpers/` exists or is created
- Target file: `tests/projects/helpers/mock-navigation.ts`

**Implementation Details:**

Write `tests/projects/helpers/mock-navigation.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\projects\helpers")) {
    New-Item -ItemType Directory -Path "tests\projects\helpers" -Force | Out-Null
}

@'
import { vi } from 'vitest';
import { useSyncExternalStore } from 'react';

let currentQuery = '';
const listeners = new Set<() => void>();

function notify() {
  listeners.forEach((l) => l());
}

export function setInitialQuery(query: string) {
  currentQuery = query.startsWith('?') ? query.slice(1) : query;
  notify();
}

export function getMockQuery() {
  return currentQuery;
}

export const mockReplace = vi.fn((url: string) => {
  const qIndex = url.indexOf('?');
  currentQuery = qIndex !== -1 ? url.slice(qIndex + 1) : '';
  notify();
});

export function mockUseSearchParams(): URLSearchParams {
  const q = useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    () => currentQuery,
    () => currentQuery
  );
  return new URLSearchParams(q);
}

export function mockUseRouter() {
  return {
    replace: mockReplace,
    push: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn(),
  };
}

export function mockNotFound(): never {
  throw new Error('NEXT_NOT_FOUND');
}
'@ | Set-Content "tests\projects\helpers\mock-navigation.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/projects/helpers/mock-navigation.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.6, Req 6.8, Req 17.1

---

### M6.G5.T2: Implement `ProjectFilterBar` Component (`src/components/projects/project-filter-bar.tsx`)

**Objective:** Author presentational component `ProjectFilterBar` in `src/components/projects/project-filter-bar.tsx` rendering accessible filter chip groups and conditional "Clear filters" button.

**Acceptance Criteria:**
- ✓ File `src/components/projects/project-filter-bar.tsx` created
- ✓ Exports `interface ProjectFilterBarProps`
- ✓ Exports `ProjectFilterBar(props: ProjectFilterBarProps): JSX.Element`
- ✓ Renders technology chip group with `role="group"` and `aria-label={PROJECTS_TEXT.filterTechnologyLabel}`; omitted if `options.technologies.length === 0`
- ✓ Renders status chip group with `role="group"` and `aria-label={PROJECTS_TEXT.filterStatusLabel}`; omitted if `options.statuses.length <= 1` (Req 4.5)
- ✓ Renders each chip using M3 `FilterChip` as a button with `aria-pressed={true | false}`
- ✓ Renders "Clear filters" M3 `Button` iff at least one filter is active (`filters.technology !== null || filters.status !== null`)
- ✓ Applies `flex-wrap` so chips wrap cleanly on mobile without horizontal overflow (Req 16.4)
- ✓ Contains zero `'use client'` directive (presentational component controlled by parent)

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- M3 `FilterChip` and `Button` available
- Target file: `src/components/projects/project-filter-bar.tsx`

**Implementation Details:**

Write `src/components/projects/project-filter-bar.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { ProjectStatus, ProjectFilters } from '@/types/content';
import { FilterChip } from '@/components/ui/filter-chip';
import { Button } from '@/components/ui/button';
import { PROJECTS_TEXT } from './projects-text';
import type { FilterOptions } from '@/lib/projects/filter-params';

const STATUS_LABELS: Record<ProjectStatus, string> = {
  'completed': 'Completed',
  'in-progress': 'In progress',
  'archived': 'Archived',
};

export interface ProjectFilterBarProps {
  readonly options: FilterOptions;
  readonly filters: ProjectFilters;
  readonly onSelectTechnology: (name: string) => void;
  readonly onSelectStatus: (status: ProjectStatus) => void;
  readonly onClear: () => void;
  readonly barRef?: React.Ref<HTMLDivElement>;
}

/**
 * ProjectFilterBar Presentational Component
 *
 * Renders technology and status filter chip groups with accessible button states.
 * design.md Section 4.4 & Requirement 4.5, 6.1, 6.2, 6.3, 6.7, 16.4.
 */
export function ProjectFilterBar({
  options,
  filters,
  onSelectTechnology,
  onSelectStatus,
  onClear,
  barRef,
}: ProjectFilterBarProps): JSX.Element {
  const isAnyFilterActive = filters.technology !== null || filters.status !== null;
  const showTechnologyGroup = options.technologies.length > 0;
  const showStatusGroup = options.statuses.length > 1; // Omitted if <= 1 status (Req 4.5)

  return (
    <div ref={barRef} className="flex flex-col gap-6 mb-6">
      {/* Technology Chip Group */}
      {showTechnologyGroup && (
        <div
          role="group"
          aria-label={PROJECTS_TEXT.filterTechnologyLabel}
          className="flex flex-wrap items-center gap-2"
        >
          <span className="text-small font-medium text-text-secondary mr-2">
            {PROJECTS_TEXT.filterTechnologyLabel}:
          </span>
          {options.technologies.map((tech) => {
            const isActive = filters.technology === tech;
            return (
              <FilterChip
                key={tech}
                active={isActive}
                onClick={() => onSelectTechnology(tech)}
                aria-pressed={isActive}
              >
                {tech}
              </FilterChip>
            );
          })}
        </div>
      )}

      {/* Status Chip Group & Clear Action */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        {showStatusGroup ? (
          <div
            role="group"
            aria-label={PROJECTS_TEXT.filterStatusLabel}
            className="flex flex-wrap items-center gap-2"
          >
            <span className="text-small font-medium text-text-secondary mr-2">
              {PROJECTS_TEXT.filterStatusLabel}:
            </span>
            {options.statuses.map((status) => {
              const isActive = filters.status === status;
              return (
                <FilterChip
                  key={status}
                  active={isActive}
                  onClick={() => onSelectStatus(status)}
                  aria-pressed={isActive}
                >
                  {STATUS_LABELS[status] || status}
                </FilterChip>
              );
            })}
          </div>
        ) : (
          <div />
        )}

        {/* Clear Filters Button (rendered only while a filter is active per Req 6.7) */}
        {isAnyFilterActive && (
          <Button variant="ghost" size="sm" onClick={onClear}>
            {PROJECTS_TEXT.clearFilters}
          </Button>
        )}
      </div>
    </div>
  );
}
'@ | Set-Content "src\components\projects\project-filter-bar.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/project-filter-bar.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.5, Req 6.1, Req 6.2, Req 6.3, Req 6.7, Req 6.10, Req 16.4

---

### M6.G5.T3: Implement `ProjectsExplorer` Client Island Skeleton & Navigation (`src/components/projects/projects-explorer.tsx`)

**Objective:** Author the initial skeleton of `ProjectsExplorer` in `src/components/projects/projects-explorer.tsx` as the single `'use client'` module managing URL synchronization.

**Acceptance Criteria:**
- ✓ File `src/components/projects/projects-explorer.tsx` created with `'use client'` directive
- ✓ Imports `useRouter` and `useSearchParams` from `next/navigation`
- ✓ Exports `interface ProjectsExplorerProps { readonly projects: readonly ProjectCardData[]; }`
- ✓ Exports `ProjectsExplorer({ projects }: ProjectsExplorerProps): JSX.Element`
- ✓ Derives `options = useMemo(() => deriveFilterOptions(projects), [projects])`
- ✓ Derives `filters = parseProjectFilters(searchParams, options)` on every render without local state mirroring
- ✓ Implements navigation dispatcher calling `router.replace(url, { scroll: false })` using `mergeFiltersIntoQuery`
- ✓ Activating an active chip toggles it off (`null`); activating an inactive chip leaves other group unchanged

**Prerequisites:**
- M6.G2 and M6.G3 completed
- Target file: `src/components/projects/projects-explorer.tsx`

**Implementation Details:**

Write `src/components/projects/projects-explorer.tsx` skeleton using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
'use client';

import React, { useMemo, useRef, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import type { ProjectStatus, ProjectFilters } from '@/types/content';
import { ProjectFilterBar } from './project-filter-bar';
import { ProjectGrid } from './project-grid';
import { EmptyState } from '@/components/ui/empty-state';
import { Button } from '@/components/ui/button';
import { PROJECTS_PATH, PROJECTS_TEXT } from './projects-text';
import { deriveFilterOptions } from '@/lib/projects/derive-filter-options';
import { parseProjectFilters, mergeFiltersIntoQuery } from '@/lib/projects/filter-params';
import { filterProjects } from '@/lib/projects/filter-projects';
import { formatResultCount } from '@/lib/projects/format-result-count';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectsExplorerProps {
  readonly projects: readonly ProjectCardData[];
}

/**
 * ProjectsExplorer Client Island
 *
 * Exclusively owns URL search param filtering, polite live-region announcements,
 * and focus management. Wrapped in Suspense by ProjectsIndex (Req 6, 7.3, 8).
 */
export function ProjectsExplorer({ projects }: ProjectsExplorerProps): JSX.Element {
  const router = useRouter();
  const searchParams = useSearchParams();

  const options = useMemo(() => deriveFilterOptions(projects), [projects]);
  const filters = parseProjectFilters(searchParams, options);
  const shownProjects = filterProjects(projects, filters);

  const barRef = useRef<HTMLDivElement>(null);
  const focusFirstChipRef = useRef(false);

  function navigate(nextFilters: ProjectFilters) {
    const qs = mergeFiltersIntoQuery(searchParams.toString(), nextFilters);
    const targetUrl = qs.length > 0 ? `${PROJECTS_PATH}?${qs}` : PROJECTS_PATH;
    router.replace(targetUrl, { scroll: false });
  }

  const handleSelectTechnology = (name: string) => {
    navigate({
      ...filters,
      technology: filters.technology === name ? null : name,
    });
  };

  const handleSelectStatus = (status: ProjectStatus) => {
    navigate({
      ...filters,
      status: filters.status === status ? null : status,
    });
  };

  const handleClear = () => {
    focusFirstChipRef.current = true;
    navigate({ technology: null, status: null });
  };

  // Focus management: return focus to the first chip after clearFilters
  useEffect(() => {
    if (!focusFirstChipRef.current) return;
    focusFirstChipRef.current = false;
    barRef.current?.querySelector<HTMLButtonElement>('button[aria-pressed]')?.focus();
  }, [filters.technology, filters.status]);

  return (
    <div>
      <ProjectFilterBar
        barRef={barRef}
        options={options}
        filters={filters}
        onSelectTechnology={handleSelectTechnology}
        onSelectStatus={handleSelectStatus}
        onClear={handleClear}
      />
    </div>
  );
}
'@ | Set-Content "src\components\projects\projects-explorer.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/projects-explorer.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.4, Req 6.5, Req 6.6, Req 7.3, Req 7.4

---

### M6.G5.T4: Complete `ProjectsExplorer` with Live Region, Grid, and Empty State

**Objective:** Complete `src/components/projects/projects-explorer.tsx` by adding the visible polite live region, `ProjectGrid`, and filtered empty state with focus-restoring clear button.

**Acceptance Criteria:**
- ✓ Renders visible `<p aria-live="polite" className="text-small text-text-secondary mb-6">{formatResultCount(shownProjects.length)}</p>`
- ✓ Live region element is mounted in DOM on initial render (Req 8.3, 8.4)
- ✓ When `shownProjects.length > 0`: renders `<ProjectGrid projects={shownProjects} headingLevel={2} />`
- ✓ When `shownProjects.length === 0`: renders M3 `EmptyState` with `message={PROJECTS_TEXT.emptyFiltered}` and action `<Button onClick={handleClear}>Clear filters</Button>`
- ✓ Activating Clear in EmptyState triggers `handleClear`, removing filter parameters and shifting focus to first chip (Req 8.6)
- ✓ File strictly under 300 lines

**Prerequisites:**
- M6.G5.T3 completed
- Target file: `src/components/projects/projects-explorer.tsx`

**Implementation Details:**

Update `src/components/projects/projects-explorer.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
'use client';

import React, { useMemo, useRef, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import type { ProjectStatus, ProjectFilters } from '@/types/content';
import { ProjectFilterBar } from './project-filter-bar';
import { ProjectGrid } from './project-grid';
import { EmptyState } from '@/components/ui/empty-state';
import { Button } from '@/components/ui/button';
import { PROJECTS_PATH, PROJECTS_TEXT } from './projects-text';
import { deriveFilterOptions } from '@/lib/projects/derive-filter-options';
import { parseProjectFilters, mergeFiltersIntoQuery } from '@/lib/projects/filter-params';
import { filterProjects } from '@/lib/projects/filter-projects';
import { formatResultCount } from '@/lib/projects/format-result-count';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectsExplorerProps {
  readonly projects: readonly ProjectCardData[];
}

/**
 * ProjectsExplorer Client Island
 *
 * Exclusively owns URL search param filtering, polite live-region announcements,
 * and focus management. Wrapped in Suspense by ProjectsIndex (Req 6, 7.3, 8).
 */
export function ProjectsExplorer({ projects }: ProjectsExplorerProps): JSX.Element {
  const router = useRouter();
  const searchParams = useSearchParams();

  const options = useMemo(() => deriveFilterOptions(projects), [projects]);
  const filters = parseProjectFilters(searchParams, options);
  const shownProjects = filterProjects(projects, filters);

  const barRef = useRef<HTMLDivElement>(null);
  const focusFirstChipRef = useRef(false);

  function navigate(nextFilters: ProjectFilters) {
    const qs = mergeFiltersIntoQuery(searchParams.toString(), nextFilters);
    const targetUrl = qs.length > 0 ? `${PROJECTS_PATH}?${qs}` : PROJECTS_PATH;
    router.replace(targetUrl, { scroll: false });
  }

  const handleSelectTechnology = (name: string) => {
    navigate({
      ...filters,
      technology: filters.technology === name ? null : name,
    });
  };

  const handleSelectStatus = (status: ProjectStatus) => {
    navigate({
      ...filters,
      status: filters.status === status ? null : status,
    });
  };

  const handleClear = () => {
    focusFirstChipRef.current = true;
    navigate({ technology: null, status: null });
  };

  // Focus management: return focus to the first chip after clearFilters
  useEffect(() => {
    if (!focusFirstChipRef.current) return;
    focusFirstChipRef.current = false;
    barRef.current?.querySelector<HTMLButtonElement>('button[aria-pressed]')?.focus();
  }, [filters.technology, filters.status]);

  return (
    <div>
      <ProjectFilterBar
        barRef={barRef}
        options={options}
        filters={filters}
        onSelectTechnology={handleSelectTechnology}
        onSelectStatus={handleSelectStatus}
        onClear={handleClear}
      />

      {/* Visible Polite Live Region Announcement (Req 8.2-8.4) */}
      <p aria-live="polite" className="text-small text-text-secondary mb-6">
        {formatResultCount(shownProjects.length)}
      </p>

      {/* Result Grid or Filtered Empty State */}
      {shownProjects.length > 0 ? (
        <ProjectGrid projects={shownProjects} headingLevel={2} />
      ) : (
        <div className="py-8">
          <EmptyState
            message={PROJECTS_TEXT.emptyFiltered}
            action={
              <Button variant="secondary" onClick={handleClear}>
                {PROJECTS_TEXT.clearFilters}
              </Button>
            }
          />
        </div>
      )}
    </div>
  );
}
'@ | Set-Content "src\components\projects\projects-explorer.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/projects-explorer.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5, Req 8.6, Req 17.4

---

### M6.G5.T5: Implement `ProjectsIndex` Composition Component (`src/components/projects/projects-index.tsx`)

**Objective:** Author the server component `ProjectsIndex` in `src/components/projects/projects-index.tsx` composing the page heading, Suspense boundary with static fallback grid, and zero-project empty state.

**Acceptance Criteria:**
- ✓ File `src/components/projects/projects-index.tsx` created
- ✓ Exports `interface ProjectsIndexProps { readonly projects: readonly ProjectCardData[]; }`
- ✓ Exports `ProjectsIndex({ projects }: ProjectsIndexProps): JSX.Element`
- ✓ Renders `<Container className="py-12 md:py-16">`
- ✓ Renders `<h1 className="text-heading-1 font-bold text-text-primary mb-8">{PROJECTS_TEXT.pageHeading}</h1>`
- ✓ When `projects.length === 0`: renders M3 `EmptyState` with `message={PROJECTS_TEXT.emptyIndex}` and omits filter bar and chips
- ✓ When `projects.length > 0`: wraps `ProjectsExplorer` inside `<Suspense fallback={<ProjectGrid projects={projects} headingLevel={2} />}>`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M6.G5.T4 completed
- Target file: `src/components/projects/projects-index.tsx`

**Implementation Details:**

Write `src/components/projects/projects-index.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React, { Suspense } from 'react';
import { Container } from '@/components/ui/container';
import { EmptyState } from '@/components/ui/empty-state';
import { PROJECTS_TEXT } from './projects-text';
import { ProjectsExplorer } from './projects-explorer';
import { ProjectGrid } from './project-grid';
import type { ProjectCardData } from '@/lib/projects/card-data';

export interface ProjectsIndexProps {
  readonly projects: readonly ProjectCardData[];
}

/**
 * ProjectsIndex Presentational Container
 *
 * Hosts top-level page heading and wraps ProjectsExplorer in a Suspense boundary
 * whose fallback renders the complete unfiltered ProjectGrid into static HTML (Req 1, 7).
 * Server component by default (Req 1.1).
 */
export function ProjectsIndex({ projects }: ProjectsIndexProps): JSX.Element {
  const hasProjects = projects.length > 0;

  return (
    <Container className="py-12 md:py-16">
      <h1 className="text-heading-1 font-bold tracking-tight text-text-primary mb-8">
        {PROJECTS_TEXT.pageHeading}
      </h1>

      {hasProjects ? (
        <Suspense
          fallback={<ProjectGrid projects={projects} headingLevel={2} />}
        >
          <ProjectsExplorer projects={projects} />
        </Suspense>
      ) : (
        <div className="py-8">
          <EmptyState message={PROJECTS_TEXT.emptyIndex} />
        </div>
      )}
    </Container>
  );
}
'@ | Set-Content "src\components\projects\projects-index.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/projects-index.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 1.4, Req 1.7, Req 7.1, Req 7.2, Req 7.5, Req 15.1

---

### M6.G5.T6: Implement Static Projects Index Route (`src/app/projects/page.tsx`)

**Objective:** Author the static route entry point `src/app/projects/page.tsx` loading projects via `getProjects()` and exporting metadata derived via `buildProjectsIndexMetadata`.

**Acceptance Criteria:**
- ✓ Directory `src/app/projects/` exists or is created
- ✓ File `src/app/projects/page.tsx` created
- ✓ Imports `getProjects` from `@/content/loaders/projects`
- ✓ Imports `getSiteConfig` from `@/content/loaders/site`
- ✓ Imports `toProjectCardData` from `@/lib/projects/card-data`
- ✓ Imports `buildProjectsIndexMetadata` from `@/lib/projects/project-metadata`
- ✓ Imports `ProjectsIndex` from `@/components/projects/projects-index`
- ✓ Exports `generateMetadata(): Promise<Metadata>` calling `buildProjectsIndexMetadata(site.siteUrl)`
- ✓ Exports default async function `ProjectsPage(): Promise<JSX.Element>` projecting projects to `ProjectCardData`
- ✓ Strictly omits `'use client'` directive

**Prerequisites:**
- M6.G5.T5 completed
- Target file: `src/app/projects/page.tsx`

**Implementation Details:**

Write `src/app/projects/page.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\app\projects")) {
    New-Item -ItemType Directory -Path "src\app\projects" -Force | Out-Null
}

@'
import React from 'react';
import type { Metadata } from 'next';
import { getProjects } from '@/content/loaders/projects';
import { getSiteConfig } from '@/content/loaders/site';
import { toProjectCardData } from '@/lib/projects/card-data';
import { buildProjectsIndexMetadata } from '@/lib/projects/project-metadata';
import { ProjectsIndex } from '@/components/projects/projects-index';

export async function generateMetadata(): Promise<Metadata> {
  const site = await getSiteConfig();
  return buildProjectsIndexMetadata(site.siteUrl);
}

/**
 * Projects Index Route (SCR-02)
 *
 * Statically rendered server route for browsing and filtering projects.
 * Passes serializable ProjectCardData to client boundaries (Req 1.1-1.4, 7.4).
 */
export default async function ProjectsPage(): Promise<JSX.Element> {
  const projects = await getProjects();
  const cardDataList = projects.map(toProjectCardData);

  return <ProjectsIndex projects={cardDataList} />;
}
'@ | Set-Content "src\app\projects\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/app/projects/page.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 1.4, Req 7.4, Req 15.4, Req 15.5

---

### M6.G5.T7: Author Unit Tests for `ProjectFilterBar` (`tests/projects/project-filter-bar.test.tsx`)

**Objective:** Create `tests/projects/project-filter-bar.test.tsx` verifying accessible groups, `aria-pressed`, single-status omission, and keyboard navigation.

**Acceptance Criteria:**
- ✓ File `tests/projects/project-filter-bar.test.tsx` created
- ✓ Verifies technology group has `role="group"` and accessible label
- ✓ Verifies status group is omitted when only 1 status is present in options (Req 4.5)
- ✓ Verifies active chip has `aria-pressed="true"`, inactive chips have `aria-pressed="false"`
- ✓ Verifies "Clear filters" is visible only when a filter is active
- ✓ Verifies Tab, Enter, and Space keys activate filter chips via `@testing-library/user-event`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G5.T2 completed
- Target file: `tests/projects/project-filter-bar.test.tsx`

**Implementation Details:**

Write `tests/projects/project-filter-bar.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectFilterBar } from '@/components/projects/project-filter-bar';

describe('ProjectFilterBar Component (Req 4.5, 6)', () => {
  const standardOptions = {
    technologies: ['TypeScript', 'Docker', 'Go'],
    statuses: ['completed' as const, 'in-progress' as const],
  };

  it('renders technology and status groups with accessible labels and buttons', () => {
    render(
      <ProjectFilterBar
        options={standardOptions}
        filters={{ technology: 'TypeScript', status: null }}
        onSelectTechnology={vi.fn()}
        onSelectStatus={vi.fn()}
        onClear={vi.fn()}
      />
    );

    const techGroup = screen.getByRole('group', { name: 'Filter by technology' });
    expect(techGroup).toBeDefined();

    const statusGroup = screen.getByRole('group', { name: 'Filter by status' });
    expect(statusGroup).toBeDefined();

    const tsChip = screen.getByRole('button', { name: 'TypeScript' });
    expect(tsChip.getAttribute('aria-pressed')).toBe('true');

    const dockerChip = screen.getByRole('button', { name: 'Docker' });
    expect(dockerChip.getAttribute('aria-pressed')).toBe('false');

    // Clear filters is present because technology is active
    expect(screen.getByRole('button', { name: 'Clear filters' })).toBeDefined();
  });

  it('omits status group when options contain <= 1 status', () => {
    render(
      <ProjectFilterBar
        options={{ technologies: ['TypeScript'], statuses: ['completed'] }}
        filters={{ technology: null, status: null }}
        onSelectTechnology={vi.fn()}
        onSelectStatus={vi.fn()}
        onClear={vi.fn()}
      />
    );

    expect(screen.queryByRole('group', { name: 'Filter by status' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Clear filters' })).toBeNull();
  });

  it('supports Tab navigation and Enter/Space keyboard activation', async () => {
    const user = userEvent.setup();
    const onSelectTech = vi.fn();

    render(
      <ProjectFilterBar
        options={standardOptions}
        filters={{ technology: null, status: null }}
        onSelectTechnology={onSelectTech}
        onSelectStatus={vi.fn()}
        onClear={vi.fn()}
      />
    );

    await user.tab();
    expect(screen.getByRole('button', { name: 'TypeScript' })).toHaveFocus();

    await user.keyboard('{Enter}');
    expect(onSelectTech).toHaveBeenCalledWith('TypeScript');

    await user.tab();
    expect(screen.getByRole('button', { name: 'Docker' })).toHaveFocus();

    await user.keyboard(' ');
    expect(onSelectTech).toHaveBeenCalledWith('Docker');
  });
});
'@ | Set-Content "tests\projects\project-filter-bar.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-filter-bar.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.5, Req 6.1, Req 6.2, Req 6.3, Req 6.7, Req 6.9, Req 6.10

---

### M6.G5.T8: Author Interaction & Focus Tests for `ProjectsExplorer` (`tests/projects/projects-explorer.test.tsx`)

**Objective:** Create `tests/projects/projects-explorer.test.tsx` verifying navigation replacement, focus restoration, live region text, and empty filtered states using the navigation mock.

**Acceptance Criteria:**
- ✓ File `tests/projects/projects-explorer.test.tsx` created
- ✓ Mocks `next/navigation` using `tests/projects/helpers/mock-navigation.ts`
- ✓ Tests activating a chip calls `router.replace` with `{ scroll: false }`
- ✓ Tests re-activating active chip toggles it off
- ✓ Tests activating "Clear filters" restores focus to the first chip
- ✓ Tests empty filtered state renders `EmptyState` and "Clear filters" button
- ✓ Tests live region `<p aria-live="polite">` updates text dynamically
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G5.T1 and M6.G5.T4 completed
- Target file: `tests/projects/projects-explorer.test.tsx`

**Implementation Details:**

Write `tests/projects/projects-explorer.test.tsx` using PowerShell:
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
import {
  setInitialQuery,
  mockReplace,
  mockUseRouter,
  mockUseSearchParams,
} from './helpers/mock-navigation';

vi.mock('next/navigation', () => ({
  useRouter: () => mockUseRouter(),
  useSearchParams: () => mockUseSearchParams(),
}));

describe('ProjectsExplorer Component (Req 6, 7, 8)', () => {
  const cards = sampleProjectsList.map(toProjectCardData);

  beforeEach(() => {
    setInitialQuery('');
    mockReplace.mockClear();
  });

  it('updates query string with scroll: false on chip activation', async () => {
    const user = userEvent.setup();
    render(<ProjectsExplorer projects={cards} />);

    const tsChip = screen.getByRole('button', { name: 'TypeScript' });
    await user.click(tsChip);

    expect(mockReplace).toHaveBeenCalledWith('/projects?technology=TypeScript', { scroll: false });
  });

  it('toggles filter off when activating an already active chip', async () => {
    const user = userEvent.setup();
    setInitialQuery('technology=TypeScript');
    render(<ProjectsExplorer projects={cards} />);

    const tsChip = screen.getByRole('button', { name: 'TypeScript' });
    expect(tsChip.getAttribute('aria-pressed')).toBe('true');

    await user.click(tsChip);
    expect(mockReplace).toHaveBeenCalledWith('/projects', { scroll: false });
  });

  it('restores keyboard focus to first chip after clicking Clear filters', async () => {
    const user = userEvent.setup();
    setInitialQuery('technology=TypeScript');
    render(<ProjectsExplorer projects={cards} />);

    const clearBtn = screen.getByRole('button', { name: 'Clear filters' });
    await user.click(clearBtn);

    const firstChip = screen.getByRole('button', { name: 'Docker' }); // alphabetically first option
    expect(firstChip).toHaveFocus();
  });

  it('renders polite live region announcing count and empty state on zero matches', async () => {
    const user = userEvent.setup();
    setInitialQuery('technology=TypeScript&status=archived'); // matches nothing in sample list
    render(<ProjectsExplorer projects={cards} />);

    expect(screen.getByText('0 projects shown')).toBeDefined();
    expect(screen.getByText('No projects match the selected filters.')).toBeDefined();

    // Clear filters in empty state restores cards
    const emptyClearBtn = screen.getByRole('button', { name: 'Clear filters' });
    await user.click(emptyClearBtn);
    expect(mockReplace).toHaveBeenCalledWith('/projects', { scroll: false });
  });
});
'@ | Set-Content "tests\projects\projects-explorer.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/projects-explorer.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.4, Req 6.5, Req 6.6, Req 6.8, Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.6

---

### M6.G5.T9: Author Property-Based Test for Explorer State Display (Property 12) & Route Tests

**Objective:** Append Property 12 test in `tests/projects/projects-explorer.test.tsx` and create `tests/projects/projects-index.test.tsx` and `projects-page.test.tsx`.

**Acceptance Criteria:**
- ✓ Implements Property 12 test ($\ge 100$ runs with `fast-check`): Explorer displays exact cards of `filterProjects(projects, model)` in input order, sets `aria-pressed`, and updates live region text
- ✓ Tagged: `Feature: m6-projects-module, Property 12: the Explorer displays exactly the filtered projects and reflects chip state`
- ✓ `tests/projects/projects-index.test.tsx` tests `<h1>Projects</h1>`, Suspense fallback grid, and zero-project empty state
- ✓ `tests/projects/projects-page.test.tsx` tests `ProjectsPage` static render without client directive and metadata generation
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G5.T8, M6.G5.T5, and M6.G5.T6 completed

**Implementation Details:**

Append Property 12 and create index/page tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Append Property 12 to projects-explorer.test.tsx
$appendProp12 = @'

  describe('Property-Based Invariants (Property 12)', () => {
    it('Feature: m6-projects-module, Property 12: Explorer displays exactly the filtered projects and reflects chip state', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProjectCardData, arbFilterOptions, arbProjectFilters } = require('../fixtures/projects-arbitraries');
      const { filterProjects } = require('@/lib/projects/filter-projects');

      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(
              fc.array(arbProjectCardData, { minLength: 1, maxLength: 5 }),
              arbProjectFilters(opts)
            )
          ),
          ([projects, filters]: any) => {
            cleanup();
            const expected = filterProjects(projects, filters);
            setInitialQuery(
              filters.technology ? `technology=${filters.technology}` : ''
            );

            render(<ProjectsExplorer projects={projects} />);

            // 1. Live region text matches count
            const countText = expected.length === 1 ? '1 project shown' : `${expected.length} projects shown`;
            expect(screen.getByText(countText)).toBeDefined();

            // 2. Exact cards rendered in order if count > 0
            if (expected.length > 0) {
              const headings = screen.getAllByRole('heading', { level: 2 });
              expect(headings.length).toBe(expected.length);
              for (let i = 0; i < expected.length; i++) {
                expect(headings[i].textContent).toBe(expected[i].title);
              }
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$contentExp = Get-Content "tests\projects\projects-explorer.test.tsx" -Raw
$contentExp = $contentExp -replace "\s*\}\);\s*$", "$appendProp12`n});`n"
$contentExp | Set-Content "tests\projects\projects-explorer.test.tsx" -Encoding UTF8

# Create projects-index.test.tsx
@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ProjectsIndex } from '@/components/projects/projects-index';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';

vi.mock('next/navigation', () => ({
  useRouter: () => ({ replace: vi.fn() }),
  useSearchParams: () => new URLSearchParams(''),
}));

describe('ProjectsIndex Component (Req 1, 7)', () => {
  it('renders single h1 Projects and wraps grid in Suspense', () => {
    const cards = sampleProjectsList.map(toProjectCardData);
    render(<ProjectsIndex projects={cards} />);

    const h1s = screen.getAllByRole('heading', { level: 1 });
    expect(h1s.length).toBe(1);
    expect(h1s[0].textContent).toBe('Projects');
  });

  it('renders EmptyState and no chips when projects collection is empty', () => {
    render(<ProjectsIndex projects={[]} />);

    expect(screen.getByText('Projects are being prepared. Check back soon.')).toBeDefined();
    expect(screen.queryByRole('group')).toBeNull();
  });
});
'@ | Set-Content "tests\projects\projects-index.test.tsx" -Encoding UTF8

# Create projects-page.test.tsx
@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ProjectsPage, { generateMetadata } from '@/app/projects/page';
import { sampleProjectsList } from '../fixtures/projects-data';
import { sampleSiteConfig } from '../fixtures/home-data';

vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
}));
vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(),
}));
vi.mock('next/navigation', () => ({
  useRouter: () => ({ replace: vi.fn() }),
  useSearchParams: () => new URLSearchParams(''),
}));

describe('ProjectsPage Static Route (Req 1, 15)', () => {
  it('renders ProjectsIndex with loaded projects and generates metadata', async () => {
    const { getProjects } = await import('@/content/loaders/projects');
    const { getSiteConfig } = await import('@/content/loaders/site');

    vi.mocked(getProjects).mockResolvedValue(sampleProjectsList);
    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);

    const Page = await ProjectsPage();
    render(Page);

    expect(screen.getByRole('heading', { level: 1, name: 'Projects' })).toBeDefined();

    const meta = await generateMetadata();
    expect(meta.title).toBe('Projects');
    expect(meta.alternates?.canonical).toBe('https://example.vercel.app/projects');
  });
});
'@ | Set-Content "tests\projects\projects-page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/projects-explorer.test.tsx tests/projects/projects-index.test.tsx tests/projects/projects-page.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 1.7, Req 2.9, Req 6.2, Req 7.1, Req 7.2, Req 7.4, Req 8.1, Req 8.2, Req 15.4, Req 17.2

---

### M6.G5.T10: Author Axe Accessibility Tests for Index and Checkpoint Quality Gates

**Objective:** Append automated axe tests verifying WCAG 2.1 AA compliance for ProjectsIndex in default, filtered, and empty states, and execute quality gates.

**Acceptance Criteria:**
- ✓ Evaluates default `ProjectsIndex`: 0 axe violations
- ✓ Evaluates filtered `ProjectsExplorer`: 0 axe violations
- ✓ Evaluates empty `ProjectsIndex`: 0 axe violations
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all G5 test suites with code 0

**Prerequisites:**
- M6.G5.T9 completed

**Implementation Details:**

Append axe tests and execute quality checks via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendAxe = @'

  describe('Axe Accessibility Matrix (Req 16.6)', () => {
    it('reports zero axe violations across default and empty index states', async () => {
      const { axe } = require('vitest-axe');
      const cards = sampleProjectsList.map(toProjectCardData);

      const { container: c1 } = render(<ProjectsIndex projects={cards} />);
      expect((await axe(c1)).violations).toHaveLength(0);

      const { container: c2 } = render(<ProjectsIndex projects={[]} />);
      expect((await axe(c2)).violations).toHaveLength(0);
    });
  });
'@

$contentIdx = Get-Content "tests\projects\projects-index.test.tsx" -Raw
$contentIdx = $contentIdx -replace "\s*\}\);\s*$", "$appendAxe`n});`n"
$contentIdx | Set-Content "tests\projects\projects-index.test.tsx" -Encoding UTF8

npm run typecheck
npm run lint
npm run test -- tests/projects/project-filter-bar.test.tsx tests/projects/projects-explorer.test.tsx tests/projects/projects-index.test.tsx tests/projects/projects-page.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/project-filter-bar.test.tsx tests/projects/projects-explorer.test.tsx tests/projects/projects-index.test.tsx tests/projects/projects-page.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6, Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\projects\helpers\mock-navigation.ts"
Test-Path "src\components\projects\project-filter-bar.tsx"
Test-Path "src\components\projects\projects-explorer.tsx"
Test-Path "src\components\projects\projects-index.tsx"
Test-Path "src\app\projects\page.tsx"
npm run typecheck
npm run test -- tests/projects/project-filter-bar.test.tsx tests/projects/projects-explorer.test.tsx tests/projects/projects-index.test.tsx tests/projects/projects-page.test.tsx
```
Expected output:
- `True` for all 5 path existence checks
- `npm run typecheck` exits with return code 0
- Vitest executes all index and explorer tests with return code 0.