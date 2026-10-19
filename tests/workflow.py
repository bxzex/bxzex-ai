import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios, subprocess
# hooks that block and follow tools, helpers side by side, ctrl-r, scheduled tasks, /commit
def call(*calls): return {"tool_calls": [{"index": i, "id": f"c{n}{i}", "function": {"name": n, "arguments": json.dumps(a)}} for i, (n, a) in enumerate(calls)]}
SCRIPT = [{"content": "ok cats"},
          call(("run_shell", {"command": "echo forbidden thing"})),
          call(("write_file", {"path": "a.txt", "content": "hi"})),
          call(("delegate", {"task": "alpha research"}), ("delegate", {"task": "beta research"})),
          {"content": "all done"},
          {"content": "again"},
          call(("schedule_task", {"when": "weekdays 9am", "task": "check the weather", "name": "Weather"})),
          {"content": "scheduled it"},
          {"content": "committed"},
          {"content": "sunny report"}]
GOT = []; SPANS = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if body.get("stream") is False:                  # a helper: answers after a while, so two at once overlap
            t = time.time(); time.sleep(1.5)
            task = body["messages"][1]["content"].split()[0]
            SPANS.append((t, time.time()))
            self.wfile.write(json.dumps({"choices": [{"message": {"content": f"report on {task}"}}]}).encode()); return
        if not body.get("stream"): return
        GOT.append(body["messages"])
        d = SCRIPT.pop(0) if SCRIPT else {"content": "extra"}
        self.wfile.write(f"data: {json.dumps({'choices': [{'delta': d}]})}\n\ndata: [DONE]\n\n".encode())
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
home = sys.argv[2]
json.dump({"hooks": [{"on": "before", "tool": "run_shell", "run": "echo \"$BXZEX_COMMAND\" | grep -q forbidden && echo no forbidden things && exit 1; exit 0"},
                     {"on": "after", "tool": "write_file|edit_file", "run": "echo formatted $(basename \"$BXZEX_FILE\")"}]}, open(home + "/config.json", "w"))
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=home, BXZEX_NO_UPDATE="1", TERM="xterm-256color", BXZEX_NO_TICKER="1")
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
pump(2); os.write(fd, b"first message about cats\r"); pump(1.5)
os.write(fd, b"go\r"); pump(2); os.write(fd, b"y"); pump(5)              # allow the write; the hook follows it; then two helpers
os.write(fd, b"\x12"); pump(0.3); os.write(fd, b"cats"); pump(0.5)       # ctrl-r cats
shown = out.decode("utf-8", "ignore")
os.write(fd, b"\r"); pump(0.3); os.write(fd, b"\r"); pump(1.5)           # take the match, then send it
os.write(fd, b"remind me\r"); pump(2); os.write(fd, b"y"); pump(2)        # schedule it
os.write(fd, b"/commit\r"); pump(1.5); os.write(fd, b"/hooks\r"); pump(1); os.write(fd, b"/export\r"); pump(1)
os.write(fd, b"/schedule\r"); pump(1); os.write(fd, b"\x1b"); pump(0.5); os.write(fd, b"exit\r"); pump(3)
plain = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out.decode("utf-8", "ignore")).replace("─", "")
tools = {m["tool_call_id"]: m["content"] for msgs in GOT for m in msgs if m["role"] == "tool"}
users = [m["content"] for msgs in GOT for m in msgs if m["role"] == "user" and isinstance(m["content"], str)]
print("before-hook blocked:", "no forbidden things" in (tools.get("crun_shell0") or ""), "| no question for it:", plain.count("Allow:") == 2)
print("after-hook ran:", "formatted a.txt" in (tools.get("cwrite_file0") or ""))
print("helpers:", tools.get("cdelegate0"), "/", tools.get("cdelegate1"))
print("side by side:", len(SPANS) == 2 and SPANS[1][0] < SPANS[0][1])
print("ctrl-r status:", "search past messages: cats" in re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", shown), "| sent again:", users.count("first message about cats") >= 2)
sched = json.load(open(home + "/schedules.json")) if os.path.exists(home + "/schedules.json") else []
print("scheduled:", [(s["name"], s.get("days"), s.get("at")) for s in sched])
print("/commit:", any("Commit my changes" in u for u in users), "| /hooks:", "Hooks" in plain and "/hooks remove 1" in plain)
import glob
exported = glob.glob(home + "/bxzex-chat-*.md")
print("/export:", bool(exported) and "**You:** first message about cats" in open(exported[0]).read())
print("/schedule:", "Scheduled tasks" in plain and "Weather" in plain)
r = subprocess.run([sys.executable, sys.argv[1], "--run-schedule", "s1"], env=env, capture_output=True, text=True, timeout=60, cwd=home)
done = json.load(open(home + "/schedules.json"))[0]
print("scheduled run:", "sunny report" in open(done["result"]).read() if done.get("result") else False, "| marked new:", done.get("seen") is False)
print("tracebacks:", "Traceback" in plain or "Traceback" in r.stdout + r.stderr)
if not done.get("result"): print(r.stdout[-1500:], r.stderr[-1500:], done)
