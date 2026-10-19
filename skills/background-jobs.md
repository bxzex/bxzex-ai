---
name: background-jobs
description: Moving long or retryable work off the request path using queues or durable workflows with safe retries.
---
# Background Jobs

If work takes more than a couple of seconds, can fail, or must not be lost, do not do it inside the request.

1. **Decide the shape.**
   - One fire-and-forget task (send an email, resize an image): a queue.
   - Several steps with waits, retries and state (onboarding, video processing): a durable workflow tool that saves progress between steps.
   - Run on a schedule: see the cron skill.
   Use the hosted option your platform offers or a library backed by Redis or Postgres. Do not build a queue from setTimeout.
2. **Request side.** Validate, save a row such as `jobs(id, type, payload, status, attempts)`, enqueue, and return `202 Accepted` with the job id. The client polls `GET /api/jobs/<id>` or gets a webhook or email later.
3. **Worker side.** Pull a job, mark it running, do the work, mark it done. Keep each handler short and focused.
4. **Retries with backoff.** On failure wait longer each time: 10s, 1m, 5m, 30m, with a little random jitter. Cap attempts at 5 to 8. Retry only errors that can pass later (timeouts, 429, 5xx), not bad input.
5. **Idempotency.** Every job can run twice. Give each job an idempotency key (for example `order-123-receipt`), store it with a unique constraint, and skip work already done. When calling payment or email APIs, pass their idempotency key header too.
6. **Dead letters.** After the last attempt, move the job to a `failed` state or dead letter queue with the error text. Alert on it. Provide a way to replay a job after the bug is fixed.
7. **Visibility.** Log job id, type, attempt and duration. Track queue depth and the age of the oldest waiting job.

**Check:** enqueue a job that throws, confirm it retries on the schedule, lands in the dead letter state, and replaying a successful job twice causes no duplicate effect.

**Pitfalls:** jobs that hold a database transaction open; payloads that hold huge data (store an id instead); workers that all start at once and flood an API.
