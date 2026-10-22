***

# M1.G5: Vitest & Testing Infrastructure

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the core unit and integration test infrastructure using **Vitest**, **React Testing Library**, and **jsdom**. This goal configures the test execution environment, test lifecycle cleanups, path alias mappings (`@/*` $\rightarrow$ `./src/*`), coverage providers (V8), and sample smoke tests to enforce the quality gate mandate defined in `TRD.md` Section 8.1 and `requirements.md` Requirement 5.

## Goal Success Criteria

- ✓ Vitest, `@vitejs/plugin-react`, `jsdom`, `@testing-library/react`, and `@testing-library/jest-dom` installed as development dependencies
- ✓ `vitest.config.ts` configured with `jsdom` environment, globals enabled, setup file hooks, and `@/` path alias resolution
- ✓ `tests/setup.ts` created with automated DOM cleanup and `@testing-library/jest-dom/vitest` matchers
- ✓ `package.json` contains `"test": "vitest run"` and `"test:coverage": "vitest run --coverage"` scripts
- ✓ At least one smoke test in `tests/example.test.ts` executes and passes
- ✓ `npm run test` executes in non-watch mode and exits with return code 0

## Prerequisites

- Goals M1.G1, M1.G2, M1.G3, and M1.G4 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `package.json` and `tsconfig.json` present and valid

---

## Tasks

### M1.G5.T1: Install Vitest and React Testing Library Dependencies

**Objective:** Install Vitest, its React plugin, jsdom environment, and React Testing Library packages into `devDependencies`.

**Acceptance Criteria:**
- ✓ `vitest` installed in `devDependencies`
- ✓ `@vitejs/plugin-react` installed in `devDependencies`
- ✓ `jsdom` installed in `devDependencies`
- ✓ `@testing-library/react` installed in `devDependencies`
- ✓ `@testing-library/jest-dom` installed in `devDependencies`
- ✓ `package.json` reflects all installed test libraries

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\`

**Implementation Details:**
Execute the following PowerShell command to install dependencies:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install --save-dev vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/jest-dom
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$dev = $pkg.devDependencies
if ($dev.vitest -and $dev."@testing-library/react" -and $dev.jsdom) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.4, Req 12.11

---

### M1.G5.T2: Create `tests/` Directory Structure

**Objective:** Create the root `tests/` directory and ensure proper file structure exists for test configuration and test suites.

**Acceptance Criteria:**
- ✓ `tests/` directory exists in the project root
- ✓ Path `c:\dev\andres-webapp-professional\personal-website-portfolio\tests\` is accessible

**Prerequisites:**
- M1.G5.T1 completed

**Implementation Details:**
Create the testing folder using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (-not (Test-Path "tests")) {
    New-Item -ItemType Directory -Path "tests"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "tests") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.7, Req 6.10

---

### M1.G5.T3: Create Global Test Setup File (`tests/setup.ts`)

**Objective:** Implement `tests/setup.ts` to register custom DOM matchers and configure automated cleanup hooks after each test.

**Acceptance Criteria:**
- ✓ `tests/setup.ts` file exists
- ✓ Imports `cleanup` from `@testing-library/react`
- ✓ Imports `@testing-library/jest-dom/vitest`
- ✓ Invokes `cleanup()` inside an `afterEach` lifecycle hook

**Prerequisites:**
- M1.G5.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tests\setup.ts`

**Implementation Details:**
Write `tests/setup.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// Automatically clean up DOM trees mounted during React Testing Library tests
afterEach(() => {
  cleanup();
});
'@ | Set-Content "tests\setup.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$setup = Get-Content "tests\setup.ts" -Raw
if ($setup -match "import '@testing-library/jest-dom/vitest'" -and $setup -match "afterEach") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.4

---

### M1.G5.T4: Initialize `vitest.config.ts` Base Configuration

**Objective:** Create the `vitest.config.ts` configuration file importing `defineConfig` and the React plugin.

**Acceptance Criteria:**
- ✓ `vitest.config.ts` exists in project root
- ✓ Integrates `react()` plugin from `@vitejs/plugin-react`
- ✓ Exports default configuration using `defineConfig`

**Prerequisites:**
- M1.G5.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\vitest.config.ts`

**Implementation Details:**
Create the initial config skeleton using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
});
'@ | Set-Content "vitest.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "vitest.config.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1

---

### M1.G5.T5: Configure Test Environment, Globals, and Setup Files

**Objective:** Configure Vitest to use the `jsdom` DOM emulation environment, enable global test APIs (`describe`, `it`, `expect`), and load `tests/setup.ts`.

**Acceptance Criteria:**
- ✓ `test.environment` set to `'jsdom'`
- ✓ `test.globals` set to `true`
- ✓ `test.setupFiles` includes `'./tests/setup.ts'`
- ✓ `test.include` captures `**/*.{test,spec}.{ts,tsx}`

**Prerequisites:**
- M1.G5.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\vitest.config.ts`

**Implementation Details:**
Update `vitest.config.ts` with test environment options:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
  },
});
'@ | Set-Content "vitest.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "vitest.config.ts" -Raw
if ($cfg -match "environment:\s*'jsdom'" -and $cfg -match "\['\./tests/setup\.ts'\]") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.2, Req 5.3, Req 5.5

---

### M1.G5.T6: Configure Coverage Provider in `vitest.config.ts`

**Objective:** Add V8 coverage configuration with text, JSON, and HTML reporters while excluding build artifacts and configuration files.

**Acceptance Criteria:**
- ✓ `test.coverage.provider` set to `'v8'`
- ✓ `test.coverage.reporter` includes `'text'`, `'json'`, and `'html'`
- ✓ Coverage exclusion patterns configured for `node_modules/`, `tests/`, and build artifacts

**Prerequisites:**
- M1.G5.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\vitest.config.ts`

**Implementation Details:**
Append coverage options to `vitest.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
        '.next/**',
      ],
    },
  },
});
'@ | Set-Content "vitest.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "vitest.config.ts" -Raw
if ($cfg -match "provider:\s*'v8'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1

---

### M1.G5.T7: Configure Path Aliases in `vitest.config.ts`

**Objective:** Map `@/*` to the `./src/*` directory in Vitest to maintain parity with `tsconfig.json`.

**Acceptance Criteria:**
- ✓ `resolve.alias` defines `'@'` pointing to `path.resolve(__dirname, './src')`
- ✓ Test imports can resolve modules using `@/` path prefixes

**Prerequisites:**
- M1.G5.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\vitest.config.ts`

**Implementation Details:**
Append path resolution mapping to `vitest.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
        '.next/**',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
'@ | Set-Content "vitest.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "vitest.config.ts" -Raw
if ($cfg -match "alias:\s*\{" -and $cfg -match "path\.resolve\(__dirname, '\./src'\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.6

---

### M1.G5.T8: Add Test Scripts to `package.json`

**Objective:** Configure `test` and `test:coverage` scripts in `package.json` for CI and local verification.

**Acceptance Criteria:**
- ✓ `scripts.test` is set to `"vitest run"` (runs in non-watch mode by default)
- ✓ `scripts["test:coverage"]` is set to `"vitest run --coverage"`

**Prerequisites:**
- M1.G5.T7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\package.json`

**Implementation Details:**
Update the scripts object in `package.json`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$pkg.scripts.test = "vitest run"
$pkg.scripts | Add-Member -MemberType NoteProperty -Name "test:coverage" -Value "vitest run --coverage" -Force
$pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.scripts.test -eq "vitest run" -and $pkg.scripts."test:coverage" -eq "vitest run --coverage") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.8, Req 7.5, Req 7.7

---

### M1.G5.T9: Author Foundation Smoke Test (`tests/example.test.ts`)

**Objective:** Write an initial test suite validating basic runtime assertion functionality, environment globals, and DOM testing utilities.

**Acceptance Criteria:**
- ✓ `tests/example.test.ts` exists
- ✓ Tests basic boolean assertions
- ✓ Tests DOM rendering via React Testing Library
- ✓ Verifies Jest-DOM matchers (`toBeInTheDocument()`) function properly

**Prerequisites:**
- M1.G5.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tests\example.test.ts`

**Implementation Details:**
Create the smoke test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import { describe, it, expect } from 'vitest';

describe('M1 Repository Foundation Smoke Tests', () => {
  it('should verify basic test framework assertion integrity', () => {
    expect(true).toBe(true);
  });

  it('should confirm environment is jsdom with DOM availability', () => {
    const element = document.createElement('div');
    element.textContent = 'Foundation Verified';
    document.body.appendChild(element);

    expect(element).toBeInTheDocument();
    expect(element.textContent).toBe('Foundation Verified');
  });
});
'@ | Set-Content "tests\example.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if (Test-Path "tests\example.test.ts") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.8

---

### M1.G5.T10: Execute Test Suite Quality Gate (`npm run test`)

**Objective:** Run `npm run test` to discover, execute, and pass all test suites in non-watch mode.

**Acceptance Criteria:**
- ✓ `npm run test` executes without hanging or waiting for user input
- ✓ All test cases pass
- ✓ Exit code is 0

**Prerequisites:**
- M1.G5.T1 through M1.G5.T9 completed

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

**Satisfies Requirements:** Req 5.9, Req 5.10, Req 5.11, Req 11.4

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "vitest.config.ts"
Test-Path "tests\setup.ts"
Test-Path "tests\example.test.ts"
npm run test
```
Expected output:
- `True` for all three file path checks
- `npm run test` exits with return code 0 and reports all tests passed.