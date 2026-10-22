# M4.G3: MobileNavToggle Client Island and PrimaryNav

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the interactive navigation components in `src/components/layout/`: the server-rendered `PrimaryNav` landmark in `primary-nav.tsx` and the single client-side island `MobileNavToggle` in `mobile-nav-toggle.tsx`. `PrimaryNav` acts as a server component owning the semantic `<nav aria-label="Primary">` landmark, invoking the pure `buildNavEntries` helper, and passing serializable navigation entries to the island. `MobileNavToggle` is designated as the sole `'use client'` module in `src/components/layout/`, encapsulating the transient disclosure state machine via `useReducer`, reading `usePathname()` to compute `aria-current="page"`, and handling Escape key collapse with focus return, link-activation collapse, and route-change collapse. Guarantee that all navigation links remain present in the server-rendered HTML while being cleanly hidden via CSS below the desktop breakpoint. Validate keyboard mechanics, property-based invariants (Property 6), and server-side markup completeness using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/layout/primary-nav.tsx` implemented as a server component without `'use client'`
- ✓ `PrimaryNav` renders `<nav aria-label="Primary">` with distinct accessible labeling
- ✓ `src/components/layout/mobile-nav-toggle.tsx` is the ONLY module in `src/components/layout/` carrying `'use client'`
- ✓ `mobile-nav-toggle.tsx` begins with the formal architectural justification comment required by Req 6.10
- ✓ Toggle button renders with accessible name `Menu`, dynamic `aria-expanded`, `aria-controls="primary-nav-list"`, `lg:hidden`, `min-h-12 min-w-12`, `FOCUS_RING`, and `MOTION_FAST`
- ✓ Pressing Escape when expanded collapses navigation and returns keyboard focus to the toggle button
- ✓ Activating any link or detecting a pathname change collapses the menu
- ✓ Navigation list uses `hidden lg:flex` when collapsed, completely removing links from tab order and accessibility tree on mobile viewports
- ✓ Navigation entries remain present in static HTML prerender (`renderToStaticMarkup` test)
- ✓ Active route exposes `aria-current="page"` and multi-cue visual styling (border and font weight); Contact anchor is never marked current
- ✓ `tests/unit/components/layout/mobile-nav-toggle.test.tsx` and `primary-nav.test.tsx` pass with 100% assertions

## Prerequisites

- Goal M4.G2 completed (pure modules `current-route.ts`, `nav-entries.ts`, `disclosure.ts`, `contact-channels.ts` available)
- Layout text constants available at `src/components/layout/layout-text.ts`
- M3 primitives (`FOCUS_RING`, `MOTION_FAST`, `cx`) available at `src/components/ui/`
- `@testing-library/user-event` installed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M4.G3.T1: Author `MobileNavToggle` Client Component Skeleton & State Reducer

**Objective:** Create `src/components/layout/mobile-nav-toggle.tsx` with the mandatory `'use client'` directive, architectural justification comment, props interface, and state reducer initialization.

**Acceptance Criteria:**
- ✓ File `src/components/layout/mobile-nav-toggle.tsx` created
- ✓ First line declares `'use client'`
- ✓ Carries immediate comment explaining client boundary justification (`useReducer`, `useRef`, `usePathname`, Req 6.10)
- ✓ Exports `MobileNavToggleProps` interface accepting `entries: readonly NavEntry[]`
- ✓ Wires `useReducer` to pure `disclosureReducer` with initial state `'collapsed'`
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M4.G2 completed (`disclosure.ts`, `nav-entries.ts` exist)
- Target file: `src/components/layout/mobile-nav-toggle.tsx`

**Implementation Details:**

Write the skeleton of `src/components/layout/mobile-nav-toggle.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
'use client';
// Client component justification (AGENTS.md 6.2, Req 6.10):
// Requires useReducer/useRef/useEffect for mobile disclosure state management and
// focus restoration on Escape, plus usePathname() for dynamic active route indication.
// This is the sole 'use client' module in src/components/layout/.

import React, { useReducer, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import type { NavEntry } from './nav-entries';
import { disclosureReducer } from './disclosure';
import { getCurrentEntryIndex } from './current-route';
import { MENU_BUTTON_LABEL, PRIMARY_NAV_LIST_ID } from './layout-text';

export interface MobileNavToggleProps {
  entries: readonly NavEntry[];
}
'@ | Set-Content "src\components\layout\mobile-nav-toggle.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/mobile-nav-toggle.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.10, Req 16.1

---

### M4.G3.T2: Implement Toggle Button and Navigation List Markup

**Objective:** Append toggle `<button>` rendering and the responsive `<ul id="primary-nav-list">` container to `src/components/layout/mobile-nav-toggle.tsx`.

**Acceptance Criteria:**
- ✓ Renders native `<button type="button">` with visible text `Menu`
- ✓ Button attaches `aria-expanded={state === 'expanded'}`
- ✓ Button attaches `aria-controls="primary-nav-list"`
- ✓ Button includes `lg:hidden`, `min-h-12 min-w-12`, `FOCUS_RING`, and `MOTION_FAST`
- ✓ Navigation list container uses `id="primary-nav-list"`
- ✓ Collapsed list applies `hidden lg:flex` (display none on mobile viewports below 1024px)
- ✓ Expanded list applies `flex flex-col lg:flex-row absolute inset-x-0 top-full bg-page border-b border-border-default shadow-elevation-2`

**Prerequisites:**
- M4.G3.T1 completed
- Target file: `src/components/layout/mobile-nav-toggle.tsx`

**Implementation Details:**

Append component structure to `src/components/layout/mobile-nav-toggle.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

const NAV_LINK_BASE =
  'inline-flex min-h-12 items-center border-b-2 px-3 text-body text-text-primary select-none';

const NAV_LINK_IDLE =
  'border-transparent hover:border-border-strong hover:text-brand-primary';

const NAV_LINK_CURRENT =
  'border-brand-primary font-semibold text-brand-primary';

export function MobileNavToggle({ entries }: MobileNavToggleProps): JSX.Element {
  const [state, dispatch] = useReducer(disclosureReducer, 'collapsed');
  const buttonRef = useRef<HTMLButtonElement | null>(null);
  const pathname = usePathname();

  const isExpanded = state === 'expanded';

  const currentIndex = getCurrentEntryIndex(
    pathname,
    entries.map((e) => (e.kind === 'route' ? e.href : null))
  );

  return (
    <div className="relative">
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={isExpanded}
        aria-controls={PRIMARY_NAV_LIST_ID}
        onClick={() => dispatch('TOGGLE')}
        className={cx(
          'inline-flex min-h-12 min-w-12 items-center justify-center rounded-md border border-border-default bg-surface px-3 py-2 text-body font-medium text-text-primary lg:hidden',
          FOCUS_RING,
          MOTION_FAST
        )}
      >
        <span className="sr-only">{MENU_BUTTON_LABEL}</span>
        {/* Hamburger / Close Icon */}
        <svg
          className="h-6 w-6 shrink-0 text-current"
          aria-hidden="true"
          focusable="false"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          {isExpanded ? (
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      <ul
        id={PRIMARY_NAV_LIST_ID}
        className={cx(
          'list-none p-0 m-0',
          isExpanded
            ? 'absolute inset-x-0 top-full z-40 flex flex-col border-b border-border-default bg-page p-4 shadow-elevation-2 lg:static lg:z-auto lg:flex-row lg:border-none lg:p-0 lg:shadow-none'
            : 'hidden lg:flex lg:flex-row lg:items-center lg:gap-2'
        )}
      >
        {entries.map((entry, index) => {
          const isCurrent = index === currentIndex;
          return (
            <li key={entry.href}>
              <Link
                href={entry.href}
                aria-current={isCurrent ? 'page' : undefined}
                onClick={() => dispatch('LINK_ACTIVATED')}
                className={cx(
                  NAV_LINK_BASE,
                  FOCUS_RING,
                  MOTION_FAST,
                  isCurrent ? NAV_LINK_CURRENT : NAV_LINK_IDLE
                )}
              >
                {entry.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
'@

Add-Content -Path "src\components\layout\mobile-nav-toggle.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/mobile-nav-toggle.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1, Req 4.6, Req 5.1, Req 5.3, Req 6.1, Req 6.2, Req 6.3, Req 6.9, Req 12.5

---

### M4.G3.T3: Implement Keyboard Event Listeners & Focus Restoration

**Objective:** Append keyboard listeners for the Escape key and route change effects to `src/components/layout/mobile-nav-toggle.tsx` to restore focus to the toggle button on collapse.

**Acceptance Criteria:**
- ✓ Pressing Escape while expanded dispatches `'ESCAPE'` and calls `buttonRef.current?.focus()`
- ✓ `useEffect` monitors `pathname` changes and dispatches `'ROUTE_CHANGED'`
- ✓ Keydown listener handles Escape on both button and list containers
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M4.G3.T2 completed
- Target file: `src/components/layout/mobile-nav-toggle.tsx`

**Implementation Details:**

Update `src/components/layout/mobile-nav-toggle.tsx` using PowerShell to add keydown and pathname observation logic:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$fullComponent = @'
'use client';
// Client component justification (AGENTS.md 6.2, Req 6.10):
// Requires useReducer/useRef/useEffect for mobile disclosure state management and
// focus restoration on Escape, plus usePathname() for dynamic active route indication.
// This is the sole 'use client' module in src/components/layout/.

import React, { useReducer, useRef, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cx } from '@/components/ui/cx';
import { FOCUS_RING } from '@/components/ui/focus-ring';
import { MOTION_FAST } from '@/components/ui/motion';
import type { NavEntry } from './nav-entries';
import { disclosureReducer } from './disclosure';
import { getCurrentEntryIndex } from './current-route';
import { MENU_BUTTON_LABEL, PRIMARY_NAV_LIST_ID } from './layout-text';

export interface MobileNavToggleProps {
  entries: readonly NavEntry[];
}

const NAV_LINK_BASE =
  'inline-flex min-h-12 items-center border-b-2 px-3 text-body text-text-primary select-none';

const NAV_LINK_IDLE =
  'border-transparent hover:border-border-strong hover:text-brand-primary';

const NAV_LINK_CURRENT =
  'border-brand-primary font-semibold text-brand-primary';

export function MobileNavToggle({ entries }: MobileNavToggleProps): JSX.Element {
  const [state, dispatch] = useReducer(disclosureReducer, 'collapsed');
  const buttonRef = useRef<HTMLButtonElement | null>(null);
  const pathname = usePathname();

  const isExpanded = state === 'expanded';

  // Collapse on route change
  useEffect(() => {
    dispatch('ROUTE_CHANGED');
  }, [pathname]);

  // Handle Escape key to collapse and restore keyboard focus (Req 6.5)
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (isExpanded && e.key === 'Escape') {
        e.preventDefault();
        dispatch('ESCAPE');
        buttonRef.current?.focus();
      }
    },
    [isExpanded]
  );

  const currentIndex = getCurrentEntryIndex(
    pathname,
    entries.map((e) => (e.kind === 'route' ? e.href : null))
  );

  return (
    <div className="relative" onKeyDown={handleKeyDown}>
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={isExpanded}
        aria-controls={PRIMARY_NAV_LIST_ID}
        onClick={() => dispatch('TOGGLE')}
        className={cx(
          'inline-flex min-h-12 min-w-12 items-center justify-center rounded-md border border-border-default bg-surface px-3 py-2 text-body font-medium text-text-primary lg:hidden',
          FOCUS_RING,
          MOTION_FAST
        )}
      >
        <span className="sr-only">{MENU_BUTTON_LABEL}</span>
        <svg
          className="h-6 w-6 shrink-0 text-current"
          aria-hidden="true"
          focusable="false"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          {isExpanded ? (
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      <ul
        id={PRIMARY_NAV_LIST_ID}
        className={cx(
          'list-none p-0 m-0',
          isExpanded
            ? 'absolute inset-x-0 top-full z-40 flex flex-col border-b border-border-default bg-page p-4 shadow-elevation-2 lg:static lg:z-auto lg:flex-row lg:border-none lg:p-0 lg:shadow-none'
            : 'hidden lg:flex lg:flex-row lg:items-center lg:gap-2'
        )}
      >
        {entries.map((entry, index) => {
          const isCurrent = index === currentIndex;
          return (
            <li key={entry.href}>
              <Link
                href={entry.href}
                aria-current={isCurrent ? 'page' : undefined}
                onClick={() => dispatch('LINK_ACTIVATED')}
                className={cx(
                  NAV_LINK_BASE,
                  FOCUS_RING,
                  MOTION_FAST,
                  isCurrent ? NAV_LINK_CURRENT : NAV_LINK_IDLE
                )}
              >
                {entry.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
'@ | Set-Content "src\components\layout\mobile-nav-toggle.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/mobile-nav-toggle.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.5, Req 6.6, Req 6.7, Req 6.10

---

### M4.G3.T4: Implement Server-Side `PrimaryNav` Landmark (`src/components/layout/primary-nav.tsx`)

**Objective:** Author the server component `PrimaryNav` in `src/components/layout/primary-nav.tsx` rendering the `<nav aria-label="Primary">` landmark and invoking `buildNavEntries`.

**Acceptance Criteria:**
- ✓ File `src/components/layout/primary-nav.tsx` created
- ✓ Exports `PrimaryNavProps` requiring `navigation: SiteConfig['navigation']` and `contactChannels: SiteConfig['contactChannels']`
- ✓ Exports `PrimaryNav(props: PrimaryNavProps): JSX.Element`
- ✓ Renders `<nav aria-label="Primary">` landmark (Req 1.2, 1.5)
- ✓ Invokes `buildNavEntries(navigation, contactChannels)`
- ✓ Passes resulting `NavEntry[]` to `<MobileNavToggle entries={entries} />`
- ✓ Server component containing zero `'use client'` statements

**Prerequisites:**
- M4.G3.T3 completed
- Target file: `src/components/layout/primary-nav.tsx`

**Implementation Details:**

Write `src/components/layout/primary-nav.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import type { SiteConfig } from '@/types/content';
import { buildNavEntries } from './nav-entries';
import { MobileNavToggle } from './mobile-nav-toggle';
import { PRIMARY_NAV_LABEL } from './layout-text';

export interface PrimaryNavProps {
  navigation: SiteConfig['navigation'];
  contactChannels: SiteConfig['contactChannels'];
}

/**
 * Primary Navigation Landmark
 *
 * Renders the top-level <nav> landmark and delegates rendering and interaction
 * to the MobileNavToggle client island. Server component by default (Req 1.5).
 */
export function PrimaryNav({ navigation, contactChannels }: PrimaryNavProps): JSX.Element {
  const entries = buildNavEntries(navigation, contactChannels);

  return (
    <nav aria-label={PRIMARY_NAV_LABEL}>
      <MobileNavToggle entries={entries} />
    </nav>
  );
}
'@ | Set-Content "src\components\layout\primary-nav.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/layout/primary-nav.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.2, Req 1.5, Req 4.1, Req 4.2, Req 4.7

---

### M4.G3.T5: Author Unit Tests for `MobileNavToggle` Keyboard Interactions

**Objective:** Create `tests/unit/components/layout/mobile-nav-toggle.test.tsx` verifying toggle click, Escape collapse with focus restoration, link activation collapse, and Enter/Space operations.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/mobile-nav-toggle.test.tsx` created
- ✓ Mocks `next/navigation` (`usePathname` returning `'/projects'`)
- ✓ Clicking toggle button updates `aria-expanded` from `false` to `true` and back
- ✓ Pressing Escape when expanded collapses menu and focuses the toggle button
- ✓ Clicking a navigation link collapses the menu
- ✓ Operating toggle via Enter and Space keys toggles menu state
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G3.T3 completed
- Target file: `tests/unit/components/layout/mobile-nav-toggle.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/mobile-nav-toggle.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MobileNavToggle } from '@/components/layout/mobile-nav-toggle';
import type { NavEntry } from '@/components/layout/nav-entries';

let mockPathname = '/projects';

vi.mock('next/navigation', () => ({
  usePathname: () => mockPathname,
}));

describe('MobileNavToggle Component (Req 6)', () => {
  const sampleEntries: NavEntry[] = [
    { label: 'Home', href: '/', kind: 'route' },
    { label: 'Projects', href: '/projects', kind: 'route' },
    { label: 'Certifications', href: '/certifications', kind: 'route' },
    { label: 'Contact', href: '#contact', kind: 'anchor' },
  ];

  beforeEach(() => {
    mockPathname = '/projects';
  });

  it('renders with button collapsed by default and list hidden on mobile', () => {
    const { container } = render(<MobileNavToggle entries={sampleEntries} />);
    const btn = screen.getByRole('button', { name: 'Menu' });

    expect(btn.getAttribute('aria-expanded')).toBe('false');
    expect(btn.getAttribute('aria-controls')).toBe('primary-nav-list');

    const list = container.querySelector('#primary-nav-list');
    expect(list?.className).toContain('hidden');
    expect(list?.className).toContain('lg:flex');
  });

  it('toggles expansion state on click', async () => {
    const user = userEvent.setup();
    render(<MobileNavToggle entries={sampleEntries} />);
    const btn = screen.getByRole('button', { name: 'Menu' });

    await user.click(btn);
    expect(btn.getAttribute('aria-expanded')).toBe('true');

    await user.click(btn);
    expect(btn.getAttribute('aria-expanded')).toBe('false');
  });

  it('collapses on Escape key press and restores focus to button', async () => {
    const user = userEvent.setup();
    render(<MobileNavToggle entries={sampleEntries} />);
    const btn = screen.getByRole('button', { name: 'Menu' });

    await user.click(btn);
    expect(btn.getAttribute('aria-expanded')).toBe('true');

    await user.keyboard('{Escape}');
    expect(btn.getAttribute('aria-expanded')).toBe('false');
    expect(document.activeElement).toBe(btn);
  });

  it('collapses when a navigation link is clicked', async () => {
    const user = userEvent.setup();
    render(<MobileNavToggle entries={sampleEntries} />);
    const btn = screen.getByRole('button', { name: 'Menu' });

    await user.click(btn);
    expect(btn.getAttribute('aria-expanded')).toBe('true');

    const projectLink = screen.getByRole('link', { name: 'Projects' });
    await user.click(projectLink);

    expect(btn.getAttribute('aria-expanded')).toBe('false');
  });

  it('operates via Enter and Space keyboard activations', async () => {
    const user = userEvent.setup();
    render(<MobileNavToggle entries={sampleEntries} />);
    const btn = screen.getByRole('button', { name: 'Menu' });

    btn.focus();
    await user.keyboard('{Enter}');
    expect(btn.getAttribute('aria-expanded')).toBe('true');

    await user.keyboard(' ');
    expect(btn.getAttribute('aria-expanded')).toBe('false');
  });
});
'@ | Set-Content "tests\unit\components\layout\mobile-nav-toggle.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.3, Req 6.4, Req 6.5, Req 6.6, Req 6.8, Req 15.4

---

### M4.G3.T6: Author Property-Based Test for Rendered Disclosure State (Property 6)

**Objective:** Append property-based test in `tests/unit/components/layout/mobile-nav-toggle.test.tsx` using `fast-check` to assert that across arbitrary click counts, `aria-expanded` and CSS classes strictly reflect click parity while keeping all entries in the DOM.

**Acceptance Criteria:**
- ✓ Implements Property 6 test ($\ge 100$ runs with `fast-check`)
- ✓ Bounded click counts ($0 \le N \le 15$)
- ✓ Asserts `aria-expanded="true"` iff click count is odd
- ✓ Asserts list has `hidden` iff click count is even
- ✓ Asserts all entries remain present in the DOM for all states
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G3.T5 completed
- Target file: `tests/unit/components/layout/mobile-nav-toggle.test.tsx`

**Implementation Details:**

Append Property 6 test to `tests/unit/components/layout/mobile-nav-toggle.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 6)', () => {
    it('Feature: m4-global-layout-navigation, Property 6: rendered disclosure reflects state and preserves DOM entries for any click sequence', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.integer({ min: 0, max: 15 }),
          (clickCount: number) => {
            cleanup();
            const { container } = render(<MobileNavToggle entries={sampleEntries} />);
            const btn = screen.getByRole('button', { name: 'Menu' });

            for (let i = 0; i < clickCount; i++) {
              fireEvent.click(btn);
            }

            const isOdd = clickCount % 2 === 1;
            expect(btn.getAttribute('aria-expanded')).toBe(String(isOdd));

            const list = container.querySelector('#primary-nav-list');
            expect(list).not.toBeNull();

            if (isOdd) {
              expect(list?.className).not.toContain('hidden');
            } else {
              expect(list?.className).toContain('hidden');
            }

            // Entries must always exist in the markup
            const links = container.querySelectorAll('a');
            expect(links.length).toBe(sampleEntries.length);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\mobile-nav-toggle.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\mobile-nav-toggle.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.3, Req 6.4, Req 6.9, Req 6.11

---

### M4.G3.T7: Author Unit Tests for `PrimaryNav` Landmark & Current Route (`tests/unit/components/layout/primary-nav.test.tsx`)

**Objective:** Create `tests/unit/components/layout/primary-nav.test.tsx` verifying `<nav aria-label="Primary">` landmark generation, entry delegation, and active route indication.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/primary-nav.test.tsx` created
- ✓ Verifies `<nav aria-label="Primary">` landmark wrapper exists
- ✓ Verifies active route has `aria-current="page"` and multi-cue border/font styling
- ✓ Verifies at most one entry is marked `aria-current`
- ✓ Verifies `#contact` anchor is never marked current
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G3.T4 completed
- Target file: `tests/unit/components/layout/primary-nav.test.tsx`

**Implementation Details:**

Write `tests/unit/components/layout/primary-nav.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PrimaryNav } from '@/components/layout/primary-nav';
import { validSiteConfig } from '../../../fixtures/site-config';

let mockPathname = '/projects';

vi.mock('next/navigation', () => ({
  usePathname: () => mockPathname,
}));

describe('PrimaryNav Component (Req 1, 4, 5)', () => {
  it('renders nav landmark with aria-label="Primary"', () => {
    mockPathname = '/projects';
    render(
      <PrimaryNav
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const nav = screen.getByRole('navigation', { name: 'Primary' });
    expect(nav).toBeDefined();
  });

  it('marks exactly one active route with aria-current="page" and visual cues', () => {
    mockPathname = '/projects';
    render(
      <PrimaryNav
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const activeLink = screen.getByRole('link', { name: 'Projects' });
    expect(activeLink.getAttribute('aria-current')).toBe('page');
    expect(activeLink.className).toContain('border-brand-primary');
    expect(activeLink.className).toContain('font-semibold');

    const homeLink = screen.getByRole('link', { name: 'Home' });
    expect(homeLink.getAttribute('aria-current')).toBeNull();
  });

  it('never marks the Contact anchor as current page', () => {
    mockPathname = '/#contact';
    render(
      <PrimaryNav
        navigation={validSiteConfig.navigation}
        contactChannels={validSiteConfig.contactChannels}
      />
    );

    const contactLink = screen.getByRole('link', { name: 'Contact' });
    expect(contactLink.getAttribute('aria-current')).toBeNull();
  });
});
'@ | Set-Content "tests\unit\components\layout\primary-nav.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/primary-nav.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 4.1, Req 5.1, Req 5.3, Req 5.4

---

### M4.G3.T8: Author Server-Side Prerender Markup Test (`renderToStaticMarkup`)

**Objective:** Append a test in `tests/unit/components/layout/primary-nav.test.tsx` verifying that `renderToStaticMarkup` contains all navigation links to prove server-rendered HTML completeness per Requirement 6.11.

**Acceptance Criteria:**
- ✓ Uses `react-dom/server`'s `renderToStaticMarkup`
- ✓ Evaluates rendered HTML string of `PrimaryNav`
- ✓ Proves all navigation links (`Home`, `Projects`, `Certifications`, `Blog`, `Contact`) are present in raw server markup
- ✓ Proves `aria-current="page"` is present for active route in initial HTML
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G3.T7 completed
- Target file: `tests/unit/components/layout/primary-nav.test.tsx`

**Implementation Details:**

Append server HTML test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Static Prerender Verification (Req 6.11)', () => {
    it('contains all navigation links in server-rendered static HTML markup', () => {
      const { renderToStaticMarkup } = require('react-dom/server');
      mockPathname = '/certifications';

      const html = renderToStaticMarkup(
        <PrimaryNav
          navigation={validSiteConfig.navigation}
          contactChannels={validSiteConfig.contactChannels}
        />
      );

      expect(html).toContain('Home');
      expect(html).toContain('Projects');
      expect(html).toContain('Certifications');
      expect(html).toContain('Blog');
      expect(html).toContain('Contact');
      expect(html).toContain('aria-current="page"');
    });
  });
'@

$content = Get-Content "tests\unit\components\layout\primary-nav.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\layout\primary-nav.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/layout/primary-nav.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 6.11

---

### M4.G3.T9: Verify Client Boundary Exclusivity (`mobile-nav-toggle.tsx`)

**Objective:** Audit `src/components/layout/` to guarantee that `mobile-nav-toggle.tsx` is the sole module declaring `'use client'` per Requirement 6.10.

**Acceptance Criteria:**
- ✓ Searches all `.ts` and `.tsx` files in `src/components/layout/`
- ✓ `mobile-nav-toggle.tsx` contains `'use client'`
- ✓ All other layout files contain zero occurrences of `'use client'`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G3.T3 and M4.G3.T4 completed

**Implementation Details:**

Execute client boundary audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$layoutFiles = Get-ChildItem -Path "src\components\layout" -Filter "*.ts*"
$violations = @()

foreach ($file in $layoutFiles) {
    $content = Get-Content $file.FullName -Raw
    $hasClient = $content -match "['""]use client['""]"
    if ($file.Name -eq "mobile-nav-toggle.tsx") {
        if (-not $hasClient) {
            $violations += "mobile-nav-toggle.tsx must declare 'use client'"
        }
    } else {
        if ($hasClient) {
            $violations += "$($file.Name) contains forbidden 'use client' directive (mobile-nav-toggle is sole client component)"
        }
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 6.10, Req 14.1, Req 16.2

---

### M4.G3.T10: Checkpoint — Navigation Components Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across `PrimaryNav` and `MobileNavToggle`.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all navigation tests and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M4.G3.T1 through M4.G3.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx tests/unit/components/layout/primary-nav.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx tests/unit/components/layout/primary-nav.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\layout\mobile-nav-toggle.tsx"
Test-Path "src\components\layout\primary-nav.tsx"
Test-Path "tests\unit\components\layout\mobile-nav-toggle.test.tsx"
Test-Path "tests\unit\components\layout\primary-nav.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/layout/mobile-nav-toggle.test.tsx tests/unit/components/layout/primary-nav.test.tsx
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all navigation test suites with code 0.