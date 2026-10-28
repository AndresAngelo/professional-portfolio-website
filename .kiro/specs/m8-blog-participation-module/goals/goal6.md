# M8.G6: BlogBreadcrumb, BlogPostHeader, and EventMetadata

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the presentational header and context components for the blog detail page: the accessible breadcrumb trail (`BlogBreadcrumb`), the post header with publication and update dates (`BlogPostHeader`), and the conditional event participation block (`EventMetadata`). Guarantee strict heading level progression (`h1` title $\rightarrow$ `h2` event heading), machine-readable `time[datetime]` tags formatted deterministically via M5 `formatDisplayDate` across different system time zones, safe omitted states when optional event fields are empty, and complete WCAG compliance verified through Property 15 (header field rendering and date timezone stability), Property 16 (event block field combinations), and axe-core accessibility audits.

## Goal Success Criteria

- ✓ `src/components/blog/blog-breadcrumb.tsx` renders `<nav aria-label="Breadcrumb">` containing a "Blog" link to `/blog` and the active post title as non-link text with `aria-current="page"`.
- ✓ `src/components/blog/blog-post-header.tsx` renders exactly one `h1`, a `time` element for `publishedAt`, a conditional "Updated {date}" `time` element if and only if `updatedAt !== null`, reading time text, `EventTypeBadge`, and conditional `TagList`.
- ✓ `src/components/blog/event-metadata.tsx` renders a `<section aria-labelledby="event-heading">` with an `h2` "Event", a `<dl>` of name, date, and location terms only for present fields, and an `ExternalLink` labeled "View event" only when `eventUrl` is valid.
- ✓ `EventMetadata` returns `null` when all four event fields are absent, rendering zero markup, zero empty headings, and zero `href="#"` anchors.
- ✓ Property 15 (header dates and timezone stability) and Property 16 (event field permutation fidelity) pass with at least 100 runs each.
- ✓ Axe-core accessibility checks report zero violations across all three components.
- ✓ All files are under 300 lines, use semantic tokens exclusively, and pass `npm run typecheck` and `npm run lint`.

## Prerequisites

- Goals M8.G1 through M8.G5 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream M3 UI primitives: `Badge`, `Tag`, `ExternalLink`, `FOCUS_RING`.
- Upstream M5 date formatter: `formatDisplayDate` (`src/lib/format-date.ts`).

---

## Tasks

### M8.G6.T1: Implement `BlogBreadcrumb` component (`src/components/blog/blog-breadcrumb.tsx`)

**Objective:** Implement `BlogBreadcrumb` rendering an accessible breadcrumb navigation landmark with a link back to `/blog` and the current post title marked with `aria-current="page"`.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-breadcrumb.tsx`.
- ✓ Props interface: `export interface BlogBreadcrumbProps { title: string }`.
- ✓ Renders `<nav aria-label="Breadcrumb">` containing an ordered list (`<ol>`) or semantic breadcrumb wrapper.
- ✓ First item links to `/blog` with visible text "Blog".
- ✓ Second item renders `title` as non-clickable text with attribute `aria-current="page"`.
- ✓ Renders a visual separator with `aria-hidden="true"`.
- ✓ Focus visible ring applied to the link via semantic classes.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `src/components/blog/blog-breadcrumb.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import Link from 'next/link';

export interface BlogBreadcrumbProps {
  title: string;
}

export function BlogBreadcrumb({ title }: BlogBreadcrumbProps) {
  return (
    <nav aria-label="Breadcrumb" className="py-2 text-small text-text-secondary">
      <ol className="flex items-center gap-2 list-none p-0 m-0">
        <li>
          <Link
            href="/blog"
            className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring rounded-sm"
          >
            Blog
          </Link>
        </li>
        <li aria-hidden="true" className="text-text-disabled select-none">
          /
        </li>
        <li aria-current="page" className="font-medium text-text-primary truncate max-w-md">
          {title}
        </li>
      </ol>
    </nav>
  );
}
'@ | Set-Content "src\components\blog\blog-breadcrumb.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 14.9, Req 16.1

---

### M8.G6.T2: Implement `BlogPostHeader` title, published date, reading time, and badge (`src/components/blog/blog-post-header.tsx`)

**Objective:** Implement the initial `BlogPostHeader` structure rendering the single `h1` post title, published date in a `time` element, reading time, and event badge.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/blog-post-header.tsx`.
- ✓ Props interface:
  ```ts
  export interface BlogPostHeaderProps {
    post: Pick<
      BlogPost,
      'title' | 'publishedAt' | 'updatedAt' | 'readingTimeMinutes' | 'eventType' | 'tags'
    >;
  }
  ```
- ✓ Renders exactly one `h1` containing `post.title`.
- ✓ Renders `post.publishedAt` formatted via `formatDisplayDate` in a `time` element with `dateTime={post.publishedAt}`.
- ✓ Renders `"{post.readingTimeMinutes} min read"`.
- ✓ Renders M3 `Badge` representing `post.eventType`.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- M8.G6.T1 completed.
- `@/types/content` (`BlogPost`) available.
- `src/lib/format-date.ts` (`formatDisplayDate`) available.

**Implementation Details:**

Create `src/components/blog/blog-post-header.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogPost } from '@/types/content';
import { Badge } from '@/components/ui/Badge';
import { formatDisplayDate } from '@/lib/format-date';

export interface BlogPostHeaderProps {
  post: Pick<
    BlogPost,
    'title' | 'publishedAt' | 'updatedAt' | 'readingTimeMinutes' | 'eventType' | 'tags'
  >;
}

export function BlogPostHeader({ post }: BlogPostHeaderProps) {
  const publishedDateText = formatDisplayDate(post.publishedAt);
  const readingTimeText = `${post.readingTimeMinutes} min read`;

  return (
    <header className="space-y-4 pb-6 border-b border-border-default">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="secondary">{post.eventType}</Badge>
        <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
        <time dateTime={post.publishedAt} className="text-caption text-text-secondary">
          {publishedDateText}
        </time>
        <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
        <span className="text-caption text-text-secondary">{readingTimeText}</span>
      </div>

      <h1 className="text-heading-1 font-bold text-text-primary tracking-tight">
        {post.title}
      </h1>
    </header>
  );
}
'@ | Set-Content "src\components\blog\blog-post-header.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.5, Req 11.6, Req 16.1, Req 16.10

---

### M8.G6.T3: Add conditional updated date and tags to `BlogPostHeader` (`src/components/blog/blog-post-header.tsx`)

**Objective:** Complete `BlogPostHeader` by adding the conditional "Updated {date}" `time` element when `updatedAt !== null` and the conditional tag list when `tags` is non-empty.

**Acceptance Criteria:**
- ✓ If `post.updatedAt !== null`, renders "Updated {date}" formatted via `formatDisplayDate` inside a `time` element with `dateTime={post.updatedAt}`.
- ✓ If `post.updatedAt === null`, renders zero "Updated" text and no extra time tag.
- ✓ Renders `post.tags` using M3 `Tag` chips if and only if `post.tags.length > 0`.
- ✓ If `post.tags` is empty, omits the tag container markup entirely.
- ✓ Heading hierarchy retains strictly one `h1`.

**Prerequisites:**
- M8.G6.T2 completed.
- M3 `Tag.tsx` available.

**Implementation Details:**

Update `src/components/blog/blog-post-header.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { BlogPost } from '@/types/content';
import { Badge } from '@/components/ui/Badge';
import { Tag } from '@/components/ui/Tag';
import { formatDisplayDate } from '@/lib/format-date';

export interface BlogPostHeaderProps {
  post: Pick<
    BlogPost,
    'title' | 'publishedAt' | 'updatedAt' | 'readingTimeMinutes' | 'eventType' | 'tags'
  >;
}

export function BlogPostHeader({ post }: BlogPostHeaderProps) {
  const publishedDateText = formatDisplayDate(post.publishedAt);
  const readingTimeText = `${post.readingTimeMinutes} min read`;

  return (
    <header className="space-y-4 pb-6 border-b border-border-default">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="secondary">{post.eventType}</Badge>
        <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
        <time dateTime={post.publishedAt} className="text-caption text-text-secondary">
          {publishedDateText}
        </time>

        {post.updatedAt !== null && (
          <>
            <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
            <span className="text-caption text-text-secondary">
              Updated{' '}
              <time dateTime={post.updatedAt} className="text-caption text-text-secondary">
                {formatDisplayDate(post.updatedAt)}
              </time>
            </span>
          </>
        )}

        <span className="text-caption text-text-secondary" aria-hidden="true">•</span>
        <span className="text-caption text-text-secondary">{readingTimeText}</span>
      </div>

      <h1 className="text-heading-1 font-bold text-text-primary tracking-tight">
        {post.title}
      </h1>

      {post.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 pt-2" aria-label="Tags">
          {post.tags.map(tag => (
            <Tag key={tag} label={tag} size="sm" />
          ))}
        </div>
      )}
    </header>
  );
}
'@ | Set-Content "src\components\blog\blog-post-header.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 11.3, Req 11.4, Req 11.7, Req 11.8, Req 16.7, Req 16.10

---

### M8.G6.T4: Implement `EventMetadata` section shell and definition list (`src/components/blog/event-metadata.tsx`)

**Objective:** Implement the initial `EventMetadata` component creating an accessible `<section>` with an `h2` "Event" and a `<dl>` mapping name, date, and location terms.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/event-metadata.tsx`.
- ✓ Props interface:
  ```ts
  export interface EventMetadataProps {
    eventName?: string | null;
    eventDate?: string | null;
    eventLocation?: string | null;
    eventUrl?: string | null;
  }
  ```
- ✓ Renders `<section aria-labelledby="event-metadata-heading">`.
- ✓ Renders an `h2` with id `event-metadata-heading` and text "Event" (`text-heading-3`).
- ✓ If present, renders `eventName` as `<dt>Event Name</dt><dd>{eventName}</dd>`.
- ✓ If present, renders `eventDate` as `<dt>Date</dt><dd><time dateTime={eventDate}>{formatDisplayDate(eventDate)}</time></dd>`.
- ✓ If present, renders `eventLocation` as `<dt>Location</dt><dd>{eventLocation}</dd>`.
- ✓ Omits definition pairs for any absent/null/empty field.

**Prerequisites:**
- M8.G6.T3 completed.
- `src/lib/format-date.ts` available.

**Implementation Details:**

Create `src/components/blog/event-metadata.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { formatDisplayDate } from '@/lib/format-date';

export interface EventMetadataProps {
  eventName?: string | null;
  eventDate?: string | null;
  eventLocation?: string | null;
  eventUrl?: string | null;
}

export function EventMetadata({
  eventName,
  eventDate,
  eventLocation,
  eventUrl,
}: EventMetadataProps) {
  const hasName = Boolean(eventName && eventName.trim().length > 0);
  const hasDate = Boolean(eventDate && eventDate.trim().length > 0);
  const hasLocation = Boolean(eventLocation && eventLocation.trim().length > 0);
  const hasUrl = Boolean(eventUrl && eventUrl.trim().length > 0);

  // Return null if all four fields are absent
  if (!hasName && !hasDate && !hasLocation && !hasUrl) {
    return null;
  }

  const hasDlPairs = hasName || hasDate || hasLocation;

  return (
    <section
      aria-labelledby="event-metadata-heading"
      className="p-6 my-6 rounded-md bg-surface border border-border-default space-y-4"
    >
      <h2 id="event-metadata-heading" className="text-heading-3 font-semibold text-text-primary">
        Event
      </h2>

      {hasDlPairs && (
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-small">
          {hasName && (
            <div>
              <dt className="font-semibold text-text-secondary">Event</dt>
              <dd className="mt-1 text-text-primary">{eventName}</dd>
            </div>
          )}

          {hasDate && (
            <div>
              <dt className="font-semibold text-text-secondary">Date</dt>
              <dd className="mt-1 text-text-primary">
                <time dateTime={eventDate!}>{formatDisplayDate(eventDate!)}</time>
              </dd>
            </div>
          )}

          {hasLocation && (
            <div>
              <dt className="font-semibold text-text-secondary">Location</dt>
              <dd className="mt-1 text-text-primary">{eventLocation}</dd>
            </div>
          )}
        </dl>
      )}
    </section>
  );
}
'@ | Set-Content "src\components\blog\event-metadata.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.3, Req 12.5, Req 12.7, Req 16.7

---

### M8.G6.T5: Add conditional external link and null safeguard to `EventMetadata` (`src/components/blog/event-metadata.tsx`)

**Objective:** Complete `EventMetadata` by rendering the M3 `ExternalLink` labeled "View event" when `eventUrl` is provided, omitting all anchors when URL is missing, and preventing disabled/placeholder links.

**Acceptance Criteria:**
- ✓ Renders M3 `ExternalLink` with `href={eventUrl}` and children "View event" only when `eventUrl` is non-empty.
- ✓ If `eventUrl` is missing or empty, renders NO anchor tag and NO `href="#"` link.
- ✓ External link includes `rel="noopener noreferrer"` and accessible external indicator via M3 primitive.
- ✓ If only `eventUrl` is present, renders the section heading and the link without rendering an empty `<dl>`.
- ✓ Entire component returns `null` when all four fields are absent.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- M8.G6.T4 completed.
- M3 `ExternalLink.tsx` available.

**Implementation Details:**

Update `src/components/blog/event-metadata.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { formatDisplayDate } from '@/lib/format-date';
import { ExternalLink } from '@/components/ui/ExternalLink';

export interface EventMetadataProps {
  eventName?: string | null;
  eventDate?: string | null;
  eventLocation?: string | null;
  eventUrl?: string | null;
}

export function EventMetadata({
  eventName,
  eventDate,
  eventLocation,
  eventUrl,
}: EventMetadataProps) {
  const hasName = Boolean(eventName && eventName.trim().length > 0);
  const hasDate = Boolean(eventDate && eventDate.trim().length > 0);
  const hasLocation = Boolean(eventLocation && eventLocation.trim().length > 0);
  const hasUrl = Boolean(eventUrl && eventUrl.trim().length > 0);

  // Return null if all four fields are absent
  if (!hasName && !hasDate && !hasLocation && !hasUrl) {
    return null;
  }

  const hasDlPairs = hasName || hasDate || hasLocation;

  return (
    <section
      aria-labelledby="event-metadata-heading"
      className="p-6 my-6 rounded-md bg-surface border border-border-default space-y-4"
    >
      <h2 id="event-metadata-heading" className="text-heading-3 font-semibold text-text-primary">
        Event
      </h2>

      {hasDlPairs && (
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-small">
          {hasName && (
            <div>
              <dt className="font-semibold text-text-secondary">Event</dt>
              <dd className="mt-1 text-text-primary">{eventName}</dd>
            </div>
          )}

          {hasDate && (
            <div>
              <dt className="font-semibold text-text-secondary">Date</dt>
              <dd className="mt-1 text-text-primary">
                <time dateTime={eventDate!}>{formatDisplayDate(eventDate!)}</time>
              </dd>
            </div>
          )}

          {hasLocation && (
            <div>
              <dt className="font-semibold text-text-secondary">Location</dt>
              <dd className="mt-1 text-text-primary">{eventLocation}</dd>
            </div>
          )}
        </dl>
      )}

      {hasUrl && (
        <div className="pt-2">
          <ExternalLink href={eventUrl!} aria-label={`View event: ${eventName || 'external page'}`}>
            View event
          </ExternalLink>
        </div>
      )}
    </section>
  );
}
'@ | Set-Content "src\components\blog\event-metadata.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 12.4, Req 12.5, Req 12.6, Req 12.8, Req 16.1

---

### M8.G6.T6: Author unit tests for `BlogBreadcrumb` and `BlogPostHeader` (`tests/blog/blog-breadcrumb.test.tsx`, `tests/blog/blog-post-header.test.tsx`)

**Objective:** Write unit tests for `BlogBreadcrumb` and `BlogPostHeader` verifying navigation landmarks, single `h1` titles, `updatedAt` conditionals, and tag list presence.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/blog-breadcrumb.test.tsx`.
- ✓ Target file: `tests/blog/blog-post-header.test.tsx`.
- ✓ Tests `BlogBreadcrumb` has landmark `<nav aria-label="Breadcrumb">` and `aria-current="page"`.
- ✓ Tests `BlogPostHeader` has exactly one `h1`.
- ✓ Tests `BlogPostHeader` renders "Updated" text if and only if `updatedAt !== null`.
- ✓ Tests `BlogPostHeader` renders tags if and only if `tags.length > 0`.

**Prerequisites:**
- Tasks M8.G6.T1 and M8.G6.T3 completed.

**Implementation Details:**

1. Create `tests/blog/blog-breadcrumb.test.tsx`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { BlogBreadcrumb } from '@/components/blog/blog-breadcrumb';

afterEach(() => {
  cleanup();
});

describe('BlogBreadcrumb unit tests', () => {
  it('renders breadcrumb landmark with link to /blog and aria-current on active title', () => {
    render(<BlogBreadcrumb title="React Summit Key Takeaways" />);

    const nav = screen.getByRole('navigation', { name: 'Breadcrumb' });
    expect(nav).toBeInTheDocument();

    const homeLink = screen.getByRole('link', { name: 'Blog' });
    expect(homeLink).toHaveAttribute('href', '/blog');

    const activeItem = screen.getByText('React Summit Key Takeaways');
    expect(activeItem).toHaveAttribute('aria-current', 'page');
  });
});
'@ | Set-Content "tests\blog\blog-breadcrumb.test.tsx" -Encoding UTF8
```

2. Create `tests/blog/blog-post-header.test.tsx`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { BlogPostHeader } from '@/components/blog/blog-post-header';
import { mockPostPublished1, mockPostPublished2, mockPostNoTags } from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('BlogPostHeader unit tests', () => {
  it('renders exactly one h1 and date time elements', () => {
    render(<BlogPostHeader post={mockPostPublished1} />);

    const headings = screen.getAllByRole('heading', { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0]).toHaveTextContent(mockPostPublished1.title);

    expect(screen.getByText(`${mockPostPublished1.readingTimeMinutes} min read`)).toBeInTheDocument();
    expect(screen.getByText(mockPostPublished1.eventType)).toBeInTheDocument();
  });

  it('renders Updated date when updatedAt is non-null', () => {
    // mockPostPublished1 has updatedAt: '2026-06-18'
    render(<BlogPostHeader post={mockPostPublished1} />);

    expect(screen.getByText(/Updated/)).toBeInTheDocument();
  });

  it('omits Updated date when updatedAt is null', () => {
    // mockPostPublished2 has updatedAt: null
    render(<BlogPostHeader post={mockPostPublished2} />);

    expect(screen.queryByText(/Updated/)).not.toBeInTheDocument();
  });

  it('renders tags when present and omits tag container when empty', () => {
    const { rerender } = render(<BlogPostHeader post={mockPostPublished1} />);
    expect(screen.getByLabelText('Tags')).toBeInTheDocument();

    rerender(<BlogPostHeader post={mockPostNoTags} />);
    expect(screen.queryByLabelText('Tags')).not.toBeInTheDocument();
  });
});
'@ | Set-Content "tests\blog\blog-post-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-breadcrumb.test.tsx tests/blog/blog-post-header.test.tsx
```
Expected: 5 tests passing.

**Satisfies Requirements:** Req 11.1, Req 11.2, Req 11.3, Req 11.4, Req 11.5, Req 11.6, Req 11.7, Req 11.8, Req 14.9

---

### M8.G6.T7: Author Property 15 test for `BlogPostHeader` (PBT with fast-check and timezone verification)

**Objective:** Implement Property 15 in `tests/blog/blog-post-header.test.tsx` verifying that post headers render dates accurately and identically regardless of system timezone (`process.env.TZ`).

**Acceptance Criteria:**
- ✓ Appends Property 15 test to `tests/blog/blog-post-header.test.tsx`.
- ✓ Contains comment: `// Feature: m8-blog-participation-module, Property 15: Post headers render dates and optional fields`.
- ✓ Tests date formatting output invariance under `process.env.TZ = 'UTC'` and `process.env.TZ = 'Asia/Manila'`.
- ✓ Configured with at least 100 runs.
- ✓ Verifies exactly one `h1`, presence of `time[datetime]`, and conditional `updatedAt` / `tags`.

**Prerequisites:**
- M8.G6.T6 completed.
- Fast-check arbitraries available.

**Implementation Details:**

Append Property 15 to `tests/blog/blog-post-header.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

import fc from 'fast-check';
import { arbitraryBlogPost } from './helpers/blog-fixtures';

describe('BlogPostHeader Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 15: Post headers render dates and optional fields
  it('Property 15: renders dates deterministically across timezones and mirrors optional fields', () => {
    const originalTz = process.env.TZ;

    try {
      fc.assert(
        fc.property(arbitraryBlogPost, post => {
          // Verify UTC rendering
          process.env.TZ = 'UTC';
          const { container: containerUtc } = render(<BlogPostHeader post={post} />);
          const timeUtc = containerUtc.querySelector('time')?.textContent;
          cleanup();

          // Verify Asia/Manila rendering
          process.env.TZ = 'Asia/Manila';
          const { container: containerManila } = render(<BlogPostHeader post={post} />);
          const timeManila = containerManila.querySelector('time')?.textContent;

          // 1. Invariance across timezones
          expect(timeUtc).toBe(timeManila);

          // 2. Exactly one h1
          const headings = screen.getAllByRole('heading', { level: 1 });
          expect(headings).toHaveLength(1);
          expect(headings[0]).toHaveTextContent(post.title);

          // 3. Updated date conditional
          if (post.updatedAt !== null) {
            expect(screen.getByText(/Updated/)).toBeInTheDocument();
          } else {
            expect(screen.queryByText(/Updated/)).not.toBeInTheDocument();
          }

          // 4. Tags conditional
          if (post.tags.length > 0) {
            expect(screen.getByLabelText('Tags')).toBeInTheDocument();
          } else {
            expect(screen.queryByLabelText('Tags')).not.toBeInTheDocument();
          }

          cleanup();
        }),
        { numRuns: 100 }
      );
    } finally {
      process.env.TZ = originalTz;
    }
  });
});
'@ | Add-Content -Path "tests\blog\blog-post-header.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/blog-post-header.test.tsx
```
Expected: All unit tests and Property 15 passing (100 runs).

**Satisfies Requirements:** Req 11.1–11.8, Req 17.1, Req 17.2

---

### M8.G6.T8: Author unit and Property 16 tests for `EventMetadata` (`tests/blog/event-metadata.test.tsx`)

**Objective:** Create `tests/blog/event-metadata.test.tsx` verifying field presence rules, absence of broken anchors, and Property 16 PBT for all event field permutations.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/event-metadata.test.tsx`.
- ✓ Unit tests cover: all 4 fields present, only `eventUrl`, only `eventName`, all fields null (returns null), and empty strings.
- ✓ Verifies zero `href="#"` or broken placeholder links.
- ✓ Property 16 test: `// Feature: m8-blog-participation-module, Property 16: The event block shows exactly the present fields` (100 runs).

**Prerequisites:**
- M8.G6.T5 completed.

**Implementation Details:**

Create `tests/blog/event-metadata.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import fc from 'fast-check';
import { EventMetadata } from '@/components/blog/event-metadata';
import { arbitraryIsoDate } from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('EventMetadata unit tests', () => {
  it('returns null when all fields are null or empty', () => {
    const { container: c1 } = render(
      <EventMetadata eventName={null} eventDate={null} eventLocation={null} eventUrl={null} />
    );
    expect(c1.firstChild).toBeNull();

    const { container: c2 } = render(
      <EventMetadata eventName="   " eventDate="" eventLocation={null} eventUrl="" />
    );
    expect(c2.firstChild).toBeNull();
  });

  it('renders all definition pairs and external link when all fields are present', () => {
    render(
      <EventMetadata
        eventName="React Summit"
        eventDate="2026-06-15"
        eventLocation="Amsterdam"
        eventUrl="https://example.com/event"
      />
    );

    expect(screen.getByRole('heading', { level: 2, name: 'Event' })).toBeInTheDocument();
    expect(screen.getByText('React Summit')).toBeInTheDocument();
    expect(screen.getByText('Amsterdam')).toBeInTheDocument();

    const link = screen.getByRole('link', { name: /View event/ });
    expect(link).toHaveAttribute('href', 'https://example.com/event');
  });

  it('renders name and location without link when eventUrl is null (no href="#" anchors)', () => {
    const { container } = render(
      <EventMetadata
        eventName="Local Meetup"
        eventDate={null}
        eventLocation="Singapore"
        eventUrl={null}
      />
    );

    expect(screen.getByText('Local Meetup')).toBeInTheDocument();
    expect(screen.getByText('Singapore')).toBeInTheDocument();

    // Zero links in entire container
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
    expect(container.querySelector('a')).toBeNull();
  });
});

describe('EventMetadata Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 16: The event block shows exactly the present fields
  it('Property 16: renders definition pairs and link matching present field combinations exactly', () => {
    const arbitraryEventProps = fc.record({
      eventName: fc.option(fc.string({ minLength: 1, maxLength: 50 }), { nil: null }),
      eventDate: fc.option(arbitraryIsoDate, { nil: null }),
      eventLocation: fc.option(fc.string({ minLength: 1, maxLength: 40 }), { nil: null }),
      eventUrl: fc.option(fc.webUrl(), { nil: null }),
    });

    fc.assert(
      fc.property(arbitraryEventProps, props => {
        const { container } = render(<EventMetadata {...props} />);

        const hasName = Boolean(props.eventName && props.eventName.trim().length > 0);
        const hasDate = Boolean(props.eventDate && props.eventDate.trim().length > 0);
        const hasLocation = Boolean(props.eventLocation && props.eventLocation.trim().length > 0);
        const hasUrl = Boolean(props.eventUrl && props.eventUrl.trim().length > 0);

        if (!hasName && !hasDate && !hasLocation && !hasUrl) {
          expect(container.firstChild).toBeNull();
        } else {
          expect(screen.getByRole('heading', { level: 2, name: 'Event' })).toBeInTheDocument();

          if (hasName) expect(screen.getByText(props.eventName!)).toBeInTheDocument();
          if (hasLocation) expect(screen.getByText(props.eventLocation!)).toBeInTheDocument();

          if (hasUrl) {
            const link = screen.getByRole('link');
            expect(link).toHaveAttribute('href', props.eventUrl);
            expect(link).not.toHaveAttribute('href', '#');
          } else {
            expect(screen.queryByRole('link')).not.toBeInTheDocument();
          }
        }

        cleanup();
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\event-metadata.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/event-metadata.test.tsx
```
Expected: 3 unit tests and Property 16 passing (100 runs).

**Satisfies Requirements:** Req 12.1–12.8, Req 17.1, Req 17.2

---

### M8.G6.T9: Author axe accessibility tests for detail header and event components

**Objective:** Create `tests/blog/detail-header-a11y.test.tsx` verifying with `axe-core` that `BlogBreadcrumb`, `BlogPostHeader`, and `EventMetadata` are free of accessibility defects.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/detail-header-a11y.test.tsx`.
- ✓ Runs axe on `BlogBreadcrumb`.
- ✓ Runs axe on `BlogPostHeader`.
- ✓ Runs axe on `EventMetadata` with all fields populated.
- ✓ Runs axe on `EventMetadata` with only URL populated.
- ✓ Zero WCAG violations reported.

**Prerequisites:**
- Tasks M8.G6.T1, M8.G6.T3, and M8.G6.T5 completed.

**Implementation Details:**

Create `tests/blog/detail-header-a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, cleanup } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import { BlogBreadcrumb } from '@/components/blog/blog-breadcrumb';
import { BlogPostHeader } from '@/components/blog/blog-post-header';
import { EventMetadata } from '@/components/blog/event-metadata';
import { mockPostPublished1 } from './helpers/blog-fixtures';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

describe('Detail header and event accessibility audits (axe)', () => {
  it('BlogBreadcrumb passes axe audit', async () => {
    const { container } = render(<BlogBreadcrumb title={mockPostPublished1.title} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('BlogPostHeader passes axe audit', async () => {
    const { container } = render(<BlogPostHeader post={mockPostPublished1} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('EventMetadata passes axe audit with full event fields', async () => {
    const { container } = render(
      <EventMetadata
        eventName="Global Summit"
        eventDate="2026-06-15"
        eventLocation="Online"
        eventUrl="https://example.com"
      />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('EventMetadata passes axe audit with only eventUrl', async () => {
    const { container } = render(<EventMetadata eventUrl="https://example.com" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\detail-header-a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/detail-header-a11y.test.tsx
```
Expected: 4 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G6.T10: Checkpoint — Execute lint, typecheck, and all M8.G6 test suites

**Objective:** Run the complete verification gate across all Goal 6 artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/blog-breadcrumb.test.tsx tests/blog/blog-post-header.test.tsx tests/blog/event-metadata.test.tsx tests/blog/detail-header-a11y.test.tsx` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ All created components are below 300 lines of code.

**Prerequisites:**
- Tasks M8.G6.T1 through M8.G6.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G6 test suites
npm test -- tests/blog/blog-breadcrumb.test.tsx tests/blog/blog-post-header.test.tsx tests/blog/event-metadata.test.tsx tests/blog/detail-header-a11y.test.tsx

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

**Satisfies Requirements:** Req 17.5, Req 17.6, Req 17.8, Req 17.10

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\blog\blog-breadcrumb.tsx"
Test-Path "src\components\blog\blog-post-header.tsx"
Test-Path "src\components\blog\event-metadata.tsx"
Test-Path "tests\blog\detail-header-a11y.test.tsx"
npm test -- tests/blog/blog-breadcrumb.test.tsx tests/blog/blog-post-header.test.tsx tests/blog/event-metadata.test.tsx tests/blog/detail-header-a11y.test.tsx
npm run typecheck
```
Expected output:
- `True` for all four paths.
- All unit, property, and axe tests passing.
- `npm run typecheck` exits with return code 0.