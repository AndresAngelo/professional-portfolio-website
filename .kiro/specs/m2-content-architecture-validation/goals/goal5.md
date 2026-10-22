# M2.G5: Certification Schemas & Loaders

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete `CertificationFrontmatterSchema` and `CertificationSchema` in `src/content/schemas/certification.ts` enforcing all constraints from `AGENTS.md` Section 5.3 (title, issuer, category, `issuedAt`, optional `expiresAt` with `expiresAt` $\ge$ `issuedAt`, absolute HTTPS verification URL, paired badge image and alt text, displayOrder). Implement the `getCertifications()` loader in `src/content/loaders/certifications.ts` to read and sort credentials from `content/certifications/*.mdx`, re-export inferred types via `src/types/content.ts`, and author comprehensive unit tests covering all validation rules and edge cases.

## Goal Success Criteria

- ✓ `src/content/schemas/certification.ts` defines and exports `CertificationFrontmatterSchema`, `CertificationSchema`, and inferred types
- ✓ Cross-field validation enforces `expiresAt` $\ge$ `issuedAt` when `expiresAt` is provided
- ✓ Cross-field validation enforces that `badgeImageUrl` and `badgeImageAlt` are both present or both absent (null)
- ✓ Verification URLs enforce absolute HTTPS protocol
- ✓ `src/content/loaders/certifications.ts` implements `getCertifications()` returning credentials sorted by `displayOrder` ascending
- ✓ `src/types/content.ts` re-exports `Certification` and `CertificationFrontmatter` with zero duplicate TypeScript interfaces
- ✓ All unit tests in `tests/unit/schemas/certification.test.ts` and `tests/unit/loaders/certifications.test.ts` pass cleanly
- ✓ `npm run typecheck` passes with zero errors

## Prerequisites

- Goals M2.G1 through M2.G4 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/content/schemas/enums.ts` (`CertificationCategorySchema`) and `src/content/schemas/utils.ts` exist and compile
- `tests/fixtures/certifications/valid-certification.mdx` exists from M2.G1.T6

---

## Tasks

### M2.G5.T1: Implement `CertificationFrontmatterSchema` with Base Fields

**Objective:** Create `src/content/schemas/certification.ts` and author `CertificationFrontmatterSchema` enforcing baseline field types.

**Acceptance Criteria:**
- ✓ `title`: `TitleSchema` (3–100 characters after trim)
- ✓ `slug`: `SlugSchema` (lowercase alphanumeric + hyphens)
- ✓ `issuer`: non-empty string
- ✓ `category`: `CertificationCategorySchema`
- ✓ `issuedAt`: `IsoDateStringSchema`
- ✓ `expiresAt`: nullable `IsoDateStringSchema`
- ✓ `credentialId`: nullable string
- ✓ `verificationUrl`: nullable `HttpsUrlSchema`
- ✓ `badgeImageUrl`: nullable string (internal asset path starting with `/` or HTTPS URL)
- ✓ `badgeImageAlt`: nullable string
- ✓ `displayOrder`: non-negative integer

**Prerequisites:**
- M2.G4 completed
- Target file: `src/content/schemas/certification.ts`

**Implementation Details:**

Write the initial `certification.ts` module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';
import { CertificationCategorySchema } from './enums';
import {
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  TitleSchema,
} from './utils';

/**
 * Certification frontmatter validation schema.
 * AGENTS.md 4.2 & 5.3
 */
export const CertificationFrontmatterSchema = z
  .object({
    title: TitleSchema,
    slug: SlugSchema,
    issuer: z.string().trim().min(1, 'Issuer must not be empty'),
    category: CertificationCategorySchema,
    issuedAt: IsoDateStringSchema,
    expiresAt: IsoDateStringSchema.nullable(),
    credentialId: z.string().trim().nullable(),
    verificationUrl: HttpsUrlSchema.nullable(),
    badgeImageUrl: z
      .string()
      .trim()
      .refine(
        (val) => val === '' || val.startsWith('/') || val.startsWith('https://'),
        'Badge image URL must be an internal asset path starting with / or an absolute HTTPS URL'
      )
      .nullable(),
    badgeImageAlt: z.string().trim().nullable(),
    displayOrder: z.number().int().nonnegative('Display order must be a non-negative integer'),
  });

export type CertificationFrontmatter = z.infer<typeof CertificationFrontmatterSchema>;
'@ | Set-Content "src\content\schemas\certification.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/certification.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.3, Req 4.5, Req 15.1

---

### M2.G5.T2: Add Refinements for Date Ordering and Badge Image Pairing

**Objective:** Update `CertificationFrontmatterSchema` with `.superRefine()` rules enforcing `expiresAt` $\ge$ `issuedAt` and strict pairing of `badgeImageUrl` and `badgeImageAlt`.

**Acceptance Criteria:**
- ✓ Rejects when `expiresAt` is earlier than `issuedAt`
- ✓ Rejects when `badgeImageUrl` is non-null/non-empty but `badgeImageAlt` is null or empty
- ✓ Rejects when `badgeImageAlt` is non-null/non-empty but `badgeImageUrl` is null or empty
- ✓ Accepts when both badge image fields are null or both are non-empty
- ✓ Produces field-specific errors targeting `expiresAt`, `badgeImageUrl`, or `badgeImageAlt`

**Prerequisites:**
- M2.G5.T1 completed
- Target file: `src/content/schemas/certification.ts`

**Implementation Details:**

Update `CertificationFrontmatterSchema` with refinement rules using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';
import { CertificationCategorySchema } from './enums';
import {
  IsoDateStringSchema,
  SlugSchema,
  HttpsUrlSchema,
  TitleSchema,
} from './utils';

/**
 * Certification frontmatter validation schema.
 * AGENTS.md 4.2 & 5.3
 */
export const CertificationFrontmatterSchema = z
  .object({
    title: TitleSchema,
    slug: SlugSchema,
    issuer: z.string().trim().min(1, 'Issuer must not be empty'),
    category: CertificationCategorySchema,
    issuedAt: IsoDateStringSchema,
    expiresAt: IsoDateStringSchema.nullable(),
    credentialId: z.string().trim().nullable(),
    verificationUrl: HttpsUrlSchema.nullable(),
    badgeImageUrl: z
      .string()
      .trim()
      .refine(
        (val) => val === '' || val.startsWith('/') || val.startsWith('https://'),
        'Badge image URL must be an internal asset path starting with / or an absolute HTTPS URL'
      )
      .nullable(),
    badgeImageAlt: z.string().trim().nullable(),
    displayOrder: z.number().int().nonnegative('Display order must be a non-negative integer'),
  })
  .superRefine((data, ctx) => {
    // AGENTS.md 5.3: expiresAt, when present, must not be earlier than issuedAt
    if (data.expiresAt !== null && data.expiresAt < data.issuedAt) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: `'expiresAt' (${data.expiresAt}) must not be earlier than 'issuedAt' (${data.issuedAt})`,
        path: ['expiresAt'],
      });
    }

    // AGENTS.md 5.3: badgeImageUrl and badgeImageAlt must both be present or both be absent
    const hasImage = Boolean(data.badgeImageUrl && data.badgeImageUrl.trim().length > 0);
    const hasAlt = Boolean(data.badgeImageAlt && data.badgeImageAlt.trim().length > 0);

    if (hasImage && !hasAlt) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "When 'badgeImageUrl' is present, 'badgeImageAlt' must also be provided",
        path: ['badgeImageAlt'],
      });
    } else if (!hasImage && hasAlt) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "When 'badgeImageAlt' is present, 'badgeImageUrl' must also be provided",
        path: ['badgeImageUrl'],
      });
    }
  });

export type CertificationFrontmatter = z.infer<typeof CertificationFrontmatterSchema>;
'@ | Set-Content "src\content\schemas\certification.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/certification.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.2, Req 4.4

---

### M2.G5.T3: Implement Complete `CertificationSchema` with Optional Body Content

**Objective:** Append `CertificationSchema` extending frontmatter with `content: z.string()` to hold the markdown body.

**Acceptance Criteria:**
- ✓ `CertificationSchema` extends `CertificationFrontmatterSchema` with `content: z.string()`
- ✓ Body content is optional in business terms (empty string allowed) per `AGENTS.md` 4.2 & 4.3
- ✓ Export inferred type `Certification`
- ✓ Module compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G5.T2 completed
- Target file: `src/content/schemas/certification.ts`

**Implementation Details:**

Append `CertificationSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Complete Certification entity schema including optional supporting body text.
 * AGENTS.md 4.2: Certification
 */
export const CertificationSchema = CertificationFrontmatterSchema.and(
  z.object({
    content: z.string(),
  })
);

export type Certification = z.infer<typeof CertificationSchema>;
'@
Add-Content -Path "src\content\schemas\certification.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/certification.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 15.1

---

### M2.G5.T4: Author `getCertifications()` Loader in `src/content/loaders/certifications.ts`

**Objective:** Implement `getCertifications()` to scan `content/certifications/*.mdx`, parse frontmatter with `gray-matter`, validate with `CertificationSchema`, enforce slug uniqueness, and sort by `displayOrder` ascending.

**Acceptance Criteria:**
- ✓ Function `getCertifications(certificationsDir?: string): Promise<Certification[]>` implemented
- ✓ Defaults to `<projectRoot>/content/certifications`
- ✓ Enforces slug uniqueness within the certifications collection
- ✓ Returns certifications sorted by `displayOrder` ascending
- ✓ Errors format file path and offending fields using `renderErrorReport`

**Prerequisites:**
- M2.G5.T3 completed
- Target file: `src/content/loaders/certifications.ts`

**Implementation Details:**

Write the certifications loader using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { ZodError } from 'zod';
import { CertificationSchema, type Certification } from '../schemas/certification';
import {
  ValidationError,
  formatZodError,
  formatValidationError,
  renderErrorReport,
} from '../errors/handler';

const DEFAULT_CERTIFICATIONS_DIR = path.join(process.cwd(), 'content', 'certifications');

/**
 * Loads, validates, and sorts all certifications and badges.
 *
 * @param certificationsDir - Optional directory path for test fixtures.
 * @returns Sorted array of validated Certification objects.
 */
export async function getCertifications(
  certificationsDir = DEFAULT_CERTIFICATIONS_DIR
): Promise<Certification[]> {
  let fileNames: string[];

  try {
    const entries = await fs.readdir(certificationsDir);
    fileNames = entries.filter((file) => file.endsWith('.mdx'));
  } catch (error) {
    const err = formatValidationError(
      certificationsDir,
      `Directory not found or unreadable: ${error instanceof Error ? error.message : String(error)}`
    );
    throw new Error(`Content validation failed:\n${renderErrorReport([err])}`);
  }

  const certifications: Certification[] = [];
  const errors: ValidationError[] = [];
  const seenSlugs = new Map<string, string>();

  for (const fileName of fileNames) {
    const filePath = path.join(certificationsDir, fileName);

    try {
      const fileContent = await fs.readFile(filePath, 'utf-8');
      const { data: frontmatter, content: rawBody } = matter(fileContent);

      const combinedPayload = {
        ...frontmatter,
        content: rawBody,
      };

      const certification = CertificationSchema.parse(combinedPayload);

      // AGENTS.md 5.1 Rule 1: slug must be unique within its content collection
      if (seenSlugs.has(certification.slug)) {
        errors.push(
          formatValidationError(
            filePath,
            `Duplicate slug '${certification.slug}' detected. Already defined in '${seenSlugs.get(certification.slug)}'`,
            'slug'
          )
        );
      } else {
        seenSlugs.set(certification.slug, filePath);
        certifications.push(certification);
      }
    } catch (error) {
      if (error instanceof ZodError) {
        errors.push(...formatZodError(error, filePath));
      } else {
        errors.push(
          formatValidationError(
            filePath,
            `Failed to parse certification file: ${error instanceof Error ? error.message : String(error)}`
          )
        );
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Content validation failed:\n${renderErrorReport(errors)}`);
  }

  // TRD.md 4.1: Sort certifications by displayOrder ascending
  return certifications.sort((a, b) => a.displayOrder - b.displayOrder);
}
'@ | Set-Content "src\content\loaders\certifications.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/loaders/certifications.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.3, Req 7.4, Req 7.9, Req 7.10, Req 9.3

---

### M2.G5.T5: Populate Canonical Root `content/certifications/example-certification.mdx`

**Objective:** Write the seed certification file in `content/certifications/example-certification.mdx` matching `AGENTS.md` Section 4.3.

**Acceptance Criteria:**
- ✓ File `content/certifications/example-certification.mdx` exists
- ✓ Frontmatter contains valid issuer, category (`cloud`), dates, and verification URL
- ✓ Badge image and alt text are properly paired
- ✓ Passes `CertificationSchema.parse()` without error

**Prerequisites:**
- M2.G5.T4 completed
- Target file: `content/certifications/example-certification.mdx`

**Implementation Details:**

Write the seed file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "content\certifications")) {
    New-Item -ItemType Directory -Path "content\certifications" -Force | Out-Null
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

Optional supporting context for the certification.
'@ | Set-Content "content\certifications\example-certification.mdx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "content\certifications\example-certification.mdx"
```
Expected output: `True`

**Satisfies Requirements:** Req 18.1, Req 18.2, Req 18.4

---

### M2.G5.T6: Author Unit Tests for `CertificationSchema` (`tests/unit/schemas/certification.test.ts`)

**Objective:** Author tests in `tests/unit/schemas/certification.test.ts` verifying date ordering (`expiresAt` $\ge$ `issuedAt`), badge pairing rules, and HTTPS URL enforcement.

**Acceptance Criteria:**
- ✓ Tests valid certification payload passes
- ✓ Tests rejection when `expiresAt` is earlier than `issuedAt`
- ✓ Tests rejection when `badgeImageUrl` is set but `badgeImageAlt` is null
- ✓ Tests rejection when `badgeImageAlt` is set but `badgeImageUrl` is null
- ✓ Tests acceptance when both badge image and alt text are null
- ✓ Tests rejection of non-HTTPS verification URL

**Prerequisites:**
- M2.G5.T3 completed
- Target file: `tests/unit/schemas/certification.test.ts`

**Implementation Details:**

Write `tests/unit/schemas/certification.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import { CertificationSchema } from '@/content/schemas/certification';

describe('CertificationSchema Validation', () => {
  const validCertification = {
    title: 'Certified Cloud Architect',
    slug: 'certified-cloud-architect',
    issuer: 'Cloud Provider',
    category: 'cloud',
    issuedAt: '2026-01-15',
    expiresAt: '2029-01-15',
    credentialId: 'CERT-98765',
    verificationUrl: 'https://example.com/verify/98765',
    badgeImageUrl: '/images/certifications/cloud.png',
    badgeImageAlt: 'Certified Cloud Architect badge',
    displayOrder: 1,
    content: 'Notes on architectural certification syllabus.',
  };

  it('accepts a fully compliant certification payload', () => {
    const result = CertificationSchema.safeParse(validCertification);
    expect(result.success).toBe(true);
  });

  describe('Date ordering constraints (AGENTS.md 5.3)', () => {
    it('rejects when expiresAt is earlier than issuedAt', () => {
      const invalid = {
        ...validCertification,
        issuedAt: '2026-06-01',
        expiresAt: '2026-01-01',
      };
      const result = CertificationSchema.safeParse(invalid);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("must not be earlier than 'issuedAt'");
      }
    });

    it('accepts expiresAt equal to issuedAt', () => {
      const valid = {
        ...validCertification,
        issuedAt: '2026-01-15',
        expiresAt: '2026-01-15',
      };
      expect(CertificationSchema.safeParse(valid).success).toBe(true);
    });

    it('accepts expiresAt as null for non-expiring credentials', () => {
      const valid = {
        ...validCertification,
        expiresAt: null,
      };
      expect(CertificationSchema.safeParse(valid).success).toBe(true);
    });
  });

  describe('Badge image pairing constraints (AGENTS.md 5.3)', () => {
    it('rejects when badgeImageUrl is provided without badgeImageAlt', () => {
      const invalid = {
        ...validCertification,
        badgeImageUrl: '/images/badge.png',
        badgeImageAlt: null,
      };
      const result = CertificationSchema.safeParse(invalid);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("'badgeImageAlt' must also be provided");
      }
    });

    it('rejects when badgeImageAlt is provided without badgeImageUrl', () => {
      const invalid = {
        ...validCertification,
        badgeImageUrl: null,
        badgeImageAlt: 'Alt text present',
      };
      const result = CertificationSchema.safeParse(invalid);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("'badgeImageUrl' must also be provided");
      }
    });

    it('accepts when both badge image fields are null', () => {
      const valid = {
        ...validCertification,
        badgeImageUrl: null,
        badgeImageAlt: null,
      };
      expect(CertificationSchema.safeParse(valid).success).toBe(true);
    });
  });

  describe('Verification URL rules (AGENTS.md 5.3)', () => {
    it('rejects non-HTTPS verification URL', () => {
      const invalid = {
        ...validCertification,
        verificationUrl: 'http://example.com/insecure',
      };
      expect(CertificationSchema.safeParse(invalid).success).toBe(false);
    });

    it('accepts null verification URL when not configured', () => {
      const valid = {
        ...validCertification,
        verificationUrl: null,
      };
      expect(CertificationSchema.safeParse(valid).success).toBe(true);
    });
  });
});
'@ | Set-Content "tests\unit\schemas\certification.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/certification.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 19.1, Req 19.2

---

### M2.G5.T7: Author Unit Tests for `getCertifications()` Loader (`tests/unit/loaders/certifications.test.ts`)

**Objective:** Write loader tests validating file system reading, sorting by `displayOrder`, and duplicate slug detection in the certifications collection.

**Acceptance Criteria:**
- ✓ Tests `getCertifications()` loads fixture files and sorts ascending by `displayOrder`
- ✓ Tests error thrown on unreadable/missing directory
- ✓ Tests duplicate slug detection within the certifications directory
- ✓ All tests pass in test runner

**Prerequisites:**
- M2.G5.T4 completed
- Target file: `tests/unit/loaders/certifications.test.ts`

**Implementation Details:**

Write `tests/unit/loaders/certifications.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import path from 'path';
import fs from 'fs/promises';
import { getCertifications } from '@/content/loaders/certifications';

describe('getCertifications Loader', () => {
  const fixturesDir = path.join(process.cwd(), 'tests', 'fixtures', 'certifications');
  const tempDir = path.join(process.cwd(), 'tests', 'fixtures', 'temp-certifications');

  it('loads valid certification fixture and verifies parsed metadata', async () => {
    const certs = await getCertifications(fixturesDir);
    expect(certs.length).toBeGreaterThanOrEqual(1);

    const first = certs[0];
    expect(first?.slug).toBe('example-certification');
    expect(first?.issuer).toBe('Example Issuer');
    expect(first?.category).toBe('cloud');
  });

  it('sorts multiple certifications by displayOrder ascending', async () => {
    await fs.mkdir(tempDir, { recursive: true });

    const c1 = `---
title: "Cert Order 10"
slug: "cert-order-10"
issuer: "Issuer A"
category: "ai"
issuedAt: "2026-01-01"
expiresAt: null
credentialId: null
verificationUrl: null
badgeImageUrl: null
badgeImageAlt: null
displayOrder: 10
---
`;

    const c2 = `---
title: "Cert Order 2"
slug: "cert-order-2"
issuer: "Issuer B"
category: "security"
issuedAt: "2026-01-01"
expiresAt: null
credentialId: null
verificationUrl: null
badgeImageUrl: null
badgeImageAlt: null
displayOrder: 2
---
`;

    await fs.writeFile(path.join(tempDir, 'c1.mdx'), c1, 'utf-8');
    await fs.writeFile(path.join(tempDir, 'c2.mdx'), c2, 'utf-8');

    try {
      const certs = await getCertifications(tempDir);
      expect(certs.length).toBe(2);
      expect(certs[0]?.displayOrder).toBe(2);
      expect(certs[1]?.displayOrder).toBe(10);
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
    }
  });

  it('detects duplicate slugs within certifications collection', async () => {
    await fs.mkdir(tempDir, { recursive: true });

    const content = `---
title: "Duplicate Cert"
slug: "dup-cert"
issuer: "Issuer"
category: "data"
issuedAt: "2026-01-01"
expiresAt: null
credentialId: null
verificationUrl: null
badgeImageUrl: null
badgeImageAlt: null
displayOrder: 1
---
`;

    await fs.writeFile(path.join(tempDir, 'd1.mdx'), content, 'utf-8');
    await fs.writeFile(path.join(tempDir, 'd2.mdx'), content, 'utf-8');

    try {
      await expect(getCertifications(tempDir)).rejects.toThrowError(/Duplicate slug 'dup-cert' detected/);
    } finally {
      await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
    }
  });
});
'@ | Set-Content "tests\unit\loaders\certifications.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/certifications.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.3, Req 7.4, Req 9.3, Req 19.3

---

### M2.G5.T8: Update Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Re-export `Certification` and `CertificationFrontmatter` in `src/types/content.ts`.

**Acceptance Criteria:**
- ✓ Exports `Certification` and `CertificationFrontmatter` from `@/content/schemas/certification`
- ✓ Types are inferred directly via `z.infer<>`
- ✓ No manual type definition duplicates exist
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G5.T3 completed
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

### M2.G5.T9: Test Default Path Resolution of `getCertifications()`

**Objective:** Write a test confirming `getCertifications()` called without arguments reads `content/certifications/` and loads the root seed certification.

**Acceptance Criteria:**
- ✓ Calling `getCertifications()` with no arguments loads `content/certifications/`
- ✓ Resolves `example-certification.mdx` cleanly
- ✓ Passes in test runner

**Prerequisites:**
- M2.G5.T5 completed
- Target file: `tests/unit/loaders/certifications.test.ts`

**Implementation Details:**

Append the root path resolution test to `tests/unit/loaders/certifications.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  it('loads the default content/certifications directory when no path argument is supplied', async () => {
    const certs = await getCertifications();
    expect(certs.length).toBeGreaterThanOrEqual(1);

    const found = certs.find((c) => c.slug === 'example-certification');
    expect(found).toBeDefined();
    expect(found?.category).toBe('cloud');
  });
'@
$content = Get-Content "tests\unit\loaders\certifications.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\loaders\certifications.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/certifications.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 18.5

---

### M2.G5.T10: Checkpoint — Certification Module Verification

**Objective:** Execute the complete verification pipeline (`typecheck`, `lint`, `test`) ensuring all certification schemas and loaders integrate cleanly.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` executes all test suites without errors
- ✓ Zero `any` types or unsafe assertions

**Prerequisites:**
- M2.G5.T1 through M2.G5.T9 completed

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

**Satisfies Requirements:** Req 4.1, Req 7.9, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\content\schemas\certification.ts"
Test-Path "src\content\loaders\certifications.ts"
Test-Path "content\certifications\example-certification.mdx"
npm run test -- tests/unit/schemas/certification.test.ts tests/unit/loaders/certifications.test.ts
npm run typecheck
```
Expected output:
- `True` for `certification.ts` schema, `certifications.ts` loader, and `example-certification.mdx`
- Tests pass cleanly with 0 failures
- `npm run typecheck` exits with return code 0.