#!/bin/bash

# Increment version code and version name
# Usage: ./scripts/increment-version.sh [major|minor|patch]

GRADLE_FILE="app/build.gradle.kts"
INCREMENT_TYPE=${1:-patch}

# Get current version
CURRENT_VERSION_CODE=$(grep "versionCode =" $GRADLE_FILE | sed 's/[^0-9]*//g')
CURRENT_VERSION_NAME=$(grep "versionName =" $GRADLE_FILE | sed 's/.*"\(.*\)".*/\1/')

# Increment version code
NEW_VERSION_CODE=$((CURRENT_VERSION_CODE + 1))

# Parse current version name
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION_NAME"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Increment based on type
case $INCREMENT_TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Unknown increment type: $INCREMENT_TYPE"
    echo "Usage: $0 [major|minor|patch]"
    exit 1
    ;;
esac

NEW_VERSION_NAME="$MAJOR.$MINOR.$PATCH"

echo "Current Version: $CURRENT_VERSION_NAME (Code: $CURRENT_VERSION_CODE)"
echo "New Version: $NEW_VERSION_NAME (Code: $NEW_VERSION_CODE)"

# Update gradle file
sed -i "s/versionCode = $CURRENT_VERSION_CODE/versionCode = $NEW_VERSION_CODE/" $GRADLE_FILE
sed -i "s/versionName = \"$CURRENT_VERSION_NAME\"/versionName = \"$NEW_VERSION_NAME\"/" $GRADLE_FILE

echo "✅ Version updated successfully!"
echo "Don't forget to commit these changes:"
echo "git add $GRADLE_FILE"
echo "git commit -m \"Bump version to $NEW_VERSION_NAME\""
echo "git tag -a android-v$NEW_VERSION_NAME -m \"Release version $NEW_VERSION_NAME\""
