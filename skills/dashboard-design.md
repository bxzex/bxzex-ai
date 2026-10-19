---
name: dashboard-design
description: Designing data-dense dashboards and admin screens that are fast to scan and honest about the numbers.
---
# Dashboard design

People open a dashboard to answer a question in seconds. Find the question first, then design for it.

1. **Write the top three questions** the viewer asks ("Are we on track today?", "What broke?", "Who needs follow up?"). Use ask_user if unknown.
2. **Show first.** Put the 3 to 5 numbers that answer those questions in a row at the top: big value, small label, change versus the previous period. Everything else is below, in order of importance.
3. **Tables over cards.** Rows with aligned columns are easier to compare than a grid of cards. Rules:
   - Right align numbers, left align text, one row height (36 to 44px).
   - `font-variant-numeric: tabular-nums` on every number.
   - Sortable column headers, sticky header, zebra or hairline row dividers (pick one).
   - Truncate long text with a tooltip, never wrap rows unevenly.
4. **Sparklines** next to a number give trend without a full chart. 80 by 24px, one line, no axes, last point marked. Use a full chart only when someone must read exact values.
5. **Status color sparingly.** Grey by default. Red for failing, amber for needs attention, green only where "good" is notable. Always pair color with a word or icon so it works for color blind users.
6. **Filters.** Date range and one or two key filters at the top, applied to the whole page, state kept in the URL (`?range=7d&team=sales`). Show the active filter as text.
7. **States.**
   - Loading: skeleton rows with the same height as real rows.
   - Empty: say why ("No orders in this range") and offer to widen the filter.
   - Error: say which panel failed, with a retry button, leave the others working.
8. **Honesty.** Label units and time zones. Show "updated 2 min ago". Never fake or round data to look better. Zero is shown as 0, not blank.

**Check.** Screenshot at 1440px. Can you answer each top question without scrolling or reading a legend? If not, move or cut things.
