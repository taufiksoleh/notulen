# Notulen Frontend

Flutter application for Indonesian meeting notes with speech-to-text capabilities.

Supports **Web**, **Android**, and **iOS** platforms.

## Features

- **Audio Recording**: Record meetings directly from your device
- **File Upload**: Upload existing audio files (MP3, WAV, M4A, OGG, FLAC, WebM)
- **Real-time Transcription**: Automatic transcription using AI models
- **Smart Summaries**: AI-generated meeting summaries
- **Action Items**: Automatic extraction of action items
- **Cross-platform**: Works on Web, Android, and iOS

## Screenshots

[Add screenshots here after testing]

## Tech Stack

- **Framework**: Flutter 3.0+
- **State Management**: Riverpod
- **Audio Recording**: record, flutter_sound
- **HTTP Client**: http, dio
- **UI**: Material Design 3

## Prerequisites

- Flutter SDK 3.0 or higher
- Dart 3.0 or higher
- For mobile development:
  - Android Studio (for Android)
  - Xcode (for iOS, macOS only)

## Installation

### 1. Install Flutter

Follow the official Flutter installation guide:
https://docs.flutter.dev/get-started/install

### 2. Clone and Setup

```bash
cd frontend
```

### 3. Install Dependencies

```bash
flutter pub get
```

### 4. Generate Code

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### 5. Configure Backend URL

Edit `lib/services/api_service.dart` and update the base URL:

```dart
ApiService({this.baseUrl = 'http://your-backend-url:8000/api/v1'});
```

For local development:
- **Mobile emulator/device**: Use your computer's IP address (e.g., `http://192.168.1.100:8000/api/v1`)
- **Web**: Use `http://localhost:8000/api/v1`

## Running the App

### Web

```bash
flutter run -d chrome
```

### Android

```bash
# Using emulator
flutter run -d android

# Using physical device (enable USB debugging)
flutter run
```

### iOS (macOS only)

```bash
# Using simulator
flutter run -d ios

# Using physical device
flutter run
```

## Building for Production

### Android APK

```bash
flutter build apk --release
```

Output: `build/app/outputs/flutter-apk/app-release.apk`

### Android App Bundle (for Play Store)

```bash
flutter build appbundle --release
```

Output: `build/app/outputs/bundle/release/app-release.aab`

### iOS (macOS only)

```bash
flutter build ios --release
```

Then open Xcode to archive and distribute.

### Web

```bash
flutter build web --release
```

Output: `build/web/`

Deploy the `build/web` folder to any static hosting service (Vercel, Netlify, Firebase Hosting, etc.)

## Project Structure

```
frontend/
├── lib/
│   ├── models/
│   │   ├── meeting.dart           # Meeting data model
│   │   └── meeting.g.dart         # Generated JSON serialization
│   ├── screens/
│   │   ├── home_screen.dart       # Meeting list
│   │   ├── record_screen.dart     # Recording interface
│   │   └── meeting_detail_screen.dart  # Meeting details
│   ├── services/
│   │   ├── api_service.dart       # Backend API client
│   │   └── audio_service.dart     # Audio recording
│   └── main.dart                   # App entry point
├── assets/
│   ├── images/
│   └── audio/
├── test/
├── pubspec.yaml                    # Dependencies
└── README.md
```

## Configuration

### Permissions

#### Android (`android/app/src/main/AndroidManifest.xml`)

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

#### iOS (`ios/Runner/Info.plist`)

```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app needs access to microphone to record meetings</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs access to photo library to upload audio files</string>
```

### Network Configuration (for local development)

#### Android

Edit `android/app/src/main/AndroidManifest.xml`:

```xml
<application
    android:usesCleartextTraffic="true"
    ...>
```

## Features Guide

### Recording a Meeting

1. Tap the "Record" button on home screen
2. Tap "Start Recording" or "Upload Audio File"
3. If recording:
   - Tap "Stop" when done
   - Tap "Cancel" to discard
4. Enter meeting title and description
5. Tap "Upload & Transcribe"
6. Wait for processing (status will show on card)

### Viewing Meeting Details

1. Tap on any meeting card from the home screen
2. View:
   - Full transcription with timestamps
   - AI-generated summary
   - Action items
   - Key discussion points

### Managing Meetings

- **Refresh**: Pull down on list or tap refresh icon
- **Delete**: Swipe left on meeting card (to be implemented)
- **Copy Transcription**: Tap copy icon in meeting detail

## API Integration

The app communicates with the backend API through `ApiService`:

### Available Methods

```dart
// Check backend health
await apiService.healthCheck();

// Create new meeting
await apiService.createMeeting(
  title: 'Team Standup',
  description: 'Daily standup meeting',
  audioFile: File('path/to/audio.mp3'),
  language: 'id',
  useIndonesianModel: true,
);

// Get all meetings
List<Meeting> meetings = await apiService.getMeetings();

// Get specific meeting
Meeting meeting = await apiService.getMeeting(meetingId);

// Delete meeting
await apiService.deleteMeeting(meetingId);

// Regenerate summary
await apiService.regenerateSummary(meetingId);
```

## Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- OGG (`.ogg`)
- FLAC (`.flac`)
- WebM (`.webm`)

## Troubleshooting

### Build Issues

```bash
# Clean build
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs

# Rebuild
flutter run
```

### Permission Issues (Mobile)

Make sure you've added the required permissions in platform-specific files (see Configuration section).

### Network Issues

- **Mobile**: Use your computer's local IP address, not `localhost`
- **Web**: CORS must be enabled in backend
- **Local development**: Backend must allow cleartext traffic

### Audio Recording Issues

- Check microphone permissions
- Ensure no other app is using the microphone
- Test on physical device (some emulators don't support audio recording)

## Development

### Adding New Features

1. Create new screens in `lib/screens/`
2. Add models in `lib/models/`
3. Update services in `lib/services/`
4. Run code generation if needed:
   ```bash
   flutter pub run build_runner build
   ```

### State Management

This app uses **Riverpod** for state management. Providers are defined at the top of screen files.

Example:
```dart
final meetingsProvider = FutureProvider<List<Meeting>>((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return await apiService.getMeetings();
});
```

### Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

## Deployment

### Web Deployment

**Vercel:**
```bash
flutter build web --release
cd build/web
vercel
```

**Netlify:**
```bash
flutter build web --release
# Upload build/web folder to Netlify
```

**Firebase Hosting:**
```bash
flutter build web --release
firebase deploy
```

### Mobile Deployment

**Google Play Store:**
1. Build app bundle: `flutter build appbundle --release`
2. Create app in Play Console
3. Upload AAB file
4. Complete store listing
5. Submit for review

**Apple App Store:**
1. Build iOS: `flutter build ios --release`
2. Open Xcode and archive
3. Upload to App Store Connect
4. Complete app information
5. Submit for review

## Performance Tips

- Use `const` constructors where possible
- Optimize images and assets
- Implement pagination for large meeting lists
- Use `ListView.builder` for long lists
- Cache API responses when appropriate

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions:
- Create an issue on GitHub
- Check documentation
- Review troubleshooting section

## Roadmap

- [ ] Offline mode
- [ ] Real-time transcription streaming
- [ ] Speaker diarization (identify different speakers)
- [ ] Export to PDF/DOCX
- [ ] Search functionality
- [ ] Meeting tags and categories
- [ ] Dark mode toggle
- [ ] Multiple language support in UI
- [ ] Share meetings

## Credits

- Built with Flutter
- UI inspired by Material Design 3
- Backend powered by Whisper and Indonesian Wav2vec 2.0
