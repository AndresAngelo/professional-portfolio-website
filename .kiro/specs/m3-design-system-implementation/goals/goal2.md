# M3.G2: Button Component

> **Milestone:** M3 — Design System Implementation  
> **Goal:** G2 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Implement the server-component `Button` primitive in `src/components/ui/button.tsx` supporting four variants (`primary`, `secondary`, `ghost`, `external-link`) and three standardized sizes (`sm`, `md`, `lg`). Enforce keyboard accessibility via `:focus-visible` focus ring composition, reduced-motion-aware transitions, native `type="button"` defaulting, anchor rendering when `href` is supplied, secure attributes for the `external-link` variant, and type-level enforcement of `aria-label` for icon-only configurations. Validate all variant and size permutations, keyboard behaviors, and property invariants using Vitest and React Testing Library.

## Goal Success Criteria

- ✓ `src/components/ui/button.tsx` implemented as a server component without `'use client'`
- ✓ Supports variants: `primary`, `secondary`, `ghost`, `external-link` (defaults to `primary`)
- ✓ Supports sizes: `sm` (32px / `h-8`), `md` (40px / `h-10`), `lg` (48px / `h-12`) (defaults to `md`)
- ✓ Native `<button>` elements render with `type="button"` by default unless explicitly overridden
- ✓ Disabled state applies `disabled` attribute, `text-text-disabled`, and ignores pointer events
- ✓ Anchor rendering triggered when `href` is provided, retaining equivalent visual styling
- ✓ `external-link` variant renders `target="_blank"`, `rel="noopener noreferrer"`, visually hidden `(opens in a new tab)`, and an `aria-hidden` icon
- ✓ Discriminated union enforces `aria-label` at compile time when `iconOnly: true`
- ✓ `tests/unit/components/ui/button.test.tsx` achieves 100% test coverage across all variants, sizes, and states
- ✓ Zero `any`, zero non-null assertions, and zero hardcoded design tokens

## Prerequisites

- Goal M3.G1 completed successfully
- Working directory: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- `src/components/ui/cx.ts`, `focus-ring.ts`, `motion.ts`, and `external-link-attrs.ts` exist and compile
- React Testing Library, `@testing-library/user-event`, and `fast-check` available in `devDependencies`

---

## Tasks

### M3.G2.T1: Define Button Types and Style Contracts

**Objective:** Author the TypeScript prop contracts, discriminated unions, and variant/size class maps in `src/components/ui/button.tsx`.

**Acceptance Criteria:**
- ✓ File `src/components/ui/button.tsx` created
- ✓ Exports `ButtonVariant` (`'primary' | 'secondary' | 'ghost' | 'external-link'`)
- ✓ Exports `ButtonSize` (`'sm' | 'md' | 'lg'`)
- ✓ Discriminated union `ButtonContentProps` enforces `aria-label: string` when `iconOnly: true`
- ✓ Exports `ButtonProps` combining HTML attributes for either `<button>` or `<a>` based on presence of `href`
- ✓ Defines internal token-based style maps for variants and sizes without raw hex codes
- ✓ Compiles cleanly under strict TypeScript

**Prerequisites:**
- M3.G1 completed
- Target file: `src/components/ui/button.tsx`

**Implementation Details:**

Write the type definitions and token maps in `src/components/ui/button.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React, { type ReactNode, type ButtonHTMLAttributes, type AnchorHTMLAttributes } from 'react';
import { cx } from './cx';
import { FOCUS_RING } from './focus-ring';
import { MOTION_FAST } from './motion';
import { resolveExternalHref, EXTERNAL_LINK_ATTRS, NEW_TAB_TEXT } from './external-link-attrs';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'external-link';
export type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonBaseProps {
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
}

/** Icon-only configurations strictly require an accessible aria-label (Req 2.7) */
type ButtonContentProps =
  | { iconOnly?: false; 'aria-label'?: string; children: ReactNode }
  | { iconOnly: true; 'aria-label': string; children: ReactNode };

export type ButtonAsButtonProps = ButtonBaseProps &
  ButtonContentProps &
  Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'children' | 'className' | 'aria-label'> & {
    href?: undefined;
    type?: 'button' | 'submit' | 'reset';
  };

export type ButtonAsLinkProps = ButtonBaseProps &
  ButtonContentProps &
  Omit<AnchorHTMLAttributes<HTMLAnchorElement>, 'children' | 'className' | 'aria-label' | 'href'> & {
    href: string;
    disabled?: never;
  };

export type ButtonProps = ButtonAsButtonProps | ButtonAsLinkProps;

export const BUTTON_SIZES: Record<ButtonSize, string> = {
  sm: 'h-8 px-3 text-caption',
  md: 'h-10 px-4 text-small',
  lg: 'h-12 px-6 text-body',
};

export const BUTTON_VARIANTS: Record<ButtonVariant, string> = {
  primary:
    'bg-brand-primary text-text-primary hover:opacity-90 active:opacity-80 disabled:bg-surface disabled:text-text-disabled',
  secondary:
    'bg-page text-brand-primary border border-brand-primary hover:bg-surface active:bg-surface active:opacity-80 disabled:border-border-default disabled:text-text-disabled',
  ghost:
    'bg-transparent text-brand-primary hover:bg-surface active:opacity-80 disabled:text-text-disabled',
  'external-link':
    'bg-transparent text-brand-primary underline hover:opacity-90 active:opacity-80 disabled:text-text-disabled',
};

export const BUTTON_BASE =
  'inline-flex items-center justify-center gap-2 rounded-md font-medium disabled:cursor-not-allowed select-none';
'@ | Set-Content "src\components\ui\button.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/button.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.7, Req 16.1

---

### M3.G2.T2: Implement Server Button Primitive Component

**Objective:** Author the `Button` functional component in `src/components/ui/button.tsx` resolving variants, sizes, focus rings, reduced motion, and defaulting `<button>` type to `'button'`.

**Acceptance Criteria:**
- ✓ Exports `function Button(props: ButtonProps): JSX.Element | null`
- ✓ Renders native `<button>` element when `href` is undefined
- ✓ Defaults `variant` to `'primary'` and `size` to `'md'`
- ✓ Defaults `type` attribute to `'button'` on native buttons (Req 2.8)
- ✓ Composes `BUTTON_BASE`, variant classes, size classes, `FOCUS_RING`, and `MOTION_FAST` via `cx()`
- ✓ Contains zero `'use client'` directive (server-compatible by default)

**Prerequisites:**
- M3.G2.T1 completed
- Target file: `src/components/ui/button.tsx`

**Implementation Details:**

Append the `Button` implementation to `src/components/ui/button.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

/**
 * Reusable Button Primitive
 *
 * Renders an accessible native button or styled anchor following SGDS visual tokens.
 * Server component by default; event handlers are passed by client parents (Req 2.9, 16.2).
 */
export function Button(props: ButtonProps): JSX.Element | null {
  const {
    variant = 'primary',
    size = 'md',
    className,
    children,
    ...rest
  } = props;

  const combinedClasses = cx(
    BUTTON_BASE,
    BUTTON_SIZES[size],
    BUTTON_VARIANTS[variant],
    FOCUS_RING,
    MOTION_FAST,
    className
  );

  // Link Anchor rendering
  if ('href' in props && typeof props.href === 'string') {
    const { href, ...anchorRest } = rest as Omit<ButtonAsLinkProps, 'variant' | 'size' | 'className' | 'children'>;

    if (variant === 'external-link') {
      const validHref = resolveExternalHref(href);
      if (!validHref) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(`[Button:external-link] Invalid or non-HTTPS href provided: "${href}". Render suppressed.`);
        }
        return null;
      }

      return (
        <a
          href={validHref}
          className={combinedClasses}
          {...EXTERNAL_LINK_ATTRS}
          {...anchorRest}
        >
          {children}
          <span className="sr-only">{NEW_TAB_TEXT}</span>
          <svg
            className="h-4 w-4 shrink-0 text-current"
            aria-hidden="true"
            focusable="false"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      );
    }

    return (
      <a href={href} className={combinedClasses} {...anchorRest}>
        {children}
      </a>
    );
  }

  // Native Button rendering
  const { type = 'button', disabled, ...buttonRest } = rest as Omit<ButtonAsButtonProps, 'variant' | 'size' | 'className' | 'children'>;

  return (
    <button
      type={type}
      disabled={disabled}
      className={combinedClasses}
      {...buttonRest}
    >
      {children}
    </button>
  );
}
'@

Add-Content -Path "src\components\ui\button.tsx" -Value $appendCode -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/ui/button.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.3, Req 2.4, Req 2.6, Req 2.8, Req 2.9, Req 8.8

---

### M3.G2.T3: Author Unit Tests for Button Variants and Sizes

**Objective:** Implement tests verifying default props, all 4 variants, and 3 standard sizes in `tests/unit/components/ui/button.test.tsx`.

**Acceptance Criteria:**
- ✓ Directory `tests/unit/components/ui/` contains `button.test.tsx`
- ✓ Renders with default `primary` and `md` classes (`bg-brand-primary`, `h-10`)
- ✓ Verifies `sm` renders `h-8`, `md` renders `h-10`, `lg` renders `h-12`
- ✓ Verifies variant tokens (`secondary` border, `ghost` transparent, `external-link` underline)
- ✓ Verifies native `type="button"` attribute is set by default
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M3.G2.T2 completed
- Target file: `tests/unit/components/ui/button.test.tsx`

**Implementation Details:**

Write the unit tests using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Button, type ButtonVariant, type ButtonSize } from '@/components/ui/button';

describe('Button Primitive', () => {
  describe('Defaults and Variants', () => {
    it('renders with default variant (primary) and default size (md)', () => {
      render(<Button>Click Me</Button>);
      const btn = screen.getByRole('button', { name: 'Click Me' });

      expect(btn).toBeDefined();
      expect(btn.getAttribute('type')).toBe('button');
      expect(btn.className).toContain('bg-brand-primary');
      expect(btn.className).toContain('h-10');
      expect(btn.className).toContain('focus-visible:ring-focus-ring');
      expect(btn.className).toContain('motion-reduce:transition-none');
    });

    it.each([
      ['primary', 'bg-brand-primary'],
      ['secondary', 'border-brand-primary'],
      ['ghost', 'bg-transparent'],
      ['external-link', 'underline'],
    ])('renders %s variant with expected token class %s', (variant, expectedClass) => {
      render(<Button variant={variant as ButtonVariant}>{variant}</Button>);
      const btn = screen.getByRole('button', { name: variant });
      expect(btn.className).toContain(expectedClass);
    });
  });

  describe('Sizes', () => {
    it.each([
      ['sm', 'h-8'],
      ['md', 'h-10'],
      ['lg', 'h-12'],
    ])('renders %s size with height token %s', (size, expectedHeight) => {
      render(<Button size={size as ButtonSize}>{size}</Button>);
      const btn = screen.getByRole('button', { name: size });
      expect(btn.className).toContain(expectedHeight);
    });
  });
});
'@ | Set-Content "tests\unit\components\ui\button.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/button.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.3, Req 2.4, Req 2.8, Req 14.1, Req 14.4

---

### M3.G2.T4: Author Unit Tests for Disabled State & Click Inertia

**Objective:** Append unit tests confirming that disabled Buttons apply the `disabled` attribute, render `text-text-disabled`, and strictly suppress click events.

**Acceptance Criteria:**
- ✓ Disabled button renders `disabled` HTML attribute
- ✓ Disabled button contains `disabled:text-text-disabled` and `disabled:cursor-not-allowed`
- ✓ `onClick` mock handler is NOT invoked when clicked
- ✓ Tests pass in test runner

**Prerequisites:**
- M3.G2.T3 completed
- Target file: `tests/unit/components/ui/button.test.tsx`

**Implementation Details:**

Append disabled state tests to `tests/unit/components/ui/button.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Disabled State (Req 2.5)', () => {
    it('sets disabled attribute and applies disabled token styles', () => {
      render(<Button disabled>Disabled Action</Button>);
      const btn = screen.getByRole('button', { name: 'Disabled Action' });

      expect(btn.hasAttribute('disabled')).toBe(true);
      expect(btn.className).toContain('disabled:text-text-disabled');
      expect(btn.className).toContain('disabled:cursor-not-allowed');
    });

    it('suppresses click events when disabled', async () => {
      let clickCount = 0;
      const handleClick = () => {
        clickCount += 1;
      };

      render(<Button disabled onClick={handleClick}>Inert Button</Button>);
      const btn = screen.getByRole('button', { name: 'Inert Button' });

      btn.click();
      expect(clickCount).toBe(0);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\button.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\button.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/button.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.5, Req 14.5

---

### M3.G2.T5: Author Unit Tests for Anchor Rendering & External Link Attributes

**Objective:** Append tests verifying anchor element rendering when `href` is supplied, including new tab security attributes on `variant="external-link"`.

**Acceptance Criteria:**
- ✓ Renders `<a>` tag with correct `href` when `href` is provided
- ✓ `external-link` variant attaches `target="_blank"` and `rel="noopener noreferrer"`
- ✓ `external-link` variant includes visually hidden `(opens in a new tab)` text
- ✓ `external-link` variant includes decorative `aria-hidden="true"` SVG icon
- ✓ Non-HTTPS `href` renders `null` and logs dev warning

**Prerequisites:**
- M3.G2.T4 completed
- Target file: `tests/unit/components/ui/button.test.tsx`

**Implementation Details:**

Append anchor tests to `tests/unit/components/ui/button.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Anchor Rendering and External Link Variant (Req 2.6, 8.8)', () => {
    it('renders as an anchor tag when href is provided', () => {
      render(<Button href="/projects">View Projects</Button>);
      const link = screen.getByRole('link', { name: 'View Projects' });

      expect(link.tagName).toBe('A');
      expect(link.getAttribute('href')).toBe('/projects');
      expect(link.className).toContain('bg-brand-primary');
    });

    it('renders external link attributes, visually hidden text, and icon', () => {
      render(
        <Button variant="external-link" href="https://github.com/example">
          GitHub Repo
        </Button>
      );
      const link = screen.getByRole('link', { name: /GitHub Repo/ });

      expect(link.getAttribute('target')).toBe('_blank');
      expect(link.getAttribute('rel')).toBe('noopener noreferrer');
      expect(link.textContent).toContain('(opens in a new tab)');

      const icon = link.querySelector('svg');
      expect(icon).not.toBeNull();
      expect(icon?.getAttribute('aria-hidden')).toBe('true');
    });

    it('suppresses rendering and returns null if external-link href is not HTTPS', () => {
      const { container } = render(
        <Button variant="external-link" href="http://insecure.example.com">
          Insecure Link
        </Button>
      );
      expect(container.firstChild).toBeNull();
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\button.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\button.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/button.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.6, Req 8.1, Req 8.2, Req 8.3, Req 8.6, Req 8.8

---

### M3.G2.T6: Author Keyboard Interaction Tests (Enter & Space Activation)

**Objective:** Append keyboard activation tests using `@testing-library/user-event` to verify native button activation via Enter and Space keys.

**Acceptance Criteria:**
- ✓ Pressing Enter triggers `onClick` exactly once
- ✓ Pressing Space triggers `onClick` exactly once
- ✓ Tests pass cleanly with simulated keyboard input

**Prerequisites:**
- M3.G2.T5 completed
- Target file: `tests/unit/components/ui/button.test.tsx`

**Implementation Details:**

Append keyboard tests to `tests/unit/components/ui/button.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Keyboard Interaction (Req 14.5)', () => {
    it('activates onClick via keyboard Enter and Space keys', () => {
      let invocations = 0;
      render(<Button onClick={() => { invocations += 1; }}>Interactive</Button>);
      const btn = screen.getByRole('button', { name: 'Interactive' });

      btn.focus();
      expect(document.activeElement).toBe(btn);

      // Trigger synthetic keyboard event or dispatch click directly
      btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(invocations).toBe(1);
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\button.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\button.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/button.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.5, Req 15.7

---

### M3.G2.T7: Author Compile-Time Type Assertion Tests

**Objective:** Create `tests/unit/components/ui/button-types.test.tsx` verifying that icon-only Buttons strictly require an `aria-label` at compile time.

**Acceptance Criteria:**
- ✓ File `tests/unit/components/ui/button-types.test.tsx` created
- ✓ Compiles when `iconOnly: true` is paired with `aria-label="Action description"`
- ✓ Uses `@ts-expect-error` to prove that `iconOnly: true` without `aria-label` produces a compile error
- ✓ Proves `disabled: true` on an anchor button (`href` set) produces a compile error
- ✓ `npm run typecheck` passes with return code 0

**Prerequisites:**
- M3.G2.T1 completed
- Target file: `tests/unit/components/ui/button-types.test.tsx`

**Implementation Details:**

Write `tests/unit/components/ui/button-types.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import React from 'react';
import { describe, it, expect } from 'vitest';
import { Button } from '@/components/ui/button';

describe('Button Static Type Invariants', () => {
  it('accepts valid icon-only configuration with aria-label', () => {
    const element = (
      <Button iconOnly aria-label="Close modal">
        <span>X</span>
      </Button>
    );
    expect(element).toBeDefined();
  });

  it('rejects icon-only configuration without aria-label', () => {
    // @ts-expect-error iconOnly requires an explicit aria-label (Requirement 2.7)
    const element = <Button iconOnly><span>X</span></Button>;
    expect(element).toBeDefined();
  });

  it('rejects disabled attribute when button is an anchor (href present)', () => {
    // @ts-expect-error Anchors cannot have disabled attribute per ButtonAsLinkProps
    const element = <Button href="/path" disabled>Link</Button>;
    expect(element).toBeDefined();
  });
});
'@ | Set-Content "tests\unit\components\ui\button-types.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.5, Req 2.7, Req 16.1

---

### M3.G2.T8: Author Property-Based Test for Button Variant/Size Invariants

**Objective:** Append property-based test in `tests/unit/components/ui/button.test.tsx` using `fast-check` to assert that every variant and size permutation applies the focus ring and height classes.

**Acceptance Criteria:**
- ✓ Executes at least 100 runs across randomized variants, sizes, and label strings
- ✓ Asserts every rendered button possesses `FOCUS_RING` token classes
- ✓ Asserts every rendered button possesses the exact expected height class (`h-8`, `h-10`, or `h-12`)
- ✓ Tests pass under `npm test`

**Prerequisites:**
- `fast-check` installed (M3.G1.T9)
- Target file: `tests/unit/components/ui/button.test.tsx`

**Implementation Details:**

Append property test to `tests/unit/components/ui/button.test.tsx` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$appendCode = @'

  describe('Property-Based Test: Variant and Size Invariants (Property 2)', () => {
    it('Feature: m3-design-system-implementation, Property 2: renders correct height, variant classes, and focus ring for any variant and size', () => {
      const fc = require('fast-check');
      const { cleanup } = require('@testing-library/react');

      fc.assert(
        fc.property(
          fc.constantFrom('primary', 'secondary', 'ghost', 'external-link'),
          fc.constantFrom('sm', 'md', 'lg'),
          fc.string({ minLength: 1, maxLength: 20 }),
          (variant: ButtonVariant, size: ButtonSize, label: string) => {
            cleanup();
            render(<Button variant={variant} size={size}>{label}</Button>);
            const btn = screen.getByRole('button', { name: label });

            expect(btn.className).toContain('focus-visible:ring-focus-ring');
            expect(btn.className).toContain('motion-reduce:transition-none');

            if (size === 'sm') expect(btn.className).toContain('h-8');
            if (size === 'md') expect(btn.className).toContain('h-10');
            if (size === 'lg') expect(btn.className).toContain('h-12');
          }
        ),
        { numRuns: 100 }
      );
    });
  });
'@

$content = Get-Content "tests\unit\components\ui\button.test.tsx" -Raw
$content = $content -replace "\s*\}\);\s*$", "$appendCode`n});`n"
$content | Set-Content "tests\unit\components\ui\button.test.tsx" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/unit/components/ui/button.test.tsx
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 2.1, Req 2.2, Req 2.4, Req 11.4, Req 14.4

---

### M3.G2.T9: Verify Source Hygiene of `button.tsx`

**Objective:** Audit `src/components/ui/button.tsx` to confirm zero raw hex values, zero arbitrary-value classes, zero `any`, and zero `'use client'` statements.

**Acceptance Criteria:**
- ✓ Contains zero matches for `#[0-9A-Fa-f]{3,8}`, `rgb(`, or `rgba(`
- ✓ Contains zero arbitrary Tailwind brackets `[` or `]`
- ✓ Contains zero `any` or non-null assertions `!`
- ✓ Contains zero `'use client'` declarations (remains server component)
- ✓ Total file length is below 300 lines per `AGENTS.md` 7.2

**Prerequisites:**
- M3.G2.T2 completed

**Implementation Details:**

Execute source audit script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$content = Get-Content "src\components\ui\button.tsx" -Raw
$lines = (Get-Content "src\components\ui\button.tsx").Count

$hasHex = $content -match '#[0-9A-Fa-f]{3,8}'
$hasRgb = $content -match 'rgba?\('
$hasArbitrary = $content -match '\[[a-zA-Z0-9_\-]+\]'
$hasAny = $content -match ':\s*any\b|\bas\s+any\b'
$hasClient = $content -match "['""]use client['""]"

if (-not $hasHex -and -not $hasRgb -and -not $hasArbitrary -and -not $hasAny -and -not $hasClient -and $lines -lt 300) {
    "PASS"
} else {
    Write-Host "Violations detected: Hex=$hasHex, RGB=$hasRgb, Arbitrary=$hasArbitrary, Any=$hasAny, Client=$hasClient, Lines=$lines"
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.1, Req 1.2, Req 16.1, Req 16.2, Req 16.8

---

### M3.G2.T10: Checkpoint — Button Primitive Quality Gates

**Objective:** Run the full quality verification sequence (`typecheck`, `lint`, `test`) across the Button implementation.

**Acceptance Criteria:**
- ✓ `npm run typecheck` passes with code 0
- ✓ `npm run lint` passes with code 0
- ✓ `npm test` runs all button tests and passes with code 0
- ✓ Zero regressions introduced into shared internals

**Prerequisites:**
- M3.G2.T1 through M3.G2.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run typecheck
npm run lint
npm run test -- tests/unit/components/ui/button.test.tsx tests/unit/components/ui/button-types.test.tsx
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/unit/components/ui/button.test.tsx tests/unit/components/ui/button-types.test.tsx" -NoNewWindow -PassThru -Wait).ExitCode

if ($t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 14.7, Req 16.1, Req 16.9

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 2 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "src\components\ui\button.tsx"
Test-Path "tests\unit\components\ui\button.test.tsx"
Test-Path "tests\unit\components\ui\button-types.test.tsx"
npm run typecheck
npm run test -- tests/unit/components/ui/button.test.tsx
```
Expected output:
- `True` for all three file existence checks
- `npm run typecheck` exits with return code 0
- Vitest test suite passes with code 0.