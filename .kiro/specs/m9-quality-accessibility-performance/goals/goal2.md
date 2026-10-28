# M9.G2: JSON-LD Builders, Serializer, and JsonLd Component

> **Milestone:** M9 — Quality, Accessibility & Performance  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

---

## Goal Objective

Implement the pure schema.org JSON-LD structured data subsystem in `src/lib/structured-data/` and the server component `JsonLd` in `src/components/structured-data/json-ld.tsx`. This goal provides pure builder functions for `Person`, `Article`, and `BreadcrumbList`, a secure serializer that sanitizes markup boundary characters (`<`, U+2028, U+2029), and exhaustive test coverage validating round-trip deserialization, markup injection immunity, accurate field derivation, clean omission of null/empty values, and zero input mutations (fast-check Properties 1 through 5). No page templates are modified in this goal.

---

## Goal Success Criteria

- ✓ `src/lib/structured-data/types.ts` exports `JsonLdObject`, `BreadcrumbItem`, and `Pick`-narrowed source contracts derived directly from M2 content types without type duplication
- ✓ `src/lib/structured-data/serialize.ts` exports `serializeJsonLd` replacing `<` with `\u003c`, U+2028 with `\u2028`, and U+2029 with `\u2029`
- ✓ `src/lib/structured-data/person.ts` exports `buildPersonJsonLd` deriving `@type: 'Person'` from profile and social link fields
- ✓ `src/lib/structured-data/article.ts` exports `buildArticleJsonLd` deriving `@type: 'Article'` with `dateModified` included only when `updatedAt` is present
- ✓ `src/lib/structured-data/breadcrumb.ts` exports `buildBreadcrumbJsonLd` generating 1-based sequential `ListItem` elements
- ✓ `src/components/structured-data/json-ld.tsx` is a lightweight React Server Component rendering `<script type="application/ld+json">` without client runtime directives
- ✓ Fast-check Properties 1, 2, 3, 4, and 5 pass $\ge 100$ iterations each
- ✓ Zero imports of `react`, `next`, or `document` exist inside `src/lib/structured-data/`
- ✓ Zero page files (`src/app/page.tsx`, etc.) are modified in this goal

---

## Prerequisites

- Goal M9.G1 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Canonical content contracts available in `src/types/content.ts`

---

## Tasks

### M9.G2.T1: Create JSON-LD Domain Types and Source Contracts

**Objective:** Define the generic schema.org JSON-LD data structures and narrowly scoped input types derived directly from `src/types/content.ts` using TypeScript's `Pick`.

**Acceptance Criteria:**
- ✓ `src/lib/structured-data/types.ts` exports `JsonLdValue`, `JsonLdObject`, `BreadcrumbItem`, `PersonSource`, and `ArticleSource`
- ✓ Uses `import type` to reference `SiteConfig`, `SiteProfile`, and `BlogPost` without type redefinition
- ✓ Zero use of `any`, `unknown`, or non-null assertions
- ✓ File length is under 100 lines and contains no runtime code

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- File `src/types/content.ts` exists

**Implementation Details:**

1. Create directory `src/lib/structured-data/` if missing.
2. Create `src/lib/structured-data/types.ts`:

```typescript
import type { SiteConfig, SiteProfile, BlogPost } from '@/types/content';

export type JsonLdPrimitive = string | number | boolean | null;

export type JsonLdValue =
  | JsonLdPrimitive
  | JsonLdObject
  | readonly JsonLdValue[];

export interface JsonLdObject {
  readonly [key: string]: JsonLdValue;
}

export type PersonSource = Pick<SiteConfig, 'siteUrl' | 'socialLinks'> & {
  readonly profile: Pick<SiteProfile, 'name' | 'professionalTitle'>;
};

export type ArticleSource = Pick<
  BlogPost,
  'title' | 'slug' | 'summary' | 'publishedAt' | 'updatedAt' | 'tags'
>;

export interface BreadcrumbItem {
  readonly name: string;
  readonly path: string;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/structured-data/types.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.9, Req 18.4

---

### M9.G2.T2: Implement Secure JSON-LD Serializer

**Objective:** Implement `serializeJsonLd` to serialize structured data objects to JSON while escaping markup boundary characters (`<`, U+2028, U+2029) to prevent HTML script break-out.

**Acceptance Criteria:**
- ✓ Replaces every `<` with `\u003c`
- ✓ Replaces U+2028 with `\u2028` and U+2029 with `\u2029`
- ✓ Standard `JSON.parse` evaluates the serialized output back to the original object
- ✓ Output is strictly valid JSON with no HTML tags or closing script sequences

**Prerequisites:**
- M9.G2.T1 completed
- Target file: `src/lib/structured-data/serialize.ts`

**Implementation Details:**

Create `src/lib/structured-data/serialize.ts`:

```typescript
import type { JsonLdObject } from './types';

/**
 * Serializes a JSON-LD object to a JSON string safe for embedding in HTML <script> tags.
 * Escapes '<' to '\u003c' to prevent premature closing of </script> or opening of <!-- comments.
 * Escapes U+2028 and U+2029 line separators for strict JavaScript evaluation compliance.
 */
export function serializeJsonLd(value: JsonLdObject): string {
  const rawJson = JSON.stringify(value);
  return rawJson
    .replace(/</g, '\\u003c')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/structured-data/serialize.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.6, Req 9.7

---

### M9.G2.T3: Implement Shared Normalization Helpers and Person JSON-LD Builder

**Objective:** Implement internal string cleaning utilities (`normalizeSiteUrl`, `omitEmpty`) and construct `buildPersonJsonLd` to generate schema.org `Person` metadata.

**Acceptance Criteria:**
- ✓ `normalizeSiteUrl` strips trailing slashes while preserving root origin
- ✓ `buildPersonJsonLd` emits `@context: 'https://schema.org'` and `@type: 'Person'`
- ✓ Correctly maps `name`, `jobTitle`, `url`, and `sameAs`
- ✓ Omits `sameAs` if social links array is empty or contains only whitespace
- ✓ Does not mutate input source objects

**Prerequisites:**
- M9.G2.T1 completed
- Target file: `src/lib/structured-data/person.ts`

**Implementation Details:**

Create `src/lib/structured-data/person.ts`:

```typescript
import type { JsonLdObject, PersonSource } from './types';

export function normalizeSiteUrl(url: string): string {
  const trimmed = url.trim();
  if (trimmed === '') {
    return '';
  }
  return trimmed.replace(/\/+$/, '');
}

export function cleanString(val: string | null | undefined): string | null {
  if (val === null || val === undefined) {
    return null;
  }
  const trimmed = val.trim();
  return trimmed === '' ? null : trimmed;
}

export function buildPersonJsonLd(site: PersonSource): JsonLdObject {
  const name = cleanString(site.profile.name);
  const jobTitle = cleanString(site.profile.professionalTitle);
  const normalizedUrl = normalizeSiteUrl(site.siteUrl);

  const sameAs = site.socialLinks
    .map(link => cleanString(link.url))
    .filter((url): url is string => url !== null);

  const result: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Person',
  };

  if (name !== null) {
    result.name = name;
  }
  if (jobTitle !== null) {
    result.jobTitle = jobTitle;
  }
  if (normalizedUrl !== '') {
    result.url = normalizedUrl;
  }
  if (sameAs.length > 0) {
    result.sameAs = sameAs;
  }

  return result as JsonLdObject;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/structured-data/person.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.2, Req 9.5, Req 9.8

---

### M9.G2.T4: Implement Article JSON-LD Builder

**Objective:** Implement `buildArticleJsonLd` to construct schema.org `Article` metadata for blog detail pages.

**Acceptance Criteria:**
- ✓ Emits `@context: 'https://schema.org'` and `@type: 'Article'`
- ✓ Maps `headline`, `description`, `datePublished`, `url`, `author`, and `keywords`
- ✓ Includes `dateModified` if and only if `updatedAt` is non-null and non-empty
- ✓ Omits `keywords` if tags array is empty
- ✓ Author is structured as `@type: 'Person'` using author profile details

**Prerequisites:**
- M9.G2.T3 completed
- Target file: `src/lib/structured-data/article.ts`

**Implementation Details:**

Create `src/lib/structured-data/article.ts`:

```typescript
import type { JsonLdObject, ArticleSource, PersonSource } from './types';
import { cleanString, normalizeSiteUrl } from './person';

export function buildArticleJsonLd(post: ArticleSource, site: PersonSource): JsonLdObject {
  const headline = cleanString(post.title);
  const description = cleanString(post.summary);
  const datePublished = cleanString(post.publishedAt);
  const dateModified = cleanString(post.updatedAt);
  const baseUrl = normalizeSiteUrl(site.siteUrl);
  const slug = cleanString(post.slug);

  const authorName = cleanString(site.profile.name);
  const authorUrl = baseUrl !== '' ? baseUrl : null;

  const validTags = post.tags
    .map(t => cleanString(t))
    .filter((t): t is string => t !== null);

  const result: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Article',
  };

  if (headline !== null) {
    result.headline = headline;
  }
  if (description !== null) {
    result.description = description;
  }
  if (datePublished !== null) {
    result.datePublished = datePublished;
  }
  if (dateModified !== null) {
    result.dateModified = dateModified;
  }
  if (baseUrl !== '' && slug !== null) {
    result.url = `${baseUrl}/blog/${slug}`;
  }

  if (authorName !== null) {
    const author: Record<string, unknown> = {
      '@type': 'Person',
      name: authorName,
    };
    if (authorUrl !== null) {
      author.url = authorUrl;
    }
    result.author = author;
  }

  if (validTags.length > 0) {
    result.keywords = validTags.join(', ');
  }

  return result as JsonLdObject;
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/structured-data/article.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.3, Req 9.5, Req 9.8

---

### M9.G2.T5: Implement BreadcrumbList JSON-LD Builder

**Objective:** Implement `buildBreadcrumbJsonLd` to construct schema.org `BreadcrumbList` metadata for project and blog pages.

**Acceptance Criteria:**
- ✓ Emits `@context: 'https://schema.org'` and `@type: 'BreadcrumbList'`
- ✓ Generates contiguous 1-based `position` sequence in `itemListElement`
- ✓ Prepends normalized `siteUrl` to root-relative paths
- ✓ Silently drops empty or whitespace-only breadcrumb items before assigning positions
- ✓ Returns an empty `itemListElement` array if no valid items remain

**Prerequisites:**
- M9.G2.T3 completed
- Target file: `src/lib/structured-data/breadcrumb.ts`

**Implementation Details:**

Create `src/lib/structured-data/breadcrumb.ts`:

```typescript
import type { JsonLdObject, BreadcrumbItem } from './types';
import { cleanString, normalizeSiteUrl } from './person';

export function buildBreadcrumbJsonLd(
  items: readonly BreadcrumbItem[],
  site: { readonly siteUrl: string }
): JsonLdObject {
  const baseUrl = normalizeSiteUrl(site.siteUrl);

  const validItems = items
    .map(item => ({
      name: cleanString(item.name),
      path: cleanString(item.path),
    }))
    .filter((item): item is { name: string; path: string } => item.name !== null && item.path !== null);

  const itemListElement = validItems.map((item, index) => {
    const fullPath = item.path.startsWith('/') ? item.path : `/${item.path}`;
    const itemUrl = baseUrl !== '' ? `${baseUrl}${fullPath}` : fullPath;

    return {
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: itemUrl,
    };
  });

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement,
  };
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/structured-data/breadcrumb.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.1, Req 9.4, Req 9.5, Req 9.8

---

### M9.G2.T6: Create JsonLd Server Component

**Objective:** Create the standalone React Server Component `JsonLd` to render serialized JSON-LD within `<script type="application/ld+json">`.

**Acceptance Criteria:**
- ✓ `src/components/structured-data/json-ld.tsx` exports `JsonLd`
- ✓ Contains zero `'use client'` directive
- ✓ Emits `<script type="application/ld+json">` with inner HTML set to `serializeJsonLd(data)`
- ✓ Component test confirms correct rendering and HTML escaping

**Prerequisites:**
- M9.G2.T2 completed
- Target files: `src/components/structured-data/json-ld.tsx`, `tests/audit/structured-data/json-ld-component.test.tsx`

**Implementation Details:**

1. Create directory `src/components/structured-data/` if missing.
2. Create `src/components/structured-data/json-ld.tsx`:

```tsx
import { serializeJsonLd } from '@/lib/structured-data/serialize';
import type { JsonLdObject } from '@/lib/structured-data/types';

export interface JsonLdProps {
  readonly data: JsonLdObject;
}

export function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: serializeJsonLd(data) }}
    />
  );
}
```

3. Create directory `tests/audit/structured-data/` if missing.
4. Create `tests/audit/structured-data/json-ld-component.test.tsx`:

```tsx
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import * as React from 'react';
import { JsonLd } from '@/components/structured-data/json-ld';

describe('JsonLd Server Component', () => {
  it('renders script tag with application/ld+json type and escaped content', () => {
    const data = {
      '@context': 'https://schema.org',
      '@type': 'Person',
      name: 'John <script>alert(1)</script> Doe',
    };

    const { container } = render(<JsonLd data={data} />);
    const script = container.querySelector('script[type="application/ld+json"]');

    expect(script).not.toBeNull();
    expect(script?.innerHTML).toContain('\\u003cscript>alert(1)\\u003c/script>');
    expect(script?.innerHTML).not.toContain('<script>');
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structured-data/json-ld-component.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 10.4, Req 18.4

---

### M9.G2.T7: Verify Properties 1 and 2 (Serialization Invariants)

**Objective:** Author unit tests and execute fast-check Property 1 (round-trip equality) and Property 2 (markup injection immunity) for `serializeJsonLd`.

**Acceptance Criteria:**
- ✓ Unit tests verify handling of `</script>`, `<!--`, U+2028, and U+2029
- ✓ Fast-check Property 1 confirms `JSON.parse(serializeJsonLd(x))` deep-equals `x` across $\ge 200$ runs
- ✓ Fast-check Property 2 confirms serialized string never contains raw `<`, U+2028, or U+2029

**Prerequisites:**
- M9.G2.T2 completed
- Target file: `tests/audit/structured-data/serialize.test.ts`

**Implementation Details:**

Create `tests/audit/structured-data/serialize.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { serializeJsonLd } from '@/lib/structured-data/serialize';
import type { JsonLdObject, JsonLdValue } from '@/lib/structured-data/types';

describe('JSON-LD Serializer Unit Tests', () => {
  it('escapes closing script tags', () => {
    const obj: JsonLdObject = {
      '@context': 'https://schema.org',
      description: '</script><script>alert(1)</script>',
    };
    const serialized = serializeJsonLd(obj);
    expect(serialized).not.toContain('</script>');
    expect(serialized).toContain('\\u003c/script>');
    expect(JSON.parse(serialized)).toEqual(obj);
  });

  it('escapes HTML comments and line separators', () => {
    const obj: JsonLdObject = {
      comment: '<!-- secret -->',
      lineSeparators: '\u2028 and \u2029',
    };
    const serialized = serializeJsonLd(obj);
    expect(serialized).not.toContain('<!--');
    expect(serialized).not.toContain('\u2028');
    expect(serialized).not.toContain('\u2029');
    expect(JSON.parse(serialized)).toEqual(obj);
  });
});

describe('JSON-LD Serializer Properties', () => {
  // Define recursive arbitrary for JsonLdObject
  const jsonLdValueArbitrary: fc.Memo<JsonLdValue> = fc.memo(n => {
    if (n <= 0) {
      return fc.oneof(
        fc.string(),
        fc.integer(),
        fc.double({ noNaN: true }),
        fc.boolean(),
        fc.constant(null)
      );
    }
    return fc.oneof(
      fc.string(),
      fc.integer(),
      fc.double({ noNaN: true }),
      fc.boolean(),
      fc.constant(null),
      fc.array(jsonLdValueArbitrary(n - 1), { maxLength: 3 }),
      fc.dictionary(fc.string({ minLength: 1, maxLength: 10 }), jsonLdValueArbitrary(n - 1), {
        maxKeys: 3,
      }) as fc.Arbitrary<JsonLdObject>
    );
  });

  const jsonLdObjectArbitrary = fc.dictionary(
    fc.string({ minLength: 1, maxLength: 10 }),
    jsonLdValueArbitrary(2),
    { maxKeys: 5 }
  ) as fc.Arbitrary<JsonLdObject>;

  // Feature: m9-quality-accessibility-performance, Property 1: JSON-LD serialization round trip
  it('Property 1: JSON-LD serialization round trip', () => {
    fc.assert(
      fc.property(jsonLdObjectArbitrary, obj => {
        const serialized = serializeJsonLd(obj);
        const parsed = JSON.parse(serialized);
        expect(parsed).toEqual(obj);
      }),
      { numRuns: 200 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 2: Serialized JSON-LD cannot close or open markup
  it('Property 2: Serialized JSON-LD cannot close or open markup', () => {
    const dangerousStringArbitrary = fc.oneof(
      fc.string(),
      fc.constant('</script><script>alert("xss")</script>'),
      fc.constant('<!-- HTML comment -->'),
      fc.constant('text with \u2028 and \u2029 chars'),
      fc.constant('<<<>>>')
    );

    fc.assert(
      fc.property(
        fc.dictionary(fc.string({ minLength: 1, maxLength: 8 }), dangerousStringArbitrary),
        rawObj => {
          const serialized = serializeJsonLd(rawObj as JsonLdObject);
          expect(serialized).not.toContain('<');
          expect(serialized).not.toContain('\u2028');
          expect(serialized).not.toContain('\u2029');
          expect(serialized.toLowerCase()).not.toContain('</script');
        }
      ),
      { numRuns: 200 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structured-data/serialize.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.6, Req 9.7

---

### M9.G2.T8: Verify Properties 3 and 4 (Builder Derivation and Omission)

**Objective:** Author unit tests and execute fast-check Property 3 (field derivation) and Property 4 (null and empty value omission) for all JSON-LD builders.

**Acceptance Criteria:**
- ✓ Unit tests verify field mappings for `Person`, `Article`, and `BreadcrumbList`
- ✓ Fast-check Property 3 confirms correct derivation of required fields across $\ge 100$ runs
- ✓ Fast-check Property 4 confirms total absence of placeholder strings (`"null"`, `"undefined"`, `"N/A"`, `"TBD"`) when optional fields are empty or null across $\ge 100$ runs

**Prerequisites:**
- M9.G2.T3, M9.G2.T4, M9.G2.T5 completed
- Target file: `tests/audit/structured-data/builders.test.ts`

**Implementation Details:**

Create `tests/audit/structured-data/builders.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { buildPersonJsonLd } from '@/lib/structured-data/person';
import { buildArticleJsonLd } from '@/lib/structured-data/article';
import { buildBreadcrumbJsonLd } from '@/lib/structured-data/breadcrumb';
import type { PersonSource, ArticleSource, BreadcrumbItem } from '@/lib/structured-data/types';

describe('JSON-LD Builders Unit Tests', () => {
  const dummySite: PersonSource = {
    siteUrl: 'https://angeloandres.com/',
    profile: {
      name: 'Angelo Andres',
      professionalTitle: 'Lead Systems Architect',
    },
    socialLinks: [
      { label: 'GitHub', url: 'https://github.com/example' },
      { label: 'LinkedIn', url: 'https://linkedin.com/in/example' },
    ],
  };

  it('buildPersonJsonLd derives all valid fields', () => {
    const result = buildPersonJsonLd(dummySite);
    expect(result['@type']).toBe('Person');
    expect(result.name).toBe('Angelo Andres');
    expect(result.jobTitle).toBe('Lead Systems Architect');
    expect(result.url).toBe('https://angeloandres.com');
    expect(result.sameAs).toEqual([
      'https://github.com/example',
      'https://linkedin.com/in/example',
    ]);
  });

  it('buildArticleJsonLd includes dateModified only when updatedAt is present', () => {
    const postWithUpdate: ArticleSource = {
      title: 'Architecting Pipelines',
      slug: 'architecting-pipelines',
      summary: 'A deep dive into deterministic pipelines.',
      publishedAt: '2026-04-01',
      updatedAt: '2026-04-10',
      tags: ['AI', 'Pipelines'],
    };

    const resWithUpdate = buildArticleJsonLd(postWithUpdate, dummySite);
    expect(resWithUpdate.dateModified).toBe('2026-04-10');

    const postWithoutUpdate: ArticleSource = {
      ...postWithUpdate,
      updatedAt: null,
    };
    const resWithoutUpdate = buildArticleJsonLd(postWithoutUpdate, dummySite);
    expect('dateModified' in resWithoutUpdate).toBe(false);
  });

  it('buildBreadcrumbJsonLd generates contiguous 1-based positions', () => {
    const items: BreadcrumbItem[] = [
      { name: 'Home', path: '/' },
      { name: 'Projects', path: '/projects' },
      { name: 'AI Platform', path: '/projects/ai-platform' },
    ];
    const res = buildBreadcrumbJsonLd(items, { siteUrl: 'https://angeloandres.com' });
    const list = res.itemListElement as Array<{ position: number; name: string; item: string }>;

    expect(list).toHaveLength(3);
    expect(list[0]?.position).toBe(1);
    expect(list[0]?.item).toBe('https://angeloandres.com/');
    expect(list[1]?.position).toBe(2);
    expect(list[1]?.item).toBe('https://angeloandres.com/projects');
    expect(list[2]?.position).toBe(3);
    expect(list[2]?.item).toBe('https://angeloandres.com/projects/ai-platform');
  });
});

describe('JSON-LD Builders Properties', () => {
  const nonEmptyString = fc.stringMatching(/^[a-zA-Z0-9_\- ]+$/).filter(s => s.trim().length > 0);

  // Feature: m9-quality-accessibility-performance, Property 3: Builders derive their required fields from the source
  it('Property 3: Builders derive their required fields from the source', () => {
    fc.assert(
      fc.property(
        nonEmptyString,
        nonEmptyString,
        fc.webUrl(),
        (name, title, siteUrl) => {
          const site: PersonSource = {
            siteUrl,
            profile: { name, professionalTitle: title },
            socialLinks: [],
          };
          const person = buildPersonJsonLd(site);
          expect(person['@context']).toBe('https://schema.org');
          expect(person['@type']).toBe('Person');
          expect(person.name).toBe(name.trim());
          expect(person.jobTitle).toBe(title.trim());
          expect(person.url).toBe(siteUrl.replace(/\/+$/, ''));
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: m9-quality-accessibility-performance, Property 4: Builders omit null and empty values
  it('Property 4: Builders omit null and empty values', () => {
    const emptyString = fc.constantFrom('', '   ', '\t\n');
    fc.assert(
      fc.property(emptyString, emptyVal => {
        const site: PersonSource = {
          siteUrl: 'https://example.com',
          profile: { name: 'Valid Name', professionalTitle: emptyVal },
          socialLinks: [{ label: 'test', url: emptyVal }],
        };
        const person = buildPersonJsonLd(site);

        expect('jobTitle' in person).toBe(false);
        expect('sameAs' in person).toBe(false);

        const serialized = JSON.stringify(person);
        expect(serialized).not.toContain('"null"');
        expect(serialized).not.toContain('"undefined"');
        expect(serialized).not.toContain('"N/A"');
        expect(serialized).not.toContain('"TBD"');
      }),
      { numRuns: 100 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structured-data/builders.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.2, Req 9.3, Req 9.4, Req 9.5

---

### M9.G2.T9: Verify Property 5 (Immutability) and Module Purity

**Objective:** Verify fast-check Property 5 (builders do not mutate input data) and assert complete absence of `react`, `next`, or `document` imports in `src/lib/structured-data/`.

**Acceptance Criteria:**
- ✓ Fast-check Property 5 asserts inputs are deeply identical before and after builder execution
- ✓ Inputs are tested with `Object.freeze` to confirm runtime immutability
- ✓ `tests/audit/structured-data/purity.test.ts` scans all `.ts` files under `src/lib/structured-data/`
- ✓ Asserts zero imports of `react`, `next`, or global DOM symbols

**Prerequisites:**
- M9.G2.T3, M9.G2.T4, M9.G2.T5 completed
- Target file: `tests/audit/structured-data/purity.test.ts`

**Implementation Details:**

Create `tests/audit/structured-data/purity.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { buildPersonJsonLd } from '@/lib/structured-data/person';
import { buildArticleJsonLd } from '@/lib/structured-data/article';
import { buildBreadcrumbJsonLd } from '@/lib/structured-data/breadcrumb';
import type { PersonSource, ArticleSource, BreadcrumbItem } from '@/lib/structured-data/types';

describe('Structured Data Module Purity Tests', () => {
  it('does not import react, next, or reference document in src/lib/structured-data/', async () => {
    const dir = path.join(process.cwd(), 'src', 'lib', 'structured-data');
    const files = await fs.readdir(dir);

    for (const file of files) {
      if (file.endsWith('.ts')) {
        const content = await fs.readFile(path.join(dir, file), 'utf8');
        expect(content).not.toMatch(/from\s+['"]react['"]/);
        expect(content).not.toMatch(/from\s+['"]next['"]/);
        expect(content).not.toMatch(/\bdocument\./);
        expect(content).not.toMatch(/\bwindow\./);
      }
    }
  });

  // Feature: m9-quality-accessibility-performance, Property 5: Builders do not mutate their inputs
  it('Property 5: Builders do not mutate their inputs', () => {
    fc.assert(
      fc.property(
        fc.record({
          name: fc.string(),
          title: fc.string(),
          siteUrl: fc.string(),
          slug: fc.string(),
          summary: fc.string(),
        }),
        data => {
          const site: PersonSource = {
            siteUrl: data.siteUrl,
            profile: { name: data.name, professionalTitle: data.title },
            socialLinks: [{ label: 'github', url: 'https://github.com' }],
          };

          const post: ArticleSource = {
            title: data.name,
            slug: data.slug,
            summary: data.summary,
            publishedAt: '2026-01-01',
            updatedAt: null,
            tags: ['tag1', 'tag2'],
          };

          const breadcrumbs: BreadcrumbItem[] = [
            { name: 'Home', path: '/' },
            { name: data.name, path: `/${data.slug}` },
          ];

          // Take deep snapshot
          const siteClone = JSON.parse(JSON.stringify(site));
          const postClone = JSON.parse(JSON.stringify(post));
          const breadcrumbsClone = JSON.parse(JSON.stringify(breadcrumbs));

          // Run builders
          buildPersonJsonLd(site);
          buildArticleJsonLd(post, site);
          buildBreadcrumbJsonLd(breadcrumbs, site);

          // Assert complete equality post-execution
          expect(site).toEqual(siteClone);
          expect(post).toEqual(postClone);
          expect(breadcrumbs).toEqual(breadcrumbsClone);
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structured-data/purity.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.8, Req 9.9, Req 18.4

---

### M9.G2.T10: Milestone 9 Goal 2 Checkpoint Verification

**Objective:** Execute the entire test suite for Goal 2, verify TypeScript compilation and lint compliance, and confirm that zero pages in `src/app/` were modified.

**Acceptance Criteria:**
- ✓ All tests under `tests/audit/structured-data/` pass cleanly
- ✓ Properties 1 through 5 pass $\ge 100$ iterations
- ✓ `npm run typecheck` exits 0 with zero errors
- ✓ `npm run lint` exits 0 with zero errors
- ✓ `git status` verifies no modifications inside `src/app/`

**Prerequisites:**
- M9.G2.T1 through M9.G2.T9 completed

**Implementation Details:**

Run checkpoint validation script via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Run structured data test suite
npx vitest run tests/audit/structured-data/
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Run static type checking
npm run typecheck
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. Run ESLint
npm run lint
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Verify no modifications to src/app
$appDiff = git status --porcelain src/app
if ($appDiff.Length -gt 0) {
    Write-Error "Unapproved modification to src/app detected: $appDiff"
    exit 1
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$appDiff = git status --porcelain src/app
if ($appDiff.Length -eq 0) { "PASS" } else { "FAIL" }
```
Expected: `PASS`

**Satisfies Requirements:** Req 9.1–9.9, Req 10.5, Req 18.5, Req 18.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/audit/structured-data/
npm run typecheck
npm run lint
```
Expected output:
- All Vitest tests in `tests/audit/structured-data/` pass (including Properties 1, 2, 3, 4, and 5)
- `tsc --noEmit` exits with 0
- ESLint reports 0 warnings and 0 errors.