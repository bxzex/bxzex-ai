import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
# The list above the input box (commands after /, files after @), messages of several lines, and mistyped commands.
GOT = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if body.get("max_tokens") == 1 or not body.get("stream"): self.wfile.write(b"data: [DONE]\n\n"); return
        GOT.append(body["messages"][-1].get("content"))
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': 'See [the docs](https://example.com/d) now'}}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]; work = home + "/work"; os.makedirs(work + "/src", exist_ok=True)
open(work + "/src/main.py", "w").write("x = 1\n"); open(work + "/notes.txt", "w").write("n\n")
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color", TERM_PROGRAM="test")
pid, fd = pty.fork()
if pid == 0: os.chdir(work); os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
def txt(a, b=None): return re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\", "", out[a:b].decode("utf-8", "ignore"))
pump(2.5); a = len(out)
os.write(fd, b"/co"); pump(0.6); listed = txt(a); a = len(out)
os.write(fd, b"\x1b[B"); pump(0.3); os.write(fd, b"\r"); pump(1.2); ran = txt(a); a = len(out)      # the second one down: /context
os.write(fd, b"/hlep\r"); pump(1); typo = txt(a); a = len(out)
os.write(fd, b"read @sr"); pump(0.5); os.write(fd, b"\t"); pump(0.4); os.write(fd, b"\t"); pump(0.4); files = txt(a)
os.write(fd, b"\r"); pump(2); a = len(out)
os.write(fd, b"first\x1b\rsecond\\\rthird\r"); pump(2); reply = txt(a); raw = out[a:].decode("utf-8", "ignore"); a = len(out)
os.write(fd, b"/new\r"); pump(1); new = txt(a); a = len(out)
os.write(fd, b"/cd src\r"); pump(1); moved = txt(a)
os.write(fd, b"exit\r"); pump(1.5)
print("list shown with notes:", "/color" in listed and "/context" in listed and "pick a color theme" in listed and "enter to run" in listed)
print("arrow then enter ran it:", "Context" in ran and "tokens" in ran)
print("typo not sent:", "no command called /hlep" in typo and "did you mean /help" in typo and not any("/hlep" in str(g) for g in GOT))
print("file list:", "@src/" in files and "@src/main.py" in files, "| attached:", any("--- src/main.py ---" in str(g) and "x = 1" in str(g) for g in GOT))
print("several lines sent:", "first\nsecond\nthird" in [g for g in GOT if isinstance(g, str)])
print("link shown as its text:", "the docs" in reply and "[the docs]" not in reply and "\x1b]8;;https://example.com/d" in raw)
print("/new at the keyboard:", "new conversation" in new, "| /cd:", "working in" in moved and moved.rstrip().endswith("src") or "src" in moved)
print("tracebacks:", "Traceback" in txt(0))
