# M8.G2: Sorting, Tag Option Derivation, Card Data, and Property Tests

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure domain algorithms that sort blog posts by date and slug, derive deduplicated tag options from published content, and extract lightweight serializable card data (`BlogCardData`). Ensure that all helper functions are deterministic, non-mutating, free of framework/DOM dependencies, and verified through both rigorous unit testing and automated Property-Based Tests (PBT) using `fast-check` to validate Property 1 (Sort order permutation and idempotence) and Property 6 (Tag options case-insensitive set equality and ordering).

## Goal Success Criteria

- ✓ `src/lib/blog/sort-blog-posts.ts` exports `sortBlogPosts`, ordering posts by `publishedAt` descending, breaking ties by `slug` ascending via M5 `compareStrings`, and never mutating inputs.
- ✓ `src/lib/blog/derive-tag-options.ts` exports `deriveTagOptions`, which filters out drafts, deduplicates tags case-insensitively using `tagKey`, preserves first observed spelling, and sorts results alphabetically.
- ✓ `src/lib/blog/to-blog-card-data.ts` exports `toBlogCardData`, producing `BlogCardData` containing exactly the 7 required card fields and copying `tags` defensively while stripping `content` and `draft`.
- ✓ Property 1 is validated with at least 100 iterations in `tests/blog/sort-blog-posts.test.ts`.
- ✓ Property 6 is validated with at least 100 iterations in `tests/blog/derive-tag-options.test.ts`.
- ✓ `npm run typecheck`, `npm run lint`, and all tests in `tests/blog/` exit with return code 0.

## Prerequisites

- Goal M8.G1 completed successfully.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream comparator available at `src/lib/home/compare.ts` (`compareStrings`).
- Fixtures and arbitraries available at `tests/blog/helpers/blog-fixtures.ts`.

---

## Tasks

### M8.G2.T1: Implement `sortBlogPosts` pure helper (`src/lib/blog/sort-blog-posts.ts`)

**Objective:** Implement the pure sorting function `sortBlogPosts` that sorts an array of objects having `slug` and `publishedAt` by publication date descending, tie-breaking by slug ascending.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/sort-blog-posts.ts`.
- ✓ Generic function signature: `export function sortBlogPosts<T extends { slug: string; publishedAt: string }>(posts: ReadonlyArray<T>): T[]`.
- ✓ Reuses `compareStrings` from `@/lib/home/compare`.
- ✓ Sorts primary order: `publishedAt` descending (newer date first).
- ✓ Sorts secondary order: `slug` ascending (alphabetical tie-breaker).
- ✓ Does NOT mutate input array (returns a new array via slice/copy).
- ✓ Does NOT filter out drafts (draft exclusion is handled downstream).
- ✓ Contains zero imports from `react`, `next`, or DOM APIs.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/lib/home/compare.ts` exists.

**Implementation Details:**

Create `src/lib/blog/sort-blog-posts.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { compareStrings } from '@/lib/home/compare';

/**
 * Sorts posts by publishedAt descending, then slug ascending as a tie-breaker.
 * Pure function: does not mutate the input array.
 */
export function sortBlogPosts<T extends { slug: string; publishedAt: string }>(
  posts: ReadonlyArray<T>
): T[] {
  return [...posts].sort((a, b) => {
    // publishedAt descending (newer first)
    const dateComparison = compareStrings(b.publishedAt, a.publishedAt);
    if (dateComparison !== 0) {
      return dateComparison;
    }
    // slug ascending (alphabetical tie-break)
    return compareStrings(a.slug, b.slug);
  });
}
'@ | Set-Content "src\lib\blog\sort-blog-posts.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 3.2, Req 3.3, Req 17.4

---

### M8.G2.T2: Author unit tests for `sortBlogPosts` (`tests/blog/sort-blog-posts.test.ts`)

**Objective:** Write comprehensive unit test cases for `sortBlogPosts` verifying empty inputs, descending date ordering, slug tie-breaking, draft preservation, and non-mutation.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/sort-blog-posts.test.ts`.
- ✓ Tests empty array returns empty array.
- ✓ Tests single element returns a new identical array.
- ✓ Tests multi-element list orders newest first.
- ✓ Tests posts with identical `publishedAt` order by `slug` alphabetically ascending.
- ✓ Tests input array is not mutated (asserts `Object.isFrozen(input)` or pre/post equality).
- ✓ Tests drafts are preserved in the sorted output (not filtered at this layer).

**Prerequisites:**
- M8.G2.T1 completed.
- Fixtures available in `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/sort-blog-posts.test.ts` with unit test suites:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { sortBlogPosts } from '@/lib/blog/sort-blog-posts';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostPublished3,
  mockPostTiedDate1,
  mockPostTiedDate2,
  mockPostDraft,
} from './helpers/blog-fixtures';

describe('sortBlogPosts unit tests', () => {
  it('returns empty array when given empty input', () => {
    expect(sortBlogPosts([])).toEqual([]);
  });

  it('handles single item without alteration', () => {
    expect(sortBlogPosts([mockPostPublished1])).toEqual([mockPostPublished1]);
  });

  it('orders posts by publishedAt descending', () => {
    // mockPostPublished1: 2026-06-15, mockPostPublished2: 2026-04-10, mockPostPublished3: 2026-02-20
    const unsorted = [mockPostPublished3, mockPostPublished1, mockPostPublished2];
    const sorted = sortBlogPosts(unsorted);

    expect(sorted.map(p => p.slug)).toEqual([
      'react-summit-2026',
      'ai-agents-hackathon',
      'singapore-dev-meetup',
    ]);
  });

  it('breaks date ties by slug ascending using compareStrings', () => {
    // Both 2026-05-01: 'tied-date-alpha' vs 'tied-date-beta'
    const unsorted = [mockPostTiedDate2, mockPostTiedDate1];
    const sorted = sortBlogPosts(unsorted);

    expect(sorted[0].slug).toBe('tied-date-alpha');
    expect(sorted[1].slug).toBe('tied-date-beta');
  });

  it('preserves draft posts without filtering them out', () => {
    const list = [mockPostPublished1, mockPostDraft];
    const sorted = sortBlogPosts(list);

    expect(sorted.some(p => p.draft === true)).toBe(true);
  });

  it('does not mutate the input array', () => {
    const input = [mockPostPublished3, mockPostPublished1];
    const originalOrder = [...input];
    Object.freeze(input);

    expect(() => sortBlogPosts(input)).not.toThrow();
    expect(input).toEqual(originalOrder);
  });
});
'@ | Set-Content "tests\blog\sort-blog-posts.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/sort-blog-posts.test.ts
```
Expected: 6 unit tests passing.

**Satisfies Requirements:** Req 3.2, Req 3.3, Req 17.1

---

### M8.G2.T3: Add Property 1 test to `sort-blog-posts.test.ts` (PBT with fast-check)

**Objective:** Implement Property 1 verifying that `sortBlogPosts` produces an exact permutation of input elements, is strictly ordered by date then slug, is idempotent, and leaves inputs unchanged.

**Acceptance Criteria:**
- ✓ Appends Property 1 test to `tests/blog/sort-blog-posts.test.ts`.
- ✓ Contains comment: `// Feature: m8-blog-participation-module, Property 1: Sorting orders by date then slug and preserves the elements`.
- ✓ Configured with `numRuns: 100` minimum.
- ✓ Verifies permutation: result has same length and every element from input is present in result.
- ✓ Verifies strict sorting invariant: for any adjacent elements `(a, b)`, either `a.publishedAt > b.publishedAt` or (`a.publishedAt === b.publishedAt` and `a.slug <= b.slug`).
- ✓ Verifies idempotence: `sortBlogPosts(sortBlogPosts(arr))` equals `sortBlogPosts(arr)`.

**Prerequisites:**
- M8.G2.T2 completed.
- Fast-check arbitraries available from `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Append Property 1 to `tests/blog/sort-blog-posts.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

import fc from 'fast-check';
import { arbitraryBlogPost } from './helpers/blog-fixtures';
import { compareStrings } from '@/lib/home/compare';

// Feature: m8-blog-participation-module, Property 1: Sorting orders by date then slug and preserves the elements
describe('sortBlogPosts Property Tests', () => {
  it('Property 1: orders by date descending then slug ascending, is a permutation, and is idempotent', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), posts => {
        const sorted = sortBlogPosts(posts);

        // 1. Permutation: same length
        expect(sorted.length).toBe(posts.length);

        // 2. Permutation: all original slugs exist
        const originalSlugs = posts.map(p => p.slug).sort();
        const sortedSlugs = sorted.map(p => p.slug).sort();
        expect(sortedSlugs).toEqual(originalSlugs);

        // 3. Strict ordering invariant
        for (let i = 0; i < sorted.length - 1; i++) {
          const current = sorted[i];
          const next = sorted[i + 1];

          const dateCmp = compareStrings(next.publishedAt, current.publishedAt);
          if (dateCmp !== 0) {
            expect(dateCmp).toBeLessThan(0); // current date >= next date
          } else {
            // Equal date: slug ascending
            expect(compareStrings(current.slug, next.slug)).toBeLessThanOrEqual(0);
          }
        }

        // 4. Idempotence: sort(sort(x)) === sort(x)
        const doubleSorted = sortBlogPosts(sorted);
        expect(doubleSorted).toEqual(sorted);
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Add-Content -Path "tests\blog\sort-blog-posts.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/sort-blog-posts.test.ts
```
Expected: All unit tests and Property 1 test passing (100 runs).

**Satisfies Requirements:** Req 3.2, Req 3.3, Req 17.2

---

### M8.G2.T4: Implement `deriveTagOptions` helper (`src/lib/blog/derive-tag-options.ts`)

**Objective:** Implement `deriveTagOptions` to extract distinct tag options from published blog posts, filtering drafts, deduplicating case-insensitively, and sorting alphabetically.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/derive-tag-options.ts`.
- ✓ Signature: `export function deriveTagOptions(posts: ReadonlyArray<{ tags: ReadonlyArray<string>; slug: string; publishedAt: string; draft?: boolean }>): TagOption[]`.
- ✓ Filters out posts where `draft === true`.
- ✓ Walks posts in `Blog_Sort_Order` (sorts internally to guarantee deterministic display spelling).
- ✓ Preserves the first observed display spelling for each unique `tagKey`.
- ✓ Discards tags that are empty or whitespace-only after `tagKey(t)`.
- ✓ Sorts resulting `TagOption` array alphabetically by `tagKey` using `compareStrings`.
- ✓ Does NOT mutate input array.

**Prerequisites:**
- `src/lib/blog/tag-key.ts` completed.
- `src/lib/blog/blog-types.ts` completed.
- `src/lib/home/compare.ts` exists.

**Implementation Details:**

Create `src/lib/blog/derive-tag-options.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { TagOption } from '@/lib/blog/blog-types';
import { tagKey } from '@/lib/blog/tag-key';
import { sortBlogPosts } from '@/lib/blog/sort-blog-posts';
import { compareStrings } from '@/lib/home/compare';

/**
 * Derives deduplicated tag options from published blog posts.
 * Drops drafts, preserves first-encountered display casing in Blog_Sort_Order,
 * and sorts resulting tags alphabetically by normalized tagKey.
 */
export function deriveTagOptions(
  posts: ReadonlyArray<{
    tags: ReadonlyArray<string>;
    slug: string;
    publishedAt: string;
    draft?: boolean;
  }>
): TagOption[] {
  // 1. Exclude drafts
  const published = posts.filter(p => p.draft !== true);

  // 2. Order posts by Blog_Sort_Order so first-seen spelling is deterministic
  const ordered = sortBlogPosts(published);

  // 3. Collect unique tags preserving first spelling
  const seenKeys = new Set<string>();
  const options: TagOption[] = [];

  for (const post of ordered) {
    for (const rawTag of post.tags) {
      const trimmed = rawTag.trim();
      const key = tagKey(trimmed);

      // Ignore empty or whitespace-only tags
      if (key.length === 0) {
        continue;
      }

      if (!seenKeys.has(key)) {
        seenKeys.add(key);
        options.push(trimmed);
      }
    }
  }

  // 4. Sort tag options alphabetically by normalized key using compareStrings
  return options.sort((a, b) => compareStrings(tagKey(a), tagKey(b)));
}
'@ | Set-Content "src\lib\blog\derive-tag-options.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 5.6

---

### M8.G2.T5: Author unit tests for `deriveTagOptions` (`tests/blog/derive-tag-options.test.ts`)

**Objective:** Write unit tests for `deriveTagOptions` covering draft exclusion, whitespace tags, first-seen casing selection, empty arrays, and alphabetical sort order.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/derive-tag-options.test.ts`.
- ✓ Tests empty array returns empty array.
- ✓ Tests post without tags contributes zero options.
- ✓ Tests draft posts do NOT contribute their tags.
- ✓ Tests whitespace-only tags are discarded.
- ✓ Tests first-seen display spelling in Blog_Sort_Order is retained across mixed-case variants.
- ✓ Tests final output list is sorted alphabetically.
- ✓ Tests input array is not mutated.

**Prerequisites:**
- M8.G2.T4 completed.

**Implementation Details:**

Create `tests/blog/derive-tag-options.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { deriveTagOptions } from '@/lib/blog/derive-tag-options';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostDraft,
  mockPostNoTags,
  mockPostWhitespaceTags,
} from './helpers/blog-fixtures';

describe('deriveTagOptions unit tests', () => {
  it('returns empty array when given empty input', () => {
    expect(deriveTagOptions([])).toEqual([]);
  });

  it('returns empty array when posts have no tags', () => {
    expect(deriveTagOptions([mockPostNoTags])).toEqual([]);
  });

  it('completely excludes tags from draft posts', () => {
    // mockPostDraft has tags: ['Standards', 'DraftTopic']
    const options = deriveTagOptions([mockPostDraft]);
    expect(options).toEqual([]);
  });

  it('ignores empty or whitespace-only tag strings', () => {
    // mockPostWhitespaceTags has: ['   ', '', 'CleanTag', '   PaddedTag   ']
    const options = deriveTagOptions([mockPostWhitespaceTags]);
    expect(options).toEqual(['CleanTag', 'PaddedTag']);
  });

  it('deduplicates tags case-insensitively and retains first-encountered spelling in sort order', () => {
    const postNewer = {
      slug: 'post-newer',
      publishedAt: '2026-06-01',
      tags: ['TypeScript', 'next.js'],
      draft: false,
    };
    const postOlder = {
      slug: 'post-older',
      publishedAt: '2026-05-01',
      tags: ['typescript', 'NEXT.JS', 'React'],
      draft: false,
    };

    const options = deriveTagOptions([postOlder, postNewer]);
    // Newer post processed first: 'TypeScript', 'next.js', then 'React' from older
    expect(options).toEqual(['next.js', 'React', 'TypeScript']);
  });

  it('sorts final tag options alphabetically by normalized key', () => {
    const posts = [mockPostPublished1, mockPostPublished2];
    const options = deriveTagOptions(posts);

    // Tags: React, Next.js, Architecture, AI, Agents, TypeScript
    expect(options).toEqual([
      'Agents',
      'AI',
      'Architecture',
      'Next.js',
      'React',
      'TypeScript',
    ]);
  });

  it('does not mutate the input array or post tags', () => {
    const input = [mockPostPublished1];
    const originalTags = [...mockPostPublished1.tags];
    Object.freeze(input);

    expect(() => deriveTagOptions(input)).not.toThrow();
    expect(mockPostPublished1.tags).toEqual(originalTags);
  });
});
'@ | Set-Content "tests\blog\derive-tag-options.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/derive-tag-options.test.ts
```
Expected: 7 unit tests passing.

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 17.1

---

### M8.G2.T6: Add Property 6 test to `derive-tag-options.test.ts` (PBT with fast-check)

**Objective:** Implement Property 6 asserting that derived tag options equal the exact case-insensitive set of tags from published posts, contain no duplicate keys, and are ordered alphabetically.

**Acceptance Criteria:**
- ✓ Appends Property 6 test to `tests/blog/derive-tag-options.test.ts`.
- ✓ Contains comment: `// Feature: m8-blog-participation-module, Property 6: Tag options equal the case-insensitive tag set of published posts`.
- ✓ Configured with `numRuns: 100` minimum.
- ✓ Verifies every tag from every non-draft post is represented in `deriveTagOptions` by key.
- ✓ Verifies no tag from any draft post is present unless also in a non-draft post.
- ✓ Verifies no two elements in the returned array have the same `tagKey`.
- ✓ Verifies strict alphabetical ordering under `compareStrings(tagKey(a), tagKey(b))`.

**Prerequisites:**
- M8.G2.T5 completed.
- Fast-check arbitraries available from `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Append Property 6 to `tests/blog/derive-tag-options.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

import fc from 'fast-check';
import { arbitraryBlogPost } from './helpers/blog-fixtures';
import { tagKey } from '@/lib/blog/tag-key';
import { compareStrings } from '@/lib/home/compare';

// Feature: m8-blog-participation-module, Property 6: Tag options equal the case-insensitive tag set of published posts
describe('deriveTagOptions Property Tests', () => {
  it('Property 6: case-insensitive set equality with published tags, no duplicate keys, and sorted', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), posts => {
        const options = deriveTagOptions(posts);

        // Compute expected published tag keys model
        const expectedKeys = new Set<string>();
        for (const post of posts) {
          if (post.draft === true) continue;
          for (const rawTag of post.tags) {
            const key = tagKey(rawTag);
            if (key.length > 0) {
              expectedKeys.add(key);
            }
          }
        }

        // 1. Equal size to unique expected keys
        expect(options.length).toBe(expectedKeys.size);

        // 2. Every option key must be in expected keys
        const optionKeys = options.map(tagKey);
        for (const key of optionKeys) {
          expect(expectedKeys.has(key)).toBe(true);
        }

        // 3. No duplicate keys
        const uniqueOptionKeys = new Set(optionKeys);
        expect(uniqueOptionKeys.size).toBe(options.length);

        // 4. Sorted alphabetically by normalized key
        for (let i = 0; i < options.length - 1; i++) {
          const cmp = compareStrings(tagKey(options[i]), tagKey(options[i + 1]));
          expect(cmp).toBeLessThanOrEqual(0);
        }
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Add-Content -Path "tests\blog\derive-tag-options.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/derive-tag-options.test.ts
```
Expected: All unit tests and Property 6 passing (100 runs).

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 17.2

---

### M8.G2.T7: Implement `toBlogCardData` helper (`src/lib/blog/to-blog-card-data.ts`)

**Objective:** Implement `toBlogCardData` to extract only the 7 presentation fields required by `BlogPostCard`, defensively copying the tags array and ensuring that `content` and `draft` are omitted.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/to-blog-card-data.ts`.
- ✓ Signature: `export function toBlogCardData(post: BlogPost): BlogCardData`.
- ✓ Extracts exactly: `slug`, `title`, `summary`, `publishedAt`, `readingTimeMinutes`, `eventType`, `tags`.
- ✓ Copies `tags` into a fresh array (`[...post.tags]`) to prevent reference leakage.
- ✓ Excludes `content`, `draft`, `updatedAt`, `eventName`, `eventDate`, `eventLocation`, and `eventUrl`.
- ✓ Return type strictly conforms to `BlogCardData` from `@/lib/blog/blog-types`.
- ✓ Does NOT mutate input.

**Prerequisites:**
- `src/lib/blog/blog-types.ts` completed.
- `@/types/content` available.

**Implementation Details:**

Create `src/lib/blog/to-blog-card-data.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogPost } from '@/types/content';
import type { BlogCardData } from '@/lib/blog/blog-types';

/**
 * Extracts lightweight, serializable card data from a full BlogPost entity.
 * Strips heavy markdown content and internal draft flags before reaching client islands.
 */
export function toBlogCardData(post: BlogPost): BlogCardData {
  return {
    slug: post.slug,
    title: post.title,
    summary: post.summary,
    publishedAt: post.publishedAt,
    readingTimeMinutes: post.readingTimeMinutes,
    eventType: post.eventType,
    tags: [...post.tags],
  };
}
'@ | Set-Content "src\lib\blog\to-blog-card-data.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 2.9, Req 8.4, Req 17.4

---

### M8.G2.T8: Author unit tests for `toBlogCardData` (`tests/blog/to-blog-card-data.test.ts`)

**Objective:** Write tests verifying `toBlogCardData` extracts exact properties, strips content/draft flags, copies tags arrays defensively, and produces clean JSON serializable output.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/to-blog-card-data.test.ts`.
- ✓ Verifies exactly the 7 keys exist on the resulting object.
- ✓ Verifies `content` property is `undefined`.
- ✓ Verifies `draft` property is `undefined`.
- ✓ Verifies modifying `post.tags` after invocation does not mutate the returned card's `tags`.
- ✓ Verifies JSON round-trip `JSON.parse(JSON.stringify(result))` matches result.

**Prerequisites:**
- M8.G2.T7 completed.
- Fixtures available from `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/to-blog-card-data.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { mockPostPublished1, mockPostDraft } from './helpers/blog-fixtures';

describe('toBlogCardData helper', () => {
  it('extracts exactly the 7 required card fields', () => {
    const card = toBlogCardData(mockPostPublished1);

    expect(Object.keys(card).sort()).toEqual([
      'eventType',
      'publishedAt',
      'readingTimeMinutes',
      'slug',
      'summary',
      'tags',
      'title',
    ]);
  });

  it('omits content, draft, and event metadata fields', () => {
    const card = toBlogCardData(mockPostPublished1) as Record<string, unknown>;

    expect(card.content).toBeUndefined();
    expect(card.draft).toBeUndefined();
    expect(card.eventName).toBeUndefined();
    expect(card.eventUrl).toBeUndefined();
  });

  it('omits draft status even when input is explicitly a draft', () => {
    const card = toBlogCardData(mockPostDraft) as Record<string, unknown>;
    expect(card.draft).toBeUndefined();
  });

  it('creates an independent copy of the tags array', () => {
    const mutablePost = {
      ...mockPostPublished1,
      tags: ['InitialTag'],
    };

    const card = toBlogCardData(mutablePost);
    mutablePost.tags.push('InjectedTag');

    expect(card.tags).toEqual(['InitialTag']);
  });

  it('produces clean JSON-serializable output', () => {
    const card = toBlogCardData(mockPostPublished1);
    const serialized = JSON.parse(JSON.stringify(card));

    expect(serialized).toEqual(card);
  });
});
'@ | Set-Content "tests\blog\to-blog-card-data.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/to-blog-card-data.test.ts
```
Expected: 5 tests passing.

**Satisfies Requirements:** Req 2.9, Req 8.4, Req 17.1

---

### M8.G2.T9: Verify purity and boundaries of G2 helpers

**Objective:** Audit `src/lib/blog/sort-blog-posts.ts`, `src/lib/blog/derive-tag-options.ts`, and `src/lib/blog/to-blog-card-data.ts` to ensure strict absence of React, Next.js, and DOM imports, and absence of `'use client'`.

**Acceptance Criteria:**
- ✓ Scan all 3 files for prohibited import specifiers: `react`, `react-dom`, `next`, `document`, `window`.
- ✓ Verify zero occurrences of `'use client'`.
- ✓ Verify types are imported strictly with `import type`.
- ✓ Script passes cleanly with output `PASS`.

**Prerequisites:**
- Tasks M8.G2.T1, M8.G2.T4, and M8.G2.T7 completed.

**Implementation Details:**

Execute PowerShell boundary audit script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$targetFiles = @(
    "src\lib\blog\sort-blog-posts.ts",
    "src\lib\blog\derive-tag-options.ts",
    "src\lib\blog\to-blog-card-data.ts"
)

$hasError = $false
foreach ($file in $targetFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "Missing: $file"
        $hasError = $true
        continue
    }
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        Write-Host "Error: $file contains 'use client'"
        $hasError = $true
    }
    if ($content -match "from ['""](react|react-dom|next)") {
        Write-Host "Error: $file imports framework modules"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$targetFiles = @(
    "src\lib\blog\sort-blog-posts.ts",
    "src\lib\blog\derive-tag-options.ts",
    "src\lib\blog\to-blog-card-data.ts"
)

$hasError = $false
foreach ($file in $targetFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "Missing: $file"
        $hasError = $true
        continue
    }
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        Write-Host "Error: $file contains 'use client'"
        $hasError = $true
    }
    if ($content -match "from ['""](react|react-dom|next)") {
        Write-Host "Error: $file imports framework modules"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

Expected output from audit: `PASS`.

**Satisfies Requirements:** Req 17.4, Req 17.7

---

### M8.G2.T10: Checkpoint — Run typecheck, lint, and all M8.G2 test suites

**Objective:** Run the full verification suite across Goal 2 implementation artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/sort-blog-posts.test.ts tests/blog/derive-tag-options.test.ts tests/blog/to-blog-card-data.test.ts` executes and passes all test suites.
- ✓ `npm run typecheck` exits with return code 0.
- ✓ `npm run lint` exits with return code 0.
- ✓ Working tree changes are strictly within `src/lib/blog/` and `tests/blog/`.

**Prerequisites:**
- Tasks M8.G2.T1 through M8.G2.T9 completed.

**Implementation Details:**

Execute full Goal 2 validation pipeline:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run all G2 test suites
npm test -- tests/blog/sort-blog-posts.test.ts tests/blog/derive-tag-options.test.ts tests/blog/to-blog-card-data.test.ts

# 2. Strict type check
npm run typecheck

# 3. Linter check
npm run lint

# 4. Check git status
git status --short
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff --name-only package.json package-lock.json tsconfig.json tailwind.config.ts src/components/ui src/content
if (-not $diff) { "PASS" } else { "FAIL: Protected files touched: $diff" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.6, Req 17.8, Req 17.10

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\blog\sort-blog-posts.ts"
Test-Path "src\lib\blog\derive-tag-options.ts"
Test-Path "src\lib\blog\to-blog-card-data.ts"
npm test -- tests/blog/sort-blog-posts.test.ts tests/blog/derive-tag-options.test.ts tests/blog/to-blog-card-data.test.ts
npm run typecheck
```
Expected output:
- `True` for all three file paths.
- All unit and property tests passing.
- `npm run typecheck` exits with code 0.