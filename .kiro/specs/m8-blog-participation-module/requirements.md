# Requirements Document

> **Spec:** M8 Blog / Participation Module  
> **Document Status:** Draft  
> **Feature Name:** m8-blog-participation-module  
> **Milestone:** M8  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 3, 4.2, 5.1, 5.4, 6), `PRD.md` (Blog / Participation Log, P0), `design.md` (Sections 4.3, 4.4, 6.4), `TRD.md` (Section 3.3 state management), `APP_FLOW.md` (Flow 4.0 steps 4.1–4.5, Stories 4.x, `SCR-05`, `SCR-06`), `implementation_plan.md` (Blog tasks)  
> **Master Files Location:** `Artifacts/master-files/`  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 8 (M8) implements the Blog / Participation module for `personal-website-portfolio-v2`: the blog index route `src/app/blog/page.tsx` (`SCR-05`), the blog detail route `src/app/blog/[slug]/page.tsx` (`SCR-06`), the components in `src/components/blog/`, and the pure helpers in `src/lib/blog/` that parse and serialize filter state, derive tag options, filter posts, order posts, and select adjacent posts.

M8 reads posts through `getBlogPosts()` and `getBlogPostBySlug()` and renders post bodies through `renderMarkdown`, all from the M2 loaders. `getBlogPosts()` excludes drafts and sorts by `publishedAt` descending; `getBlogPostBySlug()` returns `null` for drafts. M8 composes the M3 UI_Primitives (`Card`, `TagList`, `EventTypeBadge`, `FilterChip`, `ExternalLink`, `EmptyState`, `MarkdownDoc`, `Container`, `Button`, `FOCUS_RING`) and the M4 shell (`main#main-content`, title template, `not-found`). M8 mirrors the M6 Projects pattern (client island under `Suspense` with a static fallback, pure helpers, static detail route) and reuses the M5 Date_Formatter (`formatDisplayDate` in `src/lib/format-date.ts`) and the M5 string comparator (`compareStrings` in `src/lib/home/compare.ts`). The M5 `RecentActivity` component already links to `/blog` and `/blog/[slug]`; M8 makes those targets resolve.

The site is statically generated. The full unfiltered post list is present in the static HTML of `/blog`. A minimal client island reads the `tag` URL search parameter after hydration, wrapped in `Suspense` as Next.js requires for `useSearchParams` under static export. This island is the only client JavaScript M8 adds, and it is justified under `AGENTS.md` 6.2 because filtering needs interactive state that a server component cannot provide.

M8 does NOT implement JSON-LD structured data, including the `Article` schema (deferred to M9), RSS or feed output, search, comments, pagination, projects or certifications changes, performance tuning or deployment (M9, M10), dark mode, API routes, analytics, forms, new dependencies, or any change to M1–M7 modules.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Blog_Index** | The route `/blog` rendered by `src/app/blog/page.tsx` (`SCR-05`). |
| **Blog_Detail** | The route `/blog/[slug]` rendered by `src/app/blog/[slug]/page.tsx` (`SCR-06`). |
| **Blog_Component** | A component in `src/components/blog/`. |
| **BlogIndex** | Blog_Component that composes the page heading and the BlogExplorer inside a `Suspense` boundary. |
| **BlogExplorer** | The client island (`'use client'`) that reads URL search parameters and renders the BlogFilterBar, Result_Announcement, and BlogPostList. |
| **BlogFilterBar** | Blog_Component rendering the tag `FilterChip` group and the "Clear filters" action. |
| **BlogPostList** | Blog_Component rendering BlogPostCards as a list in Blog_Sort_Order. |
| **BlogPostCard** | Blog_Component rendering one post summary using the M3 `Card`. |
| **BlogCardData** | The serializable subset of `BlogPost` needed to render a BlogPostCard: `slug`, `title`, `summary`, `publishedAt`, `readingTimeMinutes`, `eventType`, `tags`. It excludes `content` and `draft`. |
| **BlogPostHeader** | Blog_Component rendering the detail `h1`, dates, reading time, EventTypeBadge, and tags. |
| **EventMetadata** | Blog_Component rendering `eventName`, `eventDate`, `eventLocation`, and the "View event" link. |
| **PostBody** | Blog_Component rendering the post `content` Markdown through `MarkdownDoc`. |
| **PostNavigation** | Blog_Component rendering the Previous_Post link, the Next_Post link, and the "Back to blog" link. |
| **BlogFilters** | The type `{ tag: string \| null }` defined in `src/lib/blog/` for the Blog_Helpers. |
| **Blog_Helper** | A pure function in `src/lib/blog/`: `parseBlogFilters`, `serializeBlogFilters`, `mergeBlogFilterParams`, `deriveTagOptions`, `filterBlogPosts`, `sortBlogPosts`, `selectAdjacentPosts`, `buildBlogIndexMetadata`, `buildBlogPostMetadata`. |
| **Tag_Option** | A distinct tag name derived from `BlogPost.tags` of non-draft posts, deduplicated case-insensitively, displayed with the spelling of its first occurrence in Blog_Sort_Order. |
| **Tag_Param** | The URL search parameter `tag`, whose value is a Tag_Option name. |
| **Filter_Semantics** | At most one tag is active; a post matches when its `tags` contain the active tag compared case-insensitively. |
| **Unfiltered_State** | The state in which `BlogFilters.tag` is `null`. |
| **Published_Post** | A `BlogPost` whose `draft` field is `false`. |
| **Blog_Sort_Order** | `publishedAt` descending, then `slug` ascending (`compareStrings`). |
| **Previous_Post** | The Published_Post immediately before the current post in chronological order (the next older post in Blog_Sort_Order). |
| **Next_Post** | The Published_Post immediately after the current post in chronological order (the next newer post in Blog_Sort_Order). |
| **Event_Block** | The EventMetadata region shown only when at least one of `eventName`, `eventDate`, `eventLocation`, or `eventUrl` is present. |
| **Result_Announcement** | Text in an `aria-live="polite"` region stating the number of displayed posts. |
| **Date_Formatter** | The deterministic M5 `formatDisplayDate` function that converts an `IsoDateString` to display text without reading the system locale or time zone. |
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

### Requirement 1: Blog Index Route and Composition

**User Story:**
As a visitor, I want a blog index page, so that I can browse all of Angelo's published participation posts in one place (`APP_FLOW.md` Flow 4.0 step 4.1).

#### Acceptance Criteria

1. THE Blog_Index SHALL be served at `/blog` by `src/app/blog/page.tsx` as a static server component with no dynamic route segment and no `'use client'` directive.
2. THE Blog_Index SHALL obtain posts by calling `getBlogPosts()` from the M2 loader module and SHALL pass BlogCardData to Blog_Components through props typed with types imported from the M2 schemas.
3. THE Blog_Index SHALL render one `h1` containing the text "Blog" followed by the BlogFilterBar and the BlogPostList, inside the M4 Main_Landmark.
4. THE Blog_Index SHALL render no `header`, `footer`, or `main` element, because the M4 Root_Layout owns those landmarks.
5. THE M8 implementation SHALL NOT redeclare `BlogPost`, `BlogPostFrontmatter`, or `EventType` (`AGENTS.md` 6.1 rule 5).
6. THE Blog_Index SHALL read no data from the network at render time.
7. IF `getBlogPosts()` returns zero posts, THEN THE Blog_Index SHALL render the M3 `EmptyState` with a message that posts are being prepared and SHALL omit the BlogFilterBar (`APP_FLOW.md` Flow 4.0 step 4.1).

#### Verification Steps

1. Render the Blog_Index with three fixture posts; assert one `h1` named "Blog", the filter bar, and three post cards.
2. Render with an empty array; assert the `EmptyState` message is present and no filter chips are present.
3. Assert `src/app/blog/page.tsx` contains no `'use client'` directive and no type declaration redefining `BlogPost`.

---

### Requirement 2: Blog Post Card Content

**User Story:**
As a visitor, I want each post card to show its key facts, so that I can decide which posts to read.

#### Acceptance Criteria

1. THE BlogPostCard SHALL render the post `title` as an `h2` containing a link to `/blog/{slug}` inside an M3 `Card`.
2. THE BlogPostCard SHALL render the post `summary` as visible text.
3. THE BlogPostCard SHALL render `publishedAt` through the Date_Formatter inside a `time` element whose `datetime` attribute equals the source `IsoDateString`.
4. THE BlogPostCard SHALL render `readingTimeMinutes` as the text "{n} min read".
5. THE BlogPostCard SHALL render the M3 `EventTypeBadge` for the post `eventType`.
6. WHERE `tags` is non-empty, THE BlogPostCard SHALL render all `tags` through the M3 `TagList` in stored order.
7. WHERE `tags` is empty, THE BlogPostCard SHALL omit the tag list element.
8. THE BlogPostCard SHALL render exactly one link, with the post `title` as its accessible name.
9. THE BlogPostCard SHALL accept BlogCardData and SHALL NOT accept or render `content`.

#### Verification Steps

1. Render a fixture; assert `h2` link `href="/blog/{slug}"`, `time[datetime]`, "4 min read", the badge, and the tags.
2. Render a fixture with empty `tags`; assert no tag list.
3. Assert the card contains exactly one `a` element.
4. Assert the BlogPostCard props type contains no `content` field.

---

### Requirement 3: Blog Post List Ordering and Draft Exclusion

**User Story:**
As a visitor, I want posts newest-first and never see drafts, so that I always read current, finished content (`AGENTS.md` 5.4).

#### Acceptance Criteria

1. THE BlogPostList SHALL render BlogPostCards as `li` elements of one `ul` element in Blog_Sort_Order.
2. THE `sortBlogPosts` Blog_Helper SHALL return a new array ordered by `publishedAt` descending and, for equal `publishedAt`, by `slug` ascending using `compareStrings`.
3. FOR ALL input arrays, THE `sortBlogPosts` result SHALL be a permutation of the input, SHALL be idempotent when applied to its own result, and SHALL NOT mutate the input.
4. IF a post with `draft` equal to `true` reaches a Blog_Component, THEN THE Blog_Component SHALL omit that post from rendered output, as defense in depth beyond the M2 loader.
5. THE Blog_Index SHALL include no draft post in the static HTML, in the BlogExplorer props, or in Tag_Options.
6. THE BlogPostList SHALL preserve Blog_Sort_Order after filtering.

#### Verification Steps

1. Write a Property_Test asserting permutation, ordering by the specified keys, idempotence, and non-mutation for generated post arrays.
2. Render the BlogPostList with a fixture set containing a draft; assert the draft title is absent.
3. Render with posts sharing a `publishedAt`; assert `slug` ascending order within the tie.

---

### Requirement 4: Tag Filter State Parsing and Serialization

**User Story:**
As a visitor, I want the selected tag stored in the URL, so that I can share or reload a filtered view and use the Back button.

#### Acceptance Criteria

1. THE `parseBlogFilters` Blog_Helper SHALL accept URL search parameters and the derived Tag_Options and SHALL return a `BlogFilters` value.
2. WHEN the Tag_Param equals a Tag_Option name compared case-insensitively, THE `parseBlogFilters` Blog_Helper SHALL return that Tag_Option's canonical name as `tag`.
3. IF the Tag_Param matches no Tag_Option, THEN THE `parseBlogFilters` Blog_Helper SHALL return `tag: null` (`APP_FLOW.md` Flow 4.0 step 4.2).
4. IF the Tag_Param is repeated, THEN THE `parseBlogFilters` Blog_Helper SHALL use its first occurrence.
5. THE `serializeBlogFilters` Blog_Helper SHALL convert a `BlogFilters` value to a query string that contains the Tag_Param only when `tag` is not `null` and is the empty string in the Unfiltered_State.
6. THE `mergeBlogFilterParams` Blog_Helper SHALL return a query string that applies a `BlogFilters` value to existing search parameters, replacing or removing only the Tag_Param and preserving all unrelated parameters in their original order.
7. FOR ALL valid `BlogFilters` values drawn from the available Tag_Options, parsing the serialized value SHALL return an equal `BlogFilters` value (round-trip property).
8. THE `parseBlogFilters`, `serializeBlogFilters`, and `mergeBlogFilterParams` Blog_Helpers SHALL NOT mutate their inputs.

#### Verification Steps

1. Write a Property_Test asserting `parseBlogFilters(serializeBlogFilters(f)) equals f` for generated valid filters.
2. Write a Property_Test asserting arbitrary string values for `tag` never yield a value outside the available Tag_Options.
3. Unit-test repeated parameters, mixed-case tags, unrelated parameters preserved by `mergeBlogFilterParams`, and encoding of tags containing spaces or `&`.

---

### Requirement 5: Tag Options Derivation

**User Story:**
As a visitor, I want tag chips that reflect the real posts, so that every chip leads to at least one result.

#### Acceptance Criteria

1. THE `deriveTagOptions` Blog_Helper SHALL return Tag_Options derived from the `tags` field of all input Published_Posts, deduplicated case-insensitively and sorted alphabetically using a case-insensitive comparison with `compareStrings` as tie-break.
2. THE `deriveTagOptions` Blog_Helper SHALL ignore posts with `draft` equal to `true`.
3. FOR ALL input arrays, THE case-insensitive set of Tag_Options SHALL equal the case-insensitive set of all tag names across the input Published_Posts, with no duplicates.
4. WHEN the input array is empty or no input post has tags, THE `deriveTagOptions` Blog_Helper SHALL return an empty array.
5. WHERE Tag_Options is empty, THE BlogFilterBar SHALL omit the tag chip group and the "Clear filters" action.
6. THE `deriveTagOptions` Blog_Helper SHALL NOT mutate its input.

#### Verification Steps

1. Write a Property_Test asserting option-set equality, no duplicates, sorted order, and draft exclusion for generated post arrays.
2. Render the BlogFilterBar with an empty option list; assert no chip group.
3. Unit-test that a tag held only by a draft post yields no chip.

---

### Requirement 6: Blog Filtering Logic

**User Story:**
As a visitor, I want to filter posts by tag, so that I can find participation relevant to a topic (`APP_FLOW.md` Story 4.1).

#### Acceptance Criteria

1. WHEN `filterBlogPosts` receives `BlogFilters` in the Unfiltered_State, THE `filterBlogPosts` Blog_Helper SHALL return all input Published_Posts.
2. WHEN `BlogFilters.tag` is not `null`, THE `filterBlogPosts` Blog_Helper SHALL return only Published_Posts whose `tags` contain that name compared case-insensitively.
3. FOR ALL input arrays and filters, THE result SHALL be a sub-sequence of the input and applying `filterBlogPosts` to its own result with the same filters SHALL return an equal result (idempotence).
4. FOR ALL input arrays, a result produced with a non-`null` tag SHALL be a subset of the result produced in the Unfiltered_State (monotonicity).
5. THE `filterBlogPosts` Blog_Helper SHALL NOT mutate its input, SHALL NOT reorder its result relative to the input, and SHALL NOT match titles, summaries, event fields, or content.
6. THE `filterBlogPosts` Blog_Helper SHALL return no post with `draft` equal to `true`.

#### Verification Steps

1. Write Property_Tests for containment, idempotence, monotonicity, order preservation, and draft exclusion against a model implementation.
2. Unit-test case-insensitive tag matching.

---

### Requirement 7: Filter Bar Interaction and Accessibility

**User Story:**
As a keyboard or screen reader user, I want operable filter controls with clear state, so that I can filter posts without a mouse.

#### Acceptance Criteria

1. THE BlogFilterBar SHALL render the tag chips in a `group` role element with the accessible label "Filter by tag", using the M3 `FilterChip`.
2. THE BlogFilterBar SHALL expose each chip as a `button` element with `aria-pressed` equal to `true` for the active chip and `false` otherwise.
3. WHILE a tag filter is active, THE BlogFilterBar SHALL render the matching chip with the M3 `FilterChip` active visual state that does not rely on color alone.
4. WHEN the visitor activates an inactive chip, THE BlogExplorer SHALL set `tag` to the chip's value, replacing any previously active tag.
5. WHEN the visitor activates the active chip, THE BlogExplorer SHALL set `tag` to `null`.
6. WHEN the visitor activates a chip, THE BlogExplorer SHALL update the URL search parameters with `router.replace` and `scroll: false`, without a full page reload.
7. WHILE a tag filter is active, THE BlogFilterBar SHALL render a "Clear filters" `Button`.
8. WHEN the visitor activates "Clear filters", THE BlogExplorer SHALL remove the Tag_Param, preserve unrelated search parameters, and move keyboard focus to the first chip of the BlogFilterBar.
9. THE BlogFilterBar SHALL make every chip reachable in document order by the Tab key and activatable by the Enter key and the Space key.
10. THE BlogFilterBar SHALL render the M3 `FOCUS_RING` on every chip and on the "Clear filters" action.

#### Verification Steps

1. Render the BlogExplorer with a mocked router; click a chip; assert `aria-pressed="true"` and the expected `replace` call including `{ scroll: false }`.
2. Click the active chip; assert the Tag_Param is removed.
3. Use `userEvent.tab()` and keyboard activation to operate every chip.
4. Run an Axe_Check on the BlogFilterBar in default and active states.

---

### Requirement 8: Static Rendering and Client Island

**User Story:**
As a visitor with slow or disabled JavaScript, I want the full post list in the initial HTML, so that I can read posts before filters become interactive.

#### Acceptance Criteria

1. THE Blog_Index SHALL render the BlogExplorer inside a React `Suspense` boundary.
2. THE Suspense fallback SHALL render the full unfiltered BlogPostList, so that the static HTML of `/blog` contains every Published_Post card.
3. THE BlogExplorer SHALL be the only module under `src/components/blog/` that contains a `'use client'` directive and calls `useSearchParams`.
4. THE BlogExplorer SHALL receive only BlogCardData and the derived Tag_Options as serializable props from the server component, and SHALL NOT receive post `content`.
5. THE Blog_Index SHALL build without a "missing Suspense boundary with useSearchParams" error under the project's static export configuration.
6. THE Blog_Detail SHALL contain no `'use client'` module in its component tree.
7. THE M8 implementation SHALL NOT add a dependency to implement filtering.

#### Verification Steps

1. Run `npm run build`; assert exit code 0 and inspect the generated `/blog` HTML for every fixture post title.
2. Grep `src/components/blog/` and `src/app/blog/` for `'use client'`; assert a match only in the BlogExplorer module (and a chip wrapper it requires, if any).
3. Inspect the BlogExplorer props type; assert it excludes `content` and `draft`.

---

### Requirement 9: Empty Result State and Result Announcement

**User Story:**
As a visitor, I want clear feedback when a filter matches nothing or changes the results, so that I understand what is displayed.

#### Acceptance Criteria

1. IF the filtered result is empty, THEN THE BlogExplorer SHALL render the M3 `EmptyState` with a message stating that no posts match the selected tag and a "Clear filters" `Button` (`APP_FLOW.md` Flow 4.0 step 4.2).
2. WHEN the filtered result changes, THE BlogExplorer SHALL update a Result_Announcement to the text "{n} posts shown", using "1 post shown" for a count of 1.
3. THE Result_Announcement SHALL be rendered in an element with `aria-live="polite"` that is present in the DOM before the first filter change.
4. THE Result_Announcement SHALL be visible text and SHALL NOT be hidden from sighted users.
5. WHEN the empty-state "Clear filters" `Button` is activated, THE BlogExplorer SHALL behave as specified in Requirement 7, criterion 8, and keyboard focus SHALL NOT be lost on the removed element.

#### Verification Steps

1. Apply a filter state matching no fixture (using a mocked search parameter); assert the `EmptyState` text and the "Clear filters" button.
2. Assert the live region text for counts 0, 1, and 3, and that its container exists at first render.
3. Activate "Clear filters" from the empty state; assert `document.activeElement` is the first chip.

---

### Requirement 10: Blog Detail Route and Static Generation

**User Story:**
As a visitor, I want each post to have its own page, so that I can read and share it at a stable URL (`APP_FLOW.md` Flow 4.0 step 4.4).

#### Acceptance Criteria

1. THE Blog_Detail SHALL be served at `/blog/{slug}` by `src/app/blog/[slug]/page.tsx` as a static server component with no `'use client'` directive.
2. THE Blog_Detail SHALL export `generateStaticParams` that returns one `{ slug }` entry per Published_Post returned by `getBlogPosts()`, and no entry for a draft.
3. THE Blog_Detail SHALL export `dynamicParams = false`.
4. THE Blog_Detail SHALL obtain the post by calling `getBlogPostBySlug(slug)` from the M2 loader module.
5. IF `getBlogPostBySlug` returns `null` for the requested slug, including a draft slug, THEN THE Blog_Detail SHALL call `notFound()` so that the M4 `not-found` boundary renders.
6. THE Blog_Detail SHALL render the breadcrumb, BlogPostHeader, EventMetadata, PostBody, and PostNavigation inside the M4 Main_Landmark in that order, with the summary shown as visible text below the BlogPostHeader.
7. THE Blog_Detail SHALL render no `header`, `footer`, or `main` element.
8. THE Blog_Detail SHALL read no data from the network at render time.

#### Verification Steps

1. Call `generateStaticParams` with fixture loaders including a draft; assert the slug list equals the Published_Post slugs.
2. Assert `dynamicParams` equals `false`.
3. Render the page with an unknown slug and with a draft slug; assert `notFound` is invoked.
4. Run `npm run build`; assert one HTML file per Published_Post slug and none for drafts.

---

### Requirement 11: Blog Post Header and Dates

**User Story:**
As a reader, I want the post title, dates, reading time, and type at the top, so that I can orient myself quickly.

#### Acceptance Criteria

1. THE BlogPostHeader SHALL render exactly one `h1` containing the post `title`.
2. THE BlogPostHeader SHALL render `publishedAt` through the Date_Formatter inside a `time` element whose `datetime` attribute equals `publishedAt`.
3. WHEN `updatedAt` is not `null`, THE BlogPostHeader SHALL render the text "Updated {date}" through the Date_Formatter inside a `time` element whose `datetime` attribute equals `updatedAt`.
4. WHILE `updatedAt` is `null`, THE BlogPostHeader SHALL render no "Updated" text and no fabricated update date.
5. THE BlogPostHeader SHALL render `readingTimeMinutes` as "{n} min read".
6. THE BlogPostHeader SHALL render the M3 `EventTypeBadge` for the post `eventType`.
7. WHERE `tags` is non-empty, THE BlogPostHeader SHALL render all `tags` through the M3 `TagList`.
8. WHERE `tags` is empty, THE BlogPostHeader SHALL omit the tag list element.
9. THE M8 implementation SHALL reuse the M5 Date_Formatter and SHALL NOT create another date formatter.

#### Verification Steps

1. Render with `updatedAt` set and `null`; assert "Updated" text and `datetime` attributes.
2. Assert the heading outline contains one `h1`.
3. Property-test that header date output is stable under different `TZ` values.

---

### Requirement 12: Event Metadata Block

**User Story:**
As a reader, I want to see which event a post is about, so that I can follow the participation context (`APP_FLOW.md` Flow 4.0 step 4.5).

#### Acceptance Criteria

1. WHERE `eventName` is not `null` and not empty, THE EventMetadata SHALL render the event name as visible text.
2. WHERE `eventDate` is not `null`, THE EventMetadata SHALL render the date through the Date_Formatter inside a `time` element whose `datetime` attribute equals `eventDate`.
3. WHERE `eventLocation` is not `null` and not empty, THE EventMetadata SHALL render the location as visible text.
4. WHERE `eventUrl` is not `null` and not empty, THE EventMetadata SHALL render an M3 `ExternalLink` labeled "View event" with that URL.
5. IF `eventName`, `eventDate`, `eventLocation`, and `eventUrl` are all `null`, empty, or omitted, THEN THE Blog_Detail SHALL render no Event_Block element, including its heading or label.
6. IF `eventUrl` is `null`, empty, or omitted, THEN THE EventMetadata SHALL omit the link and SHALL render no disabled, placeholder, or `href="#"` link (`AGENTS.md` 6.1 rule 9).
7. THE EventMetadata SHALL render each present field as a term and description pair in a `dl` element, omitting the pair for each absent field.
8. THE ExternalLink SHALL include `rel="noopener noreferrer"` and an accessible indication that the link opens externally, through the M3 `ExternalLink` behavior.

#### Verification Steps

1. Render with all four event fields; assert three `dl` pairs and one "View event" link with the expected `href`.
2. Render with all four `null`; assert the Event_Block container is absent.
3. Render with only `eventName`; assert no link, no date, and no `href="#"` anchor.

---

### Requirement 13: Post Body Rendering and Heading Demotion

**User Story:**
As a reader, I want a readable post body with a correct heading outline, so that I can navigate the content with assistive technology.

#### Acceptance Criteria

1. THE PostBody SHALL render the post `content` through the M2 `renderMarkdown` function and the M3 `MarkdownDoc` component.
2. THE PostBody SHALL render headings inside the Markdown content starting at `h2`, such that no `h1` appears in rendered body content and the page heading hierarchy has no skipped levels.
3. IF the rendered body contains an `h1`, THEN THE PostBody SHALL demote the heading levels in the rendered output by one level, with a maximum level of `h6`.
4. WHERE the M6 `demoteHeadings` helper is exported from `src/lib/projects/` and is pure, THE PostBody SHALL import it without modification; OTHERWISE THE M8 implementation SHALL provide an equivalent pure helper in `src/lib/blog/`.
5. THE PostBody SHALL render no raw HTML from the Markdown source beyond what the M2 sanitization allows.
6. THE Blog_Detail SHALL render the body as static HTML without client-side JavaScript.
7. THE `demoteHeadings` helper used by M8 SHALL preserve heading text and SHALL NOT alter non-heading content.

#### Verification Steps

1. Render a fixture with `#`, `##`, and `###` headings; assert heading levels in the output are `h2`, `h3`, `h4` and exactly one `h1` exists on the page.
2. Render a fixture containing a script tag in Markdown; assert it is not present in the output.
3. Run an Axe_Check on the full Blog_Detail and assert no heading-order violation.

---

### Requirement 14: Post Navigation and Breadcrumb

**User Story:**
As a reader, I want to move to neighboring posts or back to the index, so that I can keep reading (`APP_FLOW.md` Flow 4.0 step 4.4).

#### Acceptance Criteria

1. THE `selectAdjacentPosts` Blog_Helper SHALL accept the current slug and all posts and SHALL return `{ previous, next }`, where `previous` is the Previous_Post or `null` and `next` is the Next_Post or `null`, determined among Published_Posts ordered by Blog_Sort_Order.
2. WHEN the current post is the oldest Published_Post, THE `selectAdjacentPosts` Blog_Helper SHALL return `previous: null`.
3. WHEN the current post is the newest Published_Post, THE `selectAdjacentPosts` Blog_Helper SHALL return `next: null`.
4. FOR ALL inputs containing the current slug, THE returned `previous` and `next` SHALL NOT equal the current post and SHALL NOT be drafts, and adjacency SHALL be symmetric: the `next` of a post's `previous` SHALL be that post.
5. WHERE the Previous_Post exists, THE PostNavigation SHALL render a link labeled "Previous post" containing the post title to `/blog/{slug}`.
6. WHERE the Next_Post exists, THE PostNavigation SHALL render a link labeled "Next post" containing the post title to `/blog/{slug}`.
7. IF the Previous_Post or the Next_Post is `null`, THEN THE PostNavigation SHALL omit that link and SHALL render no placeholder.
8. THE PostNavigation SHALL render a "Back to blog" link to `/blog` after the PostBody, and SHALL render in a `nav` element with the accessible label "Post navigation".
9. THE Blog_Detail SHALL render a `nav` element with the accessible label "Breadcrumb" containing a link "Blog" to `/blog` followed by the current post `title` as non-link text with `aria-current="page"`.
10. THE `selectAdjacentPosts` Blog_Helper SHALL NOT mutate its input.

#### Verification Steps

1. Write a Property_Test asserting exclusion of the current post and drafts, boundary `null` values, and adjacency symmetry for generated post arrays with unique slugs.
2. Render the PostNavigation for first, middle, and last fixture posts; assert the presence and absence of links.
3. Render the detail page; assert the breadcrumb `nav`, `aria-current`, and the "Back to blog" link.

---

### Requirement 15: Metadata and SEO

**User Story:**
As a visitor and search engine, I want accurate page metadata, so that I can find and share blog pages.

#### Acceptance Criteria

1. THE Blog_Detail SHALL export `generateMetadata` that returns, per post, a `title` equal to the post `title` (the M4 title template appends the site name), a `description` equal to the post `summary`, and a canonical URL equal to `{siteUrl}/blog/{slug}`.
2. THE `generateMetadata` result SHALL include Open Graph `title`, `description`, `url`, `type: "article"`, and `publishedTime` equal to `publishedAt`.
3. WHEN `updatedAt` is not `null`, THE `generateMetadata` result SHALL include Open Graph `modifiedTime` equal to `updatedAt`; WHILE `updatedAt` is `null`, THE result SHALL omit `modifiedTime`.
4. THE `generateMetadata` result SHALL include Open Graph `tags` equal to the post `tags`.
5. THE Blog_Index SHALL export `metadata` with the title "Blog", a description of the participation log of 50–160 characters, a canonical URL equal to `{siteUrl}/blog`, and Open Graph fields.
6. THE canonical URL for `/blog` SHALL omit the Tag_Param and all other search parameters.
7. THE M8 metadata Blog_Helpers SHALL read `siteUrl` through `getSiteConfig()` and SHALL NOT hardcode a domain.
8. IF `generateMetadata` receives an unknown or draft slug, THEN THE Blog_Detail SHALL call `notFound()`.
9. THE M8 implementation SHALL NOT emit JSON-LD structured data, including the `Article` schema, because JSON-LD is scheduled for M9.

#### Verification Steps

1. Call `buildBlogPostMetadata` and `generateMetadata` with a fixture post and `SiteConfig`; assert title, description, canonical, and Open Graph fields, with and without `updatedAt`.
2. Assert the canonical URL for `/blog` contains no query string.
3. Grep `src/app/blog/` and `src/components/blog/` for `application/ld+json` and `@type`; assert zero matches.

---

### Requirement 16: Design System, Responsive Layout, and Accessibility

**User Story:**
As a visitor on any device and with any ability, I want the Blog module to be readable, usable, and consistent with the rest of the site.

#### Acceptance Criteria

1. THE Blog_Component set SHALL use Semantic_Tokens only and SHALL NOT contain Hardcoded_Design_Values.
2. THE BlogPostList SHALL render 1 column at Mobile and Tablet and a layout whose line length does not exceed the M3 `Container` width at Desktop and Wide Desktop, using Tailwind responsive utilities.
3. THE Blog_Detail SHALL render a single-column layout at all Breakpoints with the PostBody line length limited by `design.md` Section 4.4 typography guidance, without horizontal page scrolling at 375px.
4. THE BlogFilterBar SHALL wrap chips onto multiple lines at Mobile without horizontal scrolling.
5. THE Blog_Component set SHALL render every interactive element with a touch target of at least 44px by 44px at Mobile.
6. THE Blog_Index and Blog_Detail SHALL pass an Axe_Check with zero violations in default, filtered, and empty states.
7. THE Blog_Component set SHALL render a heading hierarchy with one `h1` per page, Section_Headings and card titles as `h2`, and no skipped levels.
8. WHILE Reduced_Motion is active, THE Blog_Component set SHALL suppress transitions and animations through the M3 motion helpers.
9. THE Blog_Component set SHALL meet the WCAG 2.2 AA contrast thresholds defined by Semantic_Tokens for text, badge, and chip states.
10. THE Blog_Component set SHALL render every `time` element with a machine-readable `datetime` attribute.

#### Verification Steps

1. Grep Blog_Components for hex colors, `px-[`, `shadow-[`, and `duration-[` patterns; assert zero matches.
2. Assert responsive utility classes on the BlogPostList and Blog_Detail markup.
3. Run Axe_Check on the index (default, filtered, empty) and a detail fixture.
4. Manually check 375px, 768px, 1024px, and 1440px layouts for overflow and touch targets.

---

### Requirement 17: Testing, Quality Gates, and Scope Boundaries

**User Story:**
As a maintainer, I want M8 verified and bounded, so that regressions and scope creep are caught early.

#### Acceptance Criteria

1. THE M8 implementation SHALL include Vitest unit tests for every Blog_Helper, React Testing Library tests for each Blog_Component, and Axe_Checks for both routes, placed in `tests/blog/`.
2. THE M8 implementation SHALL include Property_Tests using fast-check with at least 100 runs for `parseBlogFilters`/`serializeBlogFilters` round-trip, `filterBlogPosts` (containment, idempotence, monotonicity), `deriveTagOptions` (option-set equality), `sortBlogPosts` (ordering), and `selectAdjacentPosts` (adjacency).
3. THE M8 implementation SHALL include a test asserting draft exclusion at the Blog_Component boundary.
4. THE M8 implementation SHALL place Blog_Helpers in `src/lib/blog/` as pure functions with no React, Next.js, or DOM imports, except that the metadata Blog_Helpers MAY import Next.js `Metadata` as a type only.
5. THE M8 implementation SHALL keep each Blog_Component file below 300 lines.
6. THE M8 implementation SHALL pass `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build` with zero errors.
7. THE M8 implementation SHALL NOT use `any`, implicit `any`, non-null assertions, or unjustified type assertions (`AGENTS.md` 6.1 rule 7).
8. THE M8 implementation SHALL NOT modify design tokens, UI_Primitives, Layout_Components, Home_Components, Project_Components, Certification_Components, M2 loaders, `package.json`, lockfiles, `next.config.ts`, or `tsconfig.json`.
9. THE M8 implementation SHALL NOT add API routes, route handlers, server actions, RSS or feed output, analytics, cookies, forms, search, comments, pagination, JSON-LD, or dark mode.
10. THE M8 implementation SHALL NOT add a dependency.

#### Verification Steps

1. Run the four verification commands and confirm zero errors.
2. Run `git diff --stat` against the M7 baseline; confirm changes only in `src/app/blog/`, `src/components/blog/`, `src/lib/blog/`, `tests/blog/`, and, if required, new fixture files under `tests/`.
3. Grep `src/lib/blog/` for `react`, `next`, and `document` imports; assert zero matches other than the type-only `Metadata` import.
4. Count lines in each Blog_Component file; assert each is below 300.
5. Confirm `git diff` on `package.json` and lockfiles is empty.
