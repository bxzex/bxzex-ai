---
name: design-from-image
description: Turning a screenshot or mockup image into working code that matches it, with a side by side check.
---
# Design from an image

1. **Look at the image.** Use read_file on the image path so you can see it. If it is a PDF, convert a page first: `pdftoppm -png -r 110 file.pdf page`. Note the overall layout before details.
2. **Extract the palette.** Eyeball the main colors, then confirm hex values when possible:
   `python3 -c "from PIL import Image; im=Image.open('ref.png').convert('RGB'); print(im.getpixel((10,10)))"` for specific points, or `convert ref.png -colors 8 -unique-colors txt:-` with ImageMagick. Write them as CSS variables: background, surface, text, muted text, accent, border.
3. **Identify type.** Serif or sans, weights, rough sizes relative to each other. Pick the nearest Google Font. Note heading, body and label sizes in a scale.
4. **Measure spacing.** Find the base unit (often 8px). Note the content max width, column count, gutter, section padding, card padding, radius. Get pixel sizes with `identify ref.png` and scale from the image width.
5. **Map the layout.** Sketch the structure as nested boxes in your head: header, hero (two columns?), sections, footer. Build semantic HTML first, then style.
6. **Build.** Start with variables and layout, then type, then details like shadows and borders. Use real text from the image.
7. **Compare.** Screenshot your result at the same width as the reference: `npx playwright screenshot --viewport-size=1440,900 http://localhost:5173 out.png`. Read both images, then list the differences (spacing, size, color, alignment). Fix the biggest ones first. Repeat twice.

**Pitfalls:** guessing colors from memory, ignoring the mobile layout (design it sensibly if the image shows only desktop), copying logos or photos you do not have rights to (use placeholders and say so), matching pixels at the cost of accessibility (keep contrast 4.5:1 and real focus states).
