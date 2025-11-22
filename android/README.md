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

### Release Build
```bash
./gradlew assembleRelease
```

The APK will be generated at: `app/build/outputs/apk/`

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

### Minimum SDK

Current minimum SDK is 26 (Android 8.0). To change:

```kotlin
defaultConfig {
    minSdk = 26
}
```

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
