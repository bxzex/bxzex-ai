---
name: security-check
description: Checking a website, app or script the user owns for common security mistakes.
---
# Security check

This is for the user's own code and systems. Review, do not attack.

**Secrets**
- No API keys, passwords or tokens in code, in git history or in anything sent to the browser. Search: `grep -rn -iE "api[_-]?key|secret|password|token" .`
- `.env` is in `.gitignore`. Keys shipped to the browser are public, whatever the variable is called.

**Input**
- Every value from a user, URL, form, file or webhook is untrusted.
- Database queries use parameters, never strings glued together.
- Output shown in HTML is escaped. No `innerHTML` with user text.
- File paths from users cannot escape their folder (`../`).
- User input never reaches a shell command.

**Access**
- Every endpoint checks who is asking and whether they may see that specific record, on the server. Hiding a button is not a check.
- Admin pages are not reachable just by guessing the URL.
- Passwords are hashed with bcrypt, scrypt or argon2. Never stored or logged in plain text.
- Sessions expire. Cookies are `HttpOnly`, `Secure`, `SameSite`.

**Transport and config**
- HTTPS everywhere. No mixed content.
- Rate limits on login, signup, password reset and anything that sends email or SMS.
- Error pages do not leak stack traces or queries.
- Dependencies are current: `npm audit`, `pip list --outdated`.
- Uploads: check type and size, store outside the web root, never execute.

Report each finding with where it is, how it could be abused in one sentence, and the fix. Rank by how bad it is. Say what you did not check.
