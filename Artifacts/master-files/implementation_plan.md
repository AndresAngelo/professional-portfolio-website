# implementation_plan.md

# Implementation Plan & Execution Roadmap

> **Document Status:** Proposed  
> **Last Updated:** 2026-10-20  
> **Target Release Version:** `v1.0.0`  
> **PRD Alignment:** `PRD.md`  
> **TRD Alignment:** `TRD.md`  
> **App Flow Alignment:** `APP_FLOW.md`  
> **Design Alignment:** `design.md`  
> **Schema & Repository Context:** `AGENTS.md`

---

## 1. Executive Summary & Agentic Execution Rules

### 1.1 Purpose & Execution Model
This roadmap implements the P0 static portfolio in deterministic, verifiable phases. It is intended for execution by human engineers and autonomous coding agents.

```text
Phase 1: Repository Foundation
        |
        v
Phase 2: Content Contracts & Validation
        |
        v
Phase 3: Global Layout & Design System
        |
        v
Phase 4: Core Routes & Content Rendering
        |
        v
Phase 5: Quality, Accessibility & Performance
        |
        v
Phase 6: Vercel Deployment & Launch
```

### 1.2 Non-Negotiable Instructions for AI Coding Agents
1. **Atomic progression:** Complete each phase and its verification checklist before beginning the next.
2. **SSOT adherence:** Use `AGENTS.md` for all content schemas, directory paths, naming, and validation rules.
3. **No scope expansion:** Do not implement P1 or P2 features, APIs, databases, authentication, analytics, or AI features.
4. **Design-token adherence:** Use `design.md` tokens; do not hardcode visual values.
5. **Verification before completion:** Every task must pass its specified commands.
6. **Content safety:** Never fabricate project, certification, badge, event, contact, or URL data.

---

## 2. Dependency Matrix & Prerequisites

| Dependency / Requirement | Status | Required Owner / Artifact | Verification Command |
| :--- | :--- | :--- | :--- |
| Node.js and package manager installed | Pending | Engineering environment | `node -v && npm -v` |
| Next.js App Router project initialized | Pending | Engineering | `npm run dev` |
| TypeScript strict mode enabled | Pending | Engineering | `npm run typecheck` |
| Tailwind CSS configured | Pending | Engineering | `npm run build` |
| Content directories created | Pending | Engineering | `npm run typecheck` |
| Content schemas implemented | Pending | Engineering | `npm test` |
| SGDS-inspired tokens finalized | Pending | Design Owner | `npm run build` |
| Vercel project connected | Pending | Owner | Vercel dashboard / `vercel --prod` |

---

## 3. Phased Execution Roadmap

```text
Phase 1: Repository Foundation & Toolchain
└── Task 1.1: Initialize Next.js, TypeScript, Tailwind, and scripts
└── Task 1.2: Configure strict quality gates

Phase 2: Content Architecture & Validation
└── Task 2.1: Implement canonical content contracts
└── Task 2.2: Implement content loaders and Markdown pipeline
└── Task 2.3: Add seed content and validation tests

Phase 3: Global Layout & SGDS-Inspired UI
└── Task 3.1: Implement design tokens and base styles
└── Task 3.2: Implement header, footer, and navigation

Phase 4: Core Routes & Content Experiences
└── Task 4.1: Implement homepage
└── Task 4.2: Implement projects index and detail
└── Task 4.3: Implement certifications page
└── Task 4.4: Implement blog index and detail
└── Task 4.5: Implement not-found and metadata

Phase 5: Quality, Accessibility & Performance
└── Task 5.1: Add unit and content tests
└── Task 5.2: Run accessibility and performance audits

Phase 6: Deployment & Launch
└── Task 6.1: Configure Vercel deployment
└── Task 6.2: Execute production launch checklist
```

---

## 4. Detailed Task Specifications

### Phase 1: Repository Foundation & Toolchain

#### Task 1.1: Initialize Next.js, TypeScript, Tailwind, and Scripts
- **Target Files:**
  - `package.json`
  - `next.config.ts`
  - `tsconfig.json`
  - `tailwind.config.ts`
  - `src/app/layout.tsx`
  - `src/app/page.tsx`
  - `README.md`
- **Dependencies:** None
- **Step-by-Step Instructions:**
  1. Initialize a Next.js App Router project with TypeScript and Tailwind CSS.
  2. Enable TypeScript strict mode.
  3. Configure the canonical scripts: `dev`, `build`, `start`, `lint`, `typecheck`, and `test`.
  4. Create the initial root layout and homepage route.
  5. Document local setup and verification commands in `README.md`.
- **Verification Checklist & Commands:**
  - [ ] Dependencies install: `npm ci`
  - [ ] Lint passes: `npm run lint`
  - [ ] Type checking passes: `npm run typecheck`
  - [ ] Tests pass: `npm test`
  - [ ] Production build passes: `npm run build`

#### Task 1.2: Configure Strict Quality Gates
- **Target Files:**
  - `.eslintrc.json` or equivalent lint configuration
  - `tsconfig.json`
  - `tests/`
  - `package.json`
- **Dependencies:** Task 1.1
- **Step-by-Step Instructions:**
  1. Configure linting for TypeScript, accessibility-safe JSX patterns, and import consistency.
  2. Enable strict TypeScript compiler options.
  3. Add a test runner and an initial smoke test.
  4. Ensure `npm run build` fails on type or lint errors according to the configured pipeline.
- **Verification Checklist & Commands:**
  - [ ] `npm run lint`
  - [ ] `npm run typecheck`
  - [ ] `npm test`
  - [ ] `npm run build`

---

### Phase 2: Content Architecture & Validation

#### Task 2.1: Implement Canonical Content Contracts
- **Target Files:**
  - `src/types/content.ts`
  - `src/content/schemas/site.ts`
  - `src/content/schemas/project.ts`
  - `src/content/schemas/certification.ts`
  - `src/content/schemas/blog.ts`
- **Dependencies:** Task 1.1
- **Step-by-Step Instructions:**
  1. Implement the exact TypeScript contracts from `AGENTS.md` Section 4.2.
  2. Implement schema validators for `SiteConfig`, `Project`, `Certification`, and `BlogPost`.
  3. Enforce slug, date, URL, enum, array, and required-field rules from `AGENTS.md` Section 5.
  4. Prohibit `any`, implicit `any`, non-null assertions, and unjustified casts.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/content/schemas`
  - [ ] `npm run build`

#### Task 2.2: Implement Content Loaders and Markdown Pipeline
- **Target Files:**
  - `src/content/loaders/site.ts`
  - `src/content/loaders/projects.ts`
  - `src/content/loaders/certifications.ts`
  - `src/content/loaders/blog.ts`
  - `src/content/markdown/renderer.ts`
- **Dependencies:** Task 2.1
- **Step-by-Step Instructions:**
  1. Implement `getSiteConfig()`, `getProjects()`, `getProjectBySlug()`, `getCertifications()`, `getBlogPosts()`, and `getBlogPostBySlug()`.
  2. Read content exclusively from the paths defined in `AGENTS.md` Section 3.
  3. Validate every content file before returning it.
  4. Sort projects by `displayOrder`; sort certifications by `displayOrder`; sort blog posts by `publishedAt` descending.
  5. Exclude `draft: true` blog posts from production collections and route generation.
  6. Render Markdown content through a typed Markdown pipeline.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/content/loaders`
  - [ ] `npm run build`

#### Task 2.3: Add Seed Content and Validation Tests
- **Target Files:**
  - `content/site.json`
  - `content/projects/*.mdx`
  - `content/certifications/*.mdx`
  - `content/blog/*.mdx`
  - `tests/content/schema-validation.test.ts`
  - `tests/content/loader.test.ts`
- **Dependencies:** Task 2.2
- **Step-by-Step Instructions:**
  1. Add one valid example for each content type using only real or explicitly placeholder-labeled content.
  2. Add tests proving valid content loads successfully.
  3. Add tests proving invalid slug, date, enum, missing required field, and invalid URL cases fail validation.
  4. Add a test proving draft blog posts are excluded.
- **Verification Checklist & Commands:**
  - [ ] `npm test`
  - [ ] `npm run typecheck`
  - [ ] `npm run build`

---

### Phase 3: Global Layout & SGDS-Inspired UI

#### Task 3.1: Implement Design Tokens and Base Styles
- **Target Files:**
  - `tailwind.config.ts`
  - `src/app/globals.css`
  - `src/components/ui/Button.tsx`
  - `src/components/ui/Card.tsx`
  - `src/components/ui/Tag.tsx`
  - `src/components/ui/Badge.tsx`
  - `src/components/ui/ExternalLink.tsx`
  - `src/components/ui/EmptyState.tsx`
- **Dependencies:** Task 1.1
- **Step-by-Step Instructions:**
  1. Map the semantic color, typography, spacing, radius, elevation, and motion tokens from `design.md`.
  2. Implement reusable Button, Card, Tag, Badge, ExternalLink, and EmptyState components.
  3. Ensure visible focus states and WCAG 2.1 AA contrast.
  4. Respect `prefers-reduced-motion`.
- **Verification Checklist & Commands:**
  - [ ] `npm run lint`
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/ui`
  - [ ] `npm run build`

#### Task 3.2: Implement Header, Footer, and Navigation
- **Target Files:**
  - `src/components/layout/SiteHeader.tsx`
  - `src/components/layout/SiteFooter.tsx`
  - `src/components/layout/MobileNavigation.tsx`
  - `src/components/layout/ContactLinks.tsx`
  - `src/app/layout.tsx`
- **Dependencies:** Task 3.1
- **Step-by-Step Instructions:**
  1. Implement global header with site identity and primary navigation.
  2. Implement accessible mobile navigation using local `[State Hook]` state only.
  3. Implement footer with copyright, contact channels, and social links.
  4. Mark the active route programmatically and visually.
  5. Hide unconfigured contact channels.
- **Verification Checklist & Commands:**
  - [ ] `npm run lint`
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/layout`
  - [ ] `npm run build`

---

### Phase 4: Core Routes & Content Experiences

#### Task 4.1: Implement Homepage
- **Target Files:**
  - `src/app/page.tsx`
  - `src/components/home/HeroSection.tsx`
  - `src/components/home/FeaturedProjects.tsx`
  - `src/components/home/SkillsSnapshot.tsx`
  - `src/components/home/RecentActivity.tsx`
- **Dependencies:** Task 2.2, Task 3.2
- **Step-by-Step Instructions:**
  1. Render profile, introduction, and primary actions from `SiteConfig`.
  2. Render up to 3 featured projects.
  3. Render recent non-draft blog posts when available.
  4. Implement empty states for missing featured projects or posts.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/home`
  - [ ] `npm run build`

#### Task 4.2: Implement Projects Index and Detail
- **Target Files:**
  - `src/app/projects/page.tsx`
  - `src/app/projects/[slug]/page.tsx`
  - `src/components/projects/ProjectsIndex.tsx`
  - `src/components/projects/ProjectFilterBar.tsx`
  - `src/components/projects/ProjectGrid.tsx`
  - `src/components/projects/ProjectCard.tsx`
  - `src/components/projects/ProjectHeader.tsx`
  - `src/components/projects/ProjectMetadata.tsx`
  - `src/components/projects/BuildDocumentation.tsx`
  - `src/components/projects/ProjectLinks.tsx`
- **Dependencies:** Task 2.2, Task 3.1
- **Step-by-Step Instructions:**
  1. Implement the projects index with technology and status filters.
  2. Store active filters in URL search parameters.
  3. Implement default, filtered, empty-result, and no-content states.
  4. Generate static routes for every valid non-draft project slug.
  5. Render project metadata and Markdown build documentation.
  6. Omit repository, live-demo, and documentation links when not configured.
  7. Render not-found for invalid slugs.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/projects`
  - [ ] `npm test -- src/app/projects`
  - [ ] `npm run build`

#### Task 4.3: Implement Certifications Page
- **Target Files:**
  - `src/app/certifications/page.tsx`
  - `src/components/certifications/CertificationsIndex.tsx`
  - `src/components/certifications/CertificationCategorySection.tsx`
  - `src/components/certifications/CertificationCard.tsx`
- **Dependencies:** Task 2.2, Task 3.1
- **Step-by-Step Instructions:**
  1. Render certifications grouped by category when category data exists.
  2. Render badge images with meaningful alternative text.
  3. Render verification links only when configured.
  4. Implement empty state for no certifications.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/certifications`
  - [ ] `npm run build`

#### Task 4.4: Implement Blog Index and Detail
- **Target Files:**
  - `src/app/blog/page.tsx`
  - `src/app/blog/[slug]/page.tsx`
  - `src/components/blog/BlogIndex.tsx`
  - `src/components/blog/BlogFilterBar.tsx`
  - `src/components/blog/BlogPostList.tsx`
  - `src/components/blog/BlogPostCard.tsx`
  - `src/components/blog/BlogPostHeader.tsx`
  - `src/components/blog/MarkdownContent.tsx`
  - `src/components/blog/PostNavigation.tsx`
- **Dependencies:** Task 2.2, Task 3.1
- **Step-by-Step Instructions:**
  1. Implement reverse-chronological blog index.
  2. Implement tag filtering using URL search parameters.
  3. Render post metadata, Markdown content, and optional external event link.
  4. Exclude drafts from index, homepage, and static route generation.
  5. Render not-found for invalid slugs.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/components/blog`
  - [ ] `npm test -- src/app/blog`
  - [ ] `npm run build`

#### Task 4.5: Implement Not-Found and Metadata
- **Target Files:**
  - `src/app/not-found.tsx`
  - `src/app/layout.tsx`
  - `src/app/projects/[slug]/page.tsx`
  - `src/app/blog/[slug]/page.tsx`
  - `src/lib/seo.ts`
- **Dependencies:** Task 4.1–Task 4.4
- **Step-by-Step Instructions:**
  1. Implement a global not-found boundary.
  2. Add unique titles and descriptions for all P0 routes.
  3. Add route-specific metadata for project and blog detail pages.
  4. Add Open Graph metadata from configured content.
  5. Configure canonical URLs using `SiteConfig.siteUrl`.
- **Verification Checklist & Commands:**
  - [ ] `npm run typecheck`
  - [ ] `npm test -- src/lib`
  - [ ] `npm run build`

---

### Phase 5: Quality, Accessibility & Performance

#### Task 5.1: Add Unit and Content Tests
- **Target Files:**
  - `tests/content/schema-validation.test.ts`
  - `tests/content/loader.test.ts`
  - `tests/components/navigation.test.tsx`
  - `tests/components/project-filters.test.tsx`
  - `tests/components/blog-filters.test.tsx`
  - `tests/routes/static-generation.test.ts`
- **Dependencies:** Phase 4
- **Step-by-Step Instructions:**
  1. Test every EARS acceptance criterion in `APP_FLOW.md` Section 4 that is automatable.
  2. Test content validation failures and successful loaders.
  3. Test filtering, empty states, draft exclusion, and invalid-slug not-found behavior.
  4. Test that no API route or database dependency exists in P0.
- **Verification Checklist & Commands:**
  - [ ] `npm test`
  - [ ] `npm run typecheck`
  - [ ] `npm run lint`
  - [ ] `npm run build`

#### Task 5.2: Run Accessibility and Performance Audits
- **Target Files:**
  - `tests/accessibility/`
  - `README.md`
  - `docs/qa-report.md`
- **Dependencies:** Task 5.1
- **Step-by-Step Instructions:**
  1. Run automated accessibility checks against all P0 routes.
  2. Manually verify keyboard navigation, focus visibility, heading order, landmarks, and screen-reader labels.
  3. Run Lighthouse or an equivalent Core Web Vitals audit.
  4. Optimize images, fonts, scripts, and CSS if any `TRD.md` Section 6.1 target is missed.
  5. Record results and remediation actions in `docs/qa-report.md`.
- **Verification Checklist & Commands:**
  - [ ] `npm run build`
  - [ ] `npm run lint`
  - [ ] `npm run typecheck`
  - [ ] `npm test`
  - [ ] Accessibility audit passes WCAG 2.1 AA
  - [ ] Core Web Vitals targets pass

---

### Phase 6: Deployment & Launch

#### Task 6.1: Configure Vercel Deployment
- **Target Files:**
  - `README.md`
  - `next.config.ts`
  - `.gitignore`
  - `docs/deployment.md`
- **Dependencies:** Phase 5
- **Step-by-Step Instructions:**
  1. Connect the repository to a Vercel project using the Hobby Plan.
  2. Configure the production branch and build command.
  3. Ensure no secret environment variables are required for P0.
  4. Verify preview deployment for a feature branch.
  5. Document deployment and rollback procedure.
- **Verification Checklist & Commands:**
  - [ ] `npm ci`
  - [ ] `npm run lint`
  - [ ] `npm run typecheck`
  - [ ] `npm test`
  - [ ] `npm run build`
  - [ ] Vercel preview deployment succeeds
  - [ ] Vercel production deployment succeeds

#### Task 6.2: Execute Production Launch Checklist
- **Target Files:**
  - `docs/launch-checklist.md`
  - `README.md`
- **Dependencies:** Task 6.1
- **Step-by-Step Instructions:**
  1. Verify homepage, projects index, certifications, blog index, one project detail route, and one blog detail route.
  2. Verify all configured external links resolve to intended destinations.
  3. Verify no draft blog post is publicly accessible.
  4. Verify mobile, tablet, and desktop rendering.
  5. Verify no console errors and no unintended network requests to custom APIs.
  6. Confirm final production URL and share through approved professional channels.
- **Verification Checklist & Commands:**
  - [ ] `npm run build`
  - [ ] `npm test`
  - [ ] Manual route smoke test passes
  - [ ] Accessibility spot-check passes
  - [ ] Vercel production deployment is live

---

## 5. Rollback & Contingency Plan

| Failure Trigger | Immediate Action | Mitigation Command / Procedure |
| :--- | :--- | :--- |
| Content schema validation failure | Stop deployment | Correct affected file using `AGENTS.md`; run `npm test && npm run build` |
| TypeScript failure | Stop deployment | Fix types; run `npm run typecheck && npm run build` |
| Lint failure | Stop deployment | Fix violations; run `npm run lint` |
| Test failure | Stop deployment | Repair implementation or test; run `npm test` |
| Production visual regression | Roll back deployment | Redeploy last known-good Vercel deployment |
| Broken external link | Content correction | Update or remove URL in relevant content file; rebuild |
| Accessibility regression | Block release | Fix semantics, labels, contrast, or focus behavior; rerun audits |
| Performance regression | Block release | Optimize assets/bundle; rerun Lighthouse and `npm run build` |

---

## 6. Execution Status Tracking (Agent State Dashboard)

| Task ID | Task Summary | Status | Automated Test Result | Human Sign-Off |
| :--- | :--- | :--- | :--- | :--- |
| `Task 1.1` | Initialize Next.js, TypeScript, Tailwind, and scripts | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 1.2` | Configure strict quality gates | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 2.1` | Implement canonical content contracts | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 2.2` | Implement content loaders and Markdown pipeline | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 2.3` | Add seed content and validation tests | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 3.1` | Implement design tokens and base styles | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 3.2` | Implement header, footer, and navigation | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 4.1` | Implement homepage | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 4.2` | Implement projects index and detail | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 4.3` | Implement certifications page | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 4.4` | Implement blog index and detail | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 4.5` | Implement not-found and metadata | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 5.1` | Add unit and content tests | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 5.2` | Run accessibility and performance audits | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 6.1` | Configure Vercel deployment | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |
| `Task 6.2` | Execute production launch checklist | `[Not Started / In Progress / Done]` | `[PASS / FAIL]` | `[ ]` |