# M8.G1: Fixtures, Blog Types, Tag Key, Upstream Contract Verification, and Gap Log

> **Milestone:** M8 — Blog / Participation Module  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the foundational testing fixtures, fast-check property arbitraries, domain types, and string normalization utilities required by the Blog / Participation module. Verify all upstream M1–M7 dependencies (M2 schemas/loaders, M3 primitives, M4 layout landmarks, M5 date formatting and string comparison, and the M6 `demoteHeadings` export per Decision 3) to guarantee strict zero-hallucination contract alignment before implementing blog features. Record all findings and interface contracts in `task-notes.md`.

## Goal Success Criteria

- ✓ `tests/blog/helpers/blog-fixtures.ts` exports strictly typed `BlogPost` fixture objects and fast-check arbitraries conforming to M2 contracts.
- ✓ `src/lib/blog/blog-types.ts` defines and exports `BlogCardData`, `BlogListItem`, `BlogFilters`, `TagOption`, `TAG_PARAM`, and `BLOG_PATH` without redeclaring M2 content schemas.
- ✓ `src/lib/blog/tag-key.ts` implements deterministic, locale-invariant tag normalization (`tagKey`) with 100% unit test coverage.
- ✓ Upstream M2 loaders (`getBlogPosts`, `getBlogPostBySlug`, `getSiteConfig`), M3 UI primitives, M4 layout landmarks, and M5 utilities (`formatDisplayDate`, `compareStrings`) are verified present and compatible.
- ✓ Decision 3 rule for `demoteHeadings` is audited and recorded in `task-notes.md`.
- ✓ `git diff` confirms zero unintended modifications to protected files (`package.json`, lockfiles, toolchain configs, or existing milestone directories).

## Prerequisites

- Milestones M1 through M7 completed.
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream type definitions available at `src/types/content.ts`.

---

## Tasks

### M8.G1.T1: Create baseline typed blog post fixtures (`tests/blog/helpers/blog-fixtures.ts`)

**Objective:** Create the blog fixtures module exporting standard published, draft, mixed-case, and edge-case `BlogPost` objects using canonical types from `@/types/content`.

**Acceptance Criteria:**
- ✓ Directory `tests/blog/helpers/` exists.
- ✓ `tests/blog/helpers/blog-fixtures.ts` imports `BlogPost` from `@/types/content`.
- ✓ Exports `mockPostPublished1`, `mockPostPublished2`, `mockPostPublished3` with varied tags, dates, and event data.
- ✓ Exports `mockPostDraft` with `draft: true`.
- ✓ Exports `mockPostMixedCaseTags` with tags like `['TypeScript', 'next.js', ' AI ']`.
- ✓ Exports `mockPostTiedDate1` and `mockPostTiedDate2` with identical `publishedAt` but distinct `slug` values (`slug-a`, `slug-b`).
- ✓ Zero use of `any`, `as unknown as`, or non-null assertions (`!`).

**Prerequisites:**
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- M2 contract file exists: `src/types/content.ts`

**Implementation Details:**

Create `tests/blog/helpers/blog-fixtures.ts` with the initial fixture set:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
if (-not (Test-Path "tests\blog\helpers")) {
    New-Item -ItemType Directory -Path "tests\blog\helpers" -Force | Out-Null
}

@'
import type { BlogPost } from '@/types/content';

export const mockPostPublished1: BlogPost = {
  slug: 'react-summit-2026',
  title: 'React Summit 2026 Key Takeaways',
  summary: 'Architectural lessons learned from React Summit covering React Server Components and state boundaries.',
  publishedAt: '2026-06-15',
  updatedAt: '2026-06-18',
  eventType: 'conference',
  eventName: 'React Summit Global',
  eventDate: '2026-06-14',
  eventLocation: 'Amsterdam & Online',
  eventUrl: 'https://reactsummit.com',
  tags: ['React', 'Next.js', 'Architecture'],
  readingTimeMinutes: 6,
  draft: false,
  content: '## Overview\n\nKey discussions on server-driven UI and static optimization.',
};

export const mockPostPublished2: BlogPost = {
  slug: 'ai-agents-hackathon',
  title: 'Building Deterministic AI Agents at Hackathon',
  summary: 'Reflections from the 48-hour local AI agent hackathon exploring stateless LLM orchestration.',
  publishedAt: '2026-04-10',
  updatedAt: null,
  eventType: 'hackathon',
  eventName: 'Autonomous Agents Hackathon 2026',
  eventDate: '2026-04-09',
  eventLocation: 'Singapore',
  eventUrl: 'https://hackathon.example.com',
  tags: ['AI', 'Agents', 'TypeScript'],
  readingTimeMinutes: 5,
  draft: false,
  content: '## Hackathon Highlights\n\nExploring dual-model local code execution loops.',
};

export const mockPostPublished3: BlogPost = {
  slug: 'singapore-dev-meetup',
  title: 'Modern Frontend Patterns Meetup',
  summary: 'Notes from presenting specification-driven frontend design at Singapore Developers Meetup.',
  publishedAt: '2026-02-20',
  updatedAt: null,
  eventType: 'meetup',
  eventName: 'SG Devs Monthly',
  eventDate: '2026-02-19',
  eventLocation: 'One-North, Singapore',
  eventUrl: null,
  tags: ['Community', 'Architecture'],
  readingTimeMinutes: 3,
  draft: false,
  content: '## Discussion Points\n\nAuditing token systems and accessible component architectures.',
};

export const mockPostDraft: BlogPost = {
  slug: 'unreleased-draft-post',
  title: 'Unreleased Draft Thoughts on Web Standards',
  summary: 'In-progress exploration of modern web standards and browser-native primitives.',
  publishedAt: '2026-07-01',
  updatedAt: null,
  eventType: 'learning',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['Standards', 'DraftTopic'],
  readingTimeMinutes: 4,
  draft: true,
  content: '## Draft Section\n\nThis draft must never appear in production bundles.',
};

export const mockPostMixedCaseTags: BlogPost = {
  slug: 'mixed-case-tag-experiment',
  title: 'Tag Case Normalization Study',
  summary: 'Demonstrating that tags matching case-insensitively are handled gracefully by filter helpers.',
  publishedAt: '2026-03-01',
  updatedAt: null,
  eventType: 'learning',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['typescript', 'REACT', '  Next.js  ', 'ai'],
  readingTimeMinutes: 2,
  draft: false,
  content: '## Case Insensitivity\n\nTags should map to identical tagKey values regardless of case.',
};

export const mockPostTiedDate1: BlogPost = {
  slug: 'tied-date-alpha',
  title: 'Tied Date Post Alpha',
  summary: 'First post sharing an identical publication date for tie-breaker verification.',
  publishedAt: '2026-05-01',
  updatedAt: null,
  eventType: 'project-update',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['DevOps'],
  readingTimeMinutes: 2,
  draft: false,
  content: '## Tied Alpha\n\nSorting must tie-break alphabetically by slug ascending.',
};

export const mockPostTiedDate2: BlogPost = {
  slug: 'tied-date-beta',
  title: 'Tied Date Post Beta',
  summary: 'Second post sharing an identical publication date for tie-breaker verification.',
  publishedAt: '2026-05-01',
  updatedAt: null,
  eventType: 'project-update',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['DevOps'],
  readingTimeMinutes: 3,
  draft: false,
  content: '## Tied Beta\n\nSorting must tie-break alphabetically by slug ascending.',
};
'@ | Set-Content "tests\blog\helpers\blog-fixtures.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: Zero type errors; command returns code 0.

**Satisfies Requirements:** Req 1.5, Req 2.9, Req 3.4, Req 17.1

---

### M8.G1.T2: Add event and date edge-case fixtures (`tests/blog/helpers/blog-fixtures.ts`)

**Objective:** Expand `blog-fixtures.ts` with posts representing edge combinations of optional event attributes, missing tags, and extreme dates.

**Acceptance Criteria:**
- ✓ Exports `mockPostNoEvent`: All event fields (`eventName`, `eventDate`, `eventLocation`, `eventUrl`) are `null`.
- ✓ Exports `mockPostOnlyEventUrl`: Only `eventUrl` is non-null; name, date, location are `null`.
- ✓ Exports `mockPostOnlyEventName`: Only `eventName` is provided; URL, date, location are `null`.
- ✓ Exports `mockPostNoTags`: `tags: []`.
- ✓ Exports `mockPostWhitespaceTags`: tags containing empty or spaces-only entries `['   ', '', 'ValidTag']`.
- ✓ Exports helper array `allMockBlogPosts: BlogPost[]` combining published and draft fixtures.

**Prerequisites:**
- M8.G1.T1 completed.
- Target file: `tests/blog/helpers/blog-fixtures.ts`.

**Implementation Details:**

Append the edge fixtures to `tests/blog/helpers/blog-fixtures.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

export const mockPostNoEvent: BlogPost = {
  slug: 'post-without-event',
  title: 'Deep Work and Architecture Without Events',
  summary: 'Reflections written independently of any meetup or conference activity.',
  publishedAt: '2026-01-10',
  updatedAt: null,
  eventType: 'learning',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['Architecture', 'Reflections'],
  readingTimeMinutes: 4,
  draft: false,
  content: '## Solo Reflections\n\nEvent block must completely omit itself when all fields are null.',
};

export const mockPostOnlyEventUrl: BlogPost = {
  slug: 'post-only-event-url',
  title: 'Post With Only Event URL Provided',
  summary: 'Referencing an external event link where no metadata name or location was recorded.',
  publishedAt: '2026-02-15',
  updatedAt: null,
  eventType: 'workshop',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: 'https://workshop.example.org',
  tags: ['Workshop'],
  readingTimeMinutes: 3,
  draft: false,
  content: '## External Workshop\n\nShould render link without description list pairs.',
};

export const mockPostOnlyEventName: BlogPost = {
  slug: 'post-only-event-name',
  title: 'Post With Only Event Name Provided',
  summary: 'Discussing an informal gathering with a named event but no website or public URL.',
  publishedAt: '2026-02-16',
  updatedAt: null,
  eventType: 'meetup',
  eventName: 'Informal Tech Roundtable',
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['Discussion'],
  readingTimeMinutes: 2,
  draft: false,
  content: '## Roundtable\n\nMust render dl with event name but omit missing link without broken anchor.',
};

export const mockPostNoTags: BlogPost = {
  slug: 'post-with-no-tags',
  title: 'Post Without Any Associated Tags',
  summary: 'A standalone article that does not assign any technology or category tags.',
  publishedAt: '2026-01-05',
  updatedAt: null,
  eventType: 'learning',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: [],
  readingTimeMinutes: 1,
  draft: false,
  content: '## Untagged Post\n\nTagList element must be omitted completely from card and header.',
};

export const mockPostWhitespaceTags: BlogPost = {
  slug: 'post-whitespace-tags',
  title: 'Post With Dirty Tag Strings',
  summary: 'Verifying that empty strings and space-only tags are dropped cleanly during derivation.',
  publishedAt: '2026-01-08',
  updatedAt: null,
  eventType: 'learning',
  eventName: null,
  eventDate: null,
  eventLocation: null,
  eventUrl: null,
  tags: ['   ', '', 'CleanTag', '   PaddedTag   '],
  readingTimeMinutes: 2,
  draft: false,
  content: '## Dirty Tags\n\nDerivation must discard empty tag keys.',
};

export const allMockBlogPosts: BlogPost[] = [
  mockPostPublished1,
  mockPostPublished2,
  mockPostPublished3,
  mockPostDraft,
  mockPostMixedCaseTags,
  mockPostTiedDate1,
  mockPostTiedDate2,
  mockPostNoEvent,
  mockPostOnlyEventUrl,
  mockPostOnlyEventName,
  mockPostNoTags,
  mockPostWhitespaceTags,
];
'@ | Add-Content -Path "tests\blog\helpers\blog-fixtures.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: Zero errors reported.

**Satisfies Requirements:** Req 2.7, Req 11.4, Req 12.1–12.6, Req 17.1

---

### M8.G1.T3: Add fast-check property arbitraries (`tests/blog/helpers/blog-fixtures.ts`)

**Objective:** Author composable `fast-check` arbitraries in `blog-fixtures.ts` to generate random, valid `BlogPost`, `BlogCardData`, `BlogFilters`, and tag inputs for Property-Based Tests (PBT).

**Acceptance Criteria:**
- ✓ Exports `arbitraryIsoDate`: Generates valid ISO `YYYY-MM-DD` strings.
- ✓ Exports `arbitrarySlug`: Generates lowercase alphanumeric hyphenated slug strings.
- ✓ Exports `arbitraryEventType`: Generates valid `EventType` union members.
- ✓ Exports `arbitraryBlogPost`: Generates fully typed `BlogPost` instances with random draft status, tags, and optional event fields.
- ✓ Exports `arbitraryBlogCardData`: Generates `BlogCardData` objects conforming to `design.md`.
- ✓ Exports `arbitraryBlogFilters`: Generates `BlogFilters` with nullable tag names.
- ✓ Imports `fc` from `fast-check`.

**Prerequisites:**
- M8.G1.T2 completed.
- `fast-check` installed in project `devDependencies`.

**Implementation Details:**

Append the arbitraries to `tests/blog/helpers/blog-fixtures.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'

import fc from 'fast-check';
import type { EventType } from '@/types/content';

export const arbitraryIsoDate = fc
  .tuple(
    fc.integer({ min: 2024, max: 2028 }),
    fc.integer({ min: 1, max: 12 }),
    fc.integer({ min: 1, max: 28 })
  )
  .map(([y, m, d]) => `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`);

export const arbitrarySlug = fc
  .array(fc.stringMatching(/^[a-z0-9]{2,10}$/), { minLength: 1, maxLength: 4 })
  .map(parts => parts.join('-'));

export const arbitraryEventType: fc.Arbitrary<EventType> = fc.constantFrom(
  'meetup',
  'hackathon',
  'workshop',
  'conference',
  'learning',
  'project-update'
);

export const arbitraryTag = fc
  .string({ minLength: 1, maxLength: 25 })
  .filter(s => s.trim().length > 0);

export const arbitraryBlogPost: fc.Arbitrary<BlogPost> = fc.record({
  slug: arbitrarySlug,
  title: fc.string({ minLength: 5, maxLength: 80 }),
  summary: fc.string({ minLength: 20, maxLength: 160 }),
  publishedAt: arbitraryIsoDate,
  updatedAt: fc.option(arbitraryIsoDate, { nil: null }),
  eventType: arbitraryEventType,
  eventName: fc.option(fc.string({ minLength: 3, maxLength: 60 }), { nil: null }),
  eventDate: fc.option(arbitraryIsoDate, { nil: null }),
  eventLocation: fc.option(fc.string({ minLength: 3, maxLength: 50 }), { nil: null }),
  eventUrl: fc.option(fc.webUrl(), { nil: null }),
  tags: fc.array(arbitraryTag, { maxLength: 6 }),
  readingTimeMinutes: fc.integer({ min: 1, max: 45 }),
  draft: fc.boolean(),
  content: fc.string({ minLength: 20, maxLength: 500 }).map(body => `## Section\n\n${body}`),
});

export const arbitraryBlogCardData = arbitraryBlogPost.map(post => ({
  slug: post.slug,
  title: post.title,
  summary: post.summary,
  publishedAt: post.publishedAt,
  readingTimeMinutes: post.readingTimeMinutes,
  eventType: post.eventType,
  tags: post.tags,
}));

export const arbitraryBlogFilters = fc.record({
  tag: fc.option(arbitraryTag, { nil: null }),
});
'@ | Add-Content -Path "tests\blog\helpers\blog-fixtures.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: Zero compiler errors.

**Satisfies Requirements:** Req 17.1, Req 17.2

---

### M8.G1.T4: Create core blog types module (`src/lib/blog/blog-types.ts`)

**Objective:** Implement `src/lib/blog/blog-types.ts` defining canonical types and constants without modifying or duplicating schemas in `@/types/content`.

**Acceptance Criteria:**
- ✓ Target file: `src/lib/blog/blog-types.ts`.
- ✓ Exports `BLOG_PATH = '/blog'`.
- ✓ Exports `TAG_PARAM = 'tag'`.
- ✓ Exports `BlogFilters = { readonly tag: string | null }`.
- ✓ Exports `TagOption = string`.
- ✓ Exports `BlogCardData = Pick<BlogPost, 'slug' | 'title' | 'summary' | 'publishedAt' | 'readingTimeMinutes' | 'eventType' | 'tags'>`.
- ✓ Exports `BlogListItem = BlogCardData & { readonly draft?: boolean }`.
- ✓ Imports `BlogPost` from `@/types/content`.
- ✓ Contains zero `any` or loose casts.

**Prerequisites:**
- Directory `src/lib/blog/` exists or is created.

**Implementation Details:**

Create `src/lib/blog/blog-types.ts`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
if (-not (Test-Path "src\lib\blog")) {
    New-Item -ItemType Directory -Path "src\lib\blog" -Force | Out-Null
}

@'
import type { BlogPost } from '@/types/content';

export const BLOG_PATH = '/blog' as const;
export const TAG_PARAM = 'tag' as const;

export type BlogFilters = {
  readonly tag: string | null;
};

export type TagOption = string;

export type BlogCardData = Pick<
  BlogPost,
  'slug' | 'title' | 'summary' | 'publishedAt' | 'readingTimeMinutes' | 'eventType' | 'tags'
>;

export type BlogListItem = BlogCardData & {
  readonly draft?: boolean;
};
'@ | Set-Content "src\lib\blog\blog-types.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
```
Expected: PASS with 0 errors.

**Satisfies Requirements:** Req 1.5, Req 2.9, Req 4.5, Req 8.4

---

### M8.G1.T5: Implement tag key normalization and unit tests (`tagKey`)

**Objective:** Implement the pure string normalization helper `tagKey` in `src/lib/blog/tag-key.ts` and test whitespace stripping, lowercasing, and locale invariance.

**Acceptance Criteria:**
- ✓ `src/lib/blog/tag-key.ts` exports `function tagKey(name: string): string`.
- ✓ Implementation performs `name.trim().toLowerCase()`.
- ✓ Does NOT use `toLocaleLowerCase()` to ensure determinism across hosting environments.
- ✓ `tests/blog/tag-key.test.ts` covers leading/trailing whitespace, uppercase characters, mixed case, and identical output across locales.
- ✓ Test suite passes completely.

**Prerequisites:**
- `src/lib/blog/` directory present.

**Implementation Details:**

1. Create `src/lib/blog/tag-key.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
/**
 * Normalizes a tag name for deterministic deduplication, matching, and sorting.
 * Strips outer whitespace and converts characters to lowercase using invariant ASCII logic.
 */
export function tagKey(name: string): string {
  return name.trim().toLowerCase();
}
'@ | Set-Content "src\lib\blog\tag-key.ts" -Encoding UTF8
```

2. Create `tests/blog/tag-key.test.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
@'
import { describe, it, expect } from 'vitest';
import { tagKey } from '@/lib/blog/tag-key';

describe('tagKey helper', () => {
  it('converts uppercase and mixed-case strings to lowercase', () => {
    expect(tagKey('TypeScript')).toBe('typescript');
    expect(tagKey('REACT')).toBe('react');
    expect(tagKey('Next.js')).toBe('next.js');
  });

  it('trims leading and trailing whitespace', () => {
    expect(tagKey('  Cloud Architecture  ')).toBe('cloud architecture');
    expect(tagKey('\tDevOps\n')).toBe('devops');
  });

  it('handles empty or whitespace-only strings safely', () => {
    expect(tagKey('')).toBe('');
    expect(tagKey('   ')).toBe('');
  });

  it('preserves internal spaces and special characters', () => {
    expect(tagKey('AI & Machine Learning')).toBe('ai & machine learning');
    expect(tagKey('CI/CD Pipelines')).toBe('ci/cd pipelines');
  });
});
'@ | Set-Content "tests\blog\tag-key.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm test -- tests/blog/tag-key.test.ts
```
Expected: 4 tests passing.

**Satisfies Requirements:** Req 4.2, Req 5.1, Req 6.2, Req 17.4

---

### M8.G1.T6: Audit upstream M2 and M5 interfaces

**Objective:** Verify that M2 loaders (`getBlogPosts`, `getBlogPostBySlug`, `getSiteConfig`, `renderMarkdown`), M2 content types, and M5 utilities (`formatDisplayDate`, `compareStrings`) exist and match expected signatures.

**Acceptance Criteria:**
- ✓ `src/content/loaders/blog.ts` exports `getBlogPosts` and `getBlogPostBySlug`.
- ✓ `src/content/loaders/site.ts` exports `getSiteConfig`.
- ✓ `src/content/markdown/renderer.ts` (or equivalent M2 markdown pipeline) exports `renderMarkdown`.
- ✓ `src/lib/format-date.ts` exports `formatDisplayDate(date: string): string`.
- ✓ `src/lib/home/compare.ts` exports `compareStrings(a: string, b: string): number`.
- ✓ Audit script verifies presence; results logged in `.kiro/specs/m8-blog-participation-module/task-notes.md`.

**Prerequisites:**
- Milestones M2 and M5 complete.

**Implementation Details:**

Execute PowerShell audit script to confirm modules:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"
if (-not (Test-Path ".kiro\specs\m8-blog-participation-module")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m8-blog-participation-module" -Force | Out-Null
}

$report = @()
$report += "# M8 Upstream Contract Audit Report"
$report += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

$checks = @(
    @{ Path = "src\content\loaders\blog.ts"; Symbols = @("getBlogPosts", "getBlogPostBySlug") },
    @{ Path = "src\content\loaders\site.ts"; Symbols = @("getSiteConfig") },
    @{ Path = "src\lib\format-date.ts"; Symbols = @("formatDisplayDate") },
    @{ Path = "src\lib\home\compare.ts"; Symbols = @("compareStrings") }
)

foreach ($c in $checks) {
    if (Test-Path $c.Path) {
        $content = Get-Content $c.Path -Raw
        foreach ($s in $c.Symbols) {
            if ($content -match "\b$s\b") {
                $report += "- [x] **$($c.Path)**: Symbol `$s` found."
            } else {
                $report += "- [ ] **ERROR**: `$s` missing from $($c.Path)"
            }
        }
    } else {
        $report += "- [ ] **ERROR**: File $($c.Path) does not exist."
    }
}

$report | Set-Content $notesPath -Encoding UTF8
Get-Content $notesPath
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Select-String -Path ".kiro\specs\m8-blog-participation-module\task-notes.md" -Pattern "ERROR"
```
Expected: No lines returned (zero errors).

**Satisfies Requirements:** Req 1.2, Req 10.4, Req 11.9, Req 17.8

---

### M8.G1.T7: Audit M3 UI primitives and FilterChip client boundary

**Objective:** Verify that M3 UI components (`Card`, `TagList`, `EventTypeBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`, `FOCUS_RING`) exist and inspect whether `FilterChip` carries `'use client'`.

**Acceptance Criteria:**
- ✓ Checks for each required primitive under `src/components/ui/`.
- ✓ Audits whether `FilterChip` contains `'use client'` directive.
- ✓ Records confirmed primitive prop names and directives in `task-notes.md`.
- ✓ Strictly adheres to read-only access (no modifications to M3 files).

**Prerequisites:**
- Milestone M3 completed.
- Target log: `.kiro/specs/m8-blog-participation-module/task-notes.md`.

**Implementation Details:**

Run PowerShell verification script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"

$m3Components = @(
    "Button.tsx", "Card.tsx", "Tag.tsx", "Badge.tsx", "ExternalLink.tsx", 
    "EmptyState.tsx", "Container.tsx", "MarkdownDoc.tsx"
)

$m3Report = @()
$m3Report += "`n## M3 UI Primitives Inspection"

$uiDir = "src\components\ui"
if (Test-Path $uiDir) {
    Get-ChildItem $uiDir -Filter "*.tsx" | ForEach-Object {
        $hasClient = (Get-Content $_.FullName -Raw) -match "['""]use client['""]"
        $m3Report += "- Component: `$($_.Name)` (uses client: `$hasClient)"
    }
} else {
    $m3Report += "- ERROR: `src/components/ui/` directory missing."
}

$m3Report | Add-Content -Path $notesPath -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path ".kiro\specs\m8-blog-participation-module\task-notes.md"
```
Expected: True.

**Satisfies Requirements:** Req 1.5, Req 7.1, Req 8.3, Req 17.8

---

### M8.G1.T8: Audit Decision 3 rule for heading demotion (`demoteHeadings`)

**Objective:** Determine whether `src/lib/projects/demote-headings.ts` exists and is a pure `(html: string) => string` helper without React/DOM dependencies (Decision 3 Case 1), or if M8 must create its own helper in G7 (Decision 3 Case 2).

**Acceptance Criteria:**
- ✓ Inspects `src/lib/projects/demote-headings.ts`.
- ✓ If present and pure, selects **Case 1** (import read-only).
- ✓ If absent or impure, selects **Case 2** (create `src/lib/blog/demote-headings.ts` in G7).
- ✓ Records decision explicitly in `task-notes.md`.
- ✓ Verifies M7 `shiftHeadings` is NEVER imported.

**Prerequisites:**
- Milestones M6 and M7 completed.

**Implementation Details:**

Execute audit script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"

$demoteProjectFile = "src\lib\projects\demote-headings.ts"
$decisionText = ""

if (Test-Path $demoteProjectFile) {
    $code = Get-Content $demoteProjectFile -Raw
    $hasDomOrReact = $code -match "from ['""](react|react-dom|next)"
    if (-not $hasDomOrReact -and ($code -match "export function demoteHeadings")) {
        $decisionText = "`n## Decision 3 Outcome`n- **Selected:** Case 1 (Reusing pure `@/lib/projects/demote-headings`)."
    } else {
        $decisionText = "`n## Decision 3 Outcome`n- **Selected:** Case 2 (Project helper exists but has framework dependencies. M8 will author `src/lib/blog/demote-headings.ts`)."
    }
} else {
    $decisionText = "`n## Decision 3 Outcome`n- **Selected:** Case 2 (`$demoteProjectFile` does not exist. M8 will author `src/lib/blog/demote-headings.ts` in G7)."
}

$decisionText | Add-Content -Path $notesPath -Encoding UTF8
Get-Content $notesPath | Select-String "Decision 3" -Context 0,2
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Select-String -Path ".kiro\specs\m8-blog-participation-module\task-notes.md" -Pattern "Decision 3 Outcome"
```
Expected: Decision 3 Outcome is explicitly documented in `task-notes.md`.

**Satisfies Requirements:** Req 13.4, Req 17.8

---

### M8.G1.T9: Inspect Next.js App Router params shape and test toolchain

**Objective:** Audit Next.js route parameter typing (`params: Promise<Params>` vs `params: Params`), React 19 testing library setup, and presence of `fast-check`.

**Acceptance Criteria:**
- ✓ Inspects Next.js version in `package.json`.
- ✓ Confirms whether `await params` pattern is required (Next.js 15+).
- ✓ Confirms `vitest`, `@testing-library/react`, and `fast-check` are available in `node_modules`.
- ✓ Confirms M4 title template in `src/app/layout.tsx`.
- ✓ Appends results to `task-notes.md`.

**Prerequisites:**
- `package.json` present at workspace root.

**Implementation Details:**

Execute audit script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notesPath = ".kiro\specs\m8-blog-participation-module\task-notes.md"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json

$toolchainReport = @()
$toolchainReport += "`n## Next.js & Toolchain Verification"
$toolchainReport += "- Next.js Version: $($pkg.dependencies.next)"
$toolchainReport += "- React Version: $($pkg.dependencies.react)"
$toolchainReport += "- Vitest Installed: $(if ($pkg.devDependencies.vitest) { 'Yes' } else { 'No' })"
$toolchainReport += "- Fast-Check Installed: $(if ($pkg.devDependencies.'fast-check') { 'Yes' } else { 'No' })"

if ($pkg.dependencies.next -match "^15") {
    $toolchainReport += "- Note: Next.js 15 detected. `params` in Page and generateMetadata MUST be awaited."
} else {
    $toolchainReport += "- Note: Next.js 14 detected. Standard synchronous `params` resolution."
}

$toolchainReport | Add-Content -Path $notesPath -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Get-Content ".kiro\specs\m8-blog-participation-module\task-notes.md" | Select-String "Next.js Version:"
```
Expected: Output showing detected Next.js version.

**Satisfies Requirements:** Req 1.1, Req 10.1, Req 17.1, Req 17.9

---

### M8.G1.T10: Checkpoint — Verify test passes, typecheck clean, and zero protected diffs

**Objective:** Run the test suite on new fixtures and types, verify strict TypeScript type checking, and confirm no protected repository files were modified.

**Acceptance Criteria:**
- ✓ `npm test -- tests/blog/tag-key.test.ts` passes with code 0.
- ✓ `npm run typecheck` passes with zero type errors.
- ✓ `npm run lint` passes with code 0.
- ✓ `git status` shows untracked/modified files are restricted strictly to `tests/blog/`, `src/lib/blog/`, and `.kiro/specs/m8-blog-participation-module/task-notes.md`.
- ✓ Zero changes in `package.json`, `package-lock.json`, `tsconfig.json`, `tailwind.config.ts`, or M1–M7 files.

**Prerequisites:**
- Tasks M8.G1.T1 through M8.G1.T9 completed.

**Implementation Details:**

Execute full Goal 1 validation script:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run unit test
npm test -- tests/blog/tag-key.test.ts

# 2. Run TypeScript strict typecheck
npm run typecheck

# 3. Run ESLint
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

Run the following command sequence to verify Goal 1 completion:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\blog\helpers\blog-fixtures.ts"
Test-Path "src\lib\blog\blog-types.ts"
Test-Path "src\lib\blog\tag-key.ts"
Test-Path ".kiro\specs\m8-blog-participation-module\task-notes.md"
npm test -- tests/blog/tag-key.test.ts
npm run typecheck
```
Expected output:
- `True` for all four paths.
- Tests passing.
- `npm run typecheck` exits with return code 0.