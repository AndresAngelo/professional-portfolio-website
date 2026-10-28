# M8.G4: BlogPostCard, BlogPostList, and Metadata Builders

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the presentational card and list components (`BlogPostCard`, `BlogPostList`) and pure SEO metadata builders (`buildBlogIndexMetadata`, `buildBlogPostMetadata`). Enforce defense-in-depth draft exclusion at the list boundary, ensure semantic HTML and responsive layouts without hardcoded design values, and construct metadata with canonical and Open Graph specifications (without JSON-LD). Validate components and builders through unit tests, axe-core accessibility checks, and Property-Based Tests for Properties 13, 14, 19, and 20.

## Goal Success Criteria

- ✓ `src/components/blog/blog-post-card.tsx` renders an accessible M3 `Card` displaying post title, summary, formatted date (`time[datetime]`), reading time, event badge, and tags, with exactly one link pointing to `/blog/{slug}`.
- ✓ `src/components/blog/blog-post-list.tsx` renders an unordered list (`ul > li`) in input order, skipping any item where `draft === true`, using responsive grid/stack utilities.
- ✓ `src/lib/blog/blog-metadata.ts` builds metadata objects with clean canonical URLs (no query/hash), Open Graph `type: "article"` for posts, and a 50–160 character index description.
- ✓ Property 13 (card content rendering), Property 14 (draft exclusion and order preservation), Property 19 (post metadata fidelity), and Property 20 (canonical index URL cleanliness) pass with at least 100 runs each.
- ✓ Automated accessibility checks via axe-core report zero violations for card and list components.
- ✓ All files are under 300 lines, use semantic tokens exclusively, and pass `npm run typecheck` and `npm run lint`.

## Prerequisites

- Goals M8.G1 through M8.G3 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream M3 UI primitives: `Card`, `TagList`, `EventTypeBadge`, `FOCUS_RING`.
- Upstream M5 date formatter: `formatDisplayDate` (`src/lib/format-date.ts`).

---

## Tasks

### M8.G4.T1: Create `BlogPostCard` component shell and heading link (`src/components/blog/blog-post-card.tsx`)

**Objective:** Implement the initial `BlogPostCard` component wrapping an M3 `Card` with an accessible `h2` title link pointing to `/blog/{slug}` with focus rings, summary text, and strict props.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-post-card.tsx`.
- ✓ Props interface: `export interface BlogPostCardProps { post: BlogCardData }`.
- ✓ Imports `Card` from `@/components/ui/Card` (or primitive equivalent).
- ✓ Imports `FOCUS_RING` token from `@/components/ui/` or design tokens.
- ✓ Renders an `h2` heading enclosing a single `next/link` to `/blog/${post.slug}`.
- ✓ Renders post `summary` in a paragraph element using semantic text classes.
- ✓ Props type strictly omits `content` and `draft`.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/lib/blog/blog-types.ts` completed.

**Implementation Details:**

Create `src/components/blog/blog-post-card.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
if (-not (Test-Path "src\components\blog")) {
    New-Item -ItemType Directory -Path "src\components\blog" -Force | Out-Null
}

@'
import Link from 'next/link';
import type { BlogCardData } from '@/lib/blog/blog-types';
import { Card } from '@/components/ui/Card';

export interface BlogPostCardProps {
  post: BlogCardData;
}

export function BlogPostCard({ post }: BlogPostCardProps) {
  return (
    <Card className="flex flex-col justify-between p-6 h-full transition-shadow duration-fast hover:shadow-elevation-2">
      <div className="space-y-3">
        <h2 className="text-heading-3 font-semibold text-text-primary">
          <Link
            href={`/blog/${post.slug}`}
            className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring rounded-sm"
          >
            {post.title}
          </Link>
        </h2>
        <p className="text-body text-text-secondary leading-relaxed line-clamp-3">
          {post.summary}
        </p>
      </div>
    </Card>
  );
}
'@ | Set-Content "src\components\blog\blog-post-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.8, Req 2.9, Req 16.1

---

### M8.G4.T2: Add metadata elements and tags to `BlogPostCard` (`src/components/blog/blog-post-card.tsx`)

**Objective:** Complete `BlogPostCard` by adding publication date in a `time[datetime]` element, reading time, `EventTypeBadge`, and conditional `TagList`.

**Acceptance Criteria:**
- ✓ Renders publication date formatted via `formatDisplayDate(post.publishedAt)` inside a `time` element with `dateTime={post.publishedAt}`.
- ✓ Renders `readingTimeMinutes` as `"{post.readingTimeMinutes} min read"`.
- ✓ Renders `EventTypeBadge` with `type={post.eventType}`.
- ✓ Renders `TagList` (or Tag chips) if and only if `post.tags` is non-empty.
- ✓ Omits tag list markup when `post.tags` is empty.
- ✓ Entire card contains exactly ONE anchor (`<a>`) tag.
- ✓ Uses semantic tokens only (`text-secondary`, `space-3`, etc.).

**Prerequisites:**
- M8.G4.T1 completed.
- `src/lib/format-date.ts` (`formatDisplayDate`) available.
- M3 `Badge.tsx` or `EventTypeBadge.tsx` and `Tag.tsx` available.

**Implementation Details:**

Update `src/components/blog/blog-post-card.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import Link from 'next/link';
import type { BlogCardData } from '@/lib/blog/blog-types';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Tag } from '@/components/ui/Tag';
import { formatDisplayDate } from '@/lib/format-date';

export interface BlogPostCardProps {
  post: BlogCardData;
}

export function BlogPostCard({ post }: BlogPostCardProps) {
  const formattedDate = formatDisplayDate(post.publishedAt);
  const readingTimeText = `${post.readingTimeMinutes} min read`;

  return (
    <Card className="flex flex-col justify-between p-6 h-full transition-shadow duration-fast hover:shadow-elevation-2">
      <div className="space-y-3">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="secondary">{post.eventType}</Badge>
          <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
          <time dateTime={post.publishedAt} className="text-caption text-text-secondary">
            {formattedDate}
          </time>
          <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
          <span className="text-caption text-text-secondary">{readingTimeText}</span>
        </div>

        <h2 className="text-heading-3 font-semibold text-text-primary">
          <Link
            href={`/blog/${post.slug}`}
            className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring rounded-sm"
          >
            {post.title}
          </Link>
        </h2>

        <p className="text-body text-text-secondary leading-relaxed line-clamp-3">
          {post.summary}
        </p>
      </div>

      {post.tags.length > 0 && (
        <div className="pt-4 mt-auto flex flex-wrap gap-2" aria-label="Tags">
          {post.tags.map(tag => (
            <Tag key={tag} label={tag} size="sm" />
          ))}
        </div>
      )}
    </Card>
  );
}
'@ | Set-Content "src\components\blog\blog-post-card.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 2.3, Req 2.4, Req 2.5, Req 2.6, Req 2.7, Req 16.10

---

### M8.G4.T3: Implement `BlogPostList` component (`src/components/blog/blog-post-list.tsx`)

**Objective:** Implement `BlogPostList` to render an unordered list of `BlogPostCard` items with defense-in-depth draft exclusion and responsive layout styling.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-post-list.tsx`.
- ✓ Props interface: `export interface BlogPostListProps { posts: ReadonlyArray<BlogListItem> }`.
- ✓ Filters out any post item having `draft === true`.
- ✓ Renders an accessible `ul` element containing `li` elements for each non-draft post.
- ✓ Preserves exact input order.
- ✓ Uses responsive classes: single column stack on mobile/tablet, capped width layout on desktop.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- M8.G4.T2 completed.
- `src/lib/blog/blog-types.ts` (`BlogListItem`) available.

**Implementation Details:**

Create `src/components/blog/blog-post-list.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogListItem } from '@/lib/blog/blog-types';
import { BlogPostCard } from '@/components/blog/blog-post-card';

export interface BlogPostListProps {
  posts: ReadonlyArray<BlogListItem>;
}

export function BlogPostList({ posts }: BlogPostListProps) {
  // Layer 3 defense-in-depth: skip any item marked as draft
  const visiblePosts = posts.filter(post => post.draft !== true);

  if (visiblePosts.length === 0) {
    return null;
  }

  return (
    <ul
      className="grid grid-cols-1 gap-6 w-full max-w-4xl mx-auto list-none p-0 m-0"
      aria-label="Blog posts"
    >
      {visiblePosts.map(post => (
        <li key={post.slug} className="w-full">
          <BlogPostCard post={post} />
        </li>
      ))}
    </ul>
  );
}
'@ | Set-Content "src\components\blog\blog-post-list.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 3.1, Req 3.4, Req 16.2, Req 17.3

---

### M8.G4.T4: Implement SEO and Open Graph metadata builders (`src/lib/blog/blog-metadata.ts`)

**Objective:** Implement `buildBlogIndexMetadata` and `buildBlogPostMetadata` generating Next.js `Metadata` objects with pure canonical URLs and article Open Graph properties without emitting JSON-LD.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/blog-metadata.ts`.
- ✓ Imports `type { Metadata }` from `'next'`.
- ✓ Exports `export function buildBlogIndexMetadata(siteUrl: string): Metadata`.
- ✓ Exports `export function buildBlogPostMetadata(post: BlogPost, siteUrl: string): Metadata`.
- ✓ Index description is between 50 and 160 characters.
- ✓ Post metadata sets `title: post.title` (root layout appends brand template).
- ✓ Post metadata sets `openGraph.type: 'article'`, `publishedTime`, `tags`.
- ✓ Sets `modifiedTime` if and only if `post.updatedAt !== null`.
- ✓ Canonical URLs use `new URL(path, siteUrl).href` with no query or hash.
- ✓ Does NOT include `application/ld+json` or structured data scripts.

**Prerequisites:**
- `@/types/content` (`BlogPost`) available.

**Implementation Details:**

Create `src/lib/blog/blog-metadata.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { Metadata } from 'next';
import type { BlogPost } from '@/types/content';

export const BLOG_INDEX_DESCRIPTION =
  'A participation log of conferences, meetups, and community events, with notes on what was learned and shared.';

/**
 * Builds static metadata for the /blog index page.
 */
export function buildBlogIndexMetadata(siteUrl: string): Metadata {
  const canonicalUrl = new URL('/blog', siteUrl).href;

  return {
    title: 'Blog',
    description: BLOG_INDEX_DESCRIPTION,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: 'Blog',
      description: BLOG_INDEX_DESCRIPTION,
      url: canonicalUrl,
      type: 'website',
    },
  };
}

/**
 * Builds static metadata for an individual blog post route /blog/[slug].
 */
export function buildBlogPostMetadata(post: BlogPost, siteUrl: string): Metadata {
  const canonicalUrl = new URL(`/blog/${post.slug}`, siteUrl).href;

  return {
    title: post.title,
    description: post.summary,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: post.title,
      description: post.summary,
      url: canonicalUrl,
      type: 'article',
      publishedTime: post.publishedAt,
      ...(post.updatedAt !== null ? { modifiedTime: post.updatedAt } : {}),
      tags: [...post.tags],
    },
  };
}
'@ | Set-Content "src\lib\blog\blog-metadata.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 15.4, Req 15.5, Req 15.6, Req 15.7, Req 15.9

---

### M8.G4.T5: Author unit and Property 13 tests for `BlogPostCard` (`tests/blog/blog-post-card.test.tsx`)

**Objective:** Write React Testing Library tests and Property 13 PBT for `BlogPostCard` verifying link exclusivity, accessibility names, tag rendering, and DOM structure.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-post-card.test.tsx`.
- ✓ Unit test verifies card contains exactly one `<a>` element linking to `/blog/{slug}`.
- ✓ Unit test verifies `time[datetime]` contains the raw ISO date.
- ✓ Unit test verifies reading time text is formatted as `"{n} min read"`.
- ✓ Unit test verifies empty tags array causes tag container to omit.
- ✓ Property 13 test: `// Feature: m8-blog-participation-module, Property 13: Post cards render all required content` (100 runs).

**Prerequisites:**
- M8.G4.T2 completed.
- Fixtures and arbitraries available in `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Create `tests/blog/blog-post-card.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import fc from 'fast-check';
import { BlogPostCard } from '@/components/blog/blog-post-card';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { formatDisplayDate } from '@/lib/format-date';
import {
  mockPostPublished1,
  mockPostNoTags,
  arbitraryBlogPost,
} from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('BlogPostCard unit tests', () => {
  it('renders title as an h2 link pointing to /blog/[slug]', () => {
    const cardData = toBlogCardData(mockPostPublished1);
    render(<BlogPostCard post={cardData} />);

    const link = screen.getByRole('link', { name: mockPostPublished1.title });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', `/blog/${mockPostPublished1.slug}`);

    // Exactly one link on the entire card
    expect(screen.getAllByRole('link')).toHaveLength(1);
  });

  it('renders published date in time element and reading time', () => {
    const cardData = toBlogCardData(mockPostPublished1);
    const { container } = render(<BlogPostCard post={cardData} />);

    const timeElement = container.querySelector('time');
    expect(timeElement).toBeInTheDocument();
    expect(timeElement).toHaveAttribute('datetime', mockPostPublished1.publishedAt);
    expect(timeElement).toHaveTextContent(formatDisplayDate(mockPostPublished1.publishedAt));

    expect(screen.getByText(`${mockPostPublished1.readingTimeMinutes} min read`)).toBeInTheDocument();
  });

  it('omits tag container when tags array is empty', () => {
    const cardData = toBlogCardData(mockPostNoTags);
    render(<BlogPostCard post={cardData} />);

    expect(screen.queryByLabelText('Tags')).not.toBeInTheDocument();
  });
});

describe('BlogPostCard Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 13: Post cards render all required content
  it('Property 13: renders title link, summary, date, reading time, badge, and tags', () => {
    fc.assert(
      fc.property(arbitraryBlogPost, post => {
        const cardData = toBlogCardData(post);
        const { container } = render(<BlogPostCard post={cardData} />);

        // 1. One link named by title
        const links = screen.getAllByRole('link');
        expect(links).toHaveLength(1);
        expect(links[0]).toHaveAttribute('href', `/blog/${post.slug}`);

        // 2. Summary rendered
        expect(screen.getByText(post.summary)).toBeInTheDocument();

        // 3. Time element
        const timeEl = container.querySelector('time');
        expect(timeEl).toHaveAttribute('datetime', post.publishedAt);

        // 4. Reading time
        expect(screen.getByText(`${post.readingTimeMinutes} min read`)).toBeInTheDocument();

        // 5. Tags present or omitted
        if (post.tags.length > 0) {
          expect(screen.getByLabelText('Tags')).toBeInTheDocument();
        } else {
          expect(screen.queryByLabelText('Tags')).not.toBeInTheDocument();
        }

        cleanup();
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\blog-post-card.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-post-card.test.tsx
```
Expected: 3 unit tests and Property 13 passing (100 runs).

**Satisfies Requirements:** Req 2.1–2.9, Req 17.1, Req 17.2

---

### M8.G4.T6: Author unit and Property 14 tests for `BlogPostList` (`tests/blog/blog-post-list.test.tsx`)

**Objective:** Write tests and Property 14 PBT for `BlogPostList` verifying draft exclusion at the component boundary, relative ordering preservation, and list semantics.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-post-list.test.tsx`.
- ✓ Unit test verifies empty array renders `null`.
- ✓ Unit test verifies list preserves input ordering in the DOM.
- ✓ Unit test verifies `draft === true` items are omitted from output.
- ✓ Property 14 test: `// Feature: m8-blog-participation-module, Property 14: The list drops drafts and keeps order` (100 runs).

**Prerequisites:**
- M8.G4.T3 completed.
- Fixtures and arbitraries available.

**Implementation Details:**

Create `tests/blog/blog-post-list.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import fc from 'fast-check';
import { BlogPostList } from '@/components/blog/blog-post-list';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostDraft,
  arbitraryBlogPost,
} from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('BlogPostList unit tests', () => {
  it('returns null when post list is empty', () => {
    const { container } = render(<BlogPostList posts={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders list items in exact input order', () => {
    const posts = [toBlogCardData(mockPostPublished2), toBlogCardData(mockPostPublished1)];
    render(<BlogPostList posts={posts} />);

    const headings = screen.getAllByRole('heading', { level: 2 });
    expect(headings[0]).toHaveTextContent(mockPostPublished2.title);
    expect(headings[1]).toHaveTextContent(mockPostPublished1.title);
  });

  it('filters out items where draft is true', () => {
    const draftItem = { ...toBlogCardData(mockPostDraft), draft: true };
    const posts = [toBlogCardData(mockPostPublished1), draftItem];

    render(<BlogPostList posts={posts} />);

    expect(screen.getByText(mockPostPublished1.title)).toBeInTheDocument();
    expect(screen.queryByText(mockPostDraft.title)).not.toBeInTheDocument();
  });
});

describe('BlogPostList Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 14: The list drops drafts and keeps order
  it('Property 14: drops drafts and preserves relative input order', () => {
    fc.assert(
      fc.property(fc.array(arbitraryBlogPost), posts => {
        const listItems = posts.map(p => ({
          ...toBlogCardData(p),
          draft: p.draft,
        }));

        render(<BlogPostList posts={listItems} />);

        const expectedVisible = listItems.filter(p => p.draft !== true);

        if (expectedVisible.length === 0) {
          expect(screen.queryByRole('list')).not.toBeInTheDocument();
        } else {
          const renderedHeadings = screen.getAllByRole('heading', { level: 2 });
          expect(renderedHeadings).toHaveLength(expectedVisible.length);

          for (let i = 0; i < expectedVisible.length; i++) {
            expect(renderedHeadings[i]).toHaveTextContent(expectedVisible[i].title);
          }
        }

        cleanup();
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\blog-post-list.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-post-list.test.tsx
```
Expected: 3 unit tests and Property 14 passing (100 runs).

**Satisfies Requirements:** Req 3.1, Req 3.4, Req 17.1, Req 17.2, Req 17.3

---

### M8.G4.T7: Author unit and Properties 19, 20 tests for metadata builders (`tests/blog/blog-metadata.test.ts`)

**Objective:** Write tests and Property 19 and 20 PBT in `tests/blog/blog-metadata.test.ts` verifying title, description, clean canonical URL generation, and Open Graph properties.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-metadata.test.ts`.
- ✓ Unit test verifies index metadata description length is between 50 and 160 characters.
- ✓ Unit test verifies canonical URL has no query string or hash.
- ✓ Unit test verifies post with `updatedAt !== null` includes Open Graph `modifiedTime`.
- ✓ Unit test verifies post with `updatedAt === null` omits `modifiedTime`.
- ✓ Property 19 test: `// Feature: m8-blog-participation-module, Property 19: Post metadata mirrors the post` (100 runs).
- ✓ Property 20 test: `// Feature: m8-blog-participation-module, Property 20: Index canonical has no query` (100 runs).

**Prerequisites:**
- M8.G4.T4 completed.
- Fixtures and arbitraries available.

**Implementation Details:**

Create `tests/blog/blog-metadata.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import {
  buildBlogIndexMetadata,
  buildBlogPostMetadata,
  BLOG_INDEX_DESCRIPTION,
} from '@/lib/blog/blog-metadata';
import { mockPostPublished1, mockPostPublished2, arbitraryBlogPost } from './helpers/blog-fixtures';

const testSiteUrl = 'https://example.com';

describe('blog-metadata unit tests', () => {
  it('generates index metadata conforming to character limits and canonical structure', () => {
    expect(BLOG_INDEX_DESCRIPTION.length).toBeGreaterThanOrEqual(50);
    expect(BLOG_INDEX_DESCRIPTION.length).toBeLessThanOrEqual(160);

    const meta = buildBlogIndexMetadata(testSiteUrl);
    expect(meta.title).toBe('Blog');
    expect(meta.alternates?.canonical).toBe('https://example.com/blog');
    expect(meta.openGraph?.type).toBe('website');
  });

  it('includes modifiedTime when updatedAt is present', () => {
    const meta = buildBlogPostMetadata(mockPostPublished1, testSiteUrl);
    expect(meta.openGraph?.modifiedTime).toBe(mockPostPublished1.updatedAt);
  });

  it('omits modifiedTime when updatedAt is null', () => {
    const meta = buildBlogPostMetadata(mockPostPublished2, testSiteUrl);
    expect(meta.openGraph?.modifiedTime).toBeUndefined();
  });
});

describe('blog-metadata Property Tests', () => {
  const arbitraryOrigin = fc.webUrl().map(url => new URL(url).origin);

  // Feature: m8-blog-participation-module, Property 19: Post metadata mirrors the post
  it('Property 19: buildBlogPostMetadata mirrors post attributes into canonical and openGraph fields', () => {
    fc.assert(
      fc.property(arbitraryBlogPost, arbitraryOrigin, (post, siteUrl) => {
        const meta = buildBlogPostMetadata(post, siteUrl);

        expect(meta.title).toBe(post.title);
        expect(meta.description).toBe(post.summary);
        expect(meta.alternates?.canonical).toBe(`${siteUrl}/blog/${post.slug}`);

        const og = meta.openGraph;
        expect(og?.title).toBe(post.title);
        expect(og?.description).toBe(post.summary);
        expect(og?.url).toBe(`${siteUrl}/blog/${post.slug}`);
        expect(og?.type).toBe('article');
        expect(og?.publishedTime).toBe(post.publishedAt);
        expect(og?.tags).toEqual(post.tags);

        if (post.updatedAt !== null) {
          expect(og?.modifiedTime).toBe(post.updatedAt);
        } else {
          expect(og?.modifiedTime).toBeUndefined();
        }
      }),
      { numRuns: 100 }
    );
  });

  // Feature: m8-blog-participation-module, Property 20: Index canonical has no query
  it('Property 20: buildBlogIndexMetadata generates canonical URL without query string or hash', () => {
    fc.assert(
      fc.property(arbitraryOrigin, siteUrl => {
        const meta = buildBlogIndexMetadata(siteUrl);
        const canonical = meta.alternates?.canonical as string;

        expect(canonical).toBe(`${siteUrl}/blog`);
        expect(canonical).not.toContain('?');
        expect(canonical).not.toContain('#');
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\blog-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-metadata.test.ts
```
Expected: 3 unit tests and Properties 19, 20 passing (100 runs each).

**Satisfies Requirements:** Req 15.1–15.7, Req 17.1, Req 17.2

---

### M8.G4.T8: Author draft-exclusion regression test at component boundary

**Objective:** Add an explicit test case in `tests/blog/blog-post-list.test.tsx` verifying that draft titles, summaries, and unique draft tags are completely absent from the rendered DOM.

**Acceptance Criteria:**
- ✓ Test verifies that injecting multiple draft items among published posts results in zero draft content rendered.
- ✓ Verifies tag lists belonging solely to draft items do not appear in the DOM.
- ✓ Confirms layer-3 defense-in-depth works independently of M2 loader filtering.

**Prerequisites:**
- M8.G4.T6 completed.

**Implementation Details:**

Append boundary test to `tests/blog/blog-post-list.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

describe('BlogPostList defense-in-depth boundary test', () => {
  it('strictly suppresses all draft titles, summaries, and draft-specific tags from output', () => {
    const draftPost = {
      slug: 'secret-draft',
      title: 'Secret Draft Title That Must Not Leak',
      summary: 'Confidential summary text that should never appear on screen.',
      publishedAt: '2026-08-01',
      readingTimeMinutes: 5,
      eventType: 'learning' as const,
      tags: ['TopSecretTag'],
      draft: true,
    };

    const publishedPost = {
      slug: 'public-post',
      title: 'Publicly Visible Article Title',
      summary: 'A completely public summary suitable for reading.',
      publishedAt: '2026-06-01',
      readingTimeMinutes: 3,
      eventType: 'meetup' as const,
      tags: ['OpenTag'],
      draft: false,
    };

    render(<BlogPostList posts={[draftPost, publishedPost]} />);

    expect(screen.getByText('Publicly Visible Article Title')).toBeInTheDocument();
    expect(screen.getByText('OpenTag')).toBeInTheDocument();

    expect(screen.queryByText('Secret Draft Title That Must Not Leak')).not.toBeInTheDocument();
    expect(screen.queryByText('Confidential summary text that should never appear on screen.')).not.toBeInTheDocument();
    expect(screen.queryByText('TopSecretTag')).not.toBeInTheDocument();
  });
});
'@ | Add-Content -Path "tests\blog\blog-post-list.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-post-list.test.tsx
```
Expected: All tests passing including boundary test.

**Satisfies Requirements:** Req 3.4, Req 17.3

---

### M8.G4.T9: Author axe accessibility tests for `BlogPostCard` and `BlogPostList`

**Objective:** Implement automated accessibility audits using `axe-core` to verify that `BlogPostCard` and `BlogPostList` have no contrast, landmark, role, or hierarchy violations.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/card-a11y.test.tsx`.
- ✓ Uses `axe` helper or `vitest-axe` configured in project toolchain.
- ✓ Verifies `BlogPostCard` has zero accessibility violations.
- ✓ Verifies `BlogPostList` has zero accessibility violations.

**Prerequisites:**
- Tasks M8.G4.T2 and M8.G4.T3 completed.

**Implementation Details:**

Create `tests/blog/card-a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import { BlogPostCard } from '@/components/blog/blog-post-card';
import { BlogPostList } from '@/components/blog/blog-post-list';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { mockPostPublished1, mockPostPublished2 } from './helpers/blog-fixtures';

expect.extend(matchers);

describe('BlogPostCard and BlogPostList accessibility (axe)', () => {
  it('BlogPostCard passes axe check with zero violations', async () => {
    const { container } = render(<BlogPostCard post={toBlogCardData(mockPostPublished1)} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('BlogPostList passes axe check with zero violations', async () => {
    const posts = [toBlogCardData(mockPostPublished1), toBlogCardData(mockPostPublished2)];
    const { container } = render(<BlogPostList posts={posts} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\card-a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/card-a11y.test.tsx
```
Expected: 2 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G4.T10: Checkpoint — Run typecheck, lint, and all M8.G4 test suites

**Objective:** Execute full validation gate across all Goal 4 artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/blog-post-card.test.tsx tests/blog/blog-post-list.test.tsx tests/blog/blog-metadata.test.ts tests/blog/card-a11y.test.tsx` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ Zero changes in protected repository files.

**Prerequisites:**
- Tasks M8.G4.T1 through M8.G4.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G4 test suites
npm test -- tests/blog/blog-post-card.test.tsx tests/blog/blog-post-list.test.tsx tests/blog/blog-metadata.test.ts tests/blog/card-a11y.test.tsx

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

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\blog\blog-post-card.tsx"
Test-Path "src\components\blog\blog-post-list.tsx"
Test-Path "src\lib\blog\blog-metadata.ts"
Test-Path "tests\blog\card-a11y.test.tsx"
npm test -- tests/blog/blog-post-card.test.tsx tests/blog/blog-post-list.test.tsx tests/blog/blog-metadata.test.ts tests/blog/card-a11y.test.tsx
npm run typecheck
```
Expected output:
- `True` for all four file paths.
- All unit, property, and axe tests passing.
- `npm run typecheck` exits with return code 0.