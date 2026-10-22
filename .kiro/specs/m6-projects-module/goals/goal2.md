# M6.G2: Filter Parameters, Option Derivation, and Property Tests

> **Milestone:** M6 — Projects Module  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure, framework-independent business logic modules for filter parsing, serialization, query merging, and filter options derivation in `src/lib/projects/`: `filter-params.ts` and `derive-filter-options.ts`. `parseProjectFilters` extracts and normalizes the active `technology` (reconciled against derived `FilterOptions` case-insensitively to its canonical spelling) and `status` (validated against allowed project statuses), taking the first occurrence of repeated keys, falling back to `null` on unknown values, and ignoring unrelated query keys. `mergeFiltersIntoQuery` immutably injects or deletes filter parameters in a given query string while strictly preserving unrelated parameters and their relative order. `serializeProjectFilters` formats an active filter state as a query string (returning `''` for the Unfiltered_State). `deriveFilterOptions` aggregates all distinct technologies across projects, deduplicating them via `techKey`, preserving the first-seen spelling in project order, sorting them alphabetically via M5's `compareStrings`, and ordering available statuses by canonical `STATUS_ORDER`. Validate these modules with comprehensive Vitest unit tests and fast-check property tests for Properties 1, 2, 3, and 4.

## Goal Success Criteria

- ✓ `src/lib/projects/filter-params.ts` exports `FilterOptions`, `SearchParamsReader`, `parseProjectFilters`, `serializeProjectFilters`, and `mergeFiltersIntoQuery`
- ✓ `parseProjectFilters` handles missing, repeated, padded, and invalid query parameters, returning canonical option spellings or `null`
- ✓ `mergeFiltersIntoQuery` deletes all existing occurrences of `technology` and `status`, appends updated filters (technology before status), and preserves unrelated parameters in order
- ✓ `serializeProjectFilters(filters)` returns `''` iff both filters are `null` and equals `mergeFiltersIntoQuery('', filters)`
- ✓ `src/lib/projects/derive-filter-options.ts` exports pure function `deriveFilterOptions(projects: readonly Pick<Project, 'technologies' | 'status'>[]): FilterOptions`
- ✓ `deriveFilterOptions` deduplicates technologies case-insensitively, retains first-seen spelling, sorts alphabetically via `compareStrings`, and sorts statuses per `STATUS_ORDER`
- ✓ Neither module imports React, Next.js, or DOM globals (`window`, `document`) nor mutates input arguments
- ✓ Unit and property tests in `tests/projects/filter-params.test.ts` satisfy Properties 1, 2, and 3 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/projects/derive-filter-options.test.ts` satisfy Property 4 ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goal M6.G1 completed (`tech-key.ts`, `projects-text.ts`, fixtures, and arbitraries available)
- Upstream M5 comparator available at `src/lib/home/compare.ts` (`compareStrings`)
- Target files: `src/lib/projects/filter-params.ts` and `src/lib/projects/derive-filter-options.ts`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M6.G2.T1: Implement Filter Parsing Interface & Logic (`src/lib/projects/filter-params.ts`)

**Objective:** Author the data structures and `parseProjectFilters` implementation in `src/lib/projects/filter-params.ts`.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/filter-params.ts` created
- ✓ Exports `interface FilterOptions { readonly technologies: readonly string[]; readonly statuses: readonly ProjectStatus[]; }`
- ✓ Exports `type SearchParamsReader = Pick<URLSearchParams, 'get'>`
- ✓ Exports `parseProjectFilters(params: SearchParamsReader, options: FilterOptions): ProjectFilters`
- ✓ Extracts first `technology` parameter; matches against `options.technologies` using `techKey`; returns canonical spelling or `null`
- ✓ Extracts first `status` parameter; returns matching `ProjectStatus` if in `options.statuses`, else `null`
- ✓ Pure function with zero framework or browser dependencies

**Prerequisites:**
- M6.G1 completed (`tech-key.ts` available)
- Types imported from `@/types/content`

**Implementation Details:**

Write `src/lib/projects/filter-params.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { ProjectFilters, ProjectStatus } from '@/types/content';
import { techKey } from './tech-key';

export interface FilterOptions {
  readonly technologies: readonly string[];
  readonly statuses: readonly ProjectStatus[];
}

export type SearchParamsReader = Pick<URLSearchParams, 'get'>;

/**
 * Parses raw URL search parameters into a validated, canonical ProjectFilters object.
 * Resolves technologies case-insensitively against available options and ignores invalid/unknown keys (Req 3.1-3.5, 3.8).
 */
export function parseProjectFilters(
  params: SearchParamsReader,
  options: FilterOptions
): ProjectFilters {
  const rawTech = params.get('technology');
  const rawStatus = params.get('status');

  let technology: string | null = null;
  if (rawTech !== null) {
    const targetKey = techKey(rawTech);
    if (targetKey.length > 0) {
      const match = options.technologies.find((opt) => techKey(opt) === targetKey);
      if (match) {
        technology = match; // canonical spelling
      }
    }
  }

  let status: ProjectStatus | null = null;
  if (rawStatus !== null) {
    const trimmedStatus = rawStatus.trim() as ProjectStatus;
    if (options.statuses.includes(trimmedStatus)) {
      status = trimmedStatus;
    }
  }

  return {
    technology,
    status,
  };
}
'@ | Set-Content "src\lib\projects\filter-params.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/filter-params.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.3, Req 3.4, Req 3.5, Req 3.8, Req 17.3

---

### M6.G2.T2: Implement Query Merging & Filter Serialization in `src/lib/projects/filter-params.ts`

**Objective:** Append `mergeFiltersIntoQuery` and `serializeProjectFilters` to `src/lib/projects/filter-params.ts`.

**Acceptance Criteria:**
- ✓ Exports `mergeFiltersIntoQuery(currentQuery: string, filters: ProjectFilters): string`
- ✓ Deletes all occurrences of `technology` and `status` from `currentQuery`
- ✓ Appends updated non-null filters (`technology` before `status`)
- ✓ Preserves unrelated search parameters and their relative order
- ✓ Exports `serializeProjectFilters(filters: ProjectFilters): string` implemented as `mergeFiltersIntoQuery('', filters)`
- ✓ Returns `''` in the Unfiltered_State (`technology === null && status === null`)
- ✓ Does not include a leading `?`

**Prerequisites:**
- M6.G2.T1 completed
- Target file: `src/lib/projects/filter-params.ts`

**Implementation Details:**

Append functions to `src/lib/projects/filter-params.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

/**
 * Merges updated filter parameters into an existing query string.
 * Completely removes existing technology/status keys and appends new non-null values,
 * while strictly preserving all unrelated query parameters and their relative order (Req 3.6, 6.8).
 */
export function mergeFiltersIntoQuery(
  currentQuery: string,
  filters: ProjectFilters
): string {
  // Strip leading question mark if present
  const cleanQuery = currentQuery.startsWith('?') ? currentQuery.slice(1) : currentQuery;
  const params = new URLSearchParams(cleanQuery);

  // Remove existing filter parameters (removes all occurrences if repeated)
  params.delete('technology');
  params.delete('status');

  // Append in deterministic order: technology, then status
  if (filters.technology !== null) {
    params.append('technology', filters.technology);
  }
  if (filters.status !== null) {
    params.append('status', filters.status);
  }

  return params.toString();
}

/**
 * Serializes ProjectFilters into a standard URL query string.
 * Returns empty string if both filters are null (Unfiltered_State).
 */
export function serializeProjectFilters(filters: ProjectFilters): string {
  return mergeFiltersIntoQuery('', filters);
}
'@

Add-Content -Path "src\lib\projects\filter-params.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/filter-params.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 3.7, Req 3.8, Req 6.8, Req 17.3

---

### M6.G2.T3: Implement Filter Options Derivation (`src/lib/projects/derive-filter-options.ts`)

**Objective:** Author `src/lib/projects/derive-filter-options.ts` deriving deduplicated canonical technologies and status options from project collections.

**Acceptance Criteria:**
- ✓ File `src/lib/projects/derive-filter-options.ts` created
- ✓ Exports `deriveFilterOptions(projects: readonly Pick<Project, 'technologies' | 'status'>[]): FilterOptions`
- ✓ Deduplicates technologies using `techKey`; keeps the first-seen spelling in project order
- ✓ Sorts Technology_Options alphabetically by `techKey` using `compareStrings` from `@/lib/home/compare`
- ✓ Identifies unique statuses present in projects and returns them strictly in `STATUS_ORDER` sequence (`completed`, `in-progress`, `archived`)
- ✓ Returns `{ technologies: [], statuses: [] }` when input array is empty
- ✓ Operates immutably without altering input project objects
- ✓ Pure function with zero framework dependencies

**Prerequisites:**
- M6.G1 completed (`tech-key.ts` and `STATUS_ORDER` in `projects-text.ts`)
- Upstream `compareStrings` in `src/lib/home/compare.ts`
- Target file: `src/lib/projects/derive-filter-options.ts`

**Implementation Details:**

Write `src/lib/projects/derive-filter-options.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import type { Project, ProjectStatus } from '@/types/content';
import { STATUS_ORDER } from '@/components/projects/projects-text';
import { compareStrings } from '@/lib/home/compare';
import { techKey } from './tech-key';
import type { FilterOptions } from './filter-params';

/**
 * Derives available technology and status filter options directly from project data.
 * Guarantees zero fabrication: options reflect real project evidence exclusively (Req 4.1-4.6).
 */
export function deriveFilterOptions(
  projects: readonly Pick<Project, 'technologies' | 'status'>[]
): FilterOptions {
  if (!projects || projects.length === 0) {
    return {
      technologies: [],
      statuses: [],
    };
  }

  // 1. Technologies derivation: deduplicate by techKey, keep first-seen spelling
  const techMap = new Map<string, string>(); // techKey -> firstSeenSpelling
  for (const project of projects) {
    if (!project.technologies) {
      continue;
    }
    for (const rawTech of project.technologies) {
      if (typeof rawTech !== 'string') {
        continue;
      }
      const trimmed = rawTech.trim();
      const key = techKey(trimmed);
      if (key.length === 0) {
        continue;
      }
      if (!techMap.has(key)) {
        techMap.set(key, trimmed);
      }
    }
  }

  // Sort canonical spellings by their normalized key
  const technologies = Array.from(techMap.entries())
    .sort(([keyA], [keyB]) => compareStrings(keyA, keyB))
    .map(([, spelling]) => spelling);

  // 2. Statuses derivation: collect present statuses and order by STATUS_ORDER
  const presentStatuses = new Set<ProjectStatus>();
  for (const project of projects) {
    if (project.status) {
      presentStatuses.add(project.status);
    }
  }

  const statuses = STATUS_ORDER.filter((st) => presentStatuses.has(st));

  return {
    technologies,
    statuses,
  };
}
'@ | Set-Content "src\lib\projects\derive-filter-options.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/projects/derive-filter-options.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 4.6, Req 17.3

---

### M6.G2.T4: Audit Filter Modules for Framework Isolation and Immutability

**Objective:** Audit `src/lib/projects/filter-params.ts` and `derive-filter-options.ts` ensuring zero React/Next.js imports, zero `'use client'` statements, and no DOM globals.

**Acceptance Criteria:**
- ✓ Searches both files for `'use client'`
- ✓ Searches both files for imports from `'react'`, `'next'`, or `'next/*'`
- ✓ Searches both files for `window`, `document`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M6.G2.T2 and M6.G2.T3 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @(
    "src\lib\projects\filter-params.ts",
    "src\lib\projects\derive-filter-options.ts"
)
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' found in $file"
    }
    if ($content -match "\bfrom\s+['""](react|next|next\/[^'""]+)['""]") {
        $violations += "Forbidden React/Next import found in $file"
    }
    if ($content -match "\b(window|document)\b") {
        $violations += "Forbidden DOM global found in $file"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 17.3, Req 17.7

---

### M6.G2.T5: Author Unit Scenarios for Filter Parameters (`tests/projects/filter-params.test.ts`)

**Objective:** Create `tests/projects/filter-params.test.ts` testing concrete filter parsing, serialization, and query merging scenarios.

**Acceptance Criteria:**
- ✓ File `tests/projects/filter-params.test.ts` created
- ✓ Tests `parseProjectFilters` matches technology case-insensitively and returns canonical spelling
- ✓ Tests unknown technology or status returns `null`
- ✓ Tests repeated parameters pick first occurrence
- ✓ Tests `mergeFiltersIntoQuery` preserves unrelated parameters and their order
- ✓ Tests `serializeProjectFilters` outputs `''` when both filters are null
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G2.T2 completed
- Target file: `tests/projects/filter-params.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/projects/filter-params.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import {
  parseProjectFilters,
  serializeProjectFilters,
  mergeFiltersIntoQuery,
  type FilterOptions,
} from '@/lib/projects/filter-params';

describe('Filter Parameters Helpers (Req 3)', () => {
  const options: FilterOptions = {
    technologies: ['TypeScript', 'Next.js', 'Docker'],
    statuses: ['completed', 'in-progress'],
  };

  describe('parseProjectFilters Concrete Scenarios', () => {
    it('normalizes technology case-insensitively to canonical option spelling', () => {
      const params = new URLSearchParams('technology=typescript&status=completed');
      const filters = parseProjectFilters(params, options);

      expect(filters.technology).toBe('TypeScript');
      expect(filters.status).toBe('completed');
    });

    it('falls back to null on unknown technology or unknown status', () => {
      const params = new URLSearchParams('technology=Rust&status=archived');
      const filters = parseProjectFilters(params, options);

      expect(filters.technology).toBeNull();
      expect(filters.status).toBeNull();
    });

    it('uses first occurrence when parameters are repeated', () => {
      const params = new URLSearchParams('technology=Docker&technology=typescript&status=in-progress&status=completed');
      const filters = parseProjectFilters(params, options);

      expect(filters.technology).toBe('Docker');
      expect(filters.status).toBe('in-progress');
    });

    it('returns null for both fields when query string is empty', () => {
      const params = new URLSearchParams('');
      const filters = parseProjectFilters(params, options);

      expect(filters.technology).toBeNull();
      expect(filters.status).toBeNull();
    });
  });

  describe('mergeFiltersIntoQuery & serializeProjectFilters', () => {
    it('preserves unrelated query parameters and maintains their order', () => {
      const initial = 'ref=hackernews&page=2&sort=stars';
      const merged = mergeFiltersIntoQuery(initial, { technology: 'Next.js', status: null });

      expect(merged).toBe('ref=hackernews&page=2&sort=stars&technology=Next.js');
    });

    it('replaces existing filter parameters cleanly without duplicates', () => {
      const initial = 'technology=Docker&status=completed&page=1';
      const merged = mergeFiltersIntoQuery(initial, { technology: 'TypeScript', status: 'in-progress' });

      expect(merged).toBe('page=1&technology=TypeScript&status=in-progress');
    });

    it('returns empty string when serializing Unfiltered_State', () => {
      expect(serializeProjectFilters({ technology: null, status: null })).toBe('');
    });
  });
});
'@ | Set-Content "tests\projects\filter-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/filter-params.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.3, Req 3.4, Req 3.5, Req 3.6, Req 6.8

---

### M6.G2.T6: Author Property-Based Test for Total & Canonical Parsing (Property 1)

**Objective:** Append property-based test in `tests/projects/filter-params.test.ts` validating Property 1: `parseProjectFilters` is total, canonical, and unaffected by parameter repetitions.

**Acceptance Criteria:**
- ✓ Implements Property 1 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 1: filter parsing is total and canonical`
- ✓ Asserts `technology` is either `null` or one of `options.technologies`
- ✓ Asserts `status` is either `null` or one of `options.statuses`
- ✓ Asserts first parameter takes precedence over subsequent duplicate keys
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G2.T5 completed
- Arbitraries in `tests/fixtures/projects-arbitraries.ts`
- Target file: `tests/projects/filter-params.test.ts`

**Implementation Details:**

Append Property 1 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 1)', () => {
    it('Feature: m6-projects-module, Property 1: filter parsing is total, canonical, and unaffected by parameter repetitions', () => {
      const fc = require('fast-check');
      const { arbFilterOptions, arbQueryString } = require('../fixtures/projects-arbitraries');

      fc.assert(
        fc.property(arbFilterOptions, arbQueryString, (options: any, qs: string) => {
          const params = new URLSearchParams(qs);
          const parsed = parseProjectFilters(params, options);

          // 1. Technology totality & canonicalization
          if (parsed.technology !== null) {
            expect(options.technologies).toContain(parsed.technology);
            const firstTech = params.get('technology')?.trim().toLowerCase();
            expect(parsed.technology.toLowerCase()).toBe(firstTech);
          }

          // 2. Status totality
          if (parsed.status !== null) {
            expect(options.statuses).toContain(parsed.status);
            expect(parsed.status).toBe(params.get('status')?.trim());
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\filter-params.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\filter-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/filter-params.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.2, Req 3.3, Req 3.4, Req 3.5, Req 17.2

---

### M6.G2.T7: Author Property-Based Test for Serialization Round Trip (Property 2)

**Objective:** Append property-based test in `tests/projects/filter-params.test.ts` validating Property 2: `parse(serialize(filters)) === filters` for any valid filter configuration.

**Acceptance Criteria:**
- ✓ Implements Property 2 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 2: filter serialization round trip`
- ✓ Generates valid `FilterOptions` and valid `ProjectFilters`
- ✓ Asserts `parseProjectFilters(new URLSearchParams(serializeProjectFilters(f)), options)` deep-equals `f`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G2.T6 completed
- Target file: `tests/projects/filter-params.test.ts`

**Implementation Details:**

Append Property 2 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 2)', () => {
    it('Feature: m6-projects-module, Property 2: filter serialization round trip preserves exact filter state', () => {
      const fc = require('fast-check');
      const { arbFilterOptions, arbProjectFilters } = require('../fixtures/projects-arbitraries');

      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(fc.constant(opts), arbProjectFilters(opts))
          ),
          ([options, filters]: any) => {
            const serialized = serializeProjectFilters(filters);
            const params = new URLSearchParams(serialized);
            const roundTripped = parseProjectFilters(params, options);

            expect(roundTripped).toEqual(filters);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\filter-params.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\filter-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/filter-params.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 3.7, Req 17.2

---

### M6.G2.T8: Author Property-Based Test for Query Merging (Property 3)

**Objective:** Append property-based test in `tests/projects/filter-params.test.ts` validating Property 3: query merging sets filter parameters and preserves all unrelated parameters in order.

**Acceptance Criteria:**
- ✓ Implements Property 3 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m6-projects-module, Property 3: query merging sets filter parameters and preserves the rest`
- ✓ Asserts `mergeFiltersIntoQuery(query, filters)` retains all non-filter keys and values
- ✓ Asserts non-null filter values appear exactly once
- ✓ Asserts `serializeProjectFilters` is `''` iff filters are `null`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G2.T7 completed
- Target file: `tests/projects/filter-params.test.ts`

**Implementation Details:**

Append Property 3 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 3)', () => {
    it('Feature: m6-projects-module, Property 3: query merging sets filter parameters and preserves all unrelated keys in order', () => {
      const fc = require('fast-check');
      const { arbFilterOptions, arbProjectFilters, arbQueryString } = require('../fixtures/projects-arbitraries');

      fc.assert(
        fc.property(
          arbFilterOptions.chain((opts: any) =>
            fc.tuple(fc.constant(opts), arbProjectFilters(opts), arbQueryString)
          ),
          ([, filters, query]: any) => {
            const merged = mergeFiltersIntoQuery(query, filters);
            const initialParams = new URLSearchParams(query);
            const mergedParams = new URLSearchParams(merged);

            // 1. Unrelated keys preserved in order and values
            const initialUnrelated = Array.from(initialParams.entries()).filter(
              ([k]) => k !== 'technology' && k !== 'status'
            );
            const mergedUnrelated = Array.from(mergedParams.entries()).filter(
              ([k]) => k !== 'technology' && k !== 'status'
            );
            expect(mergedUnrelated).toEqual(initialUnrelated);

            // 2. Exactly one technology param iff filters.technology is non-null
            const techValues = mergedParams.getAll('technology');
            if (filters.technology !== null) {
              expect(techValues).toEqual([filters.technology]);
            } else {
              expect(techValues).toHaveLength(0);
            }

            // 3. Exactly one status param iff filters.status is non-null
            const statusValues = mergedParams.getAll('status');
            if (filters.status !== null) {
              expect(statusValues).toEqual([filters.status]);
            } else {
              expect(statusValues).toHaveLength(0);
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\projects\filter-params.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\projects\filter-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/filter-params.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 3.8, Req 6.8, Req 17.2

---

### M6.G2.T9: Author Unit & Property-Based Tests for Options Derivation (Property 4)

**Objective:** Create `tests/projects/derive-filter-options.test.ts` verifying concrete cases and fast-check Property 4 for `deriveFilterOptions`.

**Acceptance Criteria:**
- ✓ File `tests/projects/derive-filter-options.test.ts` created
- ✓ Tests empty input produces `{ technologies: [], statuses: [] }`
- ✓ Tests deduplication preserves first-seen spelling (`['TypeScript', 'typescript']` $\rightarrow$ `'TypeScript'`)
- ✓ Tests statuses sequence follows `STATUS_ORDER`
- ✓ Implements Property 4 test ($\ge 100$ runs with `fast-check`): Technology_Options match input technologies under `techKey` with zero duplicate keys and alphabetical order; Statuses match present statuses in `STATUS_ORDER`
- ✓ Tagged: `Feature: m6-projects-module, Property 4: filter options reflect the data exactly`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M6.G2.T3 completed
- Target file: `tests/projects/derive-filter-options.test.ts`

**Implementation Details:**

Write `tests/projects/derive-filter-options.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { deriveFilterOptions } from '@/lib/projects/derive-filter-options';
import { sampleProjectsList, singleStatusProjects } from '../fixtures/projects-data';
import { arbProject } from '../fixtures/projects-arbitraries';
import { techKey } from '@/lib/projects/tech-key';
import { STATUS_ORDER } from '@/components/projects/projects-text';

describe('deriveFilterOptions Helper (Req 4)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns empty options when projects array is empty', () => {
      expect(deriveFilterOptions([])).toEqual({
        technologies: [],
        statuses: [],
      });
    });

    it('deduplicates technologies by techKey, keeps first-seen spelling, and sorts alphabetically', () => {
      const mockProjects = [
        { technologies: ['React', 'TypeScript'], status: 'completed' as const },
        { technologies: ['typescript', 'Docker'], status: 'in-progress' as const },
        { technologies: ['REACT', 'Next.js'], status: 'archived' as const },
      ];

      const options = deriveFilterOptions(mockProjects);

      // Sorted by key: docker, next.js, react, typescript
      expect(options.technologies).toEqual(['Docker', 'Next.js', 'React', 'TypeScript']);
      expect(options.statuses).toEqual(['completed', 'in-progress', 'archived']);
    });

    it('returns only present statuses in canonical STATUS_ORDER sequence', () => {
      const options = deriveFilterOptions(singleStatusProjects);
      expect(options.statuses).toEqual(['completed']);
    });
  });

  describe('Property-Based Invariants (Property 4)', () => {
    it('Feature: m6-projects-module, Property 4: filter options reflect the data exactly with zero duplicate keys and canonical order', () => {
      fc.assert(
        fc.property(fc.array(arbProject, { minLength: 0, maxLength: 12 }), (projects) => {
          const options = deriveFilterOptions(projects);

          // 1. Technologies set equality under techKey
          const inputTechKeys = new Set<string>();
          for (const p of projects) {
            for (const t of p.technologies || []) {
              const k = techKey(t);
              if (k.length > 0) {
                inputTechKeys.add(k);
              }
            }
          }
          const outputTechKeys = new Set(options.technologies.map((t) => techKey(t)));
          expect(outputTechKeys).toEqual(inputTechKeys);

          // 2. Zero duplicate keys in technologies
          expect(options.technologies.length).toBe(outputTechKeys.size);

          // 3. Technologies alphabetical sorting by key
          for (let i = 1; i < options.technologies.length; i++) {
            const prev = techKey(options.technologies[i - 1]);
            const curr = techKey(options.technologies[i]);
            expect(prev < curr).toBe(true);
          }

          // 4. Statuses order invariant
          const presentStatuses = new Set(projects.map((p) => p.status));
          const expectedStatuses = STATUS_ORDER.filter((s) => presentStatuses.has(s));
          expect(options.statuses).toEqual(expectedStatuses);
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\projects\derive-filter-options.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/projects/derive-filter-options.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 4.6, Req 17.2

---

### M6.G2.T10: Checkpoint — Filter Parameters & Options Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across filter parameter and option modules.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all filter-params and derive-filter-options test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M6.G2.T1 through M6.G2.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/projects/filter-params.test.ts tests/projects/derive-filter-options.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/projects/filter-params.test.ts tests/projects/derive-filter-options.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\projects\filter-params.ts"
Test-Path "src\lib\projects\derive-filter-options.ts"
Test-Path "tests\projects\filter-params.test.ts"
Test-Path "tests\projects\derive-filter-options.test.ts"
npm run typecheck
npm run test -- tests/projects/filter-params.test.ts tests/projects/derive-filter-options.test.ts
```
Expected output:
- `True` for all 4 path existence checks
- `npm run typecheck` exits with return code 0
- Vitest executes all filter parameter and option tests with return code 0.