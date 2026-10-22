# Requirements Document

> **Spec:** M4 Global Layout & Navigation  
> **Document Status:** Draft  
> **Feature Name:** m4-global-layout-navigation  
> **Milestone:** M4  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 3, 4.2, 6), `TRD.md` (Sections 3.3, 4.3, 6.5), `design.md` (Sections 4.2, 5, 6), `APP_FLOW.md` (Flow 5.0, `SCR-07`)  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 4 (M4) implements the global layout shell for `personal-website-portfolio-v2`: the root layout in `src/app/layout.tsx` and the layout components in `src/components/layout/`. M4 delivers the SiteHeader, primary navigation, mobile navigation disclosure control, current-route indication, skip-to-content link, SiteFooter, ContactLinks, site-wide metadata defaults, and the global not-found page in `src/app/not-found.tsx`.

M4 reads site identity, navigation, social links, and contact channels from `SiteConfig` through the M2 `getSiteConfig()` loader. M4 composes the M3 primitives (`Container`, `Button`, `ExternalLink`, shared `FOCUS_RING` and motion helpers) and does not redefine them or any design token. Components are server components unless transient interaction state requires `'use client'`; the mobile navigation disclosure control is the only client component planned for M4 (`TRD.md` 3.3).

M4 does NOT implement homepage content (M5), the projects, certifications, or blog routes (M6–M8), performance tuning or deployment (M9–M10), dark mode, API routes, analytics, forms, or new dependencies.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Root_Layout** | The `src/app/layout.tsx` component that wraps every route with the shared shell. |
| **Layout_Component** | A component in `src/components/layout/` that renders part of the global shell. |
| **SiteHeader** | Layout_Component rendering site identity, the PrimaryNav, and an optional contact action (`design.md` 4.2). |
| **SiteFooter** | Layout_Component rendering copyright, social and professional links, and contact links (`design.md` 4.2). |
| **PrimaryNav** | The `nav` landmark inside the SiteHeader listing the entries from `SiteConfig.navigation`. |
| **MobileNavToggle** | Client component that discloses and collapses the PrimaryNav on Mobile breakpoints. |
| **Disclosure_State** | The expanded or collapsed state of the MobileNavToggle, exposed through `aria-expanded`. |
| **SkipLink** | First focusable element on each page that moves focus to the `main` landmark. |
| **Main_Landmark** | The `main` element with `id="main-content"` that holds the page content. |
| **Current_Route_Indicator** | The combination of `aria-current="page"` and a visual style on the PrimaryNav entry matching the active route. |
| **ContactLinks** | Layout_Component rendering the entries of `SiteConfig.contactChannels`. |
| **SiteConfig** | The typed site configuration defined once in `AGENTS.md` 4.2 and loaded from `content/site.json`. |
| **getSiteConfig** | The M2 loader function that returns a validated `SiteConfig`. |
| **Site_Metadata** | The site-wide Next.js metadata defaults (title template, description, canonical base, Open Graph defaults). |
| **NotFound_Page** | The global not-found boundary rendered by `src/app/not-found.tsx` (`SCR-07`). |
| **UI_Primitive** | A reusable M3 component in `src/components/ui/`. |
| **Semantic_Token** | A named design value from `design.md` Section 3, exposed by M1 through Tailwind and CSS custom properties. |
| **Hardcoded_Design_Value** | A raw hex color, arbitrary pixel size, arbitrary shadow, or arbitrary duration written directly in a component. |
| **Breakpoints** | Mobile `375px–767px`, Tablet `768px–1023px`, Desktop `1024px–1439px`, Wide Desktop `1440px+` (`design.md` 5.1). |
| **Axe_Check** | An automated accessibility test run against rendered components using an axe-core based tool. |
| **Reduced_Motion** | The user preference exposed by the `prefers-reduced-motion: reduce` media query. |

---

## Requirements

---

### Requirement 1: Root Layout Shell and Landmarks

**User Story:**
As a visitor using assistive technology, I want every page wrapped in a consistent landmark structure, so that I can navigate between regions of any page.

#### Acceptance Criteria

1. THE Root_Layout SHALL render the SiteHeader, the Main_Landmark, and the SiteFooter, in that document order, around every route.
2. THE Root_Layout SHALL render the SiteHeader inside a `header` element, the PrimaryNav inside a `nav` element, the page content inside the `main` element, and the SiteFooter inside a `footer` element.
3. THE Root_Layout SHALL render exactly one `main` element per page.
4. THE Root_Layout SHALL set the `lang` attribute of the `html` element to `en`.
5. THE PrimaryNav SHALL carry an `aria-label` that distinguishes it from any other `nav` landmark on the page.
6. THE Root_Layout SHALL import the global stylesheet defined in M1 and SHALL NOT define additional global styles.
7. THE Root_Layout SHALL render as a server component.

#### Verification Steps

1. Render the Root_Layout with a stub child; assert one `header`, one `main`, one `footer`, and the document order of the three.
2. Assert the `html` element has `lang="en"`.
3. Run Axe_Check on the rendered shell; confirm zero `landmark-*` and `region` violations.

---

### Requirement 2: Load SiteConfig Through the M2 Loader

**User Story:**
As a content owner, I want the shell to read identity, navigation, and links from `content/site.json`, so that I can change them without editing components.

#### Acceptance Criteria

1. THE Root_Layout SHALL obtain site data by calling `getSiteConfig()` from the M2 loader module.
2. THE Layout_Component set SHALL receive `SiteConfig` data through props typed with types imported from the M2 schemas.
3. THE M4 implementation SHALL NOT redeclare `SiteConfig`, `SiteNavigationItem`, `ContactChannel`, or `SocialLink` (`AGENTS.md` 6.3).
4. THE M4 implementation SHALL NOT hardcode the site name, owner name, navigation labels, hrefs, social URLs, or contact URLs in any Layout_Component.
5. IF `getSiteConfig()` throws a validation error, THEN THE build SHALL fail with the error message from the loader containing the file path and schema issue (`TRD.md` 4.3).
6. THE Layout_Component set SHALL read no data from the network and no data from `window` or `document` at render time.

#### Verification Steps

1. Search `src/components/layout/` and `src/app/layout.tsx` for string literals matching the values in `content/site.json`; confirm zero matches.
2. Search for `interface SiteConfig` and `type SiteConfig` outside `src/content/schemas/`; confirm zero matches.
3. Temporarily corrupt `content/site.json` in a test fixture; confirm the loader error surfaces unchanged.

---

### Requirement 3: SiteHeader

**User Story:**
As a visitor, I want a header showing the site identity and primary navigation on every page, so that I always know where I am and where I can go.

#### Acceptance Criteria

1. THE SiteHeader SHALL render the `SiteConfig.siteName` as a link to `/`.
2. THE SiteHeader SHALL render the PrimaryNav.
3. WHERE a `ContactChannel` with `isPrimary: true` exists in `SiteConfig.contactChannels`, THE SiteHeader SHALL render one contact action for that channel on the Desktop and Wide Desktop Breakpoints.
4. IF no `ContactChannel` with `isPrimary: true` exists, THEN THE SiteHeader SHALL omit the contact action.
5. THE SiteHeader SHALL constrain its content width and horizontal padding with the M3 `Container`.
6. THE SiteHeader SHALL render as a server component.

#### Verification Steps

1. Render the SiteHeader with a fixture containing a primary channel; assert the identity link `href="/"` and one contact action.
2. Render the SiteHeader with a fixture without a primary channel; assert zero contact actions.
3. Confirm the SiteHeader module has no `'use client'` directive.

---

### Requirement 4: Primary Navigation Order and Data Source

**User Story:**
As a visitor, I want primary navigation in a predictable order, so that I can find Projects, Certifications, Blog, and Contact quickly.

#### Acceptance Criteria

1. THE PrimaryNav SHALL render its entries as an unordered list of links.
2. THE PrimaryNav SHALL render the entries in the order Home, Projects, Certifications, Blog, Contact (`design.md` 4.2).
3. THE PrimaryNav SHALL derive the label and `href` of the Home, Projects, Certifications, and Blog entries from `SiteConfig.navigation`.
4. WHERE `SiteConfig.contactChannels` contains at least one entry, THE PrimaryNav SHALL render a Contact entry last, linking to the `id="contact"` region of the SiteFooter.
5. IF `SiteConfig.contactChannels` is empty, THEN THE PrimaryNav SHALL omit the Contact entry.
6. THE PrimaryNav SHALL render each internal entry with the Next.js `Link` component.
7. THE PrimaryNav SHALL render no entry whose `href` is absent from `SiteConfig.navigation`, other than the Contact entry defined in criterion 4.

#### Verification Steps

1. Render the PrimaryNav with the `content/site.json` fixture; assert the label order Home, Projects, Certifications, Blog, Contact.
2. Render with an empty `contactChannels` fixture; assert the Contact entry is absent.
3. Assert every non-Contact link `href` equals a `SiteConfig.navigation` `href`.

---

### Requirement 5: Current-Route Indication

**User Story:**
As a visitor, I want the current section highlighted in the navigation, so that I can see where I am in the site.

#### Acceptance Criteria

1. WHEN the current pathname equals a PrimaryNav entry `href`, THE PrimaryNav SHALL set `aria-current="page"` on that entry.
2. WHEN the current pathname begins with a PrimaryNav entry `href` followed by `/` and the entry `href` is not `/`, THE PrimaryNav SHALL set `aria-current="page"` on that entry (for example `/projects/example-project` marks Projects).
3. WHILE an entry has `aria-current="page"`, THE PrimaryNav SHALL apply a visual style that differs from non-current entries using Semantic_Tokens and that does not rely on color alone (for example an underline or border).
4. THE PrimaryNav SHALL apply `aria-current="page"` to at most one entry at a time.
5. WHEN the pathname is `/`, THE PrimaryNav SHALL mark only the Home entry as current.
6. IF the pathname matches no PrimaryNav entry, THEN THE PrimaryNav SHALL set `aria-current` on no entry.
7. THE current-route matching function SHALL be a pure function of pathname and entry `href` values.

#### Verification Steps

1. Run unit tests of the matching function for `/`, `/projects`, `/projects/example-project`, `/blog`, `/unknown`, and `/projectsfoo`; confirm `/projectsfoo` does not mark Projects.
2. Render the PrimaryNav at each pathname; assert the count of `[aria-current="page"]` is 1 or 0 as specified.
3. Confirm the current style includes a non-color cue in the class list.

---

### Requirement 6: Mobile Navigation Disclosure

**User Story:**
As a mobile visitor, I want a menu button that opens and closes the navigation, so that I can reach every page on a narrow screen.

#### Acceptance Criteria

1. WHILE the viewport is at the Mobile or Tablet Breakpoint, THE SiteHeader SHALL render the MobileNavToggle and collapse the PrimaryNav entries by default.
2. WHILE the viewport is at the Desktop or Wide Desktop Breakpoint, THE SiteHeader SHALL render the PrimaryNav horizontally and hide the MobileNavToggle.
3. THE MobileNavToggle SHALL render a native `button` element with an accessible name of `Menu`, `aria-expanded` reflecting the Disclosure_State, and `aria-controls` referencing the `id` of the navigation list.
4. WHEN the user activates the MobileNavToggle, THE MobileNavToggle SHALL toggle the Disclosure_State and update `aria-expanded`.
5. WHEN the Disclosure_State is expanded and the user presses the Escape key, THE MobileNavToggle SHALL collapse the navigation and return focus to the toggle button.
6. WHEN the user activates a navigation link while the Disclosure_State is expanded, THE MobileNavToggle SHALL collapse the navigation.
7. WHEN the pathname changes, THE MobileNavToggle SHALL collapse the navigation.
8. THE MobileNavToggle SHALL be operable with the Enter and Space keys.
9. WHILE the navigation is collapsed at a Mobile or Tablet Breakpoint, THE SiteHeader SHALL remove the navigation links from the tab order and from the accessibility tree.
10. THE MobileNavToggle module SHALL declare `'use client'` and hold only the Disclosure_State as client state, with a code comment justifying the directive (`AGENTS.md` 6.2).
11. THE PrimaryNav entries SHALL remain present in the server-rendered HTML.
12. WHILE Reduced_Motion is active, THE MobileNavToggle SHALL open and close the navigation without animated transitions.

#### Verification Steps

1. With React Testing Library, click the toggle; assert `aria-expanded` changes from `false` to `true` and back.
2. Open the menu, press Escape; assert the menu collapses and `document.activeElement` is the toggle.
3. Open the menu, click a link; assert the menu collapses. Re-render with a new pathname; assert collapse.
4. Tab through the collapsed Mobile header; assert the navigation links are not focusable.
5. Search the layout directory for `'use client'`; confirm only the MobileNavToggle module matches.

---

### Requirement 7: Skip-to-Content Link

**User Story:**
As a keyboard user, I want a skip link at the start of every page, so that I can bypass the header navigation.

#### Acceptance Criteria

1. THE SkipLink SHALL be the first focusable element in the document order of every page.
2. THE SkipLink SHALL have the visible text `Skip to main content` and an `href` of `#main-content`.
3. THE Main_Landmark SHALL have `id="main-content"` and `tabindex="-1"` so that activating the SkipLink moves focus to it.
4. WHILE the SkipLink does not have keyboard focus, THE SkipLink SHALL be visually hidden and remain available to assistive technology.
5. WHEN the SkipLink receives keyboard focus, THE SkipLink SHALL become visible and display the shared `FOCUS_RING` style from M3.
6. WHEN the user activates the SkipLink, THE browser SHALL move focus to the Main_Landmark.

#### Verification Steps

1. Render the shell and press Tab once; assert `document.activeElement` is the SkipLink.
2. Activate the SkipLink; assert the `href` target exists and equals the `main` element `id`.
3. Confirm the SkipLink class list includes the `FOCUS_RING` helper output and a visually-hidden-until-focus utility.

---

### Requirement 8: SiteFooter

**User Story:**
As a visitor, I want a footer with copyright and links, so that I can reach the owner's professional profiles from any page.

#### Acceptance Criteria

1. THE SiteFooter SHALL render a copyright line containing the current year and `SiteConfig.profile.name`.
2. THE SiteFooter SHALL render each entry of `SiteConfig.socialLinks` as an ExternalLink in a list with an accessible name.
3. THE SiteFooter SHALL render the ContactLinks inside a region with `id="contact"`.
4. THE SiteFooter SHALL render the secondary navigation using the entries of `SiteConfig.navigation`.
5. IF `SiteConfig.socialLinks` is empty, THEN THE SiteFooter SHALL omit the social links list and its heading.
6. IF `SiteConfig.contactChannels` is empty, THEN THE SiteFooter SHALL omit the ContactLinks, the `id="contact"` region, and its heading.
7. THE SiteFooter SHALL render the year at build time without client-side JavaScript.
8. THE SiteFooter SHALL constrain its content with the M3 `Container`.
9. THE SiteFooter SHALL render as a server component.

#### Verification Steps

1. Render the SiteFooter with a full fixture; assert the copyright text, the social link count, and the `#contact` region.
2. Render with empty arrays; assert the social list and contact region are absent.
3. Confirm the SiteFooter module has no `'use client'` directive.

---

### Requirement 9: ContactLinks Presentation

**User Story:**
As a visitor, I want clear contact links, so that I can reach the owner through email or a professional profile.

#### Acceptance Criteria

1. WHEN a `ContactChannel` has `type` equal to `email`, THE ContactLinks SHALL render an anchor with an `href` beginning with `mailto:` and without `target="_blank"`.
2. WHEN a `ContactChannel` has a `type` other than `email`, THE ContactLinks SHALL render the channel with the M3 ExternalLink component.
3. THE ContactLinks SHALL use the `label` of each `ContactChannel` as the visible link text.
4. WHERE a `ContactChannel` has `isPrimary: true`, THE ContactLinks SHALL list that channel first.
5. IF `SiteConfig.contactChannels` is empty, THEN THE ContactLinks SHALL render nothing.
6. THE ContactLinks SHALL render no form, input, textarea, or submit control.
7. THE ContactLinks SHALL render no placeholder or `#` link for an unconfigured channel (`TRD.md` 4.3).
8. THE ContactLinks SHALL render as a server component.

#### Verification Steps

1. Render ContactLinks with email, LinkedIn, and GitHub fixtures; assert the `mailto:` anchor and 2 ExternalLink anchors with `rel="noopener noreferrer"`.
2. Render with an empty array; assert the container is empty.
3. Assert zero `form`, `input`, and `textarea` elements in the rendered output.

---

### Requirement 10: Site-Wide Metadata Defaults

**User Story:**
As a content owner, I want default page metadata defined once, so that every page has a consistent title, description, and canonical base.

#### Acceptance Criteria

1. THE Root_Layout SHALL export site-wide metadata derived from `getSiteConfig()` using the Next.js `generateMetadata` or `metadata` convention.
2. THE Site_Metadata SHALL set `metadataBase` to a URL constructed from `SiteConfig.siteUrl`.
3. THE Site_Metadata SHALL set a title with `default` equal to `SiteConfig.siteName` and `template` equal to `%s | ` followed by `SiteConfig.siteName`.
4. THE Site_Metadata SHALL set a `description` derived from `SiteConfig.profile.introduction`.
5. THE Site_Metadata SHALL set Open Graph defaults for `type`, `siteName`, `title`, `description`, and `url`.
6. THE Site_Metadata SHALL set no Open Graph or Twitter image unless an image path is configured in content.
7. IF `SiteConfig.siteUrl` is not a valid absolute URL, THEN THE build SHALL fail with a descriptive error.
8. THE Site_Metadata SHALL contain no value that is not derived from `SiteConfig`.

#### Verification Steps

1. Call the metadata function with the `content/site.json` fixture; assert `metadataBase.href`, the title template, the description, and the Open Graph fields.
2. Assert no `images` key exists in the Open Graph defaults.
3. Call with an invalid `siteUrl` fixture; assert the failure.

---

### Requirement 11: Global Not-Found Page

**User Story:**
As a visitor who followed a broken link, I want a clear not-found page with a way back, so that I can continue browsing.

#### Acceptance Criteria

1. THE NotFound_Page SHALL be implemented in `src/app/not-found.tsx` and SHALL render inside the Root_Layout so that the SiteHeader and SiteFooter appear (`APP_FLOW.md` `SCR-07`).
2. THE NotFound_Page SHALL render one `h1` stating that the page was not found.
3. THE NotFound_Page SHALL render an explanatory sentence and a Button of variant `primary` rendered as a link to `/`.
4. THE NotFound_Page SHALL render links to Projects, Certifications, and Blog sourced from `SiteConfig.navigation`.
5. WHEN a route calls `notFound()` for an invalid slug, THE Next.js App Router SHALL render the NotFound_Page.
6. THE NotFound_Page SHALL render the content in the Main_Landmark.
7. THE NotFound_Page SHALL render as a server component.

#### Verification Steps

1. Render the NotFound_Page; assert one `h1`, one link with `href="/"`, and the section links.
2. Run Axe_Check on the NotFound_Page inside the shell; confirm zero violations.
3. After M6–M8 routes exist, request an invalid slug; confirm the NotFound_Page renders.

---

### Requirement 12: Responsive Behavior

**User Story:**
As a visitor on any device, I want the shell to adapt to my screen width, so that navigation and content stay usable from phones to wide monitors.

#### Acceptance Criteria

1. THE Layout_Component set SHALL render without horizontal page scrolling at viewport widths of 375px, 768px, 1024px, and 1440px.
2. WHILE the viewport is at the Mobile Breakpoint, THE SiteFooter SHALL stack its sections in a single column.
3. WHILE the viewport is at the Tablet Breakpoint or above, THE SiteFooter SHALL arrange its sections in multiple columns.
4. WHILE the viewport is at the Wide Desktop Breakpoint, THE Layout_Component set SHALL center content within the `Container` maximum width.
5. THE MobileNavToggle and navigation link touch targets SHALL be at least 44px by 44px at the Mobile Breakpoint.
6. THE Layout_Component set SHALL express breakpoints with the Tailwind breakpoint utilities configured in M1.
7. THE Layout_Component set SHALL remain usable when text is resized to 200 percent.

#### Verification Steps

1. Run the browser or Playwright check at 375, 768, 1024, and 1440px; assert `document.documentElement.scrollWidth <= window.innerWidth`.
2. Confirm the toggle is visible below 1024px and hidden at 1024px and above.
3. Search layout classes for `min-w-[` or `w-[`; confirm zero arbitrary-value matches.

---

### Requirement 13: Composition of M3 Primitives and Token Compliance

**User Story:**
As a design system maintainer, I want the shell built from the M3 primitives and tokens, so that visual values stay consistent and are changed in one place.

#### Acceptance Criteria

1. THE Layout_Component set SHALL use the M3 `Container` for content width constraints.
2. THE Layout_Component set SHALL use the M3 `ExternalLink` for every link to an external destination other than `mailto:`.
3. THE Layout_Component set SHALL use the M3 `Button` for the header contact action and the NotFound_Page home action.
4. THE Layout_Component set SHALL apply the shared `FOCUS_RING` helper to every interactive element.
5. THE Layout_Component set SHALL style colors, spacing, typography, radius, elevation, and motion exclusively through Semantic_Tokens.
6. THE Layout_Component set SHALL contain zero Hardcoded_Design_Values (`AGENTS.md` 6.1 Rule 8).
7. THE M4 implementation SHALL NOT add, modify, or remove any file in `src/components/ui/` or any token in `tailwind.config.ts` or `globals.css`.
8. IF a required UI_Primitive or Semantic_Token is absent, THEN THE M4 implementation SHALL record the gap in the spec's task notes and request human approval before any change outside `src/app/` and `src/components/layout/` (`AGENTS.md` 6.2).
9. THE Layout_Component set SHALL apply no `dark:` utilities.

#### Verification Steps

1. Search `src/components/layout/` for `#[0-9A-Fa-f]{3,8}`, `rgb(`, `rgba(`, `dark:`, and arbitrary-value classes; confirm zero matches.
2. Search for `<a ` with `target="_blank"` in `src/components/layout/`; confirm zero matches.
3. Run `git diff` on `src/components/ui/`, `tailwind.config.ts`, and `globals.css`; confirm no changes.

---

### Requirement 14: Scope and Privacy Guardrails

**User Story:**
As the project owner, I want the shell to collect no visitor data and add no backend surface, so that the site stays static and private.

#### Acceptance Criteria

1. THE M4 implementation SHALL add no API route, route handler, or server action (`AGENTS.md` 6.1 Rule 2).
2. THE M4 implementation SHALL add no analytics script, cookie, form, or third-party tracking script (`AGENTS.md` 6.1 Rule 4).
3. THE M4 implementation SHALL add no runtime dependency or dev dependency without documented purpose and human approval (`AGENTS.md` 6.2).
4. THE M4 implementation SHALL NOT modify `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, or CI configuration.
5. THE M4 implementation SHALL contain no homepage, projects, certifications, or blog page content.
6. THE M4 implementation SHALL contain no `any`, implicit `any`, non-null assertion, or unjustified type assertion (`AGENTS.md` 6.1 Rule 7).
7. THE Layout_Component set SHALL keep each component file below 300 lines where practical (`AGENTS.md` 7.2).
8. THE build output for M4 routes SHALL be statically generated.

#### Verification Steps

1. Confirm no `route.ts` file and no `'use server'` directive exists under `src/`.
2. Run `git diff` on `package.json` and the lockfile; confirm no changes.
3. Run `npm run typecheck` and `npm run lint`; confirm zero errors.
4. Run `npm run build`; confirm the output lists the shell routes as static.

---

### Requirement 15: Tests and Automated Accessibility Checks

**User Story:**
As a QA engineer, I want automated tests for the shell, so that navigation and accessibility regressions fail the build before release.

#### Acceptance Criteria

1. THE M4 implementation SHALL include Vitest and React Testing Library tests for the SiteHeader, PrimaryNav, MobileNavToggle, SiteFooter, ContactLinks, SkipLink, and NotFound_Page in `tests/`.
2. THE test suite SHALL include a unit test of the current-route matching function covering exact match, nested path match, root path, no match, and a shared-prefix path that does not match.
3. THE test suite SHALL include an Axe_Check for the SiteHeader, the SiteFooter, the expanded MobileNavToggle, and the NotFound_Page, each asserting zero violations.
4. THE test suite SHALL include keyboard tests for the MobileNavToggle covering Enter, Space, and Escape.
5. THE test suite SHALL include empty-data tests for an empty `contactChannels` array and an empty `socialLinks` array.
6. THE test suite SHALL include a property-based test asserting that FOR ALL generated pathnames and navigation `href` sets, at most one entry is marked current.
7. THE test suite SHALL run without network access and without reading files outside the repository.
8. WHEN `npm test` runs, THE test suite SHALL pass with zero failures before M4 is marked complete (`AGENTS.md` 7.3).

#### Verification Steps

1. Run `npm test`; confirm all M4 test files execute and pass.
2. Run `npm run lint`, `npm run typecheck`, and `npm run build`; confirm each exits with code 0.
3. Introduce a deliberate violation (for example remove the toggle `aria-expanded`) in a scratch branch; confirm the Axe_Check or unit test fails.
4. Perform a manual keyboard-only pass at 375px and 1440px covering the SkipLink, the PrimaryNav, the MobileNavToggle, and the footer links.
