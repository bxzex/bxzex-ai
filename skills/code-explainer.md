---
name: code-explainer
description: Making sense of an unfamiliar codebase: find entry points, map modules, trace one request, and write a short overview.
---
# Explaining a codebase

Read first, then write. Do not guess from folder names alone.

1. **Orient.** `list_files .`, then read README, package.json, pyproject.toml, go.mod or Cargo.toml. Note the language, framework, scripts and dependencies. `git log --oneline | head -15` shows what changed lately.
2. **Size it.** `find . -type f -not -path "*/node_modules/*" -not -path "./.git/*" | sed 's/.*\.//' | sort | uniq -c | sort -rn | head` and `wc -l` on the biggest folders.
3. **Find entry points.**
   - Web: `src/main.*`, `index.*`, `app/`, `pages/`, `server.*`, `cmd/`.
   - Scripts: the `scripts` section, `Makefile`, `Dockerfile` CMD.
   - Routes: `grep -rnE "app\.(get|post)|router\.|@app\.route|path\(" src | head -30`.
4. **Map modules.** For each top-level folder write one line: what it owns and what it depends on. Find who uses what: `grep -rn "from './db'" src | head`.
5. **Trace one request end to end.** Pick a single action ("user signs up" or "load dashboard"). Follow it: UI event or HTTP route, handler, validation, business logic, database call or external API, response, render. Write each hop with `file:line`. Use search_files for each function name.
6. **Find the data.** Look for schema files, migrations, models and `.env.example` to list config and external services.
7. **Note risks and oddities.** Dead code, missing tests (`ls tests`), TODO count (`grep -rn TODO . | wc -l`), anything surprising.
8. **Write the overview** (under 400 words):
   - What it is in one sentence.
   - How to run it.
   - Directory map with paths.
   - The traced request as a numbered list.
   - Where to start for common changes.
   - Open questions you could not answer.

Only state what you read. Mark guesses as guesses. Offer to save it as `ARCHITECTURE.md`.
