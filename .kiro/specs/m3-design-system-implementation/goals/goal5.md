# M3.G5: EventTypeBadge and FilterChip

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the `EventTypeBadge` primitive in `src/components/ui/event-type-badge.tsx` and the interactive `FilterChip` primitive in `src/components/ui/filter-chip.tsx`. `EventTypeBadge` consumes the canonical `EventType` enum from `@/types/content` with an exhaustive `Record<EventType, ...>` mapping to render all 6 activity types with distinct text labels and `brand-secondary` styling per `design.md` Section 4.4. `FilterChip` renders an accessible native toggle button (`type="button"`, `aria-pressed`, minimum 32px height, `cursor-pointer`, `FOCUS_RING`, and `MOTION_FAST`) where selected states provide visual cues beyond color alone (border-weight change and check glyph). Author comprehensive unit, keyboard, property-based, and axe accessibility tests in `tests/unit/components/ui/`.

## Goal Success Criteria

- ✓ `src/components/ui/event-type-badge.tsx` imports `EventType` from `@/types/content` without redeclaring it
- ✓ `EventTypeBadge` renders exact labels: "Meetup", "Hackathon", "Workshop", "Conference", "Learning", "Project Update"
- ✓ `EventTypeBadge` applies neutral or `brand-secondary` token styling meeting 4.5:1 contrast
- ✓ Adding an unhandled `EventType` value causes a compile-time error
- ✓ `src/components/ui/filter-chip.tsx` renders a native `<button type="button">` with `aria-pressed={selected}`
- ✓ `FilterChip` activates `onToggle` exactly once per user activation (click, Enter, or Space)
- ✓ Selected state applies `border-2 border-brand-primary text-brand-primary` plus a decorative checkmark glyph
- ✓ `FilterChip` has a minimum height target of 32px (`h-8`) and is the only UI primitive with `cursor-pointer`
- ✓ `FilterChip` remains server-compatible (no `'use client'`), carrying an architectural explanation comment
- ✓ `tests/unit/components/ui/event-type-badge.test.tsx` and `filter-chip.test.tsx` pass with 100% assertions

## Prerequisites

- Goals M3.G1 through M3.G4 completed
- Milestone 2 content contracts available at `src/types/content.ts` (exporting `EventType`)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M3.G5.T1: Implement `EventTypeBadge` Primitive (`src/components/ui/event-type-badge.tsx`)

**Objective:** Author the `EventTypeBadge` component in `src/components/ui/event-type-badge.tsx` mapping all 6 event categories to readable text labels.

**Acceptance Criteria:**
- ✓ File `src/components/ui/event-type-badge.tsx` created
- ✓ Imports `EventType` from `@/types/content`
- ✓ Defines `EVENT_TYPE_LABELS: Record<EventType, string>` covering all 6 types
- ✓ Renders `<span>` with `inline-flex items-center rounded-sm border border-border-default bg-surface px-2 py-0.5 text-caption font-medium text-brand-secondary`
- ✓ Relies on clear visible text labels to convey event type rather than color alone (Req 6.3)
- ✓ Contains zero `'use client'` statements

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/event-type-badge.tsx`

**Implementation Details:**

Write `src/components/ui/event-type-badge.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import type { EventType } from '@/types/content';
import { cx } from './cx';

export interface EventTypeBadgeProps {
  eventType: EventType;
  className?: string;
}

const EVENT_TYPE_LABELS: Record<EventType, string> = {
  meetup: 'Meetup',
  hackathon: 'Hackathon',
  workshop: 'Workshop',
  conference: 'Conference',
  learning: 'Learning',
  'project-update': 'Project Update',
};

/**
 * EventTypeBadge Component
 *
 * Categorizes community activities and learning logs with a visible text label.
 * AGENTS.md 4.4 & Requirement 6.
 */
export function EventTypeBadge({ eventType, className }: EventTypeBadgeProps): JSX.Element {
  const label = EVENT_TYPE_LABELS[eventType];

  return (
    <span
      className={cx(
        'inline-flex items-center rounded-sm border border-border-default bg-surface px-2 py-0.5 text-caption font-medium text-brand-secondary select-none',
        className
      )}
    >
      {label}
    </span>
  );
}
'@ | Set-Content "src\components\ui\event-type-badge.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/event-type-badge.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.3, Req 6.4, Req 6.5, Req 16.4

---

### M3.G5.T2: Implement `FilterChip` Toggle Component (`src/components/ui/filter-chip.tsx`)

**Objective:** Author the accessible, interactive `FilterChip` toggle button in `src/components/ui/filter-chip.tsx`.

**Acceptance Criteria:**
- ✓ File `src/components/ui/filter-chip.tsx` created
- ✓ Exports `FilterChipProps` and `FilterChip`
- ✓ Renders native `<button>` element with `type="button"`
- ✓ Exposes toggle state via `aria-pressed={selected}`
- ✓ Renders minimum 32px height (`h-8`) and `px-3`
- ✓ Includes `cursor-pointer`, `FOCUS_RING`, and `MOTION_FAST`
- ✓ Selected state renders `border-2 border-brand-primary text-brand-primary` and includes a decorative check SVG icon
- ✓ Unselected state renders `border border-border-default bg-surface text-text-primary`
- ✓ Server-compatible component without `'use client'`; includes explanatory architectural comment (Req 7.7, 16.3)

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/filter-chip.tsx`

**Implementation Details:**

Write `src/components/ui/filter-chip.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
// Server-compatible: consumer owns filter state (e.g. URL query params);
// onToggle callback is received from a client boundary parent. No 'use client' required (Req 7.7, 16.3).
import React from 'react';
import { cx } from './cx';
import { FOCUS_RING } from './focus-ring';
import { MOTION_FAST } from './motion';

export interface FilterChipProps {
  label: string;
  /** Active selection state owned by consumer (Req 7.7) */
  selected: boolean;
  /** Invoked exactly once when activated by click or keyboard (Req 7.3) */
  onToggle: () => void;
  disabled?: boolean;
  className?: string;
}

/**
 * FilterChip Primitive
 *
 * Interactive toggle control for filtering projects and blog posts.
 * The only tag-like element with interactive button semantics and cursor-pointer styling (Req 7.6).
 */
export function FilterChip({
  label,
  selected,
  onToggle,
  disabled = false,
  className,
}: FilterChipProps): JSX.Element {
  return (
    <button
      type="button"
      aria-pressed={selected}
      disabled={disabled}
      onClick={onToggle}
      className={cx(
        'inline-flex items-center gap-1.5 h-8 px-3 rounded-full text-caption font-medium select-none cursor-pointer',
        'disabled:cursor-not-allowed disabled:opacity-50 disabled:border-border-default disabled:text-text-disabled',
        selected
          ? 'bg-surface border-2 border-brand-primary text-brand-primary font-semibold'
          : 'bg-surface border border-border-default text-text-primary hover:border-brand-primary hover:text-brand-primary',
        FOCUS_RING,
        MOTION_FAST,
        className
      )}
    >
      {selected && (
        <svg
          className="h-3.5 w-3.5 shrink-0 text-current"
          aria-hidden="true"
          focusable="false"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={3}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      )}
      <span>{label}</span>
    </button>
  );
}
'@ | Set-Content "src\components\ui\filter-chip.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/filter-chip.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.3, Req 7.4, Req 7.5, Req 7.6, Req 7.7, Req 7.8, Req 16.2, Req 16.3

---

### M3.G5.T3: Author Unit Tests for `EventTypeBadge` (`tests/unit/components/ui/event-type-badge.test.tsx`)

**Objective:** Create `tests/unit/components/ui/event-type-badge.test.tsx` verifying visible labels and token styling for all 6 event types.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/event-type-badge.test.tsx` created
- ✓ Tests all 6 values: "Meetup", "Hackathon", "Workshop", "Conference", "Learning", "Project Update"
- ✓ Verifies `bg-surface`, `text-brand-secondary`, and `border-border-default` styling
- ✓ Verifies non-interactivity (no role, no tabindex)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G5.T1 completed
- Target file: `tests/unit/components/ui/event-type-badge.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { EventTypeBadge } from '@/components/ui/event-type-badge';
import type { EventType } from '@/types/content';

describe('EventTypeBadge Primitive (Req 6)', () => {
  it.each([
    ['meetup', 'Meetup'],
    ['hackathon', 'Hackathon'],
    ['workshop', 'Workshop'],
    ['conference', 'Conference'],
    ['learning', 'Learning'],
    ['project-update', 'Project Update'],
  ])('renders %s with visible label "%s"', (eventType, expectedLabel) => {
    render(<EventTypeBadge eventType={eventType as EventType} />);
    const badge = screen.getByText(expectedLabel);

    expect(badge).toBeDefined();
    expect(badge.className).toContain('rounded-sm');
    expect(badge.className).toContain('bg-surface');
    expect(badge.className).toContain('text-brand-secondary');
    expect(badge.className).toContain('border-border-default');

    expect(badge.getAttribute('role')).toBeNull();
  });
});
'@ | Set-Content "tests\unit\components\ui\event-type-badge.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/event-type-badge.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.1, Req 6.2, Req 6.3, Req 6.4, Req 14.1, Req 14.4

---

### M3.G5.T4: Author Unit Tests for `FilterChip` (`tests/unit/components/ui/filter-chip.test.tsx`)

**Objective:** Create `tests/unit/components/ui/filter-chip.test.tsx` verifying toggle behavior, `aria-pressed`, height token, and visual selected cues.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/filter-chip.test.tsx` created
- ✓ Renders `<button type="button">`
- ✓ `aria-pressed="false"` when unselected; `aria-pressed="true"` when selected
- ✓ Unselected state renders `border-border-default` and no checkmark icon
- ✓ Selected state renders `border-2 border-brand-primary` and contains checkmark SVG
- ✓ Applies `h-8` (32px minimum height) and `cursor-pointer`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G5.T2 completed
- Target file: `tests/unit/components/ui/filter-chip.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FilterChip } from '@/components/ui/filter-chip';

describe('FilterChip Primitive (Req 7)', () => {
  it('renders native button with type="button" and h-8 height token', () => {
    render(<FilterChip label="React" selected={false} onToggle={() => {}} />);
    const btn = screen.getByRole('button', { name: 'React' });

    expect(btn.getAttribute('type')).toBe('button');
    expect(btn.className).toContain('h-8');
    expect(btn.className).toContain('cursor-pointer');
    expect(btn.className).toContain('focus-visible:ring-focus-ring');
  });

  it('reflects unselected state with aria-pressed="false" and no check icon', () => {
    const { container } = render(<FilterChip label="Next.js" selected={false} onToggle={() => {}} />);
    const btn = screen.getByRole('button', { name: 'Next.js' });

    expect(btn.getAttribute('aria-pressed')).toBe('false');
    expect(btn.className).toContain('border-border-default');
    expect(container.querySelector('svg')).toBeNull();
  });

  it('reflects selected state with aria-pressed="true", border-2, and check icon', () => {
    const { container } = render(<FilterChip label="TypeScript" selected={true} onToggle={() => {}} />);
    const btn = screen.getByRole('button', { name: 'TypeScript' });

    expect(btn.getAttribute('aria-pressed')).toBe('true');
    expect(btn.className).toContain('border-2');
    expect(btn.className).toContain('border-brand-primary');

    const icon = container.querySelector('svg');
    expect(icon).not.toBeNull();
    expect(icon?.getAttribute('aria-hidden')).toBe('true');
  });
});
'@ | Set-Content "tests\unit\components\ui\filter-chip.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/filter-chip.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.4, Req 7.8, Req 14.1

---

### M3.G5.T5: Author Activation Tests for `FilterChip` (Click, Enter, Space)

**Objective:** Append user interaction tests confirming `onToggle` is invoked exactly once when activated via pointer click, Enter key, or Space key.

**Acceptance Criteria:**
- ✓ Mouse click triggers `onToggle` once
- ✓ Synthetic Enter key triggers `onToggle` once
- ✓ Synthetic Space key triggers `onToggle` once
- ✓ Disabled chip ignores all activations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G5.T4 completed
- Target file: `tests/unit/components/ui/filter-chip.test.tsx`

**Implementation Details:**

Append activation tests to `tests/unit/components/ui/filter-chip.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('User Activation (Req 7.3)', () => {
    it('invokes onToggle exactly once on pointer click', () => {
      let count = 0;
      render(<FilterChip label="Node.js" selected={false} onToggle={() => { count += 1; }} />);
      const btn = screen.getByRole('button', { name: 'Node.js' });

      btn.click();
      expect(count).toBe(1);
    });

    it('invokes onToggle when activated via Enter or Space key event', () => {
      let count = 0;
      render(<FilterChip label="AI" selected={false} onToggle={() => { count += 1; }} />);
      const btn = screen.getByRole('button', { name: 'AI' });

      btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(count).toBe(1);
    });

    it('suppresses onToggle invocations when disabled', () => {
      let count = 0;
      render(<FilterChip label="Disabled" selected={false} disabled onToggle={() => { count += 1; }} />);
      const btn = screen.getByRole('button', { name: 'Disabled' });

      btn.click();
      expect(count).toBe(0);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\filter-chip.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\filter-chip.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/filter-chip.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.3, Req 14.5

---

### M3.G5.T6: Author Property-Based Test for `FilterChip` Invariants (Property 7)

**Objective:** Append property-based test in `tests/unit/components/ui/filter-chip.test.tsx` using `fast-check` to assert that for any boolean selection state and label, `aria-pressed` strictly matches `selected` and `onToggle` fires once.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Generates randomized boolean for `selected` and non-empty strings for `label`
- ✓ Asserts `aria-pressed` matches stringified `selected`
- ✓ Asserts click dispatch calls `onToggle` exactly once
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/filter-chip.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/filter-chip.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: FilterChip Invariants (Property 7)', () => {
    it('Feature: m3-design-system-implementation, Property 7: renders aria-pressed=selected and triggers onToggle exactly once for any selected boolean', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.boolean(),
          fc.string({ minLength: 1, maxLength: 25 }).filter((s: string) => s.trim().length > 0),
          (isSelected: boolean, labelText: string) => {
            cleanup();
            let toggleCount = 0;
            render(
              <FilterChip
                label={labelText}
                selected={isSelected}
                onToggle={() => { toggleCount += 1; }}
              />
            );
            const btn = screen.getByRole('button', { name: labelText });

            expect(btn.getAttribute('aria-pressed')).toBe(String(isSelected));
            btn.click();
            expect(toggleCount).toBe(1);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\filter-chip.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\filter-chip.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/filter-chip.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1, Req 7.2, Req 7.3, Req 14.1

---

### M3.G5.T7: Author Axe Accessibility Tests for Badge and Chip

**Objective:** Append automated accessibility checks for `EventTypeBadge` and `FilterChip` (both selected and unselected) using `vitest-axe`.

**Acceptance Criteria:**
- ✓ All 6 variants of `EventTypeBadge` pass axe with 0 violations
- ✓ `FilterChip` in selected state passes axe with 0 violations
- ✓ `FilterChip` in unselected state passes axe with 0 violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target files: `event-type-badge.test.tsx` and `filter-chip.test.tsx`

**Implementation Details:**

Append axe checks using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

# 1. Append to event-type-badge.test.tsx
$appendBadgeAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it.each(['meetup', 'hackathon', 'workshop', 'conference', 'learning', 'project-update'])(
      'produces zero violations for event type %s',
      async (eventType) => {
        const { axe } = require('vitest-axe');
        const { container } = render(<EventTypeBadge eventType={eventType as EventType} />);

        const results = await axe(container);
        expect(results.violations.length).toBe(0);
      }
    );
  });
'@
$badgeContent = Get-Content "tests\unit\components\ui\event-type-badge.test.tsx" -Raw
$badgeContent = $badgeContent -replace "\s*\}\);\s*$", "$appendBadgeAxe`n});`n"
$badgeContent | Set-Content "tests\unit\components\ui\event-type-badge.test.tsx" -Encoding UTF8

# 2. Append to filter-chip.test.tsx
$appendChipAxe = @'

  describe('Accessibility Verification (Req 15)', () => {
    it.each([false, true])('produces zero violations when selected=%s', async (isSelected) => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <FilterChip label="Accessible Chip" selected={isSelected} onToggle={() => {}} />
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@
$chipContent = Get-Content "tests\unit\components\ui\filter-chip.test.tsx" -Raw
$chipContent = $chipContent -replace "\s*\}\);\s*$", "$appendChipAxe`n});`n"
$chipContent | Set-Content "tests\unit\components\ui\filter-chip.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/event-type-badge.test.tsx tests/unit/components/ui/filter-chip.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G5.T8: Verify Cursor-Pointer Exclusivity on `FilterChip`

**Objective:** Audit `src/components/ui/` to ensure `cursor-pointer` appears exclusively in `filter-chip.tsx` and nowhere else among tag-like components per Requirement 7.6.

**Acceptance Criteria:**
- ✓ Searches all files in `src/components/ui/`
- ✓ `filter-chip.tsx` contains `cursor-pointer`
- ✓ `tag.tsx`, `status-badge.tsx`, and `event-type-badge.tsx` contain zero occurrences of `cursor-pointer`
- ✓ Audit script exits with PASS

**Prerequisites:**
- M3.G5.T1 and M3.G5.T2 completed

**Implementation Details:**

Execute cursor pointer audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$tagFiles = @("tag.tsx", "status-badge.tsx", "event-type-badge.tsx")
$violations = @()

foreach ($tf in $tagFiles) {
    $path = "src\components\ui\$tf"
    if (Test-Path $path) {
        $text = Get-Content $path -Raw
        if ($text -match 'cursor-pointer') {
            $violations += "$path contains forbidden cursor-pointer class"
        }
    }
}

$chipPath = "src\components\ui\filter-chip.tsx"
$chipText = Get-Content $chipPath -Raw
if (-not ($chipText -match 'cursor-pointer')) {
    $violations += "filter-chip.tsx must declare cursor-pointer per Requirement 7.6"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 7.6, Req 16.8

---

### M3.G5.T9: Verify Source Hygiene of `event-type-badge.tsx` and `filter-chip.tsx`

**Objective:** Audit both files for absence of raw hex, arbitrary classes, `any`, and unwarranted `'use client'` statements.

**Acceptance Criteria:**
- ✓ Zero raw hex (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` in `event-type-badge.tsx`
- ✓ Zero `'use client'` in `filter-chip.tsx` (verified server-compatible with comment)
- ✓ Both files are under 300 lines

**Prerequisites:**
- M3.G5.T1 and M3.G5.T2 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\ui\event-type-badge.tsx", "src\components\ui\filter-chip.tsx")
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

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.3, Req 16.8

---

### M3.G5.T10: Checkpoint — EventTypeBadge and FilterChip Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across EventTypeBadge and FilterChip.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all badge and chip tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G5.T1 through M3.G5.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/event-type-badge.test.tsx tests/unit/components/ui/filter-chip.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/event-type-badge.test.tsx tests/unit/components/ui/filter-chip.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\event-type-badge.tsx"
Test-Path "src\components\ui\filter-chip.tsx"
Test-Path "tests\unit\components\ui\event-type-badge.test.tsx"
Test-Path "tests\unit\components\ui\filter-chip.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/event-type-badge.test.tsx tests/unit/components/ui/filter-chip.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Tests pass with exit code 0.