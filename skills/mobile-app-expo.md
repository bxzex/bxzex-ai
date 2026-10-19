---
name: mobile-app-expo
description: Building native iOS and Android apps with React Native and Expo: project setup, Expo Router, core components, device modules, running on a phone, EAS builds and common errors.
---
# Mobile apps with React Native and Expo

Mobile tooling changes often. If a command or flag is unsure, check the official Expo docs (docs.expo.dev) with web_search / fetch_page before running it. All commands must be non-interactive: no prompts can be answered.

**Create**
```
npx create-expo-app@latest my-app --template default --yes
cd my-app && npx expo install   # aligns package versions to the SDK
```
The default template uses Expo Router (TypeScript). Run `npx create-expo-app --help` if the flags have changed. Use `npx expo install <pkg>` (not npm i) for Expo/native packages so versions match the SDK.

**Expo Router** (file-based, folders under `app/`)
- `app/index.tsx` is the first screen, `app/settings.tsx` is `/settings`, `app/post/[id].tsx` reads `useLocalSearchParams()`.
- `app/_layout.tsx` wraps screens; use `<Stack />` for push navigation or `<Tabs />` in `app/(tabs)/_layout.tsx`.
- Navigate with `<Link href="/settings">` or `router.push('/post/3')` from `expo-router`.

**Core components** (no HTML tags here)
- `View` is a div, `Text` holds ALL text, `Pressable` for buttons, `Image` (use `expo-image` for caching), `TextInput`, `ScrollView` for short content, `FlatList` for long or dynamic lists (give it `keyExtractor`).
- Style with `StyleSheet.create({...})`. Layout is flexbox, column by default, no px units, no CSS files.
- Wrap screens in `SafeAreaView` from `react-native-safe-area-context` (not the built-in one) so content clears the notch and home bar.
- Forms: wrap in `KeyboardAvoidingView` (`behavior={Platform.OS === 'ios' ? 'padding' : undefined}`) and set `keyboardShouldPersistTaps="handled"` on the ScrollView.
- Tap targets at least 44x44.

**Common modules** (install with `npx expo install`)
- `expo-camera`, `expo-location`, `expo-notifications`: each needs a runtime permission request and a usage string in `app.json` (iOS rejects apps with missing purpose text).
- `expo-haptics` for taps, `expo-secure-store` for tokens and secrets, `@react-native-async-storage/async-storage` for plain settings and cache.
- Push notifications need a real device and a development build on recent SDKs, not Expo Go.

**Backend and auth**
- Call your API with `fetch`. Read the base URL from `process.env.EXPO_PUBLIC_API_URL` (only `EXPO_PUBLIC_` vars reach the app, and they are public: never put secrets in them).
- Save the session token in `expo-secure-store`, send it as `Authorization: Bearer ...`, and clear it on a 401.
- `localhost` on a phone is the phone. Use the computer's LAN IP or a deployed URL.
- Show loading, empty and error states on every screen that fetches.

**Run it**
1. `npx expo start` in the background; it prints a QR code. The user scans it with the phone camera (iOS) or the Expo Go app (Android) on the same Wi-Fi. Ask them to do this; you cannot.
2. Web preview: `npx expo start --web` (needs `npx expo install react-dom react-native-web @expo/metro-runtime`), then check the URL with test_page. Good for layout; camera, haptics and notifications will not work there.
3. Simulators only if installed: iOS Simulator needs Xcode on a Mac (`xcrun simctl list`), Android emulator needs Android Studio (`emulator -list-avds`). If missing, ask the user to install them rather than guessing.

**Build and ship (EAS)**
```
npm i -g eas-cli      # or npx eas-cli@latest
eas login             # the user must do this themselves
eas build:configure
eas build -p android --profile preview --non-interactive
eas build -p ios --profile preview --non-interactive
```
- `preview` makes an installable test build (APK for Android, ad hoc for iOS). iOS builds need an Apple Developer account ($99/yr); Play uploads need a Google Play account ($25 one-time). Ask the user; do not invent credentials.
- OTA JS-only updates: `eas update --branch production --message "fix"`. Native changes (new modules, permissions) need a new build.
- Store submission is covered in the app-store-release skill.

**Common errors**
- Strange red screens or stale code: `npx expo start -c` (clears the Metro cache).
- Version mismatch warnings: `npx expo install --fix`, then `npx expo-doctor` to find the rest.
- "Unable to resolve module": the package is missing or not installed with `expo install`; delete `node_modules` and reinstall if it persists.
- Text outside `<Text>` crashes with "Text strings must be rendered within a <Text>".
- Phone cannot reach the dev server: same Wi-Fi, or try `npx expo start --tunnel`.
- Check the terminal output of the dev server for errors before blaming the code.
