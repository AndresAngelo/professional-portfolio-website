# M2.G1: Zod Schema Infrastructure Setup

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the directory structure, base files, and foundation validators for the content schema module. This includes implementing reusable Zod validation utilities for common patterns (ISO date strings, regex-based URL-safe slugs, HTTPS/asset URLs, string boundary lengths), initializing test fixtures, configuring centralized error structures, and establishing clean TypeScript barrel re-exports without type duplication.

## Goal Success Criteria

- ✓ Directory structure established under `src/content/` (`schemas/`, `loaders/`, `markdown/`, `errors/`)
- ✓ Reusable primitive validation rules implemented in `src/content/schemas/utils.ts`
- ✓ Centralized error handling interface and formatter implemented in `src/content/errors/handler.ts`
- ✓ Test fixture seed files authored in `tests/fixtures/` covering all 4 content types
- ✓ `src/types/content.ts` created as the canonical type barrel deriving types exclusively via `z.infer<>`
- ✓ `npm run typecheck` passes with zero errors under TypeScript strict mode

## Prerequisites

- Milestone 1 completed (`m1-baseline` tagged, clean working tree)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `zod` installed in `dependencies` (`^3.23.0`)
- `vitest` installed in `devDependencies`

---

## Tasks

### M2.G1.T1: Create Content Infrastructure Directory Tree

**Objective:** Create the required directories under `src/content/` to support schemas, loaders, markdown rendering, and error formatting.

**Acceptance Criteria:**
- ✓ Directory `src/content/schemas` exists
- ✓ Directory `src/content/loaders` exists
- ✓ Directory `src/content/markdown` exists
- ✓ Directory `src/content/errors` exists
- ✓ Directories are created without disturbing existing layout or app files

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Execute the following PowerShell script:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$dirs = @(
    "src\content\schemas",
    "src\content\loaders",
    "src\content\markdown",
    "src\content\errors"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$valid = (Test-Path "src\content\schemas") -and (Test-Path "src\content\loaders") -and (Test-Path "src\content\markdown") -and (Test-Path "src\content\errors")
if ($valid) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 20.1

---

### M2.G1.T2: Implement Reusable Zod Validation Utilities (`src/content/schemas/utils.ts`)

**Objective:** Implement baseline primitive validators for ISO dates, URL-safe slugs, secure HTTPS URLs, and bounded string fields in `src/content/schemas/utils.ts`.

**Acceptance Criteria:**
- ✓ `src/content/schemas/utils.ts` exists and compiles
- ✓ `IsoDateStringSchema` validates `YYYY-MM-DD` and checks calendar validity via `Date`
- ✓ `SlugSchema` enforces lowercase alphanumeric characters and internal hyphens only (no leading/trailing hyphens)
- ✓ `HttpsUrlSchema` validates URLs and mandates `https://` protocol
- ✓ `TitleSchema`, `SummarySchema`, `BlogTitleSchema`, and `BlogSummarySchema` enforce length limits per `AGENTS.md` Section 5

**Prerequisites:**
- M2.G1.T1 completed
- Target file: `src/content/schemas/utils.ts`

**Implementation Details:**

Write the utility module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { z } from 'zod';

/**
 * ISO date string validation: strictly enforces YYYY-MM-DD format
 * and validates that the date actually exists on the calendar.
 */
export const IsoDateStringSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in ISO YYYY-MM-DD format')
  .refine((date) => {
    const d = new Date(`${date}T00:00:00Z`);
    return d instanceof Date && !isNaN(d.getTime()) && d.toISOString().startsWith(date);
  }, 'Invalid calendar date');

export type IsoDateString = z.infer<typeof IsoDateStringSchema>;

/**
 * Slug validation: lowercase letters, numbers, and hyphens.
 * Must not start or end with a hyphen.
 */
export const SlugSchema = z
  .string()
  .min(1, 'Slug must not be empty')
  .regex(
    /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
    'Slug must contain only lowercase alphanumeric characters and hyphens, without leading or trailing hyphens'
  )
  .toLowerCase();

/**
 * Absolute HTTPS URL validation.
 */
export const HttpsUrlSchema = z
  .string()
  .url('Must be a valid URL')
  .refine((url) => url.startsWith('https://'), 'URL must use HTTPS protocol');

/**
 * General URL or internal asset path validation.
 */
export const UrlOrAssetPathSchema = z
  .string()
  .refine(
    (val) => val.startsWith('/') || (val.startsWith('https://') && z.string().url().safeParse(val).success),
    'Must be an absolute HTTPS URL or an internal asset path starting with /'
  );

/**
 * Project title and summary boundaries per AGENTS.md 5.2.
 */
export const TitleSchema = z
  .string()
  .trim()
  .min(3, 'Title must contain at least 3 characters after trimming')
  .max(100, 'Title must not exceed 100 characters after trimming');

export const SummarySchema = z
  .string()
  .trim()
  .min(20, 'Summary must contain at least 20 characters after trimming')
  .max(280, 'Summary must not exceed 280 characters after trimming');

/**
 * Blog title and summary boundaries per AGENTS.md 5.4.
 */
export const BlogTitleSchema = z
  .string()
  .trim()
  .min(5, 'Blog title must contain at least 5 characters after trimming')
  .max(120, 'Blog title must not exceed 120 characters after trimming');

export const BlogSummarySchema = z
  .string()
  .trim()
  .min(20, 'Blog summary must contain at least 20 characters after trimming')
  .max(300, 'Blog summary must not exceed 300 characters after trimming');
'@ | Set-Content "src\content\schemas\utils.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/schemas/utils.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 10.1, Req 10.3, Req 11.1, Req 11.3

---

### M2.G1.T3: Implement Centralized Validation Error Handler (`src/content/errors/handler.ts`)

**Objective:** Author error reporting structures in `src/content/errors/handler.ts` to format Zod validation failures into descriptive, file-path-aware messages matching `AGENTS.md` Rule 5.1.10.

**Acceptance Criteria:**
- ✓ `ValidationError` interface defines `filePath`, `field`, `message`, `expected`, and `received`
- ✓ `formatZodError` maps Zod issues into structured `ValidationError` arrays
- ✓ `renderErrorReport` produces multi-line human-readable error output including file path and field context
- ✓ File compiles with zero implicit `any` types

**Prerequisites:**
- M2.G1.T1 completed
- Target file: `src/content/errors/handler.ts`

**Implementation Details:**

Write the error handler module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { ZodError } from 'zod';

export interface ValidationError {
  filePath: string;
  field: string;
  message: string;
  received?: unknown;
  expected?: string;
}

/**
 * Extracts structured ValidationError objects from a raw ZodError.
 */
export function formatZodError(error: ZodError, filePath: string): ValidationError[] {
  return error.errors.map((issue) => ({
    filePath,
    field: issue.path.length > 0 ? issue.path.join('.') : 'root',
    message: issue.message,
    expected: issue.code,
    received: 'received' in issue ? (issue as unknown as { received: unknown }).received : undefined,
  }));
}

/**
 * Creates a single formatted ValidationError from an arbitrary error message.
 */
export function formatValidationError(filePath: string, message: string, field = 'root'): ValidationError {
  return {
    filePath,
    field,
    message,
  };
}

/**
 * Renders a collection of ValidationErrors into a clear, actionable CLI report.
 */
export function renderErrorReport(errors: ValidationError[]): string {
  if (errors.length === 0) {
    return '';
  }

  return errors
    .map(
      (err) =>
        `File: ${err.filePath}\n` +
        `  Field:    ${err.field}\n` +
        `  Issue:    ${err.message}\n` +
        (err.expected ? `  Expected: ${err.expected}\n` : '') +
        (err.received !== undefined ? `  Received: ${JSON.stringify(err.received)}\n` : '')
    )
    .join('\n');
}
'@ | Set-Content "src\content\errors\handler.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/errors/handler.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.3, Req 17.1, Req 17.2

---

### M2.G1.T4: Create Test Fixtures Directory and Seed `tests/fixtures/site.json`

**Objective:** Create the `tests/fixtures/` hierarchy and add a verified, compliant `site.json` fixture matching `AGENTS.md` Section 4.3.

**Acceptance Criteria:**
- ✓ Directory `tests/fixtures` exists
- ✓ File `tests/fixtures/site.json` exists
- ✓ File contains valid profile, contact channels with `mailto:` for email, valid HTTPS social links, and navigation
- ✓ JSON parses cleanly

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create fixture file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures")) {
    New-Item -ItemType Directory -Path "tests\fixtures" -Force | Out-Null
}

@'
{
  "siteName": "Angelo Andres",
  "siteUrl": "https://example.vercel.app",
  "profile": {
    "name": "Angelo Andres",
    "professionalTitle": "Pipeline Lead & Specification Architect",
    "introduction": "I build specification-driven software and AI engineering workflows.",
    "location": "Taguig, National Capital Region, PH",
    "availableForOpportunities": true
  },
  "contactChannels": [
    {
      "type": "email",
      "label": "Email Angelo",
      "url": "mailto:hello@example.com",
      "isPrimary": true
    }
  ],
  "socialLinks": [
    {
      "label": "GitHub",
      "url": "https://github.com/example"
    }
  ],
  "navigation": [
    { "label": "Home", "href": "/" },
    { "label": "Projects", "href": "/projects" },
    { "label": "Certifications", "href": "/certifications" },
    { "label": "Blog", "href": "/blog" }
  ]
}
'@ | Set-Content "tests\fixtures\site.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
try {
    $null = Get-Content "tests\fixtures\site.json" -Raw | ConvertFrom-Json
    "PASS"
} catch {
    "FAIL"
}
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 18.1, Req 18.4

---

### M2.G1.T5: Create Project Test Fixture (`tests/fixtures/projects/valid-project.mdx`)

**Objective:** Create `tests/fixtures/projects/valid-project.mdx` containing valid frontmatter and markdown documentation containing an `##` heading.

**Acceptance Criteria:**
- ✓ Directory `tests/fixtures/projects` exists
- ✓ File `tests/fixtures/projects/valid-project.mdx` exists
- ✓ Frontmatter contains title (3–100 chars), summary (20–280 chars), valid slug, status, role, startedAt, technologies, tags, displayOrder, metrics
- ✓ Markdown body contains at least one `##` heading per `AGENTS.md` 5.2

**Prerequisites:**
- M2.G1.T4 completed

**Implementation Details:**

Write the project fixture using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures\projects")) {
    New-Item -ItemType Directory -Path "tests\fixtures\projects" -Force | Out-Null
}

@'---
title: "Example Portfolio Project"
summary: "A concise explanation of the problem, solution, and outcome within character limits."
slug: "example-project"
status: "completed"
role: "Full-Stack Engineer"
startedAt: "2026-01-15"
completedAt: "2026-03-01"
technologies:
  - "Next.js"
  - "TypeScript"
  - "Tailwind CSS"
tags:
  - "web"
  - "portfolio"
repositoryUrl: "https://github.com/example/repository"
liveDemoUrl: null
documentationUrl: null
featured: true
displayOrder: 1
metrics:
  - label: "Build time"
    value: "Under 3 minutes"
---

## Build Documentation

Detailed engineering breakdown and architectural decisions.
'@ | Set-Content "tests\fixtures\projects\valid-project.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$hasFile = Test-Path "tests\fixtures\projects\valid-project.mdx"
$hasHeading = (Get-Content "tests\fixtures\projects\valid-project.mdx" -Raw) -match "## Build Documentation"
if ($hasFile -and $hasHeading) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.5, Req 18.1, Req 18.4

---

### M2.G1.T6: Create Certification Test Fixture (`tests/fixtures/certifications/valid-certification.mdx`)

**Objective:** Create `tests/fixtures/certifications/valid-certification.mdx` conforming to `AGENTS.md` Section 4.3 and 5.3.

**Acceptance Criteria:**
- ✓ Directory `tests/fixtures/certifications` exists
- ✓ File `tests/fixtures/certifications/valid-certification.mdx` exists
- ✓ Frontmatter contains title, slug, issuer, category, issuedAt, expiresAt (or null), credentialId, verificationUrl, badgeImageUrl, badgeImageAlt, displayOrder
- ✓ Badge image and alt text are paired

**Prerequisites:**
- M2.G1.T4 completed

**Implementation Details:**

Write the certification fixture using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures\certifications")) {
    New-Item -ItemType Directory -Path "tests\fixtures\certifications" -Force | Out-Null
}

@'---
title: "Example Certification"
slug: "example-certification"
issuer: "Example Issuer"
category: "cloud"
issuedAt: "2026-02-01"
expiresAt: null
credentialId: "EXAMPLE-123"
verificationUrl: "https://example.com/verify/example-123"
badgeImageUrl: "/images/certifications/example-badge.png"
badgeImageAlt: "Example Certification badge"
displayOrder: 1
---

Supporting context and credential verification notes.
'@ | Set-Content "tests\fixtures\certifications\valid-certification.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$hasFile = Test-Path "tests\fixtures\certifications\valid-certification.mdx"
if ($hasFile) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.4, Req 18.1, Req 18.4

---

### M2.G1.T7: Create Blog Post Test Fixture (`tests/fixtures/blog/valid-blog-post.mdx`)

**Objective:** Create `tests/fixtures/blog/valid-blog-post.mdx` meeting all blog constraints from `AGENTS.md` Section 4.3 and 5.4.

**Acceptance Criteria:**
- ✓ Directory `tests/fixtures/blog` exists
- ✓ File `tests/fixtures/blog/valid-blog-post.mdx` exists
- ✓ Frontmatter contains title (5–120 chars), slug, summary (20–300 chars), publishedAt, eventType, tags, readingTimeMinutes (1–60), draft: false
- ✓ Optional eventDate is on or before publishedAt

**Prerequisites:**
- M2.G1.T4 completed

**Implementation Details:**

Write the blog fixture using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures\blog")) {
    New-Item -ItemType Directory -Path "tests\fixtures\blog" -Force | Out-Null
}

@'---
title: "Example Meetup Reflection"
slug: "example-meetup"
summary: "A short summary of the event and key takeaway meeting minimum requirements."
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

Post content describing participation, learnings, and engineering outcomes.
'@ | Set-Content "tests\fixtures\blog\valid-blog-post.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$hasFile = Test-Path "tests\fixtures\blog\valid-blog-post.mdx"
if ($hasFile) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.6, Req 4.7, Req 18.1, Req 18.4

---

### M2.G1.T8: Author Unit Tests for Primitive Validators (`tests/unit/schemas/utils.test.ts`)

**Objective:** Implement a Vitest test suite testing `IsoDateStringSchema`, `SlugSchema`, `HttpsUrlSchema`, and string length validators.

**Acceptance Criteria:**
- ✓ Tests valid and invalid ISO calendar dates (rejects leap-year violations like 2026-02-30)
- ✓ Tests valid slugs, rejects uppercase, rejects leading/trailing hyphens, rejects special chars
- ✓ Tests HTTPS enforcement on URLs, rejecting `http://`
- ✓ Tests Title and Summary length boundaries

**Prerequisites:**
- M2.G1.T2 completed
- Target file: `tests/unit/schemas/utils.test.ts`

**Implementation Details:**

Create the test file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\unit\schemas")) {
    New-Item -ItemType Directory -Path "tests\unit\schemas" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import {
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  TitleSchema,
  SummarySchema,
} from '@/content/schemas/utils';

describe('Primitive Validation Utilities', () => {
  describe('IsoDateStringSchema', () => {
    it('accepts valid ISO YYYY-MM-DD dates', () => {
      expect(IsoDateStringSchema.safeParse('2026-01-15').success).toBe(true);
      expect(IsoDateStringSchema.safeParse('2026-12-31').success).toBe(true);
    });

    it('rejects invalid date formats', () => {
      expect(IsoDateStringSchema.safeParse('01/15/2026').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2026-1-15').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2026/01/15').success).toBe(false);
    });

    it('rejects non-existent calendar dates', () => {
      expect(IsoDateStringSchema.safeParse('2026-02-30').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2026-13-01').success).toBe(false);
    });
  });

  describe('SlugSchema', () => {
    it('accepts valid lowercase hyphenated slugs', () => {
      expect(SlugSchema.safeParse('valid-slug').success).toBe(true);
      expect(SlugSchema.safeParse('project-123-alpha').success).toBe(true);
      expect(SlugSchema.safeParse('simple').success).toBe(true);
    });

    it('rejects slugs with leading or trailing hyphens', () => {
      expect(SlugSchema.safeParse('-invalid-slug').success).toBe(false);
      expect(SlugSchema.safeParse('invalid-slug-').success).toBe(false);
    });

    it('rejects slugs with uppercase letters, underscores, or spaces', () => {
      expect(SlugSchema.safeParse('Invalid-Slug').success).toBe(false);
      expect(SlugSchema.safeParse('invalid_slug').success).toBe(false);
      expect(SlugSchema.safeParse('invalid slug').success).toBe(false);
    });
  });

  describe('HttpsUrlSchema', () => {
    it('accepts valid HTTPS URLs', () => {
      expect(HttpsUrlSchema.safeParse('https://github.com/example').success).toBe(true);
    });

    it('rejects HTTP and non-web protocol URLs', () => {
      expect(HttpsUrlSchema.safeParse('http://example.com').success).toBe(false);
      expect(HttpsUrlSchema.safeParse('ftp://example.com').success).toBe(false);
      expect(HttpsUrlSchema.safeParse('example.com').success).toBe(false);
    });
  });

  describe('TitleSchema and SummarySchema boundaries', () => {
    it('validates project title length constraints (3-100 characters)', () => {
      expect(TitleSchema.safeParse('ab').success).toBe(false);
      expect(TitleSchema.safeParse('Valid Title').success).toBe(true);
      expect(TitleSchema.safeParse('a'.repeat(101)).success).toBe(false);
    });

    it('validates summary length constraints (20-280 characters)', () => {
      expect(SummarySchema.safeParse('Too short summary').success).toBe(false);
      expect(SummarySchema.safeParse('This is a sufficiently long summary meeting the minimum required length.').success).toBe(true);
      expect(SummarySchema.safeParse('a'.repeat(281)).success).toBe(false);
    });
  });
});
'@ | Set-Content "tests\unit\schemas\utils.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/schemas/utils.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1–9.4, Req 10.1–10.3, Req 11.1, Req 19.1, Req 19.5

---

### M2.G1.T9: Initialize Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Create `src/types/content.ts` providing re-exports of common inferred types and establishing the SSOT policy (all content contracts derived from Zod schemas).

**Acceptance Criteria:**
- ✓ File `src/types/content.ts` exists
- ✓ Re-exports `IsoDateString` from `@/content/schemas/utils`
- ✓ Contains explicit architectural comment forbidding manual interface duplication
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G1.T2 completed
- Target file: `src/types/content.ts`

**Implementation Details:**

Write `src/types/content.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Canonical Content Contracts (Single Source of Truth)
 *
 * All types in this file are derived directly from Zod schemas via `z.infer<>`.
 * Per AGENTS.md Section 6.1 Rule 5, manual interface duplication is strictly prohibited.
 */

export type { IsoDateString } from '@/content/schemas/utils';
'@ | Set-Content "src\types\content.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/types/content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 20.3

---

### M2.G1.T10: Checkpoint — Infrastructure Verification

**Objective:** Execute type checking and tests across the new schema infrastructure and fixtures to confirm zero regressions.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` executes the utils test suite and passes
- ✓ No `any` types or unsafe assertions introduced

**Prerequisites:**
- M2.G1.T1 through M2.G1.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\content\schemas\utils.ts"
Test-Path "src\content\errors\handler.ts"
Test-Path "tests\fixtures\site.json"
Test-Path "tests\fixtures\projects\valid-project.mdx"
Test-Path "tests\fixtures\certifications\valid-certification.mdx"
Test-Path "tests\fixtures\blog\valid-blog-post.mdx"
npm run typecheck
npm run test
```
Expected output:
- `True` for all file existence checks
- `npm run typecheck` exits with code 0
- `npm run test` passes all tests with code 0.