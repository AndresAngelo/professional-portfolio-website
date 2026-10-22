# M2.G6: BlogPost Schemas & Loaders

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete `BlogPostFrontmatterSchema` and `BlogPostSchema` in `src/content/schemas/blog-post.ts` enforcing all constraints from `AGENTS.md` Section 5.4 (title 5–120 chars, summary 20–300 chars, `publishedAt`, optional `updatedAt`, `eventType`, optional event metadata with `eventDate` $\le$ `publishedAt`, tags array, `readingTimeMinutes` 1–60, and `draft` flag). Implement the blog loaders (`getBlogPosts()`, `getBlogPostBySlug()`) in `src/content/loaders/blog.ts` with strict draft exclusion, sort by `publishedAt` descending, re-export inferred types via `src/types/content.ts`, and author comprehensive unit tests covering draft exclusion, sorting, and edge cases.

## Goal Success Criteria

- ✓ `src/content/schemas/blog-post.ts` defines and exports `BlogPostFrontmatterSchema`, `BlogPostSchema`, and inferred types
- ✓ Cross-field validation enforces `eventDate` $\le$ `publishedAt` when `eventDate` is present
- ✓ `readingTimeMinutes` is strictly constrained to an integer from 1 to 60
- ✓ `src/content/loaders/blog.ts` implements `getBlogPosts()` and `getBlogPostBySlug()`
- ✓ `getBlogPosts()` strictly filters out all posts where `draft: true`
- ✓ `getBlogPostBySlug()` returns `null` for unknown slugs and for draft posts
- ✓ Non-draft posts are returned sorted by `publishedAt` descending (most recent first)
- ✓ `src/types/content.ts` re-exports `BlogPost` and `BlogPostFrontmatter` without manual interface duplication
- ✓ All unit tests in `tests/unit/schemas/blog-post.test.ts` and `tests/unit/loaders/blog.test.ts` pass cleanly
- ✓ `npm run typecheck` passes with zero errors

## Prerequisites

- Goals M2.G1 through M2.G5 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/content/schemas/enums.ts` (`EventTypeSchema`) and `src/content/schemas/utils.ts` exist and compile
- `tests/fixtures/blog/valid-blog-post.mdx` exists from M2.G1.T7

---

## Tasks

### M2.G6.T1: Implement `BlogPostFrontmatterSchema` with Base Fields

**Objective:** Create `src/content/schemas/blog-post.ts` and author `BlogPostFrontmatterSchema` enforcing all metadata constraints.

**Acceptance Criteria:**
- ✓ `title`: `BlogTitleSchema` (5–120 characters after trim)
- ✓ `slug`: `SlugSchema` (lowercase alphanumeric + hyphens)
- ✓ `summary`: `BlogSummarySchema` (20–300 characters after trim)
- ✓ `publishedAt`: `IsoDateStringSchema`
- ✓ `updatedAt`: nullable `IsoDateStringSchema`
- ✓ `eventType`: `EventTypeSchema`
- ✓ `eventName`: nullable string
- ✓ `eventDate`: nullable `IsoDateStringSchema`
- ✓ `eventLocation`: nullable string
- ✓ `eventUrl`: nullable `HttpsUrlSchema`
- ✓ `tags`: array of non-empty strings
- ✓ `readingTimeMinutes`: integer between 1 and 60
- ✓ `draft`: boolean with default `false`

**Prerequisites:**
- M2.G5 completed
- Target file: `src/content/schemas/blog-post.ts`

**Implementation Details:**

Write the schema module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';
import { EventTypeSchema } from './enums';
import {
  IsoDateStringSchema,
  SlugSchema,
  BlogTitleSchema,
  BlogSummarySchema,
  HttpsUrlSchema,
} from './utils';

/**
 * Blog post frontmatter validation schema.
 * AGENTS.md 4.2 & 5.4
 */
export const BlogPostFrontmatterSchema = z
  .object({
    title: BlogTitleSchema,
    slug: SlugSchema,
    summary: BlogSummarySchema,
    publishedAt: IsoDateStringSchema,
    updatedAt: IsoDateStringSchema.nullable(),
    eventType: EventTypeSchema,
    eventName: z.string().trim().nullable(),
    eventDate: IsoDateStringSchema.nullable(),
    eventLocation: z.string().trim().nullable(),
    eventUrl: HttpsUrlSchema.nullable(),
    tags: z.array(z.string().trim().min(1, 'Tag must not be empty')),
    readingTimeMinutes: z
      .number()
      .int('Reading time must be an integer')
      .min(1, 'Reading time must be at least 1 minute')
      .max(60, 'Reading time must not exceed 60 minutes'),
    draft: z.boolean().default(false),
  });

export type BlogPostFrontmatter = z.infer<typeof BlogPostFrontmatterSchema>;
'@ | Set-Content "src\content\schemas\blog-post.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/blog-post.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.6, Req 15.1

---

### M2.G6.T2: Add Refinement for Event Date Temporal Ordering

**Objective:** Add `.superRefine()` to `BlogPostFrontmatterSchema` enforcing that `eventDate` $\le$ `publishedAt` when `eventDate` is present per `AGENTS.md` Section 5.4.

**Acceptance Criteria:**
- ✓ Rejects when `eventDate` is later than `publishedAt`
- ✓ Accepts when `eventDate` is on or before `publishedAt`
- ✓ Accepts when `eventDate` is null
- ✓ Produces actionable error issue targeting `eventDate`

**Prerequisites:**
- M2.G6.T1 completed
- Target file: `src/content/schemas/blog-post.ts`

**Implementation Details:**

Update `BlogPostFrontmatterSchema` with refinement rules using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';
import { EventTypeSchema } from './enums';
import {
  IsoDateStringSchema,
  SlugSchema,
  BlogTitleSchema,
  BlogSummarySchema,
  HttpsUrlSchema,
} from './utils';

/**
 * Blog post frontmatter validation schema.
 * AGENTS.md 4.2 & 5.4
 */
export const BlogPostFrontmatterSchema = z
  .object({
    title: BlogTitleSchema,
    slug: SlugSchema,
    summary: BlogSummarySchema,
    publishedAt: IsoDateStringSchema,
    updatedAt: IsoDateStringSchema.nullable(),
    eventType: EventTypeSchema,
    eventName: z.string().trim().nullable(),
    eventDate: IsoDateStringSchema.nullable(),
    eventLocation: z.string().trim().nullable(),
    eventUrl: HttpsUrlSchema.nullable(),
    tags: z.array(z.string().trim().min(1, 'Tag must not be empty')),
    readingTimeMinutes: z
      .number()
      .int('Reading time must be an integer')
      .min(1, 'Reading time must be at least 1 minute')
      .max(60, 'Reading time must not exceed 60 minutes'),
    draft: z.boolean().default(false),
  })
  .superRefine((data, ctx) => {
    // AGENTS.md 5.4: eventDate, when present, must not be later than publishedAt
    if (data.eventDate !== null && data.eventDate > data.publishedAt) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: `'eventDate' (${data.eventDate}) must not be later than 'publishedAt' (${data.publishedAt})`,
        path: ['eventDate'],
      });
    }
  });

export type BlogPostFrontmatter = z.infer<typeof BlogPostFrontmatterSchema>;
'@ | Set-Content "src\content\schemas\blog-post.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/blog-post.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.7

---

### M2.G6.T3: Implement Complete `BlogPostSchema` with Markdown Body Content

**Objective:** Append `BlogPostSchema` extending frontmatter with `content: z.string()` to hold the markdown body.

**Acceptance Criteria:**
- ✓ `BlogPostSchema` extends `BlogPostFrontmatterSchema` with `content: z.string()`
- ✓ Inferred type `BlogPost` exported
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G6.T2 completed
- Target file: `src/content/schemas/blog-post.ts`

**Implementation Details:**

Append `BlogPostSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Complete BlogPost entity schema including Markdown body content.
 * AGENTS.md 4.2: BlogPost
 */
export const BlogPostSchema = BlogPostFrontmatterSchema.and(
  z.object({
    content: z.string(),
  })
);

export type BlogPost = z.infer<typeof BlogPostSchema>;
'@
Add-Content -Path "src\content\schemas\blog-post.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/blog-post.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.6, Req 15.1

---

### M2.G6.T4: Author `getBlogPosts()` and `getBlogPostBySlug()` Loaders

**Objective:** Implement `getBlogPosts()` and `getBlogPostBySlug()` in `src/content/loaders/blog.ts` enforcing draft post exclusion, slug uniqueness, and sorting by `publishedAt` descending.

**Acceptance Criteria:**
- ✓ `getBlogPosts(blogDir?: string, includeDrafts?: boolean): Promise<BlogPost[]>` implemented
- ✓ All posts with `draft: true` are excluded from returned array when `includeDrafts` is false (default)
- ✓ Draft posts must still pass schema validation (invalid draft files fail validation)
- ✓ Posts are sorted by `publishedAt` descending (most recent first)
- ✓ `getBlogPostBySlug(slug: string, blogDir?: string): Promise<BlogPost | null>` returns matching published post or null
- ✓ `getBlogPostBySlug()` returns `null` for draft posts even if the slug matches

**Prerequisites:**
- M2.G6.T3 completed
- Target file: `src/content/loaders/blog.ts`

**Implementation Details:**

Write the blog loaders using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { ZodError } from 'zod';
import { BlogPostSchema, type BlogPost } from '../schemas/blog-post';
import {
  ValidationError,
  formatZodError,
  formatValidationError,
  renderErrorReport,
} from '../errors/handler';

const DEFAULT_BLOG_DIR = path.join(process.cwd(), 'content', 'blog');

/**
 * Loads, validates, filters, and sorts all blog posts.
 *
 * @param blogDir - Optional directory path for test fixtures.
 * @param includeDrafts - When false (default), excludes draft: true entries.
 * @returns Sorted array of validated, published BlogPost objects.
 */
export async function getBlogPosts(
  blogDir = DEFAULT_BLOG_DIR,
  includeDrafts = false
): Promise<BlogPost[]> {
  let fileNames: string[];

  try {
    const entries = await fs.readdir(blogDir);
    fileNames = entries.filter((file) => file.endsWith('.mdx'));
  } catch (error) {
    const err = formatValidationError(
      blogDir,
      `Directory not found or unreadable: ${error instanceof Error ? error.message : String(error)}`
    );
    throw new Error(`Content validation failed:\n${renderErrorReport([err])}`);
  }

  const posts: BlogPost[] = [];
  const errors: ValidationError[] = [];
  const seenSlugs = new Map<string, string>();

  for (const fileName of fileNames) {
    const filePath = path.join(blogDir, fileName);

    try {
      const fileContent = await fs.readFile(filePath, 'utf-8');
      const { data: frontmatter, content: rawBody } = matter(fileContent);

      const combinedPayload = {
        ...frontmatter,
        content: rawBody,
      };

      // Validate every post regardless of draft status
      const post = BlogPostSchema.parse(combinedPayload);

      // AGENTS.md 5.1 Rule 1: slug must be unique within its content collection
      if (seenSlugs.has(post.slug)) {
        errors.push(
          formatValidationError(
            filePath,
            `Duplicate slug '${post.slug}' detected. Already defined in '${seenSlugs.get(post.slug)}'`,
            'slug'
          )
        );
      } else {
        seenSlugs.set(post.slug, filePath);

        // AGENTS.md 5.1 Rule 9 & 5.4: draft: true posts must be excluded from production
        if (!post.draft || includeDrafts) {
          posts.push(post);
        }
      }
    } catch (error) {
      if (error instanceof ZodError) {
        errors.push(...formatZodError(error, filePath));
      } else {
        errors.push(
          formatValidationError(
            filePath,
            `Failed to parse blog post file: ${error instanceof Error ? error.message : String(error)}`
          )
        );
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Content validation failed:\n${renderErrorReport(errors)}`);
  }

  // TRD.md 4.1: Sort blog posts by publishedAt descending (most recent first)
  return posts.sort((a, b) => b.publishedAt.localeCompare(a.publishedAt));
}

/**
 * Retrieves a single published blog post by slug.
 * Returns null if post does not exist or has draft: true.
 */
export async function getBlogPostBySlug(
  slug: string,
  blogDir = DEFAULT_BLOG_DIR
): Promise<BlogPost | null> {
  const publishedPosts = await getBlogPosts(blogDir, false);
  const matched = publishedPosts.find((p) => p.slug === slug);
  return matched ?? null;
}
'@ | Set-Content "src\content\loaders\blog.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/loaders/blog.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.5, Req 7.6, Req 7.7, Req 7.8, Req 7.9, Req 7.10, Req 12.1, Req 12.2, Req 12.4

---

### M2.G6.T5: Populate Canonical Root `content/blog/example-blog-post.mdx`

**Objective:** Write the root seed post in `content/blog/example-blog-post.mdx` matching `AGENTS.md` Section 4.3.

**Acceptance Criteria:**
- ✓ File `content/blog/example-blog-post.mdx` exists
- ✓ Frontmatter contains title (5–120 chars), summary (20–300 chars), publishedAt, event metadata, draft: false
- ✓ Passes `BlogPostSchema.parse()` without error

**Prerequisites:**
- M2.G6.T4 completed
- Target file: `content/blog/example-blog-post.mdx`

**Implementation Details:**

Write the seed file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "content\blog")) {
    New-Item -ItemType Directory -Path "content\blog" -Force | Out-Null
}

@'---
title: "Example Meetup Reflection"
slug: "example-meetup"
summary: "A short summary of the event and key takeaway meeting all length constraints."
publishedAt: "2026-04-10"
updatedAt: null
eventType: "meetup"
eventName: "Example Developer Meetup"
eventDate: "2026-04-08"
eventLocation: "Singapore"
eventUrl: "https://example.com/event"
tags:
  - "community"
  - "ai"
readingTimeMinutes: 4
draft: false
---

Post content describing participation, learnings, and technical outcomes.
'@ | Set-Content "content\blog\example-blog-post.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "content\blog\example-blog-post.mdx"
```
Expected output: `True`

**Satisfies Requirements:** Req 18.1, Req 18.2, Req 18.4

---

### M2.G6.T6: Author Unit Tests for `BlogPostSchema` (`tests/unit/schemas/blog-post.test.ts`)

**Objective:** Author tests in `tests/unit/schemas/blog-post.test.ts` verifying title/summary length limits, `readingTimeMinutes` range, and `eventDate` temporal constraints.

**Acceptance Criteria:**
- ✓ Tests valid blog post payload passes
- ✓ Tests rejection when `title` is $< 5$ or $> 120$ characters
- ✓ Tests rejection when `summary` is $< 20$ or $> 300$ characters
- ✓ Tests rejection when `readingTimeMinutes` is $< 1$, $> 60$, or not an integer
- ✓ Tests rejection when `eventDate` is later than `publishedAt`
- ✓ Tests acceptance when `eventDate` equals `publishedAt` or is null

**Prerequisites:**
- M2.G6.T3 completed
- Target file: `tests/unit/schemas/blog-post.test.ts`

**Implementation Details:**

Write `tests/unit/schemas/blog-post.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import { BlogPostSchema } from '@/content/schemas/blog-post';

describe('BlogPostSchema Validation', () => {
  const validBlogPost = {
    title: 'Valid Meetup Reflection',
    slug: 'valid-meetup-reflection',
    summary: 'This is a valid blog summary meeting the minimum 20 characters threshold easily.',
    publishedAt: '2026-04-10',
    updatedAt: null,
    eventType: 'meetup',
    eventName: 'Developer Meetup',
    eventDate: '2026-04-08',
    eventLocation: 'Singapore',
    eventUrl: 'https://example.com/event',
    tags: ['community', 'ai'],
    readingTimeMinutes: 4,
    draft: false,
    content: 'Detailed discussion of pipeline architectures.',
  };

  it('accepts a fully compliant blog post payload', () => {
    const result = BlogPostSchema.safeParse(validBlogPost);
    expect(result.success).toBe(true);
  });

  describe('Length and range boundaries (AGENTS.md 5.4)', () => {
    it('rejects title shorter than 5 characters or longer than 120 characters', () => {
      expect(BlogPostSchema.safeParse({ ...validBlogPost, title: 'Four' }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, title: 'a'.repeat(121) }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, title: 'Valid Blog Title' }).success).toBe(true);
    });

    it('rejects summary shorter than 20 characters or longer than 300 characters', () => {
      expect(BlogPostSchema.safeParse({ ...validBlogPost, summary: 'Short summary' }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, summary: 'a'.repeat(301) }).success).toBe(false);
    });

    it('rejects readingTimeMinutes outside 1-60 range or non-integers', () => {
      expect(BlogPostSchema.safeParse({ ...validBlogPost, readingTimeMinutes: 0 }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, readingTimeMinutes: 61 }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, readingTimeMinutes: 3.5 }).success).toBe(false);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, readingTimeMinutes: 1 }).success).toBe(true);
      expect(BlogPostSchema.safeParse({ ...validBlogPost, readingTimeMinutes: 60 }).success).toBe(true);
    });
  });

  describe('Event date ordering (AGENTS.md 5.4)', () => {
    it('rejects when eventDate is later than publishedAt', () => {
      const invalid = {
        ...validBlogPost,
        eventDate: '2026-04-12',
        publishedAt: '2026-04-10',
      };
      const result = BlogPostSchema.safeParse(invalid);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("must not be later than 'publishedAt'");
      }
    });

    it('accepts when eventDate equals publishedAt', () => {
      const valid = {
        ...validBlogPost,
        eventDate: '2026-04-10',
        publishedAt: '2026-04-10',
      };
      expect(BlogPostSchema.safeParse(valid).success).toBe(true);
    });

    it('accepts when eventDate is null', () => {
      const valid = {
        ...validBlogPost,
        eventDate: null,
      };
      expect(BlogPostSchema.safeParse(valid).success).toBe(true);
    });
  });
});
'@ | Set-Content "tests\unit\schemas\blog-post.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/blog-post.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.6, Req 4.7, Req 19.1, Req 19.5

---

### M2.G6.T7: Author Unit Tests for Draft Post Exclusion in `getBlogPosts()`

**Objective:** Write unit tests in `tests/unit/loaders/blog.test.ts` verifying that draft posts are excluded from `getBlogPosts()`, excluded from `getBlogPostBySlug()`, and that posts are sorted by `publishedAt` descending.

**Acceptance Criteria:**
- ✓ Tests `getBlogPosts()` excludes files where `draft: true`
- ✓ Tests `getBlogPostBySlug()` returns `null` for draft posts
- ✓ Tests `getBlogPostBySlug()` returns post for published posts
- ✓ Tests posts are returned in reverse chronological order (`publishedAt` descending)

**Prerequisites:**
- M2.G6.T4 completed
- Target file: `tests/unit/loaders/blog.test.ts`

**Implementation Details:**

Write `tests/unit/loaders/blog.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import path from 'path';
import fs from 'fs/promises';
import { getBlogPosts, getBlogPostBySlug } from '@/content/loaders/blog';

describe('Blog Loaders and Draft Exclusion', () => {
  const fixturesDir = path.join(process.cwd(), 'tests', 'fixtures', 'blog');
  const tempDir = path.join(process.cwd(), 'tests', 'fixtures', 'temp-blog');

  it('loads valid blog post fixture', async () => {
    const posts = await getBlogPosts(fixturesDir);
    expect(posts.length).toBeGreaterThanOrEqual(1);

    const first = posts[0];
    expect(first?.slug).toBe('example-meetup');
    expect(first?.eventType).toBe('meetup');
    expect(first?.draft).toBe(false);
  });

  describe('Draft exclusion and sorting (AGENTS.md 5.4 & TRD.md 4.1)', () => {
    it('excludes draft: true posts and sorts remaining posts by publishedAt descending', async () => {
      await fs.mkdir(tempDir, { recursive: true });

      const publishedOld = `---
title: "Older Published Post"
slug: "older-published-post"
summary: "This is a summary for the older published post meeting length constraints."
publishedAt: "2026-01-10"
updatedAt: null
eventType: "learning"
eventName: null
eventDate: null
eventLocation: null
eventUrl: null
tags: ["learning"]
readingTimeMinutes: 3
draft: false
---

Content.
`;

      const publishedNew = `---
title: "Newer Published Post"
slug: "newer-published-post"
summary: "This is a summary for the newer published post meeting length constraints."
publishedAt: "2026-03-20"
updatedAt: null
eventType: "project-update"
eventName: null
eventDate: null
eventLocation: null
eventUrl: null
tags: ["update"]
readingTimeMinutes: 5
draft: false
---

Content.
`;

      const draftPost = `---
title: "Draft Work in Progress"
slug: "draft-work-in-progress"
summary: "This is a summary for a draft post that should never appear publicly."
publishedAt: "2026-04-01"
updatedAt: null
eventType: "hackathon"
eventName: null
eventDate: null
eventLocation: null
eventUrl: null
tags: ["hackathon"]
readingTimeMinutes: 2
draft: true
---

Draft content.
`;

      await fs.writeFile(path.join(tempDir, 'p-old.mdx'), publishedOld, 'utf-8');
      await fs.writeFile(path.join(tempDir, 'p-new.mdx'), publishedNew, 'utf-8');
      await fs.writeFile(path.join(tempDir, 'draft.mdx'), draftPost, 'utf-8');

      try {
        const posts = await getBlogPosts(tempDir);

        // Verify draft exclusion
        expect(posts.length).toBe(2);
        expect(posts.find((p) => p.slug === 'draft-work-in-progress')).toBeUndefined();

        // Verify reverse chronological sort
        expect(posts[0]?.slug).toBe('newer-published-post');
        expect(posts[1]?.slug).toBe('older-published-post');

        // Verify getBlogPostBySlug returns null for draft
        const draftLookup = await getBlogPostBySlug('draft-work-in-progress', tempDir);
        expect(draftLookup).toBeNull();

        // Verify getBlogPostBySlug returns published post
        const publishedLookup = await getBlogPostBySlug('newer-published-post', tempDir);
        expect(publishedLookup).not.toBeNull();
        expect(publishedLookup?.slug).toBe('newer-published-post');
      } finally {
        await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
      }
    });

    it('still validates schema of draft posts and fails if draft is invalid', async () => {
      await fs.mkdir(tempDir, { recursive: true });

      const invalidDraft = `---
title: "Bad"
slug: "bad-draft"
summary: "Short"
publishedAt: "invalid-date"
updatedAt: null
eventType: "invalid-event"
tags: []
readingTimeMinutes: 0
draft: true
---
`;

      await fs.writeFile(path.join(tempDir, 'invalid-draft.mdx'), invalidDraft, 'utf-8');

      try {
        await expect(getBlogPosts(tempDir)).rejects.toThrowError(/Content validation failed/);
      } finally {
        await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
      }
    });
  });
});
'@ | Set-Content "tests\unit\loaders\blog.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/blog.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.6, Req 7.7, Req 7.8, Req 12.1, Req 12.2, Req 12.4, Req 19.4

---

### M2.G6.T8: Update Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Re-export `BlogPost` and `BlogPostFrontmatter` in `src/types/content.ts`.

**Acceptance Criteria:**
- ✓ Exports `BlogPost` and `BlogPostFrontmatter` from `@/content/schemas/blog-post`
- ✓ Types are derived strictly via `z.infer<>`
- ✓ Zero manual duplicate interface definitions exist
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G6.T3 completed
- Target file: `src/types/content.ts`

**Implementation Details:**

Update `src/types/content.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
/**
 * Canonical Content Contracts (Single Source of Truth)
 *
 * All types in this file are derived directly from Zod schemas via `z.infer<>`.
 * Per AGENTS.md Section 6.1 Rule 5, manual interface duplication is strictly prohibited.
 */

export type { IsoDateString } from '@/content/schemas/utils';

export type {
  ProjectStatus,
  CertificationCategory,
  EventType,
  ContactChannelType,
} from '@/content/schemas/enums';

export type {
  SiteConfig,
  SiteProfile,
  ContactChannel,
  SocialLink,
  SiteNavigationItem,
} from '@/content/schemas/site';

export type {
  Project,
  ProjectFrontmatter,
  ProjectMetrics,
} from '@/content/schemas/project';

export type {
  Certification,
  CertificationFrontmatter,
} from '@/content/schemas/certification';

export type {
  BlogPost,
  BlogPostFrontmatter,
} from '@/content/schemas/blog-post';
'@ | Set-Content "src\types\content.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/types/content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 20.3

---

### M2.G6.T9: Test Default Path Resolution of `getBlogPosts()`

**Objective:** Write a test confirming `getBlogPosts()` called without arguments reads `content/blog/` and loads the root seed post.

**Acceptance Criteria:**
- ✓ Calling `getBlogPosts()` with no arguments loads `content/blog/`
- ✓ Resolves `example-blog-post.mdx` cleanly
- ✓ Passes in test runner

**Prerequisites:**
- M2.G6.T5 completed
- Target file: `tests/unit/loaders/blog.test.ts`

**Implementation Details:**

Append the root path resolution test to `tests/unit/loaders/blog.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  it('loads the default content/blog directory when no path argument is supplied', async () => {
    const posts = await getBlogPosts();
    expect(posts.length).toBeGreaterThanOrEqual(1);

    const found = posts.find((p) => p.slug === 'example-meetup');
    expect(found).toBeDefined();
    expect(found?.eventType).toBe('meetup');
  });
'@
$content = Get-Content "tests\unit\loaders\blog.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\loaders\blog.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/blog.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.5, Req 18.5

---

### M2.G6.T10: Checkpoint — BlogPost Module Verification

**Objective:** Execute the complete verification pipeline (`typecheck`, `lint`, `test`) ensuring all blog schemas, loaders, and draft exclusion rules pass.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` executes all test suites without errors
- ✓ Zero `any` types or unsafe assertions

**Prerequisites:**
- M2.G6.T1 through M2.G6.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
npm run lint
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.6, Req 7.9, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\content\schemas\blog-post.ts"
Test-Path "src\content\loaders\blog.ts"
Test-Path "content\blog\example-blog-post.mdx"
npm run test -- tests/unit/schemas/blog-post.test.ts tests/unit/loaders/blog.test.ts
npm run typecheck
```
Expected output:
- `True` for `blog-post.ts` schema, `blog.ts` loader, and `example-blog-post.mdx`
- Tests pass cleanly with 0 failures
- `npm run typecheck` exits with return code 0.