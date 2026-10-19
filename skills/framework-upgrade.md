---
name: framework-upgrade
description: Upgrading a framework to a new major version (Next.js, React, Vite) safely in a branch with codemods and tests.
---
# Upgrading a Framework Major Version

1. **Start clean.** `git status` should be empty and the current build and tests should pass. If they do not, note it so you do not blame the upgrade. Create a branch: `git switch -c upgrade-<framework>-<version>`.
2. **Read the notes.** Use `web_search` or `fetch_page` for "<framework> <new version> upgrade guide" and the changelog on the official site. Write the breaking changes that touch this project into a short todo list. Check the required Node version: `node -v`.
3. **Check dependencies.** `npm outdated`. Find plugins and libraries that must move too (UI kits, eslint config, types packages). Peer dependency warnings are hints.
4. **Run the official codemod or upgrade tool** when one exists, for example `npx @next/codemod@latest upgrade` or `npx vite` migration docs. Review the diff: `git diff --stat` then read the changes.
5. **Bump versions** if not done: `npm install next@latest react@latest react-dom@latest` (use exact versions the guide names). Delete `node_modules` and the lock file only if installs conflict, and tell the user first.
6. **Fix build errors in order.** Run `npm run build`, fix the first error, rebuild. Then `npx tsc --noEmit`, then `npm run lint`. Do not silence errors with `any` or `// @ts-ignore` just to pass.
7. **Run tests and use the app.** `npm test`, then `npm run dev` and click through the main flows: login, a form, a dynamic route, an API call. Check the browser console for new warnings.
8. **Compare production behavior.** Build, start (`npm start`), and curl key pages for status 200.
9. **Commit in steps** (tool run, dependency bump, fixes) so a bad step can be reverted. Do not merge or deploy without telling the user.

**Pitfalls:** upgrading several majors at once (go one major at a time); changed defaults such as caching or routing behavior that only show at runtime; a CI Node version older than the new minimum; forgetting to update the lockfile in the commit.
