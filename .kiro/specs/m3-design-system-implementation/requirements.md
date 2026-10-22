# Requirements Document

> **Spec:** M3 Design System Implementation  
> **Document Status:** Draft  
> **Feature Name:** m3-design-system-implementation  
> **Milestone:** M3  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md`, `design.md` (Sections 3–5, 7), `PRD.md`, `TRD.md`  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 3 (M3) implements the SGDS-inspired design system for `personal-website-portfolio-v2` as a set of reusable, accessible UI primitives in `src/components/ui/`. The design tokens (color, spacing, typography, radius, elevation, motion) were already configured in `tailwind.config.ts` and `globals.css` by Milestone 1 (Requirement 3). M3 consumes those tokens and does not redefine them.

M3 delivers the Button, Card, Tag, Status Badge, Event Type Badge, FilterChip, ExternalLink, EmptyState, and Markdown Documentation Layout primitives, plus focus-ring styling, `prefers-reduced-motion` handling, responsive container utilities, component tests, and automated accessibility checks. Primitives are server components unless interaction requires `'use client'`.

M3 does NOT implement the global layout, header, footer, or navigation (M4), page routes (M5–M8), or quality, build, and deployment work (M9–M10). Dark mode stays off by default; dark token values defined in M1 remain unused until explicitly approved.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **UI_Primitive** | A reusable presentational component in `src/components/ui/` that contains no hardcoded content and no content-loading logic. |
| **Semantic_Token** | A named design value from `design.md` Section 3 (for example `bg-surface`, `text-primary`, `space-4`, `radius-lg`, `elevation-1`, `motion-fast`) exposed through Tailwind and CSS custom properties by M1. |
| **Hardcoded_Design_Value** | A raw hex color, arbitrary pixel size, arbitrary shadow, or arbitrary duration written directly in a component (for example `#0052A5` or `w-[37px]`). |
| **Button** | Action control with variants Primary, Secondary, Ghost, and External Link, and sizes Small (32px), Medium (40px), and Large (48px). |
| **Card** | Surface container using `radius-lg`, `elevation-1`, and `bg-surface`; basis for project, certification, and blog cards built in M6–M8. |
| **Tag** | Compact neutral label using `radius-sm` that identifies a technology or topic. |
| **Status_Badge** | Badge that communicates `ProjectStatus` (`completed`, `in-progress`, `archived`) using a text label and semantic color. |
| **Event_Type_Badge** | Badge that communicates `EventType` (`meetup`, `hackathon`, `workshop`, `conference`, `learning`, `project-update`) using a text label. |
| **FilterChip** | Interactive toggle control that applies or clears a filter value; the only Tag-like element that is a button. |
| **ExternalLink** | Anchor to a destination outside the site, rendered with `target="_blank"`, `rel="noopener noreferrer"`, and an accessible new-tab label. |
| **EmptyState** | Component shown when a collection has no matching items, with a message and optional action. |
| **Markdown_Doc_Layout** | Container component that styles rendered Markdown HTML (headings, code, tables, lists) for readable documentation. |
| **Focus_Ring** | Visible keyboard focus indicator that uses the `focus-ring` Semantic_Token. |
| **Container** | Responsive width-constraining layout primitive that centers content and applies horizontal padding per breakpoint. |
| **Breakpoints** | Mobile `375px–767px`, Tablet `768px–1023px`, Desktop `1024px–1439px`, Wide Desktop `1440px+` (`design.md` 5.1). |
| **Reduced_Motion** | The user preference exposed by the `prefers-reduced-motion: reduce` media query. |
| **Axe_Check** | An automated accessibility test run against rendered components using an axe-core based tool. |
| **ProjectStatus / EventType** | Enumerations defined once in M2 schemas and imported by M3; M3 SHALL NOT redefine them (`AGENTS.md` 6.3). |

---

## Requirements

---

### Requirement 1: Consume Semantic Tokens Without Redefining Them

**User Story:**
As a design system maintainer, I want every UI primitive to use the tokens configured in M1, so that visual values stay consistent and are changed in exactly one place.

#### Acceptance Criteria

1. THE UI_Primitive set SHALL style colors, spacing, typography, radius, elevation, and motion exclusively through Semantic_Tokens exposed by Tailwind utilities or CSS custom properties.
2. THE UI_Primitive set SHALL contain zero Hardcoded_Design_Values (`AGENTS.md` 6.1 Rule 8, `design.md` 7.1).
3. THE M3 implementation SHALL NOT add, modify, or remove any token definition in `tailwind.config.ts` or `globals.css`.
4. IF a required Semantic_Token is absent from the M1 configuration, THEN THE M3 implementation SHALL record the missing token in the spec's task notes and request human approval before any root configuration change (`AGENTS.md` 6.2).
5. THE UI_Primitive set SHALL apply no dark-mode-specific styling by default (`design.md` 7.7).

#### Verification Steps

1. Search `src/components/ui/` for `#[0-9A-Fa-f]{3,8}`, `rgb(`, `rgba(`, and `[` arbitrary-value Tailwind classes; confirm zero matches.
2. Run `git diff` on `tailwind.config.ts` and `globals.css`; confirm no token changes.
3. Confirm no `dark:` utilities appear in `src/components/ui/`.

---

### Requirement 2: Button Component with Variants, Sizes, and States

**User Story:**
As a UI developer, I want a Button primitive with defined variants, sizes, and states, so that actions look and behave consistently across all pages.

#### Acceptance Criteria

1. THE Button SHALL support the variants `primary`, `secondary`, `ghost`, and `external-link`.
2. THE Button SHALL support the sizes `sm`, `md`, and `lg` with heights of 32px, 40px, and 48px respectively, expressed through spacing Semantic_Tokens.
3. THE Button SHALL default to variant `primary` and size `md` WHEN no variant or size is provided.
4. THE Button SHALL define visual styles for default, hover, active, focus-visible, and disabled states for every variant.
5. WHEN the Button is disabled, THE Button SHALL set the `disabled` attribute, apply the `text-disabled` token, and ignore click events.
6. WHERE the Button is rendered as a link, THE Button SHALL render an anchor element with the same variant and size styling.
7. WHERE the Button contains only an icon, THE Button SHALL require an `aria-label` prop at the type level.
8. THE Button SHALL render as a native `button` element with `type="button"` by default.
9. THE Button SHALL render as a server component.

#### Verification Steps

1. Open `src/components/ui/button.tsx`; confirm variant and size union types and the absence of `any`.
2. Run Button tests rendering all 4 variants × 3 sizes; confirm class names map to token utilities.
3. Run `npm run typecheck`; confirm an icon-only Button without `aria-label` produces a type error (`@ts-expect-error` test).

---

### Requirement 3: Card Container

**User Story:**
As a UI developer, I want a Card container primitive, so that project, certification, and blog cards share one surface style.

#### Acceptance Criteria

1. THE Card SHALL apply the `radius-lg`, `elevation-1`, `bg-surface`, and `border-default` Semantic_Tokens (`design.md` 4.3).
2. THE Card SHALL apply `space-6` internal padding by default.
3. WHEN a pointer hovers a Card that has a link destination, THE Card SHALL transition to `elevation-2` using the `motion-fast` duration token.
4. WHERE a Card has a single link destination, THE Card SHALL expose one anchor whose accessible name describes that destination, and the anchor SHALL cover the full Card area.
5. IF a Card is configured with a full-card link, THEN THE Card SHALL NOT render any other interactive element nested inside the link.
6. THE Card SHALL accept a heading level prop so that the consuming page controls document heading hierarchy.
7. THE Card SHALL render as a server component.

#### Verification Steps

1. Render Card with and without a link; confirm the class tokens and anchor count.
2. Render a Card with a full-card link and a nested button; confirm the component rejects it at the type level or in a test.
3. Run Axe_Check; confirm zero violations.

---

### Requirement 4: Tag and Technology Tag

**User Story:**
As a visitor, I want compact technology and topic labels, so that I can scan what a project or post covers.

#### Acceptance Criteria

1. THE Tag SHALL render a compact label using `radius-sm`, `bg-surface`, `border-default`, `text-caption` or `text-small`, and `space-1`–`space-3` padding tokens (`design.md` 4.4).
2. THE Tag SHALL render as a non-interactive element (for example `span` inside a list item).
3. THE Tag SHALL NOT set a `role="button"`, `tabindex`, or click handler.
4. THE Tag SHALL accept a string label as children and render the string as text content.
5. WHERE multiple Tags are grouped, THE TagList SHALL render an unordered list with an accessible name supplied by the consumer.
6. THE Tag text color SHALL meet a contrast ratio of at least 4.5:1 against its background token in light mode.

#### Verification Steps

1. Render Tag and TagList; confirm no interactive roles or attributes.
2. Run Axe_Check on TagList; confirm zero violations including `color-contrast` where the test environment supports it.
3. Confirm the contrast pairing against the `design.md` 3.1 values.

---

### Requirement 5: Status Badge

**User Story:**
As a visitor, I want a status badge on projects, so that I can see whether work is completed, in progress, or archived.

#### Acceptance Criteria

1. THE Status_Badge SHALL accept a `ProjectStatus` value imported from the M2 schemas.
2. THE Status_Badge SHALL render the label `Completed`, `In Progress`, or `Archived` for the values `completed`, `in-progress`, or `archived` respectively.
3. THE Status_Badge SHALL map `completed` to the `feedback-success` token, `in-progress` to the `feedback-warning` token, and `archived` to the `text-secondary` token.
4. THE Status_Badge SHALL convey status through the visible text label in addition to color (`design.md` 4.4).
5. THE Status_Badge SHALL render an exhaustive mapping so that adding a `ProjectStatus` value causes a TypeScript compile error until the mapping is updated.
6. THE Status_Badge SHALL render text and background combinations with a contrast ratio of at least 4.5:1.

#### Verification Steps

1. Render the badge for each of the 3 statuses; assert label text and token class.
2. Confirm the exhaustive mapping uses a `Record<ProjectStatus, ...>` or `never` check.
3. Confirm `ProjectStatus` is imported, not redeclared.

---

### Requirement 6: Event Type Badge

**User Story:**
As a visitor, I want an event type badge on blog entries, so that I can tell meetups, hackathons, workshops, conferences, learning notes, and project updates apart.

#### Acceptance Criteria

1. THE Event_Type_Badge SHALL accept an `EventType` value imported from the M2 schemas.
2. THE Event_Type_Badge SHALL render the labels `Meetup`, `Hackathon`, `Workshop`, `Conference`, `Learning`, and `Project Update` for the six `EventType` values.
3. THE Event_Type_Badge SHALL convey the event type through its visible text label and not through color alone.
4. THE Event_Type_Badge SHALL use neutral or `brand-secondary` token styling that meets a 4.5:1 contrast ratio.
5. THE Event_Type_Badge SHALL render an exhaustive mapping so that adding an `EventType` value causes a TypeScript compile error until the mapping is updated.

#### Verification Steps

1. Render the badge for each of the 6 event types; assert label text.
2. Confirm the exhaustive `Record<EventType, ...>` mapping.
3. Run Axe_Check on all 6 variants; confirm zero violations.

---

### Requirement 7: FilterChip Interactive Control

**User Story:**
As a visitor, I want filter chips I can toggle with a keyboard or pointer, so that I can narrow projects and blog posts by technology, status, or tag.

#### Acceptance Criteria

1. THE FilterChip SHALL render a native `button` element with `type="button"`.
2. THE FilterChip SHALL expose its selected state through `aria-pressed` set to `true` or `false`.
3. WHEN a visitor activates the FilterChip with a click, Enter key, or Space key, THE FilterChip SHALL invoke the provided `onToggle` callback exactly once.
4. WHILE the FilterChip is selected, THE FilterChip SHALL apply `brand-primary` styling that differs visibly from the unselected state by more than color alone (for example a border weight change or a check icon with accessible text).
5. THE FilterChip SHALL apply the Focus_Ring when focused by keyboard.
6. THE FilterChip SHALL be the only primitive that applies `cursor-pointer` styling and an `onClick`-style handler among the Tag-like components.
7. THE FilterChip SHALL declare `'use client'` only if the implementation owns state; WHERE the consumer owns state, THE FilterChip SHALL remain a server-compatible component that receives its handler from a client parent.
8. THE FilterChip SHALL provide a minimum target size of 32px height.

#### Verification Steps

1. Render the chip; fire click, Enter, and Space with `@testing-library/user-event`; assert callback counts.
2. Assert `aria-pressed` toggles with the `selected` prop.
3. Confirm the `'use client'` decision is documented in a code comment.

---

### Requirement 8: ExternalLink Component

**User Story:**
As a visitor, I want external links to be safe and clearly announced, so that I know a link leaves the site and opens a new tab.

#### Acceptance Criteria

1. THE ExternalLink SHALL render an anchor with `target="_blank"` and `rel="noopener noreferrer"`.
2. THE ExternalLink SHALL expose an accessible name that includes the link text and the phrase `(opens in a new tab)` using visually hidden text (`design.md` 5.2).
3. THE ExternalLink SHALL render a decorative external-link icon with `aria-hidden="true"`.
4. THE ExternalLink SHALL accept only an absolute `https://` URL string in its `href` prop.
5. IF the `href` prop is `null`, empty, or omitted, THEN THE ExternalLink SHALL render nothing (`AGENTS.md` 5.1 Rule 8).
6. IF the `href` prop does not begin with `https://`, THEN THE ExternalLink SHALL render nothing and log a development-time error naming the invalid value category.
7. THE ExternalLink SHALL apply the Focus_Ring and the `brand-primary` link color token.
8. WHERE the ExternalLink uses the Button `external-link` variant, THE ExternalLink SHALL render the same attributes as defined in criteria 1 through 3.

#### Verification Steps

1. Render with a valid HTTPS URL; assert `target`, `rel`, and the hidden text.
2. Render with `null`, `""`, `undefined`, and `http://` URLs; assert no anchor is rendered.
3. Run Axe_Check; confirm zero violations.

---

### Requirement 9: EmptyState Component

**User Story:**
As a visitor, I want a clear message when no items match, so that I understand the page is not broken and know how to recover.

#### Acceptance Criteria

1. THE EmptyState SHALL render a required heading or title and a required descriptive message.
2. THE EmptyState SHALL support an optional action slot that accepts a Button or link.
3. THE EmptyState SHALL render the heading with a consumer-provided heading level.
4. WHERE an action is not provided, THE EmptyState SHALL omit the action container from the DOM.
5. THE EmptyState SHALL contain no hardcoded production messages; copy SHALL be supplied by the consumer (`design.md` 7.6).
6. WHEN the EmptyState appears in response to a user-driven filter change, THE EmptyState SHALL support an optional `role="status"` live-region mode so that assistive technology announces the result.
7. THE EmptyState SHALL use `text-secondary`, `bg-surface`, `border-default`, and `space-8`–`space-12` tokens for layout.

#### Verification Steps

1. Render with and without an action; assert DOM output.
2. Render in live-region mode; assert `role="status"`.
3. Run Axe_Check; confirm zero violations.

---

### Requirement 10: Markdown Documentation Layout

**User Story:**
As a visitor reading a project or blog post, I want documentation styled for readability, so that long technical content is easy to scan.

#### Acceptance Criteria

1. THE Markdown_Doc_Layout SHALL constrain prose width to a maximum of 75 characters using the `ch` unit and target a measure of at least 65 characters (`design.md` 4.5).
2. THE Markdown_Doc_Layout SHALL style `h2` through `h4` using the `text-heading-3`, `text-heading-4`, and `text-body` typography tokens with spacing tokens between sections.
3. THE Markdown_Doc_Layout SHALL render inline code and code blocks using the monospace font stack from `design.md` 3.2.
4. WHEN a code block is wider than its container, THE Markdown_Doc_Layout SHALL scroll the code block horizontally without scrolling the page.
5. THE Markdown_Doc_Layout SHALL give each scrollable code block keyboard access through `tabindex="0"` and an accessible name.
6. THE Markdown_Doc_Layout SHALL style tables so that header cells use `th` with `scope` attributes, and tables wider than the container scroll horizontally inside a labelled wrapper.
7. THE Markdown_Doc_Layout SHALL style ordered lists, unordered lists, blockquotes, links, and images using Semantic_Tokens.
8. THE Markdown_Doc_Layout SHALL accept the sanitized HTML output of the M2 Markdown pipeline and SHALL NOT parse Markdown itself.
9. THE Markdown_Doc_Layout SHALL begin its internal heading hierarchy at `h2` (`design.md` 4.5).
10. THE Markdown_Doc_Layout SHALL render as a server component.

#### Verification Steps

1. Render sample HTML containing headings, code, a table, and a list; assert wrapper classes and attributes.
2. Verify the prose container applies a `max-w` value in `ch` units between 65 and 75.
3. Run Axe_Check, including `scrollable-region-focusable`; confirm zero violations.

---

### Requirement 11: Focus Ring Styling

**User Story:**
As a keyboard user, I want a visible focus indicator on every interactive element, so that I always know where I am on the page.

#### Acceptance Criteria

1. THE Focus_Ring SHALL be implemented as a shared utility or class composition that applies the `focus-ring` Semantic_Token on `:focus-visible`.
2. THE Focus_Ring SHALL render an outline of at least 2px width with an offset of at least 2px.
3. THE Focus_Ring SHALL meet a contrast ratio of at least 3:1 against adjacent backgrounds in light mode.
4. THE Button, FilterChip, ExternalLink, and linked Card SHALL apply the Focus_Ring.
5. THE UI_Primitive set SHALL NOT remove an outline without applying an equivalent visible indicator (`design.md` 5.2).
6. THE Focus_Ring SHALL appear on keyboard focus and SHALL NOT appear on pointer focus for non-text-input elements.

#### Verification Steps

1. Search `src/components/ui/` for `outline-none` and `outline-0`; confirm each occurrence is paired with the Focus_Ring utility.
2. Tab through a rendered fixture; assert the focus-visible class is applied to each interactive element.
3. Document the manual verification of the contrast ratio against `design.md` 3.1.

---

### Requirement 12: Reduced Motion Handling

**User Story:**
As a visitor sensitive to motion, I want animations and transitions disabled when I request it, so that the site is comfortable to use.

#### Acceptance Criteria

1. THE UI_Primitive set SHALL declare all transitions through the `motion-fast` and `motion-standard` Semantic_Tokens.
2. WHILE the visitor's system matches `prefers-reduced-motion: reduce`, THE UI_Primitive set SHALL reduce every transition and animation duration to 0ms or an equivalent non-animated state.
3. THE UI_Primitive set SHALL implement Reduced_Motion handling through Tailwind `motion-reduce:` utilities or a single shared rule in `globals.css` that the M1 stylesheet already provides.
4. THE UI_Primitive set SHALL NOT use parallax, autoplaying motion, or nonessential animation (`design.md` 5.2).
5. IF the M1 stylesheet does not provide a global Reduced_Motion rule, THEN THE M3 implementation SHALL use `motion-reduce:` utilities in each component.

#### Verification Steps

1. Search `src/components/ui/` for `transition` and `animate-`; confirm each occurrence pairs with `motion-reduce:` or a documented global rule.
2. Confirm that no `@keyframes` or `animate-` usage exists outside documented exceptions.
3. Review the stylesheet for a `prefers-reduced-motion` media query.

---

### Requirement 13: Responsive Container and Breakpoint Utilities

**User Story:**
As a UI developer, I want a responsive Container primitive, so that every page works from 375px to wide desktop widths.

#### Acceptance Criteria

1. THE Container SHALL center its content horizontally and apply horizontal padding from the spacing Semantic_Tokens.
2. THE Container SHALL support layouts for Mobile (375px–767px), Tablet (768px–1023px), Desktop (1024px–1439px), and Wide Desktop (1440px and above).
3. WHILE the viewport width is 1440px or greater, THE Container SHALL cap the content width at a maximum readable width defined by a spacing or size token.
4. WHILE the viewport width is 375px, THE Container SHALL render content without horizontal page scrolling.
5. THE Container SHALL accept a polymorphic element prop (`div`, `section`, `main`, `article`) so that consumers choose the correct landmark.
6. IF the Tailwind configuration does not define screens matching the Breakpoints, THEN THE M3 implementation SHALL record the gap and request human approval before modifying `tailwind.config.ts` (`AGENTS.md` 6.2).
7. THE Container SHALL render as a server component.

#### Verification Steps

1. Render the Container with each element type; assert tag name and class tokens.
2. Compare `tailwind.config.ts` screens to the Breakpoints; document any mismatch.
3. Confirm the responsive behavior at 375px, 768px, 1024px, and 1440px in the manual check recorded in the task notes.

---

### Requirement 14: Component Tests with Vitest and React Testing Library

**User Story:**
As a QA engineer, I want automated component tests for every primitive, so that regressions in behavior, structure, and tokens are caught before merge.

#### Acceptance Criteria

1. THE Test_Suite SHALL include at least one test file per UI_Primitive under `tests/` or co-located `*.test.tsx` files that match the M1 Vitest patterns.
2. THE Test_Suite SHALL use Vitest and React Testing Library already configured by M1.
3. THE Test_Suite SHALL query elements by role, label, or text, and SHALL NOT query by implementation-specific class names except when asserting token utilities.
4. THE Test_Suite SHALL cover every Button variant × size combination, every Status_Badge value, and every Event_Type_Badge value.
5. THE Test_Suite SHALL cover keyboard interaction for the Button and the FilterChip.
6. THE Test_Suite SHALL cover the ExternalLink rejection paths for `null`, empty, and non-HTTPS values.
7. WHEN `npm test` is executed, THE Test_Suite SHALL pass with exit code 0.
8. THE Test_Suite SHALL NOT contain `any`, non-null assertions (`!`), or unjustified type assertions (`as`) (`AGENTS.md` 6.1 Rule 7).

#### Verification Steps

1. Run `npm test`; confirm all M3 tests pass.
2. Count test files against the UI_Primitive list; confirm full coverage.
3. Run `npm run lint`; confirm zero errors in test files.

---

### Requirement 15: Automated Accessibility Checks

**User Story:**
As an accessibility owner, I want automated axe checks on every primitive, so that WCAG 2.1 AA regressions are detected during development.

#### Acceptance Criteria

1. THE Test_Suite SHALL run an Axe_Check against every UI_Primitive in each documented variant and state.
2. THE Axe_Check SHALL report zero violations for WCAG 2.1 A and AA rules supported by the tool.
3. WHERE an axe-core based test library is added, THE M3 implementation SHALL document its purpose, verify its maintenance status, and pin an exact version before adding it to `package.json` (`AGENTS.md` 6.2).
4. IF adding the Axe_Check library requires a change to `package.json` or the lockfile, THEN the change is Approved 2026-10-22 (approval 1a); pin exact version and document purpose/maintenance status before adding.
5. THE M3 implementation SHALL record, in the task notes, the accessibility criteria that require manual verification with assistive technology, including real contrast measurement and screen-reader announcement.
6. THE UI_Primitive set SHALL provide an accessible name for every interactive element.
7. THE UI_Primitive set SHALL operate with keyboard only, with logical tab order and no keyboard traps.

#### Verification Steps

1. Run `npm test`; confirm Axe_Check tests execute for every primitive.
2. Review `package.json` diff for any added dependency and its documented purpose.
3. Confirm the manual verification list exists in the task notes.

---

### Requirement 16: TypeScript Strictness, Server-Component Preference, and Scope Boundaries

**User Story:**
As a code quality owner, I want M3 code to follow the repository guardrails, so that the design system stays type-safe, statically rendered, and within its milestone scope.

#### Acceptance Criteria

1. THE UI_Primitive set SHALL compile under TypeScript strict mode with zero `any`, implicit `any`, non-null assertions, or unjustified type assertions.
2. THE UI_Primitive set SHALL use server components by default and SHALL declare `'use client'` only in components that require browser event handling or state.
3. WHEN a component declares `'use client'`, THE component file SHALL contain a comment stating which interaction requires it.
4. THE UI_Primitive set SHALL import `ProjectStatus` and `EventType` from M2 and SHALL NOT redefine canonical content schemas (`AGENTS.md` 6.3).
5. THE M3 implementation SHALL NOT add UI component libraries or class-composition dependencies without documented purpose and human approval.
6. THE M3 implementation SHALL NOT create API routes, route handlers, server actions, analytics, cookies, or forms.
7. THE M3 implementation SHALL NOT create header, footer, or navigation components (M4), page routes (M5–M8), or deployment configuration (M9–M10).
8. THE UI_Primitive source files SHALL each remain below 300 lines where practical and use explicit imports without barrel files (`AGENTS.md` 7.2).
9. WHEN M3 work is complete, THE Verification_Pipeline SHALL pass `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build` with exit code 0 (`AGENTS.md` 7.3).

#### Verification Steps

1. Run the four verification commands in order; confirm exit code 0 for each.
2. Search `src/components/ui/` for `'use client'`; confirm each occurrence carries an explanatory comment.
3. List new files; confirm none are under `src/app/` and no `index.ts` barrel files exist.

---

## Document Summary

This M3 requirements document specifies 16 EARS-formatted requirements across 5 categories:

- **Token governance (1):** consume M1 tokens; no redefinition, no hardcoded values.
- **Primitives (2–10):** Button, Card, Tag, Status Badge, Event Type Badge, FilterChip, ExternalLink, EmptyState, Markdown Documentation Layout.
- **Cross-cutting styling (11–13):** focus ring, reduced motion, responsive container and breakpoints.
- **Verification (14–15):** Vitest and React Testing Library component tests, automated accessibility checks.
- **Guardrails (16):** strict TypeScript, server-component preference, scope boundaries, verification pipeline.

Items needing human approval before design or implementation: any dependency outside the set Approved 2026-10-22 (approval 1a; axe-core test helper, `fast-check`), and any root configuration change if `tailwind.config.ts` lacks the 375/768/1024/1440 screens.
