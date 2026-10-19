import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
GOT = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if body.get("max_tokens") != 1: GOT.append([m.get("content") for m in body["messages"] if m["role"] == "user"])
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': 'ok'}}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=sys.argv[2], BXZEX_UPDATE_URL="file://" + sys.argv[3], TERM="xterm-256color")
env.pop("BXZEX_NO_UPDATE", None)
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
pump(3); os.write(fd, b"first message\r"); pump(4)
os.write(fd, b"half typ"); pump(3)          # the reload happens while this sits in the box
os.write(fd, b"ed\r"); pump(3); os.write(fd, b"/fast\r"); pump(1); os.write(fd, b"exit\r"); pump(2)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out.decode("utf-8", "ignore")).replace("─", "")
print("reloaded:", "carrying on where you were" in plain, "| now 9.9.9:", "v9.9.9" in plain)
print("chat kept across the reload:", GOT[-1] if GOT else None)
print("tracebacks:", "Traceback" in plain)
