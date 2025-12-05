<div align="center">
    <h1>🐦 Twitter-Init-Kit</h1>
    <h3><em>Systematic Twitter marketing for AI/LLM SaaS products.</em></h3>
</div>

<p align="center">
    <strong>A domain-specific toolkit that adapts the spec-kit methodology for Twitter marketing and growth operations.</strong>
</p>

<p align="center">
    <a href="https://github.com/agentii-ai/twitter-init-kit/actions/workflows/release.yml"><img src="https://github.com/agentii-ai/twitter-init-kit/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/agentii-ai/twitter-init-kit/stargazers"><img src="https://img.shields.io/github/stars/agentii-ai/twitter-init-kit?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/agentii-ai/twitter-init-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/agentii-ai/twitter-init-kit" alt="License"/></a>
</p>

---

## Table of Contents

- [⚡ Get Started](#-get-started)
- [🤔 What is Twitter-Init-Kit?](#-what-is-twitter-init-kit)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 CLI Reference](#-cli-reference)
- [📚 Use Cases](#-use-cases)
- [🏗️ Multi-Kit Architecture](#️-multi-kit-architecture)
- [📖 Case Studies](#-case-studies)
- [🔧 Prerequisites](#-prerequisites)
- [💬 Support](#-support)
- [📄 License](#-license)

## ⚡ Get Started

### 1. Install Twitterify CLI

Choose your preferred installation method:

#### Option 1: One-Time Usage (Recommended)

Run directly without installing - **always uses the latest version**:

```bash
uvx --from git+https://github.com/agentii-ai/twitter-init-kit.git twitterify init <PROJECT_NAME>
```

This is ideal because:
- **Always up-to-date**: Each run fetches the latest templates and features
- **No upgrade hassle**: No need to manually update when the repo changes
- **Zero maintenance**: No persistent installation to manage

#### Option 2: Persistent Installation

Install once and use everywhere (requires manual upgrades):

```bash
uv tool install twitterify-cli --from git+https://github.com/agentii-ai/twitter-init-kit.git
```

Then use the tool directly:

```bash
twitterify init <PROJECT_NAME>
twitterify check
```

To upgrade after repo updates:

```bash
uv tool install twitterify-cli --force --from git+https://github.com/agentii-ai/twitter-init-kit.git
```

### 2. Define Your Twitter Marketing Principles

Launch your AI assistant in the project directory. The `/twitterkit.*` commands are available.

Use **`/twitterkit.constitution`** to create your project's Twitter marketing principles:

```bash
/twitterkit.constitution Create principles for founder-led, demo-driven Twitter marketing targeting AI/LLM developers
```

### 3. Create Campaign Specification

Use **`/twitterkit.specify`** to describe your campaign. Focus on **objectives and audience**, not tactics:

```bash
/twitterkit.specify Launch campaign for our AI coding assistant targeting technical founders. Goal: 100 engaged users in 4 weeks via demo-driven content and community engagement.
```

### 4. Generate Growth Plan

Use **`/twitterkit.plan`** to create a phased growth plan:

```bash
/twitterkit.plan 4-week campaign with phases: Stealth Alpha (week 1-2), Public Launch (week 3), Scale (week 4). Focus on founder demos and power user advocacy.
```

### 5. Break Down into Tasks

Use **`/twitterkit.tasks`** to create actionable task lists:

```bash
/twitterkit.tasks
```

### 6. Execute Implementation

Use **`/twitterkit.implement`** to execute tasks systematically:

```bash
/twitterkit.implement
```

---

## 🤔 What is Twitter-Init-Kit?

Twitter-init-kit helps technical founders plan and execute systematic Twitter campaigns:

- **Structured workflow**: Constitution → Specify → Plan → Tasks → Implement
- **AI agent integration**: Works with Claude Code, Cursor, Windsurf, Gemini CLI, and 17 other agents
- **Template system**: Pre-built templates for campaign specs, growth plans, and execution tasks
- **Evidence-based**: Grounded in 2023-2025 AI SaaS success stories (Cursor, Runway, HeyGen)
- **Multi-kit architecture**: Coexists with spec-kit, pm-kit, pd-kit on the same machine

---

## 🤖 Supported AI Agents

| Agent | Support | Notes |
|-------|---------|-------|
| [Claude Code](https://www.anthropic.com/claude-code) | ✅ | Full slash command support |
| [Cursor](https://cursor.sh/) | ✅ | Via Composer |
| [Windsurf](https://windsurf.com/) | ✅ | Via Cascade workflows |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ | TOML format |
| [GitHub Copilot](https://code.visualstudio.com/) | ✅ | Agent mode |
| [Qoder CLI](https://qoder.com/cli) | ✅ | |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Limited argument support |
| [Amp](https://ampcode.com/) | ✅ | |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview) | ✅ | |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli) | ✅ | |
| [Codex CLI](https://github.com/openai/codex) | ✅ | |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | ✅ | |
| [opencode](https://opencode.ai/) | ✅ | |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | ✅ | TOML format |
| [Roo Code](https://roocode.com/) | ✅ | |
| [SHAI (OVHcloud)](https://github.com/ovh/shai) | ✅ | |
| [IBM Bob](https://www.ibm.com/products/bob) | ✅ | IDE-based |

---

## 🔧 CLI Reference

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new Twitter marketing project |
| `check` | Check for installed tools |

### `twitterify init` Options

| Option | Description |
|--------|-------------|
| `<project-name>` | Name for your project directory (use `.` for current) |
| `--ai` | AI assistant: `claude`, `gemini`, `copilot`, `cursor-agent`, `windsurf`, etc. |
| `--script` | Script variant: `sh` (bash) or `ps` (PowerShell) |
| `--here` | Initialize in current directory |
| `--force` | Force merge in non-empty directory |
| `--no-git` | Skip git initialization |
| `--debug` | Enable debug output |

### Examples

```bash
# One-time usage (recommended - always latest)
uvx --from git+https://github.com/agentii-ai/twitter-init-kit.git twitterify init my-campaign --ai claude

# Initialize with specific agent
twitterify init my-campaign --ai cursor-agent

# Initialize in current directory
twitterify init . --ai windsurf
# or
twitterify init --here --ai windsurf

# Force merge into existing directory
twitterify init . --force --ai claude
```

### Available Slash Commands

After initialization, your AI agent has access to:

#### Core Commands

| Command | Description |
|---------|-------------|
| `/twitterkit.constitution` | Define Twitter marketing principles and guardrails |
| `/twitterkit.specify` | Create campaign specification (personas, objectives, metrics) |
| `/twitterkit.plan` | Generate growth plan (phases, sprints, experiments) |
| `/twitterkit.tasks` | Break plan into actionable tasks |
| `/twitterkit.implement` | Execute tasks systematically |

#### Optional Commands

| Command | Description |
|---------|-------------|
| `/twitterkit.clarify` | Clarify underspecified areas before planning |
| `/twitterkit.analyze` | Cross-artifact consistency check |
| `/twitterkit.checklist` | Generate quality checklists |

---

## 📚 Use Cases

### Launch a New AI Product on Twitter

1. Define constitution with founder-led, demo-driven, PLG principles
2. Create campaign spec targeting technical founders
3. Generate 4-week growth plan
4. Break down into tasks
5. Execute with PDCA cycles

### Build Founder-Led Twitter Presence

1. Define Twitter persona and content pillars
2. Plan 12-week content sprint
3. Create content bank
4. Execute weekly rhythm

### Optimize Existing Twitter Strategy

1. Use `/twitterkit.clarify` to identify gaps
2. Create optimization spec
3. Generate experiment log
4. Measure and iterate

---

## 🏗️ Multi-Kit Architecture

Twitter-init-kit coexists with other kit variants without conflicts:

| Kit | Folder | CLI | Slash Commands | Use For |
|-----|--------|-----|----------------|---------|
| **spec-kit** | `.specify/` | `specify` | `/speckit.*` | Software engineering |
| **twitter-kit** | `.twitterkit/` | `twitterify` | `/twitterkit.*` | Twitter marketing |
| **pm-kit** | `.pmkit/` | `pmify` | `/pmkit.*` | Product management |
| **pd-kit** | `.pdkit/` | `pdify` | `/pdkit.*` | Product design |

### Multi-Kit Workflow

```bash
# Build product feature with spec-kit
specify init my-product
/speckit.implement

# Launch on Twitter with twitter-kit
twitterify init . --here
/twitterkit.implement
```

---

## 📖 Case Studies

Templates are grounded in 2023-2025 AI SaaS success stories:

### Cursor - Founder-Led Strategy
- CEO tweets daily demo clips
- 100K+ followers, 10-50K views per demo
- **Principle**: Founder authenticity > brand marketing

### Runway - Demo-Driven Content
- Every tweet showcases AI-generated video
- 500K+ followers, viral demos (5M+ views)
- **Principle**: Demos create wow moments

### HeyGen - PLG Activation Loop
- Low-friction signup from Twitter
- 20% activation rate, 5% advocacy rate
- **Principle**: Product is the hero

See [refs/0_overview.md](./refs/0_overview.md) for detailed analysis.

---

## 🔧 Prerequisites

- **Linux/macOS/Windows**
- [Supported AI agent](#-supported-ai-agents)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

---

## 💬 Support

For support, please open a [GitHub issue](https://github.com/agentii-ai/twitter-init-kit/issues).

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## Acknowledgments

- **Spec-Kit**: Based on [spec-kit](https://github.com/github/spec-kit) by GitHub
- **Case Studies**: Inspired by Cursor, Runway, HeyGen, and other AI SaaS companies

---

**Ready to launch your systematic Twitter growth campaign?**

```bash
uvx --from git+https://github.com/agentii-ai/twitter-init-kit.git twitterify init my-campaign --ai claude
```

🚀
