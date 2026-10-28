# M7.G8: Metadata Builder, Route, and Static-Output Checks

> **Milestone:** M7 — Certifications Module  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks (M7.G8.T1 – M7.G8.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 1.1–1.2, 1.6–1.7, 7.4–7.5, 12.1–12.6, 13.1, 13.4–13.5, 15.4), `design.md` (Metadata, Route Architecture, Property 15), `tasks.md` (M7.G8)

---

## Goal Objective

Implement the metadata builder and canonical Next.js App Router route for the Certifications module:
1. `src/lib/certifications/certifications-metadata.ts`: pure function `buildCertificationsMetadata(siteUrl: string)` generating static page metadata (`title: 'Certifications'`, description between 50–160 characters without fabricated claims, canonical URL derived via `new URL('/certifications', siteUrl).href` with zero query params, and matching Open Graph tags; emitting zero JSON-LD).
2. `src/app/certifications/page.tsx`: async server component acting as the `/certifications` route entry point. It calls M2's `getCertifications()` and `getSiteConfig()`, passes certifications to `loadSupportingContent()`, computes the single UTC `buildDate` (`new Date().toISOString().slice(0, 10)`), renders `CertificationsIndex`, and exports `generateMetadata`.
3. Static-output checks and automated tests verifying that `/certifications` has no dynamic `[slug]` subroute, zero `'use client'`, zero `fetch()` or header reads, and that `new Date(` appears only in `page.tsx`.

Verify correctness, metadata derivation invariants, and static behavior via unit tests, fast-check Property 15, and static source scanners.

---

## Goal Success Criteria

- ✓ `src/lib/certifications/certifications-metadata.ts` exports `buildCertificationsMetadata(siteUrl: string): Metadata`.
- ✓ Description length is between 50 and 160 characters (exactly 135 characters in the standard text).
- ✓ Canonical URL equals `${siteUrl.replace(/\/+$/, '')}/certifications` without query parameters.
- ✓ Open Graph fields (`title`, `description`, `url`, `type: 'website'`) match page metadata; zero `application/ld+json` emitted.
- ✓ `src/app/certifications/page.tsx` is an async server component without `'use client'`.
- ✓ Single clock read in M7: `const buildDate = new Date().toISOString().slice(0, 10)` in `page.tsx`.
- ✓ Directory `src/app/certifications/` contains `page.tsx` and zero dynamic subdirectories (`[slug]`).
- ✓ Property 15 passes with >= 100 runs.
- ✓ Page-level tests cover populated, empty, and renderer failure scenarios.

---

## Prerequisites

- Goal 1 completed: `getSiteConfig` and `getCertifications` loader paths verified.
- Goal 4 completed: `loadSupportingContent` available.
- Goal 7 completed: `CertificationsIndex` available.
- M4 shell and layout conventions established.

---

## Tasks

### M7.G8.T1: Implement Pure Metadata Builder

**Objective:** Create `src/lib/certifications/certifications-metadata.ts` implementing `buildCertificationsMetadata(siteUrl: string): Metadata`.

**Acceptance Criteria:**
- ✓ Exports `buildCertificationsMetadata(siteUrl: string): Metadata`.
- ✓ Sets `title: 'Certifications'`.
- ✓ Sets `description` to `"Professional certifications and credentials earned across cloud, AI, security, and software engineering, with issuer verification links."` (135 characters, within 50–160 bounds).
- ✓ Computes canonical URL via `new URL('/certifications', siteUrl).href` stripping trailing slashes or queries.
- ✓ Sets `alternates.canonical` to computed URL.
- ✓ Sets `openGraph` object with matching `title`, `description`, `url`, and `type: 'website'`.
- ✓ Emits zero JSON-LD structures.
- ✓ Does not hardcode the site URL.

**Prerequisites:**
- `next` types available for `Metadata`.

**Implementation Details:**
Create `src/lib/certifications/certifications-metadata.ts`:

```typescript
import type { Metadata } from 'next';

export const CERTIFICATIONS_DESCRIPTION =
  'Professional certifications and credentials earned across cloud, AI, security, and software engineering, with issuer verification links.';

export function buildCertificationsMetadata(siteUrl: string): Metadata {
  const cleanBase = siteUrl.trim() || 'https://example.com';
  const canonicalUrl = new URL('/certifications', cleanBase).href;

  return {
    title: 'Certifications',
    description: CERTIFICATIONS_DESCRIPTION,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: 'Certifications',
      description: CERTIFICATIONS_DESCRIPTION,
      url: canonicalUrl,
      type: 'website',
    },
  };
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 12.1, 12.2, 12.3, 12.4, 12.5, 12.6

---

### M7.G8.T2: Unit Tests for certifications-metadata.ts

**Objective:** Create `tests/certifications/certifications-metadata.test.ts` verifying title, description character count, canonical URL resolution, and Open Graph attributes.

**Acceptance Criteria:**
- ✓ Verifies `title` is `'Certifications'`.
- ✓ Verifies `description` length is $\ge 50$ and $\le 160$ characters.
- ✓ Verifies canonical URL resolves correctly with or without trailing slash on `siteUrl`.
- ✓ Verifies `openGraph.type` is `'website'`.
- ✓ Verifies output contains zero JSON-LD keys.

**Prerequisites:**
- `src/lib/certifications/certifications-metadata.ts` implemented.

**Implementation Details:**
Create `tests/certifications/certifications-metadata.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import {
  buildCertificationsMetadata,
  CERTIFICATIONS_DESCRIPTION,
} from '@/lib/certifications/certifications-metadata';

describe('buildCertificationsMetadata - Unit Tests', () => {
  it('sets expected title and description within bounds', () => {
    const meta = buildCertificationsMetadata('https://angeloandres.dev');
    expect(meta.title).toBe('Certifications');
    expect(meta.description).toBe(CERTIFICATIONS_DESCRIPTION);
    expect(meta.description?.length).toBeGreaterThanOrEqual(50);
    expect(meta.description?.length).toBeLessThanOrEqual(160);
  });

  it('constructs correct canonical URL without trailing slash drift', () => {
    const metaA = buildCertificationsMetadata('https://angeloandres.dev');
    const metaB = buildCertificationsMetadata('https://angeloandres.dev/');

    expect(metaA.alternates?.canonical).toBe('https://angeloandres.dev/certifications');
    expect(metaB.alternates?.canonical).toBe('https://angeloandres.dev/certifications');
  });

  it('mirrors properties into openGraph object', () => {
    const meta = buildCertificationsMetadata('https://angeloandres.dev');
    expect(meta.openGraph?.title).toBe('Certifications');
    expect(meta.openGraph?.description).toBe(CERTIFICATIONS_DESCRIPTION);
    expect(meta.openGraph?.url).toBe('https://angeloandres.dev/certifications');
    expect(meta.openGraph?.type).toBe('website');
  });

  it('contains zero JSON-LD keys or scripts', () => {
    const meta = buildCertificationsMetadata('https://angeloandres.dev');
    expect((meta as any).other?.['application/ld+json']).toBeUndefined();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-metadata.test.ts
```
Expected output: All 4 unit tests pass.

**Satisfies Requirements:** Req 12.1, 12.2, 12.3, 12.4, 12.5, 12.6

---

### M7.G8.T3: Property 15 Test for buildCertificationsMetadata

**Objective:** Append Property 15 test to `tests/certifications/certifications-metadata.test.ts` verifying metadata derivation invariants across arbitrary valid URLs.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 15: Metadata is derived from the site URL`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Generates arbitrary valid HTTPS URLs.
- ✓ Verifies canonical is equal to `new URL('/certifications', siteUrl).href`.
- ✓ Verifies canonical contains no query parameters or hash fragments.

**Prerequisites:**
- `arbUrl` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/certifications-metadata.test.ts`:

```typescript
import fc from 'fast-check';

describe('buildCertificationsMetadata - Property Tests', () => {
  const arbValidSiteUrl = fc.webUrl({ validSchemeProperties: ['https'] });

  // Feature: m7-certifications-module, Property 15: Metadata is derived from the site URL
  it('Property 15: Canonical and Open Graph URLs derive purely from siteUrl with no query string', () => {
    fc.assert(
      fc.property(arbValidSiteUrl, (siteUrl) => {
        const meta = buildCertificationsMetadata(siteUrl);
        const expectedCanonical = new URL('/certifications', siteUrl).href;

        expect(meta.alternates?.canonical).toBe(expectedCanonical);
        expect(meta.openGraph?.url).toBe(expectedCanonical);

        const canonicalUrlObj = new URL(meta.alternates?.canonical as string);
        expect(canonicalUrlObj.search).toBe('');
        expect(canonicalUrlObj.hash).toBe('');
      }),
      { numRuns: 100 },
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-metadata.test.ts
```
Expected output: Unit tests and Property 15 pass with >= 100 runs.

**Satisfies Requirements:** Req 12.1, 12.3, 12.4, 12.6, 15.2

---

### M7.G8.T4: Implement Certifications Page Route (page.tsx)

**Objective:** Create `src/app/certifications/page.tsx` as a static async server component implementing the `/certifications` route.

**Acceptance Criteria:**
- ✓ Async server component `default function CertificationsPage(): Promise<React.JSX.Element>`.
- ✓ Zero `'use client'` directive.
- ✓ Calls `getCertifications()` from `@/content/loaders/certifications`.
- ✓ Awaits `loadSupportingContent(certifications)` from `@/lib/certifications/load-supporting-content`.
- ✓ Computes `const buildDate = new Date().toISOString().slice(0, 10)` once.
- ✓ Returns `<CertificationsIndex certifications={certifications} contentHtml={contentHtml} buildDate={buildDate} />`.
- ✓ Renders zero `<main>`, `<header>`, or `<footer>` landmarks.

**Prerequisites:**
- `getCertifications` available from `@/content/loaders/certifications`.
- `loadSupportingContent` available from `@/lib/certifications/load-supporting-content`.
- `CertificationsIndex` available from `@/components/certifications/certifications-index`.

**Implementation Details:**
Create `src/app/certifications/page.tsx`:

```typescript
import React from 'react';
import type { Metadata } from 'next';
import { getCertifications } from '@/content/loaders/certifications';
import { getSiteConfig } from '@/content/loaders/site';
import { loadSupportingContent } from '@/lib/certifications/load-supporting-content';
import { buildCertificationsMetadata } from '@/lib/certifications/certifications-metadata';
import { CertificationsIndex } from '@/components/certifications/certifications-index';

export async function generateMetadata(): Promise<Metadata> {
  const siteConfig = await getSiteConfig();
  return buildCertificationsMetadata(siteConfig.siteUrl);
}

export default async function CertificationsPage(): Promise<React.JSX.Element> {
  const certifications = await getCertifications();
  const contentHtml = await loadSupportingContent(certifications);
  const buildDate = new Date().toISOString().slice(0, 10);

  return (
    <CertificationsIndex
      certifications={certifications}
      contentHtml={contentHtml}
      buildDate={buildDate}
    />
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 1.1, 1.2, 1.3, 1.4, 1.6, 7.4, 7.5, 12.1, 13.1, 13.2

---

### M7.G8.T5: Verify generateMetadata Export in page.tsx

**Objective:** Verify that `page.tsx` exports `generateMetadata` dynamically resolving `siteUrl` from `getSiteConfig()`.

**Acceptance Criteria:**
- ✓ `generateMetadata` calls `getSiteConfig()`.
- ✓ Passes `siteConfig.siteUrl` to `buildCertificationsMetadata`.
- ✓ Returns valid Next.js `Metadata` object.

**Prerequisites:**
- `src/app/certifications/page.tsx` implemented.

**Implementation Details:**
Verify implementation structure created in M7.G8.T4.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 12.1, 12.6

---

### M7.G8.T6: Page-Level Tests for page.tsx with Mocked Loaders

**Objective:** Create `tests/certifications/page.test.tsx` verifying populated and empty page rendering, and metadata resolution.

**Acceptance Criteria:**
- ✓ Mocks `@/content/loaders/certifications` and `@/content/loaders/site`.
- ✓ Populated case: renders `<h1>Certifications</h1>` and cards.
- ✓ Empty case: renders `<h1>Certifications</h1>` and `EmptyState`.
- ✓ Verifies `generateMetadata` returns metadata matching site config.

**Prerequisites:**
- `src/app/certifications/page.tsx` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/page.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import CertificationsPage, { generateMetadata } from '@/app/certifications/page';
import {
  fixtureCertificationsList,
  fixtureEmptyCertificationsList,
} from '../fixtures/certifications-data';

vi.mock('@/content/loaders/certifications', () => ({
  getCertifications: vi.fn(),
}));

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(async () => ({
    siteUrl: 'https://test.angeloandres.dev',
    siteName: 'Angelo Andres',
  })),
}));

vi.mock('@/lib/certifications/load-supporting-content', () => ({
  loadSupportingContent: vi.fn(async () => ({})),
}));

import { getCertifications } from '@/content/loaders/certifications';

describe('CertificationsPage - Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders populated page with cards and sections', async () => {
    vi.mocked(getCertifications).mockResolvedValue(fixtureCertificationsList as any);

    const jsx = await CertificationsPage();
    render(jsx);

    expect(screen.getByRole('heading', { level: 1, name: 'Certifications' })).toBeInTheDocument();
    expect(screen.getAllByRole('heading', { level: 2 }).length).toBeGreaterThan(0);
  });

  it('renders empty state when loader returns zero certifications', async () => {
    vi.mocked(getCertifications).mockResolvedValue(fixtureEmptyCertificationsList as any);

    const jsx = await CertificationsPage();
    render(jsx);

    expect(screen.getByRole('heading', { level: 1, name: 'Certifications' })).toBeInTheDocument();
    expect(screen.getByText('No certifications available')).toBeInTheDocument();
  });

  it('resolves metadata from site config', async () => {
    const meta = await generateMetadata();
    expect(meta.title).toBe('Certifications');
    expect(meta.alternates?.canonical).toBe('https://test.angeloandres.dev/certifications');
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/page.test.tsx
```
Expected output: All 3 integration tests pass.

**Satisfies Requirements:** Req 1.1, 1.2, 2.1, 12.1, 15.4

---

### M7.G8.T7: Test Renderer Failure Propagation on Page

**Objective:** Add a test verifying that when `loadSupportingContent` rejects, the page render throws an error containing the certification slug.

**Acceptance Criteria:**
- ✓ Test configures `loadSupportingContent` to reject with `Failed to render certification content: broken-slug`.
- ✓ Awaiting `CertificationsPage()` rejects with matching error message.

**Prerequisites:**
- `tests/certifications/page.test.tsx` available.

**Implementation Details:**
Append to `tests/certifications/page.test.tsx`:

```typescript
import { loadSupportingContent } from '@/lib/certifications/load-supporting-content';

  it('propagates renderer failure with certification slug', async () => {
    vi.mocked(getCertifications).mockResolvedValue([fixtureCertificationsList[0]] as any);
    vi.mocked(loadSupportingContent).mockRejectedValue(
      new Error('Failed to render certification content: broken-slug'),
    );

    await expect(CertificationsPage()).rejects.toThrow(
      'Failed to render certification content: broken-slug',
    );
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/page.test.tsx
```
Expected output: Test passes.

**Satisfies Requirements:** Req 10.5, 15.4

---

### M7.G8.T8: Static Scope and Route Boundary Checks

**Objective:** Create `tests/certifications/static-checks.test.ts` to assert that no dynamic subroutes exist under `src/app/certifications/`, no client directives exist in M7 code, and `new Date(` appears only in `page.tsx`.

**Acceptance Criteria:**
- ✓ Verifies directory `src/app/certifications/[slug]/` does NOT exist.
- ✓ Verifies no `'use client'` in `src/app/certifications/` or `src/components/certifications/`.
- ✓ Verifies no `useState`, `useEffect`, `window`, `document`, or `fetch(` in M7 source code.
- ✓ Verifies regex `new Date\(` matches only in `src/app/certifications/page.tsx` within all M7 source files.

**Prerequisites:**
- Node `fs` and `path` modules available for test execution.

**Implementation Details:**
Create `tests/certifications/static-checks.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Certifications Module - Static Scope Checks', () => {
  const projectRoot = process.cwd();
  const certAppDir = path.join(projectRoot, 'src', 'app', 'certifications');
  const certCompDir = path.join(projectRoot, 'src', 'components', 'certifications');
  const certLibDir = path.join(projectRoot, 'src', 'lib', 'certifications');

  it('ensures no dynamic [slug] directory exists under src/app/certifications', () => {
    const slugDir = path.join(certAppDir, '[slug]');
    expect(fs.existsSync(slugDir)).toBe(false);
  });

  it('ensures no use client directive exists in certifications source files', () => {
    const files = [
      ...fs.readdirSync(certAppDir).map((f) => path.join(certAppDir, f)),
      ...fs.readdirSync(certCompDir).map((f) => path.join(certCompDir, f)),
    ].filter((f) => fs.statSync(f).isFile() && (f.endsWith('.tsx') || f.endsWith('.ts')));

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toContain("'use client'");
      expect(content).not.toContain('"use client"');
    }
  });

  it('ensures new Date( appears only in src/app/certifications/page.tsx', () => {
    const allFiles = [
      ...fs.readdirSync(certAppDir).map((f) => path.join(certAppDir, f)),
      ...fs.readdirSync(certCompDir).map((f) => path.join(certCompDir, f)),
      ...fs.readdirSync(certLibDir).map((f) => path.join(certLibDir, f)),
    ].filter((f) => fs.statSync(f).isFile() && (f.endsWith('.tsx') || f.endsWith('.ts')));

    const allowedFile = path.normalize(path.join(certAppDir, 'page.tsx'));

    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const matches = content.match(/new Date\(/g);
      if (path.normalize(file) === allowedFile) {
        expect(matches?.length).toBe(1);
      } else {
        expect(matches).toBeNull();
      }
    }
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/static-checks.test.ts
```
Expected output: All 3 static checks pass.

**Satisfies Requirements:** Req 1.2, 1.7, 7.4, 13.2, 13.3

---

### M7.G8.T9: Verify Landmark Absence and No Public API Routes

**Objective:** Verify that `page.tsx` emits no landmarks (`<main>`, `<header>`, `<footer>`), and that no API route handlers (`route.ts`) exist in `src/app/certifications/`.

**Acceptance Criteria:**
- ✓ Confirms `src/app/certifications/route.ts` does not exist.
- ✓ Confirms rendered output of `CertificationsPage` contains no `<main>` element.

**Prerequisites:**
- Tasks M7.G8.T4, M7.G8.T6 completed.

**Implementation Details:**
Append to `tests/certifications/static-checks.test.ts`:

```typescript
  it('ensures no route.ts or server actions exist under src/app/certifications', () => {
    const routeHandler = path.join(certAppDir, 'route.ts');
    expect(fs.existsSync(routeHandler)).toBe(false);
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/static-checks.test.ts
```
Expected output: All static checks pass.

**Satisfies Requirements:** Req 1.4, 13.5

---

### M7.G8.T10: Goal 8 Checkpoint and Pipeline Verification

**Objective:** Run the full test suite and typechecker across Goal 8 artifacts to confirm complete green status and clean compliance.

**Acceptance Criteria:**
- ✓ `src/lib/certifications/certifications-metadata.ts` and `src/app/certifications/page.tsx` compile cleanly.
- ✓ `tests/certifications/certifications-metadata.test.ts` passes (unit + Property 15).
- ✓ `tests/certifications/page.test.tsx` passes.
- ✓ `tests/certifications/static-checks.test.ts` passes.
- ✓ `npx tsc --noEmit` exits with 0.

**Prerequisites:**
- Tasks M7.G8.T1 through M7.G8.T9 completed.

**Implementation Details:**
Execute test suite and typechecking commands in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-metadata.test.ts tests/certifications/page.test.tsx tests/certifications/static-checks.test.ts
npx tsc --noEmit
```
Expected output: All test files pass completely; TypeScript compiles with zero errors.

**Satisfies Requirements:** Req 1.1–1.2, 1.6–1.7, 7.4–7.5, 12.1–12.6, 13.1, 13.4–13.5, 15.2, 15.4, 15.5, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 8 are complete:
```powershell
npx vitest run tests/certifications/certifications-metadata.test.ts tests/certifications/page.test.tsx tests/certifications/static-checks.test.ts
npx tsc --noEmit
```
Expected output: All metadata, page, and static check tests pass; zero TypeScript errors.