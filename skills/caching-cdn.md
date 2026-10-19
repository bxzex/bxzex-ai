---
name: caching-cdn
description: Setting HTTP cache headers and using a CDN so pages are fast and still update when they should.
---
# HTTP Caching and CDN

1. **See what you send now.** `curl -sI https://example.com/page | grep -iE 'cache-control|etag|age|x-vercel-cache|cf-cache-status|last-modified'`.
2. **Pick a rule per kind of file.**
   - Hashed assets (`app.3f9a1c.js`, images with a hash in the name): `Cache-Control: public, max-age=31536000, immutable`.
   - HTML pages that change rarely: `Cache-Control: public, max-age=0, s-maxage=300, stale-while-revalidate=600`. Browsers always recheck, the CDN keeps it 5 minutes and may serve a stale copy for 10 more while it refreshes.
   - API responses that are the same for everyone: `public, s-maxage=60, stale-while-revalidate=300`.
   - Per-user or private data: `Cache-Control: private, no-store`.
3. **Set the header.** In Next.js route handlers, set it on the `Response`; in `next.config.js` use `headers()`; on Vercel use the `headers` array in `vercel.json`; for Netlify use a `_headers` file.
4. **ETags.** Most servers add them for static files. A client sends `If-None-Match` and gets `304 Not Modified` with no body. Test: `curl -sI -H 'If-None-Match: "<etag>"' <url>` should return 304.
5. **Purge after a change.** Prefer new file names for assets. For HTML or API data, use the platform's purge or revalidate option (a revalidate path call, a tag purge, or the CDN dashboard) rather than waiting out the timer.
6. **Confirm the CDN is hitting.** Request twice and compare headers: first `MISS`, second `HIT`, and `age` above 0.

**Do not cache:** responses that set cookies or depend on login, checkout and form posts, anything with a token in the URL, error pages (a cached 500 sticks around).

**Pitfalls:** `Vary: Cookie` or a cookie header can make every request a miss; long `max-age` on an un-hashed file means users see old code for a year; testing in a browser with devtools "disable cache" on hides real behavior, so trust curl.
