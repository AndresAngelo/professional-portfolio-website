# M2 Content Architecture & Validation — Requirements Document

> **Document Status:** Draft  
> **Feature Name:** m2-content-architecture-validation  
> **Milestone:** M2  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md`, `PRD.md`, `TRD.md`  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 2 (M2) establishes the complete content layer infrastructure for `personal-website-portfolio-v2`. M2 implements Zod schema validators, content loaders, Markdown rendering pipeline, and build-time validation. This transforms raw Markdown/JSON files in `content/` into typed, validated collections ready for M3+ consumption.

M2 is the bridge between raw content files and the static site generation pipeline. All content must be validated, typed, and discoverable before any route or component renders it. This milestone ensures:

- Strict schema compliance for all 6 content types (SiteConfig, Project, Certification, BlogPost, + 3 enums)
- Type-safe content loaders with error handling
- Markdown rendering pipeline for project documentation and blog posts
- Build-time validation with descriptive error messages
- Type inference from Zod (z.infer<>, NO duplicate types)
- Seed content with validation tests

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **SiteConfig** | Global site metadata (profile, contact channels, navigation). Source: `content/site.json`. Type: `SiteConfig`. |
| **Project** | Portfolio project case study with Markdown documentation. Source: `content/projects/*.mdx`. Type: `Project`. |
| **Certification** | Certification or badge credential. Source: `content/certifications/*.mdx`. Type: `Certification`. |
| **BlogPost** | Blog post covering meetups, hackathons, learning, or project updates. Source: `content/blog/*.mdx`. Type: `BlogPost`. |
| **Zod Schema** | TypeScript-first schema validator using Zod library. Used for runtime validation of JSON and frontmatter. |
| **Frontmatter** | YAML metadata at the top of Markdown files, enclosed in `***` delimiters. Contains structured metadata. |
| **Markdown Rendering** | Process of converting Markdown content to HTML using an approved Markdown renderer library. |
| **Build-Time Validation** | Schema and content validation performed during `npm run build`. Invalid content must fail the build. |
| **Type Inference** | Using Zod's `z.infer<>` to derive TypeScript types from schema definitions (SSOT). |
| **IsoDateString** | Date string in ISO `YYYY-MM-DD` format (e.g., `2026-10-20`). |
| **ProjectStatus** | Enum: `"completed"` | `"in-progress"` | `"archived"`. |
| **CertificationCategory** | Enum: `"cloud"` | `"ai"` | `"security"` | `"frontend"` | `"backend"` | `"data"` | `"devops"` | `"professional"`. |
| **EventType** | Enum: `"meetup"` | `"hackathon"` | `"workshop"` | `"conference"` | `"learning"` | `"project-update"`. |
| **ContactChannelType** | Enum: `"email"` | `"linkedin"` | `"github"` | `"website"` | `"other"`. |
| **Slug** | URL-safe content identifier: lowercase letters, numbers, hyphens; no leading/trailing hyphens. Unique within collection. |

---

## Requirements

---

### Requirement 1: Define Enum Schemas (ProjectStatus, CertificationCategory, EventType, ContactChannelType)

**User Story:**
As a system architect, I want enum schemas defined in Zod for all content types, so that enum values are validated at build time and type-safe throughout the application.

#### Acceptance Criteria

1. WHEN the Zod schema module is loaded, THE Enum_Validator SHALL define ProjectStatus with values `"completed"` | `"in-progress"` | `"archived"` (AGENTS.md 4.2).
2. WHEN the Zod schema module is loaded, THE Enum_Validator SHALL define CertificationCategory with 8 values: `"cloud"` | `"ai"` | `"security"` | `"frontend"` | `"backend"` | `"data"` | `"devops"` | `"professional"` (AGENTS.md 4.2).
3. WHEN the Zod schema module is loaded, THE Enum_Validator SHALL define EventType with 6 values: `"meetup"` | `"hackathon"` | `"workshop"` | `"conference"` | `"learning"` | `"project-update"` (AGENTS.md 4.2).
4. WHEN the Zod schema module is loaded, THE Enum_Validator SHALL define ContactChannelType with values `"email"` | `"linkedin"` | `"github"` | `"website"` | `"other"` (AGENTS.md 4.2).
5. WHEN an enum value is provided outside the allowed set, THE Schema_Validator SHALL reject it with an error message naming the field, expected values, and received value (AGENTS.md 5.1 Rule 10).
6. THE Enum_Validator SHALL use Zod's `.enum()` method or equivalent strict validation; no string enum fallbacks permitted.

#### Verification Steps

1. Open `src/content/schemas/enums.ts`.
2. Verify each enum is defined as a Zod schema: `const ProjectStatusSchema = z.enum([...])`.
3. Run `npm run typecheck` and verify no implicit-any or type errors.
4. Test with `npm test` by importing and validating invalid enum values; verify rejection.
5. Confirm schema definitions match AGENTS.md 4.2 exactly.

---

### Requirement 2: Define SiteConfig Schema with All Required and Optional Fields

**User Story:**
As an infrastructure engineer, I want a complete SiteConfig schema with strict field validation, so that global site metadata is guaranteed valid before build completion.

#### Acceptance Criteria

1. WHEN the SiteConfig schema is loaded, THE Schema_Validator SHALL enforce all fields defined in AGENTS.md 4.2 SiteConfig interface.
2. WHEN SiteConfig frontmatter is parsed, THE Validator SHALL require: `siteName`, `siteUrl`, `profile` (name, professionalTitle, introduction, location, availableForOpportunities), `contactChannels[]`, `socialLinks[]`, `navigation[]` (AGENTS.md 4.2).
3. WHEN a `contactChannels` entry is validated, THE Validator SHALL require type, label, url, isPrimary; verify type is in ContactChannelType enum (AGENTS.md 4.2).
4. WHEN a `siteUrl` or contact `url` is validated, THE Validator SHALL enforce absolute HTTPS URL format or `/` internal asset path (AGENTS.md 5.1 Rule 5).
5. WHEN an `email` contact channel is validated, THE Validator SHALL permit `mailto:` protocol; reject for other channel types (AGENTS.md 5.1 Rule 6).
6. WHEN SiteConfig validation fails, THE Error_Handler SHALL return a message including: file path, field name, expected type, received value category (AGENTS.md 5.1 Rule 10).

#### Verification Steps

1. Open `src/content/schemas/site.ts` or equivalent module.
2. Verify schema matches SiteConfig interface in AGENTS.md 4.2.
3. Run validation against `content/site.json` from example in AGENTS.md 4.3.
4. Test with invalid URLs, missing fields, and invalid channel types; verify errors include file path and field name.
5. Confirm no optional fields are made required without explicit design change.

---

### Requirement 3: Define Project Schema with All Validation Rules from AGENTS.md

**User Story:**
As a content validator, I want comprehensive Project schema validation enforcing all rules from AGENTS.md Section 5.2, so that invalid project entries fail the build with clear guidance.

#### Acceptance Criteria

1. WHEN a Project frontmatter is parsed, THE Validator SHALL enforce: `title` (3–100 chars), `summary` (20–280 chars), `slug` (unique, lowercase, hyphens only), `status` (enum), `role`, `startedAt` (ISO date), `completedAt` (ISO date or null), `technologies[]` (min 1), `tags[]`, `repositoryUrl`, `liveDemoUrl`, `documentationUrl` (null or HTTPS URL), `featured` (boolean), `displayOrder` (number), `metrics[]` (AGENTS.md 5.2).
2. WHEN `startedAt` and `completedAt` are both present, THE Validator SHALL enforce `startedAt` ≤ `completedAt` (AGENTS.md 5.2).
3. WHEN `featured: true`, THE Validator SHALL enforce `displayOrder` is present; when `featured: false`, `displayOrder` is optional (AGENTS.md 5.2).
4. WHEN project document is counted, THE Validator SHALL enforce at most 3 projects have `featured: true` across all projects (AGENTS.md 5.2).
5. WHEN project Markdown documentation is parsed, THE Validator SHALL enforce at least one `##` heading present (AGENTS.md 5.2).
6. WHEN a slug is validated, THE Validator SHALL enforce: lowercase only, hyphens permitted, no leading/trailing hyphens, unique within projects collection (AGENTS.md 5.1 Rules 1–3, 5.2).
7. WHEN dates are validated, THE Validator SHALL enforce ISO `YYYY-MM-DD` format (AGENTS.md 5.1 Rule 4).

#### Verification Steps

1. Open `src/content/schemas/project.ts`.
2. Create test cases for each validation rule: title length, summary length, slug format, status enum, date ordering, featured count, and heading detection.
3. Test with boundary values (title exactly 3 and 100 chars; summary exactly 20 and 280 chars).
4. Test with invalid slugs: uppercase letters, trailing hyphens, non-URL characters.
5. Verify validation errors include field name and expected format (AGENTS.md 5.1 Rule 10).
6. Run `npm test` and confirm all tests pass.

---

### Requirement 4: Define Certification and BlogPost Schemas with Validation Rules

**User Story:**
As a data architect, I want complete Certification and BlogPost schemas enforcing AGENTS.md rules, so that all content types are validated consistently at build time.

#### Acceptance Criteria

**Certification Schema:**

1. WHEN a Certification frontmatter is parsed, THE Validator SHALL enforce: `title`, `slug` (unique, format rules), `issuer`, `category` (CertificationCategory enum), `issuedAt` (ISO date), `expiresAt` (ISO date or null), `credentialId` (optional), `verificationUrl` (HTTPS or null), `badgeImageUrl` and `badgeImageAlt` (both present or both absent), `displayOrder` (AGENTS.md 5.3).
2. WHEN `expiresAt` is present, THE Validator SHALL enforce `expiresAt` ≥ `issuedAt` (AGENTS.md 5.3).
3. WHEN `verificationUrl` is present, THE Validator SHALL enforce absolute HTTPS URL format (AGENTS.md 5.3).
4. WHEN `badgeImageUrl` is present, THE Validator SHALL require `badgeImageAlt` also present; if one is absent, reject entry (AGENTS.md 5.3).
5. WHEN `credentialId` is present, THE Validator SHALL not fabricate or assume values; accept user-provided value only (AGENTS.md 5.3, 6.1 Rule 6).

**BlogPost Schema:**

6. WHEN a BlogPost frontmatter is parsed, THE Validator SHALL enforce: `title` (5–120 chars), `slug` (unique, format rules), `summary` (20–300 chars), `publishedAt` (ISO date, required), `updatedAt` (ISO date or null), `eventType` (EventType enum), `eventName`, `eventDate`, `eventLocation`, `eventUrl` (all optional), `tags[]`, `readingTimeMinutes` (1–60), `draft` (boolean) (AGENTS.md 5.4).
7. WHEN `eventDate` is present, THE Validator SHALL enforce `eventDate` ≤ `publishedAt` (AGENTS.md 5.4).
8. WHEN `draft: true`, THE Validator SHALL exclude the post from loaders and static route generation (AGENTS.md 5.4).

#### Verification Steps

1. Open `src/content/schemas/certification.ts` and `src/content/schemas/blog-post.ts`.
2. Create test cases for Certification: date ordering, badge image pairing, valid/invalid URLs.
3. Create test cases for BlogPost: title length, summary length, reading time range, eventDate ordering, draft exclusion.
4. Test boundary values (title 5, 120; summary 20, 300; readingTimeMinutes 1, 60).
5. Verify validation errors include file path and field details (AGENTS.md 5.1 Rule 10).
6. Run `npm test` and confirm all tests pass.

---

### Requirement 5: Implement getSiteConfig() Loader Function

**User Story:**
As a route handler, I want a type-safe getSiteConfig() function, so that I can load global site metadata with guaranteed type safety.

#### Acceptance Criteria

1. WHEN getSiteConfig() is called, THE Loader SHALL read `content/site.json` from the file system (AGENTS.md 4.3, TRD.md 4.1).
2. WHEN the file is read, THE Loader SHALL parse JSON and validate against SiteConfig schema (TRD.md 3.2).
3. WHEN validation succeeds, THE Loader SHALL return typed SiteConfig object; when validation fails, THE Loader SHALL throw error with file path and validation details (AGENTS.md 5.1 Rule 10, TRD.md 3.2).
4. WHEN the file does not exist, THE Loader SHALL throw error indicating missing required site.json file (AGENTS.md 5.1 Rule 7).
5. THE Return_Type SHALL be `SiteConfig` derived from Zod schema using `z.infer<>` (no duplicate type definition in TypeScript) (AGENTS.md 6.1 Rule 5, 4.2).

#### Verification Steps

1. Create `src/content/loaders/site.ts` with getSiteConfig() function.
2. Test with valid `content/site.json` from AGENTS.md 4.3 example.
3. Test with missing file; verify error message indicates `content/site.json` not found.
4. Test with invalid JSON; verify error includes file path and parsing error.
5. Test with invalid schema; verify error includes field name and expected type.
6. Run `npm run typecheck` and verify return type is SiteConfig (inferred from Zod).

---

### Requirement 6: Implement getProjects() and getProjectBySlug() Loader Functions

**User Story:**
As a route handler and component, I want typed project loaders, so that I can fetch all projects or individual projects by slug with type safety and validation.

#### Acceptance Criteria

1. WHEN getProjects() is called, THE Loader SHALL read all files from `content/projects/*.mdx` (AGENTS.md 3).
2. WHEN each project file is read, THE Loader SHALL parse frontmatter (YAML between `***` delimiters) and Markdown documentation (AGENTS.md 4.3).
3. WHEN frontmatter is parsed, THE Loader SHALL validate against Project schema including all rules from Req 3 (AGENTS.md 5.2).
4. WHEN Markdown documentation is extracted, THE Loader SHALL store as `documentation` field on Project object (AGENTS.md 4.2).
5. WHEN all projects are loaded and validated, THE Loader SHALL return sorted array ordered by `displayOrder` ascending, then by `startedAt` descending (TRD.md 4.1).
6. WHEN a slug is not found in the projects collection, THE Loader SHALL return `null` for getProjectBySlug(slug); the UI must handle gracefully (TRD.md 4.3).
7. WHEN any project file fails validation, THE Build_Pipeline SHALL fail with error including file path, field name, and validation issue (AGENTS.md 5.1 Rule 10, TRD.md 3.2).
8. THE Return_Type for getProjects() SHALL be `Project[]`; for getProjectBySlug() SHALL be `Project | null` (derived from Zod schema) (AGENTS.md 4.2).

#### Verification Steps

1. Create `src/content/loaders/projects.ts` with getProjects() and getProjectBySlug() functions.
2. Create example project files in `content/projects/` matching AGENTS.md 4.3 format.
3. Test loading all projects; verify sorted by displayOrder then startedAt.
4. Test getProjectBySlug() with valid and invalid slugs.
5. Test with missing frontmatter; verify error includes file path.
6. Test with invalid status enum; verify validation error.
7. Run `npm run build` and verify no errors with valid content.

---

### Requirement 7: Implement getCertifications() and getBlogPosts()/getBlogPostBySlug() Loaders

**User Story:**
As a route and component, I want typed loaders for certifications and blog posts, so that I can fetch and filter content with type safety.

#### Acceptance Criteria

1. WHEN getCertifications() is called, THE Loader SHALL read all files from `content/certifications/*.mdx` (AGENTS.md 3).
2. WHEN each certification file is read, THE Loader SHALL parse frontmatter and optional content (AGENTS.md 4.3).
3. WHEN frontmatter is parsed, THE Loader SHALL validate against Certification schema including all rules from Req 4 (AGENTS.md 5.3).
4. WHEN all certifications are loaded, THE Loader SHALL return sorted array by `displayOrder` ascending (TRD.md 4.1).
5. WHEN getBlogPosts() is called, THE Loader SHALL read all files from `content/blog/*.mdx` (AGENTS.md 3).
6. WHEN blog files are read, THE Loader SHALL exclude all entries with `draft: true` from the returned array (AGENTS.md 5.4, PRD.md 7).
7. WHEN all blog posts are loaded, THE Loader SHALL return sorted array ordered by `publishedAt` descending (most recent first) (TRD.md 4.1).
8. WHEN getBlogPostBySlug(slug) is called with invalid slug, THE Loader SHALL return `null` (TRD.md 4.3).
9. WHEN any certification or blog file fails validation, THE Build_Pipeline SHALL fail with error including file path and validation details (AGENTS.md 5.1 Rule 10).
10. THE Return_Types SHALL be `Certification[]`, `BlogPost[]`, and `BlogPost | null` (derived from Zod schemas) (AGENTS.md 4.2).

#### Verification Steps

1. Create `src/content/loaders/certifications.ts` with getCertifications() function.
2. Create `src/content/loaders/blog.ts` with getBlogPosts() and getBlogPostBySlug() functions.
3. Create example certification and blog files in `content/` matching AGENTS.md 4.3 format.
4. Test getCertifications() sorting by displayOrder.
5. Test getBlogPosts() excludes draft posts and sorts by publishedAt descending.
6. Test getBlogPostBySlug() with valid and invalid slugs.
7. Test with invalid eventType enum; verify validation error.
8. Run `npm run build` and verify no build errors with valid content.

---

### Requirement 8: Implement Loader Error Handling with Descriptive Messages

**User Story:**
As a developer, I want comprehensive error handling in loaders, so that validation failures provide clear guidance on what content needs fixing.

#### Acceptance Criteria

1. WHEN a content file fails to load, THE Error_Handler SHALL include: file path, error type (missing, parse, validation), affected field name, expected type/format, and received value category (AGENTS.md 5.1 Rule 10).
2. WHEN frontmatter YAML parsing fails, THE Error_Message SHALL indicate YAML parse error, line number if available, and the affected content file (TRD.md 3.2).
3. WHEN schema validation fails, THE Error_Message SHALL show: field name, expected constraint (e.g., "minimum 3 characters"), and received value (AGENTS.md 5.1 Rule 10, TRD.md 3.2).
4. WHEN featured project count exceeds 3, THE Error_Message SHALL indicate which projects have `featured: true` and total count (AGENTS.md 5.2).
5. WHEN slug is duplicated within a collection, THE Error_Message SHALL list all files with the duplicate slug (AGENTS.md 5.1 Rule 1).
6. WHEN the build fails due to content validation, THE Error_Output SHALL exit with non-zero code and display all validation errors before stopping (TRD.md 3.2).

#### Verification Steps

1. Create comprehensive error test cases in `tests/content-loaders.test.ts`.
2. Test missing file; verify error includes file path.
3. Test invalid YAML; verify error indicates parse failure.
4. Test invalid field value; verify error shows field name and expected format.
5. Test duplicate slugs; verify error lists all duplicates.
6. Test featured count > 3; verify error lists affected files.
7. Run `npm test` and verify all error messages are clear and actionable.

---

### Requirement 9: Implement Slug Validation (Lowercase, Hyphens, No Leading/Trailing, Unique)

**User Story:**
As a URL validator, I want strict slug validation, so that all content slugs are URL-safe and unique within collections.

#### Acceptance Criteria

1. WHEN a slug is validated, THE Validator SHALL enforce lowercase letters only (a-z), numbers (0-9), and hyphens (-); reject uppercase, underscores, spaces (AGENTS.md 5.1 Rule 2).
2. WHEN a slug is validated, THE Validator SHALL reject slugs beginning with hyphen; reject slugs ending with hyphen (AGENTS.md 5.1 Rule 3).
3. WHEN a slug is validated, THE Validator SHALL enforce unique value within its collection (projects, certifications, blog) (AGENTS.md 5.1 Rule 1).
4. WHEN a slug is validated and violates format rules, THE Error_Message SHALL indicate which characters are invalid and show expected pattern (AGENTS.md 5.1 Rule 10).
5. WHEN a slug is validated and is duplicated, THE Error_Message SHALL list the file path and all duplicate slug occurrences (AGENTS.md 5.1 Rule 1).

#### Verification Steps

1. Create slug validation tests in `tests/validation-rules.test.ts`.
2. Test valid slugs: `"my-project"`, `"project-123"`, `"a"`.
3. Test invalid slugs: `"My-Project"` (uppercase), `"-my-project"` (leading hyphen), `"my-project-"` (trailing hyphen), `"my_project"` (underscore), `"my project"` (space).
4. Test duplicate slugs within collection; verify error includes file paths.
5. Run `npm test` and verify all slug validation tests pass.

---

### Requirement 10: Implement Date Validation (ISO YYYY-MM-DD Format)

**User Story:**
As a date validator, I want strict ISO date validation, so that all temporal metadata is consistent and machine-readable.

#### Acceptance Criteria

1. WHEN a date field is validated, THE Validator SHALL enforce ISO `YYYY-MM-DD` format (e.g., `2026-10-20`) (AGENTS.md 5.1 Rule 4).
2. WHEN a date is provided in alternative format (MM/DD/YYYY, DD-MM-YYYY, etc.), THE Validator SHALL reject with message showing expected format (AGENTS.md 5.1 Rule 4).
3. WHEN a date is validated, THE Validator SHALL verify it is a valid calendar date (e.g., reject `2026-02-30`) (AGENTS.md 5.1 Rule 4).
4. WHEN two date fields have an ordering constraint (e.g., `startedAt` ≤ `completedAt`), THE Validator SHALL enforce the constraint; rejection error shall indicate which fields violate the constraint (AGENTS.md 5.2, 5.4).

#### Verification Steps

1. Create date validation tests in `tests/validation-rules.test.ts`.
2. Test valid dates: `"2026-01-15"`, `"2026-12-31"`.
3. Test invalid formats: `"01/15/2026"`, `"15-01-2026"`, `"2026/01/15"`, `"Jan 15, 2026"`.
4. Test invalid calendar dates: `"2026-02-30"`, `"2026-13-01"`.
5. Test date ordering: `startedAt > completedAt` fails; `startedAt = completedAt` passes; `startedAt < completedAt` passes.
6. Run `npm test` and verify all date tests pass.

---

### Requirement 11: Implement URL Validation (HTTPS, Null Handling, No Broken Links)

**User Story:**
As a link validator, I want strict URL validation, so that all external and internal links are valid and not broken at build time.

#### Acceptance Criteria

1. WHEN a required URL field is validated, THE Validator SHALL enforce absolute HTTPS URL format (e.g., `https://github.com/...`) (AGENTS.md 5.1 Rule 5).
2. WHEN an optional URL field is null or empty string, THE Validator SHALL accept without error; the UI must omit the corresponding action (AGENTS.md 5.1 Rule 8, PRD.md 7).
3. WHEN an internal asset path is validated, THE Validator SHALL permit paths beginning with `/` (e.g., `/images/badge.png`); reject other paths (AGENTS.md 5.1 Rule 5).
4. WHEN a `mailto:` protocol is validated, THE Validator SHALL permit only for `email` contact channels; reject for other channel types (AGENTS.md 5.1 Rule 6).
5. WHEN a URL is provided without `https://` protocol, THE Validator SHALL reject with message indicating protocol required (AGENTS.md 5.1 Rule 5).

#### Verification Steps

1. Create URL validation tests in `tests/validation-rules.test.ts`.
2. Test valid URLs: `"https://github.com/example"`, `"https://example.com/verify/abc123"`, `"/images/badge.png"`.
3. Test invalid URLs: `"http://example.com"` (HTTP), `"github.com/example"` (no protocol), `"ftp://example.com"` (wrong protocol).
4. Test null/empty for optional URLs; verify no validation error.
5. Test `mailto:` only for email channels; reject for others.
6. Run `npm test` and verify all URL tests pass.

---

### Requirement 12: Implement Draft Post Exclusion Logic

**User Story:**
As a content manager, I want draft blog posts automatically excluded from production builds, so that I can stage posts without accidentally publishing them.

#### Acceptance Criteria

1. WHEN getBlogPosts() is called, THE Loader SHALL exclude all BlogPost entries where `draft: true` (AGENTS.md 5.4).
2. WHEN a draft post is present in `content/blog/`, THE Build_Pipeline SHALL validate the draft post's schema (it must be valid), but exclude from returned collection (AGENTS.md 5.4).
3. WHEN static routes are generated for blog, THE Route_Generator SHALL only generate routes for non-draft posts; draft post slugs must not have corresponding static routes (AGENTS.md 5.4, PRD.md 7).
4. WHEN a draft post is requested via getPostBySlug(slug), THE Loader SHALL return `null` even if a draft post with matching slug exists (AGENTS.md 5.4).
5. WHEN the homepage displays recent blog activity, THE Component_Loader SHALL include only non-draft posts (PRD.md 7).

#### Verification Steps

1. Create `content/blog/draft-post.mdx` with `draft: true`.
2. Create `content/blog/published-post.mdx` with `draft: false`.
3. Call getBlogPosts(); verify only published post is returned.
4. Call getBlogPostBySlug("draft-post"); verify `null` is returned.
5. Run `npm run build`; verify no static route exists for draft-post slug.
6. Verify homepage recent blog section shows only published posts.
7. Run `npm test` and verify all draft exclusion tests pass.

---

### Requirement 13: Implement Featured Project Max-3 Constraint Validation

**User Story:**
As a content curator, I want featured project count limited to 3, so that the homepage doesn't become cluttered with featured cards.

#### Acceptance Criteria

1. WHEN all projects are loaded and validated, THE Validator SHALL count projects where `featured: true` (AGENTS.md 5.2).
2. WHEN featured project count exceeds 3, THE Validator SHALL fail build-time validation with error message listing: file paths of all featured projects, current count, and maximum allowed (3) (AGENTS.md 5.2).
3. WHEN exactly 3 projects have `featured: true`, THE Build SHALL proceed without error (AGENTS.md 5.2).
4. WHEN fewer than 3 projects have `featured: true`, THE Build SHALL proceed without error (AGENTS.md 5.2).
5. WHEN projects have `featured: false`, THE Validator SHALL ignore in featured count; count only `featured: true` (AGENTS.md 5.2).

#### Verification Steps

1. Create 5 test project files with varying `featured` values.
2. Set 4 projects to `featured: true`; run `npm run build`.
3. Verify build fails with error showing count and file paths.
4. Modify to 3 projects `featured: true`; run build; verify success.
5. Add validation test in `tests/content-validation.test.ts`.
6. Run `npm test` and verify featured count test passes.

---

### Requirement 14: Implement Markdown Rendering Pipeline

**User Story:**
As a route handler and component, I want a Markdown rendering pipeline, so that project documentation and blog posts are converted to HTML safely.

#### Acceptance Criteria

1. WHEN project documentation or blog post content is loaded, THE Markdown_Renderer SHALL parse Markdown and convert to HTML (TRD.md 3.1, 3.2).
2. WHEN Markdown contains code blocks, THE Renderer SHALL apply syntax highlighting using an approved syntax-highlighting library (e.g., Shiki or Prism) (TRD.md 3.1).
3. WHEN Markdown contains links, THE Renderer SHALL apply `rel="noopener noreferrer"` to external links opening in new tab (TRD.md 6.4).
4. WHEN Markdown contains images, THE Renderer SHALL support responsive image syntax and verify image paths exist or are external URLs (TRD.md 6.4).
5. WHEN Markdown rendering fails, THE Error_Handler SHALL include: file path, error type, and line context if available (AGENTS.md 5.1 Rule 10).
6. THE Renderer SHALL sanitize HTML output to prevent XSS; use a library like `DOMPurify` or `sanitize-html` if applicable (TRD.md 6.4).

#### Verification Steps

1. Create `src/content/markdown/render.ts` with Markdown rendering function.
2. Test with sample project documentation from AGENTS.md 4.3.
3. Test code block rendering; verify syntax highlighting applied.
4. Test external link; verify `rel="noopener noreferrer"` present.
5. Test image rendering; verify responsive attributes applied.
6. Test XSS payload; verify script tags removed/escaped.
7. Run `npm test` and verify all rendering tests pass.

---

### Requirement 15: Implement Type Inference from Zod (No Duplicate Type Definitions)

**User Story:**
As a TypeScript architect, I want all content types inferred from Zod schemas using z.infer<>, so that there is a single source of truth and no duplicated type definitions.

#### Acceptance Criteria

1. WHEN a content type is needed in TypeScript, THE Code SHALL use `z.infer<typeof SchemaName>` to derive the type from Zod schema (AGENTS.md 6.1 Rule 5).
2. THE Types File (`src/types/content.ts` or similar) SHALL export only type inferences from Zod schemas; no duplicate interface or type definitions permitted (AGENTS.md 6.1 Rule 5).
3. WHEN the Zod schema is updated, THE TypeScript type SHALL automatically update via `z.infer<>`; no manual type definition edits required (AGENTS.md 6.1 Rule 5).
4. WHEN `any`, implicit `any`, non-null assertions (`!`), or unjustified type assertions are found, THE TypeScript_Compiler SHALL reject in strict mode (AGENTS.md 6.1 Rule 7).
5. WHEN type checking is run with `npm run typecheck`, THE Compiler SHALL report zero errors and zero warnings related to content types (AGENTS.md 6.1 Rule 7).

#### Verification Steps

1. Open `src/types/content.ts` and verify all exports use `z.infer<>`.
2. Verify no duplicate interfaces or types exist in `src/` (use grep: `grep -r "interface Project"` should find only the schema definition).
3. Modify a Zod schema field type; verify TypeScript type updates automatically.
4. Run `npm run typecheck` and verify zero errors.
5. Add a non-null assertion (e.g., `const x = value!;`); run typecheck; verify error is reported.
6. Fix the assertion; run typecheck; verify error is resolved.

---

### Requirement 16: Implement Build-Time Content Validation with Error Exit

**User Story:**
As a deployment engineer, I want build-time validation to fail the build when content is invalid, so that invalid content never reaches production.

#### Acceptance Criteria

1. WHEN `npm run build` is executed, THE Build_Pipeline SHALL load and validate all content files before static generation (TRD.md 3.2).
2. WHEN any content file fails schema validation, THE Build_Pipeline SHALL halt and exit with non-zero code (TRD.md 3.2).
3. WHEN build fails, THE Error_Output SHALL display all validation errors in a clear, actionable format, including file path and field details (AGENTS.md 5.1 Rule 10, TRD.md 3.2).
4. WHEN content validation succeeds, THE Build_Pipeline SHALL proceed to static route generation and asset bundling (TRD.md 3.2).
5. WHEN a validation error is fixed and build is retried, THE Build_Pipeline SHALL succeed if all content is valid (TRD.md 3.2).

#### Verification Steps

1. Create valid project content in `content/projects/example.mdx`.
2. Run `npm run build`; verify build succeeds.
3. Introduce validation error (e.g., invalid status enum).
4. Run `npm run build`; verify build fails with exit code non-zero.
5. Verify error message includes file path and field name.
6. Fix the error and re-run build; verify build succeeds.

---

### Requirement 17: Implement Descriptive Error Messages with File Path, Field, Type, and Value

**User Story:**
As a content editor, I want descriptive error messages that show exactly what needs fixing, so that I can quickly resolve validation failures.

#### Acceptance Criteria

1. WHEN content validation fails, THE Error_Message SHALL include: file path (e.g., `content/projects/my-project.mdx`), field name (e.g., `title`), expected constraint (e.g., `minimum 3 characters`), and received value category (e.g., `received 2 characters: "ab"`) (AGENTS.md 5.1 Rule 10).
2. WHEN schema validation fails due to type mismatch, THE Error_Message SHALL show: expected type (e.g., `string`), received type (e.g., `number`), and actual received value if safe to display (e.g., `received value: 123`) (AGENTS.md 5.1 Rule 10).
3. WHEN enum validation fails, THE Error_Message SHALL list: field name, all allowed values (e.g., `allowed: "completed" | "in-progress" | "archived"`), and received value (e.g., `received: "pending"`) (AGENTS.md 5.1 Rule 10).
4. WHEN date format validation fails, THE Error_Message SHALL show: field name, expected format (ISO `YYYY-MM-DD`), and received format (e.g., `received: "01/15/2026"`) (AGENTS.md 5.1 Rule 10).

#### Verification Steps

1. Create invalid content examples for each error type (type mismatch, enum, date format, string length, etc.).
2. Run validation and capture error messages.
3. Verify each error message includes file path, field name, expected format, and received value.
4. Test that error messages are concise but sufficient for a content editor to understand the fix.
5. Create error message examples document for content editors.

---

### Requirement 18: Create Seed Content (1 Example Per Type) with Validation Tests

**User Story:**
As a developer, I want seed content files for each content type, so that I can test the entire content pipeline and demonstrate structure.

#### Acceptance Criteria

1. WHEN the project is first built, THE Seed_Content SHALL include one valid example for each content type: SiteConfig (site.json), Project (project.mdx), Certification (certification.mdx), BlogPost (blog.mdx) (AGENTS.md 4.3).
2. THE Seed_Content SHALL strictly follow the format and validation rules defined in AGENTS.md 4.3 and Section 5 (AGENTS.md 4.3, 5.1–5.4).
3. WHEN seed content is loaded via loaders, THE Validation SHALL pass without errors (AGENTS.md 5.1 Rule 7).
4. THE Seed_Content_Files SHALL be located at: `content/site.json`, `content/projects/example-project.mdx`, `content/certifications/example-certification.mdx`, `content/blog/example-blog-post.mdx` (AGENTS.md 3).
5. WHEN getProjects(), getCertifications(), and getBlogPosts() are called after build, THE Loaders SHALL return the seed content objects successfully (TRD.md 4.1).

#### Verification Steps

1. Create `content/site.json` matching AGENTS.md 4.3 example.
2. Create `content/projects/example-project.mdx` with valid frontmatter and Markdown documentation.
3. Create `content/certifications/example-certification.mdx` with valid frontmatter.
4. Create `content/blog/example-blog-post.mdx` with valid frontmatter.
5. Run `npm run build`; verify no validation errors.
6. Test loaders in `npm test`; verify seed content loads successfully.
7. Verify seed content appears in `getProjects()`, `getCertifications()`, and `getBlogPosts()` results.

---

### Requirement 19: Implement Content Validation Test Suite

**User Story:**
As a QA engineer, I want a comprehensive test suite validating all content schemas and rules, so that regressions are caught before build.

#### Acceptance Criteria

1. THE Test_Suite SHALL include test cases for each validation rule in AGENTS.md Section 5 (universal, project, certification, blog) (AGENTS.md 5.1–5.4).
2. THE Test_Suite SHALL verify schema validation for: required fields present, optional fields handled correctly, enum values validated, date formats enforced, URL formats validated (AGENTS.md 5.1–5.4).
3. THE Test_Suite SHALL verify loader functions: getProjects(), getProjectBySlug(), getCertifications(), getBlogPosts(), getBlogPostBySlug(), getSiteConfig() all return expected types (TRD.ms 4.1).
4. THE Test_Suite SHALL verify content constraint logic: featured project count ≤ 3, draft posts excluded, date ordering enforced, slug uniqueness enforced (AGENTS.md 5.2–5.4).
5. THE Test_Suite SHALL include boundary value tests: title min/max length, summary min/max, reading time range, featured count limits (AGENTS.md 5.2, 5.4).
6. THE Test_Suite SHALL include negative tests: invalid slugs, invalid enums, malformed dates, broken links, missing required fields (AGENTS.md 5.1 Rule 7).
7. WHEN `npm test` is executed, THE Test_Suite SHALL run and pass with zero failures (TRD.md 8.1).

#### Verification Steps

1. Create `tests/content-validation.test.ts` with validation test cases.
2. Create `tests/content-loaders.test.ts` with loader function tests.
3. Create `tests/validation-rules.test.ts` with rule-specific tests (slug, date, URL, enum).
4. Write at least 5 test cases per validation rule (positive and negative).
5. Run `npm test` and verify all tests pass.
6. Run `npm test -- --coverage` and verify test coverage > 80% for content modules.

---

### Requirement 20: Ensure TypeScript Strict Mode Compliance Throughout M2

**User Story:**
As a code quality owner, I want TypeScript strict mode enforced across M2 code, so that type safety is guaranteed and implicit-any errors are eliminated.

#### Acceptance Criteria

1. WHEN TypeScript compiler is run with `npm run typecheck`, THE Compiler SHALL run with `strict: true` in `tsconfig.json` (AGENTS.md 6.1 Rule 7, TRD.md 8.1).
2. WHEN code is type-checked, THE Compiler SHALL report zero errors and zero warnings related to: implicit `any`, non-null assertions (`!`), unsafe type assertions, missing types (AGENTS.md 6.1 Rule 7).
3. WHEN a file imports content types, THE Importer SHALL use types derived from Zod via `z.infer<>`, not duplicate type definitions (AGENTS.md 6.1 Rule 5).
4. WHEN functions have parameters or return values, THE Function_Signature SHALL include explicit type annotations; implicit types not permitted (AGENTS.md 6.1 Rule 7).
5. WHEN linting is run with `npm run lint`, THE Linter SHALL enforce strict TypeScript rules via ESLint rules (e.g., `@typescript-eslint/no-explicit-any`, `@typescript-eslint/no-non-null-assertion`) (AGENTS.md 6.1 Rule 7).

#### Verification Steps

1. Verify `tsconfig.json` has `"strict": true`.
2. Run `npm run typecheck`; verify zero errors and warnings.
3. Run `npm run lint`; verify zero TypeScript linting errors.
4. Create a test file with non-null assertion (e.g., `const x = value!;`).
5. Run `npm run typecheck`; verify error is reported.
6. Remove the assertion; run typecheck; verify error is resolved.
7. Run full verification: `npm ci && npm run lint && npm run typecheck && npm test && npm run build`.

---

## Document Summary

This M2 requirements document specifies 20 EARS-formatted requirements organized across 7 categories:

1. **Zod Schema Validators** (Req 1–4): Enum and type schemas with strict validation
2. **Content Loaders** (Req 5–7): Type-safe functions for loading SiteConfig, Projects, Certifications, and BlogPosts
3. **Validation Rules Enforcement** (Req 9–13): Slug, date, URL validation; featured count; draft exclusion
4. **Markdown Rendering** (Req 14): Markdown to HTML pipeline with syntax highlighting and security
5. **Type Inference** (Req 15): No duplicate types; all derived from Zod schemas
6. **Build-Time Validation** (Req 16–17): Content validation failure stops build with descriptive errors
7. **Testing & Content** (Req 18–20): Seed content, comprehensive test suite, TypeScript strict mode

All requirements reference AGENTS.md, PRD.md, and TRD.md as the single source of truth. No requirements duplicate content definitions or schema structures. All error messages include file path, field name, expected format, and received value per AGENTS.md Rule 5.1.10.

The complete M2 implementation ensures that all content is validated before static generation, types are type-safe via Zod inference, and the build fails fast with actionable errors when content is invalid.
