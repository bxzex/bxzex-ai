---
name: design-direction
description: Choosing a distinct visual direction for a brand or product instead of defaulting to a template look.
---
# Design direction

Templates happen when no one decided. Make decisions, write them down, then commit.

1. **Learn the brand.** Read any brief, README or copy. Ask for the audience and what the product does in one line. If missing, use the design-intake skill.
2. **Mood words.** Choose three that are specific and slightly unusual: "field notebook, dry, precise" instead of "modern, clean, professional". Add one anti-word the design must avoid.
3. **References.** Find 3 to 5 from outside the product's category (a map, a record sleeve, a hardware manual, a magazine). Use web_search and fetch_page. Note what you borrow from each: the grid, the paper color, the type voice.
4. **Make three directions.** For each write a short block:
   - **Name** and one sentence of feel.
   - **Palette**: background, surface, text, accent, with hex values.
   - **Type**: heading face, body face, scale, case and tracking.
   - **Layout idea**: for example a strict 12-column grid with huge numerals, or an asymmetrical two-column layout with a sticky label rail.
   - **Signature detail**: one repeatable thing (hairline rules, a stamped label, an odd crop).
   - **Risk**: what could go wrong.
5. **Commit to one.** Pick it with reasons tied to the audience and goal. Do not blend two. State what you will not do.
6. **Prove it.** Build the hero section only, screenshot it at 1440px and 375px, and check it against the mood words. Adjust, then roll the decisions into CSS variables (`--bg`, `--text`, `--accent`, `--font-display`).

**Pitfalls:** purple to blue gradients, centered hero with three feature cards, rounded cards with soft shadows everywhere, Inter on everything. If your direction could belong to any company, it is not a direction yet.
