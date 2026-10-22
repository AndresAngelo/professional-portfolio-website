# Requirements Document

> **Spec:** M6 Projects Module  
> **Document Status:** Draft  
> **Feature Name:** m6-projects-module  
> **Milestone:** M6  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 3, 4.2, 5.2, 6), `PRD.md` (Projects Index, Project Detail, P0), `design.md` (Sections 4, 5, 6.2), `TRD.md` (Section 3.3 state management), `APP_FLOW.md` (Flow 2.0, Stories 2.1, 2.2, `SCR-02`, `SCR-03`), `implementation_plan.md` (Projects tasks)  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 6 (M6) implements the Projects module for `personal-website-portfolio-v2`: the projects index route `src/app/projects/page.tsx` (`SCR-02`), the project detail route `src/app/projects/[slug]/page.tsx` (`SCR-03`), the components in `src/components/projects/`, and the pure helpers that filter projects, derive filter options, parse filter state, and select related projects.

M6 reads projects through `getProjects()` and `getProjectBySlug()` and renders documentation through `renderMarkdown`, all from the M2 loaders. M6 composes the M3 UI_Primitives (`Card`, `TagList`, `StatusBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`) and the M4 shell (`main#main-content`, title template, `not-found`). M6 follows the M5 pure-helper pattern (`src/lib/home/`) and reuses the M5 Date_Formatter. M6 does not modify any design token, UI_Primitive, Layout_Component, or Home_Component.

The site is statically generated. The full unfiltered project list is present in the static HTML of `/projects`. A minimal client island reads URL search parameters to apply filters after hydration, wrapped in `Suspense` as Next.js requires for `useSearchParams` under static export. This island is the only client JavaScript M6 adds, and it is justified under `AGENTS.md` 6.2 because filtering needs interactive state that a server component cannot provide.

M6 does NOT implement certifications or blog routes (M7, M8), search (P1), performance tuning or deployment (M9, M10), dark mode, API routes, analytics, forms, project JSON-LD (M9 or later), or new dependencies without human approval.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Projects_Index** | The route `/projects` rendered by `src/app/projects/page.tsx` (`SCR-02`). |
| **Project_Detail** | The route `/projects/[slug]` rendered by `src/app/projects/[slug]/page.tsx` (`SCR-03`). |
| **Project_Component** | A component in `src/components/projects/`. |
| **ProjectsIndex** | Project_Component that composes the page heading, ProjectFilterBar, and ProjectGrid. |
| **ProjectsExplorer** | The client island (`'use client'`) that reads URL search parameters and renders the ProjectFilterBar, result-count live region, and ProjectGrid. |
| **ProjectFilterBar** | Project_Component rendering the technology and status `FilterChip` groups and the "Clear filters" action. |
| **ProjectGrid** | Project_Component rendering ProjectCards in a responsive grid. |
| **ProjectCard** | Project_Component rendering one project summary using the M3 `Card`. |
| **ProjectHeader** | Project_Component rendering the detail `h1`, StatusBadge, role, and timeline. |
| **ProjectMetadata** | Project_Component rendering technologies, tags, and metrics. |
| **ProjectLinks** | Project_Component rendering repository, live-demo, and documentation links. |
| **BuildDocumentation** | Project_Component rendering project documentation Markdown through `MarkdownDoc`. |
| **RelatedProjects** | Project_Component rendering up to Related_Limit related project cards. |
| **ProjectFilters** | The type `{ technology: string \| null; status: ProjectStatus \| null }` defined in `AGENTS.md` 4.2. |
| **Filter_Helper** | A pure function in `src/lib/projects/`: `parseProjectFilters`, `filterProjects`, `deriveFilterOptions`, `serializeProjectFilters`. |
| **Related_Helper** | The pure function `selectRelatedProjects` in `src/lib/projects/`. |
| **Technology_Option** | A distinct technology name derived from `Project.technologies`, deduplicated case-insensitively, displayed with the spelling of its first occurrence in M2 sort order. |
| **Status_Option** | A `ProjectStatus` value held by at least one project. |
| **Filter_Param** | A URL search parameter: `technology` (Technology_Option name) or `status` (`ProjectStatus`). |
| **Filter_Semantics** | At most one technology and at most one status are active; a project matches when it satisfies every active filter (logical AND). |
| **Unfiltered_State** | The state in which both `ProjectFilters` fields are `null`. |
| **Related_Limit** | The maximum number of related projects: 3. |
| **Result_Announcement** | Text in an `aria-live="polite"` region stating the number of displayed projects. |
| **Date_Formatter** | The deterministic M5 function that converts an `IsoDateString` to display text without reading the system locale or time zone. |
| **Project_Sort_Order** | The M2 `getProjects()` order: `displayOrder` ascending, then `startedAt` descending, then `slug` ascending. |
| **Section_Heading** | An `h2` element that titles a page section. |
| **UI_Primitive** | A reusable M3 component in `src/components/ui/`. |
| **Semantic_Token** | A named design value from `design.md` Section 3, exposed by M1 through Tailwind and CSS custom properties. |
| **Hardcoded_Design_Value** | A raw hex color, arbitrary pixel size, arbitrary shadow, or arbitrary duration written directly in a component. |
| **Breakpoints** | Mobile `375px–767px`, Tablet `768px–1023px`, Desktop `1024px–1439px`, Wide Desktop `1440px+` (`design.md` 5.1). |
| **Axe_Check** | An automated accessibility test run against rendered components using an axe-core based tool. |
| **Property_Test** | A fast-check test asserting a helper property over generated inputs. |
| **Reduced_Motion** | The user preference exposed by the `prefers-reduced-motion: reduce` media query. |

---

## Requirements

---

### Requirement 1: Projects Index Route and Composition

**User Story:**
As a visitor, I want a projects index page, so that I can browse all of Angelo's published projects in one place.

#### Acceptance Criteria

1. THE Projects_Index SHALL be served at `/projects` by `src/app/projects/page.tsx` as a static server component with no dynamic route segment.
2. THE Projects_Index SHALL obtain projects by calling `getProjects()` from the M2 loader module and SHALL pass the result to Project_Components through props typed with types imported from the M2 schemas.
3. THE Projects_Index SHALL render one `h1` containing the text "Projects" followed by the ProjectFilterBar and the ProjectGrid, inside the M4 Main_Landmark.
4. THE Projects_Index SHALL render no `header`, `footer`, or `main` element, because the M4 Root_Layout owns those landmarks.
5. THE M6 implementation SHALL NOT redeclare `Project`, `ProjectFrontmatter`, `ProjectStatus`, or `ProjectFilters` (`AGENTS.md` 6.3).
6. THE Projects_Index SHALL read no data from the network at render time.
7. WHERE `getProjects()` returns zero projects, THE Projects_Index SHALL render the M3 `EmptyState` with a message that projects are being prepared and SHALL omit the ProjectFilterBar (`APP_FLOW.md` Flow 2.0 step 2.1).

#### Verification Steps

1. Render the Projects_Index with three fixture projects; assert one `h1` named "Projects", the filter bar, and three project cards.
2. Render with an empty array; assert the `EmptyState` message is present and no filter chips are present.
3. Assert `src/app/projects/page.tsx` contains no `'use client'` directive and imports no type declaration redefining `Project`.

---

### Requirement 2: Project Card Content and Ordering

**User Story:**
As a hiring manager, I want each project card to show its key facts, so that I can decide which projects to open.

#### Acceptance Criteria

1. THE ProjectCard SHALL render the project `title` as a link to `/projects/{slug}` inside an M3 `Card`.
2. THE ProjectCard SHALL render the project `summary`, the M3 `StatusBadge` for the project `status`, and the project `role`.
3. THE ProjectCard SHALL render at most 4 technologies through the M3 `TagList`, in the order stored in `Project.technologies`.
4. WHEN a project has more than 4 technologies, THE ProjectCard SHALL render a text indicator stating the count of omitted technologies.
5. THE ProjectCard SHALL render completion metadata as "Completed {date}" through the Date_Formatter WHEN `completedAt` is not `null`, and as "Started {date}" through the Date_Formatter WHEN `completedAt` is `null`.
6. THE ProjectCard SHALL render each date inside a `time` element whose `datetime` attribute equals the source `IsoDateString`.
7. THE ProjectCard SHALL render no repository, live-demo, or documentation link, because those actions belong to Project_Detail.
8. THE ProjectCard SHALL use the project `title` as the accessible name of its single primary link.
9. THE ProjectGrid SHALL render projects in Project_Sort_Order as returned by `getProjects()` and SHALL preserve that relative order after filtering.

#### Verification Steps

1. Render a fixture with six technologies; assert four tags and an indicator reading "+2 more".
2. Render fixtures with and without `completedAt`; assert "Completed" and "Started" text with matching `datetime` values.
3. Assert the card contains exactly one `a` element with `href="/projects/{slug}"` and no external links.
4. Render the ProjectGrid with sorted fixtures; assert DOM order matches input order, including after filtering.

---

### Requirement 3: Filter State Parsing and Serialization

**User Story:**
As a visitor, I want filters stored in the URL, so that I can share or reload a filtered view and use the Back button.

#### Acceptance Criteria

1. THE `parseProjectFilters` Filter_Helper SHALL accept URL search parameters and the derived Technology_Options and Status_Options and SHALL return a `ProjectFilters` value.
2. WHEN the `technology` Filter_Param equals a Technology_Option name compared case-insensitively, THE `parseProjectFilters` Filter_Helper SHALL return that Technology_Option's canonical name as `technology`.
3. IF the `technology` Filter_Param matches no Technology_Option, THEN THE `parseProjectFilters` Filter_Helper SHALL return `technology: null` (`APP_FLOW.md` Flow 2.0 step 2.3).
4. IF the `status` Filter_Param is not a Status_Option, THEN THE `parseProjectFilters` Filter_Helper SHALL return `status: null`.
5. IF a Filter_Param is repeated, THEN THE `parseProjectFilters` Filter_Helper SHALL use its first occurrence.
6. THE `serializeProjectFilters` Filter_Helper SHALL convert a `ProjectFilters` value to a query string that contains a Filter_Param only for each non-`null` field and is the empty string in the Unfiltered_State.
7. FOR ALL valid `ProjectFilters` values drawn from the available options, parsing the serialized value SHALL return an equal `ProjectFilters` value (round-trip property).
8. THE `parseProjectFilters` and `serializeProjectFilters` Filter_Helpers SHALL NOT mutate their inputs and SHALL ignore unrelated search parameters.

#### Verification Steps

1. Write a Property_Test asserting `parseProjectFilters(serializeProjectFilters(f)) equals f` for generated valid filters.
2. Write a Property_Test asserting arbitrary string values for `technology` and `status` never yield a value outside the available options.
3. Unit-test repeated parameters, mixed-case technology values, and unrelated parameters.

---

### Requirement 4: Filter Options Derivation

**User Story:**
As a visitor, I want filter chips that reflect the real project data, so that every chip leads to at least one result.

#### Acceptance Criteria

1. THE `deriveFilterOptions` Filter_Helper SHALL return Technology_Options derived from the `technologies` field of all input projects, deduplicated case-insensitively and sorted alphabetically using a case-insensitive comparison.
2. THE `deriveFilterOptions` Filter_Helper SHALL return Status_Options containing only `ProjectStatus` values held by at least one input project, in the order `completed`, `in-progress`, `archived`.
3. FOR ALL input arrays, THE case-insensitive set of Technology_Options SHALL equal the case-insensitive set of all technology names across the input projects, with no duplicates.
4. THE `deriveFilterOptions` Filter_Helper SHALL NOT mutate its input.
5. WHERE the Status_Options contain a single value, THE ProjectFilterBar SHALL omit the status chip group.
6. WHEN the input array is empty, THE `deriveFilterOptions` Filter_Helper SHALL return empty Technology_Options and empty Status_Options.

#### Verification Steps

1. Write a Property_Test asserting option-set equality, no duplicates, and sorted order for generated project arrays.
2. Unit-test that an `archived`-free dataset renders no "Archived" chip.
3. Render the ProjectFilterBar with a single-status dataset; assert the status group is absent.

---

### Requirement 5: Project Filtering Logic

**User Story:**
As a hiring manager, I want to filter projects by technology and status, so that I can find relevant engineering experience (`APP_FLOW.md` Story 2.1).

#### Acceptance Criteria

1. WHEN `filterProjects` receives `ProjectFilters` in the Unfiltered_State, THE `filterProjects` Filter_Helper SHALL return all input projects.
2. WHEN `ProjectFilters.technology` is not `null`, THE `filterProjects` Filter_Helper SHALL return only projects whose `technologies` contain that name compared case-insensitively.
3. WHEN `ProjectFilters.status` is not `null`, THE `filterProjects` Filter_Helper SHALL return only projects whose `status` equals that value.
4. WHEN both fields are not `null`, THE `filterProjects` Filter_Helper SHALL return only projects satisfying both conditions (Filter_Semantics).
5. FOR ALL input arrays and filters, THE result SHALL be contained in the input and applying `filterProjects` to its own result with the same filters SHALL return an equal result (idempotence).
6. FOR ALL input arrays and filters, adding a non-`null` filter to a `ProjectFilters` value SHALL return a result that is a subset of the previous result (monotonicity).
7. THE `filterProjects` Filter_Helper SHALL NOT mutate its input, SHALL NOT reorder its result relative to the input, and SHALL NOT match tags, titles, or summaries.

#### Verification Steps

1. Write Property_Tests for containment, idempotence, monotonicity, and the AND semantics against a model implementation.
2. Unit-test case-insensitive technology matching.

---

### Requirement 6: Filter Bar Interaction and Accessibility

**User Story:**
As a keyboard or screen reader user, I want operable filter controls with clear state, so that I can filter projects without a mouse.

#### Acceptance Criteria

1. THE ProjectFilterBar SHALL render a technology chip group and a status chip group, each wrapped in a `group` role element with an accessible label ("Filter by technology", "Filter by status"), using the M3 `FilterChip`.
2. THE ProjectFilterBar SHALL expose each chip as a `button` element with `aria-pressed` equal to `true` for the active chip and `false` otherwise.
3. WHILE a filter is active, THE ProjectFilterBar SHALL render the matching chip with the M3 `FilterChip` active visual state that does not rely on color alone (`APP_FLOW.md` Story 2.1, state-driven).
4. WHEN the visitor activates an inactive chip, THE ProjectsExplorer SHALL set that group's filter to the chip's value and SHALL clear no other group's filter.
5. WHEN the visitor activates the active chip, THE ProjectsExplorer SHALL set that group's filter to `null`.
6. WHEN the visitor activates a chip, THE ProjectsExplorer SHALL update the URL search parameters with `router.replace` and `scroll: false`, without a full page reload.
7. WHILE at least one filter is active, THE ProjectFilterBar SHALL render a "Clear filters" `Button`.
8. WHEN the visitor activates "Clear filters", THE ProjectsExplorer SHALL remove the `technology` and `status` Filter_Params, preserve unrelated search parameters, and return keyboard focus to the first chip of the ProjectFilterBar.
9. THE ProjectFilterBar SHALL make every chip reachable in document order by the Tab key and activatable by the Enter key and the Space key.
10. THE ProjectFilterBar SHALL render the M3 `FOCUS_RING` on every chip and on the "Clear filters" action.

#### Verification Steps

1. Render the ProjectsExplorer with a mocked router; click a technology chip; assert `aria-pressed="true"` and the expected `replace` call.
2. Click the active chip; assert the Filter_Param is removed.
3. Use `userEvent.tab()` and keyboard activation to operate every chip.
4. Run an Axe_Check on the ProjectFilterBar in default and active states.

---

### Requirement 7: Static Rendering and Client Island

**User Story:**
As a visitor with slow or disabled JavaScript, I want the full project list in the initial HTML, so that I can read projects before filters become interactive.

#### Acceptance Criteria

1. THE Projects_Index SHALL render the ProjectsExplorer inside a React `Suspense` boundary.
2. THE Suspense fallback SHALL render the full unfiltered ProjectGrid, so that the static HTML of `/projects` contains every project card.
3. THE ProjectsExplorer SHALL be the only module under `src/components/projects/` that contains a `'use client'` directive and calls `useSearchParams`.
4. THE ProjectsExplorer SHALL receive the full project list as serializable props from the server component.
5. THE Projects_Index SHALL build without a "missing Suspense boundary with useSearchParams" error under the project's static export configuration.
6. THE ProjectsExplorer SHALL pass only serializable fields needed for card rendering and SHALL NOT pass the `documentation` field to the client.
7. THE M6 implementation SHALL NOT add a dependency to implement filtering.

#### Verification Steps

1. Run `npm run build`; assert exit code 0 and inspect `out/projects.html` or `.next/server/app/projects.html` for every fixture project title.
2. Assert via grep that `'use client'` appears in only the ProjectsExplorer module and any chip wrapper required by it.
3. Inspect the ProjectsExplorer props type; assert it excludes `documentation`.

---

### Requirement 8: Empty Result State and Result Announcement

**User Story:**
As a visitor, I want clear feedback when filters match nothing or change the results, so that I understand what is displayed.

#### Acceptance Criteria

1. IF the filtered result is empty, THEN THE ProjectsExplorer SHALL render the M3 `EmptyState` with a message stating that no projects match the selected filters and a "Clear filters" `Button` (`APP_FLOW.md` Story 2.1, exception).
2. WHEN the filtered result changes, THE ProjectsExplorer SHALL update a Result_Announcement to the text "{n} project(s) shown", using "1 project shown" for a count of 1.
3. THE Result_Announcement SHALL be rendered in an element with `aria-live="polite"` that is present in the DOM before the first filter change.
4. THE Result_Announcement SHALL be visible text and SHALL NOT be hidden from sighted users.
5. WHEN the "Clear filters" `Button` in the `EmptyState` is activated, THE ProjectsExplorer SHALL behave as specified in Requirement 6, criterion 8.
6. IF the empty-state "Clear filters" action is activated, THEN THE ProjectsExplorer SHALL move keyboard focus to the first chip of the ProjectFilterBar so that focus is not lost on a removed element.

#### Verification Steps

1. Apply filters that match no fixture; assert the `EmptyState` text and the "Clear filters" button.
2. Assert the live region text for counts 0, 1, and 3, and that its container exists at first render.
3. Activate "Clear filters" from the empty state; assert `document.activeElement` is the first chip.

---

### Requirement 9: Project Detail Route and Static Generation

**User Story:**
As a technical evaluator, I want each project to have its own page, so that I can review the case study at a stable URL.

#### Acceptance Criteria

1. THE Project_Detail SHALL be served at `/projects/{slug}` by `src/app/projects/[slug]/page.tsx` as a static server component with no `'use client'` directive.
2. THE Project_Detail SHALL export `generateStaticParams` that returns one `{ slug }` entry per project returned by `getProjects()`.
3. THE Project_Detail SHALL export `dynamicParams = false`.
4. THE Project_Detail SHALL obtain the project by calling `getProjectBySlug(slug)` from the M2 loader module.
5. IF `getProjectBySlug` returns no project for the requested slug, THEN THE Project_Detail SHALL call `notFound()` so that the M4 `not-found` boundary renders (`APP_FLOW.md` Flow 2.0 step 2.6).
6. THE Project_Detail SHALL render ProjectHeader, ProjectMetadata, ProjectLinks, BuildDocumentation, and RelatedProjects inside the M4 Main_Landmark, with the ProjectHeader first and the RelatedProjects last.
7. THE Project_Detail SHALL render the project `summary` as visible text below the ProjectHeader.
8. THE Project_Detail SHALL render no `header`, `footer`, or `main` element.

#### Verification Steps

1. Call `generateStaticParams` with fixture loaders; assert the slug list equals the fixture slugs.
2. Assert `dynamicParams` equals `false`.
3. Render the page with an unknown slug; assert `notFound` is invoked.
4. Run `npm run build`; assert one HTML file per project slug.

---

### Requirement 10: Project Header and Timeline

**User Story:**
As a technical evaluator, I want to see a project's title, status, role, and timeline at the top, so that I can orient myself quickly.

#### Acceptance Criteria

1. THE ProjectHeader SHALL render exactly one `h1` containing the project `title`.
2. THE ProjectHeader SHALL render the M3 `StatusBadge` for the project `status` and the project `role` as visible text.
3. THE ProjectHeader SHALL render the start date through the Date_Formatter inside a `time` element whose `datetime` attribute equals `startedAt`.
4. WHEN `completedAt` is not `null`, THE ProjectHeader SHALL render the completion date through the Date_Formatter inside a `time` element whose `datetime` attribute equals `completedAt`, labeled "Completed".
5. WHILE `completedAt` is `null`, THE ProjectHeader SHALL render the timeline as "Started {date}" and SHALL NOT render a completion date or a fabricated end date.
6. WHERE a Date_Formatter exists from M5, THE M6 implementation SHALL reuse it instead of creating another.
7. IF the Date_Formatter receives an invalid date string, THEN THE Date_Formatter SHALL throw an error naming the received value.

#### Verification Steps

1. Render with `completedAt` set and `null`; assert timeline text and `datetime` attributes.
2. Assert the heading outline contains one `h1`.
3. Property-test that header date output is stable under different `TZ` values.

---

### Requirement 11: Project Metadata and Metrics

**User Story:**
As a hiring manager, I want technologies, tags, and measured outcomes in one place, so that I can assess project scope.

#### Acceptance Criteria

1. THE ProjectMetadata SHALL render all `technologies` through the M3 `TagList` under a labeled "Technologies" heading or label.
2. WHERE `tags` is non-empty, THE ProjectMetadata SHALL render all `tags` through the M3 `TagList` under a "Tags" label.
3. WHERE `tags` is empty, THE ProjectMetadata SHALL omit the "Tags" label and list.
4. WHERE `metrics` is non-empty, THE ProjectMetadata SHALL render each metric as a term and description pair in a `dl` element, in stored order, with `label` as the term and `value` as the description.
5. WHERE `metrics` is empty, THE ProjectMetadata SHALL omit the metrics list and its label.
6. THE ProjectMetadata SHALL render metric values as supplied text and SHALL NOT compute, round, or fabricate metrics.

#### Verification Steps

1. Render with metrics and tags; assert `dl` entries match the fixture order.
2. Render with empty `tags` and `metrics`; assert both labels are absent.

---

### Requirement 12: Project Links

**User Story:**
As a technical evaluator, I want working links to the repository, live demo, and documentation, so that I can inspect the evidence.

#### Acceptance Criteria

1. WHERE `repositoryUrl` is not `null` and not empty, THE ProjectLinks SHALL render an M3 `ExternalLink` labeled "Repository" with that URL.
2. WHERE `liveDemoUrl` is not `null` and not empty, THE ProjectLinks SHALL render an M3 `ExternalLink` labeled "Live demo" with that URL (`APP_FLOW.md` Story 2.2).
3. WHERE `documentationUrl` is not `null` and not empty, THE ProjectLinks SHALL render an M3 `ExternalLink` labeled "Documentation" with that URL.
4. IF a URL field is `null`, empty, or omitted, THEN THE ProjectLinks SHALL omit the corresponding link and SHALL render no disabled, placeholder, or `href="#"` link (`AGENTS.md` 6.1 rule 9).
5. IF all three URL fields are `null`, empty, or omitted, THEN THE ProjectLinks SHALL render no element, including its heading.
6. THE ProjectLinks SHALL open external destinations through the M3 `ExternalLink` behavior, including `rel="noopener noreferrer"` and an accessible indication that the link opens externally.
7. THE ProjectLinks SHALL give each link an accessible name that is unique within the page.

#### Verification Steps

1. Render with all three URLs; assert three links with the expected `href` values.
2. Render with all `null`; assert the ProjectLinks container is absent.
3. Render with only `repositoryUrl`; assert no "Live demo" element and no `href="#"` anchor.

---

### Requirement 13: Build Documentation Rendering

**User Story:**
As a technical evaluator, I want readable build documentation, so that I can assess implementation decisions (`APP_FLOW.md` Story 2.2).

#### Acceptance Criteria

1. THE BuildDocumentation SHALL render the project `documentation` through the M2 `renderMarkdown` function and the M3 `MarkdownDoc` component.
2. THE BuildDocumentation SHALL render a Section_Heading as an `h2` with the text "Build documentation" before the rendered Markdown, wrapped in a `section` element with `aria-labelledby` referencing that heading.
3. THE BuildDocumentation SHALL render headings inside the Markdown content starting at `h2`, such that no `h1` appears in rendered documentation and the page heading hierarchy has no skipped levels.
4. IF the rendered documentation contains an `h1`, THEN THE BuildDocumentation SHALL demote the heading levels in the rendered output by one level.
5. THE BuildDocumentation SHALL render no raw HTML from the Markdown source beyond what the M2 sanitization allows.
6. THE Project_Detail SHALL render the documentation as static HTML without client-side JavaScript.

#### Verification Steps

1. Render a fixture with `##` and `###` headings; assert heading levels in the output and one `h1` on the page.
2. Render a fixture containing a script tag in Markdown; assert it is not present in the output.
3. Run an Axe_Check on the full Project_Detail and assert no heading-order violation.

---

### Requirement 14: Related Projects

**User Story:**
As a visitor, I want to see similar projects at the end of a case study, so that I can continue exploring relevant work.

#### Acceptance Criteria

1. THE `selectRelatedProjects` Related_Helper SHALL accept the current project and all projects and SHALL return at most Related_Limit projects.
2. THE `selectRelatedProjects` Related_Helper SHALL exclude the current project and SHALL include only projects that share at least one technology with the current project compared case-insensitively.
3. THE `selectRelatedProjects` Related_Helper SHALL order results by shared technology count descending, then by `displayOrder` ascending, then by `slug` ascending.
4. FOR ALL inputs, THE result SHALL contain no duplicates, SHALL NOT contain the current project, and every entry SHALL exist in the input.
5. THE `selectRelatedProjects` Related_Helper SHALL NOT mutate its input.
6. WHERE `selectRelatedProjects` returns a non-empty array, THE RelatedProjects SHALL render a Section_Heading "Related projects" as an `h2` and one ProjectCard per result.
7. IF `selectRelatedProjects` returns an empty array, THEN THE Project_Detail SHALL omit the RelatedProjects section including its Section_Heading.

#### Verification Steps

1. Write a Property_Test asserting length at most 3, exclusion of the current project, shared-technology membership, no duplicates, and ordering by the specified keys.
2. Render a project with no shared technologies; assert no "Related projects" heading.

---

### Requirement 15: Detail Navigation, Metadata, and SEO

**User Story:**
As a visitor and search engine, I want clear navigation and accurate page metadata, so that I can return to the index and share project pages.

#### Acceptance Criteria

1. THE Project_Detail SHALL render a `nav` element with an accessible label "Breadcrumb" containing a link "Projects" to `/projects` followed by the current project `title` as non-link text with `aria-current="page"`.
2. THE Project_Detail SHALL render a "Back to projects" link to `/projects` after the BuildDocumentation.
3. THE Project_Detail SHALL export `generateMetadata` that returns, per project, a `title` equal to the project `title` (the M4 title template appends the site name), a `description` equal to the project `summary`, a canonical URL equal to `{siteUrl}/projects/{slug}`, and Open Graph `title`, `description`, `url`, and `type: "article"`.
4. THE Projects_Index SHALL export `metadata` with the title "Projects", a description of the portfolio projects of 50–160 characters, a canonical URL equal to `{siteUrl}/projects`, and Open Graph fields.
5. THE M6 metadata functions SHALL read `siteUrl` through `getSiteConfig()`.
6. THE canonical URL for `/projects` SHALL omit filter search parameters.
7. THE M6 implementation SHALL NOT emit JSON-LD structured data.
8. IF `generateMetadata` receives an unknown slug, THEN THE Project_Detail SHALL call `notFound()`.

#### Verification Steps

1. Call `generateMetadata` with a fixture project and `SiteConfig`; assert title, description, canonical, and Open Graph fields.
2. Assert the canonical URL for `/projects` contains no query string.
3. Render the detail page; assert the breadcrumb `nav`, `aria-current`, and the "Back to projects" link.

---

### Requirement 16: Design System, Responsive Layout, and Accessibility

**User Story:**
As a visitor on any device and with any ability, I want the Projects module to be readable, usable, and consistent with the rest of the site.

#### Acceptance Criteria

1. THE Project_Component set SHALL use Semantic_Tokens only and SHALL NOT contain Hardcoded_Design_Values.
2. THE ProjectGrid SHALL render 1 column at Mobile, 2 columns at Tablet, and 3 columns at Desktop and Wide Desktop, using Tailwind responsive utilities.
3. THE Project_Detail SHALL render a single-column layout at Mobile and Tablet and a content width limited by the M3 `Container` at Desktop and Wide Desktop, without horizontal page scrolling at 375px.
4. THE ProjectFilterBar SHALL wrap chips onto multiple lines at Mobile without horizontal scrolling.
5. THE Project_Component set SHALL render every interactive element with a touch target of at least 44px by 44px at Mobile.
6. THE Projects_Index and Project_Detail SHALL pass an Axe_Check with zero violations in default, filtered, and empty states.
7. THE Project_Component set SHALL render a heading hierarchy with one `h1` per page, Section_Headings as `h2`, and no skipped levels.
8. WHILE Reduced_Motion is active, THE Project_Component set SHALL suppress transitions and animations through the M3 motion helpers.
9. THE Project_Component set SHALL meet the WCAG 2.2 AA contrast thresholds defined by Semantic_Tokens for text and chip states.

#### Verification Steps

1. Grep Project_Components for hex colors, `px-[`, `shadow-[`, and `duration-[` patterns; assert zero matches.
2. Assert responsive column classes on the ProjectGrid markup.
3. Run Axe_Check on the index (default, filtered, empty) and a detail fixture.
4. Manually check 375px, 768px, 1024px, and 1440px layouts for overflow and touch targets.

---

### Requirement 17: Testing, Quality Gates, and Scope Boundaries

**User Story:**
As a maintainer, I want M6 verified and bounded, so that regressions and scope creep are caught early.

#### Acceptance Criteria

1. THE M6 implementation SHALL include Vitest unit tests for every Filter_Helper and the Related_Helper, React Testing Library tests for each Project_Component, and Axe_Checks for both routes.
2. THE M6 implementation SHALL include Property_Tests using fast-check with at least 100 runs for `parseProjectFilters`/`serializeProjectFilters` round-trip, `filterProjects`, `deriveFilterOptions`, and `selectRelatedProjects`.
3. THE M6 implementation SHALL place Filter_Helpers and the Related_Helper in `src/lib/projects/` as pure functions with no React, Next.js, or DOM imports.
4. THE M6 implementation SHALL keep each Project_Component file below 300 lines.
5. THE M6 implementation SHALL pass `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build` with zero errors.
6. THE M6 implementation SHALL NOT use `any`, implicit `any`, non-null assertions, or unjustified type assertions (`AGENTS.md` 6.1 rule 7).
7. THE M6 implementation SHALL NOT modify design tokens, UI_Primitives, Layout_Components, Home_Components, M2 loaders, `package.json`, lockfiles, `next.config.ts`, or `tsconfig.json`.
8. THE M6 implementation SHALL NOT add API routes, route handlers, server actions, analytics, cookies, forms, search, or dark mode.

#### Verification Steps

1. Run the four verification commands and confirm zero errors.
2. Run `git diff --stat` against the M5 baseline; confirm changes only in `src/app/projects/`, `src/components/projects/`, `src/lib/projects/`, and `tests/`.
3. Grep `src/lib/projects/` for `react`, `next`, and `document` imports; assert zero matches.
4. Count lines in each Project_Component file; assert each is below 300.

