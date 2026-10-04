---
name: ui-design
description: Designing or building any interface (web page, app screen, dashboard) so it looks intentional, not templated.
---
# UI design

Decide before you build. Write down, in one line each: who uses this, the one thing they came to do, and the feeling it should give (calm, loud, technical, warm). Every choice after that serves those three lines.

**Layout**
- One clear focal point per screen. If everything is bold, nothing is.
- Use a spacing scale and stick to it: 4, 8, 12, 16, 24, 32, 48, 64. No random 13px gaps.
- Align to a grid. Left edges line up. Leave more empty space than feels necessary.
- Design the phone width first, then let it grow.

**Type**
- Two typefaces at most. One is often enough.
- Set a scale (for example 14, 16, 20, 28, 40) and use only those sizes.
- Body text 16px or larger, line height about 1.5, lines no longer than about 70 characters.
- Headings tighter (line height 1.1 to 1.2). Never center long paragraphs.

**Color**
- One accent color, used sparingly, on the things you can click. Neutrals do the rest.
- Check contrast: body text at least 4.5:1 against its background.
- Dark mode is not inverted light mode. Use dark greys, not pure black, and soften the accent.

**Components**
- Every interactive thing needs hover, focus, active and disabled states.
- Every data view needs loading, empty and error states. Design those, not just the happy path.
- Buttons say what they do: "Save changes", not "Submit".
- Tap targets at least 44px tall.

**Finish**
- Real content, never lorem ipsum. Real numbers, real names, plausible dates.
- Consistent corner radius and consistent shadow direction across the whole page.
- Motion is short (150 to 250ms) and only where it explains a change.
- Before calling it done, look at it at 375px, 768px and 1440px wide.

Also load the no-ai-slop skill before you finish any visual work.
