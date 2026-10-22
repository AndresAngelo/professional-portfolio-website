Here is the complete, self-contained **`goal6.md`** file for Milestone 1, generated according to the Stage 3 Task Format Contract.

Save this content to:  
`.kiro/specs/m1-repository-foundation-toolchain/goal6.md`

***

# M1.G6: Prettier & Code Formatting

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Integrate Prettier for deterministic, automated code formatting across TypeScript, TSX, JSON, Markdown, and CSS files. Configure `.prettierrc` with consistent project formatting rules, establish `.prettierignore` to skip build and cache artifacts, wire `eslint-config-prettier` to prevent linting collisions, and configure `format` and `format:check` npm scripts to satisfy the quality gate standards.

## Goal Success Criteria

- ✓ `prettier` and `eslint-config-prettier` installed in `devDependencies`
- ✓ `.prettierrc` created with standardized styling rules (semi: true, singleQuote: true, tabWidth: 2, printWidth: 100)
- ✓ `.prettierignore` excludes build directories (`.next/`, `out/`, `dist/`, `node_modules/`, `coverage/`)
- ✓ `.eslintrc.json` extends `prettier` as the final entry to disable all conflicting ESLint formatting rules
- ✓ `package.json` contains `"format": "prettier --write ."` and `"format:check": "prettier --check ."` scripts
- ✓ `npm run format:check` runs clean without formatting errors
- ✓ Linting, formatting, and type-checking all pass simultaneously without conflicts

## Prerequisites

- Goals M1.G1 through M1.G5 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `package.json` and `.eslintrc.json` present and configured

---

## Tasks

### M1.G6.T1: Install Prettier and ESLint Prettier Config

**Objective:** Add `prettier` and `eslint-config-prettier` to the project's development dependencies.

**Acceptance Criteria:**
- ✓ `prettier` is added to `devDependencies` in `package.json`
- ✓ `eslint-config-prettier` is added to `devDependencies` in `package.json`
- ✓ `npm install` completes without peer dependency conflicts

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\`

**Implementation Details:**
Execute the following PowerShell command to install packages:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install --save-dev prettier eslint-config-prettier
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$dev = $pkg.devDependencies
if ($dev.prettier -and $dev."eslint-config-prettier") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.11

---

### M1.G6.T2: Create Configuration File (`.prettierrc`)

**Objective:** Define the project formatting style rules in `.prettierrc`.

**Acceptance Criteria:**
- ✓ `.prettierrc` file exists in the project root
- ✓ Formatter rules defined:
  - `semi`: `true`
  - `singleQuote`: `true`
  - `tabWidth`: `2`
  - `useTabs`: `false`
  - `trailingComma`: `"es5"`
  - `printWidth`: `100`
  - `bracketSpacing`: `true`
  - `arrowParens`: `"avoid"`
- ✓ File is valid JSON

**Prerequisites:**
- M1.G6.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\.prettierrc`

**Implementation Details:**
Create the `.prettierrc` file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "useTabs": false,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
'@ | Set-Content ".prettierrc" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
try {
    $cfg = Get-Content ".prettierrc" -Raw | ConvertFrom-Json
    if ($cfg.semi -eq $true -and $cfg.singleQuote -eq $true -and $cfg.printWidth -eq 100) { "PASS" } else { "FAIL" }
} catch {
    "FAIL"
}
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1

---

### M1.G6.T3: Create Ignore Patterns File (`.prettierignore`)

**Objective:** Establish `.prettierignore` to prevent formatting build artifacts, temporary caches, and external dependency trees.

**Acceptance Criteria:**
- ✓ `.prettierignore` exists in the project root
- ✓ Contains entries for `node_modules/`, `.next/`, `out/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, and `.vercel/`

**Prerequisites:**
- M1.G6.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\.prettierignore`

**Implementation Details:**
Write `.prettierignore` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
# Dependencies
node_modules/
package-lock.json

# Next.js & Build Outputs
.next/
out/
dist/
build/

# Test Coverage
coverage/

# Vercel & Cache
.vercel/
.turbo/
*.tsbuildinfo
next-env.d.ts
'@ | Set-Content ".prettierignore" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$ignore = Get-Content ".prettierignore" -Raw
if ($ignore -match "\.next/" -and $ignore -match "node_modules/" -and $ignore -match "coverage/") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.2

---

### M1.G6.T4: Add Prettier Config as Final Extension in `.eslintrc.json`

**Objective:** Integrate `prettier` as the last element of the `extends` array in `.eslintrc.json` so formatting conflicts are turned off.

**Acceptance Criteria:**
- ✓ `extends` array in `.eslintrc.json` contains `"prettier"`
- ✓ `"prettier"` is the final entry in the `extends` array

**Prerequisites:**
- M1.G6.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\.eslintrc.json`

**Implementation Details:**
Update the `extends` array using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content ".eslintrc.json" -Raw | ConvertFrom-Json

$extendsList = [System.Collections.ArrayList]@($cfg.extends)
if ($extendsList -contains "prettier") {
    $extendsList.Remove("prettier")
}
$extendsList.Add("prettier") | Out-Null
$cfg.extends = $extendsList

$cfg | ConvertTo-Json -Depth 10 | Set-Content ".eslintrc.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content ".eslintrc.json" -Raw | ConvertFrom-Json
$lastIndex = $cfg.extends.Length - 1
if ($cfg.extends[$lastIndex] -eq "prettier") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 6.3

---

### M1.G6.T5: Add Format Scripts to `package.json`

**Objective:** Configure `format` and `format:check` npm scripts in `package.json`.

**Acceptance Criteria:**
- ✓ `scripts.format` is set to `"prettier --write ."`
- ✓ `scripts["format:check"]` is set to `"prettier --check ."`

**Prerequisites:**
- M1.G6.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\package.json`

**Implementation Details:**
Update `package.json` with formatting scripts:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$pkg.scripts | Add-Member -MemberType NoteProperty -Name "format" -Value "prettier --write ." -Force
$pkg.scripts | Add-Member -MemberType NoteProperty -Name "format:check" -Value "prettier --check ." -Force

$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.scripts.format -eq "prettier --write ." -and $pkg.scripts."format:check" -eq "prettier --check .") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1

---

### M1.G6.T6: Run Prettier Auto-Formatting (`npm run format`)

**Objective:** Execute `npm run format` to format all existing files according to the rules in `.prettierrc`.

**Acceptance Criteria:**
- ✓ `npm run format` executes without fatal parsing errors
- ✓ Files are rewritten and brought into compliance
- ✓ Exit code is 0

**Prerequisites:**
- M1.G6.T5 completed

**Implementation Details:**
Run formatting command via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run format
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run format
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1

---

### M1.G6.T7: Verify Formatting Quality Gate (`npm run format:check`)

**Objective:** Validate that the codebase passes non-destructive formatting checks cleanly.

**Acceptance Criteria:**
- ✓ `npm run format:check` executes
- ✓ Prettier reports "All matched files are use Prettier code style!" or similar clean confirmation
- ✓ Exit code is 0

**Prerequisites:**
- M1.G6.T6 completed

**Implementation Details:**
Run the verification check via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run format:check
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run format:check
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 11.1

---

### M1.G6.T8: Verify ESLint and Prettier Compatibility

**Objective:** Ensure that ESLint does not complain about formatting decisions made by Prettier.

**Acceptance Criteria:**
- ✓ `npm run lint` runs after `npm run format`
- ✓ Zero lint warnings or errors are raised regarding code formatting or indentation
- ✓ Exit code is 0

**Prerequisites:**
- M1.G6.T7 completed

**Implementation Details:**
Execute the linter using PowerShell:
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

**Satisfies Requirements:** Req 4.13, Req 6.3

---

### M1.G6.T9: Document Formatting Standards in `CONTRIBUTING.md`

**Objective:** Document the code formatting rules, editor recommendations, and pre-commit validation expectations in a new `CONTRIBUTING.md` file.

**Acceptance Criteria:**
- ✓ `CONTRIBUTING.md` created in project root
- ✓ Outlines the requirement to run `npm run format:check` before submitting PRs
- ✓ Mentions single quotes, 2 spaces indentation, and trailing commas

**Prerequisites:**
- M1.G6.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\CONTRIBUTING.md`

**Implementation Details:**
Create `CONTRIBUTING.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
# Contributing Guidelines

## Code Style & Formatting

This project enforces strict code style via **Prettier** and **ESLint**.

### Standards:
- **Indentation:** 2 spaces (no tabs)
- **Quotes:** Single quotes for TypeScript/JavaScript (`'example'`)
- **Semicolons:** Always required (`semi: true`)
- **Print Width:** 100 characters max
- **Trailing Commas:** ES5 compatible

### Commands:
```bash
# Check code style without modifying files
npm run format:check

# Automatically fix formatting across the project
npm run format
```

All Pull Requests and commits must pass `npm run format:check`, `npm run lint`, and `npm run typecheck`.
'@ | Set-Content "CONTRIBUTING.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "CONTRIBUTING.md") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 15.1

---

### M1.G6.T10: Checkpoint: Combined Quality Verification

**Objective:** Run lint, format checking, and type checking in sequence to confirm all static analysis passes without regressions.

**Acceptance Criteria:**
- ✓ `npm run format:check` passes (code 0)
- ✓ `npm run lint` passes (code 0)
- ✓ `npm run typecheck` passes (code 0)

**Prerequisites:**
- M1.G6.T1 through M1.G6.T9 completed

**Implementation Details:**
Execute the triple validation pipeline via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run format:check
npm run lint
npm run typecheck
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run format:check" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.2, Req 11.3, Req 11.6

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path ".prettierrc"
Test-Path ".prettierignore"
Test-Path "CONTRIBUTING.md"
npm run format:check
npm run lint
npm run typecheck
```
Expected output:
- `True` for `.prettierrc`, `.prettierignore`, and `CONTRIBUTING.md`
- Clean exit code 0 for all three commands.