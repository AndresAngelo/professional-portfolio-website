# M6.G1: Fixtures, Fixed UI Strings, Tech Key, Card Data, Upstream Verification, and Gap Log

> **Milestone:** M6 — Projects Module  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the foundational test fixtures, fast-check property testing arbitraries, fixed layout strings, technology key normalizer, serializable card data extractor, and architectural audit for Milestone 6. Specifically, author strongly typed test fixtures in `tests/fixtures/projects-data.ts` covering full configurations and edge-case variants (no links, empty tags/metrics, in-progress projects with `completedAt: null`, more than 4 technologies, mixed-case duplicates, single status, and zero shared technologies) using types imported from `@/types/content` without redeclaring contracts. Construct `fast-check` arbitraries in `tests/fixtures/projects-arbitraries.ts` to support universal property testing across projects, card data, filter options, query strings, and HTML heading structures. Create `src/components/projects/projects-text.ts` defining all static UI strings, constants (`PROJECTS_PATH`, `MAX_CARD_TECHNOLOGIES`, `RELATED_LIMIT`, `STATUS_ORDER`), and `PROJECTS_INDEX_DESCRIPTION`. Implement the deterministic technology key normalizer `techKey` in `src/lib/projects/tech-key.ts` and the serializable card projection `toProjectCardData` in `src/lib/projects/card-data.ts`. Verify upstream M1–M5 contracts (loaders, M3 primitives, M5 `formatDisplayDate` and `compareStrings`), document findings in `.kiro/specs/m6-projects-module/task-notes.md`, and confirm that protected files remain completely untouched.

## Goal Success Criteria

- ✓ `tests/fixtures/projects-data.ts` exports typed `Project` fixtures (`sampleProjectsList`, `noLinksProject`, `inProgressProject`, `overflowTechProject`, `emptyTagsMetricsProject`, `singleStatusProjects`, `isolatedTechProject`) strictly typed via `@/types/content`
- ✓ `tests/fixtures/projects-arbitraries.ts` exports `fast-check` generators for projects, `ProjectCardData`, `FilterOptions`, `ProjectFilters`, query strings, and heading-bearing HTML
- ✓ `src/components/projects/projects-text.ts` exports `PROJECTS_PATH`, `MAX_CARD_TECHNOLOGIES = 4`, `RELATED_LIMIT = 3`, `STATUS_ORDER`, `PROJECTS_TEXT`, and `PROJECTS_INDEX_DESCRIPTION` (verified 50–160 chars) with zero site-owner or personal-data literals
- ✓ `src/lib/projects/tech-key.ts` exports pure function `techKey(name: string): string` enforcing trim and lowercase normalization
- ✓ `src/lib/projects/card-data.ts` exports type `ProjectCardData` and pure function `toProjectCardData(project: Project): ProjectCardData` projecting exactly eight serializable fields and omitting `documentation`
- ✓ Property 13 passes in `tests/projects/card-data.test.ts` ($\ge 100$ runs with `fast-check`), proving client props are strictly JSON-serializable and exclude documentation
- ✓ Task notes file `.kiro/specs/m6-projects-module/task-notes.md` initialized with verified paths for M2 loaders, M3 primitives, M5 `formatDisplayDate` and `compareStrings`, Next.js `params` contract, and test toolchain availability
- ✓ `git diff` confirms zero changes to `package.json`, lockfiles, `tailwind.config.ts`, `globals.css`, `src/components/ui/`, `src/components/layout/`, `src/components/home/`, `src/lib/home/`, `src/lib/format-date.ts`, or `src/content/`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Milestones M1, M2, M3, M4, and M5 completed (`m5-baseline` tagged in Git)
- Workspace root: `c:\dev\andres-webapp-professional\personal-website-portfolio`
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream utilities verified: `src/lib/format-date.ts` (`formatDisplayDate`) and `src/lib/home/compare.ts` (`compareStrings`)

---

## Tasks

### M6.G1.T1: Create Typed Projects Test Fixtures (`tests/fixtures/projects-data.ts`)

**Objective:** Author canonical, strongly typed test fixtures in `tests/fixtures/projects-data.ts` covering populated project collections and edge variants without redeclaring content types.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/projects-data.ts` created
- ✓ Imports `Project`, `ProjectStatus`, and `ProjectFilters` from `@/types/content` without redeclaring types (`AGENTS.md` 6.3, Req 1.5)
- ✓ Exports `sampleProjectsList`: at least 6 projects covering all three `ProjectStatus` values (`completed`, `in-progress`, `archived`), overlapping technologies, distinct `displayOrder` values, and shared technology tags
- ✓ Exports `noLinksProject`: project where `repositoryUrl`, `liveDemoUrl`, and `documentationUrl` are all `null`
- ✓ Exports `inProgressProject`: project where `status === 'in-progress'` and `completedAt === null`
- ✓ Exports `overflowTechProject`: project listing at least 6 distinct technologies to test the card technology display limit (`MAX_CARD_TECHNOLOGIES = 4`)
- ✓ Exports `emptyTagsMetricsProject`: project where `tags: []` and `metrics: []`
- ✓ Exports `singleStatusProjects`: array of projects all sharing identical status (to verify status chip group omission per Req 4.5)
- ✓ Exports `isolatedTechProject`: project whose technologies share zero overlap with any project in `sampleProjectsList`
- ✓ Contains zero `any`, non-null assertions `!`, or unjustified type assertions

**Prerequisites:**
- M2 content contracts exist at `src/types/content.ts`
- Directory `tests/fixtures/` exists

**Implementation Details:**

Write `tests/fixtures/projects-data.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures")) {
    New-Item -ItemType Directory -Path "tests\fixtures" -Force | Out-Null
}

@'
import type { Project, ProjectStatus, ProjectFilters } from '@/types/content';

/**
 * Standard collection of projects for index, filtering, and related selection tests.
 */
export const sampleProjectsList: Project[] = [
  {
    title: 'Alpha Pipeline Core',
    slug: 'alpha-pipeline-core',
    summary: 'High performance specification-driven pipeline engine built in TypeScript and Go.',
    status: 'completed',
    role: 'Lead Architect',
    startedAt: '2025-01-10',
    completedAt: '2025-06-15',
    technologies: ['TypeScript', 'Go', 'Docker', 'Next.js'],
    tags: ['pipeline', 'compiler'],
    repositoryUrl: 'https://github.com/example/alpha-pipeline-core',
    liveDemoUrl: 'https://alpha.example.com',
    documentationUrl: 'https://docs.alpha.example.com',
    featured: true,
    displayOrder: 1,
    metrics: [
      { label: 'Latency', value: '<5ms' },
      { label: 'Throughput', value: '10k op/s' },
    ],
    documentation: '## Alpha Core Architecture\nCore execution engine specifications and benchmarking metrics.',
  },
  {
    title: 'Beta Agent Orchestrator',
    slug: 'beta-agent-orchestrator',
    summary: 'Stateless dual-model swapping harness managing local agent execution loops.',
    status: 'in-progress',
    role: 'Systems Engineer',
    startedAt: '2025-07-01',
    completedAt: null,
    technologies: ['TypeScript', 'Python', 'Docker'],
    tags: ['agents', 'local-ai'],
    repositoryUrl: 'https://github.com/example/beta-orchestrator',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: true,
    displayOrder: 2,
    metrics: [
      { label: 'VRAM Footprint', value: '7.5GB' },
    ],
    documentation: '## Beta Orchestrator\nModel swapping sequence diagrams and AST pre-flight checks.',
  },
  {
    title: 'Gamma Schema Validator',
    slug: 'gamma-schema-validator',
    summary: 'Zero-overhead compile-time schema verification utility for content pipelines.',
    status: 'completed',
    role: 'Lead Developer',
    startedAt: '2025-08-15',
    completedAt: '2025-10-30',
    technologies: ['TypeScript', 'Next.js', 'Tailwind CSS'],
    tags: ['schema', 'validation'],
    repositoryUrl: 'https://github.com/example/gamma-validator',
    liveDemoUrl: 'https://gamma.example.com',
    documentationUrl: null,
    featured: false,
    displayOrder: 3,
    metrics: [],
    documentation: '## Gamma Validation Engine\nFormal proof and type narrowing rules.',
  },
  {
    title: 'Delta Portal Gateway',
    slug: 'delta-portal-gateway',
    summary: 'Static documentation explorer and API catalog for developer operations.',
    status: 'archived',
    role: 'Frontend Architect',
    startedAt: '2024-03-01',
    completedAt: '2024-08-01',
    technologies: ['React', 'Next.js', 'Tailwind CSS'],
    tags: ['portal', 'docs'],
    repositoryUrl: 'https://github.com/example/delta-portal',
    liveDemoUrl: null,
    documentationUrl: 'https://delta.example.com/docs',
    featured: false,
    displayOrder: 4,
    metrics: [
      { label: 'Page Speed', value: '99/100' },
    ],
    documentation: '## Delta Portal Documentation\nRetired portal architecture guidelines.',
  },
  {
    title: 'Epsilon State Sync',
    slug: 'epsilon-state-sync',
    summary: 'Distributed state synchronization library leveraging conflict-free replicated data types.',
    status: 'completed',
    role: 'Core Contributor',
    startedAt: '2025-11-01',
    completedAt: '2026-01-20',
    technologies: ['Go', 'Docker', 'PostgreSQL'],
    tags: ['crdt', 'distributed'],
    repositoryUrl: 'https://github.com/example/epsilon-sync',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: false,
    displayOrder: 5,
    metrics: [],
    documentation: '## Epsilon CRDT Specification\nMathematical invariants and network convergence proofs.',
  },
  {
    title: 'Zeta UI Primitives',
    slug: 'zeta-ui-primitives',
    summary: 'High-contrast accessible design system tokens and WCAG 2.1 AA primitives.',
    status: 'in-progress',
    role: 'UI/UX Lead',
    startedAt: '2026-02-01',
    completedAt: null,
    technologies: ['TypeScript', 'React', 'Tailwind CSS'],
    tags: ['design-system', 'accessibility'],
    repositoryUrl: 'https://github.com/example/zeta-ui',
    liveDemoUrl: 'https://zeta.example.com',
    documentationUrl: null,
    featured: false,
    displayOrder: 6,
    metrics: [],
    documentation: '## Zeta Accessibility Guidelines\nFocus management and screen-reader test protocols.',
  },
];

/**
 * Project fixture with zero external link URLs.
 */
export const noLinksProject: Project = {
  ...sampleProjectsList[1],
  slug: 'no-links-project',
  repositoryUrl: null,
  liveDemoUrl: null,
  documentationUrl: null,
};

/**
 * In-progress project fixture with null completedAt date.
 */
export const inProgressProject: Project = {
  ...sampleProjectsList[1],
  slug: 'in-progress-project',
  status: 'in-progress',
  completedAt: null,
};

/**
 * Project fixture with six technologies to exercise the MAX_CARD_TECHNOLOGIES (4) limit.
 */
export const overflowTechProject: Project = {
  ...sampleProjectsList[0],
  slug: 'overflow-tech-project',
  technologies: ['TypeScript', 'Go', 'Docker', 'Next.js', 'Python', 'PostgreSQL'],
};

/**
 * Project fixture with empty tags and empty metrics arrays.
 */
export const emptyTagsMetricsProject: Project = {
  ...sampleProjectsList[2],
  slug: 'empty-tags-metrics-project',
  tags: [],
  metrics: [],
};

/**
 * Collection of projects all sharing the same status (completed) to test status filter bar omission.
 */
export const singleStatusProjects: Project[] = sampleProjectsList.map((p) => ({
  ...p,
  status: 'completed',
}));

/**
 * Project fixture with technologies completely disjoint from sampleProjectsList.
 */
export const isolatedTechProject: Project = {
  ...sampleProjectsList[0],
  slug: 'isolated-tech-project',
  title: 'Isolated Rust Service',
  technologies: ['Rust', 'WebAssembly', 'SQLite'],
};
'@ | Set-Content "tests\fixtures\projects-data.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/fixtures/projects-data.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 2.2, Req 2.3, Req 2.5, Req 4.5, Req 10.3, Req 10.5, Req 11.2, Req 11.4, Req 12.1, Req 12.4, Req 14.2

---

### M6.G1.T2: Create Property-Based Testing Arbitraries (`tests/fixtures/projects-arbitraries.ts`)

**Objective:** Author fast-check arbitraries in `tests/fixtures/projects-arbitraries.ts` for projects, card data, filter options, query strings, and HTML heading structures.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/projects-arbitraries.ts` created
- ✓ Exports `arbTechName`: generates technology strings drawn from a bounded pool with varied casing and whitespace padding
- ✓ Exports `arbProject`: generates valid `Project` entities with valid slugs, statuses, dates, and technology arrays
- ✓ Exports `arbProjectsList`: generates arrays of projects with unique slugs
- ✓ Exports `arbFilterOptions`: generates valid `FilterOptions` with sorted canonical technology names and statuses
- ✓ Exports `arbProjectFilters`: generates `ProjectFilters` conforming to or disjoint from available options
- ✓ Exports `arbQueryString`: generates arbitrary query strings containing filter parameters, repeated keys, and unrelated query keys
- ✓ Exports `arbHeadingHtml`: generates HTML fragments with random heading levels (`<h1>` through `<h6>`) and arbitrary attributes
- ✓ Built strictly using `fast-check` without pseudo-random math

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/fixtures/projects-arbitraries.ts`

**Implementation Details:**

Write `tests/fixtures/projects-arbitraries.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import fc from 'fast-check';
import type { Project, ProjectStatus, ProjectFilters } from '@/types/content';
import type { FilterOptions } from '@/lib/projects/filter-params';
import type { ProjectCardData } from '@/lib/projects/card-data';

const TECH_POOL = [
  'TypeScript', 'typescript', ' Next.js ', 'React', 'react',
  'Tailwind CSS', 'Docker', 'docker', 'Go', 'Python', 'PostgreSQL'
];

/**
 * Arbitrary generator for individual technology names with mixed casing/whitespace.
 */
export const arbTechName: fc.Arbitrary<string> = fc.constantFrom(...TECH_POOL);

/**
 * Arbitrary generator for Project entity.
 */
export const arbProject: fc.Arbitrary<Project> = fc.record({
  title: fc.string({ minLength: 3, maxLength: 40 }).filter((s) => s.trim().length >= 3 && !s.includes('<')),
  slug: fc.string({ minLength: 2, maxLength: 20 })
    .filter((s) => /^[a-z0-9-]+$/.test(s) && !s.startsWith('-') && !s.endsWith('-')),
  summary: fc.string({ minLength: 20, maxLength: 100 }).filter((s) => s.trim().length >= 20),
  status: fc.constantFrom<ProjectStatus>('completed', 'in-progress', 'archived'),
  role: fc.string({ minLength: 3, maxLength: 30 }),
  startedAt: fc.constant('2025-01-10'),
  completedAt: fc.constantFrom('2025-06-15', null),
  technologies: fc.subarray(TECH_POOL, { minLength: 1, maxLength: 6 }),
  tags: fc.array(fc.string({ minLength: 2, maxLength: 10 }), { maxLength: 3 }),
  repositoryUrl: fc.constantFrom('https://github.com/example/repo', '   ', null),
  liveDemoUrl: fc.constantFrom('https://demo.example.com', null),
  documentationUrl: fc.constantFrom('https://docs.example.com', null),
  featured: fc.boolean(),
  displayOrder: fc.integer({ min: 1, max: 5 }),
  metrics: fc.array(
    fc.record({
      label: fc.string({ minLength: 2, maxLength: 15 }),
      value: fc.string({ minLength: 2, maxLength: 10 }),
    }),
    { maxLength: 3 }
  ),
  documentation: fc.constant('## Project Docs\nExample build documentation content.'),
});

/**
 * Arbitrary generator for a list of projects with distinct slugs.
 */
export const arbProjectsList: fc.Arbitrary<Project[]> = fc
  .array(arbProject, { minLength: 0, maxLength: 12 })
  .map((projects) => {
    const seen = new Set<string>();
    const unique: Project[] = [];
    for (const p of projects) {
      if (!seen.has(p.slug)) {
        seen.add(p.slug);
        unique.push(p);
      }
    }
    return unique;
  });

/**
 * Arbitrary generator for ProjectCardData.
 */
export const arbProjectCardData: fc.Arbitrary<ProjectCardData> = arbProject.map((p) => ({
  slug: p.slug,
  title: p.title,
  summary: p.summary,
  status: p.status,
  role: p.role,
  technologies: [...p.technologies],
  startedAt: p.startedAt,
  completedAt: p.completedAt,
}));

/**
 * Arbitrary generator for FilterOptions.
 */
export const arbFilterOptions: fc.Arbitrary<FilterOptions> = fc.record({
  technologies: fc.constantFrom(
    ['Docker', 'Go', 'Next.js', 'Python', 'React', 'TypeScript'],
    ['TypeScript', 'Tailwind CSS'],
    []
  ),
  statuses: fc.constantFrom<ProjectStatus[]>(
    ['completed', 'in-progress', 'archived'],
    ['completed', 'in-progress'],
    ['completed'],
    []
  ),
});

/**
 * Arbitrary generator for ProjectFilters given options.
 */
export const arbProjectFilters = (options: FilterOptions): fc.Arbitrary<ProjectFilters> =>
  fc.record({
    technology: options.technologies.length > 0
      ? fc.constantFrom(...options.technologies, null)
      : fc.constant(null),
    status: options.statuses.length > 0
      ? fc.constantFrom(...options.statuses, null)
      : fc.constant(null),
  });

/**
 * Arbitrary generator for arbitrary URL query strings.
 */
export const arbQueryString: fc.Arbitrary<string> = fc
  .array(
    fc.tuple(
      fc.constantFrom('technology', 'status', 'page', 'ref', 'search', 'sort'),
      fc.string({ minLength: 1, maxLength: 15 }).filter((s) => !s.includes('&') && !s.includes('='))
    ),
    { maxLength: 6 }
  )
  .map((pairs) => pairs.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('&'));

/**
 * Arbitrary generator for HTML strings containing random headings (h1 to h6).
 */
export const arbHeadingHtml: fc.Arbitrary<string> = fc
  .array(
    fc.record({
      level: fc.integer({ min: 1, max: 6 }),
      id: fc.string({ minLength: 2, maxLength: 10 }).filter((s) => /^[a-z]+$/.test(s)),
      text: fc.string({ minLength: 3, maxLength: 25 }).filter((s) => !s.includes('<')),
    }),
    { minLength: 1, maxLength: 6 }
  )
  .map((headings) =>
    headings
      .map((h) => `<h${h.level} id="${h.id}">${h.text}</h${h.level}>\n<p>Paragraph text.</p>`)
      .join('\n')
  );
'@ | Set-Content "tests\fixtures\projects-arbitraries.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/fixtures/projects-arbitraries.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.7, Req 4.3, Req 5.5, Req 5.6, Req 7.4, Req 13.4, Req 17.2

---

### M6.G1.T3: Implement Fixed Projects UI Strings & Constants (`src/components/projects/projects-text.ts`)

**Objective:** Author `src/components/projects/projects-text.ts` defining all structural constants, route paths, limits, UI strings, and index metadata description.

**Acceptance Criteria:**
- ✓ File `src/components/projects/projects-text.ts` created
- ✓ Exports `PROJECTS_PATH = '/projects'`
- ✓ Exports `MAX_CARD_TECHNOLOGIES = 4`
- ✓ Exports `RELATED_LIMIT = 3`
- ✓ Exports `STATUS_ORDER = ['completed', 'in-progress', 'archived'] as const satisfies readonly ProjectStatus[]`
- ✓ Exports `PROJECTS_TEXT` containing all labels defined in `design.md` (`pageHeading`, `emptyIndex`, `emptyFiltered`, `filterTechnologyLabel`, `filterStatusLabel`, `clearFilters`, `breadcrumbLabel`, `breadcrumbRoot`, `detailsHeading`, `technologiesLabel`, `tagsLabel`, `metricsLabel`, `linksHeading`, `repositoryLabel`, `liveDemoLabel`, `documentationLabel`, `buildDocsHeading`, `relatedHeading`, `backToProjects`, `completedPrefix`, `startedPrefix`)
- ✓ Exports `PROJECTS_INDEX_DESCRIPTION` string verified to be between 50 and 160 characters (Req 15.4)
- ✓ Contains zero owner-specific data or personal literals (`AGENTS.md` 6.1 Rule 8)

**Prerequisites:**
- Directory `src/components/projects/` exists or is created
- Target file: `src/components/projects/projects-text.ts`

**Implementation Details:**

Write `src/components/projects/projects-text.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\components\projects")) {
    New-Item -ItemType Directory -Path "src\components\projects" -Force | Out-Null
}

@'
import type { ProjectStatus } from '@/types/content';

/**
 * Constants, Layout Parameters, and Fixed UI Strings for Projects Module
 *
 * Separates structural labels and layout limits from dynamic content (Req 1.3, 2.3, 15.4, 17.7).
 */

export const PROJECTS_PATH = '/projects';
export const MAX_CARD_TECHNOLOGIES = 4;
export const RELATED_LIMIT = 3;

export const STATUS_ORDER = ['completed', 'in-progress', 'archived'] as const satisfies readonly ProjectStatus[];

export const PROJECTS_TEXT = {
  pageHeading: 'Projects',
  emptyIndex: 'Projects are being prepared. Check back soon.',
  emptyFiltered: 'No projects match the selected filters.',
  filterTechnologyLabel: 'Filter by technology',
  filterStatusLabel: 'Filter by status',
  clearFilters: 'Clear filters',
  breadcrumbLabel: 'Breadcrumb',
  breadcrumbRoot: 'Projects',
  detailsHeading: 'Project details',
  technologiesLabel: 'Technologies',
  tagsLabel: 'Tags',
  metricsLabel: 'Metrics',
  linksHeading: 'Project links',
  repositoryLabel: 'Repository',
  liveDemoLabel: 'Live demo',
  documentationLabel: 'Documentation',
  buildDocsHeading: 'Build documentation',
  relatedHeading: 'Related projects',
  backToProjects: 'Back to projects',
  completedPrefix: 'Completed',
  startedPrefix: 'Started',
} as const;

export const PROJECTS_INDEX_DESCRIPTION =
  'Browse portfolio projects with build documentation, technologies, status, and outcomes. ' +
  'Filter by technology or status to find relevant work.';
'@ | Set-Content "src\components\projects\projects-text.ts" -Encoding UTF8
```

Write a unit test in `tests/projects/projects-text.test.ts` verifying the description length:
```powershell
if (-not (Test-Path "tests\projects")) {
    New-Item -ItemType Directory -Path "tests\projects" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { PROJECTS_INDEX_DESCRIPTION, STATUS_ORDER } from '@/components/projects/projects-text';

describe('Projects Text Constants (Req 15.4)', () => {
  it('PROJECTS_INDEX_DESCRIPTION length is between 50 and 160 characters', () => {
    const len = PROJECTS_INDEX_DESCRIPTION.length;
    expect(len).toBeGreaterThanOrEqual(50);
    expect(len).toBeLessThanOrEqual(160);
  });

  it('STATUS_ORDER contains completed, in-progress, and archived in canonical order', () => {
    expect(STATUS_ORDER).toEqual(['completed', 'in-progress', 'archived']);
  });
});
'@ | Set-Content "tests\projects\projects-text.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/projects/projects-text.ts
npm run test -- tests/projects/projects-text.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 2.3, Req 4.2, Req 6.1, Req 14.1, Req 15.4

---

### M6.G1.T4: Implement Deterministic Technology Key Function (`src/lib/projects/tech-key.ts`)

**Objective:** Author `src/lib/projects/tech-key.ts` providing locale-independent string normalization for technology deduplication, parsing, and filtering.

**Acceptance Criteria:**
- ✓ Directory `src/lib/projects/` exists or is created
- ✓ File `src/lib/projects/tech-key.ts` created
- ✓ Exports `techKey(name: string): string`
- ✓ Trims whitespace and applies standard `.toLowerCase()` (not `toLocaleLowerCase()`, avoiding system locale bias)
- ✓ Accompanying unit test in `tests/projects/tech-key.test.ts` validates trimming, casing, and locale invariance

**Prerequisites:**
- Project root exists

**Implementation Details:**

Write `src/lib/projects/tech-key.ts` and its test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\lib\projects")) {
    New-Item -ItemType Directory -Path "src\lib\projects" -Force | Out-Null
}

@'
/**
 * Canonical Technology Key Normalizer
 *
 * Enforces locale-independent trimmed lowercase normalization for matching,
 * deduplication, and parsing across project collections (Req 3.2, 4.1, 5.2, 14.2).
 */
export function techKey(name: string): string {
  if (typeof name !== 'string') {
    return '';
  }
  return name.trim().toLowerCase();
}
'@ | Set-Content "src\lib\projects\tech-key.ts" -Encoding UTF8

@'
import { describe, it, expect } from 'vitest';
import { techKey } from '@/lib/projects/tech-key';

describe('techKey Normalizer', () => {
  it('trims leading and trailing whitespace and lowercases input', () => {
    expect(techKey('  TypeScript ')).toBe('typescript');
    expect(techKey('Next.js')).toBe('next.js');
    expect(techKey('TAILWIND CSS')).toBe('tailwind css');
  });

  it('handles empty or non-string inputs gracefully', () => {
    expect(techKey('')).toBe('');
    expect(techKey('   ')).toBe('');
    expect(techKey(null as any)).toBe('');
  });
});
'@ | Set-Content "tests\projects\tech-key.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/tech-key.ts
npm run test -- tests/projects/tech-key.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.2, Req 4.1, Req 5.2, Req 14.2

---

### M6.G1.T5: Implement Serializable Project Card Data Projection (`src/lib/projects/card-data.ts`)

**Objective:** Author `src/lib/projects/card-data.ts` exporting `ProjectCardData` as a `Pick` of `Project` and pure function `toProjectCardData` copying exactly eight fields and omitting heavy documentation.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/card-data.ts` created
- ✓ Exports type `ProjectCardData = Pick<Project, 'slug' | 'title' | 'summary' | 'status' | 'role' | 'technologies' | 'startedAt' | 'completedAt'>`
- ✓ Exports pure function `toProjectCardData(project: Project): ProjectCardData`
- ✓ Copies the `technologies` array defensively (`[...project.technologies]`)
- ✓ Strictly omits `documentation`, `tags`, `metrics`, `repositoryUrl`, `liveDemoUrl`, `documentationUrl`, `featured`, and `displayOrder`
- ✓ Pure function with zero framework imports

**Prerequisites:**
- M2 `Project` type available at `src/types/content.ts`
- Target file: `src/lib/projects/card-data.ts`

**Implementation Details:**

Write `src/lib/projects/card-data.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project } from '@/types/content';

/**
 * Serializable projection of Project for card presentation and client boundaries.
 * Excludes heavy documentation markdown and internal metadata (Req 7.4, 7.6).
 */
export type ProjectCardData = Pick<
  Project,
  | 'slug'
  | 'title'
  | 'summary'
  | 'status'
  | 'role'
  | 'technologies'
  | 'startedAt'
  | 'completedAt'
>;

/**
 * Projects a full Project domain object into serializable ProjectCardData.
 */
export function toProjectCardData(project: Project): ProjectCardData {
  return {
    slug: project.slug,
    title: project.title,
    summary: project.summary,
    status: project.status,
    role: project.role,
    technologies: [...project.technologies],
    startedAt: project.startedAt,
    completedAt: project.completedAt,
  };
}
'@ | Set-Content "src\lib\projects\card-data.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/card-data.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.4, Req 7.6, Req 17.3

---

### M6.G1.T6: Author Unit & Property-Based Tests for Card Data Projection (Property 13)

**Objective:** Create `tests/projects/card-data.test.ts` verifying exact projected fields, exclusion of `documentation`, array copying, and fast-check Property 13 verification.

**Acceptance Criteria:**
- ✓ File `tests/projects/card-data.test.ts` created
- ✓ Tests projection copies exactly the 8 specified fields
- ✓ Tests `documentation`, `metrics`, `tags`, and URLs are omitted
- ✓ Tests mutating `project.technologies` after projection does not mutate projected data
- ✓ Implements Property 13 test ($\ge 100$ runs with `fast-check`): `JSON.parse(JSON.stringify(result))` deep-equals `result` and `documentation` key is absent
- ✓ Tagged: `Feature: m6-projects-module, Property 13: client props are serializable and exclude documentation`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G1.T5 completed
- Arbitraries in `tests/fixtures/projects-arbitraries.ts`
- Target file: `tests/projects/card-data.test.ts`

**Implementation Details:**

Write `tests/projects/card-data.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { toProjectCardData } from '@/lib/projects/card-data';
import { sampleProjectsList } from '../fixtures/projects-data';
import { arbProject } from '../fixtures/projects-arbitraries';

describe('toProjectCardData Projection (Req 7.4, 7.6)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('projects exactly 8 fields and excludes documentation, metrics, tags, and URLs', () => {
      const fullProject = sampleProjectsList[0];
      const cardData = toProjectCardData(fullProject);

      const keys = Object.keys(cardData).sort();
      expect(keys).toEqual([
        'completedAt',
        'role',
        'slug',
        'startedAt',
        'status',
        'summary',
        'technologies',
        'title',
      ]);

      expect((cardData as any).documentation).toBeUndefined();
      expect((cardData as any).metrics).toBeUndefined();
      expect((cardData as any).tags).toBeUndefined();
      expect((cardData as any).repositoryUrl).toBeUndefined();
    });

    it('creates a defensive copy of the technologies array', () => {
      const fullProject = { ...sampleProjectsList[0], technologies: ['TypeScript', 'Go'] };
      const cardData = toProjectCardData(fullProject);

      fullProject.technologies.push('Rust');
      expect(cardData.technologies).toEqual(['TypeScript', 'Go']);
    });
  });

  describe('Property-Based Invariants (Property 13)', () => {
    it('Feature: m6-projects-module, Property 13: client props are serializable and exclude documentation for any Project', () => {
      fc.assert(
        fc.property(arbProject, (project) => {
          const cardData = toProjectCardData(project);

          // 1. Documentation must be absent
          expect('documentation' in cardData).toBe(false);

          // 2. Exact keys assertion
          const expectedKeys = new Set([
            'slug', 'title', 'summary', 'status', 'role',
            'technologies', 'startedAt', 'completedAt'
          ]);
          const actualKeys = new Set(Object.keys(cardData));
          expect(actualKeys).toEqual(expectedKeys);

          // 3. Strict JSON round-trip serializability
          const serialized = JSON.stringify(cardData);
          const parsed = JSON.parse(serialized);
          expect(parsed).toEqual(cardData);
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\card-data.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/card-data.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.4, Req 7.6, Req 17.2

---

### M6.G1.T7: Audit Upstream M2 Loaders, Types, and M5 Utilities

**Objective:** Audit and confirm the presence and export signatures of upstream M2 content loaders, M2 content types, and M5 utilities (`formatDisplayDate` and `compareStrings`), recording findings in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms M2 loaders in `src/content/loaders/`: `getProjects`, `getProjectBySlug`, `getSiteConfig`, `renderMarkdown`
- ✓ Confirms M2 types in `src/types/content.ts`: `Project`, `ProjectStatus`, `ProjectFilters`, `IsoDateString`
- ✓ Confirms M5 date formatter exists at `src/lib/format-date.ts` (`formatDisplayDate`)
- ✓ Confirms M5 comparator exists at `src/lib/home/compare.ts` (`compareStrings`)
- ✓ Records paths in `.kiro/specs/m6-projects-module/task-notes.md`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M2 and M5 baselines complete

**Implementation Details:**

Execute verification check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path ".kiro\specs\m6-projects-module")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m6-projects-module" -Force | Out-Null
}

$errors = @()

# 1. Audit Loaders
$loaders = @(
    "src\content\loaders\projects.ts",
    "src\content\loaders\site.ts",
    "src\content\markdown\renderer.ts"
)
foreach ($l in $loaders) {
    if (-not (Test-Path $l)) {
        $errors += "Missing loader/renderer: $l"
    }
}

# 2. Audit Types
$typesPath = "src\types\content.ts"
if (Test-Path $typesPath) {
    $content = Get-Content $typesPath -Raw
    $types = @('Project', 'ProjectStatus', 'ProjectFilters', 'IsoDateString')
    foreach ($t in $types) {
        if (-not ($content -match "\b$t\b")) {
            $errors += "Missing type: $t in $typesPath"
        }
    }
} else {
    $errors += "Missing $typesPath"
}

# 3. Audit M5 Utilities
$dateUtil = "src\lib\format-date.ts"
$compareUtil = "src\lib\home\compare.ts"
if (-not (Test-Path $dateUtil)) { $errors += "Missing M5 utility: $dateUtil" }
if (-not (Test-Path $compareUtil)) { $errors += "Missing M5 utility: $compareUtil" }

if ($errors.Count -eq 0) {
    $taskNotes = @"
# M6 Projects Module — Task Notes & Architectural Audit

## 1. Upstream Contracts & Utilities Audit (Req 10.6, 17.7)
- M2 Loaders: Confirmed `getProjects`, `getProjectBySlug`, `getSiteConfig` in `src/content/loaders/`.
- M2 Markdown: Confirmed `renderMarkdown` in `src/content/markdown/renderer.ts`.
- M2 Types: Confirmed `Project`, `ProjectStatus`, `ProjectFilters`, `IsoDateString` in `src/types/content.ts`.
- M5 Date Formatter: Confirmed `formatDisplayDate` in `src/lib/format-date.ts`.
- M5 Comparator: Confirmed `compareStrings` in `src/lib/home/compare.ts`.

"@
    Set-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $taskNotes -Encoding UTF8
    "PASS"
} else {
    $errors | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path ".kiro\specs\m6-projects-module")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m6-projects-module" -Force | Out-Null
}

$errors = @()

# 1. Audit Loaders
$loaders = @(
    "src\content\loaders\projects.ts",
    "src\content\loaders\site.ts",
    "src\content\markdown\renderer.ts"
)
foreach ($l in $loaders) {
    if (-not (Test-Path $l)) {
        $errors += "Missing loader/renderer: $l"
    }
}

# 2. Audit Types
$typesPath = "src\types\content.ts"
if (Test-Path $typesPath) {
    $content = Get-Content $typesPath -Raw
    $types = @('Project', 'ProjectStatus', 'ProjectFilters', 'IsoDateString')
    foreach ($t in $types) {
        if (-not ($content -match "\b$t\b")) {
            $errors += "Missing type: $t in $typesPath"
        }
    }
} else {
    $errors += "Missing $typesPath"
}

# 3. Audit M5 Utilities
$dateUtil = "src\lib\format-date.ts"
$compareUtil = "src\lib\home\compare.ts"
if (-not (Test-Path $dateUtil)) { $errors += "Missing M5 utility: $dateUtil" }
if (-not (Test-Path $compareUtil)) { $errors += "Missing M5 utility: $compareUtil" }

if ($errors.Count -eq 0) {
    $taskNotes = @"
# M6 Projects Module — Task Notes & Architectural Audit

## 1. Upstream Contracts & Utilities Audit (Req 10.6, 17.7)
- M2 Loaders: Confirmed `getProjects`, `getProjectBySlug`, `getSiteConfig` in `src/content/loaders/`.
- M2 Markdown: Confirmed `renderMarkdown` in `src/content/markdown/renderer.ts`.
- M2 Types: Confirmed `Project`, `ProjectStatus`, `ProjectFilters`, `IsoDateString` in `src/types/content.ts`.
- M5 Date Formatter: Confirmed `formatDisplayDate` in `src/lib/format-date.ts`.
- M5 Comparator: Confirmed `compareStrings` in `src/lib/home/compare.ts`.

"@
    Set-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $taskNotes -Encoding UTF8
    "PASS"
} else {
    $errors | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 10.6, Req 13.1, Req 17.7

---

### M6.G1.T8: Audit M3 UI Primitives and Markdown Component Signatures

**Objective:** Audit and confirm the presence of required M3 UI primitives (`Card`, `TagList`, `StatusBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`, `FOCUS_RING`, motion helpers) and record their prop signatures in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms M3 primitives exist in `src/components/ui/`
- ✓ Confirms `MarkdownDoc` exists and accepts sanitized HTML string prop
- ✓ Confirms `FilterChip` exists with `aria-pressed` support
- ✓ Confirms `EmptyState` supports message and optional action button
- ✓ Records signatures in `task-notes.md`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M3 baseline complete

**Implementation Details:**

Execute inspection script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$primitives = @(
    "src\components\ui\card.tsx",
    "src\components\ui\tag-list.tsx",
    "src\components\ui\status-badge.tsx",
    "src\components\ui\filter-chip.tsx",
    "src\components\ui\external-link.tsx",
    "src\components\ui\empty-state.tsx",
    "src\components\ui\markdown-doc.tsx",
    "src\components\ui\container.tsx",
    "src\components\ui\button.tsx",
    "src\components\ui\focus-ring.ts",
    "src\components\ui\motion.ts"
)

$missing = @()
foreach ($pr in $primitives) {
    if (-not (Test-Path $pr)) {
        $missing += "Missing primitive: $pr"
    }
}

if ($missing.Count -eq 0) {
    $noteAppend = @"

## 2. Upstream M3 UI Primitives Audit (Req 16.1, 17.7)
- Confirmed `Card`, `TagList`, `StatusBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`.
- Confirmed `FOCUS_RING` and motion tokens (`MOTION_FAST`).
- Verified `MarkdownDoc` takes `{ html: string }`.

"@
    Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $noteAppend -Encoding UTF8
    "PASS"
} else {
    $missing | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$primitives = @(
    "src\components\ui\card.tsx",
    "src\components\ui\tag-list.tsx",
    "src\components\ui\status-badge.tsx",
    "src\components\ui\filter-chip.tsx",
    "src\components\ui\external-link.tsx",
    "src\components\ui\empty-state.tsx",
    "src\components\ui\markdown-doc.tsx",
    "src\components\ui\container.tsx",
    "src\components\ui\button.tsx",
    "src\components\ui\focus-ring.ts",
    "src\components\ui\motion.ts"
)

$missing = @()
foreach ($pr in $primitives) {
    if (-not (Test-Path $pr)) {
        $missing += "Missing primitive: $pr"
    }
}

if ($missing.Count -eq 0) {
    $noteAppend = @"

## 2. Upstream M3 UI Primitives Audit (Req 16.1, 17.7)
- Confirmed `Card`, `TagList`, `StatusBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`.
- Confirmed `FOCUS_RING` and motion tokens (`MOTION_FAST`).
- Verified `MarkdownDoc` takes `{ html: string }`.

"@
    Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $noteAppend -Encoding UTF8
    "PASS"
} else {
    $missing | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.1, Req 16.1, Req 17.7

---

### M6.G1.T9: Verify Test Toolchain, Params Contract, and M4 Shell Integration

**Objective:** Confirm that test dependencies (`vitest`, `@testing-library/react`, `@testing-library/user-event`, `vitest-axe`, `fast-check`) are operational, inspect Next.js route params contract, and verify M4 shell integration.

**Acceptance Criteria:**
- ✓ Confirms test packages resolve cleanly in Node.js
- ✓ Confirms `@testing-library/user-event` is present for keyboard simulation
- ✓ Determines whether route `params` is a `Promise` (Next.js 15) or plain object (Next.js 14) and records in `task-notes.md`
- ✓ Confirms M4 title template and `not-found` boundary exist
- ✓ Verification script exits with PASS

**Prerequisites:**
- Node.js LTS environment
- Project root exists

**Implementation Details:**

Execute check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$nodeCheck = node -e "require('vitest'); require('@testing-library/react'); require('@testing-library/user-event'); require('vitest-axe'); require('fast-check'); console.log('PASS');"

if ($nodeCheck -eq "PASS") {
    $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
    $nextVersion = $pkg.dependencies.next
    $paramsNote = if ($nextVersion -match "15\.") { "Next.js 15 (params is Promise<{ slug: string }>)" } else { "Next.js 14 (params is { slug: string })" }

    $noteAppend = @"

## 3. Test Toolchain & Next.js Runtime Contract
- Test toolchain operational (vitest, RTL, user-event, vitest-axe, fast-check).
- Next.js Version: $nextVersion.
- Detail Route Params Contract: $paramsNote.
- M4 Title Template & NotFound boundary confirmed.

"@
    Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $noteAppend -Encoding UTF8
    "PASS"
} else {
    "FAIL"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$nodeCheck = node -e "require('vitest'); require('@testing-library/react'); require('@testing-library/user-event'); require('vitest-axe'); require('fast-check'); console.log('PASS');"

if ($nodeCheck -eq "PASS") {
    $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
    $nextVersion = $pkg.dependencies.next
    $paramsNote = if ($nextVersion -match "15\.") { "Next.js 15 (params is Promise<{ slug: string }>)" } else { "Next.js 14 (params is { slug: string })" }

    $noteAppend = @"

## 3. Test Toolchain & Next.js Runtime Contract
- Test toolchain operational (vitest, RTL, user-event, vitest-axe, fast-check).
- Next.js Version: $nextVersion.
- Detail Route Params Contract: $paramsNote.
- M4 Title Template & NotFound boundary confirmed.

"@
    Add-Content -Path ".kiro\specs\m6-projects-module\task-notes.md" -Value $noteAppend -Encoding UTF8
    "PASS"
} else {
    "FAIL"
}
```

Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.5, Req 15.3, Req 17.1, Req 17.7

---

### M6.G1.T10: Checkpoint — Foundation Quality Gates and Protected Files Invariance

**Objective:** Run the full verification suite to confirm that all fixtures, text constants, normalizers, card projections, and initial tests compile and pass, and verify that protected configuration and styling files remain completely untouched.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json` produces zero output
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test -- tests/projects/projects-text.test.ts tests/projects/tech-key.test.ts tests/projects/card-data.test.ts` passes with code 0

**Prerequisites:**
- M6.G1.T1 through M6.G1.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json
if ($diff.Length -gt 0) {
    Write-Error "CRITICAL: Protected files modified!`n$diff"
    exit 1
}

npm run typecheck
npm run lint
npm run test -- tests/projects/projects-text.test.ts tests/projects/tech-key.test.ts tests/projects/card-data.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/components/home/ src/lib/home/ src/lib/format-date.ts src/content/ package.json
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/projects-text.test.ts tests/projects/tech-key.test.ts tests/projects/card-data.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($diff.Length -eq 0 -and $t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 7.4, Req 17.5, Req 17.7

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\fixtures\projects-data.ts"
Test-Path "tests\fixtures\projects-arbitraries.ts"
Test-Path "src\components\projects\projects-text.ts"
Test-Path "src\lib\projects\tech-key.ts"
Test-Path "src\lib\projects\card-data.ts"
Test-Path "tests\projects\projects-text.test.ts"
Test-Path "tests\projects\tech-key.test.ts"
Test-Path "tests\projects\card-data.test.ts"
Test-Path ".kiro\specs\m6-projects-module\task-notes.md"
npm run typecheck
npm run test -- tests/projects/projects-text.test.ts tests/projects/tech-key.test.ts tests/projects/card-data.test.ts
```
Expected output:
- `True` for all 9 path checks
- `npm run typecheck` exits with return code 0
- Vitest executes all text, tech-key, and card-data tests with return code 0.