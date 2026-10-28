# M8.G5: BlogFilterBar, BlogExplorer, BlogIndex, and the Index Route

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the interactive blog browsing experience by delivering the tag filter bar (`BlogFilterBar`), the single client island (`BlogExplorer`), the top-level index container (`BlogIndex`), and the static Server Component index route (`src/app/blog/page.tsx`). Wire the `tag` URL search parameter to dynamic filtering using `router.replace({ scroll: false })` without client state duplication, guarantee pre-rendered static HTML via a `Suspense` boundary wrapping the full unfiltered fallback, manage keyboard focus restoration after clearing filters, provide live region feedback (`formatResultCount`), and verify complete index accessibility and routing behaviors.

## Goal Success Criteria

- ✓ `tests/blog/helpers/navigation-mock.ts` provides a store-backed `next/navigation` mock (`useRouter`, `useSearchParams`) that drives synchronous React re-renders upon URL mutation.
- ✓ `src/components/blog/blog-filter-bar.tsx` renders a `role="group"` labelled "Filter by tag" with `FilterChip` buttons exposing `aria-pressed`, returning `null` when no tag options exist, and rendering "Clear filters" only while a filter is active.
- ✓ `src/components/blog/blog-explorer.tsx` is the sole `'use client'` component in `src/components/blog/` and the only caller of `useSearchParams`; it derives filters directly from the URL, handles chip toggles, updates the live region (`formatResultCount`), and returns focus to the first chip after clearing.
- ✓ `src/components/blog/blog-index.tsx` renders a single `h1` "Blog", encloses `BlogExplorer` in `Suspense` with `<BlogPostList posts={posts} />` as the fallback, and displays `EmptyState` when zero posts exist.
- ✓ `src/app/blog/page.tsx` is a static server component exporting `metadata` from `buildBlogIndexMetadata` and passing serializable `BlogCardData` and `TagOption[]` without post markdown bodies.
- ✓ Automated axe-core tests verify zero accessibility violations on the index page across default, filtered, and empty states.
- ✓ All unit and integration test suites pass with code 0.

## Prerequisites

- Goals M8.G1 through M8.G4 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- M2 loaders: `getBlogPosts`, `getSiteConfig`.
- M3 UI primitives: `FilterChip`, `Button`, `EmptyState`.
- Helpers: `parseBlogFilters`, `mergeBlogFilterParams`, `filterBlogPosts`, `formatResultCount`, `deriveTagOptions`, `toBlogCardData`, `buildBlogIndexMetadata`.

---

## Tasks

### M8.G5.T1: Create store-backed `next/navigation` test mock (`tests/blog/helpers/navigation-mock.ts`)

**Objective:** Implement a reactive, store-backed mock of `next/navigation` in `tests/blog/helpers/navigation-mock.ts` supporting `useRouter`, `useSearchParams`, and state synchronization for Vitest and React Testing Library.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/helpers/navigation-mock.ts`.
- ✓ Implements module store holding the current query string.
- ✓ `useSearchParams()` reads the store via `useSyncExternalStore` so client components re-render upon update.
- ✓ `useRouter().replace(url, options)` records call arguments, updates internal query store, and notifies listeners.
- ✓ Exports `setMockSearchParams(query: string): void`.
- ✓ Exports `resetNavigationMock(): void`.
- ✓ Exports `getReplaceCalls(): Array<{ url: string; options?: { scroll?: boolean } }>`.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `tests/blog/helpers/navigation-mock.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { useSyncExternalStore } from 'react';

let currentQuery = '';
const listeners = new Set<() => void>();
const replaceCalls: Array<{ url: string; options?: { scroll?: boolean } }> = [];

function emitChange() {
  for (const listener of listeners) {
    listener();
  }
}

export function setMockSearchParams(query: string) {
  currentQuery = query.startsWith('?') ? query.slice(1) : query;
  emitChange();
}

export function resetNavigationMock() {
  currentQuery = '';
  replaceCalls.length = 0;
  listeners.clear();
}

export function getReplaceCalls() {
  return [...replaceCalls];
}

export function useSearchParams(): URLSearchParams {
  const query = useSyncExternalStore(
    subscribe => {
      listeners.add(subscribe);
      return () => listeners.delete(subscribe);
    },
    () => currentQuery,
    () => currentQuery
  );

  return new URLSearchParams(query);
}

export function useRouter() {
  return {
    replace: (url: string, options?: { scroll?: boolean }) => {
      replaceCalls.push({ url, options });
      const queryIndex = url.indexOf('?');
      currentQuery = queryIndex !== -1 ? url.slice(queryIndex + 1) : '';
      emitChange();
    },
    push: (url: string, options?: { scroll?: boolean }) => {
      replaceCalls.push({ url, options });
      const queryIndex = url.indexOf('?');
      currentQuery = queryIndex !== -1 ? url.slice(queryIndex + 1) : '';
      emitChange();
    },
  };
}
'@ | Set-Content "tests\blog\helpers\navigation-mock.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 7.6, Req 8.3, Req 17.1

---

### M8.G5.T2: Implement `BlogFilterBar` component (`src/components/blog/blog-filter-bar.tsx`)

**Objective:** Implement `BlogFilterBar` rendering a tagged accessibility group (`role="group" aria-label="Filter by tag"`), M3 `FilterChip` buttons with `aria-pressed`, and a conditional "Clear filters" button.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-filter-bar.tsx`.
- ✓ Props interface:
  ```ts
  export interface BlogFilterBarProps {
    tagOptions: ReadonlyArray<TagOption>;
    activeTag: string | null;
    onSelectTag: (tag: string | null) => void;
    onClear: () => void;
  }
  ```
- ✓ Returns `null` if `tagOptions` is empty.
- ✓ Renders a container with `role="group"` and `aria-label="Filter by tag"`.
- ✓ Renders each tag option using M3 `FilterChip` (or accessible button) with `aria-pressed={isActive}`.
- ✓ Shows "Clear filters" `Button` only while `activeTag !== null`.
- ✓ Chips wrap cleanly on mobile screens (`flex flex-wrap gap-2`).
- ✓ Zero `'use client'` directive (operates as pure presentational child).

**Prerequisites:**
- M3 `FilterChip.tsx` (or `Button.tsx`) available.
- `src/lib/blog/blog-types.ts` (`TagOption`) available.

**Implementation Details:**

Create `src/components/blog/blog-filter-bar.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import React from 'react';
import type { TagOption } from '@/lib/blog/blog-types';
import { tagKey } from '@/lib/blog/tag-key';
import { Button } from '@/components/ui/Button';

export interface BlogFilterBarProps {
  tagOptions: ReadonlyArray<TagOption>;
  activeTag: string | null;
  onSelectTag: (tag: string | null) => void;
  onClear: () => void;
}

export const BlogFilterBar = React.forwardRef<HTMLDivElement, BlogFilterBarProps>(
  function BlogFilterBar({ tagOptions, activeTag, onSelectTag, onClear }, ref) {
    if (tagOptions.length === 0) {
      return null;
    }

    const activeKey = activeTag ? tagKey(activeTag) : null;

    return (
      <div
        ref={ref}
        role="group"
        aria-label="Filter by tag"
        className="flex flex-wrap items-center gap-2 pt-2 pb-4"
      >
        {tagOptions.map(option => {
          const isSelected = activeKey === tagKey(option);

          return (
            <button
              key={option}
              type="button"
              aria-pressed={isSelected}
              onClick={() => onSelectTag(isSelected ? null : option)}
              className={`inline-flex items-center px-3 py-1.5 rounded-sm text-caption font-medium transition-colors duration-fast focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring ${
                isSelected
                  ? 'bg-brand-primary text-page font-semibold'
                  : 'bg-surface text-text-secondary hover:bg-border-default'
              }`}
            >
              {option}
            </button>
          );
        })}

        {activeTag !== null && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClear}
            className="text-brand-primary hover:underline ml-2"
          >
            Clear filters
          </Button>
        )}
      </div>
    );
  }
);
'@ | Set-Content "src\components\blog\blog-filter-bar.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 5.5, Req 7.1, Req 7.2, Req 7.3, Req 7.7, Req 7.9, Req 7.10, Req 16.4

---

### M8.G5.T3: Implement `BlogExplorer` client island core (`src/components/blog/blog-explorer.tsx`)

**Objective:** Implement `BlogExplorer` as the single `'use client'` component reading URL parameters via `useSearchParams`, computing filtered posts, and replacing URL state with `scroll: false`.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-explorer.tsx`.
- ✓ File starts with `'use client';`.
- ✓ Sole caller of `useSearchParams` and `useRouter` from `'next/navigation'`.
- ✓ Props interface:
  ```ts
  export interface BlogExplorerProps {
    posts: BlogCardData[];
    tagOptions: TagOption[];
  }
  ```
- ✓ Derives active filters directly from `useSearchParams()` on every render via `parseBlogFilters`.
- ✓ Filters posts via `filterBlogPosts(posts, filters)`.
- ✓ Clicking a chip calls `router.replace(url, { scroll: false })` using `mergeBlogFilterParams`.
- ✓ Props type strictly omits `content` and `draft`.

**Prerequisites:**
- Tasks M8.G5.T2 completed.
- `src/lib/blog/blog-filter-params.ts` and `src/lib/blog/filter-blog-posts.ts` completed.

**Implementation Details:**

Create `src/components/blog/blog-explorer.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
'use client';

import React, { useRef, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import type { BlogCardData, TagOption } from '@/lib/blog/blog-types';
import { BLOG_PATH } from '@/lib/blog/blog-types';
import { parseBlogFilters, mergeBlogFilterParams } from '@/lib/blog/blog-filter-params';
import { filterBlogPosts } from '@/lib/blog/filter-blog-posts';
import { formatResultCount } from '@/lib/blog/format-result-count';
import { BlogFilterBar } from '@/components/blog/blog-filter-bar';
import { BlogPostList } from '@/components/blog/blog-post-list';
import { EmptyState } from '@/components/ui/EmptyState';
import { Button } from '@/components/ui/Button';

export interface BlogExplorerProps {
  posts: BlogCardData[];
  tagOptions: TagOption[];
}

export function BlogExplorer({ posts, tagOptions }: BlogExplorerProps) {
  const searchParams = useSearchParams();
  const router = useRouter();

  const barRef = useRef<HTMLDivElement>(null);
  const shouldFocusFirstChipRef = useRef<boolean>(false);

  // Derive active filters from URL state
  const filters = parseBlogFilters(searchParams, tagOptions);
  const visiblePosts = filterBlogPosts(posts, filters);

  function handleSetTag(tag: string | null) {
    const nextQuery = mergeBlogFilterParams(searchParams.toString(), { tag });
    const nextUrl = nextQuery ? `${BLOG_PATH}?${nextQuery}` : BLOG_PATH;
    router.replace(nextUrl, { scroll: false });
  }

  function handleClear() {
    shouldFocusFirstChipRef.current = true;
    handleSetTag(null);
  }

  // Restore keyboard focus to first chip after clearing
  useEffect(() => {
    if (shouldFocusFirstChipRef.current && filters.tag === null) {
      shouldFocusFirstChipRef.current = false;
      const firstChip = barRef.current?.querySelector<HTMLButtonElement>('button[aria-pressed]');
      firstChip?.focus();
    }
  }, [filters.tag]);

  return (
    <div className="space-y-6">
      <BlogFilterBar
        ref={barRef}
        tagOptions={tagOptions}
        activeTag={filters.tag}
        onSelectTag={handleSetTag}
        onClear={handleClear}
      />

      <p aria-live="polite" className="text-small text-text-secondary">
        {formatResultCount(visiblePosts.length)}
      </p>

      {visiblePosts.length === 0 ? (
        <EmptyState
          message="No posts match the selected tag."
          action={
            <Button variant="secondary" onClick={handleClear}>
              Clear filters
            </Button>
          }
        />
      ) : (
        <BlogPostList posts={visiblePosts} />
      )}
    </div>
  );
}
'@ | Set-Content "src\components\blog\blog-explorer.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 7.4, Req 7.5, Req 7.6, Req 7.8, Req 8.3, Req 8.4, Req 9.1, Req 9.2, Req 9.3, Req 9.4, Req 9.5

---

### M8.G5.T4: Implement `BlogIndex` server container (`src/components/blog/blog-index.tsx`)

**Objective:** Implement `BlogIndex` rendering the single `h1` "Blog", wrapping `BlogExplorer` inside a `Suspense` boundary with static fallback, and displaying an empty state when zero posts exist.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-index.tsx`.
- ✓ Props interface:
  ```ts
  export interface BlogIndexProps {
    posts: BlogCardData[];
    tagOptions: TagOption[];
  }
  ```
- ✓ Renders a single `h1` with the exact text "Blog" (`text-heading-1`).
- ✓ If `posts.length === 0`, renders `EmptyState` ("Posts are being prepared.") and omits `Suspense` and `BlogExplorer`.
- ✓ If `posts.length > 0`, renders `BlogExplorer` inside `<Suspense fallback={<BlogPostList posts={posts} />}>`.
- ✓ The static prerendered HTML contains the complete post list from the fallback.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- Tasks M8.G5.T3 and M8.G4.T3 completed.
- M3 `EmptyState.tsx` available.

**Implementation Details:**

Create `src/components/blog/blog-index.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import React, { Suspense } from 'react';
import type { BlogCardData, TagOption } from '@/lib/blog/blog-types';
import { BlogExplorer } from '@/components/blog/blog-explorer';
import { BlogPostList } from '@/components/blog/blog-post-list';
import { EmptyState } from '@/components/ui/EmptyState';

export interface BlogIndexProps {
  posts: BlogCardData[];
  tagOptions: TagOption[];
}

export function BlogIndex({ posts, tagOptions }: BlogIndexProps) {
  if (posts.length === 0) {
    return (
      <div className="space-y-8">
        <h1 className="text-heading-1 font-bold text-text-primary">Blog</h1>
        <EmptyState message="Posts are being prepared." />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-heading-1 font-bold text-text-primary">Blog</h1>

      <Suspense fallback={<BlogPostList posts={posts} />}>
        <BlogExplorer posts={posts} tagOptions={tagOptions} />
      </Suspense>
    </div>
  );
}
'@ | Set-Content "src\components\blog\blog-index.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 1.7, Req 8.1, Req 8.2, Req 8.5

---

### M8.G5.T5: Implement static index route (`src/app/blog/page.tsx`)

**Objective:** Implement `src/app/blog/page.tsx` as an asynchronous static Server Component reading posts via M2 loaders, exporting static metadata, and rendering `BlogIndex`.

**Acceptance Criteria:**
- ✓ Target file: `src/app/blog/page.tsx`.
- ✓ Zero `'use client'` directive.
- ✓ Exports `export const metadata: Metadata` built via `buildBlogIndexMetadata(siteConfig.siteUrl)`.
- ✓ Default export is an async function: `export default async function BlogPage()`.
- ✓ Calls `getBlogPosts()` and `getSiteConfig()`.
- ✓ Sorts posts via `sortBlogPosts`.
- ✓ Converts posts via `toBlogCardData` and derives tags via `deriveTagOptions`.
- ✓ Renders inside standard layout container without nested `main`, `header`, or `footer` elements.

**Prerequisites:**
- Tasks M8.G5.T4 completed.
- M2 loaders `getBlogPosts` and `getSiteConfig` available.
- M3 `Container` available.

**Implementation Details:**

Create `src/app/blog/page.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
if (-not (Test-Path "src\app\blog")) {
    New-Item -ItemType Directory -Path "src\app\blog" -Force | Out-Null
}

@'
import type { Metadata } from 'next';
import { getBlogPosts } from '@/content/loaders/blog';
import { getSiteConfig } from '@/content/loaders/site';
import { sortBlogPosts } from '@/lib/blog/sort-blog-posts';
import { deriveTagOptions } from '@/lib/blog/derive-tag-options';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { buildBlogIndexMetadata } from '@/lib/blog/blog-metadata';
import { BlogIndex } from '@/components/blog/blog-index';
import { Container } from '@/components/ui/Container';

export const metadata: Metadata = buildBlogIndexMetadata(getSiteConfig().siteUrl);

export default async function BlogPage() {
  const rawPosts = await getBlogPosts();
  const orderedPosts = sortBlogPosts(rawPosts);

  const cardData = orderedPosts.map(toBlogCardData);
  const tagOptions = deriveTagOptions(orderedPosts);

  return (
    <div className="py-8 md:py-12">
      <Container>
        <BlogIndex posts={cardData} tagOptions={tagOptions} />
      </Container>
    </div>
  );
}
'@ | Set-Content "src\app\blog\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 1.4, Req 1.6, Req 15.5, Req 15.6, Req 15.7

---

### M8.G5.T6: Author unit and keyboard tests for `BlogFilterBar` (`tests/blog/blog-filter-bar.test.tsx`)

**Objective:** Write tests in `tests/blog/blog-filter-bar.test.tsx` verifying grouping semantics, `aria-pressed` states, keyboard navigation, and callback triggers.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-filter-bar.test.tsx`.
- ✓ Tests empty `tagOptions` returns null.
- ✓ Tests container has `role="group"` and `aria-label="Filter by tag"`.
- ✓ Tests active tag renders with `aria-pressed="true"`.
- ✓ Tests inactive tags render with `aria-pressed="false"`.
- ✓ Tests "Clear filters" is visible only when `activeTag` is non-null.
- ✓ Tests clicking chip invokes `onSelectTag`.
- ✓ Tests Tab key navigates across chips in document order.

**Prerequisites:**
- M8.G5.T2 completed.

**Implementation Details:**

Create `tests/blog/blog-filter-bar.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BlogFilterBar } from '@/components/blog/blog-filter-bar';

afterEach(() => {
  cleanup();
});

describe('BlogFilterBar unit tests', () => {
  const options = ['Architecture', 'Next.js', 'React'];

  it('renders null when tag options array is empty', () => {
    const { container } = render(
      <BlogFilterBar
        tagOptions={[]}
        activeTag={null}
        onSelectTag={vi.fn()}
        onClear={vi.fn()}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders group with accessible label and aria-pressed attributes', () => {
    render(
      <BlogFilterBar
        tagOptions={options}
        activeTag="Next.js"
        onSelectTag={vi.fn()}
        onClear={vi.fn()}
      />
    );

    const group = screen.getByRole('group', { name: 'Filter by tag' });
    expect(group).toBeInTheDocument();

    const nextChip = screen.getByRole('button', { name: 'Next.js' });
    expect(nextChip).toHaveAttribute('aria-pressed', 'true');

    const reactChip = screen.getByRole('button', { name: 'React' });
    expect(reactChip).toHaveAttribute('aria-pressed', 'false');
  });

  it('renders Clear filters button only when activeTag is present', () => {
    const { rerender } = render(
      <BlogFilterBar
        tagOptions={options}
        activeTag={null}
        onSelectTag={vi.fn()}
        onClear={vi.fn()}
      />
    );
    expect(screen.queryByRole('button', { name: 'Clear filters' })).not.toBeInTheDocument();

    rerender(
      <BlogFilterBar
        tagOptions={options}
        activeTag="Architecture"
        onSelectTag={vi.fn()}
        onClear={vi.fn()}
      />
    );
    expect(screen.getByRole('button', { name: 'Clear filters' })).toBeInTheDocument();
  });

  it('invokes onSelectTag when a chip is clicked', async () => {
    const onSelectTag = vi.fn();
    render(
      <BlogFilterBar
        tagOptions={options}
        activeTag={null}
        onSelectTag={onSelectTag}
        onClear={vi.fn()}
      />
    );

    await userEvent.click(screen.getByRole('button', { name: 'React' }));
    expect(onSelectTag).toHaveBeenCalledWith('React');
  });

  it('supports keyboard navigation via Tab key in document order', async () => {
    render(
      <BlogFilterBar
        tagOptions={options}
        activeTag="Next.js"
        onSelectTag={vi.fn()}
        onClear={vi.fn()}
      />
    );

    await userEvent.tab();
    expect(screen.getByRole('button', { name: 'Architecture' })).toHaveFocus();

    await userEvent.tab();
    expect(screen.getByRole('button', { name: 'Next.js' })).toHaveFocus();

    await userEvent.tab();
    expect(screen.getByRole('button', { name: 'React' })).toHaveFocus();

    await userEvent.tab();
    expect(screen.getByRole('button', { name: 'Clear filters' })).toHaveFocus();
  });
});
'@ | Set-Content "tests\blog\blog-filter-bar.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-filter-bar.test.tsx
```
Expected: 5 tests passing.

**Satisfies Requirements:** Req 5.5, Req 7.1, Req 7.2, Req 7.3, Req 7.7, Req 7.9, Req 7.10

---

### M8.G5.T7: Author integration tests for `BlogExplorer` (`tests/blog/blog-explorer.test.tsx`)

**Objective:** Write integration tests in `tests/blog/blog-explorer.test.tsx` mocking `next/navigation` to verify URL updates, live region announcements, focus restoration, and empty state behaviors.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-explorer.test.tsx`.
- ✓ Mocks `'next/navigation'` using `tests/blog/helpers/navigation-mock.ts`.
- ✓ Verifies clicking chip calls `router.replace` with `{ scroll: false }`.
- ✓ Verifies clicking active chip removes `tag` parameter.
- ✓ Verifies live region is present at initial mount and states correct count.
- ✓ Verifies empty filtered result renders `EmptyState` with a "Clear filters" action.
- ✓ Verifies clicking "Clear filters" moves focus to the first chip.

**Prerequisites:**
- Tasks M8.G5.T1 and M8.G5.T3 completed.

**Implementation Details:**

Create `tests/blog/blog-explorer.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, cleanup, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BlogExplorer } from '@/components/blog/blog-explorer';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import {
  setMockSearchParams,
  resetNavigationMock,
  getReplaceCalls,
} from './helpers/navigation-mock';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostPublished3,
} from './helpers/blog-fixtures';

vi.mock('next/navigation', async () => {
  return await import('./helpers/navigation-mock');
});

afterEach(() => {
  cleanup();
  resetNavigationMock();
});

describe('BlogExplorer integration tests', () => {
  const posts = [
    toBlogCardData(mockPostPublished1),
    toBlogCardData(mockPostPublished2),
    toBlogCardData(mockPostPublished3),
  ];
  const tagOptions = ['Architecture', 'Next.js', 'React', 'TypeScript', 'UnmatchedTag'];

  it('renders all posts initially and displays result count', () => {
    setMockSearchParams('');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    expect(screen.getByText('3 posts shown')).toBeInTheDocument();
    expect(screen.getByText(mockPostPublished1.title)).toBeInTheDocument();
    expect(screen.getByText(mockPostPublished2.title)).toBeInTheDocument();
  });

  it('navigates with scroll: false when a filter chip is clicked', async () => {
    setMockSearchParams('');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    const chip = screen.getByRole('button', { name: 'Next.js' });
    await userEvent.click(chip);

    const calls = getReplaceCalls();
    expect(calls).toHaveLength(1);
    expect(calls[0]?.url).toBe('/blog?tag=Next.js');
    expect(calls[0]?.options).toEqual({ scroll: false });
  });

  it('toggles filter off when clicking an already-active chip', async () => {
    setMockSearchParams('tag=Next.js');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    const chip = screen.getByRole('button', { name: 'Next.js' });
    expect(chip).toHaveAttribute('aria-pressed', 'true');

    await userEvent.click(chip);

    const calls = getReplaceCalls();
    expect(calls).toHaveLength(1);
    expect(calls[0]?.url).toBe('/blog');
    expect(calls[0]?.options).toEqual({ scroll: false });
  });

  it('renders EmptyState and restores focus after clicking Clear filters', async () => {
    setMockSearchParams('tag=UnmatchedTag');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    expect(screen.getByText('0 posts shown')).toBeInTheDocument();
    expect(screen.getByText('No posts match the selected tag.')).toBeInTheDocument();

    const clearBtn = screen.getByRole('button', { name: 'Clear filters' });
    await userEvent.click(clearBtn);

    const calls = getReplaceCalls();
    expect(calls[0]?.url).toBe('/blog');

    // Simulate URL state transition to verify focus restoration
    setMockSearchParams('');
    await waitFor(() => {
      const firstChip = screen.getByRole('button', { name: 'Architecture' });
      expect(firstChip).toHaveFocus();
    });
  });
});
'@ | Set-Content "tests\blog\blog-explorer.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-explorer.test.tsx
```
Expected: 4 tests passing.

**Satisfies Requirements:** Req 7.4, Req 7.5, Req 7.6, Req 7.8, Req 8.3, Req 9.1, Req 9.2, Req 9.3, Req 9.5

---

### M8.G5.T8: Author tests for `BlogIndex` and Server Page (`tests/blog/blog-index.test.tsx`, `tests/blog/blog-page.test.tsx`)

**Objective:** Write tests verifying `BlogIndex` renders a single `h1`, pre-renders fallback cards in `Suspense`, and handles zero posts, and verify `src/app/blog/page.tsx` contains no `'use client'` directive.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-index.test.tsx`.
- ✓ Target file: `tests/blog/blog-page.test.tsx`.
- ✓ Tests `BlogIndex` renders exactly one `h1` named "Blog".
- ✓ Tests zero posts renders empty state and omits `BlogExplorer`.
- ✓ Tests `src/app/blog/page.tsx` source code contains zero occurrences of `'use client'`.
- ✓ Tests `src/app/blog/page.tsx` does not redeclare `BlogPost` or M2 types.

**Prerequisites:**
- Tasks M8.G5.T4 and M8.G5.T5 completed.

**Implementation Details:**

1. Create `tests/blog/blog-index.test.tsx`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { BlogIndex } from '@/components/blog/blog-index';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { mockPostPublished1 } from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('BlogIndex container tests', () => {
  it('renders single h1 heading named Blog', () => {
    const posts = [toBlogCardData(mockPostPublished1)];
    render(<BlogIndex posts={posts} tagOptions={['Architecture']} />);

    const headings = screen.getAllByRole('heading', { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0]).toHaveTextContent('Blog');
  });

  it('renders EmptyState message when posts array is empty', () => {
    render(<BlogIndex posts={[]} tagOptions={[]} />);

    expect(screen.getByText('Posts are being prepared.')).toBeInTheDocument();
    expect(screen.queryByRole('group', { name: 'Filter by tag' })).not.toBeInTheDocument();
  });
});
'@ | Set-Content "tests\blog\blog-index.test.tsx" -Encoding UTF8
```

2. Create `tests/blog/blog-page.test.tsx`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Blog index page route boundaries', () => {
  it('confirms src/app/blog/page.tsx is a static server component with no use client', () => {
    const pagePath = path.resolve(process.cwd(), 'src/app/blog/page.tsx');
    const source = fs.readFileSync(pagePath, 'utf-8');

    expect(source).not.toMatch(/['"]use client['"]/);
    expect(source).not.toMatch(/interface BlogPost\b/);
    expect(source).not.toMatch(/type BlogPost\b/);
  });
});
'@ | Set-Content "tests\blog\blog-page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-index.test.tsx tests/blog/blog-page.test.tsx
```
Expected: 3 tests passing.

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 1.4, Req 1.5, Req 1.7, Req 8.1, Req 8.2

---

### M8.G5.T9: Author axe accessibility checks for blog index states

**Objective:** Create `tests/blog/index-a11y.test.tsx` running automated axe audits on the blog index in default, filtered, and empty states.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/index-a11y.test.tsx`.
- ✓ Tests default state (all posts visible) with axe.
- ✓ Tests filtered state with axe.
- ✓ Tests empty results state with axe.
- ✓ Zero WCAG violations reported across all states.

**Prerequisites:**
- Tasks M8.G5.T3 and M8.G5.T4 completed.

**Implementation Details:**

Create `tests/blog/index-a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, cleanup } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import { BlogExplorer } from '@/components/blog/blog-explorer';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { setMockSearchParams, resetNavigationMock } from './helpers/navigation-mock';
import { mockPostPublished1, mockPostPublished2 } from './helpers/blog-fixtures';

expect.extend(matchers);

vi.mock('next/navigation', async () => {
  return await import('./helpers/navigation-mock');
});

afterEach(() => {
  cleanup();
  resetNavigationMock();
});

describe('Blog index accessibility audits (axe)', () => {
  const posts = [toBlogCardData(mockPostPublished1), toBlogCardData(mockPostPublished2)];
  const tagOptions = ['Architecture', 'Next.js', 'React'];

  it('passes axe audit in default unfiltered state', async () => {
    setMockSearchParams('');
    const { container } = render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit in filtered state', async () => {
    setMockSearchParams('tag=Next.js');
    const { container } = render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit in empty result state', async () => {
    setMockSearchParams('tag=NonExistent');
    const { container } = render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\index-a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/index-a11y.test.tsx
```
Expected: 3 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G5.T10: Checkpoint — Execute lint, typecheck, and all M8.G5 test suites

**Objective:** Run the full verification suite across all Goal 5 artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/blog-filter-bar.test.tsx tests/blog/blog-explorer.test.tsx tests/blog/blog-index.test.tsx tests/blog/blog-page.test.tsx tests/blog/index-a11y.test.tsx` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ Protected repository files remain strictly untouched.

**Prerequisites:**
- Tasks M8.G5.T1 through M8.G5.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G5 test suites
npm test -- tests/blog/blog-filter-bar.test.tsx tests/blog/blog-explorer.test.tsx tests/blog/blog-index.test.tsx tests/blog/blog-page.test.tsx tests/blog/index-a11y.test.tsx

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

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\blog\blog-filter-bar.tsx"
Test-Path "src\components\blog\blog-explorer.tsx"
Test-Path "src\components\blog\blog-index.tsx"
Test-Path "src\app\blog\page.tsx"
Test-Path "tests\blog\helpers\navigation-mock.ts"
npm test -- tests/blog/blog-filter-bar.test.tsx tests/blog/blog-explorer.test.tsx tests/blog/blog-index.test.tsx tests/blog/blog-page.test.tsx tests/blog/index-a11y.test.tsx
npm run typecheck
```
Expected output:
- `True` for all five file paths.
- All unit, integration, and axe tests passing.
- `npm run typecheck` exits with return code 0.