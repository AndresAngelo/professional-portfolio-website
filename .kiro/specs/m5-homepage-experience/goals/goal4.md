# M5.G4: View Model, Section Visibility, and Homepage Metadata

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G4 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the central Homepage view-model aggregator `buildHomeViewModel` and visibility predicate `getVisibleSections` in `src/lib/home/view-model.ts`, alongside the homepage SEO metadata generator `buildHomeMetadata` in `src/lib/home/home-metadata.ts`. `buildHomeViewModel` orchestrates the five pure selection and derivation helpers (`selectFeaturedProjects`, `deriveSkillGroups`, `selectCertificationPreview`, `selectRecentPosts`, and `selectHeroContactAction`) into an immutable `HomeViewModel`. `getVisibleSections` enforces the single source of truth for section visibility, guaranteeing that `hero` and `featured-projects` are always present, while `skills`, `certifications`, and `recent-activity` render if and only if their respective data collections are non-empty, returned strictly in `HOME_SECTION_ORDER`. `buildHomeMetadata` constructs standard Next.js `Metadata` deriving canonical URLs and Open Graph tags from `SiteConfig.siteUrl`, mapping `profile.introduction` to description, composing `{name} | {professionalTitle}` for title, and returning an `{ absolute: ... }` title when the composed title already contains `siteName` to prevent double branding when M4's title template is applied. Validate all modules with Vitest unit tests and fast-check property tests for Properties 9 (helper part) and 14.

## Goal Success Criteria

- ✓ `src/lib/home/view-model.ts` exports `HomeViewModel`, pure function `buildHomeViewModel`, and pure function `getVisibleSections`
- ✓ `buildHomeViewModel` passes all projects to `deriveSkillGroups` and correctly maps profile, contact action, featured projects, certifications, and recent posts
- ✓ `getVisibleSections` always returns `'hero'` and `'featured-projects'`; conditionally includes `'skills'`, `'certifications'`, and `'recent-activity'` iff data is non-empty; returns IDs strictly in `HOME_SECTION_ORDER`
- ✓ `src/lib/home/home-metadata.ts` exports pure function `buildHomeMetadata(site: Pick<SiteConfig, 'siteName' | 'siteUrl' | 'profile'>): Metadata`
- ✓ `buildHomeMetadata` prevents duplicate site name branding by returning `{ absolute: ... }` title when composed title contains `siteName` case-insensitively
- ✓ Neither module imports React or Next.js layout components nor contains `'use client'` statements
- ✓ Unit and property tests in `tests/home/view-model.test.ts` and `tests/home/section-visibility.test.ts` satisfy Property 9 helper invariants ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/home/home-metadata.test.ts` satisfy Property 14 ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1, M5.G2, and M5.G3 completed (all 5 pure helpers and `home-text.ts` available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream types imported strictly from `@/types/content`

---

## Tasks

### M5.G4.T1: Implement Homepage View Model Data Structures and Builder (`src/lib/home/view-model.ts`)

**Objective:** Author `HomeViewModel` interface and `buildHomeViewModel` function in `src/lib/home/view-model.ts` composing all selection helpers.

**Acceptance Criteria:**
- ✓ File `src/lib/home/view-model.ts` created
- ✓ Exports `interface HomeViewModel` containing `profile`, `contactAction`, `featuredProjects`, `skillGroups`, `certifications`, and `recentPosts`
- ✓ Exports `buildHomeViewModel(input: { site: Pick<SiteConfig, 'profile' | 'contactChannels'>; projects: readonly Project[]; certifications: readonly Certification[]; posts: readonly BlogPost[]; }): HomeViewModel`
- ✓ Invokes `selectHeroContactAction(site.contactChannels)`
- ✓ Invokes `selectFeaturedProjects(projects)`
- ✓ Invokes `deriveSkillGroups(projects)` passing ALL projects (featured and non-featured per Req 9.3)
- ✓ Invokes `selectCertificationPreview(certifications)`
- ✓ Invokes `selectRecentPosts(posts)`
- ✓ Pure function with zero framework or browser dependencies

**Prerequisites:**
- M5.G2 and M5.G3 completed
- Target file: `src/lib/home/view-model.ts`

**Implementation Details:**

Write the view model builder in `src/lib/home/view-model.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure View Model Aggregator & Visibility Invariants
 *
 * Combines content selection helpers and dictates homepage section rendering order.
 * Contains no React, Next.js, or browser dependencies (Req 1.1, 7.3, 9.3, 9.4, 10.6, 11.8, 16.6).
 */
import type { SiteConfig, Project, Certification, BlogPost } from '@/types/content';
import { HOME_SECTION_ORDER, type HomeSectionId } from '@/components/home/home-text';
import { selectFeaturedProjects } from './select-featured-projects';
import { selectCertificationPreview } from './select-certification-preview';
import { selectRecentPosts } from './select-recent-posts';
import { deriveSkillGroups, type SkillGroup } from './derive-skill-groups';
import { selectHeroContactAction, type HeroContactAction } from './select-hero-action';

export interface HomeViewModel {
  readonly profile: SiteConfig['profile'];
  readonly contactAction: HeroContactAction | null;
  readonly featuredProjects: readonly Project[];
  readonly skillGroups: readonly SkillGroup[];
  readonly certifications: readonly Certification[];
  readonly recentPosts: readonly BlogPost[];
}

/**
 * Builds the complete Homepage view model by orchestrating selection helpers.
 */
export function buildHomeViewModel(input: {
  site: Pick<SiteConfig, 'profile' | 'contactChannels'>;
  projects: readonly Project[];
  certifications: readonly Certification[];
  posts: readonly BlogPost[];
}): HomeViewModel {
  return {
    profile: input.site.profile,
    contactAction: selectHeroContactAction(input.site.contactChannels),
    featuredProjects: selectFeaturedProjects(input.projects),
    skillGroups: deriveSkillGroups(input.projects), // all projects feed skills (Req 9.3)
    certifications: selectCertificationPreview(input.certifications),
    recentPosts: selectRecentPosts(input.posts),
  };
}
'@ | Set-Content "src\lib\home\view-model.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/view-model.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 9.3, Req 16.6

---

### M5.G4.T2: Implement Section Visibility Logic in `src/lib/home/view-model.ts`

**Objective:** Append `getVisibleSections` to `src/lib/home/view-model.ts` implementing the single source of truth for section visibility.

**Acceptance Criteria:**
- ✓ Exports `getVisibleSections(model: HomeViewModel): HomeSectionId[]`
- ✓ `'hero'` is ALWAYS present
- ✓ `'featured-projects'` is ALWAYS present (empty state renders if projects are empty)
- ✓ `'skills'` is included iff `model.skillGroups.length > 0`
- ✓ `'certifications'` is included iff `model.certifications.length > 0`
- ✓ `'recent-activity'` is included iff `model.recentPosts.length > 0`
- ✓ Returned array strictly matches the sequence of `HOME_SECTION_ORDER`
- ✓ Pure function with zero side effects

**Prerequisites:**
- M5.G4.T1 completed
- Target file: `src/lib/home/view-model.ts`

**Implementation Details:**

Append `getVisibleSections` to `src/lib/home/view-model.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

/**
 * Returns the list of visible section IDs in canonical HOME_SECTION_ORDER.
 * - hero: always visible
 * - featured-projects: always visible (renders empty state when projects is empty)
 * - skills: visible iff skillGroups is non-empty
 * - certifications: visible iff certifications is non-empty
 * - recent-activity: visible iff recentPosts is non-empty
 */
export function getVisibleSections(model: HomeViewModel): HomeSectionId[] {
  const visible = new Set<HomeSectionId>();

  visible.add('hero');
  visible.add('featured-projects');

  if (model.skillGroups.length > 0) {
    visible.add('skills');
  }

  if (model.certifications.length > 0) {
    visible.add('certifications');
  }

  if (model.recentPosts.length > 0) {
    visible.add('recent-activity');
  }

  // Filter HOME_SECTION_ORDER to preserve exact sequence
  return HOME_SECTION_ORDER.filter((sectionId) => visible.has(sectionId));
}
'@

Add-Content -Path "src\lib\home\view-model.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/view-model.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.3, Req 9.4, Req 10.6, Req 11.8

---

### M5.G4.T3: Implement Homepage SEO Metadata Generator (`src/lib/home/home-metadata.ts`)

**Objective:** Author pure helper `buildHomeMetadata` in `src/lib/home/home-metadata.ts` producing Next.js metadata while preventing site name duplication.

**Acceptance Criteria:**
- ✓ File `src/lib/home/home-metadata.ts` created
- ✓ Exports `buildHomeMetadata(site: Pick<SiteConfig, 'siteName' | 'siteUrl' | 'profile'>): Metadata`
- ✓ Generates canonical URL and Open Graph URL using `new URL('/', site.siteUrl).href`
- ✓ Maps `site.profile.introduction` to `description` and `openGraph.description`
- ✓ Composes title: `${profile.name} | ${profile.professionalTitle}`
- ✓ If composed title contains `siteName` case-insensitively, returns `title: { absolute: composedTitle }`
- ✓ If composed title does NOT contain `siteName`, returns plain string `title: composedTitle` (allowing M4 template to append ` | {siteName}`)
- ✓ Sets `openGraph.title = composedTitle`
- ✓ Sets `openGraph.type = 'website'`
- ✓ Contains zero image placeholders or Twitter cards (Req 10.6, 13.1)

**Prerequisites:**
- Target file: `src/lib/home/home-metadata.ts`

**Implementation Details:**

Write `src/lib/home/home-metadata.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Metadata Helper: Homepage
 *
 * Derives route-specific Next.js Metadata from SiteConfig.
 * Prevents siteName duplication against M4 RootLayout title template (Req 13.1-13.6).
 */
import type { Metadata } from 'next';
import type { SiteConfig } from '@/types/content';

export function buildHomeMetadata(
  site: Pick<SiteConfig, 'siteName' | 'siteUrl' | 'profile'>
): Metadata {
  const rootUrl = new URL('/', site.siteUrl).href;
  const composedTitle = `${site.profile.name} | ${site.profile.professionalTitle}`;

  // If composedTitle already contains siteName, specify absolute title to prevent template duplication
  const titleContainsSiteName = composedTitle
    .toLowerCase()
    .includes(site.siteName.toLowerCase());

  const titleField = titleContainsSiteName
    ? { absolute: composedTitle }
    : composedTitle;

  return {
    title: titleField,
    description: site.profile.introduction,
    alternates: {
      canonical: rootUrl,
    },
    openGraph: {
      type: 'website',
      siteName: site.siteName,
      title: composedTitle,
      description: site.profile.introduction,
      url: rootUrl,
    },
  };
}
'@ | Set-Content "src\lib\home\home-metadata.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/home-metadata.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 13.5

---

### M5.G4.T4: Audit View Model and Metadata Modules for Framework Directives

**Objective:** Audit `src/lib/home/view-model.ts` and `home-metadata.ts` ensuring zero `'use client'` statements, zero hardcoded content literals, and pure functional execution.

**Acceptance Criteria:**
- ✓ Scans both files for `'use client'`
- ✓ Scans both files for hardcoded owner names or emails
- ✓ Confirms zero matches
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G4.T2 and M5.G4.T3 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\lib\home\view-model.ts", "src\lib\home\home-metadata.ts")
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' in $file"
    }
    if ($content -match "['""]Angelo['""]|['""]hello@example\.com['""]") {
        $violations += "Hardcoded personal literal found in $file"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 2.5, Req 13.5, Req 16.6

---

### M5.G4.T5: Author Concrete Unit Scenarios for View Model Builder (`tests/home/view-model.test.ts`)

**Objective:** Create `tests/home/view-model.test.ts` verifying view model assembly under populated and edge-case inputs (empty projects, drafts only, no certifications).

**Acceptance Criteria:**
- ✓ File `tests/home/view-model.test.ts` created
- ✓ Verifies `buildHomeViewModel` populates all fields with full fixtures
- ✓ Verifies all projects (including non-featured) are passed into skill derivation
- ✓ Verifies empty projects input results in `featuredProjects: []` and `skillGroups: []`
- ✓ Verifies drafts-only posts input results in `recentPosts: []`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G4.T1 completed
- Fixtures available in `tests/fixtures/home-data.ts`
- Target file: `tests/home/view-model.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/home/view-model.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import { buildHomeViewModel } from '@/lib/home/view-model';
import {
  sampleSiteConfig,
  sampleProjects,
  sampleCertifications,
  sampleBlogPosts,
  emptyProjects,
  draftsOnlyBlogPosts,
  emptyCertifications,
} from '../fixtures/home-data';

describe('buildHomeViewModel Aggregator (Req 1, 9)', () => {
  it('assembles a complete view model with populated fixtures', () => {
    const model = buildHomeViewModel({
      site: sampleSiteConfig,
      projects: sampleProjects,
      certifications: sampleCertifications,
      posts: sampleBlogPosts,
    });

    expect(model.profile.name).toBe('Angelo Andres');
    expect(model.contactAction?.label).toBe('Email Angelo');
    expect(model.featuredProjects.length).toBe(3);
    expect(model.certifications.length).toBe(3);
    expect(model.recentPosts.length).toBe(3);
    expect(model.skillGroups.length).toBe(1);

    // Verify non-featured project (Delta Portal) contributed to skills
    const techs = model.skillGroups[0].technologies;
    expect(techs.some((t) => t.name === 'React')).toBe(true);
  });

  it('handles empty edge case inputs without throwing', () => {
    const model = buildHomeViewModel({
      site: sampleSiteConfig,
      projects: emptyProjects,
      certifications: emptyCertifications,
      posts: draftsOnlyBlogPosts,
    });

    expect(model.featuredProjects).toEqual([]);
    expect(model.skillGroups).toEqual([]);
    expect(model.certifications).toEqual([]);
    expect(model.recentPosts).toEqual([]);
  });
});
'@ | Set-Content "tests\home\view-model.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/view-model.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 9.3

---

### M5.G4.T6: Author Unit & Property-Based Tests for Section Visibility (Property 9 Helper Part)

**Objective:** Create `tests/home/section-visibility.test.ts` verifying `getVisibleSections` under concrete scenarios and fast-check Property 9 (helper part).

**Acceptance Criteria:**
- ✓ File `tests/home/section-visibility.test.ts` created
- ✓ Tests `hero` and `featured-projects` are present even when all collections are empty
- ✓ Tests `skills`, `certifications`, and `recent-activity` appear iff their collections are non-empty
- ✓ Tests sections strictly follow `HOME_SECTION_ORDER`
- ✓ Implements Property 9 helper test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 9: section visibility and order`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G4.T2 completed
- Target file: `tests/home/section-visibility.test.ts`

**Implementation Details:**

Write `tests/home/section-visibility.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { getVisibleSections, type HomeViewModel } from '@/lib/home/view-model';
import { HOME_SECTION_ORDER } from '@/components/home/home-text';

describe('getVisibleSections Visibility Helper (Req 1, 7, 9, 10, 11)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('always includes hero and featured-projects when collections are empty', () => {
      const emptyModel: HomeViewModel = {
        profile: {} as any,
        contactAction: null,
        featuredProjects: [],
        skillGroups: [],
        certifications: [],
        recentPosts: [],
      };

      const sections = getVisibleSections(emptyModel);
      expect(sections).toEqual(['hero', 'featured-projects']);
    });

    it('returns all five sections in exact canonical order when all collections are populated', () => {
      const fullModel: HomeViewModel = {
        profile: {} as any,
        contactAction: null,
        featuredProjects: [{ slug: 'p1' } as any],
        skillGroups: [{ label: 'Tech', technologies: [] }],
        certifications: [{ slug: 'c1' } as any],
        recentPosts: [{ slug: 'b1' } as any],
      };

      const sections = getVisibleSections(fullModel);
      expect(sections).toEqual([
        'hero',
        'featured-projects',
        'skills',
        'certifications',
        'recent-activity',
      ]);
    });
  });

  describe('Property-Based Invariants (Property 9 - Helper Part)', () => {
    it('Feature: m5-homepage-experience, Property 9: section visibility and canonical order invariants hold for any view model', () => {
      fc.assert(
        fc.property(
          fc.boolean(), // hasSkills
          fc.boolean(), // hasCerts
          fc.boolean(), // hasPosts
          (hasSkills, hasCerts, hasPosts) => {
            const model: HomeViewModel = {
              profile: {} as any,
              contactAction: null,
              featuredProjects: [],
              skillGroups: hasSkills ? [{ label: 'Tech', technologies: [] }] : [],
              certifications: hasCerts ? [{ slug: 'c' } as any] : [],
              recentPosts: hasPosts ? [{ slug: 'b' } as any] : [],
            };

            const sections = getVisibleSections(model);

            // 1. Mandatory sections
            expect(sections).toContain('hero');
            expect(sections).toContain('featured-projects');

            // 2. Conditional inclusion
            expect(sections.includes('skills')).toBe(hasSkills);
            expect(sections.includes('certifications')).toBe(hasCerts);
            expect(sections.includes('recent-activity')).toBe(hasPosts);

            // 3. Strict canonical order
            let lastIndex = -1;
            for (const sectionId of sections) {
              const canonicalIndex = HOME_SECTION_ORDER.indexOf(sectionId);
              expect(canonicalIndex).toBeGreaterThan(lastIndex);
              lastIndex = canonicalIndex;
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\home\section-visibility.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/section-visibility.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 7.1, Req 7.3, Req 9.4, Req 10.6, Req 11.8

---

### M5.G4.T7: Author Concrete Unit Scenarios for Homepage Metadata (`tests/home/home-metadata.test.ts`)

**Objective:** Create `tests/home/home-metadata.test.ts` verifying title composition, siteName duplication prevention, canonical URL derivation, and Open Graph attributes.

**Acceptance Criteria:**
- ✓ File `tests/home/home-metadata.test.ts` created
- ✓ Tests returns absolute title when composed title contains `siteName`
- ✓ Tests returns plain string title when composed title does NOT contain `siteName`
- ✓ Tests `description` and `openGraph.description` match `profile.introduction`
- ✓ Tests `alternates.canonical` and `openGraph.url` equal `https://example.vercel.app/`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G4.T3 completed
- Target file: `tests/home/home-metadata.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/home/home-metadata.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import { buildHomeMetadata } from '@/lib/home/home-metadata';
import { sampleSiteConfig } from '../fixtures/home-data';

describe('buildHomeMetadata Helper (Req 13)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns absolute title when composed title contains siteName (prevents duplicate branding)', () => {
      // sampleSiteConfig: siteName = 'Angelo Andres', profile.name = 'Angelo Andres'
      const meta = buildHomeMetadata(sampleSiteConfig);

      expect(meta.title).toEqual({
        absolute: 'Angelo Andres | Pipeline Lead & Specification Architect',
      });
      expect(meta.description).toBe(sampleSiteConfig.profile.introduction);
      expect(meta.alternates?.canonical).toBe('https://example.vercel.app/');
      expect(meta.openGraph?.url).toBe('https://example.vercel.app/');
    });

    it('returns plain string title when composed title does NOT contain siteName', () => {
      const distinctSite = {
        ...sampleSiteConfig,
        siteName: 'Zero Hallucination Studio', // distinct brand
      };

      const meta = buildHomeMetadata(distinctSite);
      expect(meta.title).toBe('Angelo Andres | Pipeline Lead & Specification Architect');
    });
  });
});
'@ | Set-Content "tests\home\home-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/home-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 13.5

---

### M5.G4.T8: Author Property-Based Test for Homepage Metadata (Property 14)

**Objective:** Append property-based test in `tests/home/home-metadata.test.ts` validating Property 14 across arbitrary site names, titles, and introductions.

**Acceptance Criteria:**
- ✓ Implements Property 14 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 14: homepage metadata derives from site configuration`
- ✓ Asserts canonical and Open Graph URLs equal root of `siteUrl`
- ✓ Asserts description equals `profile.introduction`
- ✓ Asserts title contains `profile.name` and `profile.professionalTitle`
- ✓ Asserts siteName is not duplicated when template is simulated
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G4.T7 completed
- Target file: `tests/home/home-metadata.test.ts`

**Implementation Details:**

Append Property 14 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 14)', () => {
    it('Feature: m5-homepage-experience, Property 14: homepage metadata derives strictly from SiteConfig and prevents siteName duplication', () => {
      const fc = require('fast-check');
      const { arbProfile } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          fc.string({ minLength: 3, maxLength: 25 }).filter((s: string) => s.trim().length >= 3 && !s.includes('<')),
          arbProfile,
          (siteName: string, profile: any) => {
            const site = {
              siteName,
              siteUrl: 'https://example.vercel.app',
              profile,
            };

            const meta = buildHomeMetadata(site);
            const expectedUrl = 'https://example.vercel.app/';

            expect(meta.description).toBe(profile.introduction);
            expect(meta.alternates?.canonical).toBe(expectedUrl);
            expect(meta.openGraph?.url).toBe(expectedUrl);
            expect(meta.openGraph?.title).toContain(profile.name);
            expect(meta.openGraph?.title).toContain(profile.professionalTitle);

            // Verify title resolution
            let resolvedTitle: string;
            if (typeof meta.title === 'object' && meta.title !== null && 'absolute' in meta.title) {
              resolvedTitle = (meta.title as any).absolute;
            } else {
              // M4 template simulation: `%s | ${siteName}`
              resolvedTitle = `${meta.title} | ${siteName}`;
            }

            expect(resolvedTitle).toContain(profile.name);
            expect(resolvedTitle).toContain(profile.professionalTitle);

            // Count occurrences of siteName in resolved title
            const lowerTitle = resolvedTitle.toLowerCase();
            const lowerSite = siteName.toLowerCase();
            const matches = lowerTitle.split(lowerSite).length - 1;

            // If profile.name/title natively contained siteName, matches can be >1, otherwise at most 1
            const nativeMatches =
              (`${profile.name} ${profile.professionalTitle}`).toLowerCase().split(lowerSite).length - 1;
            expect(matches).toBeLessThanOrEqual(nativeMatches + 1);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\home-metadata.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\home-metadata.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/home-metadata.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3, Req 13.4, Req 13.5

---

### M5.G4.T9: Author Purity & Determinism Test for View Model Builder

**Objective:** Append test in `tests/home/view-model.test.ts` verifying that `buildHomeViewModel` does not mutate input objects and returns identical outputs for identical inputs.

**Acceptance Criteria:**
- ✓ Asserts deeply frozen inputs are not mutated during `buildHomeViewModel`
- ✓ Asserts two executions with identical arguments produce deeply equal results
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G4.T5 completed
- Target file: `tests/home/view-model.test.ts`

**Implementation Details:**

Append purity test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Purity & Immutability', () => {
    it('executes without mutating inputs and is completely deterministic', () => {
      const input = {
        site: sampleSiteConfig,
        projects: sampleProjects,
        certifications: sampleCertifications,
        posts: sampleBlogPosts,
      };

      const frozenInput = Object.freeze(JSON.parse(JSON.stringify(input)));
      const snapshot = JSON.stringify(frozenInput);

      const run1 = buildHomeViewModel(frozenInput);
      expect(JSON.stringify(frozenInput)).toBe(snapshot);

      const run2 = buildHomeViewModel(frozenInput);
      expect(run1).toEqual(run2);
    });
  });
'@

$content = Get-Content "tests\home\view-model.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\view-model.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/view-model.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.5, Req 8.7, Req 10.3, Req 11.5

---

### M5.G4.T10: Checkpoint — View Model and Metadata Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across view model and metadata modules.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all view model and metadata test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G4.T1 through M5.G4.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/view-model.test.ts tests/home/section-visibility.test.ts tests/home/home-metadata.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/view-model.test.ts tests/home/section-visibility.test.ts tests/home/home-metadata.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 13.1, Req 16.6

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 4 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\home\view-model.ts"
Test-Path "src\lib\home\home-metadata.ts"
Test-Path "tests\home\view-model.test.ts"
Test-Path "tests\home\section-visibility.test.ts"
Test-Path "tests\home\home-metadata.test.ts"
npm run typecheck
npm run test -- tests/home/view-model.test.ts tests/home/section-visibility.test.ts tests/home/home-metadata.test.ts
```
Expected output:
- `True` for all 5 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all view model and metadata tests with return code 0.