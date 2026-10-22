# M2 Content Architecture & Validation — Design Document

> **Document Status:** Draft  
> **Feature Name:** m2-content-architecture-validation  
> **Milestone:** M2  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md`, `PRD.md`, `TRD.md`, `requirements.md`  
> **Last Updated:** 2026-10-20

---

## Overview

### Purpose
M2 establishes the complete content infrastructure for `personal-website-portfolio-v2`. This layer bridges raw Markdown/JSON files in the `content/` directory to type-safe, validated collections consumed by routes and components. M2 is not a feature visible to users; it is the internal pipeline ensuring all content is strictly validated before build completion.

### Scope
- **In-Scope:** Zod schema validators, content loaders, Markdown rendering pipeline, build-time validation hooks, type inference via `z.infer<>`, error handling, and comprehensive testing.
- **Out-of-Scope:** UI components, routes (M3), database persistence, runtime API routes (not in P0).

### Success Criteria
1. All 6 content types (SiteConfig, Project, Certification, BlogPost, + 2 enum modules) have strict Zod schemas.
2. All loaders return typed collections or individual items with guaranteed type safety.
3. Build fails with descriptive, actionable errors when any content is invalid.
4. No TypeScript type definitions are duplicated; all types derived from Zod via `z.infer<>`.
5. Markdown content is safely rendered to HTML with syntax highlighting and XSS protection.
6. 100% of content validation rules from requirements are enforced at build time.
7. Test coverage > 80% for content modules and validation rules.

---

## Architecture

### 2.1 System Diagram

```
Local Content Files (Markdown/JSON)
        |
        v
Content Loader Layer
 ├─ getSiteConfig()
 ├─ getProjects()
 ├─ getCertifications()
 └─ getBlogPosts()
        |
        v
Zod Schema Validation Layer
 ├─ Enum Schemas
 ├─ SiteConfig Schema
 ├─ Project Schema
 ├─ Certification Schema
 └─ BlogPost Schema
        |
        v
Frontmatter Parsing (YAML → object)
        |
        v
Markdown Rendering Pipeline
 ├─ remark plugins (metadata extraction)
 ├─ rehype plugins (HTML generation)
 ├─ Syntax highlighting (Shiki/Prism)
 └─ HTML sanitization (DOMPurify)
        |
        v
Type Inference via z.infer<>
 ├─ type SiteConfig = z.infer<typeof SiteConfigSchema>
 ├─ type Project = z.infer<typeof ProjectSchema>
 ├─ type Certification = z.infer<typeof CertificationSchema>
 └─ type BlogPost = z.infer<typeof BlogPostSchema>
        |
        v
Build-Time Validation Hooks
 ├─ Pre-build schema validation
 ├─ Collection-level constraints (featured count, slug uniqueness, draft exclusion)
 └─ Error aggregation and reporting
        |
        v
Static Route Generation (M3)
 └─ Routes populated with validated collections
```

### 2.2 Data Flow: From Content File to Typed Collection

1. **File Discovery:** Loader scans `content/{projects,certifications,blog}/*.mdx` or `content/site.json`.
2. **File Read:** Loader reads file content from disk.
3. **Frontmatter Extraction:** For Markdown files, extract YAML between `***` delimiters using a YAML parser (e.g., `gray-matter` or `js-yaml`).
4. **Schema Validation:** Zod schema validates extracted frontmatter and SiteConfig JSON.
5. **Markdown Rendering:** If present, Markdown content is parsed via remark/rehype pipeline, producing HTML with syntax highlighting and sanitization.
6. **Type Inference:** TypeScript derives type from Zod schema using `z.infer<>`, ensuring all downstream code is type-safe.
7. **Collection Assembly:** Individual validated items are aggregated, sorted, and filtered (e.g., draft exclusion).
8. **Error Handling:** Any validation failure triggers a detailed error with file path, field, and resolution guidance.

### 2.3 Design Principles

1. **Single Source of Truth (SSOT):** All schemas, validation rules, and contracts defined in Zod; no TypeScript interfaces duplicate schema definitions.
2. **Fail Fast:** Build fails immediately on any content validation error; no partial builds or silent failures.
3. **Descriptive Errors:** All validation errors include file path, field name, expected format, and received value category.
4. **Type Safety:** Strict TypeScript with no `any`, implicit `any`, non-null assertions, or unsafe type casts.
5. **Security:** Markdown rendering sanitizes output to prevent XSS; all external links are validated.
6. **Maintainability:** Schemas are declarative and composable; content editors can publish new entries without touching source code.

---

## Components and Interfaces

### 3.1 Schema Modules

#### `src/content/schemas/enums.ts`

Defines all enum schemas using Zod's `.enum()` method.

```typescript
import { z } from 'zod';

export const ProjectStatusSchema = z.enum(['completed', 'in-progress', 'archived']);
export type ProjectStatus = z.infer<typeof ProjectStatusSchema>;

export const CertificationCategorySchema = z.enum([
  'cloud',
  'ai',
  'security',
  'frontend',
  'backend',
  'data',
  'devops',
  'professional',
]);
export type CertificationCategory = z.infer<typeof CertificationCategorySchema>;

export const EventTypeSchema = z.enum([
  'meetup',
  'hackathon',
  'workshop',
  'conference',
  'learning',
  'project-update',
]);
export type EventType = z.infer<typeof EventTypeSchema>;

export const ContactChannelTypeSchema = z.enum(['email', 'linkedin', 'github', 'website', 'other']);
export type ContactChannelType = z.infer<typeof ContactChannelTypeSchema>;
```

**Validation Rules:**
- Enums must match exactly; no string fallbacks.
- Invalid enum values trigger errors with all allowed values listed.

#### `src/content/schemas/utils.ts`

Reusable validation utilities for common patterns.

```typescript
import { z } from 'zod';

// ISO date string validation: YYYY-MM-DD
export const IsoDateStringSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in ISO YYYY-MM-DD format')
  .refine((date) => {
    const d = new Date(date + 'T00:00:00Z');
    return d instanceof Date && !isNaN(d.getTime()) && d.toISOString().startsWith(date);
  }, 'Invalid calendar date');

export type IsoDateString = z.infer<typeof IsoDateStringSchema>;

// Slug validation: lowercase, hyphens, no leading/trailing hyphens
export const SlugSchema = z
  .string()
  .min(1, 'Slug must not be empty')
  .regex(/^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$/, 'Slug must start and end with lowercase letter or number; hyphens allowed in middle')
  .toLowerCase();

// URL validation: absolute HTTPS or internal asset path starting with /
export const UrlSchema = z
  .string()
  .url('Must be an absolute HTTPS URL')
  .or(z.string().startsWith('/'));

export const HttpsUrlSchema = z
  .string()
  .url('Must be a valid URL')
  .refine((url) => url.startsWith('https://'), 'URL must use HTTPS protocol');

// Mailto validation: mailto: protocol for email, HTTPS for others
export const MailtoOrHttpsSchema = z.string().or(HttpsUrlSchema);

// String length validation
export const NonEmptyString = z.string().min(1, 'Must not be empty');
export const TrimmedString = z.string().trim();

export const TitleSchema = z
  .string()
  .trim()
  .min(3, 'Title must be at least 3 characters')
  .max(100, 'Title must not exceed 100 characters');

export const SummarySchema = z
  .string()
  .trim()
  .min(20, 'Summary must be at least 20 characters')
  .max(280, 'Summary must not exceed 280 characters');

export const BlogTitleSchema = z
  .string()
  .trim()
  .min(5, 'Blog title must be at least 5 characters')
  .max(120, 'Blog title must not exceed 120 characters');

export const BlogSummarySchema = z
  .string()
  .trim()
  .min(20, 'Blog summary must be at least 20 characters')
  .max(300, 'Blog summary must not exceed 300 characters');
```

#### `src/content/schemas/site.ts`

SiteConfig schema with nested ContactChannel, SocialLink, and SiteProfile.

```typescript
import { z } from 'zod';
import { ContactChannelTypeSchema, HttpsUrlSchema, MailtoOrHttpsSchema } from './utils';

const ContactChannelSchema = z
  .object({
    type: ContactChannelTypeSchema,
    label: z.string().min(1, 'Label must not be empty'),
    url: z.string().refine(
      (url, ctx) => {
        if (ctx.parent.type === 'email') {
          return url.startsWith('mailto:');
        }
        return url.startsWith('https://');
      },
      'Email channels must use mailto: protocol; others must use HTTPS'
    ),
    isPrimary: z.boolean(),
  });

const SocialLinkSchema = z.object({
  label: z.string().min(1, 'Label must not be empty'),
  url: HttpsUrlSchema,
});

const SiteProfileSchema = z.object({
  name: z.string().min(1, 'Name must not be empty'),
  professionalTitle: z.string().min(1, 'Professional title must not be empty'),
  introduction: z.string().min(1, 'Introduction must not be empty'),
  location: z.string().min(1, 'Location must not be empty'),
  availableForOpportunities: z.boolean(),
});

const SiteNavigationItemSchema = z.object({
  label: z.string().min(1, 'Label must not be empty'),
  href: z.string().startsWith('/').or(HttpsUrlSchema),
});

export const SiteConfigSchema = z.object({
  siteName: z.string().min(1, 'Site name must not be empty'),
  siteUrl: HttpsUrlSchema.or(z.string().startsWith('/')),
  profile: SiteProfileSchema,
  contactChannels: z.array(ContactChannelSchema).min(1, 'At least one contact channel required'),
  socialLinks: z.array(SocialLinkSchema),
  navigation: z.array(SiteNavigationItemSchema),
});

export type SiteConfig = z.infer<typeof SiteConfigSchema>;
```

#### `src/content/schemas/project.ts`

Project schema with frontmatter validation (title, summary, slug, dates, featured count).

```typescript
import { z } from 'zod';
import {
  ProjectStatusSchema,
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
} from './utils';

const ProjectMetricsSchema = z.object({
  label: z.string().min(1),
  value: z.string().min(1),
});

export const ProjectFrontmatterSchema = z
  .object({
    title: TitleSchema,
    summary: SummarySchema,
    slug: SlugSchema,
    status: ProjectStatusSchema,
    role: z.string().min(1, 'Role must not be empty'),
    startedAt: IsoDateStringSchema,
    completedAt: IsoDateStringSchema.nullable(),
    technologies: z.array(z.string().min(1)).min(1, 'At least 1 technology required'),
    tags: z.array(z.string()),
    repositoryUrl: HttpsUrlSchema.nullable(),
    liveDemoUrl: HttpsUrlSchema.nullable(),
    documentationUrl: HttpsUrlSchema.nullable(),
    featured: z.boolean(),
    displayOrder: z.number().int().non_negative(),
    metrics: z.array(ProjectMetricsSchema),
  })
  .refine(
    (data) => !data.completedAt || data.startedAt <= data.completedAt,
    'startedAt must not be later than completedAt'
  )
  .refine(
    (data) => !data.featured || data.displayOrder !== undefined,
    'Featured projects must have displayOrder'
  );

export const ProjectSchema = ProjectFrontmatterSchema.extend({
  documentation: z.string().min(1, 'Project documentation required'),
}).refine(
  (data) => /<h2/i.test(data.documentation),
  'Project documentation must contain at least one ## heading'
);

export type Project = z.infer<typeof ProjectSchema>;
export type ProjectFrontmatter = z.infer<typeof ProjectFrontmatterSchema>;
```

#### `src/content/schemas/certification.ts`

Certification schema with category enum and date validation.

```typescript
import { z } from 'zod';
import {
  CertificationCategorySchema,
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  TitleSchema,
} from './utils';

export const CertificationFrontmatterSchema = z
  .object({
    title: TitleSchema,
    slug: SlugSchema,
    issuer: z.string().min(1, 'Issuer must not be empty'),
    category: CertificationCategorySchema,
    issuedAt: IsoDateStringSchema,
    expiresAt: IsoDateStringSchema.nullable(),
    credentialId: z.string().nullable(),
    verificationUrl: HttpsUrlSchema.nullable(),
    badgeImageUrl: z.string().nullable(),
    badgeImageAlt: z.string().nullable(),
    displayOrder: z.number().int().non_negative(),
  })
  .refine(
    (data) => !data.expiresAt || data.issuedAt <= data.expiresAt,
    'expiresAt must not be earlier than issuedAt'
  )
  .refine(
    (data) => (data.badgeImageUrl && data.badgeImageAlt) || (!data.badgeImageUrl && !data.badgeImageAlt),
    'badgeImageUrl and badgeImageAlt must both be present or both be absent'
  );

export const CertificationSchema = CertificationFrontmatterSchema.extend({
  content: z.string(),
});

export type Certification = z.infer<typeof CertificationSchema>;
export type CertificationFrontmatter = z.infer<typeof CertificationFrontmatterSchema>;
```

#### `src/content/schemas/blog-post.ts`

BlogPost schema with event metadata and draft flag.

```typescript
import { z } from 'zod';
import {
  EventTypeSchema,
  IsoDateStringSchema,
  SlugSchema,
  BlogTitleSchema,
  BlogSummarySchema,
  HttpsUrlSchema,
} from './utils';

export const BlogPostFrontmatterSchema = z
  .object({
    title: BlogTitleSchema,
    slug: SlugSchema,
    summary: BlogSummarySchema,
    publishedAt: IsoDateStringSchema,
    updatedAt: IsoDateStringSchema.nullable(),
    eventType: EventTypeSchema,
    eventName: z.string().nullable(),
    eventDate: IsoDateStringSchema.nullable(),
    eventLocation: z.string().nullable(),
    eventUrl: HttpsUrlSchema.nullable(),
    tags: z.array(z.string()),
    readingTimeMinutes: z.number().int().min(1).max(60),
    draft: z.boolean().default(false),
  })
  .refine(
    (data) => !data.eventDate || data.eventDate <= data.publishedAt,
    'eventDate must not be later than publishedAt'
  );

export const BlogPostSchema = BlogPostFrontmatterSchema.extend({
  content: z.string(),
});

export type BlogPost = z.infer<typeof BlogPostSchema>;
export type BlogPostFrontmatter = z.infer<typeof BlogPostFrontmatterSchema>;
```

### 3.2 Loader Functions

#### `src/content/loaders/site.ts`

Loads global SiteConfig from `content/site.json`.

```typescript
import fs from 'fs/promises';
import path from 'path';
import { SiteConfigSchema, type SiteConfig } from '../schemas/site';

const SITE_CONFIG_PATH = path.join(process.cwd(), 'content', 'site.json');

export async function getSiteConfig(): Promise<SiteConfig> {
  try {
    const content = await fs.readFile(SITE_CONFIG_PATH, 'utf-8');
    const parsed = JSON.parse(content);
    const validated = SiteConfigSchema.parse(parsed);
    return validated;
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(`${SITE_CONFIG_PATH}: JSON parse error: ${error.message}`);
    }
    if (error instanceof z.ZodError) {
      const issue = error.errors[0];
      throw new Error(
        `${SITE_CONFIG_PATH}: Validation failed at '${issue.path.join('.')}'. ` +
        `Expected ${issue.code}, received: ${JSON.stringify(issue.received)}`
      );
    }
    throw new Error(`${SITE_CONFIG_PATH}: File not found or unreadable`);
  }
}
```

#### `src/content/loaders/projects.ts`

Loads all projects from `content/projects/*.mdx` and optionally retrieves by slug.

```typescript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { ProjectSchema, ProjectFrontmatterSchema, type Project } from '../schemas/project';
import { renderMarkdown } from '../markdown/render';

const PROJECTS_DIR = path.join(process.cwd(), 'content', 'projects');

export async function getProjects(): Promise<Project[]> {
  try {
    const files = await fs.readdir(PROJECTS_DIR);
    const mdxFiles = files.filter((f) => f.endsWith('.mdx'));

    const projects: Project[] = [];
    const errors: string[] = [];

    for (const file of mdxFiles) {
      try {
        const filePath = path.join(PROJECTS_DIR, file);
        const content = await fs.readFile(filePath, 'utf-8');
        const { data, content: markdown } = matter(content);

        // Validate frontmatter
        const validated = ProjectFrontmatterSchema.parse(data);

        // Render markdown to HTML
        const documentation = await renderMarkdown(markdown);

        // Combine and validate full project
        const project = ProjectSchema.parse({
          ...validated,
          documentation,
        });

        projects.push(project);
      } catch (error) {
        const filePath = path.join(PROJECTS_DIR, file);
        if (error instanceof z.ZodError) {
          const issue = error.errors[0];
          errors.push(
            `${filePath}: Validation failed at '${issue.path.join('.')}'. ` +
            `Expected ${issue.code}, received: ${JSON.stringify(issue.received)}`
          );
        } else {
          errors.push(`${filePath}: ${error instanceof Error ? error.message : String(error)}`);
        }
      }
    }

    if (errors.length > 0) {
      throw new Error(`Content validation failed:\n${errors.join('\n')}`);
    }

    // Sort: displayOrder ascending, then startedAt descending
    return projects.sort((a, b) => {
      if (a.displayOrder !== b.displayOrder) {
        return a.displayOrder - b.displayOrder;
      }
      return b.startedAt.localeCompare(a.startedAt);
    });
  } catch (error) {
    throw error instanceof Error ? error : new Error(String(error));
  }
}

export async function getProjectBySlug(slug: string): Promise<Project | null> {
  const projects = await getProjects();
  return projects.find((p) => p.slug === slug) || null;
}

// Collection-level validation: featured count <= 3
export async function validateFeaturedCount(): Promise<void> {
  const projects = await getProjects();
  const featured = projects.filter((p) => p.featured);

  if (featured.length > 3) {
    const fileList = featured.map((p) => `  - ${p.slug} (content/projects/${p.slug}.mdx)`).join('\n');
    throw new Error(
      `Featured project count exceeds 3 (current: ${featured.length}):\n${fileList}`
    );
  }
}
```

#### `src/content/loaders/certifications.ts`

Loads all certifications from `content/certifications/*.mdx`.

```typescript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { CertificationSchema, CertificationFrontmatterSchema, type Certification } from '../schemas/certification';
import { renderMarkdown } from '../markdown/render';

const CERTIFICATIONS_DIR = path.join(process.cwd(), 'content', 'certifications');

export async function getCertifications(): Promise<Certification[]> {
  try {
    const files = await fs.readdir(CERTIFICATIONS_DIR);
    const mdxFiles = files.filter((f) => f.endsWith('.mdx'));

    const certifications: Certification[] = [];
    const errors: string[] = [];

    for (const file of mdxFiles) {
      try {
        const filePath = path.join(CERTIFICATIONS_DIR, file);
        const content = await fs.readFile(filePath, 'utf-8');
        const { data, content: markdown } = matter(content);

        const validated = CertificationFrontmatterSchema.parse(data);
        const renderedContent = await renderMarkdown(markdown);

        const certification = CertificationSchema.parse({
          ...validated,
          content: renderedContent,
        });

        certifications.push(certification);
      } catch (error) {
        const filePath = path.join(CERTIFICATIONS_DIR, file);
        if (error instanceof z.ZodError) {
          const issue = error.errors[0];
          errors.push(`${filePath}: Field '${issue.path.join('.')}': ${issue.message}`);
        } else {
          errors.push(`${filePath}: ${error instanceof Error ? error.message : String(error)}`);
        }
      }
    }

    if (errors.length > 0) {
      throw new Error(`Content validation failed:\n${errors.join('\n')}`);
    }

    return certifications.sort((a, b) => a.displayOrder - b.displayOrder);
  } catch (error) {
    throw error instanceof Error ? error : new Error(String(error));
  }
}
```

#### `src/content/loaders/blog.ts`

Loads all blog posts from `content/blog/*.mdx`, excluding draft posts.

```typescript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { BlogPostSchema, BlogPostFrontmatterSchema, type BlogPost } from '../schemas/blog-post';
import { renderMarkdown } from '../markdown/render';

const BLOG_DIR = path.join(process.cwd(), 'content', 'blog');

export async function getBlogPosts(): Promise<BlogPost[]> {
  try {
    const files = await fs.readdir(BLOG_DIR);
    const mdxFiles = files.filter((f) => f.endsWith('.mdx'));

    const posts: BlogPost[] = [];
    const errors: string[] = [];

    for (const file of mdxFiles) {
      try {
        const filePath = path.join(BLOG_DIR, file);
        const content = await fs.readFile(filePath, 'utf-8');
        const { data, content: markdown } = matter(content);

        const validated = BlogPostFrontmatterSchema.parse(data);

        // Skip draft posts
        if (validated.draft) {
          continue;
        }

        const renderedContent = await renderMarkdown(markdown);

        const post = BlogPostSchema.parse({
          ...validated,
          content: renderedContent,
        });

        posts.push(post);
      } catch (error) {
        // Only report errors for non-draft posts
        const filePath = path.join(BLOG_DIR, file);
        if (error instanceof z.ZodError) {
          const issue = error.errors[0];
          errors.push(`${filePath}: Field '${issue.path.join('.')}': ${issue.message}`);
        } else {
          errors.push(`${filePath}: ${error instanceof Error ? error.message : String(error)}`);
        }
      }
    }

    if (errors.length > 0) {
      throw new Error(`Content validation failed:\n${errors.join('\n')}`);
    }

    // Sort: publishedAt descending (most recent first)
    return posts.sort((a, b) => b.publishedAt.localeCompare(a.publishedAt));
  } catch (error) {
    throw error instanceof Error ? error : new Error(String(error));
  }
}

export async function getBlogPostBySlug(slug: string): Promise<BlogPost | null> {
  const posts = await getBlogPosts();
  return posts.find((p) => p.slug === slug) || null;
}
```

### 3.3 Markdown Rendering Pipeline

#### `src/content/markdown/render.ts`

Converts Markdown to HTML with syntax highlighting and XSS protection.

```typescript
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeHighlight from 'rehype-highlight';
import rehypeSanitize from 'rehype-sanitize';
import rehypeStringify from 'rehype-stringify';
import { visit } from 'unist-util-visit';

// Custom plugin: add rel="noopener noreferrer" to external links
function externalLinkPlugin() {
  return (tree: any) => {
    visit(tree, 'element', (node) => {
      if (node.tagName === 'a' && node.properties.href) {
        const href = String(node.properties.href);
        if (href.startsWith('http://') || href.startsWith('https://')) {
          node.properties.rel = ['noopener', 'noreferrer'];
        }
      }
    });
  };
}

export async function renderMarkdown(markdown: string): Promise<string> {
  try {
    const processor = unified()
      .use(remarkParse)
      .use(remarkGfm)
      .use(remarkRehype)
      .use(rehypeHighlight)
      .use(externalLinkPlugin)
      .use(rehypeSanitize)
      .use(rehypeStringify);

    const html = String(await processor.process(markdown));
    return html;
  } catch (error) {
    throw new Error(`Markdown rendering failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}
```

### 3.4 Error Handling & Validation

#### `src/content/errors/handler.ts`

Centralized error formatting with file path, field, and remediation guidance.

```typescript
import { ZodError } from 'zod';

export interface ValidationError {
  filePath: string;
  field: string;
  message: string;
  received?: unknown;
  expected?: string;
}

export function formatZodError(error: ZodError, filePath: string): ValidationError[] {
  return error.errors.map((issue) => ({
    filePath,
    field: issue.path.join('.') || 'root',
    message: issue.message,
    expected: issue.code,
    received: issue.received,
  }));
}

export function formatValidationError(filePath: string, message: string): ValidationError {
  return {
    filePath,
    field: 'unknown',
    message,
  };
}

export function renderErrorReport(errors: ValidationError[]): string {
  return errors
    .map(
      (err) =>
        `${err.filePath}\n` +
        `  Field: ${err.field}\n` +
        `  Issue: ${err.message}\n` +
        (err.expected ? `  Expected: ${err.expected}\n` : '') +
        (err.received !== undefined ? `  Received: ${JSON.stringify(err.received)}\n` : '')
    )
    .join('\n');
}
```

---

## Data Models

### 4.1 TypeScript Type Contracts (Inferred from Zod)

All TypeScript types are derived from Zod schemas using `z.infer<>`. No duplicate interface definitions exist.

```typescript
// src/types/content.ts (or equivalent)
export type {
  SiteConfig,
  SiteProfile,
  ContactChannel,
  ContactChannelType,
  SocialLink,
  SiteNavigationItem,
} from '../content/schemas/site';

export type {
  Project,
  ProjectFrontmatter,
  ProjectStatus,
  ProjectMetrics,
} from '../content/schemas/project';

export type {
  Certification,
  CertificationFrontmatter,
  CertificationCategory,
} from '../content/schemas/certification';

export type {
  BlogPost,
  BlogPostFrontmatter,
  EventType,
} from '../content/schemas/blog-post';

export type {
  ProjectStatus,
  CertificationCategory,
  EventType,
  ContactChannelType,
  IsoDateString,
} from '../content/schemas/utils';
```

### 4.2 Content Entity Relationships

```
SiteConfig
  ├─ profile: SiteProfile
  ├─ contactChannels: ContactChannel[]
  ├─ socialLinks: SocialLink[]
  └─ navigation: SiteNavigationItem[]

Project
  ├─ slug: string (unique within projects collection)
  ├─ status: ProjectStatus enum
  ├─ technologies: string[]
  ├─ documentation: string (HTML)
  └─ featured: boolean

Certification
  ├─ slug: string (unique within certifications collection)
  ├─ category: CertificationCategory enum
  ├─ badgeImageUrl: string | null (paired with badgeImageAlt)
  └─ content: string (HTML)

BlogPost
  ├─ slug: string (unique within blog collection)
  ├─ eventType: EventType enum
  ├─ draft: boolean (draft posts excluded from getBlogPosts())
  └─ content: string (HTML)
```

---

## Build-Time Validation Hooks

### 5.1 Integration with Next.js Build Pipeline

M2 validation is integrated into the Next.js build process via a custom hook in `next.config.ts` or a separate validation script invoked during build.

#### Approach 1: next.config.ts Hook (Recommended)

```typescript
// next.config.ts
import type { NextConfig } from 'next';
import { getProjects, validateFeaturedCount } from './src/content/loaders/projects';
import { getCertifications } from './src/content/loaders/certifications';
import { getBlogPosts } from './src/content/loaders/blog';
import { getSiteConfig } from './src/content/loaders/site';

const config: NextConfig = {
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Run content validation on server-side build
      config.plugins.push({
        apply: (compiler: any) => {
          compiler.hooks.beforeCompile.tapPromise('ContentValidation', async () => {
            try {
              console.log('🔍 Validating M2 content...');
              await getSiteConfig();
              await getProjects();
              await validateFeaturedCount();
              await getCertifications();
              await getBlogPosts();
              console.log('✅ All content validated successfully.');
            } catch (error) {
              console.error('❌ Content validation failed:');
              console.error(error instanceof Error ? error.message : String(error));
              process.exit(1);
            }
          });
        },
      });
    }
    return config;
  },
};

export default config;
```

#### Approach 2: Separate Validation Script (Alternative)

Create `scripts/validate-content.ts` and invoke in `package.json` during build:

```json
{
  "scripts": {
    "validate-content": "tsx scripts/validate-content.ts",
    "build": "npm run validate-content && next build"
  }
}
```

### 5.2 Validation Execution Flow

```
npm run build
    |
    v
validate-content script / webpack hook
    |
    +-- getSiteConfig() ──> Validate SiteConfig schema
    |
    +-- getProjects() ──> Validate all projects, featured count, slug uniqueness
    |
    +-- getCertifications() ──> Validate all certifications
    |
    +-- getBlogPosts() ──> Validate all blog posts, exclude drafts
    |
    v
All errors aggregated, reported with file paths and remediation
    |
    +-- Pass: proceed to next build stage
    |
    +-- Fail: exit with non-zero code, halt build
```

---

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Enum Schema Validation

**For any** enum value provided to an enum schema (ProjectStatus, CertificationCategory, EventType, ContactChannelType), the schema SHALL either accept the value if it is in the allowed set, or reject with an error message that lists all allowed values and the received value.

**Validates:** Requirements 1.1–1.6

### Property 2: Slug Format and Uniqueness

**For any** slug provided in project, certification, or blog frontmatter, the schema SHALL enforce lowercase letters, numbers, and hyphens only; no leading or trailing hyphens. Additionally, within each collection (projects, certifications, blog), no two items may have the same slug.

**Validates:** Requirements 9.1–9.5

### Property 3: ISO Date Format and Ordering

**For any** ISO date string provided in content, the schema SHALL enforce the format `YYYY-MM-DD` and verify it represents a valid calendar date. When two dates have an ordering constraint (e.g., `startedAt` ≤ `completedAt`), the schema SHALL enforce the constraint or reject with an error indicating the violated fields.

**Validates:** Requirements 10.1–10.4

### Property 4: URL Protocol Enforcement

**For any** required URL field (e.g., `siteUrl`, `repositoryUrl`), the schema SHALL enforce absolute HTTPS URL format. For optional URL fields, the schema SHALL accept `null` or empty string without error. For `mailto:` protocol, the schema SHALL permit it only for email contact channels and reject for other channel types.

**Validates:** Requirements 11.1–11.5

### Property 5: Featured Project Count Constraint

**For any** collection of projects loaded via `getProjects()`, the total count of projects where `featured: true` SHALL not exceed 3. If the count is exceeded, the validation SHALL fail with an error listing all featured projects and the current count.

**Validates:** Requirements 13.1–13.5

### Property 6: Draft Post Exclusion

**For any** blog post with `draft: true`, the post SHALL be excluded from the array returned by `getBlogPosts()`, excluded from static route generation, and return `null` when queried via `getBlogPostBySlug()`. Draft posts with `draft: false` SHALL be included in the returned array, sorted by `publishedAt` descending.

**Validates:** Requirements 12.1–12.5

### Property 7: Schema Type Inference

**For any** Zod schema defined in `src/content/schemas/`, the TypeScript type derived via `z.infer<typeof Schema>` SHALL be the exclusive source of truth for that type throughout the application. No duplicate interface or type definition SHALL exist; all downstream code SHALL use the inferred type.

**Validates:** Requirements 15.1–15.5

### Property 8: Markdown Rendering Safety

**For any** Markdown content rendered via `renderMarkdown()`, the output HTML SHALL contain no unescaped script tags, event handlers, or executable code. External links SHALL contain `rel="noopener noreferrer"` attributes. Code blocks SHALL be highlighted using an approved syntax-highlighting library.

**Validates:** Requirements 14.1–14.6

### Property 9: Build Failure on Validation Error

**For any** content file that fails schema validation during build, the build process SHALL halt with a non-zero exit code and output an error message that includes the file path, field name, expected constraint, and received value category.

**Validates:** Requirements 16.1–16.6, 17.1–17.4

### Property 10: Type-Safe Loader Functions

**For any** loader function (`getSiteConfig()`, `getProjects()`, `getCertifications()`, `getBlogPosts()`, `getProjectBySlug()`, `getBlogPostBySlug()`), the return type SHALL be derived from the corresponding Zod schema and guaranteed to satisfy the schema. No unvalidated data SHALL be returned; all data SHALL have passed schema validation before being returned to the caller.

**Validates:** Requirements 5.1–5.5, 6.1–6.8, 7.1–7.10

---

## Error Handling

### 7.1 Error Categories

| Error Type | Cause | Example | Resolution |
| :--- | :--- | :--- | :--- |
| **File Not Found** | Content file missing | `content/site.json` does not exist | Create file with valid content |
| **Parse Error** | Invalid JSON/YAML format | `{invalid json` | Fix JSON/YAML syntax |
| **Schema Validation** | Frontmatter doesn't match schema | `title` is 2 characters (min 3) | Adjust field to match constraints |
| **Date Format** | Date not ISO format | `01/15/2026` instead of `2026-01-15` | Use ISO `YYYY-MM-DD` format |
| **Slug Conflict** | Slug duplicated within collection | Two projects with slug `my-project` | Rename one project slug |
| **Featured Count** | Too many featured projects | 4 projects with `featured: true` | Change 1+ to `featured: false` |
| **Markdown Rendering** | Markdown parsing fails | Unclosed code fence | Fix Markdown syntax |
| **URL Format** | URL not HTTPS | `http://example.com` | Use `https://` protocol |

### 7.2 Error Reporting

All validation errors include:
1. **File Path:** Full path to the offending file (e.g., `content/projects/my-project.mdx`).
2. **Field Name:** The specific field that failed validation (e.g., `title`).
3. **Expected Constraint:** What the validator expects (e.g., `minimum 3 characters`).
4. **Received Value:** The actual value provided (e.g., `received 2 characters: "ab"`).

Example error message:

```
❌ Content validation failed:

content/projects/my-project.mdx
  Field: title
  Issue: String must contain at least 3 character(s)
  Expected: string
  Received: "ab"

content/blog/my-post.mdx
  Field: publishedAt
  Issue: String must match date format YYYY-MM-DD
  Expected: date
  Received: "01/15/2026"
```

---

## Testing Strategy

### 8.1 Test Coverage Areas

M2 testing covers:
1. **Schema Validation Tests:** Each Zod schema validates correct and incorrect input.
2. **Loader Function Tests:** Each loader returns expected types and handles errors.
3. **Validation Rule Tests:** Slug format, date ordering, URL protocol, enum values.
4. **Collection-Level Constraints:** Featured count, slug uniqueness, draft exclusion.
5. **Markdown Rendering Tests:** HTML generation, syntax highlighting, XSS prevention.
6. **Error Message Tests:** Errors include file path, field, and remediation guidance.
7. **Type Inference Tests:** TypeScript correctly infers types from Zod schemas; no `any` types.

### 8.2 Test File Structure

```
tests/
├── content-schemas.test.ts       # Schema validation tests
├── content-loaders.test.ts       # Loader function tests
├── validation-rules.test.ts      # Slug, date, URL, enum rules
├── markdown-rendering.test.ts    # Markdown to HTML conversion
├── error-handling.test.ts        # Error message format and content
└── fixtures/                      # Sample content files for testing
    ├── projects/
    ├── certifications/
    ├── blog/
    └── site.json
```

### 8.3 Example Test Cases (Using Jest/Vitest)

#### Schema Validation Test

```typescript
// tests/content-schemas.test.ts
import { ProjectFrontmatterSchema } from '../src/content/schemas/project';
import { z } from 'zod';

describe('Project Schema Validation', () => {
  it('accepts valid project frontmatter', () => {
    const valid = {
      title: 'My Project',
      summary: 'This is a comprehensive summary of my project.',
      slug: 'my-project',
      status: 'completed',
      role: 'Full-Stack Engineer',
      startedAt: '2026-01-15',
      completedAt: '2026-03-01',
      technologies: ['TypeScript', 'React'],
      tags: ['web'],
      repositoryUrl: 'https://github.com/example/repo',
      liveDemoUrl: null,
      documentationUrl: null,
      featured: true,
      displayOrder: 1,
      metrics: [],
    };
    expect(() => ProjectFrontmatterSchema.parse(valid)).not.toThrow();
  });

  it('rejects title shorter than 3 characters', () => {
    const invalid = {
      title: 'ab', // < 3 chars
      // ... rest of fields
    };
    expect(() => ProjectFrontmatterSchema.parse(invalid)).toThrow(z.ZodError);
  });

  it('rejects completedAt before startedAt', () => {
    const invalid = {
      // ... other fields
      startedAt: '2026-03-01',
      completedAt: '2026-01-15', // Before startedAt
    };
    expect(() => ProjectFrontmatterSchema.parse(invalid)).toThrow(z.ZodError);
  });
});
```

#### Loader Function Test

```typescript
// tests/content-loaders.test.ts
import { getProjects, getProjectBySlug } from '../src/content/loaders/projects';

describe('Project Loaders', () => {
  it('loads and returns all projects sorted by displayOrder', async () => {
    const projects = await getProjects();
    expect(Array.isArray(projects)).toBe(true);
    expect(projects.length).toBeGreaterThan(0);
    
    // Verify sort order
    for (let i = 1; i < projects.length; i++) {
      expect(projects[i].displayOrder).toBeGreaterThanOrEqual(projects[i - 1].displayOrder);
    }
  });

  it('returns null when slug not found', async () => {
    const project = await getProjectBySlug('nonexistent-slug');
    expect(project).toBeNull();
  });

  it('returns correct project when slug exists', async () => {
    const project = await getProjectBySlug('my-project');
    expect(project).not.toBeNull();
    expect(project?.slug).toBe('my-project');
  });
});
```

#### Error Handling Test

```typescript
// tests/error-handling.test.ts
describe('Error Message Format', () => {
  it('includes file path, field, and remediation guidance', async () => {
    // Create a project file with invalid title (< 3 chars)
    try {
      await getProjects();
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      expect(message).toContain('content/projects/');
      expect(message).toContain('title');
      expect(message).toContain('at least 3 character');
    }
  });
});
```

### 8.4 Test Execution

```bash
npm run lint              # ESLint and Prettier checks
npm run typecheck         # TypeScript strict mode checks
npm test                  # Run all tests with Jest/Vitest
npm run build             # Build with content validation
```

All tests must pass before code is merged. Test coverage must be > 80% for content modules.

---

## Integration Points

### 9.1 M2 → M3 (Routes and Components)

M3 consumes M2 loaders and types:

```typescript
// src/app/projects/page.tsx (M3 route component)
import { getProjects } from '@/content/loaders/projects';
import { Project } from '@/types/content';

export default async function ProjectsPage() {
  const projects: Project[] = await getProjects();
  return (
    // Render project list using projects array
  );
}
```

### 9.2 Static Route Generation

M3 routes generate static pages for each slug using M2 loaders:

```typescript
// src/app/projects/[slug]/page.tsx (M3 route with dynamic slug)
import { getProjects, getProjectBySlug } from '@/content/loaders/projects';

export async function generateStaticParams() {
  const projects = await getProjects();
  return projects.map((p) => ({ slug: p.slug }));
}

export default async function ProjectPage({ params }: { params: { slug: string } }) {
  const project = await getProjectBySlug(params.slug);
  if (!project) {
    return notFound();
  }
  return (
    // Render project detail
  );
}
```

### 9.3 Type Re-exports

M2 types are re-exported from `src/types/content.ts` for easy consumption throughout the application.

---

## Deployment & Build Strategy

### 10.1 Build-Time Validation

Content validation occurs during `npm run build`:

1. Webpack/build plugin invokes M2 validation hooks.
2. All content is loaded, parsed, and validated.
3. Errors are reported with file paths and remediation.
4. Build halts if any errors occur.
5. Build proceeds to static generation if validation passes.

### 10.2 Error Recovery

If the build fails due to content errors:

1. Developer fixes content file(s) per error message.
2. Developer re-runs `npm run build`.
3. Build succeeds if all content is now valid.

### 10.3 Deployment to Vercel

After build succeeds locally, deployment to Vercel proceeds with the validated, type-safe content pipeline.

---

## Rollout Plan

### Phase 1: Schema Definition (Week 1)
- Define all Zod schemas in `src/content/schemas/`.
- Verify schemas via `npm run typecheck`.
- No content validation yet; schemas await loader implementation.

### Phase 2: Loader Implementation (Week 2)
- Implement loaders for SiteConfig, Projects, Certifications, BlogPosts.
- Test loaders with seed content.
- Verify return types are derived from Zod via `z.infer<>`.

### Phase 3: Markdown Rendering (Week 2–3)
- Implement Markdown rendering pipeline with remark/rehype.
- Test syntax highlighting and XSS protection.
- Integrate rendered HTML into loader output.

### Phase 4: Build Integration (Week 3)
- Integrate validation hooks into Next.js build pipeline.
- Test build failure and recovery scenarios.
- Verify errors include file path and remediation.

### Phase 5: Testing & Documentation (Week 4)
- Write comprehensive test suite (> 80% coverage).
- Document error messages and troubleshooting guide.
- Prepare seed content for M3 component integration.

---

## Success Metrics

✓ All 20 M2 requirements satisfied.  
✓ 100% of content validation rules enforced at build time.  
✓ Build fails with descriptive errors when content is invalid.  
✓ No TypeScript type definitions duplicated; all derived from Zod.  
✓ Test coverage > 80% for content modules.  
✓ All tests pass: `npm run lint && npm run typecheck && npm test && npm run build`.

---

## References

- **AGENTS.md:** Content schemas, directory taxonomy, validation rules, TypeScript contracts.
- **TRD.md:** Technical requirements, build-time validation, Markdown rendering.
- **PRD.md:** Product scope, user goals, success metrics.
- **requirements.md:** M2 EARS-formatted requirements (20 requirements).
