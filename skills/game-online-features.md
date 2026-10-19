---
name: game-online-features
description: Adding leaderboards, cloud saves, daily challenges and multiplayer to a web game, with basic anti-cheat and offline fallback.
---
# Online features for web games

**Keep it optional.** The game must work with no network. Wrap every online call in try/catch with a short timeout, fall back to local data, and never block Play on a server response.

**Global leaderboard (serverless + Postgres)**
```sql
create table scores (
  id bigserial primary key,
  player_id text not null,
  name text not null,
  score int not null check (score >= 0),
  created_at timestamptz default now()
);
create index on scores (score desc);
create table bests (player_id text primary key, name text, score int, updated_at timestamptz default now());
```
- Submit: `POST /api/score` with `{name, score, token}`. Upsert into `bests` only if higher: `insert ... on conflict (player_id) do update set score = excluded.score where excluded.score > bests.score`.
- Top N: `select name, score from bests order by score desc limit 20`. Cache for 10 to 30 seconds.
- Show the player's own rank: `select count(*)+1 from bests where score > $1`.
- Use a hosted Postgres (Neon, Supabase) and read the connection string from an environment variable, never from client code.

**Basic anti-cheat.** You cannot fully trust the client, so make cheating not worth it.
- Server checks plausibility: max score per second of play, max possible score for the level.
- Signed run tokens: `GET /api/run` returns `{runId, startedAt}` signed with an HMAC secret. On submit, verify the signature and that elapsed time fits the score.
- Rate limit per IP and per player (a few submissions a minute).
- Send inputs or a replay for high scores if it matters; the server re-simulates.
- Never trust the client for prizes or money. Hold payouts until a human or server check approves them.

**Player names.** Limit to 3 to 16 characters, trim, strip control characters. Filter profanity with a word-list package (for example `bad-words`) plus a short custom list, matching on normalized text (lowercase, leetspeak mapped). Filter on the server, not only the client. Let players be anonymous by default with a generated name like "Player4821".

**Cloud saves.** Store a JSON blob keyed by a player id (anonymous id in `localStorage`, or a real account). Include a version number and `updatedAt`. On conflict, keep the newer or merge by taking the max of each progress value. Always keep the local save as the source when offline and sync later.

**Daily challenge.** Seed a PRNG with the date so everyone gets the same layout:
```js
function mulberry32(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const seed = Number(new Date().toISOString().slice(0, 10).replaceAll('-', ''));
const rand = mulberry32(seed);
```
Use the server's date (UTC) so time zones and clock changes cannot be abused. Keep a separate leaderboard per date.

**Real-time multiplayer options**
- WebSocket server in Node (`ws` or Socket.IO) for small games.
- Colyseus for rooms, state sync and matchmaking.
- Hosted realtime services (Ably, PartyKit, Supabase Realtime) if you do not want to run a server.
- Serverless platforms do not hold long-lived sockets; use a hosted service or a small always-on server.

**Multiplayer basics**
- Authoritative server: the server owns the true state; clients send inputs, not positions.
- Send updates at 10 to 20 per second, not every frame.
- Client prediction: apply your own input immediately, then reconcile when the server state arrives.
- Interpolation: render other players about 100 ms in the past, blending between the last two snapshots.
- Handle disconnects, reconnects, and a lobby with a clear "waiting for players" state.

**Latency testing.** Use browser devtools network throttling, add artificial delay on the server (a 100 to 300 ms sleep), and drop a few percent of messages. Test on a phone over mobile data, not only localhost.

**Verify with test_page.** Open the page as iPhone, Android and desktop. Check the game starts with the network failing or blocked, the leaderboard shows a friendly empty or error state, there are no console errors beyond handled ones, the name input fits phone screens, and phone-landscape layouts are not cut off. Use `steps` such as "click Play", "wait 2000", "click Submit" and look at the screenshots. Use `fetch_page` or `run_shell` with `curl` to test the API routes directly.
