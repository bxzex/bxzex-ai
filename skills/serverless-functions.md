---
name: serverless-functions
description: Writing serverless API routes on Vercel or Netlify style platforms, including timeouts, env vars and logging.
---
# Serverless Functions

A function runs per request, has a time limit, and keeps no memory between calls you can rely on.

1. **Place the file where the platform expects it.** Vercel: `api/hello.js` or `app/api/hello/route.ts` in Next.js. Netlify: `netlify/functions/hello.js`. One file is one endpoint.
2. **Handle the request.** Read the method first and return `405` for ones you do not support. Parse the body inside try/catch and return `400` for bad JSON. Validate every field before using it.
3. **Respond clearly.** Always return JSON with a status code: `200` ok, `201` created, `400` bad input, `401` not logged in, `404` missing, `500` your bug. Never return a stack trace to the caller.
4. **Env vars.** Read them with `process.env.NAME`. Set them in the platform dashboard or CLI for each environment, then redeploy. Do not commit `.env`.
5. **Timeouts.** Default limits are short (often 10 to 60 seconds). If work takes longer, answer fast and move the work to a background job. Check the limit in the platform settings and raise it only if the plan allows.
6. **Cold starts.** The first request after idle is slower. Keep imports small, create database or API clients at module top level so warm calls reuse them, and avoid loading big libraries you do not use.
7. **Logging.** Use `console.log(JSON.stringify({route, status, ms}))`. Read logs with `npx vercel logs <url>` or `npx netlify logs:function hello`.
8. **Keep them small.** One job per function, no giant shared bundle, no writing to local disk except `/tmp`.

**Test locally:** `npx vercel dev` or `npx netlify dev`, then `curl -i -X POST localhost:3000/api/hello -d '{"a":1}' -H 'content-type: application/json'`.

**Pitfalls:** database connection exhaustion (use a pooled connection string); CORS errors when called from another origin (set `Access-Control-Allow-Origin` and answer `OPTIONS`); relying on in-memory state; forgetting to await a promise so the function ends before the work finishes.
