import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
N = [0]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if not body.get("stream"): return
        N[0] += 1
        d = {"tool_calls": [{"index": 0, "id": "t1", "function": {"name": "run_shell", "arguments": json.dumps({"command": "sleep 3; date"})}}]} if N[0] == 1 else {"content": "ok"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=sys.argv[2], BXZEX_UPDATE_URL="file://" + sys.argv[3], BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0: os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 110, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
pump(2); os.write(fd, b"run something\r"); pump(1.5); os.write(fd, b"y"); pump(5)
mark = len(out); os.write(fd, b"/update\r"); pump(4); upd = out[mark:]
os.write(fd, b"exit\r"); pump(2)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]", "", out.decode("utf-8", "ignore"))
u = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]", "", upd.decode("utf-8", "ignore"))
print("loader while command ran:", plain.count("Running…"), "frames | command output:", bool(re.search(r"exit code 0", plain)))
print("update loader:", "Checking for updates…" in u or "Downloading v9.9.9…" in u, "| updated + reloaded:", "carrying on where you were" in u)
print("tracebacks:", "Traceback" in plain)
