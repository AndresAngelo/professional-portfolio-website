# M7.G4: Heading Shift and Supporting-Content Loader

> **Milestone:** M7 — Certifications Module  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks (M7.G4.T1 – M7.G4.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 5.6, 10.1–10.3, 10.5, 15.2), `design.md` (Properties 12, 13 loader half), `tasks.md` (M7.G4)

---

## Goal Objective

Implement two key modules in `src/lib/certifications/`:
1. `shift-headings.ts`: a pure string utility that parses rendered HTML heading tags (`<h[1-6]...>` and `</h[1-6]>`), computes the minimum heading level present, and shifts all headings so that the highest level is at least `h4` (capped at `h6`). This preserves relative heading structure while maintaining an unbroken, accessible document outline (`h1` page $\rightarrow$ `h2` category section $\rightarrow$ `h3` card title $\rightarrow$ `h4+` card content) without importing utilities from other milestone directories.
2. `load-supporting-content.ts`: an asynchronous loader that iterates over certifications, filters out empty or whitespace-only markdown bodies, calls M2's `renderMarkdown`, shifts headings using `shiftHeadings`, returns a dictionary `Readonly<Record<string, string>>` keyed by slug, and catches rendering errors to rethrow a descriptive error containing the certification slug and original cause.

Verify both modules through comprehensive unit tests and fast-check property tests (Property 12 and Property 13 loader half).

---

## Goal Success Criteria

- ✓ `src/lib/certifications/shift-headings.ts` exports pure function `shiftHeadings(html: string, minLevel = 4): string`.
- ✓ `shiftHeadings` preserves all HTML attributes, tag content, and casing; leaves heading-free HTML unchanged; shifts headings by `delta = max(0, minLevel - minLevel_found)`; caps shifted headings at 6; and keeps opening/closing tags paired.
- ✓ `src/lib/certifications/load-supporting-content.ts` exports `loadSupportingContent(certifications: readonly Certification[]): Promise<Readonly<Record<string, string>>>`.
- ✓ Certifications with empty or whitespace-only `content` are omitted from the returned record.
- ✓ Non-empty bodies are rendered with `renderMarkdown`, shifted with `shiftHeadings`, and stored under `slug`.
- ✓ When `renderMarkdown` fails, `loadSupportingContent` throws an error matching `Failed to render certification content: <slug>` with `{ cause }`.
- ✓ Zero cross-module imports from `src/lib/projects/` or `src/components/projects/`.
- ✓ Property 12 passes with >= 100 runs in `tests/certifications/shift-headings.test.ts`.
- ✓ Property 13 (loader half) passes with >= 100 runs in `tests/certifications/load-supporting-content.test.ts`.

---

## Prerequisites

- Goal 1 completed: `@/types/content` available, test fixtures and arbitraries available in `tests/fixtures/`.
- M2 `renderMarkdown` available at `@/content/markdown/renderer` (or equivalent verified M2 path).
- No new dependencies added to `package.json`.

---

## Tasks

### M7.G4.T1: Implement Pure shiftHeadings Utility

**Objective:** Create `src/lib/certifications/shift-headings.ts` to shift HTML heading tags to a minimum depth of `h4` while capping at `h6`.

**Acceptance Criteria:**
- ✓ Exports pure function `shiftHeadings(html: string, minLevel = 4): string`.
- ✓ If `html` contains no `<h[1-6]` tags, returns the input string unmodified.
- ✓ Finds the lowest heading level number $N$ present in the string (e.g., if `<h1>` is present, $N=1$; if only `<h2>` and `<h3>` are present, $N=2$).
- ✓ Computes `delta = Math.max(0, minLevel - N)`.
- ✓ If `delta === 0`, returns `html` unmodified.
- ✓ Replaces opening `<h([1-6])(?=[\s>])` with `<h${Math.min(6, level + delta)}` preserving attributes.
- ✓ Replaces closing `</h([1-6])>` with `</h${Math.min(6, level + delta)}>`.
- ✓ Self-contained regex logic with zero cross-milestone imports from `projects`.

**Prerequisites:**
- Directory `src/lib/certifications/` exists.

**Implementation Details:**
Create `src/lib/certifications/shift-headings.ts`:

```typescript
/**
 * Shifts HTML heading tags so that the smallest heading level is at least minLevel (default 4).
 * Ensures card content headings do not break the h1 -> h2 -> h3 hierarchy.
 */
export function shiftHeadings(html: string, minLevel = 4): string {
  if (!html || typeof html !== 'string') {
    return '';
  }

  // Regex to match any heading level opening or closing tag
  const headingLevelRegex = /<\/?h([1-6])(?=[\s>])/gi;
  let match: RegExpExecArray | null;
  let minFound = 7;

  while ((match = headingLevelRegex.exec(html)) !== null) {
    const level = parseInt(match[1], 10);
    if (level < minFound) {
      minFound = level;
    }
  }

  // No headings found or already deeper than or equal to minLevel
  if (minFound > 6 || minFound >= minLevel) {
    return html;
  }

  const delta = Math.max(0, minLevel - minFound);
  if (delta === 0) {
    return html;
  }

  // Replace opening tags: <h1 ...> -> <h4 ...>
  let shifted = html.replace(/<h([1-6])([\s>])/gi, (_, levelStr, suffix) => {
    const currentLevel = parseInt(levelStr, 10);
    const newLevel = Math.min(6, currentLevel + delta);
    return `<h${newLevel}${suffix}`;
  });

  // Replace closing tags: </h1> -> </h4>
  shifted = shifted.replace(/<\/h([1-6])>/gi, (_, levelStr) => {
    const currentLevel = parseInt(levelStr, 10);
    const newLevel = Math.min(6, currentLevel + delta);
    return `</h${newLevel}>`;
  });

  return shifted;
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero errors in `src/lib/certifications/shift-headings.ts`.

**Satisfies Requirements:** Req 5.6, 10.3

---

### M7.G4.T2: Unit Tests for shiftHeadings

**Objective:** Create `tests/certifications/shift-headings.test.ts` covering concrete cases for `shiftHeadings`.

**Acceptance Criteria:**
- ✓ Test: returns empty string for empty input.
- ✓ Test: returns HTML without headings unchanged (e.g. `<p>Hello</p>`).
- ✓ Test: shifts `<h1>Title</h1>` to `<h4>Title</h4>`.
- ✓ Test: shifts `<h2>` and `<h3>` to `<h4>` and `<h5>`.
- ✓ Test: caps deeply shifted headings at `<h6>` (e.g. `<h5>` with `delta = 3` becomes `<h6>`).
- ✓ Test: preserves heading attributes (e.g. `<h2 id="summary" class="bold">`).
- ✓ Test: already deep headings (e.g. `<h4 id="deep">`) remain unchanged when `minLevel = 4`.

**Prerequisites:**
- `src/lib/certifications/shift-headings.ts` implemented.

**Implementation Details:**
Create `tests/certifications/shift-headings.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { shiftHeadings } from '@/lib/certifications/shift-headings';

describe('shiftHeadings - Unit Tests', () => {
  it('returns empty string for empty or null input', () => {
    expect(shiftHeadings('')).toBe('');
  });

  it('leaves heading-free content unchanged', () => {
    const input = '<p>Demonstrated architecture competency across AWS infrastructure.</p>';
    expect(shiftHeadings(input)).toBe(input);
  });

  it('shifts h1 tags to h4 when minLevel is 4', () => {
    const input = '<h1>Main Topic</h1><p>Body</p>';
    const expected = '<h4>Main Topic</h4><p>Body</p>';
    expect(shiftHeadings(input, 4)).toBe(expected);
  });

  it('shifts multiple heading levels preserving relative difference', () => {
    const input = '<h2>Section</h2><h3>Subsection</h3>';
    const expected = '<h4>Section</h4><h5>Subsection</h5>';
    expect(shiftHeadings(input, 4)).toBe(expected);
  });

  it('caps heading levels at h6', () => {
    const input = '<h2>Section</h2><h5>Deep Subsection</h5>';
    // minFound is 2, delta is 2 (minLevel 4 - 2). h2 -> h4, h5 + 2 -> capped at h6
    const expected = '<h4>Section</h4><h6>Deep Subsection</h6>';
    expect(shiftHeadings(input, 4)).toBe(expected);
  });

  it('preserves HTML attributes on heading tags', () => {
    const input = '<h2 id="arch-overview" class="font-bold text-lg">Architecture</h2>';
    const expected = '<h4 id="arch-overview" class="font-bold text-lg">Architecture</h4>';
    expect(shiftHeadings(input, 4)).toBe(expected);
  });

  it('leaves headings at or below minLevel unchanged', () => {
    const input = '<h4>Subtopic</h4><h5>Detail</h5>';
    expect(shiftHeadings(input, 4)).toBe(input);
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/shift-headings.test.ts
```
Expected output: All 7 unit tests pass.

**Satisfies Requirements:** Req 5.6, 10.3

---

### M7.G4.T3: Property 12 Test for shiftHeadings

**Objective:** Append Property 12 test to `tests/certifications/shift-headings.test.ts` verifying that arbitrary HTML headings are shifted to $\ge h4$ and capped at $h6$.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 12: Heading shift keeps supporting content below h3`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Uses `arbHeadingHtml` from test fixtures.
- ✓ Verifies no tag `<h1`, `<h2`, `<h3` exists in the output.
- ✓ Verifies opening and closing tag counts match for all heading levels.
- ✓ Verifies relative difference between heading levels is preserved up to the $h6$ cap.

**Prerequisites:**
- `arbHeadingHtml` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/shift-headings.test.ts`:

```typescript
import fc from 'fast-check';
import { arbHeadingHtml } from '../fixtures/certifications-arbitraries';

describe('shiftHeadings - Property Tests', () => {
  // Feature: m7-certifications-module, Property 12: Heading shift keeps supporting content below h3
  it('Property 12: shifted output contains no heading above h4 and preserves paired tags', () => {
    fc.assert(
      fc.property(arbHeadingHtml, (html) => {
        const shifted = shiftHeadings(html, 4);

        // No h1, h2, or h3 should ever exist in shifted output
        expect(shifted).not.toMatch(/<\/?h[1-3][\s>]/i);

        // Opening and closing counts for each level 4..6 must be balanced
        for (let level = 1; level <= 6; level++) {
          const openCount = (shifted.match(new RegExp(`<h${level}[\\s>]`, 'gi')) || []).length;
          const closeCount = (shifted.match(new RegExp(`</h${level}>`, 'gi')) || []).length;
          expect(openCount).toBe(closeCount);
        }
      }),
      { numRuns: 100 },
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/shift-headings.test.ts
```
Expected output: Unit tests and Property 12 pass.

**Satisfies Requirements:** Req 5.6, 10.3, 15.2

---

### M7.G4.T4: Implement loadSupportingContent Loader

**Objective:** Create `src/lib/certifications/load-supporting-content.ts` to asynchronously render and heading-shift non-empty certification markdown bodies.

**Acceptance Criteria:**
- ✓ Exports `loadSupportingContent(certifications: readonly Certification[]): Promise<Readonly<Record<string, string>>>`.
- ✓ Iterates over certifications and inspects `cert.content.trim()`.
- ✓ Skips certifications with empty or whitespace-only bodies.
- ✓ Invokes `renderMarkdown(cert.content)` for non-empty bodies.
- ✓ Applies `shiftHeadings(renderedHtml, 4)` to the rendered result.
- ✓ Returns an immutable, frozen dictionary mapping `slug` to shifted HTML.
- ✓ Does not use `dangerouslySetInnerHTML`.

**Prerequisites:**
- `src/content/markdown/renderer.ts` (or `@/content/markdown/renderer`) exports `renderMarkdown`.
- `shiftHeadings` implemented in `src/lib/certifications/shift-headings.ts`.

**Implementation Details:**
Create `src/lib/certifications/load-supporting-content.ts`:

```typescript
import type { Certification } from '@/types/content';
import { renderMarkdown } from '@/content/markdown/renderer';
import { shiftHeadings } from './shift-headings';

export async function loadSupportingContent(
  certifications: readonly Certification[],
): Promise<Readonly<Record<string, string>>> {
  const result: Record<string, string> = {};

  for (const cert of certifications) {
    const rawContent = cert.content?.trim();
    if (!rawContent) {
      continue;
    }

    try {
      const rendered = await renderMarkdown(cert.content);
      const shifted = shiftHeadings(rendered, 4);
      result[cert.slug] = shifted;
    } catch (cause) {
      throw new Error(`Failed to render certification content: ${cert.slug}`, { cause });
    }
  }

  return Object.freeze(result);
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 10.1, 10.2, 10.3, 10.5

---

### M7.G4.T5: Add Error Wrapping with Slug and Cause

**Objective:** Ensure `loadSupportingContent` wraps any error thrown by `renderMarkdown` with a descriptive message naming the slug and forwarding the original error as `cause`.

**Acceptance Criteria:**
- ✓ Caught errors rethrow an `Error` instance with message `Failed to render certification content: <slug>`.
- ✓ The rethrown error includes `{ cause }` pointing to the original error.
- ✓ Build or server process will fail deterministically if any certification markdown is corrupted.

**Prerequisites:**
- `src/lib/certifications/load-supporting-content.ts` created in M7.G4.T4.

**Implementation Details:**
Verify error block in `src/lib/certifications/load-supporting-content.ts` matches:
```typescript
    } catch (cause) {
      throw new Error(`Failed to render certification content: ${cert.slug}`, { cause });
    }
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 10.5

---

### M7.G4.T6: Unit Tests for loadSupportingContent with Mocked Renderer

**Objective:** Create `tests/certifications/load-supporting-content.test.ts` testing empty content omission, rendering execution, and heading shifting with `renderMarkdown` mocked via `vi.mock`.

**Acceptance Criteria:**
- ✓ Mocks `@/content/markdown/renderer`.
- ✓ Test: omits certification when `content` is `""` or whitespace-only.
- ✓ Test: processes non-empty content and inserts shifted HTML into the record.
- ✓ Test: verifies shifted HTML starts at `h4` or deeper.
- ✓ Test: rethrows error containing slug when `renderMarkdown` rejects.

**Prerequisites:**
- `src/lib/certifications/load-supporting-content.ts` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/load-supporting-content.test.ts`:

```typescript
import { describe, it, expect, vi } from 'vitest';
import { loadSupportingContent } from '@/lib/certifications/load-supporting-content';
import {
  fixtureFullCertification,
  fixtureMinimalCertification,
  fixtureWhitespaceCredentialCertification,
} from '../fixtures/certifications-data';
import type { Certification } from '@/types/content';

vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(async (content: string) => {
    if (content.includes('TRIGGER_ERROR')) {
      throw new Error('Markdown parser syntax failure');
    }
    return `<h2>Overview</h2><p>${content}</p>`;
  }),
}));

describe('loadSupportingContent - Unit Tests', () => {
  it('omits certifications with empty or whitespace-only content', async () => {
    const list: Certification[] = [
      fixtureMinimalCertification, // content: ''
      { ...fixtureWhitespaceCredentialCertification, content: '   ' },
    ];

    const result = await loadSupportingContent(list);
    expect(Object.keys(result)).toHaveLength(0);
  });

  it('renders and shifts non-empty content for certifications', async () => {
    const result = await loadSupportingContent([fixtureFullCertification]);
    expect(result[fixtureFullCertification.slug]).toBeDefined();
    // Render mock returned <h2>Overview</h2>, which should be shifted to <h4>Overview</h4>
    expect(result[fixtureFullCertification.slug]).toContain('<h4>Overview</h4>');
  });

  it('rethrows error with slug and cause when renderer fails', async () => {
    const brokenCert: Certification = {
      ...fixtureFullCertification,
      slug: 'broken-cert-slug',
      content: 'TRIGGER_ERROR',
    };

    await expect(loadSupportingContent([brokenCert])).rejects.toThrow(
      'Failed to render certification content: broken-cert-slug',
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/load-supporting-content.test.ts
```
Expected output: All 3 unit tests pass.

**Satisfies Requirements:** Req 10.1, 10.2, 10.3, 10.5

---

### M7.G4.T7: Property 13 Test (Loader Half) for loadSupportingContent

**Objective:** Append Property 13 (loader half) to `tests/certifications/load-supporting-content.test.ts` verifying dictionary creation and empty omission across arbitrary certifications.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 13: Supporting content renders if and only if the body is non-empty (Loader Half)`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Generates arbitrary lists of certifications with random content strings.
- ✓ Asserts that for every certification $C$, `slug` is in `result` iff `C.content.trim().length > 0`.

**Prerequisites:**
- `createArbCertification` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/load-supporting-content.test.ts`:

```typescript
import fc from 'fast-check';
import { createArbCertification } from '../fixtures/certifications-arbitraries';

describe('loadSupportingContent - Property Tests', () => {
  // Feature: m7-certifications-module, Property 13: Supporting content renders if and only if the body is non-empty (Loader Half)
  it('Property 13 (Loader): entry exists in record iff content is non-empty after trim', async () => {
    const arbCertList = fc.uniqueArray(createArbCertification(), {
      selector: (c) => c.slug,
      minLength: 0,
      maxLength: 10,
    });

    await fc.assert(
      fc.asyncProperty(arbCertList, async (certifications) => {
        const result = await loadSupportingContent(certifications);

        for (const cert of certifications) {
          const hasContent = cert.content?.trim().length > 0;
          if (hasContent) {
            expect(result[cert.slug]).toBeDefined();
            expect(typeof result[cert.slug]).toBe('string');
          } else {
            expect(result[cert.slug]).toBeUndefined();
          }
        }
      }),
      { numRuns: 100 },
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/load-supporting-content.test.ts
```
Expected output: Unit tests and Property 13 (loader half) pass with >= 100 runs.

**Satisfies Requirements:** Req 10.1, 10.2, 15.2

---

### M7.G4.T8: Static Scope and Dependency Guard Inspection

**Objective:** Verify that `shift-headings.ts` and `load-supporting-content.ts` have no dependencies on `projects`, contain no `'use client'` directives, and do not call `dangerouslySetInnerHTML`.

**Acceptance Criteria:**
- ✓ Neither file imports from `@/lib/projects/` or `@/components/projects/`.
- ✓ Neither file contains `'use client'`.
- ✓ Neither file contains `dangerouslySetInnerHTML`.

**Prerequisites:**
- `shift-headings.ts` and `load-supporting-content.ts` implemented.

**Implementation Details:**
Run static search over both files.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\lib\certifications\shift-headings.ts, src\lib\certifications\load-supporting-content.ts -Pattern "projects|use client|dangerouslySetInnerHTML"
```
Expected output: No matches found.

**Satisfies Requirements:** Req 1.2, 10.4, 13.2, 15.7

---

### M7.G4.T9: Immutability Test for loadSupportingContent Input

**Objective:** Add a test verifying that `loadSupportingContent` does not mutate a deep-frozen array of certifications.

**Acceptance Criteria:**
- ✓ Test passes a deep-frozen array of certifications to `loadSupportingContent`.
- ✓ Asserts no mutation occurs and execution completes without throwing.

**Prerequisites:**
- `tests/certifications/load-supporting-content.test.ts` available.

**Implementation Details:**
Append to `tests/certifications/load-supporting-content.test.ts`:

```typescript
  it('does not mutate deep-frozen input array', async () => {
    const list = [fixtureFullCertification, fixtureMinimalCertification];
    const frozenList = Object.freeze(list.map((c) => Object.freeze({ ...c })));

    await expect(loadSupportingContent(frozenList)).resolves.toBeDefined();
    expect(frozenList).toHaveLength(2);
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/load-supporting-content.test.ts
```
Expected output: Immutability test passes.

**Satisfies Requirements:** Req 3.9, 15.2

---

### M7.G4.T10: Goal 4 Checkpoint and Pipeline Verification

**Objective:** Run static typing and Vitest suites for Goal 4 modules to confirm all tests pass and there are no compilation errors.

**Acceptance Criteria:**
- ✓ `src/lib/certifications/shift-headings.ts` and `load-supporting-content.ts` compile cleanly.
- ✓ `tests/certifications/shift-headings.test.ts` passes (unit + Property 12).
- ✓ `tests/certifications/load-supporting-content.test.ts` passes (unit + Property 13 + immutability).
- ✓ `npx tsc --noEmit` exits with code 0.

**Prerequisites:**
- Tasks M7.G4.T1 through M7.G4.T9 completed.

**Implementation Details:**
Execute test suite and typechecking commands in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/shift-headings.test.ts tests/certifications/load-supporting-content.test.ts
npx tsc --noEmit
```
Expected output: All unit and property tests pass across both files; zero TypeScript errors.

**Satisfies Requirements:** Req 5.6, 10.1–10.3, 10.5, 15.2, 15.5, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 4 are complete:
```powershell
npx vitest run tests/certifications/shift-headings.test.ts tests/certifications/load-supporting-content.test.ts
npx tsc --noEmit
```
Expected output: All heading-shift and supporting-content tests pass; TypeScript compiles with zero errors.