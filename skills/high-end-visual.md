---
name: high-end-visual
description: Making a page feel expensive and considered, or finding why an existing one looks cheap.
---
# High-end visual design

Expensive looks come from restraint. Remove things until what is left is clearly chosen.

**Palette**
- Two or three colors total: a near-white or near-black base, one text color, one accent. Tint your greys toward the accent hue instead of using pure #808080.
- Use the accent on one or two things per screen. Skip gradients on backgrounds and text.

**Type**
- Pair one display face with one plain text face, or use a single family in two weights. Pick real fonts (a good serif for headings, a clean sans for body) from Google Fonts or Fontsource.
- Use a big jump in scale: headline 56 to 96px, body 16 to 18px. Small caps labels at 12px with letter spacing 0.08em work for metadata.
- Tight headline tracking (-0.02em), line height 1.05 to 1.15. Body at 1.5 to 1.6.

**Space**
- Sections get 96 to 160px of vertical padding on desktop. Cap text width near 65 characters.
- Fewer elements per section: one heading, one sentence, one action.

**Image**
- One strong photo or illustration per page, large, cropped with intent. Real photography beats stock icons and 3D blobs.
- Give images a consistent aspect ratio and a slow, short fade-in at most.

**Depth**
- A soft two-layer shadow (for example `0 1px 2px rgba(0,0,0,.06), 0 12px 32px rgba(0,0,0,.08)`), or a 1px hairline border in a slightly lighter or darker tone. Never both heavy.
- Radius consistent: one value for cards, one for buttons.

**What makes a site look cheap**
- Five or more colors, rainbow gradients, heavy drop shadows.
- Default system fonts for headings, centered body paragraphs.
- Icon grids with identical cards, stock photos of handshakes.
- Tight padding, text touching edges, mixed radii.
- Animations on everything.

**Check**
1. Screenshot at 1440px and squint. Is there one obvious focal point?
2. Count colors and font sizes in the CSS. Cut to the scale above.
3. Remove one element from every section, then judge again.
