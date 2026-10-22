Here is the complete, self-contained **`goal8.md`** file for Milestone 1, generated according to the Stage 3 Task Format Contract.

Save this content to:  
`.kiro/specs/m1-repository-foundation-toolchain/goal8.md`

***

# M1.G8: Path Aliases & Module Resolution

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Verify and solidify the `@/*` module path alias mapping (`@/*` $\rightarrow$ `./src/*`) across all execution environments: TypeScript compilation (`tsc`), bundler compilation (`next build`), test runtime (`vitest`), and IDE developer tooling. This prevents brittle relative paths (e.g., `../../components/ui/button`) and enforces architectural boundaries as required by `TRD.md` and `requirements.md` Requirement 2.8 and Requirement 5.6.

## Goal Success Criteria

- ✓ `tsconfig.json` has `baseUrl: "."` and `"@/*": ["./src/*"]` configured
- ✓ `vitest.config.ts` resolves `@/` alias to `<rootDir>/src`
- ✓ Next.js App Router natively resolves `@/` imports without additional configuration
- ✓ An integration helper function using `@/` path alias is created and exported
- ✓ Component and test suites importing via `@/*` pass type checking (`npm run typecheck`), testing (`npm run test`), and production compilation (`npm run build`) with zero resolution errors

## Prerequisites

- Goals M1.G1 through M1.G7 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `tsconfig.json` and `vitest.config.ts` exist and parse cleanly

---

## Tasks

### M1.G8.T1: Verify TypeScript Path Aliases in `tsconfig.json`

**Objective:** Audit `tsconfig.json` to confirm `baseUrl` and the `@/*` mapping are properly declared.

**Acceptance Criteria:**
- ✓ `compilerOptions.baseUrl` is `"."`
- ✓ `compilerOptions.paths["@/*"]` contains `"./src/*"`

**Prerequisites:**
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tsconfig.json`

**Implementation Details:**
Inspect the paths configuration using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tsconfig.json" -Raw | ConvertFrom-Json
$cfg.compilerOptions.paths
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tsconfig.json" -Raw | ConvertFrom-Json
if ($cfg.compilerOptions.baseUrl -eq "." -and $cfg.compilerOptions.paths."@/*"[0] -eq "./src/*") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.8

---

### M1.G8.T2: Verify Vitest Path Resolution in `vitest.config.ts`

**Objective:** Confirm that `vitest.config.ts` includes `resolve.alias` mapping `@` to the `src` directory using `path.resolve`.

**Acceptance Criteria:**
- ✓ `vitest.config.ts` contains `resolve.alias`
- ✓ `@` points to `path.resolve(__dirname, './src')`

**Prerequisites:**
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\vitest.config.ts`

**Implementation Details:**
Inspect `vitest.config.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Get-Content "vitest.config.ts" -Raw | Select-String "alias:"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$vcfg = Get-Content "vitest.config.ts" -Raw
if ($vcfg -match "'@':\s*path\.resolve\(__dirname,\s*'\./src'\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.6

---

### M1.G8.T3: Create Foundation Utility Module (`src/lib/utils.ts`)

**Objective:** Implement a foundational string utility function inside `src/lib/utils.ts` to act as an aliased import target.

**Acceptance Criteria:**
- ✓ Directory `src/lib/` exists
- ✓ `src/lib/utils.ts` exists
- ✓ Exports a strictly typed utility function `formatSiteTitle(name: string, title: string): string`
- ✓ Contains zero `any` types

**Prerequisites:**
- M1.G8.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\lib\utils.ts`

**Implementation Details:**
Create the utility file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "src\lib")) {
    New-Item -ItemType Directory -Path "src\lib"
}

@'
/**
 * Formats standard page titles with consistent brand suffix.
 */
export function formatSiteTitle(pageTitle: string, siteName: string = 'Angelo Andres'): string {
  if (!pageTitle.trim()) {
    return siteName;
  }
  return `${pageTitle} | ${siteName}`;
}
'@ | Set-Content "src\lib\utils.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "src\lib\utils.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.8, Req 6.7

---

### M1.G8.T4: Author Unit Test Utilizing `@/` Path Alias

**Objective:** Write a Vitest unit test in `tests/unit/utils.test.ts` that imports `formatSiteTitle` using `@/lib/utils`.

**Acceptance Criteria:**
- ✓ Directory `tests/unit/` exists
- ✓ `tests/unit/utils.test.ts` imports using `from '@/lib/utils'`
- ✓ Test suite validates utility string formatting logic

**Prerequisites:**
- M1.G8.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tests\unit\utils.test.ts`

**Implementation Details:**
Create the unit test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "tests\unit")) {
    New-Item -ItemType Directory -Path "tests\unit"
}

@'
import { describe, it, expect } from 'vitest';
import { formatSiteTitle } from '@/lib/utils';

describe('formatSiteTitle Utility (@/ alias resolution test)', () => {
  it('formats title with custom page name and brand suffix', () => {
    const result = formatSiteTitle('Projects', 'Portfolio');
    expect(result).toBe('Projects | Portfolio');
  });

  it('falls back to default site name when page title is empty', () => {
    const result = formatSiteTitle('');
    expect(result).toBe('Angelo Andres');
  });
});
'@ | Set-Content "tests\unit\utils.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "tests\unit\utils.test.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.5, Req 5.6

---

### M1.G8.T5: Validate Test Resolution (`npm run test`)

**Objective:** Execute `npm run test` to verify Vitest successfully resolves the `@/lib/utils` path alias during execution.

**Acceptance Criteria:**
- ✓ `npm run test` discovers `tests/unit/utils.test.ts`
- ✓ Test cases pass without "module not found" errors
- ✓ Exit code is 0

**Prerequisites:**
- M1.G8.T4 completed

**Implementation Details:**
Execute the test runner via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.9, Req 5.11

---

### M1.G8.T6: Use `@/` Alias in App Router Entrypoint (`src/app/page.tsx`)

**Objective:** Import and call `formatSiteTitle` from `@/lib/utils` inside `src/app/page.tsx` to verify Next.js runtime/compiler alias compatibility.

**Acceptance Criteria:**
- ✓ `src/app/page.tsx` contains `import { formatSiteTitle } from '@/lib/utils'`
- ✓ Function is invoked safely within the Server Component

**Prerequisites:**
- M1.G8.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\app\page.tsx`

**Implementation Details:**
Update `src/app/page.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { formatSiteTitle } from '@/lib/utils';

export default function HomePage() {
  const pageHeading = formatSiteTitle('Foundation Ready');

  return (
    <main className="min-h-screen bg-page text-text-primary p-8">
      <div className="max-w-4xl mx-auto space-y-4">
        <h1 className="text-heading-1 font-bold text-brand-primary">{pageHeading}</h1>
        <p className="text-body text-text-secondary">
          Next.js App Router, TypeScript strict mode, and Tailwind SGDS tokens verified.
        </p>
      </div>
    </main>
  );
}
'@ | Set-Content "src\app\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$page = Get-Content "src\app\page.tsx" -Raw
if ($page -match "from '@/lib/utils'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 2.8

---

### M1.G8.T7: Validate TypeScript Compilation with Alias (`npm run typecheck`)

**Objective:** Run `tsc --noEmit` to confirm TypeScript compiler resolves `@/` imports without error TS2307 ("Cannot find module").

**Acceptance Criteria:**
- ✓ `npm run typecheck` executes
- ✓ No import or module resolution errors are generated
- ✓ Exit code is 0

**Prerequisites:**
- M1.G8.T6 completed

**Implementation Details:**
Execute typecheck via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.8, Req 2.10, Req 11.3

---

### M1.G8.T8: Validate ESLint Resolution with Alias (`npm run lint`)

**Objective:** Confirm ESLint resolves `@/` import specifiers without triggering `import/no-unresolved` errors.

**Acceptance Criteria:**
- ✓ `npm run lint` completes without import resolution errors
- ✓ Exit code is 0

**Prerequisites:**
- M1.G8.T6 completed

**Implementation Details:**
Execute lint via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run lint
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run lint
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.10, Req 4.13

---

### M1.G8.T9: Validate Production Static Build with Alias (`npm run build`)

**Objective:** Execute `next build` to verify webpack/turbopack bundler compiles modules using `@/` path aliases into production assets in `out/`.

**Acceptance Criteria:**
- ✓ `npm run build` executes successfully
- ✓ Static output generated in `out/`
- ✓ Exit code is 0

**Prerequisites:**
- M1.G8.T6 completed

**Implementation Details:**
Execute static export build via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
if ($LASTEXITCODE -eq 0 -and (Test-Path "out")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 7.10, Req 11.5

---

### M1.G8.T10: Stage and Commit Path Alias Integration

**Objective:** Commit the validated alias utility, updated homepage, and unit tests to Git.

**Acceptance Criteria:**
- ✓ Staged files include `src/lib/utils.ts`, `src/app/page.tsx`, and `tests/unit/utils.test.ts`
- ✓ Git commit succeeds with message `"feat(m1): establish and verify path aliases and utilities"`

**Prerequisites:**
- M1.G8.T1 through M1.G8.T9 completed

**Implementation Details:**
Stage and commit changes using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git add src/lib/utils.ts src/app/page.tsx tests/unit/utils.test.ts
git commit -m "feat(m1): establish and verify path aliases and utilities"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$log = git log -1 --pretty=oneline
if ($log -match "feat\(m1\): establish and verify path aliases") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 11.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\lib\utils.ts"
Test-Path "tests\unit\utils.test.ts"
npm run typecheck
npm run test
npm run build
```
Expected output:
- `True` for utility and test paths
- Clean exit code 0 across `typecheck`, `test`, and `build`.