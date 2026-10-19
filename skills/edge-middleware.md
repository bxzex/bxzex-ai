---
name: edge-middleware
description: Adding middleware that runs before requests for redirects, rewrites, geo or auth checks.
---
# Middleware Before the Request

Middleware runs ahead of your routes, on every matching request. Use it for quick decisions only.

1. **Create the file.** Next.js: `middleware.ts` at the project root (or `src/`). Newer versions may call it a proxy file, so check the version's docs. Vercel without Next.js: a `middleware.ts` at the root works with the platform helpers.
2. **Limit where it runs** with a matcher so static files and images skip it:
   ```
   export const config = { matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'] }
   ```
3. **Common jobs.**
   - Redirect: `return NextResponse.redirect(new URL('/new', req.url), 308)`.
   - Rewrite (URL stays the same): `return NextResponse.rewrite(new URL('/internal', req.url))`.
   - Auth gate: if the session cookie is missing on `/dashboard/*`, redirect to `/login`. This is a first filter only; still verify the session inside the page or API route.
   - Geo: read the country header your host provides (on Vercel `x-vercel-ip-country`) and send EU visitors to a notice or a local language page.
   - Add headers: set them on the `NextResponse.next()` response.
4. **Keep it fast.** No database calls, no big libraries, no slow fetches. Do cheap checks on cookies, headers and the path. The edge runtime lacks many Node APIs (`fs`, most native modules).
5. **Avoid loops.** A redirect from `/login` to `/login` or a rewrite that matches itself will hang. Exclude the target path in code.
6. **Test locally.** Run `npm run dev`, then:
   - `curl -sI localhost:3000/dashboard` should show `307` and a `location` header when logged out.
   - `curl -sI -H 'cookie: session=abc' localhost:3000/dashboard` should pass through.
   - Fake a country with `-H 'x-vercel-ip-country: DE'`.

**Pitfalls:** a matcher that is too wide slows the whole site; middleware errors take every page down, so wrap risky code in try/catch and fail open or closed on purpose; cached redirects (301) stick in browsers, so use 307 or 308 while testing.
