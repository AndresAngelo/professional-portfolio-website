# M2.G2: Enum Schemas

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Define all canonical enumeration schemas using Zod's `.enum()` constructor (`ProjectStatusSchema`, `CertificationCategorySchema`, `EventTypeSchema`, and `ContactChannelTypeSchema`). Export the corresponding inferred TypeScript types strictly via `z.infer<>`, wire re-exports through `src/types/content.ts`, and author comprehensive unit tests covering accepted values, rejected invalid inputs, and descriptive error message structures per `AGENTS.md` Section 4.2 and `requirements.md` Requirement 1.

## Goal Success Criteria

- ✓ `src/content/schemas/enums.ts` defines and exports all 4 enum schemas and their inferred types
- ✓ `ProjectStatusSchema` validates exact values: `"completed"`, `"in-progress"`, `"archived"`
- ✓ `CertificationCategorySchema` validates exact values: `"cloud"`, `"ai"`, `"security"`, `"frontend"`, `"backend"`, `"data"`, `"devops"`, `"professional"`
- ✓ `EventTypeSchema` validates exact values: `"meetup"`, `"hackathon"`, `"workshop"`, `"conference"`, `"learning"`, `"project-update"`
- ✓ `ContactChannelTypeSchema` validates exact values: `"email"`, `"linkedin"`, `"github"`, `"website"`, `"other"`
- ✓ Rejection of unlisted enum values produces descriptive errors listing the expected values
- ✓ `src/types/content.ts` re-exports all 4 inferred enum types with zero duplicate TypeScript interfaces
- ✓ `npm run typecheck` and `npm run test` pass with zero errors

## Prerequisites

- Goal M2.G1 completed successfully
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/content/schemas/utils.ts` and `src/types/content.ts` exist

---

## Tasks

### M2.G2.T1: Implement `ProjectStatusSchema` in `src/content/schemas/enums.ts`

**Objective:** Define the `ProjectStatusSchema` enum using Zod and derive the `ProjectStatus` type.

**Acceptance Criteria:**
- ✓ `src/content/schemas/enums.ts` exists
- ✓ `ProjectStatusSchema` defines `"completed"`, `"in-progress"`, and `"archived"` using `z.enum()`
- ✓ `ProjectStatus` type is inferred via `z.infer<typeof ProjectStatusSchema>`
- ✓ No fallback strings or loose union definitions used

**Prerequisites:**
- M2.G1 completed
- Target file: `src/content/schemas/enums.ts`

**Implementation Details:**

Write the initial `enums.ts` module with `ProjectStatusSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';

/**
 * Project delivery state.
 * AGENTS.md 4.2: "completed" | "in-progress" | "archived"
 */
export const ProjectStatusSchema = z.enum([
  'completed',
  'in-progress',
  'archived',
]);
export type ProjectStatus = z.infer<typeof ProjectStatusSchema>;
'@ | Set-Content "src\content\schemas\enums.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/enums.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.6, Req 15.1

---

### M2.G2.T2: Implement `CertificationCategorySchema` in `src/content/schemas/enums.ts`

**Objective:** Append the `CertificationCategorySchema` to `src/content/schemas/enums.ts` with all 8 canonical categories.

**Acceptance Criteria:**
- ✓ `CertificationCategorySchema` defines `"cloud"`, `"ai"`, `"security"`, `"frontend"`, `"backend"`, `"data"`, `"devops"`, `"professional"`
- ✓ `CertificationCategory` type is inferred via `z.infer<typeof CertificationCategorySchema>`
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G2.T1 completed
- Target file: `src/content/schemas/enums.ts`

**Implementation Details:**

Append `CertificationCategorySchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Certification or credential category.
 * AGENTS.md 4.2: "cloud" | "ai" | "security" | "frontend" | "backend" | "data" | "devops" | "professional"
 */
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
'@
Add-Content -Path "src\content\schemas\enums.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/enums.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 1.6, Req 15.1

---

### M2.G2.T3: Implement `EventTypeSchema` in `src/content/schemas/enums.ts`

**Objective:** Append `EventTypeSchema` with all 6 event categories to `src/content/schemas/enums.ts`.

**Acceptance Criteria:**
- ✓ `EventTypeSchema` defines `"meetup"`, `"hackathon"`, `"workshop"`, `"conference"`, `"learning"`, `"project-update"`
- ✓ `EventType` type is inferred via `z.infer<typeof EventTypeSchema>`
- ✓ Follows exact naming conventions from `AGENTS.md` Section 4.2

**Prerequisites:**
- M2.G2.T2 completed
- Target file: `src/content/schemas/enums.ts`

**Implementation Details:**

Append `EventTypeSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Community and participation activity event categories.
 * AGENTS.md 4.2: "meetup" | "hackathon" | "workshop" | "conference" | "learning" | "project-update"
 */
export const EventTypeSchema = z.enum([
  'meetup',
  'hackathon',
  'workshop',
  'conference',
  'learning',
  'project-update',
]);
export type EventType = z.infer<typeof EventTypeSchema>;
'@
Add-Content -Path "src\content\schemas\enums.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/enums.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.6, Req 15.1

---

### M2.G2.T4: Implement `ContactChannelTypeSchema` in `src/content/schemas/enums.ts`

**Objective:** Append `ContactChannelTypeSchema` with all 5 contact channels to `src/content/schemas/enums.ts`.

**Acceptance Criteria:**
- ✓ `ContactChannelTypeSchema` defines `"email"`, `"linkedin"`, `"github"`, `"website"`, `"other"`
- ✓ `ContactChannelType` type is inferred via `z.infer<typeof ContactChannelTypeSchema>`
- ✓ The complete `enums.ts` file parses and compiles without warnings

**Prerequisites:**
- M2.G2.T3 completed
- Target file: `src/content/schemas/enums.ts`

**Implementation Details:**

Append `ContactChannelTypeSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Public external contact channel classifications.
 * AGENTS.md 4.2: "email" | "linkedin" | "github" | "website" | "other"
 */
export const ContactChannelTypeSchema = z.enum([
  'email',
  'linkedin',
  'github',
  'website',
  'other',
]);
export type ContactChannelType = z.infer<typeof ContactChannelTypeSchema>;
'@
Add-Content -Path "src\content\schemas\enums.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/enums.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.4, Req 1.6, Req 15.1

---

### M2.G2.T5: Author Unit Tests for `ProjectStatusSchema`

**Objective:** Write tests in `tests/unit/schemas/enums.test.ts` verifying `ProjectStatusSchema` accepts all 3 valid states and rejects invalid values.

**Acceptance Criteria:**
- ✓ Validates `"completed"`, `"in-progress"`, and `"archived"` pass
- ✓ Rejects uppercase variants like `"Completed"`
- ✓ Rejects invalid status strings like `"pending"`, `"active"`, or `""`
- ✓ Error output lists expected enum choices

**Prerequisites:**
- M2.G2.T4 completed
- Target file: `tests/unit/schemas/enums.test.ts`

**Implementation Details:**

Create the test file with the `ProjectStatusSchema` suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import {
  ProjectStatusSchema,
  CertificationCategorySchema,
  EventTypeSchema,
  ContactChannelTypeSchema,
} from '@/content/schemas/enums';

describe('Enum Schemas Validation', () => {
  describe('ProjectStatusSchema', () => {
    it('accepts all canonical ProjectStatus values', () => {
      expect(ProjectStatusSchema.safeParse('completed').success).toBe(true);
      expect(ProjectStatusSchema.safeParse('in-progress').success).toBe(true);
      expect(ProjectStatusSchema.safeParse('archived').success).toBe(true);
    });

    it('rejects invalid or case-mismatched ProjectStatus values', () => {
      const result = ProjectStatusSchema.safeParse('pending');
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("Invalid enum value");
      }

      expect(ProjectStatusSchema.safeParse('Completed').success).toBe(false);
      expect(ProjectStatusSchema.safeParse('').success).toBe(false);
      expect(ProjectStatusSchema.safeParse(null).success).toBe(false);
    });
  });
});
'@ | Set-Content "tests\unit\schemas\enums.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/enums.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.5, Req 19.2

---

### M2.G2.T6: Author Unit Tests for `CertificationCategorySchema`

**Objective:** Append test cases for `CertificationCategorySchema` covering all 8 accepted values and rejection of invalid categories.

**Acceptance Criteria:**
- ✓ Validates all 8 categories: `"cloud"`, `"ai"`, `"security"`, `"frontend"`, `"backend"`, `"data"`, `"devops"`, `"professional"`
- ✓ Rejects unapproved values like `"database"`, `"mobile"`, `"management"`
- ✓ Rejection returns an invalid enum value issue

**Prerequisites:**
- M2.G2.T5 completed
- Target file: `tests/unit/schemas/enums.test.ts`

**Implementation Details:**

Append the `CertificationCategorySchema` suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  describe('CertificationCategorySchema', () => {
    it('accepts all 8 canonical CertificationCategory values', () => {
      const validCategories = [
        'cloud',
        'ai',
        'security',
        'frontend',
        'backend',
        'data',
        'devops',
        'professional',
      ];

      for (const category of validCategories) {
        expect(CertificationCategorySchema.safeParse(category).success).toBe(true);
      }
    });

    it('rejects invalid categories', () => {
      expect(CertificationCategorySchema.safeParse('mobile').success).toBe(false);
      expect(CertificationCategorySchema.safeParse('database').success).toBe(false);
      expect(CertificationCategorySchema.safeParse('Cloud').success).toBe(false);
      expect(CertificationCategorySchema.safeParse(123).success).toBe(false);
    });
  });
'@
$content = Get-Content "tests\unit\schemas\enums.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\schemas\enums.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/enums.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 1.5, Req 19.2

---

### M2.G2.T7: Author Unit Tests for `EventTypeSchema`

**Objective:** Append test cases for `EventTypeSchema` covering all 6 activity types and rejection of unapproved events.

**Acceptance Criteria:**
- ✓ Validates all 6 event types: `"meetup"`, `"hackathon"`, `"workshop"`, `"conference"`, `"learning"`, `"project-update"`
- ✓ Rejects unapproved types like `"webinar"`, `"seminar"`, `"podcast"`
- ✓ Rejects empty strings and numeric values

**Prerequisites:**
- M2.G2.T6 completed
- Target file: `tests/unit/schemas/enums.test.ts`

**Implementation Details:**

Append the `EventTypeSchema` suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  describe('EventTypeSchema', () => {
    it('accepts all 6 canonical EventType values', () => {
      const validEvents = [
        'meetup',
        'hackathon',
        'workshop',
        'conference',
        'learning',
        'project-update',
      ];

      for (const eventType of validEvents) {
        expect(EventTypeSchema.safeParse(eventType).success).toBe(true);
      }
    });

    it('rejects invalid event types', () => {
      expect(EventTypeSchema.safeParse('webinar').success).toBe(false);
      expect(EventTypeSchema.safeParse('interview').success).toBe(false);
      expect(EventTypeSchema.safeParse('HACKATHON').success).toBe(false);
      expect(EventTypeSchema.safeParse('').success).toBe(false);
    });
  });
'@
$content = Get-Content "tests\unit\schemas\enums.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\schemas\enums.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/enums.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.5, Req 19.2

---

### M2.G2.T8: Author Unit Tests for `ContactChannelTypeSchema`

**Objective:** Append test cases for `ContactChannelTypeSchema` covering all 5 allowed contact channels and rejection of invalid values.

**Acceptance Criteria:**
- ✓ Validates all 5 contact channels: `"email"`, `"linkedin"`, `"github"`, `"website"`, `"other"`
- ✓ Rejects unapproved channels like `"twitter"`, `"x"`, `"discord"`, `"phone"`
- ✓ Rejection fails `.safeParse()` with a structured ZodError

**Prerequisites:**
- M2.G2.T7 completed
- Target file: `tests/unit/schemas/enums.test.ts`

**Implementation Details:**

Append the `ContactChannelTypeSchema` suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  describe('ContactChannelTypeSchema', () => {
    it('accepts all 5 canonical ContactChannelType values', () => {
      const validChannels = [
        'email',
        'linkedin',
        'github',
        'website',
        'other',
      ];

      for (const channel of validChannels) {
        expect(ContactChannelTypeSchema.safeParse(channel).success).toBe(true);
      }
    });

    it('rejects invalid contact channels', () => {
      expect(ContactChannelTypeSchema.safeParse('twitter').success).toBe(false);
      expect(ContactChannelTypeSchema.safeParse('discord').success).toBe(false);
      expect(ContactChannelTypeSchema.safeParse('phone').success).toBe(false);
      expect(ContactChannelTypeSchema.safeParse('EMAIL').success).toBe(false);
    });
  });
'@
$content = Get-Content "tests\unit\schemas\enums.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\schemas\enums.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/enums.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.4, Req 1.5, Req 19.2

---

### M2.G2.T9: Re-Export Enum Types in `src/types/content.ts`

**Objective:** Update `src/types/content.ts` to re-export `ProjectStatus`, `CertificationCategory`, `EventType`, and `ContactChannelType` without redefining their types.

**Acceptance Criteria:**
- ✓ `src/types/content.ts` exports all 4 enum types from `@/content/schemas/enums`
- ✓ Derivation strictly uses `z.infer<>` from the schema module
- ✓ No interface or manual type alias duplicates the schema definitions

**Prerequisites:**
- M2.G2.T4 completed
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
'@ | Set-Content "src\types\content.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/types/content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 20.3

---

### M2.G2.T10: Checkpoint — Enum Schemas and Test Suite Verification

**Objective:** Run the complete quality verification cycle across the enum schemas, inferred types, and test suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with code 0
- ✓ `npm run lint` exits with code 0
- ✓ `npm run test` runs both utils and enums test suites and exits with code 0
- ✓ Total test count increases and zero failures are reported

**Prerequisites:**
- M2.G2.T1 through M2.G2.T9 completed

**Implementation Details:**

Execute the quality checks using PowerShell:
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

**Satisfies Requirements:** Req 1.6, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Get-Content "src\content\schemas\enums.ts" | Select-String "ProjectStatusSchema", "CertificationCategorySchema", "EventTypeSchema", "ContactChannelTypeSchema"
Get-Content "src\types\content.ts" | Select-String "ProjectStatus", "CertificationCategory", "EventType", "ContactChannelType"
npm run test -- tests/unit/schemas/enums.test.ts
npm run typecheck
```
Expected output:
- Matches returned for all 4 enum schema and type definitions
- Unit tests in `enums.test.ts` pass with exit code 0
- `npm run typecheck` exits with code 0.