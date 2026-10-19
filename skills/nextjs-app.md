---
name: nextjs-app
description: Creating and working in a Next.js App Router project: routes, server and client components, data, API handlers, env vars and common errors.
---
# Next.js (App Router)

**Create**
```
npx create-next-app@latest my-app --ts --app --eslint --no-tailwind --src-dir --import-alias "@/*"
cd my-app && npm run dev
```
Dev server is at http://localhost:3000. Check it with `curl -s localhost:3000 | head`.

**Routes** are folders under `src/app`:
- `app/page.tsx` is `/`
- `app/about/page.tsx` is `/about`
- `app/blog/[slug]/page.tsx` is `/blog/anything`, read via `params`
- `layout.tsx` wraps its folder, `loading.tsx` and `error.tsx` give loading and error states, `not-found.tsx` handles 404.

**Server vs client components**
- Components are server components by default. They can be `async`, read files, query a database and use secrets. They send no JavaScript to the browser.
- Add `"use client"` at the top of a file only when you need state, effects, event handlers or browser APIs. Keep client components small and leaf-level.
- You cannot import a server-only module into a client component.

**Data fetching.** In a server component, just `await`:
```
const res = await fetch("https://api.example.com/items", { next: { revalidate: 60 } });
const items = await res.json();
```
Check the installed version's docs for caching defaults, they have changed between releases.

**API route handlers**: `app/api/items/route.ts`
```
export async function GET() { return Response.json({ ok: true }); }
export async function POST(req: Request) { const body = await req.json(); return Response.json(body, { status: 201 }); }
```
Test with `curl -s localhost:3000/api/items` and `curl -s -X POST -d '{"a":1}' -H 'content-type: application/json' localhost:3000/api/items`.

**Env vars.** Put them in `.env.local` (git-ignored). Only names starting with `NEXT_PUBLIC_` reach the browser. Restart the dev server after changing them.

**Build.** `npm run build && npm start`. Always build before saying it works; dev mode hides errors.

**Common errors**
- "You're importing a component that needs useState": add `"use client"`.
- Hydration mismatch: server and browser rendered different HTML (dates, random values, `window` checks). Move that logic into an effect.
- `Module not found`: check the path alias and file case.
- "Dynamic server usage" at build: the page reads cookies or headers, mark it dynamic.
- Images from other domains need `images.remotePatterns` in `next.config`.
