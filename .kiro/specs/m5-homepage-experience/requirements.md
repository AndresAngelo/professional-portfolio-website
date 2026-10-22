# Requirements Document

> **Spec:** M5 Homepage Experience  
> **Document Status:** Draft  
> **Feature Name:** m5-homepage-experience  
> **Milestone:** M5  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 3, 4.2, 5, 6), `PRD.md` (Homepage, P0), `design.md` (Sections 4, 5, 6.1), `APP_FLOW.md` (Flow 1.0, Story 1.1, `SCR-01`), `implementation_plan.md` (Task 4.1)  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 5 (M5) implements the homepage for `personal-website-portfolio-v2`: the static server route `src/app/page.tsx` and the section components in `src/components/home/`. M5 delivers the HeroSection, FeaturedProjects, SkillsSnapshot, CertificationsPreview, and RecentActivity sections, the homepage metadata, and the pure selection helpers that choose which content each section displays.

M5 reads site identity from `SiteConfig` through `getSiteConfig()`, projects through `getProjects()`, certifications through `getCertifications()`, and blog posts through `getBlogPosts()`, all from the M2 loaders. M5 composes the M3 UI_Primitives (`Card`, `TagList`, `StatusBadge`, `EventTypeBadge`, `EmptyState`, `Button`, `ExternalLink`, `Container`, `FOCUS_RING`, motion helpers) and the M4 shell (`SiteHeader`, `SiteFooter`, `main#main-content`, title template). M5 does not modify any design token, UI_Primitive, or Layout_Component.

M5 does NOT implement the projects, certifications, or blog index and detail routes (M6–M8; M5 only links to them), filters, search, resume download (P1), performance tuning or deployment (M9–M10), dark mode, API routes, analytics, forms, or new dependencies without human approval.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Homepage** | The route `/` rendered by `src/app/page.tsx` (`SCR-01`). |
| **Home_Component** | A component in `src/components/home/` that renders one Homepage section. |
| **HeroSection** | Home_Component rendering name, professional title, introduction, location, availability indicator, and calls to action. |
| **FeaturedProjects** | Home_Component rendering the featured project cards. |
| **SkillsSnapshot** | Home_Component rendering compact technology groups derived from project data. |
| **CertificationsPreview** | Home_Component rendering a small set of certifications with a link to `/certifications`. |
| **RecentActivity** | Home_Component rendering the latest published blog entries. |
| **Selection_Helper** | A pure function in `src/lib/` or `src/components/home/` that selects or derives Homepage data without rendering: `selectFeaturedProjects`, `selectRecentPosts`, `deriveSkillGroups`, `selectCertificationPreview`. |
| **Featured_Project** | A `Project` with `featured: true`. |
| **Published_Post** | A `BlogPost` with `draft: false`. |
| **Skill_Group** | A labeled list of technology names derived from the `technologies` field of `Project` entries. |
| **Renderable_Contact_Channel** | A `ContactChannel` with a non-empty `label` and a non-empty `url`. |
| **Preview_Limit** | The maximum item count for a section: 3 for FeaturedProjects, 3 for RecentActivity, 3 for CertificationsPreview. |
| **Section_Heading** | The `h2` element that titles a Homepage section. |
| **SiteConfig** | The typed site configuration defined in `AGENTS.md` 4.2 and loaded by `getSiteConfig()`. |
| **UI_Primitive** | A reusable M3 component in `src/components/ui/`. |
| **Semantic_Token** | A named design value from `design.md` Section 3, exposed by M1 through Tailwind and CSS custom properties. |
| **Hardcoded_Design_Value** | A raw hex color, arbitrary pixel size, arbitrary shadow, or arbitrary duration written directly in a component. |
| **Date_Formatter** | A deterministic function that converts an `IsoDateString` to display text without reading the system locale or time zone. |
| **Breakpoints** | Mobile `375px–767px`, Tablet `768px–1023px`, Desktop `1024px–1439px`, Wide Desktop `1440px+` (`design.md` 5.1). |
| **Axe_Check** | An automated accessibility test run against rendered components using an axe-core based tool. |
| **Property_Test** | A fast-check test asserting a Selection_Helper property over generated inputs. |
| **Reduced_Motion** | The user preference exposed by the `prefers-reduced-motion: reduce` media query. |

---

## Requirements

---

### Requirement 1: Homepage Route Composition

**User Story:**
As a visitor, I want the homepage to present my orientation content in a predictable order, so that I can understand who Angelo is and find evidence quickly.

#### Acceptance Criteria

1. THE Homepage SHALL render the HeroSection, FeaturedProjects, SkillsSnapshot, CertificationsPreview, and RecentActivity, in that document order, inside the M4 Main_Landmark.
2. THE Homepage SHALL render as a static server component with no `'use client'` directive and no dynamic route segment.
3. THE Homepage SHALL obtain data by calling `getSiteConfig()`, `getProjects()`, `getCertifications()`, and `getBlogPosts()` from the M2 loader modules.
4. THE Homepage SHALL pass loader results to Home_Components through props typed with types imported from the M2 schemas.
5. THE M5 implementation SHALL NOT redeclare `SiteConfig`, `Project`, `Certification`, or `BlogPost` (`AGENTS.md` 6.3).
6. THE Homepage SHALL read no data from the network and no data from `window` or `document` at render time.
7. THE Homepage SHALL render no `header`, `footer`, or `main` element, because the M4 Root_Layout owns those landmarks.

#### Verification Steps

1. Render the Homepage with fixture loader results; assert the five sections appear in the specified document order.
2. Search `src/app/page.tsx` and `src/components/home/` for `'use client'`, `fetch(`, `window`, and `document`; confirm zero matches.
3. Search for `interface Project` and `type SiteConfig` outside `src/content/schemas/`; confirm zero matches.
4. Assert the rendered Homepage contains zero `header`, `footer`, and `main` elements of its own.

---

### Requirement 2: HeroSection Profile Content

**User Story:**
As a recruiter, I want to see Angelo's name, professional title, and introduction immediately, so that I can assess the technical profile within seconds.

#### Acceptance Criteria

1. THE HeroSection SHALL render `SiteConfig.profile.name` inside the only `h1` element on the Homepage.
2. THE HeroSection SHALL render `SiteConfig.profile.professionalTitle` and `SiteConfig.profile.introduction` as text.
3. THE HeroSection SHALL render `SiteConfig.profile.location` as text.
4. THE HeroSection SHALL obtain every displayed profile string from `SiteConfig.profile`.
5. THE M5 implementation SHALL NOT hardcode the owner name, professional title, introduction, or location in any Home_Component.
6. IF a required `SiteConfig.profile` field is missing, THEN THE build SHALL fail through the M2 loader validation and THE HeroSection SHALL NOT render a runtime fallback value (`APP_FLOW.md` `[HeroSection]` empty state).

#### Verification Steps

1. Render the HeroSection with a profile fixture; assert one `h1` containing the name and visible title, introduction, and location text.
2. Search `src/components/home/` for string literals matching values in `content/site.json`; confirm zero matches.
3. Run the M2 loader against a fixture missing `profile.introduction`; confirm the build-time validation error and confirm the HeroSection has no fallback string.

---

### Requirement 3: HeroSection Calls to Action

**User Story:**
As a visitor, I want clear next actions in the hero, so that I can view projects or contact Angelo.

#### Acceptance Criteria

1. THE HeroSection SHALL render a primary call to action labeled "View Projects" that links to `/projects` (`APP_FLOW.md` Step 1.3).
2. THE HeroSection SHALL render the primary call to action using the M3 `Button` primitive.
3. WHERE at least one Renderable_Contact_Channel exists in `SiteConfig.contactChannels`, THE HeroSection SHALL render one secondary contact call to action using the label and url of the channel with `isPrimary: true`, or the first Renderable_Contact_Channel when none has `isPrimary: true`.
4. IF no Renderable_Contact_Channel exists, THEN THE HeroSection SHALL omit the secondary contact call to action (`APP_FLOW.md` Step 1.2).
5. WHEN the secondary contact call to action targets an external `https://` URL, THE HeroSection SHALL render it through the M3 `ExternalLink` primitive.
6. THE HeroSection SHALL render each call to action with the M3 `FOCUS_RING` and an accessible name that is unique within the section.

#### Verification Steps

1. Render the HeroSection; assert a link named "View Projects" with `href="/projects"`.
2. Render with a fixture containing a primary channel; assert the secondary action uses that channel's label and url.
3. Render with a fixture whose channels are empty; assert the secondary action is absent and the primary action remains.
4. Run Axe_Check on the HeroSection; confirm zero violations.

---

### Requirement 4: Availability Indicator

**User Story:**
As a recruiter, I want to know whether Angelo is open to opportunities, so that I can decide whether to reach out.

#### Acceptance Criteria

1. WHERE `SiteConfig.profile.availableForOpportunities` is `true`, THE HeroSection SHALL render an availability indicator with visible text.
2. IF `SiteConfig.profile.availableForOpportunities` is `false`, THEN THE HeroSection SHALL omit the availability indicator.
3. THE HeroSection SHALL convey availability through visible text and SHALL NOT rely on color alone (`design.md` Section 4).
4. THE HeroSection SHALL style the availability indicator with Semantic_Tokens only.

#### Verification Steps

1. Render with `availableForOpportunities: true`; assert the indicator text is present.
2. Render with `availableForOpportunities: false`; assert the indicator is absent.
3. Search `src/components/home/` for Hardcoded_Design_Values; confirm zero matches.

---

### Requirement 5: Featured Project Selection

**User Story:**
As a content owner, I want the homepage to show my designated featured projects in my chosen order, so that the strongest evidence appears first.

#### Acceptance Criteria

1. THE `selectFeaturedProjects` Selection_Helper SHALL return only `Project` entries with `featured: true`.
2. THE `selectFeaturedProjects` Selection_Helper SHALL order the result by `displayOrder` ascending.
3. THE `selectFeaturedProjects` Selection_Helper SHALL return at most 3 entries (`APP_FLOW.md` Story 1.1).
4. WHEN two Featured_Projects share the same `displayOrder`, THE `selectFeaturedProjects` Selection_Helper SHALL order them by `slug` ascending.
5. THE `selectFeaturedProjects` Selection_Helper SHALL NOT mutate its input array.
6. FOR ALL input arrays, THE `selectFeaturedProjects` Selection_Helper SHALL return a result in which every entry is contained in the input, and applying the Selection_Helper to its own result SHALL return an equal result (idempotence).

#### Verification Steps

1. Write a Property_Test over generated `Project` arrays asserting: result length is at most 3; every entry has `featured: true`; the `displayOrder` sequence is non-decreasing; every entry exists in the input.
2. Write a Property_Test asserting idempotence and input immutability.
3. Write an example test with ties on `displayOrder` asserting `slug` tie-breaking.

---

### Requirement 6: FeaturedProjects Section Rendering

**User Story:**
As a recruiter, I want each featured project summarized with its status and technologies, so that I can judge scope and open the detail page.

#### Acceptance Criteria

1. THE FeaturedProjects SHALL render a Section_Heading as an `h2` element.
2. THE FeaturedProjects SHALL render one M3 `Card` per selected project containing the project title, summary, `StatusBadge`, and `TagList` of the project `technologies`.
3. THE FeaturedProjects SHALL render the project title as a link to `/projects/{slug}` (`APP_FLOW.md` Step 1.4).
4. THE FeaturedProjects SHALL render a "View all projects" link to `/projects`.
5. THE FeaturedProjects SHALL render project cards in the order returned by `selectFeaturedProjects`.
6. THE FeaturedProjects SHALL render each project title as a heading one level below the Section_Heading (`h3`).
7. THE FeaturedProjects SHALL render no repository, demo, or documentation link, because those actions belong to the M6 project detail route.

#### Verification Steps

1. Render FeaturedProjects with three fixtures; assert three cards, each with title link `href="/projects/{slug}"`, a status badge, and technology tags.
2. Assert one `h2` and three `h3` elements in the section.
3. Assert the "View all projects" link `href="/projects"` is present.
4. Run Axe_Check; confirm zero violations.

---

### Requirement 7: FeaturedProjects Empty State

**User Story:**
As a visitor, I want the homepage to remain usable when no project is featured, so that I can still navigate the site.

#### Acceptance Criteria

1. IF `selectFeaturedProjects` returns an empty array, THEN THE FeaturedProjects SHALL render the Section_Heading and the M3 `EmptyState` with a plain-language message (`APP_FLOW.md` Story 1.1).
2. IF `selectFeaturedProjects` returns an empty array, THEN THE FeaturedProjects SHALL retain the "View all projects" link to `/projects`.
3. IF `selectFeaturedProjects` returns an empty array, THEN THE Homepage SHALL continue rendering every other section and the M4 navigation without layout breakage.
4. THE FeaturedProjects empty state SHALL be exposed to assistive technology as text content within the section.

#### Verification Steps

1. Render FeaturedProjects with an empty array; assert the `EmptyState` message and the "View all projects" link.
2. Render the full Homepage with zero projects; assert HeroSection and RecentActivity still render.
3. Run Axe_Check on the empty-state Homepage; confirm zero violations.

---

### Requirement 8: Skills Snapshot Derivation

**User Story:**
As a recruiter, I want a compact view of core technologies backed by real project evidence, so that skills claims are credible.

#### Acceptance Criteria

1. THE `deriveSkillGroups` Selection_Helper SHALL derive Skill_Groups exclusively from the `technologies` field of the `Project` entries passed to it.
2. THE `deriveSkillGroups` Selection_Helper SHALL list each distinct technology name once per result, comparing names case-insensitively and retaining the first-seen spelling.
3. THE `deriveSkillGroups` Selection_Helper SHALL order technologies within a Skill_Group by descending count of projects that list the technology, with ties ordered alphabetically.
4. THE `deriveSkillGroups` Selection_Helper SHALL return an empty array WHEN the input contains no technologies.
5. THE `deriveSkillGroups` Selection_Helper SHALL NOT add any technology name that is absent from the input.
6. FOR ALL generated inputs, THE set of technology names in the result, compared case-insensitively, SHALL equal the set of technology names in the input (invariant).
7. THE `deriveSkillGroups` Selection_Helper SHALL NOT mutate its input.

#### Verification Steps

1. Write a Property_Test asserting the case-insensitive name set of the result equals that of the input, with no duplicates.
2. Write a Property_Test asserting count-descending, alphabetical-tie ordering and input immutability.
3. Write an example test with empty input asserting an empty result.

---

### Requirement 9: SkillsSnapshot Section Rendering

**User Story:**
As a recruiter, I want skills presented as compact groups, so that I can scan them in seconds.

#### Acceptance Criteria

1. THE SkillsSnapshot SHALL render a Section_Heading as an `h2` element.
2. THE SkillsSnapshot SHALL render each Skill_Group with a visible group label and an M3 `TagList` of its technologies.
3. THE SkillsSnapshot SHALL render the technologies from `getProjects()` results across all non-featured and featured projects.
4. IF `deriveSkillGroups` returns an empty array, THEN THE Homepage SHALL omit the SkillsSnapshot section including its Section_Heading.
5. THE SkillsSnapshot SHALL NOT render any skill name, proficiency level, rating, or percentage that is absent from project data.
6. THE SkillsSnapshot SHALL render as a server component using Semantic_Tokens only.

#### Verification Steps

1. Render SkillsSnapshot with fixture groups; assert one `h2`, group labels, and tags matching the fixture.
2. Render the Homepage with projects whose `technologies` are empty or with zero projects; assert no SkillsSnapshot heading.
3. Search `src/components/home/SkillsSnapshot.tsx` for string literals naming technologies; confirm zero matches.

---

### Requirement 10: Certifications Preview

**User Story:**
As a recruiter, I want a short preview of certifications with a path to the full list, so that I can verify credentials without leaving the homepage first.

#### Acceptance Criteria

1. THE `selectCertificationPreview` Selection_Helper SHALL return at most 3 `Certification` entries ordered by `displayOrder` ascending.
2. WHEN two certifications share the same `displayOrder`, THE `selectCertificationPreview` Selection_Helper SHALL order them by `slug` ascending.
3. THE `selectCertificationPreview` Selection_Helper SHALL NOT mutate its input.
4. THE CertificationsPreview SHALL render a Section_Heading as an `h2` element, one M3 `Card` per selected certification showing title, issuer, and issue date through the Date_Formatter, and a "View all certifications" link to `/certifications`.
5. THE CertificationsPreview SHALL render only fields present in the `Certification` data and SHALL NOT render a credential ID, verification link, or badge image.
6. IF `selectCertificationPreview` returns an empty array, THEN THE Homepage SHALL omit the CertificationsPreview section including its Section_Heading.

#### Verification Steps

1. Write a Property_Test asserting result length is at most 3, `displayOrder` is non-decreasing, and every entry exists in the input.
2. Render CertificationsPreview with fixtures; assert titles, issuers, formatted dates, and the `/certifications` link.
3. Render the Homepage with zero certifications; assert no CertificationsPreview heading.

---

### Requirement 11: Recent Activity Selection and Rendering

**User Story:**
As a visitor, I want to see Angelo's latest community and learning activity, so that I can see current engagement.

#### Acceptance Criteria

1. THE `selectRecentPosts` Selection_Helper SHALL return only Published_Posts.
2. THE `selectRecentPosts` Selection_Helper SHALL order the result by `publishedAt` descending.
3. THE `selectRecentPosts` Selection_Helper SHALL return at most 3 entries.
4. WHEN two Published_Posts share the same `publishedAt`, THE `selectRecentPosts` Selection_Helper SHALL order them by `slug` ascending.
5. THE `selectRecentPosts` Selection_Helper SHALL NOT mutate its input.
6. THE RecentActivity SHALL render a Section_Heading as an `h2` element and, for each selected post, a compact item showing the title as a link to `/blog/{slug}`, the `publishedAt` date through the Date_Formatter, the M3 `EventTypeBadge`, and the `summary`.
7. THE RecentActivity SHALL render a "View all posts" link to `/blog`.
8. IF `selectRecentPosts` returns an empty array, THEN THE Homepage SHALL omit the RecentActivity section including its Section_Heading (`APP_FLOW.md` Story 1.1, option-driven).
9. THE Homepage SHALL exclude every post with `draft: true` from RecentActivity (`AGENTS.md` 5.4).

#### Verification Steps

1. Write a Property_Test asserting every result entry has `draft: false`, length is at most 3, `publishedAt` is non-increasing, and every entry exists in the input.
2. Write a Property_Test asserting idempotence and input immutability.
3. Render RecentActivity with three fixtures; assert title links `href="/blog/{slug}"`, badges, dates, summaries, and the `/blog` link.
4. Render the Homepage with only draft posts; assert no RecentActivity heading.

---

### Requirement 12: Deterministic Date Formatting

**User Story:**
As a maintainer, I want dates rendered identically on every build and machine, so that static output and tests are reproducible.

#### Acceptance Criteria

1. THE Date_Formatter SHALL convert an `IsoDateString` in `YYYY-MM-DD` format to display text using a fixed locale and the UTC time zone.
2. THE Date_Formatter SHALL return identical output for identical input regardless of system locale, system time zone, and current time.
3. THE Home_Component set SHALL render each date inside a `time` element whose `datetime` attribute equals the source `IsoDateString`.
4. IF the Date_Formatter receives a string that is not a valid `YYYY-MM-DD` date, THEN THE Date_Formatter SHALL throw an error naming the received value.
5. WHERE a Date_Formatter already exists in the M3 or M2 modules, THE M5 implementation SHALL reuse it instead of creating another.

#### Verification Steps

1. Write a Property_Test over generated valid dates asserting the output is stable across repeated calls and when `TZ` is set to different values.
2. Write an example test asserting `"2026-04-10"` produces the same text under `TZ=UTC` and `TZ=Asia/Manila`.
3. Assert each rendered date has a `time` element with a matching `datetime`.
4. Assert an invalid string such as `"2026-13-40"` throws.

---

### Requirement 13: Homepage Metadata

**User Story:**
As a visitor arriving from search or a shared link, I want accurate page metadata, so that the homepage is described correctly.

#### Acceptance Criteria

1. THE Homepage SHALL export Next.js metadata that provides a title, a description, a canonical URL, and Open Graph title, description, and URL.
2. THE Homepage SHALL derive the description from `SiteConfig.profile.introduction` and the title from `SiteConfig.profile.name` and `SiteConfig.profile.professionalTitle`.
3. THE Homepage SHALL derive the canonical URL and Open Graph URL from `SiteConfig.siteUrl`.
4. THE Homepage SHALL apply the M4 title template without duplicating the site name in the rendered `title` text.
5. THE Homepage SHALL NOT hardcode metadata strings that duplicate `content/site.json` values.
6. IF `SiteConfig.siteUrl` is not an absolute `https://` URL, THEN THE build SHALL fail through M2 loader validation.

#### Verification Steps

1. Call the metadata function with a fixture `SiteConfig`; assert title, description, canonical, and Open Graph fields.
2. Assert the canonical URL equals `SiteConfig.siteUrl` for the root path.
3. Search `src/app/page.tsx` for literals matching `content/site.json` values; confirm zero matches.

---

### Requirement 14: Semantic Structure and Accessibility

**User Story:**
As a visitor using assistive technology, I want a clear heading and landmark structure, so that I can navigate the homepage by section.

#### Acceptance Criteria

1. THE Homepage SHALL contain exactly one `h1` element, located in the HeroSection.
2. THE Homepage SHALL render each rendered section as a `section` element labelled by its Section_Heading through `aria-labelledby`.
3. THE Homepage SHALL render headings in a hierarchy that skips no level.
4. THE Home_Component set SHALL render every interactive element with the M3 `FOCUS_RING` and a visible focus indicator.
5. THE Home_Component set SHALL render link text that identifies its destination without relying on surrounding context.
6. WHILE Reduced_Motion is active, THE Home_Component set SHALL suppress non-essential motion through the M3 motion helpers.
7. THE Home_Component set SHALL meet the WCAG 2.2 AA contrast ratios defined in `design.md` by using only Semantic_Tokens.
8. THE Home_Component set SHALL use Semantic_Tokens and SHALL NOT contain Hardcoded_Design_Values.

#### Verification Steps

1. Render the full Homepage; assert one `h1`, `section` elements with valid `aria-labelledby`, and no skipped heading levels.
2. Run Axe_Check on the full Homepage in the populated and empty-data states; confirm zero violations.
3. Search `src/components/home/` for hex colors, arbitrary Tailwind values, and raw durations; confirm zero matches.
4. Tab through the rendered Homepage; confirm every interactive element shows the focus indicator.

---

### Requirement 15: Responsive Layout

**User Story:**
As a visitor on any device, I want the homepage to adapt to my screen, so that content stays readable without horizontal scrolling.

#### Acceptance Criteria

1. THE Home_Component set SHALL constrain content width and horizontal padding with the M3 `Container`.
2. WHILE the viewport is at the Mobile Breakpoint, THE FeaturedProjects, CertificationsPreview, and RecentActivity SHALL render items in a single column.
3. WHILE the viewport is at the Tablet Breakpoint, THE FeaturedProjects and CertificationsPreview SHALL render items in two columns.
4. WHILE the viewport is at the Desktop or Wide Desktop Breakpoint, THE FeaturedProjects and CertificationsPreview SHALL render items in up to three columns.
5. THE Homepage SHALL render without horizontal scrolling at viewport widths of 375px, 768px, 1024px, and 1440px.
6. THE Home_Component set SHALL implement responsive behavior with Tailwind responsive utilities and Semantic_Tokens, without client-side JavaScript.

#### Verification Steps

1. Assert the responsive column utility classes on each section grid in the rendered markup.
2. Inspect the Homepage at 375px, 768px, 1024px, and 1440px; confirm no horizontal overflow.
3. Confirm no Home_Component imports `useState`, `useEffect`, or `matchMedia`.

---

### Requirement 16: Scope Boundaries and Composition Discipline

**User Story:**
As the system architect, I want M5 to compose existing foundations without changing them, so that earlier milestones stay stable.

#### Acceptance Criteria

1. THE M5 implementation SHALL import UI_Primitives from `src/components/ui/` and SHALL NOT redefine or modify them.
2. THE M5 implementation SHALL NOT modify Semantic_Token definitions, `src/components/layout/`, or `src/content/` modules.
3. THE M5 implementation SHALL NOT create API routes, route handlers, server actions, projects, certifications, or blog route files, filters, search, or a resume download.
4. THE M5 implementation SHALL NOT add dependencies, analytics, cookies, forms, or third-party scripts.
5. THE M5 implementation SHALL NOT modify `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, or CI configuration without human approval (`AGENTS.md` 6.2).
6. THE M5 implementation SHALL separate Selection_Helpers from Home_Components so that each Selection_Helper is importable and testable without rendering.
7. THE M5 implementation SHALL contain no `any`, implicit `any`, non-null assertions, or unjustified type assertions (`AGENTS.md` 6.1).
8. THE M5 implementation SHALL keep each Home_Component file below 300 lines.

#### Verification Steps

1. Run `git diff --stat` against the M4 baseline; confirm changes only in `src/app/page.tsx`, `src/components/home/`, Selection_Helper modules, and `tests/`.
2. Confirm `package.json` and lockfiles are unchanged.
3. Search the M5 files for `any`, `!.`, and `as ` casts; confirm each match is justified or absent.
4. Import each Selection_Helper in a test without rendering any component; confirm it runs.
5. Run `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`; confirm all pass (`AGENTS.md` 7.3).
