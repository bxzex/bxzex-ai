---
name: delegate-work
description: Deciding when to hand a self-contained research or search task to the delegate tool and how to write and merge it.
---
# Delegating Work

The delegate tool starts a helper that works alone and returns a report. It does not see your conversation.

**Good jobs to hand off**
- Reading many files or pages to answer one question ("which modules call the payment API?").
- Comparing several options by researching each (three hosting providers, four libraries).
- A long search where only the conclusion matters, not every step.

**Keep for yourself**
- Anything needing the user's answers, approvals or secrets.
- Edits to files the main task is also changing.
- Tiny lookups that one `search_files` call can answer.

**Write the task so a stranger could do it.** Include:
1. The goal in one sentence and why it matters.
2. Exact paths, URLs, names and versions. Say what folder to work in.
3. What is allowed: "read only, do not edit or run installs".
4. What to skip, so it does not repeat work you already did.
5. The output format: "return a table of file, line, reason, under 300 words" or "give a recommendation and the three strongest facts with source links".
6. How to prove it: ask for file paths and quoted lines, not impressions.

Example: "In /home/me/shop, find every place that reads process.env.STRIPE_KEY. Read only. Return a list of file:line and whether it runs on the server or in the browser. Ignore node_modules and .next."

**Helpers only look.** They can read, search, list, fetch pages and run read-only commands. They can't edit, install or ask the user, so have them report what should change and do the changes yourself.

**Several helpers at once.** Put 2 or 3 delegate calls in the same reply and they run side by side. Split by independent pieces (one per provider, one per folder) so no two repeat the same work.

**Merge results.**
- Check claims that matter yourself: open the cited file or page.
- If reports disagree, find out why before choosing.
- Combine into one answer for the user with sources, and say what was and was not verified.
- Use `update_todos` to track each delegated piece until its result is in.

**Pitfalls:** vague tasks ("look into the auth thing") give vague results; forgetting the helper cannot see earlier context; trusting a summary without spot-checking; delegating work and then redoing it yourself.
