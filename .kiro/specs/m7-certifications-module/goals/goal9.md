# M7.G9: Responsive, Token, and Scope Compliance; Accessibility and Keyboard Matrix; Source Hygiene

> **Milestone:** M7 — Certifications Module  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks (M7.G9.T1 – M7.G9.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 11.5, 11.7, 13.2–13.3, 13.6, 14.1–14.6, 15.5–15.6), `design.md` (Tokens, Breakpoints, WCAG 2.1 AA, Hygiene), `tasks.md` (M7.G9)

---

## Goal Objective

Execute an exhaustive compliance, accessibility, and hygiene sweep across the entire M7 module:
1. Design Token & Responsive Audit: Scan all M7 TSX files to guarantee zero hardcoded hex/RGB colors, arbitrary utility brackets (`w-[`, `p-[`, `bg-[#]`), or transition/animation classes, and verify breakpoint styling (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`).
2. Accessibility & Keyboard Navigation Matrix: Implement `tests/certifications/a11y.test.tsx` running automated `axe-core` checks across all core component fixtures (populated, expired, minimal, empty) with zero violations. Implement `tests/certifications/keyboard.test.tsx` verifying sequential `Tab` key traversal across verification links, active `FOCUS_RING` classes on `:focus-visible`, and absolute uniqueness of all link accessible names (`Verify {title} credential`).
3. Source Hygiene & Scope Boundary Guard: Implement `tests/certifications/source-hygiene.test.ts` to statically scan M7 files, failing on any usage of `any`, `!.` (non-null assertions), unjustified `as`, redeclared content types, barrel files (`index.ts`), `dangerouslySetInnerHTML`, cookies, tracking scripts, or files exceeding 300 lines.
4. Fixture Title Uniqueness & Manual Check Checklist: Confirm fixture titles are distinct to prevent screen-reader link name collision, verify git diff is confined strictly to allowed directories, and log the manual verification procedure in `task-notes.md`.

---

## Goal Success Criteria

- ✓ Zero hex values (`#`), `rgb(`, `rgba(`, arbitrary values (`[#...]`, `px-[`, `duration-[`), or transition/animation utilities in M7 source code.
- ✓ All interactive controls feature visible focus indicators via M3's `FOCUS_RING`.
- ✓ `tests/certifications/a11y.test.tsx` passes `axe-core` with zero violations across populated, expired, minimal, and empty fixtures.
- ✓ `tests/certifications/keyboard.test.tsx` passes with verified DOM Tab order and confirms every rendered verification link on the page has a unique accessible name.
- ✓ `tests/certifications/source-hygiene.test.ts` passes with zero violations: no `any`, no `!.`, no unjustified `as`, no barrel `index.ts` files, all files under 300 lines.
- ✓ `git diff --stat` confirms zero modified files outside `src/app/certifications/`, `src/components/certifications/`, `src/lib/certifications/`, `tests/certifications/`, `tests/fixtures/`, and `.kiro/specs/m7-certifications-module/`.
- ✓ Manual responsive, touch-target, 200% zoom, and high-contrast verification steps documented in `task-notes.md`.

---

## Prerequisites

- Goals 1 through 8 completed.
- `@testing-library/user-event` installed and configured.
- `vitest-axe` configured.

---

## Tasks

### M7.G9.T1: Audit Design Tokens and Eliminate Arbitrary Values

**Objective:** Audit all M7 source files in `src/app/certifications/`, `src/components/certifications/`, and `src/lib/certifications/` to ensure 100% adherence to semantic design tokens without raw hex, rgb, or arbitrary Tailwind values.

**Acceptance Criteria:**
- ✓ Scans all `.ts` and `.tsx` files in M7 directories.
- ✓ Zero matches for regex `#[0-9a-fA-F]{3,8}` (hex colors).
- ✓ Zero matches for `rgb(` or `rgba(`.
- ✓ Zero matches for arbitrary Tailwind brackets (e.g. `-[`, `bg-[`, `text-[`, `w-[`, `p-[`).
- ✓ Zero matches for raw timing or durations (e.g. `duration-`, `transition-`, `animate-`).

**Prerequisites:**
- M7 component source files exist.

**Implementation Details:**
Run PowerShell script to audit token usage:

```powershell
$files = Get-ChildItem -Path src\app\certifications, src\components\certifications -Recurse -Filter *.tsx
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match "#[0-9a-fA-F]{3,8}|rgba?\(|\[#|transition|animate") {
        Write-Error "Token violation in $($f.FullName)"
    }
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\components\certifications\*.tsx, src\app\certifications\*.tsx -Pattern "#[0-9a-fA-F]{3,6}|rgba?\(|\[#|transition|animate"
```
Expected output: No matches found.

**Satisfies Requirements:** Req 11.7, 14.2, 14.6

---

### M7.G9.T2: Audit Responsive Layout Grid Classes and Text Wrapping

**Objective:** Verify that `CertificationCategorySection` and `CertificationCard` adhere to responsive breakpoint standards and word-wrapping requirements.

**Acceptance Criteria:**
- ✓ `CertificationCategorySection` grid has classes `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch`.
- ✓ `CertificationCard` title and issuer headings have `break-words`.
- ✓ `BadgeImage` has `max-w-full object-contain` preventing overflow at 375px.
- ✓ Verified that card container applies `h-full flex flex-col justify-between`.

**Prerequisites:**
- `certification-category-section.tsx` and `certification-card.tsx` implemented.

**Implementation Details:**
Inspect class names in component files and log confirmation in `task-notes.md`.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\components\certifications\certification-category-section.tsx -Pattern "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
Select-String -Path src\components\certifications\certification-card.tsx -Pattern "break-words"
```
Expected output: Matches found in both files confirming classes are present.

**Satisfies Requirements:** Req 11.1, 11.2, 11.3, 11.4, 11.5, 11.6

---

### M7.G9.T3: Audit Focus Ring and Keyboard Indicators

**Objective:** Verify that every interactive element in M7 (specifically `VerificationLink`) applies `FOCUS_RING` styling from M3.

**Acceptance Criteria:**
- ✓ `VerificationLink` includes `${FOCUS_RING}` in its class list.
- ✓ Focus indicator is visually distinct and not suppressed with `outline-none` without replacement.

**Prerequisites:**
- `verification-link.tsx` implemented.

**Implementation Details:**
Inspect `src/components/certifications/verification-link.tsx` for `FOCUS_RING` usage.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\components\certifications\verification-link.tsx -Pattern "FOCUS_RING"
```
Expected output: Match confirmed.

**Satisfies Requirements:** Req 8.7, 14.3

---

### M7.G9.T4: Implement Comprehensive Axe Accessibility Test Matrix

**Objective:** Create `tests/certifications/a11y.test.tsx` running `axe-core` across the full spectrum of certification component fixtures.

**Acceptance Criteria:**
- ✓ Tests populated list fixture with zero axe violations.
- ✓ Tests expired credential fixture with zero axe violations.
- ✓ Tests minimal credential fixture with zero axe violations.
- ✓ Tests empty state fixture with zero axe violations.
- ✓ Runs against WCAG 2.1 AA ruleset.

**Prerequisites:**
- `vitest-axe` configured.
- Fixtures available in `tests/fixtures/certifications-data.ts`.

**Implementation Details:**
Create `tests/certifications/a11y.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { CertificationsIndex } from '@/components/certifications/certifications-index';
import {
  fixtureCertificationsList,
  fixtureEmptyCertificationsList,
  fixtureExpiredCertification,
  fixtureMinimalCertification,
} from '../fixtures/certifications-data';

describe('Certifications Module - Full Accessibility Matrix', () => {
  const buildDate = '2026-04-15';

  it('passes axe with zero violations for full populated index', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe with zero violations for single expired certification', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={[fixtureExpiredCertification]}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe with zero violations for single minimal certification', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={[fixtureMinimalCertification]}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe with zero violations for empty state index', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureEmptyCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/a11y.test.tsx
```
Expected output: All 4 axe accessibility tests pass with zero violations.

**Satisfies Requirements:** Req 14.1, 14.2, 15.1

---

### M7.G9.T5: Implement Keyboard Navigation and Unique Link Names Test

**Objective:** Create `tests/certifications/keyboard.test.tsx` verifying tab navigation sequence, focus indicator application, and uniqueness of all link accessible names on the page.

**Acceptance Criteria:**
- ✓ Uses `@testing-library/user-event` to simulate `Tab` key navigation through verification links.
- ✓ Verifies links receive focus in exact DOM document order.
- ✓ Collects all link accessible names on the page and asserts `uniqueNames.size === totalLinks.length`.
- ✓ Asserts every link has accessible name starting with `"Verify "` and ending with `" credential"`.

**Prerequisites:**
- `@testing-library/user-event` available.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/keyboard.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CertificationsIndex } from '@/components/certifications/certifications-index';
import { fixtureCertificationsList } from '../fixtures/certifications-data';

describe('Certifications Module - Keyboard Navigation & Unique Accessible Names', () => {
  const buildDate = '2026-04-15';

  it('tabs sequentially through verification links in DOM order', async () => {
    const user = userEvent.setup();
    render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    const links = screen.getAllByRole('link');
    expect(links.length).toBeGreaterThan(1);

    // Focus initial body then tab into first link
    for (const link of links) {
      await user.tab();
      expect(link).toHaveFocus();
    }
  });

  it('ensures all verification link accessible names on the page are unique', () => {
    render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    const links = screen.getAllByRole('link');
    const names = links.map((link) => link.getAttribute('aria-label') || link.textContent || '');

    const uniqueNames = new Set(names);
    expect(uniqueNames.size).toBe(links.length);

    for (const name of names) {
      expect(name).toMatch(/^Verify .+ credential$/);
    }
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/keyboard.test.tsx
```
Expected output: Both keyboard and link uniqueness tests pass.

**Satisfies Requirements:** Req 8.2, 14.3, 14.4, 15.1

---

### M7.G9.T6: Implement Source Hygiene and Type Safety Linter Test

**Objective:** Create `tests/certifications/source-hygiene.test.ts` to statically inspect M7 source code for type safety, file length, and prohibited syntax.

**Acceptance Criteria:**
- ✓ Scans all files in `src/app/certifications/`, `src/components/certifications/`, and `src/lib/certifications/`.
- ✓ Asserts zero instances of `any` (or `as any` outside tests).
- ✓ Asserts zero non-null assertions (`!.`).
- ✓ Asserts zero redeclarations of `interface Certification` or `type CertificationCategory`.
- ✓ Asserts all files have fewer than 300 lines of code.

**Prerequisites:**
- Node `fs` and `path` available.

**Implementation Details:**
Create `tests/certifications/source-hygiene.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Certifications Module - Source Hygiene Audit', () => {
  const projectRoot = process.cwd();
  const targetDirs = [
    path.join(projectRoot, 'src', 'app', 'certifications'),
    path.join(projectRoot, 'src', 'components', 'certifications'),
    path.join(projectRoot, 'src', 'lib', 'certifications'),
  ];

  const sourceFiles = targetDirs.flatMap((dir) =>
    fs.existsSync(dir)
      ? fs
          .readdirSync(dir)
          .filter((f) => f.endsWith('.ts') || f.endsWith('.tsx'))
          .map((f) => path.join(dir, f))
      : [],
  );

  it('keeps all source files below 300 lines of code', () => {
    for (const file of sourceFiles) {
      const lineCount = fs.readFileSync(file, 'utf-8').split('\n').length;
      expect(
        lineCount,
        `File ${path.basename(file)} has ${lineCount} lines, exceeding 300 limit`,
      ).toBeLessThan(300);
    }
  });

  it('prohibits any and non-null assertions (!.) in source files', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toMatch(/:\s*any\b/);
      expect(content).not.toMatch(/\w+!\./);
    }
  });

  it('prohibits redeclaration of canonical content contracts', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toMatch(/interface\s+Certification\s*\{/);
      expect(content).not.toMatch(/type\s+CertificationCategory\s*=/);
    }
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/source-hygiene.test.ts
```
Expected output: All 3 hygiene tests pass.

**Satisfies Requirements:** Req 1.5, 15.5, 15.6

---

### M7.G9.T7: Audit Architectural Boundaries and Out-of-Scope Patterns

**Objective:** Append scope boundary checks to `tests/certifications/source-hygiene.test.ts` to ensure no barrel files, cookies, analytics, forms, server actions, or tracking scripts were added.

**Acceptance Criteria:**
- ✓ Asserts no `index.ts` or `index.tsx` barrel files exist in `src/components/certifications/` or `src/lib/certifications/`.
- ✓ Asserts zero instances of `'use server'`, `<form`, `document.cookie`, `localStorage`, or third-party script tags in M7 sources.

**Prerequisites:**
- `tests/certifications/source-hygiene.test.ts` available.

**Implementation Details:**
Append to `tests/certifications/source-hygiene.test.ts`:

```typescript
  it('prohibits barrel files (index.ts / index.tsx)', () => {
    for (const file of sourceFiles) {
      const baseName = path.basename(file);
      expect(baseName).not.toBe('index.ts');
      // page.tsx and certifications-index.tsx are permitted, but no pure barrel index.tsx
      if (baseName === 'index.tsx') {
        const content = fs.readFileSync(file, 'utf-8');
        expect(content).not.toMatch(/^export\s+\*\s+from/);
      }
    }
  });

  it('prohibits out-of-scope runtime constructs (cookies, forms, server actions)', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toContain("'use server'");
      expect(content).not.toContain('"use server"');
      expect(content).not.toContain('<form');
      expect(content).not.toContain('document.cookie');
      expect(content).not.toContain('localStorage');
    }
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/source-hygiene.test.ts
```
Expected output: Tests pass.

**Satisfies Requirements:** Req 13.5, 13.6

---

### M7.G9.T8: Fixture and Real Content Title Uniqueness Test

**Objective:** Add a test verifying that all titles in `tests/fixtures/certifications-data.ts` and in real markdown files in `content/certifications/` are unique to prevent accessible link collision.

**Acceptance Criteria:**
- ✓ Asserts all fixture certifications have unique titles.
- ✓ If `content/certifications/` exists with MDX files, parses frontmatter and asserts all real titles are unique.

**Prerequisites:**
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/title-uniqueness.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fixtureCertificationsList } from '../fixtures/certifications-data';

describe('Certifications Title Uniqueness Audit', () => {
  it('verifies all test fixture certification titles are unique', () => {
    const titles = fixtureCertificationsList.map((c) => c.title);
    const unique = new Set(titles);
    expect(unique.size).toBe(titles.length);
  });

  it('verifies content/certifications markdown files have unique titles if present', () => {
    const contentDir = path.join(process.cwd(), 'content', 'certifications');
    if (fs.existsSync(contentDir)) {
      const files = fs.readdirSync(contentDir).filter((f) => f.endsWith('.mdx') || f.endsWith('.md'));
      const titles: string[] = [];

      for (const file of files) {
        const raw = fs.readFileSync(path.join(contentDir, file), 'utf-8');
        const match = raw.match(/title:\s*["']?([^"'\n\r]+)["']?/);
        if (match) {
          titles.push(match[1].trim());
        }
      }

      const unique = new Set(titles);
      expect(unique.size).toBe(titles.length);
    }
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/title-uniqueness.test.ts
```
Expected output: Test passes with zero duplicate titles.

**Satisfies Requirements:** Req 8.2, 14.4

---

### M7.G9.T9: Confine Git Diff and Document Manual Verification Procedure

**Objective:** Verify that `git status` / `git diff` touches only M7-approved paths, and document the manual physical device and assistive technology verification protocol in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Validates git diff against baseline to confirm only permitted M7 paths are modified.
- ✓ Documents manual checklist for:
  - 375px, 768px, 1024px, 1440px viewport tests (no horizontal scroll).
  - High-contrast mode / non-color expired indicator visibility.
  - 200% zoom layout integrity.
  - Touch target sizes ($\ge 44 \times 44\text{px}$ or inline link exemption).

**Prerequisites:**
- `.kiro/specs/m7-certifications-module/task-notes.md` exists.

**Implementation Details:**
Append the manual QA matrix to `.kiro/specs/m7-certifications-module/task-notes.md`:

```markdown
### 6. Manual Verification Procedure (Browser & Device Testing)

The following checks must be confirmed manually in a real browser engine:
1. **Viewport Overflow (375px - 1440px):**
   - Open `/certifications` at 375px viewport (mobile). Verify cards stack in 1 column; no horizontal scrollbar occurs.
   - Expand to 768px (tablet). Verify grid switches to 2 columns.
   - Expand to 1024px+ (desktop). Verify grid switches to 3 columns.
2. **Touch Targets & Focus:**
   - Tap verification links on mobile view; verify target responds cleanly.
   - Press Tab repeatedly; verify blue focus ring matches `FOCUS_RING` token.
3. **Non-Color Expiry Verification:**
   - Simulate greyscale mode (CSS filter: grayscale(100%)). Verify expired credentials remain immediately recognizable via the warning icon, visible "Expired" text, and card border cue.
4. **200% Zoom:**
   - Zoom page to 200%. Verify text wraps cleanly without truncation or layout clipping.
```

**Validation:**
Execute in Windows PowerShell:
```powershell
git status --porcelain
```
Expected output: Only files under `src/app/certifications/`, `src/components/certifications/`, `src/lib/certifications/`, `tests/certifications/`, `tests/fixtures/`, and `.kiro/specs/m7-certifications-module/` appear as modified or untracked.

**Satisfies Requirements:** Req 11.5, 14.2, 14.3, 14.6, 15.7

---

### M7.G9.T10: Goal 9 Checkpoint and Pipeline Verification

**Objective:** Run the full test suite, linter, and typechecker across all Goal 9 test suites.

**Acceptance Criteria:**
- ✓ `tests/certifications/a11y.test.tsx` passes.
- ✓ `tests/certifications/keyboard.test.tsx` passes.
- ✓ `tests/certifications/source-hygiene.test.ts` passes.
- ✓ `tests/certifications/title-uniqueness.test.ts` passes.
- ✓ `npx tsc --noEmit` exits with 0.

**Prerequisites:**
- Tasks M7.G9.T1 through M7.G9.T9 completed.

**Implementation Details:**
Execute test suite and typechecking commands in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/a11y.test.tsx tests/certifications/keyboard.test.tsx tests/certifications/source-hygiene.test.ts tests/certifications/title-uniqueness.test.ts
npx tsc --noEmit
```
Expected output: All 4 test files pass completely; TypeScript compiles with zero errors.

**Satisfies Requirements:** Req 11.5, 11.7, 13.2–13.3, 13.6, 14.1–14.6, 15.5–15.6, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 9 are complete:
```powershell
npx vitest run tests/certifications/a11y.test.tsx tests/certifications/keyboard.test.tsx tests/certifications/source-hygiene.test.ts tests/certifications/title-uniqueness.test.ts
npx tsc --noEmit
```
Expected output: All accessibility, keyboard, source hygiene, and title uniqueness tests pass; zero TypeScript errors.