# M1.G1: Next.js Project Initialization

> **Milestone:** M1 — Repository Foundation & Toolchain
> **Goal:** G1 of 10
> **Tasks:** ~10 atomic tasks
> **Status:** NOT STARTED

## Goal Objective

Bootstrap the Next.js 15+ project with App Router, TypeScript, Tailwind CSS, and ESLint using the `create-next-app` CLI. This establishes the core project structure and ensures all primary development dependencies are correctly installed and version-compliant.

## Goal Success Criteria

- ✓ `personal-website-portfolio-v2\` directory exists at workspace root (`c:\dev\andres-webapp-professional\personal-website-portfolio\`)
- ✓ `package.json` lists Next.js 15+, React 19+, and TypeScript 5+
- ✓ App Router structure is present: `src/app/layout.tsx`, `src/app/page.tsx`
- ✓ `next.config.ts`, `tsconfig.json`, and `tailwind.config.ts` exist
- ✓ `npm run dev` starts without fatal errors

## Prerequisites

- Access to Windows PowerShell
- Node.js 18.0.0+ and npm 9.0.0+ installed on the host machine

---

## Tasks

### M1.G1.T1: Verify workspace prerequisites (Node 18+, npm 9+)

**Objective:** Ensure the host environment meets the minimum required Node.js and npm versions.

**Acceptance Criteria:**
- ✓ `node -v` returns a version $\ge$ 18.0.0
- ✓ `npm -v` returns a version $\ge$ 9.0.0
- ✓ Commands execute successfully in PowerShell
- ✓ Output is clearly visible for verification

**Prerequisites:**
- None (Host environment check)

**Implementation Details:**

Execute the following commands in PowerShell:
```powershell
node -v
npm -v
```

**Validation:**
```powershell
# Verify Node version is 18 or higher
node -v | ForEach-Object { if ($_ -match 'v(1[8-9]|[2-9][0-9])') { "PASS" } else { "FAIL" } }

# Verify npm version is 9 or higher
npm -v | ForEach-Object { if ($_ -match '^(9|[1-9][0-9])') { "PASS" } else { "FAIL" } }
```
Expected: Both commands output `PASS`.

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T2: Create project directory

**Objective:** Create the specific project root directory at the designated workspace path.

**Acceptance Criteria:**
- ✓ Directory `personal-website-portfolio-v2` exists
- ✓ Directory is located at `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- ✓ Directory is empty or ready for initialization

**Prerequisites:**
- M1.G1.T1 completed

**Implementation Details:**

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\"
New-Item -ItemType Directory -Path "personal-website-portfolio-v2"
```

**Validation:**
```powershell
Test-Path "c:\dev\andres-webapp-professional\personal-website-portfolio"
```
Expected: `True`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T3: Run `create-next-app` CLI with App Router + TypeScript + Tailwind flags

**Objective:** Bootstrap the project using the Next.js CLI with the required tech stack.

**Acceptance Criteria:**
- ✓ `create-next-app` completes successfully
- ✓ App Router is enabled
- ✓ TypeScript is enabled
- ✓ Tailwind CSS is enabled
- ✓ ESLint is enabled
- ✓ `src/` directory is used

**Prerequisites:**
- M1.G1.T2 completed
- `npx create-next-app@latest` is available

**Implementation Details:**

Navigate into the project directory and run the interactive CLI or use flags for non-interactive automation. To ensure strict adherence to the requirements, use the following command:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm
```
*Note: The `.` tells the CLI to install in the current directory.*

**Validation:**
```powershell
ls
```
Expected: Presence of `package.json`, `src/`, `next.config.ts`, etc.

**Satisfies Requirements:** Req 1.1, 1.2

---

### M1.G1.T4: Verify Next.js installation and version in package.json

**Objective:** Confirm that `next` is installed and meets the version 15+ requirement.

**Acceptance Criteria:**
- ✓ `next` is listed in `dependencies`
- ✓ version is $\ge$ 15.0.0

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
Get-Content "package.json" | Select-String '"next":'
```

**Validation:**
```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
if ($pkg.dependencies.next -match '^15') { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T5: Verify React 19+ installation

**Objective:** Confirm that `react` and `react-dom` are installed and meet the version 19+ requirement.

**Acceptance Criteria:**
- ✓ `react` version is $\ge$ 19.0.0
- ✓ `react-dom` version is $\ge$ 19.0.0

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
$reactVer = $pkg.dependencies.react
$reactDomVer = $pkg.dependencies."react-dom"
```

**Validation:**
```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
if ($pkg.dependencies.react -match '^19' -and $pkg.dependencies."react-dom" -match '^19') { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T6: Verify TypeScript installation and tsconfig.json exists

**Objective:** Confirm TypeScript is installed and the configuration file is present.

**Acceptance Criteria:**
- ✓ `typescript` is listed in `devDependencies`
- ✓ `tsconfig.json` exists in the project root

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
ls tsconfig.json
Get-Content "package.json" | Select-String '"typescript":'
```

**Validation:**
```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
if ((Test-Path "tsconfig.json") -and ($pkg.devDependencies.typescript -match '5')) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T7: Verify Tailwind CSS installation and tailwind.config.ts exists

**Objective:** Confirm Tailwind CSS is installed and configured.

**Acceptance Criteria:**
- ✓ `tailwindcss` is listed in `devDependencies`
- ✓ `tailwind.config.ts` exists in the project root

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
ls tailwind.config.ts
Get-Content "package.json" | Select-String '"tailwindcss":'
```

**Validation:**
```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
if ((Test-Path "tailwind.config.ts") -and ($pkg.devDependencies.tailwindcss)) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T8: Verify ESLint installation and .eslintrc.json exists

**Objective:** Confirm ESLint is installed and configured.

**Acceptance Criteria:**
- ✓ `eslint` is listed in `devDependencies`
- ✓ `.eslintrc.json` or `.eslintrc.js` or `eslint.config.mjs` exists

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
ls .eslintrc*
Get-Content "package.json" | Select-String '"eslint":'
```

**Validation:**
```powershell
$pkg = Get-Content "package.json" | ConvertFrom-Json
$eslintFile = Get-ChildItem -Path . -Filter ".eslintrc*" -ErrorAction SilentlyContinue
if ($eslintFile -and ($pkg.devDependencies.eslint)) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T9: Verify .gitignore was created with standard Next.js patterns

**Objective:** Ensure a `.gitignore` file exists and includes common Next.js/Node exclusions.

**Acceptance Criteria:**
- ✓ `.gitignore` exists
- ✓ Contains `.next/`
- ✓ Contains `node_modules/`

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
Get-Content ".gitignore" | Select-String ".next/", "node_modules/"
```

**Validation:**
```powershell
$ignore = Get-Content ".gitignore"
if ($ignore -contains ".next/" -or ($ignore | Select-String ".next/") -and ($ignore -contains "node_modules/" -or ($ignore | Select-String "node_modules/"))) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1

---

### M1.G1.T10: Verify App Router directory structure (`src/app/`, layout, page)

**Objective:** Verify the core App Router files were scaffolded correctly within the `src` directory.

**Acceptance Criteria:**
- ✓ `src/app/layout.tsx` exists
- ✓ `src/app/page.tsx` exists
- ✓ `src/app/` directory exists

**Prerequisites:**
- M1.G1.T3 completed

**Implementation Details:**

```powershell
ls src/app/layout.tsx
ls src/app/page.tsx
```

**Validation:**
```powershell
if ((Test-Path "src/app/layout.tsx") -and (Test-Path "src/app/page.tsx")) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 1.1, 1.2

---

## Goal Checkpoint

Run the following to confirm all tasks in this goal are complete:
```powershell
# Check if project root exists and has basic files
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\"
ls
npm run dev -- --skip-install # Attempt to start dev server (might fail if ports are taken, but should not fail on missing files)
```
Expected: Files listed, dev server attempts to start.
```