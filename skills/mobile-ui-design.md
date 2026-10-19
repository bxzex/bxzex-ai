---
name: mobile-ui-design
description: Designing app screens that feel native on phones, for React Native apps, PWAs and mobile web apps: navigation, thumb reach, inputs, states, motion and dark mode.
---
# Mobile UI design

Everything in no-ai-slop applies. For code see mobile-app-expo or web-to-mobile-app, and accessibility for screen readers and contrast.

**Reach and layout**
- Put the main controls in the lower half of the screen where the thumb reaches. Titles and info go up top.
- Bottom tab bar with 3 to 5 tabs, each an icon and a short label. More than 5: move the rest into a "More" or profile screen.
- One primary action per screen, a full-width filled button or a floating button, and everything else is quieter.
- Side gutters of 16px. Use `100dvh`, not `100vh`.

**Safe areas**
- Respect the notch, rounded corners and home indicator.
```
padding-top: env(safe-area-inset-top);
padding-bottom: env(safe-area-inset-bottom);
```
- Web apps need `viewport-fit=cover` in the viewport meta for those values to work. In React Native use the safe area context.
- Sticky bars and floating buttons must not cover the last list item: add bottom padding equal to their height.

**Navigation**
- Screens push and pop in a stack with a back control at top left and the edge-swipe back gesture (iOS). On Android the system back button must also work.
- Forward moves slide in from the right, modals and sheets come from the bottom.
- Use bottom sheets for pickers, filters, confirmations and quick actions, not centered modals. A sheet has a grab handle, closes on drag down and on tapping outside.
- Keep the user's place: scroll position and tab state survive going back.

**Lists and content**
- Prefer plain lists with a divider line over grids of cards. A row has a title, one line of detail and a trailing value or chevron.
- Rows are at least 44px tall (48dp on Android) and the whole row is tappable.
- Pull to refresh on any list that can go stale. Swipe actions on rows only as a shortcut, never the only way.
- Long lists: paginate or virtualize.

**Loading and states**
- Use skeleton rows that match the layout instead of "Loading…" text for lists and feeds. A small spinner is fine for a button press.
- Empty: one sentence and one action. Error: what failed, a retry button, and keep any cached content visible.
- Offline: show a quiet banner, keep reading cached data, queue writes and say so ("Saved on this phone, will send when you're back online"). Slow network: show progress, never freeze a button without feedback.

**Inputs**
- Set the right keyboard: `type="email"` or `inputmode="email"`, `tel`, `numeric`, `decimal`, `search`, and `enterkeyhint` for the return key.
- Add `autocomplete` (`email`, `username`, `current-password`, `new-password`, `one-time-code`, `name`, `street-address`).
- Inputs must be 16px or larger, otherwise iOS zooms the page on focus. Never disable zoom to hide it.
- Keep the focused field visible above the keyboard. Use labels above fields, not placeholder-only.
- Use pickers, toggles and segmented controls instead of typing wherever you can.

**Type and targets**
- Body text 17px on iOS (16px minimum on the web), secondary text 13 to 15px, nothing under 12px. Use the system font stack so it matches the platform.
- Tap targets 44x44px on iOS, 48x48dp on Android, with at least 8px between neighbors. A small icon gets padding to reach this size.

**Platform differences**
- iOS: large titles, tab bar at the bottom, sheets, back swipe, text-style buttons in headers, switches.
- Android: top app bar, system back, a floating action button for the main create action, ripple on press, snackbars for short messages.
- If the app is one codebase, follow the platform for navigation and system controls, and keep your own look for content.

**Feedback and motion**
- Every press shows an immediate pressed state (color change, not opacity fade).
- Haptics on key moments only: a completed action, a toggle, a destructive confirm. Not on every tap.
- Motion is 150 to 250ms with ease-out, used to show where something came from or went. No decoration.
- Honor `prefers-reduced-motion` (and the reduce-motion setting in React Native): swap slides for a quick fade or nothing.

**Dark mode**
- Design it as its own palette, not inverted colors. Background a dark gray (not pure black, unless the screen is OLED-first), raised surfaces slightly lighter, text off-white.
- Lower the saturation of accent colors a little, and keep 4.5:1 contrast for text. Check images and shadows in both themes.
- Follow the system setting with `prefers-color-scheme`, and offer a manual choice in settings.

**Onboarding and permissions**
- Cut onboarding to the minimum: let people use the app first, ask for an account when it's needed, skip the 4-slide intro.
- Ask for notifications, location, camera or contacts at the moment the feature needs them, after a line saying why. If they say no, the app still works and explains how to change it.

**Check it**
1. Run test_page as a phone and as phone-landscape, and look at each screenshot: tab bar, sheet, keyboard-heavy forms, empty and error states, dark mode.
2. Fix any sideways scroll, targets under 44px and console errors it reports.
3. Run the no-ai-slop finish gate on the screenshots.
