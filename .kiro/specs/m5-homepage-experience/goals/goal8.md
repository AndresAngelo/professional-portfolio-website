# M5.G8: HomeContent, Route, and Heading/Landmark Structure

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the composite server component `HomeContent` in `src/components/home/home-content.tsx` and the static homepage route entry point `src/app/page.tsx` with its exported `generateMetadata` function. `HomeContent` dynamically renders only the active section components resolved by `getVisibleSections(model)` in canonical `HOME_SECTION_ORDER` (`HeroSection` $\rightarrow$ `FeaturedProjects` $\rightarrow$ `SkillsSnapshot` $\rightarrow$ `CertificationsPreview` $\rightarrow$ `RecentActivity`) wrapped inside a React fragment, introducing zero redundant landmark elements. `src/app/page.tsx` executes as an async server component loading all four content collections concurrently via `Promise.all([getSiteConfig(), getProjects(), getCertifications(), getBlogPosts()])`, passing data to `buildHomeViewModel`, and rendering `HomeContent` without client directives, browser globals, cookies, headers, search parameters, or suppressive error boundaries (allowing schema errors to fail the static build). Validate landmark ownership, heading hierarchies (single `<h1>`, all section headers `<h2>`, zero skipped levels), and Properties 9 (render part) and 12 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/home/home-content.tsx` renders visible sections in strict `HOME_SECTION_ORDER` inside a React fragment with zero outer landmark wrappers
- ✓ `src/app/page.tsx` loads data using `getSiteConfig`, `getProjects`, `getCertifications`, and `getBlogPosts` via `Promise.all`
- ✓ `src/app/page.tsx` exports `generateMetadata` returning `buildHomeMetadata(await getSiteConfig())`
- ✓ Contains zero `'use client'`, `fetch(`, `window`, `document`, `headers()`, `cookies()`, or `searchParams` (Req 1.2, 1.6, 14.8)
- ✓ Renders exactly one `<h1>` (inside `HeroSection`); all section titles are `<h2>`; cards and items are `<h3>`; zero heading levels skipped (Req 14.1, 14.3)
- ✓ Renders zero `<header>`, `<footer>`, or `<main>` elements in page markup (M4 RootLayout owns these landmarks per Req 1.7)
- ✓ Missing required profile data causes loader rejection to bubble directly, failing the build without runtime fallbacks (Req 2.6)
- ✓ Unit and property tests in `tests/home/home-content.test.tsx` and `tests/home/page.test.tsx` satisfy Properties 9 (render part) and 12 ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1 through M5.G7 completed (all helpers, metadata builder, view model, and 5 section components available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- M2 loaders available in `src/content/loaders/`

---

## Tasks

### M5.G8.T1: Implement `HomeContent` Composition Component (`src/components/home/home-content.tsx`)

**Objective:** Author the server component `HomeContent` in `src/components/home/home-content.tsx` rendering visible sections strictly per `getVisibleSections(model)` in canonical order.

**Acceptance Criteria:**
- ✓ File `src/components/home/home-content.tsx` created
- ✓ Exports `HomeContentProps` interface requiring `model: HomeViewModel`
- ✓ Exports `HomeContent({ model }: HomeContentProps): JSX.Element`
- ✓ Calls `getVisibleSections(model)` to determine active sections
- ✓ Maps section IDs to corresponding components: `'hero'` $\rightarrow$ `HeroSection`, `'featured-projects'` $\rightarrow$ `FeaturedProjects`, `'skills'` $\rightarrow$ `SkillsSnapshot`, `'certifications'` $\rightarrow$ `CertificationsPreview`, `'recent-activity'` $\rightarrow$ `RecentActivity`
- ✓ Wraps sections in a React Fragment (`<>...</>`) without adding `<main>`, `<header>`, or `<footer>` landmarks
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- Goals M5.G4 through M5.G7 completed
- Target file: `src/components/home/home-content.tsx`

**Implementation Details:**

Write `src/components/home/home-content.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { HomeViewModel } from '@/lib/home/view-model';
import { getVisibleSections } from '@/lib/home/view-model';
import { HeroSection } from './hero-section';
import { FeaturedProjects } from './featured-projects';
import { SkillsSnapshot } from './skills-snapshot';
import { CertificationsPreview } from './certifications-preview';
import { RecentActivity } from './recent-activity';

export interface HomeContentProps {
  model: HomeViewModel;
}

/**
 * HomeContent Composite Component
 *
 * Orchestrates visible homepage sections in canonical sequence.
 * design.md Section 6.1 & Requirement 1. Server component by default (Req 1.2).
 */
export function HomeContent({ model }: HomeContentProps): JSX.Element {
  const visibleSections = getVisibleSections(model);

  return (
    <>
      {visibleSections.map((sectionId) => {
        switch (sectionId) {
          case 'hero':
            return (
              <HeroSection
                key="hero"
                profile={model.profile}
                contactAction={model.contactAction}
              />
            );
          case 'featured-projects':
            return (
              <FeaturedProjects
                key="featured-projects"
                projects={model.featuredProjects}
              />
            );
          case 'skills':
            return (
              <SkillsSnapshot
                key="skills"
                groups={model.skillGroups}
              />
            );
          case 'certifications':
            return (
              <CertificationsPreview
                key="certifications"
                certifications={model.certifications}
              />
            );
          case 'recent-activity':
            return (
              <RecentActivity
                key="recent-activity"
                posts={model.recentPosts}
              />
            );
          default: {
            const _exhaustiveCheck: never = sectionId;
            return _exhaustiveCheck;
          }
        }
      })}
    </>
  );
}
'@ | Set-Content "src\components\home\home-content.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/home-content.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.7, Req 7.3, Req 9.4, Req 10.6, Req 11.8

---

### M5.G8.T2: Implement Static Route Entry Point (`src/app/page.tsx`)

**Objective:** Author or update `src/app/page.tsx` as an async server component loading site, projects, certifications, and blog posts via `Promise.all` and rendering `HomeContent`.

**Acceptance Criteria:**
- ✓ File `src/app/page.tsx` created/updated
- ✓ Imports loaders: `getSiteConfig`, `getProjects`, `getCertifications`, `getBlogPosts`
- ✓ Imports `buildHomeViewModel` from `@/lib/home/view-model`
- ✓ Imports `HomeContent` from `@/components/home/home-content`
- ✓ Exports default async function `HomePage(): Promise<JSX.Element>`
- ✓ Concurrently awaits loaders using `Promise.all`
- ✓ Passes loaded data into `buildHomeViewModel` and renders `<HomeContent model={model} />`
- ✓ Zero `try/catch` wrapping loaders (errors must bubble to fail build per Req 2.6)
- ✓ Zero framework route params, headers, cookies, or search parameters

**Prerequisites:**
- M5.G8.T1 completed
- Target file: `src/app/page.tsx`

**Implementation Details:**

Write `src/app/page.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { Metadata } from 'next';
import { getSiteConfig } from '@/content/loaders/site';
import { getProjects } from '@/content/loaders/projects';
import { getCertifications } from '@/content/loaders/certifications';
import { getBlogPosts } from '@/content/loaders/blog';
import { buildHomeViewModel } from '@/lib/home/view-model';
import { buildHomeMetadata } from '@/lib/home/home-metadata';
import { HomeContent } from '@/components/home/home-content';

/**
 * Route Metadata Generator
 */
export async function generateMetadata(): Promise<Metadata> {
  const site = await getSiteConfig();
  return buildHomeMetadata(site);
}

/**
 * Static Homepage Route Entry Point (SCR-01)
 *
 * Statically prerendered at build time. Server component by default (Req 1.2).
 * TRD.md Section 2.3, AGENTS.md Section 3.
 */
export default async function HomePage(): Promise<JSX.Element> {
  const [site, projects, certifications, posts] = await Promise.all([
    getSiteConfig(),
    getProjects(),
    getCertifications(),
    getBlogPosts(),
  ]);

  const model = buildHomeViewModel({
    site,
    projects,
    certifications,
    posts,
  });

  return <HomeContent model={model} />;
}
'@ | Set-Content "src\app\page.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/app/page.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.3, Req 1.4, Req 1.6, Req 1.7, Req 2.6, Req 13.1

---

### M5.G8.T3: Audit Framework Invariance & Absence of Dynamic APIs

**Objective:** Audit `src/app/page.tsx` and `src/components/home/home-content.tsx` ensuring zero `'use client'` statements, zero dynamic headers/cookies, and zero duplicate landmarks.

**Acceptance Criteria:**
- ✓ Searches files for `'use client'`
- ✓ Searches files for `headers()`, `cookies()`, `useSearchParams`, `window`, `document`
- ✓ Searches files for `<header`, `<footer`, `<main`
- ✓ Confirms zero matches
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G8.T1 and M5.G8.T2 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\app\page.tsx", "src\components\home\home-content.tsx")
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' found in $file"
    }
    if ($content -match "\b(headers|cookies|useSearchParams|window|document)\b") {
        $violations += "Forbidden dynamic/browser API found in $file"
    }
    if ($content -match "<(header|footer|main)\b") {
        $violations += "Forbidden shell landmark rendered in $file (owned by RootLayout)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 1.6, Req 1.7, Req 16.2

---

### M5.G8.T4: Author Concrete Unit Scenarios for `HomeContent` (`tests/home/home-content.test.tsx`)

**Objective:** Create `tests/home/home-content.test.tsx` verifying section rendering order under full and empty collections.

**Acceptance Criteria:**
- ✓ File `tests/home/home-content.test.tsx` created
- ✓ Renders full model: verifies all 5 sections present in exact canonical order
- ✓ Renders model with empty projects: verifies `FeaturedProjects` empty state renders and `SkillsSnapshot` is omitted
- ✓ Renders model with empty certs and posts: verifies both sections are omitted with zero trailing headings
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8.T1 completed
- Fixtures available in `tests/fixtures/home-data.ts`
- Target file: `tests/home/home-content.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/home-content.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { HomeContent } from '@/components/home/home-content';
import { buildHomeViewModel } from '@/lib/home/view-model';
import {
  sampleSiteConfig,
  sampleProjects,
  sampleCertifications,
  sampleBlogPosts,
  emptyProjects,
  emptyCertifications,
  draftsOnlyBlogPosts,
} from '../fixtures/home-data';

describe('HomeContent Component (Req 1, 7, 9, 10, 11)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('renders all five sections in exact canonical sequence for fully populated model', () => {
      const model = buildHomeViewModel({
        site: sampleSiteConfig,
        projects: sampleProjects,
        certifications: sampleCertifications,
        posts: sampleBlogPosts,
      });

      const { container } = render(<HomeContent model={model} />);

      const sections = container.querySelectorAll('section');
      expect(sections.length).toBe(5);

      // Verify exact section labelling order
      expect(sections[0].getAttribute('aria-labelledby')).toBe('hero-heading');
      expect(sections[1].getAttribute('aria-labelledby')).toBe('featured-projects-heading');
      expect(sections[2].getAttribute('aria-labelledby')).toBe('skills-heading');
      expect(sections[3].getAttribute('aria-labelledby')).toBe('certifications-heading');
      expect(sections[4].getAttribute('aria-labelledby')).toBe('recent-activity-heading');
    });

    it('omits skills, certifications, and recent activity when collections are empty', () => {
      const model = buildHomeViewModel({
        site: sampleSiteConfig,
        projects: emptyProjects,
        certifications: emptyCertifications,
        posts: draftsOnlyBlogPosts,
      });

      const { container } = render(<HomeContent model={model} />);

      const sections = container.querySelectorAll('section');
      expect(sections.length).toBe(2); // hero and featured-projects only

      expect(sections[0].getAttribute('aria-labelledby')).toBe('hero-heading');
      expect(sections[1].getAttribute('aria-labelledby')).toBe('featured-projects-heading');

      // Verify omitted sections leave zero headings behind
      expect(screen.queryByRole('heading', { level: 2, name: 'Skills Snapshot' })).toBeNull();
      expect(screen.queryByRole('heading', { level: 2, name: 'Certifications' })).toBeNull();
      expect(screen.queryByRole('heading', { level: 2, name: 'Recent Activity' })).toBeNull();
    });
  });
});
'@ | Set-Content "tests\home\home-content.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/home-content.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.3, Req 9.4, Req 10.6, Req 11.8

---

### M5.G8.T5: Author Property-Based Test for Section Order Rendering (Property 9 Render Part)

**Objective:** Append property-based test in `tests/home/home-content.test.tsx` using `fast-check` validating that rendered `<section>` elements strictly reflect `getVisibleSections(model)`.

**Acceptance Criteria:**
- ✓ Implements Property 9 render test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 9: section visibility and canonical order rendering`
- ✓ Asserts rendered `<section>` elements match `getVisibleSections(model)` in exact length and order
- ✓ Asserts omitted sections emit zero orphaned headings
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8.T4 completed
- Target file: `tests/home/home-content.test.tsx`

**Implementation Details:**

Append Property 9 render test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 9 - Render Part)', () => {
    it('Feature: m5-homepage-experience, Property 9: rendered section elements strictly follow getVisibleSections order for any model', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { getVisibleSections } = require('@/lib/home/view-model');

      fc.assert(
        fc.property(
          fc.boolean(), // hasFeatured
          fc.boolean(), // hasSkills
          fc.boolean(), // hasCerts
          fc.boolean(), // hasPosts
          (hasFeatured, hasSkills, hasCerts, hasPosts) => {
            cleanup();
            const model = {
              profile: sampleSiteConfig.profile,
              contactAction: null,
              featuredProjects: hasFeatured ? [sampleProjects[0]] : [],
              skillGroups: hasSkills ? [{ label: 'Tech', technologies: [{ name: 'TS', count: 1 }] }] : [],
              certifications: hasCerts ? [sampleCertifications[0]] : [],
              recentPosts: hasPosts ? [sampleBlogPosts[0]] : [],
            };

            const expectedSections = getVisibleSections(model);
            const { container } = render(<HomeContent model={model} />);

            const renderedSections = Array.from(container.querySelectorAll('section'));
            expect(renderedSections.length).toBe(expectedSections.length);

            // Verify mapping
            const idMap: Record<string, string> = {
              'hero': 'hero-heading',
              'featured-projects': 'featured-projects-heading',
              'skills': 'skills-heading',
              'certifications': 'certifications-heading',
              'recent-activity': 'recent-activity-heading',
            };

            for (let i = 0; i < expectedSections.length; i++) {
              const expectedHeadingId = idMap[expectedSections[i]];
              expect(renderedSections[i].getAttribute('aria-labelledby')).toBe(expectedHeadingId);
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\home-content.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\home-content.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/home-content.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.3, Req 9.4, Req 10.6, Req 11.8

---

### M5.G8.T6: Author Property-Based Test for Heading Hierarchy and Landmarks (Property 12)

**Objective:** Append property-based test in `tests/home/home-content.test.tsx` validating Property 12: exactly one `<h1>` in hero, valid `aria-labelledby` targets in every section, `<h2>` section headings, zero skipped heading levels, and zero shell landmarks.

**Acceptance Criteria:**
- ✓ Implements Property 12 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 12: heading hierarchy and section labelling`
- ✓ Asserts exactly one `<h1>` in output, located inside hero section
- ✓ Asserts every `<section>` has `aria-labelledby` resolving to an existing heading within that section
- ✓ Asserts every section heading is an `<h2>`
- ✓ Asserts heading hierarchy never skips levels in DOM traversal
- ✓ Asserts zero `<header>`, `<footer>`, or `<main>` elements in rendered output
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8.T5 completed
- Target file: `tests/home/home-content.test.tsx`

**Implementation Details:**

Append Property 12 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 12)', () => {
    it('Feature: m5-homepage-experience, Property 12: heading hierarchy skips no levels, exactly one h1 exists, and landmarks are properly bounded', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProfile } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          arbProfile,
          fc.boolean(),
          fc.boolean(),
          fc.boolean(),
          (profile: any, hasSkills: boolean, hasCerts: boolean, hasPosts: boolean) => {
            cleanup();
            const model = {
              profile,
              contactAction: null,
              featuredProjects: [sampleProjects[0]],
              skillGroups: hasSkills ? [{ label: 'Tech', technologies: [{ name: 'TS', count: 1 }] }] : [],
              certifications: hasCerts ? [sampleCertifications[0]] : [],
              recentPosts: hasPosts ? [sampleBlogPosts[0]] : [],
            };

            const { container } = render(<HomeContent model={model} />);

            // 1. Exactly one h1 inside hero
            const h1s = container.querySelectorAll('h1');
            expect(h1s.length).toBe(1);
            expect(h1s[0].closest('section')?.getAttribute('aria-labelledby')).toBe('hero-heading');

            // 2. Section labelling validation
            const sections = container.querySelectorAll('section');
            for (const section of sections) {
              const labelledBy = section.getAttribute('aria-labelledby');
              expect(labelledBy).not.toBeNull();
              const heading = section.querySelector(`#${labelledBy}`);
              expect(heading).not.toBeNull();
            }

            // 3. Heading level hierarchy (no skipped levels)
            const headings = Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6'));
            let currentLevel = 0;
            for (const h of headings) {
              const level = parseInt(h.tagName.substring(1), 10);
              if (currentLevel > 0) {
                // Must not jump down more than 1 level (e.g. h1 to h3 is illegal)
                expect(level).toBeLessThanOrEqual(currentLevel + 1);
              }
              currentLevel = level;
            }

            // 4. Zero shell landmarks inside HomeContent
            expect(container.querySelectorAll('header, footer, main').length).toBe(0);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\home-content.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\home-content.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/home-content.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.7, Req 2.1, Req 6.1, Req 6.6, Req 14.1, Req 14.2, Req 14.3

---

### M5.G8.T7: Author Unit Scenarios for Static Route (`tests/home/page.test.tsx`)

**Objective:** Create `tests/home/page.test.tsx` verifying route rendering and metadata generation with mocked loaders.

**Acceptance Criteria:**
- ✓ File `tests/home/page.test.tsx` created
- ✓ Mocks `getSiteConfig`, `getProjects`, `getCertifications`, `getBlogPosts` returning sample fixtures
- ✓ Tests `HomePage()` renders `HomeContent` containing `HeroSection` and `FeaturedProjects`
- ✓ Tests `generateMetadata()` returns homepage metadata with canonical URL and description
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8.T2 completed
- Target file: `tests/home/page.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/page.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import HomePage, { generateMetadata } from '@/app/page';
import {
  sampleSiteConfig,
  sampleProjects,
  sampleCertifications,
  sampleBlogPosts,
} from '../fixtures/home-data';

vi.mock('@/content/loaders/site', () => ({
  getSiteConfig: vi.fn(),
}));
vi.mock('@/content/loaders/projects', () => ({
  getProjects: vi.fn(),
}));
vi.mock('@/content/loaders/certifications', () => ({
  getCertifications: vi.fn(),
}));
vi.mock('@/content/loaders/blog', () => ({
  getBlogPosts: vi.fn(),
}));

describe('HomePage Static Route (Req 1, 13)', () => {
  beforeEach(async () => {
    const { getSiteConfig } = await import('@/content/loaders/site');
    const { getProjects } = await import('@/content/loaders/projects');
    const { getCertifications } = await import('@/content/loaders/certifications');
    const { getBlogPosts } = await import('@/content/loaders/blog');

    vi.mocked(getSiteConfig).mockResolvedValue(sampleSiteConfig);
    vi.mocked(getProjects).mockResolvedValue(sampleProjects);
    vi.mocked(getCertifications).mockResolvedValue(sampleCertifications);
    vi.mocked(getBlogPosts).mockResolvedValue(sampleBlogPosts);
  });

  it('renders complete homepage content from loaded data', async () => {
    const Component = await HomePage();
    render(Component);

    expect(screen.getByRole('heading', { level: 1, name: 'Angelo Andres' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 2, name: 'Featured Projects' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 2, name: 'Skills Snapshot' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 2, name: 'Certifications' })).toBeDefined();
    expect(screen.getByRole('heading', { level: 2, name: 'Recent Activity' })).toBeDefined();
  });

  it('generates route-specific metadata derived from site configuration', async () => {
    const meta = await generateMetadata();

    expect(meta.description).toBe(sampleSiteConfig.profile.introduction);
    expect(meta.alternates?.canonical).toBe('https://example.vercel.app/');
    expect(meta.openGraph?.url).toBe('https://example.vercel.app/');
  });
});
'@ | Set-Content "tests\home\page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/page.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 1.4, Req 13.1, Req 13.2, Req 13.3

---

### M5.G8.T8: Author Content Loader Rejection Propagation Test

**Objective:** Append test in `tests/home/page.test.tsx` verifying that loader validation failures propagate directly without suppressive try/catch boundaries per Requirement 2.6.

**Acceptance Criteria:**
- ✓ Mocks `getSiteConfig` rejecting with schema validation `Error`
- ✓ Asserts `HomePage()` rejects with identical error
- ✓ Asserts `generateMetadata()` rejects with identical error
- ✓ Proves zero try/catch blocks swallow content schema failures
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G8.T7 completed
- Target file: `tests/home/page.test.tsx`

**Implementation Details:**

Append rejection test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Loader Failure Propagation (Req 2.6)', () => {
    it('propagates loader validation rejections directly to fail static build', async () => {
      const { getSiteConfig } = await import('@/content/loaders/site');
      vi.mocked(getSiteConfig).mockRejectedValueOnce(
        new Error('Content schema validation failed: [site.json] missing profile.introduction')
      );

      await expect(HomePage()).rejects.toThrow(
        'Content schema validation failed: [site.json] missing profile.introduction'
      );
    });

    it('propagates loader rejection from generateMetadata directly', async () => {
      const { getSiteConfig } = await import('@/content/loaders/site');
      vi.mocked(getSiteConfig).mockRejectedValueOnce(
        new Error('Content schema validation failed: [site.json] invalid siteUrl')
      );

      await expect(generateMetadata()).rejects.toThrow(
        'Content schema validation failed: [site.json] invalid siteUrl'
      );
    });
  });
'@

$content = Get-Content "tests\home\page.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\page.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/page.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.6

---

### M5.G8.T9: Verify Source Hygiene of `page.tsx` and `home-content.tsx`

**Objective:** Audit `page.tsx` and `home-content.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file lengths strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ Both files are strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G8.T1 and M5.G8.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\app\page.tsx", "src\components\home\home-content.tsx")
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
        Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 14.8, Req 16.7, Req 16.8

---

### M5.G8.T10: Checkpoint — HomeContent and Route Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `HomeContent` and `src/app/page.tsx`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs home-content and page tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G8.T1 through M5.G8.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/home-content.test.tsx tests/home/page.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/home-content.test.tsx tests/home/page.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\home\home-content.tsx"
Test-Path "src\app\page.tsx"
Test-Path "tests\home\home-content.test.tsx"
Test-Path "tests\home\page.test.tsx"
npm run typecheck
npm run test -- tests/home/home-content.test.tsx tests/home/page.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all home-content and page tests with return code 0.