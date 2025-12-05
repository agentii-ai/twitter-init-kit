#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Generates release notes for Twitter-Kit templates with changelog and checksums
# Usage: generate-release-notes.sh <new_version> <previous_version>
# Output: release_notes.md

NEW_VERSION="${1:-}"
PREV_VERSION="${2:-}"

if [[ -z "$NEW_VERSION" ]]; then
  echo "Error: New version argument required" >&2
  exit 1
fi

GENRELEASES_DIR="${GENRELEASES_DIR:-.genreleases}"

# Get commits since previous version
if [[ -n "$PREV_VERSION" ]] && git rev-parse "$PREV_VERSION" >/dev/null 2>&1; then
  COMMITS=$(git log --pretty=format:"- %s" "$PREV_VERSION".."$NEW_VERSION" 2>/dev/null || echo "- Initial release")
else
  COMMITS="- Initial release"
fi

# Generate release notes
cat > release_notes.md << 'EOF'
# Twitter-Kit Templates Release

This release contains 36 template variants for Twitter-Kit, supporting 18 AI coding agents with both bash and PowerShell script options.

## What's Included

Each template includes:
- **Twitter-Kit Constitution**: Campaign-focused principles for Twitter content creation
- **Workflow Templates**: spec.md, plan.md, tasks.md for campaign planning
- **Slash Commands**: `/twitterkit.*` commands for campaign management
- **Scripts**: Automation scripts for Twitter campaign execution
- **Directory Structure**: Templates extract to `.twitterkit/` folder (enables coexistence with other kits)

## Installation

```bash
# Install Twitter-Kit CLI
pip install twitter-init-kit

# Initialize new campaign project
twitter-init init my-campaign --agent claude --script sh
```

Or download templates manually from the Assets section below.

## Changelog

EOF

echo "$COMMITS" >> release_notes.md

cat >> release_notes.md << 'EOF'

## Supported AI Agents

- Claude Code (.claude/commands/)
- Cursor Agent (.cursor/commands/)
- Windsurf (.windsurf/workflows/)
- Google Gemini (.gemini/commands/)
- GitHub Copilot (.github/agents/)
- Qoder (.qoder/commands/)
- Qwen (.qwen/commands/)
- OpenCode (.opencode/command/)
- Codex (.codex/prompts/)
- KiloCode (.kilocode/workflows/)
- Auggie (.augment/commands/)
- CodeBuddy (.codebuddy/commands/)
- AMP (.agents/commands/)
- Shai (.shai/commands/)
- Amazon Q (.amazonq/prompts/)
- Bob (.bob/commands/)
- Roo (.roo/commands/)

## Template Assets

36 template variants with SHA-256 checksums:

EOF

# Add checksums for all ZIPs
for zip in "$GENRELEASES_DIR"/*.zip; do
  [[ -f "$zip" ]] || continue
  filename=$(basename "$zip")
  size=$(ls -lh "$zip" | awk '{print $5}')
  sha256=$(shasum -a 256 "$zip" | cut -d' ' -f1)

  echo "### $filename" >> release_notes.md
  echo "- **Size**: $size" >> release_notes.md
  echo "- **SHA-256**: \`$sha256\`" >> release_notes.md
  echo "" >> release_notes.md
done

cat >> release_notes.md << 'EOF'

## Verification

Verify download integrity using SHA-256 checksums:

```bash
shasum -a 256 -c checksums.txt
```

## Documentation

- [Quick Start Guide](https://github.com/YOUR_ORG/twitter-init-kit#quick-start)
- [Template Structure](https://github.com/YOUR_ORG/twitter-init-kit/blob/main/docs/templates.md)
- [Contributing](https://github.com/YOUR_ORG/twitter-init-kit/blob/main/CONTRIBUTING.md)

---

**Note**: Templates create `.twitterkit/` directory structure to enable coexistence with other kit variants (spec-kit, pmf-kit, etc.).
EOF

echo "Release notes generated: release_notes.md"
