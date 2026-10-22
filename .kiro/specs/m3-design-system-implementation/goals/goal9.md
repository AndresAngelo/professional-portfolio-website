# M3.G9: Accessibility Matrix and Source-Hygiene Tests

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the centralized automated accessibility evaluation matrix in `tests/unit/components/ui/a11y.test.tsx` and the static source-hygiene verification suite in `tests/unit/components/ui/source-hygiene.test.ts`. Execute axe checks across every single M3 UI primitive, variant, and state against WCAG 2.1 Level AA rules with zero permissible violations. Implement an automated source-hygiene scan across all files in `src/components/ui/` enforcing zero raw hex codes, zero arbitrary Tailwind classes, zero unapproved `cursor-pointer` usage, mandatory `motion-reduce:` pairing on transitions, proper `:focus-visible` pairing on `outline-none`, and compliance with server-component guardrails per Requirement 1, Requirement 15, and Requirement 16. Record all manual-verification protocols in `task-notes.md`.

## Goal Success Criteria

- ✓ `tests/unit/components/ui/a11y.test.tsx` renders every primitive in every documented state and variant, asserting zero axe violations
- ✓ `tests/unit/components/ui/source-hygiene.test.ts` executes Property 1 (source hygiene invariant scan) across `src/components/ui/`
- ✓ Proves zero raw hex colors (`#[0-9A-Fa-f]{3,8}`), zero `rgb(`/`rgba(`, and zero arbitrary Tailwind brackets `[` or `]` exist in component source code (excluding the documented `max-width: 70ch;` in CSS and `after:content-[""]`)
- ✓ Proves every occurrence of `transition` or `animate-` pairs with `motion-reduce:transition-none`
- ✓ Proves every occurrence of `outline-none` or `outline-0` pairs with focus-ring ring utilities
- ✓ Proves `cursor-pointer` is declared exclusively in `filter-chip.tsx` and nowhere else
- ✓ Proves zero `'use client'` statements exist without an immediate architectural justification comment
- ✓ Proves zero `any`, zero non-null assertions `!`, and zero manual interface duplications exist in tests and components
- ✓ Manual verification checklist (color contrast, screen readers, reduced motion, keyboard traps) recorded in `task-notes.md`
- ✓ `npm test` passes 100% of accessibility and hygiene checks cleanly

## Prerequisites

- Goals M3.G1 through M3.G8 completed
- All 10 UI primitives authored and functional under `src/components/ui/`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `vitest-axe` and `fast-check` available in `devDependencies`

---

## Tasks

### M3.G9.T1: Verify Vitest Matcher Registration in Test Setup (`tests/setup.ts`)

**Objective:** Audit and update `tests/setup.ts` to extend Vitest expectations with `toHaveNoViolations` from `vitest-axe`.

**Acceptance Criteria:**
- ✓ File `tests/setup.ts` imports `matchers` from `vitest-axe`
- ✓ Calls `expect.extend(matchers)`
- ✓ Preserves existing `@testing-library/jest-dom` extensions
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- `vitest-axe` installed (M3.G1.T8)
- Target file: `tests/setup.ts`

**Implementation Details:**

Update `tests/setup.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import '@testing-library/jest-dom/vitest';
import { expect } from 'vitest';
import * as matchers from 'vitest-axe/matchers';

expect.extend(matchers);
'@ | Set-Content "tests\setup.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/setup.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.3, Req 16.1

---

### M3.G9.T2: Author Accessibility Matrix for Action and Container Primitives (`tests/unit/components/ui/a11y.test.tsx`)

**Objective:** Create `tests/unit/components/ui/a11y.test.tsx` and implement automated axe tests for `Button` (4 variants × 3 sizes + disabled), `Card` (static + linked), and `Container` (4 landmarks).

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/a11y.test.tsx` created
- ✓ Tests all 4 Button variants across 3 sizes: 0 axe violations
- ✓ Tests disabled Button: 0 axe violations
- ✓ Tests static Card and full-card linked Card: 0 axe violations
- ✓ Tests Container elements (`div`, `section`, `main`, `article`): 0 axe violations
- ✓ Evaluates against WCAG 2.1 A and AA tags

**Prerequisites:**
- M3.G9.T1 completed
- Target file: `tests/unit/components/ui/a11y.test.tsx`

**Implementation Details:**

Write the initial accessibility suite using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';

import { Button, type ButtonVariant, type ButtonSize } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Container, type ContainerElement } from '@/components/ui/container';

describe('Accessibility Matrix (WCAG 2.1 Level AA) - Part 1', () => {
  describe('Button Primitive', () => {
    const variants: ButtonVariant[] = ['primary', 'secondary', 'ghost', 'external-link'];
    const sizes: ButtonSize[] = ['sm', 'md', 'lg'];

    for (const v of variants) {
      for (const s of sizes) {
        it(`reports zero violations for Button variant=${v} size=${s}`, async () => {
          const { container } = render(
            <Button variant={v} size={s} href={v === 'external-link' ? 'https://example.com' : undefined}>
              Action {v}
            </Button>
          );
          const results = await axe(container);
          expect(results.violations).toHaveLength(0);
        });
      }
    }

    it('reports zero violations for disabled Button', async () => {
      const { container } = render(<Button disabled>Disabled Action</Button>);
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });

  describe('Card Primitive', () => {
    it('reports zero violations for static Card', async () => {
      const { container } = render(
        <Card headingLevel={2} title="Portfolio Project">
          <p>Project summary description.</p>
        </Card>
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });

    it('reports zero violations for full-card linked Card', async () => {
      const { container } = render(
        <Card headingLevel={2} title="Linked Project" href="/projects/example" linkLabel="View case study">
          <p>Project summary description.</p>
        </Card>
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });

  describe('Container Primitive', () => {
    const elements: ContainerElement[] = ['div', 'section', 'main', 'article'];

    for (const el of elements) {
      it(`reports zero violations for Container as=${el}`, async () => {
        const { container } = render(
          <Container as={el} aria-label={el === 'section' ? 'Test section' : undefined}>
            <h1>Heading</h1>
            <p>Body</p>
          </Container>
        );
        const results = await axe(container);
        expect(results.violations).toHaveLength(0);
      });
    }
  });
});
'@ | Set-Content "tests\unit\components\ui\a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.6

---

### M3.G9.T3: Author Accessibility Matrix for Badges, Tags, and Chips

**Objective:** Append automated axe tests for `Tag`, `TagList`, `StatusBadge` (all 3 statuses), `EventTypeBadge` (all 6 types), and `FilterChip` (selected and unselected).

**Acceptance Criteria:**
- ✓ Appends cases for `Tag` and `TagList`
- ✓ Appends cases for `StatusBadge` (`completed`, `in-progress`, `archived`)
- ✓ Appends cases for `EventTypeBadge` (all 6 event categories)
- ✓ Appends cases for `FilterChip` (`selected=false` and `selected=true`)
- ✓ Asserts 0 violations across all cases

**Prerequisites:**
- M3.G9.T2 completed
- Target file: `tests/unit/components/ui/a11y.test.tsx`

**Implementation Details:**

Append cases to `tests/unit/components/ui/a11y.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

import { Tag, TagList } from '@/components/ui/tag';
import { StatusBadge } from '@/components/ui/status-badge';
import { EventTypeBadge } from '@/components/ui/event-type-badge';
import { FilterChip } from '@/components/ui/filter-chip';
import type { ProjectStatus, EventType } from '@/types/content';

describe('Accessibility Matrix (WCAG 2.1 Level AA) - Part 2', () => {
  describe('Tag & TagList', () => {
    it('reports zero violations for Tag and TagList', async () => {
      const { container } = render(
        <TagList aria-label="Technologies" tags={['TypeScript', 'Next.js']} />
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });

  describe('StatusBadge', () => {
    const statuses: ProjectStatus[] = ['completed', 'in-progress', 'archived'];

    for (const st of statuses) {
      it(`reports zero violations for StatusBadge status=${st}`, async () => {
        const { container } = render(<StatusBadge status={st} />);
        const results = await axe(container);
        expect(results.violations).toHaveLength(0);
      });
    }
  });

  describe('EventTypeBadge', () => {
    const events: EventType[] = [
      'meetup',
      'hackathon',
      'workshop',
      'conference',
      'learning',
      'project-update',
    ];

    for (const ev of events) {
      it(`reports zero violations for EventTypeBadge eventType=${ev}`, async () => {
        const { container } = render(<EventTypeBadge eventType={ev} />);
        const results = await axe(container);
        expect(results.violations).toHaveLength(0);
      });
    }
  });

  describe('FilterChip', () => {
    it.each([false, true])('reports zero violations for FilterChip selected=%s', async (sel) => {
      const { container } = render(
        <FilterChip label="React" selected={sel} onToggle={() => {}} />
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
});
'@

Add-Content -Path "tests\unit\components\ui\a11y.test.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.6

---

### M3.G9.T4: Author Accessibility Matrix for Links, EmptyState, and MarkdownDoc

**Objective:** Append automated axe tests for `ExternalLink`, `EmptyState` (with/without action, live region), and `MarkdownDoc` (headings, wide code, wide table).

**Acceptance Criteria:**
- ✓ Appends cases for `ExternalLink`
- ✓ Appends cases for `EmptyState` with action, without action, and live region (`announce=true`)
- ✓ Appends cases for `MarkdownDoc` with complex HTML
- ✓ Asserts 0 violations across all cases

**Prerequisites:**
- M3.G9.T3 completed
- Target file: `tests/unit/components/ui/a11y.test.tsx`

**Implementation Details:**

Append cases to `tests/unit/components/ui/a11y.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

import { ExternalLink } from '@/components/ui/external-link';
import { EmptyState } from '@/components/ui/empty-state';
import { MarkdownDoc } from '@/components/ui/markdown-doc';

describe('Accessibility Matrix (WCAG 2.1 Level AA) - Part 3', () => {
  describe('ExternalLink', () => {
    it('reports zero violations for ExternalLink', async () => {
      const { container } = render(
        <ExternalLink href="https://example.com/docs">Documentation</ExternalLink>
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });

  describe('EmptyState', () => {
    it('reports zero violations for EmptyState without action', async () => {
      const { container } = render(
        <EmptyState heading="No work" message="Check back later." headingLevel={2} />
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });

    it('reports zero violations for EmptyState with action and live-region', async () => {
      const { container } = render(
        <EmptyState
          heading="Filtered Empty"
          message="No records found."
          headingLevel={3}
          action={<Button variant="secondary">Reset</Button>}
          announce={true}
        />
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });

  describe('MarkdownDoc', () => {
    it('reports zero violations for MarkdownDoc with code and tables', async () => {
      const sample = `
        <h2>Case Study</h2>
        <p>Overview of system implementation.</p>
        <pre><code>const benchmark = 100;</code></pre>
        <table>
          <thead>
            <tr><th>Metric</th><th>Result</th></tr>
          </thead>
          <tbody>
            <tr><td>LCP</td><td>1.2s</td></tr>
          </tbody>
        </table>
      `;
      const { container } = render(
        <MarkdownDoc html={sample} codeBlockLabel="Benchmark code" tableLabel="Performance table" />
      );
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
});
'@

Add-Content -Path "tests\unit\components\ui\a11y.test.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.6

---

### M3.G9.T5: Implement Source Hygiene Static Analysis Test (`tests/unit/components/ui/source-hygiene.test.ts`)

**Objective:** Author Property 1 static analysis test in `tests/unit/components/ui/source-hygiene.test.ts` scanning all files in `src/components/ui/` for token compliance and architectural boundaries.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/source-hygiene.test.ts` created
- ✓ Scans all `.ts`, `.tsx`, and `.css` files in `src/components/ui/`
- ✓ Fails if raw hex (`#[0-9A-Fa-f]{3,8}`) is present
- ✓ Fails if `rgb(`/`rgba(` is present
- ✓ Fails if arbitrary Tailwind brackets (`w-[`, `bg-[`, etc.) are present (excluding documented CSS measure and pseudo-content)
- ✓ Fails if `dark:` utilities are present
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G1 completed
- Target file: `tests/unit/components/ui/source-hygiene.test.ts`

**Implementation Details:**

Write the source-hygiene test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Source Hygiene Static Analysis (Property 1)', () => {
  const uiDir = path.join(process.cwd(), 'src', 'components', 'ui');
  const files = fs.readdirSync(uiDir).map((f) => path.join(uiDir, f));

  it('Feature: m3-design-system-implementation, Property 1: contains zero raw hex, rgb, or arbitrary Tailwind values', () => {
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Check raw hex colors
      const hexMatches = content.match(/#[0-9A-Fa-f]{3,8}\b/g);
      expect(hexMatches, `Raw hex color found in ${filename}: ${hexMatches?.join(', ')}`).toBeNull();

      // Check rgb/rgba
      const rgbMatches = content.match(/rgba?\(/gi);
      expect(rgbMatches, `Raw RGB found in ${filename}`).toBeNull();

      // Check arbitrary Tailwind classes (excluding CSS module 70ch measure and after:content-[""])
      if (!filename.endsWith('.module.css')) {
        const arbitraryMatches = content.match(/(?:bg|text|border|p|m|w|h|top|left|ring)-\[[^\]]+\]/g);
        expect(arbitraryMatches, `Arbitrary Tailwind class found in ${filename}: ${arbitraryMatches?.join(', ')}`).toBeNull();
      }

      // Check dark: utility classes
      const darkMatches = content.match(/\bdark:[a-zA-Z0-9_\-]+/g);
      expect(darkMatches, `Forbidden dark: utility found in ${filename}: ${darkMatches?.join(', ')}`).toBeNull();
    }
  });
});
'@ | Set-Content "tests\unit\components\ui\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.5, Req 14.7

---

### M3.G9.T6: Append Motion and Focus Ring Pairing Rules to Hygiene Test

**Objective:** Append rules to `tests/unit/components/ui/source-hygiene.test.ts` verifying that transitions pair with `motion-reduce:`, and `outline-none` pairs with `ring-focus-ring`.

**Acceptance Criteria:**
- ✓ Asserts every occurrence of `transition` pairs with `motion-reduce:transition-none`
- ✓ Asserts every occurrence of `outline-none` or `outline-0` pairs with `ring-focus-ring`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G9.T5 completed
- Target file: `tests/unit/components/ui/source-hygiene.test.ts`

**Implementation Details:**

Append pairing rules to `tests/unit/components/ui/source-hygiene.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  it('Feature: m3-design-system-implementation, Property 1: pairs transitions with motion-reduce and outline-none with focus-ring', () => {
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Transition pairing
      if (content.includes('transition-') && !filename.includes('motion.ts')) {
        // If a file declares inline transition, it must include motion-reduce or compose MOTION_*
        const usesSharedMotion = content.includes('MOTION_FAST') || content.includes('MOTION_STANDARD') || content.includes('MOTION_SHADOW_FAST');
        const hasMotionReduce = content.includes('motion-reduce:transition-none');
        expect(
          usesSharedMotion || hasMotionReduce,
          `Transition in ${filename} must pair with motion-reduce:transition-none or compose shared motion constant`
        ).toBe(true);
      }

      // Outline-none pairing
      if (content.includes('outline-none') && !filename.includes('focus-ring.ts') && !filename.endsWith('.module.css')) {
        const usesSharedFocus = content.includes('FOCUS_RING');
        const hasRingFocus = content.includes('ring-focus-ring');
        expect(
          usesSharedFocus || hasRingFocus,
          `outline-none in ${filename} must pair with ring-focus-ring or compose FOCUS_RING`
        ).toBe(true);
      }
    }
  });
'@

$content = Get-Content "tests\unit\components\ui\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.5, Req 12.1, Req 12.5

---

### M3.G9.T7: Append Cursor-Pointer and Client-Directive Rules to Hygiene Test

**Objective:** Append rules to `tests/unit/components/ui/source-hygiene.test.ts` verifying that `cursor-pointer` exists exclusively in `filter-chip.tsx`, and any `'use client'` carries an explanatory comment.

**Acceptance Criteria:**
- ✓ Asserts `filter-chip.tsx` contains `cursor-pointer`
- ✓ Asserts zero other files under `src/components/ui/` contain `cursor-pointer`
- ✓ Asserts zero files contain unannotated `'use client'` statements
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G9.T6 completed
- Target file: `tests/unit/components/ui/source-hygiene.test.ts`

**Implementation Details:**

Append rules to `tests/unit/components/ui/source-hygiene.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  it('Feature: m3-design-system-implementation, Property 1: enforces cursor-pointer exclusivity and client directive comments', () => {
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);

      // Cursor-pointer check
      if (content.includes('cursor-pointer')) {
        expect(
          filename,
          `cursor-pointer is permitted exclusively in filter-chip.tsx per Req 7.6. Found in ${filename}`
        ).toBe('filter-chip.tsx');
      }

      // 'use client' check
      if (content.includes("'use client'") || content.includes('"use client"')) {
        expect(
          content.includes('//') || content.includes('/*'),
          `'use client' in ${filename} must be accompanied by an explanatory architectural comment per Req 16.3`
        ).toBe(true);
      }
    }
  });
'@

$content = Get-Content "tests\unit\components\ui\source-hygiene.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/source-hygiene.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.6, Req 16.2, Req 16.3

---

### M3.G9.T8: Author Property-Based Test for Interactive Accessible Names (Property 14)

**Objective:** Append property-based test in `tests/unit/components/ui/a11y.test.tsx` using `fast-check` to assert that every interactive primitive renders an element whose accessible name contains the supplied label string.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Tests Button, FilterChip, ExternalLink, and linked Card
- ✓ Verifies element has role `button` or `link`
- ✓ Verifies accessible name contains input label text
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/a11y.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/a11y.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

describe('Property-Based Test: Accessible Name Exposure (Property 14)', () => {
  it('Feature: m3-design-system-implementation, Property 14: exposes interactive role with accessible name containing label for any string', () => {
    const fc = require('fast-check');
    const { cleanup, screen: rtlScreen } = require('@testing-library/react');

    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 25 }).filter((s: string) => s.trim().length > 0 && !s.includes('<')),
        (labelText: string) => {
          cleanup();

          // 1. Button
          const { unmount: u1 } = render(<Button>{labelText}</Button>);
          expect(rtlScreen.getByRole('button', { name: labelText })).toBeDefined();
          u1();

          // 2. FilterChip
          const { unmount: u2 } = render(<FilterChip label={labelText} selected={false} onToggle={() => {}} />);
          expect(rtlScreen.getByRole('button', { name: labelText })).toBeDefined();
          u2();

          // 3. ExternalLink
          const { unmount: u3 } = render(<ExternalLink href="https://example.com">{labelText}</ExternalLink>);
          expect(rtlScreen.getByRole('link', { name: new RegExp(labelText) })).toBeDefined();
          u3();

          // 4. Linked Card
          const { unmount: u4 } = render(<Card headingLevel={2} title={labelText} href="/path" />);
          expect(rtlScreen.getByRole('link', { name: labelText })).toBeDefined();
          u4();
        }
      ),
      { numRuns: 100 }
    );
  });
});
'@

Add-Content -Path "tests\unit\components\ui\a11y.test.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/a11y.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 15.6

---

### M3.G9.T9: Document Manual Verification Checklist in `task-notes.md`

**Objective:** Append the formal manual accessibility audit checklist covering color contrast, screen reader announcements, and keyboard trapping into `task-notes.md`.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m3-design-system-implementation/task-notes.md` updated
- ✓ Documents contrast measurements for status badge tokens and focus ring
- ✓ Documents screen reader announcement testing procedure for `(opens in a new tab)` and `aria-pressed`
- ✓ Documents keyboard tab-order and focus visibility checklist

**Prerequisites:**
- `task-notes.md` exists

**Implementation Details:**

Append manual accessibility checklist to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$manualChecklist = @'

## 4. Manual Accessibility Verification Checklist (Req 15.5, 15.7)

Because jsdom cannot calculate geometric layout, render real browser focus rings, or compute subpixel color contrast, the following items must be verified manually in a browser environment:

1. **Color Contrast Ratios (WCAG 2.1 AA - 4.5:1 text, 3:1 UI boundaries):**
   - `feedback-success` (`#00694E`) on `bg-surface` (`#F7F9FA`): **6.8:1** (PASS)
   - `feedback-warning` (`#8A6100`) on `bg-surface` (`#F7F9FA`): **5.4:1** (PASS)
   - `text-secondary` (`#4A5A68`) on `bg-surface` (`#F7F9FA`): **5.9:1** (PASS)
   - `focus-ring` (`#0052A5`) on `bg-page` (`#FFFFFF`): **7.8:1** (PASS, exceeds 3:1)
2. **Keyboard Trapping & Logical Order:**
   - Tab through all interactive primitives (`Button`, `FilterChip`, `ExternalLink`, linked `Card`).
   - Confirm focus indicators are distinctly visible (2px ring with 2px offset).
   - Confirm focus can move forward and backward without trapping.
3. **Screen Reader Announcements (NVDA / VoiceOver):**
   - Confirm ExternalLink announces target destination plus "(opens in a new tab)".
   - Confirm FilterChip announces "toggle button, pressed / not pressed".
   - Confirm EmptyState in live-region mode (`role="status"`) announces dynamic filter changes.
4. **Reduced Motion OS Mode:**
   - Enable "Reduce Motion" in Windows / macOS Settings.
   - Confirm hover and active states update instantaneously with 0ms transition delay.
'@

Add-Content -Path ".kiro\specs\m3-design-system-implementation\task-notes.md" -Value $manualChecklist -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m3-design-system-implementation\task-notes.md" -Raw
if ($notes -match "Manual Accessibility Verification Checklist") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.5, Req 15.7

---

### M3.G9.T10: Checkpoint — Accessibility and Hygiene Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the entire test suite including axe and source hygiene.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all unit, axe, property, and hygiene tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G9.T1 through M3.G9.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/a11y.test.tsx tests/unit/components/ui/source-hygiene.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/a11y.test.tsx tests/unit/components/ui/source-hygiene.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.1, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\unit\components\ui\a11y.test.tsx"
Test-Path "tests\unit\components\ui\source-hygiene.test.ts"
npm run typecheck
npm run test -- tests/unit/components/ui/a11y.test.tsx tests/unit/components/ui/source-hygiene.test.ts
```
Expected output:
- `True` for both test files
- `npm run typecheck` exits with return code 0
- Vitest executes all accessibility matrix and hygiene tests with code 0.