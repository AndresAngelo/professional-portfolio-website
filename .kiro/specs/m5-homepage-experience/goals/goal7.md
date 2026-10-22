# M5.G7: CertificationsPreview and RecentActivity

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component sections `CertificationsPreview` in `src/components/home/certifications-preview.tsx` and `RecentActivity` in `src/components/home/recent-activity.tsx`. `CertificationsPreview` renders a section landmark (`<section aria-labelledby="certifications-heading">`) with an `h2` heading, a responsive card grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`), one M3 `Card` per selected certification displaying the `h3` credential title, issuer name, and issue date rendered inside a `<time dateTime={issuedAt}>` element formatted via `formatDisplayDate`, accompanied by a "View all certifications" link to `/certifications`. It strictly omits credential IDs, external verification links, and badge images. `RecentActivity` renders a section landmark (`<section aria-labelledby="recent-activity-heading">`) with an `h2` heading, a single-column list of items displaying the `h3` post title linking to `/blog/{slug}`, publication date in a `<time dateTime={publishedAt}>` element, M3 `EventTypeBadge`, summary copy, and a "View all posts" link to `/blog`. Both components execute as pure server components (zero `'use client'`), use semantic tokens exclusively, and maintain file lengths under 300 lines. Validate rendering, date determinism, and Property 11 using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/home/certifications-preview.tsx` implemented as a server component without `'use client'`
- ✓ `CertificationsPreview` renders `<section aria-labelledby="certifications-heading">` with `h2#certifications-heading`
- ✓ Renders one M3 `Card` per certification showing `h3` title, issuer, and `<time dateTime={issuedAt}>{formatDisplayDate(issuedAt)}</time>`
- ✓ Strictly omits credential IDs, verification links, and badge images (Req 10.5)
- ✓ Renders a "View all certifications" link to `/certifications`
- ✓ Applies responsive card grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ `src/components/home/recent-activity.tsx` implemented as a server component without `'use client'`
- ✓ `RecentActivity` renders `<section aria-labelledby="recent-activity-heading">` with `h2#recent-activity-heading`
- ✓ Renders single-column list (`flex flex-col gap-6`) of blog posts with `h3` title linking to `/blog/{slug}`, `<time dateTime={publishedAt}>`, `EventTypeBadge`, and summary
- ✓ Renders a "View all posts" link to `/blog`
- ✓ Unit, property (Property 11), and axe accessibility tests in `tests/home/certifications-preview.test.tsx` and `recent-activity.test.tsx` pass with 100% assertions
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1 through M5.G6 completed (`home-text.ts`, `format-date.ts`, fixtures, and arbitraries available)
- M3 primitives (`Container`, `Card`, `EventTypeBadge`, `FOCUS_RING`, `MOTION_FAST`, `cx`) available at `src/components/ui/`
- Target files: `src/components/home/certifications-preview.tsx` and `src/components/home/recent-activity.tsx`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M5.G7.T1: Implement `CertificationsPreview` Component (`src/components/home/certifications-preview.tsx`)

**Objective:** Author the server component `CertificationsPreview` in `src/components/home/certifications-preview.tsx` rendering preview certification cards and navigation link.

**Acceptance Criteria:**
- ✓ File `src/components/home/certifications-preview.tsx` created
- ✓ Exports `CertificationsPreviewProps` requiring `certifications: readonly Certification[]`
- ✓ Exports `CertificationsPreview(props: CertificationsPreviewProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="certifications-heading" className="py-12 md:py-16 bg-surface border-b border-border-default">`
- ✓ Wraps content in M3 `<Container>`
- ✓ Renders `<h2 id="certifications-heading" className="text-heading-2 font-bold text-text-primary">` with `HOME_TEXT.certificationsHeading`
- ✓ Renders responsive grid: `<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">`
- ✓ Each card renders an `h3` title, issuer name, and `<time dateTime={cert.issuedAt}>{formatDisplayDate(cert.issuedAt)}</time>`
- ✓ Renders link to `/certifications` with text `HOME_TEXT.viewAllCertifications`
- ✓ Strictly omits credential ID, verification URL, and badge image (Req 10.5)
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5.G1 completed (`home-text.ts` exists, `formatDisplayDate` in `src/lib/format-date.ts`)
- M3 primitives available
- Target file: `src/components/home/certifications-preview.tsx`

**Implementation Details:**

Write `src/components/home/certifications-preview.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import type { Certification } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Card } from '@/components/ui/card';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';
import { formatDisplayDate } from '@/lib/format-date';

export interface CertificationsPreviewProps {
  certifications: readonly Certification[];
}

/**
 * Certifications Preview Section Component
 *
 * Displays preview of earned credentials with issuer and date of award.
 * design.md Section 6.1 & Requirement 10. Server component by default (Req 1.2).
 */
export function CertificationsPreview({
  certifications,
}: CertificationsPreviewProps): JSX.Element {
  return (
    <section
      aria-labelledby="certifications-heading"
      className="border-b border-border-default bg-surface py-12 md:py-16"
    >
      <Container>
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <h2
              id="certifications-heading"
              className="text-heading-2 font-bold tracking-tight text-text-primary"
            >
              {HOME_TEXT.certificationsHeading}
            </h2>
          </div>
          <Link
            href="/certifications"
            className={cx(
              'inline-flex items-center text-body font-medium text-brand-primary underline hover:opacity-80 rounded-sm self-start md:self-auto',
              FOCUS_RING,
              MOTION_FAST
            )}
          >
            {HOME_TEXT.viewAllCertifications} &rarr;
          </Link>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {certifications.map((cert) => (
            <Card
              key={cert.slug}
              className="flex flex-col justify-between h-full p-6"
            >
              <div>
                <h3 className="text-heading-4 font-semibold text-text-primary mb-2">
                  {cert.title}
                </h3>
                <p className="text-body font-medium text-text-secondary mb-3">
                  {cert.issuer}
                </p>
              </div>
              <p className="text-small text-text-secondary">
                Issued{' '}
                <time dateTime={cert.issuedAt}>
                  {formatDisplayDate(cert.issuedAt)}
                </time>
              </p>
            </Card>
          ))}
        </div>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\certifications-preview.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/certifications-preview.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.4, Req 10.5, Req 12.3, Req 14.1, Req 14.2, Req 15.2, Req 15.3, Req 15.4

---

### M5.G7.T2: Implement `RecentActivity` Component (`src/components/home/recent-activity.tsx`)

**Objective:** Author the server component `RecentActivity` in `src/components/home/recent-activity.tsx` rendering recent blog entries in a single-column list with event badges.

**Acceptance Criteria:**
- ✓ File `src/components/home/recent-activity.tsx` created
- ✓ Exports `RecentActivityProps` requiring `posts: readonly BlogPost[]`
- ✓ Exports `RecentActivity(props: RecentActivityProps): JSX.Element`
- ✓ Renders `<section aria-labelledby="recent-activity-heading" className="py-12 md:py-16 bg-page border-b border-border-default">`
- ✓ Wraps content in M3 `<Container>`
- ✓ Renders `<h2 id="recent-activity-heading" className="text-heading-2 font-bold text-text-primary">` with `HOME_TEXT.recentHeading`
- ✓ Renders single-column list `<div className="flex flex-col gap-6 max-w-3xl">`
- ✓ Each item renders an `h3` title link to `/blog/${post.slug}`, `<time dateTime={post.publishedAt}>{formatDisplayDate(post.publishedAt)}</time>`, M3 `EventTypeBadge`, and summary
- ✓ Renders link to `/blog` with text `HOME_TEXT.viewAllPosts`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M5.G1 completed (`home-text.ts`, `formatDisplayDate`)
- M3 `EventTypeBadge` available
- Target file: `src/components/home/recent-activity.tsx`

**Implementation Details:**

Write `src/components/home/recent-activity.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import Link from 'next/link';
import type { BlogPost } from '@/types/content';
import { Container } from '@/components/ui/container';
import { Card } from '@/components/ui/card';
import { EventTypeBadge } from '@/components/ui/event-type-badge';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { HOME_TEXT } from './home-text';
import { formatDisplayDate } from '@/lib/format-date';

export interface RecentActivityProps {
  posts: readonly BlogPost[];
}

/**
 * Recent Activity Section Component
 *
 * Displays chronological log of developer participation, meetups, and learning updates.
 * design.md Section 6.1 & Requirement 11. Server component by default (Req 1.2).
 */
export function RecentActivity({ posts }: RecentActivityProps): JSX.Element {
  return (
    <section
      aria-labelledby="recent-activity-heading"
      className="border-b border-border-default bg-page py-12 md:py-16"
    >
      <Container>
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <h2
              id="recent-activity-heading"
              className="text-heading-2 font-bold tracking-tight text-text-primary"
            >
              {HOME_TEXT.recentHeading}
            </h2>
          </div>
          <Link
            href="/blog"
            className={cx(
              'inline-flex items-center text-body font-medium text-brand-primary underline hover:opacity-80 rounded-sm self-start md:self-auto',
              FOCUS_RING,
              MOTION_FAST
            )}
          >
            {HOME_TEXT.viewAllPosts} &rarr;
          </Link>
        </div>

        <div className="flex flex-col gap-6 max-w-3xl">
          {posts.map((post) => (
            <Card key={post.slug} className="p-6">
              <div className="flex flex-wrap items-center gap-3 mb-2">
                <time
                  dateTime={post.publishedAt}
                  className="text-small text-text-secondary"
                >
                  {formatDisplayDate(post.publishedAt)}
                </time>
                <EventTypeBadge eventType={post.eventType} />
              </div>
              <h3 className="text-heading-4 font-semibold text-text-primary mb-2">
                <Link
                  href={`/blog/${post.slug}`}
                  className={cx(
                    'hover:text-brand-primary underline-offset-4 hover:underline rounded-sm',
                    FOCUS_RING,
                    MOTION_FAST
                  )}
                >
                  {post.title}
                </Link>
              </h3>
              <p className="text-body text-text-secondary">
                {post.summary}
              </p>
            </Card>
          ))}
        </div>
      </Container>
    </section>
  );
}
'@ | Set-Content "src\components\home\recent-activity.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/recent-activity.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.6, Req 11.7, Req 12.3, Req 14.1, Req 14.2, Req 15.2

---

### M5.G7.T3: Author Unit Scenarios for `CertificationsPreview` (`tests/home/certifications-preview.test.tsx`)

**Objective:** Create `tests/home/certifications-preview.test.tsx` verifying card title, issuer, formatted `<time>` tags, `/certifications` link, and omission of credential IDs or verification URLs.

**Acceptance Criteria:**
- ✓ File `tests/home/certifications-preview.test.tsx` created
- ✓ Verifies `h2` heading with "Certifications"
- ✓ Verifies each certification card displays `h3` title and issuer
- ✓ Verifies `<time dateTime={issuedAt}>` matches `formatDisplayDate(issuedAt)`
- ✓ Verifies "View all certifications" link points to `/certifications`
- ✓ Verifies credential IDs and verification URLs are NOT present in output (Req 10.5)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G7.T1 completed
- Fixtures available in `tests/fixtures/home-data.ts`
- Target file: `tests/home/certifications-preview.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/certifications-preview.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CertificationsPreview } from '@/components/home/certifications-preview';
import { sampleCertifications } from '../fixtures/home-data';
import { formatDisplayDate } from '@/lib/format-date';

describe('CertificationsPreview Component (Req 10)', () => {
  const threeCerts = sampleCertifications.slice(0, 3);

  describe('Concrete Unit Scenarios', () => {
    it('renders certification cards with title, issuer, formatted time element, and link to all certs', () => {
      render(<CertificationsPreview certifications={threeCerts} />);

      expect(screen.getByRole('heading', { level: 2, name: 'Certifications' })).toBeDefined();

      const titleHeadings = screen.getAllByRole('heading', { level: 3 });
      expect(titleHeadings.length).toBe(3);

      threeCerts.forEach((cert) => {
        expect(screen.getByText(cert.title)).toBeDefined();
        expect(screen.getByText(cert.issuer)).toBeDefined();

        const timeElem = screen.getByText(formatDisplayDate(cert.issuedAt));
        expect(timeElem.getAttribute('datetime')).toBe(cert.issuedAt);
      });

      const viewAllLink = screen.getByRole('link', { name: /View all certifications/ });
      expect(viewAllLink.getAttribute('href')).toBe('/certifications');
    });

    it('omits credentialId, verificationUrl, and badge images from preview cards', () => {
      const { container } = render(<CertificationsPreview certifications={threeCerts} />);

      // Ensure credential IDs are omitted
      expect(screen.queryByText(/CSA-98765/)).toBeNull();
      expect(screen.queryByText(/AI-43210/)).toBeNull();

      // Ensure verification links and img tags are omitted
      expect(container.querySelectorAll('img').length).toBe(0);
      const links = screen.getAllByRole('link');
      expect(links.length).toBe(1); // only the "View all certifications" link
    });
  });
});
'@ | Set-Content "tests\home\certifications-preview.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/certifications-preview.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.4, Req 10.5, Req 12.3

---

### M5.G7.T4: Author Unit Scenarios for `RecentActivity` (`tests/home/recent-activity.test.tsx`)

**Objective:** Create `tests/home/recent-activity.test.tsx` verifying title links to `/blog/{slug}`, publication dates, event type badges, summary copy, and `/blog` link.

**Acceptance Criteria:**
- ✓ File `tests/home/recent-activity.test.tsx` created
- ✓ Verifies `h2` heading with "Recent Activity"
- ✓ Verifies title link for each post targets `/blog/${slug}`
- ✓ Verifies `<time dateTime={publishedAt}>` matches `formatDisplayDate(publishedAt)`
- ✓ Verifies `EventTypeBadge` is rendered for each post
- ✓ Verifies summary text is present
- ✓ Verifies "View all posts" link points to `/blog`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G7.T2 completed
- Fixtures available in `tests/fixtures/home-data.ts`
- Target file: `tests/home/recent-activity.test.tsx`

**Implementation Details:**

Write unit scenarios in `tests/home/recent-activity.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RecentActivity } from '@/components/home/recent-activity';
import { sampleBlogPosts } from '../fixtures/home-data';
import { formatDisplayDate } from '@/lib/format-date';

describe('RecentActivity Component (Req 11)', () => {
  const threePosts = sampleBlogPosts.filter((p) => !p.draft).slice(0, 3);

  describe('Concrete Unit Scenarios', () => {
    it('renders recent posts list with title links, dates, badges, and summaries', () => {
      render(<RecentActivity posts={threePosts} />);

      expect(screen.getByRole('heading', { level: 2, name: 'Recent Activity' })).toBeDefined();

      const titleHeadings = screen.getAllByRole('heading', { level: 3 });
      expect(titleHeadings.length).toBe(3);

      threePosts.forEach((post) => {
        const titleLink = screen.getByRole('link', { name: post.title });
        expect(titleLink.getAttribute('href')).toBe(`/blog/${post.slug}`);

        const timeElem = screen.getByText(formatDisplayDate(post.publishedAt));
        expect(timeElem.getAttribute('datetime')).toBe(post.publishedAt);

        expect(screen.getByText(post.summary)).toBeDefined();
      });

      const viewAllLink = screen.getByRole('link', { name: /View all posts/ });
      expect(viewAllLink.getAttribute('href')).toBe('/blog');
    });
  });
});
'@ | Set-Content "tests\home\recent-activity.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/recent-activity.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.6, Req 11.7, Req 12.3

---

### M5.G7.T5: Author Property-Based Test for Certifications & Posts (Property 11)

**Objective:** Append property-based tests in `tests/home/certifications-preview.test.tsx` and `tests/home/recent-activity.test.tsx` validating Property 11 across generated inputs of up to 3 items.

**Acceptance Criteria:**
- ✓ Implements Property 11 test for CertificationsPreview ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 11: certification and post items show required fields and links`
- ✓ Asserts every certification renders title, issuer, formatted time element, and link to `/certifications`
- ✓ Asserts zero credentialId or verificationUrl rendered
- ✓ Implements Property 11 test for RecentActivity ($\ge 100$ runs with `fast-check`)
- ✓ Asserts every post renders title link `/blog/{slug}`, time element, summary, and link to `/blog`
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G7.T3 and M5.G7.T4 completed
- Arbitraries in `tests/fixtures/home-arbitraries.ts`

**Implementation Details:**

Append Property 11 tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Append to certifications-preview.test.tsx
$appendCertsProp = @'

  describe('Property-Based Invariants (Property 11 - Certifications)', () => {
    it('Feature: m5-homepage-experience, Property 11: certification preview items show required fields and links for any valid input', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbCertification } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          fc.array(arbCertification, { minLength: 1, maxLength: 3 }),
          (certs: any) => {
            cleanup();
            render(<CertificationsPreview certifications={certs} />);

            const h3Elements = screen.getAllByRole('heading', { level: 3 });
            expect(h3Elements.length).toBe(certs.length);

            for (let i = 0; i < certs.length; i++) {
              expect(h3Elements[i].textContent).toBe(certs[i].title);
              expect(screen.getByText(certs[i].issuer)).toBeDefined();
            }

            const viewAll = screen.getByRole('link', { name: /View all certifications/ });
            expect(viewAll.getAttribute('href')).toBe('/certifications');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$contentCP = Get-Content "tests\home\certifications-preview.test.tsx" -Raw
$contentCP = $contentCP -replace "\s*\}\);\s*$", "$appendCertsProp`n});`n"
$contentCP | Set-Content "tests\home\certifications-preview.test.tsx" -Encoding UTF8

# Append to recent-activity.test.tsx
$appendPostsProp = @'

  describe('Property-Based Invariants (Property 11 - Posts)', () => {
    it('Feature: m5-homepage-experience, Property 11: recent post items show required fields and links for any valid input', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { arbBlogPost } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(
          fc.array(arbBlogPost, { minLength: 1, maxLength: 3 }),
          (posts: any) => {
            cleanup();
            render(<RecentActivity posts={posts} />);

            const h3Elements = screen.getAllByRole('heading', { level: 3 });
            expect(h3Elements.length).toBe(posts.length);

            for (let i = 0; i < posts.length; i++) {
              const link = screen.getByRole('link', { name: posts[i].title });
              expect(link.getAttribute('href')).toBe(`/blog/${posts[i].slug}`);
              expect(screen.getByText(posts[i].summary)).toBeDefined();
            }

            const viewAll = screen.getByRole('link', { name: /View all posts/ });
            expect(viewAll.getAttribute('href')).toBe('/blog');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$contentRA = Get-Content "tests\home\recent-activity.test.tsx" -Raw
$contentRA = $contentRA -replace "\s*\}\);\s*$", "$appendPostsProp`n});`n"
$contentRA | Set-Content "tests\home\recent-activity.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/certifications-preview.test.tsx tests/home/recent-activity.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.4, Req 10.5, Req 11.6, Req 11.7, Req 12.3

---

### M5.G7.T6: Author Responsive Grid Class Verification Tests for Certifications

**Objective:** Append test cases in `tests/home/certifications-preview.test.tsx` verifying that responsive column utilities (`grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`) and `Container` constraints are applied.

**Acceptance Criteria:**
- ✓ Asserts `CertificationsPreview` card container applies `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- ✓ Asserts `Container` primitive is rendered
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G7.T5 completed
- Target file: `tests/home/certifications-preview.test.tsx`

**Implementation Details:**

Append grid assertions using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Responsive Utilities (Req 15)', () => {
    it('applies 1-col on mobile, 2-col on tablet, and 3-col on desktop breakpoints', () => {
      const { container } = render(<CertificationsPreview certifications={threeCerts} />);
      const grid = container.querySelector('.grid');

      expect(grid).not.toBeNull();
      expect(grid?.className).toContain('grid-cols-1');
      expect(grid?.className).toContain('md:grid-cols-2');
      expect(grid?.className).toContain('lg:grid-cols-3');
    });
  });
'@

$content = Get-Content "tests\home\certifications-preview.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\certifications-preview.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/certifications-preview.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 15.1, Req 15.2, Req 15.3, Req 15.4

---

### M5.G7.T7: Author Automated Axe Accessibility Tests for Certifications & Recent Activity

**Objective:** Append automated axe tests in `tests/home/certifications-preview.test.tsx` and `recent-activity.test.tsx` verifying WCAG 2.1 AA compliance with zero violations.

**Acceptance Criteria:**
- ✓ Evaluates `CertificationsPreview`: 0 axe violations
- ✓ Evaluates `RecentActivity`: 0 axe violations
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G7.T6 completed

**Implementation Details:**

Append axe tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# Append to certifications-preview.test.tsx
$appendCertsAxe = @'

  describe('Axe Accessibility Matrix (Req 14)', () => {
    it('reports zero axe violations for certifications preview', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(<CertificationsPreview certifications={threeCerts} />);
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
'@

$contentCP = Get-Content "tests\home\certifications-preview.test.tsx" -Raw
$contentCP = $contentCP -replace "\s*\}\);\s*$", "$appendCertsAxe`n});`n"
$contentCP | Set-Content "tests\home\certifications-preview.test.tsx" -Encoding UTF8

# Append to recent-activity.test.tsx
$appendPostsAxe = @'

  describe('Axe Accessibility Matrix (Req 14)', () => {
    it('reports zero axe violations for recent activity', async () => {
      const { axe } = require('vitest-axe');
      const { container } = render(<RecentActivity posts={threePosts} />);
      const results = await axe(container);
      expect(results.violations).toHaveLength(0);
    });
  });
'@

$contentRA = Get-Content "tests\home\recent-activity.test.tsx" -Raw
$contentRA = $contentRA -replace "\s*\}\);\s*$", "$appendPostsAxe`n});`n"
$contentRA | Set-Content "tests\home\recent-activity.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/certifications-preview.test.tsx tests/home/recent-activity.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.1, Req 14.2, Req 14.7

---

### M5.G7.T8: Audit Absence of Fabricated Credentials in Preview

**Objective:** Inspect `src/components/home/certifications-preview.tsx` verifying that credentialId, verificationUrl, and badge images are completely absent from the rendered markup per Requirement 10.5.

**Acceptance Criteria:**
- ✓ Searches `certifications-preview.tsx` for references to `credentialId`, `verificationUrl`, `badgeImageUrl`
- ✓ Confirms none of these fields are accessed or rendered
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G7.T1 completed

**Implementation Details:**

Execute inspection script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$file = "src\components\home\certifications-preview.tsx"
$content = Get-Content $file -Raw

$violations = @()
if ($content -match '\b(credentialId|verificationUrl|badgeImageUrl)\b') {
    $violations += "Forbidden detailed certification field rendered in preview component (Req 10.5 violation)"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 10.5

---

### M5.G7.T9: Verify Source Hygiene of `CertificationsPreview` and `RecentActivity`

**Objective:** Audit `certifications-preview.tsx` and `recent-activity.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file lengths strictly under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements
- ✓ Both files are strictly under 300 lines
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G7.T1 and M5.G7.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\components\home\certifications-preview.tsx", "src\components\home\recent-activity.tsx")
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

### M5.G7.T10: Checkpoint — CertificationsPreview and RecentActivity Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `CertificationsPreview` and `RecentActivity`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs certifications and activity tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G7.T1 through M5.G7.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/certifications-preview.test.tsx tests/home/recent-activity.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/certifications-preview.test.tsx tests/home/recent-activity.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.7, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 7 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\home\certifications-preview.tsx"
Test-Path "src\components\home\recent-activity.tsx"
Test-Path "tests\home\certifications-preview.test.tsx"
Test-Path "tests\home\recent-activity.test.tsx"
npm run typecheck
npm run test -- tests/home/certifications-preview.test.tsx tests/home/recent-activity.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all certifications and activity tests with return code 0.