#!/usr/bin/env bash
set -euo pipefail

# check-release-exists.sh
# Checks if a GitHub release already exists for the given version
# Usage: check-release-exists.sh <version>
# Exit code: 0 if exists, 1 if not exists

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Error: Version argument required" >&2
  exit 1
fi

# Check if release exists using gh CLI
if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "Release $VERSION already exists"
  exit 0
else
  echo "Release $VERSION does not exist"
  exit 1
fi
