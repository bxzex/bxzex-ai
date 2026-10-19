---
name: web-to-mobile-app
description: Turning an existing web app or web game into an installable phone app with a PWA or Capacitor, plus the mobile web fixes (safe areas, viewport, touch, performance) that apply either way.
---
# Web app or game to phone app

Mobile tooling changes often. Verify current commands on the official docs (capacitorjs.com/docs, web.dev) with web_search / fetch_page if unsure. Use non-interactive flags only.

**Choose the route**
- **PWA**: cheapest. Installs from the browser, no store, no fee, updates on deploy. Weaker on iOS (limited push, no store presence). Pick it for tools, dashboards and casual games.
- **Capacitor**: wraps the built web app in a native shell for the App Store and Google Play, with native plugins. Pick it when the user wants store listings. Apple may reject a thin wrapper (guideline 4.2), so add real native value: haptics, push, offline, share, a proper app feel.
- **React Native rewrite** (see mobile-app-expo): pick it for heavy native UI, complex gestures, or when performance of a web view is not enough. It is a rewrite, not a port.
- Games with canvas/WebGL usually work well in Capacitor; test on a real low-end phone.

**Mobile web essentials (do these first, they help every route)**
- `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`
- Safe areas: `padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);`
- Use `100dvh`, not `100vh` (the mobile address bar breaks vh).
- Tap targets 44x44px minimum; no hover-only UI. Use `touch-action: manipulation` to remove the 300ms delay and double-tap zoom.
- Games: `touch-action: none` on the canvas, `overscroll-behavior: none` and `user-select: none` on body to stop pull-to-refresh, bounce and text selection.
- Inputs: font-size 16px or more, or iOS zooms on focus.
- Pause on background: `document.addEventListener('visibilitychange', () => { if (document.hidden) pauseGame(); })`. Stop audio and timers there too.
- Landscape games: show a "rotate your phone" overlay in portrait; Capacitor can lock orientation in the native project settings (Info.plist / AndroidManifest).
- Performance: cap `devicePixelRatio` at 2, use `requestAnimationFrame`, avoid layout thrash, compress images (WebP), lazy-load, keep bundles small, reuse objects instead of allocating each frame.
- Check with test_page as iPhone, Android and iPad: no sideways scroll, no small tap targets, no console errors; look at the screenshots.

**Option A: PWA**
1. `public/manifest.json`:
```json
{ "name": "My App", "short_name": "MyApp", "start_url": "/", "display": "standalone",
  "background_color": "#ffffff", "theme_color": "#111111",
  "icons": [
    { "src": "/icons/192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" } ] }
```
2. In `<head>`: `<link rel="manifest" href="/manifest.json">`, `<meta name="theme-color" content="#111111">`, plus iOS tags: `<meta name="apple-mobile-web-app-capable" content="yes">`, `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">`, `<link rel="apple-touch-icon" href="/icons/180.png">`. Keep key art inside the center 80% of the maskable icon.
3. Service worker for offline: register `/sw.js`, precache the app shell on `install`, serve cache-first for static files and network-first for API calls. Or use `vite-plugin-pwa`.
4. Must be served over HTTPS (localhost is fine for testing).
5. Test: fetch the manifest URL and confirm it parses, check the console in test_page for service worker errors. iOS install is Share, then Add to Home Screen, which the user does by hand. Chrome DevTools Lighthouse can audit installability if available.

**Option B: Capacitor**
```
npm i @capacitor/core && npm i -D @capacitor/cli
npx cap init "My App" com.example.myapp --web-dir dist
npm i @capacitor/ios @capacitor/android
npx cap add ios && npx cap add android
npm run build && npx cap sync
npx cap open ios      # Xcode (Mac only)
npx cap open android  # Android Studio
```
- `--web-dir` must match the real build output (`dist` for Vite, `build` for CRA, `out` for static Next.js export). The app id is permanent once published, so ask the user what it should be.
- After every web change: `npm run build && npx cap sync`.
- Plugins: `@capacitor/haptics`, `@capacitor/status-bar`, `@capacitor/splash-screen`, `@capacitor/preferences` (use instead of localStorage, which iOS can purge), `@capacitor/share`, `@capacitor/push-notifications` (needs Apple and Firebase setup by the user). Run `npx cap sync` after installing any plugin.
- Use relative or HTTPS API URLs; the app runs from `capacitor://localhost`, so the backend must allow that origin in CORS.
- Running needs the user: Xcode for iOS, Android Studio for Android, plus an Apple Developer ($99/yr) or Google Play ($25 one-time) account to publish. Ask for those; do not guess. See app-store-release for submission.
