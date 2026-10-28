# M7.G6: CertificationCard and Render Properties

> **Milestone:** M7 — Certifications Module  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks (M7.G6.T1 – M7.G6.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 6.1–6.9, 7.6–7.7, 8.2, 9.1–9.4, 10.1–10.4, 11.4, 11.6, 14.4, 14.7), `design.md` (Properties 8, 9, 10 render half, 11 render half, 13 render half), `tasks.md` (M7.G6)

---

## Goal Objective

Implement `src/components/certifications/certification-card.tsx` as a pure server component composing M3 UI primitives (`Card`, `Tag`, `MarkdownDoc`) and M7 atomic components (`BadgeImage`, `ExpiredIndicator`, `VerificationLink`). The component renders credentials within an equal-height card (`h-full`), formats dates deterministically via M5's `formatDisplayDate` inside semantic `<time>` elements, conditionally renders expiration dates and non-empty credential identifiers, renders shifted markdown supporting content via `MarkdownDoc`, wraps long strings with `break-words` to eliminate horizontal overflow at 375px, and avoids inventing or hallucinating data.

Verify complete rendering correctness, security constraints, and accessibility via unit tests, fast-check property tests (Properties 8, 9, 10 render half, 11 render half, 13 render half), and `axe-core` accessibility audits.

---

## Goal Success Criteria

- ✓ `src/components/certifications/certification-card.tsx` renders certification title in an `<h3>` inside an M3 `Card` with `className="h-full flex flex-col"`.
- ✓ Formats `issuedAt` via `formatDisplayDate` inside `<time dateTime={issuedAt}>` as `"Issued {date}"`.
- ✓ Formats `expiresAt` inside `<time dateTime={expiresAt}>` as `"Expires {date}"` iff `expiresAt !== null`; renders zero expiry markup if `null`.
- ✓ Renders `"Credential ID: {credentialId}"` iff `credentialId` is non-empty after trimming; renders zero placeholder text if empty/null.
- ✓ Displays category tag via M3 `Tag` with label resolved by `getCategoryLabel`.
- ✓ Renders `ExpiredIndicator` iff `getCertificationStatus(cert, buildDate) === 'expired'`.
- ✓ Renders `VerificationLink` iff `getVerificationHref(cert) !== null`.
- ✓ Renders `BadgeImage` iff `getBadgeSource(cert) !== null`, forwarding `priority`.
- ✓ Renders `MarkdownDoc` iff `contentHtml` is provided and non-empty; zero `dangerouslySetInnerHTML` in the component.
- ✓ All text elements apply `break-words` to prevent overflow at 375px.
- ✓ Fast-check Properties 8, 9, 10 (render half), 11 (render half), and 13 (render half) pass with >= 100 runs.
- ✓ `axe-core` passes with zero violations across populated, expired, and minimal fixtures.

---

## Prerequisites

- Goal 1 completed: `tests/fixtures/` available.
- Goal 3 completed: `src/lib/certifications/certification-status.ts`, `verification-href.ts`, and `badge-source.ts` available.
- Goal 4 completed: `src/lib/certifications/load-supporting-content.ts` and `shift-headings.ts` available.
- Goal 5 completed: `ExpiredIndicator`, `VerificationLink`, and `BadgeImage` available.
- M3 primitives (`Card`, `Tag`, `MarkdownDoc`) available in `src/components/ui/`.
- M5 `formatDisplayDate` available at `@/lib/format-date`.

---

## Tasks

### M7.G6.T1: Create CertificationCard Foundation and Primary Content

**Objective:** Create `src/components/certifications/certification-card.tsx` defining `CertificationCardProps`, the outer M3 `Card` container with equal-height styling, `<h3>` title, issuer, category tag, and semantic "Issued" date.

**Acceptance Criteria:**
- ✓ Exports interface `CertificationCardProps`:
  ```typescript
  export interface CertificationCardProps {
    readonly certification: Certification;
    readonly buildDate: IsoDateString;
    readonly contentHtml?: string;
    readonly priority: boolean;
  }
  ```
- ✓ Renders M3 `Card` with `className="h-full flex flex-col justify-between"`.
- ✓ Renders `title` inside `<h3>` with `break-words text-heading-4 font-semibold text-text-primary`.
- ✓ Renders `issuer` with `break-words text-small text-text-secondary`.
- ✓ Renders category `Tag` using label from `getCategoryLabel(certification.category)`.
- ✓ Formats `issuedAt` via `formatDisplayDate(certification.issuedAt)` inside `<time dateTime={certification.issuedAt}>`.
- ✓ Text is prefixed with `"Issued "` (`Issued <time ...>`).

**Prerequisites:**
- `@/types/content` exports `Certification` and `IsoDateString`.
- `@/components/ui/Card` and `@/components/ui/Tag` available.
- `@/lib/format-date` exports `formatDisplayDate`.
- `@/lib/certifications/category-label` exports `getCategoryLabel`.

**Implementation Details:**
Create initial `src/components/certifications/certification-card.tsx`:

```typescript
import React from 'react';
import type { Certification, IsoDateString } from '@/types/content';
import { Card } from '@/components/ui/Card';
import { Tag } from '@/components/ui/Tag';
import { formatDisplayDate } from '@/lib/format-date';
import { getCategoryLabel } from '@/lib/certifications/category-label';

export interface CertificationCardProps {
  readonly certification: Certification;
  readonly buildDate: IsoDateString;
  readonly contentHtml?: string;
  readonly priority: boolean;
}

export function CertificationCard({
  certification,
  buildDate,
  contentHtml,
  priority,
}: CertificationCardProps): React.JSX.Element {
  const categoryLabel = getCategoryLabel(certification.category as any);

  return (
    <Card className="h-full flex flex-col justify-between p-6 bg-bg-surface border border-border-default rounded-lg">
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <Tag variant="neutral">{categoryLabel}</Tag>
            <h3 className="text-heading-4 font-semibold text-text-primary break-words mt-2">
              {certification.title}
            </h3>
            <p className="text-small text-text-secondary break-words font-medium">
              {certification.issuer}
            </p>
          </div>
        </div>

        <div className="text-caption text-text-secondary space-y-1">
          <p>
            Issued{' '}
            <time dateTime={certification.issuedAt} className="font-medium text-text-primary">
              {formatDisplayDate(certification.issuedAt)}
            </time>
          </p>
        </div>
      </div>
    </Card>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 1.5, 6.1, 6.2, 6.3, 6.6, 11.4, 11.6, 14.7

---

### M7.G6.T2: Add Conditional Expiry and Credential Identifier Markup

**Objective:** Add conditional rendering for `expiresAt` and `credentialId` ensuring no empty elements or placeholders are emitted when values are missing or whitespace-only.

**Acceptance Criteria:**
- ✓ If `certification.expiresAt !== null`, renders `"Expires "` followed by `<time dateTime={certification.expiresAt}>{formatDisplayDate(certification.expiresAt)}</time>`.
- ✓ If `certification.expiresAt === null`, renders zero expiry markup.
- ✓ If `certification.credentialId` is non-empty after trimming, renders `"Credential ID: {certification.credentialId}"` with the exact stored string.
- ✓ If `certification.credentialId` is `null` or whitespace-only, renders zero credential ID markup.

**Prerequisites:**
- `M7.G6.T1` completed in `src/components/certifications/certification-card.tsx`.

**Implementation Details:**
Update the date and metadata block in `src/components/certifications/certification-card.tsx`:

```typescript
        <div className="text-caption text-text-secondary space-y-1">
          <p>
            Issued{' '}
            <time dateTime={certification.issuedAt} className="font-medium text-text-primary">
              {formatDisplayDate(certification.issuedAt)}
            </time>
          </p>
          {certification.expiresAt && (
            <p>
              Expires{' '}
              <time dateTime={certification.expiresAt} className="font-medium text-text-primary">
                {formatDisplayDate(certification.expiresAt)}
              </time>
            </p>
          )}
          {certification.credentialId && certification.credentialId.trim().length > 0 && (
            <p className="break-words">
              Credential ID:{' '}
              <span className="font-mono text-text-primary">{certification.credentialId}</span>
            </p>
          )}
        </div>
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 6.4, 6.5, 6.7, 6.8, 14.7

---

### M7.G6.T3: Integrate Status, ExpiredIndicator, VerificationLink, and BadgeImage

**Objective:** Connect atomic helpers and components into `CertificationCard`, ensuring status indicator, verification link, and badge image render according to spec constraints.

**Acceptance Criteria:**
- ✓ Invokes `getCertificationStatus(certification, buildDate)`.
- ✓ Renders `<ExpiredIndicator />` iff status is `'expired'`.
- ✓ Invokes `getBadgeSource(certification)`.
- ✓ If source is valid, renders `<BadgeImage src={source.src} alt={source.alt} priority={priority} />`.
- ✓ Invokes `getVerificationHref(certification)`.
- ✓ If href is valid, renders `<VerificationLink title={certification.title} slug={certification.slug} href={validHref} />`.
- ✓ Verification action sits in card footer (`mt-6 pt-4 border-t border-border-default`).

**Prerequisites:**
- Goal 3 helpers (`getCertificationStatus`, `getVerificationHref`, `getBadgeSource`).
- Goal 5 components (`ExpiredIndicator`, `VerificationLink`, `BadgeImage`).

**Implementation Details:**
Update `src/components/certifications/certification-card.tsx`:

```typescript
import React from 'react';
import type { Certification, IsoDateString } from '@/types/content';
import { Card } from '@/components/ui/Card';
import { Tag } from '@/components/ui/Tag';
import { formatDisplayDate } from '@/lib/format-date';
import { getCategoryLabel } from '@/lib/certifications/category-label';
import { getCertificationStatus } from '@/lib/certifications/certification-status';
import { getVerificationHref } from '@/lib/certifications/verification-href';
import { getBadgeSource } from '@/lib/certifications/badge-source';
import { ExpiredIndicator } from './expired-indicator';
import { VerificationLink } from './verification-link';
import { BadgeImage } from './badge-image';

export interface CertificationCardProps {
  readonly certification: Certification;
  readonly buildDate: IsoDateString;
  readonly contentHtml?: string;
  readonly priority: boolean;
}

export function CertificationCard({
  certification,
  buildDate,
  contentHtml,
  priority,
}: CertificationCardProps): React.JSX.Element {
  const categoryLabel = getCategoryLabel(certification.category as any);
  const status = getCertificationStatus(certification, buildDate);
  const badgeSource = getBadgeSource(certification);
  const verificationHref = getVerificationHref(certification);

  return (
    <Card className="h-full flex flex-col justify-between p-6 bg-bg-surface border border-border-default rounded-lg">
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <Tag variant="neutral">{categoryLabel}</Tag>
              {status === 'expired' && <ExpiredIndicator />}
            </div>
            <h3 className="text-heading-4 font-semibold text-text-primary break-words mt-2">
              {certification.title}
            </h3>
            <p className="text-small text-text-secondary break-words font-medium">
              {certification.issuer}
            </p>
          </div>

          {badgeSource && (
            <BadgeImage
              src={badgeSource.src}
              alt={badgeSource.alt}
              priority={priority}
            />
          )}
        </div>

        <div className="text-caption text-text-secondary space-y-1">
          <p>
            Issued{' '}
            <time dateTime={certification.issuedAt} className="font-medium text-text-primary">
              {formatDisplayDate(certification.issuedAt)}
            </time>
          </p>
          {certification.expiresAt && (
            <p>
              Expires{' '}
              <time dateTime={certification.expiresAt} className="font-medium text-text-primary">
                {formatDisplayDate(certification.expiresAt)}
              </time>
            </p>
          )}
          {certification.credentialId && certification.credentialId.trim().length > 0 && (
            <p className="break-words">
              Credential ID:{' '}
              <span className="font-mono text-text-primary">{certification.credentialId}</span>
            </p>
          )}
        </div>
      </div>

      {verificationHref && (
        <div className="mt-6 pt-4 border-t border-border-default">
          <VerificationLink
            title={certification.title}
            slug={certification.slug}
            href={verificationHref}
          />
        </div>
      )}
    </Card>
  );
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 7.6, 7.7, 8.1, 8.5, 9.1, 9.2, 9.7

---

### M7.G6.T4: Integrate MarkdownDoc for Supporting Content and Zero-HTML Safety

**Objective:** Add conditional rendering of supporting content using M3's `MarkdownDoc` container and verify zero usage of `dangerouslySetInnerHTML`.

**Acceptance Criteria:**
- ✓ Renders `<MarkdownDoc html={contentHtml} className="mt-4 prose prose-sm max-w-none break-words" />` iff `contentHtml` is non-empty string.
- ✓ If `contentHtml` is undefined or whitespace, renders zero `MarkdownDoc` container.
- ✓ `certification-card.tsx` contains zero references to `dangerouslySetInnerHTML`.

**Prerequisites:**
- `src/components/ui/MarkdownDoc.tsx` available.
- `M7.G6.T3` completed.

**Implementation Details:**
Import `MarkdownDoc` and append to the top container in `src/components/certifications/certification-card.tsx`:

```typescript
import { MarkdownDoc } from '@/components/ui/MarkdownDoc';

// Inside JSX, immediately following the metadata block:
        {contentHtml && contentHtml.trim().length > 0 && (
          <div className="mt-4 pt-4 border-t border-border-default/60">
            <MarkdownDoc html={contentHtml} className="prose prose-sm max-w-none break-words text-small text-text-secondary" />
          </div>
        )}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero compilation errors.

**Satisfies Requirements:** Req 10.1, 10.2, 10.4

---

### M7.G6.T5: Unit Tests for CertificationCard

**Objective:** Create `tests/certifications/certification-card.test.tsx` testing rendering of full, minimal, expired, whitespace-credential, and extreme long-text fixtures.

**Acceptance Criteria:**
- ✓ Full fixture: renders `<h3>`, issuer, issued date, expiry date, credential ID, badge image, and verification link.
- ✓ Minimal fixture: renders zero expiry markup, zero credential ID markup, zero badge image, and zero verification link.
- ✓ Expired fixture: renders `ExpiredIndicator`.
- ✓ Whitespace credential fixture: renders zero `"Credential ID:"` text.
- ✓ Long text fixture: renders 120-character title and 60-character credential ID with `break-words`.

**Prerequisites:**
- `src/components/certifications/certification-card.tsx` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/certification-card.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CertificationCard } from '@/components/certifications/certification-card';
import {
  fixtureFullCertification,
  fixtureMinimalCertification,
  fixtureExpiredCertification,
  fixtureWhitespaceCredentialCertification,
  fixtureLongTextCertification,
} from '../fixtures/certifications-data';

describe('CertificationCard - Unit Tests', () => {
  const buildDate = '2026-04-15';

  it('renders all fields for full certification fixture', () => {
    render(
      <CertificationCard
        certification={fixtureFullCertification}
        buildDate={buildDate}
        contentHtml="<h4>Competencies</h4><p>Details</p>"
        priority={true}
      />,
    );

    expect(screen.getByRole('heading', { level: 3, name: fixtureFullCertification.title })).toBeInTheDocument();
    expect(screen.getByText(fixtureFullCertification.issuer)).toBeInTheDocument();
    expect(screen.getByText(/Issued/)).toBeInTheDocument();
    expect(screen.getByText(/Expires/)).toBeInTheDocument();
    expect(screen.getByText(fixtureFullCertification.credentialId!)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: `Verify ${fixtureFullCertification.title} credential` })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: fixtureFullCertification.badgeImageAlt! })).toBeInTheDocument();
    expect(screen.getByText('Competencies')).toBeInTheDocument();
  });

  it('omits optional fields cleanly for minimal fixture', () => {
    const { container } = render(
      <CertificationCard
        certification={fixtureMinimalCertification}
        buildDate={buildDate}
        priority={false}
      />,
    );

    expect(screen.getByRole('heading', { level: 3, name: fixtureMinimalCertification.title })).toBeInTheDocument();
    expect(screen.queryByText(/Expires/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Credential ID/)).not.toBeInTheDocument();
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
    expect(container.querySelector('img')).toBeNull();
  });

  it('renders ExpiredIndicator for expired fixture', () => {
    render(
      <CertificationCard
        certification={fixtureExpiredCertification}
        buildDate={buildDate}
        priority={false}
      />,
    );

    expect(screen.getByTestId('expired-indicator')).toBeInTheDocument();
    expect(screen.getByText('Expired')).toBeInTheDocument();
  });

  it('omits credential id line when whitespace-only', () => {
    render(
      <CertificationCard
        certification={fixtureWhitespaceCredentialCertification}
        buildDate={buildDate}
        priority={false}
      />,
    );

    expect(screen.queryByText(/Credential ID/)).not.toBeInTheDocument();
  });

  it('renders long text with break-words classes', () => {
    render(
      <CertificationCard
        certification={fixtureLongTextCertification}
        buildDate={buildDate}
        priority={false}
      />,
    );

    const heading = screen.getByRole('heading', { level: 3, name: fixtureLongTextCertification.title });
    expect(heading.className).toContain('break-words');
    expect(screen.getByText(fixtureLongTextCertification.credentialId!)).toBeInTheDocument();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-card.test.tsx
```
Expected output: All 5 unit tests pass.

**Satisfies Requirements:** Req 6.1, 6.2, 6.3, 6.4, 6.5, 6.7, 6.8, 7.6, 8.5, 9.2, 11.6

---

### M7.G6.T6: Property 8 Test — Field Traceability and Rendering Fidelity

**Objective:** Append Property 8 test to `tests/certifications/certification-card.test.tsx` verifying that every rendered field is strictly traceable to props without data fabrication.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 8: Card shows exactly the fields it was given`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Verifies title is in `h3`, issuer is present, `<time dateTime={issuedAt}>` matches `formatDisplayDate(issuedAt)`.
- ✓ Verifies `<time dateTime={expiresAt}>` appears iff `expiresAt !== null`.
- ✓ Verifies `"Credential ID:"` appears iff `credentialId?.trim()` is non-empty.

**Prerequisites:**
- `arbCertification` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/certification-card.test.tsx`:

```typescript
import fc from 'fast-check';
import { cleanup } from '@testing-library/react';
import { arbCertification, arbBuildDate } from '../fixtures/certifications-arbitraries';
import { formatDisplayDate } from '@/lib/format-date';

describe('CertificationCard - Property 8', () => {
  // Feature: m7-certifications-module, Property 8: Card shows exactly the fields it was given
  it('Property 8: Rendered card strictly reflects input props without fabrication', () => {
    fc.assert(
      fc.property(arbCertification, arbBuildDate, (cert, bDate) => {
        cleanup();
        render(<CertificationCard certification={cert} buildDate={bDate} priority={false} />);

        // Title in h3
        expect(screen.getByRole('heading', { level: 3, name: cert.title })).toBeInTheDocument();

        // Issued time
        const issuedTime = document.querySelector(`time[dateTime="${cert.issuedAt}"]`);
        expect(issuedTime).toBeInTheDocument();
        expect(issuedTime?.textContent).toBe(formatDisplayDate(cert.issuedAt));

        // Expiry time conditional
        const expiryTime = cert.expiresAt ? document.querySelector(`time[dateTime="${cert.expiresAt}"]`) : null;
        if (cert.expiresAt) {
          expect(expiryTime).toBeInTheDocument();
          expect(expiryTime?.textContent).toBe(formatDisplayDate(cert.expiresAt));
        } else {
          expect(expiryTime).toBeNull();
        }

        // Credential ID conditional
        const hasCredId = Boolean(cert.credentialId && cert.credentialId.trim().length > 0);
        if (hasCredId) {
          expect(screen.getByText(cert.credentialId!)).toBeInTheDocument();
        } else {
          expect(screen.queryByText(/Credential ID:/)).toBeNull();
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
npx vitest run tests/certifications/certification-card.test.tsx
```
Expected output: Unit tests and Property 8 pass.

**Satisfies Requirements:** Req 6.1–6.9, 14.7, 15.2

---

### M7.G6.T7: Property 9 and Property 10 (Render Half) Tests

**Objective:** Append Property 9 (Expired indicator) and Property 10 (Verification link render half) tests to `tests/certifications/certification-card.test.tsx`.

**Acceptance Criteria:**
- ✓ Property 9 tagged: `Feature: m7-certifications-module, Property 9: Expired indicator appears if and only if expired`.
- ✓ Property 9 verifies text `"Expired"` appears iff `getCertificationStatus(cert, buildDate) === 'expired'`.
- ✓ Property 10 tagged: `Feature: m7-certifications-module, Property 10: Verification link follows the HTTPS rule (Render Half)`.
- ✓ Property 10 verifies verification link appears iff `getVerificationHref(cert) !== null`, and link accessible name is `"Verify {title} credential"`.

**Prerequisites:**
- Tasks M7.G6.T1–M7.G6.T6 completed.

**Implementation Details:**
Append to `tests/certifications/certification-card.test.tsx`:

```typescript
import { getCertificationStatus } from '@/lib/certifications/certification-status';
import { getVerificationHref } from '@/lib/certifications/verification-href';

describe('CertificationCard - Properties 9 & 10', () => {
  // Feature: m7-certifications-module, Property 9: Expired indicator appears if and only if expired
  it('Property 9: Expired indicator renders iff status is expired', () => {
    fc.assert(
      fc.property(arbCertification, arbBuildDate, (cert, bDate) => {
        cleanup();
        render(<CertificationCard certification={cert} buildDate={bDate} priority={false} />);
        const status = getCertificationStatus(cert, bDate);

        if (status === 'expired') {
          expect(screen.getByTestId('expired-indicator')).toBeInTheDocument();
        } else {
          expect(screen.queryByTestId('expired-indicator')).toBeNull();
        }
      }),
      { numRuns: 100 },
    );
  });

  // Feature: m7-certifications-module, Property 10: Verification link follows the HTTPS rule (Render Half)
  it('Property 10 (Render): Verification link renders iff getVerificationHref is non-null', () => {
    fc.assert(
      fc.property(arbCertification, arbBuildDate, (cert, bDate) => {
        cleanup();
        render(<CertificationCard certification={cert} buildDate={bDate} priority={false} />);
        const validHref = getVerificationHref(cert);

        if (validHref) {
          const link = screen.getByRole('link', { name: `Verify ${cert.title} credential` });
          expect(link).toHaveAttribute('href', validHref);
          expect(link).toHaveAttribute('target', '_blank');
        } else {
          expect(screen.queryByRole('link')).toBeNull();
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
npx vitest run tests/certifications/certification-card.test.tsx
```
Expected output: Properties 9 and 10 pass with >= 100 runs.

**Satisfies Requirements:** Req 7.6, 7.7, 8.1, 8.2, 8.5, 14.4, 15.2

---

### M7.G6.T8: Property 11 and Property 13 (Render Half) Tests

**Objective:** Append Property 11 (Badge image render half) and Property 13 (MarkdownDoc supporting content render half) tests to `tests/certifications/certification-card.test.tsx`.

**Acceptance Criteria:**
- ✓ Property 11 tagged: `Feature: m7-certifications-module, Property 11: Badge image follows the pair and source rule (Render Half)`.
- ✓ Property 11 verifies `<img>` is in DOM iff `getBadgeSource(cert) !== null`.
- ✓ Property 13 tagged: `Feature: m7-certifications-module, Property 13: Supporting content renders if and only if the body is non-empty (Render Half)`.
- ✓ Property 13 verifies `MarkdownDoc` container renders iff `contentHtml` is non-empty after trim.

**Prerequisites:**
- Tasks M7.G6.T1–M7.G6.T7 completed.

**Implementation Details:**
Append to `tests/certifications/certification-card.test.tsx`:

```typescript
import { getBadgeSource } from '@/lib/certifications/badge-source';

describe('CertificationCard - Properties 11 & 13', () => {
  // Feature: m7-certifications-module, Property 11: Badge image follows the pair and source rule (Render Half)
  it('Property 11 (Render): Badge image renders iff getBadgeSource is non-null', () => {
    fc.assert(
      fc.property(arbCertification, arbBuildDate, (cert, bDate) => {
        cleanup();
        const { container } = render(<CertificationCard certification={cert} buildDate={bDate} priority={false} />);
        const source = getBadgeSource(cert);

        if (source) {
          const img = container.querySelector('img');
          expect(img).not.toBeNull();
          expect(img).toHaveAttribute('src', source.src);
          expect(img).toHaveAttribute('alt', source.alt);
        } else {
          expect(container.querySelector('img')).toBeNull();
        }
      }),
      { numRuns: 100 },
    );
  });

  // Feature: m7-certifications-module, Property 13: Supporting content renders if and only if the body is non-empty (Render Half)
  it('Property 13 (Render): MarkdownDoc renders iff contentHtml is non-empty after trim', () => {
    fc.assert(
      fc.property(
        arbCertification,
        arbBuildDate,
        fc.oneof(fc.constant('<h4>Heading</h4><p>Text</p>'), fc.constant('   '), fc.constant(''), fc.constant(undefined)),
        (cert, bDate, html) => {
          cleanup();
          const { container } = render(<CertificationCard certification={cert} buildDate={bDate} contentHtml={html} priority={false} />);
          const hasContent = Boolean(html && html.trim().length > 0);

          if (hasContent) {
            expect(container.querySelector('.prose')).not.toBeNull();
          } else {
            expect(container.querySelector('.prose')).toBeNull();
          }
        },
      ),
      { numRuns: 100 },
    );
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-card.test.tsx
```
Expected output: Properties 11 and 13 pass with >= 100 runs.

**Satisfies Requirements:** Req 9.1–9.4, 10.1, 10.2, 15.2

---

### M7.G6.T9: Axe Accessibility Tests and Static Danger Scan for CertificationCard

**Objective:** Run `axe-core` on `CertificationCard` across populated, expired, and minimal fixtures, and verify zero occurrences of `dangerouslySetInnerHTML`.

**Acceptance Criteria:**
- ✓ Populated fixture card has zero axe violations.
- ✓ Expired fixture card has zero axe violations.
- ✓ Minimal fixture card has zero axe violations.
- ✓ Static check verifies `src/components/certifications/certification-card.tsx` has zero matches for `dangerouslySetInnerHTML`.

**Prerequisites:**
- `vitest-axe` available.
- `src/components/certifications/certification-card.tsx` implemented.

**Implementation Details:**
Create `tests/certifications/certification-card-a11y.test.tsx`:

```typescript
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';
import { CertificationCard } from '@/components/certifications/certification-card';
import {
  fixtureFullCertification,
  fixtureExpiredCertification,
  fixtureMinimalCertification,
} from '../fixtures/certifications-data';

describe('CertificationCard - Accessibility & Safety', () => {
  const buildDate = '2026-04-15';

  it('passes axe with zero violations for full populated card', async () => {
    const { container } = render(
      <CertificationCard
        certification={fixtureFullCertification}
        buildDate={buildDate}
        contentHtml="<h4>Competencies</h4><p>Details</p>"
        priority={true}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe with zero violations for expired card', async () => {
    const { container } = render(
      <CertificationCard
        certification={fixtureExpiredCertification}
        buildDate={buildDate}
        priority={false}
      />,
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes axe with zero violations for minimal card', async () => {
    const { container } = render(
      <CertificationCard
        certification={fixtureMinimalCertification}
        buildDate={buildDate}
        priority={false}
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
Select-String -Path src\components\certifications\certification-card.tsx -Pattern "dangerouslySetInnerHTML"
npx vitest run tests/certifications/certification-card-a11y.test.tsx
```
Expected output: Zero string matches found; all three axe tests pass.

**Satisfies Requirements:** Req 10.4, 14.1, 15.1

---

### M7.G6.T10: Goal 6 Checkpoint and Pipeline Verification

**Objective:** Run the full test suite and typechecker across Goal 6 artifacts to confirm complete green status and clean compliance.

**Acceptance Criteria:**
- ✓ `src/components/certifications/certification-card.tsx` compiles cleanly with zero TypeScript errors.
- ✓ `tests/certifications/certification-card.test.tsx` passes (unit tests + Properties 8, 9, 10, 11, 13).
- ✓ `tests/certifications/certification-card-a11y.test.tsx` passes axe checks.
- ✓ File length of `src/components/certifications/certification-card.tsx` is under 300 lines.

**Prerequisites:**
- Tasks M7.G6.T1 through M7.G6.T9 completed.

**Implementation Details:**
Execute test suite and line count checks in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
(Get-Content src\components\certifications\certification-card.tsx).Length
npx vitest run tests/certifications/certification-card.test.tsx tests/certifications/certification-card-a11y.test.tsx
npx tsc --noEmit
```
Expected output:
- Line count is well under 300 lines.
- All test files pass.
- TypeScript compiler exits with code 0.

**Satisfies Requirements:** Req 6.1–6.9, 14.1, 15.3, 15.5, 15.6, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 6 are complete:
```powershell
npx vitest run tests/certifications/certification-card.test.tsx tests/certifications/certification-card-a11y.test.tsx
npx tsc --noEmit
```
Expected output: All unit, property, and accessibility tests for CertificationCard pass; zero TypeScript errors.