# Stage 2 Approvals Record

> Recorded: 2026-10-22. Approver: Angelo Andres. Scope: AGENTS.md 6.2 items raised by specs M3 to M10.

| # | Item | Decision | Applies to | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 1 | devDependencies: fast-check, axe test helper, @testing-library/user-event, axe-core, lighthouse, chrome-launcher | **1a Approved** | M3, M4, M9 | Exact versions pinned at implementation after documenting purpose and checking maintenance status. |
| 2 | JSON-LD page edits (Person on `/`, Article on blog posts, BreadcrumbList on project and blog detail) | **2a Approved** | M9 (touches M5, M6, M8 pages) | Limited to import and render lines. |
| 3 | `vercel.json` security headers | **3a Approved** | M10 | CSP `script-src 'self' 'unsafe-inline'`, all other directives strict. Hash mode stays an optional alternative. |
| 4 | `package.json` scripts and `.gitignore` | **4b Approved (scripts and `reports/` only)** | M9, M10 | Version bump to 1.0.0 is declined. Version lives in CHANGELOG.md and the git tag. |
| 5 | `next.config.ts` static export | **5b Approved** | M1, M9, M10 | M1 design corrected from `standalone` to `output: 'export'`, `images.unoptimized: true`, output `out/`. |
| 6 | CI workflow `.github/workflows/verify.yml` | **6a Approved** | M10 | Offline checks only. Never runs the deployment verifier. |
| 7 | Spec conflicts C1 to C8 (M10) and 404 `noindex` reading (M9) | **7b Requirements amended to match design** | M9, M10 | |
| 8 | Vercel Hobby deployment-size limit | **8b Keep 25 MB budget** | M9, M10 | Dated re-check task stays before launch. |
| 9 | `v1.0.0` tag and production merge | **9a Manual** | M10 | Explicit approval requested at launch time. |

## Open items (not approvals)

- Vercel Hobby size and file-count limits are unverified.
- Component prop names (M3 primitives), M2 loader paths and the Next.js `params` shape are confirmed by the implementer.
- No real `out/` tree exists yet. The first M10 CSP task builds and inspects it.
