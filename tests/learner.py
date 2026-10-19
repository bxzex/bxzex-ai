import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
SYS = []; LEARN = [0]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        last = body["messages"][-1]["content"]
        if body["messages"][0]["role"] == "system": SYS.append(body["messages"][0]["content"])
        if not body.get("stream"):
            LEARN[0] += 1
            LEARN[0] += 1
            b = json.dumps({"choices": [{"message": {"content": "- He sells his old MacBook and iPhone to raise cash.\n- He likes dark design."}}]}).encode()
            self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': 'ok'}}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]
open(home + "/about.md", "w").write("# About me\nMy name is Test Person.\n")
open(home + "/memory.md", "w").write("- He likes dark design.\n")
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
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
pump(2)
for m in [b"im selling my macbook\r", b"and my iphone too\r", b"for cash today\r"]: os.write(fd, m); pump(1.5)
before = LEARN[0]; pump(5); early = LEARN[0] > before
pump(20); os.write(fd, b"ok next\r"); pump(2)
os.write(fd, b"exit\r"); pump(2)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]", "", out.decode("utf-8", "ignore"))
print("about.md in prompt:", "Test Person" in SYS[0], "| knows-you line:", "you know them" in SYS[0])
print("memory.md now:", open(home + "/memory.md").read().splitlines())
print("waited for idle (not right after the reply):", not early)
print("shown to user:", re.findall(r"remembered [0-9]+ new thing[^\r\n(]*", plain))
