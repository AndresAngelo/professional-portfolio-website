# APP_FLOW.md

# App Flow & User Story Specification

> **Document Status:** Approved  
> **Last Updated:** 2026-10-20  
> **UX / Product Lead:** Angelo Andres  
> **PRD Reference:** `PRD.md`  
> **TRD Reference:** `TRD.md`  
> **Content Schema Reference:** `AGENTS.md`  
> **AI Steering Target:** Designed for deterministic consumption by Gemini CLI, Cursor, Kiro IDE, Claude Code, Copilot, and other autonomous coding agents.

---

## 1. Document Control & AI Context Scope

### 1.1 Scope & Purpose
This document defines the interaction mechanics, navigation paths, component behavior, state ownership, and EARS acceptance criteria for the P0 static portfolio.

It does **not** define content schemas, TypeScript interfaces, directory structures, performance budgets, or environment variables. Those concerns are owned exclusively by `AGENTS.md`, `TRD.md`, and `env_config.md` respectively.

### 1.2 Target User Personas
- **Primary Actor:** Technical Recruiter — evaluates skills, projects, certifications, and contact options.
- **Secondary Actor:** Hiring Manager / Technical Administrator — reviews build documentation and engineering evidence.
- **Tertiary Actor:** Co-developer / Collaborator — reviews community participation and collaboration opportunities.

### 1.3 Key Architectural Boundaries
- **Entry Points:** Direct URL, search-engine result, shared link, homepage.
- **Exit Points:** External repository, live demo, certification verification, professional profile, email client.
- **State Persistence Level:** URL search parameters for filters; transient component state for mobile navigation.
- **Data Source:** Build-time local Markdown and JSON content defined in `AGENTS.md`.
- **Backend Calls:** None in P0.

---

## 2. High-Level App Flow Map

```text
                         +----------------------+
                         |       Visitor        |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |   [Target Route: /]  |
                         |      Homepage        |
                         +----------+-----------+
                                    |
        +---------------------------+---------------------------+
        |                           |                           |
        v                           v                           v
+-----------------------+   +----------------------+   +----------------------+
| [Target Route:        |   | [Target Route:       |   | [Target Route:       |
| /projects]            |   | /certifications]     |   | /blog]               |
| Projects Index        |   | Certifications       |   | Blog Index           |
+-----------+-----------+   +----------+-----------+   +----------+-----------+
            |                          |                          |
            v                          |                          v
+-----------------------+              |              +----------------------+
| [Target Route:        |              |              | [Target Route:       |
| /projects/[slug]]     |              |              | /blog/[slug]]        |
| Project Detail        |              |              | Blog Post Detail     |
+-----------+-----------+              |              +----------+-----------+
            |                          |                         |
            v                          v                         v
+---------------------------------------------------------------------+
|                         External Destinations                        |
|     Repository | Live Demo | Certification Verification | Contact    |
+---------------------------------------------------------------------+
```

---

## 3. Step-by-Step User Flow & State Machine Spec

### Flow 1.0: Homepage Orientation

#### 3.1 Flow Overview & Trigger
- **User Goal:** Understand who Angelo is and identify the most relevant portfolio evidence.
- **Preconditions:** Site configuration and at least one featured project are available.
- **Trigger Event:** Visitor opens `[Target Route: /]`.

#### 3.2 Interaction & Logic Sequence Table

| Step | User Action | System/UI Trigger | UI State & Component | Data Effect | Edge Case / Error Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1.1 | Opens homepage | Static page renders | `[SiteHeader]`, `[HeroSection]`, `[FeaturedProjects]`, `[RecentActivity]`, `[SiteFooter]` | Reads site config, featured projects, and recent posts | If no featured project exists, render an empty-state message and retain navigation |
| 1.2 | Reviews introduction | None | `[HeroSection]` displays name, role, summary, and primary actions | Reads `SiteConfig` | If contact channels are absent, hide contact action |
| 1.3 | Selects `View Projects` | Navigates to `[Target Route: /projects]` | `[PrimaryButton]` | None | N/A |
| 1.4 | Selects a featured project | Navigates to `[Target Route: /projects/[slug]]` | `[ProjectCard]` | None | If project slug is invalid, render not-found boundary |

---

### Flow 2.0: Project Discovery and Evaluation

#### 3.1 Flow Overview & Trigger
- **User Goal:** Find and evaluate relevant engineering projects.
- **Preconditions:** One or more project content files exist.
- **Trigger Event:** Visitor opens `[Target Route: /projects]` or selects `Projects` navigation.

#### 3.2 Interaction & Logic Sequence Table

| Step | User Action | System/UI Trigger | UI State & Component | Data Effect | Edge Case / Error Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2.1 | Opens projects index | Static page renders | `[ProjectsIndex]`, `[ProjectFilterBar]`, `[ProjectGrid]` | Reads all projects | If no projects exist, render `[EmptyState]` |
| 2.2 | Selects a technology filter | Updates filter state | `[FilterChip]` active state; `[ProjectGrid]` updates | Updates URL search parameter | If no project matches, render `[EmptyState]` with `Clear filters` action |
| 2.3 | Selects a status filter | Updates filter state | `[FilterChip]` active state; `[ProjectGrid]` updates | Updates URL search parameter | Invalid or unknown filter values are ignored |
| 2.4 | Selects `Clear filters` | Resets filters | `[ProjectGrid]` displays all projects | Removes relevant URL search parameters | N/A |
| 2.5 | Selects a project card | Navigates to project detail | `[ProjectCard]` | None | N/A |
| 2.6 | Reviews project detail | Static page renders | `[ProjectHeader]`, `[ProjectMetadata]`, `[BuildDocumentation]`, `[ProjectLinks]` | Reads project by slug | Invalid slug renders `[NotFound]` |
| 2.7 | Selects repository or demo link | Opens external destination | `[ExternalLink]` | None | Omit link when URL is not configured |

---

### Flow 3.0: Certification Verification

#### 3.1 Flow Overview & Trigger
- **User Goal:** Review and verify certifications or badges.
- **Preconditions:** Certification content exists.
- **Trigger Event:** Visitor opens `[Target Route: /certifications]`.

#### 3.2 Interaction & Logic Sequence Table

| Step | User Action | System/UI Trigger | UI State & Component | Data Effect | Edge Case / Error Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 3.1 | Opens certifications page | Static page renders | `[CertificationsIndex]`, `[CertificationCard]` | Reads all certifications | If no certifications exist, render `[EmptyState]` |
| 3.2 | Reviews category grouping | None | `[CertificationCategorySection]` | Groups by category when present | Uncategorised entries render in a default group |
| 3.3 | Selects verification link | Opens issuer verification page | `[ExternalLink]` | None | Omit action when verification URL is absent |
| 3.4 | Returns to portfolio | Uses browser navigation or site navigation | `[SiteHeader]` | None | N/A |

---

### Flow 4.0: Blog and Participation Review

#### 3.1 Flow Overview & Trigger
- **User Goal:** Review meetups, hackathons, learning notes, and project updates.
- **Preconditions:** One or more blog posts exist.
- **Trigger Event:** Visitor opens `[Target Route: /blog]`.

#### 3.2 Interaction & Logic Sequence Table

| Step | User Action | System/UI Trigger | UI State & Component | Data Effect | Edge Case / Error Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 4.1 | Opens blog index | Static page renders | `[BlogIndex]`, `[BlogFilterBar]`, `[BlogPostList]` | Reads all posts | If no posts exist, render `[EmptyState]` |
| 4.2 | Selects a tag filter | Updates filter state | `[FilterChip]`; `[BlogPostList]` updates | Updates URL search parameter | If no post matches, render `[EmptyState]` with `Clear filters` action |
| 4.3 | Selects a blog card | Navigates to post detail | `[BlogPostCard]` | None | N/A |
| 4.4 | Reads post | Static page renders | `[BlogPostHeader]`, `[MarkdownContent]`, `[PostNavigation]` | Reads post by slug | Invalid slug renders `[NotFound]` |
| 4.5 | Selects external event link | Opens external destination | `[ExternalLink]` | None | Omit link when event URL is absent |

---

### Flow 5.0: Contact Initiation

#### 3.1 Flow Overview & Trigger
- **User Goal:** Contact Angelo through an external channel.
- **Preconditions:** At least one contact channel is configured.
- **Trigger Event:** Visitor selects a contact action.

#### 3.2 Interaction & Logic Sequence Table

| Step | User Action | System/UI Trigger | UI State & Component | Data Effect | Edge Case / Error Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5.1 | Selects contact action | Opens configured external channel | `[ContactLinks]` | Reads contact configuration | Hide unconfigured channels |
| 5.2 | Completes contact externally | N/A | N/A | None | Website does not collect visitor data |

---

## 4. AI-Executable User Stories (EARS Notation)

### Story 1.1: View Homepage Profile

```markdown
AS A recruiter
I WANT TO view a concise professional profile on the homepage
SO THAT I can quickly determine whether to explore projects and credentials.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** the homepage is loaded, **THE SYSTEM SHALL** display the site owner’s name, professional title, concise introduction, and primary navigation.
- **Event-Driven:**
  - **WHEN** the visitor selects `View Projects`, **THE SYSTEM SHALL** navigate to `[Target Route: /projects]`.
- **State-Driven:**
  - **WHILE** featured projects are available, **THE SYSTEM SHALL** display no more than 3 featured project cards.
- **Option-Driven:**
  - **WHERE** recent blog posts are available, **THE SYSTEM SHALL** display a recent-activity section.
- **Unwanted Behavior / Exception Handling:**
  - **IF** no featured project exists, **THEN THE SYSTEM SHALL** display an accessible empty-state message without breaking the page layout.

### Story 2.1: Filter Projects

```markdown
AS A hiring manager
I WANT TO filter projects by technology and status
SO THAT I can quickly locate relevant engineering experience.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** the projects index is loaded, **THE SYSTEM SHALL** display all published projects in the default state.
- **Event-Driven:**
  - **WHEN** the visitor selects a technology filter, **THE SYSTEM SHALL** display only projects containing that technology.
- **State-Driven:**
  - **WHILE** one or more filters are active, **THE SYSTEM SHALL** display an active visual state for each selected filter.
- **Option-Driven:**
  - **WHERE** a project status filter is available, **THE SYSTEM SHALL** filter projects by the selected status.
- **Unwanted Behavior / Exception Handling:**
  - **IF** no project matches the selected filters, **THEN THE SYSTEM SHALL** display an empty state and a `Clear filters` action.

### Story 2.2: Read Project Build Documentation

```markdown
AS A technical evaluator
I WANT TO read a project’s build documentation
SO THAT I can assess implementation decisions and engineering depth.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** a valid project slug is requested, **THE SYSTEM SHALL** render the project title, summary, role, technologies, and build documentation.
- **Event-Driven:**
  - **WHEN** the visitor selects a repository link, **THE SYSTEM SHALL** open the configured external repository URL.
- **State-Driven:**
  - **WHILE** build documentation exists, **THE SYSTEM SHALL** render its Markdown content in a readable documentation layout.
- **Option-Driven:**
  - **WHERE** a live-demo URL is configured, **THE SYSTEM SHALL** display a live-demo link.
- **Unwanted Behavior / Exception Handling:**
  - **IF** an invalid project slug is requested, **THEN THE SYSTEM SHALL** render the not-found boundary.
- **Unwanted Behavior / Exception Handling:**
  - **IF** a live-demo URL is not configured, **THEN THE SYSTEM SHALL** omit the live-demo action.

### Story 3.1: Verify a Certification

```markdown
AS A recruiter
I WANT TO open a certification verification link
SO THAT I can validate a claimed credential.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** the certifications page is loaded, **THE SYSTEM SHALL** display each certification’s title, issuer, and issue date.
- **Event-Driven:**
  - **WHEN** the visitor selects a verification link, **THE SYSTEM SHALL** open the configured issuer verification URL in a new browser tab.
- **State-Driven:**
  - **WHILE** certification categories exist, **THE SYSTEM SHALL** group entries by category.
- **Option-Driven:**
  - **WHERE** a badge image is configured, **THE SYSTEM SHALL** display the badge with appropriate alternative text.
- **Unwanted Behavior / Exception Handling:**
  - **IF** no verification URL is configured, **THEN THE SYSTEM SHALL** omit the verification action and display available metadata only.

### Story 4.1: Browse Participation Posts

```markdown
AS A co-developer
I WANT TO browse dated meetup and hackathon posts
SO THAT I can understand Angelo’s community participation and current interests.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** the blog index is loaded, **THE SYSTEM SHALL** display published posts in reverse chronological order by published date.
- **Event-Driven:**
  - **WHEN** the visitor selects a tag filter, **THE SYSTEM SHALL** display only posts containing that tag.
- **State-Driven:**
  - **WHILE** a post detail page is loaded, **THE SYSTEM SHALL** render its Markdown content and metadata.
- **Option-Driven:**
  - **WHERE** an external event URL is configured, **THE SYSTEM SHALL** display an event link.
- **Unwanted Behavior / Exception Handling:**
  - **IF** an invalid blog slug is requested, **THEN THE SYSTEM SHALL** render the not-found boundary.

### Story 5.1: Contact Through External Channel

```markdown
AS A visitor
I WANT TO select a configured contact channel
SO THAT I can contact Angelo without submitting data through the website.
```

#### EARS Acceptance Criteria Matrix
- **Ubiquitous:**
  - **GIVEN** a contact channel is configured, **THE SYSTEM SHALL** display an accessible contact action.
- **Event-Driven:**
  - **WHEN** the visitor selects an email contact action, **THE SYSTEM SHALL** open the configured email client destination.
- **State-Driven:**
  - **WHILE** the visitor is on any P0 page, **THE SYSTEM SHALL** provide access to contact navigation through the global header or footer.
- **Option-Driven:**
  - **WHERE** LinkedIn or GitHub is configured, **THE SYSTEM SHALL** display the corresponding external profile link.
- **Unwanted Behavior / Exception Handling:**
  - **IF** no contact channel is configured, **THEN THE SYSTEM SHALL** hide all contact actions.

---

## 5. Screen & Component Level Specifications

### Screen ID: `SCR-01` — Homepage
- **URL Route:** `[Target Route: /]`
- **Access Level:** Public
- **Primary Components:** `[SiteHeader]`, `[HeroSection]`, `[FeaturedProjects]`, `[RecentActivity]`, `[SiteFooter]`

#### Component: `[HeroSection]`
- **Inputs/Props:** `profile: SiteProfile`, `primaryActions: NavigationAction[]`
- **Visual States:**
  - **Default:** Name, title, introduction, and primary actions.
  - **Empty:** If profile fields are missing, build validation must fail; no runtime fallback is permitted.

#### Component: `[FeaturedProjects]`
- **Inputs/Props:** `projects: Project[]`
- **Visual States:**
  - **Default:** Up to 3 `[ProjectCard]` components.
  - **Empty:** Accessible message indicating projects are being prepared.

### Screen ID: `SCR-02` — Projects Index
- **URL Route:** `[Target Route: /projects]`
- **Access Level:** Public
- **Primary Components:** `[ProjectsIndex]`, `[ProjectFilterBar]`, `[ProjectGrid]`, `[ProjectCard]`, `[EmptyState]`

#### Component: `[ProjectFilterBar]`
- **Inputs/Props:** `availableTechnologies: string[]`, `availableStatuses: ProjectStatus[]`, `activeFilters: ProjectFilters`, `onFilterChange: (filters: ProjectFilters) => void`
- **Visual States:**
  - **Default:** Filter chips for available technologies and statuses.
  - **Active:** Selected chips use the active token state.
  - **Empty Result:** `[EmptyState]` with `Clear filters`.

#### Component: `[ProjectCard]`
- **Inputs/Props:** `project: Project`
- **Visual States:**
  - **Default:** Title, summary, technologies, status, and detail link.
  - **External Evidence:** Repository and live-demo links when configured.

### Screen ID: `SCR-03` — Project Detail
- **URL Route:** `[Target Route: /projects/[slug]]`
- **Access Level:** Public
- **Primary Components:** `[ProjectHeader]`, `[ProjectMetadata]`, `[BuildDocumentation]`, `[ProjectLinks]`, `[NotFound]`

#### Component: `[BuildDocumentation]`
- **Inputs/Props:** `documentation: string`
- **Visual States:**
  - **Default:** Rendered Markdown.
  - **Error:** Build must fail if required documentation is absent.

### Screen ID: `SCR-04` — Certifications
- **URL Route:** `[Target Route: /certifications]`
- **Access Level:** Public
- **Primary Components:** `[CertificationsIndex]`, `[CertificationCategorySection]`, `[CertificationCard]`, `[EmptyState]`

#### Component: `[CertificationCard]`
- **Inputs/Props:** `certification: Certification`
- **Visual States:**
  - **Default:** Title, issuer, issue date, badge image where configured, and verification link where configured.
  - **Empty:** Not applicable at card level; index handles the empty state.

### Screen ID: `SCR-05` — Blog Index
- **URL Route:** `[Target Route: /blog]`
- **Access Level:** Public
- **Primary Components:** `[BlogIndex]`, `[BlogFilterBar]`, `[BlogPostList]`, `[BlogPostCard]`, `[EmptyState]`

#### Component: `[BlogPostCard]`
- **Inputs/Props:** `post: BlogPost`
- **Visual States:**
  - **Default:** Title, published date, reading time, event type, summary, and tags.
  - **Empty Result:** `[EmptyState]` with `Clear filters`.

### Screen ID: `SCR-06` — Blog Post Detail
- **URL Route:** `[Target Route: /blog/[slug]]`
- **Access Level:** Public
- **Primary Components:** `[BlogPostHeader]`, `[MarkdownContent]`, `[PostNavigation]`, `[NotFound]`

### Screen ID: `SCR-07` — Not Found
- **URL Route:** `[Target Route: /not-found]` or framework not-found boundary
- **Access Level:** Public
- **Primary Components:** `[NotFound]`, `[SiteHeader]`, `[SiteFooter]`
- **Behavior:** Displays a clear message and links to Homepage, Projects, Certifications, and Blog.

---

## 6. Global State Transitions & Exception Matrix

| Exception / Edge Condition | System State Trigger | UI / UX Reaction | Recovery Path |
| :--- | :--- | :--- | :--- |
| Invalid project slug | Static route parameter does not match content | `[NotFound]` | Link to `[Target Route: /projects]` |
| Invalid blog slug | Static route parameter does not match content | `[NotFound]` | Link to `[Target Route: /blog]` |
| No projects match filters | Filter result set is empty | `[EmptyState]` | `Clear filters` action |
| No blog posts match filters | Filter result set is empty | `[EmptyState]` | `Clear filters` action |
| No content exists | Content collection is empty | `[EmptyState]` | Content owner adds valid content |
| Missing required frontmatter | Build-time validation fails | Build stops; no incomplete page deploys | Correct content against `AGENTS.md` |
| External URL absent | Optional URL field is empty | Action is omitted | Add URL in content when available |
| Reduced-motion preference | Visitor enables reduced motion | Nonessential animation is disabled | Respect `prefers-reduced-motion` |

---

## 7. AI Agent Steering Context & Implementation Prompt Guidelines

### 7.1 Framework-Agnostic Mapping Rules
- Use `[Target Route Path]` placeholders when expressing routes; resolve them to the Next.js App Router paths defined in `TRD.md` during implementation.
- Use `[State Hook]` placeholders for local interaction state; do not introduce a global state library in P0.
- Use server components for static content rendering wherever possible.
- Use client components only for mobile navigation, filtering interactions, or other genuinely interactive behavior.

### 7.2 System Implementation Rules for AI Coding Assistants
1. **Never invent content.** Render only content supplied through the typed loaders and schemas in `AGENTS.md`.
2. **Never duplicate schemas.** Import or derive content types from the contracts defined in `AGENTS.md`.
3. **Implement every UI state.** Each list-based screen must implement default, empty, filtered-empty, and not-found states where applicable.
4. **Use URL-based filters.** Project and blog filters must be shareable through URL search parameters.
5. **Preserve accessibility.** Use semantic landmarks, headings, buttons, links, labels, focus states, and alternative text.
6. **Do not add backend dependencies.** No database client, authentication provider, API route, route handler, or server mutation is permitted in P0.
7. **Fail closed on invalid content.** Required missing or malformed content must cause build validation to fail.

### 7.3 Direct AI System Prompt

```text
Act as a Senior Frontend Engineer implementing personal-website-portfolio-v2.

Refer to:
- PRD.md for product scope.
- TRD.md for architecture, rendering, performance, and deployment rules.
- APP_FLOW.md for routes, flows, and EARS acceptance criteria.
- design.md for SGDS-inspired visual tokens and accessibility rules.
- AGENTS.md for content schemas, directory taxonomy, naming, and repository guardrails.

Task: Implement the P0 routes and components described in APP_FLOW.md.

Strict Execution Rules:
1. Use Next.js App Router static rendering and TypeScript strict mode.
2. Use the exact content schemas and directory taxonomy from AGENTS.md.
3. Implement all specified default, empty, filtered-empty, loading-free static, and not-found states.
4. Use URL search parameters for project and blog filters.
5. Use semantic HTML and meet WCAG 2.1 AA.
6. Do not create APIs, databases, authentication, analytics, or server-side mutations.
7. Run npm run lint, npm run typecheck, npm test, and npm run build before completion.
```