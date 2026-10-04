---
name: data-analysis
description: Making sense of a spreadsheet, CSV or set of numbers and reporting what it shows.
---
# Data analysis

**Look before you calculate**
- Open the file and read the first rows and the column names. `head -5 file.csv`
- Count rows. Check each column: what type, how many blanks, what range, any obvious junk.
- Find out what one row represents. Most wrong answers come from getting this wrong.

**Clean, and say what you cleaned**
- Blanks, duplicates, mixed date formats, numbers stored as text, stray currency signs and commas.
- Never silently drop rows. Report how many you removed and why.

**Answer the actual question**
- Restate it in one line. Decide which columns answer it.
- Start with simple counts, sums, averages and groupings. Simple usually suffices.
- Use the median when a few huge values would skew the average.
- Compare like with like: same period, same units, per-customer or per-day where totals mislead.

**Be honest about it**
- Small samples prove little. Say the count next to every percentage.
- Two things moving together does not mean one causes the other.
- If the data cannot answer the question, say so.

**Report**
- The answer first, in one sentence with the number.
- Then the two or three figures that support it.
- Then what is uncertain or missing.
- Do the arithmetic with a tool (Python or the shell), not in your head, and show the command.
