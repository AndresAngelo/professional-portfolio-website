# AGENTS.md

# Background Schema & Repository Context

> **Document Status:** Active / Frozen for MVP  
> **Last Updated:** 2026-10-20  
> **System Architect:** Angelo Andres  
> **PRD Alignment:** `PRD.md`  
> **TRD Alignment:** `TRD.md`  
> **SSOT Scope:** This file is the exclusive source of truth for content schemas, TypeScript content contracts, directory taxonomy, naming conventions, validation rules, and agent guardrails.

---

## 1. Executive Summary & Context Scope

### 1.1 Purpose of this File
This `AGENTS.md` defines the repository context, local content architecture, strict TypeScript contracts, validation rules, and operational boundaries for human developers and autonomous coding agents building `personal-website-portfolio-v2`.

### 1.2 System Boundary & Domain Map
- **Core Application Domain:** Static developer portfolio.
- **Content Domains:** Site profile, projects, certifications/badges, blog/participation log.
- **Persistence Layer:** Local Markdown/MDX and JSON files read during Next.js build.
- **Runtime Database:** None.
- **Runtime API:** None in P0.
- **Primary Compliance Regime:** No visitor-data collection; public, owner-curated content only.

---

## 2. Universal Data Dictionary & Nomenclature Matrix

| Canonical Entity | Business Concept | Content Source | TypeScript Type | UI Label / Component |
| :--- | :--- | :--- | :--- | :--- |
| **Site Config** | Global site and owner metadata | `content/site.json` | `SiteConfig` | Site header/footer/profile |
| **Project** | Portfolio project case study | `content/projects/*.mdx` | `Project` | Project card/detail |
| **Certification** | Certification or badge credential | `content/certifications/*.mdx` | `Certification` | Certification card |
| **Blog Post** | Meetup, hackathon, learning, or update entry | `content/blog/*.mdx` | `BlogPost` | Blog card/detail |
| **Technology Tag** | Technology or skill label | Project frontmatter | `TechnologyTag` | Filter chip/tag |
| **Project Status** | Delivery state of a project | Project frontmatter | `ProjectStatus` | Status badge/filter |
| **Event Type** | Community activity category | Blog frontmatter | `EventType` | Event badge/filter |

---

## 3. Directory Taxonomy

```text
personal-website-portfolio-v2/
├── content/
│   ├── site.json
│   ├── projects/
│   │   ├── example-project.mdx
│   │   └── another-project.mdx
│   ├── certifications/
│   │   ├── example-certification.mdx
│   │   └── example-badge.mdx
│   └── blog/
│       ├── example-meetup.mdx
│       └── example-hackathon.mdx
├── public/
│   ├── images/
│   │   ├── projects/
│   │   ├── certifications/
│   │   └── blog/
│   └── files/
│       └── resume.pdf
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── not-found.tsx
│   │   ├── projects/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   ├── certifications/
│   │   │   └── page.tsx
│   │   └── blog/
│   │       ├── page.tsx
│   │       └── [slug]/
│   │           └── page.tsx
│   ├── components/
│   │   ├── layout/
│   │   ├── home/
│   │   ├── projects/
│   │   ├── certifications/
│   │   ├── blog/
│   │   └── ui/
│   ├── content/
│   │   ├── loaders/
│   │   ├── markdown/
│   │   └── schemas/
│   ├── lib/
│   └── types/
├── tests/
├── next.config.ts
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md
```

### 3.1 Directory Ownership

| Directory | Ownership | Agent Permission |
| :--- | :--- | :--- |
| `content/` | Content Owner | Create/edit content files only |
| `public/images/` | Content Owner | Add optimized image assets only |
| `public/files/` | Content Owner | Add approved downloadable files only |
| `src/app/` | Engineering | Create/edit routes and layouts |
| `src/components/` | Engineering / UI | Create/edit UI components |
| `src/content/` | Engineering | Create/edit loaders, Markdown rendering, and schema validation |
| `src/lib/` | Engineering | Create/edit shared utilities |
| `src/types/` | Engineering | Re-export or compose types; do not redefine content schemas |
| `tests/` | Engineering / QA | Create/edit tests |
| Root configuration files | Human-approved change only | Do not modify without explicit approval |

---

## 4. Core Content Schemas & Relationships

### 4.1 Entity Relationship Diagram

```text
+---------------------+
|     SiteConfig      |
|---------------------|
| profile             |
| contactChannels     |
| socialLinks         |
| navigation          |
+---------------------+
          |
          | references by slug
          v
+---------------------+          +----------------------+
|      Project        |          |    Certification     |
|---------------------|          |----------------------|
| slug                |          | slug                 |
| title               |          | title                |
| status              |          | issuer               |
| technologies[]      |          | category             |
| documentation       |          | issuedAt             |
+---------------------+          +----------------------+

+---------------------+
|      BlogPost       |
|---------------------|
| slug                |
| title               |
| eventType           |
| publishedAt         |
| tags[]              |
| content             |
+---------------------+
```

### 4.2 TypeScript Content Contracts

All content types use strict TypeScript. The use of `any`, implicit `any`, non-null assertions, and unsafe type casts is prohibited.

```typescript
export type IsoDateString = string;

export type ProjectStatus = "completed" | "in-progress" | "archived";

export type CertificationCategory =
  | "cloud"
  | "ai"
  | "security"
  | "frontend"
  | "backend"
  | "data"
  | "devops"
  | "professional";

export type EventType =
  | "meetup"
  | "hackathon"
  | "workshop"
  | "conference"
  | "learning"
  | "project-update";

export type ContactChannelType =
  | "email"
  | "linkedin"
  | "github"
  | "website"
  | "other";

export interface ContactChannel {
  type: ContactChannelType;
  label: string;
  url: string;
  isPrimary: boolean;
}

export interface SocialLink {
  label: string;
  url: string;
}

export interface SiteProfile {
  name: string;
  professionalTitle: string;
  introduction: string;
  location: string;
  availableForOpportunities: boolean;
}

export interface SiteNavigationItem {
  label: string;
  href: string;
}

export interface SiteConfig {
  siteName: string;
  siteUrl: string;
  profile: SiteProfile;
  contactChannels: ContactChannel[];
  socialLinks: SocialLink[];
  navigation: SiteNavigationItem[];
}

export interface ProjectFilters {
  technology: string | null;
  status: ProjectStatus | null;
}

export interface ProjectMetrics {
  label: string;
  value: string;
}

export interface ProjectFrontmatter {
  title: string;
  summary: string;
  slug: string;
  status: ProjectStatus;
  role: string;
  startedAt: IsoDateString;
  completedAt: IsoDateString | null;
  technologies: string[];
  tags: string[];
  repositoryUrl: string | null;
  liveDemoUrl: string | null;
  documentationUrl: string | null;
  featured: boolean;
  displayOrder: number;
  metrics: ProjectMetrics[];
}

export interface Project extends ProjectFrontmatter {
  documentation: string;
}

export interface CertificationFrontmatter {
  title: string;
  slug: string;
  issuer: string;
  category: CertificationCategory;
  issuedAt: IsoDateString;
  expiresAt: IsoDateString | null;
  credentialId: string | null;
  verificationUrl: string | null;
  badgeImageUrl: string | null;
  badgeImageAlt: string | null;
  displayOrder: number;
}

export interface Certification extends CertificationFrontmatter {
  content: string;
}

export interface BlogPostFrontmatter {
  title: string;
  slug: string;
  summary: string;
  publishedAt: IsoDateString;
  updatedAt: IsoDateString | null;
  eventType: EventType;
  eventName: string | null;
  eventDate: IsoDateString | null;
  eventLocation: string | null;
  eventUrl: string | null;
  tags: string[];
  readingTimeMinutes: number;
  draft: boolean;
}

export interface BlogPost extends BlogPostFrontmatter {
  content: string;
}
```

### 4.3 Content File Examples

#### `content/site.json`

```json
{
  "siteName": "Angelo Andres",
  "siteUrl": "[https://example.vercel.app](https://example.vercel.app)",
  "profile": {
    "name": "Angelo Andres",
    "professionalTitle": "Pipeline Lead & Specification Architect",
    "introduction": "I build specification-driven software and AI engineering workflows.",
    "location": "Taguig, National Capital Region, PH",
    "availableForOpportunities": true
  },
  "contactChannels": [
    {
      "type": "email",
      "label": "Email Angelo",
      "url": "mailto:hello@example.com",
      "isPrimary": true
    }
  ],
  "socialLinks": [
    {
      "label": "GitHub",
      "url": "[https://github.com/example](https://github.com/example)"
    }
  ],
  "navigation": [
    { "label": "Home", "href": "/" },
    { "label": "Projects", "href": "/projects" },
    { "label": "Certifications", "href": "/certifications" },
    { "label": "Blog", "href": "/blog" }
  ]
}
```

#### `content/projects/example-project.mdx`

```mdx
***
title: "Example Portfolio Project"
summary: "A concise explanation of the problem, solution, and outcome."
slug: "example-project"
status: "completed"
role: "Full-Stack Engineer"
startedAt: "2026-01-15"
completedAt: "2026-03-01"
technologies:
  - "Next.js"
  - "TypeScript"
  - "Tailwind CSS"
tags:
  - "web"
  - "portfolio"
repositoryUrl: "[https://github.com/example/repository](https://github.com/example/repository)"
liveDemoUrl: null
documentationUrl: null
featured: true
displayOrder: 1
metrics:
  - label: "Build time"
    value: "Under 3 minutes"
***

## Build Documentation

Explain the problem, constraints, architecture decisions, implementation approach,
verification, and outcome.
```

#### `content/certifications/example-certification.mdx`

```mdx
***
title: "Example Certification"
slug: "example-certification"
issuer: "Example Issuer"
category: "cloud"
issuedAt: "2026-02-01"
expiresAt: null
credentialId: "EXAMPLE-123"
verificationUrl: "[https://example.com/verify/example-123](https://example.com/verify/example-123)"
badgeImageUrl: "/images/certifications/example-badge.png"
badgeImageAlt: "Example Certification badge"
displayOrder: 1
***

Optional supporting context for the certification.
```

#### `content/blog/example-meetup.mdx`

```mdx
***
title: "Example Meetup Reflection"
slug: "example-meetup"
summary: "A short summary of the event and key takeaway."
publishedAt: "2026-04-10"
updatedAt: null
eventType: "meetup"
eventName: "Example Developer Meetup"
eventDate: "2026-04-08"
eventLocation: "Singapore"
eventUrl: "[https://example.com/event](https://example.com/event)"
tags:
  - "community"
  - "ai"
readingTimeMinutes: 4
draft: false
***

Post content describing participation, learning, and outcomes.
```

---

## 5. Validation Rules & Content Guarantees

### 5.1 Universal Rules
1. `slug` must be unique within its content collection.
2. `slug` must contain only lowercase letters, numbers, and hyphens.
3. `slug` must not begin or end with a hyphen.
4. All dates must use ISO `YYYY-MM-DD` format.
5. All URLs must be absolute `https://` URLs, except internal asset paths beginning with `/`.
6. `mailto:` is permitted only for contact channels of type `email`.
7. Required fields must be present and valid; missing required fields must fail the build.
8. Optional URL fields may be `null`, empty, or omitted; the UI must omit the corresponding action.
9. `draft: true` blog posts must be excluded from production builds.
10. Content validation errors must include the file path, field name, expected type/format, and received value category.

### 5.2 Project Rules
- `title` must contain 3–100 characters after trimming.
- `summary` must contain 20–280 characters after trimming.
- `technologies` must contain at least 1 item.
- `status` must be one of `completed`, `in-progress`, or `archived`.
- `startedAt` must not be later than `completedAt` when `completedAt` is present.
- `featured` projects must have `displayOrder`.
- At most 3 projects may have `featured: true` at any time.
- Project Markdown documentation must contain at least one `##` heading.

### 5.3 Certification Rules
- `title`, `issuer`, `category`, and `issuedAt` are required.
- `expiresAt`, when present, must not be earlier than `issuedAt`.
- `badgeImageUrl` and `badgeImageAlt` must both be present or both be absent.
- `verificationUrl` must be an absolute HTTPS URL when present.
- `credentialId` is optional and must not be fabricated.

### 5.4 Blog Rules
- `title` must contain 5–120 characters after trimming.
- `summary` must contain 20–300 characters after trimming.
- `publishedAt` is required.
- `readingTimeMinutes` must be an integer from 1 to 60.
- `eventType` must be one of the allowed `EventType` values.
- `eventName`, `eventDate`, `eventLocation`, and `eventUrl` are optional.
- `eventDate`, when present, must not be later than `publishedAt`.
- `draft: true` posts must not appear in the blog index, homepage recent activity, RSS-like output, or static route generation.

---

## 6. System Rules, Constraints & Safety Guardrails

### 6.1 Non-Negotiable Engineering Rules
1. **No runtime database:** Do not add database clients, ORM configuration, migrations, or database environment variables in P0.
2. **No custom public API:** Do not create API routes, route handlers, server actions, or external HTTP endpoints in P0.
3. **No authentication:** Do not add login, registration, sessions, JWT, OAuth, or role-based access control.
4. **No visitor tracking:** Do not add analytics, cookies, fingerprinting, forms, or third-party tracking scripts in P0.
5. **No schema duplication:** `PRD.md`, `TRD.md`, `APP_FLOW.md`, `design.md`, and implementation code must reference this file for content structures.
6. **No fabricated credentials:** Never invent certification IDs, verification URLs, issuers, dates, badges, or external links.
7. **No unsafe TypeScript:** Do not use `any`, implicit `any`, non-null assertions, or unjustified type assertions.
8. **No hardcoded design values:** Use the semantic tokens defined in `design.md`.
9. **No broken links:** Optional links must be omitted when not configured; required links must be validated at build time.
10. **No unvalidated content:** Every content file must pass schema validation before static generation.

### 6.2 Repository Guardrails
- Do not commit `.env`, `.env.local`, `.env.production`, private keys, tokens, or credential files.
- Do not modify `package.json`, lockfiles, `next.config.ts`, `tsconfig.json`, or CI configuration without human approval.
- Do not add dependencies without documenting their purpose and verifying current maintenance status.
- Do not introduce a component library that conflicts with Tailwind-based SGDS-inspired styling.
- Do not add client-side JavaScript where a server component can render the content statically.

### 6.3 Agent File Access Boundaries

| Area | Permitted Actions | Prohibited Actions |
| :--- | :--- | :--- |
| `content/` | Read, create, edit Markdown/JSON content | Delete published content without instruction |
| `public/` | Add optimized approved assets | Add unlicensed, oversized, or untracked binary assets |
| `src/app/` | Create/edit routes and layouts | Add API routes or route handlers in P0 |
| `src/components/` | Create/edit components | Hardcode content or design values |
| `src/content/` | Create/edit loaders and validators | Duplicate schema definitions |
| `src/types/` | Re-export/compose contracts | Redefine canonical schemas |
| Root configs | Read only | Modify without explicit human approval |
| `.env*` | None | Read, create, edit, commit, or expose secrets |

### 6.4 Rate Limits and Operational Safety
- No API rate limits apply in P0 because no custom API exists.
- Do not add polling, webhooks, background jobs, queues, or recurring external requests.
- Do not fetch third-party content at runtime.
- Limit local images to optimized, purposeful assets; avoid deploying large raw media files.

---

## 7. Agent Instructions & Tool Specs

### 7.1 Permitted Actions & Tool Boundaries
- **Permitted File Access:**
  - Read and write within `src/`, `tests/`, `content/`, and approved `public/` asset paths.
  - Create content files following this specification.
- **Prohibited File Access:**
  - Never edit `.env*` files.
  - Never alter root build or dependency configuration without human verification.
  - Never introduce backend services or database dependencies.

### 7.2 Context Window Optimization Guidelines
- Keep individual component files below 300 lines where practical.
- Keep content loaders small and focused on one collection.
- Use explicit imports; avoid barrel files that obscure dependencies.
- Follow existing formatting, linting, and import-order conventions.

### 7.3 Test Execution Instructions
When generating or changing code:
1. Run `npm run lint`.
2. Run `npm run typecheck`.
3. Run `npm test`.
4. Run `npm run build`.
5. Add or update tests for content validation, filtering logic, route generation, and accessibility-critical behavior.
6. Do not mark a task complete if any verification command fails.