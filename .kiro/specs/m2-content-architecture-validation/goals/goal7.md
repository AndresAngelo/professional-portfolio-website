# M2.G7: Markdown Rendering Pipeline

> **Milestone:** M2 — Content Architecture & Validation  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-side Markdown-to-HTML rendering pipeline in `src/content/markdown/render.ts` using the unified ecosystem (`remark-parse`, `remark-gfm`, `remark-rehype`, `rehype-highlight`, `rehype-sanitize`, and `rehype-stringify`). Ensure code blocks receive syntax highlighting, external links automatically acquire `rel="noopener noreferrer"`, output HTML is strictly sanitized against XSS injection, and author unit tests validating code block transformation, sanitization, and security attributes per `TRD.md` Section 6.4 and `requirements.md` Requirement 14.

## Goal Success Criteria

- ✓ Unified ecosystem packages installed in `dependencies`
- ✓ `src/content/markdown/render.ts` exports `renderMarkdown(markdown: string): Promise<string>`
- ✓ GitHub Flavored Markdown (GFM) features (tables, strikethrough, autolinks) supported
- ✓ Code blocks rendered with syntax-highlighting classes via `rehype-highlight`
- ✓ Custom unist AST plugin injects `rel="noopener noreferrer"` into external links starting with `http://` or `https://`
- ✓ HTML output sanitized via `rehype-sanitize` to strip unescaped `<script>` tags, inline event handlers, and malicious vectors
- ✓ All unit tests in `tests/unit/markdown/render.test.ts` pass cleanly
- ✓ `npm run typecheck` passes with zero errors under strict TypeScript

## Prerequisites

- Goals M2.G1 through M2.G6 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/content/markdown/` directory exists

---

## Tasks

### M2.G7.T1: Install Unified Ecosystem Dependencies

**Objective:** Install the unified, remark, and rehype toolchain libraries into `dependencies`.

**Acceptance Criteria:**
- ✓ `unified` installed
- ✓ `remark-parse` and `remark-gfm` installed
- ✓ `remark-rehype` installed
- ✓ `rehype-highlight` and `rehype-sanitize` installed
- ✓ `rehype-stringify` and `unist-util-visit` installed
- ✓ `npm install` completes cleanly with no peer dependency conflicts

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Install packages using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm install unified remark-parse remark-gfm remark-rehype rehype-highlight rehype-sanitize rehype-stringify unist-util-visit
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$deps = $pkg.dependencies
if ($deps.unified -and $deps."remark-gfm" -and $deps."rehype-sanitize") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.6

---

### M2.G7.T2: Implement External Link Security Plugin

**Objective:** Author a custom unist plugin inside `src/content/markdown/plugins.ts` that traverses HTML AST elements and attaches `rel="noopener noreferrer"` and `target="_blank"` to external links.

**Acceptance Criteria:**
- ✓ `src/content/markdown/plugins.ts` exports `externalLinkPlugin`
- ✓ Detects `<a>` tags with `href` starting with `http://` or `https://`
- ✓ Attaches `target: '_blank'` and `rel: ['noopener', 'noreferrer']`
- ✓ Leaves relative internal links (e.g. `/projects`) unmodified
- ✓ Fully typed without using explicit `any`

**Prerequisites:**
- M2.G7.T1 completed
- Target file: `src/content/markdown/plugins.ts`

**Implementation Details:**

Write the plugin module using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import type { Root, Element } from 'hast';
import { visit } from 'unist-util-visit';

/**
 * Unist plugin that inspects all <a> elements and secures external links
 * by appending rel="noopener noreferrer" and target="_blank".
 * TRD.md 6.4 & AGENTS.md 5.1
 */
export function externalLinkPlugin() {
  return (tree: Root): void => {
    visit(tree, 'element', (node: Element) => {
      if (node.tagName === 'a' && node.properties && typeof node.properties.href === 'string') {
        const href = node.properties.href.trim();

        if (href.startsWith('http://') || href.startsWith('https://')) {
          node.properties.target = '_blank';
          node.properties.rel = ['noopener', 'noreferrer'];
        }
      }
    });
  };
}
'@ | Set-Content "src\content\markdown\plugins.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/markdown/plugins.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.3, Req 20.2

---

### M2.G7.T3: Implement Markdown Rendering Pipeline Skeleton

**Objective:** Author `renderMarkdown()` in `src/content/markdown/render.ts` chaining remark, rehype, highlight, sanitization, and stringification.

**Acceptance Criteria:**
- ✓ Exports `renderMarkdown(markdown: string): Promise<string>`
- ✓ Uses `unified()` pipeline:
  - `remarkParse`
  - `remarkGfm`
  - `remarkRehype`
  - `rehypeHighlight`
  - `externalLinkPlugin`
  - `rehypeSanitize`
  - `rehypeStringify`
- ✓ Returns sanitized HTML string
- ✓ Throws descriptive error on pipeline processing failure

**Prerequisites:**
- M2.G7.T2 completed
- Target file: `src/content/markdown/render.ts`

**Implementation Details:**

Write `render.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeHighlight from 'rehype-highlight';
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize';
import rehypeStringify from 'rehype-stringify';
import { externalLinkPlugin } from './plugins';

// Extend default sanitization schema to allow class names produced by rehype-highlight
const sanitizeSchema = {
  ...defaultSchema,
  attributes: {
    ...defaultSchema.attributes,
    code: [...(defaultSchema.attributes?.code ?? []), ['className', /^hljs-/]],
    span: [...(defaultSchema.attributes?.span ?? []), ['className', /^hljs-/]],
    a: [...(defaultSchema.attributes?.a ?? []), 'target', 'rel'],
  },
};

/**
 * Converts a Markdown string into sanitized HTML.
 * Includes GitHub Flavored Markdown, syntax highlighting,
 * XSS sanitization, and rel="noopener noreferrer" injection for external links.
 *
 * @param markdown - Raw Markdown string content.
 * @returns Sanitized HTML string ready for injection.
 */
export async function renderMarkdown(markdown: string): Promise<string> {
  if (!markdown || !markdown.trim()) {
    return '';
  }

  try {
    const file = await unified()
      .use(remarkParse)
      .use(remarkGfm)
      .use(remarkRehype)
      .use(rehypeHighlight, { ignoreMissing: true })
      .use(externalLinkPlugin)
      .use(rehypeSanitize, sanitizeSchema)
      .use(rehypeStringify)
      .process(markdown);

    return String(file);
  } catch (error) {
    throw new Error(
      `Markdown rendering failed: ${error instanceof Error ? error.message : String(error)}`
    );
  }
}
'@ | Set-Content "src\content\markdown\render.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/markdown/render.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.3, Req 14.6

---

### M2.G7.T4: Author Unit Tests for Basic Markdown and GFM Tables

**Objective:** Create `tests/unit/markdown/render.test.ts` testing basic Markdown formatting (headings, lists, bold) and GFM extensions (tables, strikethrough).

**Acceptance Criteria:**
- ✓ Verifies `## Heading` produces `<h2>Heading</h2>`
- ✓ Verifies lists produce `<ul>` and `<li>` elements
- ✓ Verifies GFM tables produce `<table>`, `<thead>`, `<tbody>`, `<th>`, and `<td>` elements
- ✓ Verifies strikethrough `~~text~~` produces `<del>text</del>`

**Prerequisites:**
- M2.G7.T3 completed
- Target file: `tests/unit/markdown/render.test.ts`

**Implementation Details:**

Create test file with GFM test cases using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\unit\markdown")) {
    New-Item -ItemType Directory -Path "tests\unit\markdown" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { renderMarkdown } from '@/content/markdown/render';

describe('Markdown Rendering Pipeline', () => {
  it('renders standard Markdown headings, lists, and formatting', async () => {
    const md = '## Architecture Decisions\n\n- Point 1\n- Point 2\n\n**Bold text**';
    const html = await renderMarkdown(md);

    expect(html).toContain('<h2>Architecture Decisions</h2>');
    expect(html).toContain('<ul>');
    expect(html).toContain('<li>Point 1</li>');
    expect(html).toContain('<strong>Bold text</strong>');
  });

  it('renders GitHub Flavored Markdown (GFM) tables and strikethrough', async () => {
    const md = `
| Tool | Purpose |
| :--- | :--- |
| Vitest | Testing |

~~strikethrough~~
`;
    const html = await renderMarkdown(md);

    expect(html).toContain('<table>');
    expect(html).toContain('<th>Tool</th>');
    expect(html).toContain('<td>Testing</td>');
    expect(html).toContain('<del>strikethrough</del>');
  });

  it('returns empty string when given empty or whitespace-only markdown', async () => {
    expect(await renderMarkdown('')).toBe('');
    expect(await renderMarkdown('   \n\t  ')).toBe('');
  });
});
'@ | Set-Content "tests\unit\markdown\render.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/markdown/render.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 19.1

---

### M2.G7.T5: Author Unit Tests for Code Syntax Highlighting

**Objective:** Append tests verifying that fenced code blocks produce syntax-highlighted HTML spans with highlight.js (`hljs-`) classes.

**Acceptance Criteria:**
- ✓ Fenced code blocks with language tag (e.g. ````typescript` or ````json`) render `<pre><code class="hljs ...">`
- ✓ Code tokens contain syntax highlight spans (`hljs-keyword`, `hljs-string`, etc.)
- ✓ Test passes in the test runner

**Prerequisites:**
- M2.G7.T4 completed
- Target file: `tests/unit/markdown/render.test.ts`

**Implementation Details:**

Append syntax highlighting tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

  it('applies syntax highlighting classes to fenced code blocks', async () => {
    const md = '```typescript\nconst greeting: string = "hello world";\n```';
    const html = await renderMarkdown(md);

    expect(html).toContain('<pre><code');
    expect(html).toContain('hljs');
    expect(html).toContain('language-typescript');
  });
'@
$content = Get-Content "tests\unit\markdown\render.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\markdown\render.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/markdown/render.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.2, Req 19.1

---

### M2.G7.T6: Author Unit Tests for External Link Security Attributes

**Objective:** Append tests verifying that external links receive `rel="noopener noreferrer"` and `target="_blank"`, while relative links remain untouched.

**Acceptance Criteria:**
- ✓ External links starting with `https://` receive `rel="noopener noreferrer"`
- ✓ External links starting with `https://` receive `target="_blank"`
- ✓ Internal relative links (e.g. `/projects`) do NOT have `target="_blank"` or `rel` attributes
- ✓ Test passes in test runner

**Prerequisites:**
- M2.G7.T5 completed
- Target file: `tests/unit/markdown/render.test.ts`

**Implementation Details:**

Append external link tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

  describe('External link security (TRD.md 6.4)', () => {
    it('appends rel="noopener noreferrer" and target="_blank" to external links', async () => {
      const md = '[External Site](https://example.com)';
      const html = await renderMarkdown(md);

      expect(html).toContain('href="https://example.com"');
      expect(html).toContain('target="_blank"');
      expect(html).toContain('rel="noopener noreferrer"');
    });

    it('leaves internal relative links unmodified', async () => {
      const md = '[Internal Page](/projects)';
      const html = await renderMarkdown(md);

      expect(html).toContain('href="/projects"');
      expect(html).not.toContain('target="_blank"');
      expect(html).not.toContain('rel=');
    });
  });
'@
$content = Get-Content "tests\unit\markdown\render.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\markdown\render.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/markdown/render.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.3, Req 19.1

---

### M2.G7.T7: Author Unit Tests for XSS Sanitization

**Objective:** Append tests verifying that dangerous HTML tags and script payloads are stripped or neutralized by `rehype-sanitize`.

**Acceptance Criteria:**
- ✓ `<script>` tags embedded in markdown are removed
- ✓ Inline event handlers (e.g. `<img src="x" onerror="alert(1)">`) are stripped
- ✓ `javascript:` pseudoprotocol URLs in markdown links are neutralized
- ✓ Test passes in test runner

**Prerequisites:**
- M2.G7.T6 completed
- Target file: `tests/unit/markdown/render.test.ts`

**Implementation Details:**

Append XSS sanitization tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

  describe('XSS Sanitization (TRD.md 6.4)', () => {
    it('removes embedded script tags from markdown', async () => {
      const md = 'Hello <script>alert("xss")</script> World';
      const html = await renderMarkdown(md);

      expect(html).not.toContain('<script');
      expect(html).not.toContain('alert("xss")');
      expect(html).toContain('Hello  World');
    });

    it('strips malicious inline event handlers like onerror or onclick', async () => {
      const md = '<img src="invalid.jpg" onerror="alert(1)" alt="test" />';
      const html = await renderMarkdown(md);

      expect(html).not.toContain('onerror');
      expect(html).toContain('src="invalid.jpg"');
      expect(html).toContain('alt="test"');
    });

    it('neutralizes javascript: pseudoprotocol links', async () => {
      const md = '[Click me](javascript:alert(1))';
      const html = await renderMarkdown(md);

      expect(html).not.toContain('href="javascript:');
    });
  });
'@
$content = Get-Content "tests\unit\markdown\render.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\markdown\render.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/markdown/render.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.6, Req 19.1

---

### M2.G7.T8: Create Helper to Pre-Render Project and Blog Post Markdown

**Objective:** Implement a helper function `renderContentHtml(rawMarkdown: string)` and verify integration with loaders.

**Acceptance Criteria:**
- ✓ Exports `renderContentHtml(rawMarkdown: string): Promise<string>`
- ✓ Validates that documentation bodies with code and headings render to valid HTML
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M2.G7.T3 completed
- Target file: `src/content/markdown/render.ts`

**Implementation Details:**

Update `src/content/markdown/render.ts` with alias export using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

/**
 * Convenience alias for rendering content markdown documentation.
 */
export const renderContentHtml = renderMarkdown;
'@
Add-Content -Path "src\content\markdown\render.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/content/markdown/render.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 20.4

---

### M2.G7.T9: Test End-to-End Markdown Rendering of Seed Files

**Objective:** Author an integration test verifying that the actual seed files (`example-project.mdx` and `example-blog-post.mdx`) render to HTML without errors.

**Acceptance Criteria:**
- ✓ Reads `content/projects/example-project.mdx` body and renders to HTML
- ✓ Reads `content/blog/example-blog-post.mdx` body and renders to HTML
- ✓ Generated HTML contains expected heading structures
- ✓ Test passes cleanly

**Prerequisites:**
- M2.G7.T8 completed
- Target file: `tests/unit/markdown/render.test.ts`

**Implementation Details:**

Append seed file rendering tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appendCode = @'

  describe('Seed Content Markdown Rendering Integration', () => {
    it('successfully converts example-project.mdx documentation to HTML', async () => {
      const fs = require('fs/promises');
      const path = require('path');
      const matter = require('gray-matter');

      const projectPath = path.join(process.cwd(), 'content', 'projects', 'example-project.mdx');
      const raw = await fs.readFile(projectPath, 'utf-8');
      const { content } = matter(raw);

      const html = await renderMarkdown(content);
      expect(html).toContain('<h2>Build Documentation</h2>');
      expect(html).toContain('Explain the problem');
    });

    it('successfully converts example-blog-post.mdx body to HTML', async () => {
      const fs = require('fs/promises');
      const path = require('path');
      const matter = require('gray-matter');

      const blogPath = path.join(process.cwd(), 'content', 'blog', 'example-blog-post.mdx');
      const raw = await fs.readFile(blogPath, 'utf-8');
      const { content } = matter(raw);

      const html = await renderMarkdown(content);
      expect(html).toContain('<p>Post content describing participation');
    });
  });
'@
$content = Get-Content "tests\unit\markdown\render.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\markdown\render.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/markdown/render.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 18.1, Req 18.3

---

### M2.G7.T10: Checkpoint — Markdown Rendering Pipeline Verification

**Objective:** Execute the complete verification pipeline (`typecheck`, `lint`, `test`) to ensure the Markdown rendering pipeline passes all quality gates.

**Acceptance Criteria:**
- ✓ `npm run typecheck` exits with return code 0
- ✓ `npm run lint` exits with return code 0
- ✓ `npm run test` executes all test suites including markdown rendering and passes
- ✓ Zero `any` types or unsafe assertions

**Prerequisites:**
- M2.G7.T1 through M2.G7.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 15.5, Req 20.1, Req 20.2

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\content\markdown\render.ts"
Test-Path "src\content\markdown\plugins.ts"
npm run test -- tests/unit/markdown/render.test.ts
npm run typecheck
```
Expected output:
- `True` for `render.ts` and `plugins.ts`
- Tests in `render.test.ts` pass cleanly with 0 failures
- `npm run typecheck` exits with return code 0.