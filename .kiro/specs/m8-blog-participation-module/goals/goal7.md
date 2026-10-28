# M8.G7: PostBody and PostNavigation

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the markdown article content container (`PostBody`) and adjacent post navigation (`PostNavigation`). Guarantee an unbroken document heading outline on the detail page by applying the Decision 3 heading demotion rule (shifting `h1` down to `h2` and capping at `h6` so only one page-level `h1` exists) and rendering via M3 `MarkdownDoc`. Render bidirectional reading links ("Previous post: {title}" for older posts and "Next post: {title}" for newer posts) alongside a persistent "Back to blog" destination. Verify all heading demotions, link labeling, and accessibility structures through unit tests, Property 17 (PBT), and axe-core audits.

## Goal Success Criteria

- ✓ Apply Decision 3 rule: If `src/lib/projects/demote-headings.ts` exists and is a pure helper, reuse it read-only; otherwise create pure `src/lib/blog/demote-headings.ts`.
- ✓ `src/components/blog/post-body.tsx` receives pre-rendered markdown HTML, applies `demoteHeadings`, and delegates rendering to M3 `MarkdownDoc`, guaranteeing zero `h1` elements in the body.
- ✓ `src/components/blog/post-navigation.tsx` renders `<nav aria-label="Post navigation">` with contextual links for previous (older) and next (newer) posts and a final "Back to blog" link to `/blog`.
- ✓ Property 17 (heading demotion across levels 1 to 6 and text preservation) passes with at least 100 runs.
- ✓ Combined heading hierarchy audit verifies unbroken heading outline (`h1` title $\rightarrow$ optional `h2` event $\rightarrow$ `h2`/`h3` body headings).
- ✓ Axe-core accessibility checks report zero violations on `PostBody` and `PostNavigation`.
- ✓ All files are under 300 lines, use semantic tokens exclusively, and pass `npm run typecheck` and `npm run lint`.

## Prerequisites

- Goals M8.G1 through M8.G6 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream M3 UI primitives: `MarkdownDoc`, `FOCUS_RING`.
- Decision 3 outcome logged in `.kiro/specs/m8-blog-participation-module/task-notes.md`.

---

## Tasks

### M8.G7.T1: Implement or verify pure heading demotion helper (`demoteHeadings`) per Decision 3

**Objective:** Audit `task-notes.md` for the Decision 3 outcome. If Case 2 applies, implement `demoteHeadings` in `src/lib/blog/demote-headings.ts`. If Case 1 applies, verify the export from `@/lib/projects/demote-headings`.

**Acceptance Criteria:**
- ✓ Checks `.kiro/specs/m8-blog-participation-module/task-notes.md`.
- ✓ If Case 2: Creates `src/lib/blog/demote-headings.ts` exporting pure function `export function demoteHeadings(html: string): string`.
- ✓ If the input HTML contains no `<h1>`, returns input unchanged.
- ✓ If the input contains `<h1>`, shifts every `<hN>` and `</hN>` to level `min(N + 1, 6)`.
- ✓ Preserves all heading attributes (classes, ids) and heading text intact.
- ✓ Preserves all non-heading HTML tags, comments, and text content.
- ✓ Zero framework or DOM dependencies (`react`, `next`, `document`).

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Task M8.G1.T8 completed.

**Implementation Details:**

Create `src/lib/blog/demote-headings.ts` (enforcing Case 2 self-contained contract or providing local fallback):

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Demotes heading levels in rendered HTML if an h1 tag is present.
 * If <h1> or <h1 ...> exists, shifts every hN (h1-h6) to min(N + 1, 6).
 * Preserves tag attributes, non-heading markup, and heading text.
 * Pure function: zero DOM or framework dependencies.
 */
export function demoteHeadings(html: string): string {
  // If no h1 exists, document hierarchy is already valid (h2+)
  if (!/<h1[\s>]/i.test(html)) {
    return html;
  }

  // Replace opening and closing tags in a single pass
  return html.replace(/<\/?h([1-6])([\s>])/gi, (match, levelStr, after) => {
    const isClosing = match.startsWith('</');
    const level = parseInt(levelStr, 10);
    const newLevel = Math.min(level + 1, 6);
    return `${isClosing ? '</h' : '<h'}${newLevel}${after}`;
  });
}
'@ | Set-Content "src\lib\blog\demote-headings.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 13.2, Req 13.3, Req 13.4, Req 13.7, Req 17.4

---

### M8.G7.T2: Implement `PostBody` markdown content component (`src/components/blog/post-body.tsx`)

**Objective:** Implement `PostBody` to accept pre-rendered HTML, apply `demoteHeadings`, and delegate rendering to M3 `MarkdownDoc` within an accessible container.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/post-body.tsx`.
- ✓ Props interface: `export interface PostBodyProps { html: string }`.
- ✓ Applies `demoteHeadings` to `html`.
- ✓ Renders resulting HTML inside M3 `MarkdownDoc` (or prose article container).
- ✓ Limits readable measure via typography guidance (`max-w-prose` or M3 equivalent).
- ✓ Zero `'use client'` directive.
- ✓ No `dangerouslySetInnerHTML` bypass beyond `MarkdownDoc`'s tested primitive boundary.

**Prerequisites:**
- M8.G7.T1 completed.
- M3 `MarkdownDoc.tsx` available.

**Implementation Details:**

Create `src/components/blog/post-body.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { demoteHeadings } from '@/lib/blog/demote-headings';
import { MarkdownDoc } from '@/components/ui/MarkdownDoc';

export interface PostBodyProps {
  html: string;
}

export function PostBody({ html }: PostBodyProps) {
  const safeHtml = demoteHeadings(html);

  return (
    <article className="prose prose-slate max-w-prose w-full py-6 text-text-primary">
      <MarkdownDoc html={safeHtml} />
    </article>
  );
}
'@ | Set-Content "src\components\blog\post-body.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.5, Req 13.6, Req 16.3

---

### M8.G7.T3: Implement `PostNavigation` adjacent links component (`src/components/blog/post-navigation.tsx`)

**Objective:** Implement `PostNavigation` rendering an accessible `<nav aria-label="Post navigation">` with contextual "Previous post" (older), "Next post" (newer), and "Back to blog" links.

**Acceptance Criteria:**
- ✓ Target file: `src/components/blog/post-navigation.tsx`.
- ✓ Props interface:
  ```ts
  export interface PostNavigationProps {
    previous: BlogCardData | null;
    next: BlogCardData | null;
  }
  ```
- ✓ Renders `<nav aria-label="Post navigation">`.
- ✓ If `previous !== null`, renders link to `/blog/${previous.slug}` with text `"Previous post: ${previous.title}"`.
- ✓ If `previous === null`, omits the link (zero placeholder or broken anchor).
- ✓ If `next !== null`, renders link to `/blog/${next.slug}` with text `"Next post: ${next.title}"`.
- ✓ If `next === null`, omits the link.
- ✓ Renders persistent link to `/blog` labeled `"Back to blog"` as the final action.
- ✓ Focus visible ring applied to all links.

**Prerequisites:**
- M8.G7.T2 completed.
- `src/lib/blog/blog-types.ts` (`BlogCardData`) available.

**Implementation Details:**

Create `src/components/blog/post-navigation.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import Link from 'next/link';
import type { BlogCardData } from '@/lib/blog/blog-types';

export interface PostNavigationProps {
  previous: BlogCardData | null;
  next: BlogCardData | null;
}

export function PostNavigation({ previous, next }: PostNavigationProps) {
  return (
    <nav
      aria-label="Post navigation"
      className="mt-12 pt-8 border-t border-border-default space-y-6"
    >
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="flex flex-col items-start">
          {previous && (
            <Link
              href={`/blog/${previous.slug}`}
              className="group text-small text-brand-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring rounded-sm"
            >
              <span className="block text-caption text-text-secondary">← Previous post</span>
              <span className="font-medium text-text-primary group-hover:text-brand-primary">
                {previous.title}
              </span>
            </Link>
          )}
        </div>

        <div className="flex flex-col items-start sm:items-end text-left sm:text-right">
          {next && (
            <Link
              href={`/blog/${next.slug}`}
              className="group text-small text-brand-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring rounded-sm"
            >
              <span className="block text-caption text-text-secondary">Next post →</span>
              <span className="font-medium text-text-primary group-hover:text-brand-primary">
                {next.title}
              </span>
            </Link>
          )}
        </div>
      </div>

      <div className="pt-4 flex justify-center border-t border-border-default">
        <Link
          href="/blog"
          className="text-small font-medium text-brand-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring px-3 py-1.5 rounded-sm"
        >
          Back to blog
        </Link>
      </div>
    </nav>
  );
}
'@ | Set-Content "src\components\blog\post-navigation.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 14.5, Req 14.6, Req 14.7, Req 14.8, Req 16.1

---

### M8.G7.T4: Author unit and Property 17 tests for `demoteHeadings` (`tests/blog/demote-headings.test.ts`)

**Objective:** Write unit tests and Property 17 PBT for `demoteHeadings` verifying heading shift logic, `h6` capping, and non-heading content preservation.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/demote-headings.test.ts`.
- ✓ Tests HTML with no `h1` returns unmodified.
- ✓ Tests `<h1>` shifted to `<h2>`, `<h2>` to `<h3>`, ..., `<h6>` capped at `<h6>`.
- ✓ Tests attributes on heading tags (id, class) are preserved.
- ✓ Tests non-heading tags (`<p>`, `<code>`, `<blockquote>`) are completely unaffected.
- ✓ Property 17 test: `// Feature: m8-blog-participation-module, Property 17: Heading demotion` (100 runs).

**Prerequisites:**
- M8.G7.T1 completed.

**Implementation Details:**

Create `tests/blog/demote-headings.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { demoteHeadings } from '@/lib/blog/demote-headings';

describe('demoteHeadings unit tests', () => {
  it('leaves HTML unchanged when no h1 is present', () => {
    const input = '<h2>Section</h2><p>Paragraph text.</p><h3>Subsection</h3>';
    expect(demoteHeadings(input)).toBe(input);
  });

  it('demotes h1 through h6 by one level and caps at h6 when h1 is present', () => {
    const input = '<h1>Title</h1><h2>Heading 2</h2><h3>Heading 3</h3><h6>Heading 6</h6>';
    const expected = '<h2>Title</h2><h3>Heading 2</h3><h4>Heading 3</h4><h6>Heading 6</h6>';
    expect(demoteHeadings(input)).toBe(expected);
  });

  it('preserves tag attributes and inner heading text intact', () => {
    const input = '<h1 id="main-title" class="text-xl">Main Title</h1><p>Body</p>';
    const expected = '<h2 id="main-title" class="text-xl">Main Title</h2><p>Body</p>';
    expect(demoteHeadings(input)).toBe(expected);
  });
});

describe('demoteHeadings Property Tests', () => {
  // Feature: m8-blog-participation-module, Property 17: Heading demotion
  it('Property 17: never leaves an h1 tag when h1 was present and preserves all text content', () => {
    const arbitraryHtmlContent = fc
      .array(
        fc.oneof(
          fc.string({ minLength: 1, maxLength: 20 }).map(t => `<p>${t}</p>`),
          fc.string({ minLength: 1, maxLength: 20 }).map(t => `<h1>${t}</h1>`),
          fc.string({ minLength: 1, maxLength: 20 }).map(t => `<h2>${t}</h2>`),
          fc.string({ minLength: 1, maxLength: 20 }).map(t => `<h6>${t}</h6>`)
        ),
        { minLength: 1, maxLength: 10 }
      )
      .map(chunks => chunks.join(''));

    fc.assert(
      fc.property(arbitraryHtmlContent, html => {
        const result = demoteHeadings(html);

        if (/<h1[\s>]/i.test(html)) {
          // Output must have zero h1 tags
          expect(/<h1[\s>]/i.test(result)).toBe(false);
        } else {
          expect(result).toBe(html);
        }

        // Text content must be preserved
        const stripTags = (s: string) => s.replace(/<[^>]+>/g, '');
        expect(stripTags(result)).toBe(stripTags(html));
      }),
      { numRuns: 100 }
    );
  });
});
'@ | Set-Content "tests\blog\demote-headings.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/demote-headings.test.ts
```
Expected: 3 unit tests and Property 17 passing (100 runs).

**Satisfies Requirements:** Req 13.2, Req 13.3, Req 13.7, Req 17.1, Req 17.2

---

### M8.G7.T5: Author unit tests for `PostBody` (`tests/blog/post-body.test.tsx`)

**Objective:** Write tests in `tests/blog/post-body.test.tsx` verifying that Markdown HTML with `#`, `##`, `###` headings renders as `h2`, `h3`, `h4`, script tags are excluded, and component contains zero client directives or hooks.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/post-body.test.tsx`.
- ✓ Tests `# Header 1` in markdown renders as `<h2>` in DOM.
- ✓ Tests `## Header 2` in markdown renders as `<h3>` in DOM.
- ✓ Tests `<script>` tags in input HTML do not execute or appear in the rendered document.
- ✓ Confirms zero `'use client'` directive in `src/components/blog/post-body.tsx`.

**Prerequisites:**
- M8.G7.T2 completed.

**Implementation Details:**

Create `tests/blog/post-body.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import fs from 'fs';
import path from 'path';
import { PostBody } from '@/components/blog/post-body';

afterEach(() => {
  cleanup();
});

describe('PostBody component unit tests', () => {
  it('demotes h1 and h2 headings to h2 and h3', () => {
    const rawHtml = '<h1>Top Heading</h1><h2>Sub Heading</h2><p>Body copy.</p>';
    render(<PostBody html={rawHtml} />);

    expect(screen.queryByRole('heading', { level: 1 })).not.toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2, name: 'Top Heading' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 3, name: 'Sub Heading' })).toBeInTheDocument();
  });

  it('does not execute or render unsafe script tags', () => {
    const maliciousHtml = '<p>Normal text</p><script>window.__xss = true;</script>';
    const { container } = render(<PostBody html={maliciousHtml} />);

    expect(container.querySelector('script')).toBeNull();
  });

  it('is a server component with no use client directive', () => {
    const filePath = path.resolve(process.cwd(), 'src/components/blog/post-body.tsx');
    const source = fs.readFileSync(filePath, 'utf-8');

    expect(source).not.toMatch(/['"]use client['"]/);
  });
});
'@ | Set-Content "tests\blog\post-body.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/post-body.test.tsx
```
Expected: 3 tests passing.

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.5, Req 13.6

---

### M8.G7.T6: Author unit tests for `PostNavigation` (`tests/blog/post-navigation.test.tsx`)

**Objective:** Write tests for `PostNavigation` in `tests/blog/post-navigation.test.tsx` verifying previous, next, and back links across middle, first, and last post boundary conditions.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/post-navigation.test.tsx`.
- ✓ Tests middle post: Both "Previous post" and "Next post" links render with titles.
- ✓ Tests newest post: "Next post" link is absent; "Previous post" is present.
- ✓ Tests oldest post: "Previous post" is absent; "Next post" is present.
- ✓ Tests single post: Both directional links absent.
- ✓ Tests "Back to blog" link pointing to `/blog` is present in all cases.
- ✓ Tests `<nav aria-label="Post navigation">` container exists.

**Prerequisites:**
- M8.G7.T3 completed.

**Implementation Details:**

Create `tests/blog/post-navigation.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { PostNavigation } from '@/components/blog/post-navigation';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import {
  mockPostPublished1,
  mockPostPublished2,
  mockPostPublished3,
} from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('PostNavigation unit tests', () => {
  const p1 = toBlogCardData(mockPostPublished1);
  const p2 = toBlogCardData(mockPostPublished2);
  const p3 = toBlogCardData(mockPostPublished3);

  it('renders both previous and next links when both neighbors exist', () => {
    render(<PostNavigation previous={p3} next={p1} />);

    const nav = screen.getByRole('navigation', { name: 'Post navigation' });
    expect(nav).toBeInTheDocument();

    const prevLink = screen.getByRole('link', { name: new RegExp(p3.title) });
    expect(prevLink).toHaveAttribute('href', `/blog/${p3.slug}`);

    const nextLink = screen.getByRole('link', { name: new RegExp(p1.title) });
    expect(nextLink).toHaveAttribute('href', `/blog/${p1.slug}`);

    const backLink = screen.getByRole('link', { name: 'Back to blog' });
    expect(backLink).toHaveAttribute('href', '/blog');
  });

  it('omits next link when next is null (newest post)', () => {
    render(<PostNavigation previous={p2} next={null} />);

    expect(screen.getByRole('link', { name: new RegExp(p2.title) })).toBeInTheDocument();
    expect(screen.queryByText(/Next post →/)).not.toBeInTheDocument();
  });

  it('omits previous link when previous is null (oldest post)', () => {
    render(<PostNavigation previous={null} next={p2} />);

    expect(screen.getByRole('link', { name: new RegExp(p2.title) })).toBeInTheDocument();
    expect(screen.queryByText(/← Previous post/)).not.toBeInTheDocument();
  });

  it('renders only Back to blog when both neighbors are null', () => {
    render(<PostNavigation previous={null} next={null} />);

    expect(screen.getAllByRole('link')).toHaveLength(1);
    expect(screen.getByRole('link', { name: 'Back to blog' })).toBeInTheDocument();
  });
});
'@ | Set-Content "tests\blog\post-navigation.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/post-navigation.test.tsx
```
Expected: 4 tests passing.

**Satisfies Requirements:** Req 14.5, Req 14.6, Req 14.7, Req 14.8

---

### M8.G7.T7: Verify responsive typography and measure classes on `PostBody`

**Objective:** Audit `src/components/blog/post-body.tsx` to verify line length is constrained per `design.md` Section 4.4 without causing overflow on mobile viewports.

**Acceptance Criteria:**
- ✓ `PostBody` contains `max-w-prose` or explicit line length measure class (`65-75ch`).
- ✓ Contains `w-full` ensuring responsiveness down to 375px.
- ✓ Does not use arbitrary pixel widths (`w-[700px]`).
- ✓ Verified by automated test in `tests/blog/post-body-layout.test.tsx`.

**Prerequisites:**
- M8.G7.T2 completed.

**Implementation Details:**

Create `tests/blog/post-body-layout.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { PostBody } from '@/components/blog/post-body';

describe('PostBody layout and measure checks', () => {
  it('applies max-w-prose class to enforce readable measure', () => {
    const { container } = render(<PostBody html="<p>Test paragraph content.</p>" />);
    const article = container.querySelector('article');

    expect(article).not.toBeNull();
    expect(article?.className).toContain('max-w-prose');
    expect(article?.className).toContain('w-full');
  });
});
'@ | Set-Content "tests\blog\post-body-layout.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/post-body-layout.test.tsx
```
Expected: PASS.

**Satisfies Requirements:** Req 16.1, Req 16.3

---

### M8.G7.T8: Author axe accessibility tests for `PostBody` and `PostNavigation`

**Objective:** Implement `tests/blog/post-body-a11y.test.tsx` verifying with `axe-core` that `PostBody` and `PostNavigation` produce zero accessibility violations.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/post-body-a11y.test.tsx`.
- ✓ Tests `PostBody` with demoted headings with axe.
- ✓ Tests `PostNavigation` with both links present with axe.
- ✓ Zero WCAG violations reported.

**Prerequisites:**
- Tasks M8.G7.T2 and M8.G7.T3 completed.

**Implementation Details:**

Create `tests/blog/post-body-a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, cleanup } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import { PostBody } from '@/components/blog/post-body';
import { PostNavigation } from '@/components/blog/post-navigation';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { mockPostPublished1, mockPostPublished2 } from './helpers/blog-fixtures';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

describe('PostBody and PostNavigation accessibility audits (axe)', () => {
  it('PostBody passes axe audit', async () => {
    const html = '<h1>Introduction</h1><p>Body paragraph.</p><h2>Architecture</h2>';
    const { container } = render(<PostBody html={html} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('PostNavigation passes axe audit', async () => {
    const { container } = render(
      <PostNavigation
        previous={toBlogCardData(mockPostPublished2)}
        next={toBlogCardData(mockPostPublished1)}
      />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\post-body-a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/post-body-a11y.test.tsx
```
Expected: 2 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G7.T9: Author end-to-end heading hierarchy outline test

**Objective:** Verify that composing `BlogPostHeader`, `EventMetadata`, and `PostBody` results in an unbroken heading hierarchy with zero skipped levels.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/heading-outline.test.tsx`.
- ✓ Composes `BlogPostHeader` (`h1`), `EventMetadata` (`h2`), and `PostBody` (`h2`, `h3`, `h4`).
- ✓ Asserts exactly one `h1` exists on the page.
- ✓ Asserts all subsequent headings follow proper chronological hierarchy without skipping levels (e.g. no `h1` directly to `h3`).

**Prerequisites:**
- Tasks M8.G7.T2 and M8.G6.T3 completed.

**Implementation Details:**

Create `tests/blog/heading-outline.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, afterEach } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { BlogPostHeader } from '@/components/blog/blog-post-header';
import { EventMetadata } from '@/components/blog/event-metadata';
import { PostBody } from '@/components/blog/post-body';
import { mockPostPublished1 } from './helpers/blog-fixtures';

afterEach(() => {
  cleanup();
});

describe('Detail page heading outline verification', () => {
  it('guarantees single h1 and strict unbroken heading progression', () => {
    const markdownHtml = '<h1>Markdown Title</h1><p>Body</p><h2>Subsection</h2>';

    render(
      <div>
        <BlogPostHeader post={mockPostPublished1} />
        <EventMetadata
          eventName={mockPostPublished1.eventName}
          eventDate={mockPostPublished1.eventDate}
          eventLocation={mockPostPublished1.eventLocation}
          eventUrl={mockPostPublished1.eventUrl}
        />
        <PostBody html={markdownHtml} />
      </div>
    );

    // Exactly one h1 (the post title)
    const h1Headings = screen.getAllByRole('heading', { level: 1 });
    expect(h1Headings).toHaveLength(1);
    expect(h1Headings[0]).toHaveTextContent(mockPostPublished1.title);

    // Check all headings in document order
    const allHeadings = screen.getAllByRole('heading');
    const levels = allHeadings.map(h => parseInt(h.tagName.replace('H', ''), 10));

    expect(levels[0]).toBe(1); // h1: Title
    expect(levels[1]).toBe(2); // h2: Event
    expect(levels[2]).toBe(2); // h2: Demoted Markdown Title
    expect(levels[3]).toBe(3); // h3: Demoted Subsection

    // Verify no skipped levels
    for (let i = 0; i < levels.length - 1; i++) {
      expect(levels[i + 1] - levels[i]).toBeLessThanOrEqual(1);
    }
  });
});
'@ | Set-Content "tests\blog\heading-outline.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/heading-outline.test.tsx
```
Expected: PASS.

**Satisfies Requirements:** Req 13.2, Req 13.3, Req 16.7

---

### M8.G7.T10: Checkpoint — Execute lint, typecheck, and all M8.G7 test suites

**Objective:** Run the full verification suite across all Goal 7 artifacts.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/demote-headings.test.ts tests/blog/post-body.test.tsx tests/blog/post-navigation.test.tsx tests/blog/post-body-layout.test.tsx tests/blog/post-body-a11y.test.tsx tests/blog/heading-outline.test.tsx` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ All created components are below 300 lines.

**Prerequisites:**
- Tasks M8.G7.T1 through M8.G7.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G7 test suites
npm test -- tests/blog/demote-headings.test.ts tests/blog/post-body.test.tsx tests/blog/post-navigation.test.tsx tests/blog/post-body-layout.test.tsx tests/blog/post-body-a11y.test.tsx tests/blog/heading-outline.test.tsx

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

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\blog\demote-headings.ts"
Test-Path "src\components\blog\post-body.tsx"
Test-Path "src\components\blog\post-navigation.tsx"
Test-Path "tests\blog\heading-outline.test.tsx"
npm test -- tests/blog/demote-headings.test.ts tests/blog/post-body.test.tsx tests/blog/post-navigation.test.tsx tests/blog/heading-outline.test.tsx
npm run typecheck
```
Expected output:
- `True` for all paths.
- All unit, property, and outline tests passing.
- `npm run typecheck` exits with return code 0.