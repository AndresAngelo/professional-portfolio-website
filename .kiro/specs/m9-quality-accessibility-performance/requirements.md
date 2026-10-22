# Requirements Document

> **Spec:** M9 Quality, Accessibility & Performance  
> **Document Status:** Draft  
> **Feature Name:** m9-quality-accessibility-performance  
> **Milestone:** M9  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 5, 6.1, 6.2, 7.3), `PRD.md` (success metrics), `TRD.md` (Sections 6.1, 6.4, 6.5, 8, 9), `design.md` (Sections 5.2, 6), `implementation_plan.md` (Phase 5, Tasks 5.1 and 5.2), `APP_FLOW.md` (route inventory)  
> **Master Files Location:** `Artifacts/master-files/`  
> **Last Updated:** 2026-10-20

---

## Introduction

Milestone 9 (M9) is the cross-cutting verification layer for `personal-website-portfolio-v2`. M1 to M8 delivered the toolchain, content architecture, design system, shell, homepage, projects, certifications, and blog. M9 verifies the finished, statically built site as a whole. It audits the build output (`out/` or the `.next` static export directory fixed in design) rather than re-testing individual modules, because M3 to M8 already own their unit, axe, property, and hygiene tests.

M9 delivers: a route inventory test, a built-HTML structural audit with an internal link crawler, an axe-core accessibility audit with a manual checklist, an SEO and metadata audit, schema.org JSON-LD structured data (deferred from M4, M6, M7, and M8), performance budgets with a committed baseline, a Lighthouse audit, content-quality regression gates, `audit:*` npm scripts with JSON reports, verification pipeline documentation, and a traceability matrix from PRD success metrics to audits.

Two changes needed explicit human approval because `AGENTS.md` 6.2 restricts them: (1) new devDependencies and npm scripts in `package.json` and the lockfile for axe-core, an HTML parser, and the Lighthouse toolchain; (2) a minimal, scoped edit to the M5, M6, and M8 page modules to emit JSON-LD. Both were Approved 2026-10-22 (approvals A1-A6, see design.md). Exact dependency versions are pinned at implementation time after documenting purpose and maintenance status. Fallbacks in Requirements 10, 12, and 15 remain only as historical notes.

M9 does NOT implement Vercel project setup, deployment, security headers or `vercel.json`, production monitoring, or release tagging (M10); P1 features (search, resume download, AI assistant) or their scaffolding; dark mode; Vercel Analytics or any visitor analytics; API routes; runtime dependencies; or any change to M1 to M8 product behavior other than the approved JSON-LD additions.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Build_Output** | The static HTML, CSS, JS, image, and font files produced by `npm run build`, at the directory fixed in the design. |
| **P0_Route** | A route in the Route_Inventory: `/`, `/projects`, `/projects/{slug}`, `/certifications`, `/blog`, `/blog/{slug}`, and the not-found page. |
| **Route_Inventory** | The expected P0_Route set derived from validated content at test time: one `/projects/{slug}` per project, one `/blog/{slug}` per Published_Post. |
| **Published_Post** | A `BlogPost` whose `draft` field is `false`. |
| **Audit** | A script or test under `scripts/audit/` or `tests/audit/` that reads Build_Output and reports findings. |
| **Audit_Report** | A machine-readable JSON file written by an Audit to the git-ignored `reports/` directory. |
| **Baseline** | A committed JSON file under `baselines/` recording accepted metric values. |
| **Structural_Audit** | The Audit of heading, landmark, link, image, script, and tracking-marker rules over every P0_Route HTML file. |
| **Link_Crawler** | The offline Audit component that resolves every internal `href` and `#fragment` against Build_Output. |
| **A11y_Audit** | The axe-core Audit run with WCAG 2.1 A and AA tags over every P0_Route HTML file. |
| **Manual_Checklist** | The committed document listing criteria that need human assistive-technology verification. |
| **SEO_Audit** | The Audit of title, description, canonical, Open Graph, article, and robots metadata. |
| **JSON_LD_Builder** | A pure function in `src/lib/structured-data/` that returns a schema.org object from content. |
| **JSON_LD_Block** | A server-rendered `<script type="application/ld+json">` element. |
| **Perf_Audit** | The Audit of per-route JS and CSS size, total deploy size, images, and fonts against budgets. |
| **Lighthouse_Audit** | The Lighthouse run against a locally served Build_Output for each P0_Route. |
| **Content_Gate** | A test asserting that invalid content fixtures fail validation and that P0 content is complete. |
| **External_Link_Inventory** | The Audit_Report listing every distinct external URL found in Build_Output with the routes that contain it. |
| **Quality_Gate** | A pass or fail threshold that makes an Audit exit non-zero. |
| **Traceability_Matrix** | The committed table mapping each PRD success metric to the Audit that verifies it. |
| **Approval_Item** | A change that requires explicit human approval under `AGENTS.md` 6.2. |

---

## Requirements

---

### Requirement 1: Audit Scope and Non-Duplication

**User Story:** As a QA engineer, I want M9 to verify only cross-cutting properties of the built site, so that M9 adds signal without repeating M3 to M8 tests.

#### Acceptance Criteria

1. THE M9 Audits SHALL read Build_Output and validated content only, and SHALL NOT import M3 to M8 component modules.
2. THE M9 test suite SHALL NOT assert component-level behavior already covered by M3 to M8 tests, including filter logic, card rendering, and helper properties.
3. WHERE Build_Output is absent, THE Audit SHALL fail with a message instructing the developer to run `npm run build`.
4. THE Audits SHALL execute offline and SHALL make no network request.
5. THE Audits SHALL be deterministic: two runs against identical Build_Output and content SHALL produce identical findings.
6. THE Audits SHALL be written in strict TypeScript with no `any`, no non-null assertions, and no unjustified type assertions.

#### Verification Steps

1. Grep `scripts/audit/` and `tests/audit/` for imports from `src/components/`; assert zero matches.
2. Run an Audit with Build_Output removed; assert the non-zero exit and the build instruction.
3. Run an Audit with networking disabled; assert success.
4. Run an Audit twice; assert identical Audit_Report content apart from timestamps.

---

### Requirement 2: Route Inventory Verification

**User Story:** As a site owner, I want proof that every P0 route exists in the build, so that P0 route availability is 100%.

#### Acceptance Criteria

1. THE Route_Inventory builder SHALL derive expected routes from the M2 loaders: `/`, `/projects`, `/certifications`, `/blog`, one `/projects/{slug}` per project, and one `/blog/{slug}` per Published_Post.
2. WHEN the Route_Inventory is derived, THE Audit SHALL assert that each expected route has an HTML file in Build_Output.
3. IF an expected route has no HTML file, THEN THE Audit SHALL fail and report the missing route path.
4. THE Audit SHALL assert that Build_Output contains no HTML file for a draft blog post slug.
5. THE Audit SHALL assert that Build_Output contains a not-found page (`404.html`).
6. THE Audit SHALL assert that Build_Output contains no HTML file for a route outside the Route_Inventory, excluding the not-found page and Next.js internal files.
7. THE Audit SHALL assert that Build_Output contains no API route or route handler output.

#### Verification Steps

1. Run the route test against the real build; assert every inventory route is present.
2. Delete one project HTML file in a temporary copy; assert failure naming that route.
3. Add a draft fixture slug; assert it is absent from Build_Output.

---

### Requirement 3: Built-HTML Document Structure Audit

**User Story:** As an accessibility reviewer, I want every built page to satisfy structural rules, so that semantic defects are caught before release.

#### Acceptance Criteria

1. THE Structural_Audit SHALL parse each P0_Route HTML file with an HTML parser and SHALL NOT use regular expressions for structural checks.
2. THE Structural_Audit SHALL assert that each page has a `lang` attribute on `html`, exactly one `h1`, and exactly one `main`.
3. THE Structural_Audit SHALL assert that each page contains `header`, `nav`, `main`, and `footer` landmarks.
4. THE Structural_Audit SHALL assert that heading levels do not skip downward (an `h(n)` is followed only by `h(n+1)` or any level at or above `n`).
5. THE Structural_Audit SHALL assert that the first focusable element in the document is the skip link and that its target `id` exists.
6. THE Structural_Audit SHALL assert that every `a` has a non-empty accessible name and every `button` has a non-empty accessible name.
7. THE Structural_Audit SHALL assert that every `img` has an `alt` attribute, and an empty `alt` only when the image has `role="presentation"` or `aria-hidden="true"`.
8. THE Structural_Audit SHALL assert that every `id` is unique within a page.
9. IF a check fails, THEN THE Structural_Audit SHALL report the route, the rule, and a selector for the offending element.

#### Verification Steps

1. Run the audit against the real build; assert zero findings.
2. Run the audit against fixture HTML with two `h1` elements, a skipped heading, an empty link, and a missing `alt`; assert one finding per defect with route and selector.

---

### Requirement 4: Internal Link Crawler

**User Story:** As a visitor, I want every internal link to work, so that I never reach a dead end.

#### Acceptance Criteria

1. THE Link_Crawler SHALL collect every internal `href` (root-relative or same-origin) from every P0_Route HTML file.
2. WHEN an internal `href` is collected, THE Link_Crawler SHALL assert that it resolves to an HTML file or asset in Build_Output.
3. WHEN an internal `href` contains a `#fragment`, THE Link_Crawler SHALL assert that an element with the matching `id` exists in the target page.
4. IF an `href` equals `#` or is empty, THEN THE Link_Crawler SHALL report a placeholder-link finding.
5. THE Link_Crawler SHALL ignore query strings when resolving files and SHALL assert that a `?tag=` link on `/blog` resolves to `/blog`.
6. THE Link_Crawler SHALL report each broken link with the source route, the `href`, and the reason.
7. THE Link_Crawler SHALL make no network request for external URLs.

#### Verification Steps

1. Run the crawler on the real build; assert zero broken links.
2. Run it on a fixture with a missing page, a missing fragment target, and `href="#"`; assert three findings.

---

### Requirement 5: External Link, Script, and Privacy Hygiene

**User Story:** As the site owner, I want the built output free of tracking and unsafe links, so that the site honors the no-visitor-data rule.

#### Acceptance Criteria

1. THE Structural_Audit SHALL assert that every external `a` with `target="_blank"` has `rel` containing `noopener` and `noreferrer`.
2. THE Structural_Audit SHALL assert that every external URL uses `https://`.
3. THE Structural_Audit SHALL assert that every `script` element in a P0_Route HTML file is served from `/_next/` or is a JSON_LD_Block.
4. THE Structural_Audit SHALL assert that no P0_Route HTML file contains a `form`, `input`, `textarea`, `iframe`, or third-party `script` or `link` origin.
5. THE Structural_Audit SHALL assert that Build_Output contains no known analytics or tracking marker, including `gtag`, `googletagmanager`, `google-analytics`, `fbq`, `_vercel/insights`, `_vercel/speed-insights`, `hotjar`, `segment.com`, `plausible.io`, and `gtag(` (host and call forms rather than bare words, per design).
6. THE Structural_Audit SHALL assert that no P0_Route HTML sets a cookie through `document.cookie` or `Set-Cookie` meta markers, and that no JS chunk references `document.cookie`.
7. THE Structural_Audit SHALL assert that Build_Output contains no `.env` file, private key marker, or token pattern.
8. IF a hygiene check fails, THEN THE Structural_Audit SHALL report the file path and the matched marker.

#### Verification Steps

1. Run against the real build; assert zero findings.
2. Inject a `gtag` string, a third-party script, and a `_blank` link without `rel` into fixtures; assert one finding each.

---

### Requirement 6: Automated Accessibility Audit (axe-core)

**User Story:** As an accessibility reviewer, I want axe-core run on every built page, so that WCAG 2.1 AA automated violations are zero.

#### Acceptance Criteria

1. THE A11y_Audit SHALL run axe-core with the tags `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa` over every P0_Route HTML file from the Route_Inventory.
2. THE A11y_Audit SHALL write an Audit_Report in JSON containing, per route, the violations with rule id, impact, selector, and help URL.
3. IF any route has one or more violations, THEN THE A11y_Audit SHALL exit non-zero.
4. THE A11y_Audit SHALL list `incomplete` results in the Audit_Report and SHALL NOT treat them as passes.
5. THE A11y_Audit SHALL run the checks in a DOM environment that supports the rules enabled, and SHALL record the rules disabled for lack of layout support (including `color-contrast`) in the Audit_Report.
6. THE A11y_Audit SHALL cover the not-found page.
7. THE A11y_Audit SHALL NOT disable any rule to make a route pass.

#### Verification Steps

1. Run `npm run audit:a11y`; assert exit 0 and a report with zero violations for every route.
2. Run against a fixture with an unlabeled button; assert a non-zero exit and the rule id in the report.
3. Assert the report lists the disabled rules.

---

### Requirement 7: Manual Accessibility Checklist

**User Story:** As an accessibility reviewer, I want a documented list of criteria that automation cannot verify, so that manual checks are complete and repeatable.

#### Acceptance Criteria

1. THE M9 deliverables SHALL include a Manual_Checklist at `docs/quality/manual-accessibility-checklist.md`.
2. THE Manual_Checklist SHALL include keyboard-only traversal, visible focus, screen reader (NVDA with Firefox or Chrome, VoiceOver with Safari), 200% zoom and 320 CSS px reflow, `prefers-reduced-motion`, and color contrast measurement at 4.5:1 for normal text and 3:1 for large text and essential UI boundaries.
3. THE Manual_Checklist SHALL list each P0_Route with a pass, fail, and notes column and the tester, date, and tool versions.
4. THE Manual_Checklist SHALL state the breakpoints 375px, 768px, 1024px, and 1440px from TRD Section 6.6.
5. THE Manual_Checklist SHALL state that automated checks do not by themselves establish WCAG conformance.
6. THE M9 documentation SHALL reference the Manual_Checklist from the release verification procedure.

#### Verification Steps

1. Assert the file exists and contains each listed criterion heading.
2. Assert it lists every P0_Route pattern.

---

### Requirement 8: SEO and Metadata Audit

**User Story:** As the site owner, I want complete, unique metadata on every page, so that search and social previews are correct.

#### Acceptance Criteria

1. THE SEO_Audit SHALL assert that each P0_Route has a non-empty `title` that is unique across routes and 10 to 70 characters long.
2. THE SEO_Audit SHALL assert that each P0_Route has a `meta name="description"` that is unique across routes and 50 to 160 characters long.
3. THE SEO_Audit SHALL assert that each indexable P0_Route (every P0_Route except the not-found page) has `link rel="canonical"` whose value is an absolute URL equal to `siteUrl` plus the route path.
4. THE SEO_Audit SHALL assert that each indexable P0_Route has `og:title`, `og:description`, `og:url`, `og:type`, and `og:site_name`, and that `og:url` equals the canonical URL.
5. THE SEO_Audit SHALL assert that each `/blog/{slug}` page has `og:type` equal to `article`, `article:published_time` equal to `publishedAt`, and `article:modified_time` only when `updatedAt` is non-null.
6. THE SEO_Audit SHALL assert that each page has a `meta name="viewport"` and that no indexable P0_Route has `noindex` in a robots meta. For the not-found page, THE SEO_Audit SHALL require only a title, a viewport meta, and a `noindex` robots meta (criteria 3 to 6 otherwise apply to indexable routes only).
7. THE SEO_Audit SHALL report routes whose titles or descriptions fall outside the ranges, with the measured length.
8. IF `siteUrl` in `content/site.json` is a placeholder host (`example.com` or `example.vercel.app`), THEN THE SEO_Audit SHALL report a warning and SHALL record it as a release blocker for M10.

#### Verification Steps

1. Run `npm run audit:seo`; assert zero failures on the real build.
2. Run on fixtures with a duplicate title, a relative canonical, and a missing `og:type`; assert one finding each.
3. Run with a placeholder `siteUrl`; assert the warning.

---

### Requirement 9: JSON-LD Structured Data Builders

**User Story:** As the site owner, I want accurate schema.org data generated from content, so that search engines can interpret the pages without fabricated facts.

#### Acceptance Criteria

1. THE JSON_LD_Builder SHALL provide `buildPersonJsonLd(site)`, `buildArticleJsonLd(post, site)`, and `buildBreadcrumbJsonLd(items, site)` as pure functions in `src/lib/structured-data/`.
2. THE `buildPersonJsonLd` function SHALL return a schema.org `Person` with `name`, `jobTitle`, `url`, and `sameAs` derived only from `SiteConfig` profile and social link fields.
3. THE `buildArticleJsonLd` function SHALL return a schema.org `Article` with `headline`, `description`, `datePublished`, `author`, `url`, and `keywords` derived only from the `BlogPost` and `SiteConfig`, and SHALL include `dateModified` only when `updatedAt` is non-null.
4. THE `buildBreadcrumbJsonLd` function SHALL return a schema.org `BreadcrumbList` with absolute `item` URLs and 1-based `position` values.
5. THE JSON_LD_Builder SHALL omit any property whose source value is `null` or empty, and SHALL NOT insert a placeholder value.
6. THE `serializeJsonLd` function SHALL return JSON in which each `<` is replaced by `\u003c`, so that serialized content cannot close the script element.
7. FOR ALL generated objects, `JSON.parse(serializeJsonLd(x))` SHALL equal `x` (round-trip property).
8. THE JSON_LD_Builder functions SHALL NOT mutate their inputs.
9. THE JSON_LD_Builder SHALL NOT import `react`, `next`, or `document`.

#### Verification Steps

1. Write Property_Tests for round-trip, `<` escape (no `</script` substring in output), input immutability, and omission of null fields over generated strings including `</script><script>`.
2. Write unit tests asserting required fields for each type with fixtures.

---

### Requirement 10: JSON-LD Page Integration (Approval Item)

**User Story:** As the site owner, I want JSON-LD present in the built pages, so that the deferred structured data from M4 to M8 is delivered with minimal change.

#### Acceptance Criteria

1. Approved 2026-10-22 (approval A5): THE M5 homepage module SHALL render one JSON_LD_Block of type `Person` on `/`.
2. Approved 2026-10-22 (approval A5): THE M8 blog detail module SHALL render one JSON_LD_Block of type `Article` on each `/blog/{slug}` page.
3. Approved 2026-10-22 (approval A5): THE project detail and blog detail pages SHALL render one JSON_LD_Block of type `BreadcrumbList`.
4. THE JSON_LD_Block SHALL be rendered by a server component and SHALL add no client JavaScript.
5. THE approved edit SHALL be limited to the import and render lines in the M5, M6, and M8 page modules, namely importing the JSON_LD_Block component and rendering it, and SHALL NOT change existing markup, props, or metadata.
6. THE Structural_Audit SHALL assert that each JSON_LD_Block in Build_Output parses as JSON, has `@context` equal to `https://schema.org`, and has the type specified for its route.
7. Historical note: before approval, the fallback was to deliver Requirement 9 with JSON-LD assertions reported as `skipped: not approved`. The approval switch now defaults to approved.

#### Verification Steps

1. Build and parse the `/` HTML; assert one `Person` block with fields equal to `content/site.json`.
2. Parse each blog detail HTML; assert one `Article` block whose `headline` equals the post title.
3. Run `git diff --stat` against the M8 baseline; assert the M5 and M8 changes are limited to the approved import and render lines.

---

### Requirement 11: Performance Budget Audit

**User Story:** As a performance owner, I want asset budgets enforced with a committed baseline, so that regressions are caught before release.

#### Acceptance Criteria

1. THE Perf_Audit SHALL compute, per P0_Route, the gzip size of the JavaScript and CSS files referenced by its HTML.
2. THE Perf_Audit SHALL compare each route's size with a Baseline at `baselines/performance.json`.
3. IF a route's JavaScript or CSS size exceeds its Baseline value by more than 5%, THEN THE Perf_Audit SHALL fail and report the route, the size, and the percentage.
4. WHEN run with the `--update-baseline` flag, THE Perf_Audit SHALL rewrite the Baseline and SHALL print the diff.
5. WHERE no Baseline exists, THE Perf_Audit SHALL write one and SHALL report that a new Baseline was created.
6. THE Perf_Audit SHALL report the total Build_Output size and SHALL fail when it exceeds the budget stated in the design, which SHALL be below the Vercel Hobby Plan static deployment limit documented at design time.
7. THE Perf_Audit SHALL fail if any image file in Build_Output exceeds the per-image budget stated in the design.
8. THE Perf_Audit SHALL assert that every `img` in P0_Route HTML declares `width` and `height` (or an equivalent explicit sizing mechanism).
9. WHERE Build_Output contains font files, THE Perf_Audit SHALL assert that each is WOFF2 and that the font-face rules use `font-display` of `swap` or `optional`.
10. THE Perf_Audit SHALL assert that no route references a JavaScript file larger than the per-chunk budget stated in the design.
11. THE Perf_Audit SHALL record the `npm run build` wall-clock duration when supplied and SHALL flag durations above 3 minutes.

#### Verification Steps

1. Run `npm run audit:perf` against the real build twice; assert the first creates the Baseline and the second passes.
2. Inflate a fixture JS file by 10%; assert failure with the percentage.
3. Add an oversized image fixture; assert failure.

---

### Requirement 12: Lighthouse Audit (Approval Item)

**User Story:** As a performance owner, I want Lighthouse run against every P0 route, so that Core Web Vitals targets in TRD Section 6.1 are measured.

#### Acceptance Criteria

1. Approved 2026-10-22 (approval A3): THE Lighthouse_Audit SHALL serve Build_Output on a local port and SHALL run Lighthouse in mobile emulation against every P0_Route in the Route_Inventory.
2. THE Lighthouse_Audit SHALL fail when any route has an Accessibility score below 95.
3. THE Lighthouse_Audit SHALL fail when any route has LCP of 2.5 s or more, CLS of 0.1 or more, FCP of 1.8 s or more, or TBT of 200 ms or more.
4. THE Lighthouse_Audit SHALL report Performance, Best Practices, and SEO scores per route, with thresholds set in the design.
5. THE Lighthouse_Audit SHALL report TBT as the lab proxy for INP and SHALL state that INP below 200 ms is verified from field data when available.
6. THE Lighthouse_Audit SHALL write one Audit_Report per run containing scores, metrics, the Lighthouse version, and the Chrome version.
7. THE Lighthouse_Audit SHALL run each route a number of times fixed in the design and SHALL use the median to reduce variance.
8. Approved 2026-10-22 (approval A3): devDependencies are approved; exact versions are pinned at implementation time after documenting each devDependency's purpose and maintenance status, per `AGENTS.md` 6.2.
9. THE M9 documentation SHALL still provide a manual Lighthouse procedure (Chrome DevTools or PageSpeed Insights) and a results template at `docs/quality/manual-lighthouse-procedure.md` (historical fallback retained as a supplementary document).
10. THE Lighthouse_Audit SHALL NOT run in the default `npm test` command.

#### Verification Steps

1. Run `npm run audit:lighthouse` after approval; assert one report per route with all thresholds evaluated.
2. Review the manual procedure document; assert it covers each P0_Route and each TRD Section 6.1 metric.
3. Run `npm test`; assert Lighthouse is not invoked.

---

### Requirement 13: Content Validation Regression Gates

**User Story:** As a content owner, I want proof that invalid content fails the build with useful errors, so that no unvalidated content ships.

#### Acceptance Criteria

1. THE Content_Gate SHALL include one invalid fixture for each rule in `AGENTS.md` 5.1 (rules 1 to 7 and 10), 5.2, 5.3, and 5.4.
2. WHEN an invalid fixture is validated, THE M2 validator SHALL produce an error that contains the file path, the field name, the expected type or format, and the received value category.
3. THE Content_Gate SHALL assert that the `mailto:` scheme is rejected for non-email contact channels.
4. THE Content_Gate SHALL assert that a draft blog fixture is excluded from `getBlogPosts()` and returns `null` from `getBlogPostBySlug()`.
5. THE Content_Gate SHALL assert that a fixture with more than 3 featured projects fails validation.
6. THE Content_Gate SHALL use temporary fixture directories and SHALL NOT modify files under `content/`.
7. IF a validator accepts an invalid fixture, THEN THE Content_Gate SHALL fail and name the rule.

#### Verification Steps

1. Run the Content_Gate; assert one failing validation and one matching error per rule fixture.
2. Assert each error text contains the four required components.
3. Run `git status`; assert no `content/` modification.

---

### Requirement 14: P0 Content Completeness and Credential Integrity

**User Story:** As a recruiter, I want the shipped content to be complete and truthful, so that every project has a repository link and no credential is invented.

#### Acceptance Criteria

1. THE Content_Gate SHALL assert that real content contains at least the minimum project, certification, and blog counts set in the design from `PRD.md`.
2. THE Content_Gate SHALL assert that every project with a P0 designation has a non-empty `repositoryUrl`, giving 100% repository-link coverage.
3. THE Content_Gate SHALL assert that at most 3 projects have `featured` equal to `true` and that each has `displayOrder`.
4. THE Content_Gate SHALL assert that no certification has `credentialId` or `verificationUrl` containing a placeholder marker (`EXAMPLE`, `example.com`, `TODO`, `TBD`, `lorem`, `XXXX`).
5. THE Content_Gate SHALL assert that no content file contains a placeholder host (`example.com`, `example.vercel.app`) outside fenced code blocks, and SHALL report each occurrence.
6. THE Content_Gate SHALL assert that every `badgeImageUrl` and local image path resolves to a file under `public/`.
7. IF any assertion fails, THEN THE Content_Gate SHALL report the content file path and the field.

#### Verification Steps

1. Run the Content_Gate against real content; assert zero failures.
2. Run it against fixtures with a missing `repositoryUrl`, an `EXAMPLE-123` credential, and a missing image file; assert one finding each.

---

### Requirement 15: External Link Inventory

**User Story:** As a content owner, I want a list of every external URL on the site, so that I can check them manually without network calls in CI.

#### Acceptance Criteria

1. THE External_Link_Inventory SHALL list each distinct external URL found in P0_Route HTML, with the routes that contain it and its occurrence count.
2. THE External_Link_Inventory SHALL sort URLs lexicographically and SHALL be deterministic.
3. THE External_Link_Inventory SHALL write an Audit_Report in JSON and a Markdown table.
4. WHERE the developer runs `npm run audit:links:online`, THE script SHALL send a `HEAD` request to each URL with a timeout fixed in the design and SHALL report status codes.
5. THE `audit:links:online` script SHALL NOT be part of `npm test`, CI, or `npm run audit`.
6. IF an external URL is not `https://`, THEN THE External_Link_Inventory SHALL report a finding.
7. THE `audit:links:online` script SHALL send no request body, cookie, or custom identifying header.
8. THE External_Link_Inventory SHALL be created without adding a runtime dependency; any devDependency is an Approval_Item.

#### Verification Steps

1. Run `npm run audit:links`; assert the report lists a known fixture URL with its routes.
2. Run the audit twice; assert identical output.
3. Assert `npm test` makes no network request by running it with networking disabled.

---

### Requirement 16: Audit Scripts and Reporting

**User Story:** As a developer, I want one command per audit and one aggregate command, so that I can run the verification pipeline locally and in CI.

#### Acceptance Criteria

1. THE M9 implementation SHALL provide the scripts `audit:routes`, `audit:structure`, `audit:a11y`, `audit:seo`, `audit:perf`, `audit:links`, `audit:lighthouse`, and `audit`, with final names fixed in the design.
2. THE `audit` script SHALL run every Audit except `audit:lighthouse` and `audit:links:online`, and SHALL exit non-zero when any Audit fails.
3. THE `audit` script SHALL run all Audits to completion before exiting so that all findings appear in one run.
4. THE Audits SHALL write Audit_Reports to `reports/` and SHALL create the directory when absent.
5. THE repository `.gitignore` SHALL list `reports/`, and Baselines SHALL be committed under `baselines/`.
6. THE Audit_Report schema SHALL contain `audit`, `generatedAt`, `status`, `summary`, and `findings` fields, and each finding SHALL contain `route`, `rule`, and `message`.
7. THE `audit` script SHALL print a console summary with one line per Audit showing status and finding count.
8. THE `package.json` `audit:*` scripts (including the aggregate `audit`), lockfile, and `.gitignore` `reports/` edits were Approved 2026-10-22 (approvals A1, A4, A6). The version bump is not an M9 matter.
9. THE Audit scripts SHALL NOT modify `next.config.ts`, `tsconfig.json`, or CI configuration.

#### Verification Steps

1. Run `npm run audit`; assert reports for every included Audit and a non-zero exit on an injected failure.
2. Validate each report against the schema.
3. Run `git check-ignore reports/x.json`; assert it is ignored.

---

### Requirement 17: Verification Pipeline Documentation

**User Story:** As a maintainer, I want one document describing the verification pipeline, so that any contributor can reproduce the release checks.

#### Acceptance Criteria

1. THE M9 deliverables SHALL include `docs/quality/verification-pipeline.md`.
2. THE document SHALL describe the order `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run audit`, matching TRD Section 8.1 with the audit step added.
3. THE document SHALL describe each Audit, its Quality_Gate, its Audit_Report location, and its Baseline update procedure.
4. THE document SHALL describe the Manual_Checklist and the Lighthouse procedure (automated or manual).
5. THE document SHALL list the TRD Section 9 Definition of Done items and the Audit that verifies each.
6. THE document SHALL state that deployment verification is owned by M10.
7. THE document SHALL list every Approval_Item and its approval status.

#### Verification Steps

1. Assert the document exists and contains the six pipeline commands in order.
2. Assert each script name from Requirement 16 appears in the document.

---

### Requirement 18: Quality Gates, Traceability, and Guardrails

**User Story:** As a project lead, I want PRD success metrics mapped to audits and M9 scope bounded, so that release readiness is evidenced and no unapproved change is made.

#### Acceptance Criteria

1. THE M9 deliverables SHALL include a Traceability_Matrix at `docs/quality/traceability-matrix.md` mapping each PRD success metric to an Audit, a Quality_Gate, and a manual step where applicable.
2. THE Traceability_Matrix SHALL include Lighthouse accessibility of 95 or more, automated WCAG 2.1 AA checks on all P0 pages, Core Web Vitals per TRD Section 6.1, P0 route availability of 100%, content-only publishing, P0 project repository links of 100%, and no analytics or personal data.
3. THE Traceability_Matrix SHALL mark each metric as `automated`, `manual`, or `automated + manual`.
4. THE M9 implementation SHALL NOT add a runtime dependency, an API route, a route handler, a server action, analytics, a cookie, or a form.
5. THE M9 implementation SHALL NOT change M1 to M8 product behavior, with the sole exception of the JSON-LD additions in Requirement 10.
6. THE M9 implementation SHALL add each devDependency only after human approval, with an exact pinned version and a documented purpose.
7. THE M9 implementation SHALL NOT scaffold P1 features, dark mode, Vercel configuration, or security headers.
8. WHEN `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit` all complete, THE M9 implementation SHALL report zero errors from each.

#### Verification Steps

1. Assert every PRD success metric string appears in the Traceability_Matrix.
2. Run `git diff --stat` against the M8 baseline; assert changes only in `scripts/audit/`, `tests/audit/`, `src/lib/structured-data/`, `src/components/structured-data/`, `docs/quality/`, `baselines/`, the approved JSON-LD lines, and approved `package.json`, lockfile, and `.gitignore` edits.
3. Grep the diff for `app/api`, `route.ts`, `"use server"`, and analytics markers; assert zero matches.
4. Run the five verification commands and confirm zero errors.
