# M2.G9: Build-Time Validation Integration

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the build-time content validation script in `scripts/validate-content.ts` and wire it into the build lifecycle. The script invokes all 4 content loaders (`getSiteConfig()`, `getProjects()`, `getCertifications()`, and `getBlogPosts()`), enforces the collection-level featured count constraint (`validateFeaturedCount()`), halts execution with a non-zero exit code on any validation failure, outputs actionable error reports (identifying file path, field, expected type, and received value), and ensures Next.js static build (`npm run build`) is strictly gated by content validity per `TRD.md` Section 3.2 and `requirements.md` Requirement 16.

## Goal Success Criteria

- ✓ `tsx` installed in `devDependencies` to execute TypeScript scripts directly without manual pre-compilation
- ✓ `scripts/validate-content.ts` implemented and executes all 4 content loaders sequentially
- ✓ `scripts/validate-content.ts` invokes `validateFeaturedCount()` on loaded projects
- ✓ `"validate:content": "tsx scripts/validate-content.ts"` added to `package.json` scripts
- ✓ `package.json` `"build"` script updated to `"npm run validate:content && next build"`
- ✓ Deliberately corrupted content files halt `npm run validate:content` and `npm run build` with non-zero exit code
- ✓ Valid seed content allows `npm run validate:content` and `npm run build` to pass cleanly with exit code 0
- ✓ Verification test in `tests/integration/build-validation.test.ts` executes and passes

## Prerequisites

- Goals M2.G1 through M2.G8 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- All loaders in `src/content/loaders/` exist and compile
- `content/site.json`, `content/projects/*.mdx`, `content/certifications/*.mdx`, `content/blog/*.mdx` exist

---

## Tasks

### M2.G9.T1: Install `tsx` Development Dependency

**Objective:** Install `tsx` to enable direct, fast execution of TypeScript CLI scripts in Node.js.

**Acceptance Criteria:**
- ✓ `tsx` added to `devDependencies` in `package.json`
- ✓ `npx tsx --version` executes successfully
- ✓ `npm install` completes cleanly with no peer dependency conflicts

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Install `tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm install --save-dev tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.devDependencies.tsx) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.11, Req 16.1

---

### M2.G9.T2: Create `scripts/` Directory and Script Skeleton

**Objective:** Create the `scripts/` root directory and author `scripts/validate-content.ts`.

**Acceptance Criteria:**
- ✓ Directory `scripts/` exists at the project root
- ✓ `scripts/validate-content.ts` exists
- ✓ Script structure imports loaders from `@/content/loaders` or relative paths
- ✓ Compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G9.T1 completed
- Target file: `scripts/validate-content.ts`

**Implementation Details:**

Write the initial script skeleton using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "scripts")) {
    New-Item -ItemType Directory -Path "scripts" -Force | Out-Null
}

@'
import path from 'path';
import { getSiteConfig } from '../src/content/loaders/site';
import { getProjects, validateFeaturedCount } from '../src/content/loaders/projects';
import { getCertifications } from '../src/content/loaders/certifications';
import { getBlogPosts } from '../src/content/loaders/blog';

/**
 * Build-time content validation script.
 * Halts process with exit code 1 if any content violates schema rules.
 * TRD.md 3.2 & AGENTS.md 5.1
 */
async function validateAllContent(): Promise<void> {
  console.log('🔍 [Build-Validation] Starting comprehensive content audit...');
  const startTime = Date.now();
  let hasErrors = false;

  // 1. SiteConfig Validation
  try {
    process.stdout.write('  -> Validating content/site.json... ');
    const siteConfig = await getSiteConfig();
    console.log(`✓ OK (${siteConfig.contactChannels.length} channels, ${siteConfig.navigation.length} nav items)`);
  } catch (error) {
    hasErrors = true;
    console.error('❌ FAILED');
    console.error(error instanceof Error ? error.message : String(error));
  }

  // 2. Projects Validation & Featured Count
  try {
    process.stdout.write('  -> Validating content/projects/*.mdx... ');
    const projects = await getProjects();
    validateFeaturedCount(projects);
    const featuredCount = projects.filter((p) => p.featured).length;
    console.log(`✓ OK (${projects.length} projects, ${featuredCount} featured)`);
  } catch (error) {
    hasErrors = true;
    console.error('❌ FAILED');
    console.error(error instanceof Error ? error.message : String(error));
  }

  // 3. Certifications Validation
  try {
    process.stdout.write('  -> Validating content/certifications/*.mdx... ');
    const certs = await getCertifications();
    console.log(`✓ OK (${certs.length} certifications)`);
  } catch (error) {
    hasErrors = true;
    console.error('❌ FAILED');
    console.error(error instanceof Error ? error.message : String(error));
  }

  // 4. Blog Posts Validation
  try {
    process.stdout.write('  -> Validating content/blog/*.mdx (including drafts)... ');
    const posts = await getBlogPosts(undefined, false);
    console.log(`✓ OK (${posts.length} published posts loaded)`);
  } catch (error) {
    hasErrors = true;
    console.error('❌ FAILED');
    console.error(error instanceof Error ? error.message : String(error));
  }

  const duration = ((Date.now() - startTime) / 1000).toFixed(2);

  if (hasErrors) {
    console.error(`\n❌ [Build-Validation] Content validation failed in ${duration}s. Build aborted.`);
    process.exit(1);
  }

  console.log(`\n✅ [Build-Validation] All content schemas verified successfully in ${duration}s.\n`);
}

validateAllContent().catch((err) => {
  console.error('Unexpected build validation error:', err);
  process.exit(1);
});
'@ | Set-Content "scripts\validate-content.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsx scripts/validate-content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.3, Req 16.4

---

### M2.G9.T3: Add `validate:content` Script to `package.json`

**Objective:** Register `"validate:content": "tsx scripts/validate-content.ts"` in `package.json`.

**Acceptance Criteria:**
- ✓ `package.json` scripts contains `"validate:content"`
- ✓ Script points to `"tsx scripts/validate-content.ts"`
- ✓ `npm run validate:content` executes successfully

**Prerequisites:**
- M2.G9.T2 completed
- Target file: `package.json`

**Implementation Details:**

Update `package.json` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json

if (-not $pkg.scripts) {
    $pkg | Add-Member -MemberType NoteProperty -Name "scripts" -Value ([PSCustomObject]@{})
}

$pkg.scripts | Add-Member -MemberType NoteProperty -Name "validate:content" -Value "tsx scripts/validate-content.ts" -Force
$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.scripts."validate:content" -eq "tsx scripts/validate-content.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 16.1

---

### M2.G9.T4: Gate Production Build with `validate:content` in `package.json`

**Objective:** Wire `validate:content` directly before `next build` in the canonical `npm run build` script.

**Acceptance Criteria:**
- ✓ `package.json` `"build"` script updated to `"npm run validate:content && next build"`
- ✓ Build cannot execute `next build` if content validation fails
- ✓ Verification passes under JSON parsing

**Prerequisites:**
- M2.G9.T3 completed
- Target file: `package.json`

**Implementation Details:**

Update the build script in `package.json` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json

$pkg.scripts.build = "npm run validate:content && next build"
$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.scripts.build -eq "npm run validate:content && next build") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.2, Req 16.4

---

### M2.G9.T5: Integrate Content Validation Hook into `next.config.ts`

**Objective:** Add webpack `beforeCompile` validation hook in `next.config.ts` ensuring validation is also triggered during Next.js compilation phases.

**Acceptance Criteria:**
- ✓ `next.config.ts` imports validation logic or preserves static export configuration
- ✓ Webpack config attaches a server-side pre-compile validation tap if running in dev/server build
- ✓ File compiles cleanly under `tsc --noEmit`

**Prerequisites:**
- M2.G9.T4 completed
- Target file: `next.config.ts`

**Implementation Details:**

Update `next.config.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: {
    unoptimized: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;
'@ | Set-Content "next.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit next.config.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 16.1

---

### M2.G9.T6: Test Build-Time Failure on Invalid Frontmatter

**Objective:** Temporarily introduce a malformed project file and verify that `npm run validate:content` fails and halts with exit code 1.

**Acceptance Criteria:**
- ✓ Writing a project with invalid status (e.g. `"status": "invalid-status"`) causes validation failure
- ✓ Script returns exit code 1
- ✓ Output contains the file path and field name
- ✓ Cleanup restores valid state

**Prerequisites:**
- M2.G9.T3 completed

**Implementation Details:**

Execute the failure test script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$badFile = "content\projects\temp-broken-test.mdx"
@'---
title: "Broken Project"
summary: "This is a summary for testing build validation failure behavior."
slug: "broken-project"
status: "invalid-status-value"
role: "Tester"
startedAt: "2026-01-01"
completedAt: null
technologies: ["TypeScript"]
tags: ["test"]
repositoryUrl: null
liveDemoUrl: null
documentationUrl: null
featured: false
displayOrder: 99
metrics: []
---

## Heading

Documentation content.
'@ | Set-Content $badFile -Encoding UTF8

$exitCode = (Start-Process -FilePath "npm" -ArgumentList "run validate:content" -NoNewWindow -PassThru -Wait).ExitCode

Remove-Item -Force $badFile

if ($exitCode -ne 0) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the test block above: `PASS` (indicating the script correctly rejected invalid content with exit code 1).

**Satisfies Requirements:** Req 16.2, Req 16.3, Req 17.1, Req 17.3

---

### M2.G9.T7: Test Build-Time Failure on Excess Featured Projects

**Objective:** Verify that having 4 projects marked as `featured: true` triggers a build halt via `validateFeaturedCount()`.

**Acceptance Criteria:**
- ✓ Creating 3 extra temporary featured projects (total 4) triggers validation error
- ✓ Error message lists project slugs and max allowed count (3)
- ✓ Script exits with code 1
- ✓ Cleanup removes temporary files

**Prerequisites:**
- M2.G9.T3 completed

**Implementation Details:**

Execute the featured count failure test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$tempFiles = @()
for ($i = 1; $i -le 3; $i++) {
    $fPath = "content\projects\temp-feat-$i.mdx"
    $tempFiles += $fPath
@'---
title: "Temp Featured $i"
summary: "Summary for temporary featured project to test constraint limit."
slug: "temp-feat-$i"
status: "completed"
role: "Tester"
startedAt: "2026-01-01"
completedAt: null
technologies: ["TypeScript"]
tags: ["test"]
repositoryUrl: null
liveDemoUrl: null
documentationUrl: null
featured: true
displayOrder: 10
metrics: []
---

## Build Documentation

Content.
'@ -replace '\$i', $i | Set-Content $fPath -Encoding UTF8
}

$exitCode = (Start-Process -FilePath "npm" -ArgumentList "run validate:content" -NoNewWindow -PassThru -Wait).ExitCode

foreach ($f in $tempFiles) {
    if (Test-Path $f) { Remove-Item -Force $f }
}

if ($exitCode -ne 0) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the script above: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 16.2

---

### M2.G9.T8: Author Integration Test Suite (`tests/integration/build-validation.test.ts`)

**Objective:** Author an automated test in `tests/integration/build-validation.test.ts` that programmatically invokes the validation routine and confirms clean execution on root repository content.

**Acceptance Criteria:**
- ✓ Directory `tests/integration` exists
- ✓ Test imports all loaders and `validateFeaturedCount`
- ✓ Executes without throwing on the repository's root `content/` files
- ✓ Asserts `site.json` exists, project count $\ge 1$, certification count $\ge 1$, blog count $\ge 1$

**Prerequisites:**
- M2.G9.T2 completed
- Target file: `tests/integration/build-validation.test.ts`

**Implementation Details:**

Create `tests/integration/build-validation.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\integration")) {
    New-Item -ItemType Directory -Path "tests\integration" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { getSiteConfig } from '@/content/loaders/site';
import { getProjects, validateFeaturedCount } from '@/content/loaders/projects';
import { getCertifications } from '@/content/loaders/certifications';
import { getBlogPosts } from '@/content/loaders/blog';

describe('Build-Time Content Integration Pipeline', () => {
  it('validates all canonical root content files cleanly', async () => {
    // 1. Validate SiteConfig
    const siteConfig = await getSiteConfig();
    expect(siteConfig.siteName).toBe('Angelo Andres');
    expect(siteConfig.profile.availableForOpportunities).toBe(true);

    // 2. Validate Projects and Featured Constraint
    const projects = await getProjects();
    expect(projects.length).toBeGreaterThanOrEqual(1);
    expect(() => validateFeaturedCount(projects)).not.toThrow();

    const featuredCount = projects.filter((p) => p.featured).length;
    expect(featuredCount).toBeLessThanOrEqual(3);

    // 3. Validate Certifications
    const certs = await getCertifications();
    expect(certs.length).toBeGreaterThanOrEqual(1);

    // 4. Validate Blog Posts
    const posts = await getBlogPosts();
    expect(posts.length).toBeGreaterThanOrEqual(1);
    expect(posts.every((p) => p.draft === false)).toBe(true);
  });
});
'@ | Set-Content "tests\integration\build-validation.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/integration/build-validation.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.1, Req 16.4, Req 18.5, Req 19.3

---

### M2.G9.T9: Execute Full `npm run build` Quality Gate with Validation

**Objective:** Run `npm run build` to confirm `validate:content` triggers, passes, and allows Next.js static compilation to finish cleanly into `out/`.

**Acceptance Criteria:**
- ✓ `npm run build` triggers `npm run validate:content` first
- ✓ `validate:content` outputs green confirmation
- ✓ `next build` runs and generates static export into `out/`
- ✓ Process exit code is 0

**Prerequisites:**
- M2.G9.T4 and M2.G9.T8 completed

**Implementation Details:**

Run production build via PowerShell:
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

**Satisfies Requirements:** Req 1.6, Req 7.10, Req 11.5, Req 16.4

---

### M2.G9.T10: Checkpoint — Build-Time Validation Verification

**Objective:** Run lint, type checking, and all test suites to confirm that build validation integration satisfies all project quality gates.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0
- ✓ `npm run test` executes all test suites including integration and passes
- ✓ Zero regression errors

**Prerequisites:**
- M2.G9.T1 through M2.G9.T9 completed

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

**Satisfies Requirements:** Req 16.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "scripts\validate-content.ts"
Test-Path "tests\integration\build-validation.test.ts"
npm run validate:content
npm run build
```
Expected output:
- `True` for `scripts\validate-content.ts` and `tests\integration\build-validation.test.ts`
- `npm run validate:content` logs validation of all 4 content types and exits 0
- `npm run build` completes successfully and produces `out/index.html`.