---
name: env-secrets
description: Handling API keys, tokens and passwords safely in a project: .env files, gitignore, leak checks and rotation.
---
# Environment variables and secrets

1. **Keep secrets in `.env`,** one `NAME=value` per line, in the project root. Read them in code with `process.env.NAME` or `os.environ["NAME"]` (Python: `pip install python-dotenv`, then `load_dotenv()`).
2. **Ignore it before you create it.**
   ```
   grep -qx ".env" .gitignore || printf ".env\n.env.*\n!.env.example\n" >> .gitignore
   git check-ignore -v .env
   ```
   The second command should print a rule. If it prints nothing, the file is not ignored.
3. **Commit a `.env.example`** with names and fake values only (`STRIPE_SECRET_KEY=sk_test_xxx`), so others know what to set.
4. **Never print secrets.** Do not `cat .env`, echo keys, or paste them into logs, chat, commit messages or issue text. To check a variable exists without showing it: `[ -n "$NAME" ] && echo set || echo missing`. To show only the shape: `echo "${NAME:0:4}..."`.
5. **Keep them out of the browser.** Frontend code is public. Only values meant to be public (like a publishable key) may use `NEXT_PUBLIC_` or `VITE_` prefixes. Call paid APIs from a server.
6. **Check before you commit or push.**
   ```
   git status --short
   git diff --cached | grep -nEi "(api[_-]?key|secret|token|password|sk_live|BEGIN (RSA|PRIVATE))" 
   ```
7. **Search history for leaks.** `git log -p --all -S"sk_live" --oneline | head`, or `git log --all --full-history -- .env`. If `gitleaks` or `trufflehog` is installed, run `gitleaks detect --source .`.
8. **If a secret leaked, rotate it first.** Deleting the file or rewriting history does not help once it was pushed, because someone may have copied it.
   - Revoke the key in the provider's dashboard and create a new one.
   - Put the new one in `.env` and the host's settings (for example `vercel env add NAME production`).
   - Check the provider's usage log for activity you do not recognize.
   - Then remove it from history if needed (`git filter-repo --path .env --invert-paths`), and tell the user a force push is required. Do not force push without their approval.
9. **Local files to avoid committing:** `.env`, `*.pem`, `id_rsa`, `credentials.json`, `service-account*.json`, `.npmrc` with tokens.

Rule of thumb: if you would not post it publicly, it does not belong in a commit.
