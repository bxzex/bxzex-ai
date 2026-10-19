---
name: slide-decks
description: Building PowerPoint decks with python-pptx: one idea per slide, layouts, images, speaker notes and PDF export.
---
# Slide decks

Install: `pip install python-pptx`. PDF export needs LibreOffice.

**Plan first**
1. Ask who the audience is, how long the talk is, and the one thing they should remember.
2. Write the outline as one sentence per slide. Each slide gets one idea, and its title is the point ("Signups doubled in March"), not a label ("Results").
3. Roughly one slide per minute. Cut anything that does not serve the one thing.

**Build**
```python
from pptx import Presentation
from pptx.util import Inches, Pt
p = Presentation()
p.slide_width, p.slide_height = Inches(13.333), Inches(7.5)   # 16:9
s = p.slides.add_slide(p.slide_layouts[5])                      # title only
s.shapes.title.text = "Signups doubled in March"
s.shapes.add_picture("chart.png", Inches(1), Inches(1.6), width=Inches(11))
tb = s.shapes.add_textbox(Inches(1), Inches(6.4), Inches(11), Inches(0.6))
tb.text_frame.text = "Source: internal analytics"
s.notes_slide.notes_text_frame.text = "Say: what changed, and why."
p.save("deck.pptx")
```
Built-in layouts: 0 title, 1 title and content, 5 title only, 6 blank. For a custom look, start from a template file with `Presentation("template.pptx")`.

**Design rules**
- Max about 30 words per slide. Body text 24pt or larger, titles 36pt or larger.
- One font family, two colors plus one accent, same margins on every slide.
- Prefer a chart or photo to bullets. Make charts with matplotlib at 200 dpi and label the key point directly on them.
- Speaker notes hold the details, the slide holds the headline.

**Export and check**
- `soffice --headless --convert-to pdf --outdir out deck.pptx`
- `pdftoppm -png -r 50 out/deck.pdf out/s` then view a few pages with read_file. Look for overflowing text and cropped images.
- Report slide count and file path.
