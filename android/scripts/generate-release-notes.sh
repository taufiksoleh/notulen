#!/bin/bash

# Generate release notes from git commits
# Usage: ./scripts/generate-release-notes.sh [previous-tag] [current-tag]

PREVIOUS_TAG=${1:-$(git describe --tags --abbrev=0 HEAD^)}
CURRENT_TAG=${2:-HEAD}

echo "# Release Notes"
echo ""
echo "## Version: $CURRENT_TAG"
echo ""
echo "### Changes since $PREVIOUS_TAG"
echo ""

# Get commits between tags
git log $PREVIOUS_TAG..$CURRENT_TAG --pretty=format:"- %s" --no-merges | grep -v "^$"

echo ""
echo ""
echo "### Contributors"
git log $PREVIOUS_TAG..$CURRENT_TAG --format='%aN' | sort -u | sed 's/^/- /'

echo ""
echo ""
echo "### Files Changed"
git diff --stat $PREVIOUS_TAG..$CURRENT_TAG | tail -1
