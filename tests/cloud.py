import sys, os, threading, json, http.server, pty, time, select, re, struct, fcntl, termios, stat
# /cloud end to end against a stand-in for Modal's tool and for curl: login, card pick, key, model copy, deploy, first wake.
app, home, repo = sys.argv[1], sys.argv[2], sys.argv[3]
fake = os.path.join(home, "fakebin"); os.makedirs(fake)
log = os.path.join(home, "modal.log")
def script(name, text):
    p = os.path.join(fake, name)
    with open(p, "w") as f: f.write(text)
    os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
script("modal", f'''#!/usr/bin/env python3
import sys, os, json
a = sys.argv[1:]; mark = {json.dumps(home)} + "/logged-in"
with open({json.dumps(log)}, "a") as f: f.write(json.dumps([a, os.environ.get("MODAL_PROFILE", ""), os.getcwd()]) + "\\n")
if a[:2] == ["profile", "list"]:
    print(json.dumps([{{"name": "neo", "workspace": "neo", "active": True}}] if os.path.exists(mark) else []))
elif a[:2] == ["token", "new"]:
    print("If it didn't, please copy this URL into your web browser manually:"); print("https://modal.com/token-flow/tf-test")
    open(mark, "w").close(); print("Token verified successfully!")
elif a[:2] == ["secret", "create"]:
    print(json.dumps(json.load(open(a[a.index("--from-json") + 1]))), file=open({json.dumps(home)} + "/secret.json", "w"))
elif a[:2] == ["run", "cloud.py::fetch"]: print("already there")
elif a[:2] == ["deploy", "cloud.py"]: print("└── https://neo--bxzex-ai-gpu-engine.us-east.modal.run (unauthenticated)")
''')
script("curl", f'''#!/bin/bash
case "$*" in *modal.run*) cat > {home}/wake-headers; echo '{{"object":"list","data":[{{"id":"m"}}]}}' ;; *) exec /usr/bin/curl "$@" ;; esac
''')

def drive(args, env, steps):
    pid, fd = pty.fork()
    if pid == 0: os.execve(sys.executable, [sys.executable, app, *args], env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 110, 0, 0))
    out = b""
    def pump(t):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            if select.select([fd], [], [], 0.05)[0]:
                try: out += os.read(fd, 65536)
                except OSError: return
    for wait, keys in steps:
        pump(wait)
        if keys: os.write(fd, keys)
    pump(3)
    return re.sub(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[78]|\x1b\]8;;[^\x1b]*\x1b\\\\", "", out.decode("utf-8", "ignore")).replace("─", "")

env = dict(os.environ, BXZEX_HOME=home, BXZEX_MODAL=os.path.join(fake, "modal"), BXZEX_UPDATE_URL="file://" + repo,
           PATH=fake + ":" + os.environ["PATH"], TERM="xterm-256color")
env.pop("BXZEX_REMOTE", None); env.pop("BXZEX_REMOTE_KEY", None)
with open(os.path.join(home, "config.json"), "w") as f: json.dump({"size": "cloud"}, f)
plain = drive(["--cloud"], env, [(4, b"\x1b[B"), (1, b"\r"), (4, None)])      # second card in the list: A100-80GB
conf = json.load(open(os.path.join(home, "config.json")))
secret = json.load(open(os.path.join(home, "secret.json"))) if os.path.exists(os.path.join(home, "secret.json")) else {}
calls = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
print("login link shown:", "modal.com/token-flow/tf-test" in plain)
print("ready:", "Your cloud card is ready" in plain)
print("address saved:", conf.get("remote") == "https://neo--bxzex-ai-gpu-engine.us-east.modal.run")
print("key saved matches the card's:", bool(secret.get("ENGINE_KEY")) and conf.get("remote_key") == secret.get("ENGINE_KEY"))
print("key never on a command line:", bool(secret) and not any(secret["ENGINE_KEY"] in json.dumps(c) for c in calls))
print("card picked:", conf.get("cloud", {}).get("card") == "A100-80GB" and 'GPU = "A100-80GB"' in open(os.path.join(home, "cloud", "cloud.py")).read())
print("cost wired:", conf.get("cost") == {"app": "bxzex-ai-gpu", "profile": "neo"})
print("account used for every step:", all(p == "neo" for a, p, _ in calls if a[0] in ("secret", "run", "deploy")))
print("first wake sent the key:", os.path.exists(os.path.join(home, "wake-headers")) and secret.get("ENGINE_KEY", "-") in open(os.path.join(home, "wake-headers")).read())
print("config private:", oct(os.stat(os.path.join(home, "config.json")).st_mode & 0o777) == "0o600")

# inside the app: /cloud shows the card, and /cloud off can't leave a cloud-only install without a model
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
conf["remote"] = f"http://127.0.0.1:{srv.server_port}"
with open(os.path.join(home, "config.json"), "w") as f: json.dump(conf, f)
env["BXZEX_NO_UPDATE"] = "1"
plain = drive([], env, [(4, b"/cloud\r"), (1, b"/cloud off\r"), (1, b"/cloud nonsense\r"), (1, b"exit\r")])
print("status shows the card:", "A100-80GB in your Modal account neo" in plain)
print("off refused on cloud-only:", "no model of its own" in plain)
print("unknown word explained:", "/cloud login uses another Modal account" in plain)
print("tracebacks:", "Traceback" in plain)
