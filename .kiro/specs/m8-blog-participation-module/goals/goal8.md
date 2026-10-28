# M8.G8: Detail Route, Static Params, Metadata, and Static-Output Checks

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the blog post detail route at `src/app/blog/[slug]/page.tsx` (`SCR-06`) as a fully static Server Component. Configure `generateStaticParams` to enumerate all published post slugs while strictly excluding drafts, set `dynamicParams = false` to guarantee static boundary safety, implement `generateMetadata` delivering route-specific article Open Graph and canonical metadata, and invoke `notFound()` for invalid or draft slugs. Compose the detail components (`BlogBreadcrumb`, `BlogPostHeader`, visible summary, `EventMetadata`, `PostBody`, and `PostNavigation`) inside the standard container while ensuring zero client-side JavaScript, zero runtime network requests, zero leaked layout landmarks, and zero JSON-LD injection.

## Goal Success Criteria

- ✓ `src/app/blog/[slug]/page.tsx` exports `dynamicParams = false` and `generateStaticParams` returning `{ slug }` objects strictly for published posts.
- ✓ `generateMetadata` produces canonical URLs (`{siteUrl}/blog/{slug}`) and article Open Graph attributes (`publishedTime`, `tags`, optional `modifiedTime`), calling `notFound()` for missing or draft slugs.
- ✓ The default page export awaits `params` (supporting Next.js 15+ contracts), calls `notFound()` for unknown/draft slugs, and passes pre-rendered markdown via `renderMarkdown` and `demoteHeadings`.
- ✓ Detail composition order inside `Container` is strictly: Breadcrumb $\rightarrow$ Header $\rightarrow$ visible summary $\rightarrow$ EventMetadata $\rightarrow$ PostBody $\rightarrow$ PostNavigation.
- ✓ Page and all detail components contain zero `'use client'`, zero `fetch()`, zero `window`/`document` access, and zero `main`, `header`, or `footer` wrapper duplicates.
- ✓ Unit and static generation tests in `tests/blog/` pass with code 0.

## Prerequisites

- Goals M8.G1 through M8.G7 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- M2 loaders: `getBlogPosts`, `getBlogPostBySlug`, `getSiteConfig`, `renderMarkdown`.
- M3 UI primitive: `Container`.
- Detail components from M8.G6 and M8.G7.

---

## Tasks

### M8.G8.T1: Create detail route shell with `dynamicParams` and `generateStaticParams` (`src/app/blog/[slug]/page.tsx`)

**Objective:** Create `src/app/blog/[slug]/page.tsx` exporting `dynamicParams = false` and `generateStaticParams` returning only published post slugs.

**Acceptance Criteria:**
- ✓ Target file: `src/app/blog/[slug]/page.tsx`.
- ✓ Exports `export const dynamicParams = false;`.
- ✓ Exports `export async function generateStaticParams(): Promise<Array<{ slug: string }>>`.
- ✓ Invokes `getBlogPosts()`, filters `p.draft !== true` defensively, and maps to `{ slug: p.slug }`.
- ✓ Contains zero draft slugs in the returned array.
- ✓ Zero `'use client'` directive.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/content/loaders/blog.ts` available.

**Implementation Details:**

Create the route shell in `src/app/blog/[slug]/page.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
if (-not (Test-Path "src\app\blog\[slug]")) {
    New-Item -ItemType Directory -Path "src\app\blog\[slug]" -Force | Out-Null
}

@'
import { getBlogPosts } from '@/content/loaders/blog';

export const dynamicParams = false;

export async function generateStaticParams(): Promise<Array<{ slug: string }>> {
  const posts = await getBlogPosts();
  // Defense-in-depth: ensure no draft slug is ever pre-rendered
  return posts
    .filter(post => post.draft !== true)
    .map(post => ({
      slug: post.slug,
    }));
}
'@ | Set-Content "src\app\blog\[slug]\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3

---

### M8.G8.T2: Implement `generateMetadata` for blog detail route (`src/app/blog/[slug]/page.tsx`)

**Objective:** Implement `generateMetadata` in `src/app/blog/[slug]/page.tsx` extracting slug parameters, looking up the post, calling `notFound()` on missing/draft items, and returning `buildBlogPostMetadata`.

**Acceptance Criteria:**
- ✓ Exports `export async function generateMetadata({ params }): Promise<Metadata>`.
- ✓ Awaits `params` to satisfy Next.js 15+ asynchronous parameter conventions.
- ✓ Calls `getBlogPostBySlug(slug)` and `getSiteConfig()`.
- ✓ If `post === null` or `post.draft === true`, invokes `notFound()`.
- ✓ Returns metadata generated via `buildBlogPostMetadata(post, siteConfig.siteUrl)`.
- ✓ Canonical URL contains no query or hash.

**Prerequisites:**
- M8.G8.T1 completed.
- `src/lib/blog/blog-metadata.ts` available.
- `src/content/loaders/site.ts` available.

**Implementation Details:**

Append `generateMetadata` to `src/app/blog/[slug]/page.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getBlogPostBySlug } from '@/content/loaders/blog';
import { getSiteConfig } from '@/content/loaders/site';
import { buildBlogPostMetadata } from '@/lib/blog/blog-metadata';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }> | { slug: string };
}): Promise<Metadata> {
  const resolvedParams = await params;
  const post = await getBlogPostBySlug(resolvedParams.slug);

  if (!post || post.draft === true) {
    notFound();
  }

  const siteConfig = getSiteConfig();
  return buildBlogPostMetadata(post, siteConfig.siteUrl);
}
'@ | Add-Content -Path "src\app\blog\[slug]\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 15.4, Req 15.7, Req 15.8

---

### M8.G8.T3: Implement default page component and detail composition (`src/app/blog/[slug]/page.tsx`)

**Objective:** Complete `src/app/blog/[slug]/page.tsx` with the async `BlogPostPage` component composing breadcrumb, header, summary, event metadata, body, and navigation inside `Container`.

**Acceptance Criteria:**
- ✓ Default export is an async Server Component: `export default async function BlogPostPage({ params })`.
- ✓ Awaits `params.slug` and invokes `getBlogPostBySlug(slug)`.
- ✓ If post is missing or draft, invokes `notFound()`.
- ✓ Calls `renderMarkdown(post.content)` to obtain pre-rendered HTML.
- ✓ Calls `selectAdjacentPosts(post.slug, allPosts)` to obtain `previous` and `next` post card data.
- ✓ Renders components strictly in order: `BlogBreadcrumb` $\rightarrow$ `BlogPostHeader` $\rightarrow$ summary `<p>` $\rightarrow$ `EventMetadata` $\rightarrow$ `PostBody` $\rightarrow$ `PostNavigation`.
- ✓ Encloses layout inside M3 `Container` without adding `main`, `header`, or `footer` elements.
- ✓ Zero `'use client'` directive in page or detail child tree.

**Prerequisites:**
- Tasks M8.G8.T1 and M8.G8.T2 completed.
- Detail components (`BlogBreadcrumb`, `BlogPostHeader`, `EventMetadata`, `PostBody`, `PostNavigation`) completed.
- `renderMarkdown` available from M2 pipeline.

**Implementation Details:**

Write the complete finalized `src/app/blog/[slug]/page.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getBlogPosts, getBlogPostBySlug } from '@/content/loaders/blog';
import { getSiteConfig } from '@/content/loaders/site';
import { renderMarkdown } from '@/content/markdown/renderer';
import { selectAdjacentPosts } from '@/lib/blog/select-adjacent-posts';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { buildBlogPostMetadata } from '@/lib/blog/blog-metadata';
import { Container } from '@/components/ui/Container';
import { BlogBreadcrumb } from '@/components/blog/blog-breadcrumb';
import { BlogPostHeader } from '@/components/blog/blog-post-header';
import { EventMetadata } from '@/components/blog/event-metadata';
import { PostBody } from '@/components/blog/post-body';
import { PostNavigation } from '@/components/blog/post-navigation';

export const dynamicParams = false;

export async function generateStaticParams(): Promise<Array<{ slug: string }>> {
  const posts = await getBlogPosts();
  return posts
    .filter(post => post.draft !== true)
    .map(post => ({
      slug: post.slug,
    }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }> | { slug: string };
}): Promise<Metadata> {
  const resolvedParams = await params;
  const post = await getBlogPostBySlug(resolvedParams.slug);

  if (!post || post.draft === true) {
    notFound();
  }

  const siteConfig = getSiteConfig();
  return buildBlogPostMetadata(post, siteConfig.siteUrl);
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }> | { slug: string };
}) {
  const resolvedParams = await params;
  const post = await getBlogPostBySlug(resolvedParams.slug);

  if (!post || post.draft === true) {
    notFound();
  }

  // 1. Pre-render markdown body
  const renderedHtml = await renderMarkdown(post.content);

  // 2. Compute adjacent published posts
  const allPosts = await getBlogPosts();
  const adjacent = selectAdjacentPosts(post.slug, allPosts);

  const previousCard = adjacent.previous ? toBlogCardData(adjacent.previous) : null;
  const nextCard = adjacent.next ? toBlogCardData(adjacent.next) : null;

  return (
    <article className="py-8 md:py-12">
      <Container className="max-w-4xl mx-auto space-y-8">
        <BlogBreadcrumb title={post.title} />

        <BlogPostHeader post={post} />

        <p className="text-lead text-text-secondary leading-relaxed font-normal">
          {post.summary}
        </p>

        <EventMetadata
          eventName={post.eventName}
          eventDate={post.eventDate}
          eventLocation={post.eventLocation}
          eventUrl={post.eventUrl}
        />

        <PostBody html={renderedHtml} />

        <PostNavigation previous={previousCard} next={nextCard} />
      </Container>
    </article>
  );
}
'@ | Set-Content "src\app\blog\[slug]\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 10.1, Req 10.4, Req 10.5, Req 10.6, Req 10.7, Req 10.8, Req 13.6, Req 14.9

---

### M8.G8.T4: Author static params and route boundary tests (`tests/blog/static-params.test.ts`)

**Objective:** Write tests in `tests/blog/static-params.test.ts` verifying that `generateStaticParams` yields exactly the published post slugs, excludes drafts, and `dynamicParams` is false.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/static-params.test.ts`.
- ✓ Tests `dynamicParams` strictly equals `false`.
- ✓ Tests `generateStaticParams` returns an array of `{ slug: string }`.
- ✓ Tests every slug returned matches a published post from fixtures.
- ✓ Tests no draft post slug is ever present.

**Prerequisites:**
- M8.G8.T3 completed.

**Implementation Details:**

Create `tests/blog/static-params.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi } from 'vitest';
import { dynamicParams, generateStaticParams } from '@/app/blog/[slug]/page';
import { allMockBlogPosts, mockPostDraft } from './helpers/blog-fixtures';

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => allMockBlogPosts),
  getBlogPostBySlug: vi.fn(async (slug: string) =>
    allMockBlogPosts.find(p => p.slug === slug) ?? null
  ),
}));

describe('generateStaticParams and dynamicParams validation', () => {
  it('strictly sets dynamicParams to false for static export boundary safety', () => {
    expect(dynamicParams).toBe(false);
  });

  it('generates slugs strictly for published posts and excludes drafts', async () => {
    const params = await generateStaticParams();

    const expectedSlugs = allMockBlogPosts
      .filter(p => p.draft !== true)
      .map(p => ({ slug: p.slug }));

    expect(params).toEqual(expectedSlugs);

    // Verify draft is explicitly absent
    const hasDraftSlug = params.some(item => item.slug === mockPostDraft.slug);
    expect(hasDraftSlug).toBe(false);
  });
});
'@ | Set-Content "tests\blog\static-params.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/static-params.test.ts
```
Expected: 2 tests passing.

**Satisfies Requirements:** Req 10.2, Req 10.3

---

### M8.G8.T5: Author detail metadata generation tests (`tests/blog/detail-metadata.test.ts`)

**Objective:** Write tests in `tests/blog/detail-metadata.test.ts` verifying that `generateMetadata` creates valid article metadata, canonical links, and invokes `notFound()` for unknown/draft slugs.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/detail-metadata.test.ts`.
- ✓ Tests valid slug returns title, description, canonical link, and Open Graph article data.
- ✓ Tests unknown slug invokes `notFound()`.
- ✓ Tests draft slug invokes `notFound()`.
- ✓ Tests canonical URL contains zero query string parameters.

**Prerequisites:**
- M8.G8.T3 completed.

**Implementation Details:**

Create `tests/blog/detail-metadata.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi } from 'vitest';
import { generateMetadata } from '@/app/blog/[slug]/page';
import { notFound } from 'next/navigation';
import {
  allMockBlogPosts,
  mockPostPublished1,
  mockPostDraft,
} from './helpers/blog-fixtures';

vi.mock('next/navigation', () => ({
  notFound: vi.fn(),
}));

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => allMockBlogPosts),
  getBlogPostBySlug: vi.fn(async (slug: string) => {
    const post = allMockBlogPosts.find(p => p.slug === slug);
    return post ?? null;
  }),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(() => ({
    siteUrl: 'https://example.com',
  })),
}));

describe('generateMetadata for /blog/[slug]', () => {
  it('generates article metadata for a valid published post', async () => {
    const meta = await generateMetadata({ params: Promise.resolve({ slug: mockPostPublished1.slug }) });

    expect(meta.title).toBe(mockPostPublished1.title);
    expect(meta.description).toBe(mockPostPublished1.summary);
    expect(meta.alternates?.canonical).toBe(`https://example.com/blog/${mockPostPublished1.slug}`);
    expect(meta.openGraph?.type).toBe('article');
    expect(meta.openGraph?.publishedTime).toBe(mockPostPublished1.publishedAt);
  });

  it('invokes notFound when slug does not exist', async () => {
    await generateMetadata({ params: Promise.resolve({ slug: 'unknown-slug' }) });
    expect(notFound).toHaveBeenCalled();
  });

  it('invokes notFound when requested slug belongs to a draft post', async () => {
    await generateMetadata({ params: Promise.resolve({ slug: mockPostDraft.slug }) });
    expect(notFound).toHaveBeenCalled();
  });
});
'@ | Set-Content "tests\blog\detail-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/detail-metadata.test.ts
```
Expected: 3 tests passing.

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 15.4, Req 15.8

---

### M8.G8.T6: Author detail page integration tests (`tests/blog/detail-page.test.tsx`)

**Objective:** Write React Testing Library tests in `tests/blog/detail-page.test.tsx` verifying complete page composition, visible summary below header, adjacent post wiring, and `notFound()` triggers.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/detail-page.test.tsx`.
- ✓ Tests valid post renders breadcrumb, header, summary paragraph, body, and navigation.
- ✓ Tests unknown slug calls `notFound()`.
- ✓ Tests draft slug calls `notFound()`.
- ✓ Tests event block is omitted when post has zero event attributes.

**Prerequisites:**
- M8.G8.T3 completed.

**Implementation Details:**

Create `tests/blog/detail-page.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import BlogPostPage from '@/app/blog/[slug]/page';
import { notFound } from 'next/navigation';
import {
  allMockBlogPosts,
  mockPostPublished1,
  mockPostNoEvent,
  mockPostDraft,
} from './helpers/blog-fixtures';

vi.mock('next/navigation', () => ({
  notFound: vi.fn(),
}));

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => allMockBlogPosts),
  getBlogPostBySlug: vi.fn(async (slug: string) => {
    const post = allMockBlogPosts.find(p => p.slug === slug);
    return post ?? null;
  }),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(() => ({
    siteUrl: 'https://example.com',
  })),
}));

vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(async (md: string) => `<div>${md}</div>`),
}));

afterEach(() => {
  cleanup();
});

describe('BlogPostPage detail route integration', () => {
  it('renders complete post layout with header, summary, and navigation', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostPublished1.slug }),
    });
    render(PageJsx);

    // Breadcrumb
    expect(screen.getByRole('navigation', { name: 'Breadcrumb' })).toBeInTheDocument();

    // Single h1
    expect(screen.getByRole('heading', { level: 1, name: mockPostPublished1.title })).toBeInTheDocument();

    // Summary visible below header
    expect(screen.getByText(mockPostPublished1.summary)).toBeInTheDocument();

    // Event block present
    expect(screen.getByRole('heading', { level: 2, name: 'Event' })).toBeInTheDocument();

    // Navigation present
    expect(screen.getByRole('navigation', { name: 'Post navigation' })).toBeInTheDocument();
  });

  it('omits Event section when post has no event metadata', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostNoEvent.slug }),
    });
    render(PageJsx);

    expect(screen.queryByRole('heading', { level: 2, name: 'Event' })).not.toBeInTheDocument();
  });

  it('invokes notFound when slug is invalid', async () => {
    await BlogPostPage({ params: Promise.resolve({ slug: 'invalid-slug' }) });
    expect(notFound).toHaveBeenCalled();
  });

  it('invokes notFound when slug is a draft', async () => {
    await BlogPostPage({ params: Promise.resolve({ slug: mockPostDraft.slug }) });
    expect(notFound).toHaveBeenCalled();
  });
});
'@ | Set-Content "tests\blog\detail-page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/detail-page.test.tsx
```
Expected: 4 tests passing.

**Satisfies Requirements:** Req 10.4, Req 10.5, Req 10.6, Req 12.5, Req 14.8

---

### M8.G8.T7: Author detail page structure and landmark isolation tests

**Objective:** Audit the rendered detail page DOM to verify that no `main`, `header`, or `footer` elements are produced (preserved for M4 Root Layout) and only one `h1` exists.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/detail-structure.test.tsx`.
- ✓ Tests rendered detail page does NOT contain `<main>`, `<header>` landmarks that conflict with root layout.
- ✓ Tests rendered page has exactly one `<h1>`.
- ✓ Tests rendered page contains zero `<script type="application/ld+json">` tags.

**Prerequisites:**
- M8.G8.T6 completed.

**Implementation Details:**

Create `tests/blog/detail-structure.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import BlogPostPage from '@/app/blog/[slug]/page';
import { mockPostPublished1 } from './helpers/blog-fixtures';

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => [mockPostPublished1]),
  getBlogPostBySlug: vi.fn(async () => mockPostPublished1),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(() => ({ siteUrl: 'https://example.com' })),
}));

vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(async () => '<p>Rendered Markdown</p>'),
}));

afterEach(() => {
  cleanup();
});

describe('Detail page structure and landmark isolation', () => {
  it('does not render main, header, or footer landmark containers', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostPublished1.slug }),
    });
    const { container } = render(PageJsx);

    expect(container.querySelector('main')).toBeNull();
    expect(container.querySelector('footer')).toBeNull();
  });

  it('renders strictly one h1 on the page', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostPublished1.slug }),
    });
    render(PageJsx);

    const h1s = screen.getAllByRole('heading', { level: 1 });
    expect(h1s).toHaveLength(1);
  });

  it('contains zero JSON-LD structured data scripts', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostPublished1.slug }),
    });
    const { container } = render(PageJsx);

    const jsonLd = container.querySelector('script[type="application/ld+json"]');
    expect(jsonLd).toBeNull();
  });
});
'@ | Set-Content "tests\blog\detail-structure.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/detail-structure.test.tsx
```
Expected: 3 tests passing.

**Satisfies Requirements:** Req 10.7, Req 15.9, Req 16.7

---

### M8.G8.T8: Audit static detail tree for client boundary and network isolation

**Objective:** Audit `src/app/blog/[slug]/page.tsx` and all child components rendered on detail pages to ensure strict absence of `'use client'`, `fetch(`, `window`, and `document`.

**Acceptance Criteria:**
- ✓ Scan `src/app/blog/[slug]/page.tsx`, `blog-breadcrumb.tsx`, `blog-post-header.tsx`, `event-metadata.tsx`, `post-body.tsx`, and `post-navigation.tsx`.
- ✓ Confirms zero occurrences of `'use client'`.
- ✓ Confirms zero occurrences of `fetch(`, `window`, `document`, `cookies()`, or `headers()`.
- ✓ Outputs `PASS` upon successful verification.

**Prerequisites:**
- Tasks M8.G8.T1 through M8.G8.T7 completed.

**Implementation Details:**

Execute PowerShell script to audit client boundaries:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$detailFiles = @(
    "src\app\blog\[slug]\page.tsx",
    "src\components\blog\blog-breadcrumb.tsx",
    "src\components\blog\blog-post-header.tsx",
    "src\components\blog\event-metadata.tsx",
    "src\components\blog\post-body.tsx",
    "src\components\blog\post-navigation.tsx"
)

$hasError = $false
foreach ($file in $detailFiles) {
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
    if ($content -match "\b(fetch\(|window\.|document\.|cookies\(|headers\()") {
        Write-Host "Error: $file contains browser/network calls: $file"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$detailFiles = @(
    "src\app\blog\[slug]\page.tsx",
    "src\components\blog\blog-breadcrumb.tsx",
    "src\components\blog\blog-post-header.tsx",
    "src\components\blog\event-metadata.tsx",
    "src\components\blog\post-body.tsx",
    "src\components\blog\post-navigation.tsx"
)

$hasError = $false
foreach ($file in $detailFiles) {
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
    if ($content -match "\b(fetch\(|window\.|document\.|cookies\(|headers\()") {
        Write-Host "Error: $file contains browser/network calls: $file"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

Expected output from audit: `PASS`.

**Satisfies Requirements:** Req 8.6, Req 10.1, Req 10.8, Req 13.6

---

### M8.G8.T9: Author axe accessibility test on full detail page

**Objective:** Create `tests/blog/detail-a11y.test.tsx` running axe-core audits on the assembled `BlogPostPage` to confirm zero WCAG violations.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/detail-a11y.test.tsx`.
- ✓ Tests full `BlogPostPage` with event metadata with axe.
- ✓ Tests full `BlogPostPage` without event metadata with axe.
- ✓ Zero accessibility violations reported.

**Prerequisites:**
- M8.G8.T3 completed.

**Implementation Details:**

Create `tests/blog/detail-a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, cleanup } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import BlogPostPage from '@/app/blog/[slug]/page';
import { mockPostPublished1, mockPostNoEvent } from './helpers/blog-fixtures';

expect.extend(matchers);

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => [mockPostPublished1, mockPostNoEvent]),
  getBlogPostBySlug: vi.fn(async (slug: string) => {
    if (slug === mockPostPublished1.slug) return mockPostPublished1;
    if (slug === mockPostNoEvent.slug) return mockPostNoEvent;
    return null;
  }),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(() => ({ siteUrl: 'https://example.com' })),
}));

vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(async () => '<p>Rendered documentation.</p>'),
}));

afterEach(() => {
  cleanup();
});

describe('Full blog detail page accessibility audits (axe)', () => {
  it('passes axe audit on post with full event data', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostPublished1.slug }),
    });
    const { container } = render(PageJsx);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit on post without event data', async () => {
    const PageJsx = await BlogPostPage({
      params: Promise.resolve({ slug: mockPostNoEvent.slug }),
    });
    const { container } = render(PageJsx);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\detail-a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/detail-a11y.test.tsx
```
Expected: 2 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G8.T10: Checkpoint — Execute lint, typecheck, and all M8.G8 test suites

**Objective:** Run the full verification suite across all Goal 8 artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/static-params.test.ts tests/blog/detail-metadata.test.ts tests/blog/detail-page.test.tsx tests/blog/detail-structure.test.tsx tests/blog/detail-a11y.test.tsx` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ Zero changes in protected repository files.

**Prerequisites:**
- Tasks M8.G8.T1 through M8.G8.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G8 test suites
npm test -- tests/blog/static-params.test.ts tests/blog/detail-metadata.test.ts tests/blog/detail-page.test.tsx tests/blog/detail-structure.test.tsx tests/blog/detail-a11y.test.tsx

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

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\app\blog\[slug]\page.tsx"
Test-Path "tests\blog\static-params.test.ts"
Test-Path "tests\blog\detail-page.test.tsx"
Test-Path "tests\blog\detail-a11y.test.tsx"
npm test -- tests/blog/static-params.test.ts tests/blog/detail-metadata.test.ts tests/blog/detail-page.test.tsx tests/blog/detail-a11y.test.tsx
npm run typecheck
```
Expected output:
- `True` for all paths.
- All unit, metadata, and axe tests passing.
- `npm run typecheck` exits with return code 0.