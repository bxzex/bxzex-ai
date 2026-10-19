---
name: pdf-tools
description: Working with existing PDFs from the shell: reading text, merging, splitting, rotating, compressing, forms and images to PDF.
---
# PDF tools

Install if missing: macOS `brew install poppler qpdf ghostscript img2pdf`; Debian or WSL `sudo apt install poppler-utils qpdf ghostscript img2pdf`.

**Inspect**
- Pages and size: `pdfinfo file.pdf | grep -E "Pages|Page size|File size"`; `ls -lh file.pdf`.
- Text: `pdftotext -layout file.pdf out.txt`, then read_file. If the output is empty the PDF is scanned; use `ocrmypdf in.pdf out.pdf` (if installed) or tell the user.
- Pages to images: `pdftoppm -png -r 100 -f 1 -l 3 file.pdf page`.

**Merge, split, rotate (qpdf)**
- Merge: `qpdf --empty --pages a.pdf b.pdf -- merged.pdf`
- Pages 3 to 5: `qpdf in.pdf --pages . 3-5 -- part.pdf`
- Every page to its own file: `qpdf --split-pages in.pdf page-%d.pdf`
- Rotate all pages 90 degrees: `qpdf in.pdf --rotate=+90 -- out.pdf`
- Remove a password you know: `qpdf --password=PASS --decrypt in.pdf out.pdf`

**Compress (ghostscript)**
`gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=small.pdf in.pdf`
Use `/screen` for smallest, `/printer` for better quality. Compare sizes with `ls -lh`.

**Images to PDF**
`img2pdf *.jpg -o photos.pdf` (lossless), or `magick *.png out.pdf`.

**Fill forms**
Check for fields first: `python3 -c "import pypdf;print(pypdf.PdfReader('f.pdf').get_fields())"`. Fill with pypdf: `writer.update_page_form_field_values(page, {"name": "Ana"})` then write the file. Flat forms without fields need text placed at coordinates with reportlab and merged over the page.

**Rules**
- Never overwrite the original. Write to a new file name.
- After each operation run `pdfinfo` on the output and confirm the page count and size make sense.
- Look at one rendered page with read_file before saying the job is done.
