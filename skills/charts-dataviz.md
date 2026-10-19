---
name: charts-dataviz
description: Turning data into a clear chart, picking the right type, and saving it as an image or an HTML page.
---
# Charts and data visualization

1. **Know the question.** Write one sentence: "Show how sales changed by month." The chart must answer that sentence at a glance.
2. **Pick the type from the question.**
   - Change over time: line chart (bar if few periods).
   - Compare categories: horizontal bar, sorted by value.
   - Part of a whole: stacked bar, or a pie only for 2 to 4 slices.
   - Relationship between two numbers: scatter plot.
   - Distribution: histogram or box plot.
   - Never 3D. Never dual y-axes unless the user insists.
3. **Check the data first.** Load it, print `df.head()`, `df.describe()`, look for nulls and wrong types. Sort dates properly.
4. **Plot it.**
   ```
   python3 -m venv .venv && . .venv/bin/activate && pip install matplotlib pandas
   ```
   ```
   import matplotlib.pyplot as plt
   fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
   ax.plot(x, y, color="#0072B2", linewidth=2)
   ax.set_title("Monthly sales, 2025", loc="left")
   ax.set_xlabel("Month"); ax.set_ylabel("Sales (USD)")
   ax.spines[["top", "right"]].set_visible(False)
   fig.tight_layout(); fig.savefig("sales.png"); fig.savefig("sales.svg")
   ```
   For interactive output use plotly: `fig.write_html("chart.html")`.
5. **Label like a person will read it.** Title says the finding. Axes have units. Label lines directly instead of a far-away legend when you can. Start bar charts at zero.
6. **Colors.** Use a colorblind-safe palette: `#0072B2` blue, `#E69F00` orange, `#009E73` green, `#D55E00` vermillion, `#CC79A7` pink, `#999999` grey. Use one color and grey for emphasis. Do not rely on red versus green.
7. **Check the result.** Open the PNG with the image tool if you have one, or at least confirm `ls -l sales.png` is not empty. Look for overlapping tick labels (rotate or switch to horizontal bars), cut-off text, and unreadable font size (use 11pt or more).

Pitfalls: too many series (keep to 5), rainbow colormaps, truncated axes that exaggerate change, forgetting to say where the data came from. Put the source in a small note under the chart.
