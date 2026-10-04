---
name: frontend-build
description: Writing a web page or small site as code (HTML, CSS, JavaScript) that works when the file is opened.
---
# Building a web page

Load ui-design first for the look, and no-ai-slop before you finish.

**Structure**
- For a single page, write one self-contained `.html` file with the CSS and JavaScript inside it, so it opens with a double click.
- Start with `<!doctype html>`, `<meta charset="utf-8">`, and `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Use real elements: `header`, `nav`, `main`, `section`, `footer`, `button` for actions, `a` for links.
- Give the page a real `<title>`.

**CSS**
- Put colors, spacing and fonts in variables on `:root` and use only those.
- `box-sizing: border-box` on everything.
- Layout with flexbox and grid. No fixed pixel widths on containers; use `max-width` and let it shrink.
- Fluid sizes with `clamp()`. Media queries for the phone layout.
- Nothing should scroll sideways at 375px wide.

**JavaScript**
- Only what the page needs. No framework for a static page.
- Every button and link must do something real. If a feature is not built, leave the control out.
- Forms: label every field, validate, and show a clear message on success and on error.

**Quality**
- Images get `alt` text and set dimensions so the page does not jump while loading.
- Keyboard works: tab order makes sense and focus is visible.
- Respect `prefers-reduced-motion`.
- No lorem ipsum, no "#" links, no placeholder images.

**Before saying it is done**
Write the file, then open it (`open page.html`) and tell the user where it is. If you cannot check something yourself, say which part is unchecked.
