***

# M1.G9: Directory Structure & Source Layout

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Create and enforce the complete directory taxonomy defined in `AGENTS.md` Section 3. This establishes designated locations for local Markdown/MDX content (`content/`), static assets (`public/`), UI components (`src/components/`), content loaders/schemas (`src/content/`), shared utilities (`src/lib/`), types (`src/types/`), and test suites (`tests/`). It places necessary barrel files or `.gitkeep` markers to preserve structure in version control without violating architectural boundaries (e.g., forbidding `pages/` or root `styles/`).

## Goal Success Criteria

- ✓ `content/` created with `projects/`, `certifications/`, and `blog/` subdirectories
- ✓ `public/` structured with `images/` (subdirectories: `projects/`, `certifications/`, `blog/`) and `files/`
- ✓ `src/components/` structured with `layout/`, `home/`, `projects/`, `certifications/`, `blog/`, and `ui/`
- ✓ `src/content/` structured with `loaders/`, `markdown/`, and `schemas/`
- ✓ `src/types/index.ts` created as a root type barrel
- ✓ Zero `pages/` directory exists (Pages Router strictly forbidden)
- ✓ Zero root `styles/` directory exists
- ✓ `npm run typecheck`, `npm run lint`, and `npm run test` pass with the complete directory tree intact

## Prerequisites

- Goals M1.G1 through M1.G8 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Toolchain, path aliases, and quality gates operational

---

## Tasks

### M1.G9.T1: Verify Absence of Prohibited Directories (`pages/`, `styles/`)

**Objective:** Confirm that the repository does not contain a legacy Next.js `pages/` directory or root `styles/` folder.

**Acceptance Criteria:**
- ✓ `pages/` directory does not exist
- ✓ `src/pages/` directory does not exist
- ✓ Root `styles/` directory does not exist

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\`

**Implementation Details:**
Execute the following verification script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "pages") { Remove-Item -Recurse -Force "pages" }
if (Test-Path "src\pages") { Remove-Item -Recurse -Force "src\pages" }
if (Test-Path "styles") { Remove-Item -Recurse -Force "styles" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$hasPages = (Test-Path "pages") -or (Test-Path "src\pages")
$hasStyles = (Test-Path "styles")
if (-not $hasPages -and -not $hasStyles) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.11, Req 6.12

---

### M1.G9.T2: Create `content/` Directory Taxonomy

**Objective:** Create the `content/` directory and its required subdirectories for MDX files with `.gitkeep` markers.

**Acceptance Criteria:**
- ✓ `content/projects/` directory exists
- ✓ `content/certifications/` directory exists
- ✓ `content/blog/` directory exists
- ✓ `.gitkeep` files present in each subdirectory to track them in Git

**Prerequisites:**
- M1.G9.T1 completed

**Implementation Details:**
Create the content directories using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$dirs = @(
    "content\projects",
    "content\certifications",
    "content\blog"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
    New-Item -ItemType File -Path (Join-Path $d ".gitkeep") -Force | Out-Null
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$p = Test-Path "content\projects\.gitkeep"
$c = Test-Path "content\certifications\.gitkeep"
$b = Test-Path "content\blog\.gitkeep"
if ($p -and $c -and $b) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2

---

### M1.G9.T3: Create `public/` Asset Directory Taxonomy

**Objective:** Establish the static asset directories in `public/` for images and downloadable files.

**Acceptance Criteria:**
- ✓ `public/images/projects/` exists
- ✓ `public/images/certifications/` exists
- ✓ `public/images/blog/` exists
- ✓ `public/files/` exists
- ✓ `.gitkeep` files present in each leaf directory

**Prerequisites:**
- M1.G9.T2 completed

**Implementation Details:**
Create the asset directories using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$dirs = @(
    "public\images\projects",
    "public\images\certifications",
    "public\images\blog",
    "public\files"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
    New-Item -ItemType File -Path (Join-Path $d ".gitkeep") -Force | Out-Null
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$ip = Test-Path "public\images\projects\.gitkeep"
$ic = Test-Path "public\images\certifications\.gitkeep"
$ib = Test-Path "public\images\blog\.gitkeep"
$pf = Test-Path "public\files\.gitkeep"
if ($ip -and $ic -and $ib -and $pf) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.3, Req 6.4, Req 6.5

---

### M1.G9.T4: Create `src/components/` Directory Taxonomy

**Objective:** Create the component folder hierarchy mapped to architectural domains.

**Acceptance Criteria:**
- ✓ `src/components/layout/` exists
- ✓ `src/components/home/` exists
- ✓ `src/components/projects/` exists
- ✓ `src/components/certifications/` exists
- ✓ `src/components/blog/` exists
- ✓ `src/components/ui/` exists
- ✓ `.gitkeep` files present in each leaf directory

**Prerequisites:**
- M1.G9.T3 completed

**Implementation Details:**
Create the component directories using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$dirs = @(
    "src\components\layout",
    "src\components\home",
    "src\components\projects",
    "src\components\certifications",
    "src\components\blog",
    "src\components\ui"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
    New-Item -ItemType File -Path (Join-Path $d ".gitkeep") -Force | Out-Null
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cl = Test-Path "src\components\layout\.gitkeep"
$ch = Test-Path "src\components\home\.gitkeep"
$cp = Test-Path "src\components\projects\.gitkeep"
$cc = Test-Path "src\components\certifications\.gitkeep"
$cb = Test-Path "src\components\blog\.gitkeep"
$cu = Test-Path "src\components\ui\.gitkeep"
if ($cl -and $ch -and $cp -and $cc -and $cb -and $cu) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.7, Req 6.8

---

### M1.G9.T5: Create `src/content/` Directory Taxonomy

**Objective:** Create subdirectories under `src/content/` for loaders, markdown rendering, and Zod schemas.

**Acceptance Criteria:**
- ✓ `src/content/loaders/` exists
- ✓ `src/content/markdown/` exists
- ✓ `src/content/schemas/` exists
- ✓ `.gitkeep` files present in each directory

**Prerequisites:**
- M1.G9.T4 completed

**Implementation Details:**
Create the content code subdirectories using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$dirs = @(
    "src\content\loaders",
    "src\content\markdown",
    "src\content\schemas"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
    New-Item -ItemType File -Path (Join-Path $d ".gitkeep") -Force | Out-Null
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$l = Test-Path "src\content\loaders\.gitkeep"
$m = Test-Path "src\content\markdown\.gitkeep"
$s = Test-Path "src\content\schemas\.gitkeep"
if ($l -and $m -and $s) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.7, Req 6.9

---

### M1.G9.T6: Create `src/types/` Directory and Root Type Barrel (`src/types/index.ts`)

**Objective:** Create the `src/types/` directory and export a placeholder type barrel file to enable cleanly scoped type imports.

**Acceptance Criteria:**
- ✓ `src/types/` directory exists
- ✓ `src/types/index.ts` exists and compiles
- ✓ Exports a baseline `IsoDateString` type alias

**Prerequisites:**
- M1.G9.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\types\index.ts`

**Implementation Details:**
Create `src/types/index.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "src\types")) {
    New-Item -ItemType Directory -Path "src\types" -Force | Out-Null
}

@'
/**
 * Root Type Barrel
 * Re-exports common types across application domains.
 */

export type IsoDateString = string;
'@ | Set-Content "src\types\index.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "src\types\index.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.7, Req 14.3

---

### M1.G9.T7: Install Zod Schema Validator

**Objective:** Install `zod` version 3.x as a production dependency in `package.json` to prepare for M2 content validation.

**Acceptance Criteria:**
- ✓ `zod` is added to `dependencies` in `package.json`
- ✓ Version specified is `^3.23.0` or later 3.x release
- ✓ TypeScript compiler can resolve `zod` types

**Prerequisites:**
- M1.G9.T6 completed

**Implementation Details:**
Install Zod via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install zod
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.dependencies.zod) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.6

---

### M1.G9.T8: Verify Full Directory Tree Integrity

**Objective:** Run an automated audit script validating that every path mandated by `AGENTS.md` Section 3 exists.

**Acceptance Criteria:**
- ✓ All paths defined in the audit list evaluate to `True`
- ✓ Audit script reports 100% compliance

**Prerequisites:**
- M1.G9.T1 through M1.G9.T7 completed

**Implementation Details:**
Execute the tree validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$requiredPaths = @(
    "content\projects",
    "content\certifications",
    "content\blog",
    "public\images\projects",
    "public\images\certifications",
    "public\images\blog",
    "public\files",
    "src\app",
    "src\components\layout",
    "src\components\home",
    "src\components\projects",
    "src\components\certifications",
    "src\components\blog",
    "src\components\ui",
    "src\content\loaders",
    "src\content\markdown",
    "src\content\schemas",
    "src\lib",
    "src\types",
    "tests"
)

$allExist = $true
foreach ($path in $requiredPaths) {
    if (-not (Test-Path $path)) {
        Write-Host "Missing path: $path"
        $allExist = $false
    }
}

if ($allExist) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the script above: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.3, Req 6.6, Req 6.7, Req 6.10

---

### M1.G9.T9: Validate Build and Toolchain with Taxonomy Installed

**Objective:** Run type checking, linting, and tests to confirm the new directory tree and Zod dependency cause no regressions.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0
- ✓ `npm run test` exits 0

**Prerequisites:**
- M1.G9.T8 completed

**Implementation Details:**
Execute the quality verification pipeline via PowerShell:
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

**Satisfies Requirements:** Req 11.2, Req 11.3, Req 11.4

---

### M1.G9.T10: Stage and Commit Directory Taxonomy

**Objective:** Commit the complete directory structure, `.gitkeep` markers, `src/types/index.ts`, and Zod dependency to Git.

**Acceptance Criteria:**
- ✓ `git add .` stages all new folders, `.gitkeep` files, and `package.json` updates
- ✓ Commit created with message `"chore(m1): establish AGENTS.md directory taxonomy and install zod"`

**Prerequisites:**
- M1.G9.T9 completed

**Implementation Details:**
Stage and commit changes using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git add .
git commit -m "chore(m1): establish AGENTS.md directory taxonomy and install zod"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$log = git log -1 --pretty=oneline
if ($log -match "chore\(m1\): establish AGENTS\.md directory taxonomy") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 11.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "content\projects"
Test-Path "public\images\projects"
Test-Path "src\components\ui"
Test-Path "src\content\schemas"
Test-Path "src\types\index.ts"
npm run typecheck
```
Expected output:
- `True` for all path validations
- `npm run typecheck` exits with return code 0.