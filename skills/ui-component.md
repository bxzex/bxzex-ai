---
name: ui-component
description: Building a single UI component well (button, modal, navbar, card, table, form) with all states, keyboard support and responsive behavior.
---
# Building one component

1. **Read the project first.** Find the framework and existing components: `list_files src/components`, check for tokens (CSS variables, a Tailwind config). Match their naming, file layout and styling method. Do not add a new library for one component.
2. **Define the API before the markup.** Write the props: the few that matter (`variant`, `size`, `disabled`, `onClick`, `children`), sensible defaults, and pass through the rest (`...props`) so `aria-*`, `id` and `className` work.
3. **Use the right element.** A button is `<button type="button">`, a link is `<a href>`, a modal is `<dialog>` or has `role="dialog" aria-modal="true"` with `aria-labelledby`, a nav is `<nav aria-label="Main">`, a table is a real `<table>` with `<th scope>`. No `div onClick`.
4. **Build every state.** Default, hover, `:focus-visible`, active, disabled, loading, error (where it applies). Disabled uses the `disabled` attribute, not only styling.
5. **Keyboard.**
   - Buttons: Enter and Space.
   - Modal: focus moves in on open, Tab stays inside, Escape closes, focus returns to the trigger.
   - Menus and tabs: arrow keys, Home and End.
   - Focus ring always visible, at least 2px.
6. **Responsive.** Test at 375px. Tables get a horizontal scroll wrapper or stack as rows. Navbars collapse behind a labelled button. Tap targets 44px.
7. **Keep the DOM lean.** One root element, no wrapper divs that exist only for styling. Use gap and grid instead of spacer elements.
8. **Show it working.** Add a small usage example or story with real text, render it, and check each state by hand. Run the project's lint and type check (`npm run lint`, `npx tsc --noEmit`).

**Pitfalls:** hard-coded colors instead of tokens, missing `type="button"` inside forms (it submits), z-index wars (use one scale), animations that ignore `prefers-reduced-motion`.
