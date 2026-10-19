import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        for t in ["Sure, ", "**done**."]:
            self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': t}}]})}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=sys.argv[2], BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0:
    os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.1)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
for keys, wait in [(None, 4), (b"!echo hello-from-shell\r", 2), (b"/allow\r", 1), (b"/undo\r", 1), (b"hi there\r", 3), (b"/compact\r", 2), (b"\x03", 1), (b"\x03", 2)]:
    if keys: os.write(fd, keys)
    pump(wait)
txt = re.sub(rb"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", b"", out).decode("utf-8", "ignore")
for want in ["hello-from-shell", "exit code 0", "always allow on", "nothing to undo", "done", "press ctrl-c again"]:
    print(("OK  " if want in txt else "MISSING ") + want)
print("Traceback" in txt and "TRACEBACK FOUND" or "no tracebacks")
print("exited:", os.waitpid(pid, os.WNOHANG))
