---
name: web-design-review
description: Checking a site's code against practical web interface rules and listing exact fixes.
---
# Web design review

Read the HTML, CSS and components with read_file or search_files, then check each rule. Report file and line for every miss.

1. **Semantic HTML.** One `<h1>`, headings in order, `<header> <nav> <main> <footer>`, lists as `<ul>`, buttons as `<button>`, links as `<a href>`. Search for `onClick` on `div` or `span`: `grep -rnE "<(div|span)[^>]*onClick" src`.
2. **Focus.** Every interactive element shows a visible focus ring. Search for `outline: none` or `outline: 0` without a replacement. Use `:focus-visible`. Tab through the page in order.
3. **Forms.** Each input has a `<label for>` or wrapping label, the right `type` (email, tel, number), `autocomplete`, and `name`. Errors linked with `aria-describedby`. Placeholder is not the label.
4. **Touch targets.** 44 by 44px minimum on mobile, with spacing between them.
5. **Contrast.** Text 4.5:1, large text and UI borders 3:1. Check muted grey text on white first, it fails most often.
6. **Images.** Every `<img>` has meaningful `alt` (empty `alt=""` if decorative), `width` and `height` set, `loading="lazy"` below the fold, `srcset` or a modern format (webp, avif), and the hero image is not lazy loaded.
7. **No layout shift.** Reserve image and embed space, set `font-display: swap`, avoid injecting banners above content after load.
8. **Responsive.** `<meta name="viewport" content="width=device-width, initial-scale=1">`, no horizontal scroll at 375px, text at least 16px so iOS does not zoom inputs.
9. **Dark mode.** Colors as CSS variables, `@media (prefers-color-scheme: dark)` override, `color-scheme: light dark`, no pure black and white, images and shadows checked.
10. **Motion.** Wrap animations in `@media (prefers-reduced-motion: no-preference)`.
11. **Basics.** `<title>`, meta description, `lang` on `<html>`, favicon, working 404 page.

Output a table: rule, status (pass or fail), location, fix. Fix the failures if asked, then recheck.
