***

# M1.G3: Tailwind CSS & Design Token Configuration

> **Milestone:** M1 — Repository Foundation & Toolchain  
> **Goal:** G3 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Configure Tailwind CSS and global stylesheets to map all SGDS-inspired design tokens defined in `design.md` Section 3. This establishes semantic color mappings (with automatic dark mode support via CSS custom properties), spacing scales (4px base unit), typography scales, border radii, box-shadow elevations, and transition durations without hardcoded raw hex or arbitrary pixel values in components.

## Goal Success Criteria

- ✓ `tailwind.config.ts` extends the theme with semantic tokens for background, text, border, brand, feedback, and focus states
- ✓ `tailwind.config.ts` defines spacing scale (`1` through `24`), typography scale (`caption` through `heading-1`), border radius (`sm` through `full`), elevation shadows (`elevation-0` through `elevation-2`), and motion timings (`fast`, `standard`)
- ✓ `src/app/globals.css` declares `:root` CSS custom variables for light mode and `@media (prefers-color-scheme: dark)` overrides for dark mode
- ✓ `src/app/globals.css` injects Tailwind directives (`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`) and default element focus ring styling
- ✓ Next.js static asset and CSS compilation build succeeds without purge warnings or CSS syntax errors

## Prerequisites

- Goal M1.G1 and M1.G2 completed
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\`
- `tailwind.config.ts` and `src/app/globals.css` exist from the initial Next.js scaffold

---

## Tasks

### M1.G3.T1: Audit baseline `tailwind.config.ts` and `globals.css`

**Objective:** Inspect existing Tailwind configuration and global styles to verify current scan paths and directive setup before injecting SGDS design tokens.

**Acceptance Criteria:**
- ✓ `tailwind.config.ts` exists in the project root
- ✓ `src/app/globals.css` exists
- ✓ Content array includes `./src/**/*.{js,ts,jsx,tsx,mdx}`
- ✓ File contents are verified via PowerShell

**Prerequisites:**
- Project root exists at `c:\dev\andres-webapp-professional\personal-website-portfolio\`

**Implementation Details:**
Execute the following PowerShell script to check both files:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Get-Content "tailwind.config.ts" -Raw
Get-Content "src\app\globals.css" -Raw
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
if ((Test-Path "tailwind.config.ts") -and (Test-Path "src\app\globals.css")) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.9, Req 3.12

---

### M1.G3.T2: Configure Content Scan Paths and Theme Extension Skeleton

**Objective:** Set up the basic TypeScript Config export structure in `tailwind.config.ts` targeting all source files including MDX content.

**Acceptance Criteria:**
- ✓ `tailwind.config.ts` imports `Config` type from `'tailwindcss'`
- ✓ `content` array includes `'./src/**/*.{js,ts,jsx,tsx,mdx}'`
- ✓ `theme.extend` object is defined

**Prerequisites:**
- M1.G3.T1 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tailwind.config.ts`

**Implementation Details:**
Write the foundational structure to `tailwind.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
'@ | Set-Content "tailwind.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$content = Get-Content "tailwind.config.ts" -Raw
if ($content -match "\./src/\*\*/\*\.\{js,ts,jsx,tsx,mdx\}") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.1, Req 3.9

---

### M1.G3.T3: Add Semantic Color Tokens to `tailwind.config.ts`

**Objective:** Map all semantic background, text, border, brand, feedback, and focus CSS variables into `theme.extend.colors`.

**Acceptance Criteria:**
- ✓ Background colors mapped: `page`, `surface`, `inverse`
- ✓ Text colors mapped: `text-primary`, `text-secondary`, `text-disabled`
- ✓ Border colors mapped: `border-default`, `border-strong`
- ✓ Brand colors mapped: `brand-primary`, `brand-secondary`
- ✓ Feedback colors mapped: `feedback-success`, `feedback-warning`, `feedback-danger`
- ✓ Focus token mapped: `focus-ring`
- ✓ All values use `var(--color-*)` syntax

**Prerequisites:**
- M1.G3.T2 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tailwind.config.ts`

**Implementation Details:**
Update `tailwind.config.ts` with color token bindings:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        page: 'var(--color-bg-page)',
        surface: 'var(--color-bg-surface)',
        inverse: 'var(--color-bg-inverse)',
        'text-primary': 'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
        'text-disabled': 'var(--color-text-disabled)',
        'border-default': 'var(--color-border-default)',
        'border-strong': 'var(--color-border-strong)',
        'brand-primary': 'var(--color-brand-primary)',
        'brand-secondary': 'var(--color-brand-secondary)',
        'feedback-success': 'var(--color-feedback-success)',
        'feedback-warning': 'var(--color-feedback-warning)',
        'feedback-danger': 'var(--color-feedback-danger)',
        'focus-ring': 'var(--color-focus-ring)',
      },
    },
  },
  plugins: [],
};

export default config;
'@ | Set-Content "tailwind.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
if ($cfg -match "'brand-primary': 'var\(--color-brand-primary\)'" -and $cfg -match "'focus-ring': 'var\(--color-focus-ring\)'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.2, Req 3.3, Req 3.10

---

### M1.G3.T4: Add Spacing Scale Tokens to `tailwind.config.ts`

**Objective:** Map the 4px base-unit spacing scale (`space-1` through `space-24`) to Tailwind spacing extensions.

**Acceptance Criteria:**
- ✓ Spacing tokens defined: `1` (0.25rem / 4px), `2` (0.5rem / 8px), `3` (0.75rem / 12px), `4` (1rem / 16px), `6` (1.5rem / 24px), `8` (2rem / 32px), `12` (3rem / 48px), `16` (4rem / 64px), `24` (6rem / 96px)
- ✓ Keys are added to `theme.extend.spacing`

**Prerequisites:**
- M1.G3.T3 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tailwind.config.ts`

**Implementation Details:**
Incorporate the spacing tokens into `tailwind.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
$spacingBlock = @'
      spacing: {
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '6': '1.5rem',
        '8': '2rem',
        '12': '3rem',
        '16': '4rem',
        '24': '6rem',
      },
'@
$cfg = $cfg -replace "colors:\s*\{[^}]+\},", "`$0`n$spacingBlock"
$cfg | Set-Content "tailwind.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
if ($cfg -match "'24': '6rem'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.4

---

### M1.G3.T5: Add Typography Scale Tokens to `tailwind.config.ts`

**Objective:** Map the 8 semantic font-size tokens with explicit line-height pairings per `design.md` Section 3.2.

**Acceptance Criteria:**
- ✓ Typography tokens defined:
  - `caption`: `['0.75rem', { lineHeight: '1rem' }]` (12px/16px)
  - `small`: `['0.875rem', { lineHeight: '1.25rem' }]` (14px/20px)
  - `body`: `['1rem', { lineHeight: '1.5rem' }]` (16px/24px)
  - `lead`: `['1.125rem', { lineHeight: '1.75rem' }]` (18px/28px)
  - `heading-4`: `['1.25rem', { lineHeight: '1.75rem' }]` (20px/28px)
  - `heading-3`: `['1.5rem', { lineHeight: '2rem' }]` (24px/32px)
  - `heading-2`: `['1.875rem', { lineHeight: '2.375rem' }]` (30px/38px)
  - `heading-1`: `['2.375rem', { lineHeight: '2.875rem' }]` (38px/46px)
- ✓ Keys are added to `theme.extend.fontSize`

**Prerequisites:**
- M1.G3.T4 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tailwind.config.ts`

**Implementation Details:**
Append the fontSize block to `tailwind.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
$fontBlock = @'
      fontSize: {
        'caption': ['0.75rem', { lineHeight: '1rem' }],
        'small': ['0.875rem', { lineHeight: '1.25rem' }],
        'body': ['1rem', { lineHeight: '1.5rem' }],
        'lead': ['1.125rem', { lineHeight: '1.75rem' }],
        'heading-4': ['1.25rem', { lineHeight: '1.75rem' }],
        'heading-3': ['1.5rem', { lineHeight: '2rem' }],
        'heading-2': ['1.875rem', { lineHeight: '2.375rem' }],
        'heading-1': ['2.375rem', { lineHeight: '2.875rem' }],
      },
'@
$cfg = $cfg -replace "spacing:\s*\{[^}]+\},", "`$0`n$fontBlock"
$cfg | Set-Content "tailwind.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
if ($cfg -match "'heading-1': \['2.375rem', \{ lineHeight: '2.875rem' \}\]" -and $cfg -match "'caption': \['0.75rem'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.5

---

### M1.G3.T6: Add Border Radius, Elevation, Motion, and Font Family Tokens

**Objective:** Add tokens for border radii (`sm`, `md`, `lg`, `full`), elevation shadows (`elevation-0`, `elevation-1`, `elevation-2`), motion timing, and typography font families.

**Acceptance Criteria:**
- ✓ `borderRadius` includes `sm`, `md`, `lg`, and `full`
- ✓ `boxShadow` includes `elevation-0`, `elevation-1`, and `elevation-2`
- ✓ `transitionDuration` includes `fast` (150ms) and `standard` (250ms)
- ✓ `fontFamily` includes `sans` (Inter) and `mono` (JetBrains Mono)

**Prerequisites:**
- M1.G3.T5 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\tailwind.config.ts`

**Implementation Details:**
Write the finalized, complete `tailwind.config.ts`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        page: 'var(--color-bg-page)',
        surface: 'var(--color-bg-surface)',
        inverse: 'var(--color-bg-inverse)',
        'text-primary': 'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
        'text-disabled': 'var(--color-text-disabled)',
        'border-default': 'var(--color-border-default)',
        'border-strong': 'var(--color-border-strong)',
        'brand-primary': 'var(--color-brand-primary)',
        'brand-secondary': 'var(--color-brand-secondary)',
        'feedback-success': 'var(--color-feedback-success)',
        'feedback-warning': 'var(--color-feedback-warning)',
        'feedback-danger': 'var(--color-feedback-danger)',
        'focus-ring': 'var(--color-focus-ring)',
      },
      spacing: {
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '6': '1.5rem',
        '8': '2rem',
        '12': '3rem',
        '16': '4rem',
        '24': '6rem',
      },
      fontSize: {
        'caption': ['0.75rem', { lineHeight: '1rem' }],
        'small': ['0.875rem', { lineHeight: '1.25rem' }],
        'body': ['1rem', { lineHeight: '1.5rem' }],
        'lead': ['1.125rem', { lineHeight: '1.75rem' }],
        'heading-4': ['1.25rem', { lineHeight: '1.75rem' }],
        'heading-3': ['1.5rem', { lineHeight: '2rem' }],
        'heading-2': ['1.875rem', { lineHeight: '2.375rem' }],
        'heading-1': ['2.375rem', { lineHeight: '2.875rem' }],
      },
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.5rem',
        'lg': '0.75rem',
        'full': '9999px',
      },
      boxShadow: {
        'elevation-0': 'none',
        'elevation-1': '0 1px 2px rgba(11, 15, 20, 0.06)',
        'elevation-2': '0 4px 12px rgba(11, 15, 20, 0.10)',
      },
      transitionDuration: {
        'fast': '150ms',
        'standard': '250ms',
      },
      transitionTimingFunction: {
        'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['JetBrains Mono', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
'@ | Set-Content "tailwind.config.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$cfg = Get-Content "tailwind.config.ts" -Raw
if ($cfg -match "'elevation-1'" -and $cfg -match "'radius-lg'" -and $cfg -match "'fast': '150ms'") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.6, Req 3.7, Req 3.8

---

### M1.G3.T7: Define Light Mode Design Tokens in `globals.css`

**Objective:** Declare the CSS custom property mappings for light mode inside `:root` in `src/app/globals.css`.

**Acceptance Criteria:**
- ✓ `:root` block defines `--color-bg-page: #FFFFFF`
- ✓ `:root` block defines `--color-bg-surface: #F7F9FA`
- ✓ `:root` block defines `--color-bg-inverse: #0B0F14`
- ✓ `:root` block defines text, border, brand, and feedback hex colors matching `design.md` Section 3.1 exactly

**Prerequisites:**
- M1.G3.T6 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\app\globals.css`

**Implementation Details:**
Write the light mode CSS variables to `src/app/globals.css`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
@'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  /* SGDS-Inspired Semantic Tokens - Light Mode */
  --color-bg-page: #FFFFFF;
  --color-bg-surface: #F7F9FA;
  --color-bg-inverse: #0B0F14;
  --color-text-primary: #17202A;
  --color-text-secondary: #4A5A68;
  --color-text-disabled: #7A8894;
  --color-border-default: #D7DEE4;
  --color-border-strong: #17202A;
  --color-brand-primary: #0052A5;
  --color-brand-secondary: #00694E;
  --color-feedback-success: #00694E;
  --color-feedback-warning: #8A6100;
  --color-feedback-danger: #B42318;
  --color-focus-ring: #0052A5;

  /* Font variables */
  --font-sans: var(--font-inter), system-ui, -apple-system, 'Segoe UI', sans-serif;
}
'@ | Set-Content "src\app\globals.css" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$css = Get-Content "src\app\globals.css" -Raw
if ($css -match "--color-brand-primary: #0052A5;" -and $css -match "--color-bg-page: #FFFFFF;") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.10, Req 3.12

---

### M1.G3.T8: Define Dark Mode Token Overrides in `globals.css`

**Objective:** Add `@media (prefers-color-scheme: dark)` variable overrides in `src/app/globals.css` matching `design.md` Section 3.1.

**Acceptance Criteria:**
- ✓ `@media (prefers-color-scheme: dark)` overrides `--color-bg-page` to `#0B0F14`
- ✓ Overrides `--color-bg-surface` to `#131A21`
- ✓ Overrides `--color-text-primary` to `#F4F7F9`
- ✓ Overrides `--color-border-default` to `#2A3540`
- ✓ Overrides `--color-brand-primary` to `#4FA3E3`
- ✓ Overrides `--color-focus-ring` to `#4FA3E3`

**Prerequisites:**
- M1.G3.T7 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\app\globals.css`

**Implementation Details:**
Append the dark mode block to `src/app/globals.css`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$darkCss = @'

@media (prefers-color-scheme: dark) {
  :root {
    /* SGDS-Inspired Semantic Tokens - Dark Mode */
    --color-bg-page: #0B0F14;
    --color-bg-surface: #131A21;
    --color-bg-inverse: #F7F9FA;
    --color-text-primary: #F4F7F9;
    --color-text-secondary: #B8C4CE;
    --color-text-disabled: #7A8894;
    --color-border-default: #2A3540;
    --color-border-strong: #F4F7F9;
    --color-brand-primary: #4FA3E3;
    --color-brand-secondary: #4FC49B;
    --color-feedback-success: #4FC49B;
    --color-feedback-warning: #E8B339;
    --color-feedback-danger: #F97066;
    --color-focus-ring: #4FA3E3;
  }
}
'@
Add-Content -Path "src\app\globals.css" -Value $darkCss -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$css = Get-Content "src\app\globals.css" -Raw
if ($css -match "prefers-color-scheme: dark" -and $css -match "--color-brand-primary: #4FA3E3;") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.10

---

### M1.G3.T9: Configure Base Layer and Focus Ring Standards in `globals.css`

**Objective:** Apply default border colors and accessible focus rings via `@layer base` in `src/app/globals.css`.

**Acceptance Criteria:**
- ✓ `@layer base` configures `*` with `@apply border-border-default;`
- ✓ `@layer base` configures `body` with `@apply font-sans;`
- ✓ Accessible `:focus-visible` ring rule is declared using `ring-focus-ring`

**Prerequisites:**
- M1.G3.T8 completed
- Target file: `c:\dev\andres-webapp-professional\personal-website-portfolio\src\app\globals.css`

**Implementation Details:**
Append the `@layer base` configuration to `src/app/globals.css`:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$baseLayer = @'

@layer base {
  * {
    @apply border-border-default;
  }

  body {
    @apply font-sans;
  }

  /* Focus visible accessibility styles */
  *:focus-visible {
    @apply outline-none ring-2 ring-focus-ring ring-offset-2;
  }
}
'@
Add-Content -Path "src\app\globals.css" -Value $baseLayer -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
$css = Get-Content "src\app\globals.css" -Raw
if ($css -match "@layer base" -and $css -match "ring-focus-ring") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.3, Req 3.11, Req 3.12

---

### M1.G3.T10: Validate PostCSS Processing and Build Output

**Objective:** Run `next build` (or build script) to ensure Tailwind CSS and PostCSS process all semantic classes without syntax or bundle errors.

**Acceptance Criteria:**
- ✓ `npm run build` executes successfully
- ✓ PostCSS processes `globals.css` without errors
- ✓ Build completes with exit code 0

**Prerequisites:**
- M1.G3.T1 through M1.G3.T9 completed

**Implementation Details:**
Execute the Next.js production build:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
npm run build
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 3.11, Req 11.5, Req 13.7

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 3 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio"
Get-Content "tailwind.config.ts" | Select-String "page:", "brand-primary:", "elevation-1:"
Get-Content "src\app\globals.css" | Select-String "--color-brand-primary", "prefers-color-scheme"
npm run build
```
Expected output:
- Matches found for semantic tokens in both `tailwind.config.ts` and `src\app\globals.css`
- `npm run build` exits with return code 0.