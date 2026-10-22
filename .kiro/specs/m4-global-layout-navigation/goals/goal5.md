# M4.G5: ContactLinks and SiteFooter

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component `ContactLinks` primitive in `src/components/layout/contact-links.tsx` and the global `SiteFooter` component in `src/components/layout/site-footer.tsx`. `ContactLinks` renders a clean unordered list (`<ul>`) of public contact channels ordered via `orderContactChannels`, rendering email channels as plain `mailto:` anchors and non-email channels using M3's `ExternalLink` component, strictly avoiding forms, inputs, textareas, and `#` placeholder links. `SiteFooter` provides a three-column responsive grid (`grid-cols-1 md:grid-cols-3`) containing the secondary site navigation (`aria-label="Footer"`), public professional profiles (rendered as `ExternalLink` items), and the public contact region wrapped in an accessible `<section id="contact">` landmark. Enforce that empty collections are completely omitted rather than rendered with empty containers, and render the copyright year at build time without client JavaScript via an injectable `year` prop. Validate all states and properties (Property 8, 9, 10) using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/layout/contact-links.tsx` implemented as a server component without `'use client'`
- ✓ `ContactLinks` renders list items ordered by `orderContactChannels` (primary channels first)
- ✓ Email channels render as `<a href="mailto:...">` with `FOCUS_RING` and no `target` attribute
- ✓ Non-email channels render via M3 `ExternalLink` (`target="_blank"`, `rel="noopener noreferrer"`)
- ✓ Contains zero forms, inputs, textareas, submit buttons, or `#` placeholder links (Req 9.6, 9.7)
- ✓ `src/components/layout/site-footer.tsx` implemented as a server component without `'use client'`
- ✓ `SiteFooter` renders copyright line `© {year} {profileName}` at build time with an injectable `year` prop (defaults to `new Date().getFullYear()`)
- ✓ Social links list and heading are completely omitted when `socialLinks` is empty
- ✓ Contact section (`<section id="contact">`), heading, and `ContactLinks` are completely omitted when renderable channels are empty
- ✓ Secondary navigation renders all `SiteConfig.navigation` items using `Link` with `aria-label="Footer"`
- ✓ `tests/unit/components/layout/contact-links.test.tsx` and `site-footer.test.tsx` pass with 100% assertions
- ✓ Property 8, Property 9, and Property 10 tests pass $\ge 100$ runs with `fast-check`

## Prerequisites

- Goals M4.G1 and M4.G2 completed (`contact-channels.ts`, `layout-text.ts` available)
- M3 primitives (`Container`, `ExternalLink`, `FOCUS_RING`, `MOTION_FAST`, `cx`, `resolveExternalHref`) available at `src/components/ui/`
- Test fixtures available at `tests/fixtures/site-config.ts`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M4.G5.T1: Implement `ContactLinks` Component (`src/components/layout/contact-links.tsx`)

**Objective:** Author the server component `ContactLinks` in `src/components/layout/contact-links.tsx` rendering ordered, safe contact channels.

**Acceptance Criteria:**
- ✓ File `src/components/layout/contact-links.tsx` created
- ✓ Exports `ContactLinksProps` interface accepting `channels: readonly ContactChannel[]` and optional `className?: string`
- ✓ Exports `ContactLinks(props: ContactLinksProps): JSX.Element | null`
- ✓ Filters channels using `getRenderableChannels` and sorts using `orderContactChannels`
- ✓ Returns `null` if ordered renderable channels array is empty
- ✓ Renders `<ul className="flex flex-col gap-2 list-none p-0 m-0">`
- ✓ Email channel renders native `<a>` with `href="mailto:..."`, `FOCUS_RING`, and no `target`
- ✓ Non-email channel renders `<ExternalLink href={url}>{label}</ExternalLink>`
- ✓ Contains zero forms, inputs, textareas, or submit buttons
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G2 completed (`contact-channels.ts` exists)
- M3 `ExternalLink` available
- Target file: `src/components/layout/contact-links.tsx`

**Implementation Details:**

Write `src/components/layout/contact-links.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import type { ContactChannel } from '@/types/content';
import { ExternalLink } from '@/components/ui/external-link';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { getRenderableChannels, orderContactChannels } from './contact-channels';

export interface ContactLinksProps {
  channels: readonly ContactChannel[];
  className?: string;
}

/**
 * ContactLinks Component
 *
 * Renders verified public communication channels with zero visitor data collection.
 * AGENTS.md 4.2 & Requirement 9. Server component by default (Req 9.8).
 */
export function ContactLinks({ channels, className }: ContactLinksProps): JSX.Element | null {
  const renderable = getRenderableChannels(channels);
  if (renderable.length === 0) {
    return null;
  }

  const ordered = orderContactChannels(renderable);

  return (
    <ul className={cx('flex flex-col gap-2 list-none p-0 m-0', className)}>
      {ordered.map((channel) => {
        const isEmail = channel.type === 'email';
        return (
          <li key={`${channel.type}-${channel.url}`}>
            {isEmail ? (
              <a
                href={channel.url}
                className={cx(
                  'inline-flex items-center text-body text-brand-primary underline hover:opacity-80 rounded-sm',
                  FOCUS_RING,
                  MOTION_FAST
                )}
              >
                {channel.label}
              </a>
            ) : (
              <ExternalLink href={channel.url}>
                {channel.label}
              </ExternalLink>
            )}
          </li>
        );
      })}
    </ul>
  );
}
'@ | Set-Content "src\components\layout\contact-links.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/layout/contact-links.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3, Req 9.4, Req 9.5, Req 9.6, Req 9.7, Req 9.8

---

### M4.G5.T2: Implement `SiteFooter` Component (`src/components/layout/site-footer.tsx`)

**Objective:** Author the server component `SiteFooter` in `src/components/layout/site-footer.tsx` with responsive layout, secondary navigation, social links, contact region, and build-time copyright.

**Acceptance Criteria:**
- ✓ File `src/components/layout/site-footer.tsx` created
- ✓ Exports `SiteFooterProps` interface with `profileName`, `navigation`, `socialLinks`, `contactChannels`, and optional `year?: number`
- ✓ Exports `SiteFooter(props: SiteFooterProps): JSX.Element`
- ✓ Root renders `<footer className="border-t border-border-default bg-surface">`
- ✓ Wraps content in `<Container className="py-12">`
- ✓ Renders 3-column responsive grid: `<div className="grid grid-cols-1 gap-8 md:grid-cols-3">`
- ✓ Column 1 renders secondary navigation: `<nav aria-label="Footer">` with `h2` "Site"
- ✓ Column 2 renders social links filtered via `resolveExternalHref` with `h2` "Profiles"; omitted completely if empty
- ✓ Column 3 renders `<section id="contact" aria-labelledby="footer-contact-heading">` with `h2` "Contact" and `<ContactLinks>`; omitted completely if empty
- ✓ Copyright line renders `© {year} {profileName}` where `year` defaults to `new Date().getFullYear()`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G5.T1 completed (`ContactLinks` available)
- M3 `Container`, `ExternalLink`, `resolveExternalHref` available
- Target file: `src/components/layout/site-footer.tsx`

**Implementation Details:**

Write `src/components/layout/site-footer.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import Link from 'next/link';
import type { SiteConfig } from '@/types/content';
import { Container } from '@/components/ui/container';
import { ExternalLink } from '@/components/ui/external-link';
import { resolveExternalHref } from '@/components/ui/external-link-attrs';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import { ContactLinks } from './contact-links';
import { getRenderableChannels } from './contact-channels';
import {
  CONTACT_REGION_ID,
  FOOTER_NAV_LABEL,
  FOOTER_SITE_HEADING,
  FOOTER_SOCIAL_HEADING,
  FOOTER_CONTACT_HEADING,
} from './layout-text';

export interface SiteFooterProps {
  profileName: SiteConfig['profile']['name'];
  navigation: SiteConfig['navigation'];
  socialLinks: SiteConfig['socialLinks'];
  contactChannels: SiteConfig['contactChannels'];
  /** Optional injectable year for deterministic testing (defaults to build year) */
  year?: number;
}

/**
 * Global SiteFooter Component
 *
 * Provides site directory, verified social profiles, contact channels, and copyright.
 * design.md Section 4.2 & Requirement 8. Server component by default (Req 8.9).
 */
export function SiteFooter({
  profileName,
  navigation,
  socialLinks,
  contactChannels,
  year = new Date().getFullYear(),
}: SiteFooterProps): JSX.Element {
  const validSocialLinks = socialLinks.filter((s) => resolveExternalHref(s.url) !== null);
  const hasContact = getRenderableChannels(contactChannels).length > 0;

  return (
    <footer className="border-t border-border-default bg-surface">
      <Container className="py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {/* Column 1: Secondary Site Navigation */}
          <nav aria-label={FOOTER_NAV_LABEL}>
            <h2 className="text-small font-semibold text-text-primary uppercase tracking-wider mb-3">
              {FOOTER_SITE_HEADING}
            </h2>
            <ul className="flex flex-col gap-2 list-none p-0 m-0">
              {navigation.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={cx(
                      'text-body text-brand-primary underline hover:opacity-80 rounded-sm',
                      FOCUS_RING,
                      MOTION_FAST
                    )}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Column 2: External Social Profiles */}
          {validSocialLinks.length > 0 && (
            <section aria-labelledby="footer-social-heading">
              <h2
                id="footer-social-heading"
                className="text-small font-semibold text-text-primary uppercase tracking-wider mb-3"
              >
                {FOOTER_SOCIAL_HEADING}
              </h2>
              <ul className="flex flex-col gap-2 list-none p-0 m-0">
                {validSocialLinks.map((social) => (
                  <li key={`${social.label}-${social.url}`}>
                    <ExternalLink href={social.url}>
                      {social.label}
                    </ExternalLink>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Column 3: Contact Channels Region */}
          {hasContact && (
            <section
              id={CONTACT_REGION_ID}
              aria-labelledby="footer-contact-heading"
            >
              <h2
                id="footer-contact-heading"
                className="text-small font-semibold text-text-primary uppercase tracking-wider mb-3"
              >
                {FOOTER_CONTACT_HEADING}
              </h2>
              <ContactLinks channels={contactChannels} />
            </section>
          )}
        </div>

        {/* Build-Time Static Copyright */}
        <p className="mt-8 border-t border-border-default pt-6 text-small text-text-secondary">
          &copy; {year} {profileName}
        </p>
      </Container>
    </footer>
  );
}
'@ | Set-Content "src\components\layout\site-footer.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/layout/site-footer.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5, Req 8.6, Req 8.7, Req 8.8, Req 8.9, Req 12.2, Req 12.3

---

### M4.G5.T3: Author Unit Tests for `ContactLinks` (`tests/unit/components/layout/contact-links.test.tsx`)

**Objective:** Create `tests/unit/components/layout/contact-links.test.tsx` verifying email vs external link rendering, priority ordering, empty array suppression, and absence of form controls.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/contact-links.test.tsx` created
- ✓ Email channel renders `mailto:` anchor without `target` attribute
- ✓ LinkedIn and GitHub channels render with `target="_blank"` and `rel="noopener noreferrer"`
- ✓ Primary channel is listed first in DOM list items
- ✓ Returns `null` and renders nothing when `channels` is empty `[]`
- ✓ Asserts zero `<form>`, `<input>`, or `<textarea>` elements in the output
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G5.T1 completed
- Target file: `tests/unit/components/layout/contact-links.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/contact-links.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ContactLinks } from '@/components/layout/contact-links';
import { validSiteConfig } from '../../../fixtures/site-config';

describe('ContactLinks Component (Req 9)', () => {
  it('renders email as mailto: link without target and other channels as external links', () => {
    render(<ContactLinks channels={validSiteConfig.contactChannels} />);

    // Email link check
    const emailLink = screen.getByRole('link', { name: 'Email Angelo' });
    expect(emailLink.getAttribute('href')).toBe('mailto:hello@example.com');
    expect(emailLink.getAttribute('target')).toBeNull();

    // External link check
    const linkedinLink = screen.getByRole('link', { name: /LinkedIn Profile/ });
    expect(linkedinLink.getAttribute('href')).toBe('https://linkedin.com/in/example');
    expect(linkedinLink.getAttribute('target')).toBe('_blank');
    expect(linkedinLink.getAttribute('rel')).toBe('noopener noreferrer');
  });

  it('orders primary channel first in DOM order', () => {
    render(<ContactLinks channels={validSiteConfig.contactChannels} />);
    const listItems = screen.getAllByRole('listitem');

    expect(listItems[0].textContent).toContain('Email Angelo');
  });

  it('returns null and suppresses DOM output when channels array is empty', () => {
    const { container } = render(<ContactLinks channels={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('guarantees zero forms, inputs, or textareas exist in rendered output', () => {
    const { container } = render(<ContactLinks channels={validSiteConfig.contactChannels} />);
    expect(container.querySelectorAll('form').length).toBe(0);
    expect(container.querySelectorAll('input').length).toBe(0);
    expect(container.querySelectorAll('textarea').length).toBe(0);
    expect(container.querySelectorAll('button').length).toBe(0);
  });
});
'@ | Set-Content "tests\unit\components\layout\contact-links.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/contact-links.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3, Req 9.4, Req 9.5, Req 9.6, Req 9.7, Req 15.1

---

### M4.G5.T4: Author Property-Based Test for `ContactLinks` (Property 8)

**Objective:** Append property-based test in `tests/unit/components/layout/contact-links.test.tsx` using `fast-check` to assert Property 8: for any generated contact channels array, links render correct safe markup without `#` placeholders or forms.

**Acceptance Criteria:**
- ✓ Implements Property 8 test ($\ge 100$ runs with `fast-check`)
- ✓ Asserts every email channel renders `mailto:` and no `target`
- ✓ Asserts every non-email channel renders `target="_blank"` and `rel="noopener noreferrer"`
- ✓ Asserts zero hrefs equal `#`
- ✓ Asserts zero form controls exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/layout/contact-links.test.tsx`

**Implementation Details:**

Append Property 8 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 8)', () => {
    it('Feature: m4-global-layout-navigation, Property 8: contact links render safe, correct markup for any contact channels array', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { contactChannelArbitrary } = require('../../../fixtures/site-config-arbitraries');
      const { getRenderableChannels } = require('@/components/layout/contact-channels');

      fc.assert(
        fc.property(
          fc.array(contactChannelArbitrary, { minLength: 1, maxLength: 8 }),
          (channels: any) => {
            cleanup();
            const { container } = render(<ContactLinks channels={channels} />);
            const renderable = getRenderableChannels(channels);

            if (renderable.length === 0) {
              expect(container.firstChild).toBeNull();
              return;
            }

            const links = container.querySelectorAll('a');
            expect(links.length).toBe(renderable.length);

            links.forEach((a: HTMLAnchorElement) => {
              const href = a.getAttribute('href') || '';
              expect(href).not.toBe('#');

              if (href.startsWith('mailto:')) {
                expect(a.getAttribute('target')).toBeNull();
              } else {
                expect(a.getAttribute('target')).toBe('_blank');
                expect(a.getAttribute('rel')).toBe('noopener noreferrer');
              }
            });

            expect(container.querySelectorAll('form, input, textarea, button').length).toBe(0);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\contact-links.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\contact-links.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/contact-links.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.3, Req 9.6, Req 9.7, Req 15.1

---

### M4.G5.T5: Author Unit Tests for `SiteFooter` Rendering (`tests/unit/components/layout/site-footer.test.tsx`)

**Objective:** Create `tests/unit/components/layout/site-footer.test.tsx` verifying copyright, secondary navigation, social links, contact section, and empty-state omissions.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/site-footer.test.tsx` created
- ✓ Verifies copyright displays injected `year` and `profileName`
- ✓ Verifies `<nav aria-label="Footer">` renders all navigation links
- ✓ Verifies social links render with external security attributes
- ✓ Verifies `<section id="contact">` is present when renderable channels exist
- ✓ Verifies social section is omitted when `socialLinks` is empty
- ✓ Verifies contact section is omitted when `contactChannels` is empty
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G5.T2 completed
- Target file: `tests/unit/components/layout/site-footer.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/site-footer.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SiteFooter } from '@/components/layout/site-footer';
import {
  validSiteConfig,
  emptyContactChannelsSiteConfig,
  emptySocialLinksSiteConfig,
} from '../../../fixtures/site-config';

describe('SiteFooter Component (Req 8)', () => {
  it('renders copyright with injected year and profileName', () => {
    render(
      <SiteFooter
        profileName={validSiteConfig.profile.name}
        navigation={validSiteConfig.navigation}
        socialLinks={validSiteConfig.socialLinks}
        contactChannels={validSiteConfig.contactChannels}
        year={2026}
      />
    );

    const copyright = screen.getByText(/© 2026 Angelo Andres/);
    expect(copyright).toBeDefined();
  });

  it('renders secondary navigation with aria-label="Footer"', () => {
    render(
      <SiteFooter
        profileName={validSiteConfig.profile.name}
        navigation={validSiteConfig.navigation}
        socialLinks={validSiteConfig.socialLinks}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const footerNav = screen.getByRole('navigation', { name: 'Footer' });
    expect(footerNav).toBeDefined();

    validSiteConfig.navigation.forEach((item) => {
      expect(screen.getByRole('link', { name: item.label })).toBeDefined();
    });
  });

  it('renders #contact section landmark when renderable channels exist', () => {
    const { container } = render(
      <SiteFooter
        profileName={validSiteConfig.profile.name}
        navigation={validSiteConfig.navigation}
        socialLinks={validSiteConfig.socialLinks}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const contactSection = container.querySelector('#contact');
    expect(contactSection).not.toBeNull();
    expect(contactSection?.getAttribute('aria-labelledby')).toBe('footer-contact-heading');
  });

  it('omits social section when socialLinks array is empty', () => {
    const { container } = render(
      <SiteFooter
        profileName={emptySocialLinksSiteConfig.profile.name}
        navigation={emptySocialLinksSiteConfig.navigation}
        socialLinks={emptySocialLinksSiteConfig.socialLinks}
        contactChannels={emptySocialLinksSiteConfig.contactChannels}
      />
    );

    expect(container.querySelector('#footer-social-heading')).toBeNull();
  });

  it('omits #contact section when contactChannels array is empty', () => {
    const { container } = render(
      <SiteFooter
        profileName={emptyContactChannelsSiteConfig.profile.name}
        navigation={emptyContactChannelsSiteConfig.navigation}
        socialLinks={emptyContactChannelsSiteConfig.socialLinks}
        contactChannels={emptyContactChannelsSiteConfig.contactChannels}
      />
    );

    expect(container.querySelector('#contact')).toBeNull();
    expect(container.querySelector('#footer-contact-heading')).toBeNull();
  });
});
'@ | Set-Content "tests\unit\components\layout\site-footer.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-footer.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5, Req 8.6, Req 8.7, Req 15.1, Req 15.5

---

### M4.G5.T6: Author Property-Based Test for Footer Content Derivation (Property 9)

**Objective:** Append property-based test in `tests/unit/components/layout/site-footer.test.tsx` using `fast-check` verifying Property 9: copyright, footer nav links, and social links derive strictly from input props.

**Acceptance Criteria:**
- ✓ Implements Property 9 test ($\ge 100$ runs with `fast-check`)
- ✓ Asserts copyright text strictly contains randomized year and profileName
- ✓ Asserts every navigation item has a corresponding link with identical label and href
- ✓ Asserts every valid HTTPS social link has a corresponding external link
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/layout/site-footer.test.tsx`

**Implementation Details:**

Append Property 9 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 9)', () => {
    it('Feature: m4-global-layout-navigation, Property 9: footer content strictly derives from SiteConfig props for any input', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { navItemArbitrary, socialLinkArbitrary } = require('../../../fixtures/site-config-arbitraries');

      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 25 }).filter((s: string) => s.trim().length > 0 && !s.includes('<')),
          fc.integer({ min: 2020, max: 2050 }),
          fc.array(navItemArbitrary, { minLength: 1, maxLength: 4 }),
          fc.array(socialLinkArbitrary, { maxLength: 4 }),
          (name: string, yr: number, navItems: any, socials: any) => {
            cleanup();
            render(
              <SiteFooter
                profileName={name}
                navigation={navItems}
                socialLinks={socials}
                contactChannels={[]}
                year={yr}
              />
            );

            // Copyright check
            expect(screen.getByText(new RegExp(`© ${yr} ${name}`))).toBeDefined();

            // Nav links check
            for (const item of navItems) {
              const link = screen.getByRole('link', { name: item.label });
              expect(link.getAttribute('href')).toBe(item.href);
            }

            // Social links check
            for (const s of socials) {
              const link = screen.getByRole('link', { name: new RegExp(s.label) });
              expect(link.getAttribute('href')).toBe(s.url);
              expect(link.getAttribute('target')).toBe('_blank');
              expect(link.getAttribute('rel')).toBe('noopener noreferrer');
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\site-footer.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\site-footer.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-footer.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.4, Req 15.1

---

### M4.G5.T7: Author Property-Based Test for Empty Section Omission (Property 10)

**Objective:** Append property-based test in `tests/unit/components/layout/site-footer.test.tsx` verifying Property 10: empty data collections are completely omitted rather than rendered with empty containers.

**Acceptance Criteria:**
- ✓ Implements Property 10 test ($\ge 100$ runs with `fast-check`)
- ✓ Social section exists if and only if valid HTTPS social links exist
- ✓ Contact section `#contact` exists if and only if renderable contact channels exist
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed
- Target file: `tests/unit/components/layout/site-footer.test.tsx`

**Implementation Details:**

Append Property 10 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$appendCode = @'

  describe('Property-Based Invariants (Property 10)', () => {
    it('Feature: m4-global-layout-navigation, Property 10: empty social and contact data is omitted, never rendered empty', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');
      const { contactChannelArbitrary, socialLinkArbitrary } = require('../../../fixtures/site-config-arbitraries');
      const { getRenderableChannels } = require('@/components/layout/contact-channels');
      const { resolveExternalHref } = require('@/components/ui/external-link-attrs');

      fc.assert(
        fc.property(
          fc.array(socialLinkArbitrary, { maxLength: 4 }),
          fc.array(contactChannelArbitrary, { maxLength: 4 }),
          (socials: any, contacts: any) => {
            cleanup();
            const { container } = render(
              <SiteFooter
                profileName="Test Owner"
                navigation={[]}
                socialLinks={socials}
                contactChannels={contacts}
              />
            );

            const hasValidSocials = socials.some((s: any) => resolveExternalHref(s.url) !== null);
            const hasRenderableContacts = getRenderableChannels(contacts).length > 0;

            const socialHeading = container.querySelector('#footer-social-heading');
            if (hasValidSocials) {
              expect(socialHeading).not.toBeNull();
            } else {
              expect(socialHeading).toBeNull();
            }

            const contactSection = container.querySelector('#contact');
            if (hasRenderableContacts) {
              expect(contactSection).not.toBeNull();
            } else {
              expect(contactSection).toBeNull();
            }
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\site-footer.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\site-footer.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/site-footer.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.3, Req 8.5, Req 8.6, Req 9.5, Req 15.1

---

### M4.G5.T8: Audit Hardcoded Site Literals in Footer and ContactLinks

**Objective:** Audit `src/components/layout/contact-links.tsx` and `site-footer.tsx` to verify zero personal name, email, or site-owner literals are hardcoded per Requirement 2.4.

**Acceptance Criteria:**
- ✓ Searches files for `'Angelo'`, `'Andres'`, `'hello@example.com'`, and `'example.vercel.app'`
- ✓ Confirms zero string matches in source code
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G5.T1 and M4.G5.T2 completed

**Implementation Details:**

Execute literal audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\layout\contact-links.tsx", "src\components\layout\site-footer.tsx")
$forbiddenLiterals = @('Angelo', 'Andres', 'hello@example.com', 'example.vercel.app')
$violations = @()

foreach ($f in $files) {
    $content = Get-Content $f -Raw
    foreach ($lit in $forbiddenLiterals) {
        if ($content.Contains($lit)) {
            $violations += "Hardcoded site literal '$lit' found in $f (Req 2.4 violation)"
        }
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 2.4, Req 14.5

---

### M4.G5.T9: Verify Source Hygiene of ContactLinks and SiteFooter

**Objective:** Audit `contact-links.tsx` and `site-footer.tsx` ensuring zero raw hex colors, zero arbitrary Tailwind brackets, zero `'use client'`, and file lengths under 300 lines.

**Acceptance Criteria:**
- ✓ Zero raw hex colors (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero arbitrary Tailwind brackets `[` or `]`
- ✓ Zero `any` or `!`
- ✓ Zero `'use client'` statements (both must be server components)
- ✓ Both files are under 300 lines

**Prerequisites:**
- M4.G5.T1 and M4.G5.T2 completed

**Implementation Details:**

Execute hygiene audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$files = @("src\components\layout\contact-links.tsx", "src\components\layout\site-footer.tsx")
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
        Write-Host "Violation in $file (Lines=$lines, Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient)"
    }
}

if ($allPass) { "PASS" } else { "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 8.9, Req 9.8, Req 13.5, Req 13.6, Req 14.6, Req 14.7, Req 16.2

---

### M4.G5.T10: Checkpoint — ContactLinks and SiteFooter Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `ContactLinks` and `SiteFooter`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all ContactLinks and SiteFooter tests and passes with code 0
- ✓ Zero regressions introduced into upstream modules

**Prerequisites:**
- M4.G5.T1 through M4.G5.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/contact-links.test.tsx tests/unit/components/layout/site-footer.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/contact-links.test.tsx tests/unit/components/layout/site-footer.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 5 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "src\components\layout\contact-links.tsx"
Test-Path "src\components\layout\site-footer.tsx"
Test-Path "tests\unit\components\layout\contact-links.test.tsx"
Test-Path "tests\unit\components\layout\site-footer.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/layout/contact-links.test.tsx tests/unit/components/layout/site-footer.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all ContactLinks and SiteFooter tests with return code 0.