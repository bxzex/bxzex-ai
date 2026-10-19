---
name: observability
description: Knowing when an app breaks, using structured logs, error tracking, uptime checks and platform log commands.
---
# Observability

You want to hear about a failure before a user tells you.

1. **Structured logs.** Log one JSON object per event, not free text:
   `console.log(JSON.stringify({level:'error', route:'/api/pay', userId, msg:err.message, ms}))`.
   Include a request id so you can follow one request. Never log passwords, tokens, card numbers or full request bodies.
2. **Levels.** `error` for failures someone must look at, `warn` for odd but handled, `info` for key events. Avoid logging inside tight loops.
3. **Error tracking.** Add a hosted error tracker (Sentry or a similar service) through its SDK for both server and browser. Set the DSN in env vars, set the release name to the git commit, and upload source maps. Trigger one test error and confirm it appears.
4. **Read platform logs from the CLI.**
   - Vercel: `npx vercel logs <deployment-url>`
   - Netlify: `npx netlify logs:function <name>`
   - Fly: `fly logs`
   - Docker: `docker logs --tail 200 -f <container>`
   - Server: `journalctl -u myapp -n 200 --no-pager`
   Filter fast: `... | grep -i error | tail -50`.
5. **Uptime check with curl in cron.** Save as `check.sh`:
   ```
   #!/bin/sh
   code=$(curl -s -o /dev/null -m 10 -w "%{http_code}" https://example.com/api/health)
   [ "$code" = "200" ] || curl -s -d "site down: $code" https://ntfy.sh/your-private-topic
   ```
   Then `crontab -e` and add `*/5 * * * * /path/check.sh`. Or use a hosted uptime monitor with a free tier. A scheduled GitHub Actions workflow also works.
6. **Health endpoint.** `GET /api/health` returns 200 only if the database answers a `select 1`. Do not expose secrets or versions publicly.
7. **Alerts.** Alert on: site down, error rate jump, failed background jobs, certificate expiring in under 14 days. Send to one place someone reads (email, chat channel). Too many alerts get ignored, so tune them.

**Check:** break something on purpose in a preview (throw in a route), confirm the log line, the tracker event and the alert all show up, then fix it.

**Pitfalls:** logs lost because the platform keeps them only briefly; alerts that go to nobody; health checks that always return 200.
