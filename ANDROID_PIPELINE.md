# Android CI/CD Pipeline Documentation

Complete guide for the Android application CI/CD pipeline using GitHub Actions.

## Overview

The Notulen Android app uses GitHub Actions for automated building, testing, and deployment. The pipeline ensures code quality, runs tests, and generates release artifacts.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Android    │  │   Android    │  │   Android    │      │
│  │      CI      │  │   Release    │  │  PR Checks   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Build & Test Jobs                    │      │
│  │  • Compile code                                   │      │
│  │  • Run lint checks                                │      │
│  │  • Execute unit tests                             │      │
│  │  • Generate APK/AAB                               │      │
│  │  • Code coverage                                  │      │
│  │  • Security scanning                              │      │
│  └──────────────────────────────────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Workflows

### 1. Android CI (Continuous Integration)

**File:** `.github/workflows/android-ci.yml`

**Triggers:**
- Push to `main`, `develop`, or `claude/**` branches
- Changes in `android/` directory
- Changes in the workflow file itself

**Jobs:**

#### Build and Test
- Compiles the Android app
- Runs lint checks
- Executes unit tests
- Generates debug APK and AAB
- Uploads artifacts (7-day retention)

#### Code Quality Check
- Runs Detekt for code analysis
- Checks for dependency updates
- Generates quality reports

#### Build Matrix
- Tests on multiple Android API levels (26, 29, 33, 34)
- Ensures compatibility across versions
- Parallel execution for faster feedback

#### Security Scan
- Dependency vulnerability scanning
- OWASP dependency check
- Security report generation

**Artifacts:**
- Debug APK
- Debug AAB
- Lint results
- Test reports
- Security reports

### 2. Android Release

**File:** `.github/workflows/android-release.yml`

**Triggers:**
- Git tags matching `v*.*.*` or `android-v*.*.*`
- Manual workflow dispatch

**Jobs:**

#### Release Build
1. Checks out code
2. Sets up JDK 17
3. Decodes keystore from GitHub Secrets
4. Builds signed release APK
5. Builds signed release AAB
6. Renames artifacts with version
7. Generates release notes
8. Creates GitHub release
9. Uploads to Play Store (optional)

**Required Secrets:**
- `KEYSTORE_BASE64`: Base64-encoded keystore file
- `SIGNING_STORE_PASSWORD`: Keystore password
- `SIGNING_KEY_ALIAS`: Key alias
- `SIGNING_KEY_PASSWORD`: Key password

**Optional Secrets:**
- `PLAY_STORE_JSON_KEY`: For automatic Play Store publishing

**Artifacts:**
- Release APK (90-day retention)
- Release AAB (90-day retention)
- Release notes

### 3. Android PR Checks

**File:** `.github/workflows/android-pr-checks.yml`

**Triggers:**
- Pull requests to `main` or `develop`
- Changes in `android/` directory

**Jobs:**

#### Validation
- Validates Gradle wrapper
- Checks code formatting (Spotless)
- Runs lint with detailed reporting
- Executes tests with coverage
- Uploads coverage to Codecov
- Posts results as PR comments

#### Size Analysis
- Builds release APK
- Analyzes APK size
- Comments size on PR
- Tracks size changes over time

## Setup Instructions

### Initial Setup

1. **Fork or Clone Repository**
   ```bash
   git clone https://github.com/taufiksoleh/notulen.git
   cd notulen
   ```

2. **Generate Keystore** (for releases)
   ```bash
   cd android/app
   keytool -genkey -v -keystore release-keystore.jks \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias release
   ```

3. **Encode Keystore for GitHub**
   ```bash
   base64 -i release-keystore.jks -o keystore-base64.txt
   ```

4. **Add GitHub Secrets**
   - Go to repository **Settings → Secrets and variables → Actions**
   - Add the following secrets:
     - `KEYSTORE_BASE64`: Contents of `keystore-base64.txt`
     - `SIGNING_STORE_PASSWORD`: Your keystore password
     - `SIGNING_KEY_ALIAS`: `release`
     - `SIGNING_KEY_PASSWORD`: Your key password

### Local Testing

Before pushing, test the build locally:

```bash
cd android

# Run all checks
./gradlew check

# Run lint
./gradlew lintDebug

# Run tests
./gradlew testDebugUnitTest

# Build debug APK
./gradlew assembleDebug

# Build release APK (requires keystore)
./gradlew assembleRelease
```

## Creating a Release

### Automated Release Process

1. **Update Version**
   ```bash
   cd android
   ./scripts/increment-version.sh [major|minor|patch]
   ```

2. **Commit Changes**
   ```bash
   git add app/build.gradle.kts
   git commit -m "Bump version to X.Y.Z"
   ```

3. **Create Tag**
   ```bash
   git tag -a android-vX.Y.Z -m "Release version X.Y.Z"
   ```

4. **Push**
   ```bash
   git push origin main --tags
   ```

5. **Wait for Pipeline**
   - GitHub Actions will automatically:
     - Build signed APK and AAB
     - Run all tests
     - Create GitHub release
     - Upload artifacts

### Manual Release (Workflow Dispatch)

1. Go to **Actions** tab
2. Select **Android Release** workflow
3. Click **Run workflow**
4. Enter version (e.g., `1.0.0`)
5. Click **Run workflow** button

## Monitoring Builds

### View Build Status

1. Go to **Actions** tab in GitHub
2. Select the workflow run
3. View job logs and artifacts

### Build Status Badges

Add to README:
```markdown
![Android CI](https://github.com/taufiksoleh/notulen/workflows/Android%20CI/badge.svg)
```

### Download Artifacts

1. Go to completed workflow run
2. Scroll to **Artifacts** section
3. Download desired artifact (APK, AAB, reports)

## Troubleshooting

### Build Fails on CI but Works Locally

**Possible causes:**
- Gradle wrapper version mismatch
- Missing dependencies
- Environment-specific configurations

**Solution:**
```bash
# Clean and rebuild
./gradlew clean
./gradlew assembleDebug --stacktrace
```

### Signing Error in Release Build

**Error:** "Keystore was tampered with, or password was incorrect"

**Solution:**
1. Verify GitHub Secrets are correct
2. Re-encode keystore: `base64 -i release-keystore.jks`
3. Update `KEYSTORE_BASE64` secret
4. Ensure no extra whitespace in secrets

### Tests Pass Locally but Fail on CI

**Possible causes:**
- Timezone differences
- File system case sensitivity
- Missing test resources

**Solution:**
- Run tests in CI mode locally: `./gradlew testDebugUnitTest --info`
- Check test logs in GitHub Actions

### APK Size Too Large

**Solution:**
1. Enable R8 shrinking (already enabled)
2. Remove unused resources
3. Use ProGuard rules
4. Optimize images
5. Check dependency sizes: `./gradlew app:dependencies`

## Advanced Configuration

### Customizing Build Variants

Edit `app/build.gradle.kts`:

```kotlin
android {
    flavorDimensions += "version"
    productFlavors {
        create("free") {
            dimension = "version"
            applicationIdSuffix = ".free"
        }
        create("pro") {
            dimension = "version"
            applicationIdSuffix = ".pro"
        }
    }
}
```

### Adding Code Coverage

Coverage is already configured with JaCoCo. View reports:

```bash
./gradlew testDebugUnitTest jacocoTestReport
open app/build/reports/jacoco/jacocoTestReport/html/index.html
```

### Play Store Publishing

To enable automatic Play Store publishing:

1. **Create Service Account**
   - Go to [Google Play Console](https://play.google.com/console)
   - Setup → API access
   - Create service account

2. **Download JSON Key**
   - Grant "Release manager" permissions
   - Create and download JSON key

3. **Add Secret**
   - Add `PLAY_STORE_JSON_KEY` secret with JSON content

4. **Configure Track**
   - Edit `android-release.yml`
   - Change `track: production` to `track: internal|beta|production`

## Performance Optimization

### Caching

The pipeline uses caching for:
- Gradle dependencies
- Build outputs
- Test results

### Parallel Execution

Build matrix runs on multiple API levels in parallel:
- API 26 (Android 8.0)
- API 29 (Android 10)
- API 33 (Android 13)
- API 34 (Android 14)

### Artifact Management

- Debug builds: 7-day retention
- Release builds: 90-day retention
- Automatic cleanup of old artifacts

## Best Practices

1. **Always run tests before pushing**
   ```bash
   ./gradlew check
   ```

2. **Use feature branches**
   - Create branch: `git checkout -b feature/my-feature`
   - Push and create PR
   - Wait for CI checks
   - Merge when green

3. **Keep dependencies updated**
   ```bash
   ./gradlew dependencyUpdates
   ```

4. **Monitor build times**
   - Check Actions tab for slow jobs
   - Optimize if builds take > 10 minutes

5. **Review security reports**
   - Check for dependency vulnerabilities
   - Update vulnerable dependencies promptly

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [Gradle Best Practices](https://docs.gradle.org/current/userguide/performance.html)
- [Keystore Setup Guide](android/keystore-setup.md)

## Support

For issues related to:
- **CI/CD Pipeline**: Check workflow logs in Actions tab
- **Build Issues**: See [Android README](android/README.md)
- **App Issues**: Open issue on GitHub

---

Last updated: 2025-01-XX
Version: 1.0.0
