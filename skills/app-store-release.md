---
name: app-store-release
description: Shipping a mobile app to the Apple App Store and Google Play: accounts, icons, screenshots, listing copy, privacy forms, test tracks, submission and avoiding common rejections.
---
# App Store and Google Play release

Store rules and screen sizes change every year. Confirm current requirements on developer.apple.com and support.google.com/googleplay/android-developer with web_search / fetch_page before relying on numbers below.

**What the user must do personally (ask, never guess)**
- Apple Developer Program account, $99/yr, then create the app in App Store Connect.
- Google Play Console account, $25 one-time, identity verification, then create the app.
- Sign in to EAS/Expo (`eas login`) or Xcode with their Apple ID. You cannot type passwords or 2FA codes.
- Accept store agreements, fill tax and banking info if the app is paid.
- Brand-new personal Play accounts may need a closed test with a number of testers for a set time before production. Check the current rule and tell the user early.

**Identity and versions**
- iOS bundle ID and Android package name (`com.company.app`) are permanent. Ask the user, set both in `app.json` (Expo) or `capacitor.config`.
- Version (`1.0.0`) is what users see. Build number (iOS `buildNumber`) / `versionCode` (Android) must go up on every upload. With EAS, set `"autoIncrement": true` in the production profile of `eas.json`.

**Icon and splash**
- App icon 1024x1024 PNG. iOS: no transparency, no rounded corners (the system rounds it). Android adaptive icon: foreground on a transparent layer with a background color; keep art in the center safe zone. Google Play listing icon is 512x512.
- Splash: simple logo on a solid color. Do not use text that needs reading.

**Screenshots** (required per device class; check current sizes)
- iPhone 6.9" (or 6.7") portrait, iPad 13" if the app supports iPad. Android: at least 2 phone screenshots, plus 7" and 10" tablet if offered; also a 1024x500 feature graphic.
- Make them with test_page at those device sizes, or from a simulator (`xcrun simctl io booted screenshot shot.png`). Use real app screens, not mockups with fake data. Add a short caption only if it helps.

**Listing copy** (plain and honest, no claims the app cannot back up)
- Apple: name up to 30 chars, subtitle 30, keywords 100 chars comma-separated (no spaces, no repeating the name), description, promo text, support URL, marketing URL.
- Google: title 30, short description 80, full description 4000.
- Describe what the user can do in the first two lines. No competitor names, no "best" or "#1", no keyword stuffing.

**Privacy and ratings**
- A public privacy policy URL is required by both stores. Write one that matches what the app really collects and host it on the user's site.
- Apple "App Privacy" nutrition label and Google "Data safety" form: list every data type collected, including analytics, crash reports and SDKs. Answers must match the policy and the code.
- Complete the age rating questionnaire honestly. Declare ads and content rules.
- Apps with accounts must offer in-app account deletion (both stores). Provide a delete option and a working flow.

**Test first**
- iOS: upload to TestFlight, add internal testers (no review), then external testers (light review).
- Android: Play Console internal testing track (instant), then closed/open testing.
- Install on a real device and go through sign-up, login, core flow, offline, and deletion.

**Build and upload**
- Expo: `eas build -p ios --profile production` and `eas build -p android --profile production`, then `eas submit -p ios --latest` and `eas submit -p android --latest`. Android first upload may need to be done by hand in Play Console; EAS needs a service account key from the user.
- Without EAS: Xcode, Product, Archive, then upload via Organizer or Transporter. Android: build an `.aab` (`./gradlew bundleRelease`) signed with an upload key and upload it in Play Console. Keep the keystore and passwords safe and tell the user to back them up.

**Common rejection reasons**
- Crashes, broken links, or features that need a backend that is not live.
- Placeholder content, lorem ipsum, empty screens, "coming soon" buttons.
- Login required but no demo account in the review notes. Always give reviewers working credentials.
- Web wrapper with no native value (Apple guideline 4.2). Add real native features or ship a PWA instead.
- Missing account deletion; missing or wrong privacy policy; permission requests without a clear purpose string.
- Selling digital goods, subscriptions or unlocks without store billing (Apple in-app purchase, Google Play Billing). Physical goods and services use other payment methods.
- Metadata that does not match the app, or mentions other platforms.

**Release checklist**
1. Version and build number bumped, production API URLs set, debug code and test keys removed.
2. Icon, screenshots, listing copy, policy URL, privacy forms, age rating done.
3. Tested on a real device from TestFlight / Play internal track.
4. Review notes written with demo login and how to reach any hidden features.
5. Submit for review (Apple usually 1 to 2 days; Google hours to days). Choose manual release so you control launch.

**Updating later**
- Bump version and build number, rebuild, submit again with "what's new" text. Apple re-reviews every build.
- JS-only fixes in Expo can go out with `eas update`, but do not use OTA to change what the app fundamentally does.
- Watch crash reports and reviews after launch; reply to reviews.
