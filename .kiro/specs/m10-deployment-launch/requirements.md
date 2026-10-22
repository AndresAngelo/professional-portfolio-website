# Requirements Document

> **Spec:** M10 Deployment & Launch  
> **Document Status:** Draft  
> **Feature Name:** m10-deployment-launch  
> **Milestone:** M10 (final milestone)  
> **Workflow:** Requirements-First  
> **SSOT References:** `AGENTS.md` (Sections 5, 6.1, 6.2, 7.3), `PRD.md` (Sections 10, 11, 12, 13, 15, success metrics, stakeholder approvals), `TRD.md` (Sections 6.1, 6.3, 6.4, 7, 8), `implementation_plan.md` (Phase 6, Tasks 6.1 and 6.2), `APP_FLOW.md` (route inventory), M9 spec `m9-quality-accessibility-performance`  
> **Master Files Location:** `Artifacts/master-files/`  
> **Last Updated:** 2026-10-22

---

## Introduction

Milestone 10 (M10) takes the verified `personal-website-portfolio-v2` build from a local release candidate to a live, documented, recoverable production site. M1 to M8 delivered the product. M9 delivered offline audits, baselines, JSON-LD, manual checklists in `docs/quality/`, and release blockers such as the placeholder `siteUrl`. M10 consumes those results and adds the launch layer: a launch checklist, a documented Vercel configuration, security headers, a deployed-URL smoke script, release management, rollback and incident procedures, content publishing documentation, a post-launch schedule, and final sign-off.

Most M10 work is human-performed (Vercel dashboard, DNS, tagging, sign-off). Those requirements are written as documented procedures with evidence to record. The code M10 adds is limited to `vercel.json`, `scripts/launch/**` (including `verify-deployment.ts` and `csp-hashes.ts`), `tests/launch/**`, the CI configuration `.github/workflows/verify.yml`, and documentation. The only content change is the `content/site.json` values.

Human decisions were recorded on 2026-10-22 for the changes that need explicit approval under `AGENTS.md` 6.2:

1. New root file `vercel.json` (Requirements 5 and 6): Approved 2026-10-22 (approval A1), with the CSP script policy `script-src 'self' 'unsafe-inline'` and all other directives strict.
2. `package.json` script entries `verify:deployment` and `launch:csp` (Requirement 7.14): Approved 2026-10-22 (approvals A2 and A4). `.gitignore` entry `reports/`: Approved 2026-10-22 (approval A8).
3. `package.json` `version` `1.0.0` (Requirement 11.1): Declined (approval A3). The version lives in `CHANGELOG.md` and the `v1.0.0` tag only. This is a separate Approval_Item from the script entries.
4. `next.config.ts`: the M1 configuration is a static export (`output: 'export'`, output directory `out`). An edit is pre-approved 2026-10-22 (approval A5) only if the verification in Requirement 4.4 fails.
5. New CI configuration `.github/workflows/verify.yml` (Requirement 15): Approved 2026-10-22 (approval A6), offline checks only.
6. devDependencies: all approved 2026-10-22 (approval 1a), pinned to exact versions at implementation.

Creating and pushing the `v1.0.0` git tag stays manual (approval A7, Requirement 11.2): explicit approval is requested at launch time, not before.

M10 does NOT implement P1 features or P1/AI scaffolding (search, resume download, AI assistant), analytics or visitor tracking of any kind, dark mode, API routes, databases, authentication, comments, i18n, a CMS, new runtime dependencies, or any product code change other than the `content/site.json` values.

---

## Glossary

| Term | Definition |
| :--- | :--- |
| **Build_Output** | The static files produced by `npm run build`, at the directory fixed in M9 and Requirement 4. |
| **Route_Inventory** | The expected route set defined in M9: `/`, `/projects`, `/projects/{slug}`, `/certifications`, `/blog`, `/blog/{slug}` for each Published_Post. |
| **Published_Post** | A `BlogPost` whose `draft` field is `false`. |
| **Launch_Checklist** | The committed document `docs/operations/launch-checklist.md`. |
| **Release_Blocker** | A condition that prevents production deployment, including a placeholder `siteUrl`, a placeholder contact email, fewer than 3 complete P0 projects, an unverified certification, or any failing verification command. |
| **Verification_Pipeline** | The command set `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit`. |
| **Evidence_Record** | A dated entry in a committed document stating who performed a step, the outcome, and a reference (command output summary, deployment URL, or screenshot path). |
| **Deployment_Guide** | The committed document `docs/operations/deployment.md`. |
| **Operations_Guide** | The committed document `docs/operations/monitoring.md`. |
| **Runbook** | The committed document `docs/operations/rollback-and-incidents.md`. |
| **Preview_Deployment** | A Vercel deployment created from a non-production branch. |
| **Production_Deployment** | A Vercel deployment created from the production branch and served at the production URL. |
| **Production_URL** | The public HTTPS origin of the live site, equal to `siteUrl` in `content/site.json`. |
| **Deployment_Verifier** | The script `scripts/launch/verify-deployment.ts` that checks a deployed URL over the network. |
| **Security_Headers** | The HTTP response headers declared in `vercel.json`. |
| **CSP** | The `Content-Security-Policy` response header. |
| **Inline_Script_Hash** | A `sha256-` digest of the content of an inline executable `script` element in Build_Output. |
| **Data_Block** | A `script` element of type `application/ld+json`, which the browser does not execute. |
| **Passive_Monitoring** | Observation of the site that adds no script, cookie, or tracking code to Build_Output. |
| **Severity_Level** | An incident classification: SEV1 (site unreachable or wrong content on a P0 route), SEV2 (degraded route or broken link), SEV3 (cosmetic or content defect). |
| **Rollback** | Restoring the last known-good Production_Deployment through Vercel, or reverting a content commit in git. |
| **Release_Tag** | The annotated git tag `v1.0.0`. |
| **Known_Issues_Document** | The committed document `docs/operations/known-issues.md`. |
| **Publishing_Guide** | The committed document `docs/operations/content-publishing.md`. |
| **Post_Launch_Schedule** | The Week 1, Week 4, and Week 12 check-in plan from `PRD.md` Section 15. |
| **Traceability_Matrix** | The committed table mapping each PRD success metric to launch evidence. |
| **Approval_Item** | A change that requires explicit human approval under `AGENTS.md` 6.2. |
| **Human_Procedure** | A step performed by the owner outside the repository, documented with the evidence to record. |

---

## Requirements

---

### Requirement 1: Launch Scope and Change Boundaries

**User Story:** As the site owner, I want M10 limited to deployment, documentation, and verification, so that launch does not alter verified product behavior.

#### Acceptance Criteria

1. THE M10 deliverables SHALL consist of documentation under `docs/operations/`, `vercel.json`, `scripts/launch/**` (including `scripts/launch/verify-deployment.ts` and `scripts/launch/csp-hashes.ts`), `tests/launch/**`, `.github/workflows/verify.yml`, `CHANGELOG.md`, README updates, the approved `package.json` script entries and `.gitignore` entry, and `content/site.json` value changes.
2. THE M10 deliverables SHALL NOT edit EXISTING files under `src/`, `tests/`, or `scripts/audit/`; new files under `scripts/launch/` and `tests/launch/` are permitted.
3. THE M10 deliverables SHALL NOT add a runtime dependency, and any devDependency SHALL be one approved on 2026-10-22 (approval 1a) and pinned to an exact version at implementation.
4. THE M10 deliverables SHALL NOT add analytics, tracking scripts, cookies, API routes, route handlers, middleware, or environment variables.
5. THE M10 deliverables SHALL NOT add P1 features or P1/AI scaffolding, including search, resume download, and an AI assistant.
6. WHEN a change to an Approval_Item is needed, THE M10 documentation SHALL list the item, the reason, and the fallback if approval is withheld.
7. THE M10 documents SHALL be written in Markdown, and THE Deployment_Verifier SHALL be written in strict TypeScript with no `any`, no non-null assertions, and no unjustified type assertions.

#### Verification Steps

1. Run `git diff --name-only` against the M9 completion commit; assert every changed path belongs to the deliverable list in criterion 1.
2. Assert `package.json` `dependencies` is unchanged, `devDependencies` differ only by approved, exactly pinned entries, `version` is unchanged, and the only other change is the approved script entries.
3. Grep the diff for `analytics`, `speed-insights`, `gtag`, and `process.env`; assert zero matches in added lines.

---

### Requirement 2: Pre-Launch Readiness Gate and Launch Checklist

**User Story:** As the site owner, I want one checklist that consolidates every launch blocker, so that I deploy to production only when all gates are green.

#### Acceptance Criteria

1. THE Launch_Checklist SHALL exist at `docs/operations/launch-checklist.md` and SHALL be organized into the sections: Content, Configuration, Verification Pipeline, Accessibility and Performance, Security, Deployment, and Sign-off.
2. THE Launch_Checklist SHALL list each Release_Blocker with the command or Human_Procedure that clears it and a field for an Evidence_Record.
3. THE Launch_Checklist SHALL require that `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit` each exit with code 0 on the release candidate commit.
4. THE Launch_Checklist SHALL require that no M9 Audit_Report lists a release-blocker finding.
5. THE Launch_Checklist SHALL require the signed M9 manual accessibility checklist in `docs/quality/` and SHALL require an Evidence_Record of the `audit:lighthouse` results for every route in the Route_Inventory.
6. THE Launch_Checklist SHALL record the release candidate commit SHA, so that the commit verified is the commit deployed.
7. WHILE any Launch_Checklist item is unchecked, THE Launch_Checklist SHALL state that Production_Deployment is not permitted.
8. THE Launch_Checklist SHALL incorporate the `implementation_plan.md` Task 6.2 steps: route checks, external-link checks, draft-post inaccessibility, mobile/tablet/desktop rendering, and console and network checks.

#### Verification Steps

1. Read the Launch_Checklist; assert all seven sections and every Release_Blocker are present.
2. Assert each item has an Evidence_Record field.
3. Run the Verification_Pipeline on the release candidate; assert exit code 0 for each command.

---

### Requirement 3: Content Completeness and Open-Question Resolution

**User Story:** As a recruiter, I want only real, verified content on the live site, so that every claim on the portfolio is credible.

#### Acceptance Criteria

1. THE Launch_Checklist SHALL require at least 3 complete P0 projects, each exposing a repository link, a technology list, and build documentation, per the `PRD.md` Section 12 dependency table.
2. THE Launch_Checklist SHALL require that every published certification has a verifiable `verificationUrl` or is removed, and that no credential ID, issuer, date, badge, or link is fabricated.
3. THE Launch_Checklist SHALL require that `content/site.json` `siteUrl` is not `example.vercel.app`, `example.com`, or any other placeholder host.
4. THE Launch_Checklist SHALL require that every contact channel URL and every social link URL in `content/site.json` is a real destination, and that no `example.com` email or username remains.
5. THE Launch_Checklist SHALL require that the owner opens each external link and records that it resolves to the intended destination, using `npm run audit:links:online` where the command exists in M9.
6. THE Launch_Checklist SHALL record the resolution of each `PRD.md` Section 12 open question: the P0 project list, the certifications with verifiable credential URLs, the contact channels shown at launch, and the theme decision.
7. THE Launch_Checklist SHALL record the theme decision as light mode only, and SHALL record that no dark mode toggle ships in P0.
8. THE Launch_Checklist SHALL require that no placeholder, lorem ipsum, or example-prefixed content file remains in `content/`.
9. THE Launch_Checklist SHALL require that no draft blog post is reachable in Build_Output or on the deployed site.

#### Verification Steps

1. Run the M9 SEO and release-blocker audits; assert no placeholder `siteUrl` or contact finding.
2. Count complete project entries under `content/projects/`; assert at least 3.
3. Grep `content/` for `example`; assert zero placeholder matches.
4. Read the Launch_Checklist; assert all four open questions carry an answer and an Evidence_Record.

---

### Requirement 4: Vercel Project Configuration Procedure

**User Story:** As the site owner, I want a documented Vercel setup, so that anyone can recreate the deployment configuration.

#### Acceptance Criteria

1. THE Deployment_Guide at `docs/operations/deployment.md` SHALL document, as a Human_Procedure, connecting the Git repository to a Vercel project on the Hobby Plan.
2. THE Deployment_Guide SHALL document the project settings: framework preset Next.js, install command `npm ci`, build command `npm run build`, and the output directory.
3. THE Deployment_Guide SHALL document the Node.js version, and the version SHALL match the version fixed by M1 in `package.json` `engines` or `.nvmrc`.
4. THE M1 `next.config.ts` is a static export (`output: 'export'`, output directory `out`), and THE Deployment_Guide SHALL state the output directory as `out` and SHALL record the result of a one-line verification of the M1 `next.config.ts`.
5. IF the verification in criterion 4 fails, THEN THE `next.config.ts` edit that restores `output: 'export'` is pre-approved (Approved 2026-10-22, approval A5), and THE Deployment_Guide SHALL record the reason and the edit.
6. THE Deployment_Guide SHALL document the production branch, and SHALL document that Preview_Deployments are enabled for every non-production branch.
7. THE Deployment_Guide SHALL state that no environment variable is required for P0, SHALL record the result of verifying that no `process.env` reference exists in `src/` and `next.config.ts`, and SHALL state that no `.env` file is committed.
8. THE Deployment_Guide SHALL document the Hobby Plan limits relevant to the site, including deployment size, and SHALL cite the M9 total deploy size result.
9. THE Deployment_Guide SHALL list the Evidence_Record fields: project name, production branch, Node.js version, and the date of each setting verification.

#### Verification Steps

1. Read `next.config.ts`; assert `output: 'export'` and record the output directory `out`.
2. Run `npm run build`; assert the documented output directory exists and contains `index.html`.
3. Grep `src/` and `next.config.ts` for `process.env`; assert zero matches.
4. Read the Deployment_Guide; assert every setting from criteria 2 to 7 is present.

---

### Requirement 5: Security Headers Configuration

**User Story:** As the site owner, I want standard security headers on every response, so that the deployed site resists clickjacking, MIME sniffing, and unnecessary browser capabilities.

#### Acceptance Criteria

1. THE `vercel.json` file (Approved 2026-10-22, approval A1) SHALL declare Security_Headers for the source pattern that matches every route.
2. THE Security_Headers SHALL include `X-Content-Type-Options: nosniff`.
3. THE Security_Headers SHALL include `Referrer-Policy: strict-origin-when-cross-origin`.
4. THE Security_Headers SHALL include a `Permissions-Policy` that disables camera, microphone, geolocation, payment, and USB access.
5. THE Security_Headers SHALL prevent framing through the CSP `frame-ancestors 'none'` directive and through `X-Frame-Options: DENY`.
6. THE `vercel.json` file SHALL declare `Cache-Control: public, max-age=31536000, immutable` for fingerprinted assets under `/_next/static/`.
7. THE `vercel.json` file SHALL NOT declare long-lived immutable caching for HTML routes.
8. THE Deployment_Guide SHALL state whether `Strict-Transport-Security` is provided by Vercel by default, SHALL record the result of checking the header on the deployed URL, and SHALL document a manual `Strict-Transport-Security` header only if Vercel does not provide it.
9. THE `vercel.json` file SHALL contain no redirect, rewrite, function, or cron configuration.
10. THE `vercel.json` file SHALL be valid JSON.
11. THE `vercel.json` approval is recorded as Approved 2026-10-22 (approval A1), so THE Security_Headers are version controlled; THE Deployment_Guide MAY document dashboard configuration only as a recovery fallback and SHALL state that such configuration is not version controlled.

#### Verification Steps

1. Parse `vercel.json` as JSON; assert it is valid and contains no redirect, rewrite, function, or cron keys.
2. Assert each header from criteria 2 to 6 is present with the stated value.
3. After deployment, run the Deployment_Verifier header checks (Requirement 7); assert every header is present on all Route_Inventory routes.

---

### Requirement 6: Content Security Policy That the Real Build Satisfies

**User Story:** As the site owner, I want a CSP that the actual build passes, so that security hardening does not break page hydration.

#### Acceptance Criteria

1. THE CSP SHALL be derived from an inspection of the real Build_Output, and SHALL NOT assume `script-src 'self'`, because Next.js static export emits inline scripts for hydration and flight data.
2. THE chosen script policy SHALL be `script-src 'self' 'unsafe-inline'` with all other directives strict (Approved 2026-10-22, approval A1), and THE Deployment_Guide SHALL document that policy and its tradeoff; a hash-based `script-src` using Inline_Script_Hashes remains an optional documented alternative only.
3. WHERE a hash-based `script-src` is chosen, THE launch tooling SHALL extract Inline_Script_Hashes from every Build_Output HTML file by parsing the HTML, and SHALL assert that every executable inline script has a matching hash in the CSP.
4. WHERE a hash-based `script-src` is chosen, THE launch tooling SHALL fail when Build_Output contains an executable inline script whose hash is absent from `vercel.json`.
5. THE CSP SHALL set `default-src 'self'`, `img-src 'self' data:`, `style-src` to the value the real build requires, `font-src 'self'`, `connect-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, and `frame-ancestors 'none'`.
6. THE CSP SHALL NOT permit any third-party origin.
7. THE CSP SHALL treat Data_Blocks as non-executable and SHALL NOT require a hash or `unsafe-inline` for them.
8. WHEN the CSP is finalized, THE owner SHALL load every Route_Inventory route and the not-found page in a browser with the console open, and SHALL record zero CSP violation reports as an Evidence_Record.
9. IF a CSP violation is reported, THEN THE owner SHALL adjust the policy to the minimum change that resolves the violation, and SHALL repeat the browser check.
10. WHEN the content of Build_Output changes in a way that changes an inline script, THE Deployment_Guide SHALL instruct the maintainer to regenerate the CSP before deployment.
11. THE Deployment_Guide SHALL record that a CSP pass depends on the build in use, so that the browser check is repeated for each release candidate that changes `src/` or dependencies.

#### Verification Steps

1. Build the site; extract inline script hashes with the launch tooling; assert each is present in the CSP when hash-based.
2. Add an inline script to a temporary copy of Build_Output; assert the tooling reports the missing hash.
3. Open each route in a browser against a local static server that applies the same headers; assert zero CSP violations in the console.
4. Assert the CSP contains no `http://` or `https://` origin.

---

### Requirement 7: Deployed-URL Smoke Verification Script

**User Story:** As the site owner, I want one script that checks a deployed URL, so that I can verify each deployment consistently.

#### Acceptance Criteria

1. THE Deployment_Verifier SHALL accept the base URL as a command-line argument, and SHALL fail with a usage message when the argument is absent or is not an absolute `https://` URL.
2. THE Deployment_Verifier SHALL use only Node.js built-in modules and the built-in `fetch`, and SHALL NOT add a dependency.
3. THE Deployment_Verifier SHALL derive the Route_Inventory from validated content using the M2 loaders, and SHALL request each route.
4. WHEN a Route_Inventory route is requested, THE Deployment_Verifier SHALL assert an HTTP status of 200.
5. WHEN a bogus path such as `/this-route-does-not-exist-m10` is requested, THE Deployment_Verifier SHALL assert an HTTP status of 404 and SHALL assert that the response body contains the not-found page content.
6. WHEN a draft blog post slug is requested, THE Deployment_Verifier SHALL assert an HTTP status of 404.
7. THE Deployment_Verifier SHALL assert that every Security_Headers value declared in `vercel.json` is present and equal on each response.
8. WHERE the `x-powered-by` header is present on a response, THE Deployment_Verifier SHALL report a finding.
9. THE Deployment_Verifier SHALL parse each HTML response and SHALL assert, for Route_Inventory routes only, that no `noindex` robots directive is present in the `meta` tag or the `X-Robots-Tag` header, and that the canonical link equals the requested base URL plus the route path on the Production_URL run. On a Preview_Deployment, Vercel's `X-Robots-Tag: noindex` is expected and SHALL be reported as an info finding, and the canonical SHALL be compared against `siteUrl`; both checks are strict on the production run. The not-found response is expected to carry `noindex`.
10. WHEN the base URL differs from `siteUrl` in `content/site.json`, THE Deployment_Verifier SHALL report the difference as an info finding, SHALL compare the canonical against `siteUrl`, and SHALL treat a canonical mismatch against the requested base URL as a finding only for the Production_URL run.
11. THE Deployment_Verifier SHALL apply a request timeout and SHALL report timeouts as findings.
12. THE Deployment_Verifier SHALL print a summary of passed and failed checks per route, SHALL write a JSON report to the git-ignored `reports/` directory, and SHALL exit with a non-zero code when any check fails.
13. THE Deployment_Verifier SHALL NOT be part of `npm test` or any CI job, because THE Deployment_Verifier uses the network.
14. THE Deployment_Guide SHALL document the invocation command, and THE `package.json` script entries `verify:deployment` and `launch:csp` are Approved 2026-10-22 (approvals A2 and A4); this is a separate Approval_Item from the `version` change in Requirement 11.1, and the direct `vite-node` invocation SHALL also be documented.
15. THE Deployment_Verifier SHALL contain pure functions for header comparison, canonical comparison, and report building that are covered by offline unit tests using fixture responses.

#### Verification Steps

1. Run the Deployment_Verifier without an argument; assert a usage message and a non-zero exit.
2. Run the offline unit tests with fixture responses for a missing header, a wrong canonical, a `noindex` tag, and a 200 on a bogus path; assert one finding each.
3. Run the Deployment_Verifier against a Preview_Deployment; assert exit code 0 (with the expected `X-Robots-Tag: noindex` and canonical-versus-`siteUrl` handled as info findings) and a JSON report.
4. Assert `package.json` `test` script and CI configuration do not invoke the Deployment_Verifier.

---

### Requirement 8: Production Domain and Site URL

**User Story:** As a recruiter, I want canonical and sharing URLs to point at the real site, so that links and previews resolve correctly.

#### Acceptance Criteria

1. THE Deployment_Guide SHALL document, as a Human_Procedure, the owner decision between the default `*.vercel.app` domain and a custom domain, and SHALL record the decision date.
2. WHERE a custom domain is chosen, THE Deployment_Guide SHALL document adding the domain in Vercel, the DNS records the owner configures at the registrar, and the verification of HTTPS certificate issuance.
3. WHERE a custom domain is chosen, THE Deployment_Guide SHALL document the choice of apex or `www` as the canonical host and the redirect of the other host to it.
4. WHEN the Production_URL is decided, THE owner SHALL set `content/site.json` `siteUrl` to the Production_URL before the final production build, as a content change.
5. THE `siteUrl` value SHALL be an absolute `https://` URL with no trailing path and no placeholder host.
6. WHEN `siteUrl` is changed, THE owner SHALL run `npm run build` and the M9 SEO audit, and SHALL record that canonical, Open Graph, and JSON-LD URLs equal the Production_URL.
7. IF the M9 SEO audit reports a placeholder-host finding after the change, THEN THE Launch_Checklist SHALL keep Production_Deployment blocked.
8. THE Deployment_Guide SHALL state that the domain decision is reversible only with a repeat of criteria 4 to 6.

#### Verification Steps

1. Read `content/site.json`; assert `siteUrl` is the decided Production_URL.
2. Run `npm run build` and the SEO audit; assert zero findings.
3. Grep Build_Output for `example.vercel.app` and `example.com`; assert zero matches.

---

### Requirement 9: Preview and Production Deployment Execution

**User Story:** As the site owner, I want a repeatable preview-then-production deployment procedure, so that only a verified commit reaches production.

#### Acceptance Criteria

1. THE Deployment_Guide SHALL document creating a release branch (for example `release/v1.0.0`) from the verified release candidate commit.
2. WHEN the release branch is pushed, THE owner SHALL record the Preview_Deployment URL and its Vercel build status as an Evidence_Record.
3. WHEN a Preview_Deployment succeeds, THE owner SHALL run the Deployment_Verifier against the Preview_Deployment URL, and SHALL record the result; on a Preview_Deployment Vercel's `X-Robots-Tag: noindex` is expected (info finding) and the canonical compares against `siteUrl`.
4. WHEN a Preview_Deployment succeeds, THE owner SHALL perform the manual route smoke test, the mobile, tablet, and desktop rendering check at 375px, 768px, and 1024px or wider, and the console and network check, and SHALL record the results.
5. THE console and network check SHALL assert zero console errors, zero CSP violations, and zero requests to origins other than the site origin.
6. THE Deployment_Guide SHALL require that the commit SHA of the Preview_Deployment equals the release candidate SHA recorded in the Launch_Checklist.
7. WHEN every Launch_Checklist item before the Deployment section is checked, THE owner SHALL merge the release branch into the production branch, and the merge SHALL be the only trigger for a Production_Deployment.
8. WHEN the Production_Deployment completes, THE owner SHALL run the Deployment_Verifier against the Production_URL (strict run: canonical against the Production_URL and `X-Robots-Tag: noindex` as an error) and SHALL record the result.
9. WHEN the Production_Deployment completes, THE owner SHALL confirm the six TRD Section 8.2 post-deploy routes: homepage, projects index, certifications page, blog index, one project detail route, and one blog detail route.
10. IF any post-deploy verification fails, THEN THE owner SHALL follow the Rollback procedure (Requirement 12) before further changes.
11. THE Deployment_Guide SHALL require that the owner shares the Production_URL through professional profiles only after the Production_Deployment verification passes.

#### Verification Steps

1. Read the Evidence_Records; assert the Preview_Deployment SHA equals the release candidate SHA.
2. Run the Deployment_Verifier against the Preview_Deployment and the Production_URL; assert exit code 0 for each.
3. Open the browser network panel on three routes; assert all requests are to the site origin.

---

### Requirement 10: No Analytics and Passive Monitoring

**User Story:** As a privacy-conscious owner, I want monitoring that adds no tracking to the site, so that launch honors the no-visitor-data rule.

#### Acceptance Criteria

1. THE M10 deliverables SHALL NOT install or reference `@vercel/analytics`, `@vercel/speed-insights`, or any tracking script, per `PRD.md` Section 10 and `AGENTS.md` 6.1 rule 4.
2. THE Operations_Guide at `docs/operations/monitoring.md` SHALL state that the earlier plan listing Vercel Analytics and Speed Insights is superseded by `PRD.md` Section 10.
3. THE Operations_Guide SHALL document Passive_Monitoring options: Vercel deployment status notifications, an external uptime monitor owned by the owner, and manual PageSpeed Insights and CrUX field-data checks.
4. THE Operations_Guide SHALL document that an external uptime monitor sends requests to the site and adds no script to Build_Output.
5. THE Operations_Guide SHALL list for the uptime monitor: the URLs to check (the Production_URL and `/projects`), the check interval, the alert channel, and the Evidence_Record of the configured monitor.
6. THE Operations_Guide SHALL define SEV1, SEV2, and SEV3 Severity_Levels, with a target response time and a response procedure for each.
7. THE Operations_Guide SHALL state the availability target of 99.5 percent as a goal and SHALL state that the target is not an enforceable SLA on the Hobby Plan, consistent with `TRD.md` Section 6.3.
8. THE Operations_Guide SHALL document how to read PageSpeed Insights results against the `TRD.md` Section 6.1 targets: LCP below 2.5 s, INP below 200 ms, CLS below 0.1, FCP below 1.8 s, and TBT below 200 ms.
9. THE M9 analytics-marker audit SHALL pass on the production Build_Output.

#### Verification Steps

1. Grep `package.json`, `src/`, and Build_Output for `@vercel/analytics`, `speed-insights`, and `_vercel/insights`; assert zero matches.
2. Read the Operations_Guide; assert Severity_Levels, the availability goal, and the monitor setup fields are present.
3. Run the M9 structural audit on the production build; assert zero tracking-marker findings.

---

### Requirement 11: Release Management

**User Story:** As a maintainer, I want a versioned, tagged, and documented release, so that the live site maps to an exact commit and change summary.

#### Acceptance Criteria

1. THE release version SHALL live in `CHANGELOG.md` and the `v1.0.0` Release_Tag only; THE `package.json` `version` bump to `1.0.0` is Declined (approval A3) and SHALL NOT be made. This is a separate Approval_Item from the script entries in Requirement 7.14.
2. THE Release_Tag SHALL be an annotated tag named `v1.0.0` on the Production_Deployment commit; creating and pushing the tag and the merge to the production branch stay manual, and explicit human approval (approval A7) SHALL be requested at launch time, not before.
3. THE `CHANGELOG.md` file SHALL contain a `1.0.0` entry with the release date, a summary of the M1 to M10 capabilities, and links to the Launch_Checklist and Known_Issues_Document.
4. THE `README.md` file SHALL state the Production_URL, the launch date, the Verification_Pipeline commands, and links to `docs/operations/` documents and `docs/quality/` documents.
5. THE Known_Issues_Document SHALL exist at `docs/operations/known-issues.md` and SHALL list each known issue with an identifier, description, severity, affected route, workaround, and planned resolution.
6. THE Known_Issues_Document SHALL list every accepted M9 baseline exception and every item deferred to P1.
7. WHERE no known issue exists, THE Known_Issues_Document SHALL state "No known issues" with the verification date.
8. THE README SHALL NOT contain a placeholder URL, and THE README SHALL NOT contain a secret or token.

#### Verification Steps

1. Run `git tag -v v1.0.0` or `git show v1.0.0`; assert an annotated tag at the Production_Deployment SHA.
2. Read `CHANGELOG.md`, `README.md`, and the Known_Issues_Document; assert the stated fields.
3. Grep `README.md` for `example.com` and `example.vercel.app`; assert zero matches.

---

### Requirement 12: Rollback and Incident Procedure

**User Story:** As the site owner, I want a tested recovery procedure, so that I can restore the site quickly when a deployment regresses.

#### Acceptance Criteria

1. THE Runbook at `docs/operations/rollback-and-incidents.md` SHALL document, as a Human_Procedure, the Vercel instant rollback of the Production_Deployment, SHALL state that on the Hobby Plan instant rollback reaches only the previous production deployment, and SHALL document the path for an older known-good state: `git revert` followed by a new Production_Deployment, or redeploying the older deployment from the Deployments list.
2. THE Runbook SHALL document content rollback through `git revert` of the offending content commit followed by a new Production_Deployment.
3. THE Runbook SHALL contain a decision tree that selects a procedure from the failure trigger: build validation failure, production regression, broken external link, wrong content, and domain or certificate failure, consistent with `TRD.md` Section 8.4.
4. THE Runbook SHALL state that runtime patching is not permitted, per `TRD.md` Section 6.3.
5. WHEN a Rollback completes, THE Runbook SHALL require running the Deployment_Verifier against the Production_URL and recording the result.
6. THE Runbook SHALL define a post-incident note template with the fields: incident date, Severity_Level, detection method, impact, root cause, action taken, time to restore, and prevention.
7. THE Runbook SHALL require that a rollback drill be performed once against a Preview_Deployment or the Production_Deployment before launch sign-off, and SHALL provide an Evidence_Record field for the drill.
8. THE Runbook SHALL state that rolling back a deployment does not revert the git history, and SHALL instruct the maintainer to reconcile the production branch with the rolled-back state.

#### Verification Steps

1. Read the Runbook; assert the procedures, decision tree, and note template are present.
2. Perform the rollback drill; assert the Evidence_Record contains the date and the verification result.
3. Assert each failure trigger from `TRD.md` Section 8.4 maps to a procedure in the decision tree.

---

### Requirement 13: Content Publishing Workflow Documentation

**User Story:** As the content owner, I want a documented publishing flow, so that I can add or edit content without changing application code.

#### Acceptance Criteria

1. THE Publishing_Guide SHALL define branch naming for content changes, including `content/add-project-{slug}`, `content/add-certification-{slug}`, `content/add-post-{slug}`, and `content/edit-{slug}`.
2. THE Publishing_Guide SHALL document the content-only change flow: create or edit one MDX file under `content/`, add optimized assets under `public/images/`, run the Verification_Pipeline, push the branch, review the Preview_Deployment, merge, and verify the Production_Deployment.
3. THE Publishing_Guide SHALL state that a content-only change modifies no file under `src/`, `tests/`, or root configuration.
4. THE Publishing_Guide SHALL include a project QA checklist: frontmatter fields per `AGENTS.md` 5.1 and 5.2, repository link, technology list, a `##` heading in the documentation, at most 3 featured projects, and a working link check.
5. THE Publishing_Guide SHALL include a certification QA checklist: `AGENTS.md` 5.3 rules, a verifiable `verificationUrl`, matching `badgeImageUrl` and `badgeImageAlt`, and no fabricated credential ID, issuer, date, or badge.
6. THE Publishing_Guide SHALL include a blog QA checklist: `AGENTS.md` 5.4 rules, `eventDate` not later than `publishedAt`, `readingTimeMinutes` from 1 to 60, and the `draft` field set intentionally.
7. THE Publishing_Guide SHALL instruct the author to run `npm run audit:links:online` for new external URLs, where the command exists in M9.
8. THE Publishing_Guide SHALL document draft handling: `draft: true` posts are excluded from production builds, and the author verifies the draft slug returns 404 on the Preview_Deployment.
9. THE Publishing_Guide SHALL document post-deploy verification of the new page with the Deployment_Verifier.
10. THE Publishing_Guide SHALL reference `AGENTS.md` for schemas and SHALL NOT redefine any content schema.

#### Verification Steps

1. Read the Publishing_Guide; assert the three QA checklists, branch names, and draft handling are present.
2. Follow the guide with a sample draft blog post on a branch; assert the Verification_Pipeline passes and the draft slug is absent from Build_Output.
3. Grep the guide for schema field tables; assert it references `AGENTS.md` rather than duplicating the schema.

---

### Requirement 14: Post-Launch Plan and Feedback Intake

**User Story:** As the product owner, I want a scheduled post-launch review, so that I can decide on P1 work from evidence.

#### Acceptance Criteria

1. THE Post_Launch_Schedule at `docs/operations/post-launch-plan.md` SHALL define the Week 1 check-in: deployment health, route availability through the Deployment_Verifier, and content rendering.
2. THE Post_Launch_Schedule SHALL define the Week 4 check-in: contact-channel effectiveness measured through direct feedback and enquiries, and content gaps.
3. THE Post_Launch_Schedule SHALL define the Week 12 check-in: a decision on whether to add search, resume download, or an AI assistant, recorded as a decision record with the evidence considered.
4. THE Post_Launch_Schedule SHALL compute each check-in date from the launch date recorded in the README.
5. THE Post_Launch_Schedule SHALL document the feedback intake process: direct recruiter feedback, peer review, and personal usability testing, with a repository issue tracker as the record.
6. THE Post_Launch_Schedule SHALL define an issue template with the fields: source, route, description, severity, and proposed action.
7. THE Post_Launch_Schedule SHALL document the shipping cadence from `PRD.md` Section 15: content updates ship independently, and UI changes follow a reviewed release cycle.
8. THE Post_Launch_Schedule SHALL record the PRD learning goals as questions to answer at the Week 12 check-in.
9. THE Post_Launch_Schedule SHALL state that the check-ins use no visitor analytics, and that measurement relies on direct feedback and manual review.

#### Verification Steps

1. Read the Post_Launch_Schedule; assert the three check-ins, intake process, and issue template are present.
2. Assert each check-in has a calendar date derived from the launch date.
3. Grep the document for analytics tooling references; assert none is recommended.

---

### Requirement 15: Optional Continuous Integration Workflow

**User Story:** As a maintainer, I want automated verification on every pull request, so that regressions are caught before merge.

#### Acceptance Criteria

1. THE `.github/workflows/verify.yml` workflow (Approved 2026-10-22, approval A6) SHALL run on pull requests and on pushes to the production branch.
2. THE workflow SHALL run, in order, `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit`.
3. THE workflow SHALL run only offline audits, and SHALL NOT run `audit:links:online`, `audit:lighthouse`, or the Deployment_Verifier.
4. THE workflow SHALL use the Node.js version documented in the Deployment_Guide.
5. THE workflow SHALL declare minimal read-only repository permissions, and SHALL reference no secret.
6. THE workflow SHALL pin third-party actions to a full commit SHA or a documented major version tag.
7. THE Deployment_Guide SHALL also document the Verification_Pipeline as a manual local procedure that the owner runs before each merge, with an Evidence_Record field, for use when CI is unavailable (the CI workflow is Approved 2026-10-22, approval A6).
8. THE Deployment_Guide SHALL state that Vercel build success does not replace the Verification_Pipeline.

#### Verification Steps

1. Parse the workflow as YAML; assert the step order, permissions, and trigger events.
2. Grep the workflow for `secrets.` and for `audit:lighthouse`; assert zero matches.
3. Open a test pull request; assert the workflow passes.

---

### Requirement 16: Final Sign-off, Traceability, and Handoff

**User Story:** As the product owner, I want launch evidence mapped to the PRD, so that I can approve the MVP and hand it into maintenance.

#### Acceptance Criteria

1. THE Launch_Checklist SHALL contain a Traceability_Matrix mapping each `PRD.md` success metric to launch evidence: portfolio usability, technical credibility, maintainability, accessibility, and performance.
2. THE Traceability_Matrix SHALL name for each metric the evidence source, such as the M9 manual checklist, the M9 Lighthouse results, the Deployment_Verifier report, or the Publishing_Guide.
3. WHERE a PRD metric depends on a human test that cannot be automated, including the 3-minute recruiter task, THE Traceability_Matrix SHALL mark the metric as Human_Procedure and SHALL schedule it in the Post_Launch_Schedule.
4. THE Launch_Checklist SHALL record the `PRD.md` Section 16 stakeholder approvals: Product Lead, Engineering Lead, and Design Lead, each with a name, a date, and a decision.
5. THE Launch_Checklist SHALL record a handoff summary listing the Production_URL, the Release_Tag, the Vercel project name, the monitoring setup, and links to every `docs/operations/` document.
6. THE Launch_Checklist SHALL record the final `implementation_plan.md` Phase 6 status for Tasks 6.1 and 6.2, and SHALL note that the paths `docs/deployment.md` and `docs/launch-checklist.md` in the plan are superseded by `docs/operations/`.
7. IF a stakeholder approval is withheld, THEN THE Launch_Checklist SHALL record the reason and SHALL mark the launch as incomplete.
8. THE Launch_Checklist SHALL mark the MVP launch complete only WHEN all Evidence_Records are filled, the Production_Deployment is verified, the Release_Tag exists, and all three stakeholder approvals are recorded.

#### Verification Steps

1. Read the Traceability_Matrix; assert every PRD success metric has an evidence source.
2. Assert the stakeholder approval fields and handoff summary are present.
3. Assert every link in the handoff summary resolves to a committed file.
