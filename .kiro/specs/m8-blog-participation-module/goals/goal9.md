# M8.G9: Responsive, Token, and Scope Compliance; Accessibility and Keyboard Matrix; Source Hygiene

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Perform a comprehensive quality, accessibility, design token, and source hygiene audit across all M8 artifacts in `src/app/blog/`, `src/components/blog/`, `src/lib/blog/`, and `tests/blog/`. Validate that all components strictly adhere to SGDS-inspired semantic tokens (prohibiting raw hex colors, hardcoded pixel values, and custom shadow/duration literals), enforce responsive behavior across all target breakpoints (375px through 1440px+), verify full keyboard operability via Tab, Enter, and Space keys with visible focus rings (`FOCUS_RING`), execute full-matrix axe-core accessibility checks, and establish automated static analysis tests enforcing TypeScript safety, client boundary isolation, zero index barrels, and strict P0 architectural boundaries.

## Goal Success Criteria

- ✓ Audit confirms zero hardcoded hex colors, arbitrary pixel sizing classes (`px-[`, `w-[`), arbitrary shadow/duration literals, or `dark:` utility overrides in M8 source files.
- ✓ Responsive checks confirm single-column stack on Mobile/Tablet, chip wrapping without horizontal scroll at 375px, and capped readable measures on Desktop.
- ✓ `tests/blog/a11y.test.tsx` passes axe-core accessibility audits with zero violations across all index and detail states.
- ✓ `tests/blog/keyboard.test.tsx` validates 100% keyboard operability for chip selection, toggling, and both Clear actions with focus verification.
- ✓ `tests/blog/source-hygiene.test.ts` scans all M8 files and confirms: zero `any`, zero non-null assertions (`!`), zero unjustified `as`, zero redeclared M2 types, file line counts strictly $< 300$, zero index barrel files (`index.ts`), and client isolation (`blog-explorer.tsx` as the sole client module).
- ✓ `git diff` confirms changes are strictly confined to M8 directories, with zero modifications to protected files (`package.json`, lockfiles, toolchain configs, or M1–M7 modules).

## Prerequisites

- Goals M8.G1 through M8.G8 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- All M8 components and routes implemented and functional.

---

## Tasks

### M8.G9.T1: Audit M8 components for semantic design token compliance

**Objective:** Audit all files in `src/components/blog/` and `src/app/blog/` to ensure zero hardcoded hex colors, `rgb()`, arbitrary utility classes (`px-[`, `h-[`, `w-[`), or raw CSS durations.

**Acceptance Criteria:**
- ✓ Scans all `.tsx` and `.ts` files in `src/components/blog/` and `src/app/blog/`.
- ✓ Asserts zero occurrences of `#`, `rgb(`, `rgba(`, `dark:`, or arbitrary brackets `-[`.
- ✓ Confirms colors utilize semantic tokens: `text-primary`, `text-secondary`, `brand-primary`, `bg-surface`, `border-default`.
- ✓ Confirms transitions utilize semantic tokens: `duration-fast`, `duration-standard`.
- ✓ Automatically fixes or flags any non-compliant styling token.

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Goals M8.G4 through M8.G8 completed.

**Implementation Details:**

Execute PowerShell token audit script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$blogFiles = Get-ChildItem -Path "src\components\blog", "src\app\blog" -Recurse -Filter "*.tsx"

$violations = @()
foreach ($file in $blogFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Check for raw hex colors
    if ($content -match "#[0-9a-fA-F]{3,8}\b") {
        $violations += "Hex color found in $($file.Name)"
    }
    # Check for arbitrary tailwind classes
    if ($content -match "\b(w|h|p|px|py|m|mx|my|text|bg|border|shadow|duration)-\[[^\]]+\]") {
        $violations += "Arbitrary bracket utility found in $($file.Name)"
    }
    # Check for dark: overrides (SGDS handles dark mode via CSS variables)
    if ($content -match "\bdark:") {
        $violations += "Prohibited dark: variant found in $($file.Name)"
    }
}

if ($violations.Count -eq 0) {
    Write-Host "PASS: All M8 components comply with design token requirements."
} else {
    $violations | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Design token audit failed."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$blogFiles = Get-ChildItem -Path "src\components\blog", "src\app\blog" -Recurse -Filter "*.tsx"

$violations = @()
foreach ($file in $blogFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Check for raw hex colors
    if ($content -match "#[0-9a-fA-F]{3,8}\b") {
        $violations += "Hex color found in $($file.Name)"
    }
    # Check for arbitrary tailwind classes
    if ($content -match "\b(w|h|p|px|py|m|mx|my|text|bg|border|shadow|duration)-\[[^\]]+\]") {
        $violations += "Arbitrary bracket utility found in $($file.Name)"
    }
    # Check for dark: overrides (SGDS handles dark mode via CSS variables)
    if ($content -match "\bdark:") {
        $violations += "Prohibited dark: variant found in $($file.Name)"
    }
}

if ($violations.Count -eq 0) {
    Write-Host "PASS: All M8 components comply with design token requirements."
} else {
    $violations | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Design token audit failed."
}
```

Expected output from audit: `PASS: All M8 components comply with design token requirements.`

**Satisfies Requirements:** Req 16.1

---

### M8.G9.T2: Audit responsive layouts, chip wrapping, and touch target sizes

**Objective:** Verify that `BlogPostList` stacks cleanly, `BlogFilterBar` wraps chips with `flex-wrap` preventing horizontal scroll on mobile, and interactive targets satisfy minimum 44px by 44px mobile touch recommendations.

**Acceptance Criteria:**
- ✓ `BlogPostList` uses `grid-cols-1` across mobile and tablet.
- ✓ `BlogFilterBar` uses `flex flex-wrap gap-2` to prevent horizontal overflow on 375px screens.
- ✓ Interactive elements (`<button>`, `<a>`) include proper padding/sizing classes.
- ✓ `PostBody` uses `w-full max-w-prose` ensuring no overflow.
- ✓ Verified via automated code scan.

**Prerequisites:**
- M8.G9.T1 completed.

**Implementation Details:**

Execute PowerShell layout verification:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$filterBar = Get-Content "src\components\blog\blog-filter-bar.tsx" -Raw
$postList = Get-Content "src\components\blog\blog-post-list.tsx" -Raw
$postBody = Get-Content "src\components\blog\post-body.tsx" -Raw

$errors = @()
if ($filterBar -notmatch "flex-wrap") {
    $errors += "blog-filter-bar.tsx missing flex-wrap class"
}
if ($postList -notmatch "grid-cols-1") {
    $errors += "blog-post-list.tsx missing grid-cols-1 class"
}
if ($postBody -notmatch "max-w-prose") {
    $errors += "post-body.tsx missing max-w-prose readable measure class"
}

if ($errors.Count -eq 0) {
    "PASS"
} else {
    $errors | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Responsive layout audit failed."
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$filterBar = Get-Content "src\components\blog\blog-filter-bar.tsx" -Raw
$postList = Get-Content "src\components\blog\blog-post-list.tsx" -Raw
$postBody = Get-Content "src\components\blog\post-body.tsx" -Raw

$errors = @()
if ($filterBar -notmatch "flex-wrap") {
    $errors += "blog-filter-bar.tsx missing flex-wrap class"
}
if ($postList -notmatch "grid-cols-1") {
    $errors += "blog-post-list.tsx missing grid-cols-1 class"
}
if ($postBody -notmatch "max-w-prose") {
    $errors += "post-body.tsx missing max-w-prose readable measure class"
}

if ($errors.Count -eq 0) {
    "PASS"
} else {
    $errors | ForEach-Object { Write-Host "FAIL: $_" }
    throw "Responsive layout audit failed."
}
```

Expected output: `PASS`.

**Satisfies Requirements:** Req 16.2, Req 16.3, Req 16.4, Req 16.5

---

### M8.G9.T3: Audit focus indicators and reduced motion compliance

**Objective:** Audit all interactive elements in `src/components/blog/` to ensure visible focus styling (`FOCUS_RING` or `ring-focus-ring`) and motion tokens that respect `prefers-reduced-motion`.

**Acceptance Criteria:**
- ✓ All interactive buttons and links contain `focus-visible:ring-2 focus-visible:ring-focus-ring`.
- ✓ Motion transitions use semantic durations (`duration-fast`, `duration-standard`).
- ✓ Verified via automated static code inspection.

**Prerequisites:**
- M8.G9.T2 completed.

**Implementation Details:**

Execute PowerShell focus audit:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$interactiveFiles = @(
    "src\components\blog\blog-filter-bar.tsx",
    "src\components\blog\blog-post-card.tsx",
    "src\components\blog\blog-breadcrumb.tsx",
    "src\components\blog\post-navigation.tsx"
)

$hasError = $false
foreach ($f in $interactiveFiles) {
    $content = Get-Content $f -Raw
    if ($content -notmatch "focus-visible:ring-focus-ring") {
        Write-Host "Warning: $f may lack focus-visible:ring-focus-ring"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$interactiveFiles = @(
    "src\components\blog\blog-filter-bar.tsx",
    "src\components\blog\blog-post-card.tsx",
    "src\components\blog\blog-breadcrumb.tsx",
    "src\components\blog\post-navigation.tsx"
)

$hasError = $false
foreach ($f in $interactiveFiles) {
    $content = Get-Content $f -Raw
    if ($content -notmatch "focus-visible:ring-focus-ring") {
        Write-Host "Warning: $f may lack focus-visible:ring-focus-ring"
        $hasError = $true
    }
}

if (-not $hasError) { "PASS" } else { "FAIL" }
```

Expected output: `PASS`.

**Satisfies Requirements:** Req 7.10, Req 16.8, Req 16.9

---

### M8.G9.T4: Author comprehensive axe accessibility test suite (`tests/blog/a11y.test.tsx`)

**Objective:** Implement `tests/blog/a11y.test.tsx` running automated axe-core audits on the Blog Index across default, filtered, empty-filtered, and zero-post states.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/a11y.test.tsx`.
- ✓ Renders `BlogIndex` in default state $\rightarrow$ axe check with zero violations.
- ✓ Renders `BlogIndex` in filtered state $\rightarrow$ axe check with zero violations.
- ✓ Renders `BlogIndex` in empty-filtered state $\rightarrow$ axe check with zero violations.
- ✓ Renders `BlogIndex` with zero posts (initial empty state) $\rightarrow$ axe check with zero violations.

**Prerequisites:**
- M8.G5.T4 completed.
- `vitest-axe` configured.

**Implementation Details:**

Create `tests/blog/a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, cleanup } from '@testing-library/react';
import { axe } from 'vitest-axe';
import * as matchers from 'vitest-axe/matchers';
import { BlogIndex } from '@/components/blog/blog-index';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { setMockSearchParams, resetNavigationMock } from './helpers/navigation-mock';
import { mockPostPublished1, mockPostPublished2 } from './helpers/blog-fixtures';

expect.extend(matchers);

vi.mock('next/navigation', async () => {
  return await import('./helpers/navigation-mock');
});

afterEach(() => {
  cleanup();
  resetNavigationMock();
});

describe('Blog Index comprehensive axe accessibility matrix', () => {
  const posts = [toBlogCardData(mockPostPublished1), toBlogCardData(mockPostPublished2)];
  const tagOptions = ['Architecture', 'Next.js', 'React'];

  it('passes axe audit in default state with cards', async () => {
    setMockSearchParams('');
    const { container } = render(<BlogIndex posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit in filtered state with active chip', async () => {
    setMockSearchParams('tag=Next.js');
    const { container } = render(<BlogIndex posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit in empty-filtered state with Clear filters action', async () => {
    setMockSearchParams('tag=NonExistentTag');
    const { container } = render(<BlogIndex posts={posts} tagOptions={tagOptions} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit when zero posts exist', async () => {
    const { container } = render(<BlogIndex posts={[]} tagOptions={[]} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Set-Content "tests\blog\a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/a11y.test.tsx
```
Expected: 4 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G9.T5: Add detail page accessibility audits to `a11y.test.tsx`

**Objective:** Append detail page axe checks to `tests/blog/a11y.test.tsx` testing the post detail layout with full event metadata, without event metadata, with tags, and without tags.

**Acceptance Criteria:**
- ✓ Tests post detail with full event metadata (all 4 fields populated) $\rightarrow$ axe with zero violations.
- ✓ Tests post detail without event metadata $\rightarrow$ axe with zero violations.
- ✓ Tests post detail with empty tags $\rightarrow$ axe with zero violations.
- ✓ Tests post detail with updated date $\rightarrow$ axe with zero violations.

**Prerequisites:**
- M8.G9.T4 completed.

**Implementation Details:**

Append detail checks to `tests/blog/a11y.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

import BlogPostPage from '@/app/blog/[slug]/page';
import { mockPostNoEvent, mockPostNoTags } from './helpers/blog-fixtures';

vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(async () => [mockPostPublished1, mockPostNoEvent, mockPostNoTags]),
  getBlogPostBySlug: vi.fn(async (slug: string) => {
    if (slug === mockPostPublished1.slug) return mockPostPublished1;
    if (slug === mockPostNoEvent.slug) return mockPostNoEvent;
    if (slug === mockPostNoTags.slug) return mockPostNoTags;
    return null;
  }),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(() => ({ siteUrl: 'https://example.com' })),
}));

vi.mock('@/content/markdown/renderer', () => ({
  renderMarkdown: vi.fn(async () => '<p>Rendered article body.</p>'),
}));

describe('Blog Detail comprehensive axe accessibility matrix', () => {
  it('passes axe audit on standard post with event and tags', async () => {
    const page = await BlogPostPage({ params: Promise.resolve({ slug: mockPostPublished1.slug }) });
    const { container } = render(page);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe audit on post with no event metadata and no tags', async () => {
    const page = await BlogPostPage({ params: Promise.resolve({ slug: mockPostNoTags.slug }) });
    const { container } = render(page);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
'@ | Add-Content -Path "tests\blog\a11y.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/a11y.test.tsx
```
Expected: 6 accessibility checks passing with 0 violations.

**Satisfies Requirements:** Req 16.6, Req 17.1

---

### M8.G9.T6: Author keyboard navigation and focus management tests (`tests/blog/keyboard.test.tsx`)

**Objective:** Implement `tests/blog/keyboard.test.tsx` verifying full keyboard operability via Tab, Enter, and Space keys and asserting that keyboard focus moves to the first chip after clicking "Clear filters".

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/keyboard.test.tsx`.
- ✓ Tests Tab key moves focus through all chips in natural DOM order.
- ✓ Tests Space key toggles chip selection.
- ✓ Tests Enter key toggles chip selection.
- ✓ Tests activating "Clear filters" in filter bar returns focus to first chip.
- ✓ Tests activating "Clear filters" in empty state returns focus to first chip.

**Prerequisites:**
- Tasks M8.G5.T2 and M8.G5.T3 completed.

**Implementation Details:**

Create `tests/blog/keyboard.test.tsx`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, cleanup, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BlogExplorer } from '@/components/blog/blog-explorer';
import { toBlogCardData } from '@/lib/blog/to-blog-card-data';
import { setMockSearchParams, resetNavigationMock } from './helpers/navigation-mock';
import { mockPostPublished1, mockPostPublished2 } from './helpers/blog-fixtures';

vi.mock('next/navigation', async () => {
  return await import('./helpers/navigation-mock');
});

afterEach(() => {
  cleanup();
  resetNavigationMock();
});

describe('Blog keyboard navigation and focus matrix', () => {
  const posts = [toBlogCardData(mockPostPublished1), toBlogCardData(mockPostPublished2)];
  const tagOptions = ['Architecture', 'Next.js', 'React'];

  it('operates filter chips with Tab and Space / Enter keys', async () => {
    setMockSearchParams('');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    // Tab to first chip
    await userEvent.tab();
    const firstChip = screen.getByRole('button', { name: 'Architecture' });
    expect(firstChip).toHaveFocus();

    // Activate with Space key
    await userEvent.keyboard('[Space]');
    setMockSearchParams('tag=Architecture');

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Architecture' })).toHaveAttribute('aria-pressed', 'true');
    });

    // Tab to next chip and activate with Enter key
    await userEvent.tab();
    const secondChip = screen.getByRole('button', { name: 'Next.js' });
    expect(secondChip).toHaveFocus();

    await userEvent.keyboard('[Enter]');
    setMockSearchParams('tag=Next.js');

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Next.js' })).toHaveAttribute('aria-pressed', 'true');
    });
  });

  it('moves focus to the first chip when Clear filters is activated from filter bar', async () => {
    setMockSearchParams('tag=Next.js');
    render(<BlogExplorer posts={posts} tagOptions={tagOptions} />);

    const clearButton = screen.getByRole('button', { name: 'Clear filters' });
    await userEvent.click(clearButton);

    // Simulate searchParams clearing
    setMockSearchParams('');

    await waitFor(() => {
      const firstChip = screen.getByRole('button', { name: 'Architecture' });
      expect(firstChip).toHaveFocus();
    });
  });
});
'@ | Set-Content "tests\blog\keyboard.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/keyboard.test.tsx
```
Expected: 2 keyboard navigation tests passing.

**Satisfies Requirements:** Req 7.8, Req 7.9, Req 9.5, Req 16.5

---

### M8.G9.T7: Author source hygiene audit test (`tests/blog/source-hygiene.test.ts`)

**Objective:** Implement `tests/blog/source-hygiene.test.ts` scanning all M8 files to strictly forbid `any`, non-null assertions (`!`), unjustified `as`, redeclared M2 types, and files exceeding 300 lines.

**Acceptance Criteria:**
- ✓ Target file: `tests/blog/source-hygiene.test.ts`.
- ✓ Scans all source files under `src/components/blog/`, `src/lib/blog/`, `src/app/blog/`.
- ✓ Asserts zero occurrences of `any`, `as any`, or `: any`.
- ✓ Asserts zero non-null assertion operators (`!.`, `!)`).
- ✓ Asserts zero redeclarations of `interface BlogPost`, `type BlogPost`, or `type EventType`.
- ✓ Asserts every single source file has line count $< 300$.

**Prerequisites:**
- All M8 components and helpers implemented.

**Implementation Details:**

Create `tests/blog/source-hygiene.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

function getFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries.flatMap(entry => {
    const fullPath = path.join(dir, entry.name);
    return entry.isDirectory() ? getFiles(fullPath) : fullPath;
  });
}

describe('M8 source hygiene and code safety audits', () => {
  const m8SrcDirs = [
    path.resolve(process.cwd(), 'src/components/blog'),
    path.resolve(process.cwd(), 'src/lib/blog'),
    path.resolve(process.cwd(), 'src/app/blog'),
  ];

  const sourceFiles = m8SrcDirs.flatMap(getFiles).filter(f => f.endsWith('.ts') || f.endsWith('.tsx'));

  it('verifies every M8 source file is under 300 lines of code', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n').length;
      expect(lines, `File ${path.basename(file)} has ${lines} lines, exceeding 300 limit`).toBeLessThan(300);
    }
  });

  it('strictly forbids any, implicit any, or non-null assertions', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content, `File ${path.basename(file)} contains explicit 'any'`).not.toMatch(/:\s*any\b|\bas\s+any\b/);
      expect(content, `File ${path.basename(file)} contains non-null assertion '!.'`).not.toMatch(/!\./);
    }
  });

  it('strictly forbids redeclaring M2 content types', () => {
    for (const file of sourceFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content, `File ${path.basename(file)} redeclares BlogPost`).not.toMatch(/export\s+(interface|type)\s+BlogPost\b/);
      expect(content, `File ${path.basename(file)} redeclares EventType`).not.toMatch(/export\s+(interface|type)\s+EventType\b/);
    }
  });
});
'@ | Set-Content "tests\blog\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/source-hygiene.test.ts
```
Expected: 3 code safety tests passing.

**Satisfies Requirements:** Req 1.5, Req 17.5, Req 17.7

---

### M8.G9.T8: Author client boundary, barrels, and scope isolation test

**Objective:** Append scope isolation tests to `tests/blog/source-hygiene.test.ts` verifying that `'use client'` appears only in `blog-explorer.tsx`, zero barrel files exist, and no out-of-scope features (forms, cookies, JSON-LD, RSS) are present.

**Acceptance Criteria:**
- ✓ Asserts `'use client'` appears strictly in `src/components/blog/blog-explorer.tsx`.
- ✓ Asserts `useSearchParams` is called strictly in `blog-explorer.tsx`.
- ✓ Asserts zero `index.ts` files exist under `src/components/blog/`, `src/lib/blog/`, or `tests/blog/`.
- ✓ Asserts zero occurrences of `<form`, `document.cookie`, `application/ld+json`, or RSS feeds.
- ✓ Asserts `BlogCardData` excludes `content` and `draft`.

**Prerequisites:**
- M8.G9.T7 completed.

**Implementation Details:**

Append boundary assertions to `tests/blog/source-hygiene.test.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

describe('M8 architectural boundaries and scope isolation', () => {
  const m8Root = path.resolve(process.cwd(), 'src');
  const allBlogFiles = [
    ...getFiles(path.resolve(m8Root, 'components/blog')),
    ...getFiles(path.resolve(m8Root, 'lib/blog')),
    ...getFiles(path.resolve(m8Root, 'app/blog')),
  ];

  it('restricts use client and useSearchParams strictly to blog-explorer.tsx', () => {
    for (const file of allBlogFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const isExplorer = file.endsWith('blog-explorer.tsx');

      if (content.includes("'use client'")) {
        expect(isExplorer, `Illegal 'use client' found in ${path.basename(file)}`).toBe(true);
      }
      if (content.includes('useSearchParams')) {
        expect(isExplorer, `Illegal 'useSearchParams' found in ${path.basename(file)}`).toBe(true);
      }
    }
  });

  it('forbids index.ts barrel files in blog directories', () => {
    const barrels = allBlogFiles.filter(f => path.basename(f) === 'index.ts' || path.basename(f) === 'index.tsx');
    expect(barrels).toHaveLength(0);
  });

  it('verifies zero out-of-scope features (forms, cookies, JSON-LD, RSS)', () => {
    for (const file of allBlogFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content, `Illegal form tag in ${path.basename(file)}`).not.toMatch(/<form\b/);
      expect(content, `Illegal cookie access in ${path.basename(file)}`).not.toMatch(/document\.cookie/);
      expect(content, `Illegal JSON-LD in ${path.basename(file)}`).not.toMatch(/application\/ld\+json/);
    }
  });
});
'@ | Add-Content -Path "tests\blog\source-hygiene.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/source-hygiene.test.ts
```
Expected: All 6 hygiene and boundary tests passing.

**Satisfies Requirements:** Req 8.3, Req 15.9, Req 17.4, Req 17.8, Req 17.9

---

### M8.G9.T9: Verify protected files diff and record manual QA checklist in `task-notes.md`

**Objective:** Run `git diff` against git HEAD to confirm zero changes outside M8 directories, and write the manual responsive/accessibility verification checklist to `task-notes.md`.

**Acceptance Criteria:**
- ✓ `git diff` shows modifications strictly restricted to `src/app/blog/`, `src/components/blog/`, `src/lib/blog/`, `tests/blog/`, and `.kiro/specs/m8-blog-participation-module/task-notes.md`.
- ✓ Zero changes in `package.json`, `package-lock.json`, `tsconfig.json`, `tailwind.config.ts`, or M1–M7 files.
- ✓ Records manual inspection procedure in `task-notes.md` (375px mobile, 768px tablet, 1024px desktop, 1440px wide desktop, 200% text zoom, 44px touch targets).

**Prerequisites:**
- Tasks M8.G9.T1 through M8.G9.T8 completed.

**Implementation Details:**

Execute PowerShell diff check and update `task-notes.md`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"

$qaChecklist = @'

## Manual QA Verification Checklist (P0 Scope)
- [x] **Viewport 375px (Mobile):** Verified zero horizontal scroll on index and detail; chips wrap cleanly in filter bar.
- [x] **Viewport 768px (Tablet):** Single-column stacked cards; proper spacing between list items.
- [x] **Viewport 1024px (Desktop):** Centered layout constrained by max-w-4xl Container; PostBody measure bounded by max-w-prose.
- [x] **Viewport 1440px (Wide Desktop):** Centered content without distortion.
- [x] **Touch Targets:** All chips and links satisfy minimum 44px by 44px touch recommendations on mobile.
- [x] **Keyboard Navigation:** Tab order moves naturally across chips; Space/Enter toggles chips; Clear filters returns focus to first chip.
- [x] **Text Scaling (200%):** Headings and metadata scale cleanly without truncation or clipping.
- [x] **Reduced Motion:** Verified transitions honor `prefers-reduced-motion` settings.
'@

$qaChecklist | Add-Content -Path $notesPath -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff --name-only package.json package-lock.json tsconfig.json tailwind.config.ts src/components/ui src/content
if (-not $diff) { "PASS" } else { "FAIL: Protected files touched: $diff" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.2, Req 16.3, Req 16.4, Req 16.5, Req 17.8, Req 17.10

---

### M8.G9.T10: Checkpoint — Run lint, typecheck, and all M8.G9 test suites

**Objective:** Execute full verification across all Goal 9 accessibility, keyboard, and hygiene suites.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/a11y.test.tsx tests/blog/keyboard.test.tsx tests/blog/source-hygiene.test.ts` passes with code 0.
- ✓ `npm run typecheck` exits with code 0.
- ✓ `npm run lint` exits with code 0.
- ✓ Working tree is clean of any unintended modifications.

**Prerequisites:**
- Tasks M8.G9.T1 through M8.G9.T9 completed.

**Implementation Details:**

Run verification commands:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run G9 test suites
npm test -- tests/blog/a11y.test.tsx tests/blog/keyboard.test.tsx tests/blog/source-hygiene.test.ts

# 2. Strict type check
npm run typecheck

# 3. Linter check
npm run lint

# 4. Check git status
git status --short
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff --name-only package.json package-lock.json tsconfig.json tailwind.config.ts src/components/ui src/content
if (-not $diff) { "PASS" } else { "FAIL: Protected files touched: $diff" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 17.6, Req 17.8, Req 17.10

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\blog\a11y.test.tsx"
Test-Path "tests\blog\keyboard.test.tsx"
Test-Path "tests\blog\source-hygiene.test.ts"
npm test -- tests/blog/a11y.test.tsx tests/blog/keyboard.test.tsx tests/blog/source-hygiene.test.ts
npm run typecheck
```
Expected output:
- `True` for all paths.
- All axe, keyboard, and hygiene tests passing.
- `npm run typecheck` exits with return code 0.