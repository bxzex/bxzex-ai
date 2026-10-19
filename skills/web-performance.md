---
name: web-performance
description: Making a website load faster, starting from measurements and fixing the biggest costs first.
---
# Web performance

1. **Measure first.** Write the numbers down before changing anything.
   - Lighthouse: `npx lighthouse https://site --only-categories=performance --output=json --output-path=./lh.json --chrome-flags="--headless"` then read LCP, CLS, TBT and total byte weight from the JSON.
   - Quick server timing: `curl -s -o /dev/null -w "dns %{time_namelookup} connect %{time_connect} ttfb %{time_starttransfer} total %{time_total} size %{size_download}\n" URL`.
   - Headers: `curl -sI URL`.
2. **Find the heavy things.** List the largest files: `find dist -type f -size +100k -exec ls -lh {} \; | sort -k5 -h`. Images are usually the biggest cost, then JavaScript.
3. **Images**
   - Convert to WebP or AVIF: `cwebp -q 80 in.jpg -o out.webp` (`brew install webp` or `apt install webp`).
   - Resize to the largest size actually shown, plus 2x for sharp screens. A 4000px photo in a 400px slot is waste.
   - Always set `width` and `height` attributes (stops layout shift).
   - `loading="lazy"` on images below the fold. Never on the main hero image; give that `fetchpriority="high"`.
   - Use `srcset` and `sizes` for responsive images.
4. **Fonts**
   - Self-host WOFF2, subset to the characters you need.
   - `font-display: swap`, and preload only the one or two fonts used above the fold.
   - Cut weights you do not use.
5. **JavaScript and CSS**
   - Check bundle size: `npx vite-bundle-visualizer` or `npx source-map-explorer dist/assets/*.js`.
   - Remove unused dependencies, import only what you call (`lodash/debounce`, not all of lodash), split routes with dynamic `import()`.
   - Add `defer` to scripts. Inline only small critical CSS.
6. **Caching and delivery**
   - Hashed assets: `Cache-Control: public, max-age=31536000, immutable`.
   - HTML: `max-age=0, must-revalidate`.
   - Confirm compression: `curl -sI -H "Accept-Encoding: br,gzip" URL | grep -i content-encoding`.
7. **Third parties.** Each tracker, chat widget or embed costs time. Remove what the owner does not use, load the rest late.
8. **Measure again** with the same command and report before and after numbers.

Pitfalls: optimizing something that is not the bottleneck, lazy loading the largest visible image, testing only on a fast machine.
