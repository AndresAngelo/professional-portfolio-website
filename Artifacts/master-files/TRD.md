# TRD.md

# Technical Requirement Document (TRD)

> **Document Status:** Approved  
> **Last Updated:** 2026-10-20  
> **Lead Architect / Tech Lead:** Angelo Andres  
> **PRD Reference:** `PRD.md`  
> **Repository:** `personal-website-portfolio-v2`  
> **SSOT References:** Content schemas, directory taxonomy, validation rules, and repository guardrails are defined exclusively in `AGENTS.md`. Product scope is defined in `PRD.md`.

---

## 1. Document Control & Executive Summary

### 1.1 Revision History & Change Log

| Date | Version | Author | Summary of Changes | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| 2026-10-20 | v1.0 | Angelo Andres | Approved static MVP architecture | Angelo Andres |

### 1.2 System Purpose & Technical Scope
- **Problem Summary:** Provide a fast, maintainable, publicly accessible developer portfolio that presents projects, build documentation, certifications, and participation logs without backend infrastructure.
- **Technical Boundary:**
  - **In-Scope:** Next.js App Router static rendering, TypeScript, Tailwind CSS, local Markdown/JSON content pipeline, SGDS-inspired UI, SEO metadata, accessibility, and Vercel deployment.
  - **Out-of-Scope:** Databases, authentication, user-generated content, custom public APIs, server-side data mutations, CMS, comments, analytics-based personal-data collection, and production AI features.

### 1.3 Key Stakeholders & System Roles
- **System Owner:** Angelo Andres
- **Reviewers:** Engineering, UI/UX, QA
- **Target Audience:** Hiring talent, recruiters, technical administrators, co-developers, and autonomous coding agents.

---

## 2. High-Level System Architecture & Tech Stack

### 2.1 Technology Stack Matrix

| Layer | Framework / Technology | Version / Specification | Rationale / Notes |
| :--- | :--- | :--- | :--- |
| **Framework** | Next.js App Router | Current LTS-compatible major version selected at scaffold time | File-based routing, React Server Components, static generation, Vercel-native deployment |
| **Language** | TypeScript | Strict mode | Type-safe content and component contracts |
| **Styling** | Tailwind CSS | Current stable major version | Utility-first styling mapped to SGDS-inspired semantic tokens |
| **Content** | Markdown with YAML frontmatter; JSON indexes | Local repository files | Build-time content source; no database |
| **Markdown Rendering** | Approved Markdown renderer selected during scaffold | Current stable version | Renders project documentation and blog posts |
| **Schema Validation** | Zod or equivalent strict validator | Current stable version | Validates content frontmatter and JSON at build time |
| **Hosting** | Vercel Hobby Plan | Current platform configuration | Static-friendly deployment and preview workflows |
| **AI Integration** | Vercel AI SDK / LangGraph | Deferred | Not used in P0; reserved for separately specified future feature |

### 2.2 System Architecture Diagram

```text
+---------------------------------------------------------------------+
|                            VISITOR BROWSER                          |
|                                                                     |
|   Next.js App Router UI: Home | Projects | Certifications | Blog    |
+----------------------------------+----------------------------------+
                                   |
                                   | HTTPS
                                   v
+---------------------------------------------------------------------+
|                             VERCEL CDN                              |
|                                                                     |
|                 Static HTML / CSS / JS / optimized assets           |
+----------------------------------+----------------------------------+
                                   |
                                   | Build-time content access
                                   v
+---------------------------------------------------------------------+
|                       NEXT.JS BUILD PIPELINE                        |
|                                                                     |
|  /content/projects/*.mdx  --> Frontmatter + Markdown validation     |
|  /content/certifications/*.mdx --> Certification validation         |
|  /content/blog/*.mdx --> Blog validation and metadata extraction    |
|  /content/site.json --> Global site, profile, and contact metadata  |
|                                                                     |
|  Output: statically generated routes and content collections        |
+---------------------------------------------------------------------+
```

### 2.3 Rendering Strategy
- Use Next.js App Router static generation for all P0 routes.
- Read Markdown and JSON content during the build process.
- Generate static routes for project and blog slugs.
- Do not use runtime server functions, database connections, route handlers, or API routes in P0.
- Static export may be enabled only if all selected Next.js features remain compatible; Vercel can host the standard Next.js build without requiring `next export`.

---

## 3. Detailed Data & State Architecture

### 3.1 Content Architecture
All content entities, frontmatter fields, TypeScript contracts, validation constraints, file locations, and relationships are defined exclusively in `AGENTS.md`.

The application must not define duplicate schema definitions in `PRD.md`, `TRD.md`, `APP_FLOW.md`, `design.md`, or implementation code.

### 3.2 Build-Time Data Flow

```text
Local content files
        |
        v
Content loader
        |
        v
Strict schema validation
        |
        +--> Invalid content: fail build with file path and validation error
        |
        +--> Valid content: normalized typed collection
                          |
                          v
              Static route generation
                          |
                          v
             HTML, CSS, JS, and optimized assets
```

### 3.3 Client State Model
P0 has no persistent client state and no server state synchronization.

| State Domain | Owner | Persistence | Example |
| :--- | :--- | :--- | :--- |
| Navigation visibility | `[State Hook]` in header component | Component state | Mobile navigation open/closed |
| Project filters | `[State Hook]` in projects index | URL search parameters preferred | Selected technology/status filters |
| Blog filters | `[State Hook]` in blog index | URL search parameters preferred | Selected tag |
| Theme preference | Deferred | Not in P0 unless dark mode is approved | Light/dark preference |

### 3.4 System State Transition Model

```text
[content_draft]
      |
      | Content file committed to repository
      v
[build_validation]
      |
      +--> Invalid schema --> [build_failed]
      |
      +--> Valid schema --> [static_generation]
                               |
                               v
                        [deployed_preview]
                               |
                               | Merge to production branch
                               v
                         [deployed_production]
```

- `content_draft`: Content exists locally but is not yet validated by a build.
- `build_validation`: Frontmatter and JSON are checked against `AGENTS.md`.
- `build_failed`: Terminal failure state; deployment must not proceed.
- `static_generation`: Valid content is transformed into static pages.
- `deployed_preview`: Vercel preview deployment generated from a non-production branch.
- `deployed_production`: Public production deployment.

---

## 4. Interface Specifications

### 4.1 Internal Content Interface
The application reads only local content through typed loader modules. No public HTTP API is exposed in P0.

| Internal Module | Responsibility | Input | Output |
| :--- | :--- | :--- | :--- |
| `getSiteConfig()` | Load global site metadata | `content/site.json` | Typed `SiteConfig` |
| `getProjects()` | Load all valid projects | `/content/projects/*.mdx` | Sorted `Project[]` |
| `getProjectBySlug(slug)` | Load one project | Valid project slug | `Project | null` |
| `getCertifications()` | Load all certifications | `/content/certifications/*.mdx` | Sorted `Certification[]` |
| `getBlogPosts()` | Load all blog posts | `/content/blog/*.mdx` | Sorted `BlogPost[]` |
| `getBlogPostBySlug(slug)` | Load one blog post | Valid blog slug | `BlogPost | null` |

### 4.2 Route Contract
Canonical route paths are defined in `APP_FLOW.md`. Route implementations must use the Next.js App Router conventions defined in this document.

### 4.3 Error and Not-Found Behavior
- Invalid static route parameters must render the application not-found boundary.
- Content validation failures must fail `next build` with a descriptive error containing the affected file path and schema issue.
- Missing optional external links must not render broken or placeholder links.
- Missing required content fields must fail validation; the UI must not supply default values for required fields.

---

## 5. Sequence Diagram & Key System Workflows

### 5.1 Content Publishing Workflow

```text
Content Owner            Repository              Build Pipeline             Vercel
     |                       |                         |                       |
     |-- Add/edit MDX/JSON ->|                         |                       |
     |                       |-- Push branch --------->|                       |
     |                       |                         |-- Validate schemas -->|
     |                       |                         |<-- Invalid: fail -----|
     |                       |                         |-- Generate static ----|
     |                       |                         |-- Deploy preview ---->|
     |                       |                         |                       |
     |                       |-- Merge production ---->|                       |
     |                       |                         |-- Build production -->|
     |                       |                         |-- Deploy production ->|
     |                       |                         |                       |
     |<------------------------- Public static site ------------------------|
```

### 5.2 Project Evaluation Workflow

```text
Visitor                 Projects Index              Project Detail
   |                          |                           |
   |-- Open /projects ------->|                           |
   |<-- Project summaries ----|                           |
   |                          |                           |
   |-- Select project ------->|                           |
   |                          |-- Navigate by slug ------>|
   |                          |                           |-- Render metadata
   |                          |                           |-- Render Markdown docs
   |<-- Case study page ----------------------------------|
   |                          |                           |
   |-- Select repository ---->|                           |
   |<-- External GitHub link ----------------------------|
```

---

## 6. Non-Functional Requirements (NFRs) & SLA Matrix

### 6.1 Performance Benchmarks
These are the exclusive system-wide performance targets for this project.

| Metric | Target | Measurement Method |
| :--- | :--- | :--- |
| Largest Contentful Paint (LCP) | `< 2.5 s` on mid-tier mobile hardware | Lighthouse / PageSpeed Insights |
| Interaction to Next Paint (INP) | `< 200 ms` | Field data when available; lab proxy otherwise |
| Cumulative Layout Shift (CLS) | `< 0.1` | Lighthouse / PageSpeed Insights |
| First Contentful Paint (FCP) | `< 1.8 s` | Lighthouse |
| Total Blocking Time (TBT) | `< 200 ms` | Lighthouse |
| Initial JavaScript payload per P0 route | Minimize; no unused large client libraries | Build analyzer / bundle review |
| Static image delivery | Responsive, optimized, explicitly sized | Next.js image conventions and build audit |
| Build time | `< 3 minutes` for the P0 content set | CI or local `npm run build` timing |

### 6.2 Scalability & Throughput Targets
- The site must serve static assets through Vercel’s CDN without application-owned scaling logic.
- The MVP must support portfolio-scale content: at least 25 projects, 50 certifications/badges, and 100 blog posts without architectural changes.
- Content growth must not require a database or API introduction.

### 6.3 Availability & Reliability
- **Hosting availability:** Follow Vercel Hobby Plan service availability; no custom uptime SLA is offered by this project.
- **Deployment reliability:** A production deployment must succeed only after `npm run build`, type checking, linting, content validation, and tests pass.
- **Rollback strategy:** Redeploy the last known-good production deployment through Vercel; do not attempt runtime patching.

### 6.4 Security, Privacy & Data Protection
- **Authentication:** None; the site is fully public.
- **Authorization:** Not applicable.
- **Visitor data collection:** None in P0.
- **Secrets:** No secret values are required for P0. Any future integration secret must be configured through Vercel environment variables and never committed to the repository.
- **External links:** Use `rel="noopener noreferrer"` for links opening in a new tab.
- **Content trust:** Display only owner-curated content; do not fetch or render untrusted third-party content at runtime.

### 6.5 Accessibility
- **Standard:** WCAG 2.1 Level AA.
- **Keyboard operation:** All interactive elements must be reachable and operable by keyboard.
- **Focus visibility:** Every focusable element must have a visible focus indicator.
- **Semantic structure:** Use landmark elements, logical heading order, and descriptive link text.
- **Color contrast:** Minimum 4.5:1 for normal text and 3:1 for large text and essential UI boundaries.
- **Motion:** Respect `prefers-reduced-motion`.

### 6.6 Browser & Platform Support
- Chrome, Edge, Firefox, and Safari: latest two stable versions.
- iOS Safari and Android Chrome: current major version.
- Responsive breakpoints: mobile `375px`, tablet `768px`, desktop `1024px+`, wide desktop `1440px`.

---

## 7. Third-Party Integrations & Dependencies

| Service | Provider | Integration Pattern | P0 Status | Failure Strategy |
| :--- | :--- | :--- | :--- | :--- |
| Vercel | Vercel | Git-based deployment | Required | Use last known-good deployment; inspect build logs |
| GitHub | GitHub | Static external links | Optional | Render only configured valid URLs |
| Certification issuers | Issuer-specific | Static external verification links | Optional | Omit verification link when unavailable |
| Vercel AI SDK | Vercel | Future client/server AI integration | Not in P0 | Do not implement |
| LangGraph | LangChain | Future orchestration integration | Not in P0 | Do not implement |

---

## 8. Deployment, CI/CD & Rollback Strategy

### 8.1 Local Verification Pipeline
The canonical local commands are:

1. Install dependencies: `npm ci`
2. Lint: `npm run lint`
3. Type-check: `npm run typecheck`
4. Test: `npm test`
5. Build: `npm run build`

The scaffold must define these scripts in `package.json`.

### 8.2 CI/CD Pipeline
1. **Pull request trigger:** Run `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`.
2. **Preview deployment:** Vercel creates a preview deployment for every non-production branch.
3. **Production deployment:** Merge to the configured production branch only after all checks pass.
4. **Post-deploy verification:** Confirm homepage, projects index, certifications page, blog index, one project detail route, and one blog detail route return successfully.

### 8.3 Deployment Constraints
- No API routes, route handlers, middleware requiring server execution, or database connections may be introduced in P0.
- Static assets must remain within Vercel Hobby Plan limits.
- Large binary assets must be optimized or externally hosted only when their source and licensing are explicitly documented.

### 8.4 Rollback Plan

| Failure Trigger | Immediate Action | Mitigation Procedure |
| :--- | :--- | :--- |
| Build validation failure | Stop deployment | Fix the affected content file or schema usage; rerun `npm run build` |
| Production regression | Roll back deployment | Redeploy last known-good Vercel deployment |
| Broken external link | Content correction | Update or remove the URL in the relevant content file |
| Accessibility defect | Block release | Fix component semantics or styling; rerun accessibility checks |
| Performance regression | Block release | Profile bundle/assets; optimize before redeployment |

---

## 9. QA Testability & Acceptance Criteria

### Definition of Done (DoD) Checklist
- [ ] `npm ci` completes successfully.
- [ ] `npm run lint` passes with zero errors.
- [ ] `npm run typecheck` passes with zero errors.
- [ ] `npm test` passes.
- [ ] `npm run build` completes successfully.
- [ ] All content files validate against `AGENTS.md`.
- [ ] All P0 routes render without console errors.
- [ ] All interactive components are keyboard accessible.
- [ ] Automated accessibility checks pass at WCAG 2.1 AA.
- [ ] Core Web Vitals targets in Section 6.1 are met.
- [ ] Vercel preview and production deployments are verified.