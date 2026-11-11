import sys, os, threading, json, http.server, subprocess
seen = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        seen.append(self.rfile.read(int(self.headers["Content-Length"])).decode())
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        for t in ["Sure, ", "**done**."]:
            self.wfile.write(f"data: {json.dumps({'choices': [{'delta': {'content': t}}]})}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, BXZEX_REMOTE=f"http://127.0.0.1:{srv.server_port}", BXZEX_HOME=sys.argv[2], BXZEX_NO_UPDATE="1", TERM="xterm-256color")
# piped both ways: only the answer comes out, and what was piped in reaches the model
r = subprocess.run([sys.executable, sys.argv[1], "-p", "sum this up"], input="PIPED-TEXT-123", capture_output=True, text=True, env=env, timeout=60)
print("answer only:", r.stdout == "Sure, **done**.\n")
print("no working lines:", "\033" not in r.stdout and "\r" not in r.stdout)
print("exit 0:", r.returncode == 0)
print("piped text sent:", any("PIPED-TEXT-123" in s and "sum this up" in s for s in seen))
r = subprocess.run([sys.executable, sys.argv[1], "-p"], input="", capture_output=True, text=True, env=env, timeout=60)
print("nothing asked, exit 2:", r.returncode == 2 and "usage" in r.stderr)
print("no tracebacks" if "Traceback" not in r.stderr else "TRACEBACK FOUND")
