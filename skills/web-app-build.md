---
name: web-app-build
description: Building a complete, working web app (SaaS, dashboard, tool, marketplace) end to end, with real data, real states and a live deploy, not a mockup.
---
# Building a web app end to end

Load no-ai-slop and ui-design for the look, and the skill for each layer as you reach it: nextjs-app or frontend-build, database-postgres, auth-login, payments-stripe, deploy-vercel, testing, accessibility.

**1. Start from the one job**
- Write one sentence: "This app lets [who] do [what] so that [result]." If you need two sentences, you have two apps. Build the first.
- List the main screens (usually 4 to 8): sign in, the home or list view, the detail view, the create or edit flow, settings. Write them in update_todos before any code.
- Name the main flow: the shortest path from landing to the result the user came for. Everything else serves it.

**2. Pick the stack, then stick to it**
- If the project already has a stack, use it. Do not add a second framework or router.
- Client app with a small API: Vite + React, a router, and a small Node API.
- Full-stack with server rendering, forms and API in one place: Next.js (see nextjs-app).
- Postgres for data, an auth library rather than hand-rolled login, Stripe only if the app takes money.
- Fewer dependencies is better. Each one needs a reason.

**3. Data model first**
- Write the tables before the screens: users, the main thing the app manages, what belongs to what, timestamps, a soft-delete or status column where needed.
- Every row that belongs to a user carries a `user_id` (or team id) and every query filters on it.
- Add indexes for the columns you filter and sort by. Write migrations as files, not manual edits.

**4. Build order**
1. Data and API: tables, migrations, endpoints, tested with `curl`.
2. The main flow end to end with real data, ugly is fine: sign in, create the main thing, see it in a list, open it, change it.
3. Everything else: settings, secondary screens, search, filters, billing.
4. Polish and design pass last, on screens that already work.

**5. Every screen has four states**
- Empty: says what goes here and offers the one action to fill it ("No invoices yet. Create your first invoice.").
- Loading: a skeleton shaped like the content, or "Loading…". Never a blank page.
- Error: says what failed and what to do, with a retry button. No raw stack traces or "Something went wrong".
- Filled: with realistic amounts of data, including very long names and 200 rows.

**6. Forms**
- Label every field, use the right `type`, `name` and `autocomplete`.
- Validate on the server always, and on the client for speed. Show the message next to the field: "Enter an email like name@example.com", not "Invalid input".
- Disable the submit button while sending and show the result. Keep what the user typed after an error.
- Optimistic updates where they help (toggles, checkboxes, reordering, deleting from a list): update the screen at once, roll back and show an error if the request fails. Skip them for payments and anything irreversible.

**7. Routing and links**
- Every screen has its own URL, and filters, tabs and selected items live in the URL so a refresh or a shared link lands in the same place.
- Real 404 page, redirect to sign in with a return path, back button that behaves.

**8. Account basics**
- Settings page: name, email, password change, plan and billing link if paid.
- Delete account that really deletes (or schedules deletion) the user's data, behind a confirmation that names what will be lost.
- Sign out works everywhere, including expired sessions.

**9. Security basics**
- Check permission on the server for every read and write. Hiding a button is not protection.
- Never trust the client: re-validate every body, id and price on the server; look up ownership by the signed-in user, not an id from the request.
- Secrets only in env vars, never in the repo or the browser bundle. Commit a `.env.example` with names and no values.
- Rate limit sign in, sign up, password reset and any expensive endpoint.
- Parameterized queries only. Escape or sanitize anything rendered as HTML.

**10. Seed data that looks real**
- A seed script with believable names, dates near today, plausible amounts and a mix of statuses. No "Test 1", "John Doe", lorem ipsum.
- One demo account so the app can be clicked through at once.

**11. Run it and click through it**
- Start the app, then use test_page on phone (390px wide) and desktop. Run the main flow with steps, for example: "click Sign up", "type #email a@b.com", "type #password ...", "click Create account", then create the main thing and open it.
- Read the console errors, sideways scroll and small tap target reports and fix all of them. Look at the screenshots of each state.
- Run the production build (`npm run build`), not only the dev server.

**12. Deploy and check live**
- Deploy (see deploy-vercel), set the env vars on the host, run migrations against the production database.
- Open the live URL with test_page and run the main flow once more. Confirm sign in, saving, and any emails or payments work there.

**Definition of done**
- [ ] The main flow works end to end on the live URL
- [ ] Every screen has real empty, loading and error states
- [ ] Forms validate on the server and show helpful errors
- [ ] Settings and delete account work
- [ ] Every write checks the user on the server; no secrets in the repo
- [ ] Seed data looks real; no placeholder text or dead buttons
- [ ] 390px wide has no sideways scroll; tap targets are 44px
- [ ] Production build passes with no console errors
- [ ] The no-ai-slop finish gate has been run on the screenshots and fixed
- [ ] Anything not finished or not checked is stated plainly in the final message
