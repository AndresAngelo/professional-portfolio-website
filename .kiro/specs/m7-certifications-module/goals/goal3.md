# M7.G3: Status, Verification Href, and Badge Source Helpers

> **Milestone:** M7 — Certifications Module  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks (M7.G3.T1 – M7.G3.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 7.1–7.4, 8.1, 8.5–8.6, 9.1–9.3, 9.6, 15.2), `design.md` (Properties 6, 10 helper half, 11 helper half), `tasks.md` (M7.G3)

---

## Goal Objective

Implement three pure domain helper modules in `src/lib/certifications/`:
1. `certification-status.ts`: pure expiry classification comparing `expiresAt` against a provided `buildDate` parameter via lexical string slicing, without constructing system clock `Date` instances.
2. `verification-href.ts`: defense-in-depth URL validator accepting only absolute `https://` URLs that parse cleanly, rejecting `http:`, `javascript:`, whitespace-padded, or empty values.
3. `badge-source.ts`: pair and origin validator ensuring badge image URLs and alts are mutually non-empty and point to `/images/certifications/` or `https://`.

Verify all three helpers with concrete unit tests and fast-check property tests (Property 6, and the helper halves of Properties 10 and 11).

---

## Goal Success Criteria

- ✓ `src/lib/certifications/certification-status.ts` exports `CertificationStatus` and `getCertificationStatus(cert, buildDate)`.
- ✓ `getCertificationStatus` returns `'active'` when `expiresAt` is `null` or equal to `buildDate`, and `'expired'` when `expiresAt.slice(0, 10) < buildDate`. Zero `new Date()` calls.
- ✓ `src/lib/certifications/verification-href.ts` exports `getVerificationHref(cert)`. Returns the exact stored string without trimming if valid HTTPS; returns `null` otherwise.
- ✓ `src/lib/certifications/badge-source.ts` exports `BadgeSource` interface and `getBadgeSource(cert)`. Returns `{ src, alt }` if both are non-empty after trimming and `src` begins with `/images/certifications/` or `https://`; returns `null` otherwise.
- ✓ Zero client directives, DOM dependencies, React/Next.js imports, or clock reads in any helper.
- ✓ Vitest unit tests pass for all edge cases across all three modules.
- ✓ Fast-check property tests pass (>= 100 runs each):
  - Property 6: Expiry classification matches date order.
  - Property 10 (helper half): Verification href follows strict HTTPS URL rules.
  - Property 11 (helper half): Badge source follows pair and origin prefix rules.

---

## Prerequisites

- Goal 1 completed: `src/types/content.ts` available, test fixtures and arbitraries available in `tests/fixtures/`.
- No new packages or dependencies added to `package.json`.

---

## Tasks

### M7.G3.T1: Implement Pure Expiry Helper (certification-status.ts)

**Objective:** Create `src/lib/certifications/certification-status.ts` providing pure, clock-free status classification.

**Acceptance Criteria:**
- ✓ Exports `type CertificationStatus = 'active' | 'expired'`.
- ✓ Exports `getCertificationStatus(certification: Pick<Certification, 'expiresAt'>, buildDate: IsoDateString): CertificationStatus`.
- ✓ Returns `'active'` if `expiresAt === null`.
- ✓ Performs lexical comparison using `expiresAt.slice(0, 10)` and `buildDate.slice(0, 10)`.
- ✓ Returns `'expired'` if `expiresAt.slice(0, 10) < buildDate.slice(0, 10)`.
- ✓ Returns `'active'` if `expiresAt.slice(0, 10) >= buildDate.slice(0, 10)`.
- ✓ Does not invoke `new Date()`, `Date.now()`, or any clock API.

**Prerequisites:**
- `@/types/content` exports `Certification` and `IsoDateString`.

**Implementation Details:**
Create `src/lib/certifications/certification-status.ts`:

```typescript
import type { Certification, IsoDateString } from '@/types/content';

export type CertificationStatus = 'active' | 'expired';

export function getCertificationStatus(
  certification: Pick<Certification, 'expiresAt'>,
  buildDate: IsoDateString,
): CertificationStatus {
  if (certification.expiresAt === null) {
    return 'active';
  }

  const expiryDay = certification.expiresAt.slice(0, 10);
  const targetDay = buildDate.slice(0, 10);

  if (expiryDay < targetDay) {
    return 'expired';
  }

  return 'active';
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero TypeScript errors.

**Satisfies Requirements:** Req 7.1, 7.2, 7.3, 7.4

---

### M7.G3.T2: Implement Verification Href Validator (verification-href.ts)

**Objective:** Create `src/lib/certifications/verification-href.ts` validating external verification URLs.

**Acceptance Criteria:**
- ✓ Exports `getVerificationHref(certification: Pick<Certification, 'verificationUrl'>): string | null`.
- ✓ Returns `null` if `verificationUrl` is `null`, empty, or whitespace-only.
- ✓ Rejects URLs that do not strictly start with `'https://'`.
- ✓ Rejects padded URLs (e.g., `' https://...'`) without trimming (stored string must be returned unchanged).
- ✓ Validates URL via `new URL(raw)` to ensure parsing validity.
- ✓ Returns the stored URL string unchanged when valid.

**Prerequisites:**
- `@/types/content` exports `Certification`.

**Implementation Details:**
Create `src/lib/certifications/verification-href.ts`:

```typescript
import type { Certification } from '@/types/content';

export function getVerificationHref(
  certification: Pick<Certification, 'verificationUrl'>,
): string | null {
  const url = certification.verificationUrl;
  if (!url || typeof url !== 'string') {
    return null;
  }

  // Reject unpadded or non-https prefixes
  if (!url.startsWith('https://')) {
    return null;
  }

  try {
    const parsed = new URL(url);
    if (parsed.protocol !== 'https:') {
      return null;
    }
    return url;
  } catch {
    return null;
  }
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero TypeScript errors.

**Satisfies Requirements:** Req 8.1, 8.5, 8.6

---

### M7.G3.T3: Implement Badge Source Validator (badge-source.ts)

**Objective:** Create `src/lib/certifications/badge-source.ts` ensuring badge URL and alt pairs conform to security and path standards.

**Acceptance Criteria:**
- ✓ Exports interface `BadgeSource` with `readonly src: string` and `readonly alt: string`.
- ✓ Exports `getBadgeSource(certification: Pick<Certification, 'badgeImageUrl' | 'badgeImageAlt'>): BadgeSource | null`.
- ✓ Returns `null` if either `badgeImageUrl` or `badgeImageAlt` is `null`, empty, or whitespace-only after trimming.
- ✓ Ensures the trimmed URL starts with `/images/certifications/` or `https://`.
- ✓ Returns `{ src: trimmedSrc, alt: trimmedAlt }` when valid.
- ✓ Returns `null` for arbitrary external paths, `http://`, or root files like `/badge.png`.

**Prerequisites:**
- `@/types/content` exports `Certification`.

**Implementation Details:**
Create `src/lib/certifications/badge-source.ts`:

```typescript
import type { Certification } from '@/types/content';

export interface BadgeSource {
  readonly src: string;
  readonly alt: string;
}

const ALLOWED_INTERNAL_PREFIX = '/images/certifications/';
const ALLOWED_HTTPS_PREFIX = 'https://';

export function getBadgeSource(
  certification: Pick<Certification, 'badgeImageUrl' | 'badgeImageAlt'>,
): BadgeSource | null {
  const rawUrl = certification.badgeImageUrl;
  const rawAlt = certification.badgeImageAlt;

  if (!rawUrl || !rawAlt) {
    return null;
  }

  const src = rawUrl.trim();
  const alt = rawAlt.trim();

  if (src.length === 0 || alt.length === 0) {
    return null;
  }

  const isInternal = src.startsWith(ALLOWED_INTERNAL_PREFIX);
  const isHttps = src.startsWith(ALLOWED_HTTPS_PREFIX);

  if (!isInternal && !isHttps) {
    return null;
  }

  return { src, alt };
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: Zero TypeScript errors.

**Satisfies Requirements:** Req 9.1, 9.2, 9.3, 9.6

---

### M7.G3.T4: Static Purity and Dependency Inspection of M7.G3 Helpers

**Objective:** Verify that `certification-status.ts`, `verification-href.ts`, and `badge-source.ts` contain no React, Next.js, DOM, or clock calls.

**Acceptance Criteria:**
- ✓ No `'use client'` or `'use server'` directives.
- ✓ No imports of `react`, `next`, or node filesystem APIs.
- ✓ No references to `Date`, `new Date()`, `Date.now()`, `window`, or `document`.
- ✓ Confirmed via automated string inspection in Windows PowerShell.

**Prerequisites:**
- Tasks M7.G3.T1, M7.G3.T2, M7.G3.T3 completed.

**Implementation Details:**
Scan files for forbidden tokens.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\lib\certifications\certification-status.ts, src\lib\certifications\verification-href.ts, src\lib\certifications\badge-source.ts -Pattern "use client|use server|new Date|Date\.now|window|document|react|next"
```
Expected output: No matches found.

**Satisfies Requirements:** Req 1.2, 7.4, 13.2, 13.3

---

### M7.G3.T5: Unit Tests for certification-status.ts

**Objective:** Create `tests/certifications/certification-status.test.ts` with unit test cases for past, equal, future, null, and datetime-formatted `expiresAt` strings.

**Acceptance Criteria:**
- ✓ Returns `'active'` when `expiresAt` is `null`.
- ✓ Returns `'expired'` when `expiresAt` is one day before `buildDate`.
- ✓ Returns `'active'` when `expiresAt` is equal to `buildDate`.
- ✓ Returns `'active'` when `expiresAt` is one day after `buildDate`.
- ✓ Handles ISO strings containing time elements (e.g. `'2026-03-01T12:00:00Z'`) by slicing to date portion.

**Prerequisites:**
- `src/lib/certifications/certification-status.ts` implemented.

**Implementation Details:**
Create `tests/certifications/certification-status.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { getCertificationStatus } from '@/lib/certifications/certification-status';

describe('certification-status - Unit Tests', () => {
  const buildDate = '2026-04-15';

  it('returns active when expiresAt is null', () => {
    expect(getCertificationStatus({ expiresAt: null }, buildDate)).toBe('active');
  });

  it('returns expired when expiresAt is earlier than buildDate', () => {
    expect(getCertificationStatus({ expiresAt: '2026-04-14' }, buildDate)).toBe('expired');
    expect(getCertificationStatus({ expiresAt: '2025-12-31' }, buildDate)).toBe('expired');
  });

  it('returns active when expiresAt equals buildDate', () => {
    expect(getCertificationStatus({ expiresAt: '2026-04-15' }, buildDate)).toBe('active');
  });

  it('returns active when expiresAt is later than buildDate', () => {
    expect(getCertificationStatus({ expiresAt: '2026-04-16' }, buildDate)).toBe('active');
    expect(getCertificationStatus({ expiresAt: '2027-01-01' }, buildDate)).toBe('active');
  });

  it('correctly handles expiresAt strings that contain time components', () => {
    expect(getCertificationStatus({ expiresAt: '2026-04-14T23:59:59Z' }, buildDate)).toBe('expired');
    expect(getCertificationStatus({ expiresAt: '2026-04-15T00:00:00Z' }, buildDate)).toBe('active');
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-status.test.ts
```
Expected output: All 5 unit tests pass.

**Satisfies Requirements:** Req 7.1, 7.2, 7.3, 7.4

---

### M7.G3.T6: Property 6 Test — Expiry Classification Invariants

**Objective:** Add Property 6 to `tests/certifications/certification-status.test.ts` verifying expiry classification behavior against arbitrary generated dates.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 6: Expiry classification matches date order`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Verifies that `getCertificationStatus` returns `'expired'` iff `expiresAt !== null` and `expiresAt.slice(0, 10) < buildDate.slice(0, 10)`.
- ✓ Verifies that for any date where `expiresAt >= buildDate` or `expiresAt === null`, the result is `'active'`.

**Prerequisites:**
- `arbBuildDate` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/certification-status.test.ts`:

```typescript
import fc from 'fast-check';
import { arbBuildDate } from '../fixtures/certifications-arbitraries';

describe('certification-status - Property Tests', () => {
  // Feature: m7-certifications-module, Property 6: Expiry classification matches date order
  it('Property 6: Returns expired iff expiresAt is non-null and earlier than buildDate', () => {
    fc.assert(
      fc.property(
        fc.option(arbBuildDate, { nil: null }),
        arbBuildDate,
        (expiresAt, buildDate) => {
          const status = getCertificationStatus({ expiresAt }, buildDate);
          if (expiresAt === null) {
            expect(status).toBe('active');
          } else if (expiresAt.slice(0, 10) < buildDate.slice(0, 10)) {
            expect(status).toBe('expired');
          } else {
            expect(status).toBe('active');
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
npx vitest run tests/certifications/certification-status.test.ts
```
Expected output: Unit tests and Property 6 pass with >= 100 runs.

**Satisfies Requirements:** Req 7.1, 7.2, 7.3, 7.4, 15.2

---

### M7.G3.T7: Unit Tests and Property 10 (Helper Half) for verification-href.ts

**Objective:** Create `tests/certifications/verification-href.test.ts` testing `getVerificationHref` with unit cases and Property 10 (helper half).

**Acceptance Criteria:**
- ✓ Unit test verifies valid HTTPS URLs return identical stored string.
- ✓ Unit test verifies `http://`, `javascript:`, whitespace-padded, empty, and `null` URLs return `null`.
- ✓ Property test (helper half of Property 10) verifies with at least 100 runs that `getVerificationHref` returns non-null iff the string begins with `https://` and parses as a valid URL without modification.
- ✓ Tagged: `Feature: m7-certifications-module, Property 10: Verification link follows the HTTPS rule (Helper Half)`.

**Prerequisites:**
- `src/lib/certifications/verification-href.ts` implemented.
- `arbUrl` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Create `tests/certifications/verification-href.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { getVerificationHref } from '@/lib/certifications/verification-href';
import { arbUrl } from '../fixtures/certifications-arbitraries';

describe('verification-href - Unit Tests', () => {
  it('returns valid https URL unchanged', () => {
    const valid = 'https://aws.amazon.com/verify/12345';
    expect(getVerificationHref({ verificationUrl: valid })).toBe(valid);
  });

  it('rejects http URLs', () => {
    expect(getVerificationHref({ verificationUrl: 'http://aws.amazon.com/verify/12345' })).toBeNull();
  });

  it('rejects javascript: schemes', () => {
    expect(getVerificationHref({ verificationUrl: 'javascript:alert(1)' })).toBeNull();
  });

  it('rejects padded https URLs without trimming', () => {
    expect(getVerificationHref({ verificationUrl: '  https://aws.amazon.com/verify/12345  ' })).toBeNull();
  });

  it('returns null for null, empty, or whitespace-only inputs', () => {
    expect(getVerificationHref({ verificationUrl: null })).toBeNull();
    expect(getVerificationHref({ verificationUrl: '' })).toBeNull();
    expect(getVerificationHref({ verificationUrl: '   ' })).toBeNull();
  });
});

describe('verification-href - Property Tests', () => {
  // Feature: m7-certifications-module, Property 10: Verification link follows the HTTPS rule (Helper Half)
  it('Property 10 (Helper): returns non-null iff url starts strictly with https:// and parses cleanly', () => {
    fc.assert(
      fc.property(arbUrl, (url) => {
        const result = getVerificationHref({ verificationUrl: url });
        if (result !== null) {
          expect(result).toBe(url);
          expect(result.startsWith('https://')).toBe(true);
          expect(() => new URL(result)).not.toThrow();
        } else {
          const isValidHttps =
            typeof url === 'string' &&
            url.startsWith('https://') &&
            (() => {
              try {
                return new URL(url).protocol === 'https:';
              } catch {
                return false;
              }
            })();
          expect(isValidHttps).toBe(false);
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
npx vitest run tests/certifications/verification-href.test.ts
```
Expected output: Unit tests and Property 10 helper half pass.

**Satisfies Requirements:** Req 8.1, 8.5, 8.6, 15.2

---

### M7.G3.T8: Unit Tests for badge-source.ts

**Objective:** Create `tests/certifications/badge-source.test.ts` testing `getBadgeSource` against edge cases and paired presence constraints.

**Acceptance Criteria:**
- ✓ Unit test verifies valid `/images/certifications/badge.png` and `alt` returns `{ src, alt }`.
- ✓ Unit test verifies valid `https://badges.org/badge.png` and `alt` returns `{ src, alt }`.
- ✓ Unit test verifies missing alt with present URL returns `null`.
- ✓ Unit test verifies missing URL with present alt returns `null`.
- ✓ Unit test verifies whitespace-only URL or alt returns `null`.
- ✓ Unit test verifies disallowed relative paths (e.g. `../images/badge.png` or `/badge.png`) return `null`.

**Prerequisites:**
- `src/lib/certifications/badge-source.ts` implemented.

**Implementation Details:**
Create `tests/certifications/badge-source.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { getBadgeSource } from '@/lib/certifications/badge-source';

describe('badge-source - Unit Tests', () => {
  it('returns source when internal path and alt are valid', () => {
    const input = {
      badgeImageUrl: '/images/certifications/aws.png',
      badgeImageAlt: 'AWS Badge',
    };
    expect(getBadgeSource(input)).toEqual({
      src: '/images/certifications/aws.png',
      alt: 'AWS Badge',
    });
  });

  it('returns source when https URL and alt are valid', () => {
    const input = {
      badgeImageUrl: 'https://badges.org/badge.png',
      badgeImageAlt: 'Remote Badge',
    };
    expect(getBadgeSource(input)).toEqual({
      src: 'https://badges.org/badge.png',
      alt: 'Remote Badge',
    });
  });

  it('trims whitespace around src and alt', () => {
    const input = {
      badgeImageUrl: '  /images/certifications/aws.png  ',
      badgeImageAlt: '  AWS Badge  ',
    };
    expect(getBadgeSource(input)).toEqual({
      src: '/images/certifications/aws.png',
      alt: 'AWS Badge',
    });
  });

  it('returns null when alt is missing or empty', () => {
    expect(getBadgeSource({ badgeImageUrl: '/images/certifications/aws.png', badgeImageAlt: null })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: '/images/certifications/aws.png', badgeImageAlt: '' })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: '/images/certifications/aws.png', badgeImageAlt: '   ' })).toBeNull();
  });

  it('returns null when url is missing or empty', () => {
    expect(getBadgeSource({ badgeImageUrl: null, badgeImageAlt: 'AWS Badge' })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: '', badgeImageAlt: 'AWS Badge' })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: '   ', badgeImageAlt: 'AWS Badge' })).toBeNull();
  });

  it('rejects disallowed path prefixes', () => {
    expect(getBadgeSource({ badgeImageUrl: '/images/badge.png', badgeImageAlt: 'Badge' })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: '/badge.png', badgeImageAlt: 'Badge' })).toBeNull();
    expect(getBadgeSource({ badgeImageUrl: 'http://badges.org/badge.png', badgeImageAlt: 'Badge' })).toBeNull();
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/badge-source.test.ts
```
Expected output: All 6 unit tests pass.

**Satisfies Requirements:** Req 9.1, 9.2, 9.3, 9.6

---

### M7.G3.T9: Property 11 Test (Helper Half) for badge-source.ts

**Objective:** Append Property 11 (helper half) to `tests/certifications/badge-source.test.ts` verifying badge extraction invariants over arbitrary inputs.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 11: Badge image follows the pair and source rule (Helper Half)`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Generates optional badge URLs and alts across allowed prefixes, invalid prefixes, and empty strings.
- ✓ Verifies that a non-null result is returned iff both fields are non-empty after trim and URL begins with `/images/certifications/` or `https://`.

**Prerequisites:**
- `tests/certifications/badge-source.test.ts` implemented.

**Implementation Details:**
Append to `tests/certifications/badge-source.test.ts`:

```typescript
import fc from 'fast-check';

describe('badge-source - Property Tests', () => {
  const arbBadgeUrl = fc.oneof(
    fc.constant('/images/certifications/valid.png'),
    fc.constant('https://badges.org/cert.png'),
    fc.constant('/other-path/cert.png'),
    fc.constant('http://insecure.org/cert.png'),
    fc.constant('   '),
    fc.constant(''),
    fc.constant(null),
  );

  const arbBadgeAlt = fc.oneof(
    fc.string({ min: 1, max: 40 }),
    fc.constant('   '),
    fc.constant(''),
    fc.constant(null),
  );

  // Feature: m7-certifications-module, Property 11: Badge image follows the pair and source rule (Helper Half)
  it('Property 11 (Helper): Returns source iff both fields non-empty after trim and prefix is valid', () => {
    fc.assert(
      fc.property(arbBadgeUrl, arbBadgeAlt, (rawUrl, rawAlt) => {
        const result = getBadgeSource({ badgeImageUrl: rawUrl, badgeImageAlt: rawAlt });

        const trimmedUrl = rawUrl?.trim() ?? '';
        const trimmedAlt = rawAlt?.trim() ?? '';

        const hasValidUrl =
          trimmedUrl.startsWith('/images/certifications/') || trimmedUrl.startsWith('https://');
        const hasValidAlt = trimmedAlt.length > 0;

        if (hasValidUrl && hasValidAlt) {
          expect(result).not.toBeNull();
          expect(result?.src).toBe(trimmedUrl);
          expect(result?.alt).toBe(trimmedAlt);
        } else {
          expect(result).toBeNull();
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
npx vitest run tests/certifications/badge-source.test.ts
```
Expected output: Unit and Property 11 tests pass.

**Satisfies Requirements:** Req 9.1, 9.2, 9.3, 9.6, 15.2

---

### M7.G3.T10: Goal 3 Checkpoint and Typecheck Inspection

**Objective:** Run the full test suite for Goal 3 helpers, verify zero regressions or clock reads, and confirm typecheck passes.

**Acceptance Criteria:**
- ✓ `src/lib/certifications/certification-status.ts` compiles and passes unit + property tests.
- ✓ `src/lib/certifications/verification-href.ts` compiles and passes unit + property tests.
- ✓ `src/lib/certifications/badge-source.ts` compiles and passes unit + property tests.
- ✓ Zero `new Date` or clock calls found across all three helper modules.
- ✓ `npx tsc --noEmit` exits with 0.

**Prerequisites:**
- Tasks M7.G3.T1 through M7.G3.T9 completed.

**Implementation Details:**
Execute test suite and typechecking commands in Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/certification-status.test.ts tests/certifications/verification-href.test.ts tests/certifications/badge-source.test.ts
npx tsc --noEmit
```
Expected output: All unit and property tests across the three files pass with exit code 0. Zero TypeScript errors.

**Satisfies Requirements:** Req 7.1–7.4, 8.1, 8.5–8.6, 9.1–9.3, 9.6, 15.2, 15.5, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 3 are complete:
```powershell
npx vitest run tests/certifications/certification-status.test.ts tests/certifications/verification-href.test.ts tests/certifications/badge-source.test.ts
npx tsc --noEmit
```
Expected output: All 3 helper test files pass completely; TypeScript compiles with zero errors.