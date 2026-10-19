---
name: word-docs
description: Creating, reading and editing Word (.docx) files with python-docx, and converting them with LibreOffice.
---
# Word documents

Install: `pip install python-docx`. Converting needs LibreOffice (`soffice`).

**Create**
```python
from docx import Document
from docx.shared import Pt, Inches
d = Document()
d.styles["Normal"].font.name = "Calibri"
d.styles["Normal"].font.size = Pt(11)
d.add_heading("Report title", 0)
d.add_heading("Section", level=1)
d.add_paragraph("Body text.")
d.add_paragraph("Item", style="List Bullet")
t = d.add_table(rows=1, cols=3); t.style = "Light Grid Accent 1"
for c, h in zip(t.rows[0].cells, ["Name", "Qty", "Price"]): c.text = h
r = t.add_row().cells; r[0].text, r[1].text, r[2].text = "Widget", "2", "$10"
d.add_picture("chart.png", width=Inches(5.5))
d.add_page_break()
d.save("report.docx")
```
Use built-in styles (Heading 1, List Number, Title) so the navigation pane and table of contents work. Do not fake headings with bold text.

**Read and edit an existing file**
1. Copy it first: `cp in.docx work.docx`.
2. Print structure: `for p in Document("work.docx").paragraphs: print(p.style.name, "|", p.text)`. Tables are in `doc.tables`.
3. Replace text by editing `run.text` inside each paragraph, not `paragraph.text`, which drops formatting. Text split across runs needs joining the runs carefully.
4. Save to a new name and reopen it to confirm it loads.

**Convert**
- To PDF: `soffice --headless --convert-to pdf --outdir out/ report.docx`
- Old .doc to .docx: `soffice --headless --convert-to docx file.doc`
- On macOS the binary may be `/Applications/LibreOffice.app/Contents/MacOS/soffice`.

**Check.** Convert to PDF, then `pdftoppm -png -r 80 -f 1 -l 1 report.pdf page` and view the image to see the real layout. Tracked changes, headers, footers and comments need extra care, so tell the user if the file has them.
