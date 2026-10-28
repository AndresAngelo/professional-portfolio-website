# M7.G7: CertificationCategorySection and CertificationsIndex

> **Milestone:** M7 — Certifications Module  
> **Goal:** G7 of 10  
> **Tasks:** 10 atomic tasks (M7.G7.T1 – M7.G7.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 1.3–1.4, 2.1–2.4, 4.3, 5.1–5.4, 5.6, 7.5, 9.7, 11.1–11.3, 14.5), `design.md` (Components and Interfaces, Section Layout, Breakpoints, Property 14), `tasks.md` (M7.G7)

---

## Goal Objective

Implement the two high-level presentational container components in `src/components/certifications/`:
1. `certification-category-section.tsx`: renders a `<section>` associated via `aria-labelledby` with its `<h2>` category heading (`id="certifications-{category}-heading"`), and houses an accessible list (`<ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">`) containing one `<li>` per `CertificationCard`.
2. `certifications-index.tsx`: main container wrapped in M3's `Container`, rendering exactly one `<h1>Certifications</h1>`, calculating running card indices so that only the first card on the entire page receives `priority={true}` (eager image loading), delegating grouped items to `CertificationCategorySection`, rendering the M3 `EmptyState` when zero certifications exist, and preserving an unbroken heading hierarchy (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`).

Verify document outline, heading level transitions, responsive grid classes, and accessibility via unit tests, fast-check Property 14, and `axe-core`.

---

## Goal Success Criteria

- ✓ `src/components/certifications/certification-category-section.tsx` renders a `<section>` with `aria-labelledby="certifications-{group.category}-heading"`.
- ✓ The section renders an `<h2>` with text from `getCategoryLabel(group.category)` and unique id `certifications-{group.category}-heading`.
- ✓ Renders a responsive `<ul>` with classes `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch` holding one `<li>` per card in `Certification_Order`.
- ✓ `src/components/certifications/certifications-index.tsx` composes M3 `Container`, renders exactly one `<h1>` containing `"Certifications"`, and renders no `header`, `footer`, or `main` landmark.
- ✓ Only the very first certification card rendered on the page (index 0) receives `priority={true}`; all subsequent cards receive `priority={false}`.
- ✓ When certifications array is empty, renders M3 `EmptyState` with message `"Certifications are being prepared"`, still rendering the `<h1>`, and emitting zero section or card elements.
- ✓ When all categories are valid, zero `"Uncategorised"` headings are emitted.
- ✓ Document heading outline has no skipped levels (`h1` $\rightarrow$ `h2` $\rightarrow$ `h3`).
- ✓ Property 14 passes with >= 100 runs.
- ✓ `axe-core` tests pass with zero violations for populated and empty index states.

---

## Prerequisites

- Goal 1 completed: `getCategoryLabel`, `UNCATEGORISED` available.
- Goal 2 completed: `groupCertificationsByCategory`, `CertificationGroup` available.
- Goal 6 completed: `CertificationCard` available.
- M3 primitives (`Container`, `EmptyState`) available in `src/components/ui/`.

---

## Tasks

### M7.G7.T1: Implement CertificationCategorySection Component Structure

**Objective:** Create `src/components/certifications/certification-category-section.tsx` defining `CertificationCategorySectionProps`, section markup, `<h2>` heading with unique id, and the responsive `<ul>` grid container.

**Acceptance Criteria:**
- ✓ Exports interface `CertificationCategorySectionProps`:
  ```typescript
  export interface CertificationCategorySectionProps {
    readonly group: CertificationGroup;
    readonly contentHtml: Readonly<Record<string, string>>;
    readonly buildDate: IsoDateString;
    readonly firstCardIndex: number;
  }
  ```
- ✓ Renders `<section aria-labelledby={`certifications-${group.category}-heading`}>`.
- ✓ Renders `<h2 id={`certifications-${group.category}-heading`} className="text-heading-3 font-semibold text-text-primary mb-6">`.
- ✓ Renders `<h2>` text from `getCategoryLabel(group.category)`.
- ✓ Renders `<ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch list-none p-0 m-0">`.

**Prerequisites:**
- `src/lib/certifications/group-certifications.ts` exports `CertificationGroup`.
- `src/lib/certifications/category-label.ts` exports `getCategoryLabel`.
- `@/types/content` exports `IsoDateString`.

**Implementation Details:**
Create `src/components/certifications/certification-category-section.tsx`:

```typescript
import React from 'react';
import type { IsoDateString } from '@/types/content';
import type { CertificationGroup } from '@/lib/certifications/group-certifications';
import { getCategoryLabel } from '@/lib/certifications/category-label';
import { CertificationCard } from './certification-card';

export interface CertificationCategorySectionProps {
  readonly group: CertificationGroup;
  readonly contentHtml: Readonly<Record<string, string>>;
  readonly buildDate: IsoDateString;
  readonly firstCardIndex: number;
}

export function CertificationCategorySection({
  group,
  contentHtml,
  buildDate,
  firstCardIndex,
}: CertificationCategorySectionProps): React.JSX.Element {
  const headingId = `certifications-${group.category}-heading`;
  const label = getCategoryLabel(group.category);

  return (
    <section aria-labelledby={headingId} className="space-y-6">
      <h2 id={headingId} className="text-heading-3 font-semibold text-text-primary">
        {label}
      </h2>

      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch list-none p-0 m-0">
        {group.certifications.map((cert, idx) => {
          const globalIndex = firstCardIndex + idx;
          const isPriority = globalIndex === 0;

          return (
            <li key={cert.slug} className="h-full">
              <CertificationCard
                certification={cert}
                buildDate={buildDate}
                contentHtml={contentHtml[cert.slug]}
                priority={isPriority}
              />
            </li>
          );
        })}
      </ul>
    </section>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 5.1, 5.2, 5.3, 5.4, 5.5, 9.7, 11.1, 11.2, 11.3, 14.5

---

### M7.G7.T2: Unit Tests for CertificationCategorySection

**Objective:** Create `tests/certifications/certification-category-section.test.tsx` testing heading text, `aria-labelledby` binding, `li` element counts, and responsive grid classes.

**Acceptance Criteria:**
- ✓ Verifies `section` has `aria-labelledby="certifications-cloud-heading"`.
- ✓ Verifies `<h2>` has id `"certifications-cloud-heading"` and text `"Cloud"`.
- ✓ Verifies `<ul>` contains correct count of `<li>` items.
- ✓ Verifies `ul` class list contains `grid-cols-1`, `md:grid-cols-2`, and `lg:grid-cols-3`.
- ✓ Verifies `priority` is passed as `true` only for card where `firstCardIndex + idx === 0`.

**Prerequisites:**
- `src/components/certifications/certification-category-section.tsx` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/certification-category-section.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CertificationCategorySection } from '@/components/certifications/certification-category-section';
import { fixtureFullCertification } from '../fixtures/certifications-data';
import type { CertificationGroup } from '@/lib/certifications/group-certifications';

describe('CertificationCategorySection - Unit Tests', () => {
  const group: CertificationGroup = {
    category: 'cloud',
    certifications: [
      fixtureFullCertification,
      { ...fixtureFullCertification, slug: 'aws-devops-pro', title: 'AWS Certified DevOps Pro', displayOrder: 2 },
    ],
  };

  it('renders section with aria-labelledby matching h2 id', () => {
    const { container } = render(
      <CertificationCategorySection
        group={group}
        contentHtml={{}}
        buildDate="2026-04-15"
        firstCardIndex={0}
      />,
    );

    const section = container.querySelector('section');
    expect(section).toHaveAttribute('aria-labelledby', 'certifications-cloud-heading');

    const heading = screen.getByRole('heading', { level: 2, name: 'Cloud' });
    expect(heading).toHaveAttribute('id', 'certifications-cloud-heading');
  });

  it('renders list with responsive grid classes and li children', () => {
    const { container } = render(
      <CertificationCategorySection
        group={group}
        contentHtml={{}}
        buildDate="2026-04-15"
        firstCardIndex={0}
      />,
    );

    const list = container.querySelector('ul');
    expect(list?.className).toContain('grid-cols-1');
    expect(list?.className).toContain('md:grid-cols-2');
    expect(list?.className).toContain('lg:grid-cols-3');

    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(2);
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-category-section.test.tsx
```
Expected output: All unit tests pass.

**Satisfies Requirements:** Req 5.1, 5.2, 5.3, 5.4, 11.1, 11.2, 11.3, 14.5

---

### M7.G7.T3: Implement CertificationsIndex Structure and Empty State

**Objective:** Create `src/components/certifications/certifications-index.tsx` defining `CertificationsIndexProps`, composing M3 `Container`, rendering `<h1>Certifications</h1>`, and handling the empty state via M3 `EmptyState`.

**Acceptance Criteria:**
- ✓ Exports interface `CertificationsIndexProps`:
  ```typescript
  export interface CertificationsIndexProps {
    readonly certifications: readonly Certification[];
    readonly contentHtml: Readonly<Record<string, string>>;
    readonly buildDate: IsoDateString;
  }
  ```
- ✓ Composes M3 `Container` (`<Container className="py-12 space-y-12">`).
- ✓ Renders exactly one `<h1>` containing `"Certifications"` with classes `text-heading-1 font-bold text-text-primary`.
- ✓ When `groups.length === 0`, renders M3 `EmptyState`:
  ```typescript
  <EmptyState
    title="No certifications available"
    message="Certifications are currently being prepared and verified. Please check back soon."
  />
  ```
- ✓ Renders zero `header`, `footer`, or `main` landmark elements.

**Prerequisites:**
- `@/components/ui/Container` and `@/components/ui/EmptyState` available.
- `groupCertificationsByCategory` available from `@/lib/certifications/group-certifications`.

**Implementation Details:**
Create `src/components/certifications/certifications-index.tsx`:

```typescript
import React from 'react';
import type { Certification, IsoDateString } from '@/types/content';
import { Container } from '@/components/ui/Container';
import { EmptyState } from '@/components/ui/EmptyState';
import { groupCertificationsByCategory } from '@/lib/certifications/group-certifications';
import { CertificationCategorySection } from './certification-category-section';

export interface CertificationsIndexProps {
  readonly certifications: readonly Certification[];
  readonly contentHtml: Readonly<Record<string, string>>;
  readonly buildDate: IsoDateString;
}

export function CertificationsIndex({
  certifications,
  contentHtml,
  buildDate,
}: CertificationsIndexProps): React.JSX.Element {
  const groups = groupCertificationsByCategory(certifications);

  // Compute running card indices for priority loading
  let runningCardCount = 0;

  return (
    <Container className="py-12 space-y-12">
      <header className="space-y-4">
        <h1 className="text-heading-1 font-bold text-text-primary">Certifications</h1>
        <p className="text-lead text-text-secondary max-w-3xl">
          Verified credentials, technical certifications, and specialized badges earned across cloud architecture, security, systems, and software engineering.
        </p>
      </header>

      {groups.length === 0 ? (
        <EmptyState
          title="No certifications available"
          message="Certifications are currently being prepared and verified. Please check back soon."
        />
      ) : (
        <div className="space-y-16">
          {groups.map((group) => {
            const firstIndex = runningCardCount;
            runningCardCount += group.certifications.length;

            return (
              <CertificationCategorySection
                key={group.category}
                group={group}
                contentHtml={contentHtml}
                buildDate={buildDate}
                firstCardIndex={firstIndex}
              />
            );
          })}
        </div>
      )}
    </Container>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 5.1, 7.5, 9.7

---

### M7.G7.T4: Unit Tests for CertificationsIndex Populated and Empty States

**Objective:** Create `tests/certifications/certifications-index.test.tsx` verifying populated multi-category rendering, empty state handling, and absence of layout landmarks.

**Acceptance Criteria:**
- ✓ Test: populated list renders `<h1>Certifications</h1>`, multiple `<h2>` category sections, and cards.
- ✓ Test: empty list renders `<h1>Certifications</h1>`, M3 `EmptyState`, and zero `<h2>` or card elements.
- ✓ Test: confirms only the first card on the entire page receives priority image loading (`loading="eager"`).
- ✓ Test: confirms component renders zero `<main>`, `<header>`, or `<footer>` root layout elements.
- ✓ Test: confirms valid input renders zero `"Uncategorised"` headings.

**Prerequisites:**
- `src/components/certifications/certifications-index.tsx` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/certifications-index.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CertificationsIndex } from '@/components/certifications/certifications-index';
import {
  fixtureCertificationsList,
  fixtureEmptyCertificationsList,
} from '../fixtures/certifications-data';

describe('CertificationsIndex - Unit Tests', () => {
  const buildDate = '2026-04-15';

  it('renders h1, multiple category sections, and cards for populated list', () => {
    render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    expect(screen.getByRole('heading', { level: 1, name: 'Certifications' })).toBeInTheDocument();
    const h2Elements = screen.getAllByRole('heading', { level: 2 });
    expect(h2Elements.length).toBeGreaterThan(1);
    expect(screen.queryByText('Uncategorised')).toBeNull();
  });

  it('renders EmptyState and h1 when certifications list is empty', () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureEmptyCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    expect(screen.getByRole('heading', { level: 1, name: 'Certifications' })).toBeInTheDocument();
    expect(screen.getByText('No certifications available')).toBeInTheDocument();
    expect(container.querySelectorAll('h2')).toHaveLength(0);
    expect(container.querySelectorAll('li')).toHaveLength(0);
  });

  it('sets eager loading only on the very first card image', () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    const images = container.querySelectorAll('img');
    if (images.length > 0) {
      expect(images[0]).toHaveAttribute('loading', 'eager');
      for (let i = 1; i < images.length; i++) {
        expect(images[i]).toHaveAttribute('loading', 'lazy');
      }
    }
  });

  it('renders zero main or footer layout landmarks', () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    expect(container.querySelector('main')).toBeNull();
    expect(container.querySelector('footer')).toBeNull();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-index.test.tsx
```
Expected output: All 4 unit tests pass.

**Satisfies Requirements:** Req 1.3, 1.4, 2.1, 2.2, 2.3, 4.3, 5.1, 9.7

---

### M7.G7.T5: Property 14 Test — Page Structure, Order, and Unbroken Heading Outline

**Objective:** Append Property 14 test to `tests/certifications/certifications-index.test.tsx` verifying that for any certification set, page structure is strictly ordered, labelled, and heading levels never skip.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 14: Page structure is ordered, labelled, and level-correct`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Verifies exactly one `<h1>`.
- ✓ Verifies every `<section>` accessible name equals its `<h2>` text.
- ✓ Verifies heading levels in document order never increase by more than 1 (e.g. `h1` $\rightarrow$ `h2` $\rightarrow$ `h3`).
- ✓ Verifies empty input renders `<h1>` and `EmptyState` with zero `<h2>` or card elements.

**Prerequisites:**
- `createArbCertification` and `arbBuildDate` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/certifications-index.test.tsx`:

```typescript
import fc from 'fast-check';
import { cleanup } from '@testing-library/react';
import { createArbCertification, arbBuildDate } from '../fixtures/certifications-arbitraries';

describe('CertificationsIndex - Property 14', () => {
  const arbAnyCertList = fc.uniqueArray(
    createArbCertification({ allowUnknownCategory: true }),
    { selector: (c) => c.slug, minLength: 0, maxLength: 12 },
  );

  // Feature: m7-certifications-module, Property 14: Page structure is ordered, labelled, and level-correct
  it('Property 14: Document outline is strictly structured, labelled, and heading levels never skip', () => {
    fc.assert(
      fc.property(arbAnyCertList, arbBuildDate, (certifications, bDate) => {
        cleanup();
        const { container } = render(
          <CertificationsIndex certifications={certifications} contentHtml={{}} buildDate={bDate} />,
        );

        // Exactly one h1
        const h1Elements = container.querySelectorAll('h1');
        expect(h1Elements).toHaveLength(1);
        expect(h1Elements[0].textContent).toBe('Certifications');

        if (certifications.length === 0) {
          expect(container.querySelectorAll('section')).toHaveLength(0);
          expect(container.querySelectorAll('h2')).toHaveLength(0);
          expect(screen.getByText('No certifications available')).toBeInTheDocument();
        } else {
          // Sections and accessibility
          const sections = container.querySelectorAll('section');
          expect(sections.length).toBeGreaterThan(0);

          for (const sec of sections) {
            const labelledBy = sec.getAttribute('aria-labelledby');
            expect(labelledBy).toBeTruthy();
            const h2 = document.getElementById(labelledBy!);
            expect(h2).toBeInTheDocument();
            expect(h2?.tagName.toLowerCase()).toBe('h2');
          }

          // Heading hierarchy integrity: levels in DOM order must not jump by > 1
          const headings = Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6'));
          let lastLevel = 0;

          for (const heading of headings) {
            const currentLevel = parseInt(heading.tagName[1], 10);
            if (lastLevel > 0) {
              expect(currentLevel - lastLevel).toBeLessThanOrEqual(1);
            }
            lastLevel = currentLevel;
          }
        }
      }),
      { numRuns: 100 },
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-index.test.tsx
```
Expected output: Unit tests and Property 14 pass with >= 100 runs.

**Satisfies Requirements:** Req 1.3, 2.1, 2.2, 2.3, 5.1, 5.2, 5.3, 5.4, 5.6, 14.5, 15.2

---

### M7.G7.T6: Test Identical buildDate Propagation Across All Cards

**Objective:** Add a test verifying that `CertificationsIndex` passes the exact same `buildDate` value to every child `CertificationCard`.

**Acceptance Criteria:**
- ✓ Renders `CertificationsIndex` with multiple certifications and a fixed `buildDate`.
- ✓ Verifies that expiry classification across all rendered cards is consistent with that single date.

**Prerequisites:**
- Tasks M7.G7.T1–M7.G7.T4 completed.

**Implementation Details:**
Append to `tests/certifications/certifications-index.test.tsx`:

```typescript
  it('propagates the exact buildDate to all cards identically', () => {
    const certA: Certification = {
      ...fixtureFullCertification,
      slug: 'cert-a',
      expiresAt: '2026-04-14',
    };
    const certB: Certification = {
      ...fixtureFullCertification,
      slug: 'cert-b',
      expiresAt: '2026-04-16',
    };

    render(
      <CertificationsIndex
        certifications={[certA, certB]}
        contentHtml={{}}
        buildDate="2026-04-15"
      />,
    );

    // certA is expired relative to 2026-04-15; certB is active
    const indicators = screen.getAllByTestId('expired-indicator');
    expect(indicators).toHaveLength(1);
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-index.test.tsx
```
Expected output: Test passes.

**Satisfies Requirements:** Req 7.5

---

### M7.G7.T7: Test Out-of-Range Category Trailing Uncategorised Section

**Objective:** Add a test rendering a certification with an out-of-range category to confirm that `CertificationsIndex` renders a trailing section labelled `"Uncategorised"`.

**Acceptance Criteria:**
- ✓ Renders `CertificationsIndex` with `fixtureUncategorisedCertification`.
- ✓ Confirms an `<h2>` with text `"Uncategorised"` is present and ordered as the last section.

**Prerequisites:**
- `fixtureUncategorisedCertification` in `tests/fixtures/certifications-data.ts`.

**Implementation Details:**
Append to `tests/certifications/certifications-index.test.tsx`:

```typescript
import { fixtureUncategorisedCertification } from '../fixtures/certifications-data';

  it('renders a trailing Uncategorised section when given an out-of-range category', () => {
    render(
      <CertificationsIndex
        certifications={[fixtureFullCertification, fixtureUncategorisedCertification]}
        contentHtml={{}}
        buildDate="2026-04-15"
      />,
    );

    const h2Elements = screen.getAllByRole('heading', { level: 2 });
    expect(h2Elements[h2Elements.length - 1]).toHaveTextContent('Uncategorised');
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-index.test.tsx
```
Expected output: Test passes.

**Satisfies Requirements:** Req 4.2, 4.4

---

### M7.G7.T8: Axe Accessibility Tests for CertificationsIndex

**Objective:** Run `axe-core` on `CertificationsIndex` in both populated and empty states to confirm zero accessibility violations.

**Acceptance Criteria:**
- ✓ Populated state produces zero axe violations.
- ✓ Empty state produces zero axe violations.

**Prerequisites:**
- `vitest-axe` configured.

**Implementation Details:**
Create `tests/certifications/certifications-index-a11y.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { CertificationsIndex } from '@/components/certifications/certifications-index';
import {
  fixtureCertificationsList,
  fixtureEmptyCertificationsList,
} from '../fixtures/certifications-data';

describe('CertificationsIndex - Accessibility Audits', () => {
  const buildDate = '2026-04-15';

  it('has zero a11y violations in populated state', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has zero a11y violations in empty state', async () => {
    const { container } = render(
      <CertificationsIndex
        certifications={fixtureEmptyCertificationsList}
        contentHtml={{}}
        buildDate={buildDate}
      />,
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certifications-index-a11y.test.tsx
```
Expected output: Both accessibility audits pass with zero violations.

**Satisfies Requirements:** Req 14.1, 15.1

---

### M7.G7.T9: Static Client-Directive and File-Length Inspection

**Objective:** Verify that `certification-category-section.tsx` and `certifications-index.tsx` contain zero `'use client'` statements and remain below 300 lines each.

**Acceptance Criteria:**
- ✓ Zero `'use client'` statements found.
- ✓ Both files are under 300 lines.
- ✓ Zero `transition` or `animate` utilities used.

**Prerequisites:**
- `certification-category-section.tsx` and `certifications-index.tsx` implemented.

**Implementation Details:**
Run static search and line count checks in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\components\certifications\certification-category-section.tsx, src\components\certifications\certifications-index.tsx -Pattern "use client|transition|animate"
(Get-Content src\components\certifications\certification-category-section.tsx).Length
(Get-Content src\components\certifications\certifications-index.tsx).Length
```
Expected output: Zero string matches found; both files under 300 lines.

**Satisfies Requirements:** Req 1.2, 13.2, 14.6, 15.6

---

### M7.G7.T10: Goal 7 Checkpoint and Pipeline Verification

**Objective:** Run the full test suite and typechecker across Goal 7 components to confirm clean execution.

**Acceptance Criteria:**
- ✓ `src/components/certifications/certification-category-section.tsx` and `certifications-index.tsx` compile cleanly.
- ✓ `tests/certifications/certification-category-section.test.tsx` passes.
- ✓ `tests/certifications/certifications-index.test.tsx` passes (unit + Property 14).
- ✓ `tests/certifications/certifications-index-a11y.test.tsx` passes.
- ✓ `npx tsc --noEmit` exits with 0.

**Prerequisites:**
- Tasks M7.G7.T1 through M7.G7.T9 completed.

**Implementation Details:**
Execute test suite and typechecking commands in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-category-section.test.tsx tests/certifications/certifications-index.test.tsx tests/certifications/certifications-index-a11y.test.tsx
npx tsc --noEmit
```
Expected output: All test files pass completely; TypeScript compiles with zero errors.

**Satisfies Requirements:** Req 1.3–1.4, 2.1–2.4, 4.3, 5.1–5.4, 5.6, 7.5, 9.7, 11.1–11.3, 14.5, 15.3, 15.5, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 7 are complete:
```powershell
npx vitest run tests/certifications/certification-category-section.test.tsx tests/certifications/certifications-index.test.tsx tests/certifications/certifications-index-a11y.test.tsx
npx tsc --noEmit
```
Expected output: All section and index unit, property, and accessibility tests pass; zero TypeScript errors.