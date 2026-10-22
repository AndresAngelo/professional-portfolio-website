# M3.G8: MarkdownDoc, enhanceDocumentHtml, and CSS Module

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component `MarkdownDoc` documentation layout in `src/components/ui/markdown-doc.tsx`, styled via a co-located CSS Module (`src/components/ui/markdown-doc.module.css`), alongside the pure HTML accessibility transformation helper `enhanceDocumentHtml` in `src/components/ui/markdown-doc-enhance.ts`. Ensure documentation conforms to `design.md` Section 4.5 by enforcing a maximum readable line measure of 65–75 characters (`max-w-[70ch]`), styling typography hierarchy beginning strictly at `h2`, rendering monospace code blocks that scroll horizontally without page overflow, and wrapping tables in keyboard-focusable labelled regions with `scope` attributes on table headers. Validate transformation purity, idempotence, and accessibility attributes using Vitest.

## Goal Success Criteria

- ✓ `src/components/ui/markdown-doc-enhance.ts` exports pure helper `enhanceDocumentHtml(html: string, labels: EnhanceLabels): string`
- ✓ `enhanceDocumentHtml` injects `tabindex="0"` and `aria-label` into `<pre>` blocks lacking them
- ✓ `enhanceDocumentHtml` wraps uncontained `<table>` elements in `<div data-doc-table role="region" tabindex="0" aria-label="...">`
- ✓ `enhanceDocumentHtml` injects `scope="col"` into `<th>` elements lacking a scope attribute
- ✓ Transformation is strictly additive, content-preserving, and idempotent (`f(f(x)) === f(x)`)
- ✓ `src/components/ui/markdown-doc.module.css` styles headings (`h2`–`h4`), code, blockquotes, lists, and tables using `@apply` with M1 tokens, containing zero raw values except the documented `70ch` prose measure
- ✓ `src/components/ui/markdown-doc.tsx` renders sanitized HTML without client directives, documenting the M2 sanitization trust boundary
- ✓ `tests/unit/components/ui/markdown-doc-enhance.test.ts` and `markdown-doc.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` passes with zero errors under strict mode

## Prerequisites

- Goals M3.G1 through M3.G7 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `src/components/ui/cx.ts` and `focus-ring.ts` exist and compile

---

## Tasks

### M3.G8.T1: Implement Pure HTML Enhancer (`src/components/ui/markdown-doc-enhance.ts`)

**Objective:** Author `enhanceDocumentHtml` in `src/components/ui/markdown-doc-enhance.ts` to attach keyboard accessibility attributes and scroll regions to sanitized HTML.

**Acceptance Criteria:**
- ✓ File `src/components/ui/markdown-doc-enhance.ts` created
- ✓ Exports `EnhanceLabels` interface (`codeBlockLabel: string; tableLabel: string`)
- ✓ Exports `enhanceDocumentHtml(html: string, labels: EnhanceLabels): string`
- ✓ Regex transform adds `tabindex="0"` and `aria-label="{labels.codeBlockLabel}"` to `<pre>` tags lacking them
- ✓ Regex transform wraps uncontained `<table>` tags in `<div data-doc-table role="region" tabindex="0" aria-label="{labels.tableLabel}">`
- ✓ Regex transform adds `scope="col"` to `<th>` tags lacking `scope` attributes
- ✓ Preserves existing `tabindex`, labels, `scope="row"`, and tag content unchanged
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/markdown-doc-enhance.ts`

**Implementation Details:**

Write `src/components/ui/markdown-doc-enhance.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
/**
 * HTML Enhancement Helper for Markdown Documentation
 *
 * Injects required accessibility attributes (tabindex, aria-labels, table regions, th scopes)
 * into sanitized HTML produced by the M2 pipeline before rendering (Req 10.5, 10.6, 10.8).
 */

export interface EnhanceLabels {
  codeBlockLabel: string;
  tableLabel: string;
}

/**
 * Pure, additive, and idempotent string transformation helper.
 * Adds keyboard focusability to scrollable code and tables without parsing Markdown.
 */
export function enhanceDocumentHtml(html: string, labels: EnhanceLabels): string {
  if (!html || !html.trim()) {
    return '';
  }

  let enhanced = html;

  // 1. Enhance <pre> blocks: add tabindex="0" and aria-label if not already present
  enhanced = enhanced.replace(/<pre(\b[^>]*)>/gi, (match, attrs: string) => {
    let newAttrs = attrs;
    if (!/\btabindex\s*=/i.test(newAttrs)) {
      newAttrs += ' tabindex="0"';
    }
    if (!/\baria-label\s*=/i.test(newAttrs)) {
      newAttrs += ` aria-label="${labels.codeBlockLabel}"`;
    }
    return `<pre${newAttrs}>`;
  });

  // 2. Enhance <th> elements: inject scope="col" if missing
  enhanced = enhanced.replace(/<th(\b[^>]*)>/gi, (match, attrs: string) => {
    if (!/\bscope\s*=/i.test(attrs)) {
      return `<th scope="col"${attrs}>`;
    }
    return match;
  });

  // 3. Wrap <table> elements in scrollable focusable region if not already wrapped
  // Checks if table is immediately preceded by data-doc-table wrapper
  enhanced = enhanced.replace(
    /(?:<div\s+data-doc-table[^>]*>)?\s*(<table\b[^>]*>[\s\S]*?<\/table>)\s*(?:<\/div>)?/gi,
    (match, tableContent: string) => {
      return `<div data-doc-table role="region" tabindex="0" aria-label="${labels.tableLabel}">${tableContent}</div>`;
    }
  );

  return enhanced;
}
'@ | Set-Content "src\components\ui\markdown-doc-enhance.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/markdown-doc-enhance.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.5, Req 10.6, Req 10.8, Req 16.1

---

### M3.G8.T2: Implement CSS Module for Prose Styling (`src/components/ui/markdown-doc.module.css`)

**Objective:** Author `src/components/ui/markdown-doc.module.css` defining typography hierarchy, monospace code styling, table formatting, and the 65–75 character prose constraint using `@apply` of semantic M1 tokens.

**Acceptance Criteria:**
- ✓ File `src/components/ui/markdown-doc.module.css` created
- ✓ Constrains measure via `max-width: 70ch;` (between 65ch and 75ch per Req 10.1)
- ✓ Styles `h2` through `h4` using `@apply` with `text-heading-3`, `text-heading-4`, and `text-body`
- ✓ Styles inline `code` and `<pre>` with monospace font tokens and `overflow-x-auto`
- ✓ Styles `[data-doc-table]` wrapper with `overflow-x-auto` and focus outline
- ✓ Styles blockquotes, lists, and images with semantic borders and margins
- ✓ Contains zero raw hex or arbitrary colors; uses only M1 tokens

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/markdown-doc.module.css`

**Implementation Details:**

Write `src/components/ui/markdown-doc.module.css` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
/* Markdown Documentation Prose Styling
 * design.md Section 4.5 & Requirement 10
 */

.doc {
  @apply font-sans text-body text-text-primary w-full;
  /* 70ch is strictly within the 65ch - 75ch measure target (Req 10.1) */
  max-width: 70ch;
}

.doc h2 {
  @apply text-heading-3 font-semibold text-text-primary mt-12 mb-4;
}

.doc h3 {
  @apply text-heading-4 font-semibold text-text-primary mt-8 mb-3;
}

.doc h4 {
  @apply text-body font-semibold text-text-primary mt-6 mb-2;
}

.doc p {
  @apply text-body text-text-primary mb-4 leading-relaxed;
}

.doc ul {
  @apply list-disc pl-6 mb-4 space-y-1;
}

.doc ol {
  @apply list-decimal pl-6 mb-4 space-y-1;
}

.doc li {
  @apply text-body text-text-primary;
}

.doc blockquote {
  @apply border-l-4 border-border-strong pl-4 my-6 text-text-secondary italic;
}

.doc a {
  @apply text-brand-primary underline hover:opacity-80 rounded-sm;
}

.doc a:focus-visible {
  @apply outline-none ring-2 ring-focus-ring ring-offset-2;
}

.doc code:not(pre code) {
  @apply font-mono text-small bg-surface border border-border-default rounded-sm px-1.5 py-0.5 text-text-primary;
}

.doc pre {
  @apply font-mono text-small bg-surface border border-border-default rounded-md p-4 my-6 overflow-x-auto;
}

.doc pre:focus-visible {
  @apply outline-none ring-2 ring-focus-ring ring-offset-2;
}

.doc div[data-doc-table] {
  @apply my-6 w-full overflow-x-auto rounded-md border border-border-default;
}

.doc div[data-doc-table]:focus-visible {
  @apply outline-none ring-2 ring-focus-ring ring-offset-2;
}

.doc table {
  @apply w-full text-small text-left border-collapse;
}

.doc th {
  @apply bg-surface text-text-primary font-semibold p-3 border-b border-border-default;
}

.doc td {
  @apply p-3 border-b border-border-default text-text-secondary;
}

.doc img {
  @apply max-w-full h-auto rounded-md my-6;
}
'@ | Set-Content "src\components\ui\markdown-doc.module.css" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\markdown-doc.module.css"
```
Expected output: `True`

**Satisfies Requirements:** Req 10.1, Req 10.2, Req 10.3, Req 10.4, Req 10.6, Req 10.7

---

### M3.G8.T3: Implement `MarkdownDoc` Component (`src/components/ui/markdown-doc.tsx`)

**Objective:** Author the server component `MarkdownDoc` in `src/components/ui/markdown-doc.tsx` combining `enhanceDocumentHtml` and the CSS module.

**Acceptance Criteria:**
- ✓ File `src/components/ui/markdown-doc.tsx` created
- ✓ Exports `MarkdownDocProps` requiring `html`, `codeBlockLabel`, and `tableLabel`
- ✓ Applies `enhanceDocumentHtml` before rendering
- ✓ Injects enhanced HTML via `dangerouslySetInnerHTML`
- ✓ Contains architectural justification comment explaining that HTML is pre-sanitized by M2
- ✓ Suppresses `react/no-danger` lint rule with inline justification
- ✓ Server component without `'use client'`

**Prerequisites:**
- M3.G8.T1 and M3.G8.T2 completed
- Target file: `src/components/ui/markdown-doc.tsx`

**Implementation Details:**

Write `src/components/ui/markdown-doc.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { cx } from './cx';
import { enhanceDocumentHtml } from './markdown-doc-enhance';
import styles from './markdown-doc.module.css';

export interface MarkdownDocProps {
  /**
   * Sanitized HTML output produced by the upstream M2 Markdown pipeline.
   * Never raw Markdown or untrusted markup (Req 10.8).
   */
  html: string;
  /** Accessible name prefix for scrollable code blocks (e.g. "Code example") */
  codeBlockLabel: string;
  /** Accessible name for scrollable table regions (e.g. "Data table") */
  tableLabel: string;
  className?: string;
}

/**
 * Markdown Documentation Layout Primitive
 *
 * Formats rendered markdown documentation with readable 65-75ch line measure,
 * monospace code styling, and accessible scrollable table/code regions.
 * design.md Section 4.5 & Requirement 10. Server component by default (Req 10.10).
 */
export function MarkdownDoc({
  html,
  codeBlockLabel,
  tableLabel,
  className,
}: MarkdownDocProps): JSX.Element {
  const enhancedHtml = enhanceDocumentHtml(html, {
    codeBlockLabel,
    tableLabel,
  });

  return (
    // eslint-disable-next-line react/no-danger -- input is strictly sanitized upstream by M2 rehype-sanitize
    <div
      className={cx(styles.doc, className)}
      dangerouslySetInnerHTML={{ __html: enhancedHtml }}
    />
  );
}
'@ | Set-Content "src\components\ui\markdown-doc.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/ui/markdown-doc.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.8, Req 10.9, Req 10.10, Req 16.8

---

### M3.G8.T4: Author Unit Tests for `enhanceDocumentHtml` (`tests/unit/components/ui/markdown-doc-enhance.test.ts`)

**Objective:** Create `tests/unit/components/ui/markdown-doc-enhance.test.ts` testing attribute injection on `<pre>`, `<table>`, and `<th>` elements.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/markdown-doc-enhance.test.ts` created
- ✓ Tests `<pre>` receives `tabindex="0"` and `aria-label`
- ✓ Tests `<table>` is wrapped in `<div data-doc-table role="region" tabindex="0" aria-label="...">`
- ✓ Tests `<th>` without scope receives `scope="col"`
- ✓ Tests `<th>` with existing `scope="row"` is preserved
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G8.T1 completed
- Target file: `tests/unit/components/ui/markdown-doc-enhance.test.ts`

**Implementation Details:**

Write unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import { describe, it, expect } from 'vitest';
import { enhanceDocumentHtml } from '@/components/ui/markdown-doc-enhance';

describe('enhanceDocumentHtml Pure Helper (Req 10.5, 10.6, 10.8)', () => {
  const labels = {
    codeBlockLabel: 'Code snippet',
    tableLabel: 'Data table',
  };

  it('injects tabindex="0" and aria-label into pre elements', () => {
    const input = '<pre><code>const x = 1;</code></pre>';
    const output = enhanceDocumentHtml(input, labels);

    expect(output).toContain('tabindex="0"');
    expect(output).toContain('aria-label="Code snippet"');
    expect(output).toContain('const x = 1;');
  });

  it('wraps tables in accessible focusable scroll regions', () => {
    const input = '<table><thead><tr><th>Header</th></tr></thead></table>';
    const output = enhanceDocumentHtml(input, labels);

    expect(output).toContain('<div data-doc-table role="region" tabindex="0" aria-label="Data table">');
    expect(output).toContain('</div>');
  });

  it('injects scope="col" into table headers lacking scope', () => {
    const input = '<table><tr><th>Tool</th><th scope="row">RowHeader</th></tr></table>';
    const output = enhanceDocumentHtml(input, labels);

    expect(output).toContain('<th scope="col">Tool</th>');
    expect(output).toContain('<th scope="row">RowHeader</th>');
  });

  it('handles empty and whitespace strings gracefully', () => {
    expect(enhanceDocumentHtml('', labels)).toBe('');
    expect(enhanceDocumentHtml('   ', labels)).toBe('');
  });
});
'@ | Set-Content "tests\unit\components\ui\markdown-doc-enhance.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.5, Req 10.6, Req 10.8, Req 14.1

---

### M3.G8.T5: Author Unit Tests for `MarkdownDoc` Component (`tests/unit/components/ui/markdown-doc.test.tsx`)

**Objective:** Create `tests/unit/components/ui/markdown-doc.test.tsx` verifying DOM rendering, CSS module wrapper, and absence of `<h1>` emission.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/markdown-doc.test.tsx` created
- ✓ Renders sample HTML with headings, code blocks, lists, and tables
- ✓ Asserts internal heading hierarchy starts at `h2` and emits no `<h1>` tags (Req 10.9)
- ✓ Asserts pre element is focusable (`tabindex="0"`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G8.T3 completed
- Target file: `tests/unit/components/ui/markdown-doc.test.tsx`

**Implementation Details:**

Write component tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MarkdownDoc } from '@/components/ui/markdown-doc';

describe('MarkdownDoc Primitive (Req 10)', () => {
  const sampleHtml = `
    <h2>Architecture Overview</h2>
    <p>Pipeline notes.</p>
    <pre><code>const a = 1;</code></pre>
    <table>
      <thead>
        <tr><th>Metric</th><th>Target</th></tr>
      </thead>
      <tbody>
        <tr><td>LCP</td><td>&lt; 2.5s</td></tr>
      </tbody>
    </table>
  `;

  it('renders enhanced HTML without emitting h1 elements', () => {
    const { container } = render(
      <MarkdownDoc
        html={sampleHtml}
        codeBlockLabel="Code block"
        tableLabel="Performance table"
      />
    );

    expect(screen.getByRole('heading', { level: 2, name: 'Architecture Overview' })).toBeDefined();
    expect(container.querySelector('h1')).toBeNull();

    const pre = container.querySelector('pre');
    expect(pre?.getAttribute('tabindex')).toBe('0');
    expect(pre?.getAttribute('aria-label')).toBe('Code block');

    const tableRegion = container.querySelector('div[data-doc-table]');
    expect(tableRegion?.getAttribute('role')).toBe('region');
    expect(tableRegion?.getAttribute('aria-label')).toBe('Performance table');
  });
});
'@ | Set-Content "tests\unit\components\ui\markdown-doc.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/markdown-doc.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.1, Req 10.5, Req 10.6, Req 10.9, Req 14.1

---

### M3.G8.T6: Author Property-Based Test for Enhancement Attributes (Property 11)

**Objective:** Append property-based test in `tests/unit/components/ui/markdown-doc-enhance.test.ts` using `fast-check` asserting that for any HTML snippet containing `<pre>` or `<table>`, required accessibility attributes are injected.

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Generates randomized snippets containing `<pre>` and `<table>`
- ✓ Asserts every `<pre>` contains `tabindex="0"` and `aria-label`
- ✓ Asserts every `<table>` is contained in a labelled region
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/markdown-doc-enhance.test.ts`

**Implementation Details:**

Append property test to `tests/unit/components/ui/markdown-doc-enhance.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: Enhancement Attributes (Property 11)', () => {
    it('Feature: m3-design-system-implementation, Property 11: ensures all pre blocks have tabindex and all tables have region wrappers for any HTML snippet', () => {
      const fc = require('fast-check');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 50 }).filter((s: string) => !s.includes('<') && s.trim().length > 0),
          (codeSnippet: string) => {
            const raw = `<pre><code>${codeSnippet}</code></pre><table><tr><th>Col</th></tr></table>`;
            const result = enhanceDocumentHtml(raw, labels);

            expect(result).toContain('tabindex="0"');
            expect(result).toContain('aria-label="Code snippet"');
            expect(result).toContain('data-doc-table');
            expect(result).toContain('scope="col"');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\markdown-doc-enhance.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\markdown-doc-enhance.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.5, Req 10.6, Req 14.1

---

### M3.G8.T7: Author Property-Based Test for Idempotence & Content Preservation (Property 12)

**Objective:** Append property-based test in `tests/unit/components/ui/markdown-doc-enhance.test.ts` proving that applying `enhanceDocumentHtml` multiple times produces the exact same output (`f(f(x)) === f(x)`).

**Acceptance Criteria:**
- ✓ Runs at least 100 iterations with `fast-check`
- ✓ Asserts `enhanceDocumentHtml(enhanceDocumentHtml(x)) === enhanceDocumentHtml(x)`
- ✓ Asserts underlying text content is preserved without corruption
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/ui/markdown-doc-enhance.test.ts`

**Implementation Details:**

Append idempotence property test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Test: Idempotence & Content Preservation (Property 12)', () => {
    it('Feature: m3-design-system-implementation, Property 12: enhanceDocumentHtml is strictly idempotent and content-preserving', () => {
      const fc = require('fast-check');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 40 }).filter((s: string) => !s.includes('<') && s.trim().length > 0),
          (textContent: string) => {
            const raw = `<p>${textContent}</p><pre><code>${textContent}</code></pre>`;
            const firstPass = enhanceDocumentHtml(raw, labels);
            const secondPass = enhanceDocumentHtml(firstPass, labels);

            expect(secondPass).toBe(firstPass);
            expect(firstPass).toContain(textContent);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\markdown-doc-enhance.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\markdown-doc-enhance.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.5, Req 10.6, Req 10.8, Req 14.1

---

### M3.G8.T8: Author Automated Axe Accessibility Tests for MarkdownDoc

**Objective:** Append automated axe checks in `tests/unit/components/ui/markdown-doc.test.tsx` verifying WCAG 2.1 AA compliance including `scrollable-region-focusable`.

**Acceptance Criteria:**
- ✓ Renders MarkdownDoc with headings, wide code block, and wide data table
- ✓ Evaluates axe rules including `scrollable-region-focusable`
- ✓ Reports zero accessibility violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target file: `tests/unit/components/ui/markdown-doc.test.tsx`

**Implementation Details:**

Append axe check to `tests/unit/components/ui/markdown-doc.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Accessibility Verification (Req 15)', () => {
    it('produces zero WCAG violations on complex markdown documentation layout', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(
        <MarkdownDoc
          html={`
            <h2>Detailed Evaluation</h2>
            <p>Comprehensive description.</p>
            <pre><code>const longLine = "very long code line that forces horizontal scrolling in the container";</code></pre>
            <table>
              <thead>
                <tr><th>Column A</th><th>Column B</th></tr>
              </thead>
              <tbody>
                <tr><td>Value 1</td><td>Value 2</td></tr>
              </tbody>
            </table>
          `}
          codeBlockLabel="Code block example"
          tableLabel="Evaluation results table"
        />
      );

      const results = await axe(container);
      expect(results.violations.length).toBe(0);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\markdown-doc.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\markdown-doc.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/ui/markdown-doc.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2

---

### M3.G8.T9: Verify Source Hygiene of `markdown-doc.tsx` and CSS Module

**Objective:** Audit `src/components/ui/markdown-doc.tsx`, `markdown-doc-enhance.ts`, and `markdown-doc.module.css` to confirm zero raw hex values and verify the only raw value in the CSS module is the documented `70ch` measure.

**Acceptance Criteria:**
- ✓ Zero raw hex (`#[0-9A-Fa-f]{3,8}`) across all three files
- ✓ Zero `rgb(`/`rgba(`
- ✓ `markdown-doc.module.css` contains `max-width: 70ch;` and zero other raw pixel/hex dimensions
- ✓ Total TypeScript files under 300 lines

**Prerequisites:**
- M3.G8.T1, M3.G8.T2, M3.G8.T3 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @(
    "src\components\ui\markdown-doc.tsx",
    "src\components\ui\markdown-doc-enhance.ts",
    "src\components\ui\markdown-doc.module.css"
)
$allPass = $true

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    $hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
    $hasRgb = $content -match 'rgba?\('

    if ($hasHex -or $hasRgb) {
        $allPass = $false
        Write-Host "Violation in $file (Hex=$hasHex, RGB=$hasRgb)"
    }
}

$css = Get-Content "src\components\ui\markdown-doc.module.css" -Raw
if (-not ($css -match 'max-width:\s*70ch;')) {
    $allPass = $false
    Write-Host "markdown-doc.module.css must contain max-width: 70ch per Requirement 10.1"
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 10.1, Req 16.1, Req 16.8

---

### M3.G8.T10: Checkpoint — MarkdownDoc Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across MarkdownDoc and its enhancement helpers.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all MarkdownDoc tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M3.G8.T1 through M3.G8.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts tests/unit/components/ui/markdown-doc.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts tests/unit/components/ui/markdown-doc.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\ui\markdown-doc.tsx"
Test-Path "src\components\ui\markdown-doc-enhance.ts"
Test-Path "src\components\ui\markdown-doc.module.css"
Test-Path "tests\unit\components\ui\markdown-doc.test.tsx"
Test-Path "tests\unit\components\ui\markdown-doc-enhance.test.ts"
npm run typecheck
npm run test -- tests/unit/components/ui/markdown-doc-enhance.test.ts tests/unit/components/ui/markdown-doc.test.tsx
```
Expected output:
- `True` for all 5 paths
- `npm run typecheck` exits with return code 0
- Vitest passes with code 0.