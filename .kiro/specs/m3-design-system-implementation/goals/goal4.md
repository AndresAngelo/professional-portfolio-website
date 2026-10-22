# M3.G4: Tag, TagList, and StatusBadge

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the non-interactive `Tag` and `TagList` primitives in `src/components/ui/tag.tsx` and the semantic `StatusBadge` primitive in `src/components/ui/status-badge.tsx`. Enforce strict non-interactivity on `Tag` (prohibiting `role="button"`, `tabindex`, and click handlers) while wrapping grouped tags in an accessible unordered list (`<ul>`). Implement `StatusBadge` consuming the canonical `ProjectStatus` enum from `@/types/content` with an exhaustive `Record<ProjectStatus, ...>` mapping, guaranteeing compile-time errors if any status value is omitted, and verifying visible text labels alongside semantic colors per `design.md` Section 4.4 and Requirement 5.

## Goal Success Criteria

- ✓ `src/components/ui/tag.tsx` implements `Tag` and `TagList` as server components without `'use client'`
- ✓ `Tag` applies `radius-sm`, `bg-surface`, `border-border-default`, `text-caption`, `text-text-secondary`, and `space-1`–`space-3` padding tokens
- ✓ `Tag` carries no `role="button"`, no `tabindex`, and no pointer event handlers
- ✓ `TagList` renders an unordered list (`<ul>`) with a required `aria-label` and `<li>` items
- ✓ `TagList` renders `null` when given an empty or undefined `tags` array
- ✓ `src/components/ui/status-badge.tsx` imports `ProjectStatus` from `@/types/content` without redeclaring it
- ✓ `StatusBadge` maps statuses exhaustively to visible text: `completed` $\rightarrow$ "Completed", `in-progress` $\rightarrow$ "In Progress", `archived` $\rightarrow$ "Archived"
- ✓ `StatusBadge` maps semantic colors: `completed` $\rightarrow$ `feedback-success`, `in-progress` $\rightarrow$ `feedback-warning`, `archived` $\rightarrow$ `text-text-secondary`
- ✓ `tests/unit/components/ui/tag.test.tsx` and `tests/unit/components/ui/status-badge.test.tsx` achieve 100% test pass rates
- ✓ `npm run typecheck` passes with zero errors

## Prerequisites

- Goal M3.G1 completed
- Milestone 2 content types available at `src/types/content.ts` (exporting `ProjectStatus`)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M3.G4.T1: Implement `Tag` and `TagList` Primitives (`src/components/ui/tag.tsx`)

**Objective:** Author the non-interactive `Tag` and `TagList` components in `src/components/ui/tag.tsx` using SGDS semantic tokens.

**Acceptance Criteria:**
- ✓ File `src/components/ui/tag.tsx` created
- ✓ Exports `TagProps` and `TagListProps`
- ✓ Exports `Tag(props: TagProps): JSX.Element`
- ✓ Exports `TagList(props: TagListProps): JSX.Element | null`
- ✓ `Tag` renders a `<span>` with `inline-block rounded-sm border border-border-default bg-surface px-2 py-1 text-caption text-text-secondary`
- ✓ `TagList` renders `<ul aria-label={props['aria-label']}>` with `flex flex-wrap gap-2`
- ✓ Returns `null` if `tags` array is empty or length is 0
- ✓ Contains zero interactive roles, tabindex, or cursor-pointer styling

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/tag.tsx`

**Implementation Details:**

Write `src/components/ui/tag.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { cx } from './cx';

export interface TagProps {
  children: string;
  className?: string;
}

/**
 * Non-interactive metadata tag for skills and project categories.
 * AGENTS.md 4.4 & Requirement 4.
 */
export function Tag({ children, className }: TagProps): JSX.Element {
  return (
    <span
      className={cx(
        'inline-block rounded-sm border border-border-default bg-surface px-2 py-0.5 text-caption text-text-secondary select-none',
        className
      )}
    >
      {children}
    </span>
  );
}

export interface TagListProps {
  /** Accessible name describing the collection of tags (Req 4.5) */
  'aria-label': string;
  tags: readonly string[];
  className?: string;
}

/**
 * Grouped tag list rendered as an accessible unordered list.
 */
export function TagList({ 'aria-label': ariaLabel, tags, className }: TagListProps): JSX.Element | null {
  if (!tags || tags.length === 0) {
    return null;
  }

  return (
    <ul aria-label={ariaLabel} className={cx('flex flex-wrap gap-2 list-none p-0 m-0', className)}>
      {tags.map((tag, index) => (
        <li key={`${tag}-${index}`}>
          <Tag>{tag}</Tag>
        </li>
      ))}
    </ul>
  );
}
'@ | Set-Content "src\components\ui\tag.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/tag.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 4.5, Req 16.8

---

### M3.G4.T2: Implement `StatusBadge` Primitive (`src/components/ui/status-badge.tsx`)

**Objective:** Author `StatusBadge` in `src/components/ui/status-badge.tsx` consuming `ProjectStatus` with exhaustive compile-time verification.

**Acceptance Criteria:**
- ✓ File `src/components/ui/status-badge.tsx` created
- ✓ Imports `ProjectStatus` directly from `@/types/content` (does NOT redeclare it)
- ✓ Defines `STATUS_LABELS: Record<ProjectStatus, string>` with exact text labels
- ✓ Defines `STATUS_TOKENS: Record<ProjectStatus, string>` with semantic feedback tokens
- ✓ Renders `<span>` with `inline-flex items-center rounded-full border bg-surface px-2.5 py-0.5 text-caption font-medium`
- ✓ Renders visible text label conveying meaning alongside color (Req 5.4)
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M3.G1 completed
- `@/types/content` exports `ProjectStatus`
- Target file: `src/components/ui/status-badge.tsx`

**Implementation Details:**

Write `src/components/ui/status-badge.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { ProjectStatus } from '@/types/content';
import { cx } from './cx';

export interface StatusBadgeProps {
  status: ProjectStatus;
  className?: string;
}

const STATUS_LABELS: Record<ProjectStatus, string> = {
  completed: 'Completed',
  'in-progress': 'In Progress',
  archived: 'Archived',
};

const STATUS_TOKENS: Record<ProjectStatus, string> = {
  completed: 'text-feedback-success border-feedback-success',
  'in-progress': 'text-feedback-warning border-feedback-warning',
  archived: 'text-text-secondary border-border-default',
};

/**
 * StatusBadge Component
 *
 * Communicates project delivery state through a visible text label and semantic color.
 * Exhaustively typed against ProjectStatus per Requirement 5.
 */
export function StatusBadge({ status, className }: StatusBadgeProps): JSX.Element {
  const label = STATUS_LABELS[status];
  const tokenClasses = STATUS_TOKENS[status];

  return (
    <span
      className={cx(
        'inline-flex items-center rounded-full border bg-surface px-2.5 py-0.5 text-caption font-medium select-none',
        tokenClasses,
        className
      )}
    >
      {label}
    </span>
  );
}
'@ | Set-Content "src\components\ui\status-badge.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/status-badge.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 5.5, Req 16.4

---

### M3.G4.T3: Author Unit Tests for `Tag` and `TagList` (`tests/unit/components/ui/tag.test.tsx`)

**Objective:** Create `tests/unit/components/ui/tag.test.tsx` verifying non-interactivity, styling tokens, and accessible list rendering.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/tag.test.tsx` created
- ✓ Verifies `Tag` renders text content inside a `<span>`
- ✓ Verifies `Tag` has no `role="button"`, no `tabindex`, and no `cursor-pointer`
- ✓ Verifies `TagList` renders `<ul aria-label="...">` with `<li>` children
- ✓ Verifies `TagList` returns `null` when `tags` array is empty
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G4.T1 completed
- Target file: `tests/unit/components/ui/tag.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Tag, TagList } from '@/components/ui/tag';

describe('Tag and TagList Primitives (Req 4)', () => {
  describe('Tag', () => {
    it('renders text content with non-interactive span and token classes', () => {
      const { container } = render(<Tag>TypeScript</Tag>);
      const span = container.querySelector('span');

      expect(span).not.toBeNull();
      expect(span?.textContent).toBe('TypeScript');
      expect(span?.className).toContain('rounded-sm');
      expect(span?.className).toContain('border-border-default');
      expect(span?.className).toContain('bg-surface');
      expect(span?.className).toContain('text-caption');
      expect(span?.className).toContain('text-text-secondary');

      // Non-interactive guarantees
      expect(span?.getAttribute('role')).toBeNull();
      expect(span?.getAttribute('tabindex')).toBeNull();
      expect(span?.className).not.toContain('cursor-pointer');
    });
  });

  describe('TagList', () => {
    it('renders an accessible unordered list with list items', () => {
      render(<TagList aria-label="Project technologies" tags={['Next.js', 'TypeScript', 'Tailwind']} />);
      const list = screen.getByRole('list', { name: 'Project technologies' });

      expect(list).toBeDefined();
      const items = screen.getAllByRole('listitem');
      expect(items.length).toBe(3);
      expect(items[0]?.textContent).toBe('Next.js');
      expect(items[1]?.textContent).toBe('TypeScript');
      expect(items[2]?.textContent).toBe('Tailwind');
    });

    it('returns null when tags array is empty or undefined', () => {
      const { container: c1 } = render(<TagList aria-label="Empty list" tags={[]} />);
      expect(c1.firstChild).toBeNull();

      // @ts-expect-error testing runtime tolerance for undefined
      const { container: c2 } = render(<TagList aria-label="Undefined list" tags={undefined} />);
      expect(c2.firstChild).toBeNull();
    });
  });
});
'@ | Set-Content "tests\unit\components\ui\tag.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/tag.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4, Req 4.5, Req 14.1

---

### M3.G4.T4: Author Unit Tests for `StatusBadge` (`tests/unit/components/ui/status-badge.test.tsx`)

**Objective:** Create `tests/unit/components/ui/status-badge.test.tsx` asserting text labels, semantic feedback color tokens, and rounded-full badge styling for all 3 project statuses.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/status-badge.test.tsx` created
- ✓ Tests `completed`: renders "Completed" with `text-feedback-success`
- ✓ Tests `in-progress`: renders "In Progress" with `text-feedback-warning`
- ✓ Tests `archived`: renders "Archived" with `text-text-secondary`
- ✓ Verifies `rounded-full` styling token present on all badges
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G4.T2 completed
- Target file: `tests/unit/components/ui/status-badge.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StatusBadge } from '@/components/ui/status-badge';
import type { ProjectStatus } from '@/types/content';

describe('StatusBadge Primitive (Req 5)', () => {
  it.each([
    ['completed', 'Completed', 'text-feedback-success', 'border-feedback-success'],
    ['in-progress', 'In Progress', 'text-feedback-warning', 'border-feedback-warning'],
    ['archived', 'Archived', 'text-text-secondary', 'border-border-default'],
  ])('renders %s status with label "%s" and tokens %s / %s', (status, expectedLabel, textToken, borderToken) => {
    render(<StatusBadge status={status as ProjectStatus} />);
    const badge = screen.getByText(expectedLabel);

    expect(badge).toBeDefined();
    expect(badge.className).toContain('rounded-full');
    expect(badge.className).toContain('bg-surface');
    expect(badge.className).toContain(textToken);
    expect(badge.className).toContain(borderToken);
  });
});
'@ | Set-Content "tests\unit\components\ui\status-badge.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/status-badge.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.2, Req 5.3, Req 5.4, Req 14.1, Req 14.4

---

### M3.G4.T5: Author Compile-Time Exhaustiveness Test for `StatusBadge`

**Objective:** Append a compile-time exhaustiveness check ensuring `STATUS_LABELS` and `STATUS_TOKENS` produce TypeScript compilation errors if `ProjectStatus` is expanded without updating `status-badge.tsx`.

**Acceptance Criteria:**
- ✓ Test checks `Record<ProjectStatus, string>` exhaustiveness
- ✓ Contains type assertion verifying all keys of `ProjectStatus` are handled
- ✓ `npm run typecheck` passes with zero errors

**Prerequisites:**
- M3.G4.T2 completed
- Target file: `tests/unit/components/ui/status-badge.test.tsx`

**Implementation Details:**

Append exhaustiveness type test to `tests/unit/components/ui/status-badge.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Compile-Time Exhaustiveness (Req 5.5)', () => {
    it('exhaustively covers all ProjectStatus variants without missing mappings', () => {
      const allStatuses: ProjectStatus[] = ['completed', 'in-progress', 'archived'];
      for (const status of allStatuses) {
        const { unmount } = render(<StatusBadge status={status} />);
        unmount();
      }
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\status-badge.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\status-badge.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.5, Req 16.1

---

### M3.G4.T6: Author Property-Based Test for Tag Non-Interactivity (Property 5)

**Objective:** Append property-based test in `tests/unit/components/ui/tag.test.tsx` using `fast-check` to assert that for any arbitrary label string, `Tag` renders exact text content and contains no button role, no tabindex, and no click handlers.

**Acceptance Criteria:**
- ✓ Executes at least 100 iterations with `fast-check`
- ✓ Generates randomized string labels
- ✓ Asserts `textContent` equals input string
- ✓ Asserts `role` attribute is null and `tabindex` is null
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/tag.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/tag.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Test: Tag Invariants (Property 5)', () => {
    it('Feature: m3-design-system-implementation, Property 5: renders exact label string and remains non-interactive for any string', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 30 }).filter((s: string) => s.trim().length > 0),
          (label: string) => {
            cleanup();
            const { container } = render(<Tag>{label}</Tag>);
            const span = container.querySelector('span');

            expect(span).not.toBeNull();
            expect(span?.textContent).toBe(label);
            expect(span?.getAttribute('role')).toBeNull();
            expect(span?.getAttribute('tabindex')).toBeNull();
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\tag.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\tag.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/tag.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.2, Req 4.3, Req 4.4, Req 14.1

---

### M3.G4.T7: Author Property-Based Test for StatusBadge Label & Color Mapping (Property 6)

**Objective:** Append property-based test in `tests/unit/components/ui/status-badge.test.tsx` verifying Property 6: StatusBadge maps every `ProjectStatus` value to visible text and semantic tokens.

**Acceptance Criteria:**
- ✓ Uses `fast-check` over `fc.constantFrom('completed', 'in-progress', 'archived')`
- ✓ Asserts visible text label is never empty
- ✓ Asserts semantic feedback token is applied
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/status-badge.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/status-badge.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Test: StatusBadge Mappings (Property 6)', () => {
    it('Feature: m3-design-system-implementation, Property 6: renders visible text label and semantic color token for any ProjectStatus', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.constantFrom('completed', 'in-progress', 'archived'),
          (status: ProjectStatus) => {
            cleanup();
            const { container } = render(<StatusBadge status={status} />);
            const span = container.querySelector('span');

            expect(span).not.toBeNull();
            expect(span?.textContent).toBeTruthy();
            expect(span?.className).toContain('bg-surface');

            if (status === 'completed') expect(span?.className).toContain('text-feedback-success');
            if (status === 'in-progress') expect(span?.className).toContain('text-feedback-warning');
            if (status === 'archived') expect(span?.className).toContain('text-text-secondary');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\status-badge.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\status-badge.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/status-badge.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.2, Req 5.3, Req 5.4, Req 14.4

---

### M3.G4.T8: Author Automated Axe Accessibility Tests

**Objective:** Append axe accessibility checks for `Tag`, `TagList`, and all 3 variants of `StatusBadge` using `vitest-axe`.

**Acceptance Criteria:**
- ✓ `Tag` passes axe with 0 violations
- ✓ `TagList` passes axe with 0 violations
- ✓ All 3 variants of `StatusBadge` pass axe with 0 violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target files: `tag.test.tsx` and `status-badge.test.tsx`

**Implementation Details:**

Append axe tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Append to tag.test.tsx
$appendTagAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it('produces zero accessibility violations for Tag and TagList', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <TagList aria-label="Accessible skills list" tags={['HTML', 'CSS', 'JavaScript']} />
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@
$tagContent = Get-Content "tests\unit\components\ui\tag.test.tsx" -Raw
$tagContent = $tagContent -replace "\s*\}\);\s*$", "$appendTagAxe`n});`n"
$tagContent | Set-Content "tests\unit\components\ui\tag.test.tsx" -Encoding UTF8

# 2. Append to status-badge.test.tsx
$appendBadgeAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it.each(['completed', 'in-progress', 'archived'])('produces zero violations for status %s', async (status) => {
      const { axe } = require('vitest-axe');
      const { container } = render(<StatusBadge status={status as ProjectStatus} />);

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@
$badgeContent = Get-Content "tests\unit\components\ui\status-badge.test.tsx" -Raw
$badgeContent = $badgeContent -replace "\s*\}\);\s*$", "$appendBadgeAxe`n});`n"
$badgeContent | Set-Content "tests\unit\components\ui\status-badge.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/tag.test.tsx tests/unit/components/ui/status-badge.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G4.T9: Verify Source Hygiene of `tag.tsx` and `status-badge.tsx`

**Objective:** Audit `src/components/ui/tag.tsx` and `src/components/ui/status-badge.tsx` to verify zero raw hex colors, zero arbitrary classes, zero `any`, and zero `'use client'`.

**Acceptance Criteria:**
- ✓ Both files contain zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Both files contain zero `rgb(`/`rgba(`
- ✓ Both files contain zero arbitrary Tailwind brackets `[` or `]`
- ✓ Both files contain zero `any` or non-null assertions `!`
- ✓ Both files contain zero `'use client'` statements
- ✓ Both files are under 300 lines

**Prerequisites:**
- M3.G4.T1 and M3.G4.T2 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\components\ui\tag.tsx", "src\components\ui\status-badge.tsx")
$allPass = $true

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    $lines = (Get-Content $file).Count

    $hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
    $hasRgb = $content -match 'rgba?\('
    $hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
    $hasAny = $content -match ':\s*any\b|\bas\s+any\b'
    $hasClient = $content -match "['""]use client['""]"

    if ($hasHex -or $hasRgb -or $hasArbitrary -or $hasAny -or $hasClient -or ($lines -ge 300)) {
        $allPass = $false
        Write-Host "Violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.8

---

### M3.G4.T10: Checkpoint — Tag and StatusBadge Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across Tag, TagList, and StatusBadge.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all tag and status badge tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G4.T1 through M3.G4.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/tag.test.tsx tests/unit/components/ui/status-badge.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/tag.test.tsx tests/unit/components/ui/status-badge.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\ui\tag.tsx"
Test-Path "src\components\ui\status-badge.tsx"
Test-Path "tests\unit\components\ui\tag.test.tsx"
Test-Path "tests\unit\components\ui\status-badge.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/tag.test.tsx tests/unit/components/ui/status-badge.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- All tests pass with exit code 0.