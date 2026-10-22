# M2.G3: SiteConfig Schema & Loader

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the complete `SiteConfigSchema` in `src/content/schemas/site.ts` with all nested models (`ContactChannelSchema`, `SocialLinkSchema`, `SiteProfileSchema`, `SiteNavigationItemSchema`), enforce protocol rules (`mailto:` only for email, HTTPS for web channels), implement the `getSiteConfig()` loader in `src/content/loaders/site.ts` reading from `content/site.json`, re-export the inferred `SiteConfig` type in `src/types/content.ts`, and author comprehensive unit tests verifying valid loads, protocol constraints, missing file errors, and parse failures.

## Goal Success Criteria

- ✓ `src/content/schemas/site.ts` defines and exports `SiteConfigSchema` and inferred `SiteConfig`
- ✓ `ContactChannelSchema` validates that `email` uses `mailto:` and non-email channels use `https://`
- ✓ `src/content/loaders/site.ts` implements `getSiteConfig()` returning `Promise<SiteConfig>`
- ✓ Missing `content/site.json` or syntax errors throw descriptive, formatted errors identifying file path and field context
- ✓ `src/types/content.ts` re-exports `SiteConfig`, `SiteProfile`, `ContactChannel`, `SocialLink`, and `SiteNavigationItem` without manual type duplication
- ✓ All unit tests in `tests/unit/schemas/site.test.ts` and `tests/unit/loaders/site.test.ts` pass cleanly
- ✓ `npm run typecheck` passes with zero errors

## Prerequisites

- Goal M2.G1 and M2.G2 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/content/schemas/enums.ts` and `src/content/schemas/utils.ts` exist and compile
- `tests/fixtures/site.json` exists from M2.G1.T4

---

## Tasks

### M2.G3.T1: Implement Nested Schemas (`SiteProfile`, `SocialLink`, `SiteNavigationItem`)

**Objective:** Create `src/content/schemas/site.ts` and author the schemas for `SiteProfileSchema`, `SocialLinkSchema`, and `SiteNavigationItemSchema`.

**Acceptance Criteria:**
- ✓ `SiteProfileSchema` requires non-empty `name`, `professionalTitle`, `introduction`, `location`, and boolean `availableForOpportunities`
- ✓ `SocialLinkSchema` requires non-empty `label` and valid HTTPS `url`
- ✓ `SiteNavigationItemSchema` requires non-empty `label` and relative path starting with `/` or HTTPS `href`
- ✓ Module compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G2 completed
- Target file: `src/content/schemas/site.ts`

**Implementation Details:**

Write the nested schema definitions using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { z } from 'zod';
import { ContactChannelTypeSchema } from './enums';
import { HttpsUrlSchema } from './utils';

/**
 * Professional owner profile metadata.
 * AGENTS.md 4.2: SiteProfile
 */
export const SiteProfileSchema = z.object({
  name: z.string().trim().min(1, 'Name must not be empty'),
  professionalTitle: z.string().trim().min(1, 'Professional title must not be empty'),
  introduction: z.string().trim().min(1, 'Introduction must not be empty'),
  location: z.string().trim().min(1, 'Location must not be empty'),
  availableForOpportunities: z.boolean(),
});
export type SiteProfile = z.infer<typeof SiteProfileSchema>;

/**
 * External social link destination.
 * AGENTS.md 4.2: SocialLink
 */
export const SocialLinkSchema = z.object({
  label: z.string().trim().min(1, 'Label must not be empty'),
  url: HttpsUrlSchema,
});
export type SocialLink = z.infer<typeof SocialLinkSchema>;

/**
 * Site navigation bar link item.
 * AGENTS.md 4.2: SiteNavigationItem
 */
export const SiteNavigationItemSchema = z.object({
  label: z.string().trim().min(1, 'Label must not be empty'),
  href: z
    .string()
    .trim()
    .refine(
      (val) => val.startsWith('/') || val.startsWith('https://'),
      'Navigation href must be an internal path starting with / or an absolute HTTPS URL'
    ),
});
export type SiteNavigationItem = z.infer<typeof SiteNavigationItemSchema>;
'@ | Set-Content "src\content\schemas\site.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/site.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 15.1

---

### M2.G3.T2: Implement `ContactChannelSchema` with Protocol Enforcement

**Objective:** Append `ContactChannelSchema` enforcing `mailto:` protocol exclusively for email and `https://` protocol for all other channel types.

**Acceptance Criteria:**
- ✓ Requires `type` validated against `ContactChannelTypeSchema`
- ✓ Requires non-empty `label`
- ✓ `email` channel type requires `url` starting with `mailto:` followed by valid email characters
- ✓ `linkedin`, `github`, `website`, and `other` channel types require `https://` URL
- ✓ Requires boolean `isPrimary`
- ✓ Inferred type `ContactChannel` exported

**Prerequisites:**
- M2.G3.T1 completed
- Target file: `src/content/schemas/site.ts`

**Implementation Details:**

Append `ContactChannelSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Contact channel with protocol enforcement.
 * AGENTS.md 5.1 Rule 6: mailto: is permitted only for contact channels of type email.
 */
export const ContactChannelSchema = z
  .object({
    type: ContactChannelTypeSchema,
    label: z.string().trim().min(1, 'Label must not be empty'),
    url: z.string().trim().min(1, 'URL must not be empty'),
    isPrimary: z.boolean(),
  })
  .superRefine((data, ctx) => {
    if (data.type === 'email') {
      if (!data.url.startsWith('mailto:')) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Contact channels of type 'email' must use the 'mailto:' protocol",
          path: ['url'],
        });
      }
    } else {
      if (!data.url.startsWith('https://')) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: `Contact channels of type '${data.type}' must use an absolute HTTPS URL`,
          path: ['url'],
        });
      } else {
        const urlParsed = z.string().url().safeParse(data.url);
        if (!urlParsed.success) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: 'Must be a valid HTTPS URL',
            path: ['url'],
          });
        }
      }
    }
  });
export type ContactChannel = z.infer<typeof ContactChannelSchema>;
'@
Add-Content -Path "src\content\schemas\site.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/site.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.3, Req 2.5, Req 11.4

---

### M2.G3.T3: Implement Canonical `SiteConfigSchema`

**Objective:** Append `SiteConfigSchema` binding all sub-schemas to validate the complete `content/site.json` payload.

**Acceptance Criteria:**
- ✓ `SiteConfigSchema` enforces `siteName` (non-empty string)
- ✓ Enforces `siteUrl` as valid HTTPS URL or relative `/` root
- ✓ Integrates `profile: SiteProfileSchema`
- ✓ Enforces `contactChannels: z.array(ContactChannelSchema).min(1)`
- ✓ Integrates `socialLinks: z.array(SocialLinkSchema)`
- ✓ Integrates `navigation: z.array(SiteNavigationItemSchema)`
- ✓ Inferred type `SiteConfig` exported

**Prerequisites:**
- M2.G3.T2 completed
- Target file: `src/content/schemas/site.ts`

**Implementation Details:**

Append `SiteConfigSchema` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

/**
 * Root site and owner configuration schema.
 * AGENTS.md 4.2: SiteConfig
 */
export const SiteConfigSchema = z.object({
  siteName: z.string().trim().min(1, 'Site name must not be empty'),
  siteUrl: z
    .string()
    .trim()
    .refine(
      (val) => val.startsWith('/') || (val.startsWith('https://') && z.string().url().safeParse(val).success),
      'Site URL must be an absolute HTTPS URL or an internal path starting with /'
    ),
  profile: SiteProfileSchema,
  contactChannels: z.array(ContactChannelSchema).min(1, 'At least one contact channel is required'),
  socialLinks: z.array(SocialLinkSchema),
  navigation: z.array(SiteNavigationItemSchema),
});
export type SiteConfig = z.infer<typeof SiteConfigSchema>;
'@
Add-Content -Path "src\content\schemas\site.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/schemas/site.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.4, Req 15.1

---

### M2.G3.T4: Author `getSiteConfig()` Loader in `src/content/loaders/site.ts`

**Objective:** Implement `getSiteConfig()` to asynchronously read `content/site.json`, parse the JSON payload, validate against `SiteConfigSchema`, and format errors cleanly using the error handler.

**Acceptance Criteria:**
- ✓ Function `getSiteConfig(configPath?: string): Promise<SiteConfig>` implemented
- ✓ Defaults path to `<projectRoot>/content/site.json`
- ✓ Throws actionable errors on file not found, invalid JSON syntax, or schema violations
- ✓ Errors format file path and offending fields using `renderErrorReport`

**Prerequisites:**
- M2.G3.T3 completed
- Target file: `src/content/loaders/site.ts`

**Implementation Details:**

Write the loader module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import fs from 'fs/promises';
import path from 'path';
import { ZodError } from 'zod';
import { SiteConfigSchema, type SiteConfig } from '../schemas/site';
import { formatZodError, formatValidationError, renderErrorReport } from '../errors/handler';

const DEFAULT_SITE_CONFIG_PATH = path.join(process.cwd(), 'content', 'site.json');

/**
 * Loads and validates the global site configuration.
 *
 * @param configPath - Optional override path for testing fixtures.
 * @returns Validated SiteConfig object guaranteed to satisfy schema.
 */
export async function getSiteConfig(configPath = DEFAULT_SITE_CONFIG_PATH): Promise<SiteConfig> {
  let fileContent: string;

  try {
    fileContent = await fs.readFile(configPath, 'utf-8');
  } catch (error) {
    const err = formatValidationError(
      configPath,
      `File not found or unreadable: ${error instanceof Error ? error.message : String(error)}`
    );
    throw new Error(`Content validation failed:\n${renderErrorReport([err])}`);
  }

  let parsedJson: unknown;
  try {
    parsedJson = JSON.parse(fileContent);
  } catch (error) {
    const err = formatValidationError(
      configPath,
      `JSON parse error: ${error instanceof Error ? error.message : String(error)}`
    );
    throw new Error(`Content validation failed:\n${renderErrorReport([err])}`);
  }

  try {
    return SiteConfigSchema.parse(parsedJson);
  } catch (error) {
    if (error instanceof ZodError) {
      const formattedErrors = formatZodError(error, configPath);
      throw new Error(`Content validation failed:\n${renderErrorReport(formattedErrors)}`);
    }
    throw error;
  }
}
'@ | Set-Content "src\content\loaders\site.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/content/loaders/site.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 5.5

---

### M2.G3.T5: Populate Canonical Root `content/site.json`

**Objective:** Write the verified `content/site.json` file in the project content directory matching the example in `AGENTS.md` Section 4.3.

**Acceptance Criteria:**
- ✓ File `content/site.json` exists
- ✓ Contains Angelo Andres's valid profile information
- ✓ Contains valid primary email with `mailto:` protocol
- ✓ Contains valid social links and navigation array
- ✓ Passes `SiteConfigSchema.parse()` without error

**Prerequisites:**
- M2.G3.T3 completed
- Target file: `content/site.json`

**Implementation Details:**

Write `content/site.json` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
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
'@ | Set-Content "content\site.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
node -e "const fs = require('fs'); JSON.parse(fs.readFileSync('content/site.json', 'utf8')); console.log('PASS');"
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 18.1, Req 18.4

---

### M2.G3.T6: Author Schema Unit Tests (`tests/unit/schemas/site.test.ts`)

**Objective:** Author unit tests in `tests/unit/schemas/site.test.ts` validating `SiteConfigSchema`, nested structures, and email `mailto:` protocol enforcement.

**Acceptance Criteria:**
- ✓ Tests valid full site configuration
- ✓ Tests email channel rejection if URL does not begin with `mailto:`
- ✓ Tests non-email channel rejection if URL uses `mailto:` or insecure `http://`
- ✓ Tests rejection of empty profile name, missing title, and empty contact channels

**Prerequisites:**
- M2.G3.T3 completed
- Target file: `tests/unit/schemas/site.test.ts`

**Implementation Details:**

Create `tests/unit/schemas/site.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';
import { SiteConfigSchema, ContactChannelSchema } from '@/content/schemas/site';

describe('SiteConfigSchema Validation', () => {
  const validSiteConfig = {
    siteName: 'Angelo Andres',
    siteUrl: 'https://example.vercel.app',
    profile: {
      name: 'Angelo Andres',
      professionalTitle: 'Pipeline Lead',
      introduction: 'Specification-driven engineering.',
      location: 'Taguig, PH',
      availableForOpportunities: true,
    },
    contactChannels: [
      {
        type: 'email',
        label: 'Email Angelo',
        url: 'mailto:hello@example.com',
        isPrimary: true,
      },
    ],
    socialLinks: [
      {
        label: 'GitHub',
        url: 'https://github.com/example',
      },
    ],
    navigation: [
      { label: 'Home', href: '/' },
      { label: 'Projects', href: '/projects' },
    ],
  };

  it('accepts valid full SiteConfig payload', () => {
    const result = SiteConfigSchema.safeParse(validSiteConfig);
    expect(result.success).toBe(true);
  });

  describe('ContactChannel protocol rules (AGENTS.md Rule 5 & 6)', () => {
    it('accepts email channels using mailto: protocol', () => {
      const channel = {
        type: 'email',
        label: 'Email',
        url: 'mailto:test@example.com',
        isPrimary: true,
      };
      expect(ContactChannelSchema.safeParse(channel).success).toBe(true);
    });

    it('rejects email channels using https: protocol', () => {
      const channel = {
        type: 'email',
        label: 'Email',
        url: 'https://example.com/contact',
        isPrimary: true,
      };
      const result = ContactChannelSchema.safeParse(channel);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("mailto:");
      }
    });

    it('rejects non-email channels using mailto: protocol', () => {
      const channel = {
        type: 'linkedin',
        label: 'LinkedIn',
        url: 'mailto:linkedin@example.com',
        isPrimary: false,
      };
      const result = ContactChannelSchema.safeParse(channel);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.errors[0]?.message).toContain("absolute HTTPS URL");
      }
    });

    it('rejects non-email channels using insecure http:// protocol', () => {
      const channel = {
        type: 'github',
        label: 'GitHub',
        url: 'http://github.com/example',
        isPrimary: false,
      };
      expect(ContactChannelSchema.safeParse(channel).success).toBe(false);
    });
  });

  it('rejects configuration missing required contact channels array', () => {
    const invalid = { ...validSiteConfig, contactChannels: [] };
    const result = SiteConfigSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  it('rejects empty profile fields', () => {
    const invalid = {
      ...validSiteConfig,
      profile: {
        ...validSiteConfig.profile,
        name: '   ',
      },
    };
    expect(SiteConfigSchema.safeParse(invalid).success).toBe(false);
  });
});
'@ | Set-Content "tests\unit\schemas\site.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/schemas/site.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.3, Req 2.5, Req 19.2

---

### M2.G3.T7: Author Loader Unit Tests (`tests/unit/loaders/site.test.ts`)

**Objective:** Write loader tests validating successful loading from disk, handling of missing files, JSON parse failures, and schema error formatting.

**Acceptance Criteria:**
- ✓ Tests `getSiteConfig()` loads `tests/fixtures/site.json` successfully
- ✓ Tests non-existent file path throws descriptive file not found error
- ✓ Tests malformed JSON file throws descriptive syntax error
- ✓ Tests schema error formatting includes file path and offending field names

**Prerequisites:**
- M2.G3.T4 completed
- Target file: `tests/unit/loaders/site.test.ts`

**Implementation Details:**

Write `tests/unit/loaders/site.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "tests\unit\loaders")) {
    New-Item -ItemType Directory -Path "tests\unit\loaders" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import path from 'path';
import fs from 'fs/promises';
import { getSiteConfig } from '@/content/loaders/site';

describe('getSiteConfig Loader', () => {
  const fixturePath = path.join(process.cwd(), 'tests', 'fixtures', 'site.json');
  const tempInvalidJson = path.join(process.cwd(), 'tests', 'fixtures', 'invalid-syntax.json');
  const tempBadSchemaJson = path.join(process.cwd(), 'tests', 'fixtures', 'invalid-schema.json');

  it('loads and validates the site configuration fixture cleanly', async () => {
    const config = await getSiteConfig(fixturePath);
    expect(config.siteName).toBe('Angelo Andres');
    expect(config.profile.name).toBe('Angelo Andres');
    expect(config.contactChannels.length).toBeGreaterThanOrEqual(1);
  });

  it('throws descriptive error when target file does not exist', async () => {
    const missingPath = path.join(process.cwd(), 'tests', 'fixtures', 'non-existent.json');
    await expect(getSiteConfig(missingPath)).rejects.toThrowError(/File not found or unreadable/);
  });

  it('throws descriptive error on JSON parse failure', async () => {
    await fs.writeFile(tempInvalidJson, '{ "siteName": "Unclosed string }', 'utf-8');
    try {
      await expect(getSiteConfig(tempInvalidJson)).rejects.toThrowError(/JSON parse error/);
    } finally {
      await fs.unlink(tempInvalidJson).catch(() => {});
    }
  });

  it('throws descriptive error with field and file details on schema violation', async () => {
    const badData = {
      siteName: '',
      siteUrl: 'invalid-url',
    };
    await fs.writeFile(tempBadSchemaJson, JSON.stringify(badData), 'utf-8');
    try {
      await expect(getSiteConfig(tempBadSchemaJson)).rejects.toThrowError(/Content validation failed/);
    } finally {
      await fs.unlink(tempBadSchemaJson).catch(() => {});
    }
  });
});
'@ | Set-Content "tests\unit\loaders\site.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/site.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 19.3

---

### M2.G3.T8: Update Canonical Types Barrel (`src/types/content.ts`)

**Objective:** Re-export `SiteConfig`, `SiteProfile`, `ContactChannel`, `SocialLink`, and `SiteNavigationItem` in `src/types/content.ts`.

**Acceptance Criteria:**
- ✓ Exports `SiteConfig`, `SiteProfile`, `ContactChannel`, `SocialLink`, and `SiteNavigationItem` from `@/content/schemas/site`
- ✓ All types are inferred directly from Zod schemas
- ✓ Compiles cleanly with zero type errors

**Prerequisites:**
- M2.G3.T3 completed
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

### M2.G3.T9: Test Default Path Resolution of `getSiteConfig()`

**Objective:** Write a verification test confirming `getSiteConfig()` called with zero arguments resolves to the root `content/site.json` and loads successfully.

**Acceptance Criteria:**
- ✓ Calling `getSiteConfig()` with no arguments loads `content/site.json`
- ✓ Verified against root repository state
- ✓ Test passes in the test runner

**Prerequisites:**
- M2.G3.T5 completed
- Target file: `tests/unit/loaders/site.test.ts`

**Implementation Details:**

Append the root path resolution test to `tests/unit/loaders/site.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$appendCode = @'

  it('loads the default content/site.json file when no path parameter is supplied', async () => {
    const config = await getSiteConfig();
    expect(config.siteName).toBe('Angelo Andres');
    expect(config.navigation.length).toBeGreaterThan(0);
  });
'@
$content = Get-Content "tests\unit\loaders\site.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\loaders\site.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/loaders/site.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 18.5

---

### M2.G3.T10: Checkpoint — SiteConfig Module Verification

**Objective:** Run the full validation suite (`lint`, `typecheck`, `test`) to ensure SiteConfig schemas, loader, and types integrate seamlessly.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` passes all tests across utils, enums, schemas, and loaders
- ✓ Zero `any` types or unsafe assertions

**Prerequisites:**
- M2.G3.T1 through M2.G3.T9 completed

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

**Satisfies Requirements:** Req 2.6, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\content\schemas\site.ts"
Test-Path "src\content\loaders\site.ts"
Test-Path "content\site.json"
npm run test -- tests/unit/schemas/site.test.ts tests/unit/loaders/site.test.ts
npm run typecheck
```
Expected output:
- `True` for `site.ts` schema, `site.ts` loader, and `content/site.json`
- Tests pass cleanly with 0 failures
- `npm run typecheck` exits with return code 0.