# Requirements Document

## Introduction

Milestone 1 (M1) establishes the foundational repository structure, build toolchain, and quality gates for the `personal-website-portfolio-v2` project. This milestone creates a Next.js App Router application with TypeScript strict mode, Tailwind CSS, comprehensive linting, type checking, testing infrastructure, and build pipeline. The foundation enables all subsequent development milestones while enforcing architectural constraints defined in the master specification files.

This milestone delivers a verified, executable repository skeleton that passes all quality gates without implementing content schemas, design systems, or application routes.

## Glossary

- **Build_Pipeline**: The automated process that validates, compiles, and bundles source code into deployable static assets
- **Next_App_Router**: Next.js 15+ application structure using the `app/` directory convention for file-based routing
- **TypeScript_Strict_Mode**: TypeScript compiler configuration with `strict: true` and all strict family options enabled
- **Quality_Gate**: A verification checkpoint that must pass before code can be merged or deployed
- **Tailwind_CSS**: Utility-first CSS framework configured with custom design tokens
- **Verification_Pipeline**: The sequential execution of install, lint, typecheck, test, and build commands
- **Schema_Validator**: Library for runtime type validation and parsing (Zod or equivalent)
- **Repository_Root**: The top-level directory `personal-website-portfolio-v2/` containing all project files
- **SGDS_Tokens**: Singapore Government Design System-inspired semantic design tokens for colors, spacing, typography, and other visual properties
- **ESLint**: Pluggable JavaScript and TypeScript linting tool for code quality and style enforcement
- **Test_Framework**: Testing infrastructure (Vitest or Jest) for unit and integration tests
- **Content_Directory**: Local file-based content storage location at `content/` for Markdown and JSON files

## Requirements

### Requirement 1: Next.js App Router Project Initialization

**User Story:** As a developer, I want a properly initialized Next.js 15+ App Router project with TypeScript, so that I can build a modern, statically-rendered portfolio application with type safety.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a Next.js project initialized with App Router architecture
2. THE Package_Configuration SHALL specify Next.js version 15.0.0 or later
3. THE Package_Configuration SHALL specify React version 19.0.0 or later compatible with the Next.js version
4. THE Package_Configuration SHALL specify TypeScript as a dependency
5. THE Repository_Root SHALL contain a `next.config.ts` file with TypeScript configuration
6. THE Next_Config SHALL enable static export compatibility for Vercel deployment
7. THE Repository_Root SHALL contain a valid `package.json` with name `personal-website-portfolio-v2`
8. THE Package_Configuration SHALL define all five required scripts: `lint`, `typecheck`, `test`, `build`, and `dev`
9. WHEN the project is initialized, THE Repository_Root SHALL NOT contain any runtime database dependencies
10. WHEN the project is initialized, THE Repository_Root SHALL NOT contain any authentication libraries

### Requirement 2: TypeScript Strict Mode Configuration

**User Story:** As a developer, I want TypeScript configured with strict mode and zero unsafe patterns, so that I can prevent type-related runtime errors and maintain code quality.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `tsconfig.json` file with TypeScript configuration
2. THE TypeScript_Configuration SHALL enable `strict: true` mode
3. THE TypeScript_Configuration SHALL enable `noUncheckedIndexedAccess: true`
4. THE TypeScript_Configuration SHALL enable `noImplicitAny: true` (implied by strict, but explicit is acceptable)
5. THE TypeScript_Configuration SHALL enable `strictNullChecks: true` (implied by strict, but explicit is acceptable)
6. THE TypeScript_Configuration SHALL set `module` to support Next.js requirements
7. THE TypeScript_Configuration SHALL set `target` to `ES2022` or later
8. THE TypeScript_Configuration SHALL include path aliases with `@/` mapped to `./src/`
9. THE TypeScript_Configuration SHALL set `skipLibCheck: false` for maximum type safety
10. WHEN `npm run typecheck` is executed, THE Build_Pipeline SHALL fail if any implicit `any` types exist
11. WHEN `npm run typecheck` is executed, THE Build_Pipeline SHALL fail if any non-null assertions (`!`) are used without justification
12. WHEN `npm run typecheck` is executed, THE Build_Pipeline SHALL fail if any `any` types are explicitly used

### Requirement 3: Tailwind CSS Configuration

**User Story:** As a developer, I want Tailwind CSS configured with SGDS-inspired semantic tokens, so that I can build accessible, consistent UI components without hardcoding design values.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `tailwind.config.ts` file with TypeScript configuration
2. THE Tailwind_Configuration SHALL extend the default theme with SGDS_Tokens
3. THE Tailwind_Configuration SHALL define semantic color tokens for `bg-page`, `bg-surface`, `bg-inverse`, `text-primary`, `text-secondary`, `text-disabled`, `border-default`, `border-strong`, `brand-primary`, `brand-secondary`, `feedback-success`, `feedback-warning`, `feedback-danger`, and `focus-ring`
4. THE Tailwind_Configuration SHALL define spacing scale tokens from `space-1` (4px) through `space-24` (96px) using 4px base unit
5. THE Tailwind_Configuration SHALL define typography tokens for `text-caption`, `text-small`, `text-body`, `text-lead`, `text-heading-4`, `text-heading-3`, `text-heading-2`, and `text-heading-1`
6. THE Tailwind_Configuration SHALL define border radius tokens for `radius-sm` (4px), `radius-md` (8px), `radius-lg` (12px), and `radius-full` (9999px)
7. THE Tailwind_Configuration SHALL define elevation tokens for `elevation-0`, `elevation-1`, and `elevation-2` as box shadows
8. THE Tailwind_Configuration SHALL define motion duration tokens for `motion-fast` (150ms) and `motion-standard` (250ms)
9. THE Tailwind_Configuration SHALL configure content paths to scan `./src/**/*.{js,ts,jsx,tsx,mdx}`
10. THE Tailwind_Configuration SHALL support light and dark mode color tokens through CSS custom properties or Tailwind dark mode utilities
11. WHEN Tailwind is built, THE Output_Stylesheet SHALL include all defined semantic tokens
12. WHEN the repository is initialized, THE Global_Stylesheet SHALL import Tailwind base, components, and utilities

### Requirement 4: ESLint Configuration with TypeScript and Accessibility Rules

**User Story:** As a developer, I want comprehensive ESLint rules including TypeScript checks and accessibility validations, so that I can catch code quality issues and accessibility violations during development.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain an `.eslintrc.json` or `eslint.config.js` file with ESLint configuration
2. THE ESLint_Configuration SHALL extend `next/core-web-vitals` base configuration
3. THE ESLint_Configuration SHALL extend `@typescript-eslint/recommended` ruleset
4. THE ESLint_Configuration SHALL include `eslint-plugin-jsx-a11y` for accessibility checks
5. THE ESLint_Configuration SHALL enable the rule `@typescript-eslint/no-explicit-any` as error
6. THE ESLint_Configuration SHALL enable the rule `@typescript-eslint/no-non-null-assertion` as warning or error
7. THE ESLint_Configuration SHALL enable the rule `@typescript-eslint/no-unsafe-assignment` as error
8. THE ESLint_Configuration SHALL enable accessibility rules from `jsx-a11y` plugin
9. THE ESLint_Configuration SHALL configure the parser to `@typescript-eslint/parser`
10. WHEN `npm run lint` is executed, THE Build_Pipeline SHALL check all TypeScript and TSX files in `src/`
11. WHEN `npm run lint` is executed, THE Build_Pipeline SHALL report errors for explicit `any` types
12. WHEN `npm run lint` is executed, THE Build_Pipeline SHALL report errors for accessibility violations
13. WHEN `npm run lint` is executed with no violations, THE Command SHALL exit with code 0

### Requirement 5: Test Framework Setup

**User Story:** As a developer, I want a configured test framework with React testing utilities, so that I can write and execute unit and integration tests for components and utilities.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain test framework configuration (Vitest or Jest)
2. THE Test_Configuration SHALL support TypeScript test files
3. THE Test_Configuration SHALL support JSX and TSX test files
4. THE Test_Configuration SHALL include React Testing Library for component testing
5. THE Test_Configuration SHALL configure test file patterns to match `**/*.test.{ts,tsx}` and `**/*.spec.{ts,tsx}`
6. THE Test_Configuration SHALL set up path aliases matching TypeScript configuration (`@/` → `./src/`)
7. THE Repository_Root SHALL contain a `tests/` directory for test files
8. THE Repository_Root SHALL contain at least one example test file that passes
9. WHEN `npm run test` is executed, THE Test_Framework SHALL discover and run all test files
10. WHEN `npm run test` is executed, THE Test_Framework SHALL report test results with pass/fail status
11. WHEN `npm run test` is executed with all tests passing, THE Command SHALL exit with code 0
12. WHEN `npm run test` is executed with any test failing, THE Command SHALL exit with non-zero code

### Requirement 6: Directory Structure Creation

**User Story:** As a developer, I want the complete directory structure defined in AGENTS.md created, so that all milestones have consistent file locations and the repository matches the architectural specification.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `content/` directory for local content files
2. THE Content_Directory SHALL contain subdirectories `projects/`, `certifications/`, and `blog/`
3. THE Repository_Root SHALL contain a `public/` directory for static assets
4. THE Public_Directory SHALL contain subdirectories `images/` and `files/`
5. THE Public_Images_Directory SHALL contain subdirectories `projects/`, `certifications/`, and `blog/`
6. THE Repository_Root SHALL contain a `src/` directory for application source code
7. THE Src_Directory SHALL contain subdirectories `app/`, `components/`, `content/`, `lib/`, and `types/`
8. THE Src_Components_Directory SHALL contain subdirectories `layout/`, `home/`, `projects/`, `certifications/`, `blog/`, and `ui/`
9. THE Src_Content_Directory SHALL contain subdirectories `loaders/`, `markdown/`, and `schemas/`
10. THE Repository_Root SHALL contain a `tests/` directory for test files
11. WHEN the directory structure is created, THE Repository SHALL NOT contain a `pages/` directory (Pages Router)
12. WHEN the directory structure is created, THE Repository SHALL NOT contain a `styles/` directory at root level

### Requirement 7: Package Scripts Configuration

**User Story:** As a developer, I want all required npm scripts configured according to TRD.md Section 8.1, so that I can execute the standard verification pipeline locally and in CI/CD.

#### Acceptance Criteria

1. THE Package_Configuration SHALL define a `dev` script that starts the Next.js development server
2. THE Package_Configuration SHALL define a `build` script that executes `next build`
3. THE Package_Configuration SHALL define a `lint` script that executes ESLint on all source files
4. THE Package_Configuration SHALL define a `typecheck` script that executes `tsc --noEmit`
5. THE Package_Configuration SHALL define a `test` script that executes the test framework
6. THE Lint_Script SHALL check files in the `src/` directory with extensions `.ts`, `.tsx`, `.js`, `.jsx`
7. THE Test_Script SHALL run in non-watch mode by default for CI compatibility
8. WHEN `npm ci` is executed, THE Command SHALL install dependencies from lock file
9. WHEN `npm run dev` is executed, THE Development_Server SHALL start on localhost
10. WHEN `npm run build` is executed, THE Build_Pipeline SHALL produce static output in `.next/` directory
11. WHEN any verification script fails, THE Command SHALL exit with non-zero code
12. WHEN all verification scripts pass, THE Command SHALL exit with code 0

### Requirement 8: Schema Validator Dependency

**User Story:** As a developer, I want Zod or equivalent schema validator installed, so that content validation can be implemented in Milestone 2 without additional dependency changes.

#### Acceptance Criteria

1. THE Package_Configuration SHALL include Zod version 3.x or later as a production dependency
2. THE Schema_Validator SHALL support TypeScript type inference from schemas
3. THE Schema_Validator SHALL support runtime validation with descriptive error messages
4. THE Schema_Validator SHALL support object, array, string, number, boolean, date, and union types
5. THE Schema_Validator SHALL support optional and nullable field definitions
6. WHEN Zod is imported in TypeScript files, THE TypeScript_Compiler SHALL resolve types correctly
7. WHEN a schema is defined, THE Schema_Validator SHALL infer TypeScript types without manual type definitions

### Requirement 9: Repository Documentation

**User Story:** As a developer or autonomous agent, I want comprehensive README documentation, so that I understand the repository structure, verification commands, and architectural constraints.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `README.md` file with project documentation
2. THE README SHALL include the project name `personal-website-portfolio-v2`
3. THE README SHALL include a brief description referencing specification-driven development approach
4. THE README SHALL document all five required npm scripts with descriptions
5. THE README SHALL document the directory structure with brief explanations
6. THE README SHALL reference master specification files: `PRD.md`, `TRD.md`, `AGENTS.md`, `design.md`
7. THE README SHALL document TypeScript strict mode requirement
8. THE README SHALL document the SGDS-inspired design token approach
9. THE README SHALL state that no runtime database, authentication, or public API is used in MVP
10. THE README SHALL include a "Prerequisites" section listing Node.js and npm version requirements
11. THE README SHALL include a "Getting Started" section with install and run instructions
12. THE README SHALL include a "Verification Pipeline" section documenting the quality gate sequence

### Requirement 10: Git Configuration and Ignores

**User Story:** As a developer, I want proper Git ignore patterns configured, so that generated files, dependencies, environment files, and IDE artifacts are not committed to version control.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `.gitignore` file with ignore patterns
2. THE Gitignore_File SHALL exclude `node_modules/` directory
3. THE Gitignore_File SHALL exclude `.next/` build output directory
4. THE Gitignore_File SHALL exclude `out/` static export directory
5. THE Gitignore_File SHALL exclude `.env`, `.env.local`, `.env.*.local` files
6. THE Gitignore_File SHALL exclude `*.log` files
7. THE Gitignore_File SHALL exclude `.DS_Store` and OS-specific files
8. THE Gitignore_File SHALL exclude IDE directories like `.vscode/`, `.idea/`, `*.swp`
9. THE Gitignore_File SHALL exclude `coverage/` test coverage reports
10. THE Gitignore_File SHALL exclude `.vercel/` deployment configuration
11. WHEN sensitive files are created, THE Version_Control_System SHALL NOT track them
12. WHEN the repository is initialized, THE Gitignore_File SHALL NOT exclude the `public/` directory

### Requirement 11: Verification Pipeline Execution

**User Story:** As a developer, I want to execute the complete verification pipeline and have all quality gates pass, so that I can confirm the repository foundation is correctly configured before starting feature development.

#### Acceptance Criteria

1. WHEN `npm ci` is executed, THE Command SHALL complete successfully without errors
2. WHEN `npm run lint` is executed after install, THE Command SHALL complete with exit code 0
3. WHEN `npm run typecheck` is executed after install, THE Command SHALL complete with exit code 0
4. WHEN `npm run test` is executed after install, THE Command SHALL complete with exit code 0
5. WHEN `npm run build` is executed after install, THE Command SHALL complete with exit code 0
6. WHEN all verification commands are executed sequentially, THE Pipeline SHALL complete without any command failing
7. WHEN `npm run build` completes, THE Output_Directory SHALL contain generated static files
8. IF any verification command fails, THE Error_Message SHALL clearly indicate which check failed and why
9. THE Verification_Pipeline SHALL complete in less than 5 minutes on modern development hardware
10. THE Build_Output SHALL NOT contain any TypeScript errors
11. THE Build_Output SHALL NOT contain any ESLint errors
12. THE Repository SHALL be ready for Milestone 2 content schema implementation

### Requirement 12: Dependency Version Management

**User Story:** As a developer, I want explicit, compatible dependency versions with a lock file, so that builds are reproducible and dependency conflicts are prevented.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `package-lock.json` or `pnpm-lock.yaml` lock file
2. THE Package_Configuration SHALL use explicit version ranges or exact versions for all dependencies
3. THE Next_Dependency SHALL specify version `^15.0.0` or compatible range
4. THE React_Dependency SHALL specify version `^19.0.0` or compatible with Next.js version
5. THE TypeScript_Dependency SHALL specify version `^5.0.0` or later
6. THE Tailwind_Dependency SHALL specify current stable major version 3.x
7. THE ESLint_Dependency SHALL specify version compatible with Next.js requirements
8. THE Package_Configuration SHALL NOT include unused dependencies in production or development sections
9. WHEN dependencies are installed with `npm ci`, THE Installed_Versions SHALL match lock file exactly
10. WHEN dependencies are audited, THE Audit SHALL NOT report high or critical severity vulnerabilities in direct dependencies
11. THE Package_Configuration SHALL separate production dependencies from development dependencies correctly
12. THE Lock_File SHALL be committed to version control

### Requirement 13: PostCSS and Autoprefixer Configuration

**User Story:** As a developer, I want PostCSS configured with Autoprefixer for cross-browser CSS compatibility, so that Tailwind-generated styles work correctly across supported browsers.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `postcss.config.js` or `postcss.config.mjs` file
2. THE PostCSS_Configuration SHALL include the Tailwind CSS plugin
3. THE PostCSS_Configuration SHALL include the Autoprefixer plugin
4. THE Autoprefixer_Configuration SHALL target browsers matching "last 2 versions" or equivalent
5. THE Package_Configuration SHALL include `autoprefixer` as a development dependency
6. WHEN Tailwind CSS is processed, THE Output_Stylesheet SHALL include vendor prefixes for compatibility
7. WHEN the build is executed, THE PostCSS_Pipeline SHALL process CSS without errors

### Requirement 14: Type Definitions and Global Types

**User Story:** As a developer, I want global type definitions and Next.js-specific types configured, so that TypeScript recognizes Next.js APIs, environment variables, and custom global types.

#### Acceptance Criteria

1. THE Repository_Root SHALL contain a `next-env.d.ts` file for Next.js type definitions
2. THE Next_Env_Types SHALL reference Next.js and Next.js image types
3. IF custom global types are needed, THE Src_Types_Directory SHALL contain a `global.d.ts` file
4. THE TypeScript_Configuration SHALL include `next-env.d.ts` in types array
5. THE TypeScript_Configuration SHALL recognize Next.js-specific modules like `next/link` and `next/image`
6. WHEN TypeScript compiles, THE Compiler SHALL recognize all Next.js built-in types
7. WHEN custom type declarations are added, THE Compiler SHALL merge them with existing definitions

### Requirement 15: Development Environment Constraints

**User Story:** As a developer or autonomous agent, I want clear documentation of prohibited patterns and architectural boundaries, so that I do not accidentally violate the MVP architectural constraints.

#### Acceptance Criteria

1. THE README SHALL document that no runtime database may be added in MVP
2. THE README SHALL document that no authentication system may be added in MVP
3. THE README SHALL document that no custom API routes may be created in MVP
4. THE README SHALL document that no visitor tracking or analytics may be added in MVP
5. THE README SHALL document that all content must come from local Markdown and JSON files
6. THE README SHALL document that TypeScript `any`, `as`, and `!` are prohibited patterns
7. THE README SHALL document that design values must use semantic tokens, not hardcoded values
8. THE README SHALL reference AGENTS.md Section 6.1 for complete engineering rules
9. WHEN a developer attempts to install database clients, THE Documentation SHALL clearly state this violates MVP scope
10. WHEN an autonomous agent reads the README, THE Agent SHALL understand all architectural boundaries and prohibited patterns

