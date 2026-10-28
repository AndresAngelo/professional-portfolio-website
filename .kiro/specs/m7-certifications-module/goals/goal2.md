# M7.G2: Grouping Helper and Property Tests

> **Milestone:** M7 — Certifications Module  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks (M7.G2.T1 – M7.G2.T10)  
> **Status:** NOT STARTED  
> **Workspace Root:** `c:\dev\andres-webapp-professional\personal-website-portfolio`  
> **Project Root:** `personal-website-portfolio-v2\`  
> **Spec References:** `requirements.md` (Req 3.1–3.10, 4.2–4.4, 15.2), `design.md` (Properties 1–5, Data Models), `tasks.md` (M7.G2)

---

## Goal Objective

Implement the pure, deterministic `groupCertificationsByCategory` domain helper in `src/lib/certifications/group-certifications.ts`. This module partitions an input list of certifications into non-empty, ordered `CertificationGroup` instances adhering strictly to canonical `Category_Order`, sort specifications (`Certification_Order`: `displayOrder` ascending, then `slug` tie-breaker via `compareStrings`), and a defensive trailing `"Uncategorised"` fallback for out-of-spec category values. Verify total correctness across edge cases, deep freezing, and mathematical properties (partitioning, ordering, input-order independence, idempotence, immutability) via Vitest and `fast-check` Property Tests 1 through 5.

---

## Goal Success Criteria

- ✓ `src/lib/certifications/group-certifications.ts` exports `CertificationGroup` interface and `groupCertificationsByCategory`.
- ✓ Emits groups in exact `CATEGORY_ORDER` sequence, followed by at most one trailing `uncategorised` group when invalid/unknown categories exist.
- ✓ Completely empty categories produce no `CertificationGroup` (every returned group is strictly non-empty).
- ✓ Within each group, certifications are sorted by `displayOrder` ascending; ties broken deterministically by `compareStrings(a.slug, b.slug)`.
- ✓ The function is completely pure: zero I/O, no clock/locale/timezone reads, no client directives, zero side-effects.
- ✓ Input array and its objects remain unmodified; deep-frozen inputs execute without throwing.
- ✓ All 5 mathematical properties pass with >= 100 runs each using fast-check:
  - Property 1: Partition and no loss (conservation of elements).
  - Property 2: Groups in `Category_Order`, members in `Certification_Order`.
  - Property 3: Input-order independence (permutation invariance).
  - Property 4: Idempotence under flatten (`group(flatten(group(x))) === group(x)`).
  - Property 5: Immutability (no mutation of deep-frozen input).

---

## Prerequisites

- Goal 1 completed: `src/lib/certifications/category-order.ts`, `src/lib/certifications/category-label.ts`, `tests/fixtures/certifications-data.ts`, and `tests/fixtures/certifications-arbitraries.ts` available.
- `compareStrings` available at `@/lib/home/compare`.
- `Certification` and `CertificationCategory` available at `@/types/content`.

---

## Tasks

### M7.G2.T1: Define CertificationGroup and Ordering Comparators

**Objective:** Create `src/lib/certifications/group-certifications.ts` defining the `CertificationGroup` interface and the pure comparator for `Certification_Order`.

**Acceptance Criteria:**
- ✓ Exports interface `CertificationGroup` with `readonly category: GroupKey` and `readonly certifications: readonly Certification[]`.
- ✓ Implements internal comparator `compareCertifications(a: Certification, b: Certification): number`.
- ✓ Sorts primarily by `displayOrder` ascending (`a.displayOrder - b.displayOrder`).
- ✓ Sorts secondarily by `compareStrings(a.slug, b.slug)` for identical `displayOrder`.
- ✓ Reuses `compareStrings` from `@/lib/home/compare` without redefining it.
- ✓ Compiles cleanly with TypeScript strict mode.

**Prerequisites:**
- `src/lib/certifications/category-label.ts` exports `GroupKey`.
- `src/lib/home/compare.ts` exports `compareStrings`.
- `src/types/content.ts` exports `Certification`.

**Implementation Details:**
Create `src/lib/certifications/group-certifications.ts` with initial interfaces and comparator logic:

```typescript
import type { Certification } from '@/types/content';
import { compareStrings } from '@/lib/home/compare';
import { UNCATEGORISED, CATEGORY_ORDER } from './category-order';
import type { GroupKey } from './category-label';

export interface CertificationGroup {
  readonly category: GroupKey;
  readonly certifications: readonly Certification[];
}

export function compareCertifications(a: Certification, b: Certification): number {
  if (a.displayOrder !== b.displayOrder) {
    return a.displayOrder - b.displayOrder;
  }
  return compareStrings(a.slug, b.slug);
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors in `src/lib/certifications/group-certifications.ts`.

**Satisfies Requirements:** Req 1.5, 3.3, 15.5

---

### M7.G2.T2: Implement groupCertificationsByCategory Algorithm

**Objective:** Implement and export `groupCertificationsByCategory` in `src/lib/certifications/group-certifications.ts` supporting partitioning, canonical ordering, and defensive `"Uncategorised"` fallback.

**Acceptance Criteria:**
- ✓ Returns an empty array when input is empty.
- ✓ Creates a shallow copy of the input certifications and sorts them using `compareCertifications`.
- ✓ Buckets sorted certifications by category.
- ✓ Places any certification with a category not in `CATEGORY_ORDER` into the `UNCATEGORISED` bucket.
- ✓ Emits groups in the exact order of `CATEGORY_ORDER`, omitting any category with zero items.
- ✓ If the `UNCATEGORISED` bucket contains items, emits it as the final group.
- ✓ Returns a frozen or readonly array of immutable `CertificationGroup` objects.

**Prerequisites:**
- `M7.G2.T1` completed in `src/lib/certifications/group-certifications.ts`.

**Implementation Details:**
Update `src/lib/certifications/group-certifications.ts`:

```typescript
import type { Certification, CertificationCategory } from '@/types/content';
import { compareStrings } from '@/lib/home/compare';
import { UNCATEGORISED, CATEGORY_ORDER } from './category-order';
import type { GroupKey } from './category-label';

export interface CertificationGroup {
  readonly category: GroupKey;
  readonly certifications: readonly Certification[];
}

export function compareCertifications(a: Certification, b: Certification): number {
  if (a.displayOrder !== b.displayOrder) {
    return a.displayOrder - b.displayOrder;
  }
  return compareStrings(a.slug, b.slug);
}

const KNOWN_CATEGORIES = new Set<string>(CATEGORY_ORDER);

export function groupCertificationsByCategory(
  certifications: readonly Certification[],
): readonly CertificationGroup[] {
  if (certifications.length === 0) {
    return [];
  }

  // Defensive copy to prevent mutation of input array
  const sorted = [...certifications].sort(compareCertifications);

  // Group buckets initialized
  const buckets = new Map<GroupKey, Certification[]>();
  for (const cat of CATEGORY_ORDER) {
    buckets.set(cat, []);
  }
  buckets.set(UNCATEGORISED, []);

  // Partition elements
  for (const cert of sorted) {
    if (KNOWN_CATEGORIES.has(cert.category)) {
      buckets.get(cert.category)?.push(cert);
    } else {
      buckets.get(UNCATEGORISED)?.push(cert);
    }
  }

  const result: CertificationGroup[] = [];

  // Emit non-empty groups in Category_Order
  for (const cat of CATEGORY_ORDER) {
    const items = buckets.get(cat);
    if (items && items.length > 0) {
      result.push({
        category: cat,
        certifications: Object.freeze(items),
      });
    }
  }

  // Emit trailing uncategorised group if populated
  const uncategorisedItems = buckets.get(UNCATEGORISED);
  if (uncategorisedItems && uncategorisedItems.length > 0) {
    result.push({
      category: UNCATEGORISED,
      certifications: Object.freeze(uncategorisedItems),
    });
  }

  return Object.freeze(result);
}
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx tsc --noEmit
```
Expected output: No compilation errors.

**Satisfies Requirements:** Req 3.1, 3.2, 3.3, 3.4, 3.5, 3.8, 4.2, 4.4

---

### M7.G2.T3: Static Purity and Dependency Inspection

**Objective:** Verify that `src/lib/certifications/group-certifications.ts` contains no DOM references, React imports, Next.js imports, system clock reads, or locale calls.

**Acceptance Criteria:**
- ✓ File contains no `'use client'` or `'use server'` directives.
- ✓ File imports no modules from `'react'`, `'next'`, or node filesystem/network APIs.
- ✓ File contains zero references to `Date`, `new Date()`, `Intl`, `window`, or `document`.
- ✓ All types imported strictly from `@/types/content` and local helper modules.

**Prerequisites:**
- `src/lib/certifications/group-certifications.ts` completed.

**Implementation Details:**
Review source code and verify via AST/grep that no forbidden keywords or imports exist.

**Validation:**
Execute in Windows PowerShell:
```powershell
Select-String -Path src\lib\certifications\group-certifications.ts -Pattern "use client|use server|Date|Intl|window|document|react|next"
```
Expected output: No matches found.

**Satisfies Requirements:** Req 1.2, 3.10, 13.2, 13.3

---

### M7.G2.T4: Unit Tests for Standard, Edge, and Uncategorised Cases

**Objective:** Create `tests/certifications/group-certifications.test.ts` implementing concrete unit test cases for empty input, single category, multi-category, tie-breaking, and out-of-range categories.

**Acceptance Criteria:**
- ✓ Test: empty input `[]` returns `[]`.
- ✓ Test: single item input returns an array with exactly one group.
- ✓ Test: tie-breaking by `displayOrder` uses `compareStrings` on `slug`.
- ✓ Test: unknown category (via test cast) creates a trailing `"Uncategorised"` group.
- ✓ Test: valid categories only result in zero `"Uncategorised"` groups.

**Prerequisites:**
- `src/lib/certifications/group-certifications.ts` implemented.
- `tests/fixtures/certifications-data.ts` available.

**Implementation Details:**
Create `tests/certifications/group-certifications.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import {
  groupCertificationsByCategory,
  compareCertifications,
} from '@/lib/certifications/group-certifications';
import { UNCATEGORISED } from '@/lib/certifications/category-order';
import {
  fixtureCertificationsList,
  fixtureEmptyCertificationsList,
  fixtureUncategorisedCertification,
  fixtureFullCertification,
  fixtureExpiredCertification,
} from '../fixtures/certifications-data';
import type { Certification } from '@/types/content';

describe('groupCertificationsByCategory - Unit Tests', () => {
  it('returns empty array when given empty input', () => {
    const result = groupCertificationsByCategory(fixtureEmptyCertificationsList);
    expect(result).toEqual([]);
  });

  it('groups a single certification into its category', () => {
    const result = groupCertificationsByCategory([fixtureFullCertification]);
    expect(result.length).toBe(1);
    expect(result[0].category).toBe('cloud');
    expect(result[0].certifications).toEqual([fixtureFullCertification]);
  });

  it('breaks displayOrder ties using compareStrings on slug', () => {
    const certA: Certification = {
      ...fixtureFullCertification,
      slug: 'cert-alpha',
      displayOrder: 1,
    };
    const certB: Certification = {
      ...fixtureFullCertification,
      slug: 'cert-beta',
      displayOrder: 1,
    };

    expect(compareCertifications(certA, certB)).toBeLessThan(0);
    expect(compareCertifications(certB, certA)).toBeGreaterThan(0);

    const result = groupCertificationsByCategory([certB, certA]);
    expect(result[0].certifications[0].slug).toBe('cert-alpha');
    expect(result[0].certifications[1].slug).toBe('cert-beta');
  });

  it('places unknown categories in trailing uncategorised group', () => {
    const mixed = [fixtureFullCertification, fixtureUncategorisedCertification];
    const result = groupCertificationsByCategory(mixed);

    expect(result.length).toBe(2);
    expect(result[0].category).toBe('cloud');
    expect(result[1].category).toBe(UNCATEGORISED);
    expect(result[1].certifications).toEqual([fixtureUncategorisedCertification]);
  });

  it('does not produce an uncategorised group when all categories are valid', () => {
    const result = groupCertificationsByCategory(fixtureCertificationsList);
    const hasUncategorised = result.some((g) => g.category === UNCATEGORISED);
    expect(hasUncategorised).toBe(false);
  });
});
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: All 5 unit tests pass.

**Satisfies Requirements:** Req 3.1, 3.3, 3.8, 4.2, 4.3

---

### M7.G2.T5: Property 1 Test — Partition and Conservation of Elements

**Objective:** Implement Property 1 in `tests/certifications/group-certifications.test.ts` verifying that grouping forms a complete partition with zero element loss or duplication.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 1: Grouping is a partition with no loss`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Flattens output groups and asserts element count equals input length.
- ✓ Asserts every item in `group.certifications` has category matching `group.category` (or non-standard category matching `UNCATEGORISED`).
- ✓ Asserts every group in output is non-empty (`certifications.length > 0`).

**Prerequisites:**
- `createArbCertification` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/group-certifications.test.ts`:

```typescript
import fc from 'fast-check';
import { createArbCertification } from '../fixtures/certifications-arbitraries';
import { CATEGORY_ORDER } from '@/lib/certifications/category-order';

const arbAnyCertList = fc.array(createArbCertification({ allowUnknownCategory: true }), {
  minLength: 0,
  maxLength: 25,
});

describe('groupCertificationsByCategory - Property Tests', () => {
  // Feature: m7-certifications-module, Property 1: Grouping is a partition with no loss
  it('Property 1: Partition and no loss across arbitrary certifications', () => {
    fc.assert(
      fc.property(arbAnyCertList, (certifications) => {
        const groups = groupCertificationsByCategory(certifications);

        // Every group must be non-empty
        for (const group of groups) {
          expect(group.certifications.length).toBeGreaterThan(0);
        }

        // Flatten all groups
        const flattened = groups.flatMap((g) => g.certifications);

        // Count conservation
        expect(flattened.length).toBe(certifications.length);

        // Category matching assertion
        for (const group of groups) {
          for (const cert of group.certifications) {
            if (group.category === UNCATEGORISED) {
              expect(CATEGORY_ORDER).not.toContain(cert.category);
            } else {
              expect(cert.category).toBe(group.category);
            }
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
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: Property 1 passes with >= 100 runs.

**Satisfies Requirements:** Req 3.1, 3.4, 3.5, 3.8, 4.2, 15.2

---

### M7.G2.T6: Property 2 Test — Group and Member Ordering

**Objective:** Implement Property 2 in `tests/certifications/group-certifications.test.ts` verifying that category groups and members within groups strictly follow ordering requirements.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 2: Groups and members are ordered`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Asserts group sequence matches `CATEGORY_ORDER` index order, with `UNCATEGORISED` always last.
- ✓ Asserts certifications within each group are strictly ordered by `displayOrder` ascending, then `slug` ascending.

**Prerequisites:**
- `tests/certifications/group-certifications.test.ts` updated with Property 1.

**Implementation Details:**
Append to `tests/certifications/group-certifications.test.ts`:

```typescript
  // Feature: m7-certifications-module, Property 2: Groups and members are ordered
  it('Property 2: Groups follow Category_Order and members follow Certification_Order', () => {
    fc.assert(
      fc.property(arbAnyCertList, (certifications) => {
        const groups = groupCertificationsByCategory(certifications);

        // Check group ordering
        let lastIndex = -1;
        for (const group of groups) {
          if (group.category === UNCATEGORISED) {
            // Uncategorised must be the last group
            expect(group).toBe(groups[groups.length - 1]);
          } else {
            const currentIndex = CATEGORY_ORDER.indexOf(group.category as any);
            expect(currentIndex).toBeGreaterThan(lastIndex);
            lastIndex = currentIndex;
          }
        }

        // Check member ordering inside each group
        for (const group of groups) {
          for (let i = 0; i < group.certifications.length - 1; i++) {
            const current = group.certifications[i];
            const next = group.certifications[i + 1];
            expect(compareCertifications(current, next)).toBeLessThanOrEqual(0);
          }
        }
      }),
      { numRuns: 100 },
    );
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: Property 2 passes with >= 100 runs.

**Satisfies Requirements:** Req 3.2, 3.3, 4.4, 15.2

---

### M7.G2.T7: Property 3 Test — Input-Order Independence

**Objective:** Implement Property 3 in `tests/certifications/group-certifications.test.ts` verifying that output grouping is completely invariant under arbitrary permutations of the input list.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 3: Grouping is independent of input order`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Pairs an arbitrary certification list with a shuffled version of itself.
- ✓ Asserts `groupCertificationsByCategory(list)` deeply equals `groupCertificationsByCategory(shuffled)`.

**Prerequisites:**
- `arbCertification` in `tests/fixtures/certifications-arbitraries.ts`.

**Implementation Details:**
Append to `tests/certifications/group-certifications.test.ts`:

```typescript
  // Feature: m7-certifications-module, Property 3: Grouping is independent of input order
  it('Property 3: Output is invariant under input permutation', () => {
    const arbPermutationPair = fc
      .uniqueArray(createArbCertification(), { selector: (c) => c.slug, minLength: 2, maxLength: 15 })
      .chain((list) => fc.tuple(fc.constant(list), fc.shuffledSubarray(list, { minLength: list.length })));

    fc.assert(
      fc.property(arbPermutationPair, ([original, shuffled]) => {
        const outOriginal = groupCertificationsByCategory(original);
        const outShuffled = groupCertificationsByCategory(shuffled);
        expect(outOriginal).toEqual(outShuffled);
      }),
      { numRuns: 100 },
    );
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: Property 3 passes with >= 100 runs.

**Satisfies Requirements:** Req 3.6, 15.2

---

### M7.G2.T8: Property 4 Test — Idempotence under Flatten

**Objective:** Implement Property 4 in `tests/certifications/group-certifications.test.ts` verifying that `groupCertificationsByCategory` is idempotent when reapplied to its own flattened output.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 4: Grouping is idempotent under flatten`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Defines `flatten = (groups) => groups.flatMap(g => g.certifications)`.
- ✓ Asserts `groupCertificationsByCategory(flatten(groupCertificationsByCategory(list)))` deeply equals `groupCertificationsByCategory(list)`.

**Prerequisites:**
- `tests/certifications/group-certifications.test.ts` updated with Property 3.

**Implementation Details:**
Append to `tests/certifications/group-certifications.test.ts`:

```typescript
  // Feature: m7-certifications-module, Property 4: Grouping is idempotent under flatten
  it('Property 4: group(flatten(group(list))) deeply equals group(list)', () => {
    fc.assert(
      fc.property(arbAnyCertList, (certifications) => {
        const firstPass = groupCertificationsByCategory(certifications);
        const flattened = firstPass.flatMap((g) => g.certifications);
        const secondPass = groupCertificationsByCategory(flattened);
        expect(secondPass).toEqual(firstPass);
      }),
      { numRuns: 100 },
    );
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: Property 4 passes with >= 100 runs.

**Satisfies Requirements:** Req 3.7, 15.2

---

### M7.G2.T9: Property 5 Test — Immutability and Deep-Freeze Safety

**Objective:** Implement Property 5 in `tests/certifications/group-certifications.test.ts` verifying that input arrays and objects are never mutated and that deep-frozen inputs execute cleanly.

**Acceptance Criteria:**
- ✓ Tagged: `Feature: m7-certifications-module, Property 5: Grouping does not mutate its input`.
- ✓ Tests at least 100 runs using `fast-check`.
- ✓ Creates a recursive `deepFreeze` helper in test.
- ✓ Deeply freezes the input array and every certification element.
- ✓ Calls `groupCertificationsByCategory` on the frozen structure and asserts it does not throw.
- ✓ Asserts original input array and properties remain unchanged.

**Prerequisites:**
- `tests/certifications/group-certifications.test.ts` updated with Property 4.

**Implementation Details:**
Append to `tests/certifications/group-certifications.test.ts`:

```typescript
function deepFreeze<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  Object.freeze(obj);
  for (const key of Object.keys(obj)) {
    const val = (obj as any)[key];
    if (val !== null && typeof val === 'object' && !Object.isFrozen(val)) {
      deepFreeze(val);
    }
  }
  return obj;
}

  // Feature: m7-certifications-module, Property 5: Grouping does not mutate its input
  it('Property 5: Does not mutate input array or objects, handles deep-frozen input', () => {
    fc.assert(
      fc.property(arbAnyCertList, (certifications) => {
        const cloned = JSON.parse(JSON.stringify(certifications));
        deepFreeze(cloned);

        expect(() => groupCertificationsByCategory(cloned)).not.toThrow();

        // Verify elements still equal original representation
        expect(cloned).toEqual(certifications);
      }),
      { numRuns: 100 },
    );
  });
```

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
```
Expected output: Property 5 passes with >= 100 runs.

**Satisfies Requirements:** Req 3.9, 3.10, 15.2

---

### M7.G2.T10: Goal 2 Verification and Pipeline Checkpoint

**Objective:** Run the full test suite, linter, and typechecker across Goal 2 artifacts to verify that `group-certifications.ts` passes all quality gates.

**Acceptance Criteria:**
- ✓ `src/lib/certifications/group-certifications.ts` compiles cleanly with no type assertions (`as any` only justified if in tests).
- ✓ `tests/certifications/group-certifications.test.ts` passes all 5 unit tests and all 5 property tests (100 runs each).
- ✓ `npx tsc --noEmit` exits with 0.
- ✓ `git status` shows no modified files outside permitted scope.

**Prerequisites:**
- Tasks M7.G2.T1 through M7.G2.T9 completed.

**Implementation Details:**
Execute test suite, linter, and typecheck commands via Windows PowerShell.

**Validation:**
Execute in Windows PowerShell:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
npx tsc --noEmit
```
Expected output:
- Vitest reports 10 tests passing (5 unit, 5 property) in `tests/certifications/group-certifications.test.ts`.
- TypeScript compiler exits with code 0.

**Satisfies Requirements:** Req 3.1–3.10, 4.2–4.4, 15.2, 15.5, 15.8

---

## Goal Checkpoint

Run the following command to confirm all tasks in Goal 2 are complete:
```powershell
npx vitest run tests/certifications/group-certifications.test.ts
npx tsc --noEmit
```
Expected output: All 10 unit and property tests in `group-certifications.test.ts` pass with exit code 0. Zero TypeScript errors.