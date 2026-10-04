---
name: git-workflow
description: Using git: committing, branching, undoing mistakes, pushing to GitHub.
---
# Git

Look before you act: `git status`, `git diff`, `git log --oneline -10`, `git branch -a`.

**Committing**
- Stage on purpose: `git add <files>`, not `git add .` unless you have read the status.
- One change per commit. The message says what changed and why, in plain words, under about 70 characters on the first line.
- Never commit secrets, `.env` files, keys or large binaries. Check the diff first.

**Branches**
- New work goes on a branch: `git switch -c short-name`.
- Update with `git pull --rebase` on your own branch, plain `git pull` on shared ones.

**Undoing, from safest to most dangerous**
- Unstage: `git restore --staged <file>`
- Drop local edits to one file: `git restore <file>` (this loses them, ask first)
- Fix the last commit message: `git commit --amend`
- Undo a pushed commit safely: `git revert <hash>`
- `git reset --hard`, `git push --force`, `git clean -fd` destroy work. Only with the user's clear yes, and say what will be lost.

**GitHub**
- `gh repo create`, `gh pr create`, `gh pr view --web` if the `gh` tool is installed.
- Before pushing, check which remote and branch: `git remote -v`, `git branch --show-current`.

If something looks wrong, stop and show the user the status rather than trying to fix it blind. `git reflog` can recover most things.
