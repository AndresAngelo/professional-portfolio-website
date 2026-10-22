***

# M1.G7: Git & Husky Pre-commit Hooks

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Initialize the local Git repository, establish `.gitignore` boundary rules, and install **Husky** paired with **lint-staged**. This automates Git pre-commit verification so that every commit is guarded against formatting regressions (`prettier`), lint violations (`eslint`), and compilation defects (`tsc --noEmit`), enforcing the quality gate mandate defined in `TRD.md` Section 8 and `requirements.md` Requirement 10.

## Goal Success Criteria

- ✓ Local Git repository initialized with a valid `.git/` directory
- ✓ `.gitignore` configured to exclude `node_modules/`, `.next/`, `out/`, `coverage/`, `.env*`, and OS/IDE metadata
- ✓ `husky` and `lint-staged` installed in `devDependencies`
- ✓ Husky initialized with a `.husky/pre-commit` hook executing `npx lint-staged`
- ✓ `package.json` contains a `lint-staged` configuration block targeting `*.{ts,tsx,js,jsx}` with `prettier --write` and `eslint --fix`
- ✓ A test commit or dry-run commit triggers hooks without failures
- ✓ Git initial commit cleanly tracks all foundation configuration and scaffolding files

## Prerequisites

- Goals M1.G1 through M1.G6 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Git installed and accessible in the system environment PATH

---

## Tasks

### M1.G7.T1: Verify Git Installation and Initialize Repository

**Objective:** Confirm Git CLI availability and initialize a new Git repository at the project root if `.git` does not yet exist.

**Acceptance Criteria:**
- ✓ `git --version` executes successfully
- ✓ `git init` initializes the repository in `personal-website-portfolio-v2\`
- ✓ `.git` directory exists

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\`

**Implementation Details:**
Execute the following PowerShell script:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git --version
if (-not (Test-Path ".git")) {
    git init
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path ".git") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1

---

### M1.G7.T2: Configure Comprehensive `.gitignore`

**Objective:** Write the complete `.gitignore` file to prevent committing dependencies, build artifacts, coverage reports, and environment secrets.

**Acceptance Criteria:**
- ✓ `.gitignore` exists at the project root
- ✓ Ignores `node_modules/`, `.next/`, `out/`, `dist/`, `build/`
- ✓ Ignores `.env`, `.env*.local`, `.env.production`
- ✓ Ignores `coverage/`, `.nyc_output/`
- ✓ Ignores `.vscode/`, `.idea/`, `.DS_Store`, and `*.log`
- ✓ Does NOT ignore the `public/` directory

**Prerequisites:**
- M1.G7.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\.gitignore`

**Implementation Details:**
Create or overwrite `.gitignore` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
# Dependencies
node_modules/
package-lock.json
pnpm-lock.yaml
yarn.lock

# Next.js Build Outputs
.next/
out/
build/
dist/

# Environment Variables
.env
.env*.local
.env.production

# Testing & Coverage
coverage/
.nyc_output/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# IDE & OS Metadata
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Vercel & Deployments
.vercel/

# TypeScript Cache
*.tsbuildinfo
next-env.d.ts

# Temporary Folders
.temp/
.cache/
tmp/
'@ | Set-Content ".gitignore" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$gi = Get-Content ".gitignore" -Raw
if ($gi -match "node_modules/" -and $gi -match "\.next/" -and $gi -match "\.env\*\.local") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.5, Req 10.12

---

### M1.G7.T3: Install Husky and lint-staged Dependencies

**Objective:** Install `husky` and `lint-staged` into `devDependencies` for automated git hook management.

**Acceptance Criteria:**
- ✓ `husky` added to `devDependencies` in `package.json`
- ✓ `lint-staged` added to `devDependencies` in `package.json`
- ✓ Dependencies installed cleanly

**Prerequisites:**
- M1.G7.T2 completed

**Implementation Details:**
Install the packages using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install --save-dev husky lint-staged
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$dev = $pkg.devDependencies
if ($dev.husky -and $dev."lint-staged") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.11

---

### M1.G7.T4: Initialize Husky Directory (`.husky/`)

**Objective:** Execute `husky init` or configure the `.husky` directory with automatic install hooks in `package.json`.

**Acceptance Criteria:**
- ✓ `.husky/` directory exists in the project root
- ✓ `prepare` script is added to `package.json` (`"prepare": "husky"`)

**Prerequisites:**
- M1.G7.T3 completed

**Implementation Details:**
Execute the following PowerShell script:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx husky init
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ((Test-Path ".husky") -and $pkg.scripts.prepare -match "husky") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1

---

### M1.G7.T5: Configure Pre-commit Hook (`.husky/pre-commit`)

**Objective:** Set up `.husky/pre-commit` to invoke `npx lint-staged` prior to allowing git commits.

**Acceptance Criteria:**
- ✓ `.husky/pre-commit` file exists
- ✓ Script contains `npx lint-staged`
- ✓ Carriage returns and encoding are shell-friendly

**Prerequisites:**
- M1.G7.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\.husky\pre-commit`

**Implementation Details:**
Write the pre-commit hook using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
npx lint-staged
'@ | Set-Content ".husky\pre-commit" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$hook = Get-Content ".husky\pre-commit" -Raw
if ($hook -match "npx lint-staged") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1

---

### M1.G7.T6: Configure `lint-staged` Rules in `package.json`

**Objective:** Add a `lint-staged` object in `package.json` to automatically format, lint, and run type checks on staged files.

**Acceptance Criteria:**
- ✓ `lint-staged` configured in `package.json`
- ✓ `*.{ts,tsx}` triggers `prettier --write` and `eslint --fix`
- ✓ `*.{json,md,css}` triggers `prettier --write`

**Prerequisites:**
- M1.G7.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\package.json`

**Implementation Details:**
Update `package.json` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json

$lintStagedObj = [PSCustomObject]@{
    "*.{ts,tsx}" = @("prettier --write", "eslint --fix")
    "*.{json,md,css}" = @("prettier --write")
}
$pkg | Add-Member -MemberType NoteProperty -Name "lint-staged" -Value $lintStagedObj -Force

$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$ls = $pkg."lint-staged"
if ($ls."*.{ts,tsx}" -contains "eslint --fix" -and $ls."*.{json,md,css}" -contains "prettier --write") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.10, Req 6.1, Req 7.1

---

### M1.G7.T7: Verify lint-staged Pipeline Execution

**Objective:** Perform a dry-run test of `lint-staged` to verify rule parsing and command generation.

**Acceptance Criteria:**
- ✓ `npx lint-staged` executes
- ✓ No syntax or configuration errors are raised
- ✓ Process exits cleanly

**Prerequisites:**
- M1.G7.T6 completed

**Implementation Details:**
Execute `lint-staged` via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx lint-staged --allow-empty
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx lint-staged --allow-empty
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1

---

### M1.G7.T8: Stage Foundation Files for Baseline Commit

**Objective:** Add all initialized configuration, source files, and test assets to the Git staging index.

**Acceptance Criteria:**
- ✓ `git add .` executes cleanly
- ✓ Staged files include `package.json`, `tsconfig.json`, `tailwind.config.ts`, `.eslintrc.json`, `vitest.config.ts`, `.prettierrc`, and `.gitignore`
- ✓ Excluded files (like `node_modules/`) remain untracked

**Prerequisites:**
- M1.G7.T7 completed

**Implementation Details:**
Stage files using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git add .
git status --short
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$status = git status --porcelain
if ($status) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1

---

### M1.G7.T9: Execute Initial Commit with Hook Verification

**Objective:** Commit the staged baseline files, confirming that Husky pre-commit hooks run cleanly during commit execution.

**Acceptance Criteria:**
- ✓ `git commit` executes with message `"chore(m1): foundation toolchain and quality gates"`
- ✓ Pre-commit hook triggers `lint-staged` successfully
- ✓ Commit is recorded in repository history

**Prerequisites:**
- M1.G7.T8 completed

**Implementation Details:**
Execute the commit via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git commit -m "chore(m1): foundation toolchain and quality gates"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$log = git log -1 --pretty=oneline
if ($log -match "chore\(m1\): foundation toolchain and quality gates") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 11.1

---

### M1.G7.T10: Validate Clean Working Tree

**Objective:** Ensure no dirty files, untracked artifacts, or ignored files are lingering in `git status`.

**Acceptance Criteria:**
- ✓ `git status` reports `"nothing to commit, working tree clean"`
- ✓ Exit code is 0

**Prerequisites:**
- M1.G7.T9 completed

**Implementation Details:**
Check working tree status using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
git status
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$status = git status --porcelain
if (-not $status) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 11.12

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path ".git"
Test-Path ".husky\pre-commit"
Get-Content "package.json" | Select-String "lint-staged"
git status
```
Expected output:
- `True` for `.git` and `.husky\pre-commit`
- Matches found for `lint-staged` block in `package.json`
- `git status` reports working tree clean.