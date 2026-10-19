import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios
def call(name, **a): return {"tool_calls": [{"index": 0, "id": f"c{name}", "function": {"name": name, "arguments": json.dumps(a)}}]}
SCRIPT = [call("update_todos", todos="[x] look around\n[>] ask the user\n[ ] start the job"),
          call("ask_user", question="Which color?", options="red|blue|green"),
          call("run_shell", command="echo job-is-alive; sleep 30", background="true"),
          call("check_job", job="1"),
          call("delegate", task="list the files here"),
          call("list_files", path="."),
          {"content": "helper report: found the files"},
          {"content": "all done"},
          call("write_file", path="x.txt", content="hi"),
          {"content": "plan written"},
          {"content": "hello command ran"}]
GOT = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if body.get("stream") is False:                  # a helper: the whole reply at once
            d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
            msg = {"content": d.get("content", ""), "tool_calls": [{k: v for k, v in t.items() if k != "index"} for t in d.get("tool_calls", [])]}
            b = json.dumps({"choices": [{"message": msg}]}).encode()
            self.wfile.write(b); return
        if not body.get("stream"): return
        GOT.append(body["messages"])
        d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]; os.makedirs(home + "/commands", exist_ok=True)
open(home + "/commands/hello.md", "w").write("Say hello to $ARGUMENTS")
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color")
pid, fd = pty.fork()
if pid == 0: os.chdir(home); os.execve(sys.executable, [sys.executable, sys.argv[1]], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
out = b""
def pump(t):
    global out
    end = time.time() + t
    while time.time() < end:
        if select.select([fd], [], [], 0.05)[0]:
            try: out += os.read(fd, 65536)
            except OSError: return
pump(2); os.write(fd, b"do the thing\r"); pump(2)
os.write(fd, b"\x1b[B"); pump(0.3); os.write(fd, b"\r"); pump(1.5)      # ask_user: pick blue
os.write(fd, b"y"); pump(5)                                            # allow the background job, then the rest runs
os.write(fd, b"\x1b[Z"); pump(0.5); os.write(fd, b"make the file\r"); pump(3)   # shift-tab: plan mode on
os.write(fd, b"/todos\r"); pump(1); os.write(fd, b"/jobs\r"); pump(1); os.write(fd, b"/context\r"); pump(1)
os.write(fd, b"/hello world\r"); pump(2); os.write(fd, b"exit\r"); pump(3)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out.decode("utf-8", "ignore")).replace("─", "")
tools = {m["tool_call_id"]: m["content"] for msgs in GOT for m in msgs if m["role"] == "tool"}
print("todos shown:", "▸ ask the user" in plain and "✓ look around" in plain)
print("ask_user answer:", tools.get("cask_user"))
print("background job:", "job-is-alive" in (tools.get("ccheck_job") or ""), "| still running:", "still running" in (tools.get("ccheck_job") or ""))
print("helper:", "◆ helper 1" in plain and "└ helper 1:" in plain, "| report:", (tools.get("cdelegate") or "")[:40])
print("plan mode blocked write:", "Plan mode is on" in (tools.get("cwrite_file") or ""), "| x.txt exists:", os.path.exists(home + "/x.txt"))
print("/jobs:", "Background jobs" in plain, "| /context:", "% · about" in plain, "| plan status:", "plan mode on (shift+tab to cycle)" in plain)
print("custom /hello:", any(m.get("content") == "Say hello to world" for msgs in GOT for m in msgs))
print("tracebacks:", "Traceback" in plain)
