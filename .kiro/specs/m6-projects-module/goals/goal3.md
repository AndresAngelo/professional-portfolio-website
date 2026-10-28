# M6.G3: Filtering, Related Selection, Links, Heading Demotion, Result Count, and Metadata Builders

> **Milestone:** M6 — Projects Module  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement all remaining pure domain helpers in `src/lib/projects/`: `filter-projects.ts`, `select-related-projects.ts`, `get-project-links.ts`, `demote-headings.ts`, `format-result-count.ts`, and `project-metadata.ts`. `filterProjects` executes boolean AND filtering across projects without altering relative order or matching against tags, titles, or summaries. `selectRelatedProjects` identifies up to 3 related projects sharing at least one technology, ordered by shared count descending, then `displayOrder` ascending, then `slug` ascending, strictly excluding the current project. `getProjectLinks` normalizes and filters repository, demo, and documentation links, omitting null or blank entries. `demoteHeadings` shifts Markdown headings by one level if an `<h1>` is detected, ensuring no `<h1>` appears inside documentation. `formatResultCount` generates deterministic live region text (`"1 project shown"` vs `"{n} projects shown"`). `buildProjectsIndexMetadata` and `buildProjectDetailMetadata` construct Next.js metadata objects deriving canonical URLs without query strings. Guarantee that all helpers are pure, React/DOM-free, and leave deeply frozen inputs completely untouched. Validate all helpers with Vitest unit tests and fast-check property tests for Properties 5, 6, 7, 8, 9, 10, 11, 18, and 21.

## Goal Success Criteria

- ✓ `src/lib/projects/filter-projects.ts` exports pure generic function `filterProjects` executing logical AND filtering while preserving input order
- ✓ `src/lib/projects/select-related-projects.ts` exports pure function `selectRelatedProjects` returning at most 3 related projects ordered by overlap count descending, `displayOrder` ascending, and `slug` ascending
- ✓ `src/lib/projects/get-project-links.ts` exports `ProjectLinkItem` and pure function `getProjectLinks` returning valid trimmed links in canonical order (Repository, Live demo, Documentation)
- ✓ `src/lib/projects/demote-headings.ts` exports pure function `demoteHeadings` shifting headings by one level if `<h1>` is present, leaving non-`h1` HTML completely untouched
- ✓ `src/lib/projects/format-result-count.ts` exports pure function `formatResultCount(count: number): string`
- ✓ `src/lib/projects/project-metadata.ts` exports `ProjectsMetadata`, `buildProjectsIndexMetadata`, and `buildProjectDetailMetadata`
- ✓ Zero imports from `react`, `next`, or DOM globals (`window`, `document`) across all helper modules
- ✓ Unit and property tests in `tests/projects/filter-projects.test.ts` satisfy Properties 5, 6, and 7 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/projects/select-related-projects.test.ts` satisfy Properties 9 and 10 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/projects/demote-headings.test.ts` satisfy Property 18 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/projects/format-result-count.test.ts` satisfy Property 11 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/projects/project-metadata.test.ts` satisfy Property 21 ($\ge 100$ runs with `fast-check`)
- ✓ Purity tests in `tests/projects/purity.test.ts` satisfy Property 8 across all pure helpers on deeply frozen inputs ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M6.G1 and M6.G2 completed (`tech-key.ts`, `projects-text.ts`, `card-data.ts`, `filter-params.ts`, and M5's `compareStrings` available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G3.T1: Implement Generic Project Filtering Helper (`src/lib/projects/filter-projects.ts`)

**Objective:** Author generic pure function `filterProjects` in `src/lib/projects/filter-projects.ts` applying logical AND filtering while preserving input order.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/filter-projects.ts` created
- ✓ Exports `filterProjects<T extends Pick<Project, 'technologies' | 'status'>>(projects: readonly T[], filters: ProjectFilters): T[]`
- ✓ Returns all projects in original order when filters are in the Unfiltered_State
- ✓ Matches `technology` case-insensitively using `techKey`
- ✓ Matches `status` using strict equality
- ✓ Applies boolean AND: returns only items matching both active criteria
- ✓ Does NOT filter or match against tags, title, or summary (Req 5.7)
- ✓ Does NOT mutate input array or objects
- ✓ Pure function with zero framework imports

**Prerequisites:**
- M6.G1 completed (`tech-key.ts` available)
- Target file: `src/lib/projects/filter-projects.ts`

**Implementation Details:**

Write `src/lib/projects/filter-projects.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project, ProjectFilters } from '@/types/content';
import { techKey } from './tech-key';

/**
 * Pure Project Filtering Helper
 *
 * Filters projects by technology and status using logical AND semantics.
 * Preserves input sort order and reads no tags, titles, or summaries (Req 5.1-5.7, 17.3).
 */
export function filterProjects<T extends Pick<Project, 'technologies' | 'status'>>(
  projects: readonly T[],
  filters: ProjectFilters
): T[] {
  const targetTechKey = filters.technology !== null ? techKey(filters.technology) : null;
  const targetStatus = filters.status;

  // Fast path: Unfiltered_State returns shallow copy preserving original order
  if (targetTechKey === null && targetStatus === null) {
    return [...projects];
  }

  return projects.filter((project) => {
    // 1. Technology match: true if technology filter is null or project contains target techKey
    let matchesTech = true;
    if (targetTechKey !== null) {
      matchesTech = (project.technologies || []).some(
        (t) => typeof t === 'string' && techKey(t) === targetTechKey
      );
    }

    // 2. Status match: true if status filter is null or project matches status
    let matchesStatus = true;
    if (targetStatus !== null) {
      matchesStatus = project.status === targetStatus;
    }

    // Logical AND
    return matchesTech && matchesStatus;
  });
}
'@ | Set-Content "src\lib\projects\filter-projects.ts" -Encoding UTF8
```

Write unit scenarios in `tests/projects/filter-projects.test.ts`:
```powershell
@'
import { describe, it, expect } from 'vitest';
import { filterProjects } from '@/lib/projects/filter-projects';
import { sampleProjectsList } from '../fixtures/projects-data';

describe('filterProjects Helper (Req 5)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns all projects in original order when filters are in Unfiltered_State', () => {
      const result = filterProjects(sampleProjectsList, { technology: null, status: null });
      expect(result.length).toBe(sampleProjectsList.length);
      expect(result.map((p) => p.slug)).toEqual(sampleProjectsList.map((p) => p.slug));
    });

    it('filters by technology case-insensitively and ignores tags/summary', () => {
      // In sampleProjectsList, Docker is in Alpha (completed), Beta (in-progress), Epsilon (completed)
      const result = filterProjects(sampleProjectsList, { technology: 'docker', status: null });
      expect(result.map((p) => p.slug)).toEqual([
        'alpha-pipeline-core',
        'beta-agent-orchestrator',
        'epsilon-state-sync',
      ]);
    });

    it('filters by status strictly', () => {
      const result = filterProjects(sampleProjectsList, { technology: null, status: 'in-progress' });
      expect(result.map((p) => p.slug)).toEqual([
        'beta-agent-orchestrator',
        'zeta-ui-primitives',
      ]);
    });

    it('applies logical AND when both filters are active', () => {
      const result = filterProjects(sampleProjectsList, { technology: 'Docker', status: 'in-progress' });
      expect(result.map((p) => p.slug)).toEqual(['beta-agent-orchestrator']);
    });

    it('returns empty array when filters match no projects', () => {
      const result = filterProjects(sampleProjectsList, { technology: 'Go', status: 'archived' });
      expect(result).toEqual([]);
    });
  });
});
'@ | Set-Content "tests\projects\filter-projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/filter-projects.ts
npm run test -- tests/projects/filter-projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 5.7, Req 17.3

---

### M6.G3.T2: Author Property-Based Tests for Project Filtering (Properties 5, 6, 7)

**Objective:** Append property-based tests in `tests/projects/filter-projects.test.ts` validating Property 5 (model equality), Property 6 (idempotence), and Property 7 (monotonicity).

**Acceptance Criteria:**
- ✓ Implements Property 5 test ($\ge 100$ runs with `fast-check`): result equals model filter specification exactly
- ✓ Tagged: `Feature: m6-projects-module, Property 5: filtering matches the specified model`
- ✓ Implements Property 6 test ($\ge 100$ runs with `fast-check`): `filterProjects(filterProjects(p, f), f) === filterProjects(p, f)`
- ✓ Tagged: `Feature: m6-projects-module, Property 6: filtering is idempotent`
- ✓ Implements Property 7 test ($\ge 100$ runs with `fast-check`): adding a filter never increases result set size
- ✓ Tagged: `Feature: m6-projects-module, Property 7: adding a filter never adds results`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G3.T1 completed
- Arbitraries in `tests/fixtures/projects-arbitraries.ts`
- Target file: `tests/projects/filter-projects.test.ts`

**Implementation Details:**

Append property tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Properties 5, 6, 7)', () => {
    const fc = require('fast-check');
    const { arbProjectsList, arbFilterOptions, arbProjectFilters } = require('../fixtures/projects-arbitraries');

    it('Feature: m6-projects-module, Property 5: filtering matches the specified model and preserves input order', () => {
      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(arbProjectsList, arbProjectFilters(opts))
          ),
          ([projects, filters]: any) => {
            const result = filterProjects(projects, filters);

            // Subsequence check
            let projectIdx = 0;
            for (const item of result) {
              while (projectIdx < projects.length && projects[projectIdx].slug !== item.slug) {
                projectIdx++;
              }
              expect(projectIdx).toBeLessThan(projects.length);
              projectIdx++;
            }

            // Every item satisfies filters
            for (const p of result) {
              if (filters.technology !== null) {
                const targetKey = filters.technology.trim().toLowerCase();
                const hasTech = p.technologies.some((t: string) => t.trim().toLowerCase() === targetKey);
                expect(hasTech).toBe(true);
              }
              if (filters.status !== null) {
                expect(p.status).toBe(filters.status);
              }
            }
          }
        ),
        { numRuns: 100 }
      );
    });

    it('Feature: m6-projects-module, Property 6: filtering is idempotent for any project array and filter set', () => {
      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(arbProjectsList, arbProjectFilters(opts))
          ),
          ([projects, filters]: any) => {
            const firstPass = filterProjects(projects, filters);
            const secondPass = filterProjects(firstPass, filters);
            expect(secondPass).toEqual(firstPass);
          }
        ),
        { numRuns: 100 }
      );
    });

    it('Feature: m6-projects-module, Property 7: adding a filter never adds results (monotonicity)', () => {
      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(arbProjectsList, arbProjectFilters(opts), fc.constant(opts))
          ),
          ([projects, baseFilters, opts]: any) => {
            const baseResult = filterProjects(projects, baseFilters);

            // If technology was null, set it
            if (baseFilters.technology === null && opts.technologies.length > 0) {
              const narrowed = filterProjects(projects, {
                ...baseFilters,
                technology: opts.technologies[0],
              });
              expect(narrowed.length).toBeLessThanOrEqual(baseResult.length);
              for (const p of narrowed) {
                expect(baseResult.some((b: any) => b.slug === p.slug)).toBe(true);
              }
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\filter-projects.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\filter-projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/filter-projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.5, Req 5.6, Req 17.2

---

### M6.G3.T3: Implement Related Projects Selection Helper (`src/lib/projects/select-related-projects.ts`)

**Objective:** Author `selectRelatedProjects` in `src/lib/projects/select-related-projects.ts` identifying up to 3 related projects based on shared technology overlap.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/select-related-projects.ts` created
- ✓ Exports `selectRelatedProjects(current: Project, all: readonly Project[]): Project[]`
- ✓ Excludes candidate where `slug === current.slug`
- ✓ Compares technologies case-insensitively using `techKey`
- ✓ Requires shared technology count $> 0$
- ✓ Deduplicates candidates by slug (first-seen wins)
- ✓ Sorts candidates: shared technology count descending, then `displayOrder` ascending, then `slug` ascending via `compareStrings`
- ✓ Slices output array to `RELATED_LIMIT` (3)
- ✓ Does not mutate input arguments

**Prerequisites:**
- M6.G1 completed (`tech-key.ts`, `RELATED_LIMIT` in `projects-text.ts`, M5 `compareStrings`)
- Target file: `src/lib/projects/select-related-projects.ts`

**Implementation Details:**

Write `src/lib/projects/select-related-projects.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project } from '@/types/content';
import { RELATED_LIMIT } from '@/components/projects/projects-text';
import { compareStrings } from '@/lib/home/compare';
import { techKey } from './tech-key';

interface ScoredCandidate {
  project: Project;
  sharedCount: number;
}

/**
 * Pure Related Projects Selection Helper
 *
 * Selects up to RELATED_LIMIT related projects sharing technologies with current project.
 * Ranked by shared technology overlap descending, displayOrder ascending, and slug ascending (Req 14.1-14.5).
 */
export function selectRelatedProjects(
  current: Project,
  all: readonly Project[]
): Project[] {
  if (!all || all.length === 0 || !current.technologies || current.technologies.length === 0) {
    return [];
  }

  // Set of current project's normalized technology keys
  const currentKeys = new Set(
    current.technologies
      .map((t) => techKey(t))
      .filter((k) => k.length > 0)
  );

  if (currentKeys.size === 0) {
    return [];
  }

  const seenSlugs = new Set<string>();
  const scored: ScoredCandidate[] = [];

  for (const candidate of all) {
    // Exclude current project itself
    if (candidate.slug === current.slug) {
      continue;
    }
    // Deduplicate candidate slugs in input
    if (seenSlugs.has(candidate.slug)) {
      continue;
    }
    seenSlugs.add(candidate.slug);

    // Compute distinct shared technology keys
    let sharedCount = 0;
    const candidateKeys = new Set(
      (candidate.technologies || [])
        .map((t) => techKey(t))
        .filter((k) => k.length > 0)
    );

    for (const key of candidateKeys) {
      if (currentKeys.has(key)) {
        sharedCount++;
      }
    }

    if (sharedCount > 0) {
      scored.push({
        project: candidate,
        sharedCount,
      });
    }
  }

  // Sort candidates
  scored.sort((a, b) => {
    // 1. Shared count descending
    if (a.sharedCount !== b.sharedCount) {
      return b.sharedCount - a.sharedCount;
    }
    // 2. displayOrder ascending
    if (a.project.displayOrder !== b.project.displayOrder) {
      return a.project.displayOrder - b.project.displayOrder;
    }
    // 3. slug ascending (code-unit order)
    return compareStrings(a.project.slug, b.project.slug);
  });

  return scored.slice(0, RELATED_LIMIT).map((item) => item.project);
}
'@ | Set-Content "src\lib\projects\select-related-projects.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/select-related-projects.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.4, Req 14.5, Req 17.3

---

### M6.G3.T4: Author Unit & Property-Based Tests for Related Projects (Properties 9, 10)

**Objective:** Create `tests/projects/select-related-projects.test.ts` verifying concrete cases and fast-check Properties 9 and 10 for `selectRelatedProjects`.

**Acceptance Criteria:**
- ✓ File `tests/projects/select-related-projects.test.ts` created
- ✓ Tests current project is excluded
- ✓ Tests projects with zero technology overlap are excluded
- ✓ Tests ranking orders higher shared overlap first
- ✓ Implements Property 9 test ($\ge 100$ runs with `fast-check`): at most 3 items, distinct, excludes current, all share $\ge 1$ technology
- ✓ Tagged: `Feature: m6-projects-module, Property 9: related projects are bounded, distinct, and share a technology`
- ✓ Implements Property 10 test ($\ge 100$ runs with `fast-check`): ordered by overlap descending, displayOrder ascending, slug ascending
- ✓ Tagged: `Feature: m6-projects-module, Property 10: related projects are ordered by overlap, then display order, then slug`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G3.T3 completed
- Target file: `tests/projects/select-related-projects.test.ts`

**Implementation Details:**

Write `tests/projects/select-related-projects.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { selectRelatedProjects } from '@/lib/projects/select-related-projects';
import { sampleProjectsList, isolatedTechProject } from '../fixtures/projects-data';
import { arbProject, arbProjectsList } from '../fixtures/projects-arbitraries';
import { techKey } from '@/lib/projects/tech-key';

describe('selectRelatedProjects Helper (Req 14)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns at most 3 related projects sharing technologies with current project', () => {
      // sampleProjectsList[0] has: TypeScript, Go, Docker, Next.js
      const current = sampleProjectsList[0];
      const related = selectRelatedProjects(current, sampleProjectsList);

      expect(related.length).toBeLessThanOrEqual(3);
      expect(related.some((p) => p.slug === current.slug)).toBe(false);

      // Verify all returned share at least one technology
      for (const r of related) {
        const hasOverlap = r.technologies.some((t) =>
          current.technologies.map(techKey).includes(techKey(t))
        );
        expect(hasOverlap).toBe(true);
      }
    });

    it('returns empty array when candidate projects share zero technologies', () => {
      const related = selectRelatedProjects(isolatedTechProject, sampleProjectsList);
      expect(related).toEqual([]);
    });
  });

  describe('Property-Based Invariants (Properties 9, 10)', () => {
    it('Feature: m6-projects-module, Property 9: related projects are bounded, distinct, and share a technology for any input', () => {
      fc.assert(
        fc.property(arbProject, arbProjectsList, (current, all) => {
          const related = selectRelatedProjects(current, all);

          // 1. Bounded at 3
          expect(related.length).toBeLessThanOrEqual(3);

          // 2. Excludes current project
          expect(related.every((p) => p.slug !== current.slug)).toBe(true);

          // 3. Distinct slugs
          const slugs = related.map((p) => p.slug);
          expect(slugs.length).toBe(new Set(slugs).size);

          // 4. Shares at least one technology
          const currentKeys = new Set(current.technologies.map(techKey));
          for (const p of related) {
            const shares = p.technologies.some((t) => currentKeys.has(techKey(t)));
            expect(shares).toBe(true);
          }
        }),
        { numRuns: 100 }
      );
    });

    it('Feature: m6-projects-module, Property 10: related projects are ordered by overlap, then display order, then slug', () => {
      fc.assert(
        fc.property(arbProject, arbProjectsList, (current, all) => {
          const related = selectRelatedProjects(current, all);
          const currentKeys = new Set(current.technologies.map(techKey));

          const getOverlap = (p: any) =>
            new Set(p.technologies.map(techKey)).size > 0
              ? p.technologies.filter((t: string) => currentKeys.has(techKey(t))).length
              : 0;

          for (let i = 1; i < related.length; i++) {
            const prev = related[i - 1];
            const curr = related[i];
            const prevOverlap = getOverlap(prev);
            const currOverlap = getOverlap(curr);

            if (prevOverlap === currOverlap) {
              if (prev.displayOrder === curr.displayOrder) {
                expect(prev.slug.localeCompare(curr.slug)).toBeLessThanOrEqual(0);
              } else {
                expect(prev.displayOrder).toBeLessThan(curr.displayOrder);
              }
            } else {
              expect(prevOverlap).toBeGreaterThan(currOverlap);
            }
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\select-related-projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/select-related-projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.4, Req 14.5, Req 17.2

---

### M6.G3.T5: Implement Project Links Extractor Helper (`src/lib/projects/get-project-links.ts`)

**Objective:** Author `getProjectLinks` in `src/lib/projects/get-project-links.ts` extracting repository, demo, and documentation link items in deterministic order.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/get-project-links.ts` created
- ✓ Exports `interface ProjectLinkItem { readonly key: 'repository' | 'liveDemo' | 'documentation'; readonly label: string; readonly href: string; }`
- ✓ Exports `getProjectLinks(project: Pick<Project, 'repositoryUrl' | 'liveDemoUrl' | 'documentationUrl'>): ProjectLinkItem[]`
- ✓ Returns items strictly in canonical order: Repository, Live demo, Documentation
- ✓ Trims all URLs; excludes null, undefined, and whitespace-only URLs
- ✓ Labels are unique by construction (`Repository`, `Live demo`, `Documentation`)
- ✓ Accompanied by unit tests in `tests/projects/get-project-links.test.ts`

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- Target file: `src/lib/projects/get-project-links.ts`

**Implementation Details:**

Write `src/lib/projects/get-project-links.ts` and its test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project } from '@/types/content';
import { PROJECTS_TEXT } from '@/components/projects/projects-text';

export interface ProjectLinkItem {
  readonly key: 'repository' | 'liveDemo' | 'documentation';
  readonly label: string;
  readonly href: string;
}

/**
 * Extracts and normalizes external links for project presentation.
 * Omits null, undefined, and whitespace-only URLs in canonical sequence (Req 12.1-12.5).
 */
export function getProjectLinks(
  project: Pick<Project, 'repositoryUrl' | 'liveDemoUrl' | 'documentationUrl'>
): ProjectLinkItem[] {
  const links: ProjectLinkItem[] = [];

  const checkAndAdd = (
    key: ProjectLinkItem['key'],
    label: string,
    rawUrl: string | null | undefined
  ) => {
    if (typeof rawUrl === 'string') {
      const trimmed = rawUrl.trim();
      if (trimmed.length > 0) {
        links.push({ key, label, href: trimmed });
      }
    }
  };

  checkAndAdd('repository', PROJECTS_TEXT.repositoryLabel, project.repositoryUrl);
  checkAndAdd('liveDemo', PROJECTS_TEXT.liveDemoLabel, project.liveDemoUrl);
  checkAndAdd('documentation', PROJECTS_TEXT.documentationLabel, project.documentationUrl);

  return links;
}
'@ | Set-Content "src\lib\projects\get-project-links.ts" -Encoding UTF8

@'
import { describe, it, expect } from 'vitest';
import { getProjectLinks } from '@/lib/projects/get-project-links';
import { sampleProjectsList, noLinksProject } from '../fixtures/projects-data';

describe('getProjectLinks Helper (Req 12)', () => {
  it('extracts all three valid URLs in canonical order', () => {
    // sampleProjectsList[0] contains repository, liveDemo, and documentationUrl
    const links = getProjectLinks(sampleProjectsList[0]);
    expect(links.length).toBe(3);
    expect(links[0].label).toBe('Repository');
    expect(links[1].label).toBe('Live demo');
    expect(links[2].label).toBe('Documentation');
  });

  it('omits null and whitespace URLs completely', () => {
    expect(getProjectLinks(noLinksProject)).toEqual([]);
    expect(getProjectLinks({ repositoryUrl: '  ', liveDemoUrl: null, documentationUrl: undefined })).toEqual([]);
  });
});
'@ | Set-Content "tests\projects\get-project-links.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/get-project-links.ts
npm run test -- tests/projects/get-project-links.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.3, Req 12.4, Req 12.5, Req 12.7, Req 17.3

---

### M6.G3.T6: Implement Heading Demotion Helper (`src/lib/projects/demote-headings.ts`)

**Objective:** Author `demoteHeadings` in `src/lib/projects/demote-headings.ts` demoting Markdown HTML headings by one level if an `<h1>` exists, accompanied by Property 18 fast-check tests.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/demote-headings.ts` created
- ✓ Exports pure function `demoteHeadings(html: string): string`
- ✓ Checks for presence of `<h1>` tags (`/<h1[\s>]/i`); if absent, returns input unchanged (Req 13.3)
- ✓ If `<h1>` exists, replaces headings in a single pass (`/<(\/?)h([1-6])(?=[\s>])/gi`), capping level at 6 (`min(level + 1, 6)`)
- ✓ Preserves all heading attributes (including `id`), inner markup, and non-heading content unchanged
- ✓ Implements Property 18 test in `tests/projects/demote-headings.test.ts` ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 18: heading demotion guarantees no h1 and preserves content`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- Target file: `src/lib/projects/demote-headings.ts`

**Implementation Details:**

Write `src/lib/projects/demote-headings.ts` and its tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Heading Demotion Helper
 *
 * Scans rendered HTML and demotes heading levels by 1 if an h1 is present.
 * Ensures the detail page contains only one top-level h1 for the project title (Req 13.3, 13.4).
 */
export function demoteHeadings(html: string): string {
  if (typeof html !== 'string' || html.length === 0) {
    return '';
  }

  // Fast check: if no h1 exists, return original HTML unmodified
  if (!/<h1[\s>]/i.test(html)) {
    return html;
  }

  // Single-pass replacement to avoid cascading demotions
  return html.replace(/<(\/?)h([1-6])(?=[\s>])/gi, (_, slash, levelStr) => {
    const level = parseInt(levelStr, 10);
    const newLevel = Math.min(level + 1, 6);
    return `<${slash}h${newLevel}`;
  });
}
'@ | Set-Content "src\lib\projects\demote-headings.ts" -Encoding UTF8

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { demoteHeadings } from '@/lib/projects/demote-headings';
import { arbHeadingHtml } from '../fixtures/projects-arbitraries';

describe('demoteHeadings Helper (Req 13)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns original HTML unmodified when no h1 is present', () => {
      const input = '<h2 id="sec-1">Heading 2</h2>\n<p>Content</p>\n<h3>Heading 3</h3>';
      expect(demoteHeadings(input)).toBe(input);
    });

    it('demotes all heading tags by 1 level when h1 is present', () => {
      const input = '<h1 id="title">Doc Title</h1>\n<h2>Sub Title</h2>\n<p>Text</p>';
      const expected = '<h2 id="title">Doc Title</h2>\n<h3 id="sub-title">Sub Title</h3>\n<p>Text</p>';
      expect(demoteHeadings(input)).toBe(expected);
    });

    it('caps demoted levels at h6', () => {
      const input = '<h1>Title</h1>\n<h6>Level 6</h6>';
      const output = demoteHeadings(input);
      expect(output).toContain('<h2>Title</h2>');
      expect(output).toContain('<h6>Level 6</h6>');
    });
  });

  describe('Property-Based Invariants (Property 18)', () => {
    it('Feature: m6-projects-module, Property 18: heading demotion guarantees no h1 and preserves content for any HTML fragment', () => {
      fc.assert(
        fc.property(arbHeadingHtml, (html) => {
          const demoted = demoteHeadings(html);

          // 1. Output must never contain an opening h1 tag
          expect(/<h1[\s>]/i.test(demoted)).toBe(false);

          // 2. If input had no h1, output is identical
          if (!/<h1[\s>]/i.test(html)) {
            expect(demoted).toBe(html);
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\demote-headings.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/demote-headings.ts
npm run test -- tests/projects/demote-headings.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.3, Req 13.4, Req 17.2, Req 17.3

---

### M6.G3.T7: Implement Result Count Text Formatter (`src/lib/projects/format-result-count.ts`)

**Objective:** Author `formatResultCount` in `src/lib/projects/format-result-count.ts` generating deterministic live-region text, accompanied by Property 11 fast-check test.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/format-result-count.ts` created
- ✓ Exports pure function `formatResultCount(count: number): string`
- ✓ Returns `'1 project shown'` for count 1
- ✓ Returns `'{n} projects shown'` for any count $\neq 1$ (including 0)
- ✓ Implements Property 11 test in `tests/projects/format-result-count.test.ts` ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 11: result announcement text follows the count`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- Target file: `src/lib/projects/format-result-count.ts`

**Implementation Details:**

Write `src/lib/projects/format-result-count.ts` and its test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Result Announcement Formatter
 *
 * Formats visible polite live-region text reflecting matching projects count (Req 8.2).
 */
export function formatResultCount(count: number): string {
  if (count === 1) {
    return '1 project shown';
  }
  return `${count} projects shown`;
}
'@ | Set-Content "src\lib\projects\format-result-count.ts" -Encoding UTF8

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { formatResultCount } from '@/lib/projects/format-result-count';

describe('formatResultCount Formatter (Req 8.2)', () => {
  it('formats counts 0, 1, and 5 accurately', () => {
    expect(formatResultCount(0)).toBe('0 projects shown');
    expect(formatResultCount(1)).toBe('1 project shown');
    expect(formatResultCount(5)).toBe('5 projects shown');
  });

  describe('Property-Based Invariants (Property 11)', () => {
    it('Feature: m6-projects-module, Property 11: result announcement text follows the count for any non-negative integer', () => {
      fc.assert(
        fc.property(fc.integer({ min: 0, max: 1000 }), (count) => {
          const formatted = formatResultCount(count);
          if (count === 1) {
            expect(formatted).toBe('1 project shown');
          } else {
            expect(formatted).toBe(`${count} projects shown`);
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\format-result-count.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/format-result-count.ts
npm run test -- tests/projects/format-result-count.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.2, Req 17.2, Req 17.3

---

### M6.G3.T8: Implement Index and Detail Metadata Builders (`src/lib/projects/project-metadata.ts`)

**Objective:** Author pure metadata builders `buildProjectsIndexMetadata` and `buildProjectDetailMetadata` in `src/lib/projects/project-metadata.ts`.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/project-metadata.ts` created
- ✓ Exports `interface ProjectsMetadata`
- ✓ Exports `buildProjectsIndexMetadata(siteUrl: string): ProjectsMetadata`
- ✓ Sets index canonical URL and Open Graph URL using `new URL('/projects', siteUrl).href`
- ✓ Sets index description to `PROJECTS_INDEX_DESCRIPTION`
- ✓ Exports `buildProjectDetailMetadata(project: Pick<Project, 'slug' | 'title' | 'summary'>, siteUrl: string): ProjectsMetadata`
- ✓ Sets detail canonical URL using `new URL(`/projects/${encodeURIComponent(project.slug)}`, siteUrl).href`
- ✓ Sets `openGraph.type = 'article'` for detail, `'website'` for index
- ✓ Strictly omits JSON-LD structured data (Req 15.7)

**Prerequisites:**
- M6.G1 completed (`PROJECTS_TEXT` in `projects-text.ts`)
- Target file: `src/lib/projects/project-metadata.ts`

**Implementation Details:**

Write `src/lib/projects/project-metadata.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project } from '@/types/content';
import { PROJECTS_TEXT, PROJECTS_INDEX_DESCRIPTION } from '@/components/projects/projects-text';

export interface ProjectsMetadata {
  readonly title: string;
  readonly description: string;
  readonly alternates: { readonly canonical: string };
  readonly openGraph: {
    readonly title: string;
    readonly description: string;
    readonly url: string;
    readonly type: 'website' | 'article';
  };
}

/**
 * Builds metadata for the Projects Index route (/projects).
 */
export function buildProjectsIndexMetadata(siteUrl: string): ProjectsMetadata {
  const rootUrl = new URL('/projects', siteUrl).href;
  return {
    title: PROJECTS_TEXT.pageHeading,
    description: PROJECTS_INDEX_DESCRIPTION,
    alternates: {
      canonical: rootUrl,
    },
    openGraph: {
      title: PROJECTS_TEXT.pageHeading,
      description: PROJECTS_INDEX_DESCRIPTION,
      url: rootUrl,
      type: 'website',
    },
  };
}

/**
 * Builds metadata for an individual Project Detail route (/projects/[slug]).
 */
export function buildProjectDetailMetadata(
  project: Pick<Project, 'slug' | 'title' | 'summary'>,
  siteUrl: string
): ProjectsMetadata {
  const detailUrl = new URL(`/projects/${encodeURIComponent(project.slug)}`, siteUrl).href;
  return {
    title: project.title,
    description: project.summary,
    alternates: {
      canonical: detailUrl,
    },
    openGraph: {
      title: project.title,
      description: project.summary,
      url: detailUrl,
      type: 'article',
    },
  };
}
'@ | Set-Content "src\lib\projects\project-metadata.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/project-metadata.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.4, Req 15.5, Req 15.6, Req 15.7, Req 17.3

---

### M6.G3.T9: Author Property-Based Tests for Metadata & Pure Helper Invariance (Properties 8, 21)

**Objective:** Create `tests/projects/project-metadata.test.ts` and `tests/projects/purity.test.ts` validating Property 21 (metadata derivation) and Property 8 (universal input immutability).

**Acceptance Criteria:**
- ✓ File `tests/projects/project-metadata.test.ts` created
- ✓ Implements Property 21 test ($\ge 100$ runs with `fast-check`): canonical URLs contain no `?` or `#`, og.type is article for detail and website for index
- ✓ Tagged: `Feature: m6-projects-module, Property 21: metadata derives from the project and site URL`
- ✓ File `tests/projects/purity.test.ts` created
- ✓ Implements Property 8 test ($\ge 100$ runs with `fast-check`): calls all 8 pure helpers on deeply frozen inputs without mutation or throws
- ✓ Tagged: `Feature: m6-projects-module, Property 8: pure helpers do not mutate their inputs`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G3.T8 completed
- Target files: `tests/projects/project-metadata.test.ts` and `tests/projects/purity.test.ts`

**Implementation Details:**

Write `tests/projects/project-metadata.test.ts` and `tests/projects/purity.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { buildProjectsIndexMetadata, buildProjectDetailMetadata } from '@/lib/projects/project-metadata';
import { arbProject } from '../fixtures/projects-arbitraries';

describe('Project Metadata Builders (Req 15)', () => {
  describe('Property-Based Invariants (Property 21)', () => {
    it('Feature: m6-projects-module, Property 21: metadata derives from the project and site URL without query or hash', () => {
      fc.assert(
        fc.property(
          arbProject,
          fc.constant('https://example.vercel.app'),
          (project, siteUrl) => {
            // 1. Index metadata
            const indexMeta = buildProjectsIndexMetadata(siteUrl);
            expect(indexMeta.alternates.canonical).toBe('https://example.vercel.app/projects');
            expect(indexMeta.alternates.canonical.includes('?')).toBe(false);
            expect(indexMeta.alternates.canonical.includes('#')).toBe(false);
            expect(indexMeta.openGraph.type).toBe('website');

            // 2. Detail metadata
            const detailMeta = buildProjectDetailMetadata(project, siteUrl);
            expect(detailMeta.title).toBe(project.title);
            expect(detailMeta.description).toBe(project.summary);
            expect(detailMeta.alternates.canonical).toBe(
              `https://example.vercel.app/projects/${encodeURIComponent(project.slug)}`
            );
            expect(detailMeta.alternates.canonical.includes('?')).toBe(false);
            expect(detailMeta.openGraph.type).toBe('article');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\project-metadata.test.ts" -Encoding UTF8

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { parseProjectFilters, serializeProjectFilters, mergeFiltersIntoQuery } from '@/lib/projects/filter-params';
import { deriveFilterOptions } from '@/lib/projects/derive-filter-options';
import { filterProjects } from '@/lib/projects/filter-projects';
import { selectRelatedProjects } from '@/lib/projects/select-related-projects';
import { getProjectLinks } from '@/lib/projects/get-project-links';
import { toProjectCardData } from '@/lib/projects/card-data';
import { arbProjectsList, arbFilterOptions, arbProjectFilters } from '../fixtures/projects-arbitraries';

function deepFreeze<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  Object.freeze(obj);
  Object.keys(obj).forEach((key) => {
    const prop = (obj as any)[key];
    if (prop !== null && typeof prop === 'object') {
      deepFreeze(prop);
    }
  });
  return obj;
}

describe('Pure Helpers Immutability (Property 8)', () => {
  it('Feature: m6-projects-module, Property 8: pure helpers do not mutate their inputs across any frozen arguments', () => {
    fc.assert(
      fc.property(
        arbFilterOptions.chain((opts: any) =>
          fc.tuple(arbProjectsList, arbProjectFilters(opts), fc.constant(opts))
        ),
        ([projects, filters, options]: any) => {
          if (projects.length === 0) return;

          const frozenProjects = deepFreeze(JSON.parse(JSON.stringify(projects)));
          const snapshot = JSON.stringify(frozenProjects);

          // 1. deriveFilterOptions
          deriveFilterOptions(frozenProjects);
          expect(JSON.stringify(frozenProjects)).toBe(snapshot);

          // 2. filterProjects
          filterProjects(frozenProjects, filters);
          expect(JSON.stringify(frozenProjects)).toBe(snapshot);

          // 3. selectRelatedProjects
          selectRelatedProjects(frozenProjects[0], frozenProjects);
          expect(JSON.stringify(frozenProjects)).toBe(snapshot);

          // 4. toProjectCardData
          toProjectCardData(frozenProjects[0]);
          expect(JSON.stringify(frozenProjects)).toBe(snapshot);

          // 5. getProjectLinks
          getProjectLinks(frozenProjects[0]);
          expect(JSON.stringify(frozenProjects)).toBe(snapshot);

          // 6. filter-params helpers
          const frozenParams = deepFreeze(new URLSearchParams('technology=TypeScript&status=completed'));
          const frozenOpts = deepFreeze(JSON.parse(JSON.stringify(options)));
          parseProjectFilters(frozenParams, frozenOpts);
          serializeProjectFilters(filters);
          mergeFiltersIntoQuery('page=1', filters);
        }
      ),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\projects\purity.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/project-metadata.test.ts tests/projects/purity.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.8, Req 4.4, Req 5.7, Req 14.5, Req 15.3, Req 15.6, Req 17.2, Req 17.3

---

### M6.G3.T10: Checkpoint — Domain Helpers Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across all domain helpers and their comprehensive test suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all G3 test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G3.T1 through M6.G3.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/filter-projects.test.ts tests/projects/select-related-projects.test.ts tests/projects/get-project-links.test.ts tests/projects/demote-headings.test.ts tests/projects/format-result-count.test.ts tests/projects/project-metadata.test.ts tests/projects/purity.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/filter-projects.test.ts tests/projects/select-related-projects.test.ts tests/projects/get-project-links.test.ts tests/projects/demote-headings.test.ts tests/projects/format-result-count.test.ts tests/projects/project-metadata.test.ts tests/projects/purity.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\projects\filter-projects.ts"
Test-Path "src\lib\projects\select-related-projects.ts"
Test-Path "src\lib\projects\get-project-links.ts"
Test-Path "src\lib\projects\demote-headings.ts"
Test-Path "src\lib\projects\format-result-count.ts"
Test-Path "src\lib\projects\project-metadata.ts"
npm run typecheck
npm run test -- tests/projects/filter-projects.test.ts tests/projects/select-related-projects.test.ts tests/projects/get-project-links.test.ts tests/projects/demote-headings.test.ts tests/projects/format-result-count.test.ts tests/projects/project-metadata.test.ts tests/projects/purity.test.ts
```
Expected output:
- `True` for all 6 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all domain helper tests with return code 0.