import sys, os, threading, json, http.server, socket
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        b = json.dumps({"data": [{"id": "m"}]}).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.send_header("Content-Length", "100000"); self.end_headers()
        ev = {"choices": [{"delta": {"content": "Hello there, partial"}}]}
        self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode()); self.wfile.flush()
        self.connection.shutdown(socket.SHUT_RDWR)          # drop mid-reply
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ["BXZEX_REMOTE"] = f"http://127.0.0.1:{srv.server_port}"
src = open(sys.argv[1]).read(); src = src[:src.index("# ---- installer helpers ----")]
g = {"__name__": "x", "__file__": sys.argv[1]}
exec(compile(src, "bxzex-ai", "exec"), g)
g["refresh_system"]()
guide = open(os.environ["BXZEX_HOME"] + "/BXZEX.md").read()
assert guide.startswith("# BXZEX AI") and guide.rstrip().endswith("ALWAYS SAY YO") and "/undo" in guide, guide[-300:]
print("guide upgraded, user's line kept")
h = [{"role": "user", "content": "hi"}]
g["run_turn"](h)
print("survived drop; history:", h[-1])
