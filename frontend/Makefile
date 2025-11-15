.PHONY: help install get build-runner run-web run-android run-ios build-web build-android build-ios test format clean doctor

# Default target
help:
	@echo "Frontend Makefile Commands:"
	@echo "==========================="
	@echo "install          - Install Flutter dependencies"
	@echo "get              - Get Flutter packages"
	@echo "build-runner     - Generate code with build_runner"
	@echo "run-web          - Run app on Chrome"
	@echo "run-android      - Run app on Android"
	@echo "run-ios          - Run app on iOS"
	@echo "run-mobile       - Run app on connected mobile device"
	@echo "build-web        - Build for web production"
	@echo "build-android    - Build Android APK"
	@echo "build-appbundle  - Build Android App Bundle"
	@echo "build-ios        - Build iOS app"
	@echo "test             - Run tests"
	@echo "test-cov         - Run tests with coverage"
	@echo "format           - Format Dart code"
	@echo "analyze          - Analyze Dart code"
	@echo "clean            - Clean build artifacts"
	@echo "doctor           - Run flutter doctor"
	@echo "upgrade          - Upgrade Flutter dependencies"

# Install Flutter dependencies
install: get

# Get Flutter packages
get:
	flutter pub get

# Generate code with build_runner
build-runner:
	flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode for build_runner
build-runner-watch:
	flutter pub run build_runner watch --delete-conflicting-outputs

# Run on web
run-web:
	flutter run -d chrome

# Run on web with specific port
run-web-port:
	flutter run -d chrome --web-port=8080

# Run on Android
run-android:
	flutter run -d android

# Run on iOS
run-ios:
	flutter run -d ios

# Run on any connected device
run-mobile:
	flutter run

# Run with specific device
run-device:
	@echo "Available devices:"
	@flutter devices
	@read -p "Enter device ID: " device; \
	flutter run -d $$device

# Build for web (production)
build-web:
	flutter build web --release
	@echo "Web build completed! Output: build/web/"

# Build for web with specific base href
build-web-base:
	@read -p "Enter base href (e.g., /notulen/): " href; \
	flutter build web --release --base-href $$href

# Build Android APK
build-android:
	flutter build apk --release
	@echo "APK built! Output: build/app/outputs/flutter-apk/app-release.apk"

# Build Android App Bundle (for Play Store)
build-appbundle:
	flutter build appbundle --release
	@echo "App Bundle built! Output: build/app/outputs/bundle/release/app-release.aab"

# Build iOS
build-ios:
	flutter build ios --release
	@echo "iOS build completed!"

# Build for all platforms
build-all: build-web build-android build-appbundle

# Run tests
test:
	flutter test

# Run tests with coverage
test-cov:
	flutter test --coverage
	@echo "Coverage report: coverage/lcov.info"

# Format code
format:
	flutter format lib/ test/

# Check formatting
format-check:
	flutter format --set-exit-if-changed lib/ test/

# Analyze code
analyze:
	flutter analyze

# Clean build artifacts
clean:
	flutter clean
	rm -rf build/
	rm -rf .dart_tool/
	@echo "Cleaned build artifacts"

# Full clean (including packages)
clean-all: clean
	rm -rf .packages
	rm -rf pubspec.lock
	@echo "Cleaned all artifacts and packages"

# Run flutter doctor
doctor:
	flutter doctor -v

# Upgrade dependencies
upgrade:
	flutter pub upgrade

# Upgrade Flutter SDK
upgrade-flutter:
	flutter upgrade

# Generate app icons (requires flutter_launcher_icons package)
icons:
	flutter pub run flutter_launcher_icons:main

# Generate splash screens (requires flutter_native_splash package)
splash:
	flutter pub run flutter_native_splash:create

# Setup project (first time)
setup: get build-runner
	@echo "Setup complete! Edit lib/services/api_service.dart to configure backend URL."
	@echo "Run 'make run-web' to start the app."

# Development setup with watch mode
dev: get
	@echo "Starting development mode with build_runner watch..."
	@echo "In another terminal, run 'make run-web' or 'make run-mobile'"
	flutter pub run build_runner watch --delete-conflicting-outputs

# Production build for web deployment
deploy-web: build-web
	@echo "Web app built for production!"
	@echo "Deploy the 'build/web' folder to your hosting service."
	@echo ""
	@echo "Quick deploy options:"
	@echo "  Vercel:  cd build/web && vercel"
	@echo "  Netlify: netlify deploy --prod --dir=build/web"
	@echo "  Firebase: firebase deploy"

# Check for outdated packages
outdated:
	flutter pub outdated

# Repair cache (if having issues)
repair:
	flutter pub cache repair

# List all connected devices
devices:
	flutter devices

# Performance profiling
profile-web:
	flutter run -d chrome --profile

profile-android:
	flutter run -d android --profile

# Release information
release-info:
	@echo "Build Information:"
	@echo "=================="
	@flutter --version
	@echo ""
	@echo "Dependencies:"
	@flutter pub deps --style=compact

# Run linter
lint: analyze format-check

# Complete check before commit
check: format analyze test
	@echo "All checks passed! ✓"

# Watch and run (for development)
watch:
	@echo "Watching for changes..."
	@while true; do \
		flutter pub run build_runner build --delete-conflicting-outputs 2>/dev/null; \
		sleep 5; \
	done
