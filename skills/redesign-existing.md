---
name: redesign-existing
description: Improving the look of an existing site or app without breaking its content or behavior.
---
# Redesign an existing site

Never start by rewriting. Start by looking.

1. **Snapshot the current state.** Read the markup and styles. If a headless browser is available, take screenshots at 375px and 1440px wide (`npx playwright screenshot --viewport-size=375,800 URL before-mobile.png`). Save the originals.
2. **Make a safety net.** Run `git status` and commit or stash first so changes are reversible. Run the existing tests and build and note whether they pass now.
3. **List problems by impact,** highest first, in a short file:
   - No clear focal point or primary action.
   - Text hard to read: contrast under 4.5:1, size under 16px, long lines.
   - Spacing with no pattern, things touching, cramped sections.
   - Too many fonts, sizes, colors or radii.
   - Broken or ugly on mobile, tap targets under 44px.
   - Missing hover, focus, loading, empty and error states.
   - Placeholder text, fake numbers, broken images or links.
4. **Fix in this order:** hierarchy and layout, then spacing, then type, then color and contrast, then polish. Introduce CSS variables for the values you keep repeating, rather than editing 40 places.
5. **Keep what works.** Do not change copy, routes, form field names, ids or classes that scripts depend on. If you rename something, search for every use first: `grep -rn "old-name" .`.
6. **Work in small steps.** After each step reload and compare with the screenshot. Do not restyle every page at once; finish the home page, then carry the pattern over.
7. **Verify after.**
   - Build and tests still pass.
   - Forms, links and buttons still work (click or curl them).
   - New screenshots at 375, 768 and 1440 wide, checked for overflow and overlap.
   - Contrast checked on the new colors.
8. **Report** what changed and what you left alone on purpose.

Also load ui-design and no-ai-slop. Do not add effects (gradients, glows, blur) just to make it look new. Better spacing and type almost always do more.
