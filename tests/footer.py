import sys, os, threading, json, http.server, pty, time, select, struct, fcntl, termios, re
# the box at the bottom stays through a question with choices, typing your own answer, and an allow question
def call(n, a): return {"tool_calls": [{"index": 0, "id": f"c{n}", "function": {"name": n, "arguments": json.dumps(a)}}]}
SCRIPT = [call("ask_user", {"question": "Which route?", "options": "Fast|Slow"}), call("ask_user", {"question": "And then?", "options": "A|B"}),
          call("run_shell", {"command": "touch made.txt"}), {"content": "all done"}]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if not body.get("stream"): return
        d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0: os.chdir(home); os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
ROWS, COLS = 30, 100
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
erased = []                       # after each step: was the box's rule row wiped by an erase-to-end-of-screen inside the scroll area?
def check(label):
    tail = out.decode("utf-8", "ignore")
    tail = tail[max(0, tail.find(f"\x1b[{ROWS - 3};1H\x1b[J")):]        # from when the box is first drawn
    # an erase below that runs while the cursor is in the conversation area wipes the box; the box's own redraw starts at its row
    bad = [m for m in re.finditer(r"\x1b\[J", tail) if not re.search(rf"\x1b\[{ROWS - 3};1H$", tail[max(0, m.start() - 12):m.start()])]
    erased.append((label, len(bad), [repr(tail[max(0, m.start() - 25):m.start() + 3]) for m in bad][:2]))
pump(2); os.write(fd, b"go\r"); pump(2); check("first list shown")
os.write(fd, b"\x1b[B\x1b[B\r"); pump(0.6); check("picked: type my own")
os.write(fd, b"my own words\r"); pump(1.5); check("own answer sent")
os.write(fd, b"\r"); pump(1.5); check("second list picked")
os.write(fd, b"y"); pump(2); check("allowed")
os.write(fd, b"exit\r"); pump(2)
total = sum(n for _, n, _ in erased)
print("box never wiped:", total == 0, erased if total else "")
plain = out.decode("utf-8", "ignore")
print("own answer used:", "The user answered: my own words" in plain or "my own words" in plain)
print("tracebacks:", "Traceback" in plain)
