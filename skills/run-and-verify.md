---
name: run-and-verify
description: After changing an app, run it for real and check it works with curl, logs and a screenshot, then stop it.
---
# Run and verify

Do not say it works until you have seen it work.

1. **Find the start command.** Read package.json scripts, a Makefile or the README. Typical: `npm run dev`, `python app.py`, `go run .`.
2. **Start in the background and capture logs.**
   `npm run dev > /tmp/dev.log 2>&1 & echo $! > /tmp/dev.pid`
   Use run_shell's background option if it exists. Never run a server in the foreground, the tool will hang.
3. **Wait until it is ready.**
   `for i in $(seq 1 30); do curl -s -o /dev/null http://localhost:5173 && break; sleep 1; done`
   Read the port from the log: `tail -20 /tmp/dev.log`.
4. **Check the response.**
   - `curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" http://localhost:5173/`
   - `curl -s http://localhost:5173/ | grep -i "<title>"`
   - APIs: `curl -s -X POST localhost:3000/api/x -H 'content-type: application/json' -d '{"a":1}'`
5. **Read the logs** for errors or warnings: `grep -iE "error|warn|fail" /tmp/dev.log`.
6. **Screenshot if a headless browser exists.**
   `npx playwright screenshot --viewport-size=1280,800 http://localhost:5173 /tmp/shot.png` (first run may need `npx playwright install chromium`). Or `chromium --headless --screenshot=/tmp/shot.png URL`. View it with read_file. Also try 375px wide.
7. **Exercise the change.** Hit the specific route or form you modified, not only the home page.
8. **Stop the server.** `kill $(cat /tmp/dev.pid)`. If a port stays busy: `lsof -ti :5173 | xargs kill`.
9. **Report** what you ran, what you saw (status codes, log lines, the screenshot), and anything you could not check.

Pitfalls: a 200 on a blank page (check the HTML body and console errors), stale processes serving old code (check the port first with `lsof -i :5173`), a missing `.env` (copy `.env.example` and tell the user).
