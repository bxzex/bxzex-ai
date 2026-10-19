import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
SLOW = [3.0]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        time.sleep(SLOW[0])
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': 'ok done'}}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]; os.makedirs(home + "/chats", exist_ok=True)
json.dump({"title": "my old chat about trading", "messages": [{"role": "user", "content": "my old chat about trading"}, {"role": "assistant", "content": "sure"}]},
          open(home + "/chats/2026-10-18_22-00-00.json", "w"))
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0: os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
def send(b, gap=0.03):
    if 'whole' == 'whole': os.write(fd, b); pump(0.2); return
    for i in range(len(b)):
        os.write(fd, b[i:i+1]); pump(gap)
pump(1.0); send(b"\x1b[A\x1b[B\x1b[C\x08\x7f")   # arrows and delete while it is still starting (slow server)
pump(6)
mark = len(out)
send(b"\x1b[B"); send(b"\r"); pump(1.5)            # menu: down to New chat, enter
menu_part = out[mark:]
SLOW[0] = 2.0
send(b"hello\r"); pump(0.3); send(b"So lets \x1b[A\x1b[D\x08\x08"); pump(5)   # type during the wake gap of a turn
send(b"\x7f\x7f\x7f"); pump(0.5); send(b"\x1b[1;3D"); send(b"X"); pump(0.5); send(b"\r"); pump(4)
send(b"exit\r"); pump(2)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out.decode("utf-8", "ignore")).replace("─", "")
print("raw ^[ or ^H echoed:", "^[" in plain or "^H" in plain)
print("menu shown:", "Where do you want to start?" in plain, "| new chat picked:", "New chat · /history" in plain)
print("sent lines:", re.findall(r"❯\x1b\[0m \x1b\[1m([^\x1b]*)", out.decode("utf-8", "ignore")))
print("Traceback" in plain and "TRACEBACK" or "no tracebacks")
print(re.findall(r"❯ [^\r\n]{0,30}|stopped[^\r\n]{0,40}|ok done", plain)[-30:])
