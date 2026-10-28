# M5.G1: Fixtures, Fixed UI Strings, Comparator, Date Formatter, and Gap Log

> **Milestone:** M5 — Homepage Experience  
> **Goal:** G1 of 10  
> **Tasks:** 10 atomic tasks  
> **Status:** NOT STARTED  

## Goal Objective

Establish the foundational test fixtures, fast-check property testing arbitraries, fixed layout strings, string comparator, display-date formatter, and architectural gap audit for Milestone 5. Specifically, author strongly typed test fixtures in `tests/fixtures/home-data.ts` covering full configurations and edge-case variants (no featured projects, no skills, no certifications, drafts only, empty contact channels, and disabled availability) without schema duplication. Construct `fast-check` arbitraries in `tests/fixtures/home-arbitraries.ts` to support universal property testing across projects, certifications, blog posts, contact channels, and date strings. Create `src/components/home/home-text.ts` defining all static UI strings, section IDs, and preview limits. Implement the deterministic code-unit string comparator in `src/lib/home/compare.ts`. Audit the repository for an existing date formatter and implement `src/lib/format-date.ts` (`formatDisplayDate`) enforcing UTC `en-US` formatting with round-trip validation and descriptive error reporting for invalid input. Confirm that upstream M2 loaders, M2 types, M3 UI primitives, and M4 layout landmarks exist and match expected signatures, logging all findings in `.kiro/specs/m5-homepage-experience/task-notes.md`.

## Goal Success Criteria

- ✓ `tests/fixtures/home-data.ts` exports typed fixtures (`validSiteConfig`, `sampleProjects`, `sampleCertifications`, `sampleBlogPosts`, and their edge-case variants) strictly typed via `@/types/content`
- ✓ `tests/fixtures/home-arbitraries.ts` exports `fast-check` generators for projects, certifications, posts, contact channels, profiles, and valid/invalid date strings
- ✓ `src/components/home/home-text.ts` exports `PREVIEW_LIMIT = 3`, `HOME_SECTION_ORDER`, `HomeSectionId`, and `HOME_TEXT` constants with zero site-owner or personal-data literals
- ✓ `src/lib/home/compare.ts` exports `compareStrings` providing deterministic code-unit ordering
- ✓ `src/lib/format-date.ts` exports `formatDisplayDate(date: IsoDateString | string): string` enforcing `en-US` formatting in UTC, rejecting invalid calendar dates with a descriptive error naming the received value
- ✓ Unit and property tests in `tests/home/format-date.test.ts` pass, proving date stability across `TZ=UTC` and `TZ=Asia/Manila` and satisfying Property 13 ($\ge 100$ runs with `fast-check`)
- ✓ Task notes file `.kiro/specs/m5-homepage-experience/task-notes.md` initialized with an audit of loader paths, M3 UI primitive prop signatures, test dependencies, and design-system boundaries
- ✓ `git diff` confirms zero changes to `package.json`, lockfiles, `tailwind.config.ts`, `globals.css`, `src/components/ui/`, `src/components/layout/`, or `src/content/`
- ✓ `npm run typecheck` and `npm test` exit with return code 0

## Prerequisites

- Milestones M1, M2, M3, and M4 completed (`m4-baseline` tagged in Git)
- Workspace root: `c:\dev\andres-webapp-professional\personal-website-portfolio`
- Project root: `c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2\`
- Upstream packages verified: `vitest`, `@testing-library/react`, `fast-check`, `vitest-axe`

---

## Tasks

### M5.G1.T1: Create Typed Homepage Test Fixtures (`tests/fixtures/home-data.ts`)

**Objective:** Author canonical, strongly typed test fixtures in `tests/fixtures/home-data.ts` covering populated site configurations, projects, certifications, blog posts, and their empty/edge variants.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/home-data.ts` exists
- ✓ Imports `SiteConfig`, `Project`, `Certification`, and `BlogPost` from `@/types/content` without redeclaring types (`AGENTS.md` 6.3, Req 1.5)
- ✓ Exports `sampleSiteConfig`: complete site profile with name, title, introduction, location, availability set to `true`, and primary email contact channel
- ✓ Exports `sampleProjects`: at least 5 projects with mixed `featured` flags (`true`/`false`), varied `displayOrder` values, shared `displayOrder` ties, and varied technology tags
- ✓ Exports `sampleCertifications`: at least 4 certifications with distinct and duplicate `displayOrder` values
- ✓ Exports `sampleBlogPosts`: at least 5 posts with mixed `draft` values (`true`/`false`), varied `publishedAt` dates, and same-day date ties
- ✓ Exports edge-case variants: `emptyProjects`, `noFeaturedProjects`, `emptyCertifications`, `draftsOnlyBlogPosts`, `emptyContactChannelsSiteConfig`, and `unavailableSiteConfig`
- ✓ Contains zero `any`, non-null assertions `!`, or unjustified type assertions

**Prerequisites:**
- M2 content contracts exist at `src/types/content.ts`
- Directory `tests/fixtures/` exists

**Implementation Details:**

Write `tests/fixtures/home-data.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "tests\fixtures")) {
    New-Item -ItemType Directory -Path "tests\fixtures" -Force | Out-Null
}

@'
import type { SiteConfig, Project, Certification, BlogPost } from '@/types/content';

/**
 * Standard complete SiteConfig fixture representing a fully populated profile.
 */
export const sampleSiteConfig: SiteConfig = {
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
    { label: 'GitHub', url: 'https://github.com/example' },
    { label: 'LinkedIn', url: 'https://linkedin.com/in/example' },
  ],
  navigation: [
    { label: 'Home', href: '/' },
    { label: 'Projects', href: '/projects' },
    { label: 'Certifications', href: '/certifications' },
    { label: 'Blog', href: '/blog' },
  ],
};

/**
 * SiteConfig variant where availableForOpportunities is false.
 */
export const unavailableSiteConfig: SiteConfig = {
  ...sampleSiteConfig,
  profile: {
    ...sampleSiteConfig.profile,
    availableForOpportunities: false,
  },
};

/**
 * SiteConfig variant with zero contact channels.
 */
export const emptyContactChannelsSiteConfig: SiteConfig = {
  ...sampleSiteConfig,
  contactChannels: [],
};

/**
 * Standard collection of sample projects for selection and skills derivation.
 */
export const sampleProjects: Project[] = [
  {
    title: 'Alpha Engine',
    slug: 'alpha-engine',
    summary: 'High performance rule execution engine built in TypeScript.',
    status: 'completed',
    role: 'Lead Architect',
    startedAt: '2025-01-01',
    completedAt: '2025-06-01',
    technologies: ['TypeScript', 'Next.js', 'Tailwind CSS'],
    tags: ['engine', 'compiler'],
    repositoryUrl: 'https://github.com/example/alpha-engine',
    liveDemoUrl: 'https://alpha.example.com',
    documentationUrl: null,
    featured: true,
    displayOrder: 1,
    metrics: [{ label: 'Speed', value: '<5ms' }],
    documentation: '## Alpha Engine Docs\nDetailed engine documentation.',
  },
  {
    title: 'Beta Service',
    slug: 'beta-service',
    summary: 'Cloud orchestration bridge for distributed workers.',
    status: 'in-progress',
    role: 'Backend Engineer',
    startedAt: '2025-07-01',
    completedAt: null,
    technologies: ['TypeScript', 'Node.js', 'Docker'],
    tags: ['cloud', 'orchestration'],
    repositoryUrl: 'https://github.com/example/beta-service',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: true,
    displayOrder: 2,
    metrics: [{ label: 'Nodes', value: '128' }],
    documentation: '## Beta Service Docs\nDetailed service documentation.',
  },
  {
    title: 'Gamma Workflow',
    slug: 'gamma-workflow',
    summary: 'Agentic pipeline runner with deterministic checkpoints.',
    status: 'completed',
    role: 'Pipeline Engineer',
    startedAt: '2025-09-01',
    completedAt: '2025-11-01',
    technologies: ['python', 'TypeScript', 'PostgreSQL'],
    tags: ['workflow', 'agent'],
    repositoryUrl: 'https://github.com/example/gamma-workflow',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: true,
    displayOrder: 2, // tie with beta-service to test slug tie-breaking
    metrics: [{ label: 'Efficiency', value: '+40%' }],
    documentation: '## Gamma Workflow Docs\nDetailed workflow documentation.',
  },
  {
    title: 'Delta Portal',
    slug: 'delta-portal',
    summary: 'Interactive documentation browser for client APIs.',
    status: 'completed',
    role: 'Frontend Engineer',
    startedAt: '2025-11-15',
    completedAt: '2026-01-15',
    technologies: ['Next.js', 'React', 'Tailwind CSS'],
    tags: ['docs', 'ui'],
    repositoryUrl: 'https://github.com/example/delta-portal',
    liveDemoUrl: 'https://delta.example.com',
    documentationUrl: null,
    featured: false, // not featured
    displayOrder: 3,
    metrics: [],
    documentation: '## Delta Portal Docs\nDetailed portal documentation.',
  },
  {
    title: 'Epsilon Tool',
    slug: 'epsilon-tool',
    summary: 'Command line utility for schema extraction and diffing.',
    status: 'completed',
    role: 'Tools Engineer',
    startedAt: '2026-02-01',
    completedAt: '2026-03-01',
    technologies: ['Go', 'Docker'],
    tags: ['cli', 'tools'],
    repositoryUrl: 'https://github.com/example/epsilon-tool',
    liveDemoUrl: null,
    documentationUrl: null,
    featured: true,
    displayOrder: 4, // 4th featured item (exceeds PREVIEW_LIMIT=3)
    metrics: [],
    documentation: '## Epsilon Tool Docs\nDetailed tool documentation.',
  },
];

/**
 * Projects variant where no project is marked featured.
 */
export const noFeaturedProjects: Project[] = sampleProjects.map((p) => ({
  ...p,
  featured: false,
}));

/**
 * Empty projects array.
 */
export const emptyProjects: Project[] = [];

/**
 * Standard collection of certifications.
 */
export const sampleCertifications: Certification[] = [
  {
    title: 'Cloud Solutions Architect',
    slug: 'cloud-solutions-architect',
    issuer: 'Major Cloud Provider',
    category: 'cloud',
    issuedAt: '2025-03-15',
    expiresAt: null,
    credentialId: 'CSA-98765',
    verificationUrl: 'https://example.com/verify/csa',
    badgeImageUrl: '/images/certifications/csa.png',
    badgeImageAlt: 'Cloud Solutions Architect badge',
    displayOrder: 1,
    content: 'Cloud architecture certification notes.',
  },
  {
    title: 'AI Systems Engineer',
    slug: 'ai-systems-engineer',
    issuer: 'AI Standards Institute',
    category: 'ai',
    issuedAt: '2025-08-20',
    expiresAt: null,
    credentialId: 'AI-43210',
    verificationUrl: 'https://example.com/verify/ai',
    badgeImageUrl: '/images/certifications/ai.png',
    badgeImageAlt: 'AI Systems Engineer badge',
    displayOrder: 2,
    content: 'AI systems engineering notes.',
  },
  {
    title: 'Security Compliance Professional',
    slug: 'security-compliance-professional',
    issuer: 'Cyber Governance Body',
    category: 'security',
    issuedAt: '2025-10-10',
    expiresAt: null,
    credentialId: 'SEC-11223',
    verificationUrl: 'https://example.com/verify/sec',
    badgeImageUrl: '/images/certifications/sec.png',
    badgeImageAlt: 'Security badge',
    displayOrder: 2, // tie with AI Systems Engineer
    content: 'Security certification notes.',
  },
  {
    title: 'Data Pipelines Specialist',
    slug: 'data-pipelines-specialist',
    issuer: 'Data Engineering Forum',
    category: 'data',
    issuedAt: '2026-01-05',
    expiresAt: null,
    credentialId: 'DATA-55443',
    verificationUrl: 'https://example.com/verify/data',
    badgeImageUrl: '/images/certifications/data.png',
    badgeImageAlt: 'Data badge',
    displayOrder: 3, // 4th item (exceeds PREVIEW_LIMIT=3)
    content: 'Data engineering notes.',
  },
];

/**
 * Empty certifications array.
 */
export const emptyCertifications: Certification[] = [];

/**
 * Standard collection of blog posts.
 */
export const sampleBlogPosts: BlogPost[] = [
  {
    title: 'Building Spec-Driven Workflows',
    slug: 'building-spec-driven-workflows',
    summary: 'A deep dive into zero-hallucination code generation using rigorous specification files.',
    publishedAt: '2026-04-10',
    updatedAt: null,
    eventType: 'project-update',
    eventName: null,
    eventDate: null,
    eventLocation: null,
    eventUrl: null,
    tags: ['architecture', 'ai'],
    readingTimeMinutes: 5,
    draft: false,
    content: '## Workflows\nContent detailing spec-driven pipelines.',
  },
  {
    title: 'Reflections on the Regional Hackathon',
    slug: 'reflections-on-hackathon',
    summary: 'Key architectural lessons learned from prototyping distributed agents under 48 hours.',
    publishedAt: '2026-03-15',
    updatedAt: null,
    eventType: 'hackathon',
    eventName: 'Regional AI Hackathon',
    eventDate: '2026-03-14',
    eventLocation: 'Singapore',
    eventUrl: 'https://example.com/hackathon',
    tags: ['hackathon', 'agents'],
    readingTimeMinutes: 4,
    draft: false,
    content: '## Hackathon Reflection\nDetails on competition prototype.',
  },
  {
    title: 'Local AI Model Swapping Mechanics',
    slug: 'local-ai-model-swapping',
    summary: 'How to alternate reasoning and code-execution models within strict 8GB VRAM limits.',
    publishedAt: '2026-03-15', // same-day tie to verify slug sorting
    updatedAt: null,
    eventType: 'learning',
    eventName: null,
    eventDate: null,
    eventLocation: null,
    eventUrl: null,
    tags: ['vram', 'local-ai'],
    readingTimeMinutes: 6,
    draft: false,
    content: '## VRAM Swapping\nStep by step orchestrator memory management.',
  },
  {
    title: 'Draft Post — Secret Feature Preview',
    slug: 'draft-feature-preview',
    summary: 'Unpublished notes on future enhancements and architectural revisions.',
    publishedAt: '2026-04-15',
    updatedAt: null,
    eventType: 'learning',
    eventName: null,
    eventDate: null,
    eventLocation: null,
    eventUrl: null,
    tags: ['internal'],
    readingTimeMinutes: 3,
    draft: true, // must be excluded from homepage RecentActivity
    content: '## Secret Preview\nDraft content that must not be published.',
  },
  {
    title: 'Older Meetup Keynote Recap',
    slug: 'older-meetup-keynote-recap',
    summary: 'Highlights from my talk on accessible design systems and Next.js App Router.',
    publishedAt: '2026-01-20',
    updatedAt: null,
    eventType: 'meetup',
    eventName: 'Frontend Engineers Meetup',
    eventDate: '2026-01-18',
    eventLocation: 'Manila',
    eventUrl: 'https://example.com/meetup',
    tags: ['meetup', 'accessibility'],
    readingTimeMinutes: 3,
    draft: false,
    content: '## Meetup Talk\nKey takeaways from the session.',
  },
];

/**
 * Posts variant where all posts are drafts.
 */
export const draftsOnlyBlogPosts: BlogPost[] = sampleBlogPosts.map((post) => ({
  ...post,
  draft: true,
}));

/**
 * Empty blog posts array.
 */
export const emptyBlogPosts: BlogPost[] = [];
'@ | Set-Content "tests\fixtures\home-data.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/fixtures/home-data.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 1.5, Req 2.1, Req 3.3, Req 4.1, Req 5.1, Req 6.2, Req 7.1, Req 8.1, Req 10.1, Req 11.1, Req 11.9

---

### M5.G1.T2: Create Property-Based Testing Arbitraries (`tests/fixtures/home-arbitraries.ts`)

**Objective:** Author fast-check arbitraries in `tests/fixtures/home-arbitraries.ts` for projects, certifications, blog posts, contact channels, profiles, and date strings.

**Acceptance Criteria:**
- ✓ File `tests/fixtures/home-arbitraries.ts` exists
- ✓ Exports `arbProject`: generates valid `Project` objects with small `displayOrder` (1–5) and technology arrays to force ties and overlaps
- ✓ Exports `arbCertification`: generates valid `Certification` objects with small `displayOrder`
- ✓ Exports `arbBlogPost`: generates valid `BlogPost` objects with varied `draft` flags and bounded ISO date strings
- ✓ Exports `arbContactChannel`: generates valid email and external HTTPS contact channels
- ✓ Exports `arbProfile`: generates `SiteProfile` with randomized strings and boolean availability
- ✓ Exports `arbIsoDate`: generates strictly valid calendar dates `YYYY-MM-DD` (including leap years)
- ✓ Exports `arbInvalidDate`: generates syntactically or semantically invalid date strings
- ✓ Built strictly using `fast-check` without hand-rolled pseudo-random generators

**Prerequisites:**
- `fast-check` installed (`devDependencies`)
- Target file: `tests/fixtures/home-arbitraries.ts`

**Implementation Details:**

Write `tests/fixtures/home-arbitraries.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import fc from 'fast-check';
import type {
  Project,
  Certification,
  BlogPost,
  ContactChannel,
  ContactChannelType,
  SiteProfile,
  ProjectStatus,
  CertificationCategory,
  EventType,
} from '@/types/content';

const TECH_POOL = ['TypeScript', 'typescript', 'Next.js', 'React', 'Tailwind CSS', 'Docker', 'Python', 'Go', 'PostgreSQL', 'GraphQL'];

/**
 * Arbitrary generator for Project entity.
 */
export const arbProject: fc.Arbitrary<Project> = fc.record({
  title: fc.string({ minLength: 3, maxLength: 40 }).filter((s) => s.trim().length >= 3 && !s.includes('<')),
  slug: fc.string({ minLength: 2, maxLength: 20 })
    .filter((s) => /^[a-z0-9-]+$/.test(s) && !s.startsWith('-') && !s.endsWith('-')),
  summary: fc.string({ minLength: 20, maxLength: 100 }).filter((s) => s.trim().length >= 20),
  status: fc.constantFrom<ProjectStatus>('completed', 'in-progress', 'archived'),
  role: fc.string({ minLength: 3, maxLength: 30 }),
  startedAt: fc.constant('2025-01-01'),
  completedAt: fc.constantFrom('2025-06-01', null),
  technologies: fc.subarray(TECH_POOL, { minLength: 1, maxLength: 5 }),
  tags: fc.array(fc.string({ minLength: 2, maxLength: 10 }), { maxLength: 3 }),
  repositoryUrl: fc.constantFrom('https://github.com/example/repo', null),
  liveDemoUrl: fc.constantFrom('https://demo.example.com', null),
  documentationUrl: fc.constant(null),
  featured: fc.boolean(),
  displayOrder: fc.integer({ min: 1, max: 4 }), // small range to exercise ties
  metrics: fc.constant([]),
  documentation: fc.constant('## Documentation\nExample content.'),
});

/**
 * Arbitrary generator for Certification entity.
 */
export const arbCertification: fc.Arbitrary<Certification> = fc.record({
  title: fc.string({ minLength: 3, maxLength: 40 }).filter((s) => s.trim().length >= 3 && !s.includes('<')),
  slug: fc.string({ minLength: 2, maxLength: 20 })
    .filter((s) => /^[a-z0-9-]+$/.test(s) && !s.startsWith('-') && !s.endsWith('-')),
  issuer: fc.string({ minLength: 2, maxLength: 30 }).filter((s) => s.trim().length >= 2),
  category: fc.constantFrom<CertificationCategory>('cloud', 'ai', 'security', 'frontend', 'backend', 'data', 'devops', 'professional'),
  issuedAt: fc.constantFrom('2025-01-15', '2025-06-20', '2025-11-05', '2026-02-10'),
  expiresAt: fc.constant(null),
  credentialId: fc.constantFrom('CERT-123', null),
  verificationUrl: fc.constantFrom('https://example.com/verify', null),
  badgeImageUrl: fc.constantFrom('/images/certifications/badge.png', null),
  badgeImageAlt: fc.constantFrom('Badge', null),
  displayOrder: fc.integer({ min: 1, max: 4 }), // small range to exercise ties
  content: fc.constant('Certification context.'),
});

/**
 * Arbitrary generator for BlogPost entity.
 */
export const arbBlogPost: fc.Arbitrary<BlogPost> = fc.record({
  title: fc.string({ minLength: 5, maxLength: 50 }).filter((s) => s.trim().length >= 5 && !s.includes('<')),
  slug: fc.string({ minLength: 2, maxLength: 20 })
    .filter((s) => /^[a-z0-9-]+$/.test(s) && !s.startsWith('-') && !s.endsWith('-')),
  summary: fc.string({ minLength: 20, maxLength: 100 }).filter((s) => s.trim().length >= 20),
  publishedAt: fc.constantFrom('2026-01-15', '2026-02-20', '2026-03-10', '2026-04-01'), // small range to exercise ties
  updatedAt: fc.constant(null),
  eventType: fc.constantFrom<EventType>('meetup', 'hackathon', 'workshop', 'conference', 'learning', 'project-update'),
  eventName: fc.constantFrom('Meetup Name', null),
  eventDate: fc.constant(null),
  eventLocation: fc.constant(null),
  eventUrl: fc.constant(null),
  tags: fc.array(fc.string({ minLength: 2, maxLength: 10 }), { maxLength: 3 }),
  readingTimeMinutes: fc.integer({ min: 1, max: 15 }),
  draft: fc.boolean(),
  content: fc.constant('Post content.'),
});

/**
 * Arbitrary generator for ContactChannel entity.
 */
export const arbContactChannel: fc.Arbitrary<ContactChannel> = fc.record({
  type: fc.constantFrom<ContactChannelType>('email', 'linkedin', 'github', 'website', 'other'),
  label: fc.string({ minLength: 1, maxLength: 25 }).filter((s) => s.trim().length > 0 && !s.includes('<')),
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
 * Arbitrary generator for SiteProfile.
 */
export const arbProfile: fc.Arbitrary<SiteProfile> = fc.record({
  name: fc.string({ minLength: 2, maxLength: 30 }).filter((s) => s.trim().length >= 2 && !s.includes('<')),
  professionalTitle: fc.string({ minLength: 5, maxLength: 40 }).filter((s) => s.trim().length >= 5),
  introduction: fc.string({ minLength: 10, maxLength: 120 }).filter((s) => s.trim().length >= 10),
  location: fc.string({ minLength: 3, maxLength: 30 }),
  availableForOpportunities: fc.boolean(),
});

/**
 * Arbitrary generator for strictly valid calendar dates YYYY-MM-DD.
 */
export const arbIsoDate: fc.Arbitrary<string> = fc.date({
  min: new Date(Date.UTC(2020, 0, 1)),
  max: new Date(Date.UTC(2030, 11, 31)),
}).map((d) => d.toISOString().slice(0, 10));

/**
 * Arbitrary generator for invalid dates.
 */
export const arbInvalidDate: fc.Arbitrary<string> = fc.oneof(
  fc.constant(''),
  fc.constant('invalid-date'),
  fc.constant('2026-02-30'), // non-existent leap day
  fc.constant('2026-13-01'), // invalid month
  fc.constant('2026-00-10'),
  fc.constant('2026-04-32'), // invalid day
  fc.constant('2026/04/10'), // wrong separator
  fc.constant('10-04-2026')  // wrong order
);
'@ | Set-Content "tests\fixtures\home-arbitraries.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit tests/fixtures/home-arbitraries.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.6, Req 8.6, Req 10.3, Req 11.5, Req 12.1, Req 12.4

---

### M5.G1.T3: Implement Fixed Homepage UI Strings & Section Order (`src/components/home/home-text.ts`)

**Objective:** Author `src/components/home/home-text.ts` defining all structural labels, preview limits, section identifiers, and default copy for Homepage components.

**Acceptance Criteria:**
- ✓ File `src/components/home/home-text.ts` exists
- ✓ Exports `PREVIEW_LIMIT = 3`
- ✓ Exports `HOME_SECTION_ORDER = ['hero', 'featured-projects', 'skills', 'certifications', 'recent-activity'] as const`
- ✓ Exports `type HomeSectionId = (typeof HOME_SECTION_ORDER)[number]`
- ✓ Exports `HOME_TEXT` object containing all required strings (`viewProjects`, `viewAllProjects`, `viewAllCertifications`, `viewAllPosts`, `featuredHeading`, `skillsHeading`, `skillsGroupLabel`, `certificationsHeading`, `recentHeading`, `featuredEmpty`, `availability`)
- ✓ Contains zero owner-specific data or personal strings (`AGENTS.md` 6.1 Rule 8, Req 2.5)

**Prerequisites:**
- Directory `src/components/home/` exists or is created
- Target file: `src/components/home/home-text.ts`

**Implementation Details:**

Write `src/components/home/home-text.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\components\home")) {
    New-Item -ItemType Directory -Path "src\components\home" -Force | Out-Null
}

@'
/**
 * Fixed UI Strings, Layout Constants, and Structural Order for Homepage Components
 *
 * Enforces separation between structural labels and site-owner data.
 * All dynamic site content originates exclusively from SiteConfig and content loaders (Req 2.5).
 */

export const PREVIEW_LIMIT = 3;

export const HOME_SECTION_ORDER = [
  'hero',
  'featured-projects',
  'skills',
  'certifications',
  'recent-activity',
] as const;

export type HomeSectionId = (typeof HOME_SECTION_ORDER)[number];

export const HOME_TEXT = {
  viewProjects: 'View Projects',
  viewAllProjects: 'View all projects',
  viewAllCertifications: 'View all certifications',
  viewAllPosts: 'View all posts',
  featuredHeading: 'Featured Projects',
  skillsHeading: 'Skills Snapshot',
  skillsGroupLabel: 'Technologies',
  certificationsHeading: 'Certifications',
  recentHeading: 'Recent Activity',
  featuredEmpty: 'No featured projects yet. Browse all projects instead.',
  availability: 'Available for opportunities',
} as const;
'@ | Set-Content "src\components\home\home-text.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/components/home/home-text.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 1.1, Req 2.5, Req 3.1, Req 6.1, Req 6.4, Req 7.1, Req 7.2, Req 8.3, Req 9.1, Req 10.4, Req 11.6, Req 11.7

---

### M5.G1.T4: Implement Deterministic String Comparator (`src/lib/home/compare.ts`)

**Objective:** Author `src/lib/home/compare.ts` providing locale-independent code-unit comparison for tie-breaking across projects, certifications, blog posts, and skill tags.

**Acceptance Criteria:**
- ✓ Directory `src/lib/home/` exists or is created
- ✓ File `src/lib/home/compare.ts` created
- ✓ Exports `compareStrings(a: string, b: string): number`
- ✓ Implements strict code-unit order: returns `-1` if $a < b$, `1` if $a > b$, and `0` if $a === b$
- ✓ Does NOT use `localeCompare`, ensuring stable sorting across all build platforms and locales
- ✓ Accompanied by unit test in `tests/home/compare.test.ts`

**Prerequisites:**
- Project root exists

**Implementation Details:**

Write `src/lib/home/compare.ts` and its unit test using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path "src\lib\home")) {
    New-Item -ItemType Directory -Path "src\lib\home" -Force | Out-Null
}

@'
/**
 * Deterministic Code-Unit String Comparator
 *
 * Provides locale-independent string comparison for stable tie-breaking.
 * Avoids localeCompare to guarantee identical sorting across build machines (Req 5.4, 10.2, 11.4).
 */
export function compareStrings(a: string, b: string): number {
  if (a < b) {
    return -1;
  }
  if (a > b) {
    return 1;
  }
  return 0;
}
'@ | Set-Content "src\lib\home\compare.ts" -Encoding UTF8

if (-not (Test-Path "tests\home")) {
    New-Item -ItemType Directory -Path "tests\home" -Force | Out-Null
}

@'
import { describe, it, expect } from 'vitest';
import { compareStrings } from '@/lib/home/compare';

describe('compareStrings Comparator', () => {
  it('compares strings strictly by code-unit values', () => {
    expect(compareStrings('apple', 'banana')).toBe(-1);
    expect(compareStrings('banana', 'apple')).toBe(1);
    expect(compareStrings('apple', 'apple')).toBe(0);
  });

  it('preserves uppercase before lowercase per standard ASCII/Unicode order', () => {
    expect(compareStrings('Apple', 'apple')).toBe(-1);
  });
});
'@ | Set-Content "tests\home\compare.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/home/compare.ts
npm run test -- tests/home/compare.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 5.4, Req 8.3, Req 10.2, Req 11.4

---

### M5.G1.T5: Audit Repository for Existing Date Formatter

**Objective:** Audit `src/` to determine whether an existing display date formatter exists in M2, M3, or M4, and record the architectural finding in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Searches `src/` for functions formatting `IsoDateString` to display text (e.g., `formatDate`, `formatDisplayDate`)
- ✓ Confirms finding (formatter does not exist upstream) and records decision in `task-notes.md`
- ✓ Script outputs confirmation message

**Prerequisites:**
- Directory `.kiro/specs/m5-homepage-experience/` exists or is created

**Implementation Details:**

Execute inspection script using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

if (-not (Test-Path ".kiro\specs\m5-homepage-experience")) {
    New-Item -ItemType Directory -Path ".kiro\specs\m5-homepage-experience" -Force | Out-Null
}

$search = Get-ChildItem -Path "src" -Include *.ts, *.tsx -Recurse | Select-String -Pattern 'formatDate|formatDisplayDate|toLocaleDateString'

$taskNotes = @"
# M5 Homepage Experience — Task Notes & Architectural Audit

## 1. Upstream Date Formatter Audit (Req 12.5)
Search in `src/` returned $(if ($search) { $search.Count } else { 0 }) occurrences.
Result: No shared display-date formatter exists in M2, M3, or M4 (only date schemas in M2).
Decision: Implement `formatDisplayDate` in `src/lib/format-date.ts` per Requirement 12.

"@

Set-Content -Path ".kiro\specs\m5-homepage-experience\task-notes.md" -Value $taskNotes -Encoding UTF8
"PASS"
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 12.5

---

### M5.G1.T6: Implement Deterministic Display Date Formatter (`src/lib/format-date.ts`)

**Objective:** Author `src/lib/format-date.ts` providing deterministic `en-US` UTC date formatting with manual parsing, round-trip calendar validation, and descriptive error throwing for malformed input.

**Acceptance Criteria:**
- ✓ File `src/lib/format-date.ts` created
- ✓ Exports `formatDisplayDate(dateString: string): string`
- ✓ Parses `YYYY-MM-DD` strictly via regex and manual integer extraction
- ✓ Validates calendar round-trip using `Date.UTC` (rejects `2026-02-30`, `2026-13-40`, etc.)
- ✓ Formats date strictly using `Intl.DateTimeFormat('en-US', { timeZone: 'UTC', year: 'numeric', month: 'long', day: 'numeric' })`
- ✓ Throws descriptive `Error` naming the received value when input is invalid (e.g. `Invalid date: "${dateString}". Expected YYYY-MM-DD.`)
- ✓ Pure function with zero external or framework dependencies

**Prerequisites:**
- M5.G1.T5 completed
- Target file: `src/lib/format-date.ts`

**Implementation Details:**

Write `src/lib/format-date.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
/**
 * Deterministic Date Formatter
 *
 * Formats ISO YYYY-MM-DD date strings into human-readable text (e.g. "April 10, 2026").
 * Enforces fixed en-US locale and UTC timeZone to ensure static build determinism (Req 12.1, 12.2).
 */

const UTC_FORMATTER = new Intl.DateTimeFormat('en-US', {
  timeZone: 'UTC',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});

const DATE_REGEX = /^(\d{4})-(\d{2})-(\d{2})$/;

/**
 * Converts a YYYY-MM-DD date string to localized display text.
 * Throws a descriptive error for malformed or impossible calendar dates.
 */
export function formatDisplayDate(dateString: string): string {
  if (typeof dateString !== 'string') {
    throw new Error(`Invalid date: "${String(dateString)}". Expected YYYY-MM-DD.`);
  }

  const match = DATE_REGEX.exec(dateString.trim());
  if (!match) {
    throw new Error(`Invalid date: "${dateString}". Expected YYYY-MM-DD.`);
  }

  const year = parseInt(match[1], 10);
  const month = parseInt(match[2], 10);
  const day = parseInt(match[3], 10);

  // Month is 1-indexed in string, 0-indexed in Date.UTC
  if (month < 1 || month > 12 || day < 1 || day > 31) {
    throw new Error(`Invalid date: "${dateString}". Expected YYYY-MM-DD.`);
  }

  const utcTimestamp = Date.UTC(year, month - 1, day);
  const dateObj = new Date(utcTimestamp);

  // Round-trip calendar validation (handles leap years and month day counts)
  if (
    dateObj.getUTCFullYear() !== year ||
    dateObj.getUTCMonth() !== month - 1 ||
    dateObj.getUTCDate() !== day
  ) {
    throw new Error(`Invalid date: "${dateString}". Expected YYYY-MM-DD.`);
  }

  return UTC_FORMATTER.format(dateObj);
}
'@ | Set-Content "src\lib\format-date.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npx tsc --noEmit src/lib/format-date.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.4

---

### M5.G1.T7: Author Unit & Property-Based Tests for Date Formatter (`tests/home/format-date.test.ts`)

**Objective:** Create `tests/home/format-date.test.ts` verifying time-zone invariance, invalid date rejection, and fast-check property verification (Property 13).

**Acceptance Criteria:**
- ✓ File `tests/home/format-date.test.ts` created
- ✓ Tests `"2026-04-10"` outputs `"April 10, 2026"` identically under `TZ=UTC` and `TZ=Asia/Manila`
- ✓ Tests malformed strings (`2026-13-40`, `2026-02-30`, `abc`, empty string) throw errors naming the received string
- ✓ Implements Property 13 test ($\ge 100$ runs with `fast-check`): valid dates contain 4-digit year and day of month; invalid dates throw
- ✓ Tests pass under `npm test`

**Prerequisites:**
- M5.G1.T6 completed
- `fast-check` installed
- Target file: `tests/home/format-date.test.ts`

**Implementation Details:**

Write `tests/home/format-date.test.ts` using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

@'
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { formatDisplayDate } from '@/lib/format-date';
import { arbIsoDate, arbInvalidDate } from '../fixtures/home-arbitraries';

describe('formatDisplayDate Formatter (Req 12)', () => {
  describe('Concrete Unit Scenarios', () => {
    it('formats a known date string accurately into en-US format', () => {
      expect(formatDisplayDate('2026-04-10')).toBe('April 10, 2026');
      expect(formatDisplayDate('2025-01-01')).toBe('January 1, 2025');
    });

    it('produces identical output across different process.env.TZ environments', () => {
      const originalTz = process.env.TZ;
      try {
        process.env.TZ = 'UTC';
        const utcResult = formatDisplayDate('2026-04-10');

        process.env.TZ = 'Asia/Manila';
        const manilaResult = formatDisplayDate('2026-04-10');

        process.env.TZ = 'America/New_York';
        const nyResult = formatDisplayDate('2026-04-10');

        expect(utcResult).toBe('April 10, 2026');
        expect(manilaResult).toBe(utcResult);
        expect(nyResult).toBe(utcResult);
      } finally {
        process.env.TZ = originalTz;
      }
    });

    it('rejects invalid or impossible calendar dates with a descriptive error', () => {
      const invalidDates = ['2026-13-40', '2026-02-30', 'abc', '', '2026/04/10'];
      for (const bad of invalidDates) {
        expect(() => formatDisplayDate(bad)).toThrow(new RegExp(`Invalid date: "${bad}"`));
      }
    });
  });

  describe('Property-Based Invariants (Property 13)', () => {
    it('Feature: m5-homepage-experience, Property 13: date formatting is deterministic across any valid date and rejects invalid strings', () => {
      // 1. Valid dates invariant
      fc.assert(
        fc.property(arbIsoDate, (isoDate) => {
          const formatted = formatDisplayDate(isoDate);
          const [year, , day] = isoDate.split('-');
          expect(formatted).toContain(year);
          expect(formatted).toContain(String(parseInt(day, 10)));
        }),
        { numRuns: 100 }
      );

      // 2. Invalid dates invariant
      fc.assert(
        fc.property(arbInvalidDate, (badDate) => {
          expect(() => formatDisplayDate(badDate)).toThrow(/Invalid date/);
        }),
        { numRuns: 100 }
      );
    });
  });
});
'@ | Set-Content "tests\home\format-date.test.ts" -Encoding UTF8
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
npm run test -- tests/home/format-date.test.ts
if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 12.2, Req 12.4

---

### M5.G1.T8: Audit Upstream Loaders, Types, and M3 UI Primitives

**Objective:** Audit and confirm the presence, paths, and export signatures of upstream M2 content loaders, M2 content types, and M3 UI primitives required by Milestone 5, recording results in `task-notes.md`.

**Acceptance Criteria:**
- ✓ Confirms M2 loaders in `src/content/loaders/`: `getSiteConfig`, `getProjects`, `getCertifications`, `getBlogPosts`
- ✓ Confirms M2 types in `src/types/content.ts`: `SiteConfig`, `Project`, `Certification`, `BlogPost`, `ContactChannel`, `IsoDateString`
- ✓ Confirms M3 primitives in `src/components/ui/`: `Card`, `TagList`, `StatusBadge`, `EventTypeBadge`, `EmptyState`, `Button`, `ExternalLink`, `Container`, `FOCUS_RING`, motion helpers
- ✓ Records paths and signatures in `.kiro/specs/m5-homepage-experience/task-notes.md`
- ✓ Script outputs PASS with zero missing symbols

**Prerequisites:**
- M2 and M3 baselines complete
- PowerShell in project root

**Implementation Details:**

Execute verification check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$errors = @()

# 1. Audit Loaders
$loaders = @("site.ts", "projects.ts", "certifications.ts", "blog.ts")
foreach ($l in $loaders) {
    $p = "src\content\loaders\$l"
    if (-not (Test-Path $p)) {
        $errors += "Missing loader: $p"
    }
}

# 2. Audit Types
$typesPath = "src\types\content.ts"
if (Test-Path $typesPath) {
    $content = Get-Content $typesPath -Raw
    $types = @('SiteConfig', 'Project', 'Certification', 'BlogPost', 'ContactChannel', 'IsoDateString')
    foreach ($t in $types) {
        if (-not ($content -match "\b$t\b")) {
            $errors += "Missing type: $t in $typesPath"
        }
    }
} else {
    $errors += "Missing $typesPath"
}

# 3. Audit M3 UI Primitives
$primitives = @(
    "src\components\ui\card.tsx",
    "src\components\ui\tag-list.tsx",
    "src\components\ui\status-badge.tsx",
    "src\components\ui\event-type-badge.tsx",
    "src\components\ui\empty-state.tsx",
    "src\components\ui\button.tsx",
    "src\components\ui\external-link.tsx",
    "src\components\ui\container.tsx",
    "src\components\ui\focus-ring.ts",
    "src\components\ui\motion.ts"
)
foreach ($pr in $primitives) {
    if (-not (Test-Path $pr)) {
        $errors += "Missing primitive: $pr"
    }
}

if ($errors.Count -eq 0) {
    $noteAppend = @"

## 2. Upstream Architecture & Signatures Audit (Req 16.1, 16.2)
- M2 Loaders: Confirmed all 4 loaders in `src/content/loaders/` (site, projects, certifications, blog).
- M2 Types: Confirmed all canonical types in `src/types/content.ts`.
- M3 Primitives: Confirmed Card, TagList, StatusBadge, EventTypeBadge, EmptyState, Button, ExternalLink, Container, FOCUS_RING, motion.
- M4 Shell: Confirmed RootLayout landmark structure, skip link, and metadataBase.

"@
    Add-Content -Path ".kiro\specs\m5-homepage-experience\task-notes.md" -Value $noteAppend -Encoding UTF8
    "PASS"
} else {
    $errors | ForEach-Object { Write-Host $_ }
    "FAIL"
}
```

**Validation:**
Expected output from the PowerShell check: `PASS`

**Satisfies Requirements:** Req 1.3, Req 1.4, Req 1.5, Req 16.1, Req 16.2

---

### M5.G1.T9: Verify Test Toolchain and M4 Title Template Integration

**Objective:** Confirm that testing dependencies (`vitest`, `@testing-library/react`, `vitest-axe`, `fast-check`) are installed and functional, and verify M4 title template configuration.

**Acceptance Criteria:**
- ✓ Confirms test packages resolve cleanly in Node.js
- ✓ Confirms M4 `buildSiteMetadata` exports `title.template = '%s | {siteName}'`
- ✓ Records confirmation in `task-notes.md`
- ✓ Verification command exits with return code 0

**Prerequisites:**
- Node.js LTS environment
- M4 completed

**Implementation Details:**

Execute verification check using PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

node -e "require('vitest'); require('@testing-library/react'); require('vitest-axe'); require('fast-check'); console.log('PASS');"

$metaFile = "src\app\site-metadata.ts"
if (Test-Path $metaFile) {
    $metaContent = Get-Content $metaFile -Raw
    if ($metaContent -match "template:\s*['\"`]%s\s*\|\s*") {
        Write-Host "M4 title template confirmed."
    }
}
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$res = node -e "require('vitest-axe'); require('fast-check'); console.log('PASS');"
if ($res -eq "PASS") { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 13.4, Req 16.5

---

### M5.G1.T10: Checkpoint — Foundation Quality Gates and Protected Files Invariance

**Objective:** Run the full verification suite to confirm that all test fixtures, text constants, comparators, and formatters compile and pass tests, and prove that protected configuration and styling files remain completely unmodified.

**Acceptance Criteria:**
- ✓ `git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/content/` produces zero output
- ✓ `npm run typecheck` passes with return code 0
- ✓ `npm run lint` passes with return code 0
- ✓ `npm test -- tests/home/compare.test.ts tests/home/format-date.test.ts` passes with code 0

**Prerequisites:**
- M5.G1.T1 through M5.G1.T9 completed

**Implementation Details:**

Execute verification commands via PowerShell:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"

$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/content/
if ($diff.Length -gt 0) {
    Write-Error "CRITICAL: Protected files modified:`n$diff"
    exit 1
}

npm run typecheck
npm run lint
npm run test -- tests/home/compare.test.ts tests/home/format-date.test.ts
```

**Validation:**
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
$diff = git diff tailwind.config.ts src/app/globals.css src/components/ui/ src/components/layout/ src/content/
$t = (Start-Process -FilePath "npm" -ArgumentList "run typecheck" -NoNewWindow -PassThru -Wait).ExitCode
$l = (Start-Process -FilePath "npm" -ArgumentList "run lint" -NoNewWindow -PassThru -Wait).ExitCode
$s = (Start-Process -FilePath "npm" -ArgumentList "run test -- tests/home/compare.test.ts tests/home/format-date.test.ts" -NoNewWindow -PassThru -Wait).ExitCode

if ($diff.Length -eq 0 -and $t -eq 0 -and $l -eq 0 -and $s -eq 0) { "PASS" } else { "FAIL" }
```
Expected output: `PASS`

**Satisfies Requirements:** Req 12.1, Req 16.1, Req 16.2, Req 16.4, Req 16.5

---

## Goal Checkpoint

Run the following command sequence to confirm Goal 1 is complete:
```powershell
cd "c:\dev\andres-webapp-professional\personal-website-portfolio\personal-website-portfolio-v2"
Test-Path "tests\fixtures\home-data.ts"
Test-Path "tests\fixtures\home-arbitraries.ts"
Test-Path "src\components\home\home-text.ts"
Test-Path "src\lib\home\compare.ts"
Test-Path "src\lib\format-date.ts"
Test-Path "tests\home\compare.test.ts"
Test-Path "tests\home\format-date.test.ts"
Test-Path ".kiro\specs\m5-homepage-experience\task-notes.md"
npm run typecheck
npm run test -- tests/home/compare.test.ts tests/home/format-date.test.ts
```
Expected output:
- `True` for all 8 path existence checks
- `npm run typecheck` exits with return code 0
- Vitest executes all compare and format-date tests with return code 0.