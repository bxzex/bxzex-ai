---
name: component-libraries
description: Using a copy-in component library such as shadcn with Tailwind, including setup, adding components and theming.
---
# Copy-In Component Library (shadcn style)

These libraries copy component source into your repo, so you own and edit the files. They build on Tailwind and unstyled accessible primitives.

1. **Prereqs.** A React project with Tailwind and a path alias (`@/*` in `tsconfig.json`). Confirm: `ls tailwind.config.* components.json 2>/dev/null` and check the Tailwind major version, since setup differs between v3 and v4.
2. **Init.** `npx shadcn@latest init`. Answer the prompts (base color, CSS variables yes). It writes `components.json`, a `cn()` helper in `lib/utils.ts`, and theme variables in your global CSS.
3. **Add components one at a time.** `npx shadcn@latest add button card dialog input`. Files land in `components/ui/`. Import them: `import { Button } from '@/components/ui/button'`. Add only what you use.
4. **Theme with CSS variables.** Colors live in the global CSS as `--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--radius`, with a `.dark` block for dark mode. Change those values and every component follows. Pick a real brand color and a custom radius rather than shipping the defaults untouched.
5. **Variants.** Edit the `cva` variants in a component file to add your own (`variant="brand"`). Edit the file directly; it is your code.
6. **Compose, do not fork.** Build page-level pieces (a `PricingCard`) from the base components in a separate folder. Pass `className` for one-off tweaks and merge with `cn()`.
7. **Do not fight the defaults.** If you are overriding most of a component with long class strings, stop and either change the variable or edit the component once. Do not stack `!important`.
8. **Updates.** Re-running `add` overwrites your edits, so check `git diff` before accepting. Use `npx shadcn@latest diff` if available.

**Check:** `npm run build` passes, tab through each dialog and menu with the keyboard, and toggle dark mode to confirm text is readable.

**Pitfalls:** missing `'use client'` on interactive components in Next.js server files; forgetting the Tailwind `content` paths so styles do not appear; mixing two icon sets.
