---
name: connect-apps
description: Using the user's own apps (Gmail, Calendar, Slack, GitHub, Notion, Drive, Sheets, Instagram, Stripe and 1,600 more) through the composio tools.
---
# Connect and use apps

This only works when /mcp shows composio connected. If it doesn't, tell the user to add it (see the end of this skill).

**Which apps exist**
- The full list is in `~/.bxzex-ai/connectors.txt`: one line per app with its slug, what it does and how many tools it has, grouped by category.
- Find one with search_files: pattern `(?i)notion`, path `~/.bxzex-ai/connectors.txt`. For "what can I connect for email?", search the category: pattern `(?i)^## email`, then read that part.
- Never invent an app slug or a tool name. Look it up.

**Doing a task in an app**
1. Call `composio__COMPOSIO_SEARCH_TOOLS` with what you want to do in plain words, like `{"queries": [{"use_case": "read my latest 5 emails in gmail"}]}`. It returns the right tools, a step plan and known pitfalls. Follow the plan.
2. If it says the app isn't connected, call `composio__COMPOSIO_MANAGE_CONNECTIONS` for that toolkit. It returns a link. Give the link to the user, ask them to open it and sign in, then call `composio__COMPOSIO_WAIT_FOR_CONNECTIONS` if you have it, or wait for them to say done. A connection is kept for next time.
3. If you need the exact inputs of a tool, call `composio__COMPOSIO_GET_TOOL_SCHEMAS` with its slug.
4. Run it with `composio__COMPOSIO_MULTI_EXECUTE_TOOL`. The user is asked before anything runs. You can send several independent calls at once.
5. Read the result and answer with the parts that matter: names, dates, amounts, links. Don't paste raw JSON at them.

**Rules**
- Read before you write: list or fetch first, then send, post, delete or pay only when they asked for it.
- For anything that sends, posts, deletes, pays or invites, say exactly what will happen first (to whom, what text, what amount).
- One app at a time unless the task needs more. Don't connect apps they didn't ask about.
- If a call fails with an auth error, reconnect that app with MANAGE_CONNECTIONS and try once more.
- Big outputs: ask for fewer items (limit 5 or 10) instead of everything.

**Adding composio**
They need a Composio account and a session address with its key. With those, `/mcp add composio <url> x-api-key:<key>` saves it on this computer only, and it connects the next time the app opens.
