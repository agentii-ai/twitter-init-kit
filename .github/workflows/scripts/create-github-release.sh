#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Creates a GitHub release and uploads template assets
# Usage: create-github-release.sh <version>

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Error: Version argument required" >&2
  exit 1
fi

GENRELEASES_DIR="${GENRELEASES_DIR:-.genreleases}"

if [[ ! -f "release_notes.md" ]]; then
  echo "Error: release_notes.md not found" >&2
  exit 1
fi

echo "Creating GitHub release $VERSION..."

# Create release with all template ZIPs
gh release create "$VERSION" \
  "$GENRELEASES_DIR"/*.zip \
  --title "Twitter-Kit Templates $VERSION" \
  --notes-file release_notes.md

echo "✓ Release $VERSION created successfully"
echo "  URL: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/releases/tag/$VERSION"
