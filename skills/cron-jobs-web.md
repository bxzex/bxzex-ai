---
name: cron-jobs-web
description: Scheduling recurring jobs for a hosted app with platform cron, a secured endpoint and safe re-runs.
---
# Scheduled Jobs on a Hosted App

Hosted platforms do not keep a process running, so cron calls an HTTP endpoint on a schedule.

1. **Write the job as an endpoint**, for example `GET /api/cron/cleanup`. Keep it short, and have it do one task.
2. **Schedule it.** On Vercel add to `vercel.json`:
   ```
   { "crons": [ { "path": "/api/cron/cleanup", "schedule": "0 3 * * *" } ] }
   ```
   Times are UTC. Format is `minute hour day month weekday`. Free plans limit how often and how many jobs run, so check the current plan limits. Other hosts have their own scheduler UI; GitHub Actions with `on: schedule` also works and can `curl` your endpoint.
3. **Secure it.** Anyone can hit a public URL. Set `CRON_SECRET` as an env var and reject requests without a matching header:
   ```
   if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) return new Response('no', {status: 401})
   ```
   Vercel sends that header automatically when `CRON_SECRET` is set.
4. **Make it idempotent.** The platform can run a job twice or late. Use a "last processed" marker, an upsert, or a unique key so a repeat does nothing harmful. Never send the same email twice because of a retry.
5. **Bound the work.** Process in batches (for example 100 rows) so you stay under the function timeout. The next run picks up the rest.
6. **Log the result.** Print how many items were handled, how long it took, and any error. A job that fails silently is worse than none.

**Test it:** `curl -i -H "Authorization: Bearer $CRON_SECRET" https://your-site.vercel.app/api/cron/cleanup`. Without the header it should return 401.

**Pitfalls:** cron only runs on production deployments; changing the schedule needs a redeploy; time zones are UTC; long jobs belong in a background queue, with cron just starting them.
