---
name: ai-chat-app
description: Adding an AI chat feature to a web app with a streaming server route, history, stop button and error handling.
---
# AI Chat Feature

The browser never talks to the model API directly. A server route does, so the key stays secret.

1. **Key.** Put the key in `.env.local` (for example `CHAT_API_KEY`), add `.env*` to `.gitignore`, and read it only in server code. Never use a `NEXT_PUBLIC_` or `VITE_` prefix.
2. **Route.** Create `POST /api/chat`. It accepts `{ messages: [{role, content}] }`, checks the shape, caps the number and length of messages, then calls the chat completions API with `stream: true`.
3. **Stream back.** Pipe the provider's event stream to the client as it arrives. Return a `Response` with a `ReadableStream` and the header `Content-Type: text/event-stream` (or plain text chunks). Do not wait for the full answer.
4. **Client.** Keep `messages` in state. On send, push the user message, push an empty assistant message, then read `response.body.getReader()` and append each decoded chunk to the last message.
5. **Stop button.** Create an `AbortController`, pass `signal` to `fetch`, and call `abort()` on click. Keep whatever text already arrived. On the server, pass `req.signal` on to the upstream call so you stop paying for tokens.
6. **History.** Send the last N messages, not the whole thread. Put a short system message first. Store threads in the database or localStorage if they must survive a reload.
7. **Errors.** Map upstream 401 and 403 to a server log only (never show key problems to users). Map 429 to "busy, try again in a moment" and honor the `Retry-After` header. Show a retry button on failure.
8. **Rate limit your own route.** Limit per IP or per user, for example 20 requests a minute, so one visitor cannot drain your credit. Require login if the app is public.

**Check it**
- `curl -N -X POST localhost:3000/api/chat -H 'content-type: application/json' -d '{"messages":[{"role":"user","content":"hi"}]}'` should print text gradually.
- Search the built client bundle for the key: `grep -r "sk-" .next/static dist 2>/dev/null` must find nothing.
- Set a timeout or max token limit so one request cannot run forever.

**Pitfalls:** buffering proxies can break streaming (disable compression on that route); serverless time limits cut long streams; never trust a `role: "system"` message sent from the browser.
