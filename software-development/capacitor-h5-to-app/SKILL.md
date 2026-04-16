---
name: capacitor-h5-to-app
description: Package any H5 web app into a native Android/iOS app using Capacitor. Handles static asset downloading, HTTP backend configuration, offline-capable packaging, and automated build pipelines.
---

# Package H5 App with Capacitor

Use when the user wants to turn an existing H5/web app (hosted at a URL) into a downloadable Android/iOS native app.

## Prerequisites
- Node.js 22+ installed (Capacitor 8 requires >=22)
- npm installed
- For local builds: Android Studio + JDK 21+ (Capacitor 8 requires 21; older Capacitor uses 17)

## Steps

### 1. Create project directory and download web assets
```bash
mkdir h5-to-app && cd h5-to-app
mkdir -p web-assets

# Download index page and parse asset references
curl -s <H5_URL>/ -o web-assets/index.html

# Extract JS/CSS filenames from index.html, then download them
# Also download any other static assets (images, fonts, etc.)
curl -s <H5_URL>/path/to/asset.js -o web-assets/path/to/asset.js
```

### 2. Initialize npm project and install Capacitor
```bash
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
# Add @capacitor/ios for iOS support
```

### 3. Create `capacitor.config.json`
```json
{
  "appId": "com.yourcompany.yourapp",
  "appName": "Your App Name",
  "webDir": "web-assets",
  "server": {
    "androidScheme": "https",
    "allowNavigation": [
      "http://your-api-server:*",
      "https://your-api-server:*"
    ]
  },
  "android": {
    "allowMixedContent": true
  }
}
```

### 4. Add platforms and sync
```bash
npm install @capacitor/android @capacitor/ios
npx cap add android
npx cap add ios
npx cap sync
```

For both platforms, use `npx cap sync` (no args) to sync all. Use `npx cap sync android` or `npx cap sync ios` for individual.

### 5. Configure HTTP cleartext traffic (if backend uses HTTP)

Edit `android/app/src/main/AndroidManifest.xml`, add to `<application>`:
```xml
android:usesCleartextTraffic="true"
```

Create `android/app/src/main/res/xml/network_security_config.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">your-api-domain.com</domain>
    </domain-config>
    <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

### 6. Build APK

**Android Studio**: Open `android/` folder → Build → Build APK(s)

**Command line** (requires Android SDK):
```bash
cd android && ./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```

**GitHub Actions** (no local Android SDK needed): Create `.github/workflows/build-apk.yml`:

Important: Capacitor 8 requires Node.js >=22 and JDK 21. The `capacitor-android` module lives in `node_modules`, so CI must run `npm install` + `npx cap sync android` before building. Do NOT rely on pre-committed generated files alone.

```yaml
name: Build Android APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'   # Capacitor 8 requires >=22
      - name: Install dependencies
        run: npm install
      - name: Sync Capacitor
        run: npx cap sync android
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '21'   # Capacitor 8 requires 21
          distribution: 'temurin'
      - uses: android-actions/setup-android@v3
      - run: chmod +x android/gradlew
      - run: cd android && ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: app-debug
          path: android/app/build/outputs/apk/debug/app-debug.apk
```

**Download the built APK**:
```bash
# Using gh CLI
gh run download --name app-debug -D ~/Downloads/

# Or via API
curl -L -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/artifacts/ARTIFACT_ID/zip" \
  -o app-debug.zip && unzip app-debug.zip
```

## iOS Build

### iOS Prerequisites
- macOS with **full Xcode** from App Store (Command Line Tools alone is NOT sufficient)
- Apple Developer account (for signing and distribution; simulator testing doesn't need it)

### iOS HTTP Cleartext Traffic
iOS blocks HTTP by default via App Transport Security (ATS). Add to `ios/App/App/Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```
For production, prefer domain-specific exceptions instead of NSAllowsArbitraryLoads.

### Open in Xcode and Build
```bash
npx cap open ios
# Or: open ios/App/App.xcworkspace
```
In Xcode: select target device/simulator → Product → Build (Cmd+B). For release: Product → Archive.

### iOS Project Structure
- Uses Swift Package Manager (SPM) by default in Capacitor 8 (no CocoaPods needed)
- Xcode project: `ios/App/App.xcodeproj`
- Web assets: `ios/App/App/public/`
- Config: `ios/App/App/capacitor.config.json`

### GitHub Actions: Unified Android + iOS Build

For dual-platform CI, use parallel jobs. Key learnings from trial-and-error:

```yaml
name: Build All Platforms
on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: write  # REQUIRED for creating releases

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm install
      - run: npx cap sync android
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
      - uses: android-actions/setup-android@v3
      - run: |
          chmod +x android/gradlew
          cd android && ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: android-apk
          path: android/app/build/outputs/apk/debug/app-debug.apk

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm install
      - run: npx cap sync ios
      # Use -project NOT -workspace (Capacitor 8 uses SPM, not CocoaPods)
      # Do NOT pin Xcode version unless you've verified it exists on runner
      - name: Build iOS (Simulator, no signing)
        run: |
          cd ios/App
          xcodebuild -project App.xcodeproj \
            -scheme App \
            -configuration Debug \
            -destination 'generic/platform=iOS Simulator' \
            -derivedDataPath build \
            CODE_SIGN_IDENTITY="" \
            CODE_SIGNING_REQUIRED=NO \
            CODE_SIGNING_ALLOWED=NO \
            build
      - name: Package iOS App
        run: |
          cd ios/App/build/Build/Products/Debug-iphonesimulator
          zip -r -y App-debug.zip App.app
      - uses: actions/upload-artifact@v4
        with:
          name: ios-app
          path: ios/App/build/Build/Products/Debug-iphonesimulator/App-debug.zip

  release:
    needs: [build-android, build-ios]
    runs-on: ubuntu-latest
    if: success()
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: android-apk
          path: ./artifacts
      - uses: actions/download-artifact@v4
        with:
          name: ios-app
          path: ./artifacts
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: v1.0.${{ github.run_number }}
          name: App v1.0.${{ github.run_number }}
          body: |
            ## Auto Build - ${{ github.sha }}
            ### Android
            - `app-debug.apk` - Install directly
            ### iOS
            - `App-debug.zip` - Simulator version
          files: |
            ./artifacts/app-debug.apk
            ./artifacts/App-debug.zip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**CI Pitfalls discovered through trial and error:**
- **`-project` not `-workspace`**: Capacitor 8 uses SPM (Package.swift) not CocoaPods. Using `-workspace App.xcworkspace` fails with exit code 66. Use `-project App.xcodeproj`.
- **Don't pin Xcode version**: `macos-latest` may not have the version you specify. Remove the `sudo xcode-select -s` step unless needed. Add a debug step `ls /Applications/ | grep Xcode` to check.
- **Release needs `permissions: contents: write`**: Without this at workflow level, `softprops/action-gh-release` fails with "Resource not accessible by integration".
- **Release job needs both builds**: Use `needs: [build-android, build-ios]` and `if: success()` so release only runs when both pass.
- **Simulator build needs signing flags**: Even for simulator, must explicitly set `CODE_SIGN_IDENTITY="" CODE_SIGNING_REQUIRED=NO CODE_SIGNING_ALLOWED=NO` or xcodebuild fails.
- **iOS output path**: xcodebuild puts output at `build/Build/Products/Debug-iphonesimulator/` (note the nested Build directory).

## Pitfalls
- **Capacitor 8 version requirements**: Requires Node.js >=22 and JDK 21. Using older versions gives cryptic errors ("invalid source release: 21", "requires NodeJS >=22.0.0"). Check versions before starting.
- **CI needs npm install + cap sync**: The `capacitor-android` module lives in `node_modules/@capacitor/android/`. On CI, you must run `npm install` then `npx cap sync` before building. The android `.gitignore` excludes `capacitor-cordova-android-plugins/` and `app/src/main/assets/public/` — either commit them or (better) regenerate via `capacitor sync` in CI.
- **capacitor.settings.gradle references node_modules**: The generated `capacitor.settings.gradle` does `project(':capacitor-android').projectDir = new File('../node_modules/@capacitor/android/capacitor')`. Without `npm install`, gradle can't find the module and fails with "No matching variant of project :capacitor-android".
- **HTTP backends (Android)**: Android 9+ blocks cleartext HTTP by default. Must set `usesCleartextTraffic="true"` AND network security config, or API calls fail silently.
- **HTTP backends (iOS)**: iOS blocks HTTP via App Transport Security. Must add `NSAllowsArbitraryLoads` to Info.plist, or API calls silently fail.
- **SPA routing**: If the H5 app uses client-side routing (React Router, Vue Router), local file loading may break deep links. Consider adding a fallback or using hash routing.
- **Offline vs online**: Static assets are bundled in APK/IPA (UI loads offline), but API calls still need network. Full offline requires implementing local data caching in the H5 app itself.
- **iOS requires full Xcode**: Command Line Tools alone won't work. Must install full Xcode from App Store and run `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`.
- **iOS signing**: Requires Apple Developer account for device testing and App Store distribution. Simulator testing works without signing.
- **Asset updates**: When H5 source changes, re-download assets and run `npx cap sync` (syncs all platforms) before rebuilding.

## Asset Update Script Template
```bash
#!/bin/bash
# update-assets.sh - re-download and sync
BASE_URL="http://your-h5-url"
DIR="$(cd "$(dirname "$0")" && pwd)/web-assets"
curl -s "$BASE_URL/" -o "$DIR/index.html"
# Re-download all referenced assets...
cd "$DIR/.." && npx cap sync
echo "Done. Rebuild in Android Studio / Xcode."
```

## Verification
- Install APK on device/emulator
- Confirm app launches with correct name/icon
- Confirm API calls work (check for HTTP errors in logcat)
- Enable airplane mode → confirm UI still loads (static assets offline)
