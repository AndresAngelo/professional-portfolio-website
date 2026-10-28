# M5.G2: Selection Helpers and Property Tests

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the three pure, React-free content selection helpers in `src/lib/home/`: `selectFeaturedProjects`, `selectCertificationPreview`, and `selectRecentPosts`. Ensure `selectFeaturedProjects` filters projects strictly by `featured === true`, orders them by `displayOrder` ascending with deterministic `slug` ascending tie-breaking, and caps results at `PREVIEW_LIMIT` (3). Ensure `selectCertificationPreview` sorts certifications by `displayOrder` ascending with `slug` ascending tie-breaking, capped at 3. Ensure `selectRecentPosts` filters out all draft blog posts (`draft === false`), orders published posts by `publishedAt` descending with `slug` ascending tie-breaking, and caps results at 3. Guarantee that all three helpers operate on shallow copies, never mutate input arrays, contain zero framework or client-side directives, and exhibit strict mathematical idempotence. Validate all three helpers with comprehensive Vitest unit tests and fast-check property tests for Properties 1, 2, 3, and 4.

## Goal Success Criteria

- ✓ `src/lib/home/select-featured-projects.ts` exports pure function `selectFeaturedProjects(projects: readonly Project[]): Project[]`
- ✓ `src/lib/home/select-certification-preview.ts` exports pure function `selectCertificationPreview(certifications: readonly Certification[]): Certification[]`
- ✓ `src/lib/home/select-recent-posts.ts` exports pure function `selectRecentPosts(posts: readonly BlogPost[]): BlogPost[]`
- ✓ All three modules contain zero React/Next.js imports and zero `'use client'` statements
- ✓ Unit and property tests in `tests/home/select-featured-projects.test.ts` satisfy Property 1 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/home/select-certification-preview.test.ts` satisfy Property 2 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/home/select-recent-posts.test.ts` satisfy Property 3 ($\ge 100$ runs with `fast-check`)
- ✓ Purity and idempotence tests in `tests/home/selection-purity.test.ts` satisfy Property 4 on deep-frozen inputs ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goal M5.G1 completed (`home-text.ts`, `compare.ts`, test fixtures, and arbitraries available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream types imported strictly from `@/types/content`

---

## Tasks

### M5.G2.T1: Implement Featured Projects Selection Helper (`src/lib/home/select-featured-projects.ts`)

**Objective:** Author the pure function `selectFeaturedProjects` in `src/lib/home/select-featured-projects.ts` selecting up to 3 featured projects ordered by `displayOrder` then `slug`.

**Acceptance Criteria:**
- ✓ File `src/lib/home/select-featured-projects.ts` created
- ✓ Exports `selectFeaturedProjects(projects: readonly Project[]): Project[]`
- ✓ Filters input array to entries where `featured === true`
- ✓ Clones array before sorting (guarantees input immutability per Req 5.5)
- ✓ Sorts entries by `displayOrder` ascending
- ✓ Breaks ties on identical `displayOrder` using `compareStrings(a.slug, b.slug)` ascending
- ✓ Slices output array to `PREVIEW_LIMIT` (3)
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M5.G1 completed (`compareStrings` in `src/lib/home/compare.ts`, `PREVIEW_LIMIT` in `src/components/home/home-text.ts`)
- Target file: `src/lib/home/select-featured-projects.ts`

**Implementation Details:**

Write `src/lib/home/select-featured-projects.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Selection Helper: Featured Projects
 *
 * Filters, sorts, and limits projects for homepage presentation.
 * Contains no React, Next.js, or browser dependencies (Req 5.1-5.6, 16.6).
 */
import type { Project } from '@/types/content';
import { PREVIEW_LIMIT } from '@/components/home/home-text';
import { compareStrings } from './compare';

/**
 * Returns up to PREVIEW_LIMIT projects marked as featured,
 * sorted by displayOrder ascending, breaking ties by slug ascending.
 */
export function selectFeaturedProjects(projects: readonly Project[]): Project[] {
  return projects
    .filter((project) => project.featured)
    .slice() // defensive copy
    .sort((a, b) => {
      if (a.displayOrder !== b.displayOrder) {
        return a.displayOrder - b.displayOrder;
      }
      return compareStrings(a.slug, b.slug);
    })
    .slice(0, PREVIEW_LIMIT);
}
'@ | Set-Content "src\lib\home\select-featured-projects.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/select-featured-projects.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 5.5, Req 16.6

---

### M5.G2.T2: Implement Certification Preview Selection Helper (`src/lib/home/select-certification-preview.ts`)

**Objective:** Author the pure function `selectCertificationPreview` in `src/lib/home/select-certification-preview.ts` selecting up to 3 certifications ordered by `displayOrder` then `slug`.

**Acceptance Criteria:**
- ✓ File `src/lib/home/select-certification-preview.ts` created
- ✓ Exports `selectCertificationPreview(certifications: readonly Certification[]): Certification[]`
- ✓ Clones array before sorting (guarantees input immutability per Req 10.3)
- ✓ Sorts entries by `displayOrder` ascending
- ✓ Breaks ties on identical `displayOrder` using `compareStrings(a.slug, b.slug)` ascending
- ✓ Slices output array to `PREVIEW_LIMIT` (3)
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M5.G1 completed (`compareStrings`, `PREVIEW_LIMIT`)
- Target file: `src/lib/home/select-certification-preview.ts`

**Implementation Details:**

Write `src/lib/home/select-certification-preview.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Selection Helper: Certification Preview
 *
 * Sorts and limits certifications for homepage presentation.
 * Contains no React, Next.js, or browser dependencies (Req 10.1-10.3, 16.6).
 */
import type { Certification } from '@/types/content';
import { PREVIEW_LIMIT } from '@/components/home/home-text';
import { compareStrings } from './compare';

/**
 * Returns up to PREVIEW_LIMIT certifications,
 * sorted by displayOrder ascending, breaking ties by slug ascending.
 */
export function selectCertificationPreview(
  certifications: readonly Certification[]
): Certification[] {
  return certifications
    .slice() // defensive copy
    .sort((a, b) => {
      if (a.displayOrder !== b.displayOrder) {
        return a.displayOrder - b.displayOrder;
      }
      return compareStrings(a.slug, b.slug);
    })
    .slice(0, PREVIEW_LIMIT);
}
'@ | Set-Content "src\lib\home\select-certification-preview.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/select-certification-preview.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 16.6

---

### M5.G2.T3: Implement Recent Posts Selection Helper (`src/lib/home/select-recent-posts.ts`)

**Objective:** Author the pure function `selectRecentPosts` in `src/lib/home/select-recent-posts.ts` filtering drafts and selecting up to 3 published posts ordered by `publishedAt` descending then `slug`.

**Acceptance Criteria:**
- ✓ File `src/lib/home/select-recent-posts.ts` created
- ✓ Exports `selectRecentPosts(posts: readonly BlogPost[]): BlogPost[]`
- ✓ Filters out posts where `draft === true` (only `draft === false` included per Req 11.1, 11.9)
- ✓ Clones array before sorting (guarantees input immutability per Req 11.5)
- ✓ Sorts entries by `publishedAt` descending (fixed-width ISO strings sort lexicographically)
- ✓ Breaks ties on equal dates using `compareStrings(a.slug, b.slug)` ascending
- ✓ Slices output array to `PREVIEW_LIMIT` (3)
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M5.G1 completed (`compareStrings`, `PREVIEW_LIMIT`)
- Target file: `src/lib/home/select-recent-posts.ts`

**Implementation Details:**

Write `src/lib/home/select-recent-posts.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Selection Helper: Recent Blog Posts
 *
 * Excludes drafts, sorts newest first, and limits posts for homepage presentation.
 * Contains no React, Next.js, or browser dependencies (Req 11.1-11.5, 11.9, 16.6).
 */
import type { BlogPost } from '@/types/content';
import { PREVIEW_LIMIT } from '@/components/home/home-text';
import { compareStrings } from './compare';

/**
 * Returns up to PREVIEW_LIMIT published blog posts (draft: false),
 * sorted by publishedAt descending, breaking ties by slug ascending.
 */
export function selectRecentPosts(posts: readonly BlogPost[]): BlogPost[] {
  return posts
    .filter((post) => !post.draft)
    .slice() // defensive copy
    .sort((a, b) => {
      if (a.publishedAt !== b.publishedAt) {
        // Newer date strings sort higher in descending order
        return a.publishedAt > b.publishedAt ? -1 : 1;
      }
      return compareStrings(a.slug, b.slug);
    })
    .slice(0, PREVIEW_LIMIT);
}
'@ | Set-Content "src\lib\home\select-recent-posts.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/select-recent-posts.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.5, Req 11.9, Req 16.6

---

### M5.G2.T4: Audit Selection Modules for Framework Directives and Isolation

**Objective:** Inspect all three selection helper modules ensuring zero `'use client'` statements, zero React/Next.js imports, and isolated import signatures.

**Acceptance Criteria:**
- ✓ Searches `select-featured-projects.ts`, `select-certification-preview.ts`, and `select-recent-posts.ts`
- ✓ Confirms zero occurrences of `'use client'`
- ✓ Confirms zero imports from `'react'` or `'next/*'`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G2.T1 through M5.G2.T3 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$helperFiles = @(
    "src\lib\home\select-featured-projects.ts",
    "src\lib\home\select-certification-preview.ts",
    "src\lib\home\select-recent-posts.ts"
)
$violations = @()

foreach ($file in $helperFiles) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' directive in $file"
    }
    if ($content -match "\bfrom\s+['""](react|next|next\/[^'""]+)['""]") {
        $violations += "Forbidden React/Next import in $file"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 16.6

---

### M5.G2.T5: Author Concrete Unit Scenarios for Featured Projects Selection

**Objective:** Create `tests/home/select-featured-projects.test.ts` testing concrete selection cases: displayOrder ordering, slug tie-breaking, preview limit cap, and empty/unfeatured inputs.

**Acceptance Criteria:**
- ✓ File `tests/home/select-featured-projects.test.ts` created
- ✓ Verifies returns only projects where `featured === true`
- ✓ Verifies capped at 3 when 4 or more featured projects exist
- ✓ Verifies ties on `displayOrder` resolve by `slug` ascending
- ✓ Verifies returns empty array `[]` when input is empty or has zero featured projects
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G2.T1 completed
- Fixtures available at `tests/fixtures/home-data.ts`
- Target file: `tests/home/select-featured-projects.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/home/select-featured-projects.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import { selectFeaturedProjects } from '@/lib/home/select-featured-projects';
import {
  sampleProjects,
  noFeaturedProjects,
  emptyProjects,
} from '../fixtures/home-data';

describe('selectFeaturedProjects Helper (Req 5)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns at most 3 featured projects in displayOrder ascending order', () => {
      const result = selectFeaturedProjects(sampleProjects);
      expect(result.length).toBe(3);
      expect(result.every((p) => p.featured)).toBe(true);

      // Expected displayOrder sequence: 1 (alpha), 2 (beta), 2 (gamma)
      expect(result[0].slug).toBe('alpha-engine');
      expect(result[1].slug).toBe('beta-service');
      expect(result[2].slug).toBe('gamma-workflow');
    });

    it('resolves ties on displayOrder using slug in ascending code-unit order', () => {
      const tiedProjects = [
        { ...sampleProjects[0], slug: 'zebra', displayOrder: 1, featured: true },
        { ...sampleProjects[0], slug: 'alpha', displayOrder: 1, featured: true },
        { ...sampleProjects[0], slug: 'middle', displayOrder: 1, featured: true },
      ];

      const result = selectFeaturedProjects(tiedProjects);
      expect(result.map((p) => p.slug)).toEqual(['alpha', 'middle', 'zebra']);
    });

    it('returns empty array when input contains zero featured projects', () => {
      expect(selectFeaturedProjects(noFeaturedProjects)).toEqual([]);
      expect(selectFeaturedProjects(emptyProjects)).toEqual([]);
    });

    it('returns fewer than 3 projects if fewer than 3 featured projects exist', () => {
      const singleFeatured = [sampleProjects[0], sampleProjects[3]]; // only sampleProjects[0] is featured
      const result = selectFeaturedProjects(singleFeatured);
      expect(result.length).toBe(1);
      expect(result[0].slug).toBe('alpha-engine');
    });
  });
});
'@ | Set-Content "tests\home\select-featured-projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-featured-projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4

---

### M5.G2.T6: Author Property-Based Test for Featured Projects Selection (Property 1)

**Objective:** Append property-based test to `tests/home/select-featured-projects.test.ts` using `fast-check` validating Property 1 across arbitrary generated project arrays.

**Acceptance Criteria:**
- ✓ Implements Property 1 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 1: featured project selection`
- ✓ Asserts result length strictly equals $\min(3, \text{count of featured in input})$
- ✓ Asserts every item in result has `featured === true`
- ✓ Asserts `displayOrder` sequence is non-decreasing
- ✓ Asserts items with identical `displayOrder` are ordered with `slug` strictly ascending
- ✓ Asserts every result item exists in the input array
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G2.T5 completed
- Arbitraries available at `tests/fixtures/home-arbitraries.ts`
- Target file: `tests/home/select-featured-projects.test.ts`

**Implementation Details:**

Append Property 1 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 1)', () => {
    it('Feature: m5-homepage-experience, Property 1: featured project selection invariants hold for any project array', () => {
      const fc = require('fast-check');
      const { arbProject } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(fc.array(arbProject, { minLength: 0, maxLength: 20 }), (projects: any) => {
          const result = selectFeaturedProjects(projects);
          const featuredCount = projects.filter((p: any) => p.featured).length;

          // 1. Length invariant
          expect(result.length).toBe(Math.min(3, featuredCount));

          // 2. All items are featured
          expect(result.every((p: any) => p.featured)).toBe(true);

          // 3. Order invariant: non-decreasing displayOrder, slug ascending ties
          for (let i = 1; i < result.length; i++) {
            const prev = result[i - 1];
            const curr = result[i];

            if (prev.displayOrder === curr.displayOrder) {
              expect(prev.slug.localeCompare(curr.slug)).toBeLessThanOrEqual(0);
            } else {
              expect(prev.displayOrder).toBeLessThan(curr.displayOrder);
            }
          }

          // 4. Membership invariant
          for (const item of result) {
            expect(projects.some((p: any) => p.slug === item.slug)).toBe(true);
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\select-featured-projects.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\select-featured-projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-featured-projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4

---

### M5.G2.T7: Author Unit & Property-Based Tests for Certification Preview (Property 2)

**Objective:** Create `tests/home/select-certification-preview.test.ts` verifying concrete cases and fast-check Property 2 for `selectCertificationPreview`.

**Acceptance Criteria:**
- ✓ File `tests/home/select-certification-preview.test.ts` created
- ✓ Tests output is capped at 3 when 4 or more certifications are provided
- ✓ Tests sorting is `displayOrder` ascending then `slug` ascending
- ✓ Tests empty input produces `[]`
- ✓ Implements Property 2 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 2: certification preview selection`
- ✓ Asserts result length equals $\min(3, \text{input length})$
- ✓ Asserts every item is present in input with non-decreasing order
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G2.T2 completed
- Target file: `tests/home/select-certification-preview.test.ts`

**Implementation Details:**

Write `tests/home/select-certification-preview.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { selectCertificationPreview } from '@/lib/home/select-certification-preview';
import { sampleCertifications, emptyCertifications } from '../fixtures/home-data';
import { arbCertification } from '../fixtures/home-arbitraries';

describe('selectCertificationPreview Helper (Req 10)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns at most 3 certifications ordered by displayOrder then slug', () => {
      const result = selectCertificationPreview(sampleCertifications);
      expect(result.length).toBe(3);
      expect(result[0].slug).toBe('cloud-solutions-architect');
      expect(result[1].slug).toBe('ai-systems-engineer'); // displayOrder 2
      expect(result[2].slug).toBe('security-compliance-professional'); // displayOrder 2, slug 'security' > 'ai'
    });

    it('returns empty array when input is empty', () => {
      expect(selectCertificationPreview(emptyCertifications)).toEqual([]);
    });
  });

  describe('Property-Based Invariants (Property 2)', () => {
    it('Feature: m5-homepage-experience, Property 2: certification preview selection invariants hold for any input array', () => {
      fc.assert(
        fc.property(fc.array(arbCertification, { minLength: 0, maxLength: 15 }), (certs) => {
          const result = selectCertificationPreview(certs);

          // 1. Length invariant
          expect(result.length).toBe(Math.min(3, certs.length));

          // 2. Ordering invariant
          for (let i = 1; i < result.length; i++) {
            const prev = result[i - 1];
            const curr = result[i];

            if (prev.displayOrder === curr.displayOrder) {
              expect(prev.slug.localeCompare(curr.slug)).toBeLessThanOrEqual(0);
            } else {
              expect(prev.displayOrder).toBeLessThan(curr.displayOrder);
            }
          }

          // 3. Membership invariant
          for (const item of result) {
            expect(certs.some((c) => c.slug === item.slug)).toBe(true);
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\home\select-certification-preview.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-certification-preview.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2

---

### M5.G2.T8: Author Unit & Property-Based Tests for Recent Posts Selection (Property 3)

**Objective:** Create `tests/home/select-recent-posts.test.ts` verifying draft exclusion, reverse chronological sorting, and fast-check Property 3 for `selectRecentPosts`.

**Acceptance Criteria:**
- ✓ File `tests/home/select-recent-posts.test.ts` created
- ✓ Tests zero posts with `draft: true` appear in result
- ✓ Tests published posts are ordered by `publishedAt` descending (newest first)
- ✓ Tests ties on `publishedAt` resolve by `slug` ascending
- ✓ Tests capped at 3 when more than 3 published posts exist
- ✓ Implements Property 3 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 3: recent post selection excludes drafts and orders newest first`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G2.T3 completed
- Target file: `tests/home/select-recent-posts.test.ts`

**Implementation Details:**

Write `tests/home/select-recent-posts.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { selectRecentPosts } from '@/lib/home/select-recent-posts';
import {
  sampleBlogPosts,
  draftsOnlyBlogPosts,
  emptyBlogPosts,
} from '../fixtures/home-data';
import { arbBlogPost } from '../fixtures/home-arbitraries';

describe('selectRecentPosts Helper (Req 11)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns at most 3 published posts newest first and excludes drafts', () => {
      const result = selectRecentPosts(sampleBlogPosts);
      expect(result.length).toBe(3);
      expect(result.every((p) => !p.draft)).toBe(true);

      // Expected publishedAt order: 2026-04-10, 2026-03-15 (local-ai), 2026-03-15 (reflections)
      expect(result[0].slug).toBe('building-spec-driven-workflows');
      expect(result[1].slug).toBe('local-ai-model-swapping'); // tie-breaker: 'local' < 'reflections'
      expect(result[2].slug).toBe('reflections-on-hackathon');
    });

    it('returns empty array when input contains only drafts or is empty', () => {
      expect(selectRecentPosts(draftsOnlyBlogPosts)).toEqual([]);
      expect(selectRecentPosts(emptyBlogPosts)).toEqual([]);
    });
  });

  describe('Property-Based Invariants (Property 3)', () => {
    it('Feature: m5-homepage-experience, Property 3: recent post selection excludes drafts and orders newest first for any input', () => {
      fc.assert(
        fc.property(fc.array(arbBlogPost, { minLength: 0, maxLength: 20 }), (posts) => {
          const result = selectRecentPosts(posts);
          const publishedCount = posts.filter((p) => !p.draft).length;

          // 1. Length invariant
          expect(result.length).toBe(Math.min(3, publishedCount));

          // 2. Draft exclusion invariant
          expect(result.every((p) => !p.draft)).toBe(true);

          // 3. Newest-first date ordering with slug tie-breaker
          for (let i = 1; i < result.length; i++) {
            const prev = result[i - 1];
            const curr = result[i];

            if (prev.publishedAt === curr.publishedAt) {
              expect(prev.slug.localeCompare(curr.slug)).toBeLessThanOrEqual(0);
            } else {
              expect(prev.publishedAt > curr.publishedAt).toBe(true);
            }
          }

          // 4. Membership invariant
          for (const item of result) {
            expect(posts.some((p) => p.slug === item.slug)).toBe(true);
          }
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\home\select-recent-posts.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-recent-posts.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.9

---

### M5.G2.T9: Author Property-Based Test for Purity & Idempotence (Property 4)

**Objective:** Create `tests/home/selection-purity.test.ts` verifying that `selectFeaturedProjects`, `selectCertificationPreview`, and `selectRecentPosts` never mutate input arrays (tested against `Object.freeze`) and exhibit idempotence.

**Acceptance Criteria:**
- ✓ File `tests/home/selection-purity.test.ts` created
- ✓ Tests all 3 helpers against deeply frozen input objects without throwing mutation errors
- ✓ Asserts input array before call strictly matches input array after call
- ✓ Asserts `selectFeaturedProjects(selectFeaturedProjects(input))` equals `selectFeaturedProjects(input)`
- ✓ Asserts `selectRecentPosts(selectRecentPosts(input))` equals `selectRecentPosts(input)`
- ✓ Implements Property 4 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 4: selection helpers are pure and idempotent`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G2.T1, M5.G2.T2, M5.G2.T3 completed
- Target file: `tests/home/selection-purity.test.ts`

**Implementation Details:**

Write `tests/home/selection-purity.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { selectFeaturedProjects } from '@/lib/home/select-featured-projects';
import { selectCertificationPreview } from '@/lib/home/select-certification-preview';
import { selectRecentPosts } from '@/lib/home/select-recent-posts';
import { arbProject, arbCertification, arbBlogPost } from '../fixtures/home-arbitraries';

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

describe('Selection Helpers Purity & Idempotence (Property 4)', () => {
  it('Feature: m5-homepage-experience, Property 4: selection helpers are pure and idempotent across any frozen inputs', () => {
    // 1. selectFeaturedProjects purity & idempotence
    fc.assert(
      fc.property(fc.array(arbProject, { minLength: 0, maxLength: 10 }), (projects) => {
        const frozen = deepFreeze(JSON.parse(JSON.stringify(projects)));
        const snapshot = JSON.stringify(frozen);

        const firstRun = selectFeaturedProjects(frozen);
        expect(JSON.stringify(frozen)).toBe(snapshot); // no mutation

        const secondRun = selectFeaturedProjects(firstRun);
        expect(secondRun).toEqual(firstRun); // idempotence
      }),
      { numRuns: 100 }
    );

    // 2. selectCertificationPreview purity
    fc.assert(
      fc.property(fc.array(arbCertification, { minLength: 0, maxLength: 10 }), (certs) => {
        const frozen = deepFreeze(JSON.parse(JSON.stringify(certs)));
        const snapshot = JSON.stringify(frozen);

        const firstRun = selectCertificationPreview(frozen);
        expect(JSON.stringify(frozen)).toBe(snapshot);

        const secondRun = selectCertificationPreview(firstRun);
        expect(secondRun).toEqual(firstRun);
      }),
      { numRuns: 100 }
    );

    // 3. selectRecentPosts purity & idempotence
    fc.assert(
      fc.property(fc.array(arbBlogPost, { minLength: 0, maxLength: 10 }), (posts) => {
        const frozen = deepFreeze(JSON.parse(JSON.stringify(posts)));
        const snapshot = JSON.stringify(frozen);

        const firstRun = selectRecentPosts(frozen);
        expect(JSON.stringify(frozen)).toBe(snapshot);

        const secondRun = selectRecentPosts(firstRun);
        expect(secondRun).toEqual(firstRun);
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\home\selection-purity.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/selection-purity.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.5, Req 5.6, Req 10.3, Req 11.5

---

### M5.G2.T10: Checkpoint — Selection Helpers Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the selection helper modules and their corresponding unit and property test suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all selection test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G2.T1 through M5.G2.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/select-featured-projects.test.ts tests/home/select-certification-preview.test.ts tests/home/select-recent-posts.test.ts tests/home/selection-purity.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/select-featured-projects.test.ts tests/home/select-certification-preview.test.ts tests/home/select-recent-posts.test.ts tests/home/selection-purity.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 10.1, Req 11.1, Req 16.6

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\home\select-featured-projects.ts"
Test-Path "src\lib\home\select-certification-preview.ts"
Test-Path "src\lib\home\select-recent-posts.ts"
Test-Path "tests\home\select-featured-projects.test.ts"
Test-Path "tests\home\select-certification-preview.test.ts"
Test-Path "tests\home\select-recent-posts.test.ts"
Test-Path "tests\home\selection-purity.test.ts"
npm run typecheck
npm run test -- tests/home/select-featured-projects.test.ts tests/home/select-certification-preview.test.ts tests/home/select-recent-posts.test.ts tests/home/selection-purity.test.ts
```
Expected output:
- `True` for all 7 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all selection test suites with return code 0.