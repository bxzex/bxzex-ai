import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
LONG = "echo " + "x" * 200 + " ; touch HIDDEN_END_MARK"
N = [0]; GOT = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        GOT.append(body["messages"][-1])
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if body.get("max_tokens") == 1: self.wfile.write(b"data: [DONE]\n\n"); return
        N[0] += 1
        if N[0] == 2:
            d = {"tool_calls": [{"index": 0, "id": "t1", "function": {"name": "run_shell", "arguments": json.dumps({"command": LONG})}}]}
        else: d = {"content": "ok done"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]; os.makedirs(home + "/chats", exist_ok=True)
for i in range(30):
    json.dump({"title": f"chat number {i}", "messages": [{"role": "user", "content": f"chat number {i}"}]}, open(f"{home}/chats/2026-10-{10+i//10:02d}_10-00-{i:02d}.json", "w"))
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
def run(steps):
    pid, fd = pty.fork()
    if pid == 0: os.chdir(home); os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 100, 0, 0))
    out = b""
    for keys, wait in steps:
        if keys: os.write(fd, keys)
        end = time.time() + wait
        while time.time() < end:
            if select.select([fd], [], [], 0.05)[0]:
                try: out += os.read(fd, 65536)
                except OSError: break
    os.waitpid(pid, 0)
    return out.decode("utf-8", "ignore")
o1 = run([(None, 2), (b"\x1b", 1), (b"\x1b[200~line one\r\nline two\x1b[201~\r", 2), (b"run it\r", 2), (b"n", 2),
          (b"/hist\t\r", 1.5), (b"\x1b[B" * 25, 1), (b"\x03", 1), (b"/compa\t", 0.5), (b"\x15", 0.3), (b"exit\r", 2)])
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", o1).replace("─", "")
print("paste kept lines:", any(isinstance(m.get("content"), str) and m["content"] == "line one\nline two" for m in GOT))
print([m.get("content") for m in GOT][:4]); print(re.findall(r"[0-9]+ of [0-9]+|↑↓[^\r\n]{0,70}", plain)[:5])
print("whole long command shown:", "HIDDEN_END_MARK" in plain, "| declined:", any(m.get("content") == "The user declined to run this command." for m in GOT))
print("tab completed /history:", "History" in plain, "| scrolled list:", "of 30" in plain, "| ctrl-c in menu kept app:", "cancelled" in plain)
print("tab /compa ->", "/compact " in plain)
print("tracebacks:", "Traceback" in plain)
o2 = run([(None, 2), (b"\x1b", 1), (b"\x1b[A\x1b[A", 0.8), (b"\x15exit\r", 2)])
print("history across sessions:", "❯ run it" in re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]", "", o2))
