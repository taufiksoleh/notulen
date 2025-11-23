# Notulen Android App

Android application for Notulen - AI-powered meeting notes with speech-to-text and automatic summarization.

## Architecture

This app follows **Clean Architecture** principles with three distinct layers:

```
┌─────────────────────────────────────┐
│   Presentation Layer                │
│   - Jetpack Compose UI              │
│   - ViewModels (MVVM)               │
│   - Navigation                      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Domain Layer                      │
│   - Use Cases                       │
│   - Repository Interfaces           │
│   - Domain Models                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Data Layer                        │
│   - Repository Implementations      │
│   - API Service (Retrofit)          │
│   - Local Database (Room)           │
│   - Audio Recorder                  │
└─────────────────────────────────────┘
```

## Tech Stack

- **UI**: Jetpack Compose with Material 3
- **Architecture**: Clean Architecture + MVVM
- **Dependency Injection**: Hilt
- **Networking**: Retrofit + OkHttp
- **Database**: Room
- **Async**: Kotlin Coroutines + Flow
- **Navigation**: Jetpack Navigation Compose
- **Permissions**: Accompanist Permissions
- **Logging**: Timber

## Features

- 🎙️ **Audio Recording**: Record meetings with high-quality audio
- 📝 **Transcription**: Automatic speech-to-text conversion
- 🤖 **AI Summaries**: Generate meeting summaries with action items
- 💾 **Offline Support**: Local database for offline access
- 🔄 **Sync**: Sync with backend API
- 🎨 **Modern UI**: Material 3 design with Jetpack Compose

## Project Structure

```
android/
├── app/
│   ├── src/main/java/com/notulen/
│   │   ├── data/
│   │   │   ├── local/
│   │   │   │   ├── dao/              # Room DAOs
│   │   │   │   ├── database/         # Room Database
│   │   │   │   └── entity/           # Room Entities
│   │   │   ├── remote/
│   │   │   │   ├── api/              # Retrofit API Service
│   │   │   │   └── dto/              # Data Transfer Objects
│   │   │   └── repository/           # Repository Implementations
│   │   ├── domain/
│   │   │   ├── model/                # Domain Models
│   │   │   ├── repository/           # Repository Interfaces
│   │   │   └── usecase/              # Use Cases
│   │   ├── presentation/
│   │   │   ├── components/           # Reusable UI Components
│   │   │   ├── navigation/           # Navigation Graph
│   │   │   ├── theme/                # Material 3 Theme
│   │   │   ├── ui/                   # Screens
│   │   │   └── viewmodel/            # ViewModels
│   │   ├── di/                       # Dependency Injection Modules
│   │   ├── MainActivity.kt
│   │   └── NotulenApplication.kt
│   └── build.gradle.kts
├── build.gradle.kts
└── settings.gradle.kts
```

## Prerequisites

- Android Studio Hedgehog | 2023.1.1 or later
- JDK 17
- Android SDK 34
- Gradle 8.2

## Setup

1. **Clone the repository**
   ```bash
   cd android
   ```

2. **Configure API URL**

   Edit `app/build.gradle.kts` and update the API base URL:
   ```kotlin
   buildConfigField("String", "API_BASE_URL", "\"http://your-backend-url:8000\"")
   ```

   For local development (emulator):
   - Use `http://10.0.2.2:8000` for Android Emulator
   - Use your computer's IP address for physical devices

3. **Sync Gradle**
   ```bash
   ./gradlew build
   ```

4. **Run the app**
   - Open the project in Android Studio
   - Click Run or press Shift+F10

## Building

### Debug Build
```bash
./gradlew assembleDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`

### Release Build
```bash
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

### Build AAB (for Play Store)
```bash
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

## CI/CD Pipeline

The project includes comprehensive CI/CD pipelines using GitHub Actions:

### Workflows

#### 1. Android CI (`android-ci.yml`)
**Triggers:** Push to main/develop/claude branches, PRs

**Jobs:**
- **Build and Test**: Compiles code, runs lint, unit tests, generates debug APK/AAB
- **Code Quality Check**: Runs Detekt and dependency checks
- **Build Matrix**: Tests on multiple API levels (26, 29, 33, 34)
- **Security Scan**: Dependency vulnerability scanning

#### 2. Android Release (`android-release.yml`)
**Triggers:** Git tags (`v*.*.*`, `android-v*.*.*`), manual dispatch

**Features:**
- Builds signed release APK and AAB
- Creates GitHub release with artifacts
- Generates release notes
- Optional: Uploads to Google Play Store

#### 3. Android PR Checks (`android-pr-checks.yml`)
**Triggers:** Pull requests

**Features:**
- Gradle wrapper validation
- Code formatting checks
- Lint analysis with comments
- Test coverage with Codecov
- APK size analysis
- Automated PR comments with build results

### Setting Up CI/CD

#### Required GitHub Secrets

For release builds, add these secrets to your repository:

- `KEYSTORE_BASE64`: Base64-encoded release keystore
- `SIGNING_STORE_PASSWORD`: Keystore password
- `SIGNING_KEY_ALIAS`: Key alias (usually "release")
- `SIGNING_KEY_PASSWORD`: Key password

#### Optional Secrets

- `PLAY_STORE_JSON_KEY`: For Play Store publishing
- `CODECOV_TOKEN`: For code coverage reporting

See [keystore-setup.md](keystore-setup.md) for detailed instructions.

### Creating a Release

#### Method 1: Git Tag
```bash
# Increment version first
./scripts/increment-version.sh [major|minor|patch]

# Commit and tag
git add app/build.gradle.kts
git commit -m "Bump version to X.Y.Z"
git tag -a android-vX.Y.Z -m "Release version X.Y.Z"
git push origin main --tags
```

#### Method 2: Manual Workflow Dispatch
1. Go to **Actions** tab in GitHub
2. Select **Android Release** workflow
3. Click **Run workflow**
4. Enter version number
5. Click **Run workflow** button

### Artifacts

All builds generate artifacts available in the Actions tab:

- **Debug builds**: 7-day retention
- **Release builds**: 90-day retention
- **Test results**: Available for all builds
- **Lint reports**: Available for all builds

## Running Tests

### Unit Tests
```bash
./gradlew test
```

### Instrumentation Tests
```bash
./gradlew connectedAndroidTest
```

## Clean Architecture Layers

### 1. Presentation Layer
- **UI**: Jetpack Compose screens and components
- **ViewModels**: Handle UI state and business logic
- **Navigation**: Screen navigation using Navigation Compose

### 2. Domain Layer
- **Models**: Core business entities (Meeting, TranscriptionResult)
- **Repository Interfaces**: Define data operations
- **Use Cases**: Encapsulate business logic
  - `GetMeetingsUseCase`
  - `CreateMeetingUseCase`
  - `RecordAudioUseCase`
  - `RequestSummaryUseCase`
  - etc.

### 3. Data Layer
- **Repository Implementations**: Implement domain interfaces
- **API Service**: Retrofit for network calls
- **Local Database**: Room for offline storage
- **Audio Recorder**: MediaRecorder for audio capture

## Key Components

### API Integration

The app connects to the Notulen backend API:

- `GET /api/meetings` - List all meetings
- `GET /api/meetings/{id}` - Get meeting details
- `POST /api/transcribe` - Upload audio for transcription
- `POST /api/summarize` - Request AI summary
- `DELETE /api/meetings/{id}` - Delete meeting

### Database Schema

```kotlin
@Entity(tableName = "meetings")
data class MeetingEntity(
    @PrimaryKey val id: String,
    val title: String,
    val transcription: String,
    val summary: String?,
    val actionItems: List<String>,
    val keyPoints: List<String>,
    val audioPath: String?,
    val duration: Long,
    val createdAt: Date,
    val updatedAt: Date,
    val status: String
)
```

## Permissions

The app requires the following permissions:

- `RECORD_AUDIO` - Required for recording meetings
- `INTERNET` - Required for API calls
- `WRITE_EXTERNAL_STORAGE` - For older Android versions (≤ API 28)
- `READ_EXTERNAL_STORAGE` - For older Android versions (≤ API 32)

## Configuration

### Backend URL

Update the backend URL in `app/build.gradle.kts`:

```kotlin
buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000\"")
```

For production, you might want to use:
- `http://10.0.2.2:8000` - Android Emulator (localhost)
- `http://YOUR_IP:8000` - Physical device
- `https://api.yourapp.com` - Production server

### Minimum SDK

Current minimum SDK is 26 (Android 8.0). To change:

```kotlin
defaultConfig {
    minSdk = 26
}
```

### App Signing

See [keystore-setup.md](keystore-setup.md) for complete signing setup instructions.

**Quick setup for local development:**
1. Generate keystore: `keytool -genkey -v -keystore release-keystore.jks ...`
2. Create `keystore.properties` with credentials
3. Build: `./gradlew assembleRelease`

## Scripts

The project includes helpful scripts in the `scripts/` directory:

### Increment Version
```bash
./scripts/increment-version.sh [major|minor|patch]
```
Automatically updates version code and version name in `build.gradle.kts`

### Generate Release Notes
```bash
./scripts/generate-release-notes.sh [previous-tag] [current-tag]
```
Generates release notes from git commits between tags

## Contributing

1. Follow Clean Architecture principles
2. Use Kotlin coding conventions
3. Write unit tests for use cases
4. Update documentation

## License

MIT License - see LICENSE file for details

## Related

- [Backend API](../backend/README.md)
- [Frontend Web App](../frontend/README.md)
- [Main Documentation](../README.md)
