# M2.G10: Testing & Documentation

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G10 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Finalize the comprehensive verification suite for Milestone 2, ensuring test coverage exceeds 80% across all content modules (`src/content/`). Verify all 10 Correctness Properties from `design.md` Section 6, author the content authoring and error troubleshooting guide (`TROUBLESHOOTING.md`), execute the full quality gate sequence (`format:check`, `lint`, `typecheck`, `test`, `build`), tag the repository with `m2-baseline`, and update `local-ai/program-states/progress-tracker.md` to seal Milestone 2.

## Goal Success Criteria

- ✓ Comprehensive rule verification tests in `tests/unit/schemas/validation-rules.test.ts`
- ✓ `npm run test:coverage` reports $>80\%$ line and branch coverage across `src/content/`
- ✓ All 10 Correctness Properties from `design.md` verified by automated unit or integration tests
- ✓ `TROUBLESHOOTING.md` authored detailing all 8 error categories from `design.md` Section 7.1 with remediation guidance
- ✓ Full sequential verification passes cleanly: `npm run format:check && npm run lint && npm run typecheck && npm run test && npm run build`
- ✓ Git working tree is clean and tagged with `m2-baseline`
- ✓ `local-ai/program-states/progress-tracker.md` updated with Milestone 2 sign-off status

## Prerequisites

- Goals M2.G1 through M2.G9 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- All schemas, loaders, markdown pipeline, and build validation scripts active

---

## Tasks

### M2.G10.T1: Author Comprehensive Validation Rules Test Suite (`tests/unit/schemas/validation-rules.test.ts`)

**Objective:** Implement dedicated edge-case tests in `tests/unit/schemas/validation-rules.test.ts` targeting slug constraints, leap years, boundary strings, and URL protocol edge cases.

**Acceptance Criteria:**
- ✓ Validates slug boundary patterns (single letter slugs, multi-hyphen slugs)
- ✓ Validates calendar edge cases (rejects leap-year violations like `2026-02-29`, accepts leap-year `2024-02-29`)
- ✓ Validates URL protocol enforcement (`http://` rejected, internal asset paths `/images/...` accepted)
- ✓ Validates whitespace trimming behavior across titles and summaries
- ✓ Tests pass in test runner

**Prerequisites:**
- M2.G9 completed
- Target file: `tests/unit/schemas/validation-rules.test.ts`

**Implementation Details:**

Create `tests/unit/schemas/validation-rules.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import {
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  UrlOrAssetPathSchema,
  TitleSchema,
  SummarySchema,
} from '@/content/schemas/utils';

describe('Exhaustive Validation Rules (AGENTS.md Section 5)', () => {
  describe('Slug Validation Rules (AGENTS.md 5.1 Rules 1-3)', () => {
    it('accepts valid alphanumeric slugs with internal hyphens', () => {
      expect(SlugSchema.safeParse('a').success).toBe(true);
      expect(SlugSchema.safeParse('v2-release-notes').success).toBe(true);
      expect(SlugSchema.safeParse('deep-learning-101').success).toBe(true);
    });

    it('rejects slugs with leading, trailing, or double hyphens', () => {
      expect(SlugSchema.safeParse('-leading').success).toBe(false);
      expect(SlugSchema.safeParse('trailing-').success).toBe(false);
      expect(SlugSchema.safeParse('double--hyphen').success).toBe(false);
    });

    it('rejects uppercase letters and special characters', () => {
      expect(SlugSchema.safeParse('Uppercase-Slug').success).toBe(false);
      expect(SlugSchema.safeParse('slug.with.dots').success).toBe(false);
      expect(SlugSchema.safeParse('slug_with_underscores').success).toBe(false);
    });
  });

  describe('Calendar Date Validation Rules (AGENTS.md 5.1 Rule 4)', () => {
    it('verifies non-leap year February 29 is rejected', () => {
      expect(IsoDateStringSchema.safeParse('2026-02-29').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2025-02-29').success).toBe(false);
    });

    it('verifies leap year February 29 is accepted', () => {
      expect(IsoDateStringSchema.safeParse('2024-02-29').success).toBe(true);
      expect(IsoDateStringSchema.safeParse('2028-02-29').success).toBe(true);
    });

    it('rejects months outside 01-12 range and days outside 01-31 range', () => {
      expect(IsoDateStringSchema.safeParse('2026-00-15').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2026-13-15').success).toBe(false);
      expect(IsoDateStringSchema.safeParse('2026-04-31').success).toBe(false); // April has 30 days
      expect(IsoDateStringSchema.safeParse('2026-01-32').success).toBe(false);
    });
  });

  describe('URL Protocol Rules (AGENTS.md 5.1 Rule 5 & 8)', () => {
    it('enforces https:// protocol on external URLs', () => {
      expect(HttpsUrlSchema.safeParse('https://example.com/spec').success).toBe(true);
      expect(HttpsUrlSchema.safeParse('http://example.com/insecure').success).toBe(false);
      expect(HttpsUrlSchema.safeParse('ftp://example.com').success).toBe(false);
    });

    it('accepts internal asset paths starting with /', () => {
      expect(UrlOrAssetPathSchema.safeParse('/images/certifications/badge.png').success).toBe(true);
      expect(UrlOrAssetPathSchema.safeParse('/files/resume.pdf').success).toBe(true);
      expect(UrlOrAssetPathSchema.safeParse('images/no-leading-slash.png').success).toBe(false);
    });
  });

  describe('Boundary String Trimming (AGENTS.md 5.2)', () => {
    it('trims leading/trailing whitespace before measuring length', () => {
      expect(TitleSchema.safeParse('   ab   ').success).toBe(false); // 2 chars trimmed
      expect(TitleSchema.safeParse('   abc   ').success).toBe(true); // 3 chars trimmed

      const shortSummary = '   ' + 'a'.repeat(18) + '   ';
      expect(SummarySchema.safeParse(shortSummary).success).toBe(false); // 18 chars trimmed
    });
  });
});
'@ | Set-Content "tests\unit\schemas\validation-rules.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/schemas/validation-rules.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 10.1, Req 10.3, Req 11.1, Req 11.3, Req 19.1, Req 19.5, Req 19.6

---

### M2.G10.T2: Author Correctness Properties Verification Suite (`tests/unit/properties/correctness.test.ts`)

**Objective:** Implement dedicated property tests verifying all 10 Correctness Properties defined in `design.md` Section 6.

**Acceptance Criteria:**
- ✓ Property 1 (Enum Validation): Rejects unlisted values with choice list
- ✓ Property 2 (Slug Format & Uniqueness): Enforces lowercase, hyphens, and unique identifiers
- ✓ Property 3 (Date Format & Ordering): Enforces `startedAt` $\le$ `completedAt`, `issuedAt` $\le$ `expiresAt`, `eventDate` $\le$ `publishedAt`
- ✓ Property 4 (URL Protocol): Enforces `https://` and permits `mailto:` only for email
- ✓ Property 5 (Featured Count): Limits featured projects to $\le 3$
- ✓ Property 6 (Draft Exclusion): Excludes `draft: true` from loaders and slug queries
- ✓ Property 7 (Type Inference): Re-exported types match Zod output
- ✓ Property 8 (Markdown Safety): Strips script tags and injects `rel="noopener noreferrer"`
- ✓ Property 9 (Build Failure): Validation throws on invalid data
- ✓ Property 10 (Type-Safe Loaders): Data returned matches schema contracts

**Prerequisites:**
- M2.G10.T1 completed
- Target file: `tests/unit/properties/correctness.test.ts`

**Implementation Details:**

Create `tests/unit/properties/correctness.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\unit\properties")) {
    New-Item -ItemType Directory -Path "tests\unit\properties" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { ProjectStatusSchema } from '@/content/schemas/enums';
import { ContactChannelSchema } from '@/content/schemas/site';
import { ProjectSchema } from '@/content/schemas/project';
import { CertificationSchema } from '@/content/schemas/certification';
import { BlogPostSchema } from '@/content/schemas/blog-post';
import { renderMarkdown } from '@/content/markdown/render';
import { validateFeaturedCount } from '@/content/loaders/projects';

describe('M2 Correctness Properties Verification (design.md Section 6)', () => {
  it('Property 1: Enum schemas reject values outside allowed set', () => {
    const res = ProjectStatusSchema.safeParse('non-existent');
    expect(res.success).toBe(false);
  });

  it('Property 3: Temporal date ordering constraints are enforced across schemas', () => {
    // Project: startedAt <= completedAt
    expect(
      ProjectSchema.safeParse({
        title: 'Project',
        summary: 'A valid summary that meets the minimum twenty characters requirement.',
        slug: 'project-slug',
        status: 'completed',
        role: 'Engineer',
        startedAt: '2026-05-01',
        completedAt: '2026-01-01',
        technologies: ['TS'],
        tags: [],
        repositoryUrl: null,
        liveDemoUrl: null,
        documentationUrl: null,
        featured: false,
        displayOrder: 1,
        metrics: [],
        documentation: '## Heading\n\nBody',
      }).success
    ).toBe(false);

    // Certification: issuedAt <= expiresAt
    expect(
      CertificationSchema.safeParse({
        title: 'Cert',
        slug: 'cert-slug',
        issuer: 'Issuer',
        category: 'cloud',
        issuedAt: '2026-06-01',
        expiresAt: '2026-01-01',
        credentialId: null,
        verificationUrl: null,
        badgeImageUrl: null,
        badgeImageAlt: null,
        displayOrder: 1,
        content: '',
      }).success
    ).toBe(false);

    // BlogPost: eventDate <= publishedAt
    expect(
      BlogPostSchema.safeParse({
        title: 'Post Title',
        slug: 'post-slug',
        summary: 'A valid summary that meets the minimum twenty characters requirement.',
        publishedAt: '2026-04-01',
        updatedAt: null,
        eventType: 'meetup',
        eventName: null,
        eventDate: '2026-04-10', // later than publishedAt
        eventLocation: null,
        eventUrl: null,
        tags: ['tech'],
        readingTimeMinutes: 5,
        draft: false,
        content: 'Content',
      }).success
    ).toBe(false);
  });

  it('Property 4: URL protocol enforcement permits mailto: exclusively for email', () => {
    expect(
      ContactChannelSchema.safeParse({
        type: 'email',
        label: 'Email',
        url: 'mailto:user@example.com',
        isPrimary: true,
      }).success
    ).toBe(true);

    expect(
      ContactChannelSchema.safeParse({
        type: 'website',
        label: 'Site',
        url: 'mailto:user@example.com',
        isPrimary: false,
      }).success
    ).toBe(false);
  });

  it('Property 5: Featured project count constraint limits featured: true to at most 3', () => {
    const makeP = (featured: boolean): any => ({ featured });
    expect(() => validateFeaturedCount([makeP(true), makeP(true), makeP(true)])).not.toThrow();
    expect(() => validateFeaturedCount([makeP(true), makeP(true), makeP(true), makeP(true)])).toThrow();
  });

  it('Property 8: Markdown rendering sanitizes HTML and adds noopener noreferrer to external links', async () => {
    const md = 'Payload: <script>alert(1)</script> [External Link](https://example.com)';
    const html = await renderMarkdown(md);

    expect(html).not.toContain('<script');
    expect(html).toContain('rel="noopener noreferrer"');
    expect(html).toContain('target="_blank"');
  });
});
'@ | Set-Content "tests\unit\properties\correctness.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/properties/correctness.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 10.4, Req 11.4, Req 13.2, Req 14.3, Req 14.6, Req 19.4

---

### M2.G10.T3: Author Content Authoring & Error Reference Guide (`TROUBLESHOOTING.md`)

**Objective:** Author `TROUBLESHOOTING.md` documenting all 8 error categories from `design.md` Section 7.1 with clear examples and remediation steps for content authors.

**Acceptance Criteria:**
- ✓ File `TROUBLESHOOTING.md` exists in project root
- ✓ Documents all 8 categories: File Not Found, Parse Error, Schema Validation, Date Format, Slug Conflict, Featured Count, Markdown Rendering, URL Format
- ✓ Provides concrete examples of bad vs good frontmatter
- ✓ Documents verification commands (`npm run validate:content`, `npm run build`)

**Prerequisites:**
- M2.G10.T2 completed
- Target file: `TROUBLESHOOTING.md`

**Implementation Details:**

Write `TROUBLESHOOTING.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
# Content Authoring & Error Troubleshooting Guide

This guide details the validation rules enforced during build time for all Markdown/MDX and JSON content in `content/`.

---

## Quick Verification

Run content validation locally without triggering a full build:
```bash
npm run validate:content
```

---

## Error Categories & Remediation Matrix

### 1. File Not Found
- **Cause:** A required file or directory does not exist.
- **Example:** `content/site.json: File not found or unreadable`
- **Resolution:** Ensure `content/site.json` exists and matches the `SiteConfig` structure.

### 2. Parse Error (JSON / YAML Frontmatter)
- **Cause:** Malformed syntax in JSON or YAML frontmatter delimiters.
- **Example:** `JSON parse error: Unexpected token } in JSON`
- **Resolution:** Validate JSON syntax with an online validator or ensure YAML frontmatter is enclosed between triple hyphens `---`.

### 3. Schema Validation (Boundary Violations)
- **Cause:** Field value violates length or format constraints.
- **Example:** `Field: title | Issue: Title must contain at least 3 characters after trimming`
- **Rules:**
  - Project Title: `3–100` characters.
  - Project Summary: `20–280` characters.
  - Blog Title: `5–120` characters.
  - Blog Summary: `20–300` characters.
  - Reading Time: Integer between `1` and `60` minutes.

### 4. Date Format & Ordering Violations
- **Cause:** Date is not in ISO `YYYY-MM-DD` format, represents a non-existent calendar day, or violates temporal order.
- **Example:** `'startedAt' (2026-06-01) must not be later than 'completedAt' (2026-01-01)`
- **Rules:**
  - Dates must strictly use `YYYY-MM-DD` (e.g. `2026-10-20`).
  - Project: `startedAt <= completedAt` (when `completedAt` is not null).
  - Certification: `issuedAt <= expiresAt` (when `expiresAt` is not null).
  - Blog Post: `eventDate <= publishedAt` (when `eventDate` is present).

### 5. Duplicate Slug Conflict
- **Cause:** Two content files in the same collection have identical `slug` fields.
- **Example:** `Duplicate slug 'my-project' detected. Already defined in 'content/projects/p1.mdx'`
- **Resolution:** Edit the `slug` field in one of the files to make it unique. Slugs must be lowercase alphanumeric and internal hyphens only (e.g. `my-project-v2`).

### 6. Featured Project Count Limit Exceeded
- **Cause:** More than 3 projects have `featured: true`.
- **Example:** `Featured project count exceeds maximum of 3 (found 4)`
- **Resolution:** Set `featured: false` on one or more projects so that at most 3 projects are featured.

### 7. Markdown Documentation Formatting
- **Cause:** Project documentation missing a level-2 heading.
- **Example:** `Project Markdown documentation must contain at least one level-2 heading (##)`
- **Resolution:** Ensure the project MDX body includes at least one `## Heading` section.

### 8. URL Protocol Enforcement
- **Cause:** External URL does not use secure HTTPS, or non-email channel uses `mailto:`.
- **Example:** `Contact channels of type 'email' must use the 'mailto:' protocol`
- **Rules:**
  - Email channels must start with `mailto:`.
  - Social, repository, verification, and demo URLs must start with `https://`.
  - Internal images must start with `/` (e.g. `/images/certifications/badge.png`).
  - Badge image and alt text must both be provided together, or both omitted.
'@ | Set-Content "TROUBLESHOOTING.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "TROUBLESHOOTING.md"
```
Expected output: `True`

**Satisfies Requirements:** Req 17.1, Req 17.2, Req 17.3, Req 17.4

---

### M2.G10.T4: Verify Test Coverage Across Content Modules (`npm run test:coverage`)

**Objective:** Execute the coverage reporter to verify that all modules under `src/content/` exceed the required 80% coverage threshold.

**Acceptance Criteria:**
- ✓ `npm run test:coverage` completes without errors
- ✓ Coverage for `src/content/schemas/` is $>80\%$
- ✓ Coverage for `src/content/loaders/` is $>80\%$
- ✓ Coverage for `src/content/markdown/` is $>80\%$
- ✓ Coverage for `src/content/errors/` is $>80\%$

**Prerequisites:**
- M2.G10.T2 completed

**Implementation Details:**

Run coverage analysis using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test:coverage
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test:coverage
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 19.7

---

### M2.G10.T5: Execute Formatting Quality Gate (`npm run format:check`)

**Objective:** Verify that all newly created schema, loader, script, and test files comply with Prettier rules without formatting discrepancies.

**Acceptance Criteria:**
- ✓ `npm run format:check` runs clean across all files
- ✓ Reports "All matched files use Prettier code style!"
- ✓ Exit code is 0

**Prerequisites:**
- M2.G10.T4 completed

**Implementation Details:**

Run format check via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run format
npm run format:check
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run format:check
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 20.1

---

### M2.G10.T6: Execute Linting Quality Gate (`npm run lint`)

**Objective:** Run ESLint across the repository to verify zero linting errors, no unsafe type assignments, and no accessibility issues.

**Acceptance Criteria:**
- ✓ `npm run lint` completes execution
- ✓ Process exit code is 0
- ✓ Zero warnings or errors reported

**Prerequisites:**
- M2.G10.T5 completed

**Implementation Details:**

Run linting via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run lint
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 20.2, Req 20.5

---

### M2.G10.T7: Execute Type-Checking Quality Gate (`npm run typecheck`)

**Objective:** Confirm strict TypeScript compilation across the entire project including all new content modules, loaders, types, and test suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` executes `tsc --noEmit`
- ✓ Process exit code is 0
- ✓ Zero type errors or resolution errors

**Prerequisites:**
- M2.G10.T6 completed

**Implementation Details:**

Run type checking via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 20.1, Req 20.2

---

### M2.G10.T8: Execute Production Build Quality Gate (`npm run build`)

**Objective:** Run `npm run build` to verify content validation and static export compilation into `out/`.

**Acceptance Criteria:**
- ✓ `validate:content` triggers and passes
- ✓ `next build` static export succeeds
- ✓ `out/` contains static assets and HTML
- ✓ Process exit code is 0

**Prerequisites:**
- M2.G10.T7 completed

**Implementation Details:**

Execute production build via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run build
if ($LASTEXITCODE -eq 0 -and (Test-Path "out\index.html")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.4, Req 16.5

---

### M2.G10.T9: Commit and Tag Milestone 2 Baseline (`m2-baseline`)

**Objective:** Stage all Milestone 2 assets, commit with a standardized conventional commit message, and create the immutable Git tag `m2-baseline`.

**Acceptance Criteria:**
- ✓ All modified and untracked files in Milestone 2 are committed
- ✓ Working tree is clean
- ✓ Git tag `m2-baseline` is created on HEAD

**Prerequisites:**
- M2.G10.T8 completed

**Implementation Details:**

Execute Git commit and tagging via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git add .
git commit -m "feat(m2): content architecture, zod schemas, loaders, and validation pipeline"
git tag -a "m2-baseline" -m "Milestone 2 Content Architecture & Validation Verified"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$tag = git tag -l "m2-baseline"
if ($tag -eq "m2-baseline") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 18.1, Req 20.1

---

### M2.G10.T10: Update State Tracker for Milestone 2 Completion

**Objective:** Record completion of Milestone 2 in `local-ai/program-states/progress-tracker.md`.

**Acceptance Criteria:**
- ✓ `local-ai/program-states/progress-tracker.md` updated
- ✓ Marks **M2: Content Architecture & Validation** as `COMPLETED`
- ✓ Records validation status: PASS across Lint, Types, Tests (>80% coverage), Build
- ✓ Commit updated tracker to Git

**Prerequisites:**
- M2.G10.T9 completed
- Target file: `local-ai/program-states/progress-tracker.md`

**Implementation Details:**

Update the state tracker using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
# Orchestrator Progress Tracker

## Milestone Execution Status

| Milestone | Status | Gates Status | Baseline Tag | Completed Date |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Repository Foundation & Toolchain** | **COMPLETED** | PASS (Lint, Types, Tests, Build) | `m1-baseline` | 2026-10-20 |
| **M2: Content Architecture & Validation** | **COMPLETED** | PASS (Lint, Types, Tests >80%, Build) | `m2-baseline` | 2026-10-20 |
| **M3: Global Layout & Design System** | NOT STARTED | PENDING | — | — |
| **M4: Core Routes & Experiences** | NOT STARTED | PENDING | — | — |
| **M5: QA, Accessibility & Audits** | NOT STARTED | PENDING | — | — |
| **M6: Production Deployment** | NOT STARTED | PENDING | — | — |

## Milestone 2 Verification Log
- `npm run format:check`: PASS (All files compliant)
- `npm run lint`: PASS (0 errors, 0 warnings)
- `npm run typecheck`: PASS (0 errors, strict mode verified)
- `npm run test:coverage`: PASS (>80% coverage across `src/content/`)
- `npm run validate:content`: PASS (all 4 content types validated)
- `npm run build`: PASS (static export generated into `out/`)
- Git Baseline: `m2-baseline` tagged cleanly
'@ | Set-Content "local-ai\program-states\progress-tracker.md" -Encoding UTF8

git add local-ai/program-states/progress-tracker.md
git commit -m "docs(m2): record milestone 2 completion in progress tracker"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$content = Get-Content "local-ai\program-states\progress-tracker.md" -Raw
if ($content -match "M2: Content Architecture & Validation.*COMPLETED") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 18.1, Req 20.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 10 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "TROUBLESHOOTING.md"
Test-Path "tests\unit\schemas\validation-rules.test.ts"
Test-Path "tests\unit\properties\correctness.test.ts"
git tag -l "m2-baseline"
git status
```
Expected output:
- `True` for `TROUBLESHOOTING.md` and both test suites
- Git tag lists `m2-baseline`
- Working tree clean.

***

### Summary of Completed M2 Goals
All 10 Goal specification files for Milestone 2 are now generated:
- `goal1.md`: Zod Schema Infrastructure Setup
- `goal2.md`: Enum Schemas
- `goal3.md`: SiteConfig Schema & Loader
- `goal4.md`: Project Schemas & Loaders
- `goal5.md`: Certification Schemas & Loaders
- `goal6.md`: BlogPost Schemas & Loaders
- `goal7.md`: Markdown Rendering Pipeline
- `goal8.md`: Type Inference & Type Safety
- `goal9.md`: Build-Time Validation Integration
- `goal10.md`: Testing & Documentation