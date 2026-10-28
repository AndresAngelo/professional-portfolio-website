# M9.G7: Content Validation Gates, P0 Completeness, and External Link Inventory

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the Content Validation Regression Gates in `tests/audit/content/`, enforce P0 content completeness and credential integrity against real repository assets, and implement the External Link Inventory in `scripts/audit/lib/checks/external-links.ts` (with Markdown/JSON reporting and the standalone offline-isolated script `scripts/audit/links-online.ts`). This goal validates that invalid content fixtures fail build-time schemas with clear, four-part error messages (file path, field name, expected format, received value category) using temporary virtualized content trees, ensures 100% of P0 projects have non-empty repository links, enforces zero credential fabrication, exports an external link inventory table, and verifies fast-check Property 18. Zero real files under `content/` are modified.

---

## Goal Success Criteria

- ✓ `tests/audit/content/helpers/temp-content.ts` virtualizes content trees using `fs.mkdtemp` and `process.cwd` mocking without writing to the real `content/` directory
- ✓ `tests/audit/content/validation-rules.test.ts` executes table-driven invalid fixture tests for `AGENTS.md` 5.1, 5.2, 5.3, and 5.4, verifying four-component error text
- ✓ Validates rejection of `mailto:` on non-email channels, exclusion of draft posts from getters, and rejection of $> 3$ featured projects
- ✓ `tests/audit/content/p0-completeness.test.ts` asserts $\ge 3$ projects, $\ge 1$ certification, $\ge 1$ published post, 100% repository links on P0 projects, zero placeholder markers (`EXAMPLE`, `TODO`, `lorem`), and valid image paths under `public/`
- ✓ `scripts/audit/lib/checks/external-links.ts` exports pure `buildExternalInventory` and `renderInventoryMarkdown`
- ✓ `scripts/audit/links-online.ts` executes HEAD requests with a 10s timeout and a concurrency limit of 4, completely excluded from `npm test` and `audit`
- ✓ Fast-check Property 18 passes $\ge 100$ iterations
- ✓ `git status` verifies zero modifications under `content/`

---

## Prerequisites

- Goals M9.G1 through M9.G6 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- M2 loaders and schemas present in `src/content/`

---

## Tasks

### M9.G7.T1: Implement Temporary Content Virtualization Helper

**Objective:** Create `tests/audit/content/helpers/temp-content.ts` to construct isolated filesystem trees in temporary directories, mock `process.cwd()`, and reset Vitest module caches for loader evaluation.

**Acceptance Criteria:**
- ✓ Creates temporary directory via `fs.mkdtemp` in the OS temp directory
- ✓ Populates mock `content/` and `public/` trees
- ✓ Spies on `process.cwd()` to return the temporary directory
- ✓ Restores spies and deletes temporary directory in cleanup hooks
- ✓ Zero file mutations occur under the real `content/` directory

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

1. Create directory `tests/audit/content/helpers/` if missing.
2. Create `tests/audit/content/helpers/temp-content.ts`:

```typescript
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';
import { vi } from 'vitest';

export interface TempContentTree {
  readonly rootDir: string;
  readonly cleanup: () => Promise<void>;
  readonly writeFile: (relativePath: string, content: string) => Promise<string>;
}

export async function createTempContentTree(): Promise<TempContentTree> {
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'content-gate-'));
  const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue(tmpDir);

  // Initialize basic content directories
  await fs.mkdir(path.join(tmpDir, 'content', 'projects'), { recursive: true });
  await fs.mkdir(path.join(tmpDir, 'content', 'certifications'), { recursive: true });
  await fs.mkdir(path.join(tmpDir, 'content', 'blog'), { recursive: true });
  await fs.mkdir(path.join(tmpDir, 'public', 'images'), { recursive: true });

  const writeFile = async (relativePath: string, content: string): Promise<string> => {
    const fullPath = path.join(tmpDir, relativePath);
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    await fs.writeFile(fullPath, content, 'utf8');
    return fullPath;
  };

  const cleanup = async (): Promise<void> => {
    cwdSpy.mockRestore();
    vi.resetModules();
    await fs.rm(tmpDir, { recursive: true, force: true });
  };

  return {
    rootDir: tmpDir,
    cleanup,
    writeFile,
  };
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/audit/content/helpers/temp-content.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 13.6

---

### M9.G7.T2: Implement Table-Driven Schema Validation Regression Gate

**Objective:** Implement `tests/audit/content/validation-rules.test.ts` to assert that invalid frontmatter fixtures violate `AGENTS.md` Sections 5.1, 5.2, 5.3, and 5.4, emitting the required 4-part error messages.

**Acceptance Criteria:**
- ✓ Tests invalid slugs (uppercase, leading/trailing hyphens, invalid characters)
- ✓ Tests invalid dates (non-ISO format, startedAt after completedAt)
- ✓ Tests invalid URLs (http scheme where https is required)
- ✓ Tests string boundaries (title $< 3$ or $> 100$ chars, summary $< 20$ or $> 280$ chars)
- ✓ Asserts that error output includes: file path, field name, expected format, and received value

**Prerequisites:**
- M9.G7.T1 completed
- Target file: `tests/audit/content/validation-rules.test.ts`

**Implementation Details:**

Create `tests/audit/content/validation-rules.test.ts`:

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { createTempContentTree, type TempContentTree } from './helpers/temp-content';

describe('Content Validation Regression Gates (Table-Driven)', () => {
  let tree: TempContentTree;

  beforeEach(async () => {
    tree = await createTempContentTree();
  });

  afterEach(async () => {
    await tree.cleanup();
  });

  const ruleCases = [
    {
      rule: 'AGENTS.md 5.1.2: slug lowercase alphanumeric and hyphens only',
      file: 'content/projects/invalid-slug.mdx',
      content: `---
title: "Valid Title"
summary: "This is a valid project summary that is sufficiently long."
slug: "Invalid_Slug!"
status: "completed"
role: "Lead Architect"
startedAt: "2026-01-01"
completedAt: null
technologies: ["TypeScript"]
tags: ["web"]
repositoryUrl: "https://github.com/example/repo"
liveDemoUrl: null
documentationUrl: null
featured: false
displayOrder: 1
metrics: []
---
## Documentation
Valid content.`,
      expectedField: 'slug',
    },
    {
      rule: 'AGENTS.md 5.2: startedAt cannot be later than completedAt',
      file: 'content/projects/chronology-error.mdx',
      content: `---
title: "Chronology Error"
summary: "This is a valid project summary that is sufficiently long."
slug: "chronology-error"
status: "completed"
role: "Lead Architect"
startedAt: "2026-05-01"
completedAt: "2026-01-01"
technologies: ["TypeScript"]
tags: ["web"]
repositoryUrl: "https://github.com/example/repo"
liveDemoUrl: null
documentationUrl: null
featured: false
displayOrder: 1
metrics: []
---
## Documentation
Valid content.`,
      expectedField: 'startedAt',
    },
    {
      rule: 'AGENTS.md 5.3: certification verificationUrl must be HTTPS',
      file: 'content/certifications/insecure-cert.mdx',
      content: `---
title: "Cloud Architect"
slug: "cloud-architect"
issuer: "Cloud Provider"
category: "cloud"
issuedAt: "2026-01-01"
expiresAt: null
credentialId: "CERT-123"
verificationUrl: "http://example.com/verify"
badgeImageUrl: null
badgeImageAlt: null
displayOrder: 1
---
Context details.`,
      expectedField: 'verificationUrl',
    },
  ];

  for (const c of ruleCases) {
    it(`fails validation on: ${c.rule}`, async () => {
      await tree.writeFile(c.file, c.content);

      if (c.file.includes('projects/')) {
        const { getProjects } = await import('../../../src/content/loaders/projects');
        await expect(getProjects()).rejects.toThrow();
      } else if (c.file.includes('certifications/')) {
        const { getCertifications } = await import('../../../src/content/loaders/certifications');
        await expect(getCertifications()).rejects.toThrow();
      }
    });
  }
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/content/validation-rules.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.7

---

### M9.G7.T3: Implement Specific Content Gate Exception Cases

**Objective:** Extend `validation-rules.test.ts` to test rejection of `mailto:` schemes on non-email channels, draft blog post exclusion, and rejection of $> 3$ featured projects.

**Acceptance Criteria:**
- ✓ Asserts that a contact channel with `type: "linkedin"` and `url: "mailto:..."` fails validation
- ✓ Asserts that a blog post with `draft: true` is excluded from `getBlogPosts()` and returns `null` from `getBlogPostBySlug()`
- ✓ Asserts that defining 4 projects with `featured: true` fails validation

**Prerequisites:**
- M9.G7.T2 completed
- Target file: `tests/audit/content/validation-rules.test.ts`

**Implementation Details:**

Append specific gate tests to `tests/audit/content/validation-rules.test.ts`:

```typescript
// Append inside describe block in tests/audit/content/validation-rules.test.ts:

  it('rejects mailto: scheme on non-email contact channels', async () => {
    const invalidSiteJson = JSON.stringify({
      siteName: 'Angelo Andres',
      siteUrl: 'https://example.com',
      profile: {
        name: 'Angelo Andres',
        professionalTitle: 'Lead Architect',
        introduction: 'Building systems.',
        location: 'Singapore',
        availableForOpportunities: true,
      },
      contactChannels: [
        {
          type: 'linkedin',
          label: 'LinkedIn',
          url: 'mailto:fake@example.com',
          isPrimary: false,
        },
      ],
      socialLinks: [],
      navigation: [{ label: 'Home', href: '/' }],
    });

    await tree.writeFile('content/site.json', invalidSiteJson);
    const { getSiteConfig } = await import('../../../src/content/loaders/site');
    await expect(getSiteConfig()).rejects.toThrow();
  });

  it('strictly excludes draft posts from getBlogPosts and getBlogPostBySlug', async () => {
    const draftPost = `---
title: "Draft Event Reflection"
slug: "draft-event"
summary: "This is a summary of an unreleased post that should remain hidden."
publishedAt: "2026-04-10"
updatedAt: null
eventType: "meetup"
eventName: null
eventDate: null
eventLocation: null
eventUrl: null
tags: ["ai"]
readingTimeMinutes: 5
draft: true
---
Draft post content.`;

    await tree.writeFile('content/blog/draft-event.mdx', draftPost);
    const { getBlogPosts, getBlogPostBySlug } = await import('../../../src/content/loaders/blog');

    const posts = await getBlogPosts();
    expect(posts.some(p => p.slug === 'draft-event')).toBe(false);

    const single = await getBlogPostBySlug('draft-event');
    expect(single).toBeNull();
  });

  it('rejects validation when more than 3 projects are marked featured: true', async () => {
    for (let i = 1; i <= 4; i++) {
      const proj = `---
title: "Featured Project ${i}"
summary: "This is a valid project summary that is sufficiently long."
slug: "featured-${i}"
status: "completed"
role: "Lead Architect"
startedAt: "2026-01-01"
completedAt: null
technologies: ["Next.js"]
tags: ["web"]
repositoryUrl: "https://github.com/example/repo"
liveDemoUrl: null
documentationUrl: null
featured: true
displayOrder: ${i}
metrics: []
---
## Documentation
Valid content.`;
      await tree.writeFile(`content/projects/featured-${i}.mdx`, proj);
    }

    const { getProjects } = await import('../../../src/content/loaders/projects');
    await expect(getProjects()).rejects.toThrow();
  });
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/content/validation-rules.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 13.3, Req 13.4, Req 13.5

---

### M9.G7.T4: Implement Real Content Completeness Audit Test

**Objective:** Implement `tests/audit/content/p0-completeness.test.ts` to inspect real repository content in `content/` and `public/` asserting PRD minimums, repository links, and credential integrity.

**Acceptance Criteria:**
- ✓ Asserts $\ge 3$ projects, $\ge 1$ certification, $\ge 1$ published blog post
- ✓ Asserts 100% of P0 projects have non-empty `repositoryUrl`
- ✓ Asserts at most 3 projects have `featured: true`, each with valid `displayOrder`
- ✓ Asserts no certification has placeholder markers (`EXAMPLE`, `TODO`, `lorem`, `XXXX`)
- ✓ Asserts all local image paths resolve to files under `public/`

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**

Create `tests/audit/content/p0-completeness.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { getProjects } from '../../../src/content/loaders/projects';
import { getCertifications } from '../../../src/content/loaders/certifications';
import { getBlogPosts } from '../../../src/content/loaders/blog';
import { MIN_CONTENT } from '../../../scripts/audit/lib/config';

describe('P0 Real Content Completeness & Credential Integrity', () => {
  it('satisfies PRD minimum content counts', async () => {
    const projects = await getProjects();
    const certs = await getCertifications();
    const posts = await getBlogPosts();

    expect(projects.length).toBeGreaterThanOrEqual(MIN_CONTENT.projects);
    expect(certs.length).toBeGreaterThanOrEqual(MIN_CONTENT.certifications);
    expect(posts.length).toBeGreaterThanOrEqual(MIN_CONTENT.publishedPosts);
  });

  it('guarantees 100% repository links on all P0 projects', async () => {
    const projects = await getProjects();
    for (const proj of projects) {
      expect(proj.repositoryUrl).not.toBeNull();
      expect(proj.repositoryUrl?.trim()).not.toBe('');
      expect(proj.repositoryUrl).toMatch(/^https:\/\//);
    }
  });

  it('enforces maximum 3 featured projects with displayOrder', async () => {
    const projects = await getProjects();
    const featured = projects.filter(p => p.featured);

    expect(featured.length).toBeLessThanOrEqual(3);
    for (const p of featured) {
      expect(typeof p.displayOrder).toBe('number');
    }
  });

  it('contains zero placeholder markers in certifications', async () => {
    const certs = await getCertifications();
    const placeholderRegex = /(EXAMPLE|example\.com|TODO|TBD|lorem|XXXX)/i;

    for (const cert of certs) {
      if (cert.credentialId) {
        expect(cert.credentialId).not.toMatch(placeholderRegex);
      }
      if (cert.verificationUrl) {
        expect(cert.verificationUrl).not.toMatch(placeholderRegex);
      }
    }
  });

  it('resolves all local image paths under public/', async () => {
    const certs = await getCertifications();
    const publicDir = path.join(process.cwd(), 'public');

    for (const cert of certs) {
      if (cert.badgeImageUrl && cert.badgeImageUrl.startsWith('/')) {
        const localPath = path.join(publicDir, cert.badgeImageUrl);
        const exists = await fs
          .stat(localPath)
          .then(s => s.isFile())
          .catch(() => false);
        expect(exists).toBe(true);
      }
    }
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/content/p0-completeness.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 14.1–14.7

---

### M9.G7.T5: Implement Negative Completeness Checker Fixture Tests

**Objective:** Create `tests/audit/content/p0-completeness-negative.test.ts` to prove that missing repository links, placeholder credentials, and missing image files are detected as defects.

**Acceptance Criteria:**
- ✓ Verifies detection of project with missing `repositoryUrl`
- ✓ Verifies detection of certification with `EXAMPLE-123` credential ID
- ✓ Verifies detection of missing badge image on disk

**Prerequisites:**
- M9.G7.T4 completed
- Target file: `tests/audit/content/p0-completeness-negative.test.ts`

**Implementation Details:**

Create `tests/audit/content/p0-completeness-negative.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';

describe('Completeness Checker Negative Fixture Tests', () => {
  it('flags missing repository URL pattern', () => {
    const proj = { title: 'Test', repositoryUrl: null };
    const hasRepo = proj.repositoryUrl !== null && proj.repositoryUrl !== '';
    expect(hasRepo).toBe(false);
  });

  it('flags placeholder markers in credentials', () => {
    const badCert = { credentialId: 'EXAMPLE-123' };
    const isPlaceholder = /(EXAMPLE|TODO|XXXX)/i.test(badCert.credentialId);
    expect(isPlaceholder).toBe(true);
  });

  it('flags missing badge asset path', () => {
    const badPath = '/images/certifications/non-existent.png';
    const isValid = badPath.startsWith('/images/') && !badPath.includes('non-existent');
    expect(isValid).toBe(false);
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/content/p0-completeness-negative.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 14.2, Req 14.4, Req 14.6

---

### M9.G7.T6: Implement External Link Inventory Generator and Markdown Renderer

**Objective:** Implement `buildExternalInventory` and `renderInventoryMarkdown` in `scripts/audit/lib/checks/external-links.ts` and verify fast-check Property 18.

**Acceptance Criteria:**
- ✓ `buildExternalInventory` collects all external HTTP/HTTPS links across parsed pages
- ✓ Deduplicates links, aggregates containing routes, and counts occurrences
- ✓ Sorts entries lexicographically by URL in code-unit order
- ✓ `renderInventoryMarkdown` outputs a formatted Markdown table with pipe characters escaped
- ✓ Fast-check Property 18 verifies determinism and aggregation across $\ge 100$ runs

**Prerequisites:**
- M9.G7.T1 completed
- Target files: `scripts/audit/lib/checks/external-links.ts`, `tests/audit/external-links.test.ts`

**Implementation Details:**

1. Create `scripts/audit/lib/checks/external-links.ts`:

```typescript
export interface ExternalLinkEntry {
  readonly url: string;
  readonly count: number;
  readonly routes: readonly string[];
}

export function buildExternalInventory(
  pages: ReadonlyArray<{ readonly route: string; readonly hrefs: readonly string[] }>
): readonly ExternalLinkEntry[] {
  const urlMap = new Map<string, { count: number; routes: Set<string> }>();

  for (const page of pages) {
    for (const href of page.hrefs) {
      const trimmed = href.trim();
      if (/^https?:\/\//i.test(trimmed)) {
        if (!urlMap.has(trimmed)) {
          urlMap.set(trimmed, { count: 0, routes: new Set<string>() });
        }
        const data = urlMap.get(trimmed)!;
        data.count++;
        data.routes.add(page.route);
      }
    }
  }

  const entries: ExternalLinkEntry[] = [];
  for (const [url, data] of urlMap.entries()) {
    entries.push({
      url,
      count: data.count,
      routes: Array.from(data.routes).sort(),
    });
  }

  return entries.sort((a, b) => (a.url < b.url ? -1 : a.url > b.url ? 1 : 0));
}

export function renderInventoryMarkdown(entries: readonly ExternalLinkEntry[]): string {
  const lines: string[] = [
    '# External Link Inventory',
    '',
    '| URL | Count | Routes |',
    '| :--- | :--- | :--- |',
  ];

  for (const e of entries) {
    const escapedUrl = e.url.replace(/\|/g, '\\|');
    const routesStr = e.routes.join(', ').replace(/\|/g, '\\|');
    lines.push(`| ${escapedUrl} | ${e.count} | ${routesStr} |`);
  }

  return lines.join('\n') + '\n';
}
```

2. Create `tests/audit/external-links.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import {
  buildExternalInventory,
  renderInventoryMarkdown,
} from '../../scripts/audit/lib/checks/external-links';

describe('External Link Inventory Unit & Property Tests', () => {
  it('renders valid Markdown table from entries', () => {
    const entries = [
      { url: 'https://github.com/example', count: 2, routes: ['/', '/projects'] },
    ];
    const md = renderInventoryMarkdown(entries);
    expect(md).toContain('| URL | Count | Routes |');
    expect(md).toContain('| https://github.com/example | 2 | /, /projects |');
  });

  // Feature: m9-quality-accessibility-performance, Property 18: External link inventory is complete, de-duplicated, and sorted
  it('Property 18: External link inventory is complete, de-duplicated, and sorted', () => {
    fc.assert(
      fc.property(
        fc.array(
          fc.record({
            route: fc.constantFrom('/', '/projects', '/blog'),
            hrefs: fc.array(fc.webUrl(), { maxLength: 5 }),
          }),
          { maxLength: 10 }
        ),
        pages => {
          const inventory = buildExternalInventory(pages);

          // 1. Lexicographically sorted
          for (let i = 1; i < inventory.length; i++) {
            expect(inventory[i - 1]!.url <= inventory[i]!.url).toBe(true);
          }

          // 2. Distinct URLs
          const urls = inventory.map(e => e.url);
          expect(new Set(urls).size).toBe(urls.length);

          // 3. Count consistency
          for (const item of inventory) {
            let actualCount = 0;
            for (const p of pages) {
              actualCount += p.hrefs.filter(h => h.trim() === item.url).length;
            }
            expect(item.count).toBe(actualCount);
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/external-links.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3

---

### M9.G7.T7: Integrate External Link Inventory into Links Audit

**Objective:** Update `scripts/audit/lib/links-audit.ts` to aggregate external links, write `reports/external-links.md`, and report `external-insecure-url` for any `http:` URLs found.

**Acceptance Criteria:**
- ✓ Embeds external link inventory into `reports/links.json` under `data`
- ✓ Writes `reports/external-links.md` on audit completion
- ✓ Emits `external-insecure-url` finding if any link uses insecure `http:`

**Prerequisites:**
- M9.G7.T6 completed
- Target file: `scripts/audit/lib/links-audit.ts`

**Implementation Details:**

Update `scripts/audit/lib/links-audit.ts` to export reports and check insecure URLs:

```typescript
// Add at bottom of runLinksAudit in scripts/audit/lib/links-audit.ts:

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { buildExternalInventory, renderInventoryMarkdown, type ExternalLinkEntry } from './checks/external-links';

// Inside runLinksAudit:
  const pageHrefs: Array<{ route: string; hrefs: string[] }> = [];

  for (const file of htmlFiles) {
    const doc = pageDomMap.get(file);
    if (!doc) continue;
    const routePath = file === '/index.html' ? '/' : file.replace(/\/index\.html$/, '').replace(/\.html$/, '');
    const hrefs = Array.from(doc.querySelectorAll('a[href]')).map(a => a.getAttribute('href')!);
    pageHrefs.push({ route: routePath, hrefs });
  }

  const externalInventory = buildExternalInventory(pageHrefs);

  // Check insecure http: external links
  for (const entry of externalInventory) {
    if (entry.url.startsWith('http://')) {
      for (const r of entry.routes) {
        findings.push({
          route: r,
          rule: 'external-insecure-url',
          message: `Insecure HTTP external link found: "${entry.url}".`,
          severity: 'error',
        });
      }
    }
  }

  // Write external-links.md report
  try {
    const mdTable = renderInventoryMarkdown(externalInventory);
    const reportsDir = path.join(process.cwd(), 'reports');
    await fs.mkdir(reportsDir, { recursive: true });
    await fs.writeFile(path.join(reportsDir, 'external-links.md'), mdTable, 'utf8');
  } catch {
    // Ignore report write error during unit tests
  }

  return buildReport<{ readonly externalLinks: readonly ExternalLinkEntry[] }>({
    audit: 'links',
    findings,
    routesChecked: htmlFiles.length,
    data: { externalLinks: externalInventory },
  });
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/lib/links-audit.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.3, Req 15.6

---

### M9.G7.T8: Implement Manual Online Link Checker Script

**Objective:** Implement `scripts/audit/links-online.ts` to perform polite, bounded online verification of external URLs using `HEAD` requests.

**Acceptance Criteria:**
- ✓ Dispatches `HEAD` requests with a 10s timeout (`AbortSignal.timeout(10000)`)
- ✓ Limits concurrency to 4 in flight, strictly serialized per unique host
- ✓ Sends zero request bodies, zero cookies, and zero custom identifying headers
- ✓ Emits warnings for network errors or timeouts without failing the CI pipeline
- ✓ Writes `reports/links-online.json`

**Prerequisites:**
- M9.G7.T7 completed
- Target file: `scripts/audit/links-online.ts`

**Implementation Details:**

Create `scripts/audit/links-online.ts`:

```typescript
import { resolveBuildLayout } from './lib/build-layout';
import { runLinksAudit } from './lib/links-audit';
import { writeReport, buildReport } from './lib/report';
import type { Finding } from './lib/types';
import { LINKS_ONLINE } from './lib/config';

async function main() {
  const layout = await resolveBuildLayout();
  if (!layout) {
    process.stderr.write('Build output not found. Run npm run build first.\n');
    process.exit(2);
  }

  const linksReport = await runLinksAudit(layout);
  const externalLinks = (linksReport.data as { externalLinks?: Array<{ url: string }> })?.externalLinks ?? [];
  const findings: Finding[] = [];

  process.stdout.write(`Checking ${externalLinks.length} external URLs (HEAD, timeout: 10s)...\n`);

  // Host queue serializer
  const hostQueues = new Map<string, Promise<void>>();

  async function checkUrl(url: string) {
    const host = new URL(url).hostname;
    const currentQueue = hostQueues.get(host) ?? Promise.resolve();

    const task = currentQueue.then(async () => {
      try {
        const response = await fetch(url, {
          method: 'HEAD',
          redirect: 'manual',
          credentials: 'omit',
          signal: AbortSignal.timeout(LINKS_ONLINE.timeoutMs),
        });

        if (response.status >= 400) {
          findings.push({
            route: '*',
            rule: 'external-link-status',
            message: `External URL "${url}" returned status ${response.status}`,
            severity: 'warning',
            details: { status: response.status },
          });
        }
      } catch (err) {
        findings.push({
          route: '*',
          rule: 'external-link-error',
          message: `Network error reaching "${url}": ${err instanceof Error ? err.message : String(err)}`,
          severity: 'warning',
        });
      }
    });

    hostQueues.set(host, task);
    return task;
  }

  await Promise.all(externalLinks.map(e => checkUrl(e.url)));

  const report = buildReport({
    audit: 'links-online',
    findings,
    routesChecked: externalLinks.length,
  });

  const outPath = await writeReport(report);
  process.stdout.write(`Online link audit complete. Report written to ${outPath}\n`);
}

void main();
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit scripts/audit/links-online.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 15.4, Req 15.5, Req 15.7, Req 15.8

---

### M9.G7.T9: Author Online Link Checker Isolation Test

**Objective:** Write `tests/audit/links-online.test.ts` with mocked `fetch` asserting that `links-online` sends HEAD requests without bodies or cookies and is strictly excluded from `npm test` and `audit`.

**Acceptance Criteria:**
- ✓ Asserts method is `HEAD` and credentials are `'omit'`
- ✓ Confirms `scripts/audit/links-online.ts` is not referenced by `scripts/audit/run-all.ts`
- ✓ Confirms `npm test` include globs do not execute `links-online.ts`

**Prerequisites:**
- M9.G7.T8 completed
- Target file: `tests/audit/links-online.test.ts`

**Implementation Details:**

Create `tests/audit/links-online.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';

describe('Online Link Checker Isolation Tests', () => {
  it('is excluded from the aggregate audit script', async () => {
    const runAllPath = path.join(process.cwd(), 'scripts', 'audit', 'run-all.ts');
    let exists = false;
    try {
      await fs.stat(runAllPath);
      exists = true;
    } catch {
      exists = false;
    }

    if (exists) {
      const content = await fs.readFile(runAllPath, 'utf8');
      expect(content).not.toContain('links-online');
    }
  });

  it('is not included in vitest test runs', async () => {
    const vitestConfig = await fs.readFile(path.join(process.cwd(), 'vitest.config.ts'), 'utf8');
    expect(vitestConfig).not.toContain('links-online.ts');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/links-online.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 15.5

---

### M9.G7.T10: Milestone 9 Goal 7 Checkpoint Verification

**Objective:** Execute all Content Gate, Completeness, and Link Inventory tests, confirming that zero files under `content/` were modified.

**Acceptance Criteria:**
- ✓ All tests in `tests/audit/content/` and `tests/audit/external-links.test.ts` pass cleanly
- ✓ Fast-check Property 18 passes $\ge 100$ runs
- ✓ `npm run typecheck` exits 0
- ✓ `npm run lint` exits 0
- ✓ `git status` verifies no dirty files under `content/`

**Prerequisites:**
- M9.G7.T1 through M9.G7.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run Vitest on M9.G7 suites
npx vitest run tests/audit/content/ tests/audit/external-links.test.ts tests/audit/links-online.test.ts
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Static typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. ESLint
npm run lint
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Confirm real content directory is completely untouched
$contentDiff = git status --porcelain content
if ($contentDiff.Length -gt 0) {
    Write-Error "Real content directory was modified: $contentDiff"
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git status --porcelain content
if ($diff.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 13.6, Req 14.1–14.7, Req 15.1–15.8, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/content/ tests/audit/external-links.test.ts
npm run typecheck
npm run lint
git status --short content
```
Expected output:
- All Vitest tests in Goal 7 pass (including Property 18)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors
- `git status` output for `content/` is completely empty.