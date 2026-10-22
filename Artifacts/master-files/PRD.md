# PRD.md

# Product Requirements Document (PRD)

> **Document Status:** Approved  
> **Last Updated:** 2026-10-20  
> **Product Manager:** Angelo Andres  
> **Contributors:** Zero-Hallucination Engineering Studio  
> **SSOT References:** Content schemas and repository taxonomy are defined exclusively in `AGENTS.md`. System performance targets are defined exclusively in `TRD.md`.

---

## 1. Executive Summary

### Product Name
`personal-website-portfolio-v2`

### Problem Statement
Recruiters, hiring managers, technical administrators, and prospective collaborators need a fast, credible way to evaluate Angelo Andres’s engineering work, certifications, and community participation. Scattered repositories, PDFs, and social profiles make it difficult to assess project quality, implementation decisions, and hands-on technical depth.

### Proposed Solution
A publicly hosted, static developer portfolio that presents curated projects with build documentation, certifications and badges, and a blog documenting meetups and hackathon participation. The MVP uses locally managed Markdown and JSON content, Next.js App Router, TypeScript, Tailwind CSS, and Vercel hosting.

### Success Metrics
- **Portfolio usability:** At least 90% of tested recruiters can locate a project case study, certification, and contact link within 3 minutes.
- **Technical credibility:** Every P0 project entry exposes a repository link, technology list, and build documentation.
- **Accessibility:** All P0 pages pass automated WCAG 2.1 AA checks.
- **Performance:** All P0 pages meet the Core Web Vitals targets defined in `TRD.md` Section 6.
- **Maintainability:** New project, certification, or blog entries can be published by editing content files only, without application-code changes.

### Launch Target
`MVP launch: Q4 2026`

---

## 2. Background & Context

### Why Now?
The existing portfolio must communicate both product-facing capability and engineering rigor. A specification-driven, statically generated site provides a low-cost, maintainable platform while demonstrating modern Next.js, TypeScript, design-system, and deployment practices.

### User Research & Insights
- **Research Methods:** Recruiter expectations review, developer-portfolio benchmarking, accessibility review, and personal project inventory.
- **Key Findings:**
  1. Technical evaluators prioritize source links, architecture notes, and evidence of real implementation over visual polish alone.
  2. Recruiters need a rapid path from homepage to skills, projects, certifications, and contact details.
  3. Community participation adds credibility when presented as dated, verifiable activity rather than generic claims.

### User Quotes
> “I want to see what you built, how you built it, and whether I can verify it.”

---

## 3. Market Analysis

### Competitive Landscape
Developer portfolios commonly range from single-page resume sites to full case-study platforms. Many lack structured build documentation, accessible design, or clear evidence of technical decision-making.

### Differentiation
`personal-website-portfolio-v2` combines:
- Structured project case studies with build documentation.
- Verifiable certifications and badges.
- A dated participation log for meetups and hackathons.
- SGDS-inspired accessible, high-trust visual standards.
- A fully static, zero-backend MVP suitable for Vercel Hobby Plan hosting.

---

## 4. Goals & Success Criteria

### Business Goals
1. Establish a professional, credible public engineering presence.
2. Increase inbound recruiter, hiring-manager, and collaboration inquiries.
3. Demonstrate capability in specification-driven, accessible frontend engineering.

### User Goals
1. Quickly understand Angelo’s technical profile and focus areas.
2. Evaluate selected projects through summaries, technologies, repositories, and build documentation.
3. Verify certifications, badges, and community participation.
4. Contact Angelo or access professional profiles without friction.

### Detailed Success Metrics

| Metric | Baseline | Target | Timeframe | Measurement Method |
| :--- | :--- | :--- | :--- | :--- |
| P0 route availability | N/A | 100% | Launch | `npm run build` and Vercel deployment checks |
| Lighthouse accessibility score | N/A | 95+ | Launch | Lighthouse CI or manual Lighthouse audit |
| P0 project entries with repository links | N/A | 100% | Launch | Content validation |
| Contact-action discoverability | N/A | Present in global header and footer | Launch | Manual QA |
| Content-only publishing workflow | N/A | No source-code change required | Launch | Add sample content and rebuild |

---

## 5. Non-Goals (Out of Scope)

- No backend database.
- No user registration, authentication, profiles, or accounts.
- No user-generated content.
- No custom public API endpoints for the MVP.
- No analytics requiring personal-data collection.
- No CMS integration for the MVP.
- No comment system.
- No payment, e-commerce, or subscription functionality.
- No production AI chat feature in the P0 scope.
- No multi-language localization in the P0 scope.

---

## 6. User Personas & Key Use Cases

### Personas

#### Primary Persona: Technical Recruiter
- **Role:** Sources and screens engineering candidates.
- **Goals:** Rapidly assess skills, project quality, certifications, and contact options.
- **Pain Points:** Vague project descriptions, missing source links, unclear technology depth.
- **Technical Proficiency:** Intermediate.
- **Context:** Desktop or mobile, typically reviewing multiple candidates quickly.

#### Secondary Persona: Hiring Manager / Technical Administrator
- **Role:** Evaluates hands-on engineering capability and system-design maturity.
- **Goals:** Review implementation decisions, architecture notes, and build documentation.
- **Pain Points:** Portfolios that show outputs but omit constraints, trade-offs, and verification.
- **Technical Proficiency:** Advanced.
- **Context:** Desktop, deeper project evaluation.

#### Tertiary Persona: Co-developer / Collaborator
- **Role:** Potential open-source contributor, hackathon teammate, or technical peer.
- **Goals:** Identify interests, community activity, collaboration history, and contact channels.
- **Pain Points:** Difficulty finding current activity or relevant project context.
- **Technical Proficiency:** Advanced.
- **Context:** Desktop or mobile.

---

### Key Use Cases

#### Use Case 1: Evaluate a Portfolio Project
- **Actor:** Technical Recruiter or Hiring Manager.
- **Preconditions:** At least one published project exists.
- **Flow:**
  1. **User:** Opens the homepage.
  2. **System:** Displays profile introduction, core skills, featured projects, and primary navigation.
  3. **User:** Selects a featured project or opens the projects index.
  4. **System:** Displays the project detail page with summary, role, technologies, repository link, live-demo link when available, and build documentation.
- **Expected Outcome:** The user can assess project scope, implementation evidence, and technical depth.
- **Edge Cases:** If a live demo is unavailable, the page must clearly omit or disable that link without displaying a broken action.

#### Use Case 2: Verify Certifications
- **Actor:** Recruiter or Hiring Manager.
- **Preconditions:** Certification content has been published.
- **Flow:**
  1. **User:** Opens the certifications page.
  2. **System:** Displays certification and badge entries with issuer, date, credential identifier where public, and verification link where available.
  3. **User:** Selects a verification link.
  4. **System:** Opens the issuer verification destination in a new browser tab.
- **Expected Outcome:** The user can validate claimed credentials.
- **Edge Cases:** If no public verification URL exists, the entry must display only issuer-provided metadata and must not fabricate a verification link.

#### Use Case 3: Review Community Participation
- **Actor:** Co-developer or Recruiter.
- **Preconditions:** Blog posts exist for meetups or hackathons.
- **Flow:**
  1. **User:** Opens the blog index.
  2. **System:** Displays chronological entries with title, date, event type, summary, and tags.
  3. **User:** Opens a post.
  4. **System:** Renders Markdown content, event metadata, and optional external links.
- **Expected Outcome:** The user can review dated, contextual participation evidence.
- **Edge Cases:** If a post has no external event link, the page must render without a broken or placeholder link.

#### Use Case 4: Contact Angelo
- **Actor:** Any visitor.
- **Preconditions:** Contact details are configured in site metadata.
- **Flow:**
  1. **User:** Selects a contact action in the header, footer, or contact section.
  2. **System:** Opens the configured external contact channel.
- **Expected Outcome:** The visitor can initiate contact without submitting data to the website.
- **Edge Cases:** If no contact channel is configured, the contact action must not render.

---

## 7. Product Requirements

### Functional Requirements

#### Must Have (P0) — MVP

##### Homepage
- **Description:** Presents a concise professional introduction, core skill areas, featured projects, certifications preview, recent blog activity, and contact navigation.
- **User Story:** As a recruiter, I want to quickly understand Angelo’s technical profile and navigate to relevant evidence so that I can evaluate suitability efficiently.
- **Acceptance Criteria:**
  - [ ] Displays name, professional title, concise introduction, and primary call-to-action.
  - [ ] Displays up to 3 featured projects sourced from project content.
  - [ ] Displays links to Projects, Certifications, Blog, and Contact.
  - [ ] Displays recent blog entries when available.
  - [ ] Renders correctly at mobile, tablet, and desktop breakpoints.

##### Projects Index
- **Description:** Lists all published portfolio projects in a scannable, filterable index.
- **User Story:** As a hiring manager, I want to browse projects by technology and domain so that I can find relevant work quickly.
- **Acceptance Criteria:**
  - [ ] Displays project title, summary, primary technologies, completion/status metadata, and link to detail page.
  - [ ] Supports filtering by technology tag.
  - [ ] Supports filtering by project status where configured.
  - [ ] Displays an empty state when no projects match selected filters.
  - [ ] Sorts projects by configured display order or published date.

##### Project Detail
- **Description:** Presents a complete project case study, including problem, approach, architecture notes, technologies, outcomes, repository, and build documentation.
- **User Story:** As a technical evaluator, I want to review how a project was built so that I can assess engineering judgment and implementation quality.
- **Acceptance Criteria:**
  - [ ] Renders Markdown build documentation.
  - [ ] Displays project metadata from the schema defined in `AGENTS.md`.
  - [ ] Displays repository URL when available.
  - [ ] Displays live-demo URL when available.
  - [ ] Displays related technologies and tags.
  - [ ] Returns a user-friendly not-found state for an invalid project slug.

##### Certifications & Badges
- **Description:** Presents earned certifications, badges, issuers, dates, and verification links.
- **User Story:** As a recruiter, I want to verify certifications and badges so that I can trust the candidate’s stated qualifications.
- **Acceptance Criteria:**
  - [ ] Displays certification title, issuer, issue date, badge image where available, and verification URL where available.
  - [ ] Groups entries by category when category metadata is present.
  - [ ] Opens external verification links in a new tab with an accessible link label.
  - [ ] Displays an empty state when no certifications exist.

##### Blog / Participation Log
- **Description:** Presents dated blog posts covering meetups, hackathons, technical learning, and project updates.
- **User Story:** As a collaborator, I want to review Angelo’s community participation and technical activity so that I can understand current interests and experience.
- **Acceptance Criteria:**
  - [ ] Displays posts in reverse chronological order by published date.
  - [ ] Displays title, published date, reading time, event type where applicable, summary, and tags.
  - [ ] Renders Markdown post content.
  - [ ] Supports tag-based filtering.
  - [ ] Returns a user-friendly not-found state for an invalid post slug.

##### Global Navigation and Footer
- **Description:** Provides persistent, accessible navigation and site identity across all pages.
- **User Story:** As any visitor, I want consistent navigation so that I can move between portfolio sections without losing context.
- **Acceptance Criteria:**
  - [ ] Header displays site identity and navigation links.
  - [ ] Mobile viewport provides an accessible navigation control.
  - [ ] Footer displays copyright, social/professional links, and contact links where configured.
  - [ ] Current route is visually and programmatically indicated in navigation.

##### Static Contact Presentation
- **Description:** Presents contact channels without collecting or transmitting user data through the website.
- **User Story:** As a visitor, I want to contact Angelo through a preferred external channel so that I can start a conversation.
- **Acceptance Criteria:**
  - [ ] Displays configured email, LinkedIn, GitHub, or other public contact channels.
  - [ ] Does not include a website-hosted form in P0.
  - [ ] Does not collect, store, or transmit visitor personal data.
  - [ ] Hides unconfigured contact channels.

##### SEO and Social Metadata
- **Description:** Provides baseline discoverability and link-preview metadata.
- **User Story:** As a recruiter, I want clear page titles and preview metadata so that shared portfolio links are understandable.
- **Acceptance Criteria:**
  - [ ] Each route defines a unique page title and description.
  - [ ] Project, certification, and blog detail pages generate route-specific metadata.
  - [ ] Includes Open Graph metadata where content supports it.
  - [ ] Includes a canonical URL configuration.

#### Should Have (P1) — Post-Launch

##### Project Search
- **Description:** Provides keyword search across project titles, summaries, technologies, and documentation.
- **User Story:** As a hiring manager, I want to search projects by keyword so that I can locate relevant experience faster.
- **Acceptance Criteria:**
  - [ ] Searches locally generated project content.
  - [ ] Returns results without a backend API.
  - [ ] Displays no-results state.

##### Downloadable Resume
- **Description:** Provides a current PDF resume download.
- **User Story:** As a recruiter, I want to download a resume so that I can retain candidate details offline.
- **Acceptance Criteria:**
  - [ ] Serves a static PDF from public assets.
  - [ ] Uses an accessible, descriptive download link.
  - [ ] Displays file type in the link label.

#### Nice to Have (P2) — Future Consideration

##### Embedded Interactive AI Assistant
- **Description:** Provides a portfolio-scoped assistant that answers questions using locally curated portfolio content.
- **User Story:** As a recruiter, I want to ask questions about projects and experience so that I can evaluate fit interactively.
- **Acceptance Criteria:**
  - [ ] Uses only approved public portfolio content.
  - [ ] Clearly identifies AI-generated responses.
  - [ ] Does not collect or persist visitor conversation data in P2 unless explicitly approved.
  - [ ] Remains disabled by default until separately specified and reviewed.

---

## 8. User Experience & Design

### Links & Assets
- **Design System:** Singapore Government Design System (SGDS): https://www.designsystem.tech.gov.sg/
- **Visual Direction:** Clean, accessible, high-trust, government-inspired developer portfolio.
- **Detailed visual specification:** `design.md`.

### Key Interactions

#### Project Filtering
- **Trigger:** User selects a technology or status filter.
- **Behavior:** Project list updates to show only matching entries.
- **Feedback:** Active filter state is visible; empty result state is shown when no items match.

#### External Link Opening
- **Trigger:** User selects a repository, live demo, certification verification, or social link.
- **Behavior:** External destination opens in a new browser tab.
- **Feedback:** Link text communicates the external destination and new-tab behavior where appropriate.

#### Content Not Found
- **Trigger:** User opens an invalid project or blog slug.
- **Behavior:** Application renders the configured not-found page.
- **Feedback:** Clear message and navigation back to the relevant index or homepage.

### Design Principles for This Product
1. **Evidence over assertion:** Every major claim should link to verifiable work, documentation, or credentials.
2. **Clarity over decoration:** Use restrained SGDS-inspired visual hierarchy and generous whitespace.
3. **Accessible by default:** Meet WCAG 2.1 AA across all P0 experiences.
4. **Progressive disclosure:** Show concise summaries first; expose detailed build documentation on demand.
5. **Content-owned publishing:** Add or update portfolio content through structured Markdown and JSON files.

---

## 9. Technical Specifications

### System Architecture
The MVP is a statically rendered Next.js App Router application. Content is read from local Markdown and JSON files at build time. No runtime database, authentication service, or custom API is required.

Detailed architecture and performance requirements are defined in `TRD.md`.

### Data Model
All content schemas, frontmatter fields, TypeScript content contracts, directory taxonomy, validation rules, and naming conventions are defined exclusively in `AGENTS.md`.

### API Requirements
No custom public API endpoints are included in P0.

| Endpoint | Method | Purpose | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| None | N/A | Static-only MVP | N/A | N/A |

### Third-Party Integrations

| Service | Purpose | Authentication | MVP Requirement |
| :--- | :--- | :--- | :--- |
| Vercel | Static hosting and deployment | Vercel account authorization | Required |
| GitHub | Source-code links and potential README integration | Public links only | Optional |
| External certification issuers | Credential verification | Public links only | Optional |
| Vercel AI SDK / LangGraph | Future embedded AI feature | Provider-specific | Not used in P0 |

### Technical Constraints
- The MVP must operate as a static site with no server-side runtime dependencies.
- Vercel Hobby Plan constraints apply, including the platform’s static upload and usage limits.
- All content must be valid before deployment; invalid content must fail the build rather than silently render incomplete pages.
- No personal visitor data may be collected in P0.

---

## 10. Analytics & Tracking

P0 does not include visitor analytics or personal-data tracking.

| Event Name | Trigger | Properties Captured | Purpose |
| :--- | :--- | :--- | :--- |
| None | N/A | None | Privacy-preserving static MVP |

---

## 11. Go-to-Market Strategy

### Launch Plan
- **Alpha Testing:** Manual desktop and mobile review by the owner.
- **Accessibility Review:** Automated and manual keyboard/screen-reader checks.
- **Performance Review:** Lighthouse and Core Web Vitals validation.
- **Public Launch:** Deploy production branch to Vercel and share through professional profiles.

### Marketing & Positioning
- **Value Proposition:** A transparent, evidence-based developer portfolio demonstrating real engineering work, verified credentials, and community participation.
- **Key Messaging:** “Built to be evaluated: projects, documentation, certifications, and participation in one accessible portfolio.”

---

## 12. Dependencies & Risks

### Dependencies

| Dependency | Owner | Status | Impact if Delayed | Mitigation Plan |
| :--- | :--- | :--- | :--- | :--- |
| Project content inventory | Angelo Andres | Pending | Project pages cannot launch | Launch with a minimum of 3 complete P0 projects |
| Certification metadata and verification URLs | Angelo Andres | Pending | Certification page has reduced value | Publish only verified entries |
| SGDS-inspired design tokens | Design Owner | Pending | UI implementation blocked | Finalize `design.md` before UI build |
| Vercel project configuration | Angelo Andres | Pending | Deployment blocked | Configure Vercel project before release candidate |

### Risks & Mitigation

#### High Risk: Content Schema Drift
- **Probability:** Medium.
- **Impact:** High.
- **Mitigation:** Enforce the content schemas and validation rules in `AGENTS.md`; fail builds on invalid content.
- **Owner:** Specification Architect.

#### Medium Risk: Accessibility Regressions
- **Probability:** Medium.
- **Impact:** High.
- **Mitigation:** Apply SGDS-inspired accessible patterns, semantic HTML, keyboard testing, and automated accessibility checks.
- **Owner:** Lead UI/UX Designer.

#### Medium Risk: Vercel Hobby Plan Limits
- **Probability:** Low.
- **Impact:** Medium.
- **Mitigation:** Optimize images, limit bundled assets, avoid server functions, and monitor deployment size and usage.
- **Owner:** Technical Lead.

### Open Questions
- [ ] Which 3–5 projects are designated as P0 launch projects?
- [ ] Which certifications have publicly verifiable credential URLs?
- [ ] Which external contact channels should be displayed at launch?
- [ ] Should the MVP use light mode only, or include a dark mode toggle?

---

## 13. Timeline & Milestones

### Development Phases

| Phase | Timeline | Key Deliverables | Owner |
| :--- | :--- | :--- | :--- |
| Specification Lock | Week 1 | Approved 6 master files | Product/Architecture Owner |
| Foundation | Week 1–2 | Next.js, TypeScript, Tailwind, content pipeline, layout shell | Engineering |
| Core Content | Week 2–3 | Projects, certifications, blog content and rendering | Engineering / Content Owner |
| Design Implementation | Week 3–4 | SGDS-inspired components and responsive pages | UI/UX / Engineering |
| QA & Accessibility | Week 4 | Build, type, lint, accessibility, performance, and content validation | QA / Engineering |
| Launch | Week 5 | Vercel production deployment | Engineering / Owner |

### Key Milestones
- **Specification Approval:** End of Week 1.
- **Content Pipeline Complete:** End of Week 2.
- **Feature Complete:** End of Week 4.
- **Public MVP Launch:** End of Week 5.

---

## 14. Resources & Team

### Core Team
- **Product Manager / Specification Architect:** Angelo Andres
- **Systems Architect:** Angelo Andres
- **Lead UI/UX Designer:** Angelo Andres
- **Engineering Lead:** Angelo Andres
- **QA Lead:** Angelo Andres

---

## 15. Post-Launch Plan

### Success Criteria Check-in Schedule
- **Week 1:** Verify deployment health, route availability, and content rendering.
- **Week 4:** Review contact-channel effectiveness and content gaps.
- **Week 12:** Decide whether to add search, resume download, or an AI assistant.

### Iteration Plan
- **Feedback Channels:** Direct recruiter feedback, peer review, and personal usability testing.
- **Shipping Cadence:** Content updates can ship independently; UI changes follow a reviewed release cycle.

### Learning Goals
- Validate whether structured project documentation improves technical evaluation outcomes.
- Determine whether certifications and participation logs increase perceived credibility.
- Identify which project categories attract the most recruiter attention.

---

## 16. Appendix & Changelog

### References
- Singapore Government Design System: https://www.designsystem.tech.gov.sg/
- Next.js App Router documentation: https://nextjs.org/docs/app
- Vercel Hobby Plan documentation: https://vercel.com/docs/plans/hobby

### Changelog

| Date | Version | Description of Changes | Author |
| :--- | :--- | :--- | :--- |
| 2026-10-20 | v1.0 | Initial approved MVP PRD | Angelo Andres |

### Stakeholder Approvals
- [ ] **Product Lead:** Angelo Andres
- [ ] **Engineering Lead:** Angelo Andres
- [ ] **Design Lead:** Angelo Andres