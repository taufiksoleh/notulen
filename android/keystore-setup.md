# Android Keystore Setup Guide

This guide explains how to set up signing keys for releasing the Android app.

## Local Development

### 1. Generate a Keystore

```bash
cd android/app
keytool -genkey -v -keystore release-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release
```

Follow the prompts to set:
- Keystore password
- Key password
- Your name and organization details

### 2. Configure Local Properties

Create or update `android/keystore.properties`:

```properties
storeFile=release-keystore.jks
storePassword=YOUR_STORE_PASSWORD
keyAlias=release
keyPassword=YOUR_KEY_PASSWORD
```

**Important:** Never commit `keystore.properties` or `release-keystore.jks` to Git!

### 3. Add to .gitignore

Ensure these are in `.gitignore`:
```
*.jks
*.keystore
keystore.properties
```

## CI/CD Setup (GitHub Actions)

### 1. Encode Keystore to Base64

```bash
base64 -i release-keystore.jks -o keystore-base64.txt
```

### 2. Add GitHub Secrets

Go to your repository: **Settings → Secrets and variables → Actions**

Add the following secrets:

- `KEYSTORE_BASE64`: Contents of `keystore-base64.txt`
- `SIGNING_STORE_PASSWORD`: Your keystore password
- `SIGNING_KEY_ALIAS`: Your key alias (usually "release")
- `SIGNING_KEY_PASSWORD`: Your key password

### 3. Optional: Play Store Publishing

For automatic Play Store uploads, add:

- `PLAY_STORE_JSON_KEY`: Service account JSON key from Google Play Console

#### How to Get Play Store JSON Key:

1. Go to [Google Play Console](https://play.google.com/console)
2. Navigate to **Setup → API access**
3. Create a new service account or use existing
4. Grant permissions: **Release manager** role
5. Create and download JSON key
6. Copy the entire JSON content to the GitHub secret

## Building Signed APK Locally

### Debug Build (No Signing Required)
```bash
cd android
./gradlew assembleDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`

### Release Build (Requires Keystore)
```bash
cd android
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

### Build AAB (Android App Bundle)
```bash
cd android
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

## Security Best Practices

1. **Never commit** keystore files to version control
2. **Use strong passwords** for keystore and key
3. **Backup your keystore** securely - if lost, you cannot update your app!
4. **Rotate keys periodically** for better security
5. **Use GitHub Secrets** for CI/CD, never hardcode credentials

## Testing Signed APK

After building:

```bash
# Verify signing
jarsigner -verify -verbose -certs app/build/outputs/apk/release/app-release.apk

# Install on device
adb install app/build/outputs/apk/release/app-release.apk
```

## Backup Your Keystore

**CRITICAL:** Store your keystore securely:

- ✅ Encrypted cloud storage (Google Drive, 1Password, etc.)
- ✅ Encrypted external drive
- ✅ Company password manager
- ❌ Never in version control
- ❌ Never in plain text

If you lose your keystore, you **cannot** update your published app. You'll need to publish a new app with a different package name.

## Troubleshooting

### Error: "Keystore was tampered with, or password was incorrect"
- Double-check your passwords
- Ensure the keystore file path is correct
- Verify the key alias matches

### Error: "Failed to read key from keystore"
- The key alias might be wrong
- The key password might be different from store password

### CI/CD Build Fails with Signing Error
- Check that GitHub Secrets are set correctly
- Verify base64 encoding of keystore is correct
- Ensure no extra whitespace in secrets

## Additional Resources

- [Android App Signing Guide](https://developer.android.com/studio/publish/app-signing)
- [Managing Your App's Signing Keys](https://support.google.com/googleplay/android-developer/answer/9842756)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
