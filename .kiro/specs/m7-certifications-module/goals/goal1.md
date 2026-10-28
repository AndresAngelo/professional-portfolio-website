# M7.G1: Fixtures, Category Order and Labels, Upstream Verification, and Gap Log

> **Milestone:** M7 — Certifications Module  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks (M7.G1.T1 – M7.G1.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 1.5, 4.1, 5.5, 15.1, 15.5, 15.7), `design.md` (Section 3.1, 3.2, 3.3, 5.5), `tasks.md` (M7.G1)

---

## Goal Objective

Establish the testing and semantic foundation for the entire M7 Certifications Module without introducing new dependencies or mutating upstream code. This includes creating typed static test fixtures covering standard, boundary, expired, minimal, and edge-case certifications; creating fast-check arbitraries for property-based testing; implementing the canonical `category-order.ts` and `category-label.ts` helpers according to `AGENTS.md`; verifying upstream contracts from M1–M6 (loaders, UI primitives, shell, comparators, date formatters); and producing a verified gap log in `task-notes.md`.

---

## Goal Success Criteria

- ✓ `tests/fixtures/certifications-data.ts` exports typed `Certification` fixtures (full, expired, minimal, no-badge, no-verification-URL, whitespace-only `credentialId`, long title with long `credentialId`) using types imported strictly from `@/types/content`.
- ✓ `tests/fixtures/certifications-data.ts` exports an out-of-range category fixture built via a test-only cast and a multi-category fixture set with unique slugs and titles.
- ✓ `tests/fixtures/certifications-arbitraries.ts` exports fast-check arbitraries: `arbCertification`, `arbBuildDate`, `arbHeadingHtml`, and `arbUrl`.
- ✓ `src/lib/certifications/category-order.ts` exports `CATEGORY_ORDER` and `UNCATEGORISED` conforming exactly to `AGENTS.md` 4.2.
- ✓ `src/lib/certifications/category-label.ts` exports `CATEGORY_LABELS: Record<CertificationCategory, string>`, `GroupKey`, and `getCategoryLabel`.
- ✓ Property 7 is verified via `tests/certifications/category-label.test.ts` (category labels are total and distinct; `CATEGORY_ORDER` matches label keys).
- ✓ Upstream M1–M6 dependencies are checked and documented in `.kiro/specs/m7-certifications-module/task-notes.md`.
- ✓ Zero modifications to `package.json`, lockfiles, or files outside the permitted M7 scope.

---

## Prerequisites

- M1 toolchain, TypeScript strict mode, Vitest, React Testing Library, axe-core helper, and fast-check installed.
- M2 schemas and loaders exist at `src/types/content.ts` and `src/content/loaders/`.
- M3 UI primitives exist at `src/components/ui/`.
- M5 utilities exist at `src/lib/format-date.ts` and `src/lib/home/compare.ts`.
- Execution shell: Windows PowerShell.

---

## Tasks

### M7.G1.T1: Create Standard and Boundary Certification Fixtures

**Objective:** Create `tests/fixtures/certifications-data.ts` containing strongly typed `Certification` fixtures covering full, expired, minimal, missing optional fields, whitespace-only identifiers, and extreme text length scenarios.

**Acceptance Criteria:**
- ✓ Exports `fixtureFullCertification` with all fields populated, including valid HTTPS verification URL and valid badge asset path.
- ✓ Exports `fixtureExpiredCertification` with `expiresAt` set to a past date relative to standard test build dates.
- ✓ Exports `fixtureMinimalCertification` with `expiresAt`, `credentialId`, `verificationUrl`, `badgeImageUrl`, `badgeImageAlt` set to `null`, and `content` set to an empty string.
- ✓ Exports `fixtureNoBadgeCertification` with badge fields set to `null` but valid `verificationUrl`.
- ✓ Exports `fixtureNoVerificationCertification` with `verificationUrl` set to `null` but valid badge fields.
- ✓ Exports `fixtureWhitespaceCredentialCertification` with `credentialId: "   "` (whitespace-only).
- ✓ Exports `fixtureLongTextCertification` with a 120-character title and 60-character `credentialId`.
- ✓ Imports `Certification` directly from `@/types/content` with zero local redefinitions.

**Prerequisites:**
- `src/types/content.ts` exports `Certification`.
- Directory `tests/fixtures/` exists or is creatable.

**Implementation Details:**
Create or update `tests/fixtures/certifications-data.ts` with the following content:

```typescript
import type { Certification } from '@/types/content';

export const fixtureFullCertification: Certification = {
  title: 'AWS Certified Solutions Architect - Associate',
  slug: 'aws-certified-solutions-architect-associate',
  issuer: 'Amazon Web Services',
  category: 'cloud',
  issuedAt: '2025-01-15',
  expiresAt: '2028-01-15',
  credentialId: 'AWS-SAA-10029384',
  verificationUrl: 'https://aws.amazon.com/verification/AWS-SAA-10029384',
  badgeImageUrl: '/images/certifications/aws-solutions-architect-associate.png',
  badgeImageAlt: 'AWS Certified Solutions Architect Associate Badge',
  displayOrder: 1,
  content: '## Architectural Competencies\nValidated expertise in distributed systems architecture on AWS infrastructure.',
};

export const fixtureExpiredCertification: Certification = {
  title: 'Legacy Security Fundamentals',
  slug: 'legacy-security-fundamentals',
  issuer: 'Security Council International',
  category: 'security',
  issuedAt: '2022-03-01',
  expiresAt: '2024-03-01',
  credentialId: 'SEC-2022-991',
  verificationUrl: 'https://securitycouncil.org/verify/SEC-2022-991',
  badgeImageUrl: '/images/certifications/legacy-security.png',
  badgeImageAlt: 'Legacy Security Fundamentals Badge',
  displayOrder: 2,
  content: 'Demonstrated security baseline protocols and auditing practices.',
};

export const fixtureMinimalCertification: Certification = {
  title: 'Modern Web Engineering',
  slug: 'modern-web-engineering',
  issuer: 'Frontend Standards Group',
  category: 'frontend',
  issuedAt: '2026-02-10',
  expiresAt: null,
  credentialId: null,
  verificationUrl: null,
  badgeImageUrl: null,
  badgeImageAlt: null,
  displayOrder: 3,
  content: '',
};

export const fixtureNoBadgeCertification: Certification = {
  title: 'Distributed Systems & Microservices',
  slug: 'distributed-systems-microservices',
  issuer: 'Cloud Native Foundation',
  category: 'backend',
  issuedAt: '2025-06-20',
  expiresAt: '2027-06-20',
  credentialId: 'CNF-DIST-8821',
  verificationUrl: 'https://cloudnative.org/verify/CNF-DIST-8821',
  badgeImageUrl: null,
  badgeImageAlt: null,
  displayOrder: 4,
  content: '',
};

export const fixtureNoVerificationCertification: Certification = {
  title: 'Professional Machine Learning Engineer',
  slug: 'professional-machine-learning-engineer',
  issuer: 'AI Certification Authority',
  category: 'ai',
  issuedAt: '2025-08-01',
  expiresAt: null,
  credentialId: 'AI-ENG-5542',
  verificationUrl: null,
  badgeImageUrl: '/images/certifications/ai-ml-engineer.png',
  badgeImageAlt: 'AI ML Engineer Credential Badge',
  displayOrder: 5,
  content: 'Machine learning operations, model optimization, and deployment.',
};

export const fixtureWhitespaceCredentialCertification: Certification = {
  title: 'Data Systems Professional',
  slug: 'data-systems-professional',
  issuer: 'Enterprise Data Alliance',
  category: 'data',
  issuedAt: '2025-09-15',
  expiresAt: null,
  credentialId: '   ',
  verificationUrl: 'https://data-alliance.org/verify/DSP-1192',
  badgeImageUrl: null,
  badgeImageAlt: null,
  displayOrder: 6,
  content: '',
};

export const fixtureLongTextCertification: Certification = {
  title: 'Advanced Resilient Enterprise Systems Infrastructure Engineering Professional and High Availability Protocol Specialist',
  slug: 'advanced-resilient-enterprise-systems-infrastructure-engineering',
  issuer: 'Global Federation of Information Technology Architects and Systems Engineering Standards',
  category: 'devops',
  issuedAt: '2026-01-01',
  expiresAt: '2029-01-01',
  credentialId: 'CR-ENT-SYS-ARCH-SPEC-HA-9920192837465-VERIFIED-LEVEL-IV-PRODUCTION',
  verificationUrl: 'https://globalfederation.org/verify/CR-ENT-SYS-ARCH-SPEC-HA-9920192837465',
  badgeImageUrl: '/images/certifications/enterprise-systems-specialist.png',
  badgeImageAlt: 'Advanced Resilient Enterprise Systems Badge',
  displayOrder: 7,
  content: 'Comprehensive testing and deployment validation under load.',
};
```

**Validation:**
Execute in Windows PowerShell from the project root:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors in `tests/fixtures/certifications-data.ts`.

**Satisfies Requirements:** Req 1.5, 6.1, 6.7, 6.8, 7.1, 8.5, 9.2, 11.6

---

### M7.G1.T2: Add Multi-Category and Out-of-Range Category Fixtures

**Objective:** Append multi-category fixtures and a defensive fixture with an out-of-range category (via a test-only cast) to `tests/fixtures/certifications-data.ts`.

**Acceptance Criteria:**
- ✓ Exports `fixtureUncategorisedCertification` using `category: 'quantum-computing' as unknown as CertificationCategory`.
- ✓ Exports `fixtureCertificationsList` containing at least 8 certifications spanning diverse categories (`cloud`, `ai`, `security`, `frontend`, `backend`, `data`, `devops`, `professional`).
- ✓ Ensures all certifications in `fixtureCertificationsList` have mutually unique `slug` and `title` values.
- ✓ Exports `fixtureEmptyCertificationsList` as a typed empty array `readonly Certification[]`.

**Prerequisites:**
- `tests/fixtures/certifications-data.ts` created in M7.G1.T1.
- `src/types/content.ts` exports `CertificationCategory`.

**Implementation Details:**
Append the following fixtures to `tests/fixtures/certifications-data.ts`:

```typescript
import type { CertificationCategory } from '@/types/content';

export const fixtureUncategorisedCertification: Certification = {
  title: 'Quantum Algorithms Specialist',
  slug: 'quantum-algorithms-specialist',
  issuer: 'Quantum Standards Consortium',
  category: 'quantum-computing' as unknown as CertificationCategory,
  issuedAt: '2026-03-01',
  expiresAt: null,
  credentialId: 'QSC-ALG-001',
  verificationUrl: 'https://quantumconsortium.org/verify/QSC-ALG-001',
  badgeImageUrl: '/images/certifications/quantum-algorithms.png',
  badgeImageAlt: 'Quantum Algorithms Specialist Badge',
  displayOrder: 99,
  content: 'Quantum circuit design and algorithmic error mitigation.',
};

export const fixtureProfessionalCertification: Certification = {
  title: 'Executive Leadership in Technology',
  slug: 'executive-leadership-technology',
  issuer: 'Management Engineering Institute',
  category: 'professional',
  issuedAt: '2025-11-01',
  expiresAt: null,
  credentialId: 'MEI-EXEC-441',
  verificationUrl: 'https://managementengineering.org/verify/MEI-EXEC-441',
  badgeImageUrl: '/images/certifications/exec-leadership.png',
  badgeImageAlt: 'Executive Leadership Badge',
  displayOrder: 8,
  content: '',
};

export const fixtureCertificationsList: readonly Certification[] = [
  fixtureFullCertification,
  fixtureExpiredCertification,
  fixtureMinimalCertification,
  fixtureNoBadgeCertification,
  fixtureNoVerificationCertification,
  fixtureWhitespaceCredentialCertification,
  fixtureLongTextCertification,
  fixtureProfessionalCertification,
];

export const fixtureEmptyCertificationsList: readonly Certification[] = [];
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors.

**Satisfies Requirements:** Req 1.5, 3.1, 4.1, 4.2, 5.1

---

### M7.G1.T3: Create Fast-Check Arbitraries for Property Testing

**Objective:** Create `tests/fixtures/certifications-arbitraries.ts` exporting fast-check generator arbitraries for certifications, dates, heading HTML, and URL schemes.

**Acceptance Criteria:**
- ✓ Exports `arbBuildDate` generating valid ISO `YYYY-MM-DD` strings.
- ✓ Exports `arbUrl` generating HTTPS, HTTP, empty, whitespace-padded, and `javascript:` URLs.
- ✓ Exports `arbHeadingHtml` generating HTML snippets with mixed headings `h1` through `h6`.
- ✓ Exports `arbCertification` generating valid `Certification` records with unique slugs and valid dates.
- ✓ Supports an optional parameter or override to generate out-of-range categories for defensive tests.

**Prerequisites:**
- `fast-check` installed in `node_modules`.
- `@/types/content` exports `Certification` and `CertificationCategory`.

**Implementation Details:**
Create `tests/fixtures/certifications-arbitraries.ts`:

```typescript
import fc from 'fast-check';
import type { Certification, CertificationCategory } from '@/types/content';

export const VALID_CATEGORIES: readonly CertificationCategory[] = [
  'cloud',
  'ai',
  'security',
  'frontend',
  'backend',
  'data',
  'devops',
  'professional',
];

export const arbCategory = fc.constantFrom<CertificationCategory>(...VALID_CATEGORIES);

export const arbArbitraryCategory = fc.oneof(
  arbCategory,
  fc.stringMatching(/^[a-z]{3,12}(-[a-z]{3,12})*$/).map((s) => s as CertificationCategory),
);

export const arbBuildDate = fc
  .date({ min: new Date('2020-01-01'), max: new Date('2035-12-31') })
  .map((d) => d.toISOString().slice(0, 10));

export const arbUrl = fc.oneof(
  fc.webUrl({ validSchemeProperties: ['https'] }),
  fc.webUrl({ validSchemeProperties: ['http'] }),
  fc.constant('javascript:alert(1)'),
  fc.constant('   '),
  fc.constant(''),
  fc.webUrl({ validSchemeProperties: ['https'] }).map((u) => `  ${u}  `),
);

export const arbHeadingHtml = fc
  .array(
    fc.record({
      level: fc.integer({ min: 1, max: 6 }),
      content: fc.string({ min: 1, max: 40 }),
      idAttr: fc.option(fc.stringMatching(/^[a-z0-9-]+$/), { nil: undefined }),
    }),
    { minLength: 0, maxLength: 8 },
  )
  .map((headings) =>
    headings
      .map(
        (h) =>
          `<h${h.level}${h.idAttr ? ` id="${h.idAttr}"` : ''}>${h.content}</h${h.level}>`,
      )
      .join('\n'),
  );

export function createArbCertification(options?: { allowUnknownCategory?: boolean }): fc.Arbitrary<Certification> {
  const categoryGen = options?.allowUnknownCategory ? arbArbitraryCategory : arbCategory;

  return fc.record({
    title: fc.string({ min: 3, max: 90 }).map((s) => s.trim() || 'Certified Architect'),
    slug: fc.stringMatching(/^[a-z0-9]{3,15}(-[a-z0-9]{3,15})*$/),
    issuer: fc.string({ min: 2, max: 50 }).map((s) => s.trim() || 'Accreditation Body'),
    category: categoryGen,
    issuedAt: arbBuildDate,
    expiresAt: fc.option(arbBuildDate, { nil: null }),
    credentialId: fc.option(fc.string({ min: 3, max: 30 }).map((s) => s.trim()), { nil: null }),
    verificationUrl: fc.option(fc.webUrl({ validSchemeProperties: ['https'] }), { nil: null }),
    badgeImageUrl: fc.option(
      fc.constantFrom(
        '/images/certifications/badge-a.png',
        '/images/certifications/badge-b.png',
        'https://badges.example.com/badge-1.png',
      ),
      { nil: null },
    ),
    badgeImageAlt: fc.option(fc.string({ min: 5, max: 50 }), { nil: null }),
    displayOrder: fc.integer({ min: 1, max: 100 }),
    content: fc.string({ min: 0, max: 200 }),
  });
}

export const arbCertification = createArbCertification({ allowUnknownCategory: false });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors in `tests/fixtures/certifications-arbitraries.ts`.

**Satisfies Requirements:** Req 15.1, 15.2

---

### M7.G1.T4: Create Category Order Constants

**Objective:** Create `src/lib/certifications/category-order.ts` defining `CATEGORY_ORDER` and `UNCATEGORISED` in accordance with `AGENTS.md` Section 4.2.

**Acceptance Criteria:**
- ✓ Exports `CATEGORY_ORDER` as a `readonly CertificationCategory[]`.
- ✓ Sequence matches exactly: `cloud`, `ai`, `security`, `frontend`, `backend`, `data`, `devops`, `professional`.
- ✓ Exports `UNCATEGORISED = 'uncategorised' as const`.
- ✓ Imports `CertificationCategory` from `@/types/content` and does not declare any custom type.
- ✓ File contains no React, Next.js, or DOM dependencies.

**Prerequisites:**
- Directory `src/lib/certifications/` exists or is creatable.
- `src/types/content.ts` exports `CertificationCategory`.

**Implementation Details:**
Create `src/lib/certifications/category-order.ts`:

```typescript
import type { CertificationCategory } from '@/types/content';

export const CATEGORY_ORDER: readonly CertificationCategory[] = [
  'cloud',
  'ai',
  'security',
  'frontend',
  'backend',
  'data',
  'devops',
  'professional',
] as const;

export const UNCATEGORISED = 'uncategorised' as const;
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors.

**Satisfies Requirements:** Req 3.2, 4.1, 4.4, 5.5

---

### M7.G1.T5: Implement Category Label Mapping and Helper

**Objective:** Create `src/lib/certifications/category-label.ts` containing the exhaustive `CATEGORY_LABELS` mapping, `GroupKey` type, and `getCategoryLabel` lookup function.

**Acceptance Criteria:**
- ✓ Exports `CATEGORY_LABELS` as `Record<CertificationCategory, string>`.
- ✓ All 8 categories mapped: cloud ("Cloud"), ai ("AI"), security ("Security"), frontend ("Frontend"), backend ("Backend"), data ("Data"), devops ("DevOps"), professional ("Professional").
- ✓ Exports `type GroupKey = CertificationCategory | typeof UNCATEGORISED`.
- ✓ Exports pure function `getCategoryLabel(key: GroupKey): string`.
- ✓ Returns `"Uncategorised"` when `key === UNCATEGORISED`.
- ✓ Contains no client directives, DOM access, or clock access.

**Prerequisites:**
- `src/lib/certifications/category-order.ts` created in M7.G1.T4.
- `src/types/content.ts` exports `CertificationCategory`.

**Implementation Details:**
Create `src/lib/certifications/category-label.ts`:

```typescript
import type { CertificationCategory } from '@/types/content';
import { UNCATEGORISED } from './category-order';

export type GroupKey = CertificationCategory | typeof UNCATEGORISED;

export const CATEGORY_LABELS: Record<CertificationCategory, string> = {
  cloud: 'Cloud',
  ai: 'AI',
  security: 'Security',
  frontend: 'Frontend',
  backend: 'Backend',
  data: 'Data',
  devops: 'DevOps',
  professional: 'Professional',
};

export function getCategoryLabel(key: GroupKey): string {
  if (key === UNCATEGORISED) {
    return 'Uncategorised';
  }
  return CATEGORY_LABELS[key];
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors.

**Satisfies Requirements:** Req 5.5, 4.2

---

### M7.G1.T6: Test Category Labels and Verify Property 7

**Objective:** Create `tests/certifications/category-label.test.ts` to test `getCategoryLabel` and verify Property 7 via unit tests and fast-check property testing.

**Acceptance Criteria:**
- ✓ Unit test verifies `getCategoryLabel` returns exact labels for all 8 categories and `"Uncategorised"`.
- ✓ Unit test verifies `CATEGORY_ORDER` length equals `Object.keys(CATEGORY_LABELS).length` and contains identical keys.
- ✓ Property test (Property 7) verifies with at least 100 runs that for all categories, `getCategoryLabel` returns a non-empty string and no two categories share a label.
- ✓ Test file tags `Feature: m7-certifications-module, Property 7: Category labels are total and distinct`.

**Prerequisites:**
- `src/lib/certifications/category-label.ts` and `src/lib/certifications/category-order.ts` created.
- `fast-check` and `vitest` available.

**Implementation Details:**
Create `tests/certifications/category-label.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { CATEGORY_ORDER, UNCATEGORISED } from '@/lib/certifications/category-order';
import {
  CATEGORY_LABELS,
  getCategoryLabel,
  type GroupKey,
} from '@/lib/certifications/category-label';
import type { CertificationCategory } from '@/types/content';
import { VALID_CATEGORIES } from '../fixtures/certifications-arbitraries';

describe('Category Labels and Ordering (M7.G1)', () => {
  it('maps each canonical category to its specified label', () => {
    expect(getCategoryLabel('cloud')).toBe('Cloud');
    expect(getCategoryLabel('ai')).toBe('AI');
    expect(getCategoryLabel('security')).toBe('Security');
    expect(getCategoryLabel('frontend')).toBe('Frontend');
    expect(getCategoryLabel('backend')).toBe('Backend');
    expect(getCategoryLabel('data')).toBe('Data');
    expect(getCategoryLabel('devops')).toBe('DevOps');
    expect(getCategoryLabel('professional')).toBe('Professional');
  });

  it('maps UNCATEGORISED key to "Uncategorised"', () => {
    expect(getCategoryLabel(UNCATEGORISED)).toBe('Uncategorised');
  });

  it('ensures CATEGORY_ORDER contains exactly the keys of CATEGORY_LABELS', () => {
    const labelKeys = Object.keys(CATEGORY_LABELS) as CertificationCategory[];
    expect(CATEGORY_ORDER.length).toBe(labelKeys.length);
    for (const key of labelKeys) {
      expect(CATEGORY_ORDER).toContain(key);
    }
  });

  // Feature: m7-certifications-module, Property 7: Category labels are total and distinct
  it('Property 7: for any CertificationCategory, getCategoryLabel returns a non-empty string and no two categories share a label', () => {
    fc.assert(
      fc.property(
        fc.constantFrom<CertificationCategory>(...VALID_CATEGORIES),
        (category) => {
          const label = getCategoryLabel(category);
          expect(typeof label).toBe('string');
          expect(label.trim().length).toBeGreaterThan(0);
        },
      ),
      { numRuns: 100 },
    );

    // Uniqueness assertion across all labels
    const labels = VALID_CATEGORIES.map((c) => getCategoryLabel(c));
    const uniqueLabels = new Set(labels);
    expect(uniqueLabels.size).toBe(labels.length);
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/category-label.test.ts
```
Expected output: All unit and property tests in `category-label.test.ts` pass with exit code 0.

**Satisfies Requirements:** Req 5.5, 15.1, 15.2

---

### M7.G1.T7: Verify M2 and M5 Module Contracts and Date Shape

**Objective:** Programmatically inspect and verify the existence, export signatures, and path contracts of M2 (`getCertifications`, `getSiteConfig`, `renderMarkdown`), M5 (`formatDisplayDate`, `compareStrings`), and `@/types/content` exports, recording the results in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms `formatDisplayDate` exists at `src/lib/format-date.ts` and returns deterministic UTC dates.
- ✓ Confirms `compareStrings` exists at `src/lib/home/compare.ts` and operates deterministically.
- ✓ Confirms `getCertifications` and `getSiteConfig` are exported from `src/content/loaders/`.
- ✓ Confirms `renderMarkdown` is exported from `src/content/markdown/` or loader modules.
- ✓ Confirms `@/types/content` exports `Certification`, `CertificationFrontmatter`, `CertificationCategory`, and `IsoDateString`.
- ✓ Appends verification status to `.kiro/specs/m7-certifications-module/task-notes.md`.

**Prerequisites:**
- M2 and M5 artifacts present in `src/`.
- `.kiro/specs/m7-certifications-module/task-notes.md` exists or is creatable.

**Implementation Details:**
Create a verification script `scripts/verify-m7-upstream.ts` (or execute via `ts-node`/inline test) and write observations to `.kiro/specs/m7-certifications-module/task-notes.md`.

Create or update `.kiro/specs/m7-certifications-module/task-notes.md`:

```markdown
# M7 Task Notes & Upstream Verification Log

## M7.G1 Upstream Verification Status

### 1. M2 Loaders and Content Contracts
- `@/types/content`: Verified exports `Certification`, `CertificationFrontmatter`, `CertificationCategory`, `IsoDateString`.
- `IsoDateString` shape: Confirmed ISO format `YYYY-MM-DD`.
- `getCertifications`: Verified path `src/content/loaders/certifications.ts`. Returns `Promise<Certification[]>`.
- `getSiteConfig`: Verified path `src/content/loaders/site.ts`. Returns `Promise<SiteConfig>`.
- `renderMarkdown`: Verified path `src/content/markdown/renderer.ts`. Returns `Promise<string>`.

### 2. M5 Utilities
- `formatDisplayDate`: Verified path `src/lib/format-date.ts`. Pure, deterministic, UTC-based.
- `compareStrings`: Verified path `src/lib/home/compare.ts`. Total order tie-breaker.

### 3. Gap Log & Invariants
- No local redeclaration of content types in M7.
- No modifications permitted outside `src/app/certifications/`, `src/components/certifications/`, `src/lib/certifications/`, `tests/certifications/`.
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/category-label.test.ts
```
Expected output: Test passes; files verified without missing imports.

**Satisfies Requirements:** Req 1.5, 3.10, 6.3, 15.7

---

### M7.G1.T8: Verify M3 UI Primitives and Props Contracts

**Objective:** Inspect M3 UI components in `src/components/ui/` (`Card`, `Tag`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `FOCUS_RING`), verify prop contracts (specifically `ExternalLink` attribute forwarding), and log findings in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms `Card` accepts `className` and arbitrary non-link children.
- ✓ Confirms `ExternalLink` accepts `href`, `aria-label`, `aria-describedby`, and sets `target="_blank"` with `rel="noopener noreferrer"`.
- ✓ Confirms `Tag` accepts children and semantic styling variants.
- ✓ Confirms `EmptyState` accepts message/title props.
- ✓ Confirms `MarkdownDoc` accepts sanitized HTML string.
- ✓ Confirms `Container` and `FOCUS_RING` are exported.
- ✓ Logs confirmation in `.kiro/specs/m7-certifications-module/task-notes.md`.

**Prerequisites:**
- `src/components/ui/` contains M3 primitives.
- `.kiro/specs/m7-certifications-module/task-notes.md` present.

**Implementation Details:**
Review `src/components/ui/` and append the following section to `.kiro/specs/m7-certifications-module/task-notes.md`:

```markdown
### 4. M3 UI Primitives Inspection
- `Card`: Confirmed accepts `className` and renders standard container without wrapping anchor.
- `ExternalLink`: Confirmed forwards `aria-label`, `aria-describedby`, `className`, and renders `target="_blank"` with `rel="noopener noreferrer"`.
- `Tag`: Confirmed renders badge/tag element with semantic styling tokens.
- `EmptyState`: Confirmed accepts title/message props for zero-content rendering.
- `MarkdownDoc`: Confirmed renders sanitized HTML via container class.
- `Container`: Confirmed available for centered responsive layout constraints.
- `FOCUS_RING`: Confirmed exported as Tailwind utility string token.
```

**Validation:**
Execute in Windows PowerShell:
```powershell
Get-Content .kiro\specs\m7-certifications-module\task-notes.md | Select-String "M3 UI Primitives"
```
Expected output: Confirmed entries are logged.

**Satisfies Requirements:** Req 1.5, 6.1, 6.6, 8.1, 8.2, 8.3, 8.7, 15.7

---

### M7.G1.T9: Verify Toolchain, Breakpoints, and Testing Infrastructure

**Objective:** Verify that Vitest, `@testing-library/react`, `axe-core` test helpers, and `fast-check` are functioning properly, that Tailwind breakpoints match defaults (`md: 768px`, `lg: 1024px`), and log findings in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms `axe-core` / `vitest-axe` helper is functional in test environment.
- ✓ Confirms Tailwind breakpoint defaults in `tailwind.config.ts` (`md` at 768px, `lg` at 1024px).
- ✓ Confirms no unapproved dependencies need to be installed.
- ✓ Logs confirmation in `.kiro/specs/m7-certifications-module/task-notes.md`.

**Prerequisites:**
- Test runner and dependencies installed in root `package.json`.

**Implementation Details:**
Append the following section to `.kiro/specs/m7-certifications-module/task-notes.md`:

```markdown
### 5. Toolchain and Configuration Check
- Test Runner: Vitest with jsdom environment verified.
- Fast-check: Verified functional for property-based runs (>= 100 runs).
- Accessibility: axe-core / vitest-axe integrated and operational.
- Breakpoints: Standard Tailwind breakpoints confirmed (mobile < 768px, md = 768px, lg = 1024px).
- Package integrity: Zero changes required in package.json or lockfile.
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/category-label.test.ts
```
Expected output: Test passes without configuration or environment errors.

**Satisfies Requirements:** Req 11.1, 11.2, 11.3, 14.1, 15.1, 15.7

---

### M7.G1.T10: Goal 1 Checkpoint and Scope Integrity Audit

**Objective:** Run static typing, linting, and git diff checks to confirm Goal 1 deliverables are complete and no files outside the M7 boundary were modified.

**Acceptance Criteria:**
- ✓ `tests/fixtures/certifications-data.ts` and `certifications-arbitraries.ts` exist and compile.
- ✓ `src/lib/certifications/category-order.ts` and `category-label.ts` exist and compile.
- ✓ `tests/certifications/category-label.test.ts` passes.
- ✓ `npm run typecheck` and `npm run lint` pass with exit code 0.
- ✓ `git status` / `git diff` confirms no modifications to `package.json`, lockfiles, or files outside M7.

**Prerequisites:**
- Tasks M7.G1.T1 through M7.G1.T9 completed.

**Implementation Details:**
Run the test suite, linter, typechecker, and check git status across the project.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
npx vitest run tests/certifications/category-label.test.ts
git status --porcelain
```
Expected output:
- `tsc --noEmit` exits with 0.
- Vitest reports 4 tests passing in `category-label.test.ts`.
- `git status` shows only newly added files in `tests/fixtures/`, `src/lib/certifications/`, `tests/certifications/`, and `.kiro/specs/m7-certifications-module/task-notes.md`.

**Satisfies Requirements:** Req 1.5, 5.5, 13.7, 15.1, 15.5, 15.7, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 1 are complete:
```powershell
npx vitest run tests/certifications/category-label.test.ts
npx tsc --noEmit
```
Expected output: All category-label unit and property tests pass; TypeScript compiles with zero errors.