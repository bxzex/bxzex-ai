import sys, os, threading, json, http.server, time, subprocess, re
# the phone bridge against a stand-in Telegram: only the owner is answered, an action is OK'd with a button, the reply comes back; then /export
def call(n, a): return {"tool_calls": [{"index": 0, "id": f"c{n}", "function": {"name": n, "arguments": json.dumps(a)}}]}
SCRIPT = [call("run_shell", {"command": "echo made-by-phone > phone.txt"}), {"content": "Made phone.txt for you."}]
SENT = []; UPDATES = [{"update_id": 1, "message": {"chat": {"id": 999, "type": "private"}, "from": {"id": 999}, "text": "stranger here"}},
                      {"update_id": 2, "message": {"chat": {"id": 42, "type": "private"}, "from": {"id": 42}, "text": "make a file"}}]
GOT = []
class TG(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        method = self.path.rsplit("/", 1)[1]; result = True
        if method == "getUpdates":
            off = body.get("offset", 0)
            ready = [u for u in UPDATES if u["update_id"] >= off]
            if not ready: time.sleep(min(body.get("timeout", 1), 1))
            result = ready
        elif method == "sendMessage":
            SENT.append(body); result = {"message_id": len(SENT)}
            if body.get("reply_markup", {}).get("inline_keyboard"):          # tap "Yes"
                data = body["reply_markup"]["inline_keyboard"][0][0]["callback_data"]
                UPDATES.append({"update_id": 10 + len(SENT), "callback_query": {"id": "q", "data": data, "message": {"chat": {"id": 42}}}})
        b = json.dumps({"ok": True, "result": result}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
class M(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if not body.get("stream"): return
        GOT.append(body); d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
tg = http.server.ThreadingHTTPServer(("127.0.0.1", 0), TG); threading.Thread(target=tg.serve_forever, daemon=True).start()
md = http.server.ThreadingHTTPServer(("127.0.0.1", 0), M); threading.Thread(target=md.serve_forever, daemon=True).start()
home = sys.argv[2]
json.dump({"phone": {"token": "T", "chat": 42, "user": 42, "bot": "test_bot", "offset": 0}}, open(home + "/config.json", "w"))
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{md.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", BXZEX_NO_TICKER="1",
           BXZEX_TELEGRAM_API=f"http://127.0.0.1:{tg.server_port}")
p = subprocess.Popen([sys.executable, sys.argv[1], "--phone"], env=env, cwd=home, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
end = time.time() + 30
while time.time() < end and not any("Made phone.txt" in s.get("text", "") for s in SENT): time.sleep(0.3)
p.kill(); log = p.communicate()[0]
texts = [s.get("text", "") for s in SENT]
print("stranger ignored:", not any(s.get("chat_id") == 999 for s in SENT) and all("stranger" not in json.dumps(m) for b in GOT for m in b["messages"]))
print("asked with buttons:", any(t.startswith("Allow: run command") for t in texts), "| file made:", os.path.exists(home + "/phone.txt"))
print("reply sent:", any("Made phone.txt" in t for t in texts))
print("chat kept:", os.path.exists(home + "/phone-chat.json"))
print("tracebacks:", "Traceback" in log)
