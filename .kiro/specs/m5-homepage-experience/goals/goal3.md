# M5.G3: Skill Derivation, Hero Contact Action, and Property Tests

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure business logic modules for technology skill derivation and hero call-to-action resolution in `src/lib/home/`: `derive-skill-groups.ts` and `select-hero-action.ts`. `deriveSkillGroups` aggregates technology labels from project data into a structured single group labeled `Technologies`, trimming names, reconciling case-insensitive duplicates to their first-seen spelling, counting occurrences once per project, and ordering entries by project frequency descending with deterministic alphabetical tie-breaking, returning an empty array when no technologies exist without fabricating categories or proficiency ratings. `selectHeroContactAction` evaluates public communication channels, selecting the first renderable channel designated as primary (`isPrimary: true`) or falling back to the first renderable channel, classifying actions as `external` (for `https://`), `mailto` (for `mailto:`), or `internal`, and returning `null` when no renderable channels exist. Validate both modules with comprehensive Vitest unit tests and fast-check property tests for Properties 5, 6, 7, and the skill-derivation case of Property 4.

## Goal Success Criteria

- ✓ `src/lib/home/derive-skill-groups.ts` exports `SkillEntry`, `SkillGroup`, and pure function `deriveSkillGroups(projects: readonly Pick<Project, 'technologies'>[]): SkillGroup[]`
- ✓ `deriveSkillGroups` deduplicates technology names case-insensitively, preserves first-seen spelling, increments count at most once per project, and orders by `count` descending then alphabetical ascending
- ✓ `deriveSkillGroups` returns `[]` when input contains zero technologies and fabricates zero skill names or categories
- ✓ `src/lib/home/select-hero-action.ts` exports `HeroContactAction`, `isRenderableChannel`, and pure function `selectHeroContactAction(channels: readonly ContactChannel[]): HeroContactAction | null`
- ✓ `selectHeroContactAction` selects primary channel first, falls back to first renderable channel, identifies URL kind accurately, and returns `null` when channels are empty or invalid
- ✓ Neither module imports React or Next.js nor contains `'use client'` statements
- ✓ Unit and property tests in `tests/home/derive-skill-groups.test.ts` satisfy Properties 5, 6, and the immutability case of Property 4 ($\ge 100$ runs with `fast-check`)
- ✓ Unit and property tests in `tests/home/select-hero-action.test.ts` satisfy Property 7 ($\ge 100$ runs with `fast-check`)
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Goals M5.G1 and M5.G2 completed (`compare.ts`, `home-text.ts`, fixtures, and arbitraries available)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream types imported strictly from `@/types/content`

---

## Tasks

### M5.G3.T1: Implement Skill Groups Derivation Data Structures and Core Algorithm (`src/lib/home/derive-skill-groups.ts`)

**Objective:** Author the data structures and core aggregation loop for `deriveSkillGroups` in `src/lib/home/derive-skill-groups.ts`.

**Acceptance Criteria:**
- ✓ File `src/lib/home/derive-skill-groups.ts` created
- ✓ Exports `interface SkillEntry { readonly name: string; readonly count: number; }`
- ✓ Exports `interface SkillGroup { readonly label: string; readonly technologies: readonly SkillEntry[]; }`
- ✓ Accepts `readonly Pick<Project, 'technologies'>[]`
- ✓ Traverses projects, builds a unique case-insensitive set of trimmed technologies per project
- ✓ Retains first-seen casing and increments frequency count per project
- ✓ Skips empty or whitespace-only technology strings
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- M5.G1 completed (`compareStrings` in `compare.ts`, `HOME_TEXT` in `home-text.ts`)
- Target file: `src/lib/home/derive-skill-groups.ts`

**Implementation Details:**

Write the initial implementation of `src/lib/home/derive-skill-groups.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Business Logic: Technology Skills Derivation
 *
 * Derives compact skill groups from project metadata.
 * Enforces zero-fabrication: derives exclusively from project technologies (Req 8.1-8.7, 9.5, 16.6).
 */
import type { Project } from '@/types/content';
import { HOME_TEXT } from '@/components/home/home-text';
import { compareStrings } from './compare';

export interface SkillEntry {
  readonly name: string;
  readonly count: number;
}

export interface SkillGroup {
  readonly label: string;
  readonly technologies: readonly SkillEntry[];
}
'@ | Set-Content "src\lib\home\derive-skill-groups.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/derive-skill-groups.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.4, Req 16.6

---

### M5.G3.T2: Implement Sorting and Group Packaging in `deriveSkillGroups`

**Objective:** Complete `deriveSkillGroups` in `src/lib/home/derive-skill-groups.ts` with frequency-descending alphabetical sorting and empty group suppression.

**Acceptance Criteria:**
- ✓ Exports `deriveSkillGroups(projects: readonly Pick<Project, 'technologies'>[]): SkillGroup[]`
- ✓ Sorts aggregated skills by `count` descending
- ✓ Breaks ties on identical `count` by lowercase name ascending via `compareStrings`, then by original name
- ✓ Returns `[]` if input contains zero valid technologies (Req 8.4)
- ✓ Packages non-empty skills into a single `SkillGroup` with `label: HOME_TEXT.skillsGroupLabel` (`'Technologies'`)
- ✓ Operates immutably without altering input project objects
- ✓ Pure function with zero runtime framework dependencies

**Prerequisites:**
- M5.G3.T1 completed
- Target file: `src/lib/home/derive-skill-groups.ts`

**Implementation Details:**

Append the function body to `src/lib/home/derive-skill-groups.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

interface RawSkillData {
  firstSeenName: string;
  count: number;
}

/**
 * Derives skill groups exclusively from project technologies.
 * Returns empty array if no technologies exist in input.
 */
export function deriveSkillGroups(
  projects: readonly Pick<Project, 'technologies'>[]
): SkillGroup[] {
  const skillMap = new Map<string, RawSkillData>();

  for (const project of projects) {
    if (!project.technologies || project.technologies.length === 0) {
      continue;
    }

    // Set of normalized keys seen in this single project to avoid multi-counting
    const projectSeenKeys = new Set<string>();

    for (const rawTech of project.technologies) {
      if (typeof rawTech !== 'string') {
        continue;
      }
      const trimmed = rawTech.trim();
      if (trimmed.length === 0) {
        continue;
      }

      const key = trimmed.toLowerCase();
      if (projectSeenKeys.has(key)) {
        continue; // duplicate in same project counts once (Req 8.3)
      }
      projectSeenKeys.add(key);

      const existing = skillMap.get(key);
      if (existing) {
        existing.count += 1;
      } else {
        skillMap.set(key, {
          firstSeenName: trimmed,
          count: 1,
        });
      }
    }
  }

  if (skillMap.size === 0) {
    return [];
  }

  const entries: SkillEntry[] = Array.from(skillMap.values()).map((item) => ({
    name: item.firstSeenName,
    count: item.count,
  }));

  // Sort by count descending, then alphabetical ascending
  entries.sort((a, b) => {
    if (a.count !== b.count) {
      return b.count - a.count;
    }
    const lowerA = a.name.toLowerCase();
    const lowerB = b.name.toLowerCase();
    const cmp = compareStrings(lowerA, lowerB);
    if (cmp !== 0) {
      return cmp;
    }
    return compareStrings(a.name, b.name);
  });

  return [
    {
      label: HOME_TEXT.skillsGroupLabel,
      technologies: entries,
    },
  ];
}
'@

Add-Content -Path "src\lib\home\derive-skill-groups.ts" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/derive-skill-groups.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5, Req 8.7, Req 9.4, Req 9.5

---

### M5.G3.T3: Implement Hero Contact Action Selection Helper (`src/lib/home/select-hero-action.ts`)

**Objective:** Author `selectHeroContactAction` and `isRenderableChannel` in `src/lib/home/select-hero-action.ts` resolving the primary or fallback contact call to action.

**Acceptance Criteria:**
- ✓ File `src/lib/home/select-hero-action.ts` created
- ✓ Exports `interface HeroContactAction { readonly label: string; readonly url: string; readonly kind: 'external' | 'mailto' | 'internal'; }`
- ✓ Exports `isRenderableChannel(channel: Pick<ContactChannel, 'label' | 'url'>): boolean` (requires non-empty trimmed label and url)
- ✓ Exports `selectHeroContactAction(channels: readonly ContactChannel[]): HeroContactAction | null`
- ✓ Selects first renderable channel where `isPrimary === true`; falls back to first renderable channel if none is primary
- ✓ Classifies URLs: `https://` $\rightarrow$ `'external'`, `mailto:` $\rightarrow$ `'mailto'`, otherwise `'internal'`
- ✓ Returns `null` if channels array is empty or contains zero renderable channels
- ✓ Zero imports from `react` or `next`

**Prerequisites:**
- Target file: `src/lib/home/select-hero-action.ts`

**Implementation Details:**

Write `src/lib/home/select-hero-action.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Pure Selection Helper: Hero Contact Action
 *
 * Resolves the primary or fallback contact action for the hero section.
 * Contains no React, Next.js, or browser dependencies (Req 3.3-3.5, 16.6).
 */
import type { ContactChannel } from '@/types/content';

export interface HeroContactAction {
  readonly label: string;
  readonly url: string;
  readonly kind: 'external' | 'mailto' | 'internal';
}

/**
 * Checks whether a contact channel has non-empty label and destination URL.
 */
export function isRenderableChannel(
  channel: Pick<ContactChannel, 'label' | 'url'>
): boolean {
  if (!channel || typeof channel.label !== 'string' || typeof channel.url !== 'string') {
    return false;
  }
  return channel.label.trim().length > 0 && channel.url.trim().length > 0;
}

/**
 * Selects the hero contact call-to-action from configured channels.
 * Prioritizes the isPrimary channel, falling back to the first renderable channel.
 * Returns null if no channel is renderable.
 */
export function selectHeroContactAction(
  channels: readonly ContactChannel[]
): HeroContactAction | null {
  if (!channels || channels.length === 0) {
    return null;
  }

  const renderable = channels.filter(isRenderableChannel);
  if (renderable.length === 0) {
    return null;
  }

  const chosen = renderable.find((c) => c.isPrimary) ?? renderable[0];
  const trimmedUrl = chosen.url.trim();

  let kind: 'external' | 'mailto' | 'internal' = 'internal';
  if (trimmedUrl.startsWith('https://')) {
    kind = 'external';
  } else if (trimmedUrl.startsWith('mailto:')) {
    kind = 'mailto';
  }

  return {
    label: chosen.label.trim(),
    url: trimmedUrl,
    kind,
  };
}
'@ | Set-Content "src\lib\home\select-hero-action.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/select-hero-action.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.4, Req 3.5, Req 16.6

---

### M5.G3.T4: Audit Modules for Client Directives and Hardcoded Data

**Objective:** Audit `src/lib/home/derive-skill-groups.ts` and `select-hero-action.ts` ensuring zero `'use client'` statements and zero hardcoded technology or contact strings.

**Acceptance Criteria:**
- ✓ Searches both files for `'use client'`
- ✓ Searches both files for literals from `content/site.json` or sample project names
- ✓ Confirms zero matches
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M5.G3.T2 and M5.G3.T3 completed

**Implementation Details:**

Execute audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$files = @("src\lib\home\derive-skill-groups.ts", "src\lib\home\select-hero-action.ts")
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    if ($content -match "['""]use client['""]") {
        $violations += "Forbidden 'use client' found in $file"
    }
    if ($content -match "['""]Angelo['""]|['""]hello@example\.com['""]|['""]TypeScript['""]") {
        $violations += "Hardcoded site/content literal found in $file"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.2, Req 2.5, Req 8.5, Req 9.5, Req 16.6

---

### M5.G3.T5: Author Unit Scenarios for Skill Derivation (`tests/home/derive-skill-groups.test.ts`)

**Objective:** Create `tests/home/derive-skill-groups.test.ts` testing concrete skill aggregation scenarios: case insensitivity, intra-project deduplication, frequency ranking, and empty inputs.

**Acceptance Criteria:**
- ✓ File `tests/home/derive-skill-groups.test.ts` created
- ✓ Tests empty project array yields `[]`
- ✓ Tests projects with empty technologies yield `[]`
- ✓ Tests `['TypeScript', 'typescript']` across projects merges into single entry with count 2 and first-seen casing
- ✓ Tests project listing `['Docker', 'Docker']` twice increments count by 1 only
- ✓ Tests ranking orders higher frequency technologies first
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G3.T2 completed
- Target file: `tests/home/derive-skill-groups.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/home/derive-skill-groups.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import { deriveSkillGroups } from '@/lib/home/derive-skill-groups';
import { sampleProjects, emptyProjects } from '../fixtures/home-data';

describe('deriveSkillGroups Helper (Req 8)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('returns empty array when projects list is empty', () => {
      expect(deriveSkillGroups(emptyProjects)).toEqual([]);
    });

    it('returns empty array when projects contain no technologies', () => {
      const noTechs = [{ technologies: [] }, { technologies: ['   ', ''] }];
      expect(deriveSkillGroups(noTechs as any)).toEqual([]);
    });

    it('merges case variations under first-seen spelling and counts once per project', () => {
      const projects = [
        { technologies: ['TypeScript', 'React'] },
        { technologies: ['typescript', 'Docker'] }, // lowercased typescript
        { technologies: ['TYPESCRIPT', 'React', 'React'] }, // intra-project duplicate React
      ];

      const groups = deriveSkillGroups(projects as any);
      expect(groups.length).toBe(1);
      expect(groups[0].label).toBe('Technologies');

      const techs = groups[0].technologies;
      expect(techs.find((t) => t.name === 'TypeScript')?.count).toBe(3);
      expect(techs.find((t) => t.name === 'React')?.count).toBe(2);
      expect(techs.find((t) => t.name === 'Docker')?.count).toBe(1);
    });

    it('sorts skills by count descending, then alphabetical', () => {
      const groups = deriveSkillGroups(sampleProjects);
      expect(groups.length).toBe(1);
      const techs = groups[0].technologies;

      // In sampleProjects:
      // TypeScript appears in Alpha, Beta, Gamma (count: 3)
      // Docker in Beta, Epsilon (count: 2)
      // Next.js in Alpha, Delta (count: 2)
      // Tailwind CSS in Alpha, Delta (count: 2)
      expect(techs[0].name).toBe('TypeScript');
      expect(techs[0].count).toBe(3);

      // Verify non-increasing counts
      for (let i = 1; i < techs.length; i++) {
        expect(techs[i].count).toBeLessThanOrEqual(techs[i - 1].count);
      }
    });
  });
});
'@ | Set-Content "tests\home\derive-skill-groups.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/derive-skill-groups.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.3, Req 8.4, Req 8.5

---

### M5.G3.T6: Author Property-Based Test for Skill Derivation Content Invariant (Property 5)

**Objective:** Append property-based test in `tests/home/derive-skill-groups.test.ts` validating Property 5: derived skills match the input technology set case-insensitively with zero duplicates.

**Acceptance Criteria:**
- ✓ Implements Property 5 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 5: derived skills contain exactly the technologies in project data`
- ✓ Asserts set of derived technology names (lowercased) equals set of input technology names (lowercased)
- ✓ Asserts zero duplicate names exist in result
- ✓ Asserts spelling matches first-seen occurrence in input order
- ✓ Asserts result is `[]` iff input has no valid technologies
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G3.T5 completed
- Arbitraries available in `tests/fixtures/home-arbitraries.ts`
- Target file: `tests/home/derive-skill-groups.test.ts`

**Implementation Details:**

Append Property 5 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 5)', () => {
    it('Feature: m5-homepage-experience, Property 5: derived skills contain exactly the technologies in project data with zero fabrication', () => {
      const fc = require('fast-check');
      const { arbProject } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(fc.array(arbProject, { minLength: 0, maxLength: 15 }), (projects: any) => {
          const groups = deriveSkillGroups(projects);

          // Collect all non-empty trimmed technologies from input
          const inputNames: string[] = [];
          for (const p of projects) {
            for (const t of p.technologies || []) {
              const trimmed = t.trim();
              if (trimmed.length > 0) {
                inputNames.push(trimmed);
              }
            }
          }

          if (inputNames.length === 0) {
            expect(groups).toEqual([]);
            return;
          }

          expect(groups.length).toBe(1);
          const derived = groups[0].technologies;

          // 1. Set equality (lowercased)
          const inputLowerSet = new Set(inputNames.map((s) => s.toLowerCase()));
          const derivedLowerSet = new Set(derived.map((s) => s.name.toLowerCase()));
          expect(derivedLowerSet).toEqual(inputLowerSet);

          // 2. Zero duplicates in result
          expect(derived.length).toBe(derivedLowerSet.size);

          // 3. First-seen spelling check
          const firstSeenMap = new Map<string, string>();
          for (const name of inputNames) {
            const key = name.toLowerCase();
            if (!firstSeenMap.has(key)) {
              firstSeenMap.set(key, name);
            }
          }
          for (const entry of derived) {
            expect(entry.name).toBe(firstSeenMap.get(entry.name.toLowerCase()));
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\derive-skill-groups.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\derive-skill-groups.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/derive-skill-groups.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1, Req 8.2, Req 8.4, Req 8.5, Req 8.6, Req 9.5

---

### M5.G3.T7: Author Property-Based Test for Skill Ordering & Immutability (Property 6 & 4)

**Objective:** Append property-based test in `tests/home/derive-skill-groups.test.ts` validating Property 6 (ranking by count then alphabetical) and the skill-derivation case of Property 4 (input immutability).

**Acceptance Criteria:**
- ✓ Implements Property 6 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 6: skill ordering by project count then name`
- ✓ Asserts counts strictly equal number of projects containing technology
- ✓ Asserts ordering is `count` descending with alphabetical tie-breaking
- ✓ Asserts deep-frozen project inputs are never mutated
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G3.T6 completed
- Target file: `tests/home/derive-skill-groups.test.ts`

**Implementation Details:**

Append Property 6 and immutability test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 6 & Immutability)', () => {
    it('Feature: m5-homepage-experience, Property 6: skills ordered by project count then name, and input is never mutated', () => {
      const fc = require('fast-check');
      const { arbProject } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(fc.array(arbProject, { minLength: 1, maxLength: 10 }), (projects: any) => {
          const frozen = Object.freeze(JSON.parse(JSON.stringify(projects)));
          const snapshot = JSON.stringify(frozen);

          const groups = deriveSkillGroups(frozen);
          expect(JSON.stringify(frozen)).toBe(snapshot); // input immutability (Property 4)

          if (groups.length === 0) {
            return;
          }

          const techs = groups[0].technologies;

          // Verify exact counts and ordering
          for (let i = 0; i < techs.length; i++) {
            const entry = techs[i];
            const lowerKey = entry.name.toLowerCase();

            // Calculate expected project count
            let expectedCount = 0;
            for (const p of projects) {
              const hasTech = (p.technologies || []).some((t: string) => t.trim().toLowerCase() === lowerKey);
              if (hasTech) {
                expectedCount += 1;
              }
            }
            expect(entry.count).toBe(expectedCount);

            if (i > 0) {
              const prev = techs[i - 1];
              if (prev.count === entry.count) {
                expect(prev.name.toLowerCase().localeCompare(entry.name.toLowerCase())).toBeLessThanOrEqual(0);
              } else {
                expect(prev.count).toBeGreaterThan(entry.count);
              }
            }
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\derive-skill-groups.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\derive-skill-groups.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/derive-skill-groups.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.5, Req 8.3, Req 8.7

---

### M5.G3.T8: Author Concrete Unit Scenarios for Hero Contact Action Selection

**Objective:** Create `tests/home/select-hero-action.test.ts` verifying concrete cases for `selectHeroContactAction` and `isRenderableChannel`.

**Acceptance Criteria:**
- ✓ File `tests/home/select-hero-action.test.ts` created
- ✓ Tests `isRenderableChannel` rejects empty label or whitespace URL
- ✓ Tests primary channel is selected when present
- ✓ Tests falls back to first renderable channel when no primary exists
- ✓ Tests classifies `https://` as `'external'`, `mailto:` as `'mailto'`, and relative path as `'internal'`
- ✓ Tests returns `null` when channels array is empty
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G3.T3 completed
- Target file: `tests/home/select-hero-action.test.ts`

**Implementation Details:**

Write unit scenarios in `tests/home/select-hero-action.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import {
  selectHeroContactAction,
  isRenderableChannel,
} from '@/lib/home/select-hero-action';
import { sampleSiteConfig, emptyContactChannelsSiteConfig } from '../fixtures/home-data';

describe('selectHeroContactAction Helper (Req 3)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('validates renderability of contact channels', () => {
      expect(isRenderableChannel({ label: 'Email', url: 'mailto:a@b.com' })).toBe(true);
      expect(isRenderableChannel({ label: '  ', url: 'https://example.com' })).toBe(false);
      expect(isRenderableChannel({ label: 'Email', url: '   ' })).toBe(false);
    });

    it('selects primary channel with mailto kind', () => {
      const action = selectHeroContactAction(sampleSiteConfig.contactChannels);
      expect(action).not.toBeNull();
      expect(action?.label).toBe('Email Angelo');
      expect(action?.url).toBe('mailto:hello@example.com');
      expect(action?.kind).toBe('mailto');
    });

    it('selects primary channel with external kind when url starts with https', () => {
      const channels = [
        { type: 'linkedin' as const, label: 'LinkedIn', url: 'https://linkedin.com/in/test', isPrimary: true },
        { type: 'email' as const, label: 'Email', url: 'mailto:test@test.com', isPrimary: false },
      ];
      const action = selectHeroContactAction(channels);
      expect(action?.label).toBe('LinkedIn');
      expect(action?.kind).toBe('external');
    });

    it('falls back to first renderable channel when no channel is marked primary', () => {
      const channels = [
        { type: 'github' as const, label: 'GitHub', url: 'https://github.com/test', isPrimary: false },
        { type: 'website' as const, label: 'Web', url: 'https://test.com', isPrimary: false },
      ];
      const action = selectHeroContactAction(channels);
      expect(action?.label).toBe('GitHub');
      expect(action?.kind).toBe('external');
    });

    it('returns null when channels array is empty or unrenderable', () => {
      expect(selectHeroContactAction(emptyContactChannelsSiteConfig.contactChannels)).toBeNull();
      expect(selectHeroContactAction([{ type: 'other', label: '', url: '', isPrimary: true } as any])).toBeNull();
    });
  });
});
'@ | Set-Content "tests\home\select-hero-action.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-hero-action.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.4, Req 3.5

---

### M5.G3.T9: Author Property-Based Test for Hero Contact Action Selection (Property 7)

**Objective:** Append property-based test in `tests/home/select-hero-action.test.ts` validating Property 7 across arbitrary contact channel arrays.

**Acceptance Criteria:**
- ✓ Implements Property 7 test ($\ge 100$ runs with `fast-check`)
- ✓ Tagged: `Feature: m5-homepage-experience, Property 7: hero contact action selection`
- ✓ Asserts returns `null` iff no renderable channel exists
- ✓ Asserts returns primary channel if one exists among renderable items
- ✓ Asserts returns first renderable channel if no primary exists
- ✓ Asserts `kind` strictly reflects URL protocol (`https://` $\rightarrow$ `'external'`, `mailto:` $\rightarrow$ `'mailto'`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G3.T8 completed
- Arbitraries available in `tests/fixtures/home-arbitraries.ts`
- Target file: `tests/home/select-hero-action.test.ts`

**Implementation Details:**

Append Property 7 test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Invariants (Property 7)', () => {
    it('Feature: m5-homepage-experience, Property 7: hero contact action selection invariants hold for any channels array', () => {
      const fc = require('fast-check');
      const { arbContactChannel } = require('../fixtures/home-arbitraries');

      fc.assert(
        fc.property(fc.array(arbContactChannel, { minLength: 0, maxLength: 8 }), (channels: any) => {
          const action = selectHeroContactAction(channels);
          const renderable = channels.filter((c: any) => isRenderableChannel(c));

          if (renderable.length === 0) {
            expect(action).toBeNull();
            return;
          }

          expect(action).not.toBeNull();
          const primary = renderable.find((c: any) => c.isPrimary);
          const expectedChosen = primary || renderable[0];

          expect(action?.label).toBe(expectedChosen.label.trim());
          expect(action?.url).toBe(expectedChosen.url.trim());

          if (expectedChosen.url.trim().startsWith('https://')) {
            expect(action?.kind).toBe('external');
          } else if (expectedChosen.url.trim().startsWith('mailto:')) {
            expect(action?.kind).toBe('mailto');
          } else {
            expect(action?.kind).toBe('internal');
          }
        }),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\home\select-hero-action.test.ts" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\home\select-hero-action.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/select-hero-action.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.4, Req 3.5

---

### M5.G3.T10: Checkpoint — Skill Derivation and Hero Action Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across skill derivation and hero action helper modules.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs all skill and hero action test suites with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M5.G3.T1 through M5.G3.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

npm run typecheck
npm run lint
npm run test -- tests/home/derive-skill-groups.test.ts tests/home/select-hero-action.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/derive-skill-groups.test.ts tests/home/select-hero-action.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 16.6

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\lib\home\derive-skill-groups.ts"
Test-Path "src\lib\home\select-hero-action.ts"
Test-Path "tests\home\derive-skill-groups.test.ts"
Test-Path "tests\home\select-hero-action.test.ts"
npm run typecheck
npm run test -- tests/home/derive-skill-groups.test.ts tests/home/select-hero-action.test.ts
```
Expected output:
- `True` for all 4 paths
- `npm run typecheck` exits with return code 0
- Vitest executes all skill derivation and hero action tests with return code 0.