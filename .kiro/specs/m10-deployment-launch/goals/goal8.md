# M10.G8: Release Management Files, README, Versioning, and Optional CI

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the formal release management files: author `CHANGELOG.md` adhering to the Keep a Changelog standard (summarizing Milestones M1 through M10), update `README.md` with production operational references, document the manual `siteUrl` update procedure and release tag instructions, enforce Decision A3 (Declined: `package.json` version remains unmodified), and construct the automated offline CI verification workflow (`.github/workflows/verify.yml`) under verified Human Approval A6. Validate all documentation and workflow assets using automated lint and structural testing suites.

## Goal Success Criteria

- ✓ `CHANGELOG.md` is authored with the `[1.0.0]` entry, release date field, M1–M10 capability summary, and links to `launch-checklist.md` and `known-issues.md`
- ✓ `README.md` is updated with sections for Production URL, Launch Date, Verification Pipeline, Operations Documents, and Quality Documents, with zero placeholder hosts (`example.com`, `example.vercel.app`)
- ✓ `docs/operations/deployment.md` documents the `siteUrl` update procedure (Human_Procedure: owner edits `content/site.json`, runs `npm run build` and `npm run audit:seo`, and records URL equality) and its reversal rules
- ✓ Approval A3 is verified as `Declined`: `package.json` `version` field remains untouched at `"0.1.0"` (version lives exclusively in `CHANGELOG.md` and git tag `v1.0.0`)
- ✓ Approval A6 is verified as `Approved 2026-10-22`: `.github/workflows/verify.yml` is created, running offline checks only (`npm ci`, `lint`, `typecheck`, `test`, `build`, `audit`), with `permissions: contents: read`, zero secrets, and zero invocations of `verify:deployment` or `audit:lighthouse`
- ✓ Release tag procedure (`git tag -a v1.0.0 -m "Release v1.0.0"`) is documented in `deployment.md` as Human Approval A7 (Manual, at launch)
- ✓ `tests/launch/release-files.test.ts`, `tests/launch/ci-workflow.test.ts`, and `tests/launch/docs-real-all.test.ts` pass cleanly with exit code 0

## Prerequisites

- Goals M10.G1 through M10.G7 completed
- Approval records A3 (Declined), A6 (Approved), and A7 (Manual, at launch) confirmed in `task-notes.md`
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M10.G8.T1: Author Project Changelog (`CHANGELOG.md`)

**Objective:** Author `CHANGELOG.md` in the project root adhering to the Keep a Changelog layout, establishing the `[1.0.0]` release baseline with a comprehensive summary of capabilities delivered from M1 through M10 and links to operational guides.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ File `CHANGELOG.md` exists in project root
- ✓ Formatted with H1 `# Changelog` and standard versioning preamble
- ✓ Contains `## [1.0.0] - [Pending Launch]` section
- ✓ Details delivered capabilities from M1 through M10 in structured bullet points
- ✓ Contains links to `docs/operations/launch-checklist.md` and `docs/operations/known-issues.md`

**Prerequisites:**
- M10.G7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\CHANGELOG.md`

**Implementation Details:**
Create `CHANGELOG.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - [Pending Launch]

### Added
- **M1 Repository Foundation & Toolchain:** Next.js 15+ App Router bootstrap, TypeScript strict mode, Tailwind CSS with Singapore Government Design System (SGDS) semantic tokens, ESLint with `jsx-a11y`, Vitest testing harness with jsdom, and pre-commit hooks via Husky/lint-staged.
- **M2 Content Architecture & Validation:** Canonical Zod schemas and typed content loaders for site profile, portfolio projects, certifications/badges, and blog participation logs with strict build-time validation.
- **M3 Global Layout & SGDS Design System:** SGDS-inspired atomic components (Button, Card, Tag, Badge, EmptyState), header, accessible navigation, and footer.
- **M4 Core Application Shell & Navigation:** Global layout shell, routing metadata, and skip-to-content accessibility landmarks.
- **M5 Homepage Experience:** Professional overview, hero positioning, skills taxonomy, featured projects preview, and recent participation feed.
- **M6 Projects Index & Detail Pages:** Filterable project showcase (by technology tag and status), dynamic MDX case-study detail pages with build documentation, metrics, and repository links.
- **M7 Certifications & Credentials Showcase:** Categorized technical certifications and badges with authentic issuer verification links.
- **M8 Blog & Participation Log:** Chronological activity stream covering meetups, hackathons, and technical updates with tag filtering and draft isolation.
- **M9 Offline Audits, Performance & Quality Gates:** Zero-network offline quality audits for structural accessibility (axe-core), performance budgets, metadata completeness, schema validation, and offline link integrity.
- **M10 Deployment & Production Launch:** Vercel Hobby hosting configuration, immutable static caching, Content Security Policy tooling (`csp-hashes.ts`), deployed-URL verification harness (`verify-deployment.ts`), and complete operational runbooks under `docs/operations/`.

### Release Links
- **Launch Readiness Gate:** [Launch Checklist](docs/operations/launch-checklist.md)
- **Defect & Exceptions Registry:** [Known Issues](docs/operations/known-issues.md)
'@ | Set-Content -Path "CHANGELOG.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$cl = Get-Content "CHANGELOG.md" -Raw
if ($cl -match "\[1\.0\.0\]" -and $cl -match "M10 Deployment & Production Launch") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.1, Req 11.3

---

### M10.G8.T2: Update Master Documentation (`README.md`)

**Objective:** Update `README.md` to document the production live site details, canonical quality pipeline commands, links to operations and quality documents, and content publishing workflows, with zero placeholder hosts or secrets.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `README.md` contains sections: `Live Site`, `Verification Pipeline`, `Operations Documentation`, `Quality Audits & Checklists`, and `Content Publishing`
- ✓ Documents all six pipeline commands in order: `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run audit`
- ✓ Contains links resolving to committed files under `docs/operations/` and `docs/quality/`
- ✓ Contains zero placeholder hosts (`example.com`, `example.vercel.app`)
- ✓ Contains zero private tokens or secret references

**Prerequisites:**
- M10.G8.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\README.md`

**Implementation Details:**
Update `README.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
# personal-website-portfolio-v2

A specification-driven, statically generated developer portfolio built with Next.js App Router, TypeScript strict mode, and Tailwind CSS using Singapore Government Design System (SGDS) semantic tokens.

## Live Site

- **Production URL:** [Pending Production Deployment]
- **Release Version:** `v1.0.0`
- **Hosting Platform:** Vercel (Hobby Plan)

---

## Prerequisites

- **Node.js:** `>= 18.0.0`
- **npm:** `>= 9.0.0`

---

## Getting Started

### Local Development
```bash
# Install dependencies
npm ci

# Start local Next.js development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the application.

---

## Verification Pipeline

All changes must pass the complete quality gate sequence prior to merging or deployment:
```bash
npm ci && npm run lint && npm run typecheck && npm test && npm run build && npm run audit
```

### Available Scripts

| Script | Command | Purpose |
| :--- | :--- | :--- |
| `dev` | `next dev` | Starts local Next.js development server |
| `build` | `next build` | Generates static export production output into `out/` |
| `lint` | `next lint` | Executes ESLint checking type safety and accessibility |
| `typecheck` | `tsc --noEmit` | Validates TypeScript strict mode and module resolution |
| `test` | `vitest run` | Runs unit, property, and integration test suites |
| `test:coverage`| `vitest run --coverage` | Generates test coverage report |
| `audit` | `vite-node ... run-all.ts` | Executes M9 offline quality, accessibility, and link audits |
| `verify:deployment` | `vite-node ... verify-deployment.ts` | Verifies deployed preview or production URLs over HTTP |
| `launch:csp` | `vite-node ... csp-hashes.ts` | Analyzes build script hashes and validates CSP compliance |

---

## Operations Documentation

Comprehensive operational documentation and recovery runbooks:
- **Pre-Launch Checklist:** [`docs/operations/launch-checklist.md`](docs/operations/launch-checklist.md)
- **Deployment Guide:** [`docs/operations/deployment.md`](docs/operations/deployment.md)
- **Monitoring & Health Guide:** [`docs/operations/monitoring.md`](docs/operations/monitoring.md)
- **Rollback & Incident Runbook:** [`docs/operations/rollback-and-incidents.md`](docs/operations/rollback-and-incidents.md)
- **Content Publishing Workflow:** [`docs/operations/content-publishing.md`](docs/operations/content-publishing.md)
- **Known Issues & Defect Registry:** [`docs/operations/known-issues.md`](docs/operations/known-issues.md)
- **Post-Launch Review Plan:** [`docs/operations/post-launch-plan.md`](docs/operations/post-launch-plan.md)

---

## Quality Audits & Checklists

Quality evidence and baseline audit records:
- **Offline Quality Audits:** `docs/quality/`
- **Generated Audit Reports:** `reports/` (git-ignored)

---

## Content Publishing

Publishing new projects, certifications, or blog entries is entirely content-driven and requires zero application code modifications. Refer to the [Content Publishing Guide](docs/operations/content-publishing.md) for branch naming conventions and QA checklists.

---

## Architectural Constraints (P0 Scope)

Per `AGENTS.md` and `TRD.md`, the following boundaries are non-negotiable:
- ❌ **No runtime database:** Zero ORMs, SQL drivers, or external DB connections.
- ❌ **No authentication:** Zero session management, cookies, JWT, or OAuth.
- ❌ **No custom public APIs:** Zero route handlers, API routes, or server actions.
- ❌ **No visitor tracking:** Zero analytics, third-party telemetry, or data collection.
- ✅ **Static-first:** 100% pre-rendered HTML/CSS/JS served via CDN.
- ✅ **Local Content:** All portfolio data loaded from `content/` Markdown/MDX and JSON files.
- ✅ **Strict Types:** Zero `any`, non-null assertions (`!`), or unsafe type casting.
'@ | Set-Content -Path "README.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$readme = Get-Content "README.md" -Raw
$hasPlaceholder = $readme -match "example\.com" -or $readme -match "example\.vercel\.app"
if (-not $hasPlaceholder -and ($readme -match "Operations Documentation") -and ($readme -match "verify:deployment")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.4, Req 11.8

---

### M10.G8.T3: Document Site URL Update Procedure in Deployment Guide

**Objective:** Append the human procedure for updating `siteUrl` in `content/site.json` to `docs/operations/deployment.md`, specifying local build verification, SEO audit verification, and domain reversal instructions.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Documents owner procedure to update `content/site.json` `siteUrl` to production HTTPS domain
- ✓ Details required verification: `npm run build` followed by `npm run audit:seo`
- ✓ Confirms that any placeholder finding keeps production deployment strictly blocked
- ✓ Details the reversal procedure should the domain decision change

**Prerequisites:**
- M10.G8.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**
Append the siteUrl update procedure to `docs/operations/deployment.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$siteUrlProc = @'

### Site URL Finalization Procedure (Human_Procedure)
1. Open `content/site.json` in your editor.
2. Update the `siteUrl` field to the decided Production URL (e.g. `https://portfolio.vercel.app` or `https://angeloandres.dev`):
   - Value must be an absolute `https://` URL.
   - Value must NOT contain a trailing slash or path.
   - Value must NOT contain `example.com` or `example.vercel.app`.
3. Execute local static compilation:
   ```bash
   npm run build
   ```
4. Execute M9 SEO and metadata audit:
   ```bash
   npm run audit:seo
   ```
5. Confirm zero placeholder findings in `reports/seo-audit.json`.
6. Confirm canonical link tags, Open Graph meta tags, and JSON-LD schema blocks in `out/*.html` reflect the new domain.

*Domain Reversal Note: If the domain decision is reversed (e.g. reverting from a custom domain back to Vercel default), repeat steps 1 through 6 in full. Never point production traffic to an unverified domain.*
'@

Add-Content -Path "docs\operations\deployment.md" -Value $siteUrlProc -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$dep = Get-Content "docs\operations\deployment.md" -Raw
if ($dep -match "Site URL Finalization Procedure" -and $dep -match "Domain Reversal Note") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.4, Req 8.5, Req 8.6, Req 8.7, Req 8.8

---

### M10.G8.T4: Verify Approval Decisions for A3, A6, and A7 in Task Notes

**Objective:** Inspect `.kiro/specs/m10-deployment-launch/task-notes.md` to programmatically confirm that Approval A3 is recorded as Declined, Approval A6 is recorded as Approved, and Approval A7 is recorded as Manual at launch before proceeding.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Programmatically confirms Decision A3 is `Declined 2026-10-22 (approval A3)`
- ✓ Programmatically confirms Decision A6 is `Approved 2026-10-22 (approval A6)`
- ✓ Programmatically confirms Decision A7 is `Manual, at launch`
- ✓ Throws exception and halts execution if any status is inconsistent

**Prerequisites:**
- M10.G1.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Execute the decision gate verification script via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw

$a3Declined = $notes -match "Declined 2026-10-22 \(approval A3\)"
$a6Approved = $notes -match "Approved 2026-10-22 \(approval A6\)"
$a7Manual = $notes -match "Manual, at launch"

if (-not ($a3Declined -and $a6Approved -and $a7Manual)) {
    throw "Approval Gate Failure: Status for A3, A6, or A7 does not match recorded decisions."
}

Write-Host "Approval Gate Passed: A3 confirmed Declined; A6 confirmed Approved; A7 confirmed Manual at launch."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "approval A3" -and $notes -match "approval A6" -and $notes -match "A7") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 11.1, Req 11.2, Req 15.1

---

### M10.G8.T5: Enforce Declined Version Bump (Decision A3)

**Objective:** Audit `package.json` to verify that the `version` property has not been modified and remains `"0.1.0"`, documenting that the release version lives strictly in `CHANGELOG.md` and the annotated Git tag `v1.0.0`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Inspects `package.json` and asserts `pkg.version === "0.1.0"`
- ✓ `git diff package.json` confirms zero changes to the `version` field
- ✓ Verifies compliance with Human Decision A3 (Declined)

**Prerequisites:**
- M10.G8.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\package.json`

**Implementation Details:**
Execute the version audit script via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.version -ne "0.1.0") {
    throw "Boundary Violation: package.json version was altered to '$($pkg.version)'. Decision A3 mandates version remains 0.1.0."
}

$diff = git diff package.json
if ($diff -match '"version":') {
    throw "Boundary Violation: git diff shows unapproved modification to package.json version."
}

Write-Host "Decision A3 Verified: package.json version remains cleanly unchanged at 0.1.0."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.version -eq "0.1.0") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 11.1

---

### M10.G8.T6: Create Offline CI Verification Workflow (`.github/workflows/verify.yml`)

**Objective:** Under verified Approval A6, create `.github/workflows/verify.yml` configuring automated offline verification on pull requests and main pushes, declaring read-only permissions, and excluding all network tools.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ File `.github/workflows/verify.yml` exists
- ✓ Triggers on `pull_request` and `push` to `main`
- ✓ Declares `permissions: contents: read`
- ✓ Configured with Node version matching `engines.node` (18)
- ✓ Runs canonical offline sequence: `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run audit`
- ✓ Contains zero references to `secrets.`
- ✓ Strictly excludes `verify:deployment`, `audit:lighthouse`, and `audit:links:online`

**Prerequisites:**
- M10.G8.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.github\workflows\verify.yml`

**Implementation Details:**
Create `.github/workflows/verify.yml` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path ".github\workflows")) {
    New-Item -ItemType Directory -Path ".github\workflows" -Force | Out-Null
}

@'
name: verify

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Code Quality & Lint
        run: npm run lint

      - name: Type Checking
        run: npm run typecheck

      - name: Unit & Property Tests
        run: npm test

      - name: Static Build Export
        run: npm run build

      - name: Offline Audits & Quality Gates
        run: npm run audit
'@ | Set-Content -Path ".github\workflows\verify.yml" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$ci = Get-Content ".github\workflows\verify.yml" -Raw
$hasSecrets = $ci -match "secrets\."
$hasNetwork = $ci -match "verify:deployment" -or $ci -match "audit:lighthouse"
if (-not $hasSecrets -and -not $hasNetwork -and ($ci -match "contents: read")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 15.1, Req 15.2, Req 15.3, Req 15.4, Req 15.5, Req 15.6

---

### M10.G8.T7: Document Release Tag Procedure in Deployment Guide (Approval A7)

**Objective:** Append the manual annotated Git release tag procedure to `docs/operations/deployment.md`, noting that tag creation and remote pushing require explicit human approval at launch time.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Documents procedure to create annotated tag `v1.0.0` on production deployment commit
- ✓ Details verification command: `git show v1.0.0`
- ✓ Documents remote push: `git push origin v1.0.0`
- ✓ Documents fallback in case approval is withheld: recording commit SHA in `launch-checklist.md` and `CHANGELOG.md`

**Prerequisites:**
- M10.G8.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**
Append tag procedure to `docs/operations/deployment.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$tagProc = @'

---

## Release Tagging Procedure (Human Approval A7)

Creating and pushing the production release tag is a **Human_Procedure** executed only after production deployment verification passes:

### Tag Creation Steps
1. Identify the verified Production Deployment commit SHA:
   ```bash
   git rev-parse HEAD
   ```
2. Create an annotated release tag on the verified commit:
   ```bash
   git tag -a v1.0.0 HEAD -m "Release v1.0.0: Personal Website Portfolio P0 MVP"
   ```
3. Verify the tag properties:
   ```bash
   git show v1.0.0
   ```
   Confirm that the tag type is `tag` (annotated) and matches the production SHA.
4. Push the tag to remote:
   ```bash
   git push origin v1.0.0
   ```

### Fallback if Approval Withheld
If human approval for creating or pushing the Git tag is withheld, record the production deployment commit SHA directly in `docs/operations/launch-checklist.md` and `CHANGELOG.md` without tagging.
'@

Add-Content -Path "docs\operations\deployment.md" -Value $tagProc -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$dep = Get-Content "docs\operations\deployment.md" -Raw
if ($dep -match "Release Tagging Procedure" -and $dep -match "git tag -a v1\.0\.0") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.2

---

### M10.G8.T8: Author Release Files Integrity Unit Test (`tests/launch/release-files.test.ts`)

**Objective:** Write `tests/launch/release-files.test.ts` to assert that `CHANGELOG.md` adheres to Keep a Changelog structure, `README.md` links resolve to committed files, and zero placeholder URLs or secrets exist.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Asserts `CHANGELOG.md` contains `## [1.0.0]` and references M1–M10
- ✓ Asserts all documentation links in `README.md` resolve to existing committed files on disk
- ✓ Asserts zero instances of `example.com` or `example.vercel.app` in `README.md`
- ✓ Asserts zero private tokens or secret patterns in `README.md`
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G8.T1 and M10.G8.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\release-files.test.ts`

**Implementation Details:**
Create `tests/launch/release-files.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('Release Management Files Verification', () => {
  it('validates CHANGELOG.md format and milestone coverage', () => {
    const clPath = path.resolve(process.cwd(), 'CHANGELOG.md');
    expect(fs.existsSync(clPath)).toBe(true);

    const content = fs.readFileSync(clPath, 'utf8');
    expect(content).toContain('## [1.0.0]');
    expect(content).toContain('M1 Repository Foundation');
    expect(content).toContain('M10 Deployment & Production Launch');
    expect(content).toContain('docs/operations/launch-checklist.md');
    expect(content).toContain('docs/operations/known-issues.md');
  });

  it('validates README.md operational links and hygiene', () => {
    const readmePath = path.resolve(process.cwd(), 'README.md');
    expect(fs.existsSync(readmePath)).toBe(true);

    const content = fs.readFileSync(readmePath, 'utf8');

    // 1. Hygiene checks
    expect(content).not.toContain('example.com');
    expect(content).not.toContain('example.vercel.app');
    expect(content).not.toMatch(/ghp_[a-zA-Z0-9]{36}/); // Token regex

    // 2. Resolve internal markdown links
    const linkMatches = content.match(/\[.*?\]\((docs\/operations\/.*?\.md)\)/g) ?? [];
    expect(linkMatches.length).toBeGreaterThanOrEqual(5);

    for (const match of linkMatches) {
      const relPath = match.replace(/\[.*?\]\(/, '').replace(/\)/, '');
      const fullPath = path.resolve(process.cwd(), relPath);
      expect(fs.existsSync(fullPath), `Link target ${relPath} must exist on disk`).toBe(true);
    }
  });
});
'@ | Set-Content -Path "tests\launch\release-files.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/release-files.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.3, Req 11.4, Req 11.8

---

### M10.G8.T9: Author CI Workflow & Real Docs Verification Tests

**Objective:** Write `tests/launch/ci-workflow.test.ts` to validate workflow triggers, step sequences, and permissions, and `tests/launch/docs-real-all.test.ts` to run `checkDocStructure` across all 7 operational documents and `README.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `tests/launch/ci-workflow.test.ts` validates YAML structure of `.github/workflows/verify.yml`
- ✓ Asserts presence of `contents: read` permissions and zero secrets
- ✓ Asserts exact 6-step offline verification sequence
- ✓ `tests/launch/docs-real-all.test.ts` executes `checkDocStructure` over all 7 `DOC_SPECS` and `README_SPEC` with 0 issues
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G8.T6 and M10.G8.T8 completed
- Target files: `tests/launch/ci-workflow.test.ts`, `tests/launch/docs-real-all.test.ts`

**Implementation Details:**
Create the test files using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. ci-workflow.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('CI Workflow Verification (.github/workflows/verify.yml)', () => {
  it('validates workflow triggers, permissions, and offline step sequence', () => {
    const ciPath = path.resolve(process.cwd(), '.github/workflows/verify.yml');
    expect(fs.existsSync(ciPath)).toBe(true);

    const content = fs.readFileSync(ciPath, 'utf8');

    // Permissions and triggers
    expect(content).toContain('pull_request:');
    expect(content).toContain('branches: [main]');
    expect(content).toContain('contents: read');

    // Security hygiene: zero secrets
    expect(content).not.toContain('secrets.');

    // Zero network verification tools
    expect(content).not.toContain('verify-deployment');
    expect(content).not.toContain('audit:lighthouse');
    expect(content).not.toContain('audit:links:online');

    // Step order
    const stepOrder = [
      'npm ci',
      'npm run lint',
      'npm run typecheck',
      'npm test',
      'npm run build',
      'npm run audit',
    ];

    let lastIdx = -1;
    for (const step of stepOrder) {
      const idx = content.indexOf(step);
      expect(idx, `Expected step '${step}' to be present`).toBeGreaterThan(-1);
      expect(idx, `Expected step '${step}' to follow previous step`).toBeGreaterThan(lastIdx);
      lastIdx = idx;
    }
  });
});
'@ | Set-Content -Path "tests\launch\ci-workflow.test.ts" -Encoding UTF8

# 2. docs-real-all.test.ts
@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { checkDocStructure, DOC_SPECS, README_SPEC } from '../../scripts/launch/lib/docs-structure';

describe('Full Repository Documentation Schema Lint', () => {
  for (const spec of DOC_SPECS) {
    it(`validates ${spec.path} against schema`, () => {
      const fullPath = path.resolve(process.cwd(), spec.path);
      expect(fs.existsSync(fullPath)).toBe(true);

      const content = fs.readFileSync(fullPath, 'utf8');
      const issues = checkDocStructure(content, spec);
      expect(issues).toEqual([]);
    });
  }

  it('validates README.md against README_SPEC with no placeholder hosts', () => {
    const readmePath = path.resolve(process.cwd(), README_SPEC.path);
    expect(fs.existsSync(readmePath)).toBe(true);

    const content = fs.readFileSync(readmePath, 'utf8');
    const issues = checkDocStructure(content, README_SPEC);
    expect(issues).toEqual([]);
  });
});
'@ | Set-Content -Path "tests\launch\docs-real-all.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/ci-workflow.test.ts tests/launch/docs-real-all.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.4, Req 11.8, Req 15.1–15.6

---

### M10.G8.T10: Goal 8 Checkpoint and Quality Gate Verification

**Objective:** Run the full quality verification suite (lint, typecheck, release file tests, CI workflow tests, and comprehensive docs lint) to seal Goal 8 with zero regressions.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ All release file, CI workflow, and full docs lint test suites pass
- ✓ `git diff` confirms modifications are strictly limited to `CHANGELOG.md`, `README.md`, `docs/operations/`, `.github/workflows/verify.yml`, and `tests/launch/`
- ✓ `package.json` version remains completely unmodified

**Prerequisites:**
- M10.G8.T1 through M10.G8.T9 completed

**Implementation Details:**
Execute the verification pipeline via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw "Typecheck failed" }

# 2. Lint
npm run lint
if ($LASTEXITCODE -ne 0) { throw "Lint failed" }

# 3. Test Suites
npx vitest run tests/launch/release-files.test.ts tests/launch/ci-workflow.test.ts tests/launch/docs-real-all.test.ts
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

# 4. Final Version Check
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
if ($pkg.version -ne "0.1.0") { throw "Version violation detected in package.json" }

Write-Host "M10.G8 Checkpoint: All release management and CI assets verified cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/release-files.test.ts tests/launch/ci-workflow.test.ts tests/launch/docs-real-all.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 8.4–8.8, Req 11.1–11.4, Req 11.8, Req 15.1–15.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "CHANGELOG.md"
Test-Path ".github\workflows\verify.yml"
npx vitest run tests/launch/release-files.test.ts tests/launch/ci-workflow.test.ts tests/launch/docs-real-all.test.ts
git diff --stat package.json
```
Expected output:
- `True` for `CHANGELOG.md` and `verify.yml`
- Vitest reports 3 test files passed with 0 failures
- `git diff --stat package.json` shows only scripts modified (0 version lines changed)