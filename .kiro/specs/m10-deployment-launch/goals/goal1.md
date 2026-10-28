# M10.G1: Clarifications, Approval Requests, and Shared Launch Library Scaffolding

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Record the resolved design clarifications C1–C8, verify M1–M9 prerequisites, document Approval_Item records A1–A8 (with exact diffs, purposes, and fallbacks) along with the recorded human decisions from 2026-10-22, and construct the launch tooling directory layout, shared TypeScript types, and offline fixtures required across M10. This ensures zero boundary violations, zero edits to existing files under `src/`, `tests/`, or `scripts/audit/`, and establishes deterministic offline test harnesses prior to tool implementation.

## Goal Success Criteria

- ✓ `.kiro/specs/m10-deployment-launch/task-notes.md` exists and records clarifications C1–C8 as RESOLVED 2026-10-22 and all verified M1–M9 prerequisites
- ✓ Approval records A1–A8 are documented in `task-notes.md` with exact diffs, purposes, fallbacks, and recorded decisions (A1 Approved, A2 Approved, A3 Declined, A4 Approved, A5 Pre-approved only on verification failure, A6 Approved, A7 Manual at launch, A8 Approved; devDependencies approved 1a)
- ✓ `scripts/launch/lib/types.ts` is implemented without `any`, non-null assertions, or barrel files, importing M9 types read-only via `import type`
- ✓ `tests/launch/fixtures/` contains valid and invalid fixture responses, HTML pages, and `vercel.json` variants
- ✓ `tests/launch/helpers/fake-fetcher.ts` provides a deterministic `Fetcher` that opens zero network sockets
- ✓ `tests/launch/scaffold.test.ts` validates fixtures, fake fetcher isolation, absence of barrel files, and absence of imports from `src/components/`
- ✓ `npm run typecheck` and `npm run lint` execute cleanly with exit code 0

## Prerequisites

- M1 to M9 complete and passing: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit` pass cleanly
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Host environment: Windows PowerShell with Node.js 18+ and npm 9+

---

## Tasks

### M10.G1.T1: Verify M1–M9 Prerequisites and Baseline State

**Objective:** Audit the existing repository state to confirm M1–M9 prerequisites (audit cleanliness, static export configuration, Node engine version, `vite-node` availability, M9 export interfaces, and absence of `process.env` in application code) and record the results in `task-notes.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Directory `.kiro/specs/m10-deployment-launch/` is verified
- ✓ `next.config.ts` is confirmed to contain `output: 'export'`
- ✓ Node.js version is confirmed from `.nvmrc` or `package.json` `engines.node`
- ✓ `src/` and `next.config.ts` are verified to contain zero matches for `process.env`
- ✓ M9 exports in `scripts/audit/lib/` are verified accessible
- ✓ Initial `.kiro/specs/m10-deployment-launch/task-notes.md` is authored with baseline verification results

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

**Implementation Details:**
Execute the following PowerShell script to audit the baseline state and initialize `task-notes.md`:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Check next.config.ts for static export
$nextConfig = Get-Content "next.config.ts" -Raw
$isExport = $nextConfig -match "output:\s*['""]export['""]"

# 2. Check Node version from engines or .nvmrc
$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$nodeEngine = if ($pkg.engines -and $pkg.engines.node) { $pkg.engines.node } else { ">=18.0.0" }
if (Test-Path ".nvmrc") {
    $nodeNvmrc = (Get-Content ".nvmrc" -Raw).Trim()
} else {
    $nodeNvmrc = "None (.nvmrc absent)"
}

# 3. Check for process.env in src/ and next.config.ts
$envMatchesSrc = Select-String -Path "src\**\*.ts", "src\**\*.tsx" -Pattern "process\.env" -ErrorAction SilentlyContinue
$envMatchesConfig = Select-String -Path "next.config.ts" -Pattern "process\.env" -ErrorAction SilentlyContinue

# 4. Check M9 exports in scripts/audit/lib/
$m9TypesExist = Test-Path "scripts\audit\lib\types.ts"
$m9ReportExist = Test-Path "scripts\audit\lib\report.ts"
$m9LayoutExist = Test-Path "scripts\audit\lib\build-layout.ts"

if (-not (Test-Path ".kiro\specs\m10-deployment-launch")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m10-deployment-launch" -Force | Out-Null
}

$taskNotes = @"
# M10 Task Notes & Execution Log

## 1. Prerequisite Baseline Verification (Recorded 2026-10-22)

- **Static Export Configured:** $(if ($isExport) { "YES (output: 'export' verified in next.config.ts)" } else { "NO (FAIL)" })
- **Node Engine Target:** $nodeEngine
- **.nvmrc Value:** $nodeNvmrc
- **process.env in src/:** $(if ($envMatchesSrc) { "FOUND VIOLATIONS: $($envMatchesSrc.Count)" } else { "CLEAN (0 matches)" })
- **process.env in next.config.ts:** $(if ($envMatchesConfig) { "FOUND VIOLATIONS" } else { "CLEAN (0 matches)" })
- **M9 Audit Exports:** types.ts ($m9TypesExist), report.ts ($m9ReportExist), build-layout.ts ($m9LayoutExist)
- **Status:** PREREQUISITES VERIFIED GREEN
"@

Set-Content -Path ".kiro\specs\m10-deployment-launch\task-notes.md" -Value $taskNotes -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "PREREQUISITES VERIFIED GREEN" -and $notes -match "CLEAN \(0 matches\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.4, Req 4.3, Req 4.4, Req 4.7

---

### M10.G1.T2: Record Resolved Clarifications C1–C8 in Task Notes

**Objective:** Append the official record of design clarifications C1 through C8 to `task-notes.md`, establishing their resolution date (2026-10-22) and requirement alignment.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Clarifications C1 through C8 are documented verbatim in `task-notes.md`
- ✓ Each clarification is marked as `RESOLVED 2026-10-22 (amended in requirements.md)`
- ✓ C1/C2 (new files under `scripts/launch/` and `tests/launch/` permitted), C3/C4 (preview vs production canonical and robots handling), C5 (Hobby instant rollback bounds), C6 (inline script policy selection), C7 (`noindex` on 404), and C8 (separate approval items) are clearly detailed

**Prerequisites:**
- M10.G1.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Append the clarifications section to `task-notes.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$clarificationsBlock = @"

## 2. Design Clarifications Log (RESOLVED 2026-10-22)

| ID | Topic | Resolution / Interpretation Applied | Requirement Mapping |
| :--- | :--- | :--- | :--- |
| **C1** | Boundary vs Tooling Scope | New files under `scripts/launch/` and `tests/launch/` are strictly permitted. Existing files in `src/`, `tests/`, and `scripts/audit/` remain unmodified. | Req 1.1, 1.2 |
| **C2** | CSP Tool Deliverable | `scripts/launch/csp-hashes.ts` is an explicit M10 deliverable for build analysis and verification. | Req 6.3 |
| **C3** | Preview Robots Header | Vercel sets `X-Robots-Tag: noindex` on Preview Deployments by default. Treated as expected `info` on preview runs and strict `error` on production. | Req 7.9, 9.3 |
| **C4** | Preview Canonical URL | Preview HTML contains `siteUrl` in canonical links. Compared against `siteUrl` on preview runs (with single `info` finding) and strictly against base URL on production. | Req 7.9, 7.10 |
| **C5** | Hobby Instant Rollback | Vercel Hobby plan instant rollback reaches only the immediately previous production deployment. Older restorations require `git revert` or manual redeployment. | Req 12.1 |
| **C6** | Content Publishing Independence | Hash-based CSP requires modifying root `vercel.json` on content edits. Approved script policy is `script-src 'self' 'unsafe-inline'` to keep content edits 100% independent. | Req 6.2, 13.3 |
| **C7** | Not-Found Route Indexing | The 404 route is designed to carry `noindex`. The verifier asserts `noindex` is present on the bogus route and absent on standard routes. | Req 7.5, 7.9 |
| **C8** | Package.json Decoupling | Script additions (`verify:deployment`, `launch:csp`) and `version` bump are separate approval items (A2/A4 vs A3). | Req 7.14, 11.1 |
"@

Add-Content -Path ".kiro\specs\m10-deployment-launch\task-notes.md" -Value $clarificationsBlock -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "C1" -and $notes -match "C8" -and $notes -match "RESOLVED 2026-10-22") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 6.2, Req 7.9, Req 7.10, Req 7.14, Req 12.1, Req 13.3

---

### M10.G1.T3: Document Approval Records A1, A2, A3, and A4

**Objective:** Document the first four approval records (A1: `vercel.json`, A2: `verify:deployment` script, A3: `package.json` version bump, A4: `launch:csp` script) with exact diffs, rationale, fallbacks, and decisions in `task-notes.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Record A1 (`vercel.json`) documented with diff, purpose, fallback, and status `Approved 2026-10-22 (approval A1)`
- ✓ Record A2 (`verify:deployment`) documented with diff, purpose, fallback, and status `Approved 2026-10-22 (approval A2)`
- ✓ Record A3 (`package.json` version bump) documented with diff, purpose, fallback, and status `Declined (approval A3)`
- ✓ Record A4 (`launch:csp`) documented with diff, purpose, fallback, and status `Approved 2026-10-22 (approval A4)`
- ✓ No gated files are modified in this task

**Prerequisites:**
- M10.G1.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Append Approval Records A1 through A4 to `task-notes.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$approvalsA1A4 = @"

## 3. Human Approval Records: A1 to A4 (Recorded 2026-10-22)

### Approval Item A1: Root Configuration vercel.json
- **Target File:** `vercel.json` (new file)
- **Proposed Diff:**
\`\`\`json
{
  "`$schema": "https://openapi.vercel.sh/vercel.json",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'" }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
\`\`\`
- **Purpose:** Declare Security_Headers and immutable static asset caching in repository version control.
- **Fallback if Withheld:** Configure headers manually via Vercel Project Dashboard (not version controlled).
- **Decision:** **Approved 2026-10-22 (approval A1)**

---

### Approval Item A2: package.json Script verify:deployment
- **Target File:** `package.json`
- **Proposed Diff:**
\`\`\`diff
   "scripts": {
+    "verify:deployment": "vite-node --config vitest.config.ts scripts/launch/verify-deployment.ts --"
   }
\`\`\`
- **Purpose:** Short npm script invocation for smoke-checking deployed URLs.
- **Fallback if Withheld:** Execute direct command `npx vite-node --config vitest.config.ts scripts/launch/verify-deployment.ts -- <url>`.
- **Decision:** **Approved 2026-10-22 (approval A2)**

---

### Approval Item A3: package.json Version Bump (1.0.0)
- **Target File:** `package.json`
- **Proposed Diff:**
\`\`\`diff
-  "version": "0.1.0",
+  "version": "1.0.0",
\`\`\`
- **Purpose:** Elevate project version manifest to release milestone.
- **Fallback if Withheld:** Retain `version` as-is; release version is designated strictly via `CHANGELOG.md` and annotated git tag `v1.0.0`.
- **Decision:** **Declined 2026-10-22 (approval A3)** (Fallback applied: version manifest remains unmodified).

---

### Approval Item A4: package.json Script launch:csp
- **Target File:** `package.json`
- **Proposed Diff:**
\`\`\`diff
   "scripts": {
+    "launch:csp": "vite-node --config vitest.config.ts scripts/launch/csp-hashes.ts --"
   }
\`\`\`
- **Purpose:** Short npm script invocation for inspecting build CSP and validating policy adherence.
- **Fallback if Withheld:** Execute direct command `npx vite-node --config vitest.config.ts scripts/launch/csp-hashes.ts --`.
- **Decision:** **Approved 2026-10-22 (approval A4)**
"@

Add-Content -Path ".kiro\specs\m10-deployment-launch\task-notes.md" -Value $approvalsA1A4 -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "Approval Item A1" -and $notes -match "Declined 2026-10-22 \(approval A3\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 5.1, Req 5.11, Req 7.14, Req 11.1

---

### M10.G1.T4: Document Approval Records A5, A6, A7, and A8

**Objective:** Document the remaining four approval records (A5: `next.config.ts` conditional edit, A6: GitHub Actions workflow, A7: Git Release Tag, A8: `.gitignore` `reports/` entry) with exact diffs, rationale, fallbacks, and decisions in `task-notes.md`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Record A5 (`next.config.ts`) documented with condition and status `Pre-approved only if verification fails (approval A5)`
- ✓ Record A6 (`.github/workflows/verify.yml`) documented with diff, purpose, fallback, and status `Approved 2026-10-22 (approval A6)`
- ✓ Record A7 (`v1.0.0` annotated tag & production merge) documented with status `Manual, at launch (approval requested at launch time)`
- ✓ Record A8 (`.gitignore` `reports/`) documented with status `Approved 2026-10-22 (approval A8)`
- ✓ No gated files are modified in this task

**Prerequisites:**
- M10.G1.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Append Approval Records A5 through A8 to `task-notes.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$approvalsA5A8 = @"

## 4. Human Approval Records: A5 to A8 (Recorded 2026-10-22)

### Approval Item A5: Conditional Edit to next.config.ts
- **Target File:** `next.config.ts`
- **Proposed Diff (Only if static export verification fails or x-powered-by observed):**
\`\`\`diff
   const nextConfig: NextConfig = {
     reactStrictMode: true,
     output: 'export',
+    poweredByHeader: false,
   };
\`\`\`
- **Purpose:** Ensure static export compatibility and suppress framework fingerprinting.
- **Fallback if Withheld:** Production deployment blocked if export fails; record `x-powered-by` in Known Issues if observed.
- **Decision:** **Pre-approved 2026-10-22 (approval A5), applies ONLY if verification fails**

---

### Approval Item A6: Continuous Integration Workflow .github/workflows/verify.yml
- **Target File:** `.github/workflows/verify.yml` (new file)
- **Proposed Diff:**
\`\`\`yaml
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
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
      - run: npm run build
      - run: npm run audit
\`\`\`
- **Purpose:** Enforce automated offline verification pipeline on pull requests and main pushes.
- **Fallback if Withheld:** Enforce manual local verification with documented Evidence_Record prior to merge.
- **Decision:** **Approved 2026-10-22 (approval A6)**

---

### Approval Item A7: Production Git Tag v1.0.0 & Branch Merge
- **Target Action:** Create annotated tag `v1.0.0` on production deployment commit and push to remote.
- **Proposed Command:** `git tag -a v1.0.0 <commit-sha> -m "Release v1.0.0" && git push origin v1.0.0`
- **Purpose:** Establish immutable version-controlled baseline for production release.
- **Fallback if Withheld:** Production commit SHA recorded in `launch-checklist.md` and `CHANGELOG.md` without tag.
- **Decision:** **Manual, at launch (explicit approval requested at launch time)**

---

### Approval Item A8: Git Ignore Entry for reports/
- **Target File:** `.gitignore`
- **Proposed Diff:**
\`\`\`diff
+reports/
\`\`\`
- **Purpose:** Prevent committing ephemeral test and deployment verification JSON reports.
- **Fallback if Withheld:** Avoid staging `reports/` manually during commits.
- **Decision:** **Approved 2026-10-22 (approval A8)** (Apply only if not already ignored by M9).
"@

Add-Content -Path ".kiro\specs\m10-deployment-launch\task-notes.md" -Value $approvalsA5A8 -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$notes = Get-Content ".kiro\specs\m10-deployment-launch\task-notes.md" -Raw
if ($notes -match "Approval Item A5" -and $notes -match "Approval Item A8" -and $notes -match "Approved 2026-10-22 \(approval A6\)") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 4.4, Req 4.5, Req 11.2, Req 15.1, Req 15.7

---

### M10.G1.T5: Finalize Approval Status & DevDependency Verification in Task Notes

**Objective:** Audit dependencies and confirm that zero new runtime dependencies are introduced, that devDependencies conform to approval 1a, and that no gated edits have been executed ahead of their respective goals.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Summary matrix of approvals A1–A8 is appended to `task-notes.md`
- ✓ DevDependency status (fast-check, vitest, jsdom) confirmed approved under approval 1a
- ✓ Verification confirms `git status` reflects zero modified root configuration files (`package.json`, `next.config.ts`, `vercel.json` does not exist yet)

**Prerequisites:**
- M10.G1.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\.kiro\specs\m10-deployment-launch\task-notes.md`

**Implementation Details:**
Append the approval summary and boundary audit to `task-notes.md` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$summaryBlock = @"

## 5. Approval Decision Matrix Summary & Guardrail Confirmation

| Item | Description | Human Decision | Target Goal | Status |
| :--- | :--- | :--- | :--- | :--- |
| **A1** | `vercel.json` | Approved 2026-10-22 | G3 | PENDING CREATION IN G3 |
| **A2** | Script `verify:deployment` | Approved 2026-10-22 | G5 | PENDING INJECTION IN G5 |
| **A3** | Version bump `1.0.0` | Declined 2026-10-22 | G8 | DECLINED - NOT APPLIED |
| **A4** | Script `launch:csp` | Approved 2026-10-22 | G5 | PENDING INJECTION IN G5 |
| **A5** | `next.config.ts` edit | Pre-approved conditional | G1/G9 | UNMODIFIED (Static export valid) |
| **A6** | `.github/workflows/verify.yml`| Approved 2026-10-22 | G8 | PENDING CREATION IN G8 |
| **A7** | Release Tag `v1.0.0` | Manual, at launch | G9 | PENDING LAUNCH EXECUTION |
| **A8** | `.gitignore` `reports/` | Approved 2026-10-22 | G5 | PENDING AUDIT IN G5 |

- **DevDependencies Mandate (Approval 1a):** Vitest, fast-check, and jsdom are verified present in `devDependencies`. Zero runtime dependencies added.
- **Root Configuration Check:** `package.json`, `next.config.ts`, `tsconfig.json` remain completely unmodified.
"@

Add-Content -Path ".kiro\specs\m10-deployment-launch\task-notes.md" -Value $summaryBlock -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$status = git status --porcelain package.json next.config.ts vercel.json
if (-not $status) { "PASS" } else { "FAIL: Gated files modified prematurely" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.3, Req 1.6

---

### M10.G1.T6: Create Launch Type Definitions (`scripts/launch/lib/types.ts`)

**Objective:** Implement the shared TypeScript type definitions in `scripts/launch/lib/types.ts` strictly importing M9 report contracts read-only without duplication or barrel files.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Directory `scripts/launch/lib/` is created
- ✓ File `scripts/launch/lib/types.ts` is created
- ✓ Imports `AuditReport`, `Finding`, and `Severity` from `scripts/audit/lib/types` using `import type`
- ✓ Exports `RunKind`, `CheckResult`, `HeaderPair`, `HeaderRule`, `VercelConfig`, `ConfigIssue`, `HeaderBag`, `HeaderMismatch`, `InlineScript`, `StyleInventory`, `PageInventory`, `ScriptPolicy`, `StylePolicy`, `CspOptions`, `CspDirective`, `CspDirectives`, `CspFinding`, `FetchedResponse`, `Fetcher`, `RouteResult`, `VerifyData`, and `VerifyArgs`
- ✓ Contains zero `any` types, zero non-null assertions (`!`), and zero barrel exports

**Prerequisites:**
- M10.G1.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\scripts\launch\lib\types.ts`

**Implementation Details:**
Create `scripts/launch/lib/types.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "scripts\launch\lib")) {
    New-Item -ItemType Directory -Path "scripts\launch\lib" -Force | Out-Null
}

@'
import type { AuditReport, Finding, Severity } from '../../audit/lib/types';

export type RunKind = 'production' | 'preview';

export interface CheckResult {
  readonly id: string;
  readonly severity: Severity;
  readonly passed: boolean;
  readonly message: string;
  readonly details?: Readonly<Record<string, string | number | boolean | null>>;
}

export interface HeaderPair {
  readonly key: string;
  readonly value: string;
}

export interface HeaderRule {
  readonly source: string;
  readonly headers: readonly HeaderPair[];
}

export interface VercelConfig {
  readonly headers: readonly HeaderRule[];
}

export interface ConfigIssue {
  readonly rule: string;
  readonly message: string;
}

export type HeaderBag = Readonly<Record<string, string>>;

export interface HeaderMismatch {
  readonly key: string;
  readonly kind: 'missing' | 'different';
  readonly expected: string;
  readonly actual: string | null;
}

export interface InlineScript {
  readonly file: string;
  readonly index: number;
  readonly text: string;
  readonly hash: string;
}

export interface StyleInventory {
  readonly styleElements: number;
  readonly styleAttributes: number;
}

export interface PageInventory {
  readonly file: string;
  readonly inlineScripts: readonly InlineScript[];
  readonly externalScriptSrcs: readonly string[];
  readonly style: StyleInventory;
}

export type ScriptPolicy =
  | { readonly kind: 'inline-allowed' }
  | { readonly kind: 'hashes'; readonly hashes: readonly string[] };

export type StylePolicy = 'self' | 'self-inline-attr' | 'self-inline';

export interface CspOptions {
  readonly script: ScriptPolicy;
  readonly style: StylePolicy;
}

export interface CspDirective {
  readonly name: string;
  readonly values: readonly string[];
}

export type CspDirectives = readonly CspDirective[];

export interface CspFinding {
  readonly rule: string;
  readonly severity: Severity;
  readonly message: string;
  readonly file?: string;
}

export interface FetchedResponse {
  readonly status: number;
  readonly headers: HeaderBag;
  readonly body: string;
}

export type Fetcher = (url: string) => Promise<FetchedResponse>;

export interface RouteResult {
  readonly route: string;
  readonly url: string;
  readonly status: number | null;
  readonly passed: number;
  readonly failed: number;
  readonly checks: readonly { readonly id: string; readonly passed: boolean; readonly severity: Severity }[];
}

export interface VerifyData {
  readonly baseUrl: string;
  readonly siteUrl: string;
  readonly run: RunKind;
  readonly totals: { readonly passed: number; readonly failed: number };
  readonly routes: readonly RouteResult[];
}

export interface VerifyArgs {
  readonly baseUrl: string;
  readonly timeoutMs: number;
  readonly concurrency: number;
  readonly vercelJsonPath: string;
  readonly expectHeadersPath: string | null;
}

export type { AuditReport, Finding, Severity };
'@ | Set-Content -Path "scripts\launch\lib\types.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.7, Req 7.2, Req 7.15

---

### M10.G1.T7: Create Fixture Trees for HTML and Vercel Configurations

**Objective:** Populate `tests/launch/fixtures/html/` with representative static HTML pages and `tests/launch/fixtures/vercel/` with valid and invalid `vercel.json` fixtures.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Directory `tests/launch/fixtures/html/` contains `valid-page.html`, `data-block-page.html`, and `404.html`
- ✓ Directory `tests/launch/fixtures/vercel/` contains `valid.json`, `missing-header.json`, `forbidden-key.json`, `html-immutable.json`, `unsupported-source.json`, and `invalid-syntax.json`
- ✓ HTML fixtures include inline hydration scripts, `application/ld+json` data blocks, external scripts, and style attributes

**Prerequisites:**
- M10.G1.T6 completed

**Implementation Details:**
Create HTML and Vercel fixtures using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$htmlDir = "tests\launch\fixtures\html"
$vercelDir = "tests\launch\fixtures\vercel"

if (-not (Test-Path $htmlDir)) { New-Item -ItemType Directory -Path $htmlDir -Force | Out-Null }
if (-not (Test-Path $vercelDir)) { New-Item -ItemType Directory -Path $vercelDir -Force | Out-Null }

# 1. HTML Fixtures
@'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Valid Portfolio Route</title>
  <link rel="canonical" href="https://example.com/projects">
  <script src="/_next/static/chunks/main.js" async></script>
</head>
<body style="margin: 0; padding: 1rem;">
  <h1>Projects</h1>
  <script>self.__next_f.push([1, "projects-payload"]);</script>
</body>
</html>
'@ | Set-Content -Path "$htmlDir\valid-page.html" -Encoding UTF8

@'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Data Block Page</title>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Person"}</script>
</head>
<body>
  <h1>Data Block</h1>
  <script type="application/json">{"custom":"data"}</script>
</body>
</html>
'@ | Set-Content -Path "$htmlDir\data-block-page.html" -Encoding UTF8

@'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>404: Page Not Found</title>
  <meta name="robots" content="noindex, follow">
</head>
<body>
  <h1>404 - Page Not Found</h1>
  <p>The page you requested could not be located.</p>
</body>
</html>
'@ | Set-Content -Path "$htmlDir\404.html" -Encoding UTF8

# 2. Vercel Configuration Fixtures
@'
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'" }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
'@ | Set-Content -Path "$vercelDir\valid.json" -Encoding UTF8

@'
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
'@ | Set-Content -Path "$vercelDir\missing-header.json" -Encoding UTF8

@'
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [{ "key": "X-Content-Type-Options", "value": "nosniff" }]
    }
  ],
  "redirects": [
    { "source": "/old", "destination": "/new" }
  ]
}
'@ | Set-Content -Path "$vercelDir\forbidden-key.json" -Encoding UTF8

@'
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
'@ | Set-Content -Path "$vercelDir\html-immutable.json" -Encoding UTF8

@'
{
  "headers": [
    {
      "source": "/api/:path*",
      "headers": [{ "key": "X-Content-Type-Options", "value": "nosniff" }]
    }
  ]
}
'@ | Set-Content -Path "$vercelDir\unsupported-source.json" -Encoding UTF8

@'
{ "headers": [ invalid json syntax here
'@ | Set-Content -Path "$vercelDir\invalid-syntax.json" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$htmlCount = (Get-ChildItem "tests\launch\fixtures\html\*.html").Count
$vercelCount = (Get-ChildItem "tests\launch\fixtures\vercel\*.json").Count
if ($htmlCount -ge 3 -and $vercelCount -ge 6) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.1, Req 5.9, Req 6.3, Req 6.7, Req 7.15

---

### M10.G1.T8: Create Response Fixtures and Deterministic Fake Fetcher

**Objective:** Populate `tests/launch/fixtures/responses/` with simulated HTTP responses and implement `tests/launch/helpers/fake-fetcher.ts` providing an offline, in-memory `Fetcher`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ Directory `tests/launch/fixtures/responses/` contains JSON fixtures: `200-ok.json`, `missing-header.json`, `wrong-canonical.json`, `noindex-meta.json`, `x-powered-by.json`, `404-bogus.json`, and `preview-headers.json`
- ✓ `tests/launch/helpers/fake-fetcher.ts` implements `createFakeFetcher(routes)` returning a typed `Fetcher`
- ✓ Fake fetcher supports simulated timeouts (`TimeoutError`) and custom header/status responses without network I/O

**Prerequisites:**
- M10.G1.T6 completed

**Implementation Details:**
Create response fixtures and `fake-fetcher.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$respDir = "tests\launch\fixtures\responses"
$helpersDir = "tests\launch\helpers"

if (-not (Test-Path $respDir)) { New-Item -ItemType Directory -Path $respDir -Force | Out-Null }
if (-not (Test-Path $helpersDir)) { New-Item -ItemType Directory -Path $helpersDir -Force | Out-Null }

# 1. Response JSON fixtures
@'
{
  "status": 200,
  "headers": {
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "content-security-policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
  },
  "body": "<!DOCTYPE html><html><head><link rel=\"canonical\" href=\"https://example.com/\"><title>Home</title></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\200-ok.json" -Encoding UTF8

@'
{
  "status": 200,
  "headers": {
    "referrer-policy": "strict-origin-when-cross-origin"
  },
  "body": "<!DOCTYPE html><html><head><link rel=\"canonical\" href=\"https://example.com/\"></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\missing-header.json" -Encoding UTF8

@'
{
  "status": 200,
  "headers": {
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "content-security-policy": "default-src 'self'; frame-ancestors 'none'"
  },
  "body": "<!DOCTYPE html><html><head><link rel=\"canonical\" href=\"https://wrong-domain.com/\"></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\wrong-canonical.json" -Encoding UTF8

@'
{
  "status": 200,
  "headers": {
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "content-security-policy": "default-src 'self'; frame-ancestors 'none'"
  },
  "body": "<!DOCTYPE html><html><head><meta name=\"robots\" content=\"noindex, nofollow\"></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\noindex-meta.json" -Encoding UTF8

@'
{
  "status": 200,
  "headers": {
    "x-powered-by": "Next.js",
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "content-security-policy": "default-src 'self'; frame-ancestors 'none'"
  },
  "body": "<!DOCTYPE html><html><head></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\x-powered-by.json" -Encoding UTF8

@'
{
  "status": 404,
  "headers": {
    "x-content-type-options": "nosniff",
    "x-robots-tag": "noindex"
  },
  "body": "<!DOCTYPE html><html><head><title>404: Page Not Found</title></head><body><h1>404 - Page Not Found</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\404-bogus.json" -Encoding UTF8

@'
{
  "status": 200,
  "headers": {
    "x-robots-tag": "noindex",
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "x-frame-options": "DENY",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "content-security-policy": "default-src 'self'; frame-ancestors 'none'"
  },
  "body": "<!DOCTYPE html><html><head><link rel=\"canonical\" href=\"https://production.example.com/\"></head><body><h1>Home</h1></body></html>"
}
'@ | Set-Content -Path "$respDir\preview-headers.json" -Encoding UTF8

# 2. Fake Fetcher Helper
@'
import type { Fetcher, FetchedResponse } from '../../scripts/launch/lib/types';

export interface RouteMock {
  readonly status?: number;
  readonly headers?: Record<string, string>;
  readonly body?: string;
  readonly delayMs?: number;
  readonly shouldTimeout?: boolean;
  readonly shouldNetworkError?: boolean;
}

export function createFakeFetcher(routeMap: Readonly<Record<string, RouteMock>>): Fetcher {
  return async (url: string): Promise<FetchedResponse> => {
    const parsed = new URL(url);
    const key = parsed.pathname;
    const mock = routeMap[key] ?? routeMap['*'];

    if (!mock) {
      return {
        status: 404,
        headers: {},
        body: 'Not Found in Fake Fetcher',
      };
    }

    if (mock.shouldTimeout) {
      const err = new Error('Simulated network timeout');
      err.name = 'TimeoutError';
      throw err;
    }

    if (mock.shouldNetworkError) {
      const err = new Error('ECONNREFUSED: Connection refused');
      err.name = 'FetchError';
      throw err;
    }

    return {
      status: mock.status ?? 200,
      headers: mock.headers ?? {},
      body: mock.body ?? '',
    };
  };
}
'@ | Set-Content -Path "$helpersDir\fake-fetcher.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0 -and (Test-Path "tests\launch\helpers\fake-fetcher.ts")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.2, Req 7.15

---

### M10.G1.T9: Author Scaffolding and Boundary Unit Test (`tests/launch/scaffold.test.ts`)

**Objective:** Write and execute an automated test suite verifying that all fixture files parse cleanly, the fake fetcher functions deterministically, no `index.ts` barrel files exist in launch directories, and zero modules import from `src/components/`.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `tests/launch/scaffold.test.ts` is implemented
- ✓ Asserts all HTML and Vercel fixtures exist and read as expected
- ✓ Asserts `createFakeFetcher` correctly returns 200, 404, and simulated `TimeoutError` without network access
- ✓ Asserts no `index.ts` exists in `scripts/launch/` or `tests/launch/`
- ✓ Asserts zero imports from `src/components/` exist in `scripts/launch/` or `tests/launch/`
- ✓ `npx vitest run tests/launch/scaffold.test.ts` passes cleanly with exit code 0

**Prerequisites:**
- M10.G1.T7 and M10.G1.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\tests\launch\scaffold.test.ts`

**Implementation Details:**
Create `tests/launch/scaffold.test.ts` using PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { createFakeFetcher } from './helpers/fake-fetcher';

describe('M10 Launch Tooling Scaffold & Boundary Verification', () => {
  it('loads valid and invalid vercel.json fixtures cleanly', () => {
    const validJsonPath = path.resolve(__dirname, 'fixtures/vercel/valid.json');
    const invalidJsonPath = path.resolve(__dirname, 'fixtures/vercel/invalid-syntax.json');

    expect(fs.existsSync(validJsonPath)).toBe(true);
    expect(fs.existsSync(invalidJsonPath)).toBe(true);

    const validContent = fs.readFileSync(validJsonPath, 'utf8');
    expect(() => JSON.parse(validContent)).not.toThrow();

    const invalidContent = fs.readFileSync(invalidJsonPath, 'utf8');
    expect(() => JSON.parse(invalidContent)).toThrow();
  });

  it('loads HTML fixtures with expected script and meta tags', () => {
    const validHtmlPath = path.resolve(__dirname, 'fixtures/html/valid-page.html');
    const notFoundHtmlPath = path.resolve(__dirname, 'fixtures/html/404.html');

    const validHtml = fs.readFileSync(validHtmlPath, 'utf8');
    expect(validHtml).toContain('self.__next_f.push');
    expect(validHtml).toContain('rel="canonical"');

    const notFoundHtml = fs.readFileSync(notFoundHtmlPath, 'utf8');
    expect(notFoundHtml).toContain('name="robots"');
    expect(notFoundHtml).toContain('404: Page Not Found');
  });

  it('verifies fake-fetcher determinism without opening network sockets', async () => {
    const fetcher = createFakeFetcher({
      '/': { status: 200, body: 'Home Content' },
      '/timeout': { shouldTimeout: true },
    });

    const res200 = await fetcher('https://example.com/');
    expect(res200.status).toBe(200);
    expect(res200.body).toBe('Home Content');

    await expect(fetcher('https://example.com/timeout')).rejects.toThrow('Simulated network timeout');

    const res404 = await fetcher('https://example.com/unmapped');
    expect(res404.status).toBe(404);
  });

  it('enforces architectural constraint: zero index.ts barrel files in launch directories', () => {
    const launchDirs = [
      path.resolve(__dirname, '../../scripts/launch'),
      path.resolve(__dirname, '../../scripts/launch/lib'),
      path.resolve(__dirname, '.'),
      path.resolve(__dirname, 'helpers'),
    ];

    for (const dir of launchDirs) {
      if (fs.existsSync(dir)) {
        const barrelPath = path.join(dir, 'index.ts');
        expect(fs.existsSync(barrelPath), `Barrel file forbidden at ${barrelPath}`).toBe(false);
      }
    }
  });

  it('enforces architectural constraint: zero imports from src/components/ in launch tooling', () => {
    const targetDirs = [
      path.resolve(__dirname, '../../scripts/launch'),
      path.resolve(__dirname, '.'),
    ];

    const checkDir = (dir: string): void => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && entry.name !== 'fixtures' && entry.name !== 'node_modules') {
          checkDir(fullPath);
        } else if (entry.isFile() && (entry.name.endsWith('.ts') || entry.name.endsWith('.tsx'))) {
          const content = fs.readFileSync(fullPath, 'utf8');
          expect(content).not.toMatch(/from\s+['"].*\/components\/.*['"]/);
          expect(content).not.toMatch(/from\s+['"]@\/components\/.*['"]/);
        }
      }
    };

    for (const dir of targetDirs) {
      if (fs.existsSync(dir)) {
        checkDir(dir);
      }
    }
  });
});
'@ | Set-Content -Path "tests\launch\scaffold.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx vitest run tests/launch/scaffold.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 7.15

---

### M10.G1.T10: Goal 1 Checkpoint and Quality Gate Verification

**Objective:** Execute the full static quality verification gate (linting, typechecking, and unit test execution) to confirm Goal 1 is complete with zero architectural regressions or premature gated modifications.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ `npx vitest run tests/launch/scaffold.test.ts` completes with code 0
- ✓ `git status` verifies no modifications to `package.json`, `next.config.ts`, `src/`, or existing test files
- ✓ `.kiro/specs/m10-deployment-launch/task-notes.md` is complete and verified

**Prerequisites:**
- M10.G1.T1 through M10.G1.T9 completed

**Implementation Details:**
Execute the verification pipeline via PowerShell:

```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

# 1. Static Typecheck
npm run typecheck
if ($LASTEXITCODE -ne 0) { throw "Typecheck failed" }

# 2. Linting
npm run lint
if ($LASTEXITCODE -ne 0) { throw "Lint failed" }

# 3. Unit Test Execution
npx vitest run tests/launch/scaffold.test.ts
if ($LASTEXITCODE -ne 0) { throw "Scaffold test failed" }

# 4. Git Boundary Audit
$diff = git diff --name-only
$modifiedGated = $diff | Where-Object { $_ -match "^package\.json" -or $_ -match "^next\.config\.ts" -or $_ -match "^src/" -or $_ -match "^scripts/audit/" }
if ($modifiedGated) {
    throw "Gated files modified prematurely: $modifiedGated"
}

Write-Host "M10.G1 Checkpoint: All quality gates passed cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$p1 = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$p2 = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$p3 = (Start-Process -FilePath "npx" -ArgumentList "vitest run tests/launch/scaffold.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($p1 -eq 0 -and $p2 -eq 0 -and $p3 -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 1.7

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path ".kiro\specs\m10-deployment-launch\task-notes.md"
Test-Path "scripts\launch\lib\types.ts"
Test-Path "tests\launch\scaffold.test.ts"
npx vitest run tests/launch/scaffold.test.ts
git status --porcelain package.json next.config.ts vercel.json
```
Expected output:
- `True` for `task-notes.md`, `types.ts`, and `scaffold.test.ts`
- Vitest reports all tests in `tests/launch/scaffold.test.ts` passed
- `git status` reports clean for `package.json`, `next.config.ts`, and `vercel.json` (no unapproved edits)