---
name: design-system
description: Setting up a small design system (color, type, spacing, radius, shadow tokens, dark mode, component states) for a web project.
---
# Design system

A design system here means one CSS file of variables and one doc that explains them. Keep it small.

1. **Look first.** Search the project for existing colors and sizes: `grep -rhoE "#[0-9a-fA-F]{3,6}|[0-9]+px" src | sort | uniq -c | sort -rn | head -40`. Reuse what is already common.
2. **Create `tokens.css`** and import it before every other stylesheet:
   ```
   :root {
     --bg: #faf9f6;  --surface: #ffffff;  --text: #1b1b1b;  --muted: #666660;
     --border: #e3e1da;  --accent: #1f5f8b;  --accent-text: #ffffff;
     --danger: #b3261e;  --ok: #1e7a46;
     --font-body: system-ui, sans-serif;  --font-display: Georgia, serif;
     --step--1: 0.875rem; --step-0: 1rem; --step-1: 1.25rem;
     --step-2: 1.75rem;   --step-3: 2.5rem;
     --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
     --space-6: 24px; --space-8: 32px; --space-12: 48px;
     --radius: 8px;
     --shadow: 0 1px 2px rgb(0 0 0 / 0.08), 0 4px 12px rgb(0 0 0 / 0.06);
   }
   ```
3. **Dark mode** by overriding only the color tokens:
   ```
   @media (prefers-color-scheme: dark) {
     :root { --bg:#14161a; --surface:#1c1f24; --text:#ecebe8; --muted:#a2a4a8; --border:#2c3037; --accent:#6fb1e0; --accent-text:#0b1620; }
   }
   ```
   Also support a manual `[data-theme="dark"]` selector if the site has a toggle.
4. **Use tokens only.** Components read `var(--accent)`, never a raw hex. Search for leftovers: `grep -rnE "#[0-9a-fA-F]{6}" src --include=*.css | grep -v tokens.css`.
5. **Define states** for each component: default, hover, focus-visible (visible outline using `--accent`), active, disabled, plus loading, empty and error for data views.
6. **Check contrast** for every text and background pair, in both themes: 4.5:1 for body text, 3:1 for large text and borders on inputs.
7. **Document it** in `DESIGN.md`: a table of tokens with their purpose, the type scale, spacing rules, and a "do and do not" list of five lines. Keep the file short enough that someone reads it.

Pitfalls: too many near-identical greys, a different radius per component, shadows with heavy blur, adding tokens nobody uses. Delete unused tokens.
