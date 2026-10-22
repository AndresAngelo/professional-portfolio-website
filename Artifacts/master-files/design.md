# design.md

# Design Brief & System Specification

> **Document Status:** Approved  
> **Last Updated:** 2026-10-20  
> **Lead Product Designer:** Angelo Andres  
> **PRD Reference:** `PRD.md`  
> **TRD Reference:** `TRD.md`  
> **Design System Basis:** Singapore Government Design System (SGDS)  
> **SGDS Reference:** https://www.designsystem.tech.gov.sg/

---

## 1. Document Control & Executive Summary

### 1.1 Revision History & Change Log

| Date | Version | Author | Summary of Changes | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| 2026-10-20 | v1.0 | Angelo Andres | Approved SGDS-inspired MVP design system | Angelo Andres |

### 1.2 Aesthetic Vision & Core Principles
- **Product Aesthetic:** Clean, professional, high-trust, content-first developer portfolio with a restrained governmental design language.
- **Core Design Principles:**
  1. **Clarity over decoration:** Visual elements support scanning, evaluation, and navigation.
  2. **Evidence-first hierarchy:** Projects, documentation, certifications, and participation are visually prioritized.
  3. **Accessible by default:** WCAG 2.1 AA is a baseline, not an enhancement.
  4. **Consistency through tokens:** Colors, type, spacing, radius, elevation, and motion use named semantic tokens.
  5. **Calm technical density:** Present enough detail for technical evaluators without overwhelming recruiters.

SGDS organizes visual decisions through design tokens spanning color, typography, spacing, borders, iconography, layout, layering, and motion; this specification maps those principles to a portfolio-specific token set. [8][9][10][11]

---

## 2. Brand Voice, Tone & References

### 2.1 Tone & Voice Matrix

| Context | Voice Tone | Example Copy |
| :--- | :--- | :--- |
| Homepage | Confident, concise, evidence-oriented | “Engineering work, build documentation, and verified credentials.” |
| Projects | Direct, technical, outcome-focused | “Explore the implementation, architecture notes, and repository.” |
| Certifications | Factual, verifiable | “View issuer verification.” |
| Blog | Reflective, practical, specific | “Notes from the event and what I built or learned.” |
| Empty state | Reassuring, neutral | “No matching projects yet. Clear filters to see all work.” |
| Not found | Helpful, direct | “This page could not be found. Return to the portfolio.” |

### 2.2 Visual References
- **Primary Reference:** Singapore Government Design System.
- **Supporting References:** Modern developer documentation sites, technical case-study layouts, accessible portfolio patterns.
- **Avoid:** Dense dashboards, decorative gradients, aggressive animations, low-contrast gray text, and generic startup landing-page patterns.

---

## 3. Design Tokens & Core Systems

### 3.1 Color Palette

The following are portfolio-specific semantic tokens inspired by SGDS’s token-based approach. Implementation must reference tokens or Tailwind mappings; raw hex values must not be hardcoded in components. [8][9]

| Token Name | Light Value | Dark Value | Usage |
| :--- | :--- | :--- | :--- |
| `--color-bg-page` | `#FFFFFF` | `#0B0F14` | Page background |
| `--color-bg-surface` | `#F7F9FA` | `#131A21` | Cards, panels, documentation containers |
| `--color-bg-inverse` | `#0B0F14` | `#F7F9FA` | Footer or high-contrast section |
| `--color-text-primary` | `#17202A` | `#F4F7F9` | Headings and primary body copy |
| `--color-text-secondary` | `#4A5A68` | `#B8C4CE` | Supporting copy and metadata |
| `--color-text-disabled` | `#7A8894` | `#7A8894` | Disabled controls |
| `--color-border-default` | `#D7DEE4` | `#2A3540` | Card, input, and divider borders |
| `--color-border-strong` | `#17202A` | `#F4F7F9` | Emphasized boundaries and focus contexts |
| `--color-brand-primary` | `#0052A5` | `#4FA3E3` | Primary actions, active navigation, key links |
| `--color-brand-secondary` | `#00694E` | `#4FC49B` | Secondary accent, success-oriented emphasis |
| `--color-feedback-success` | `#00694E` | `#4FC49B` | Success and verified states |
| `--color-feedback-warning` | `#8A6100` | `#E8B339` | Draft, experimental, or cautionary metadata |
| `--color-feedback-danger` | `#B42318` | `#F97066` | Errors and destructive emphasis |
| `--color-focus-ring` | `#0052A5` | `#4FA3E3` | Keyboard focus indicator |

### 3.2 Typography Scale

- **Primary sans-serif:** `Inter`, `system-ui`, `-apple-system`, `Segoe UI`, `sans-serif`
- **Monospace:** `JetBrains Mono`, `SFMono-Regular`, `Menlo`, `Consolas`, `monospace`

| Token | Size | Line Height | Weight | Usage |
| :--- | :--- | :--- | :--- | :--- |
| `text-caption` | `12px` / `0.75rem` | `16px` | 400 | Metadata, badges, legal text |
| `text-small` | `14px` / `0.875rem` | `20px` | 400 / 500 | Secondary copy, labels, table text |
| `text-body` | `16px` / `1rem` | `24px` | 400 | Primary reading text |
| `text-lead` | `18px` / `1.125rem` | `28px` | 400 / 500 | Introduction and section leads |
| `text-heading-4` | `20px` / `1.25rem` | `28px` | 600 | Card titles and minor headings |
| `text-heading-3` | `24px` / `1.5rem` | `32px` | 600 | Section headings |
| `text-heading-2` | `30px` / `1.875rem` | `38px` | 700 | Page titles |
| `text-heading-1` | `38px` / `2.375rem` | `46px` | 700 | Hero headline |

### 3.3 Spacing & Layout Grid

Base unit: `4px`.

| Token | Value | Usage |
| :--- | :--- | :--- |
| `space-1` | `4px` | Icon-to-label spacing |
| `space-2` | `8px` | Tight internal component spacing |
| `space-3` | `12px` | Chip and badge padding |
| `space-4` | `16px` | Standard component padding |
| `space-6` | `24px` | Card padding and grid gaps |
| `space-8` | `32px` | Section spacing on mobile |
| `space-12` | `48px` | Section spacing on tablet/desktop |
| `space-16` | `64px` | Major page-section separation |
| `space-24` | `96px` | Hero and footer separation |

### 3.4 Radius, Elevation & Motion

| Token | Value | Usage |
| :--- | :--- | :--- |
| `radius-sm` | `4px` | Chips, tags, small controls |
| `radius-md` | `8px` | Inputs, buttons, compact cards |
| `radius-lg` | `12px` | Project and blog cards |
| `radius-full` | `9999px` | Avatars, circular badges |
| `elevation-0` | None | Page background |
| `elevation-1` | `0 1px 2px rgba(11, 15, 20, 0.06)` | Cards at rest |
| `elevation-2` | `0 4px 12px rgba(11, 15, 20, 0.10)` | Hovered or elevated cards |
| `motion-fast` | `150ms ease-out` | Hover, focus, and small state changes |
| `motion-standard` | `250ms ease-out` | Navigation and disclosure transitions |

---

## 4. Component Architecture & UI Elements

### 4.1 Buttons
- **Variants:** Primary, Secondary, Ghost, External Link.
- **States:** Default, Hover, Active, Focus Visible, Disabled.
- **Sizes:** Small `32px` height, Medium `40px` height, Large `48px` height.
- **Rules:**
  - Use Primary for one main action per section.
  - Use Secondary for navigation-like supporting actions.
  - Use External Link for destinations outside the site.
  - Every icon-only control requires an accessible name.

### 4.2 Navigation
- **Header:** Site identity, primary navigation, and optional contact action.
- **Mobile Navigation:** Accessible disclosure control with expanded/collapsed states.
- **Footer:** Copyright, professional links, contact links, and secondary navigation.
- **Rules:**
  - Current route must have both visual and programmatic current-page indication.
  - Navigation order: Home, Projects, Certifications, Blog, Contact.

### 4.3 Cards & Containers
- **Project Card:** Title, summary, technology tags, status badge, and detail link.
- **Certification Card:** Badge or icon, title, issuer, date, category, and verification link.
- **Blog Card:** Title, date, reading time, event type, summary, and tags.
- **Rules:**
  - Cards use `radius-lg`, `elevation-1`, and `--color-bg-surface`.
  - Entire card may be clickable only when it has one clear accessible destination.
  - Avoid nesting interactive elements inside a clickable card.

### 4.4 Tags, Badges & Metadata
- **Technology Tag:** Compact, neutral surface with `radius-sm`.
- **Status Badge:** Uses semantic color only when it communicates state, such as `Completed`, `In Progress`, or `Archived`.
- **Event Type Badge:** Identifies `Meetup`, `Hackathon`, `Workshop`, or `Learning`.
- **Rules:**
  - Tags are not buttons unless they perform filtering.
  - Badge color must not be the sole carrier of meaning.

### 4.5 Markdown Documentation Layout
- Use a readable measure of approximately `65–75` characters per line.
- Use clear heading hierarchy beginning at `h2` within article content.
- Use monospace styling for inline code and code blocks.
- Use accessible tables with scoped headers when tabular data is present.
- Ensure code blocks support horizontal scrolling without breaking page layout.

---

## 5. Responsive Breakpoints & Accessibility

### 5.1 Responsive Layout Breakpoints

| Breakpoint | Width | Layout Behavior |
| :--- | :--- | :--- |
| Mobile | `375px–767px` | Single column, stacked cards, collapsible navigation |
| Tablet | `768px–1023px` | Two-column project/blog grids where appropriate |
| Desktop | `1024px–1439px` | Multi-column grids, persistent horizontal navigation |
| Wide Desktop | `1440px+` | Centered content container with maximum readable width |

### 5.2 Accessibility Targets (WCAG 2.1 AA)
- **Contrast:** At least `4.5:1` for normal text and `3:1` for large text and meaningful UI boundaries.
- **Keyboard:** All interactions are reachable and usable with keyboard only.
- **Focus:** Visible focus ring using `--color-focus-ring`; never remove focus outlines without an equivalent visible indicator.
- **Screen Readers:** Use semantic landmarks, headings, lists, labels, and descriptive accessible names.
- **Images:** All informative images require meaningful alternative text; decorative images require empty alternative text.
- **External Links:** Communicate external destination and new-tab behavior in accessible link text where appropriate.
- **Motion:** Respect `prefers-reduced-motion`; avoid parallax, autoplaying motion, and nonessential animation.

---

## 6. Page-Level Layout Direction

### 6.1 Homepage
- Hero: Name, role, concise positioning statement, primary project CTA, secondary contact CTA.
- Featured Projects: Maximum 3 project cards.
- Skills Snapshot: Compact technology and capability groups.
- Recent Activity: Up to 3 latest blog entries.
- Footer: Contact and professional links.

### 6.2 Projects
- Index: Filter bar, responsive project grid, empty state.
- Detail: Title, status, role, timeline, technology tags, summary, build documentation, repository/demo links, and related projects where available.

### 6.3 Certifications
- Category sections.
- Certification cards in a responsive grid.
- Verification links visually distinguished from general navigation.

### 6.4 Blog
- Index: Tag filter bar, chronological post list, empty state.
- Detail: Title, date, reading time, event type, tags, Markdown body, and optional external event link.

---

## 7. Instructions for AI Design Agents (`design.md` Protocol)

1. **Token adherence:** Never hardcode arbitrary colors, font sizes, spacing, radii, shadows, or durations; use the semantic tokens or their approved Tailwind mappings.
2. **SGDS alignment:** Favor restrained, accessible, high-trust layouts over decorative visual effects.
3. **Component consistency:** Reuse the same card, badge, button, filter, and documentation patterns across sections.
4. **Responsive safety:** Every page must function from `375px` through wide desktop widths.
5. **Accessibility enforcement:** Every generated component must include semantic structure, keyboard operability, visible focus, and appropriate alternative text.
6. **No fabricated content:** Use empty states rather than placeholder project, certification, or blog data in production UI.
7. **No dark mode by default:** Implement dark mode only if explicitly approved; all tokens already define dark values for future use.