#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Auto-increments patch version for Twitter-Kit template releases
# Usage: get-next-version.sh
# Output: Next semantic version (e.g., v0.1.1)

# Get latest tag, default to v0.0.0 if none exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Parse semantic version components
if [[ $LATEST_TAG =~ ^v([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
  MAJOR="${BASH_REMATCH[1]}"
  MINOR="${BASH_REMATCH[2]}"
  PATCH="${BASH_REMATCH[3]}"
else
  echo "Error: Invalid version format: $LATEST_TAG" >&2
  exit 1
fi

# Increment patch version
NEXT_PATCH=$((PATCH + 1))
NEXT_VERSION="v${MAJOR}.${MINOR}.${NEXT_PATCH}"

echo "$NEXT_VERSION"
