# M7.G5: ExpiredIndicator, VerificationLink, and BadgeImage

> **Milestone:** M7 — Certifications Module  
> **Goal:** G5 of 10  
> **Tasks:** 10 atomic tasks (M7.G5.T1 – M7.G5.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 7.6–7.8, 8.1–8.3, 8.5–8.8, 9.1–9.5, 9.7, 14.3, 14.6, 15.3), `design.md` (Components and Interfaces, Badges, Links, Tokens), `tasks.md` (M7.G5)

---

## Goal Objective

Implement three core atomic presentation components in `src/components/certifications/`:
1. `expired-indicator.tsx`: visual indicator rendering the text `"Expired"`, an `aria-hidden` icon, and a distinct border cue so status is not conveyed by color alone.
2. `verification-link.tsx`: external verification action composing M3's `ExternalLink`, assigning accessible name `"Verify {title} credential"`, linking to an accessible `"Opens in a new tab"` description, applying `FOCUS_RING` and underline styling, and providing defense-in-depth by rendering `null` for non-HTTPS hrefs.
3. `badge-image.tsx`: badge picture rendering an optimized plain `<img>` with explicit `width={64}` and `height={64}` dimensions, `decoding="async"`, `loading="eager"` when `priority` is true (else `lazy`), constrained to `h-16 w-16 max-w-full object-contain`, carrying a justified `@next/next/no-img-element` disable comment for static export compatibility, and rendering `null` when inputs fail security/pair checks.

Verify all three components with unit tests, accessibility scans via `axe-core`, and keyboard/DOM structure verifications.

---

## Goal Success Criteria

- ✓ `src/components/certifications/expired-indicator.tsx` renders visible text `"Expired"`, an `aria-hidden` warning icon, and a border style cue.
- ✓ `src/components/certifications/verification-link.tsx` renders an M3 `ExternalLink` with `target="_blank"`, `rel="noopener noreferrer"`, `aria-label="Verify {title} credential"`, and an `aria-describedby` target announcing new-tab opening.
- ✓ `verification-link.tsx` renders `null` if given a non-HTTPS URL.
- ✓ `src/components/certifications/badge-image.tsx` renders `<img width={64} height={64} ...>` with priority-aware loading and returns `null` for invalid or unpaired inputs.
- ✓ Zero `'use client'` directives; zero transition/animation classes (`transition-*`, `animate-*`).
- ✓ Zero hardcoded hex colors; uses only Tailwind tokens mapped to semantic colors.
- ✓ All three components pass automated `axe-core` accessibility checks with zero violations.

---

## Prerequisites

- Goal 1 completed: `src/components/ui/` M3 primitives (`ExternalLink`, `FOCUS_RING`) verified.
- Goal 3 completed: `src/lib/certifications/verification-href.ts` and `src/lib/certifications/badge-source.ts` available.
- Testing environment: `@testing-library/react` and `vitest-axe` configured.

---

## Tasks

### M7.G5.T1: Implement ExpiredIndicator Component

**Objective:** Create `src/components/certifications/expired-indicator.tsx` rendering the visible `"Expired"` label with non-color cues (icon and border).

**Acceptance Criteria:**
- ✓ Exports function component `ExpiredIndicator()`.
- ✓ Renders a container `<span>` with border styling (e.g., `border border-feedback-warning/40` or semantic token border).
- ✓ Renders an SVG warning/clock icon marked with `aria-hidden="true"`.
- ✓ Renders visible text `"Expired"`.
- ✓ Contains no `'use client'` directive.
- ✓ Does not rely on color alone to communicate expiry (includes icon, text, and border).

**Prerequisites:**
- Semantic tokens available from Tailwind configuration.

**Implementation Details:**
Create `src/components/certifications/expired-indicator.tsx`:

```typescript
import React from 'react';

export function ExpiredIndicator(): React.JSX.Element {
  return (
    <span
      data-testid="expired-indicator"
      className="inline-flex items-center gap-1.5 px-2 py-0.5 text-caption font-medium rounded-sm border border-feedback-warning text-feedback-warning bg-feedback-warning/10"
    >
      <svg
        className="w-3.5 h-3.5 flex-shrink-0"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth="2"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
        />
      </svg>
      <span>Expired</span>
    </span>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 7.6, 7.8, 14.2

---

### M7.G5.T2: Implement VerificationLink Component

**Objective:** Create `src/components/certifications/verification-link.tsx` rendering the external verification link with distinct focus ring, underline, and accessible descriptions.

**Acceptance Criteria:**
- ✓ Exports interface `VerificationLinkProps` with `readonly title: string`, `readonly slug: string`, `readonly href: string`.
- ✓ Composes M3 `ExternalLink` with `href={href}`, `target="_blank"`, `rel="noopener noreferrer"`.
- ✓ Sets `aria-label="Verify {title} credential"`.
- ✓ Associates with a visually hidden element via `aria-describedby={`cert-${slug}-newtab`}`.
- ✓ Renders a visually hidden `<span id={`cert-${slug}-newtab`} className="sr-only">Opens in a new tab</span>`.
- ✓ Applies `FOCUS_RING` and `underline` styling.

**Prerequisites:**
- `src/components/ui/ExternalLink.tsx` and `FOCUS_RING` available from `@/components/ui/ExternalLink` or `@/components/ui`.

**Implementation Details:**
Create `src/components/certifications/verification-link.tsx`:

```typescript
import React from 'react';
import { ExternalLink, FOCUS_RING } from '@/components/ui/ExternalLink';
import { getVerificationHref } from '@/lib/certifications/verification-href';

export interface VerificationLinkProps {
  readonly title: string;
  readonly slug: string;
  readonly href: string;
}

export function VerificationLink({
  title,
  slug,
  href,
}: VerificationLinkProps): React.JSX.Element | null {
  const validHref = getVerificationHref({ verificationUrl: href });
  if (!validHref) {
    return null;
  }

  const descriptionId = `cert-${slug}-newtab`;

  return (
    <>
      <ExternalLink
        href={validHref}
        aria-label={`Verify ${title} credential`}
        aria-describedby={descriptionId}
        className={`${FOCUS_RING} inline-flex items-center gap-1 text-small font-medium text-brand-primary underline hover:text-brand-primary/80`}
      >
        <span>Verify credential</span>
      </ExternalLink>
      <span id={descriptionId} className="sr-only">
        Opens in a new tab
      </span>
    </>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 8.1, 8.2, 8.3, 8.4, 8.7, 8.8, 14.3, 14.4

---

### M7.G5.T3: Add Defense-in-Depth HTTPS Guard to VerificationLink

**Objective:** Verify that `VerificationLink` renders `null` when provided with invalid, non-HTTPS, or empty URL values.

**Acceptance Criteria:**
- ✓ Calls `getVerificationHref({ verificationUrl: href })`.
- ✓ If helper returns `null`, `VerificationLink` renders `null` without throwing or emitting an empty anchor tag.
- ✓ Verified for `http://`, `javascript:`, empty string, and whitespace.

**Prerequisites:**
- `M7.G5.T2` completed.

**Implementation Details:**
Confirm guard implementation in `src/components/certifications/verification-link.tsx`:
```typescript
  const validHref = getVerificationHref({ verificationUrl: href });
  if (!validHref) {
    return null;
  }
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero errors.

**Satisfies Requirements:** Req 8.5, 8.6

---

### M7.G5.T4: Implement BadgeImage Component

**Objective:** Create `src/components/certifications/badge-image.tsx` using a plain `<img>` with explicit dimensions, priority-aware loading, and ESLint suppression for static export compatibility.

**Acceptance Criteria:**
- ✓ Exports interface `BadgeImageProps` with `readonly src: string`, `readonly alt: string`, `readonly priority: boolean`.
- ✓ Renders a plain `<img>` with `width={64}` and `height={64}` to reserve layout space and prevent CLS.
- ✓ Sets `decoding="async"`.
- ✓ Sets `loading={priority ? 'eager' : 'lazy'}`.
- ✓ Applies responsive classes `h-16 w-16 max-w-full object-contain`.
- ✓ Includes justified comment: `// eslint-disable-next-line @next/next/no-img-element -- plain img required for static export compatibility`.

**Prerequisites:**
- `getBadgeSource` available from `@/lib/certifications/badge-source`.

**Implementation Details:**
Create `src/components/certifications/badge-image.tsx`:

```typescript
import React from 'react';
import { getBadgeSource } from '@/lib/certifications/badge-source';

export interface BadgeImageProps {
  readonly src: string;
  readonly alt: string;
  readonly priority: boolean;
}

export function BadgeImage({
  src,
  alt,
  priority,
}: BadgeImageProps): React.JSX.Element | null {
  const source = getBadgeSource({ badgeImageUrl: src, badgeImageAlt: alt });
  if (!source) {
    return null;
  }

  return (
    <div className="flex-shrink-0">
      {/* eslint-disable-next-line @next/next/no-img-element -- plain img required for Next.js static export compatibility without custom loader */}
      <img
        src={source.src}
        alt={source.alt}
        width={64}
        height={64}
        decoding="async"
        loading={priority ? 'eager' : 'lazy'}
        className="h-16 w-16 max-w-full object-contain"
      />
    </div>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 9.1, 9.4, 9.5, 9.6, 9.7

---

### M7.G5.T5: Add Pair and Prefix Validation Guard to BadgeImage

**Objective:** Verify that `BadgeImage` returns `null` and renders no wrapper or empty image element when inputs are invalid.

**Acceptance Criteria:**
- ✓ When `src` or `alt` is empty/whitespace, returns `null`.
- ✓ When `src` points outside `/images/certifications/` or `https://`, returns `null`.
- ✓ Verified that no empty `<div>` container is left in the DOM.

**Prerequisites:**
- `M7.G5.T4` completed.

**Implementation Details:**
Ensure `src/components/certifications/badge-image.tsx` executes `getBadgeSource` guard before rendering DOM markup.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero errors.

**Satisfies Requirements:** Req 9.2, 9.3

---

### M7.G5.T6: Unit Tests for ExpiredIndicator

**Objective:** Create `tests/certifications/expired-indicator.test.tsx` verifying DOM output, text content, and accessible icon.

**Acceptance Criteria:**
- ✓ Renders visible text `"Expired"`.
- ✓ Verifies SVG icon has `aria-hidden="true"`.
- ✓ Verifies border class is present on container element.

**Prerequisites:**
- `src/components/certifications/expired-indicator.tsx` implemented.
- React Testing Library installed.

**Implementation Details:**
Create `tests/certifications/expired-indicator.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ExpiredIndicator } from '@/components/certifications/expired-indicator';

describe('ExpiredIndicator - Component Tests', () => {
  it('renders visible Expired text and aria-hidden icon', () => {
    const { container } = render(<ExpiredIndicator />);

    const badge = screen.getByTestId('expired-indicator');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent('Expired');

    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
    expect(svg).toHaveAttribute('aria-hidden', 'true');
  });

  it('contains border styling for non-color status indication', () => {
    render(<ExpiredIndicator />);
    const badge = screen.getByTestId('expired-indicator');
    expect(badge.className).toContain('border');
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/expired-indicator.test.tsx
```
Expected output: All unit tests pass.

**Satisfies Requirements:** Req 7.6, 7.8

---

### M7.G5.T7: Unit Tests for VerificationLink

**Objective:** Create `tests/certifications/verification-link.test.tsx` testing attribute assignment, accessible name, description target, and defense guard.

**Acceptance Criteria:**
- ✓ Renders anchor with `aria-label="Verify AWS Solutions Architect credential"`.
- ✓ Anchor has `href="https://aws.amazon.com/verify/123"`.
- ✓ Anchor has `target="_blank"` and `rel="noopener noreferrer"`.
- ✓ Element referenced by `aria-describedby` exists in DOM and reads `"Opens in a new tab"`.
- ✓ Renders `null` for non-HTTPS URL (`http://...`).

**Prerequisites:**
- `src/components/certifications/verification-link.tsx` implemented.

**Implementation Details:**
Create `tests/certifications/verification-link.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { VerificationLink } from '@/components/certifications/verification-link';

describe('VerificationLink - Component Tests', () => {
  it('renders valid https link with accessible name and description', () => {
    render(
      <VerificationLink
        title="AWS Solutions Architect"
        slug="aws-solutions-architect"
        href="https://aws.amazon.com/verify/123"
      />,
    );

    const link = screen.getByRole('link', { name: 'Verify AWS Solutions Architect credential' });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'https://aws.amazon.com/verify/123');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');

    const describedById = link.getAttribute('aria-describedby');
    expect(describedById).toBe('cert-aws-solutions-architect-newtab');

    const descSpan = document.getElementById(describedById!);
    expect(descSpan).toBeInTheDocument();
    expect(descSpan).toHaveTextContent('Opens in a new tab');
  });

  it('renders null when href is not https', () => {
    const { container } = render(
      <VerificationLink
        title="Insecure Credential"
        slug="insecure-cred"
        href="http://insecure.org/verify"
      />,
    );

    expect(container).toBeEmptyDOMElement();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/verification-link.test.tsx
```
Expected output: All unit tests pass.

**Satisfies Requirements:** Req 8.1, 8.2, 8.3, 8.5, 8.6, 8.8, 14.4

---

### M7.G5.T8: Unit Tests for BadgeImage

**Objective:** Create `tests/certifications/badge-image.test.tsx` verifying plain `img` attributes, eager vs lazy loading, and invalid source handling.

**Acceptance Criteria:**
- ✓ Sets `src`, `alt`, `width="64"`, `height="64"`.
- ✓ Sets `loading="eager"` when `priority={true}`.
- ✓ Sets `loading="lazy"` when `priority={false}`.
- ✓ Returns `null` when `src` is missing or alt is empty.

**Prerequisites:**
- `src/components/certifications/badge-image.tsx` implemented.

**Implementation Details:**
Create `tests/certifications/badge-image.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BadgeImage } from '@/components/certifications/badge-image';

describe('BadgeImage - Component Tests', () => {
  it('renders plain img with attributes and eager loading when priority is true', () => {
    const { container } = render(
      <BadgeImage
        src="/images/certifications/aws.png"
        alt="AWS Certification Badge"
        priority={true}
      />,
    );

    const img = container.querySelector('img');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', '/images/certifications/aws.png');
    expect(img).toHaveAttribute('alt', 'AWS Certification Badge');
    expect(img).toHaveAttribute('width', '64');
    expect(img).toHaveAttribute('height', '64');
    expect(img).toHaveAttribute('loading', 'eager');
  });

  it('renders plain img with lazy loading when priority is false', () => {
    const { container } = render(
      <BadgeImage
        src="https://badges.org/badge.png"
        alt="Remote Badge"
        priority={false}
      />,
    );

    const img = container.querySelector('img');
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('loading', 'lazy');
  });

  it('renders null when alt is empty or url has invalid prefix', () => {
    const { container: c1 } = render(
      <BadgeImage src="/images/certifications/aws.png" alt="   " priority={false} />,
    );
    expect(c1).toBeEmptyDOMElement();

    const { container: c2 } = render(
      <BadgeImage src="/invalid/path.png" alt="Invalid Path" priority={false} />,
    );
    expect(c2).toBeEmptyDOMElement();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/badge-image.test.tsx
```
Expected output: All unit tests pass.

**Satisfies Requirements:** Req 9.1, 9.2, 9.3, 9.4, 9.7

---

### M7.G5.T9: Axe Accessibility Tests for Atomic Components

**Objective:** Run `axe-core` checks on `ExpiredIndicator`, `VerificationLink`, and `BadgeImage` to guarantee zero WCAG violations.

**Acceptance Criteria:**
- ✓ Tests `ExpiredIndicator` via `axe` with zero violations.
- ✓ Tests `VerificationLink` via `axe` with zero violations.
- ✓ Tests `BadgeImage` via `axe` with zero violations.

**Prerequisites:**
- `vitest-axe` helper available.

**Implementation Details:**
Create `tests/certifications/atomic-components-a11y.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { ExpiredIndicator } from '@/components/certifications/expired-indicator';
import { VerificationLink } from '@/components/certifications/verification-link';
import { BadgeImage } from '@/components/certifications/badge-image';

describe('Atomic Presentation Components - Accessibility', () => {
  it('ExpiredIndicator has no a11y violations', async () => {
    const { container } = render(<ExpiredIndicator />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('VerificationLink has no a11y violations', async () => {
    const { container } = render(
      <VerificationLink
        title="Kubernetes Administrator"
        slug="kubernetes-administrator"
        href="https://cncf.io/verify/100"
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('BadgeImage has no a11y violations', async () => {
    const { container } = render(
      <BadgeImage
        src="/images/certifications/aws.png"
        alt="AWS Certified Solutions Architect Badge"
        priority={true}
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
npx vitest run tests/certifications/atomic-components-a11y.test.tsx
```
Expected output: All accessibility tests pass with zero violations.

**Satisfies Requirements:** Req 14.1, 15.1

---

### M7.G5.T10: Goal 5 Checkpoint and Hygiene Inspection

**Objective:** Audit Goal 5 components for absence of client directives, transitions/animations, and file length under 300 lines.

**Acceptance Criteria:**
- ✓ Files `expired-indicator.tsx`, `verification-link.tsx`, and `badge-image.tsx` contain zero `'use client'` statements.
- ✓ Zero `transition` or `animate` utilities used.
- ✓ All three source files are well under 300 lines.
- ✓ All test files pass; `npx tsc --noEmit` exits with 0.

**Prerequisites:**
- Tasks M7.G5.T1 through M7.G5.T9 completed.

**Implementation Details:**
Execute static inspection and run test suites in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\components\certifications\*.tsx -Pattern "use client|transition|animate"
npx vitest run tests/certifications/expired-indicator.test.tsx tests/certifications/verification-link.test.tsx tests/certifications/badge-image.test.tsx tests/certifications/atomic-components-a11y.test.tsx
npx tsc --noEmit
```
Expected output:
- No string matches found.
- All test suites pass.
- TypeScript compiler exits with code 0.

**Satisfies Requirements:** Req 1.2, 13.2, 14.6, 15.3, 15.5, 15.6, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 5 are complete:
```powershell
npx vitest run tests/certifications/expired-indicator.test.tsx tests/certifications/verification-link.test.tsx tests/certifications/badge-image.test.tsx tests/certifications/atomic-components-a11y.test.tsx
npx tsc --noEmit
```
Expected output: All atomic component and accessibility tests pass; zero TypeScript errors.