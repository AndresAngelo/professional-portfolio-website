# M4.G1: Fixtures, Fixed UI Strings, Dependency Approval, and Gap Log

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the foundational test fixtures, property-based testing arbitraries, fixed layout strings, and architectural gap audit for Milestone 4. Specifically, construct strongly typed `SiteConfig` fixtures in `tests/fixtures/site-config.ts` covering full and edge-case site configurations without schema duplication. Author `fast-check` arbitraries in `tests/fixtures/site-config-arbitraries.ts` to support universal property verification across navigation, contact channels, and metadata. Create `src/components/layout/layout-text.ts` defining all static, non-content UI strings and HTML element IDs (such as skip links, landmark IDs, and section labels). Verify that all required upstream dependencies, M2 types/loaders, and M3 UI primitives exist, and formally document design-system gaps (such as `z-50` stacking and dark-mode postures) alongside tool approvals (`@testing-library/user-event@14.5.2`, `vitest-axe@0.1.0`, and `fast-check@3.23.2` under Approval 1a) in `task-notes.md`.

## Goal Success Criteria

- ✓ `tests/fixtures/site-config.ts` exports typed fixtures (`validSiteConfig`, `noPrimaryChannelSiteConfig`, `emptyContactChannelsSiteConfig`, `emptySocialLinksSiteConfig`, `reorderedNavSiteConfig`) strictly typed via `@/types/content`
- ✓ `tests/fixtures/site-config-arbitraries.ts` exports `fast-check` generators for navigation items, contact channels, social links, valid absolute URLs, and non-URL strings
- ✓ `src/components/layout/layout-text.ts` exports all canonical UI constants (`SKIP_LINK_TEXT`, `MAIN_CONTENT_ID`, `CONTACT_REGION_ID`, `PRIMARY_NAV_LABEL`, etc.) with zero site-owner or personal-data literals
- ✓ Upstream M2 types (`SiteConfig`, `SiteNavigationItem`, `ContactChannel`, `SocialLink`), M2 loaders (`getSiteConfig`), and M3 primitives (`Container`, `Button`, `ExternalLink`, `FOCUS_RING`, `MOTION_FAST`, `cx`, `resolveExternalHref`) confirmed intact
- ✓ Task notes file `.kiro/specs/m4-global-layout-navigation/task-notes.md` initialized with audit of the `z-50` stacking token, dark-mode posture, `usePathname()` boundary notes, and toolchain approvals
- ✓ Approved dev-dependencies (`@testing-library/user-event@14.5.2`, `vitest-axe@0.1.0`, `fast-check@3.23.2`) verified in `package.json`
- ✓ Unit tests in `tests/unit/components/layout/layout-text.test.ts` pass, proving constants are non-empty and IDs adhere to HTML syntax
- ✓ Fixture sanity tests in `tests/fixtures/site-config.test.ts` pass, validating type compliance and edge-case array structures
- ✓ `git diff` confirms zero edits to `tailwind.config.ts`, `globals.css`, or `src/components/ui/`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Milestones M1, M2, and M3 completed (`m3-baseline` tagged in Git)
- Workspace root: `c:\dev\andres-webapp-professional\personal-website-portfolio`
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- Upstream packages installed: `vitest`, `@testing-library/react`, `fast-check`, `vitest-axe`

---

## Tasks

### M4.G1.T1: Create Typed SiteConfig Test Fixtures (`tests/fixtures/site-config.ts`)

**Objective:** Author canonical, strongly typed `SiteConfig` test fixtures in `tests/fixtures/site-config.ts` covering full configurations, missing primary channels, empty contact arrays, empty social links, and reordered navigation.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/site-config.ts` exists
- ✓ Imports `SiteConfig` from `@/types/content` without redeclaring interfaces (`AGENTS.md` 6.3, Req 2.3)
- ✓ Exports `validSiteConfig`: includes primary email contact, external links, social links, and canonical navigation (`/`, `/projects`, `/certifications`, `/blog`)
- ✓ Exports `noPrimaryChannelSiteConfig`: contact channels where `isPrimary` is false for all entries
- ✓ Exports `emptyContactChannelsSiteConfig`: `contactChannels` is an empty array `[]`
- ✓ Exports `emptySocialLinksSiteConfig`: `socialLinks` is an empty array `[]`
- ✓ Exports `reorderedNavSiteConfig`: navigation items specified in non-canonical order plus custom routes
- ✓ Contains zero `any`, non-null assertions `!`, or unjustified type assertions

**Prerequisites:**
- M2 content contracts exist at `src/types/content.ts`
- Target directory `tests/fixtures/` exists or is created

**Implementation Details:**

Write `tests/fixtures/site-config.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "tests\fixtures")) {
    New-Item -ItemType Directory -Path "tests\fixtures" -Force | Out-Null
}

@'
import type { SiteConfig } from '@/types/content';

/**
 * Standard complete SiteConfig fixture representing a fully populated profile.
 */
export const validSiteConfig: SiteConfig = {
  siteName: 'Angelo Andres',
  siteUrl: 'https://example.vercel.app',
  profile: {
    name: 'Angelo Andres',
    professionalTitle: 'Pipeline Lead & Specification Architect',
    introduction: 'I build specification-driven software and AI engineering workflows.',
    location: 'Taguig, National Capital Region, PH',
    availableForOpportunities: true,
  },
  contactChannels: [
    {
      type: 'email',
      label: 'Email Angelo',
      url: 'mailto:hello@example.com',
      isPrimary: true,
    },
    {
      type: 'linkedin',
      label: 'LinkedIn Profile',
      url: 'https://linkedin.com/in/example',
      isPrimary: false,
    },
    {
      type: 'github',
      label: 'GitHub Account',
      url: 'https://github.com/example',
      isPrimary: false,
    },
  ],
  socialLinks: [
    {
      label: 'GitHub',
      url: 'https://github.com/example',
    },
    {
      label: 'LinkedIn',
      url: 'https://linkedin.com/in/example',
    },
  ],
  navigation: [
    { label: 'Home', href: '/' },
    { label: 'Projects', href: '/projects' },
    { label: 'Certifications', href: '/certifications' },
    { label: 'Blog', href: '/blog' },
  ],
};

/**
 * SiteConfig fixture where no contact channel is designated as primary.
 */
export const noPrimaryChannelSiteConfig: SiteConfig = {
  ...validSiteConfig,
  contactChannels: validSiteConfig.contactChannels.map((channel) => ({
    ...channel,
    isPrimary: false,
  })),
};

/**
 * SiteConfig fixture with zero contact channels.
 */
export const emptyContactChannelsSiteConfig: SiteConfig = {
  ...validSiteConfig,
  contactChannels: [],
};

/**
 * SiteConfig fixture with zero social links.
 */
export const emptySocialLinksSiteConfig: SiteConfig = {
  ...validSiteConfig,
  socialLinks: [],
};

/**
 * SiteConfig fixture with reordered navigation and custom paths.
 */
export const reorderedNavSiteConfig: SiteConfig = {
  ...validSiteConfig,
  navigation: [
    { label: 'Blog', href: '/blog' },
    { label: 'Docs', href: '/docs' },
    { label: 'Projects', href: '/projects' },
    { label: 'Home', href: '/' },
    { label: 'Certifications', href: '/certifications' },
  ],
};
'@ | Set-Content "tests\fixtures\site-config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit tests/fixtures/site-config.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 2.3, Req 3.3, Req 3.4, Req 4.4, Req 4.5, Req 8.5, Req 8.6, Req 15.5

---

### M4.G1.T2: Create Property-Based Testing Arbitraries (`tests/fixtures/site-config-arbitraries.ts`)

**Objective:** Author fast-check arbitraries in `tests/fixtures/site-config-arbitraries.ts` for property tests validating navigation ordering, contact rendering, and URL boundaries.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/site-config-arbitraries.ts` exists
- ✓ Exports `navItemArbitrary`: generates `{ label: string, href: string }` with valid route formats
- ✓ Exports `contactChannelArbitrary`: generates channels across all `ContactChannelType` values (`email`, `linkedin`, `github`, `website`, `other`) with matching URL schemes
- ✓ Exports `socialLinkArbitrary`: generates valid HTTPS social links
- ✓ Exports `absoluteUrlArbitrary`: generates syntactically valid `https://` URLs
- ✓ Exports `invalidUrlArbitrary`: generates strings that fail absolute URL parsing
- ✓ Built strictly using `fast-check` without hand-rolled pseudo-random generators

**Prerequisites:**
- `fast-check` installed (`devDependencies`)
- Types available at `@/types/content`
- Target file: `tests/fixtures/site-config-arbitraries.ts`

**Implementation Details:**

Write `tests/fixtures/site-config-arbitraries.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import fc from 'fast-check';
import type { ContactChannel, ContactChannelType, SiteNavigationItem, SocialLink } from '@/types/content';

/**
 * Arbitrary generator for navigation items.
 */
export const navItemArbitrary: fc.Arbitrary<SiteNavigationItem> = fc.record({
  label: fc.string({ minLength: 1, maxLength: 25 }).filter((s) => s.trim().length > 0 && !s.includes('<')),
  href: fc.oneof(
    fc.constantFrom('/', '/projects', '/certifications', '/blog'),
    fc.string({ minLength: 1, maxLength: 15 })
      .filter((s) => /^[a-z0-9-]+$/.test(s))
      .map((slug) => `/${slug}`)
  ),
});

/**
 * Arbitrary generator for contact channels with protocol-adherent URLs.
 */
export const contactChannelArbitrary: fc.Arbitrary<ContactChannel> = fc.record({
  type: fc.constantFrom<ContactChannelType>('email', 'linkedin', 'github', 'website', 'other'),
  label: fc.string({ minLength: 1, maxLength: 30 }).filter((s) => s.trim().length > 0 && !s.includes('<')),
  isPrimary: fc.boolean(),
  url: fc.string(),
}).chain((base) => {
  if (base.type === 'email') {
    return fc.emailAddress().map((email) => ({
      ...base,
      url: `mailto:${email}`,
    }));
  }
  return fc.webUrl({ validSchemes: ['https'] }).map((url) => ({
    ...base,
    url,
  }));
});

/**
 * Arbitrary generator for external social links.
 */
export const socialLinkArbitrary: fc.Arbitrary<SocialLink> = fc.record({
  label: fc.string({ minLength: 1, maxLength: 25 }).filter((s) => s.trim().length > 0 && !s.includes('<')),
  url: fc.webUrl({ validSchemes: ['https'] }),
});

/**
 * Valid HTTPS URL generator.
 */
export const absoluteUrlArbitrary: fc.Arbitrary<string> = fc.webUrl({ validSchemes: ['https'] });

/**
 * Arbitrary generator for invalid non-absolute URLs.
 */
export const invalidUrlArbitrary: fc.Arbitrary<string> = fc.oneof(
  fc.constant(''),
  fc.constant('not-a-url'),
  fc.constant('/relative/path'),
  fc.constant('http://insecure.example.com'),
  fc.constant('javascript:alert(1)'),
  fc.string().filter((s) => {
    try {
      new URL(s);
      return false;
    } catch {
      return true;
    }
  })
);
'@ | Set-Content "tests\fixtures\site-config-arbitraries.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit tests/fixtures/site-config-arbitraries.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 10.7, Req 15.6, Req 15.7

---

### M4.G1.T3: Implement Fixed UI Strings and Element IDs (`src/components/layout/layout-text.ts`)

**Objective:** Author `src/components/layout/layout-text.ts` defining all static, non-content UI strings and HTML element IDs so that no layout text is hardcoded across components.

**Acceptance Criteria:**
- ✓ File `src/components/layout/layout-text.ts` exists
- ✓ Exports `SKIP_LINK_TEXT = 'Skip to main content'`
- ✓ Exports `MAIN_CONTENT_ID = 'main-content'`
- ✓ Exports `CONTACT_REGION_ID = 'contact'`
- ✓ Exports `CONTACT_NAV_LABEL = 'Contact'`
- ✓ Exports `MENU_BUTTON_LABEL = 'Menu'`
- ✓ Exports `PRIMARY_NAV_LABEL = 'Primary'`
- ✓ Exports `PRIMARY_NAV_LIST_ID = 'primary-nav-list'`
- ✓ Exports `FOOTER_NAV_LABEL = 'Footer'`
- ✓ Exports `FOOTER_SITE_HEADING = 'Site'`, `FOOTER_SOCIAL_HEADING = 'Profiles'`, `FOOTER_CONTACT_HEADING = 'Contact'`
- ✓ Exports `NOT_FOUND_HEADING = 'Page not found'`, `NOT_FOUND_MESSAGE = 'The page you followed does not exist or has moved.'`, `NOT_FOUND_HOME_LABEL = 'Back to home'`, `NOT_FOUND_SECTIONS_LABEL = 'Browse a section'`
- ✓ Contains zero owner-specific data or personal strings

**Prerequisites:**
- Directory `src/components/layout/` exists or is created
- Target file: `src/components/layout/layout-text.ts`

**Implementation Details:**

Write `src/components/layout/layout-text.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "src\components\layout")) {
    New-Item -ItemType Directory -Path "src\components\layout" -Force | Out-Null
}

@'
/**
 * Fixed UI Strings and Structural Element IDs for Layout Components
 *
 * Enforces separation between structural labels and site-owner data.
 * All dynamic site content originates exclusively from SiteConfig (Req 2.4).
 */

export const SKIP_LINK_TEXT = 'Skip to main content';
export const MAIN_CONTENT_ID = 'main-content';

export const CONTACT_REGION_ID = 'contact';
export const CONTACT_NAV_LABEL = 'Contact';

export const MENU_BUTTON_LABEL = 'Menu';
export const PRIMARY_NAV_LABEL = 'Primary';
export const PRIMARY_NAV_LIST_ID = 'primary-nav-list';

export const FOOTER_NAV_LABEL = 'Footer';
export const FOOTER_SITE_HEADING = 'Site';
export const FOOTER_SOCIAL_HEADING = 'Profiles';
export const FOOTER_CONTACT_HEADING = 'Contact';

export const NOT_FOUND_HEADING = 'Page not found';
export const NOT_FOUND_MESSAGE = 'The page you followed does not exist or has moved.';
export const NOT_FOUND_HOME_LABEL = 'Back to home';
export const NOT_FOUND_SECTIONS_LABEL = 'Browse a section';
'@ | Set-Content "src\components\layout\layout-text.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npx tsc --noEmit src/components/layout/layout-text.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 2.4, Req 4.4, Req 6.3, Req 7.2, Req 8.4, Req 11.2, Req 11.3, Req 11.4

---

### M4.G1.T4: Verify Upstream Contracts, M2 Loaders, and M3 UI Primitives

**Objective:** Audit and confirm the presence and export signatures of upstream M2 loader functions, M2 content types, and M3 UI primitives required by Milestone 4.

**Acceptance Criteria:**
- ✓ Confirms `src/content/loaders/site.ts` exports `getSiteConfig()`
- ✓ Confirms `src/types/content.ts` exports `SiteConfig`, `SiteNavigationItem`, `ContactChannel`, `ContactChannelType`, `SocialLink`
- ✓ Confirms `src/components/ui/` exports `Container`, `Button`, `ExternalLink`, `FOCUS_RING`, `MOTION_FAST`, `cx`, and `resolveExternalHref`
- ✓ Script outputs exact path and symbol confirmation without errors

**Prerequisites:**
- M2 and M3 baselines complete
- PowerShell terminal in workspace root

**Implementation Details:**

Execute inspection script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$errors = @()

# 1. Check M2 Loader
$siteLoader = "src\content\loaders\site.ts"
if (Test-Path $siteLoader) {
    $content = Get-Content $siteLoader -Raw
    if (-not ($content -match 'getSiteConfig')) {
        $errors += "Missing getSiteConfig export in $siteLoader"
    }
} else {
    $errors += "Missing file: $siteLoader"
}

# 2. Check M2 Types
$contentTypes = "src\types\content.ts"
if (Test-Path $contentTypes) {
    $content = Get-Content $contentTypes -Raw
    $typesToCheck = @('SiteConfig', 'SiteNavigationItem', 'ContactChannel', 'ContactChannelType', 'SocialLink')
    foreach ($t in $typesToCheck) {
        if (-not ($content -match "\b$t\b")) {
            $errors += "Missing type export $t in $contentTypes"
        }
    }
} else {
    $errors += "Missing file: $contentTypes"
}

# 3. Check M3 Primitives
$uiFiles = @(
    "src\components\ui\container.tsx",
    "src\components\ui\button.tsx",
    "src\components\ui\external-link.tsx",
    "src\components\ui\focus-ring.ts",
    "src\components\ui\motion.ts",
    "src\components\ui\cx.ts",
    "src\components\ui\external-link-attrs.ts"
)
foreach ($f in $uiFiles) {
    if (-not (Test-Path $f)) {
        $errors += "Missing M3 primitive file: $f"
    }
}

if ($errors.Count -eq 0) { "PASS" } else { $errors | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 13.1, Req 13.2, Req 13.3, Req 13.4

---

### M4.G1.T5: Audit Design Tokens and Screens; Initialize `task-notes.md`

**Objective:** Audit `tailwind.config.ts` and `src/app/globals.css` to verify required color, spacing, typography, and responsive screens, and log all M4 configuration gaps in `.kiro/specs/m4-global-layout-navigation/task-notes.md`.

**Acceptance Criteria:**
- ✓ Directory `.kiro/specs/m4-global-layout-navigation/` contains `task-notes.md`
- ✓ Logs `z-50` stacking gap: Tailwind default `z-50` used for skip link because no custom elevation token exists
- ✓ Logs Global focus-visible overlap: M1 defines `*:focus-visible` ring in `globals.css`, but M4 explicitly composes `FOCUS_RING` on interactive elements
- ✓ Logs Dark mode status: M1 specifies dark CSS variables, but M4 applies zero `dark:` utility overrides (`design.md` 7.7)
- ✓ Logs `usePathname()` boundary note: `usePathname()` on static `/_not-found` prerender returns `null` or `/_not-found`, which must be tolerated cleanly
- ✓ Confirms zero modifications to `tailwind.config.ts` or `src/app/globals.css`

**Prerequisites:**
- Project root exists

**Implementation Details:**

Write `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path ".kiro\specs\m4-global-layout-navigation")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m4-global-layout-navigation" -Force | Out-Null
}

@'
# M4 Global Layout & Navigation — Task Notes & Architectural Audit

## 1. M1/M3 Design Token & Configuration Gaps (Req 13.8)

In compliance with `AGENTS.md` Section 6.2, root configuration files remain unmodified. The following discrepancies and implementation postures are recorded:

| Area / Concern | Specification Expectation | Current Repository Configuration | Interim Implementation Approach |
| :--- | :--- | :--- | :--- |
| **SkipLink Stacking (`z-50`)** | High elevation above header | Tailwind default `z-50` (`z-index: 50`). No custom token in `tailwind.config.ts`. | Use built-in `z-50` utility on `SkipLink`. No token changes without explicit approval. |
| **Global Focus Ring Overlap** | Visible keyboard focus | M1 `globals.css` declares `*:focus-visible` ring. | M4 components explicitly compose `FOCUS_RING` from M3 (`focus-visible:ring-2 focus-visible:ring-focus-ring`) to remain resilient against CSS alterations. |
| **Dark Mode Overrides** | Dark mode off by default (`design.md` 7.7) | M1 `globals.css` defines dark theme variables under `@media (prefers-color-scheme: dark)`. | M4 layout components consume semantic tokens (`bg-page`, `text-text-primary`, etc.) directly with zero `dark:` utility classes. |
| **MobileNavToggle Breakpoint** | Mobile/Tablet collapse, Desktop horizontal | Tailwind screens: `md: 768px`, `lg: 1024px`. | Mobile toggle displays below `lg` (`lg:hidden`); desktop nav expands at `lg` (`lg:flex`). |
| **NotFound Prerender Pathname** | `usePathname()` at build time | Statically prerendered App Router pages execute `usePathname()` during build. | `current-route.ts` and `MobileNavToggle` safely handle `null` or unmapped paths without throwing. |

## 2. Toolchain & Testing Approvals (Approval 1a, 2026-10-22)

Human approval was granted on 2026-10-22 for test tooling in `devDependencies`:
- `@testing-library/user-event@14.5.2`: Simulates realistic Enter, Space, and Escape keyboard activations in jsdom.
- `vitest-axe@0.1.0`: Automated WCAG 2.1 AA accessibility checks.
- `fast-check@3.23.2`: Property-based testing for route matching, nav ordering, and disclosure state machines.

None of these packages affect the static production bundle.
'@ | Set-Content ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path ".kiro\specs\m4-global-layout-navigation\task-notes.md"
```
Expected output: `True`

**Satisfies Requirements:** Req 1.6, Req 6.1, Req 6.2, Req 7.5, Req 13.5, Req 13.7, Req 13.8

---

### M4.G1.T6: Verify Pinned User-Event Testing Tool (`@testing-library/user-event`)

**Objective:** Confirm that `@testing-library/user-event` is pinned in `devDependencies` per Approval 1a (2026-10-22) to enable realistic keyboard simulation (Enter, Space, Tab) in jsdom.

**Acceptance Criteria:**
- ✓ `@testing-library/user-event` present in `package.json` `devDependencies` (pinned at `^14.5.2` or exact)
- ✓ Module resolves cleanly via Node.js require/import
- ✓ Zero runtime or production bundle footprint

**Prerequisites:**
- Working directory: `personal-website-portfolio-v2`
- Node.js LTS environment

**Implementation Details:**

Verify dependency presence using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
$installed = $pkg.devDependencies."@testing-library/user-event"

if ($null -eq $installed) {
    Write-Host "Installing approved @testing-library/user-event@14.5.2..."
    npm install --save-dev --save-exact @testing-library/user-event@14.5.2
} else {
    Write-Host "Confirmed @testing-library/user-event version: $installed"
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
node -e "require('@testing-library/user-event'); console.log('PASS');"
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.3, Req 15.4

---

### M4.G1.T7: Verify Pinned Accessibility and Property Testing Dependencies

**Objective:** Verify that `vitest-axe` and `fast-check` remain pinned and installed in `devDependencies` per Approval 1a (2026-10-22).

**Acceptance Criteria:**
- ✓ `vitest-axe` resolves cleanly from `node_modules`
- ✓ `fast-check` resolves cleanly from `node_modules`
- ✓ Both packages confirmed in `package.json` `devDependencies`
- ✓ Verification command exits with return code 0

**Prerequisites:**
- M3.G1 completed (`vitest-axe` and `fast-check` installed)

**Implementation Details:**

Execute verification check via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

node -e "require('vitest-axe'); require('fast-check'); console.log('PASS');"
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$res = node -e "require('vitest-axe'); require('fast-check'); console.log('PASS');"
if ($res -eq "PASS") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.3, Req 15.3, Req 15.6

---

### M4.G1.T8: Author Unit Tests for Layout Text Constants (`tests/unit/components/layout/layout-text.test.ts`)

**Objective:** Create unit tests in `tests/unit/components/layout/layout-text.test.ts` verifying that all layout text constants and element IDs are non-empty and comply with HTML ID specifications.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/layout-text.test.ts` created
- ✓ Tests all exported string constants are non-empty after trimming
- ✓ Tests all exported element IDs (`MAIN_CONTENT_ID`, `CONTACT_REGION_ID`, `PRIMARY_NAV_LIST_ID`) contain only alphanumeric characters and hyphens without spaces
- ✓ Tests `MAIN_CONTENT_ID` equals `'main-content'` and `CONTACT_REGION_ID` equals `'contact'`
- ✓ All tests pass under `npm test`

**Prerequisites:**
- M4.G1.T3 completed (`layout-text.ts` exists)
- Target file: `tests/unit/components/layout/layout-text.test.ts`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

if (-not (Test-Path "tests\unit\components\layout")) {
    New-Item -ItemType Directory -Path "tests\unit\components\layout" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import * as layoutText from '@/components/layout/layout-text';

describe('Layout Text & Structural Constants', () => {
  it('exports non-empty strings for all defined UI labels', () => {
    const stringKeys = Object.keys(layoutText) as Array<keyof typeof layoutText>;
    expect(stringKeys.length).toBeGreaterThan(10);

    for (const key of stringKeys) {
      const val = layoutText[key];
      expect(typeof val).toBe('string');
      expect(val.trim().length).toBeGreaterThan(0);
    }
  });

  it('enforces valid HTML id syntax for structural element IDs', () => {
    const ids = [
      layoutText.MAIN_CONTENT_ID,
      layoutText.CONTACT_REGION_ID,
      layoutText.PRIMARY_NAV_LIST_ID,
    ];

    for (const id of ids) {
      expect(id).toMatch(/^[a-z0-9-]+$/);
      expect(id.startsWith('-')).toBe(false);
      expect(id.endsWith('-')).toBe(false);
    }
  });

  it('guarantees exact IDs required by accessibility specifications', () => {
    expect(layoutText.MAIN_CONTENT_ID).toBe('main-content');
    expect(layoutText.CONTACT_REGION_ID).toBe('contact');
    expect(layoutText.SKIP_LINK_TEXT).toBe('Skip to main content');
    expect(layoutText.MENU_BUTTON_LABEL).toBe('Menu');
    expect(layoutText.PRIMARY_NAV_LABEL).toBe('Primary');
    expect(layoutText.FOOTER_NAV_LABEL).toBe('Footer');
  });
});
'@ | Set-Content "tests\unit\components\layout\layout-text.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/layout-text.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.5, Req 2.4, Req 4.4, Req 6.3, Req 7.2, Req 8.4

---

### M4.G1.T9: Author Fixture Sanity and Validation Tests (`tests/fixtures/site-config.test.ts`)

**Objective:** Create `tests/fixtures/site-config.test.ts` verifying that all test fixtures adhere to `SiteConfig` contracts, contain expected edge cases, and validate against the M2 Zod schema.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/site-config.test.ts` created
- ✓ Validates `validSiteConfig` contains non-empty navigation, profile, and contact channels
- ✓ Validates `noPrimaryChannelSiteConfig` has 0 primary contact channels
- ✓ Validates `emptyContactChannelsSiteConfig` has `contactChannels.length === 0`
- ✓ Validates `emptySocialLinksSiteConfig` has `socialLinks.length === 0`
- ✓ Validates `reorderedNavSiteConfig` contains custom routes
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G1.T1 completed (`tests/fixtures/site-config.ts` exists)
- Target file: `tests/fixtures/site-config.test.ts`

**Implementation Details:**

Write fixture sanity tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import { describe, it, expect } from 'vitest';
import {
  validSiteConfig,
  noPrimaryChannelSiteConfig,
  emptyContactChannelsSiteConfig,
  emptySocialLinksSiteConfig,
  reorderedNavSiteConfig,
} from './site-config';

describe('SiteConfig Test Fixtures Sanity', () => {
  it('validates structure of validSiteConfig', () => {
    expect(validSiteConfig.siteName).toBe('Angelo Andres');
    expect(validSiteConfig.siteUrl.startsWith('https://')).toBe(true);
    expect(validSiteConfig.navigation.length).toBe(4);
    expect(validSiteConfig.contactChannels.some((c) => c.isPrimary)).toBe(true);
    expect(validSiteConfig.socialLinks.length).toBeGreaterThan(0);
  });

  it('validates noPrimaryChannelSiteConfig has zero primary channels', () => {
    const primaryCount = noPrimaryChannelSiteConfig.contactChannels.filter((c) => c.isPrimary).length;
    expect(primaryCount).toBe(0);
    expect(noPrimaryChannelSiteConfig.contactChannels.length).toBeGreaterThan(0);
  });

  it('validates empty array edge case fixtures', () => {
    expect(emptyContactChannelsSiteConfig.contactChannels).toEqual([]);
    expect(emptySocialLinksSiteConfig.socialLinks).toEqual([]);
  });

  it('validates reordered navigation fixture', () => {
    const hrefs = reorderedNavSiteConfig.navigation.map((n) => n.href);
    expect(hrefs[0]).toBe('/blog');
    expect(hrefs).toContain('/docs');
  });
});
'@ | Set-Content "tests\fixtures\site-config.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/fixtures/site-config.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.2, Req 15.5

---

### M4.G1.T10: Checkpoint — Fixtures and Foundation Quality Gates

**Objective:** Execute the full verification suite to confirm that all fixtures, constants, and test helpers compile cleanly and pass tests, and prove that root styling and UI primitives remain completely unmodified.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts src/app/globals.css src/components/ui/` produces zero output
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test -- tests/unit/components/layout/layout-text.test.ts tests/fixtures/site-config.test.ts` passes with code 0

**Prerequisites:**
- M4.G1.T1 through M4.G1.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/
if ($diff.Length -gt 0) {
    Write-Error "CRITICAL: Protected files modified:`n$diff"
    exit 1
}

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/layout-text.test.ts tests/fixtures/site-config.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/layout-text.test.ts tests/fixtures/site-config.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($diff.Length -eq 0 -and $t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.6, Req 2.3, Req 13.7, Req 14.4, Req 14.7, Req 15.8

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "tests\fixtures\site-config.ts"
Test-Path "tests\fixtures\site-config-arbitraries.ts"
Test-Path "src\components\layout\layout-text.ts"
Test-Path "tests\unit\components\layout\layout-text.test.ts"
Test-Path "tests\fixtures\site-config.test.ts"
Test-Path ".kiro\specs\m4-global-layout-navigation\task-notes.md"
npm run typecheck
npm run test -- tests/unit/components/layout/layout-text.test.ts tests/fixtures/site-config.test.ts
```
Expected output:
- `True` for all 6 file existence checks
- `npm run typecheck` exits with return code 0
- Vitest executes all fixture and layout-text tests with return code 0.