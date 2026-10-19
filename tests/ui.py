import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
def call(name, **a): return {"tool_calls": [{"index": 0, "id": f"c{name}{time.time()}", "function": {"name": name, "arguments": json.dumps(a)}}]}
TABLE = "Here you go:\n\n| Plan | Price | Notes |\n|---|---|---|\n| **Free** | $0 | a little usage |\n| Pro | $15 | more |\n\n```python\ndef hi(n):\n    return \"hello\" * 2  # a comment\n```\nDone."
SCRIPT = [{"content": TABLE},
          call("run_shell", command="printf 'one\\ntwo\\nthree\\nfour-secret-line\\n'"), {"content": "ran it"},
          call("run_shell", command="printf 'again\\n'"), {"content": "ran again"},
          call("write_file", path="made.txt", content="new file"), {"content": "wrote it"}]
GOT = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if not body.get("stream"): return
        GOT.append(body["messages"])
        d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
        if "content" in d:
            for i in range(0, len(d["content"]), 7):
                self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': d['content'][i:i+7]}}]})}\n\n".encode())
        else: self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]; work = home + "/work"; os.makedirs(work, exist_ok=True)
open(home + "/connectors.txt", "w").write(open(sys.argv[3]).read())
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0: os.chdir(work); os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 110, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
def mark(): return len(out)
pump(2); os.write(fd, b"show me a table\r"); pump(2.5); m1 = mark()
os.write(fd, b"run something\r"); pump(1.5); os.write(fd, b"f"); pump(2.5); m2 = mark()
os.write(fd, b"\x0f"); pump(1); m3 = mark()
os.write(fd, b"run again\r"); pump(2.5); m4 = mark()
os.write(fd, b"make a file\r"); pump(1.5); os.write(fd, b"y"); pump(2); m5 = mark()
os.write(fd, b"\x1b"); pump(0.3); os.write(fd, b"\x1b"); pump(1.2)        # esc esc: rewind
os.write(fd, b"\r"); pump(1); os.write(fd, b"\x1b[B\r"); pump(1.5); m6 = mark()   # newest message, then "put files back too"
os.write(fd, b"\x15/apps shopify\r"); pump(1.5); os.write(fd, b"exit\r"); pump(2)
txt = lambda a, b=None: re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out[a:b].decode("utf-8", "ignore"))
t1 = txt(0, m1); raw1 = out[:m1].decode("utf-8", "ignore")
print("table grid:", "┌" in t1 and "│ Free" in t1 and "| Plan" not in t1, "| code coloured:", "\x1b[38;5;150m\"hello\"" in raw1, "| ``` hidden:", "```" not in t1)
print("folder rule button shown:", "always here: printf" in txt(m1, m2))
print("ctrl-o full output:", "four-secret-line" in txt(m2, m3))
print("second command not asked:", "Allow: run command" not in txt(m3, m4), "| ran:", "again" in txt(m3, m4))
print("file made:", os.path.exists(work + "/made.txt"))
print("rewind:", "Went back" in txt(m5, m6), "| file put back (removed):", not os.path.exists(work + "/made.txt"))
print("/apps search:", "Shopify" in txt(m6))
print("tracebacks:", "Traceback" in txt(0))
cfg = json.load(open(home + "/config.json")); print("saved rule:", cfg.get("allow"))
