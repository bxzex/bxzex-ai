import sys, os, threading, json, http.server, pty, time, select, struct, fcntl, termios, re, shutil
# shift-tab cycles the mode in the footer; a new release shows up in the footer with a ping and "new:" after the switch
app, home, upd = sys.argv[1], sys.argv[2], sys.argv[3]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"])); self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(b'data: {"choices":[{"delta":{"content":"ok"}}]}\n\ndata: [DONE]\n\n')
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
open(upd + "/WHATSNEW", "w").write("9.9.9: a test release line\n")
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, TERM="xterm-256color",
           BXZEX_UPDATE_URL="file://" + upd, BXZEX_UPDATE_EVERY="3")
real_version = open(upd + "/VERSION").read(); open(upd + "/VERSION", "w").write("0.0.1 2")      # nothing new at first
pid, fd = pty.fork()
if pid == 0: os.chdir(home); os.execve(sys.executable, [sys.executable, app], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 140, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
plain = lambda: re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]", "", out.decode("utf-8", "ignore"))
pump(3); a = len(plain())
os.write(fd, b"\x1b[Z"); pump(0.6); plan = "plan mode on (shift+tab to cycle)" in plain()[a:]; a = len(plain())
os.write(fd, b"\x1b[Z"); pump(0.6); allow = "always allow on (shift+tab to cycle)" in plain()[a:]; a = len(plain())
os.write(fd, b"\x1b[Z"); pump(0.6); back = "shift+tab for modes" in plain()[a:]
print("shift-tab: plan:", plan, "| always allow:", allow, "| back to asking first:", back)
open(upd + "/VERSION", "w").write(real_version)                 # now a release comes out
pump(9)
print("footer says new update:", "new update released: v9.9.9" in plain(), "| ping:", b"\x07" in out)
print("after the switch:", "Updated to v9.9.9" in plain(), "| what's new line:", "new: a test release line" in plain())
os.write(fd, b"exit\r"); pump(2)
print("tracebacks:", "Traceback" in plain())
