---
name: ui-polish
description: Final polish pass on a finished interface: spacing, alignment, radii, borders, states, icons and type details.
---
# UI polish

Do this after the thing works. Open the CSS and the page side by side and go through in order.

1. **Spacing rhythm.** List every padding, margin and gap: `grep -rhoE "(padding|margin|gap)[a-z-]*: *[^;]+" src | sort | uniq -c | sort -rn`. Reduce to a scale (4, 8, 12, 16, 24, 32, 48, 64). Related items sit closer than unrelated ones.
2. **Alignment.** Left edges share one line. Icons and text are vertically centered (`display:flex; align-items:center`). Numbers in columns are right aligned.
3. **Radii.** One radius for controls, one for cards, one for pills. Nested radius = outer radius minus padding.
4. **Borders and shadows.** One border color and width (1px). Shadows share one direction and softness. Remove any that do not separate anything.
5. **States.** Every button, link and input has hover, `:focus-visible` (a clear 2px ring with offset), active (slightly darker or 1px down), and disabled (reduced contrast plus `cursor:not-allowed`). Add `transition: 150ms` on color, background and shadow only.
6. **Icons.** One icon set, one stroke width, sizes 16, 20 or 24. Icon next to text matches the text's cap height.
7. **Type details.**
   - `font-variant-numeric: tabular-nums` for numbers in tables.
   - `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
   - Proper quotes and an ellipsis character, no double spaces, no orphaned single word on the last line.
   - Max line length about 70 characters.
8. **Images.** Set width and height to avoid shift, `object-fit: cover`, same aspect ratio in a set.
9. **Selection and scrollbars.** Set `::selection` to the accent tint, `color-scheme` for dark mode so form controls match.

Finish by screenshotting at 375, 768 and 1440px. Fix what you see, then stop. Polish is not a redesign.
