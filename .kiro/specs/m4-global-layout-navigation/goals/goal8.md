# M4.G8: Responsive Verification and Token/Scope Compliance

> **Milestone:** M4 — Global Layout & Navigation  
> **Goal:** G8 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Conduct an exhaustive responsive design audit and design-token compliance verification across all Milestone 4 layout components (`SiteHeader`, `PrimaryNav`, `MobileNavToggle`, `SkipLink`, `SiteFooter`, `ContactLinks`, and `NotFound`). Ensure responsive layout switches strictly employ standard Tailwind breakpoints (`lg:` for navigation expansion, `md:` for footer multi-column layouts) without raw pixel widths or arbitrary Tailwind brackets (`w-[`, `min-w-[`). Verify that mobile touch targets achieve the mandatory minimum 44px by 44px sizing (`min-h-12 min-w-12`), text wrapping safeguards (`break-words`, `flex-wrap`) prevent horizontal page scroll at 375px mobile viewport widths, and content remains fully readable when text is scaled to 200%. Verify that M3 UI primitives (`Container`, `Button`, `ExternalLink`, `FOCUS_RING`, `MOTION_FAST`, `cx`) are composed faithfully without local redefinition, and confirm via `git diff` that `tailwind.config.ts`, `globals.css`, and `src/components/ui/` remain completely untouched. Formally document the manual responsive verification checklist in `task-notes.md`.

## Goal Success Criteria

- ✓ All M4 layout files utilize standard Tailwind breakpoints (`lg:` header switch, `md:` footer columns)
- ✓ Zero arbitrary Tailwind dimension classes (`w-[`, `min-w-[`, `h-[`, `p-[`) in any M4 layout or app file
- ✓ Mobile toggle button and primary navigation links satisfy minimum 44px touch targets via `min-h-12` (48px)
- ✓ Header flex containers apply `flex-wrap` and label text wraps without forcing horizontal document scrolling at 375px
- ✓ Static analysis confirms M3 `Container` is used by `SiteHeader`, `SiteFooter`, and `NotFound`
- ✓ Static analysis confirms M3 `ExternalLink` is used for all external non-`mailto:` destinations
- ✓ Static analysis confirms M3 `Button` is used for header contact action and not-found home link
- ✓ Static analysis confirms M3 `FOCUS_RING` is applied to every interactive control
- ✓ `git diff` confirms zero changes to `tailwind.config.ts`, `src/app/globals.css`, or `src/components/ui/`
- ✓ Detailed manual responsive verification procedure (375px, 768px, 1024px, 1440px, and 200% zoom) documented in `task-notes.md`
- ✓ `tests/unit/components/layout/compliance.test.ts` passes with 100% assertions

## Prerequisites

- Goals M4.G1 through M4.G7 completed (all layout components and app files exist)
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`

---

## Tasks

### M4.G8.T1: Audit Breakpoint Utilities and Absence of Arbitrary Dimension Classes

**Objective:** Inspect all files in `src/components/layout/` and `src/app/` to ensure responsive layout behavior relies on standard Tailwind breakpoints (`md:`, `lg:`) and contains zero arbitrary dimension brackets `[` or `]`.

**Acceptance Criteria:**
- ✓ Scans all layout and app source files
- ✓ Confirms header switch uses `lg:` (`lg:hidden` on toggle, `lg:flex` on nav list)
- ✓ Confirms footer column grid uses `md:` (`grid-cols-1 md:grid-cols-3`)
- ✓ Confirms zero occurrences of arbitrary dimension utilities (`w-[`, `min-w-[`, `h-[`, `min-h-[`, `p-[`, `px-[`, `py-[`)
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M4.G3, M4.G4, M4.G5, M4.G6, M4.G7 completed

**Implementation Details:**

Execute breakpoint audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$targetDirs = @("src\components\layout", "src\app")
$files = Get-ChildItem -Path $targetDirs -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $arbitraryMatches = [regex]::Matches($content, '(?:w|min-w|max-w|h|min-h|p|px|py|m|mx|my)-\[[^\]]+\]')
    foreach ($m in $arbitraryMatches) {
        $violations += "Arbitrary dimension class found in $($file.Name): $($m.Value)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.6, Req 13.5, Req 13.6

---

### M4.G8.T2: Verify Mobile Touch Targets and Overflow Safeguards

**Objective:** Audit `src/components/layout/mobile-nav-toggle.tsx` and `site-header.tsx` to verify touch target minimums of 44px by 44px (`min-h-12 min-w-12`) and flex container wrapping safeguards against horizontal scroll.

**Acceptance Criteria:**
- ✓ Confirms toggle button includes `min-h-12 min-w-12` (48px $\ge$ 44px minimum target, Req 12.5)
- ✓ Confirms navigation links include `min-h-12`
- ✓ Confirms header container includes `flex-wrap` to accommodate 200% text zoom
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G3 and M4.G4 completed

**Implementation Details:**

Execute touch target and overflow check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$toggleFile = "src\components\layout\mobile-nav-toggle.tsx"
$headerFile = "src\components\layout\site-header.tsx"
$violations = @()

$toggleContent = Get-Content $toggleFile -Raw
if (-not ($toggleContent -match 'min-h-12') -or -not ($toggleContent -match 'min-w-12')) {
    $violations += "mobile-nav-toggle.tsx must specify min-h-12 and min-w-12 for touch targets (Req 12.5)"
}

$headerContent = Get-Content $headerFile -Raw
if (-not ($headerContent -match 'flex-wrap')) {
    $violations += "site-header.tsx must declare flex-wrap to prevent overflow at 200% zoom (Req 12.7)"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.5, Req 12.7

---

### M4.G8.T3: Verify Composition of M3 UI Primitives

**Objective:** Perform static analysis on M4 components to confirm mandatory composition of M3 primitives (`Container`, `ExternalLink`, `Button`) without raw external anchor elements.

**Acceptance Criteria:**
- ✓ `SiteHeader`, `SiteFooter`, and `NotFound` import and render `Container`
- ✓ `SiteFooter` and `ContactLinks` import and render `ExternalLink` for external destinations
- ✓ `SiteHeader` and `NotFound` import and render `Button`
- ✓ Confirms zero raw `<a ` tags with `target="_blank"` exist in `src/components/layout/`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- M4.G4, M4.G5, M4.G7 completed

**Implementation Details:**

Execute primitive composition audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$violations = @()

# 1. Check Container usage
$containerConsumers = @(
    "src\components\layout\site-header.tsx",
    "src\components\layout\site-footer.tsx",
    "src\app\not-found.tsx"
)
foreach ($f in $containerConsumers) {
    $content = Get-Content $f -Raw
    if (-not ($content -match '\bContainer\b')) {
        $violations += "$f must import and render Container primitive (Req 13.1)"
    }
}

# 2. Check Button usage
$buttonConsumers = @(
    "src\components\layout\site-header.tsx",
    "src\app\not-found.tsx"
)
foreach ($f in $buttonConsumers) {
    $content = Get-Content $f -Raw
    if (-not ($content -match '\bButton\b')) {
        $violations += "$f must import and render Button primitive (Req 13.3)"
    }
}

# 3. Check ExternalLink usage
$externalConsumers = @(
    "src\components\layout\contact-links.tsx",
    "src\components\layout\site-footer.tsx"
)
foreach ($f in $externalConsumers) {
    $content = Get-Content $f -Raw
    if (-not ($content -match '\bExternalLink\b')) {
        $violations += "$f must import and render ExternalLink primitive (Req 13.2)"
    }
}

# 4. Check absence of raw <a target="_blank">
$layoutFiles = Get-ChildItem -Path "src\components\layout" -Filter "*.tsx"
foreach ($f in $layoutFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match '<a\b[^>]*\btarget\s*=\s*["'']_blank["'']') {
        $violations += "Raw <a target='_blank'> found in $($f.Name). Must use ExternalLink primitive (Req 13.2)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.1, Req 13.2, Req 13.3

---

### M4.G8.T4: Verify Focus Ring Composition on All Interactive Elements

**Objective:** Audit all interactive elements across M4 components to verify that each composes M3's `FOCUS_RING` helper (`focus-visible:ring-focus-ring`) and that the sole `focus:outline-none` exception on `main` is justified.

**Acceptance Criteria:**
- ✓ `MobileNavToggle` button and links compose `FOCUS_RING`
- ✓ `SiteHeader` identity link composes `FOCUS_RING`
- ✓ `SkipLink` composes `FOCUS_RING`
- ✓ `SiteFooter` navigation links compose `FOCUS_RING`
- ✓ `ContactLinks` email link composes `FOCUS_RING`
- ✓ `NotFound` section links compose `FOCUS_RING`
- ✓ `src/app/layout.tsx` contains an explanatory comment for `focus:outline-none` on `main`
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M4.G3 through M4.G7 completed

**Implementation Details:**

Execute focus ring composition check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$interactiveFiles = @(
    "src\components\layout\mobile-nav-toggle.tsx",
    "src\components\layout\site-header.tsx",
    "src\components\layout\skip-link.tsx",
    "src\components\layout\site-footer.tsx",
    "src\components\layout\contact-links.tsx",
    "src\app\not-found.tsx"
)
$violations = @()

foreach ($f in $interactiveFiles) {
    $content = Get-Content $f -Raw
    if (-not ($content -match '\bFOCUS_RING\b')) {
        $violations += "$f does not import or apply FOCUS_RING helper (Req 13.4)"
    }
}

$layoutContent = Get-Content "src\app\layout.tsx" -Raw
if (-not ($layoutContent -match 'focus:outline-none')) {
    $violations += "layout.tsx must apply focus:outline-none to non-interactive main container"
}
if (-not ($layoutContent -match '//[\s\S]*main is given tabIndex')) {
    $violations += "layout.tsx must document the focus:outline-none exception on main"
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 7.3, Req 7.5, Req 11.3, Req 13.4

---

### M4.G8.T5: Audit Semantic Tokens and Absence of Dark Mode Classes

**Objective:** Audit all layout and app files to ensure visual values are styled exclusively via semantic tokens, containing zero raw hex codes, zero `rgb(`/`rgba(`, and zero `dark:` utility overrides.

**Acceptance Criteria:**
- ✓ Scans all `.ts` and `.tsx` files under `src/components/layout/` and `src/app/`
- ✓ Zero raw hex color codes (`#[0-9A-Fa-f]{3,8}`)
- ✓ Zero `rgb(`/`rgba(`
- ✓ Zero `dark:` utilities
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Goals M4.G3 through M4.G7 completed

**Implementation Details:**

Execute token audit using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$targetDirs = @("src\components\layout", "src\app")
$files = Get-ChildItem -Path $targetDirs -Include *.ts, *.tsx -Recurse
$violations = @()

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw

    if ($content -match '#[0-9A-Fa-f]{3,8}\b') {
        $violations += "Raw hex color found in $($file.Name)"
    }
    if ($content -match 'rgba?\(') {
        $violations += "Raw rgb/rgba color found in $($file.Name)"
    }
    if ($content -match '\bdark:[a-zA-Z0-9_\-]+') {
        $violations += "Forbidden dark: utility found in $($file.Name) (dark mode off by default, Req 13.9)"
    }
}

if ($violations.Count -eq 0) { "PASS" } else { $violations | ForEach-Object { Write-Host $_ }; "FAIL" }
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.5, Req 13.6, Req 13.9

---

### M4.G8.T6: Document Detailed Manual Responsive Protocol in `task-notes.md`

**Objective:** Append the comprehensive step-by-step manual responsive verification protocol across the canonical breakpoints (375px, 768px, 1024px, 1440px) and 200% text zoom into `task-notes.md`.

**Acceptance Criteria:**
- ✓ File `.kiro/specs/m4-global-layout-navigation/task-notes.md` updated
- ✓ Documents 375px mobile test: verify toggle visible, nav collapsed, header action hidden, zero horizontal scroll
- ✓ Documents 768px tablet test: verify footer stacks into 3 columns, mobile menu operational
- ✓ Documents 1024px desktop test: verify toggle hidden, horizontal nav visible, desktop contact action shown
- ✓ Documents 1440px wide desktop test: verify centering within `max-w-screen-xl`
- ✓ Documents 200% zoom test: verify layout wraps without clipping or trapping

**Prerequisites:**
- `task-notes.md` exists (created in M4.G1.T5)

**Implementation Details:**

Append responsive protocol to `task-notes.md` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$protocolNotes = @'

## 3. Manual Responsive & Viewport Verification Protocol (Req 12.1, 12.7, 15 manual)

The following verification steps must be manually validated in Chromium and WebKit DevTools prior to milestone closure:

1. **Mobile Viewport (375px width — iPhone SE / Small Viewport):**
   - Toggle button is visible (`lg:hidden`).
   - Primary navigation list is hidden (`hidden lg:flex`).
   - Desktop header contact action is hidden (`hidden lg:block`).
   - Footer renders sections stacked in a single vertical column (`grid-cols-1`).
   - Run in Console: `document.documentElement.scrollWidth <= window.innerWidth`. Expected: `true`. Zero horizontal scrolling.
   - Activating toggle expands dropdown menu cleanly below header.
2. **Tablet Viewport (768px width — iPad Mini):**
   - Toggle button remains visible (`md` is below `lg: 1024px`).
   - Footer transitions into 3-column grid (`md:grid-cols-3`).
   - Zero horizontal overflow.
3. **Desktop Viewport (1024px width):**
   - Toggle button is completely hidden (`lg:hidden`).
   - Primary navigation entries expand horizontally (`lg:flex lg:flex-row`).
   - Desktop header primary contact action becomes visible (`lg:block`).
4. **Wide Desktop Viewport (1440px+ width):**
   - Content container width is capped at 1280px (`max-w-screen-xl`).
   - Header, main content, and footer remain centered horizontally (`mx-auto`).
5. **200% Text Scaling & Zoom (WCAG 2.1 AA 1.4.4):**
   - In browser settings, set Zoom to 200% at 1024px width.
   - Verify header row wraps (`flex-wrap`) cleanly without text clipping or button overlapping.
   - Verify touch targets maintain comfortable accessibility spacing.
'@

Add-Content -Path ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Value $protocolNotes -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$notes = Get-Content ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Raw
if ($notes -match "Manual Responsive & Viewport Verification Protocol") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.3, Req 12.4, Req 12.7

---

### M4.G8.T7: Author Automated Layout Compliance Test (`tests/unit/components/layout/compliance.test.ts`)

**Objective:** Create `tests/unit/components/layout/compliance.test.ts` running static analysis assertions on layout source code to verify token and primitive compliance.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/layout/compliance.test.ts` created
- ✓ Tests zero arbitrary brackets `[` or `]` in layout and app files
- ✓ Tests zero raw hex colors exist in layout files
- ✓ Tests zero `dark:` utilities exist in layout files
- ✓ Tests mandatory M3 primitive imports (`Container`, `FOCUS_RING`, `MOTION_FAST`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M4.G8.T1 through M4.G8.T5 completed
- Target file: `tests/unit/components/layout/compliance.test.ts`

**Implementation Details:**

Write `tests/unit/components/layout/compliance.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

@'
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

describe('Layout Compliance & Token Adherence (Req 12, 13)', () => {
  const layoutDir = path.join(process.cwd(), 'src', 'components', 'layout');
  const appDir = path.join(process.cwd(), 'src', 'app');

  const getFiles = (dir: string): string[] => {
    return fs.readdirSync(dir)
      .filter((f) => f.endsWith('.ts') || f.endsWith('.tsx'))
      .map((f) => path.join(dir, f));
  };

  const allFiles = [...getFiles(layoutDir), ...getFiles(appDir)];

  it('contains zero arbitrary dimension Tailwind classes', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);
      const arbitraryMatches = content.match(/(?:w|min-w|max-w|h|min-h|p|px|py|m|mx|my)-\[[^\]]+\]/g);
      expect(arbitraryMatches, `Arbitrary dimension class found in ${filename}`).toBeNull();
    }
  });

  it('contains zero raw hex or rgb/rgba color declarations', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);
      expect(content.match(/#[0-9A-Fa-f]{3,8}\b/g), `Raw hex color in ${filename}`).toBeNull();
      expect(content.match(/rgba?\(/gi), `Raw RGB/RGBA in ${filename}`).toBeNull();
    }
  });

  it('contains zero dark: utility overrides', () => {
    for (const file of allFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      const filename = path.basename(file);
      expect(content.match(/\bdark:[a-zA-Z0-9_\-]+/g), `dark: class found in ${filename}`).toBeNull();
    }
  });

  it('enforces Container primitive usage in top-level containers', () => {
    const consumers = ['site-header.tsx', 'site-footer.tsx', 'not-found.tsx'];
    for (const consumer of consumers) {
      const filePath = allFiles.find((f) => f.endsWith(consumer));
      expect(filePath, `Consumer file ${consumer} must exist`).toBeDefined();
      const content = fs.readFileSync(filePath!, 'utf-8');
      expect(content).toContain('Container');
    }
  });
});
'@ | Set-Content "tests\unit\components\layout\compliance.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run test -- tests/unit/components/layout/compliance.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.6, Req 13.1, Req 13.5, Req 13.6, Req 13.9

---

### M4.G8.T8: Verify Protected Files Invariance via `git diff`

**Objective:** Execute `git diff` on `src/components/ui/`, `tailwind.config.ts`, and `globals.css` to confirm that Milestone 4 consumed primitives and tokens without modifying upstream design system foundations.

**Acceptance Criteria:**
- ✓ `git diff src/components/ui/` produces zero output
- ✓ `git diff tailwind.config.ts` produces zero output
- ✓ `git diff src/app/globals.css` produces zero output
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- Project root exists

**Implementation Details:**

Execute diff check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/
if ($diff.Length -eq 0) {
    "PASS"
} else {
    Write-Host "CRITICAL: Upstream protected files modified!`n$diff"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.6, Req 13.7

---

### M4.G8.T9: Audit and Record Missing Tokens in `task-notes.md`

**Objective:** Confirm that any missing token requirements (such as custom z-index elevation tokens for `SkipLink`) remain logged in `task-notes.md` and are not patched without human approval per Requirement 13.8.

**Acceptance Criteria:**
- ✓ Confirms `task-notes.md` contains the `z-50` gap entry
- ✓ Confirms zero edits to root Tailwind configuration
- ✓ PowerShell verification script exits with PASS

**Prerequisites:**
- `task-notes.md` exists

**Implementation Details:**

Execute gap audit check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

$notes = Get-Content ".kiro\specs\m4-global-layout-navigation\task-notes.md" -Raw
if ($notes.Contains("SkipLink Stacking (`z-50`)")) {
    "PASS"
} else {
    Write-Host "Missing z-50 token gap entry in task-notes.md"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 13.8

---

### M4.G8.T10: Checkpoint — Responsive and Token Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across layout compliance and responsive testing suites.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test` runs compliance test and passes with code 0
- ✓ Zero regressions introduced

**Prerequisites:**
- M4.G8.T1 through M4.G8.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"

npm run typecheck
npm run lint
npm run test -- tests/unit/components/layout/compliance.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/layout/compliance.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 15.8, Req 16.1

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 8 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Test-Path "tests\unit\components\layout\compliance.test.ts"
Test-Path ".kiro\specs\m4-global-layout-navigation\task-notes.md"
npm run typecheck
npm run test -- tests/unit/components/layout/compliance.test.ts
```
Expected output:
- `True` for both paths
- `npm run typecheck` exits with return code 0
- Vitest executes compliance tests with return code 0.