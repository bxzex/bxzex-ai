---
name: firewall-security-headers
description: Hardening a website with security headers, rate limiting and bot protection, then checking with curl.
---
# Security Headers, Rate Limits and Bots

1. **Look first.** `curl -sI https://example.com | grep -iE 'strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy'`.
2. **Add these headers** (in `next.config.js` `headers()`, `vercel.json`, a Netlify `_headers` file, or your server):
   - `Strict-Transport-Security: max-age=31536000; includeSubDomains` (only once HTTPS works everywhere; add `preload` later if you want).
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY` (or `SAMEORIGIN` if you embed your own pages). The modern form is CSP `frame-ancestors 'none'`.
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Permissions-Policy: camera=(), microphone=(), geolocation=()` (list only what you use).
3. **Content-Security-Policy.** Start in report-only mode: `Content-Security-Policy-Report-Only: default-src 'self'; img-src 'self' data: https:; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'`. Open the site, read console violations, add the exact hosts you need (analytics, fonts, payment scripts), then switch to the enforcing header. Avoid `'unsafe-inline'` for scripts; use nonces if you must have inline code.
4. **Rate limiting.** Limit login, signup, password reset, contact forms and any route that costs money. Use the platform firewall rules if available, or a counter keyed by IP in Redis or the database, for example 10 requests per minute. Return `429` with a `Retry-After` header.
5. **Bot protection.** Add a honeypot field to forms, a challenge widget (Turnstile or similar) on signup and contact, and block obvious bad user agents at the firewall. Do not block search engine crawlers you want.
6. **Verify.** Re-run the curl command. Hammer a limited route: `for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code} " https://example.com/api/login -X POST; done` and expect 429 near the end.
7. **Scan.** Run a free header checker or `npx observatory-cli example.com` for a score.

**Pitfalls:** an overly strict CSP breaks the site silently, so test every page type; HSTS cannot be undone quickly, so confirm all subdomains support HTTPS first; limits keyed only on IP hurt users behind shared networks.
