# M2.G4: Project Schemas & Loaders

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete `ProjectFrontmatterSchema` and `ProjectSchema` in `src/content/schemas/project.ts` enforcing all validation constraints from `AGENTS.md` Section 5.2 (title 3–100 chars, summary 20–280 chars, lowercase slug, `startedAt` $\le$ `completedAt`, displayOrder requirement for featured projects, and `##` heading requirement in documentation). Implement `gray-matter` parsing and project loaders (`getProjects()`, `getProjectBySlug()`, `validateFeaturedCount()`) in `src/content/loaders/projects.ts`. Re-export types via `src/types/content.ts` and author comprehensive unit tests covering sorting, slug resolution, and collection-level constraints (featured count $\le$ 3).

## Goal Success Criteria

- ✓ `gray-matter` installed in dependencies for frontmatter parsing
- ✓ `src/content/schemas/project.ts` defines and exports `ProjectMetricsSchema`, `ProjectFrontmatterSchema`, `ProjectSchema`, and inferred types
- ✓ Cross-field validation enforces `startedAt` $\le$ `completedAt` when `completedAt` is present
- ✓ `ProjectSchema` enforces that `documentation` contains at least one `##` heading
- ✓ `src/content/loaders/projects.ts` implements `getProjects()`, `getProjectBySlug()`, and `validateFeaturedCount()`
- ✓ `getProjects()` returns projects sorted by `displayOrder` ascending, then `startedAt` descending
- ✓ `validateFeaturedCount()` throws an actionable error if more than 3 projects have `featured: true`
- ✓ `src/types/content.ts` re-exports `Project`, `ProjectFrontmatter`, and `ProjectMetrics`
- ✓ All unit tests pass with zero errors; `npm run typecheck` exits 0

## Prerequisites

- Goal M2.G1, M2.G2, and M2.G3 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/content/schemas/utils.ts` and `src/content/schemas/enums.ts` exist and compile

---

## Tasks

### M2.G4.T1: Install `gray-matter` and Type Definitions

**Objective:** Install `gray-matter` to enable YAML frontmatter extraction from MDX files.

**Acceptance Criteria:**
- ✓ `gray-matter` added to `dependencies` in `package.json`
- ✓ `@types/gray-matter` installed if needed, or types verified via native declarations
- ✓ `npm install` completes cleanly with no peer dependency errors

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Install `gray-matter` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm install gray-matter
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.dependencies."gray-matter") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.2, Req 12.8

---

### M2.G4.T2: Implement `ProjectFrontmatterSchema` in `src/content/schemas/project.ts`

**Objective:** Author `ProjectMetricsSchema` and `ProjectFrontmatterSchema` enforcing field types, boundaries, and cross-field date ordering.

**Acceptance Criteria:**
- ✓ `ProjectMetricsSchema` enforces non-empty `label` and `value`
- ✓ `ProjectFrontmatterSchema` enforces:
  - `title`: `TitleSchema` (3–100 chars after trim)
  - `summary`: `SummarySchema` (20–280 chars after trim)
  - `slug`: `SlugSchema` (lowercase alphanumeric + hyphens)
  - `status`: `ProjectStatusSchema`
  - `role`: non-empty string
  - `startedAt`: `IsoDateStringSchema`
  - `completedAt`: nullable `IsoDateStringSchema`
  - `technologies`: array of non-empty strings with at least 1 item
  - `tags`: array of strings
  - `repositoryUrl`, `liveDemoUrl`, `documentationUrl`: nullable `HttpsUrlSchema`
  - `featured`: boolean
  - `displayOrder`: non-negative integer
  - `metrics`: array of `ProjectMetricsSchema`
- ✓ Cross-field refinement enforces `startedAt` $\le$ `completedAt` when `completedAt` is not null
- ✓ Cross-field refinement enforces that `featured: true` requires an explicit `displayOrder`

**Prerequisites:**
- M2.G4.T1 completed
- Target file: `src/content/schemas/project.ts`

**Implementation Details:**

Write the frontmatter schema using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { z } from 'zod';
import { ProjectStatusSchema } from './enums';
import {
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  TitleSchema,
  SummarySchema,
} from './utils';

/**
 * Metric measurement associated with a portfolio project.
 * AGENTS.md 4.2: ProjectMetrics
 */
export const ProjectMetricsSchema = z.object({
  label: z.string().trim().min(1, 'Metric label must not be empty'),
  value: z.string().trim().min(1, 'Metric value must not be empty'),
});
export type ProjectMetrics = z.infer<typeof ProjectMetricsSchema>;

/**
 * Project frontmatter validation schema.
 * AGENTS.md 4.2 & 5.2
 */
export const ProjectFrontmatterSchema = z
  .object({
    title: TitleSchema,
    summary: SummarySchema,
    slug: SlugSchema,
    status: ProjectStatusSchema,
    role: z.string().trim().min(1, 'Role must not be empty'),
    startedAt: IsoDateStringSchema,
    completedAt: IsoDateStringSchema.nullable(),
    technologies: z
      .array(z.string().trim().min(1, 'Technology item must not be empty'))
      .min(1, 'At least 1 technology is required'),
    tags: z.array(z.string().trim()),
    repositoryUrl: HttpsUrlSchema.nullable(),
    liveDemoUrl: HttpsUrlSchema.nullable(),
    documentationUrl: HttpsUrlSchema.nullable(),
    featured: z.boolean(),
    displayOrder: z.number().int().nonnegative('Display order must be a non-negative integer'),
    metrics: z.array(ProjectMetricsSchema),
  })
  .superRefine((data, ctx) => {
    // AGENTS.md 5.2: startedAt must not be later than completedAt when completedAt is present
    if (data.completedAt !== null && data.startedAt > data.completedAt) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: `'startedAt' (${data.startedAt}) must not be later than 'completedAt' (${data.completedAt})`,
        path: ['startedAt'],
      });
    }

    // AGENTS.md 5.2: featured projects must have displayOrder
    if (data.featured && (data.displayOrder === undefined || data.displayOrder === null)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Featured projects must have an explicit displayOrder',
        path: ['displayOrder'],
      });
    }
  });

export type ProjectFrontmatter = z.infer<typeof ProjectFrontmatterSchema>;
'@ | Set-Content "src\content\schemas\project.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/schemas/project.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.3, Req 3.6, Req 3.7, Req 15.1

---

### M2.G4.T3: Implement Complete `ProjectSchema` with Markdown Heading Enforcement

**Objective:** Extend `ProjectFrontmatterSchema` with the `documentation: string` field and validate that documentation contains at least one `##` heading per `AGENTS.md` Section 5.2.

**Acceptance Criteria:**
- ✓ `ProjectSchema` extends `ProjectFrontmatterSchema` with `documentation: z.string()`
- ✓ Refinement checks that `documentation` contains at least one Markdown `## ` heading (or `##` at start of line)
- ✓ Export inferred type `Project`
- ✓ Module compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G4.T2 completed
- Target file: `src/content/schemas/project.ts`

**Implementation Details:**

Append `ProjectSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

/**
 * Complete Project entity schema including Markdown documentation body.
 * AGENTS.md 4.2 & 5.2: Project Markdown documentation must contain at least one ## heading.
 */
export const ProjectSchema = ProjectFrontmatterSchema.and(
  z.object({
    documentation: z.string().min(1, 'Documentation body must not be empty'),
  })
).superRefine((data, ctx) => {
  const hasHeading2 = /^##\s+[^\r\n]+/m.test(data.documentation);
  if (!hasHeading2) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Project Markdown documentation must contain at least one level-2 heading (##)',
      path: ['documentation'],
    });
  }
});

export type Project = z.infer<typeof ProjectSchema>;
'@
Add-Content -Path "src\content\schemas\project.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/schemas/project.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.5, Req 15.1

---

### M2.G4.T4: Author `getProjects()` and Helper Loaders in `src/content/loaders/projects.ts`

**Objective:** Implement `getProjects()`, `getProjectBySlug()`, and `validateFeaturedCount()` in `src/content/loaders/projects.ts`.

**Acceptance Criteria:**
- ✓ `getProjects(projectsDir?: string): Promise<Project[]>` scans directory for `.mdx` files
- ✓ Frontmatter and markdown body are extracted using `gray-matter`
- ✓ Every file is validated against `ProjectSchema`
- ✓ Projects are returned sorted by `displayOrder` ascending, then `startedAt` descending
- ✓ Enforces slug uniqueness across all project files in the collection
- ✓ `getProjectBySlug(slug: string, projectsDir?: string): Promise<Project | null>` returns matching project or null
- ✓ `validateFeaturedCount(projects: Project[]): void` throws error if count of `featured: true` projects exceeds 3

**Prerequisites:**
- M2.G4.T3 completed
- Target file: `src/content/loaders/projects.ts`

**Implementation Details:**

Write the project loaders using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { ZodError } from 'zod';
import { ProjectSchema, type Project } from '../schemas/project';
import {
  ValidationError,
  formatZodError,
  formatValidationError,
  renderErrorReport,
} from '../errors/handler';

const DEFAULT_PROJECTS_DIR = path.join(process.cwd(), 'content', 'projects');

/**
 * Validates that at most 3 projects are marked as featured.
 * AGENTS.md 5.2: At most 3 projects may have featured: true at any time.
 */
export function validateFeaturedCount(projects: Project[]): void {
  const featured = projects.filter((p) => p.featured);
  if (featured.length > 3) {
    const list = featured.map((p) => `  - ${p.slug} (displayOrder: ${p.displayOrder})`).join('\n');
    throw new Error(
      `Content validation failed: Featured project count exceeds maximum of 3 (found ${featured.length}):\n${list}`
    );
  }
}

/**
 * Loads, validates, and sorts all portfolio projects.
 *
 * @param projectsDir - Optional directory path for test fixtures.
 * @returns Sorted array of validated Project objects.
 */
export async function getProjects(projectsDir = DEFAULT_PROJECTS_DIR): Promise<Project[]> {
  let fileNames: string[];

  try {
    const entries = await fs.readdir(projectsDir);
    fileNames = entries.filter((file) => file.endsWith('.mdx'));
  } catch (error) {
    const err = formatValidationError(
      projectsDir,
      `Directory not found or unreadable: ${error instanceof Error ? error.message : String(error)}`
    );
    throw new Error(`Content validation failed:\n${renderErrorReport([err])}`);
  }

  const projects: Project[] = [];
  const errors: ValidationError[] = [];
  const seenSlugs = new Map<string, string>();

  for (const fileName of fileNames) {
    const filePath = path.join(projectsDir, fileName);

    try {
      const fileContent = await fs.readFile(filePath, 'utf-8');
      const { data: frontmatter, content: rawDocumentation } = matter(fileContent);

      const combinedPayload = {
        ...frontmatter,
        documentation: rawDocumentation,
      };

      const project = ProjectSchema.parse(combinedPayload);

      // AGENTS.md 5.1 Rule 1: slug must be unique within its content collection
      if (seenSlugs.has(project.slug)) {
        errors.push(
          formatValidationError(
            filePath,
            `Duplicate slug '${project.slug}' detected. Already defined in '${seenSlugs.get(project.slug)}'`,
            'slug'
          )
        );
      } else {
        seenSlugs.set(project.slug, filePath);
        projects.push(project);
      }
    } catch (error) {
      if (error instanceof ZodError) {
        errors.push(...formatZodError(error, filePath));
      } else {
        errors.push(
          formatValidationError(
            filePath,
            `Failed to parse project file: ${error instanceof Error ? error.message : String(error)}`
          )
        );
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Content validation failed:\n${renderErrorReport(errors)}`);
  }

  // TRD.md 4.1: Sort projects by displayOrder ascending, then startedAt descending
  return projects.sort((a, b) => {
    if (a.displayOrder !== b.displayOrder) {
      return a.displayOrder - b.displayOrder;
    }
    return b.startedAt.localeCompare(a.startedAt);
  });
}

/**
 * Loads a single project by slug. Returns null if not found.
 */
export async function getProjectBySlug(slug: string, projectsDir = DEFAULT_PROJECTS_DIR): Promise<Project | null> {
  const allProjects = await getProjects(projectsDir);
  const matched = allProjects.find((p) => p.slug === slug);
  return matched ?? null;
}
'@ | Set-Content "src\content\loaders\projects.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/loaders/projects.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.3, Req 6.4, Req 6.5, Req 6.6, Req 6.8, Req 8.5, Req 13.1, Req 13.2

---

### M2.G4.T5: Populate Canonical Root `content/projects/example-project.mdx`

**Objective:** Write the seed project file in `content/projects/example-project.mdx` matching the specification in `AGENTS.md` Section 4.3.

**Acceptance Criteria:**
- ✓ File `content/projects/example-project.mdx` exists
- ✓ Frontmatter contains valid metadata matching all constraints
- ✓ Contains valid metrics array
- ✓ Documentation contains `## Build Documentation` heading

**Prerequisites:**
- M2.G4.T4 completed
- Target file: `content/projects/example-project.mdx`

**Implementation Details:**

Write the project seed file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "content\projects")) {
    New-Item -ItemType Directory -Path "content\projects" -Force | Out-Null
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

Explain the problem, constraints, architecture decisions, implementation approach, verification, and outcome.
'@ | Set-Content "content\projects\example-project.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "content\projects\example-project.mdx"
```
Expected output: `True`

**Satisfies Requirements:** Req 18.1, Req 18.2, Req 18.4

---

### M2.G4.T6: Author Unit Tests for `ProjectSchema` (`tests/unit/schemas/project.test.ts`)

**Objective:** Author tests in `tests/unit/schemas/project.test.ts` verifying frontmatter boundary limits, date ordering (`startedAt` $\le$ `completedAt`), and `##` heading detection.

**Acceptance Criteria:**
- ✓ Tests valid project payload passes parsing
- ✓ Tests rejection when `title` is $< 3$ or $> 100$ characters
- ✓ Tests rejection when `summary` is $< 20$ or $> 280$ characters
- ✓ Tests rejection when `startedAt` is after `completedAt`
- ✓ Tests rejection when `documentation` lacks an `##` heading
- ✓ Tests rejection when `technologies` array is empty

**Prerequisites:**
- M2.G4.T3 completed
- Target file: `tests/unit/schemas/project.test.ts`

**Implementation Details:**

Write `tests/unit/schemas/project.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { ProjectSchema, ProjectFrontmatterSchema } from '@/content/schemas/project';

describe('ProjectSchema Validation', () => {
  const validProjectData = {
    title: 'Valid Project Title',
    summary: 'This is a valid project summary that easily satisfies the minimum 20 characters requirement.',
    slug: 'valid-project',
    status: 'completed',
    role: 'Lead Architect',
    startedAt: '2026-01-01',
    completedAt: '2026-03-01',
    technologies: ['Next.js', 'TypeScript'],
    tags: ['web'],
    repositoryUrl: 'https://github.com/example/repo',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: true,
    displayOrder: 1,
    metrics: [{ label: 'Performance', value: '100%' }],
    documentation: '## Architectural Overview\n\nDetailed implementation notes.',
  };

  it('accepts a fully compliant project payload', () => {
    const result = ProjectSchema.safeParse(validProjectData);
    expect(result.success).toBe(true);
  });

  describe('Date ordering constraint (AGENTS.md 5.2)', () => {
    it('rejects when startedAt is later than completedAt', () => {
      const invalid = {
        ...validProjectData,
        startedAt: '2026-04-01',
        completedAt: '2026-03-01',
      };
      const result = ProjectSchema.safeParse(invalid);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("must not be later than 'completedAt'");
      }
    });

    it('accepts when startedAt equals completedAt', () => {
      const valid = {
        ...validProjectData,
        startedAt: '2026-03-01',
        completedAt: '2026-03-01',
      };
      expect(ProjectSchema.safeParse(valid).success).toBe(true);
    });

    it('accepts completedAt as null for in-progress projects', () => {
      const inProgress = {
        ...validProjectData,
        status: 'in-progress',
        completedAt: null,
      };
      expect(ProjectSchema.safeParse(inProgress).success).toBe(true);
    });
  });

  describe('Documentation heading constraint (AGENTS.md 5.2)', () => {
    it('rejects documentation without at least one ## heading', () => {
      const noH2 = {
        ...validProjectData,
        documentation: '# Heading 1 Only\n\nParagraph text.',
      };
      const result = ProjectSchema.safeParse(noH2);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain('level-2 heading (##)');
      }
    });

    it('accepts documentation containing a valid ## heading', () => {
      const withH2 = {
        ...validProjectData,
        documentation: 'Introductory text.\n\n## Implementation Details\n\nCode explanation.',
      };
      expect(ProjectSchema.safeParse(withH2).success).toBe(true);
    });
  });

  it('rejects project with empty technologies array', () => {
    const emptyTech = {
      ...validProjectData,
      technologies: [],
    };
    expect(ProjectSchema.safeParse(emptyTech).success).toBe(false);
  });
});
'@ | Set-Content "tests\unit\schemas\project.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/schemas/project.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.5, Req 19.1, Req 19.4

---

### M2.G4.T7: Author Unit Tests for Project Loaders (`tests/unit/loaders/projects.test.ts`)

**Objective:** Write loader tests for `getProjects()` and `getProjectBySlug()` validating directory reading, frontmatter extraction, sorting, and duplicate slug detection.

**Acceptance Criteria:**
- ✓ Tests `getProjects()` reads fixture directory and returns sorted projects
- ✓ Tests `getProjectBySlug()` returns correct project for valid slug
- ✓ Tests `getProjectBySlug()` returns `null` for unknown slug
- ✓ Tests duplicate slug detection throws validation error listing both files

**Prerequisites:**
- M2.G4.T4 completed
- Target file: `tests/unit/loaders/projects.test.ts`

**Implementation Details:**

Write `tests/unit/loaders/projects.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import path from 'path';
import fs from 'fs/promises';
import { getProjects, getProjectBySlug } from '@/content/loaders/projects';

describe('Project Loaders', () => {
  const fixturesDir = path.join(process.cwd(), 'tests', 'fixtures', 'projects');
  const tempDir = path.join(process.cwd(), 'tests', 'fixtures', 'temp-projects');

  it('loads valid project fixture and resolves content', async () => {
    const projects = await getProjects(fixturesDir);
    expect(projects.length).toBeGreaterThanOrEqual(1);

    const first = projects[0];
    expect(first?.slug).toBe('example-project');
    expect(first?.documentation).toContain('## Build Documentation');
  });

  it('retrieves project by slug correctly', async () => {
    const project = await getProjectBySlug('example-project', fixturesDir);
    expect(project).not.toBeNull();
    expect(project?.title).toBe('Example Portfolio Project');
  });

  it('returns null when slug does not exist', async () => {
    const project = await getProjectBySlug('non-existent-slug', fixturesDir);
    expect(project).toBeNull();
  });

  it('throws descriptive error on duplicate slug within collection', async () => {
    await fs.mkdir(tempDir, { recursive: true });

    const fileContent = `---
title: "Project Alpha"
summary: "This is a valid summary for testing duplicate slug validation."
slug: "duplicate-slug"
status: "completed"
role: "Engineer"
startedAt: "2026-01-01"
completedAt: null
technologies: ["TypeScript"]
tags: ["test"]
repositoryUrl: null
liveDemoUrl: null
documentationUrl: null
featured: false
displayOrder: 1
metrics: []
---

## Section Heading

Body content.
`;

    await fs.writeFile(path.join(tempDir, 'p1.mdx'), fileContent, 'utf-8');
    await fs.writeFile(path.join(tempDir, 'p2.mdx'), fileContent, 'utf-8');

    try {
      await expect(getProjects(tempDir)).rejects.toThrowError(/Duplicate slug 'duplicate-slug' detected/);
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
    }
  });
});
'@ | Set-Content "tests\unit\loaders\projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/loaders/projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.5, Req 6.6, Req 8.5, Req 9.3, Req 19.3

---

### M2.G4.T8: Author Tests for `validateFeaturedCount()`

**Objective:** Write tests validating the collection-level constraint that at most 3 projects may have `featured: true`.

**Acceptance Criteria:**
- ✓ Pass when featured projects count is $\le 3$
- ✓ Throws actionable error listing project slugs when featured count $> 3$
- ✓ Tests pass in test runner

**Prerequisites:**
- M2.G4.T4 completed
- Target file: `tests/unit/loaders/projects.test.ts`

**Implementation Details:**

Append the featured count test suite to `tests/unit/loaders/projects.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

  describe('validateFeaturedCount Constraint (AGENTS.md 5.2)', () => {
    const makeProject = (slug: string, featured: boolean, displayOrder: number): any => ({
      title: `Project ${slug}`,
      summary: 'Valid summary meeting length requirement for testing.',
      slug,
      status: 'completed',
      role: 'Dev',
      startedAt: '2026-01-01',
      completedAt: null,
      technologies: ['TS'],
      tags: [],
      repositoryUrl: null,
      liveDemoUrl: null,
      documentationUrl: null,
      featured,
      displayOrder,
      metrics: [],
      documentation: '## Heading\n\nDocs',
    });

    it('passes when featured projects count is 3 or fewer', () => {
      const { validateFeaturedCount } = require('@/content/loaders/projects');
      const projects = [
        makeProject('p1', true, 1),
        makeProject('p2', true, 2),
        makeProject('p3', true, 3),
        makeProject('p4', false, 4),
      ];

      expect(() => validateFeaturedCount(projects)).not.toThrow();
    });

    it('throws error when more than 3 projects are marked as featured', () => {
      const { validateFeaturedCount } = require('@/content/loaders/projects');
      const projects = [
        makeProject('p1', true, 1),
        makeProject('p2', true, 2),
        makeProject('p3', true, 3),
        makeProject('p4', true, 4),
      ];

      expect(() => validateFeaturedCount(projects)).toThrowError(/Featured project count exceeds maximum of 3 \(found 4\)/);
    });
  });
'@
$content = Get-Content "tests\unit\loaders\projects.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\loaders\projects.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/loaders/projects.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 19.4

---

### M2.G4.T9: Update Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Re-export `Project`, `ProjectFrontmatter`, and `ProjectMetrics` in `src/types/content.ts`.

**Acceptance Criteria:**
- ✓ Exports `Project`, `ProjectFrontmatter`, and `ProjectMetrics` from `@/content/schemas/project`
- ✓ Re-exports purely inferred types derived from Zod schemas
- ✓ No interface duplication exists
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G4.T3 completed
- Target file: `src/types/content.ts`

**Implementation Details:**

Update `src/types/content.ts` using PowerShell:
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

### M2.G4.T10: Checkpoint — Project Module Verification

**Objective:** Execute the complete verification suite across schemas, loaders, and test cases to ensure the project module is fully operational.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` executes all test suites (utils, enums, site, project) and passes
- ✓ Calling `getProjects()` on the root `content/projects` directory succeeds

**Prerequisites:**
- M2.G4.T1 through M2.G4.T9 completed

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

**Satisfies Requirements:** Req 3.1, Req 6.7, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\content\schemas\project.ts"
Test-Path "src\content\loaders\projects.ts"
Test-Path "content\projects\example-project.mdx"
npm run test -- tests/unit/schemas/project.test.ts tests/unit/loaders/projects.test.ts
npm run typecheck
```
Expected output:
- `True` for `project.ts` schema, `projects.ts` loader, and `example-project.mdx`
- Tests pass cleanly with 0 failures
- `npm run typecheck` exits with return code 0.