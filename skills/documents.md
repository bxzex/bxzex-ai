---
name: documents
description: Creating PDF, Word, Excel or PowerPoint files with Python and checking that the result opens.
---
# Documents (PDF, DOCX, XLSX, PPTX)

1. **Use a virtual environment** so nothing pollutes the system:
   ```
   python3 -m venv .venv && . .venv/bin/activate
   pip install python-docx openpyxl python-pptx reportlab
   ```
   For HTML to PDF use `pip install weasyprint` (needs pango: `brew install pango` or `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`).
2. **Write one script** (`make_doc.py`) that builds the file from data, so it can be rerun after edits.

**PDF**
- Simple layouts: reportlab `SimpleDocTemplate`, `Paragraph`, `Table`, `getSampleStyleSheet()`.
- Styled pages: write HTML and CSS, then `weasyprint page.html out.pdf`. Set `@page { size: A4; margin: 20mm }`.

**Word**
```
from docx import Document
d = Document(); d.add_heading("Title", 1); d.add_paragraph("Text")
d.save("out.docx")
```
Use built-in styles ("List Bullet", "Heading 2") instead of manual bold text.

**Excel**
```
from openpyxl import Workbook
wb = Workbook(); ws = wb.active; ws.append(["Item", "Cost"])
ws["C2"] = "=SUM(B2:B10)"; wb.save("out.xlsx")
```
Keep formulas as formulas, set column widths, freeze the header row with `ws.freeze_panes = "A2"`.

**PowerPoint**
```
from pptx import Presentation
p = Presentation(); s = p.slides.add_slide(p.slide_layouts[1])
s.shapes.title.text = "Heading"; p.save("out.pptx")
```
One idea per slide, large text, at most 6 lines.

**Verify the output**
- File exists and is not empty: `ls -l out.*`.
- Reopen it in Python (`Document("out.docx")`, `load_workbook`, `Presentation`) to confirm it parses.
- PDF page count: `pdfinfo out.pdf` or `python -c "import pypdf;print(len(pypdf.PdfReader('out.pdf').pages))"`.
- Convert to check rendering when LibreOffice exists (`which soffice libreoffice`): `soffice --headless --convert-to pdf out.docx`. Convert the PDF to a PNG with `pdftoppm -png -r 60 out.pdf page` and look at it.

Pitfalls: fonts missing on the machine change the look, so use common ones. Never overwrite a file the user gave you; write to a new name.
