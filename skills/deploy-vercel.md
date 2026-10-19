---
name: deploy-vercel
description: Deploying a static, Vite or Next.js site to Vercel from the command line and checking that it is live.
---
# Deploy to Vercel

1. **Build locally first.** Run `npm install && npm run build`. If that fails, Vercel will fail too. Fix it here.
2. **Log in.** `npx vercel whoami`. If it errors, run `npx vercel login` (this needs the user, it opens a browser).
3. **Link the project.** From the project folder run `npx vercel link`. This creates `.vercel/`. Make sure `.vercel` is in `.gitignore`.
4. **Preview deploy.** `npx vercel` gives a preview URL. Open it with `curl -sI <url> | head -5` and expect `HTTP/2 200`. Preview URLs may be password protected, a 401 there is not a build failure.
5. **Production deploy.** `npx vercel --prod`. Copy the production URL from the output.
6. **Verify live.** `curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" https://your-site.vercel.app`. Then `curl -s https://your-site.vercel.app | grep -i "<title>"` to confirm it is the new build.

**Environment variables**
- Add: `npx vercel env add NAME production` (it prompts for the value).
- List: `npx vercel env ls`.
- Pull to local: `npx vercel env pull .env.local`.
- Changing a variable needs a new deploy to take effect.
- Only variables starting with `NEXT_PUBLIC_` (Next.js) or `VITE_` (Vite) reach the browser. Never put secrets behind those prefixes.

**Domains**
- `npx vercel domains add example.com`, then set the DNS records it prints (usually an A record to 76.76.21.21 or a CNAME to cname.vercel-dns.com).
- Check with `dig +short example.com`.

**Common build failures**
- Wrong output folder: Vite builds to `dist`, Next.js to `.next`, plain static to the folder you choose. Set it in project settings or `vercel.json`.
- Node version mismatch: set `"engines": {"node": "20.x"}` in package.json.
- Case-sensitive imports: `./Header` vs `./header` works on macOS but fails on the Linux build.
- Missing env var at build time: add it for the Production environment.
- Lockfile not committed: commit `package-lock.json`.
- SPA routes 404 on refresh: add a rewrite of `/(.*)` to `/index.html` in `vercel.json`.

Read the build log with `npx vercel logs <deployment-url>` and fix the first error.
