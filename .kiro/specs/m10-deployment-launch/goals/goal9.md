# M10.G9: HUMAN Launch Execution Runbook

> **Milestone:** M10 — Deployment & Launch  
> **Goal:** G9 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Execute the end-to-end production launch as a deterministic sequence of Human_Procedures guided by committed operational specifications. The site owner executes external platform steps (content cleanup, domain DNS, Vercel Hobby project configuration, multi-viewport rendering evaluations, rollback drills, production merges, tag creation, and uptime monitoring); the autonomous agent inspects repository state, provides exact commands, and populates the structured Evidence_Record tables in `docs/operations/launch-checklist.md`, `deployment.md`, and `monitoring.md` strictly using human-reported outcomes. Zero evidence may be fabricated.

## Goal Success Criteria

- ✓ `content/site.json` is updated with authentic production `siteUrl`, active contact channels, and zero placeholder domains (`example.com`, `example.vercel.app`)
- ✓ The 6-command Verification_Pipeline executes cleanly on the release candidate commit, and its SHA is recorded in `launch-checklist.md`
- ✓ Vercel Hobby deployment is configured, and Preview_Deployment commit SHA is verified identical to the release candidate SHA
- ✓ `verify:deployment <preview-url>` passes cleanly (code 0) with `X-Robots-Tag: noindex` and `siteUrl` canonical comparison evaluated as `info` findings
- ✓ Browser CSP checks across all inventory routes and 404 page confirm zero console violation reports
- ✓ Pre-launch rollback drill is executed and recorded in `rollback-and-incidents.md`
- ✓ `release/v1.0.0` is merged into the production branch, and `verify:deployment <production-url>` executes cleanly with exit code 0
- ✓ The six TRD 8.2 post-deploy routes are verified accessible over HTTPS
- ✓ Annotated release tag `v1.0.0` is created under approved Human Decision A7 (Manual, at launch) and pushed to remote
- ✓ External uptime monitor is active and recorded in `monitoring.md`

## Prerequisites

- Goals M10.G1 through M10.G8 completed (all launch tooling, tests, and operational guides available)
- Active Vercel account, domain registrar DNS access, and modern browser with developer tools
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`

---

## Tasks

### M10.G9.T1: Clear Content Release Blockers & Validate External Links

**Objective:** The site owner replaces all placeholder contact, social, and URL values in `content/site.json` with authentic production data, confirms the presence of at least 3 complete P0 projects and verifiable credentials, and validates external link targets.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ `content/site.json` contains real contact email and active public profile links
- ✓ `content/` contains at least 3 completed projects exposing repository links and build documentation
- ✓ All published certifications have authentic `verificationUrl` links
- ✓ `npm run audit:links:online` executes cleanly with zero broken external links
- ✓ Agent verifies absence of `example.com` or `example.vercel.app` in `content/`
- ✓ Agent populates Content section Evidence_Record (`EV-LCH-02`) in `docs/operations/launch-checklist.md`

**Prerequisites:**
- M10.G8 completed
- Target files: `content/site.json`, `docs/operations/launch-checklist.md`

**Implementation Details:**

1. **Human Step:** Edit `content/site.json` replacing placeholder emails, GitHub handles, and LinkedIn URLs with authentic personal channels.
2. **Agent Verification Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

   # 1. Check for placeholder strings in content
   $matches = Select-String -Path "content\**\*.json", "content\**\*.mdx" -Pattern "example\.com", "example\.vercel\.app"
   if ($matches) {
       throw "Release Blocker: Placeholders found in content: $($matches.Count) matches"
   }

   # 2. Run online link audit if supported in M9
   npm run audit:links:online
   ```
3. **Agent Evidence Recording:** Upon human confirmation, update Evidence_Record `EV-LCH-02` in `docs/operations/launch-checklist.md`.

**Evidence Record:**
- **Document:** `docs/operations/launch-checklist.md`
- **Section:** `Content`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <head-sha>`, `Outcome: PASS`, `Reference: Clean online links audit and 0 content placeholders`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$matches = Select-String -Path "content\site.json" -Pattern "example\.com"
if (-not $matches) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 3.1–3.9

---

### M10.G9.T2: Finalize Production Domain & Validate Site URL

**Objective:** The site owner determines the production domain (default `*.vercel.app` or custom domain), configures registrar DNS records if custom, and updates `content/site.json` `siteUrl`. The agent runs a full build and the SEO audit to verify canonical and metadata parity.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ Production domain selected and DNS configured at registrar (if custom domain)
- ✓ `content/site.json` `siteUrl` updated to exact production HTTPS origin (e.g. `https://portfolio.vercel.app`)
- ✓ `npm run build` succeeds
- ✓ `npm run audit:seo` exits with code 0 and reports zero placeholder findings
- ✓ Canonical link tags, Open Graph meta tags, and JSON-LD structured data in `out/` reflect the production origin
- ✓ Agent populates Domain Configuration Evidence_Record (`EV-DEP-02`) in `docs/operations/deployment.md`

**Prerequisites:**
- M10.G9.T1 completed
- Target files: `content/site.json`, `docs/operations/deployment.md`

**Implementation Details:**

1. **Human Step:** Configure custom domain DNS records (CNAME to `cname.vercel-dns.com` or A record to `76.76.21.21`) or confirm Vercel assigned domain. Update `siteUrl` in `content/site.json`.
2. **Agent Verification Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

   # 1. Compile production static export
   npm run build
   if ($LASTEXITCODE -ne 0) { throw "Build failed" }

   # 2. Run M9 SEO Audit
   npm run audit:seo
   if ($LASTEXITCODE -ne 0) { throw "SEO audit failed" }

   # 3. Verify HTML output contains the siteUrl
   $pkgSiteUrl = (Get-Content "content/site.json" -Raw | ConvertFrom-Json).siteUrl
   $indexHtml = Get-Content "out/index.html" -Raw
   if (-not $indexHtml.Contains($pkgSiteUrl)) {
       throw "Verification Failed: out/index.html does not contain the production siteUrl."
   }
   ```
3. **Agent Evidence Recording:** Populate Evidence_Record `EV-DEP-02` in `docs/operations/deployment.md`.

**Evidence Record:**
- **Document:** `docs/operations/deployment.md`
- **Section:** `Domain and Site URL`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <head-sha>`, `Outcome: PASS`, `Reference: SEO audit clean and out/index.html canonical matches siteUrl`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$pkgSiteUrl = (Get-Content "content/site.json" -Raw | ConvertFrom-Json).siteUrl
$indexHtml = Get-Content "out/index.html" -Raw
if ($indexHtml.Contains($pkgSiteUrl) -and -not $indexHtml.Contains("example.vercel.app")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 8.1–8.8

---

### M10.G9.T3: Execute Verification Pipeline on Release Candidate Commit

**Objective:** Execute all six canonical verification commands on the release candidate commit, confirm zero release-blocker findings from M9 audits, verify the signed accessibility checklist in `docs/quality/`, and record the release candidate SHA in `launch-checklist.md`.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ `npm ci`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run audit` exit with code 0
- ✓ Head commit SHA retrieved and confirmed as the immutable Release Candidate SHA
- ✓ Signed M9 manual accessibility checklist in `docs/quality/` confirmed present
- ✓ Agent populates Verification Pipeline Evidence_Record (`EV-LCH-04`) and Accessibility Evidence_Record (`EV-LCH-05`) in `launch-checklist.md`

**Prerequisites:**
- M10.G9.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\launch-checklist.md`

**Implementation Details:**

1. **Agent Pipeline Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

   npm ci
   npm run lint
   npm run typecheck
   npm test
   npm run build
   npm run audit

   $rcSha = (git rev-parse HEAD).Trim()
   Write-Host "Release Candidate Verified: $rcSha"
   ```
2. **Human Verification:** Inspect `docs/quality/` to confirm the manual accessibility checklist is signed off.
3. **Agent Evidence Recording:** Record `$rcSha` in the Release Candidate section of `docs/operations/launch-checklist.md` and populate Evidence_Records `EV-LCH-01`, `EV-LCH-04`, and `EV-LCH-05`.

**Evidence Record:**
- **Document:** `docs/operations/launch-checklist.md`
- **Sections:** `Release Candidate`, `Verification Pipeline`, `Accessibility and Performance`
- **Fields to Update:** `Commit SHA: <rc-sha>`, `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Outcome: PASS`, `Reference: All 6 pipeline commands exit 0`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$lch = Get-Content "docs/operations/launch-checklist.md" -Raw
if ($lch -notmatch "\[PENDING RELEASE CANDIDATE\]") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.3, Req 2.4, Req 2.5, Req 2.6

---

### M10.G9.T4: Create Vercel Project & Push Release Branch (`release/v1.0.0`)

**Objective:** The site owner connects the repository to Vercel on the Hobby Plan, confirms project settings, creates and pushes the release branch `release/v1.0.0`, and verifies that the Preview Deployment commit SHA exactly matches the Release Candidate SHA.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ Vercel Hobby project connected (framework Next.js, build `npm run build`, output `out`, zero env vars)
- ✓ Branch `release/v1.0.0` created from the release candidate commit and pushed to remote
- ✓ Vercel Preview Deployment generated successfully
- ✓ Preview Deployment commit SHA confirmed identical to the Release Candidate SHA
- ✓ Agent populates Vercel Project Setup Evidence_Record (`EV-DEP-01`) in `docs/operations/deployment.md`

**Prerequisites:**
- M10.G9.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**

1. **Human Step:** Log into Vercel, connect `personal-website-portfolio-v2` on Hobby Plan, and set Output Directory to `out`.
2. **Human / Shell Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   git checkout -b release/v1.0.0
   git push origin release/v1.0.0
   ```
3. **Human Step:** Observe Vercel deployment logs for the preview branch. Confirm build success and record the preview deployment URL (e.g. `https://personal-website-portfolio-v2-git-release-v100-*.vercel.app`). Confirm the commit SHA in the Vercel dashboard matches `git rev-parse HEAD`.
4. **Agent Evidence Recording:** Populate Evidence_Record `EV-DEP-01` in `docs/operations/deployment.md`.

**Evidence Record:**
- **Document:** `docs/operations/deployment.md`
- **Section:** `Vercel Project Setup`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <rc-sha>`, `Outcome: PASS`, `Reference: <preview-url>`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$branch = (git branch --show-current).Trim()
if ($branch -eq "release/v1.0.0" -or (git branch -a) -match "release/v1.0.0") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 4.1–4.9, Req 9.1, Req 9.2, Req 9.6

---

### M10.G9.T5: Execute Deployment Verifier Against Preview Deployment

**Objective:** Execute `npm run verify:deployment` against the live Vercel Preview Deployment URL, confirming that status 200, headers, canonical URLs (compared against `siteUrl`), and robots tags (treating Vercel's `X-Robots-Tag: noindex` as `info` per Decision 10) pass cleanly with exit code 0.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ `npm run verify:deployment -- <preview-url>` executes over the network
- ✓ All inventory routes return HTTP 200
- ✓ `/this-route-does-not-exist-m10` returns HTTP 404 with expected body text
- ✓ Preview `X-Robots-Tag: noindex` evaluated as `info` finding (`details.reason: 'expected-on-preview'`)
- ✓ Canonical URLs evaluated against `siteUrl` with single `base-differs-from-siteUrl` info finding
- ✓ Process exits with code 0
- ✓ Agent populates Preview Deployment Evidence_Record (`EV-DEP-04`) in `docs/operations/deployment.md`

**Prerequisites:**
- M10.G9.T4 completed (Preview URL available)
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\deployment.md`

**Implementation Details:**

1. **Human Step:** Provide the live Preview URL generated by Vercel.
2. **Agent Execution Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   npm run verify:deployment -- <preview-url>
   ```
3. **Agent Verification:** Assert exit code 0. Verify `reports/verify-deployment.json` records 0 errors.
4. **Agent Evidence Recording:** Populate Evidence_Record `EV-DEP-04` in `docs/operations/deployment.md`.

**Evidence Record:**
- **Document:** `docs/operations/deployment.md`
- **Section:** `Preview Deployment`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <rc-sha>`, `Outcome: PASS`, `Reference: reports/verify-deployment.json clean with 0 errors`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$report = Get-Content "reports/verify-deployment.json" -Raw | ConvertFrom-Json
if ($report.status -eq "pass" -and $report.summary.errors -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 7.1–7.15, Req 9.3

---

### M10.G9.T6: Manual Smoke Test, Responsive Viewport & Browser CSP Audit

**Objective:** The site owner conducts manual smoke testing across all routes on the Preview Deployment, auditing viewports at 375px, 768px, and 1024px+, inspecting developer console for zero CSP violations, and confirming network hygiene (zero third-party requests).

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ Manual navigation verified across `/`, `/projects`, `/projects/[slug]`, `/certifications`, `/blog`, `/blog/[slug]`, and `/this-route-does-not-exist`
- ✓ Responsive layout confirmed functional at 375px (mobile), 768px (tablet), and 1024px+ (desktop)
- ✓ Browser console reports zero Content Security Policy violation warnings or errors across all routes
- ✓ Network tab confirms zero outbound requests to unapproved third-party domains (zero analytics/tracking)
- ✓ Agent populates Security Evidence_Record (`EV-LCH-06`) in `launch-checklist.md` and Browser CSP Evidence_Record (`EV-DEP-03`) in `deployment.md`

**Prerequisites:**
- M10.G9.T5 completed
- Target files: `docs/operations/launch-checklist.md`, `docs/operations/deployment.md`

**Implementation Details:**

1. **Human Step:** Open browser (Chrome/Edge/Firefox/Safari) to the Preview URL. Open DevTools Console and Network tabs.
2. **Human Step:** Test viewports at 375px, 768px, and desktop widths. Click primary navigation links and external links.
3. **Human Step:** Confirm zero CSP violation logs and zero failed requests.
4. **Agent Evidence Recording:** Upon human confirmation, populate `EV-LCH-06` in `launch-checklist.md` and `EV-DEP-03` in `deployment.md`.

**Evidence Record:**
- **Document:** `docs/operations/launch-checklist.md` & `docs/operations/deployment.md`
- **Sections:** `Security`, `Content Security Policy`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <rc-sha>`, `Outcome: PASS`, `Reference: Clean console audit; tested on Chrome and Edge`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$lch = Get-Content "docs/operations/launch-checklist.md" -Raw
if ($lch -match "EV-LCH-06" -and $lch -match "Angelo Andres") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.8, Req 6.8, Req 6.9, Req 9.4, Req 9.5

---

### M10.G9.T7: Execute Pre-Launch Rollback Drill

**Objective:** The site owner performs a simulated rollback drill following `docs/operations/rollback-and-incidents.md` to confirm the instant recovery procedure prior to production release sign-off.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ Rollback drill executed against a preview deployment or staging target in the Vercel Dashboard
- ✓ Verified restoration of predecessor deployment
- ✓ Health confirmed via deployment verifier execution
- ✓ Agent populates Rollback Drill Evidence_Record (`EV-ROL-01`) in `docs/operations/rollback-and-incidents.md`

**Prerequisites:**
- M10.G9.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\docs\operations\rollback-and-incidents.md`

**Implementation Details:**

1. **Human Step:** In Vercel Project > Deployments, test the Instant Rollback or redeployment action on a preview branch.
2. **Human Step:** Confirm traffic immediately routes to the rolled-back target.
3. **Agent Verification Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   npm run verify:deployment -- <rolled-back-preview-url>
   ```
4. **Agent Evidence Recording:** Populate Evidence_Record `EV-ROL-01` in `docs/operations/rollback-and-incidents.md`.

**Evidence Record:**
- **Document:** `docs/operations/rollback-and-incidents.md`
- **Section:** `Rollback Drill`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <rc-sha>`, `Outcome: PASS`, `Reference: Drill completed; rollback verified via verifier`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$rol = Get-Content "docs/operations/rollback-and-incidents.md" -Raw
if ($rol -match "EV-ROL-01" -and $rol -match "Angelo Andres") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.7

---

### M10.G9.T8: Merge Release Branch to Production & Execute Strict Verification

**Objective:** The site owner merges `release/v1.0.0` into `main` (the exclusive trigger for Production_Deployment), executes `verify:deployment` in strict production mode, confirms the six TRD 8.2 post-deploy routes, verifies HSTS, and sets up external synthetic uptime monitoring.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ `release/v1.0.0` merged into `main` and pushed to remote
- ✓ Vercel Production Deployment completes successfully
- ✓ `npm run verify:deployment -- https://<production-domain>` executes with exit code 0
- ✓ Production check strictly asserts canonical matches production domain (0 errors)
- ✓ Production check strictly asserts `X-Robots-Tag: noindex` is absent on production routes (0 errors)
- ✓ Six TRD 8.2 post-deploy routes verified live over HTTPS
- ✓ External uptime monitor configured and confirmed active
- ✓ Agent populates Production Deployment Evidence_Record (`EV-DEP-05`) in `deployment.md`, Deployment Evidence_Record (`EV-LCH-07`) in `launch-checklist.md`, and Uptime Evidence_Record (`EV-MON-01`) in `monitoring.md`

**Prerequisites:**
- M10.G9.T7 completed
- Target files: `docs/operations/deployment.md`, `docs/operations/launch-checklist.md`, `docs/operations/monitoring.md`

**Implementation Details:**

1. **Human / Shell Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   git checkout main
   git merge release/v1.0.0 --ff-only
   git push origin main
   ```
2. **Human Step:** Observe Vercel Production Deployment build logs until completed.
3. **Agent Verification Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   npm run verify:deployment -- https://<production-domain>
   ```
4. **Human Step:** In external monitor (UptimeRobot / Better Uptime), configure checks for `<production-url>/` and `<production-url>/projects` with 5-minute interval.
5. **Agent Evidence Recording:** Populate `EV-DEP-05` in `deployment.md`, `EV-LCH-07` in `launch-checklist.md`, and `EV-MON-01` in `monitoring.md`.

**Evidence Record:**
- **Documents:** `deployment.md`, `launch-checklist.md`, `monitoring.md`
- **Sections:** `Production Deployment`, `Deployment`, `Uptime Monitor`
- **Fields to Update:** `Performed by: Angelo Andres`, `Date (UTC): <current-date>`, `Commit SHA: <prod-sha>`, `Outcome: PASS`, `Reference: Production verifier passed cleanly with 0 errors`.

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$lch = Get-Content "docs/operations/launch-checklist.md" -Raw
if ($lch -match "EV-LCH-07" -and $lch -match "Angelo Andres") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.8, Req 7.1–7.15, Req 9.7–9.11, Req 10.5

---

### M10.G9.T9: Create Annotated Release Tag & Finalize Launch Date

**Objective:** Under verified Human Approval A7 (Manual, at launch), the site owner creates and pushes the annotated Git tag `v1.0.0` on the production deployment commit. The agent updates the launch date in `README.md`, `CHANGELOG.md`, and recomputes post-launch check-in dates via `computeCheckInDates` in `post-launch-plan.md`.

**Performed By:** HUMAN (owner) & AGENT

**Acceptance Criteria:**
- ✓ Human explicitly approves release tagging at launch time
- ✓ Annotated tag `v1.0.0` created on production commit and pushed: `git tag -a v1.0.0 -m "Release v1.0.0"`
- ✓ `git show v1.0.0` confirms annotated tag type and matching commit SHA
- ✓ `README.md` and `CHANGELOG.md` updated with verified launch date (replacing `[Pending Launch]`)
- ✓ `docs/operations/post-launch-plan.md` updated with calculated calendar dates for Week 1, Week 4, and Week 12
- ✓ Site owner authorized to share Production URL across professional profiles

**Prerequisites:**
- M10.G9.T8 completed
- Target files: `README.md`, `CHANGELOG.md`, `docs/operations/post-launch-plan.md`

**Implementation Details:**

1. **Human Step:** Request and record explicit launch approval.
2. **Human / Shell Command:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   $prodSha = (git rev-parse HEAD).Trim()
   git tag -a v1.0.0 $prodSha -m "Release v1.0.0: Personal Website Portfolio P0 MVP"
   git push origin v1.0.0
   ```
3. **Agent Date Synchronization Script:**
   ```powershell
   cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
   $launchDate = Get-Date -Format "yyyy-MM-dd"

   # 1. Update README.md
   $readme = Get-Content "README.md" -Raw
   $readme = $readme -replace "\[Pending Production Deployment\]", (Get-Content "content/site.json" -Raw | ConvertFrom-Json).siteUrl
   $readme = $readme -replace "\[Pending Launch Date\]", $launchDate
   Set-Content -Path "README.md" -Value $readme -Encoding UTF8

   # 2. Update CHANGELOG.md
   $cl = Get-Content "CHANGELOG.md" -Raw
   $cl = $cl -replace "## \[1\.0\.0\] - \[Pending Launch\]", "## [1.0.0] - $launchDate"
   Set-Content -Path "CHANGELOG.md" -Value $cl -Encoding UTF8

   # 3. Update post-launch-plan.md via computeCheckInDates
   # Invocable via node inline evaluation of check-in-dates
   $script = @"
   const { computeCheckInDates } = require('./scripts/launch/lib/check-in-dates');
   const dates = computeCheckInDates('$launchDate');
   console.log(JSON.stringify(dates));
   "@
   # Update dates in post-launch-plan.md accordingly
   ```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$tag = git tag -l "v1.0.0"
if ($tag -eq "v1.0.0") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 11.2, Req 14.4

---

### M10.G9.T10: Goal 9 Checkpoint and Launch Execution Verification

**Objective:** Audit all operations documents to verify that every Evidence_Record table across Content, Configuration, Verification Pipeline, Accessibility, Security, and Deployment has been populated with authentic human-reported evidence, and that the docs schema lint passes cleanly.

**Performed By:** AGENT

**Acceptance Criteria:**
- ✓ `npm run lint` completes with code 0
- ✓ `npm run typecheck` completes with code 0
- ✓ All Evidence_Records in `docs/operations/launch-checklist.md` are filled (zero `PENDING` statuses in completed sections)
- ✓ All Evidence_Records in `docs/operations/deployment.md` are filled
- ✓ `tests/launch/docs-real-all.test.ts` passes cleanly
- ✓ Zero fabricated URLs, SHAs, or timestamps

**Prerequisites:**
- M10.G9.T1 through M10.G9.T9 completed

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

# 3. Docs Schema Lint
npx vitest run tests/launch/docs-real-all.test.ts
if ($LASTEXITCODE -ne 0) { throw "Docs schema lint failed" }

Write-Host "M10.G9 Checkpoint: Production launch executed and all operational evidence recorded cleanly."
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$lch = Get-Content "docs/operations/launch-checklist.md" -Raw
if ($lch -match "EV-LCH-07" -and $lch -notmatch "EV-LCH-01 \| Step \| Release Candidate Identification \|\s*\| Performed by \| \[Pending") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1–2.8, Req 9.1–9.11, Req 16.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 9 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
git tag -l "v1.0.0"
npx vitest run tests/launch/docs-real-all.test.ts
git status --porcelain
```
Expected output:
- Tag output lists `v1.0.0`
- Vitest reports all documentation schemas passed cleanly
- Working tree clean or ready for final sign-off commit