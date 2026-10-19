---
name: auth-login
description: Adding user login to a web app using a hosted auth provider or secure cookie sessions.
---
# Adding Login

Never write your own crypto or token scheme. Pick one path.

**Path A: hosted auth provider (fastest, least risk).** Use a hosted service or a well-known library for your framework (Clerk, Auth0, Auth.js, Supabase Auth and similar). Follow its quickstart, put its keys in env vars, wrap the app in its provider, and protect routes with its middleware. Choose this unless the user needs full control or has no budget.

**Path B: your own sessions with passwords.**
1. Add a `users` table with `id`, `email` (unique, stored lowercase), `password_hash`, `created_at`.
2. Hash with argon2id (`npm i argon2`) or bcrypt with cost 12 or higher. Never store, log or email plain passwords. Never use plain SHA or MD5.
3. On login, look up by email, verify the hash, and return the same vague error ("wrong email or password") for both failures.
4. Create a random session id (`crypto.randomBytes(32).toString('hex')`), store it server side with the user id and an expiry, and set it as a cookie with `HttpOnly; Secure; SameSite=Lax; Path=/`.
5. Rate limit the login route and lock out after repeated failures.
6. Logout deletes the server session and clears the cookie.

**Protect routes.** Check the session on the server for every protected page and API route, not only by hiding links in the UI. Redirect to `/login` with a `next` parameter, and validate that `next` is a path on your own site.

**OAuth (sign in with Google or GitHub).** Register an app with the provider, set the exact redirect URI for local and production, store the client id and secret in env vars, and use a library to run the authorization code flow with `state` and PKCE. Match accounts by the provider's stable user id, not just email.

**Checklist:** HTTPS in production; secrets only in env; CSRF protection on cookie-based POST routes; password reset links are single use and expire in about an hour; test by opening a protected URL while logged out with `curl -i`, expecting a redirect or 401.
