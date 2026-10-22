# Requirements Document

> **Spec:** M7 Certifications Module  
> **Document Status:** Draft  
> **Feature Name:** m7-certifications-module  
> **Milestone:** M7  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 3, 4.2, 5.1, 5.3, 6.1, 6.2), `PRD.md` (Certifications & Badges, P0), `design.md` (Sections 4.3, 6.3), `TRD.md` (static generation), `APP_FLOW.md` (Flow 3.0, Story 3.1, `SCR-04`), `implementation_plan.md` (Certifications tasks)  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 7 (M7) implements the Certifications module for `personal-website-portfolio-v2`: the single static route `src/app/certifications/page.tsx` (`SCR-04`), the components in `src/components/certifications/`, and the pure helpers in `src/lib/certifications/` that group, order, and classify certifications.

M7 reads certifications through `getCertifications()` and renders optional supporting content through `renderMarkdown`, both from the M2 loaders. M7 composes the M3 UI_Primitives (`Card`, `Tag`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`, `FOCUS_RING`) and the M4 shell (`main#main-content`, title template, `not-found`). M7 follows the M5 and M6 pure-helper pattern and reuses the M5 `formatDisplayDate` (`src/lib/format-date.ts`) and `compareStrings` (`src/lib/home/compare.ts`) read-only. M7 does not modify any M1 to M6 module.

`AGENTS.md` Section 3 defines no certification detail route. M7 therefore ships one index page only. `AGENTS.md` 4.2 makes `category` a required `CertificationCategory` value, so every certification belongs to a known category. The default "Uncategorised" group in `APP_FLOW.md` Flow 3.0 step 3.2 is a defensive fallback that the design document must reconcile with the schema.

The page is statically generated and ships no client JavaScript. M7 adds no `'use client'` component and no `Suspense` island, because certifications have no interactive state in P0.

M7 does NOT implement blog routes (M8), certification detail routes, search or filtering of certifications (P1), JSON-LD (M9), performance tuning or deployment (M9, M10), dark mode, API routes, analytics, forms, or new dependencies.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Certifications_Index** | The route `/certifications` rendered by `src/app/certifications/page.tsx` (`SCR-04`). |
| **Certification_Component** | A component in `src/components/certifications/`. |
| **CertificationsIndex** | Certification_Component that composes the page `h1` and the CertificationCategorySections, or the `EmptyState`. |
| **CertificationCategorySection** | Certification_Component rendering one `h2` category heading and a responsive grid of CertificationCards. |
| **CertificationCard** | Certification_Component rendering one certification using the M3 `Card`. |
| **VerificationLink** | Certification_Component rendering the issuer verification action through the M3 `ExternalLink`. |
| **BadgeImage** | The badge picture of a certification, rendered from `badgeImageUrl` and `badgeImageAlt`. |
| **Certification_Helper** | A pure function in `src/lib/certifications/`: `groupCertificationsByCategory`, `getCertificationStatus`, `getCategoryLabel`. |
| **CertificationGroup** | A pair of one `CertificationCategory` and the non-empty ordered list of `Certification` entries in that category. |
| **Category_Order** | The order of the `CertificationCategory` union in `AGENTS.md` 4.2: `cloud`, `ai`, `security`, `frontend`, `backend`, `data`, `devops`, `professional`. |
| **Certification_Order** | Within a CertificationGroup: `displayOrder` ascending, then `slug` ascending using `compareStrings`. |
| **Category_Label** | The human-readable text for a `CertificationCategory`, defined once in `src/lib/certifications/`. |
| **Build_Date** | The single `IsoDateString` captured once per build and passed as an argument to Certification_Helpers. The design document selects its source. |
| **Certification_Status** | The value `expired` when `expiresAt` is not `null` and is earlier than the Build_Date, and `active` otherwise. |
| **Expired_Indicator** | A visible text label "Expired" plus an icon or border cue, so status does not rely on color alone. |
| **Date_Formatter** | The deterministic M5 function `formatDisplayDate` that converts an `IsoDateString` to display text without reading the system locale or time zone. |
| **Supporting_Content** | The Markdown body of a certification (`Certification.content`) rendered through `renderMarkdown` and `MarkdownDoc`. |
| **Section_Heading** | An `h2` element that titles a page section. |
| **UI_Primitive** | A reusable M3 component in `src/components/ui/`. |
| **Semantic_Token** | A named design value from `design.md` Section 3, exposed by M1 through Tailwind and CSS custom properties. |
| **Hardcoded_Design_Value** | A raw hex color, arbitrary pixel size, arbitrary shadow, or arbitrary duration written directly in a component. |
| **Breakpoints** | Mobile `375px–767px`, Tablet `768px–1023px`, Desktop `1024px–1439px`, Wide Desktop `1440px+` (`design.md` 5.1). |
| **Axe_Check** | An automated accessibility test run against rendered components using an axe-core based tool. |
| **Property_Test** | A fast-check test asserting a helper property over generated inputs. |

---

## Requirements

---

### Requirement 1: Certifications Index Route and Composition

**User Story:**
As a recruiter, I want a certifications page, so that I can review all of Angelo's published credentials in one place.

#### Acceptance Criteria

1. THE Certifications_Index SHALL be served at `/certifications` by `src/app/certifications/page.tsx` as a static server component with no dynamic route segment.
2. THE Certifications_Index SHALL obtain certifications by calling `getCertifications()` from the M2 loader module and SHALL pass the result to Certification_Components through props typed with types imported from the M2 schemas.
3. THE Certifications_Index SHALL render exactly one `h1` containing the text "Certifications" inside the M4 Main_Landmark.
4. THE Certifications_Index SHALL render no `header`, `footer`, or `main` element, because the M4 Root_Layout owns those landmarks.
5. THE M7 implementation SHALL import `Certification`, `CertificationFrontmatter`, and `CertificationCategory` from the M2 schemas and SHALL NOT redeclare them (`AGENTS.md` 6.3).
6. THE Certifications_Index SHALL read no data from the network at render time.
7. THE M7 implementation SHALL create no file under `src/app/certifications/[slug]/`.

#### Verification Steps

1. Render the Certifications_Index with three fixture certifications; assert one `h1` named "Certifications" and three certification cards.
2. Assert `src/app/certifications/page.tsx` contains no `'use client'` directive and no `fetch(` call.
3. Assert the directory `src/app/certifications/` contains `page.tsx` and no dynamic segment folder.
4. Assert no file in `src/components/certifications/` or `src/lib/certifications/` declares `interface Certification` or `type CertificationCategory`.

---

### Requirement 2: Empty State

**User Story:**
As a visitor, I want a clear message when no certifications are published, so that the page does not look broken.

#### Acceptance Criteria

1. WHERE `getCertifications()` returns zero certifications, THE Certifications_Index SHALL render the M3 `EmptyState` with a message that certifications are being prepared (`APP_FLOW.md` Flow 3.0 step 3.1).
2. WHERE `getCertifications()` returns zero certifications, THE Certifications_Index SHALL render no CertificationCategorySection and no CertificationCard.
3. WHERE `getCertifications()` returns zero certifications, THE Certifications_Index SHALL still render the page `h1`.
4. THE Certifications_Index SHALL render no placeholder, sample, or fabricated certification in any state (`design.md` Section 8, `AGENTS.md` 6.1).

#### Verification Steps

1. Render with an empty array; assert the `EmptyState` message, the `h1`, and zero `h2` or card elements.
2. Render with one fixture; assert the `EmptyState` is absent.
3. Run an Axe_Check on the empty state and assert zero violations.

---

### Requirement 3: Category Grouping and Ordering Helper

**User Story:**
As a recruiter, I want certifications grouped by category in a stable order, so that I can scan related credentials together.

#### Acceptance Criteria

1. WHEN `groupCertificationsByCategory` receives a list of certifications, THE Certification_Helper SHALL return one CertificationGroup for each category held by at least one input certification and no group for any other category.
2. THE Certification_Helper SHALL order the returned CertificationGroups by Category_Order.
3. THE Certification_Helper SHALL order the certifications inside each CertificationGroup by Certification_Order.
4. THE Certification_Helper SHALL place every input certification in exactly one CertificationGroup, and the total count of certifications across all groups SHALL equal the input length.
5. THE Certification_Helper SHALL place each certification in the group whose category equals the certification `category`.
6. THE Certification_Helper SHALL return the same output for the same input regardless of the input order.
7. THE Certification_Helper SHALL return the same output when applied to its own flattened output (idempotence).
8. WHEN `groupCertificationsByCategory` receives an empty list, THE Certification_Helper SHALL return an empty list.
9. THE Certification_Helper SHALL leave the input array and its elements unmodified.
10. THE Certification_Helper SHALL perform no I/O and SHALL NOT read the system clock, locale, or time zone.

#### Verification Steps

1. Property_Test: for generated certification lists, assert the flattened group output is a permutation of the input (partition, no loss, no duplication).
2. Property_Test: assert group order follows Category_Order and member order follows Certification_Order.
3. Property_Test: assert the output is identical for a shuffled copy of the input.
4. Property_Test: assert `flatten(groupCertificationsByCategory(flatten(g)))` equals `g`.
5. Assert a deep-frozen input does not throw and is unchanged.

---

### Requirement 4: Uncategorised Fallback Reconciliation

**User Story:**
As a maintainer, I want the specified fallback group handled consistently with the schema, so that the page cannot silently drop an entry.

#### Acceptance Criteria

1. THE M7 implementation SHALL treat `category` as required, in line with `AGENTS.md` 5.3.
2. IF a certification reaches `groupCertificationsByCategory` with a `category` value outside Category_Order, THEN THE Certification_Helper SHALL place that certification in a final CertificationGroup labelled "Uncategorised" and SHALL NOT discard it.
3. WHERE every certification has a category inside Category_Order, THE Certifications_Index SHALL render no "Uncategorised" heading.
4. THE Certification_Helper SHALL order the "Uncategorised" CertificationGroup after all CertificationGroups in Category_Order, with members in Certification_Order.

#### Verification Steps

1. Call the helper with a fixture whose category is cast through a test-only unknown value; assert one trailing "Uncategorised" group holding the entry.
2. Render a fixture set with valid categories only; assert no heading containing "Uncategorised".
3. Property_Test: for inputs that include out-of-range categories, assert no entry is lost.

---

### Requirement 5: Category Sections

**User Story:**
As a visitor, I want each category to have its own headed section, so that I can navigate the page by heading.

#### Acceptance Criteria

1. THE CertificationsIndex SHALL render one CertificationCategorySection for each CertificationGroup, in the order returned by `groupCertificationsByCategory`.
2. THE CertificationCategorySection SHALL render the Category_Label as an `h2` Section_Heading.
3. THE CertificationCategorySection SHALL render its CertificationCards in a list structure (`ul` with `li` children) in Certification_Order.
4. THE CertificationCategorySection SHALL associate its list with its heading through `aria-labelledby` referencing a unique heading `id` derived from the category.
5. THE Certification_Helper `getCategoryLabel` SHALL return a non-empty Category_Label for each of the 8 `CertificationCategory` values.
6. THE CertificationsIndex SHALL render the headings in the order `h1`, then `h2` per section, then `h3` per card, with no skipped level.

#### Verification Steps

1. Render fixtures across three categories; assert three `h2` elements in Category_Order with correct Category_Labels.
2. Assert each `section` has an accessible name equal to its `h2` text and each list contains the expected number of `li` elements.
3. Assert the heading outline contains no level skip.
4. Assert `getCategoryLabel` returns a distinct non-empty string for each category value.

---

### Requirement 6: Certification Card Content

**User Story:**
As a recruiter, I want each card to show the core credential facts, so that I can evaluate it at a glance.

#### Acceptance Criteria

1. THE CertificationCard SHALL render the certification `title` as an `h3` inside an M3 `Card`.
2. THE CertificationCard SHALL render the `issuer` text.
3. THE CertificationCard SHALL render the issue date as "Issued {date}" through the Date_Formatter inside a `time` element whose `datetime` attribute equals `issuedAt`.
4. WHEN `expiresAt` is not `null`, THE CertificationCard SHALL render "Expires {date}" through the Date_Formatter inside a `time` element whose `datetime` attribute equals `expiresAt`.
5. WHEN `expiresAt` is `null`, THE CertificationCard SHALL render no expiry text and no empty `time` element.
6. THE CertificationCard SHALL render the Category_Label through the M3 `Tag`.
7. WHEN `credentialId` is a non-empty string after trimming, THE CertificationCard SHALL render "Credential ID: {credentialId}" with the value exactly as stored.
8. WHEN `credentialId` is `null` or empty, THE CertificationCard SHALL render no credential label and no placeholder text.
9. THE CertificationCard SHALL derive every displayed value from the `Certification` prop and SHALL NOT invent an issuer, date, identifier, or link.

#### Verification Steps

1. Render a full fixture; assert the `h3`, issuer, "Issued" and "Expires" text, matching `datetime` values, the category tag, and the credential line.
2. Render a fixture with `expiresAt: null` and `credentialId: null`; assert no "Expires" text, no "Credential ID" text, and exactly one `time` element.
3. Render a fixture with a whitespace-only `credentialId`; assert no credential line.
4. Property_Test: for generated certifications, assert every text node in the card is traceable to a prop value or a fixed label.

---

### Requirement 7: Expired Status Indicator

**User Story:**
As a recruiter, I want expired credentials flagged, so that I do not mistake them for current ones.

#### Acceptance Criteria

1. WHEN `getCertificationStatus` receives a certification and a Build_Date, THE Certification_Helper SHALL return `expired` if `expiresAt` is not `null` and `expiresAt` is earlier than the Build_Date.
2. WHEN `getCertificationStatus` receives a certification whose `expiresAt` is `null`, THE Certification_Helper SHALL return `active`.
3. WHEN `expiresAt` equals the Build_Date, THE Certification_Helper SHALL return `active`.
4. THE Certification_Helper SHALL compare `IsoDateString` values without constructing a `Date` from the system clock and SHALL receive the Build_Date as an argument.
5. THE Certifications_Index SHALL compute the Build_Date once per render and SHALL pass the same value to every CertificationCard.
6. WHILE the Certification_Status of a certification is `expired`, THE CertificationCard SHALL render the Expired_Indicator containing the visible text "Expired".
7. WHILE the Certification_Status of a certification is `active`, THE CertificationCard SHALL render no Expired_Indicator.
8. THE Expired_Indicator SHALL convey status through text and a non-color cue in addition to any color.

#### Verification Steps

1. Unit-test `getCertificationStatus` for `expiresAt` one day before, equal to, and one day after the Build_Date, and for `null`.
2. Property_Test: for generated date pairs, assert the result is `expired` if and only if `expiresAt < buildDate`.
3. Render an expired fixture; assert the text "Expired" is present and an active fixture renders none.
4. Assert the Expired_Indicator remains distinguishable with all color styles removed.

---

### Requirement 8: Verification Link

**User Story:**
As a recruiter, I want a verification link on each credential, so that I can confirm it with the issuer.

#### Acceptance Criteria

1. WHEN `verificationUrl` is an absolute `https://` URL, THE VerificationLink SHALL render an M3 `ExternalLink` whose `href` equals `verificationUrl`.
2. THE VerificationLink SHALL set the accessible name to "Verify {title} credential", unique per certification.
3. THE VerificationLink SHALL open in a new browser tab with `target="_blank"` and `rel` containing `noopener` and `noreferrer` (`APP_FLOW.md` Flow 3.0 step 3.3).
4. THE VerificationLink SHALL be visually distinguished from non-link card text through an underline or an icon in addition to color (`design.md` 6.3).
5. WHEN `verificationUrl` is `null`, empty, or omitted, THE CertificationCard SHALL omit the VerificationLink and SHALL render no placeholder or disabled action.
6. IF `verificationUrl` does not begin with `https://`, THEN THE VerificationLink SHALL render no link.
7. THE VerificationLink SHALL provide a visible focus indicator through `FOCUS_RING`.
8. THE VerificationLink SHALL announce that it opens a new tab through screen-reader text or an equivalent accessible description.

#### Verification Steps

1. Render a fixture with a valid URL; assert one link named "Verify {title} credential" with matching `href`, `target`, and `rel`.
2. Render three fixtures with distinct titles; assert the three link names are distinct.
3. Render fixtures with `null`, `""`, and `"http://example.com"`; assert no link element in each case.
4. Assert the link class list includes the `FOCUS_RING` classes.

---

### Requirement 9: Badge Image Handling

**User Story:**
As a visitor, I want the badge shown with a text alternative, so that credentials are recognizable and accessible.

#### Acceptance Criteria

1. WHERE `badgeImageUrl` and `badgeImageAlt` are both non-empty, THE CertificationCard SHALL render the BadgeImage with `src` equal to `badgeImageUrl` and `alt` equal to `badgeImageAlt`.
2. WHERE `badgeImageUrl` is `null` or empty, THE CertificationCard SHALL render no image element and no empty image container.
3. IF `badgeImageUrl` is present and `badgeImageAlt` is `null` or empty, THEN THE CertificationCard SHALL render no BadgeImage rather than an image without alternative text.
4. THE BadgeImage SHALL declare explicit `width` and `height` values so that layout does not shift on load.
5. THE BadgeImage SHALL be constrained by the card width at the 375px Breakpoint with no horizontal overflow.
6. THE BadgeImage SHALL use an internal asset path under `/images/certifications/` or an absolute `https://` URL, in line with `AGENTS.md` 5.1 rule 5.
7. THE BadgeImage SHALL NOT load lazily when it is above the fold and SHALL use native lazy loading otherwise, as selected in the design document.
8. THE M7 implementation SHALL add no image file to `public/images/certifications/` that is not supplied by the Content Owner.

#### Verification Steps

1. Render a fixture with image fields; assert one `img` with matching `src`, non-empty `alt`, `width`, and `height`.
2. Render fixtures with null image fields and with URL-only fields; assert zero `img` elements.
3. Assert at 375px viewport that the card `scrollWidth` does not exceed its `clientWidth`.
4. List `public/images/certifications/` in the change set and assert no unrequested binary assets.

---

### Requirement 10: Supporting Content

**User Story:**
As a recruiter, I want optional context for a credential, so that I understand what it covers.

#### Acceptance Criteria

1. WHEN `Certification.content` is non-empty after trimming, THE CertificationCard SHALL render the Supporting_Content through `renderMarkdown` and the M3 `MarkdownDoc`.
2. WHEN `Certification.content` is empty after trimming, THE CertificationCard SHALL render no Supporting_Content container.
3. THE CertificationCard SHALL render Supporting_Content headings at level `h4` or lower, so that the heading outline defined in Requirement 5 stays unbroken.
4. THE CertificationCard SHALL render Supporting_Content as sanitized output from `renderMarkdown` and SHALL NOT use `dangerouslySetInnerHTML` outside the M3 `MarkdownDoc`.
5. IF `renderMarkdown` throws for a certification, THEN THE build SHALL fail with an error that includes the certification slug.

#### Verification Steps

1. Render a fixture with body "Covers cloud architecture."; assert the text appears inside the card.
2. Render a fixture with an empty body; assert no `MarkdownDoc` container.
3. Render a fixture whose body contains `## Topic`; assert the rendered heading is not an `h1`, `h2`, or `h3`.
4. Assert `grep dangerouslySetInnerHTML src/components/certifications` returns no match.

---

### Requirement 11: Responsive Layout

**User Story:**
As a mobile visitor, I want the certification grid to adapt to my screen, so that cards stay readable at every width.

#### Acceptance Criteria

1. WHILE the viewport width is between 375px and 767px, THE CertificationCategorySection SHALL render its cards in 1 column.
2. WHILE the viewport width is between 768px and 1023px, THE CertificationCategorySection SHALL render its cards in 2 columns.
3. WHILE the viewport width is 1024px or greater, THE CertificationCategorySection SHALL render its cards in 3 columns (`design.md` 6.3).
4. THE CertificationCard SHALL render cards of one row at equal height.
5. THE Certification_Components SHALL cause no horizontal page scroll from 375px through 1440px.
6. THE Certification_Components SHALL wrap long titles, issuer names, and credential identifiers within the card width.
7. THE Certification_Components SHALL use only Semantic_Tokens and the existing Tailwind breakpoint utilities, with no Hardcoded_Design_Value.

#### Verification Steps

1. Assert the grid class list contains the one-, two-, and three-column utilities at the `sm`-less, `md`, and `lg` breakpoints defined by M1.
2. Render a fixture with a 120-character title and a 60-character credential ID; assert no element overflows its card at 375px.
3. Run a static scan of `src/components/certifications/` and `src/app/certifications/` for hex colors and arbitrary-value utilities; assert zero matches.

---

### Requirement 12: Page Metadata

**User Story:**
As a visitor arriving from search or a shared link, I want accurate page metadata, so that the page is identified and previewed correctly.

#### Acceptance Criteria

1. THE Certifications_Index SHALL export a Next.js `metadata` object with the `title` "Certifications", which the M4 title template renders as "Certifications | {siteName}".
2. THE Certifications_Index SHALL export a `description` between 50 and 160 characters that contains no fabricated claim.
3. THE Certifications_Index SHALL set the canonical URL to `{siteUrl}/certifications`, where `siteUrl` is read from the M2 site configuration.
4. THE Certifications_Index SHALL set Open Graph `title`, `description`, `url`, and `type` values consistent with the page metadata.
5. THE Certifications_Index SHALL emit no JSON-LD in M7.
6. THE Certifications_Index SHALL hardcode no site URL or site name.

#### Verification Steps

1. Import the metadata export; assert `title` equals "Certifications" and the description length is within 50 to 160.
2. Assert the canonical value equals `${siteUrl}/certifications` for a mocked site configuration.
3. Assert the Open Graph `url` equals the canonical value.
4. Assert the rendered page contains no `script[type="application/ld+json"]`.

---

### Requirement 13: Static Rendering and Zero Client JavaScript

**User Story:**
As a visitor on a slow connection, I want the page to load as plain HTML, so that it is fast and works without scripts.

#### Acceptance Criteria

1. THE Certifications_Index SHALL be prerendered to static HTML at build time.
2. THE M7 implementation SHALL contain no `'use client'` directive in `src/app/certifications/` or `src/components/certifications/`.
3. THE M7 implementation SHALL use no React state, effect, or browser-only API in Certification_Components.
4. THE Certifications_Index SHALL expose the full certification list, all verification links, and all badge images in the static HTML.
5. THE M7 implementation SHALL create no API route, route handler, or server action (`AGENTS.md` 6.1 rule 2).
6. THE M7 implementation SHALL add no analytics, cookie, form, or third-party script (`AGENTS.md` 6.1 rule 4).
7. THE M7 implementation SHALL add no dependency and SHALL modify no root configuration file (`AGENTS.md` 6.2).

#### Verification Steps

1. Run `npm run build` and assert the output lists `/certifications` as a static route.
2. Search `src/app/certifications/` and `src/components/certifications/` for `'use client'`, `useState`, `useEffect`, and `window`; assert zero matches.
3. Parse the built HTML for `/certifications`; assert verification links and `img` elements are present with scripts ignored.
4. Compare `package.json` and lockfile against the base commit; assert no change.

---

### Requirement 14: Accessibility

**User Story:**
As a visitor using assistive technology, I want the certifications page to be fully operable, so that I can review credentials without barriers.

#### Acceptance Criteria

1. THE Certification_Components SHALL pass an Axe_Check with zero violations for populated, expired, minimal, and empty fixtures.
2. THE Certification_Components SHALL meet WCAG 2.1 AA contrast for text and interactive elements by using Semantic_Tokens.
3. THE VerificationLink SHALL be reachable and operable by keyboard in DOM order with a visible focus indicator.
4. THE CertificationCard SHALL provide each link with an accessible name that differs from every other link on the page.
5. THE Certifications_Index SHALL use semantic landmarks and headings only, with no `div` acting as a heading or list.
6. WHILE the user prefers Reduced_Motion, THE Certification_Components SHALL render no transition or animation.
7. THE Certification_Components SHALL render each date in a `time` element.

#### Verification Steps

1. Run the Axe_Check on four fixtures and assert zero violations each.
2. Tab through a page with three verification links; assert focus order matches DOM order and each focused link shows the `FOCUS_RING` classes.
3. Collect all link accessible names on the rendered page and assert they are unique.
4. Assert no `transition` or `animate` utility applies under the reduced-motion media query.

---

### Requirement 15: Testing and Quality Gates

**User Story:**
As an engineer, I want M7 covered by automated tests and gates, so that regressions in credential data are caught before deployment.

#### Acceptance Criteria

1. THE M7 test suite SHALL use Vitest, React Testing Library, an axe-core based tool, and fast-check, all already installed by M1.
2. THE M7 test suite SHALL include a Property_Test for each of: partition and no loss, order, input-order independence, idempotence, and expiry classification.
3. THE M7 test suite SHALL include a component test for each Certification_Component.
4. THE M7 test suite SHALL include a page-level test for `src/app/certifications/page.tsx` covering the populated and empty cases.
5. THE M7 implementation SHALL use no `any`, no implicit `any`, no non-null assertion, and no unjustified type assertion (`AGENTS.md` 6.1 rule 7).
6. THE M7 implementation SHALL keep each component file below 300 lines (`AGENTS.md` 7.2).
7. THE M7 implementation SHALL leave all M1 to M6 files and tests unmodified.
8. WHEN `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build` run, THE M7 implementation SHALL pass all four.

#### Verification Steps

1. Run `npm test` and assert all M7 test files pass alongside the existing suites.
2. Run `npm run lint`, `npm run typecheck`, and `npm run build` and assert exit code 0 for each.
3. Run `git diff --stat` against the M6 base and assert changes appear only under `src/app/certifications/`, `src/components/certifications/`, `src/lib/certifications/`, `tests/`, and optionally `content/certifications/` and `public/images/certifications/`.
4. Scan for `any`, `!.`, and `as ` assertions in M7 files and assert each is absent or justified in a comment.
