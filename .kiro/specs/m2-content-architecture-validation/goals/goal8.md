# M2.G8: Type Inference & Type Safety

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Solidify and audit TypeScript strict mode compliance across all content modules and types. Finalize `src/types/content.ts` as the canonical re-export barrel where every content contract is derived strictly via `z.infer<>` from Zod schemas. Audit the repository to ensure zero duplicated manual interface definitions exist (`AGENTS.md` Section 6.1 Rule 5), enforce zero `any` types and zero unjustified non-null assertions (`!`), and author automated type inference smoke tests validating strict assignment compatibility.

## Goal Success Criteria

- ✓ `src/types/content.ts` re-exports all canonical content contracts derived from Zod schemas
- ✓ Audit script confirms zero duplicate manual TypeScript `interface` or `type` definitions exist for content models
- ✓ Zero explicit `any`, zero implicit `any`, and zero non-null assertions (`!`) across `src/content/` and `src/types/`
- ✓ `npm run typecheck` passes with zero errors under strict mode (`strict: true`, `noUncheckedIndexedAccess: true`)
- ✓ Automated type assignability smoke test in `tests/unit/types/inference.test.ts` compiles and passes
- ✓ ESLint rules (`@typescript-eslint/no-explicit-any`, `@typescript-eslint/no-non-null-assertion`) exit cleanly with 0 errors

## Prerequisites

- Goals M2.G1 through M2.G7 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/types/content.ts` and all schema modules exist and compile

---

## Tasks

### M2.G8.T1: Finalize Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Audit and finalize `src/types/content.ts` ensuring all types from `AGENTS.md` Section 4.2 are cleanly re-exported via `z.infer<>`.

**Acceptance Criteria:**
- ✓ Exports `IsoDateString`
- ✓ Exports `ProjectStatus`, `CertificationCategory`, `EventType`, `ContactChannelType`
- ✓ Exports `ContactChannel`, `SocialLink`, `SiteProfile`, `SiteNavigationItem`, `SiteConfig`
- ✓ Exports `ProjectMetrics`, `ProjectFrontmatter`, `Project`
- ✓ Exports `CertificationFrontmatter`, `Certification`
- ✓ Exports `BlogPostFrontmatter`, `BlogPost`
- ✓ Contains zero manual `interface` declarations
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G7 completed
- Target file: `src/types/content.ts`

**Implementation Details:**

Write the finalized `src/types/content.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Canonical Content Contracts (Single Source of Truth)
 *
 * All types in this file are derived directly from Zod schemas via `z.infer<>`.
 * Per AGENTS.md Section 6.1 Rule 5, manual interface duplication is strictly prohibited.
 */

// Primitive and scalar types
export type { IsoDateString } from '@/content/schemas/utils';

// Canonical enumerations
export type {
  ProjectStatus,
  CertificationCategory,
  EventType,
  ContactChannelType,
} from '@/content/schemas/enums';

// Site configuration models
export type {
  SiteProfile,
  ContactChannel,
  SocialLink,
  SiteNavigationItem,
  SiteConfig,
} from '@/content/schemas/site';

// Project case study models
export type {
  ProjectMetrics,
  ProjectFrontmatter,
  Project,
} from '@/content/schemas/project';

// Certification and badge models
export type {
  CertificationFrontmatter,
  Certification,
} from '@/content/schemas/certification';

// Blog and participation log models
export type {
  BlogPostFrontmatter,
  BlogPost,
} from '@/content/schemas/blog-post';
'@ | Set-Content "src\types\content.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/types/content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 20.3

---

### M2.G8.T2: Update Root Types Barrel (`src/types/index.ts`)

**Objective:** Re-export all content contracts from `src/types/content.ts` through the root index barrel `src/types/index.ts`.

**Acceptance Criteria:**
- ✓ `src/types/index.ts` re-exports everything from `./content`
- ✓ Consumers can import via `@/types` or `@/types/content`
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G8.T1 completed
- Target file: `src/types/index.ts`

**Implementation Details:**

Write `src/types/index.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Root Application Types Barrel
 */

export * from './content';
'@ | Set-Content "src\types\index.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/types/index.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 20.3

---

### M2.G8.T3: Audit Repository for Duplicate Interface Definitions

**Objective:** Execute an automated script searching `src/` to verify that no manual interfaces duplicate content schemas (e.g., `interface Project`, `interface BlogPost`).

**Acceptance Criteria:**
- ✓ Audits all `.ts` and `.tsx` files in `src/`
- ✓ Fails if any manual `interface` declaration matches canonical content entity names (`SiteConfig`, `Project`, `Certification`, `BlogPost`)
- ✓ Reports PASS when zero duplicates exist

**Prerequisites:**
- M2.G8.T2 completed

**Implementation Details:**

Execute the interface audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$forbiddenPatterns = @(
    "interface\s+SiteConfig\b",
    "interface\s+SiteProfile\b",
    "interface\s+ContactChannel\b",
    "interface\s+Project\b",
    "interface\s+ProjectFrontmatter\b",
    "interface\s+Certification\b",
    "interface\s+BlogPost\b"
)

$files = Get-ChildItem -Path "src" -Recurse -Include *.ts, *.tsx
$foundViolations = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    foreach ($pat in $forbiddenPatterns) {
        if ($content -match $pat) {
            $foundViolations += "Violation in $($file.FullName): matches forbidden duplicate '$pat'"
        }
    }
}

if ($foundViolations.Count -eq 0) {
    "PASS"
} else {
    $foundViolations | ForEach-Object { Write-Error $_ }
    "FAIL"
}
```

**Validation:**
Expected output from the script above: `PASS`

**Satisfies Requirements:** Req 15.2, Req 15.5

---

### M2.G8.T4: Audit Repository for Prohibited `any` and Non-Null Assertions

**Objective:** Audit `src/content/` and `src/types/` to verify absence of explicit `any` types and non-null assertions (`!`).

**Acceptance Criteria:**
- ✓ Scans `src/content/` and `src/types/`
- ✓ Flags any occurrence of `: any`, `as any`, `<any>`, or non-null assertion `!` (excluding `!=` or `!==`)
- ✓ Confirms zero violations

**Prerequisites:**
- M2.G8.T3 completed

**Implementation Details:**

Execute the unsafe pattern audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = Get-ChildItem -Path "src\content", "src\types" -Recurse -Include *.ts, *.tsx
$violations = @()

foreach ($file in $files) {
    $lines = Get-Content $file.FullName
    $lineNum = 1
    foreach ($line in $lines) {
        # Check for explicit any
        if ($line -match ':\s*any\b|\bas\s+any\b|<any>') {
            $violations += "$($file.FullName):$lineNum contains explicit 'any': $line"
        }
        # Check for non-null assertion (identifier followed by ! not part of != or !!)
        if ($line -match '[a-zA-Z0-9_\)\]]!(?!=)') {
            $violations += "$($file.FullName):$lineNum contains non-null assertion '!': $line"
        }
        $lineNum++
    }
}

if ($violations.Count -eq 0) {
    "PASS"
} else {
    $violations | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

**Validation:**
Expected output from the script above: `PASS`

**Satisfies Requirements:** Req 15.4, Req 20.2

---

### M2.G8.T5: Author Type Assignability Smoke Tests (`tests/unit/types/inference.test.ts`)

**Objective:** Author compile-time type verification tests in `tests/unit/types/inference.test.ts` to assert that inferred types match expected schema shapes.

**Acceptance Criteria:**
- ✓ Directory `tests/unit/types` exists
- ✓ Test file imports types from `@/types/content`
- ✓ Validates that variables assigned valid shapes compile cleanly without type errors
- ✓ Uses TypeScript type assertions (`expectTypeOf` from Vitest) to check type equivalence
- ✓ Tests pass under `npm run test`

**Prerequisites:**
- M2.G8.T1 completed
- Target file: `tests/unit/types/inference.test.ts`

**Implementation Details:**

Create `tests/unit/types/inference.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\unit\types")) {
    New-Item -ItemType Directory -Path "tests\unit\types" -Force | Out-Null
}

@'
import { describe, it, expectTypeOf } from 'vitest';
import type {
  SiteConfig,
  Project,
  Certification,
  BlogPost,
  ProjectStatus,
  CertificationCategory,
  EventType,
} from '@/types/content';

describe('Type Inference Validation (z.infer<> SSOT)', () => {
  it('verifies SiteConfig property types match inferred contracts', () => {
    expectTypeOf<SiteConfig>().toHaveProperty('siteName').toBeString();
    expectTypeOf<SiteConfig>().toHaveProperty('profile').toBeObject();
    expectTypeOf<SiteConfig>().toHaveProperty('contactChannels').toBeArray();
  });

  it('verifies Project property types match inferred contracts', () => {
    expectTypeOf<Project>().toHaveProperty('slug').toBeString();
    expectTypeOf<Project>().toHaveProperty('status').toMatchTypeOf<ProjectStatus>();
    expectTypeOf<Project>().toHaveProperty('technologies').toBeArray();
    expectTypeOf<Project>().toHaveProperty('documentation').toBeString();
    expectTypeOf<Project>().toHaveProperty('featured').toBeBoolean();
  });

  it('verifies Certification property types match inferred contracts', () => {
    expectTypeOf<Certification>().toHaveProperty('slug').toBeString();
    expectTypeOf<Certification>().toHaveProperty('category').toMatchTypeOf<CertificationCategory>();
    expectTypeOf<Certification>().toHaveProperty('issuedAt').toBeString();
    expectTypeOf<Certification>().toHaveProperty('content').toBeString();
  });

  it('verifies BlogPost property types match inferred contracts', () => {
    expectTypeOf<BlogPost>().toHaveProperty('slug').toBeString();
    expectTypeOf<BlogPost>().toHaveProperty('eventType').toMatchTypeOf<EventType>();
    expectTypeOf<BlogPost>().toHaveProperty('readingTimeMinutes').toBeNumber();
    expectTypeOf<BlogPost>().toHaveProperty('draft').toBeBoolean();
    expectTypeOf<BlogPost>().toHaveProperty('content').toBeString();
  });
});
'@ | Set-Content "tests\unit\types\inference.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/types/inference.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.3, Req 20.3

---

### M2.G8.T6: Create Centralized Schemas Barrel (`src/content/schemas/index.ts`)

**Objective:** Author `src/content/schemas/index.ts` to provide a unified export point for all Zod schemas.

**Acceptance Criteria:**
- ✓ Exports all primitive validators from `./utils`
- ✓ Exports all enum schemas from `./enums`
- ✓ Exports `SiteConfigSchema` from `./site`
- ✓ Exports `ProjectSchema` and `ProjectFrontmatterSchema` from `./project`
- ✓ Exports `CertificationSchema` and `CertificationFrontmatterSchema` from `./certification`
- ✓ Exports `BlogPostSchema` and `BlogPostFrontmatterSchema` from `./blog-post`
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G8.T1 completed
- Target file: `src/content/schemas/index.ts`

**Implementation Details:**

Write `src/content/schemas/index.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Canonical Zod Content Schemas
 */

export * from './utils';
export * from './enums';
export * from './site';
export * from './project';
export * from './certification';
export * from './blog-post';
'@ | Set-Content "src\content\schemas\index.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/schemas/index.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 20.4

---

### M2.G8.T7: Create Centralized Loaders Barrel (`src/content/loaders/index.ts`)

**Objective:** Author `src/content/loaders/index.ts` to provide a clean export point for all typed loaders.

**Acceptance Criteria:**
- ✓ Exports `getSiteConfig` from `./site`
- ✓ Exports `getProjects`, `getProjectBySlug`, `validateFeaturedCount` from `./projects`
- ✓ Exports `getCertifications` from `./certifications`
- ✓ Exports `getBlogPosts`, `getBlogPostBySlug` from `./blog`
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G8.T1 completed
- Target file: `src/content/loaders/index.ts`

**Implementation Details:**

Write `src/content/loaders/index.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Canonical Content Loaders
 */

export * from './site';
export * from './projects';
export * from './certifications';
export * from './blog';
'@ | Set-Content "src\content\loaders\index.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/loaders/index.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 6.1, Req 7.1, Req 20.4

---

### M2.G8.T8: Verify Function Signature Return Type Annotations

**Objective:** Audit all loader functions and schema files to ensure explicit return types are declared on every exported function without implicit inference.

**Acceptance Criteria:**
- ✓ `getSiteConfig(): Promise<SiteConfig>` has explicit return type
- ✓ `getProjects(): Promise<Project[]>` has explicit return type
- ✓ `getProjectBySlug(): Promise<Project | null>` has explicit return type
- ✓ `getCertifications(): Promise<Certification[]>` has explicit return type
- ✓ `getBlogPosts(): Promise<BlogPost[]>` has explicit return type
- ✓ `getBlogPostBySlug(): Promise<BlogPost | null>` has explicit return type
- ✓ `renderMarkdown(): Promise<string>` has explicit return type

**Prerequisites:**
- M2.G8.T7 completed

**Implementation Details:**

Inspect loaders for explicit type annotations using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Get-ChildItem -Path "src\content\loaders\*.ts" | Select-String "export async function"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$res = Get-ChildItem -Path "src\content\loaders\*.ts" | Select-String "export async function"
$allHaveReturn = $true
foreach ($line in $res) {
    if ($line.Line -notmatch ':\s*Promise<') {
        $allHaveReturn = $false
        Write-Host "Missing return type: $($line.Line)"
    }
}
if ($allHaveReturn) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 20.4

---

### M2.G8.T9: Execute ESLint Strict Type-Checking Rules

**Objective:** Run `npm run lint` to enforce `@typescript-eslint/no-explicit-any`, `@typescript-eslint/no-non-null-assertion`, and `@typescript-eslint/no-unsafe-assignment` across `src/content/` and `src/types/`.

**Acceptance Criteria:**
- ✓ `npm run lint` runs without fatal configuration errors
- ✓ Reports 0 errors across `src/content/` and `src/types/`
- ✓ Exit code is 0

**Prerequisites:**
- M2.G8.T1 through M2.G8.T8 completed

**Implementation Details:**

Execute linting using PowerShell:
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

### M2.G8.T10: Checkpoint — Strict Type Safety Verification

**Objective:** Run `npm run typecheck` across the entire codebase to confirm 100% strict type safety compliance.

**Acceptance Criteria:**
- ✓ `npm run typecheck` (`tsc --noEmit`) passes with exit code 0
- ✓ No missing type declarations or implicit `any` errors reported
- ✓ All tests pass cleanly

**Prerequisites:**
- M2.G8.T1 through M2.G8.T9 completed

**Implementation Details:**

Execute typecheck and test runner via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\types\content.ts"
Test-Path "src\types\index.ts"
Test-Path "src\content\schemas\index.ts"
Test-Path "src\content\loaders\index.ts"
Test-Path "tests\unit\types\inference.test.ts"
npm run typecheck
npm run test -- tests/unit/types/inference.test.ts
```
Expected output:
- `True` for all path validations
- `npm run typecheck` exits with code 0
- Type inference tests pass with exit code 0.