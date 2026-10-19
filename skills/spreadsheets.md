---
name: spreadsheets
description: Reading, building and cleaning Excel and CSV files with openpyxl and pandas without losing data.
---
# Spreadsheets

Install: `pip install pandas openpyxl`.

**Look before you touch**
- `head -5 file.csv` and `file file.csv` for encoding. Try `pd.read_csv(p, encoding="utf-8-sig")`, then `latin-1`.
- Excel sheets: `pd.ExcelFile("f.xlsx").sheet_names`.
- Messy files: `pd.read_excel(p, header=None, dtype=str)` first, find the real header row, then reread with `header=N`. Keep IDs, phone numbers and zip codes as strings so leading zeros survive.

**Clean**
```python
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.dropna(how="all").drop_duplicates()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print(df.isna().sum(), len(df))
```
Print row counts before and after each step. Never delete rows silently, write rejects to `rejected.csv`.

**Write with formatting and formulas (openpyxl)**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, Reference
wb = Workbook(); ws = wb.active; ws.title = "Sales"
ws.append(["Item", "Qty", "Price", "Total"])
ws.append(["Widget", 2, 10, "=B2*C2"])
for c in ws[1]: c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDDDDD")
ws.freeze_panes = "A2"; ws.column_dimensions["A"].width = 24
ws["C2"].number_format = '"$"#,##0.00'
ch = BarChart(); ch.add_data(Reference(ws, min_col=4, min_row=1, max_row=2), titles_from_data=True)
ws.add_chart(ch, "F2"); wb.save("out.xlsx")
```
Use formulas as strings starting with `=` so the sheet stays live. Extra sheets: `wb.create_sheet("Summary")`, or `pd.ExcelWriter` with several `to_excel` calls.

**Never lose data**
- Never overwrite the original, save to a new name.
- `load_workbook(p)` keeps formulas, `data_only=True` shows cached values but saving it destroys formulas.
- openpyxl drops some features (pivot tables, macros). Warn the user and work on a copy.
- Verify by reloading the output and comparing row counts.
