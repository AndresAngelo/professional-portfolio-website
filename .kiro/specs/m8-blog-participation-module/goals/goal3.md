# M8.G3: Filter Parameters, Filtering, Adjacent Posts, Result Count, and Property Tests

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure domain algorithms governing URL parameter parsing and serialization, tag-based post filtering, chronological adjacent post selection, and accessible result-count text generation. Validate all helpers through unit tests and automated Property-Based Tests (PBT) using `fast-check` to prove Properties 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, and 18, ensuring mathematical correctness, idempotence, monotonicity, parameter preservation, and input immutability across all edge cases.

## Goal Success Criteria

- ✓ `src/lib/blog/blog-filter-params.ts` exports `parseBlogFilters`, `serializeBlogFilters`, and `mergeBlogFilterParams`, correctly manipulating the `tag` parameter while preserving unrelated query parameters.
- ✓ `src/lib/blog/filter-blog-posts.ts` exports `filterBlogPosts`, matching tags case-insensitively via `tagKey`, dropping drafts, and preserving order without inspecting post bodies.
- ✓ `src/lib/blog/select-adjacent-posts.ts` exports `selectAdjacentPosts`, returning chronologically adjacent published posts (`previous`: older, `next`: newer) and null at boundaries.
- ✓ `src/lib/blog/format-result-count.ts` exports `formatResultCount`, returning `"1 post shown"` for 1 and `"{n} posts shown"` for all other counts.
- ✓ Properties 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, and 18 pass with at least 100 iterations.
- ✓ `src/lib/blog/` remains free of React, Next.js, and DOM imports (except type imports).
- ✓ `npm run typecheck`, `npm run lint`, and all tests pass with code 0.

## Prerequisites

- Goals M8.G1 and M8.G2 completed successfully.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Types, tag normalization, sorting, and fixtures available from M8.G1 and M8.G2.

---

## Tasks

### M8.G3.T1: Implement URL parameter parsing helper (`src/lib/blog/blog-filter-params.ts`)

**Objective:** Implement `parseBlogFilters` to extract and validate the `tag` query parameter against available `TagOption` values using case-insensitive normalization.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/blog-filter-params.ts`.
- ✓ Defines interface `ParamsReader { getAll(name: string): string[] }`.
- ✓ Signature: `export function parseBlogFilters(params: ParamsReader, options: ReadonlyArray<TagOption>): BlogFilters`.
- ✓ Extracts the first occurrence of parameter `tag` (`TAG_PARAM`).
- ✓ Matches candidate tag value against `options` using `tagKey`.
- ✓ Returns `{ tag: canonicalOptionSpelling }` when matched.
- ✓ Returns `{ tag: null }` if `tag` parameter is missing, empty, or not found in `options`.
- ✓ Ignores extra/repeated `tag` values and unrelated query keys.
- ✓ Zero runtime dependencies on browser DOM (`window` or `document`).

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/lib/blog/blog-types.ts` and `src/lib/blog/tag-key.ts` completed.

**Implementation Details:**

Create `src/lib/blog/blog-filter-params.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogFilters, TagOption } from '@/lib/blog/blog-types';
import { TAG_PARAM } from '@/lib/blog/blog-types';
import { tagKey } from '@/lib/blog/tag-key';

export interface ParamsReader {
  getAll(name: string): string[];
}

/**
 * Parses the active tag filter from query parameters.
 * Validates against available tag options case-insensitively, returning the
 * canonical spelling from options, or null if invalid or absent.
 */
export function parseBlogFilters(
  params: ParamsReader,
  options: ReadonlyArray<TagOption>
): BlogFilters {
  const values = params.getAll(TAG_PARAM);
  if (values.length === 0) {
    return { tag: null };
  }

  const rawValue = values[0];
  if (!rawValue) {
    return { tag: null };
  }

  const normalizedTarget = tagKey(rawValue);
  if (normalizedTarget.length === 0) {
    return { tag: null };
  }

  // Find canonical display spelling among allowed options
  const matchedOption = options.find(opt => tagKey(opt) === normalizedTarget);
  if (matchedOption) {
    return { tag: matchedOption };
  }

  return { tag: null };
}
'@ | Set-Content "src\lib\blog\blog-filter-params.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 17.4

---

### M8.G3.T2: Implement URL serialization and parameter merging (`src/lib/blog/blog-filter-params.ts`)

**Objective:** Implement `mergeBlogFilterParams` and `serializeBlogFilters` to construct safe, clean query strings while preserving unrelated parameters.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/blog-filter-params.ts`.
- ✓ Signature: `export function mergeBlogFilterParams(currentQuery: string, filters: BlogFilters): string`.
- ✓ Signature: `export function serializeBlogFilters(filters: BlogFilters): string`.
- ✓ `serializeBlogFilters(f)` delegates directly to `mergeBlogFilterParams('', f)`.
- ✓ Replaces or deletes ALL existing `tag` occurrences in `currentQuery`.
- ✓ Preserves order and values of all non-`tag` parameters (e.g. `ref=home&tag=old&page=2` becomes `ref=home&page=2&tag=new`).
- ✓ Strips leading `?` if present on input query string.
- ✓ Returns clean query string without trailing `?` or `&`.

**Prerequisites:**
- M8.G3.T1 completed.

**Implementation Details:**

Append the serialization functions to `src/lib/blog/blog-filter-params.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

/**
 * Merges a BlogFilters state into an existing query string.
 * Preserves all non-tag parameters in their original relative order.
 * Removes the tag parameter if filters.tag is null.
 */
export function mergeBlogFilterParams(currentQuery: string, filters: BlogFilters): string {
  const cleanInput = currentQuery.startsWith('?') ? currentQuery.slice(1) : currentQuery;
  const searchParams = new URLSearchParams(cleanInput);

  // Preserve unrelated parameters while deleting all existing tag keys
  const preservedEntries: Array<[string, string]> = [];
  searchParams.forEach((value, key) => {
    if (key !== TAG_PARAM) {
      preservedEntries.push([key, value]);
    }
  });

  const nextParams = new URLSearchParams();
  for (const [key, value] of preservedEntries) {
    nextParams.append(key, value);
  }

  // Append new tag parameter if active
  if (filters.tag !== null && filters.tag.trim().length > 0) {
    nextParams.set(TAG_PARAM, filters.tag);
  }

  return nextParams.toString();
}

/**
 * Serializes a BlogFilters state to a query string.
 * Returns empty string for unfiltered state, or "tag=..." when active.
 */
export function serializeBlogFilters(filters: BlogFilters): string {
  return mergeBlogFilterParams('', filters);
}
'@ | Add-Content -Path "src\lib\blog\blog-filter-params.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 4.5, Req 4.6, Req 4.7, Req 17.4

---

### M8.G3.T3: Author tests and Properties 7, 8, 9 for filter parameter helpers

**Objective:** Create `tests/blog/blog-filter-params.test.ts` covering unit edge cases and Properties 7, 8, and 9 with `fast-check`.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-filter-params.test.ts`.
- ✓ Unit tests cover: repeated `tag` values, case-insensitive canonical matching, unknown tag fallback to null, preservation of unrelated query keys, URL special characters (`&`, spaces, `=`).
- ✓ Property 7 test: `// Feature: m8-blog-participation-module, Property 7: Filter URL round trip` (100 runs).
- ✓ Property 8 test: `// Feature: m8-blog-participation-module, Property 8: Parsing never yields a tag outside the options` (100 runs).
- ✓ Property 9 test: `// Feature: m8-blog-participation-module, Property 9: Merging replaces only the tag parameter` (100 runs).

**Prerequisites:**
- M8.G3.T2 completed.
- Fixtures and arbitraries available in `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/blog-filter-params.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import {
  parseBlogFilters,
  serializeBlogFilters,
  mergeBlogFilterParams,
} from '@/lib/blog/blog-filter-params';
import { arbitraryBlogFilters } from './helpers/blog-fixtures';

describe('blog-filter-params unit tests', () => {
  const options = ['Architecture', 'Next.js', 'React & Web', 'TypeScript'];

  it('parses valid tag matching case-insensitively and returns canonical spelling', () => {
    const params = new URLSearchParams('tag=next.js');
    expect(parseBlogFilters(params, options)).toEqual({ tag: 'Next.js' });
  });

  it('returns tag: null when tag parameter is not in options', () => {
    const params = new URLSearchParams('tag=NonExistentTag');
    expect(parseBlogFilters(params, options)).toEqual({ tag: null });
  });

  it('uses first value when tag parameter is repeated', () => {
    const params = new URLSearchParams('tag=Architecture&tag=TypeScript');
    expect(parseBlogFilters(params, options)).toEqual({ tag: 'Architecture' });
  });

  it('preserves unrelated query parameters when merging', () => {
    const query = 'source=twitter&tag=old&ref=profile';
    const merged = mergeBlogFilterParams(query, { tag: 'TypeScript' });

    expect(merged).toBe('source=twitter&ref=profile&tag=TypeScript');
  });

  it('removes tag parameter entirely when setting tag to null', () => {
    const query = 'filter=active&tag=Next.js';
    const merged = mergeBlogFilterParams(query, { tag: null });

    expect(merged).toBe('filter=active');
  });

  it('safely serializes tags with special characters', () => {
    const serialized = serializeBlogFilters({ tag: 'React & Web' });
    expect(serialized).toBe('tag=React+%26+Web');

    const parsed = parseBlogFilters(new URLSearchParams(serialized), options);
    expect(parsed).toEqual({ tag: 'React & Web' });
  });
});

describe('blog-filter-params Property Tests', () => {
  const options = ['Cloud', 'AI', 'Frontend', 'Next.js', 'DevOps'];

  // Feature: m8-blog-participation-module, Property 7: Filter URL round trip
  it('Property 7: filter URL serialization and parsing round trip', () => {
    const validFiltersArbitrary = fc.record({
      tag: fc.option(fc.constantFrom(...options), { nil: null }),
    });

    fc.assert(
      fc.property(validFiltersArbitrary, filters => {
        const query = serializeBlogFilters(filters);
        if (filters.tag === null) {
          expect(query).toBe('');
        } else {
          expect(query).toContain('tag=');
        }

        const parsed = parseBlogFilters(new URLSearchParams(query), options);
        expect(parsed).toEqual(filters);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 8: Parsing never yields a tag outside the options
  it('Property 8: parseBlogFilters never returns a tag outside allowed options', () => {
    fc.assert(
      fc.property(fc.string(), rawParam => {
        const params = new URLSearchParams();
        params.set('tag', rawParam);

        const parsed = parseBlogFilters(params, options);
        if (parsed.tag !== null) {
          expect(options).toContain(parsed.tag);
        }
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 9: Merging replaces only the tag parameter
  it('Property 9: mergeBlogFilterParams preserves all non-tag parameters exactly in order', () => {
    const arbitraryEntries = fc.array(
      fc.tuple(
        fc.string({ minLength: 1, maxLength: 10 }).filter(k => k !== 'tag'),
        fc.string({ maxLength: 20 })
      ),
      { maxLength: 5 }
    );

    fc.assert(
      fc.property(arbitraryEntries, arbitraryBlogFilters, (entries, filters) => {
        const initialParams = new URLSearchParams();
        entries.forEach(([k, v]) => initialParams.append(k, v));
        initialParams.append('tag', 'existingTagValue');

        const merged = mergeBlogFilterParams(initialParams.toString(), filters);
        const resultParams = new URLSearchParams(merged);

        // Check non-tag entries
        const nonTagResultEntries: Array<[string, string]> = [];
        resultParams.forEach((v, k) => {
          if (k !== 'tag') nonTagResultEntries.push([k, v]);
        });
        expect(nonTagResultEntries).toEqual(entries);

        // Check tag entry
        if (filters.tag === null) {
          expect(resultParams.has('tag')).toBe(false);
        } else {
          expect(resultParams.get('tag')).toBe(filters.tag);
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\blog-filter-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-filter-params.test.ts
```
Expected: 6 unit tests and Properties 7, 8, 9 passing (100 runs each).

**Satisfies Requirements:** Req 4.1–4.7, Req 17.1, Req 17.2

---

### M8.G3.T4: Implement `filterBlogPosts` helper (`src/lib/blog/filter-blog-posts.ts`)

**Objective:** Implement `filterBlogPosts` to return published posts matching the active tag case-insensitively, dropping drafts, and preserving original order without mutating input.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/filter-blog-posts.ts`.
- ✓ Signature: `export function filterBlogPosts<T extends { tags: ReadonlyArray<string>; draft?: boolean }>(posts: ReadonlyArray<T>, filters: BlogFilters): T[]`.
- ✓ Filters out any post with `draft === true`.
- ✓ If `filters.tag` is `null`, returns all published posts.
- ✓ If `filters.tag` is set, matches posts having at least one tag where `tagKey(t) === tagKey(filters.tag)`.
- ✓ Preserves relative sequence (sub-sequence property).
- ✓ Never inspects titles, summaries, event fields, or markdown content.
- ✓ Does NOT mutate input array.

**Prerequisites:**
- `src/lib/blog/blog-types.ts` and `src/lib/blog/tag-key.ts` completed.

**Implementation Details:**

Create `src/lib/blog/filter-blog-posts.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogFilters } from '@/lib/blog/blog-types';
import { tagKey } from '@/lib/blog/tag-key';

/**
 * Filters a list of posts according to active BlogFilters.
 * Drops drafts, preserves original relative order, and matches tags case-insensitively.
 * Pure function: does not mutate inputs.
 */
export function filterBlogPosts<T extends { tags: ReadonlyArray<string>; draft?: boolean }>(
  posts: ReadonlyArray<T>,
  filters: BlogFilters
): T[] {
  // 1. Exclude drafts
  const published = posts.filter(p => p.draft !== true);

  // 2. Unfiltered state: return all published posts
  if (filters.tag === null) {
    return published;
  }

  const targetKey = tagKey(filters.tag);
  if (targetKey.length === 0) {
    return published;
  }

  // 3. Keep items matching tagKey
  return published.filter(post => post.tags.some(t => tagKey(t) === targetKey));
}
'@ | Set-Content "src\lib\blog\filter-blog-posts.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.5, Req 6.6, Req 17.4

---

### M8.G3.T5: Author tests and Properties 2, 3, 4, 5 for `filterBlogPosts`

**Objective:** Create `tests/blog/filter-blog-posts.test.ts` testing tag filtering against a model implementation and verifying idempotence, monotonicity, and order preservation with `fast-check`.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/filter-blog-posts.test.ts`.
- ✓ Unit tests cover: case-insensitive match, unfiltered state, draft exclusion, and zero matches.
- ✓ Property 2 test: `// Feature: m8-blog-participation-module, Property 2: Filtering returns exactly the published posts matching the tag` (100 runs).
- ✓ Property 3 test: `// Feature: m8-blog-participation-module, Property 3: Filtering is idempotent` (100 runs).
- ✓ Property 4 test: `// Feature: m8-blog-participation-module, Property 4: Filtering is monotonic` (100 runs).
- ✓ Property 5 test: `// Feature: m8-blog-participation-module, Property 5: Filtering preserves input order` (100 runs).

**Prerequisites:**
- M8.G3.T4 completed.
- Fixtures and arbitraries available in `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/filter-blog-posts.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { filterBlogPosts } from '@/lib/blog/filter-blog-posts';
import { tagKey } from '@/lib/blog/tag-key';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostDraft,
  arbitraryBlogPost,
  arbitraryBlogFilters,
} from './helpers/blog-fixtures';

describe('filterBlogPosts unit tests', () => {
  it('returns all published posts when filter is null', () => {
    const list = [mockPostPublished1, mockPostPublished2, mockPostDraft];
    const filtered = filterBlogPosts(list, { tag: null });

    expect(filtered).toEqual([mockPostPublished1, mockPostPublished2]);
  });

  it('matches tag case-insensitively and drops drafts', () => {
    const list = [mockPostPublished1, mockPostPublished2, mockPostDraft];
    // mockPostPublished1 has 'react', 'next.js', 'architecture'
    const filtered = filterBlogPosts(list, { tag: 'REACT' });

    expect(filtered).toEqual([mockPostPublished1]);
  });

  it('returns empty array when no posts match tag', () => {
    const list = [mockPostPublished1, mockPostPublished2];
    const filtered = filterBlogPosts(list, { tag: 'UnmatchedTag' });

    expect(filtered).toEqual([]);
  });
});

describe('filterBlogPosts Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 2: Filtering returns exactly the published posts matching the tag
  it('Property 2: matches exact specification model for published posts and tag keys', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), arbitraryBlogFilters, (posts, filters) => {
        const filtered = filterBlogPosts(posts, filters);

        // Reference model implementation
        const expected = posts.filter(post => {
          if (post.draft === true) return false;
          if (filters.tag === null) return true;
          const targetKey = tagKey(filters.tag);
          return post.tags.some(t => tagKey(t) === targetKey);
        });

        expect(filtered).toEqual(expected);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 3: Filtering is idempotent
  it('Property 3: filtering is idempotent', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), arbitraryBlogFilters, (posts, filters) => {
        const firstPass = filterBlogPosts(posts, filters);
        const secondPass = filterBlogPosts(firstPass, filters);

        expect(secondPass).toEqual(firstPass);
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 4: Filtering is monotonic
  it('Property 4: active filter result is a subset of unfiltered result', () => {
    fc.assert(
      fc.property(
        fc.array(arbitraryBlogPost),
        fc.string({ minLength: 1, maxLength: 20 }),
        (posts, tag) => {
          const unfiltered = filterBlogPosts(posts, { tag: null });
          const tagged = filterBlogPosts(posts, { tag });

          // Every post in tagged must be in unfiltered
          const unfilteredSlugs = new Set(unfiltered.map(p => p.slug));
          for (const post of tagged) {
            expect(unfilteredSlugs.has(post.slug)).toBe(true);
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 5: Filtering preserves input order
  it('Property 5: preserves relative input order', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), arbitraryBlogFilters, (posts, filters) => {
        const filtered = filterBlogPosts(posts, filters);
        const filteredSlugs = filtered.map(p => p.slug);

        // Check sub-sequence order
        let lastIndex = -1;
        for (const slug of filteredSlugs) {
          const nextIndex = posts.findIndex((p, idx) => idx > lastIndex && p.slug === slug);
          expect(nextIndex).toBeGreaterThan(lastIndex);
          lastIndex = nextIndex;
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\filter-blog-posts.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/filter-blog-posts.test.ts
```
Expected: 3 unit tests and Properties 2, 3, 4, 5 passing (100 runs each).

**Satisfies Requirements:** Req 6.1–6.6, Req 17.1, Req 17.2

---

### M8.G3.T6: Implement `selectAdjacentPosts` helper (`src/lib/blog/select-adjacent-posts.ts`)

**Objective:** Implement `selectAdjacentPosts` to determine chronological neighbors (`previous`: older, `next`: newer) among published posts sorted by `Blog_Sort_Order`.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/select-adjacent-posts.ts`.
- ✓ Signature: `export function selectAdjacentPosts<T extends { slug: string; publishedAt: string; draft?: boolean }>(currentSlug: string, posts: ReadonlyArray<T>): { previous: T | null; next: T | null }`.
- ✓ Drops drafts before computing adjacency.
- ✓ Sorts published posts into `Blog_Sort_Order` (newest first).
- ✓ For post at index `i`: `previous` is `i + 1` (older) or `null` if oldest.
- ✓ For post at index `i`: `next` is `i - 1` (newer) or `null` if newest.
- ✓ Returns `{ previous: null, next: null }` if `currentSlug` is not found or is a draft.
- ✓ Pure function: does not mutate inputs.

**Prerequisites:**
- `src/lib/blog/sort-blog-posts.ts` completed.

**Implementation Details:**

Create `src/lib/blog/select-adjacent-posts.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { sortBlogPosts } from '@/lib/blog/sort-blog-posts';

/**
 * Computes adjacent published posts for reading navigation.
 * Posts are ordered newest-first (Blog_Sort_Order):
 * - previous: index + 1 (the next older post in time)
 * - next: index - 1 (the next newer post in time)
 * Returns { previous: null, next: null } if currentSlug is not found among published posts.
 */
export function selectAdjacentPosts<
  T extends { slug: string; publishedAt: string; draft?: boolean }
>(
  currentSlug: string,
  posts: ReadonlyArray<T>
): { previous: T | null; next: T | null } {
  // 1. Exclude drafts
  const published = posts.filter(p => p.draft !== true);

  // 2. Sort published posts in Blog_Sort_Order (newest first)
  const ordered = sortBlogPosts(published);

  // 3. Find current post index
  const index = ordered.findIndex(p => p.slug === currentSlug);
  if (index === -1) {
    return { previous: null, next: null };
  }

  // next newer post (index - 1)
  const next = index > 0 ? (ordered[index - 1] ?? null) : null;

  // next older post (index + 1)
  const previous = index < ordered.length - 1 ? (ordered[index + 1] ?? null) : null;

  return { previous, next };
}
'@ | Set-Content "src\lib\blog\select-adjacent-posts.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.4, Req 14.10, Req 17.4

---

### M8.G3.T7: Author tests and Properties 10 and 11 for `selectAdjacentPosts`

**Objective:** Create `tests/blog/select-adjacent-posts.test.ts` covering boundary conditions, unknown slugs, draft skips, and Properties 10 and 11 with `fast-check`.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/select-adjacent-posts.test.ts`.
- ✓ Unit tests cover: newest post (`next === null`), oldest post (`previous === null`), middle post, single post (`both null`), unknown slug, draft slug.
- ✓ Property 10 test: `// Feature: m8-blog-participation-module, Property 10: Adjacent posts exclude the current post and drafts, with null boundaries` (100 runs).
- ✓ Property 11 test: `// Feature: m8-blog-participation-module, Property 11: Adjacency is symmetric` (100 runs).

**Prerequisites:**
- M8.G3.T6 completed.
- Fixtures and arbitraries available in `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/select-adjacent-posts.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { selectAdjacentPosts } from '@/lib/blog/select-adjacent-posts';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostPublished3,
  mockPostDraft,
  arbitraryBlogPost,
} from './helpers/blog-fixtures';

describe('selectAdjacentPosts unit tests', () => {
  // Ordered newest to oldest:
  // 1. mockPostPublished1 (2026-06-15)
  // 2. mockPostPublished2 (2026-04-10)
  // 3. mockPostPublished3 (2026-02-20)
  const posts = [mockPostPublished3, mockPostPublished1, mockPostPublished2, mockPostDraft];

  it('identifies newest post boundary (next is null, previous is older post)', () => {
    const { previous, next } = selectAdjacentPosts(mockPostPublished1.slug, posts);

    expect(next).toBeNull();
    expect(previous?.slug).toBe(mockPostPublished2.slug);
  });

  it('identifies middle post (both previous and next are present)', () => {
    const { previous, next } = selectAdjacentPosts(mockPostPublished2.slug, posts);

    expect(next?.slug).toBe(mockPostPublished1.slug); // newer
    expect(previous?.slug).toBe(mockPostPublished3.slug); // older
  });

  it('identifies oldest post boundary (previous is null, next is newer post)', () => {
    const { previous, next } = selectAdjacentPosts(mockPostPublished3.slug, posts);

    expect(next?.slug).toBe(mockPostPublished2.slug);
    expect(previous).toBeNull();
  });

  it('returns both null for single published post', () => {
    const { previous, next } = selectAdjacentPosts(mockPostPublished1.slug, [mockPostPublished1]);

    expect(previous).toBeNull();
    expect(next).toBeNull();
  });

  it('returns both null for unknown slug or draft slug', () => {
    expect(selectAdjacentPosts('non-existent-slug', posts)).toEqual({
      previous: null,
      next: null,
    });
    expect(selectAdjacentPosts(mockPostDraft.slug, posts)).toEqual({
      previous: null,
      next: null,
    });
  });
});

describe('selectAdjacentPosts Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 10: Adjacent posts exclude the current post and drafts, with null boundaries
  it('Property 10: excludes current post and drafts with proper null boundaries', () => {
    fc.assert(
      fc.property(
        fc.uniqueArray(arbitraryBlogPost, { selector: p => p.slug, minLength: 1 }),
        posts => {
          const published = posts.filter(p => p.draft !== true);
          if (published.length === 0) return;

          for (const current of published) {
            const { previous, next } = selectAdjacentPosts(current.slug, posts);

            if (previous !== null) {
              expect(previous.slug).not.toBe(current.slug);
              expect(previous.draft).not.toBe(true);
            }
            if (next !== null) {
              expect(next.slug).not.toBe(current.slug);
              expect(next.draft).not.toBe(true);
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 11: Adjacency is symmetric
  it('Property 11: symmetry holds: next(previous(p)) === p and previous(next(p)) === p', () => {
    fc.assert(
      fc.property(
        fc.uniqueArray(arbitraryBlogPost, { selector: p => p.slug, minLength: 2 }),
        posts => {
          const published = posts.filter(p => p.draft !== true);
          if (published.length < 2) return;

          for (const current of published) {
            const { previous, next } = selectAdjacentPosts(current.slug, published);

            if (previous !== null) {
              const prevAdj = selectAdjacentPosts(previous.slug, published);
              expect(prevAdj.next?.slug).toBe(current.slug);
            }

            if (next !== null) {
              const nextAdj = selectAdjacentPosts(next.slug, published);
              expect(nextAdj.previous?.slug).toBe(current.slug);
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\select-adjacent-posts.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/select-adjacent-posts.test.ts
```
Expected: 5 unit tests and Properties 10 and 11 passing (100 runs each).

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.4, Req 17.1, Req 17.2

---

### M8.G3.T8: Implement and test `formatResultCount` and Property 18

**Objective:** Implement `formatResultCount` in `src/lib/blog/format-result-count.ts` and verify count wording formatting (unit tests and Property 18).

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/format-result-count.ts`.
- ✓ Signature: `export function formatResultCount(count: number): string`.
- ✓ `count === 1` returns `"1 post shown"`.
- ✓ `count !== 1` returns `"{count} posts shown"` (including 0 and negative integers).
- ✓ Test file: `tests/blog/format-result-count.test.ts`.
- ✓ Property 18 test: `// Feature: m8-blog-participation-module, Property 18: Result count wording` (100 runs).

**Prerequisites:**
- Project root exists.

**Implementation Details:**

1. Create `src/lib/blog/format-result-count.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Formats visible post result counts for screen reader live region announcements.
 * Employs singular form for count = 1, plural for 0 and all other counts.
 */
export function formatResultCount(count: number): string {
  if (count === 1) {
    return '1 post shown';
  }
  return `${count} posts shown`;
}
'@ | Set-Content "src\lib\blog\format-result-count.ts" -Encoding UTF8
```

2. Create `tests/blog/format-result-count.test.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { formatResultCount } from '@/lib/blog/format-result-count';

describe('formatResultCount unit tests', () => {
  it('formats singular count correctly', () => {
    expect(formatResultCount(1)).toBe('1 post shown');
  });

  it('formats zero count in plural form', () => {
    expect(formatResultCount(0)).toBe('0 posts shown');
  });

  it('formats multi-item counts in plural form', () => {
    expect(formatResultCount(5)).toBe('5 posts shown');
    expect(formatResultCount(42)).toBe('42 posts shown');
  });
});

describe('formatResultCount Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 18: Result count wording
  it('Property 18: formatResultCount strictly satisfies singular/plural grammar invariants', () => {
    fc.assert(
      fc.property(fc.nat(10000), count => {
        const text = formatResultCount(count);
        if (count === 1) {
          expect(text).toBe('1 post shown');
        } else {
          expect(text).toBe(`${count} posts shown`);
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\format-result-count.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/format-result-count.test.ts
```
Expected: 3 unit tests and Property 18 passing (100 runs).

**Satisfies Requirements:** Req 9.2, Req 17.1, Req 17.2

---

### M8.G3.T9: Author Property 12 purity test (`tests/blog/purity.test.ts`)

**Objective:** Implement Property 12 verifying that all M8 pure helpers function properly without throwing or mutating deeply frozen input parameters.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/purity.test.ts`.
- ✓ Contains comment: `// Feature: m8-blog-participation-module, Property 12: Helpers do not mutate their inputs`.
- ✓ Deep-freezes generated inputs using recursive `Object.freeze`.
- ✓ Tests: `sortBlogPosts`, `deriveTagOptions`, `filterBlogPosts`, `selectAdjacentPosts`, `parseBlogFilters`, `serializeBlogFilters`, `mergeBlogFilterParams`, and `toBlogCardData`.
- ✓ Configured for at least 100 iterations.

**Prerequisites:**
- Tasks M8.G3.T1 through M8.G3.T8 completed.

**Implementation Details:**

Create `tests/blog/purity.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { sortBlogPosts } from '@/lib/blog/sort-blog-posts';
import { deriveTagOptions } from '@/lib/blog/derive-tag-options';
import { filterBlogPosts } from '@/lib/blog/filter-blog-posts';
import { selectAdjacentPosts } from '@/lib/blog/select-adjacent-posts';
import {
  parseBlogFilters,
  serializeBlogFilters,
  mergeBlogFilterParams,
} from '@/lib/blog/blog-filter-params';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { arbitraryBlogPost, arbitraryBlogFilters } from './helpers/blog-fixtures';

function deepFreeze<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  Object.freeze(obj);
  Object.values(obj as Record<string, unknown>).forEach(val => {
    if (typeof val === 'object' && val !== null && !Object.isFrozen(val)) {
      deepFreeze(val);
    }
  });
  return obj;
}

// Feature: m8-blog-participation-module, Property 12: Helpers do not mutate their inputs
describe('Property 12: Purity and Immutability of Blog Helpers', () => {
  it('Property 12: all pure helpers execute without throwing on deeply frozen inputs', () => {
    fc.assert(
      fc.property(
        fc.array(arbitraryBlogPost, { minLength: 1, maxLength: 5 }),
        arbitraryBlogFilters,
        fc.string(),
        (posts, filters, query) => {
          const frozenPosts = deepFreeze(JSON.parse(JSON.stringify(posts)));
          const frozenFilters = deepFreeze(JSON.parse(JSON.stringify(filters)));

          // 1. sortBlogPosts
          expect(() => sortBlogPosts(frozenPosts)).not.toThrow();

          // 2. deriveTagOptions
          const options = deriveTagOptions(frozenPosts);
          const frozenOptions = deepFreeze([...options]);

          // 3. filterBlogPosts
          expect(() => filterBlogPosts(frozenPosts, frozenFilters)).not.toThrow();

          // 4. selectAdjacentPosts
          const slug = frozenPosts[0]?.slug ?? 'non-existent';
          expect(() => selectAdjacentPosts(slug, frozenPosts)).not.toThrow();

          // 5. blog-filter-params
          const params = new URLSearchParams(query);
          expect(() => parseBlogFilters(params, frozenOptions)).not.toThrow();
          expect(() => serializeBlogFilters(frozenFilters)).not.toThrow();
          expect(() => mergeBlogFilterParams(query, frozenFilters)).not.toThrow();

          // 6. toBlogCardData
          if (frozenPosts[0]) {
            expect(() => toBlogCardData(frozenPosts[0])).not.toThrow();
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\purity.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/purity.test.ts
```
Expected: Property 12 passing (100 runs).

**Satisfies Requirements:** Req 3.3, Req 4.8, Req 5.6, Req 6.5, Req 14.10, Req 17.2

---

### M8.G3.T10: Audit purity and run all M8.G3 verification gates

**Objective:** Audit all M8 helper files for prohibited framework imports and execute linting, typechecking, and test suites.

**Acceptance Criteria:**
- ✓ Scan `src/lib/blog/` for imports from `react`, `react-dom`, `next`, `document`, or `window`.
- ✓ Grep returns zero prohibited imports.
- ✓ `npm test -- tests/blog/` runs all tests and passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.

**Prerequisites:**
- Tasks M8.G3.T1 through M8.G3.T9 completed.

**Implementation Details:**

Execute PowerShell validation script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Purity scan
$files = Get-ChildItem "src\lib\blog\*.ts"
$hasViolation = $false
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match "from ['""](react|react-dom|next)['""]") {
        Write-Host "Violation in $($f.Name): framework import found."
        $hasViolation = $true
    }
}
if ($hasViolation) { throw "Purity audit failed." }

# 2. Run vitest on blog suites
npm test -- tests/blog/

# 3. Strict typecheck
npm run typecheck

# 4. ESLint
npm run lint
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff --name-only package.json package-lock.json tsconfig.json tailwind.config.ts src/components/ui src/content
if (-not $diff) { "PASS" } else { "FAIL: Protected files touched: $diff" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.4, Req 17.6, Req 17.8, Req 17.10

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\blog\blog-filter-params.ts"
Test-Path "src\lib\blog\filter-blog-posts.ts"
Test-Path "src\lib\blog\select-adjacent-posts.ts"
Test-Path "src\lib\blog\format-result-count.ts"
Test-Path "tests\blog\purity.test.ts"
npm test -- tests/blog/
npm run typecheck
```
Expected output:
- `True` for all paths.
- All unit and property tests passing.
- `npm run typecheck` exits with return code 0.