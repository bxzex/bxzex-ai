---
name: api-design
description: Designing or building a web API or backend endpoints.
---
# API design

Design it from the caller's side: what do they need to send, and what do they get back?

**Shape**
- Nouns for resources, HTTP verbs for actions: `GET /orders`, `POST /orders`, `GET /orders/42`, `PATCH /orders/42`, `DELETE /orders/42`.
- Plural, lowercase, hyphenated paths. Keep them shallow.
- JSON in and out. One naming style for fields everywhere.
- Lists are paginated from day one, and return the same item shape as the single-item endpoint.

**Status codes that mean what they say**
- 200 ok, 201 created, 204 no content
- 400 bad input, 401 not signed in, 403 not allowed, 404 not found, 409 conflict, 422 failed validation, 429 too many requests
- 500 only for your own bugs

**Errors**
- Always the same shape: a machine code, a human message, and which field was wrong.
- Never leak stack traces or SQL.

**Safety**
- Validate every input on the server: type, length, range, allowed values.
- Check on every request that this user may touch this record.
- Rate limit anything public, and anything that sends email or costs money.
- Make retries safe: accept an idempotency key on actions that create or charge.
- Secrets live in environment variables.

**Care for the caller**
- Version it (`/v1/`) before anyone depends on it.
- Do not remove or rename fields in place. Add new ones.
- Write one example request and response for every endpoint.
- Timestamps in ISO 8601 UTC. Money in integer minor units with a currency code.

Test each endpoint with a real request (`curl`) including one bad input, and show the result.
