---
name: no-ai-slop
description: Required check on every design, website, web app, mobile app or game UI, so it never looks generic or machine-made ("vibecoded").
---
# No AI slop

Run this on anything with a screen, before you call it done. If the user has their own design rules (about.md, BXZEX.md, the project's notes), theirs win wherever they differ from this.

**Never (the 20 signs a page was vibecoded)**
1. Purple-to-blue, pink-to-orange or any "AI" gradient.
2. Gradient text (`background-clip: text`).
3. Emoji in headings, buttons, bullets or UI.
4. Inter everywhere (or Roboto, or Arial as the face).
5. Cards with a colored left or top border.
6. Glassmorphism: `backdrop-filter`, translucent frosted panels, glow behind cards.
7. Low-contrast text. Body text and labels must clear 4.5:1.
8. Three icon boxes in a row (icon tile, two-word title, vague sentence, times three).
9. A pill badge above the headline ("New ✦ Now with AI").
10. Lucide icons by default. Use Phosphor, or a few hand-drawn glyphs.
11. Untouched shadcn or component-library defaults.
12. Fade-in or slide-in on scroll, count-up numbers, staggered word reveals. Content is on the page when it loads.
13. Cursor-following glows, spotlights, tilt cards, magnetic buttons.
14. Buttons that fade (opacity) on hover. Change color, border or background instead.
15. Inconsistent spacing. One spacing scale per project.
16. Em dashes in copy, or en dashes used as dashes.
17. Buzzwords: seamless, elevate, leverage, unlock, empower, robust, cutting-edge, next-gen, effortless, supercharge, revolutionize.
18. A serif italic accent word in a sans headline.
19. Space Grotesk with Instrument Serif.
20. Grain or noise over a gradient.

**Also never**
- Sparkle or star icons (the "AI" glyph). Glowing, pulsing or gradient dots and blobs. Grid-and-glow backgrounds.
- Fake browser traffic-light dots. Three-dot typing loaders: write "Loading…" instead.
- One phrase of the headline in the accent color.
- "AI-powered" or any claim the product can't back up. Invented testimonials, "Trusted by 10,000+ teams", logo walls, made-up ratings, stats like "99.9% satisfaction".
- Buttons that go nowhere, links to "#", forms that submit to nothing, placeholder images or lorem ipsum, stock people smiling at laptops.
- Everything centered, every corner the same big radius, a drop shadow on everything.

**Do**
- Look like the real software of that kind: an inbox looks like an inbox, a store like a store, a game like a game. Each project gets its own direction from its subject; never reuse one skin for everything.
- One accent color, kept for things you can press. Tinted shadows, not black at 30%.
- Sentence case for headings and buttons. Plain, specific copy in active voice: "Brake jobs done the same day, from $180" beats "Quality automotive solutions".
- Status as colored label text. Bullets as a short hairline or nothing.
- Real data that holds up: current dates, plausible numbers, real maps (Leaflet with OpenStreetMap), real photos of the real thing or none.
- Empty, loading and error states exist and read like a person wrote them.
- Keyboard: everything interactive works with Tab and Enter and shows a visible `:focus-visible` ring. Icon-only buttons have `aria-label`; inputs have labels, `name`, `autocomplete` and the right `type`; images have `alt`, `width` and `height`. Honor `prefers-reduced-motion`.
- Phones (390px wide): no sideways scroll, 16px side gutters, tap targets of 44px, nothing hidden under a floating button, `100dvh` not `100vh`, safe areas respected.
- Asymmetry is allowed. So is a page with no cards at all.

**Finish gate**
1. Check it with test_page on phone and desktop, and look at the screenshots.
2. Go down the Never list line by line against the code and the screenshots.
3. Fix everything in one batch, then check once more.
4. Cover the logo: could this belong to any of a thousand other products? If yes, it isn't finished.
5. If something can't be fixed now, say so plainly instead of claiming it passed.
