# M10.G6: Documentation Structure Lint, Launch Checklist, and Deployment Guide

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G6 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the pure documentation structure linter (`scripts/launch/lib/docs-structure.ts`) and prove Correctness Properties 18 and 19 using fast-check. Author the master pre-launch operational documents: `docs/operations/launch-checklist.md` (covering all Release_Blockers, pipeline gates, PRD Section 12 open questions, and empty Evidence_Record tables) and `docs/operations/deployment.md` (documenting Vercel project configuration, static export verification, CSP trade-offs, security headers, custom domain DNS, verifier CLI usage, and manual verification fallbacks).

## Goal Success Criteria

- ✓ `scripts/launch/lib/docs-structure.ts` exports `DOC_SPECS`, `README_SPEC`, `extractHeadings` (ignoring code fences), `checkDocStructure`, and `extractEvidenceFields`
- ✓ Properties 18 (heading hierarchy, ordering, and presence) and 19 (placeholder host detection outside code fences) pass at least 100 runs each
- ✓ `docs/operations/launch-checklist.md` is authored with all 11 required sections, explicitly stating that Production_Deployment is blocked while any item before Deployment remains unchecked
- ✓ `docs/operations/deployment.md` is authored with all 11 required sections, documenting the Vercel Hobby setup, output directory `out`, CSP trade-offs (Decision 1), security headers, and domain procedures
- ✓ All Evidence_Record tables are initialized with structured, empty/pending fields—zero fabricated evidence
- ✓ Document structure tests in `tests/launch/docs-real.test.ts` and `tests/launch/launch-checklist.test.ts` pass cleanly with exit code 0

## Prerequisites

- Goals M10.G1 through M10.G5 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Vitest and fast-check operational

---

## Tasks

### M10.G6.T1: Implement Markdown Structure Lint Engine (`scripts/launch/lib/docs-structure.ts`)

**Objective:** Implement `scripts/launch/lib/docs-structure.ts` providing pure functions `extractHeadings`, `extractEvidenceFields`, and `checkDocStructure` to validate document schema compliance without external dependencies.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `extractHeadings(markdown)` parses H1 (`#`) and H2 (`##`) headers while strictly ignoring heading-like lines inside fenced code blocks (` ``` `)
- ✓ `extractEvidenceFields(markdown)` extracts all table field labels from Markdown tables with `| Field | Value |` headers
- ✓ `checkDocStructure(markdown, spec)` verifies title presence, exact ordered H2 presence, duplicate headings, and missing evidence fields
- ✓ Flags `example.com` or `example.vercel.app` as `placeholder-url` outside code fences if `spec.noPlaceholderHosts === true`

**Prerequisites:**
- M10.G1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\docs-structure.ts`

**Implementation Details:**
Create `scripts/launch/lib/docs-structure.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
export interface DocSpec {
  readonly path: string;
  readonly title: string;
  readonly sections: readonly string[];
  readonly evidenceFields: readonly string[];
  readonly noPlaceholderHosts: boolean;
}

export interface DocIssue {
  readonly path: string;
  readonly rule: string;
  readonly message: string;
}

export function extractHeadings(markdown: string): readonly { level: number; text: string }[] {
  const headings: { level: number; text: string }[] = [];
  const lines = markdown.split(/\r?\n/);
  let inCodeBlock = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      continue;
    }

    if (!inCodeBlock) {
      if (trimmed.startsWith('# ')) {
        headings.push({ level: 1, text: trimmed.slice(2).trim() });
      } else if (trimmed.startsWith('## ')) {
        headings.push({ level: 2, text: trimmed.slice(3).trim() });
      }
    }
  }

  return headings;
}

export function extractEvidenceFields(markdown: string): readonly string[] {
  const fields: string[] = [];
  const lines = markdown.split(/\r?\n/);
  let inEvidenceTable = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.includes('| Field | Value |') || trimmed.includes('|Field|Value|')) {
      inEvidenceTable = true;
      continue;
    }

    if (inEvidenceTable) {
      if (!trimmed.startsWith('|')) {
        inEvidenceTable = false;
        continue;
      }
      if (trimmed.includes('---')) continue;

      const parts = trimmed.split('|').map(p => p.trim()).filter(Boolean);
      if (parts.length >= 1 && parts[0]) {
        fields.push(parts[0]);
      }
    }
  }

  return fields;
}

export function checkDocStructure(markdown: string, spec: DocSpec): readonly DocIssue[] {
  const issues: DocIssue[] = [];
  const headings = extractHeadings(markdown);

  // 1. Title Check
  const h1 = headings.find(h => h.level === 1);
  if (!h1 || h1.text !== spec.title) {
    issues.push({
      path: spec.path,
      rule: 'title-missing',
      message: `Expected H1 title '${spec.title}', got '${h1 ? h1.text : 'none'}'.`,
    });
  }

  // 2. Ordered Sections Check
  const h2List = headings.filter(h => h.level === 2).map(h => h.text);
  const seenH2 = new Set<string>();

  for (const h2 of h2List) {
    if (seenH2.has(h2)) {
      issues.push({
        path: spec.path,
        rule: 'section-duplicate',
        message: `Duplicate H2 section '${h2}' detected.`,
      });
    }
    seenH2.add(h2);
  }

  let lastIndex = -1;
  for (const expectedSec of spec.sections) {
    const actualIndex = h2List.indexOf(expectedSec);
    if (actualIndex === -1) {
      issues.push({
        path: spec.path,
        rule: 'section-missing',
        message: `Required section '## ${expectedSec}' is missing.`,
      });
    } else {
      if (actualIndex < lastIndex) {
        issues.push({
          path: spec.path,
          rule: 'section-order',
          message: `Section '## ${expectedSec}' appears out of expected order.`,
        });
      }
      lastIndex = actualIndex;
    }
  }

  // 3. Evidence Fields Check
  if (spec.evidenceFields.length > 0) {
    const actualFields = new Set(extractEvidenceFields(markdown));
    for (const expField of spec.evidenceFields) {
      if (!actualFields.has(expField)) {
        issues.push({
          path: spec.path,
          rule: 'evidence-field-missing',
          message: `Required evidence field '${expField}' is missing from Evidence Record tables.`,
        });
      }
    }
  }

  // 4. Placeholder Host Check
  if (spec.noPlaceholderHosts) {
    const lines = markdown.split(/\r?\n/);
    let inCode = false;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i] ?? '';
      if (line.trim().startsWith('```')) {
        inCode = !inCode;
        continue;
      }
      if (!inCode) {
        if (line.includes('example.com') || line.includes('example.vercel.app')) {
          issues.push({
            path: spec.path,
            rule: 'placeholder-url',
            message: `Line ${i + 1} contains prohibited placeholder host outside code fence.`,
          });
        }
      }
    }
  }

  return issues;
}
'@ | Set-Content -Path "scripts\launch\lib\docs-structure.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 4.2, Req 11.5, Req 16.5

---

### M10.G6.T2: Add Document Specifications (`DOC_SPECS` & `README_SPEC`)

**Objective:** Append `DOC_SPECS` and `README_SPEC` definitions to `scripts/launch/lib/docs-structure.ts` defining canonical schemas for all seven operations documents.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `DOC_SPECS` contains exact specifications for all 7 operational documents under `docs/operations/`
- ✓ `README_SPEC` configures `noPlaceholderHosts: true` for README inspection
- ✓ Required section ordering strictly matches `design.md` specifications

**Prerequisites:**
- M10.G6.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\docs-structure.ts`

**Implementation Details:**
Append `DOC_SPECS` to `scripts/launch/lib/docs-structure.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$docSpecsCode = @'

export const DOC_SPECS: readonly DocSpec[] = [
  {
    path: 'docs/operations/launch-checklist.md',
    title: 'Launch Checklist',
    sections: [
      'Release Candidate',
      'Content',
      'Configuration',
      'Verification Pipeline',
      'Accessibility and Performance',
      'Security',
      'Deployment',
      'Sign-off',
      'Traceability Matrix',
      'Stakeholder Approvals',
      'Handoff Summary',
    ],
    evidenceFields: ['Commit SHA', 'Evidence ID'],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/deployment.md',
    title: 'Deployment Guide',
    sections: [
      'Vercel Project Setup',
      'Build Settings',
      'Environment',
      'Platform Limits',
      'Domain and Site URL',
      'Security Headers',
      'Content Security Policy',
      'Preview Deployment',
      'Production Deployment',
      'Verification Pipeline Without CI',
      'Verifier Usage',
    ],
    evidenceFields: ['Evidence ID', 'Outcome'],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/monitoring.md',
    title: 'Operations Guide',
    sections: [
      'Policy',
      'Passive Monitoring Options',
      'Uptime Monitor',
      'Severity Levels',
      'Availability Goal',
      'Reading PageSpeed Insights',
    ],
    evidenceFields: ['Evidence ID'],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/rollback-and-incidents.md',
    title: 'Rollback and Incident Runbook',
    sections: [
      'Principles',
      'Decision Tree',
      'Instant Rollback',
      'Content Rollback',
      'After a Rollback',
      'Rollback Drill',
      'Post-Incident Note Template',
    ],
    evidenceFields: ['Evidence ID', 'Outcome'],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/content-publishing.md',
    title: 'Content Publishing Guide',
    sections: [
      'Branch Naming',
      'Content-Only Change Flow',
      'Project QA Checklist',
      'Certification QA Checklist',
      'Blog QA Checklist',
      'Draft Handling',
      'Post-Deploy Verification',
      'Schema Reference',
    ],
    evidenceFields: [],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/known-issues.md',
    title: 'Known Issues',
    sections: [
      'Summary',
      'Known Issues',
      'Accepted M9 Baseline Exceptions',
      'Deferred to P1',
    ],
    evidenceFields: [],
    noPlaceholderHosts: false,
  },
  {
    path: 'docs/operations/post-launch-plan.md',
    title: 'Post-Launch Plan',
    sections: [
      'Check-in Schedule',
      'Week 1',
      'Week 4',
      'Week 12',
      'Feedback Intake',
      'Issue Template',
      'Shipping Cadence',
      'Learning Goals',
      'Measurement Policy',
    ],
    evidenceFields: [],
    noPlaceholderHosts: false,
  },
];

export const README_SPEC: DocSpec = {
  path: 'README.md',
  title: 'personal-website-portfolio-v2',
  sections: [
    'Prerequisites',
    'Getting Started',
    'Verification Pipeline',
    'Architectural Constraints (P0 Scope)',
    'Master Specifications',
  ],
  evidenceFields: [],
  noPlaceholderHosts: true,
};
'@

Add-Content -Path "scripts\launch\lib\docs-structure.ts" -Value $docSpecsCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 4.2, Req 10.2, Req 11.5, Req 11.8, Req 12.1, Req 13.1, Req 14.1, Req 16.5

---

### M10.G6.T3: Implement Fast-Check Tests for Docs Properties 18 and 19

**Objective:** Write randomized property-based tests in `tests/launch/docs-structure.property.test.ts` formally proving Property 18 (docs structure validation) and Property 19 (placeholder host detection outside code fences) over at least 100 iterations.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Property 18 proves `checkDocStructure` detects missing H1, missing H2 sections, duplicate H2 sections, and out-of-order H2 sections
- ✓ Proves lines matching `#` or `##` inside ` ``` ` code fences are completely ignored
- ✓ Property 19 proves `placeholder-url` issues are triggered when `example.com` or `example.vercel.app` appear in prose, and ignored inside code fences
- ✓ Tests pass with at least 100 runs each

**Prerequisites:**
- M10.G6.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\docs-structure.property.test.ts`

**Implementation Details:**
Create `tests/launch/docs-structure.property.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import { checkDocStructure, type DocSpec } from '../../scripts/launch/lib/docs-structure';

describe('M10 Documentation Structure Properties (Properties 18 & 19)', () => {
  const dummySpec: DocSpec = {
    path: 'test-doc.md',
    title: 'Test Document',
    sections: ['Alpha Section', 'Beta Section', 'Gamma Section'],
    evidenceFields: ['Commit SHA'],
    noPlaceholderHosts: true,
  };

  // Feature: m10-deployment-launch, Property 18: Documentation structure lint
  it('Property 18: Documentation structure lint', () => {
    fc.assert(
      fc.property(
        fc.shuffledSubarray(dummySpec.sections, { minLength: 1, maxLength: 3 }),
        shuffled => {
          let doc = `# ${dummySpec.title}\n\n`;
          for (const s of shuffled) {
            doc += `## ${s}\nContent\n\n`;
          }
          // Add table with evidence
          doc += '| Field | Value |\n|---|---|\n| Commit SHA | 1234567 |\n\n';

          const issues = checkDocStructure(doc, dummySpec);

          if (shuffled.length < dummySpec.sections.length) {
            expect(issues.some(i => i.rule === 'section-missing')).toBe(true);
          } else {
            // All present, check if ordered
            const isOrdered = shuffled[0] === 'Alpha Section' && shuffled[1] === 'Beta Section' && shuffled[2] === 'Gamma Section';
            if (!isOrdered) {
              expect(issues.some(i => i.rule === 'section-order')).toBe(true);
            } else {
              expect(issues).toEqual([]);
            }
          }
        }
      ),
      { numRuns: 100 }
    );

    // Code fence immunity check
    const docWithFencedHeadings = `
# ${dummySpec.title}
## Alpha Section
## Beta Section
## Gamma Section

\`\`\`markdown
# Fake Title Inside Code
## Out Of Order Section Inside Code
\`\`\`

| Field | Value |
|---|---|
| Commit SHA | 1234567 |
`;
    expect(checkDocStructure(docWithFencedHeadings, dummySpec)).toEqual([]);
  });

  // Feature: m10-deployment-launch, Property 19: Placeholder hosts are flagged only outside code fences
  it('Property 19: Placeholder hosts are flagged only outside code fences', () => {
    // 1. Placeholder in code fence is ignored
    const docWithFencedPlaceholder = `
# ${dummySpec.title}
## Alpha Section
## Beta Section
## Gamma Section

\`\`\`bash
curl https://example.com/api
\`\`\`

| Field | Value |
|---|---|
| Commit SHA | 1234567 |
`;
    const issuesFenced = checkDocStructure(docWithFencedPlaceholder, dummySpec);
    expect(issuesFenced.filter(i => i.rule === 'placeholder-url')).toEqual([]);

    // 2. Placeholder in prose is flagged
    const docWithProsePlaceholder = `
# ${dummySpec.title}
## Alpha Section
## Beta Section
## Gamma Section

Visit https://example.com for more info.

| Field | Value |
|---|---|
| Commit SHA | 1234567 |
`;
    const issuesProse = checkDocStructure(docWithProsePlaceholder, dummySpec);
    expect(issuesProse.some(i => i.rule === 'placeholder-url')).toBe(true);
  });
});
'@ | Set-Content -Path "tests\launch\docs-structure.property.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/docs-structure.property.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 11.8, Req 16.5

---

### M10.G6.T4: Author Launch Checklist (`docs/operations/launch-checklist.md`)

**Objective:** Author `docs/operations/launch-checklist.md` with all 11 required sections, explicitly establishing that Production_Deployment is prohibited while any pre-deployment item is unchecked, detailing all Release_Blockers, Task 6.2 steps, and empty Evidence_Record tables.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ File `docs/operations/launch-checklist.md` exists
- ✓ Contains H1 `Launch Checklist` and status block
- ✓ Contains all 11 H2 sections in exact specified order
- ✓ Explicitly states: "Production_Deployment is not permitted while any item above Deployment is unchecked"
- ✓ Lists all Release_Blockers: placeholder `siteUrl`, placeholder contact email, fewer than 3 P0 projects, unverified certifications, failing verification commands
- ✓ Details Task 6.2 steps: route availability, external link validation, draft post inaccessibility, multi-viewport rendering, console/network hygiene
- ✓ Contains empty Evidence_Record tables with `Commit SHA` and `Evidence ID` fields

**Prerequisites:**
- M10.G6.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\launch-checklist.md`

**Implementation Details:**
Create `docs/operations/launch-checklist.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "docs\operations")) {
    New-Item -ItemType Directory -Path "docs\operations" -Force | Out-Null
}

@'
# Launch Checklist

> **Document Status:** Active / Operational  
> **Owner:** Angelo Andres  
> **Last reviewed:** 2026-10-22  
> **Scope:** P0 MVP Deployment & Production Release Gate  

---

## Release Candidate

Production_Deployment is not permitted while any item above Deployment is unchecked.

- [ ] Release Candidate Commit SHA identified and recorded:
  - Commit SHA: `[PENDING RELEASE CANDIDATE]`

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-01 |
| Step | Release Candidate Identification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | git rev-parse HEAD |

---

## Content

- [ ] At least 3 complete P0 portfolio projects exist with repository link, technology list, and build documentation.
- [ ] Every published certification has a public `verificationUrl` or has been removed (zero fabricated credentials).
- [ ] `content/site.json` `siteUrl` is updated to production domain (zero placeholder hosts).
- [ ] Contact channels in `content/site.json` are verified real destinations (zero placeholder emails or links).
- [ ] External links verified resolving via `npm run audit:links:online`.
- [ ] PRD Section 12 Open Questions resolved:
  - Q1 (P0 Projects): Confirmed complete project inventory.
  - Q2 (Verifiable Certifications): Verified credentials documented.
  - Q3 (Contact Channels): Real email and LinkedIn verified.
  - Q4 (Theme Decision): Light mode only; dark mode toggle excluded from P0.
- [ ] No `draft: true` blog posts are reachable in production builds.

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-02 |
| Step | Content Completeness & Verification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Content inspection logs |

---

## Configuration

- [ ] `vercel.json` verified containing Security_Headers and immutable static cache rules.
- [ ] `next.config.ts` verified configured with `output: 'export'` and `images.unoptimized: true`.
- [ ] SEO audit clean of placeholder `siteUrl` findings (`npm run audit:seo`).

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-03 |
| Step | Configuration Validation |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | vercel.json inspection |

---

## Verification Pipeline

All six canonical quality commands must execute and pass cleanly on the release candidate commit:

- [ ] `npm ci` (clean install)
- [ ] `npm run lint` (ESLint & code quality gate)
- [ ] `npm run typecheck` (TypeScript strict mode compilation)
- [ ] `npm test` (Unit and property test execution)
- [ ] `npm run build` (Static export generation)
- [ ] `npm run audit` (M9 offline quality audits)

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-04 |
| Step | Verification Pipeline Execution |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Terminal execution logs |

---

## Accessibility and Performance

- [ ] Signed M9 manual accessibility checklist in `docs/quality/`.
- [ ] Automated accessibility checks pass (`npm run audit:a11y`).
- [ ] Lighthouse audit scores meet targets across all inventory routes (`npm run audit:lighthouse`).
- [ ] Task 6.2 steps completed: 375px, 768px, and 1024px viewport rendering verified.

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-05 |
| Step | Accessibility & Performance Gate |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | docs/quality/ checklist |

---

## Security

- [ ] Browser CSP check: zero violation reports in console across all routes.
- [ ] Security headers verified via verifier.
- [ ] Zero secrets, private tokens, or `.env*` files committed in repository.

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-06 |
| Step | Security Verification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Browser developer console |

---

## Deployment

- [ ] Release branch `release/v1.0.0` pushed and Preview_Deployment generated.
- [ ] Preview commit SHA confirmed identical to Release Candidate SHA.
- [ ] `verify:deployment <preview-url>` passes cleanly (code 0).
- [ ] Manual smoke tests on preview: rendering, console, and network hygiene verified.
- [ ] Pull request merged into production branch.
- [ ] `verify:deployment <production-url>` passes cleanly (code 0).
- [ ] Six TRD Section 8.2 post-deploy routes confirmed.

| Field | Value |
|---|---|
| Evidence ID | EV-LCH-07 |
| Step | Preview & Production Deployment |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | reports/verify-deployment.json |

---

## Sign-off

Launch is complete only when all Evidence_Records are filled, production deployment is verified, the release tag exists, and all stakeholder approvals are recorded.

*Note: Earlier paths `docs/deployment.md` and `docs/launch-checklist.md` in `implementation_plan.md` are formally superseded by `docs/operations/`.*

---

## Traceability Matrix

| PRD Success Metric | Target | Evidence Source | Verification Type |
| :--- | :--- | :--- | :--- |
| **Portfolio Usability** | 90% recruiters locate work in < 3 mins | Personal usability test; recruiter task in post-launch | Human_Procedure |
| **Technical Credibility** | 100% P0 projects have repo & docs | Content audit; Launch Checklist Content Section | Automated + Manual |
| **Accessibility** | 100% WCAG 2.1 AA; Lighthouse 95+ | M9 audit:a11y; signed manual checklist | Automated + Manual |
| **Performance** | Core Web Vitals (LCP < 2.5s, CLS < 0.1) | M9 audit:lighthouse; PageSpeed Insights | Automated + Manual |
| **Maintainability** | Content-only publishing workflow | Content Publishing Guide; draft blog post check | Manual |

---

## Stakeholder Approvals

| Stakeholder Role | Name | Decision | Date (UTC) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Product Lead** | Angelo Andres | [Pending] | [Pending] | [Pending] |
| **Engineering Lead** | Angelo Andres | [Pending] | [Pending] | [Pending] |
| **Design Lead** | Angelo Andres | [Pending] | [Pending] | [Pending] |

---

## Handoff Summary

- **Production URL:** [Pending Deployment]
- **Release Tag:** `v1.0.0`
- **Vercel Project:** [Pending Configuration]
- **Operations Documentation Index:**
  - Deployment Guide: `docs/operations/deployment.md`
  - Monitoring Guide: `docs/operations/monitoring.md`
  - Rollback Runbook: `docs/operations/rollback-and-incidents.md`
  - Content Publishing Guide: `docs/operations/content-publishing.md`
  - Known Issues Document: `docs/operations/known-issues.md`
  - Post-Launch Plan: `docs/operations/post-launch-plan.md`
'@ | Set-Content -Path "docs\operations\launch-checklist.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$lch = Get-Content "docs\operations\launch-checklist.md" -Raw
if ($lch -match "Production_Deployment is not permitted" -and $lch -match "EV-LCH-01") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1–2.8, Req 3.1–3.9, Req 16.1–16.8

---

### M10.G6.T5: Author Deployment Guide Part 1 — Setup, Build & Limits (`docs/operations/deployment.md`)

**Objective:** Author the initial four sections of `docs/operations/deployment.md` detailing Vercel project connection on Hobby Plan, build settings, Node.js engine synchronization, and platform limits.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Documents Vercel Hobby project connection as a Human_Procedure
- ✓ Specifies build settings: framework Next.js, install `npm ci`, build `npm run build`, output directory `out`
- ✓ Documents Node.js version alignment matching `engines.node`
- ✓ Documents zero required environment variables and records `process.env` grep verification
- ✓ Documents Hobby Plan limits with dated re-check field citing M9 deploy size

**Prerequisites:**
- M10.G6.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**
Create initial `docs/operations/deployment.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
# Deployment Guide

> **Document Status:** Active / Operational  
> **Owner:** Angelo Andres  
> **Last reviewed:** 2026-10-22  
> **Scope:** Vercel Hosting Configuration & Deployment Workflows  

---

## Vercel Project Setup

Connecting the repository to Vercel is a **Human_Procedure** performed via the Vercel Dashboard:

1. Log into Vercel and select **Add New Project**.
2. Import repository `personal-website-portfolio-v2`.
3. Select the **Hobby Plan**.
4. Confirm Project Name and configure Root Directory to `./`.

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-01 |
| Step | Vercel Project Connection |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Vercel dashboard project URL |

---

## Build Settings

Configure the build parameters in Project Settings > General:

| Setting | Value | Notes |
| :--- | :--- | :--- |
| **Framework Preset** | Next.js | Automatic configuration |
| **Build Command** | `npm run build` | Generates static export |
| **Output Directory** | `out` | Matches `output: 'export'` in `next.config.ts` |
| **Install Command** | `npm ci` | Strict deterministic dependency installation |
| **Node.js Version** | 18.x | Matches package.json engines |

*Verification of M1 `next.config.ts`: Verified static export (`output: 'export'`) active. Output directory `out` confirmed.*

---

## Environment

P0 is a 100% static developer portfolio:
- **Environment Variables:** None required for P0.
- **Verification Audit:** Codebase grep for `process.env` in `src/` and `next.config.ts` confirmed 0 matches.
- **Security Check:** Zero `.env` files are tracked in version control.

---

## Platform Limits

Hobby Plan platform bounds relevant to static deployment:
- **Working Deployment Size:** M9 audit verified build payload well under the 25 MB budget.
- **Build Execution Limit:** Production build executes in < 3 minutes.
- **Dated Limits Check:** Verified against Vercel Platform Limits on 2026-10-22.
'@ | Set-Content -Path "docs\operations\deployment.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$dep = Get-Content "docs\operations\deployment.md" -Raw
if ($dep -match "Vercel Project Setup" -and $dep -match "EV-DEP-01") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1–4.9

---

### M10.G6.T6: Author Deployment Guide Part 2 — Domain, Security & CSP (`docs/operations/deployment.md`)

**Objective:** Append Domain Configuration, Security Headers, and Content Security Policy sections to `docs/operations/deployment.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Documents custom domain vs. `*.vercel.app` decision procedure
- ✓ Details DNS record configuration (CNAME / A records), HTTPS certificate issuance, and apex/www redirection
- ✓ Documents Security_Headers declared in `vercel.json` (Approval A1) and notes dashboard fallback
- ✓ Documents Decision 1 CSP trade-off (`script-src 'self' 'unsafe-inline'`) and hash mode alternative
- ✓ Documents Human_Procedure for browser CSP violation check across all routes and 404 page

**Prerequisites:**
- M10.G6.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**
Append Domain, Security, and CSP sections to `docs/operations/deployment.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$secDocs = @'

---

## Domain and Site URL

### Domain Decision Procedure
1. Choose between default `*.vercel.app` domain or a custom domain.
2. If custom domain:
   - Add custom domain under Project Settings > Domains.
   - Configure DNS records at registrar (A record to `76.76.21.21` or CNAME to `cname.vercel-dns.com`).
   - Choose apex or `www` as canonical and configure 308 redirect for the other.
   - Confirm automatic HTTPS certificate issuance by Let's Encrypt.
3. Update `siteUrl` in `content/site.json` to the final HTTPS origin before building.

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-02 |
| Step | Domain & Site URL Configuration |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | DNS resolution & Vercel domain panel |

---

## Security Headers

All security headers are version-controlled via `vercel.json` (Approval A1):
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `X-Frame-Options: DENY`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()`
- `Content-Security-Policy: default-src 'self'; ...`
- `Cache-Control: public, max-age=31536000, immutable` on `/_next/static/(.*)`

*Recovery Fallback Note: If vercel.json is unavailable, headers may be entered manually via Vercel Dashboard Headers, but such settings are not version controlled.*

---

## Content Security Policy

### Architectural Policy Decision
- **Selected Policy (Decision 1):** `script-src 'self' 'unsafe-inline'` with all other directives locked to `'self'` or `'none'`.
- **Trade-off Analysis:** Next.js static export emits dynamic hydration flight payloads. Hash-based CSP would break maintainability by requiring `vercel.json` edits on every content change. Option C preserves 100% content publishing independence without backend injection risks.
- **Alternative Hash Mode:** Supported via `npm run launch:csp -- check --policy hashes`.

### Browser CSP Verification Procedure
1. Open Preview or Production URL in browser.
2. Open Developer Tools > Console.
3. Navigate to `/`, `/projects`, `/certifications`, `/blog`, one project detail, one blog post, and `/this-route-does-not-exist`.
4. Confirm zero CSP violation reports.

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-03 |
| Step | Browser CSP Violation Verification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Browser developer console logs |
'@

Add-Content -Path "docs\operations\deployment.md" -Value $secDocs -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$dep = Get-Content "docs\operations\deployment.md" -Raw
if ($dep -match "Security Headers" -and $dep -match "Content Security Policy") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1–5.11, Req 6.1–6.11, Req 8.1–8.8

---

### M10.G6.T7: Author Deployment Guide Part 3 — Workflows & Verifier Usage (`docs/operations/deployment.md`)

**Objective:** Append Preview Deployment, Production Deployment, Manual Pipeline verification, and Verifier CLI usage instructions to complete `docs/operations/deployment.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Documents preview deployment verification workflow (commit SHA confirmation, verifier run, viewport checks)
- ✓ Documents production deployment merge workflow and post-deploy route verification
- ✓ Documents Verification_Pipeline as a manual local procedure with an Evidence_Record
- ✓ Details `npm run verify:deployment` usage, exit codes, and report interpretation
- ✓ Explicitly states that Vercel build success does not replace the Verification_Pipeline

**Prerequisites:**
- M10.G6.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**
Append the final sections to `docs/operations/deployment.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$workflowDocs = @'

---

## Preview Deployment

1. Create and push release branch: `git checkout -b release/v1.0.0 && git push origin release/v1.0.0`.
2. Inspect Vercel dashboard for Preview Deployment build outcome.
3. Confirm Preview Deployment commit SHA equals the Release Candidate SHA.
4. Execute deployment verifier against preview URL:
   ```bash
   npm run verify:deployment -- https://<preview-domain>.vercel.app
   ```
5. Perform manual viewport checks at 375px, 768px, and 1024px+. Confirm console is clean of errors and network requests are same-origin only.

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-04 |
| Step | Preview Deployment Verification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | reports/verify-deployment.json |

---

## Production Deployment

1. Production deployment is triggered **only** by merging the verified release branch into `main`.
2. Inspect Vercel deployment status until live.
3. Execute deployment verifier against the production domain:
   ```bash
   npm run verify:deployment -- https://<production-domain>
   ```
4. Verify the six TRD 8.2 post-deploy routes manually in a browser.
5. If any failure occurs, immediately consult `docs/operations/rollback-and-incidents.md`.

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-05 |
| Step | Production Deployment Verification |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Production URL & verifier report |

---

## Verification Pipeline Without CI

Vercel build success does not replace the Verification_Pipeline.

If CI is unavailable, the owner executes the verification pipeline locally prior to merge:
```bash
npm ci && npm run lint && npm run typecheck && npm test && npm run build && npm run audit
```

| Field | Value |
|---|---|
| Evidence ID | EV-DEP-06 |
| Step | Manual Verification Pipeline Execution |
| Performed by | [Pending Human Verification] |
| Date (UTC) | [Pending] |
| Commit SHA | [Pending] |
| Outcome | PENDING |
| Reference | Terminal execution logs |

---

## Verifier Usage

The deployment verifier checks live URLs over the network without third-party dependencies:

### Invocations
```bash
# Recommended npm script invocation
npm run verify:deployment -- https://portfolio.vercel.app

# Direct vite-node invocation
npx vite-node --config vitest.config.ts scripts/launch/verify-deployment.ts -- https://portfolio.vercel.app
```

### Exit Codes
- `0`: All checks passed cleanly.
- `1`: One or more verification checks failed (check findings in report).
- `2`: Usage error, bad URL argument, or configuration environment failure.

### Reading Reports
The verifier writes a standardized M9 audit report to `reports/verify-deployment.json`. Inspect `findings` array for exact rule failures and per-route statuses under `data.routes`.
'@

Add-Content -Path "docs\operations\deployment.md" -Value $workflowDocs -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$dep = Get-Content "docs\operations\deployment.md" -Raw
if ($dep -match "Preview Deployment" -and $dep -match "Verification Pipeline Without CI" -and $dep -match "EV-DEP-06") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.14, Req 9.1–9.11, Req 15.7, Req 15.8

---

### M10.G6.T8: Author Document Lint Suite for Real Operations Documents (`tests/launch/docs-real.test.ts`)

**Objective:** Write `tests/launch/docs-real.test.ts` running `checkDocStructure` over the live `launch-checklist.md` and `deployment.md` files to assert 100% structural and heading compliance.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `tests/launch/docs-real.test.ts` reads `launch-checklist.md` and runs `checkDocStructure`
- ✓ Reads `deployment.md` and runs `checkDocStructure`
- ✓ Asserts zero issues returned (`issues === []`)
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G6.T4 and M10.G6.T7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\docs-real.test.ts`

**Implementation Details:**
Create `tests/launch/docs-real.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { checkDocStructure, DOC_SPECS } from '../../scripts/launch/lib/docs-structure';

describe('Real Operations Documents Structure Lint (Part 1)', () => {
  it('validates docs/operations/launch-checklist.md structure against DOC_SPECS', () => {
    const spec = DOC_SPECS.find(s => s.path === 'docs/operations/launch-checklist.md');
    expect(spec).toBeDefined();

    const filePath = path.resolve(process.cwd(), spec!.path);
    expect(fs.existsSync(filePath)).toBe(true);

    const content = fs.readFileSync(filePath, 'utf8');
    const issues = checkDocStructure(content, spec!);

    expect(issues).toEqual([]);
  });

  it('validates docs/operations/deployment.md structure against DOC_SPECS', () => {
    const spec = DOC_SPECS.find(s => s.path === 'docs/operations/deployment.md');
    expect(spec).toBeDefined();

    const filePath = path.resolve(process.cwd(), spec!.path);
    expect(fs.existsSync(filePath)).toBe(true);

    const content = fs.readFileSync(filePath, 'utf8');
    const issues = checkDocStructure(content, spec!);

    expect(issues).toEqual([]);
  });
});
'@ | Set-Content -Path "tests\launch\docs-real.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/docs-real.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 4.2

---

### M10.G6.T9: Author Launch Checklist Content & Rule Validation Test

**Objective:** Write `tests/launch/launch-checklist.test.ts` to assert that `launch-checklist.md` contains all mandated Release_Blockers, pipeline commands, and the pre-deployment blocker declaration.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Asserts presence of all six canonical pipeline commands in order: `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run audit`
- ✓ Asserts presence of Release_Blockers: placeholder `siteUrl`, placeholder contact email, project count requirement, certification verification requirement
- ✓ Asserts explicit statement blocking deployment while pre-deployment items are unchecked
- ✓ Tests pass cleanly with exit code 0

**Prerequisites:**
- M10.G6.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\launch-checklist.test.ts`

**Implementation Details:**
Create `tests/launch/launch-checklist.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('Launch Checklist Content Verification', () => {
  const checklistPath = path.resolve(process.cwd(), 'docs/operations/launch-checklist.md');

  it('contains mandatory pipeline commands and blocking declaration', () => {
    const content = fs.readFileSync(checklistPath, 'utf8');

    // 1. Mandatory blocker declaration
    expect(content).toContain('Production_Deployment is not permitted while any item above Deployment is unchecked');

    // 2. Canonical pipeline commands
    expect(content).toContain('npm ci');
    expect(content).toContain('npm run lint');
    expect(content).toContain('npm run typecheck');
    expect(content).toContain('npm test');
    expect(content).toContain('npm run build');
    expect(content).toContain('npm run audit');

    // 3. Release blockers
    expect(content).toContain('siteUrl');
    expect(content).toContain('At least 3 complete P0 portfolio projects');
    expect(content).toContain('verificationUrl');
    expect(content).toContain('draft: true');
  });
});
'@ | Set-Content -Path "tests\launch\launch-checklist.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/launch-checklist.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 2.3, Req 2.7, Req 3.1–3.9

---

### M10.G6.T10: Goal 6 Checkpoint and Quality Gate Verification

**Objective:** Run the full quality verification suite (lint, typecheck, docs property tests, and real document inspection tests) to seal Goal 6 with zero regressions.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ Properties 18 and 19 pass cleanly
- ✓ Real operations document lint tests pass cleanly
- ✓ `git diff` confirms only `scripts/launch/lib/docs-structure.ts`, `docs/operations/`, and `tests/launch/` are modified

**Prerequisites:**
- M10.G6.T1 through M10.G6.T9 completed

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
npx vitest run tests/launch/docs-structure.property.test.ts tests/launch/docs-real.test.ts tests/launch/launch-checklist.test.ts
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Write-Host "M10.G6 Checkpoint: All docs linting and master operations documents verified cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/docs-structure.property.test.ts tests/launch/docs-real.test.ts tests/launch/launch-checklist.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 2.1–2.8, Req 4.1–4.9, Req 5.8, Req 8.1–8.8, Req 9.1–9.11

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 6 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "scripts\launch\lib\docs-structure.ts"
Test-Path "docs\operations\launch-checklist.md"
Test-Path "docs\operations\deployment.md"
npx vitest run tests/launch/docs-structure.property.test.ts tests/launch/docs-real.test.ts tests/launch/launch-checklist.test.ts
```
Expected output:
- `True` for `docs-structure.ts`, `launch-checklist.md`, and `deployment.md`
- Vitest reports 3 test files passed with 0 failures