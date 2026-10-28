# M5.G5: HeroSection

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component `HeroSection` in `src/components/home/hero-section.tsx`. `HeroSection` renders the opening region of the homepage (`<section aria-labelledby="hero-heading">`) containing the page's single `<h1>` (`h1#hero-heading`) displaying `profile.name`, followed by the professional title, concise introduction, and location. It presents a prominent primary call to action linking to `/projects` (`View Projects`) using M3's `Button` primitive, alongside an optional secondary contact action derived from `contactAction` (`ExternalLink` for `external` URLs, secondary `Button` for `mailto:` or `internal` destinations). When `availableForOpportunities` is `true`, it displays an accessible availability indicator with both visual cues and visible text without relying on color alone. If the secondary action label matches the primary action label case-insensitively, it disambiguates the accessible name using `aria-label="{label} (contact)"`. Enforce strict server-component execution (zero `'use client'`), zero hardcoded profile values or fallback strings, and complete semantic token usage. Validate all states, accessibility rules, and Property 8 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/home/hero-section.tsx` implemented as a server component without `'use client'`
- ✓ Contains the only `<h1>` on the Homepage, rendering `profile.name`
- ✓ Renders `professionalTitle`, `introduction`, and `location` derived strictly from props
- ✓ Renders primary call to action using M3 `Button` (`variant="primary"`, `href="/projects"`, text `HOME_TEXT.viewProjects`)
- ✓ Conditionally renders secondary contact action: `ExternalLink` for external URLs, secondary `Button` for mailto/internal; omitted when `contactAction` is `null`
- ✓ Resolves name collisions: applies `aria-label="{label} (contact)"` if contact action label matches primary button label case-insensitively
- ✓ Renders availability indicator with visible text `HOME_TEXT.availability` iff `availableForOpportunities === true`
- ✓ Applies M3 `FOCUS_RING` and motion classes to interactive controls; contains zero hardcoded colors or durations
- ✓ Unit, property (Property 8), and axe accessibility tests in `tests/home/hero-section.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1, M5.G2, M5.G3, and M5.G4 completed
- `home-text.ts` available at `src/components/home/home-text.ts`
- M3 primitives (`Container`, `Button`, `ExternalLink`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available at `src/components/ui/`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M5.G5.T1: Implement HeroSection Component Skeleton & Landmarks (`src/components/home/hero-section.tsx`)

**Objective:** Author the initial skeleton of `src/components/home/hero-section.tsx` with semantic `<section>` landmark, accessible heading association, and single `<h1>` tag.

**Acceptance Criteria:**
- ✓ File `src/components/home/hero-section.tsx` created
- ✓ Exports `HeroSectionProps` interface requiring `profile: SiteConfig['profile']` and `contactAction: HeroContactAction | null`
- ✓ Exports `HeroSection(props: HeroSectionProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="hero-heading" className="py-12 md:py-20 bg-page">`
- ✓ Wraps content in M3 `<Container>`
- ✓ Renders `<h1 id="hero-heading" className="text-heading-1 font-bold text-text-primary tracking-tight">` with `profile.name`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5.G1 completed (`home-text.ts` exists)
- M3 `Container` exists
- Target file: `src/components/home/hero-section.tsx`

**Implementation Details:**

Write the skeleton of `src/components/home/hero-section.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { SiteConfig } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Button } from '@/components/ui/button';
import { ExternalLink } from '@/components/ui/external-link';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';
import type { HeroContactAction } from '@/lib/home/select-hero-action';

export interface HeroSectionProps {
  profile: SiteConfig['profile'];
  contactAction: HeroContactAction | null;
}

/**
 * Hero Section Component
 *
 * Orientation landmark rendering profile identity, concise positioning, and calls-to-action.
 * design.md Section 6.1 & Requirement 2, 3, 4. Server component by default (Req 1.2).
 */
export function HeroSection({ profile, contactAction }: HeroSectionProps): JSX.Element {
  return (
    <section
      aria-labelledby="hero-heading"
      className="border-b border-border-default bg-page py-12 md:py-20"
    >
      <Container className="max-w-4xl">
        <h1
          id="hero-heading"
          className="text-heading-1 font-bold tracking-tight text-text-primary mb-3"
        >
          {profile.name}
        </h1>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\hero-section.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/hero-section.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 2.1, Req 14.1, Req 14.2, Req 15.1

---

### M5.G5.T2: Append Profile Metadata Copy (Title, Introduction, Location)

**Objective:** Append professional title, introduction, and location paragraphs to `HeroSection` using semantic typography tokens.

**Acceptance Criteria:**
- ✓ Renders `profile.professionalTitle` with `text-heading-3 font-semibold text-brand-primary`
- ✓ Renders `profile.introduction` with `text-lead text-text-secondary`
- ✓ Renders `profile.location` with `text-small text-text-secondary`
- ✓ Values derived exclusively from `profile` props (zero hardcoded strings)

**Prerequisites:**
- M5.G5.T1 completed
- Target file: `src/components/home/hero-section.tsx`

**Implementation Details:**

Update `src/components/home/hero-section.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$code = @'
import React from 'react';
import type { SiteConfig } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Button } from '@/components/ui/button';
import { ExternalLink } from '@/components/ui/external-link';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';
import type { HeroContactAction } from '@/lib/home/select-hero-action';

export interface HeroSectionProps {
  profile: SiteConfig['profile'];
  contactAction: HeroContactAction | null;
}

/**
 * Hero Section Component
 *
 * Orientation landmark rendering profile identity, concise positioning, and calls-to-action.
 * design.md Section 6.1 & Requirement 2, 3, 4. Server component by default (Req 1.2).
 */
export function HeroSection({ profile, contactAction }: HeroSectionProps): JSX.Element {
  return (
    <section
      aria-labelledby="hero-heading"
      className="border-b border-border-default bg-page py-12 md:py-20"
    >
      <Container className="max-w-4xl">
        <h1
          id="hero-heading"
          className="text-heading-1 font-bold tracking-tight text-text-primary mb-2"
        >
          {profile.name}
        </h1>

        <p className="text-heading-3 font-semibold text-brand-primary mb-4">
          {profile.professionalTitle}
        </p>

        <p className="text-lead text-text-secondary mb-4 leading-relaxed">
          {profile.introduction}
        </p>

        <p className="text-small text-text-secondary flex items-center gap-1.5 mb-6">
          <svg
            className="h-4 w-4 shrink-0 text-text-secondary"
            aria-hidden="true"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span>{profile.location}</span>
        </p>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\hero-section.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/hero-section.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 2.5

---

### M5.G5.T3: Append Accessible Availability Indicator

**Objective:** Append the availability indicator to `HeroSection` displaying visible text and decorative indicator iff `availableForOpportunities === true`.

**Acceptance Criteria:**
- ✓ Renders only when `profile.availableForOpportunities === true`
- ✓ Omitted completely when `profile.availableForOpportunities === false`
- ✓ Contains decorative dot with `aria-hidden="true"`
- ✓ Contains visible text `HOME_TEXT.availability` (`'Available for opportunities'`)
- ✓ Does NOT convey status using color alone (Req 4.3)

**Prerequisites:**
- M5.G5.T2 completed
- Target file: `src/components/home/hero-section.tsx`

**Implementation Details:**

Update `src/components/home/hero-section.tsx` to include the availability indicator:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$code = Get-Content "src\components\home\hero-section.tsx" -Raw
$target = "<span>{profile.location}</span>`r`n        </p>"
if (-not $code.Contains($target)) {
  $target = "<span>{profile.location}</span>`n        </p>"
}

$replacement = @"
<span>{profile.location}</span>
        </p>

        {profile.availableForOpportunities && (
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface border border-border-default mb-8">
            <span
              className="h-2 w-2 rounded-full bg-feedback-success shrink-0"
              aria-hidden="true"
            />
            <span className="text-small font-medium text-text-primary">
              {HOME_TEXT.availability}
            </span>
          </div>
        )}
"@

$code = $code.Replace($target, $replacement)
$code | Set-Content "src\components\home\hero-section.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/hero-section.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.2, Req 4.3, Req 4.4

---

### M5.G5.T4: Implement Calls to Action and Name Collision Resolution

**Objective:** Append primary "View Projects" button and conditional secondary contact action with name disambiguation to `HeroSection`.

**Acceptance Criteria:**
- ✓ Renders primary call to action using M3 `Button` (`variant="primary"`, `size="lg"`, `href="/projects"`, text `HOME_TEXT.viewProjects`)
- ✓ Secondary CTA renders iff `contactAction !== null`
- ✓ External contact URL renders M3 `ExternalLink` (`target="_blank"`, `rel="noopener noreferrer"`)
- ✓ Mailto or internal contact URL renders M3 `Button` (`variant="secondary"`, `size="lg"`, `href={url}`)
- ✓ If `contactAction.label.toLowerCase() === HOME_TEXT.viewProjects.toLowerCase()`, applies `aria-label="${contactAction.label} (contact)"`
- ✓ Actions container wraps with `flex flex-wrap items-center gap-4`

**Prerequisites:**
- M5.G5.T3 completed
- Target file: `src/components/home/hero-section.tsx`

**Implementation Details:**

Append the calls to action block to `src/components/home/hero-section.tsx`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$fullComponent = @'
import React from 'react';
import type { SiteConfig } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Button } from '@/components/ui/button';
import { ExternalLink } from '@/components/ui/external-link';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';
import type { HeroContactAction } from '@/lib/home/select-hero-action';

export interface HeroSectionProps {
  profile: SiteConfig['profile'];
  contactAction: HeroContactAction | null;
}

/**
 * Hero Section Component
 *
 * Orientation landmark rendering profile identity, concise positioning, and calls-to-action.
 * design.md Section 6.1 & Requirement 2, 3, 4. Server component by default (Req 1.2).
 */
export function HeroSection({ profile, contactAction }: HeroSectionProps): JSX.Element {
  // Disambiguate accessible name if secondary CTA label matches primary CTA
  const isLabelCollision =
    contactAction !== null &&
    contactAction.label.trim().toLowerCase() === HOME_TEXT.viewProjects.toLowerCase();

  const secondaryAriaLabel = isLabelCollision
    ? `${contactAction!.label} (contact)`
    : undefined;

  return (
    <section
      aria-labelledby="hero-heading"
      className="border-b border-border-default bg-page py-12 md:py-20"
    >
      <Container className="max-w-4xl">
        <h1
          id="hero-heading"
          className="text-heading-1 font-bold tracking-tight text-text-primary mb-2"
        >
          {profile.name}
        </h1>

        <p className="text-heading-3 font-semibold text-brand-primary mb-4">
          {profile.professionalTitle}
        </p>

        <p className="text-lead text-text-secondary mb-4 leading-relaxed">
          {profile.introduction}
        </p>

        <p className="text-small text-text-secondary flex items-center gap-1.5 mb-6">
          <svg
            className="h-4 w-4 shrink-0 text-text-secondary"
            aria-hidden="true"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span>{profile.location}</span>
        </p>

        {profile.availableForOpportunities && (
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface border border-border-default mb-8">
            <span
              className="h-2 w-2 rounded-full bg-feedback-success shrink-0"
              aria-hidden="true"
            />
            <span className="text-small font-medium text-text-primary">
              {HOME_TEXT.availability}
            </span>
          </div>
        )}

        {/* Hero Calls to Action */}
        <div className="flex flex-wrap items-center gap-4 pt-2">
          <Button variant="primary" size="lg" href="/projects">
            {HOME_TEXT.viewProjects}
          </Button>

          {contactAction && (
            <div>
              {contactAction.kind === 'external' ? (
                <ExternalLink
                  href={contactAction.url}
                  aria-label={secondaryAriaLabel}
                >
                  {contactAction.label}
                </ExternalLink>
              ) : (
                <Button
                  variant="secondary"
                  size="lg"
                  href={contactAction.url}
                  aria-label={secondaryAriaLabel}
                >
                  {contactAction.label}
                </Button>
              )}
            </div>
          )}
        </div>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\hero-section.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/hero-section.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.2, Req 3.3, Req 3.4, Req 3.5, Req 3.6, Req 13.3

---

### M5.G5.T5: Author Concrete Unit Scenarios for HeroSection (`tests/home/hero-section.test.tsx`)

**Objective:** Create `tests/home/hero-section.test.tsx` testing concrete rendering scenarios: name in `h1`, profile copy, primary CTA link, mailto vs external CTA, availability toggle, and absence of fallback strings.

**Acceptance Criteria:**
- ✓ File `tests/home/hero-section.test.tsx` created
- ✓ Verifies exactly one `<h1>` containing `profile.name`
- ✓ Verifies presence of professional title, introduction, and location
- ✓ Verifies primary action points to `/projects` with text "View Projects"
- ✓ Verifies secondary action renders `mailto:` without target
- ✓ Verifies availability indicator renders when `availableForOpportunities: true` and is omitted when `false`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G5.T4 completed
- Target file: `tests/home/hero-section.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/hero-section.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { HeroSection } from '@/components/home/hero-section';
import { sampleSiteConfig, unavailableSiteConfig } from '../fixtures/home-data';
import { selectHeroContactAction } from '@/lib/home/select-hero-action';

describe('HeroSection Component (Req 2, 3, 4)', () => {
  const contactAction = selectHeroContactAction(sampleSiteConfig.contactChannels);

  describe('Concrete Unit Scenarios', () => {
    it('renders single h1 containing profile name and full profile copy', () => {
      render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={contactAction}
        />
      );

      const headings = screen.getAllByRole('heading', { level: 1 });
      expect(headings.length).toBe(1);
      expect(headings[0].textContent).toBe('Angelo Andres');

      expect(screen.getByText('Pipeline Lead & Specification Architect')).toBeDefined();
      expect(screen.getByText(/I build specification-driven software/)).toBeDefined();
      expect(screen.getByText(/Taguig, National Capital Region, PH/)).toBeDefined();
    });

    it('renders primary CTA linking to /projects', () => {
      render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={contactAction}
        />
      );

      const primaryBtn = screen.getByRole('link', { name: 'View Projects' });
      expect(primaryBtn.getAttribute('href')).toBe('/projects');
    });

    it('renders secondary CTA as mailto button when primary contact channel is email', () => {
      render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={contactAction}
        />
      );

      const emailBtn = screen.getByRole('link', { name: 'Email Angelo' });
      expect(emailBtn.getAttribute('href')).toBe('mailto:hello@example.com');
      expect(emailBtn.getAttribute('target')).toBeNull();
    });

    it('renders availability indicator iff availableForOpportunities is true', () => {
      const { rerender } = render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={contactAction}
        />
      );
      expect(screen.getByText('Available for opportunities')).toBeDefined();

      rerender(
        <HeroSection
          profile={unavailableSiteConfig.profile}
          contactAction={contactAction}
        />
      );
      expect(screen.queryByText('Available for opportunities')).toBeNull();
    });

    it('omits secondary CTA when contactAction is null', () => {
      render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={null}
        />
      );

      expect(screen.getByRole('link', { name: 'View Projects' })).toBeDefined();
      expect(screen.queryByRole('link', { name: 'Email Angelo' })).toBeNull();
    });
  });
});
'@ | Set-Content "tests\home\hero-section.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/hero-section.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 3.1, Req 3.3, Req 3.4, Req 4.1, Req 4.2

---

### M5.G5.T6: Author Property-Based Test for HeroSection (Property 8)

**Objective:** Append property-based test in `tests/home/hero-section.test.tsx` validating Property 8 across generated profile objects and contact actions.

**Acceptance Criteria:**
- ✓ Implements Property 8 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 8: hero renders profile data and availability exactly as configured`
- ✓ Asserts single `<h1>` strictly equals `profile.name`
- ✓ Asserts title, introduction, and location are present in DOM
- ✓ Asserts "View Projects" link with `href="/projects"` is present
- ✓ Asserts secondary contact action present iff `contactAction !== null`
- ✓ Asserts availability text present iff `profile.availableForOpportunities === true`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G5.T5 completed
- Arbitraries in `tests/fixtures/home-arbitraries.ts`
- Target file: `tests/home/hero-section.test.tsx`

**Implementation Details:**

Append Property 8 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 8)', () => {
    it('Feature: m5-homepage-experience, Property 8: hero renders profile data and availability exactly as configured for any input', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbProfile } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          arbProfile,
          fc.constantFrom(
            null,
            { label: 'Contact Me', url: 'mailto:me@test.com', kind: 'mailto' as const },
            { label: 'LinkedIn', url: 'https://linkedin.com/in/test', kind: 'external' as const }
          ),
          (profile: any, action: any) => {
            cleanup();
            render(<HeroSection profile={profile} contactAction={action} />);

            // 1. Single h1 equals profile.name
            const h1Elements = screen.getAllByRole('heading', { level: 1 });
            expect(h1Elements.length).toBe(1);
            expect(h1Elements[0].textContent).toBe(profile.name);

            // 2. Profile metadata presence
            expect(screen.getByText(profile.professionalTitle)).toBeDefined();
            expect(screen.getByText(profile.introduction)).toBeDefined();
            expect(screen.getByText(profile.location)).toBeDefined();

            // 3. Primary CTA invariant
            const primaryLink = screen.getByRole('link', { name: 'View Projects' });
            expect(primaryLink.getAttribute('href')).toBe('/projects');

            // 4. Secondary CTA invariant
            if (action) {
              const secondaryLink = screen.getByRole('link', { name: new RegExp(action.label) });
              expect(secondaryLink.getAttribute('href')).toBe(action.url);
            }

            // 5. Availability indicator invariant
            if (profile.availableForOpportunities) {
              expect(screen.getByText('Available for opportunities')).toBeDefined();
            } else {
              expect(screen.queryByText('Available for opportunities')).toBeNull();
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\hero-section.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\hero-section.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/hero-section.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 3.1, Req 3.3, Req 3.4, Req 4.1, Req 4.2

---

### M5.G5.T7: Author Accessible Name Disambiguation Test for HeroSection

**Objective:** Append a unit test in `tests/home/hero-section.test.tsx` verifying that when a contact action label matches "View Projects" (case-insensitive), an `aria-label` suffix is attached to avoid duplicate accessible names within the section per Requirement 3.6.

**Acceptance Criteria:**
- ✓ Configures `contactAction = { label: 'View Projects', url: 'https://example.com', kind: 'external' }`
- ✓ Renders `HeroSection`
- ✓ Asserts secondary link has `aria-label="View Projects (contact)"`
- ✓ Confirms primary button accessible name remains "View Projects"
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G5.T6 completed
- Target file: `tests/home/hero-section.test.tsx`

**Implementation Details:**

Append collision test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Accessible Name Collision Disambiguation (Req 3.6)', () => {
    it('appends (contact) suffix to aria-label when secondary CTA label matches primary CTA', () => {
      const collidingAction = {
        label: 'View Projects',
        url: 'https://github.com/example',
        kind: 'external' as const,
      };

      render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={collidingAction}
        />
      );

      const secondaryLink = screen.getByRole('link', { name: 'View Projects (contact)' });
      expect(secondaryLink).toBeDefined();
      expect(secondaryLink.getAttribute('href')).toBe('https://github.com/example');

      const primaryLink = screen.getByRole('link', { name: 'View Projects' });
      expect(primaryLink.getAttribute('href')).toBe('/projects');
    });
  });
'@

$content = Get-Content "tests\home\hero-section.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\hero-section.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/hero-section.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6

---

### M5.G5.T8: Author Automated Axe Accessibility Test for HeroSection

**Objective:** Append automated axe test in `tests/home/hero-section.test.tsx` verifying WCAG 2.1 Level AA compliance across populated, unavailable, and no-contact states with zero violations.

**Acceptance Criteria:**
- ✓ Evaluates `HeroSection` using `axe` helper
- ✓ Tests standard populated state: 0 axe violations
- ✓ Tests unavailable state (`availableForOpportunities: false`): 0 axe violations
- ✓ Tests no-contact state (`contactAction: null`): 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `vitest-axe` installed
- Target file: `tests/home/hero-section.test.tsx`

**Implementation Details:**

Append axe accessibility tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Axe Accessibility Matrix (Req 14)', () => {
    it('reports zero axe violations across populated and edge configurations', async () => {
      const { axe } = require('vitest-axe');

      // 1. Full populated
      const { container: c1 } = render(
        <HeroSection
          profile={sampleSiteConfig.profile}
          contactAction={contactAction}
        />
      );
      expect((await axe(c1)).violations).toHaveLength(0);

      // 2. Unavailable & no contact
      const { container: c2 } = render(
        <HeroSection
          profile={unavailableSiteConfig.profile}
          contactAction={null}
        />
      );
      expect((await axe(c2)).violations).toHaveLength(0);
    });
  });
'@

$content = Get-Content "tests\home\hero-section.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\hero-section.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/hero-section.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.7

---

### M5.G5.T9: Verify Source Hygiene of `HeroSection`

**Objective:** Audit `src/components/home/hero-section.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file length strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ File length strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G5.T4 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\components\home\hero-section.tsx"
$content = Get-Content $file -Raw
$lines = (Get-Content $file).Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and ($lines -lt 300)) {
    "PASS"
} else {
    Write-Host "Hygiene violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 4.4, Req 14.8, Req 16.7, Req 16.8

---

### M5.G5.T10: Checkpoint — HeroSection Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `HeroSection`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs `hero-section.test.tsx` and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G5.T1 through M5.G5.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/hero-section.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/hero-section.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\home\hero-section.tsx"
Test-Path "tests\home\hero-section.test.tsx"
npm run typecheck
npm run test -- tests/home/hero-section.test.tsx
```
Expected output:
- `True` for both paths
- `npm run typecheck` exits with return code 0
- Vitest executes all hero section tests with return code 0.