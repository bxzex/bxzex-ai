---
name: github-cli
description: Using the gh command line tool to create repos, push code, open pull requests, publish releases and turn on GitHub Pages.
---
# GitHub CLI

Install: `brew install gh` on macOS, `sudo apt install gh` on Debian or Ubuntu (WSL included).

1. **Check auth.** `gh auth status`. If not logged in, `gh auth login` needs the user (browser or token). Do not try to guess credentials.
2. **Create a repo from the current folder.**
   ```
   git init -b main
   git add -A && git commit -m "Initial commit"
   gh repo create my-project --private --source=. --remote=origin --push
   ```
   Use `--public` only when the user clearly wants it public. Private is the safe default.
3. **Before the first push to a public repo,** run `git status` and look for `.env`, keys, `node_modules`, build output. Add them to `.gitignore` first.
4. **Branch and PR.**
   ```
   git switch -c fix/login-bug
   git add -A && git commit -m "Fix login redirect"
   git push -u origin fix/login-bug
   gh pr create --title "Fix login redirect" --body "What changed and why."
   ```
   Then `gh pr status`, `gh pr checks`, and `gh pr merge --squash` when the user approves.
5. **Release with files.**
   ```
   git tag v1.0.0 && git push origin v1.0.0
   gh release create v1.0.0 dist/app.zip --title "v1.0.0" --notes "First release"
   ```
   Add files later with `gh release upload v1.0.0 file.zip`.
6. **Change visibility.** `gh repo edit OWNER/NAME --visibility private --accept-visibility-change-consequences`.
7. **GitHub Pages.** Push the built site to a `gh-pages` branch or a `/docs` folder, then:
   ```
   gh api -X POST repos/OWNER/NAME/pages -f "source[branch]=main" -f "source[path]=/docs"
   gh api repos/OWNER/NAME/pages --jq .html_url
   ```
   Wait a minute, then `curl -sI <url>`. Private repos may not support Pages on a free plan.

Pitfalls:
- A repo name already taken gives "name already exists". Pick another.
- `gh repo create` without `--source` makes an empty remote repo and does not push.
- Never force push to main. Never delete a repo without the user saying so.
- Look at the repo with `gh repo view --web` only if a browser is available; otherwise `gh repo view`.
