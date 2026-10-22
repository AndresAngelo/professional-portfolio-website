# M3.G1: Shared Internals, Dependency Approvals, and Config-Gap Log

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the shared foundational styling and utility modules in `src/components/ui/` that all downstream M3 primitives compose: a lightweight class joiner (`cx.ts`), the focus-ring token composition (`focus-ring.ts`), motion constants with strict `prefers-reduced-motion` pairing (`motion.ts`), heading level types (`heading-level.ts`), and external URL verification helpers (`external-link-attrs.ts`). Furthermore, record design token and breakpoint gaps against M1, document pre-approved dependencies (`fast-check` and `vitest-axe` per Approval 1a, 2026-10-22), and verify all shared utilities with Vitest unit tests without modifying root configuration files.

## Goal Success Criteria

- ✓ `src/components/ui/cx.ts` implemented without third-party class libraries (`clsx`/`tailwind-merge`)
- ✓ `src/components/ui/focus-ring.ts` defines `FOCUS_RING` utilizing `ring-focus-ring` with 2px width and 2px offset on `:focus-visible`
- ✓ `src/components/ui/motion.ts` pairs every transition with `motion-reduce:transition-none`
- ✓ `src/components/ui/heading-level.ts` exports `HeadingLevel` (`2 | 3 | 4`)
- ✓ `src/components/ui/external-link-attrs.ts` exports `HttpsUrl` type, `resolveExternalHref`, `EXTERNAL_LINK_ATTRS`, and `NEW_TAB_TEXT`
- ✓ `tests/unit/components/ui/shared.test.ts` passes with 100% assertions on shared helpers
- ✓ Task notes file `.kiro/specs/m3-design-system-implementation/task-notes.md` created, logging M1 configuration gaps and Approval 1a
- ✓ Pinned dependencies (`fast-check@3.23.2` and `vitest-axe@0.1.0`) added to `package.json` `devDependencies`
- ✓ `git diff` confirms zero changes to `tailwind.config.ts` and `globals.css`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Milestone 1 and Milestone 2 completed (`m2-baseline` tagged, clean working tree)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Node.js LTS and npm available
- Pre-installed test framework: `vitest`

---

## Tasks

### M3.G1.T1: Create Shared Class Joiner (`src/components/ui/cx.ts`)

**Objective:** Implement a lightweight, zero-dependency class joiner in `src/components/ui/cx.ts` that filters falsy values and joins class strings.

**Acceptance Criteria:**
- ✓ File `src/components/ui/cx.ts` exists
- ✓ Exports `ClassValue` type defining `string | false | null | undefined`
- ✓ Exports `cx(...values: ClassValue[]): string` function
- ✓ Filters out empty strings, `null`, `undefined`, and `false`
- ✓ Concatenates truthy string classes with a single space separator
- ✓ Contains no dependencies on `clsx` or `tailwind-merge` (`AGENTS.md` 6.2, Req 16.5)

**Prerequisites:**
- Workspace at `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Target directory `src/components/ui/` exists

**Implementation Details:**

Write `src/components/ui/cx.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "src\components\ui")) {
    New-Item -ItemType Directory -Path "src\components\ui" -Force | Out-Null
}

@'
/**
 * Lightweight class name joiner utility.
 * Replaces external class-merging dependencies per Requirement 16.5.
 */
export type ClassValue = string | false | null | undefined;

export function cx(...values: ClassValue[]): string {
  return values.filter((v): v is string => typeof v === 'string' && v.length > 0).join(' ');
}
'@ | Set-Content "src\components\ui\cx.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/cx.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 16.5, Req 16.8

---

### M3.G1.T2: Implement Focus Ring Token Composition (`src/components/ui/focus-ring.ts`)

**Objective:** Author the canonical focus-ring class composition in `src/components/ui/focus-ring.ts` using the semantic `focus-ring` token.

**Acceptance Criteria:**
- ✓ File `src/components/ui/focus-ring.ts` exists
- ✓ Exports `FOCUS_RING` string constant
- ✓ Applies `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring focus-visible:ring-offset-2`
- ✓ Enforces minimum 2px outline width and 2px offset on keyboard focus (`:focus-visible`)
- ✓ Employs zero raw hex codes or arbitrary values
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M3.G1.T1 completed
- Target file: `src/components/ui/focus-ring.ts`

**Implementation Details:**

Write `src/components/ui/focus-ring.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
/**
 * Canonical Focus Ring Utility Composition
 *
 * Applies a 2px outline ring with a 2px offset using the semantic --color-focus-ring token.
 * Appears exclusively on keyboard focus (:focus-visible) per design.md Section 5.2 and Requirement 11.
 */
export const FOCUS_RING =
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring focus-visible:ring-offset-2';
'@ | Set-Content "src\components\ui\focus-ring.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/focus-ring.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 11.1, Req 11.2, Req 11.4, Req 11.5, Req 16.8

---

### M3.G1.T3: Implement Motion Constants with Reduced Motion Pairing (`src/components/ui/motion.ts`)

**Objective:** Author `src/components/ui/motion.ts` exporting standardized transition class compositions strictly paired with `motion-reduce:transition-none`.

**Acceptance Criteria:**
- ✓ File `src/components/ui/motion.ts` exists
- ✓ Exports `MOTION_FAST` (`transition-colors duration-fast motion-reduce:transition-none`)
- ✓ Exports `MOTION_SHADOW_FAST` (`transition-shadow duration-fast motion-reduce:transition-none`)
- ✓ Exports `MOTION_STANDARD` (`transition-all duration-standard motion-reduce:transition-none`)
- ✓ Every transition utility pairs with `motion-reduce:transition-none` per Requirement 12.5
- ✓ Uses `duration-fast` (150ms) and `duration-standard` (250ms) semantic tokens from M1

**Prerequisites:**
- M3.G1.T1 completed
- Target file: `src/components/ui/motion.ts`

**Implementation Details:**

Write `src/components/ui/motion.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
/**
 * Canonical Motion and Transition Utilities
 *
 * Enforces semantic duration tokens and mandatory pairing with motion-reduce:transition-none
 * to guarantee WCAG 2.1 AA compliance for users sensitive to motion (Requirement 12).
 */
export const MOTION_FAST =
  'transition-colors duration-fast motion-reduce:transition-none';

export const MOTION_SHADOW_FAST =
  'transition-shadow duration-fast motion-reduce:transition-none';

export const MOTION_STANDARD =
  'transition-all duration-standard motion-reduce:transition-none';
'@ | Set-Content "src\components\ui\motion.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/motion.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 12.1, Req 12.2, Req 12.5, Req 16.8

---

### M3.G1.T4: Implement Heading Level Contract (`src/components/ui/heading-level.ts`)

**Objective:** Define the discrete `HeadingLevel` type in `src/components/ui/heading-level.ts` to allow consumers to govern heading hierarchies.

**Acceptance Criteria:**
- ✓ File `src/components/ui/heading-level.ts` exists
- ✓ Exports `HeadingLevel` type defined as `2 | 3 | 4`
- ✓ Exports helper `HeadingTag` mapping (`'h2' | 'h3' | 'h4'`)
- ✓ Prohibits `1` (level-1 headings reserved exclusively for hero/page layout)
- ✓ Contains no runtime dependencies

**Prerequisites:**
- M3.G1.T1 completed
- Target file: `src/components/ui/heading-level.ts`

**Implementation Details:**

Write `src/components/ui/heading-level.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
/**
 * Constrained heading level union for accessible cards and empty states.
 * Level 1 is omitted to preserve single-h1 page landmarks (Req 3.6, Req 9.3).
 */
export type HeadingLevel = 2 | 3 | 4;

export type HeadingTag = `h${HeadingLevel}`;
'@ | Set-Content "src\components\ui\heading-level.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/heading-level.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 9.3, Req 16.8

---

### M3.G1.T5: Implement External Link Attribute Utilities (`src/components/ui/external-link-attrs.ts`)

**Objective:** Author external link URL verification and attribute resolution helpers in `src/components/ui/external-link-attrs.ts`.

**Acceptance Criteria:**
- ✓ File `src/components/ui/external-link-attrs.ts` exists
- ✓ Exports `HttpsUrl` template literal type: `` `https://${string}` ``
- ✓ Exports `resolveExternalHref(href: string | null | undefined): HttpsUrl | null`
- ✓ Validates that input is a non-empty string starting with `https://`
- ✓ Exports `EXTERNAL_LINK_ATTRS` constant containing `target: '_blank'` and `rel: 'noopener noreferrer'`
- ✓ Exports `NEW_TAB_TEXT` constant containing `'(opens in a new tab)'`

**Prerequisites:**
- M3.G1.T1 completed
- Target file: `src/components/ui/external-link-attrs.ts`

**Implementation Details:**

Write `src/components/ui/external-link-attrs.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
/**
 * External Link Validation and Attribute Utilities
 * AGENTS.md 5.1 Rule 5, 8 & Requirement 8
 */
export type HttpsUrl = `https://${string}`;

export const EXTERNAL_LINK_ATTRS = {
  target: '_blank',
  rel: 'noopener noreferrer',
} as const;

export const NEW_TAB_TEXT = '(opens in a new tab)';

/**
 * Validates whether an href string is a non-empty, absolute HTTPS URL.
 * Returns the narrowed HttpsUrl or null if invalid or absent.
 */
export function resolveExternalHref(href: string | null | undefined): HttpsUrl | null {
  if (typeof href !== 'string') {
    return null;
  }
  const trimmed = href.trim();
  if (trimmed.startsWith('https://') && trimmed.length > 'https://'.length) {
    return trimmed as HttpsUrl;
  }
  return null;
}
'@ | Set-Content "src\components\ui\external-link-attrs.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/external-link-attrs.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.4, Req 8.5, Req 8.6, Req 16.8

---

### M3.G1.T6: Author Unit Tests for Shared Internals (`tests/unit/components/ui/shared.test.ts`)

**Objective:** Write Vitest unit tests in `tests/unit/components/ui/shared.test.ts` testing `cx`, `FOCUS_RING`, `MOTION_FAST`, and `resolveExternalHref`.

**Acceptance Criteria:**
- ✓ Tests `cx()` handles empty values, false, null, and multi-class joins
- ✓ Tests `FOCUS_RING` includes `focus-visible:ring-focus-ring`, `focus-visible:ring-2`, and `focus-visible:ring-offset-2`
- ✓ Tests `MOTION_FAST` and `MOTION_STANDARD` include `motion-reduce:transition-none`
- ✓ Tests `resolveExternalHref` accepts valid `https://` URLs
- ✓ Tests `resolveExternalHref` returns `null` for `null`, `undefined`, empty string, `http://`, and plain text
- ✓ All tests pass under `npm test`

**Prerequisites:**
- M3.G1.T1 through M3.G1.T5 completed
- Target file: `tests/unit/components/ui/shared.test.ts`

**Implementation Details:**

Write the unit test file using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "tests\unit\components\ui")) {
    New-Item -ItemType Directory -Path "tests\unit\components\ui" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST, MOTION_SHADOW_FAST, MOTION_STANDARD } from '@/components/ui/motion';
import { resolveExternalHref, EXTERNAL_LINK_ATTRS, NEW_TAB_TEXT } from '@/components/ui/external-link-attrs';

describe('M3 Shared Internals', () => {
  describe('cx class joiner', () => {
    it('joins truthy strings with a space and omits falsy values', () => {
      expect(cx('base', false, 'active', null, undefined, '', 'extra')).toBe('base active extra');
    });

    it('returns empty string when given no truthy values', () => {
      expect(cx(false, null, undefined, '')).toBe('');
    });
  });

  describe('Focus ring constant', () => {
    it('contains mandatory focus-visible, 2px ring, 2px offset, and token classes', () => {
      expect(FOCUS_RING).toContain('focus-visible:outline-none');
      expect(FOCUS_RING).toContain('focus-visible:ring-2');
      expect(FOCUS_RING).toContain('focus-visible:ring-focus-ring');
      expect(FOCUS_RING).toContain('focus-visible:ring-offset-2');
    });
  });

  describe('Motion constants', () => {
    it('pairs all motion transitions with motion-reduce:transition-none', () => {
      expect(MOTION_FAST).toContain('duration-fast');
      expect(MOTION_FAST).toContain('motion-reduce:transition-none');

      expect(MOTION_SHADOW_FAST).toContain('transition-shadow');
      expect(MOTION_SHADOW_FAST).toContain('motion-reduce:transition-none');

      expect(MOTION_STANDARD).toContain('duration-standard');
      expect(MOTION_STANDARD).toContain('motion-reduce:transition-none');
    });
  });

  describe('resolveExternalHref', () => {
    it('accepts valid absolute HTTPS URLs', () => {
      expect(resolveExternalHref('https://example.com')).toBe('https://example.com');
      expect(resolveExternalHref('https://github.com/angelo')).toBe('https://github.com/angelo');
    });

    it('rejects null, undefined, and empty string', () => {
      expect(resolveExternalHref(null)).toBeNull();
      expect(resolveExternalHref(undefined)).toBeNull();
      expect(resolveExternalHref('')).toBeNull();
      expect(resolveExternalHref('   ')).toBeNull();
    });

    it('rejects non-HTTPS URLs and protocols', () => {
      expect(resolveExternalHref('http://example.com')).toBeNull();
      expect(resolveExternalHref('ftp://example.com')).toBeNull();
      expect(resolveExternalHref('javascript:alert(1)')).toBeNull();
      expect(resolveExternalHref('/internal/path')).toBeNull();
    });

    it('verifies static link attributes and accessible new tab text', () => {
      expect(EXTERNAL_LINK_ATTRS.target).toBe('_blank');
      expect(EXTERNAL_LINK_ATTRS.rel).toBe('noopener noreferrer');
      expect(NEW_TAB_TEXT).toBe('(opens in a new tab)');
    });
  });
});
'@ | Set-Content "tests\unit\components\ui\shared.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/shared.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 8.1, Req 8.4, Req 11.1, Req 12.1, Req 14.1

---

### M3.G1.T7: Audit M1 Configuration Gaps & Create `task-notes.md`

**Objective:** Audit `tailwind.config.ts` and `globals.css` against `design.md` Sections 3–5, verify token presence, and record all interim configuration gaps in `.kiro/specs/m3-design-system-implementation/task-notes.md`.

**Acceptance Criteria:**
- ✓ Directory `.kiro/specs/m3-design-system-implementation/` contains `task-notes.md`
- ✓ Documents Button `md` height gap: 40px required by `design.md`, but M1 lacks `space-10` (interim: use Tailwind standard `h-10`)
- ✓ Documents Wide-desktop breakpoint gap: 1440px required by `design.md` 5.1, but M1 uses Tailwind default screens (interim: capped by `max-w-screen-xl`)
- ✓ Documents Dark mode status: M1 defines dark tokens, but `design.md` 7.7 requires dark mode disabled by default
- ✓ Verifies zero edits made to `tailwind.config.ts` or `globals.css`

**Prerequisites:**
- Project root exists

**Implementation Details:**

Write `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path ".kiro\specs\m3-design-system-implementation")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m3-design-system-implementation" -Force | Out-Null
}

@'
# M3 Design System Implementation — Task Notes & Audit Log

## 1. M1 Configuration Gaps & Interim Decisions (Req 1.4, Req 13.6)

Per `AGENTS.md` Section 6.2, root configuration files must not be altered without explicit human approval. The following discrepancies between `design.md` and M1 `tailwind.config.ts` are recorded:

| Gap / Token | Specification Target | M1 Tailwind Status | Interim Implementation Approach |
| :--- | :--- | :--- | :--- |
| **Button `md` Height** | `40px` (`design.md` 4.1, Req 2.2) | `spacing` extension lists `1,2,3,4,6,8,12,16,24`. Lacks `10` (`2.5rem` / `40px`). | Use built-in Tailwind class `h-10` (`2.5rem` = `40px`). Do not add custom spacing tokens without approval. |
| **Wide Desktop Breakpoint** | `1440px` (`design.md` 5.1) | Tailwind defaults: `sm: 640`, `md: 768`, `lg: 1024`, `xl: 1280`, `2xl: 1536`. Lacks `1440px` screen. | `Container` uses `md:` and `lg:` padding steps plus `max-w-screen-xl` cap (`1280px`), fulfilling content bounds cleanly. |
| **Max Content Cap** | Max readable width (`design.md` 5.1) | No custom max-width token configured. | Use `max-w-screen-xl` on `Container`. |
| **Dark Mode Styling** | Disabled by default (`design.md` 7.7) | M1 `globals.css` specifies dark theme CSS variables under `@media (prefers-color-scheme: dark)`. | M3 UI primitives use semantic color tokens directly and apply zero `dark:` utility overrides. |

## 2. Dependency Approvals (Approval 1a, 2026-10-22)

Human approval was granted on 2026-10-22 for adding test tooling:
- `fast-check` (exact pinned version `3.23.2`): Property-based testing for pure logic and invariants.
- `vitest-axe` (exact pinned version `0.1.0`): Automated WCAG 2.1 AA accessibility checks.

Neither package affects the production bundle (`devDependencies` only).
'@ | Set-Content ".kiro\specs\m3-design-system-implementation\task-notes.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path ".kiro\specs\m3-design-system-implementation\task-notes.md"
```
Expected output: `True`

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 13.6, Req 16.5

---

### M3.G1.T8: Install Pinned Axe Accessibility Helper (`vitest-axe`)

**Objective:** Install `vitest-axe@0.1.0` into `devDependencies` per Approval 1a (2026-10-22) and document its purpose in `package.json`.

**Acceptance Criteria:**
- ✓ `vitest-axe` pinned exactly at `0.1.0` in `package.json` `devDependencies`
- ✓ `axe-core` resolves as underlying engine
- ✓ `npm install` completes cleanly with zero errors
- ✓ Verified as devDependency only; no production footprint

**Prerequisites:**
- M3.G1.T7 completed
- Approval 1a recorded

**Implementation Details:**

Install `vitest-axe` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install --save-dev --save-exact vitest-axe@0.1.0
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.devDependencies."vitest-axe" -eq "0.1.0") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.4, Req 16.5

---

### M3.G1.T9: Install Pinned Property-Based Testing Helper (`fast-check`)

**Objective:** Install `fast-check@3.23.2` into `devDependencies` per Approval 1a (2026-10-22) to enable property-based testing across M3.

**Acceptance Criteria:**
- ✓ `fast-check` pinned exactly at `3.23.2` in `package.json` `devDependencies`
- ✓ `npm install` completes cleanly
- ✓ Verified as devDependency only; no production bundle impact

**Prerequisites:**
- M3.G1.T7 completed
- Approval 1a recorded

**Implementation Details:**

Install `fast-check` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm install --save-dev --save-exact fast-check@3.23.2
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.devDependencies."fast-check" -eq "3.23.2") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.3, Req 15.4, Req 16.5

---

### M3.G1.T10: Checkpoint — Shared Modules and Foundation Verification

**Objective:** Execute the TypeScript compiler and Vitest runner to ensure all shared modules compile and pass testing, and verify that root styling files remain unmodified.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts globals.css` produces zero output
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test -- tests/unit/components/ui/shared.test.ts` passes with code 0

**Prerequisites:**
- M3.G1.T1 through M3.G1.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$diff = git diff tailwind.config.ts src/app/globals.css
if ($diff.Length -gt 0) {
    Write-Error "CRITICAL: tailwind.config.ts or globals.css was modified!"
    exit 1
}

npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/shared.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$diff = git diff tailwind.config.ts src/app/globals.css
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/shared.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($diff.Length -eq 0 -and $t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\cx.ts"
Test-Path "src\components\ui\focus-ring.ts"
Test-Path "src\components\ui\motion.ts"
Test-Path "src\components\ui\heading-level.ts"
Test-Path "src\components\ui\external-link-attrs.ts"
Test-Path "tests\unit\components\ui\shared.test.ts"
Test-Path ".kiro\specs\m3-design-system-implementation\task-notes.md"
npm run typecheck
npm run test -- tests/unit/components/ui/shared.test.ts
```
Expected output:
- `True` for all 7 file existence checks
- `npm run typecheck` exits with return code 0
- Unit tests pass with 0 errors.