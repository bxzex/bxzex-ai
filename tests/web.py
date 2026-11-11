import sys, os, threading, json, http.server, subprocess, time, tempfile
# A fake model and a fake site in one server: the site hands out what "the page" wrote and collects what the app shows there.
home = sys.argv[2]; work = tempfile.mkdtemp(dir=os.path.realpath("/tmp")); target = work + "/made.txt"
inbox = [{"id": 2, "kind": "text", "body": "make the file"}]
shown = []; keys = set(); calls = {"n": 0}; lock = threading.Lock(); asked = []
# the chat that is "open in the terminal": the remote has to carry on this one, in its folder
os.makedirs(home + "/chats"); chat = home + "/chats/2026-01-01_10-00-00.json"
json.dump({"title": "the word", "messages": [{"role": "user", "content": "the secret word is PINEAPPLE"}, {"role": "assistant", "content": "Noted."}]}, open(chat, "w"))
json.dump({"chat": chat, "cwd": work}, open(home + "/current-chat.json", "w"))
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def send(self, obj):
        b = json.dumps(obj).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        if self.path.startswith("/remote/"):
            keys.add(self.headers.get("x-bxzex-remote"))
            with lock:
                if self.path.endswith("/pull"):
                    out, inbox[:] = list(inbox), []
                    return self.send({"messages": out})
                for e in body.get("events", []):
                    shown.append(e)
                    if e["kind"] == "ask": inbox.append({"id": 9, "kind": "answer", "ask": e["ask"], "pick": 0})     # tap "Yes"
                return self.send({"ok": True})
        calls["n"] += 1; asked.append(json.dumps(body))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if calls["n"] == 1:
            d = {"tool_calls": [{"index": 0, "id": "c1", "function": {"name": "write_file", "arguments": json.dumps({"path": "made.txt", "content": "hi\n"})}}]}
            self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\n".encode())
        else:
            for t in ["Made ", "**the file**."]:
                self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': t}}]})}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"
json.dump({"web": {"url": base + "/remote", "key": "k" * 40}}, open(home + "/config.json", "w"))
env = dict(os.environ, BXZEX_REMOTE=base, BXZEX_HOME=home, BXZEX_NO_UPDATE="1", BXZEX_NO_TICKER="1")
p = subprocess.Popen([sys.executable, sys.argv[1], "--web"], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
end = time.time() + 60
while time.time() < end and not any(e["kind"] == "reply" and e["body"].startswith("Made") for e in shown): time.sleep(0.3)
first = len(shown)
def send(text, until, wait=30):
    with lock: inbox.append({"id": 50 + len(shown), "kind": "text", "body": text})
    stop = time.time() + wait
    while time.time() < stop and not until(shown[first:]): time.sleep(0.3)
    return until(shown[first:])
# every terminal command works from the page: its output comes back as the reply
print("/fast from the page:", send("/fast", lambda ev: any(e["kind"] == "reply" and "fast mode" in e["body"] for e in ev)))
print("!shell from the page:", send("!echo shell-from-page", lambda ev: any(e["kind"] == "reply" and "shell-from-page" in e["body"] for e in ev)))
print("/help from the page:", send("/help", lambda ev: any(e["kind"] == "reply" and "/schedule" in e["body"] for e in ev)))
print("keyboard-only ones say so:", send("/password", lambda ev: any(e["kind"] == "note" and "keyboard" in e["body"] for e in ev)))
print("/history lists chats:", send("/history", lambda ev: any(e["kind"] == "reply" and "chats" in e["body"].lower() for e in ev)))
# /new starts a fresh chat that does not fall back into the old one
before = len(asked); send("/new", lambda ev: any(e["kind"] == "note" and "New chat" in e["body"] for e in ev))
n = sum(1 for e in shown if e["kind"] == "reply")
send("hello again", lambda ev: sum(1 for e in shown if e["kind"] == "reply") > n)
print("new chat is really new:", len(asked) > before and "PINEAPPLE" not in asked[-1] and len(os.listdir(home + "/chats")) == 2)
time.sleep(1); p.terminate(); out = p.communicate(timeout=10)[0].decode("utf-8", "ignore")
kinds = [e["kind"] for e in shown]
print("key sent:", keys == {"k" * 40})
print("carried on the terminal chat:", any(e["kind"] == "note" and "Carrying on your terminal chat" in e["body"] for e in shown))
print("earlier messages shown:", any(e["kind"] == "said" and "PINEAPPLE" in e["body"] for e in shown))
print("model got the history:", all("PINEAPPLE" in a for a in asked[:2]) and len(asked) >= 2)
saved = json.load(open(chat))["messages"]
print("saved back into that chat:", saved[0]["content"].endswith("PINEAPPLE") and any(m.get("content") == "Made **the file**." for m in saved) and len(saved) >= 5)
print("asked on the page:", any(e["kind"] == "ask" and "made.txt" in e["body"] and e.get("choices") == ["Yes", "No", "Always, this chat"] for e in shown))
print("file made after the tap:", os.path.exists(target) and open(target).read() == "hi\n")
print("work shown:", any(e["kind"] == "log" and "write_file" in e["body"] for e in shown))
print("no escape codes shown:", not any("\x1b" in e["body"] for e in shown))
print("reply shown:", any(e["kind"] == "reply" and e["body"] == "Made **the file**." for e in shown))
print("ask before its reply:", "ask" in kinds[:first] and shown[first - 1]["kind"] == "reply")
print("no tracebacks" if "Traceback" not in out else "TRACEBACK FOUND\n" + out[-1500:])
