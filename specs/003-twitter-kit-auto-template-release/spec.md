# Feature Specification: Automated Template Release Generation for Twitter-Init-Kit

**Feature Branch**: `003-twitter-kit-auto-template-release`
**Created**: 2025-12-05
**Status**: Draft
**Input**: Automated template release generation for twitter-init-kit that packages .twitterkit folder contents for distribution on GitHub releases

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Release Manager Creates New Twitter-Kit Release (Priority: P1)

A Twitter-Kit maintainer wants to create a new release with templates for all supported AI agents (Claude, Cursor, Windsurf, Gemini, Copilot, Qoder, etc.) using both bash and PowerShell script variants. They should be able to trigger the release process that automatically generates 36 template ZIP files from the `.twitterkit/` directory and publishes them to GitHub releases.

**Why this priority**: This is the core capability that enables Twitter-Kit to distribute its campaign-driven Twitter content templates to users through the CLI.

**Independent Test**: Can be fully tested by triggering the release workflow, verifying all 36 ZIP files are generated correctly with `.twitterkit` folder structure, and confirming the GitHub release is published with proper naming and versioning.

**Acceptance Scenarios**:

1. **Given** the maintainer has merged changes to main branch, **When** they create a new version tag (e.g., `v0.1.0`), **Then** the automated workflow triggers and generates all template variants from `.twitterkit/` directory
2. **Given** the workflow is running, **When** it processes each agent/script combination, **Then** it creates correctly structured ZIP files with `.twitterkit/` directory (NOT `.specify/`) and `/twitterkit.*` commands
3. **Given** all templates are generated, **When** the workflow publishes the release, **Then** a GitHub release appears with all 36 ZIP files attached and proper release notes
4. **Given** a release is published, **When** users run `twitter-init init my-project`, **Then** the CLI downloads templates from twitter-init-kit releases with `.twitterkit/` structure

---

### User Story 2 - Developer Tests Template Generation Locally (Priority: P2)

A developer wants to test template generation locally before pushing changes, ensuring their modifications to `.twitterkit/` templates or scripts work correctly across all agent/script combinations.

**Why this priority**: Enables rapid iteration and validation without waiting for CI/CD, reducing the feedback loop for template development.

**Independent Test**: Can be tested by running the local build script and verifying all template ZIPs are created in the dist/ directory with correct `.twitterkit/` structure and content.

**Acceptance Scenarios**:

1. **Given** a developer has modified templates in `.twitterkit/`, **When** they run `./scripts/build-templates.sh`, **Then** all 36 template variants are generated locally in `dist/templates/`
2. **Given** templates are built locally, **When** the developer inspects a ZIP file, **Then** it contains a `.twitterkit/` directory (not `.specify/`) with agent-specific commands and Twitter campaign templates
3. **Given** a build completes, **When** errors occur in any template, **Then** the script reports which template failed and provides actionable error messages
4. **Given** local testing is complete, **When** the developer commits changes, **Then** CI validation runs the same build process to catch issues before release

---

### User Story 3 - CI System Validates Template Integrity (Priority: P2)

The continuous integration system should validate that all templates are correctly formatted, contain required files from `.twitterkit/`, and have proper Twitter-Kit branding before allowing merge to main.

**Why this priority**: Prevents broken or incomplete templates from being released, maintaining quality standards.

**Independent Test**: Can be tested by triggering CI on a pull request and verifying it checks for required files, validates command references, and ensures `.twitterkit/` folder structure is preserved.

**Acceptance Scenarios**:

1. **Given** a pull request modifies templates in `.twitterkit/`, **When** CI runs validation, **Then** it verifies all templates contain required files (commands, scripts, constitution, campaign templates)
2. **Given** CI is validating templates, **When** it finds templates creating `.specify/` instead of `.twitterkit/`, **Then** the build fails with clear error messages
3. **Given** CI validation passes, **When** templates are generated, **Then** automated tests extract and verify the structure of each ZIP file has `.twitterkit/` directory
4. **Given** all validations pass, **When** maintainer merges the PR, **Then** the changes are ready for the next release

---

### Edge Cases

- What happens if a template ZIP fails to generate for one agent but succeeds for others?
- How does the system handle version numbering when multiple releases happen on the same day?
- What if the GitHub API rate limit is exceeded during release publication?
- How are templates validated to ensure `.twitterkit/` folder structure (not `.specify/`) is preserved?
- What happens if the release workflow is triggered but no templates have changed?
- How does the system ensure `.twitterkit/` contents are packaged correctly without conflicting with other kits that use `.specify/`?

## Requirements *(mandatory)*

### Functional Requirements

#### Template Generation

- **FR-001**: System MUST generate template variants for all 18 supported AI agents: claude, cursor-agent, windsurf, gemini, copilot, qoder, qwen, opencode, codex, kilocode, auggie, codebuddy, amp, shai, q (Amazon Q), bob, roo
- **FR-002**: System MUST generate both bash (sh) and PowerShell (ps) script variants for each agent, resulting in 36 total template combinations
- **FR-003**: Each template MUST include agent-specific command directory (e.g., `.claude/commands/`, `.cursor/commands/`, `.windsurf/commands/`)
- **FR-004**: Each template MUST contain Twitter-Kit specific files from `.twitterkit/` directory: constitution.md (Twitter principles), Twitter campaign templates, and twitter-specific command files
- **FR-005**: All agent command files MUST use `/twitterkit.*` command prefix (not `/speckit.*` or `/pmfkit.*`)
- **FR-006**: Template naming MUST follow pattern: `spec-kit-template-{agent}-{script}-v{version}.zip` for CLI compatibility
- **FR-007**: Each template ZIP MUST create `.twitterkit/` directory (NOT `.specify/`) when extracted: `.twitterkit/templates/`, `.twitterkit/scripts/{bash|powershell}/`, `.twitterkit/memory/`, and `.{agent}/commands/`
- **FR-008**: Templates MUST package contents from `.twitterkit/` source directory in repository, preserving folder structure
- **FR-009**: Templates MUST support coexistence with other kits by using `.twitterkit/` namespace instead of `.specify/`

#### Build System

- **FR-010**: System MUST provide local build script (`scripts/build-templates.sh`) that generates all 36 template variants from `.twitterkit/` source
- **FR-011**: Build script MUST be idempotent and support incremental rebuilds
- **FR-012**: Build script MUST validate template structure before creating ZIP files, ensuring `.twitterkit/` folder is created
- **FR-013**: Build script MUST report progress and any errors encountered during generation
- **FR-014**: Build script MUST calculate and verify SHA-256 checksums for each generated ZIP file

#### GitHub Actions Workflow

- **FR-015**: System MUST provide GitHub Actions workflow (`.github/workflows/release.yml`) that triggers on version tag creation (pattern: `v*.*.*`)
- **FR-016**: Workflow MUST execute the build script to generate all template variants from `.twitterkit/` directory
- **FR-017**: Workflow MUST create a GitHub release with generated templates as release assets
- **FR-018**: Workflow MUST generate release notes that include changelog, template list, and SHA-256 checksums
- **FR-019**: Workflow MUST support manual triggering via `workflow_dispatch` for testing

#### Template Validation

- **FR-020**: System MUST provide validation script (`scripts/validate-templates.sh`) that verifies template integrity
- **FR-021**: Validation MUST check for presence of required files in each template: `.twitterkit/` directory with commands, templates, scripts, constitution
- **FR-022**: Validation MUST ensure templates create `.twitterkit/` directory (NOT `.specify/`) when extracted
- **FR-023**: Validation MUST verify agent command frontmatter uses correct `agent: twitterkit.{command}` format
- **FR-024**: Validation MUST confirm all templates reference Twitter-Kit branding and use `.twitterkit/` paths

#### CI Integration

- **FR-025**: System MUST provide CI workflow (`.github/workflows/ci.yml`) that runs on pull requests
- **FR-026**: CI MUST execute template validation before allowing merge
- **FR-027**: CI MUST build all templates to ensure they can be generated successfully from `.twitterkit/`
- **FR-028**: CI MUST fail if any template creates wrong directory structure or missing `.twitterkit/` folder

### Key Entities

- **Template Variant**: A combination of agent type and script type (e.g., claude-sh, cursor-ps), resulting in 36 unique variants, each containing `.twitterkit/` directory
- **Agent Configuration**: Metadata for each supported agent including name, command directory name, and whether it requires CLI tools
- **Template ZIP**: A compressed archive containing `.twitterkit/` directory with all files needed for a specific agent/script combination
- **Release Asset**: A ZIP file attached to a GitHub release with versioned naming and SHA-256 checksum
- **Build Manifest**: JSON file documenting all generated templates with metadata (agent, script, size, checksum, timestamp)
- **TwitterKit Base**: Source directory `.twitterkit/` containing Twitter-Kit specific files before agent/script customization
- **Command File**: Markdown file with YAML frontmatter that defines a `/twitterkit.*` slash command for AI agents

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### Release Automation Success

- **SC-001**: Maintainer can create a new release by creating a version tag, with full automation completing in under 10 minutes
- **SC-002**: Each release generates exactly 36 template ZIP files (18 agents × 2 script types) with correct `.twitterkit/` directory structure
- **SC-003**: GitHub release page displays all templates with proper versioning, release notes, and SHA-256 checksums
- **SC-004**: After release, `twitter-init init` command successfully downloads templates from twitter-init-kit repository with `.twitterkit/` folder structure

#### Template Quality

- **SC-005**: 100% of generated templates pass validation checks: correct `.twitterkit/` directory structure, required files present, no wrong namespace references
- **SC-006**: All templates contain `/twitterkit.*` command references (zero `/speckit.*` or `/pmfkit.*` references remain)
- **SC-007**: Each template creates `.twitterkit/` directory when extracted (NOT `.specify/`), enabling coexistence with other kits
- **SC-008**: Templates extract successfully and create functional Twitter campaign projects when used with `twitter-init init`

#### Developer Experience

- **SC-009**: Developers can build all templates locally in under 5 minutes using `./scripts/build-templates.sh`
- **SC-010**: Local builds produce identical results to CI builds (byte-for-byte reproducible)
- **SC-011**: CI validation catches template issues before merge, with 95% of problems detected before release
- **SC-012**: Build script provides clear progress indicators and actionable error messages when failures occur

#### Maintainability

- **SC-013**: Adding a new AI agent requires modifying only the AGENTS array in build script (under 5 lines of code)
- **SC-014**: Template structure changes to `.twitterkit/` automatically propagate to all 36 variants without manual editing
- **SC-015**: Release process is fully automated with zero manual steps required after tag creation
- **SC-016**: All workflows and scripts are documented with inline comments explaining each step

## Out of Scope *(optional)*

- Automated testing of templates with actual AI agents (manual testing required)
- Generating templates for agents not listed in the 18 supported agents
- Creating separate twitter-kit-template naming convention (keeping spec-kit naming for CLI compatibility)
- Hosting templates outside GitHub releases (S3, CDN, etc.)
- Automatic version bumping in pyproject.toml (manual version management)
- Rollback mechanism for failed releases (manual deletion/recreation required)
- Template customization per agent beyond command directory names (all agents use same Twitter templates from `.twitterkit/`)
- Docker-based build environment (assumes standard Unix/Windows environments)
- Conversion of existing `.specify/`-based kits to `.twitterkit/` structure

## Assumptions *(optional)*

- GitHub Actions is available and workflows can be enabled in the repository
- Repository has proper permissions to create releases and upload assets
- Build environment has bash, zip, and standard Unix utilities available
- PowerShell templates can be generated on Unix systems (script copying only, no execution needed)
- Maximum template ZIP size will not exceed GitHub's 2GB release asset limit
- Template generation completes within GitHub Actions timeout (6 hours max)
- Version tags follow semantic versioning (v{major}.{minor}.{patch})
- All AI agents use similar directory structures (`.{agent}/commands/` pattern)
- Templates will be used with uv package manager or direct extraction for installation
- Local builds run on macOS or Linux (Windows support via Git Bash or WSL)
- Source templates in `.twitterkit/` directory are already correctly structured
- Twitter-init-kit CLI is configured to create `.twitterkit/` directory when extracting templates

## Dependencies *(optional)*

- **GitHub Actions**: Required for automated releases and CI validation
- **GitHub Releases API**: For publishing releases and uploading assets
- **Bash**: Required for build and validation scripts
- **zip utility**: Required for creating template archives
- **Git**: Required for versioning and tag-based triggering
- **sed/awk/grep**: Required for text processing during template generation
- **Existing .twitterkit/ directory**: Source templates must exist and be properly structured

## Constraints *(optional)*

- Must maintain CLI compatibility by using `spec-kit-template-` naming convention
- Must support all 18 agents that Spec-Kit supports
- Must generate both bash and PowerShell variants for each agent
- Build scripts must work on Unix-like systems (macOS, Linux)
- GitHub Actions free tier limits: 2000 minutes/month for private repos
- Template ZIPs must be under 2GB each (GitHub release asset limit)
- Must not require Docker or containerization for local builds
- Must create `.twitterkit/` directory (NOT `.specify/`) to avoid conflicts with other kits
- Must preserve folder name isolation from spec-kit and other kit variants

## Related Features or Documentation *(optional)*

- **Spec-Kit Release Process**: https://github.com/github/spec-kit/blob/main/.github/workflows/release.yml - Reference implementation for template generation workflow
- **PMF-Kit Release Process** (spec 002): specs/002-automated-template-releases/ - Successful example of kit-specific automated releases
- **Twitter-Kit Templates**: `.twitterkit/templates/` directory - Source templates for campaigns that need to be included in each variant
- **Twitter-Kit Commands**: `.twitterkit/templates/commands/` - Command templates that define `/twitterkit.*` slash commands
- **Twitter-Kit Constitution**: `.twitterkit/memory/constitution.md` - Twitter-specific principles to include in all templates
- **Twitter-Kit Scripts**: `.twitterkit/scripts/bash/` and `.twitterkit/scripts/powershell/` - Automation scripts for campaigns
- **CLI Template Downloader**: CLI code expects `spec-kit-template-{agent}-{script}.zip` naming and must extract to `.twitterkit/` directory
