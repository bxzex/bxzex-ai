---
name: accessibility
description: Checking or building a web page so people using keyboards, screen readers or low vision can use it.
---
# Accessibility

Check these in order. Most problems are in the first five.

1. **Contrast.** Body text at least 4.5:1 against its background, large text 3:1. Grey text on grey fails often.
2. **Keyboard.** Tab through the whole page. Everything clickable must be reachable, in a sensible order, with a visible focus ring. Never `outline: none` without a replacement.
3. **Real elements.** `button` for actions, `a` for navigation, `label` tied to every form field. A clickable `div` is a bug.
4. **Images.** Meaningful images get `alt` text describing what they show. Decorative ones get `alt=""`.
5. **Headings.** One `h1`, then `h2`, `h3` in order without skipping. They are how screen reader users scan.
6. **Forms.** Errors are written in text next to the field, not shown only by color. Say how to fix them.
7. **Color alone** never carries meaning. Add an icon, label or pattern.
8. **Text size.** Page still works zoomed to 200%. Use `rem`, not fixed pixels, for type.
9. **Motion.** Respect `prefers-reduced-motion`. Nothing flashes more than three times a second.
10. **Touch.** Targets at least 44 by 44 pixels with space between them.
11. **Language.** Set `lang` on the `html` element. Give the page a real `title`.
12. **ARIA** only when no real element does the job. Wrong ARIA is worse than none.

Report what fails with the element and the fix. Say what you could not test.
