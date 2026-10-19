---
name: chat-bots
description: Building a bot for Slack, Discord or Telegram, from creating the token to verifying requests and deploying.
---
# Chat Bots (Slack, Discord, Telegram)

1. **Pick the delivery mode.**
   - Webhook (the platform POSTs events to your HTTPS URL): best for serverless hosting.
   - Polling or socket connection (your process pulls events): easiest for local work, needs a long-running host.
2. **Create the bot and keep the secrets.**
   - Telegram: message the official bot-creation bot in the app, run `/newbot`, copy the token.
   - Discord: developer portal, new application, Bot tab, copy the token, then invite it with the OAuth2 URL builder using scopes `bot` and `applications.commands`.
   - Slack: api.slack.com/apps, create an app, add bot scopes (such as `chat:write`, `commands`), install to the workspace, copy the bot token and signing secret.
   Put tokens in env vars. Never commit them; if one leaks, regenerate it at once.
3. **Local testing.** Start your server, then expose it with a tunnel (`npx localtunnel --port 3000` or `cloudflared tunnel --url http://localhost:3000`) and paste the URL into the platform settings.
4. **Verify every incoming request.**
   - Slack: compute HMAC SHA256 of `v0:<timestamp>:<raw body>` with the signing secret, compare to `X-Slack-Signature` with a constant time compare, and reject timestamps older than 5 minutes. Use the raw body, not parsed JSON.
   - Discord interactions: verify the Ed25519 signature headers with your application public key, and answer the `PING` type with `{type:1}`.
   - Telegram: set a `secret_token` in `setWebhook` and check the `X-Telegram-Bot-Api-Secret-Token` header.
5. **Respond fast.** Platforms expect an answer in about 3 seconds. Acknowledge immediately, then do slow work in the background and post the result later through the response URL or the send-message API.
6. **Slash commands.** Register them (Discord and Slack in the app settings or API, Telegram with `setMyCommands`). Keep names lowercase and give each a one-line description. Slash commands that change things should confirm first.
7. **Deploy.** Put the app on a host with a stable HTTPS URL, set the env vars, update the webhook URL from the tunnel to the real one, and test in a private channel.

**Pitfalls:** answering events twice because of retries (store the event id); bot not in the channel; missing intents or scopes after adding features; logging full message text that contains private data.
