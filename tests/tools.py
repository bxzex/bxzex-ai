import sys, os
src = open(sys.argv[1]).read()
src = src[:src.index("# ---- installer helpers ----")]
g = {"__name__": "x", "__file__": sys.argv[1]}
exec(compile(src, "bxzex-ai", "exec"), g)
ok = g["only_looks"]
for cmd, want in [('ls -la ~/trader/*.py && echo "---" && wc -l ~/trader/*.py', True), ("git status", True), ("cat a | grep x | head", True),
                  ("rm -rf x", False), ("ls > out.txt", False), ("echo $(rm x)", False), ("ls; rm x", False), ("ls & rm x", False),
                  ("find . -delete", False), ("find . -exec rm {} ;", False), ("git push", False), ("git branch -D x", False),
                  ("sort -o f x", False), ("rg --pre sh x", False), ("FOO=1 ls", False), ("python3 x.py", False), ("cat `rm x`", False),
                  ("git diff --output=x", False), ("tree -o f", False), ("grep -o foo x", True)]:
    assert ok(cmd) == want, (cmd, ok(cmd))
print("only_looks: all 20 right")
d = os.path.join(sys.argv[2], "proj"); os.makedirs(d + "/src", exist_ok=True); os.makedirs(d + "/node_modules/z", exist_ok=True)
open(d + "/src/a.py", "w").write("def hi():\n    return 1\n\ndef bye():\n    return 1\n")
open(d + "/node_modules/z/x.js", "w").write("junk")
g["allow_all"] = True
print(g["list_files"](d))
print(g["search_files"]("return", d))
print(g["edit_file"](d + "/src/a.py", "return 1", "return 2"))
print(g["edit_file"](d + "/src/a.py", "def hi():\n    return 1", "def hi():\n    return 2"))
print(g["edit_file"](d + "/src/a.py", "nope", "x"))
print(g["changes"]("a\nb\nc\n", "a\nB\nc\n"))
print(open(d + "/src/a.py").read())
g["undo"](); print(open(d + "/src/a.py").read())
print(g["attach_files"](f"explain @{d}/src/a.py please")[-60:])
print(g["run_tool"]({"function": {"name": "read_file", "arguments": "[1,2]"}}))

# edits that forgive spacing, say where the closest lines are, and check the result
import tempfile, shutil
d = tempfile.mkdtemp(dir=os.path.realpath("/tmp")); os.makedirs(d + "/src")     # the test home sits under /var on a Mac, where every change asks
f = d + "/src/b.py"; open(f, "w").write("class A:\n    def hi(self):\n        x = 1\n        return x\n")
print("loose:", g["edit_file"](f, "def hi(self):\n    x = 1\n    return x", "def hi(self):\n    x = 2\n    return x"))
print("loose kept indent:", open(f).read() == "class A:\n    def hi(self):\n        x = 2\n        return x\n")
print("nearest:", "3│" in g["edit_file"](f, "x = 22 ", "x = 3") or "closest" in g["edit_file"](f, "xx = 2", "x = 3"))
print("syntax caught:", "syntax error" in g["edit_file"](f, "x = 2", "x = (2"))
print("syntax fine:", "syntax error" not in g["edit_file"](f, "x = (2", "x = 2"))
print("json caught:", "syntax error" in g["write_file"](d + "/c.json", "{bad"))
# a working helper changes its own copy; the real file changes only when kept
over = {}
print("helper edit:", g["helper_file"]("edit_file", {"path": f, "old_text": "x = 2", "new_text": "x = 5"}, over)[:6] == "edited")
print("real untouched:", "x = 2" in open(f).read())
print("helper reads own copy:", "x = 5" in g["helper_file"]("read_file", {"path": f}, over))
g["helper_file"]("write_file", {"path": d + "/src/new.py", "content": "y = 1\n"}, over)
print("kept:", "saved" in g["keep_helper_changes"](1, over), "x = 5" in open(f).read(), os.path.exists(d + "/src/new.py"))
over = {}; g["helper_file"]("edit_file", {"path": f, "old_text": "x = 5", "new_text": "x = 6"}, over); open(f, "a").write("# moved on\n")
print("stale skipped:", "Not kept" in g["keep_helper_changes"](1, over), "x = 5" in open(f).read())
print("helper blocked from ssh:", g["helper_file"]("write_file", {"path": "~/.ssh/x", "content": "k"}, {})[:5] == "error")
# the terminal takes the newer copy of its chat that the remote saved, but never throws away its own unsaved lines
import json
cf = d + "/chat.json"; base = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
g["history"] = list(base); g["chat_file"] = cf; open(cf, "w").write(g["chat_data"]()); g["last_saved"] = g["chat_data"]()
print("nothing new:", g["sync_chat"]() == 0)
g2 = dict(g); newer = base + [{"role": "user", "content": "from the phone"}, {"role": "assistant", "content": "done on the phone"}]
open(cf, "w").write(json.dumps({"title": "hi", "messages": newer}))
print("picked up the remote's turns:", g["sync_chat"]() == 2 and g["history"][-1]["content"] == "done on the phone")
g["history"].append({"role": "user", "content": "typed here, not saved yet"})
open(cf, "w").write(json.dumps({"title": "hi", "messages": base}))
print("own unsaved lines kept:", g["sync_chat"]() == 0 and g["history"][-1]["content"].startswith("typed here"))
# the terminal and the remote both saving one chat: neither loses the other's turns
g["CHATS"] = d + "/chats"; cf2 = d + "/chats/c.json"; os.makedirs(d + "/chats", exist_ok=True)
g["history"][:] = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}]; g["chat_file"] = cf2; g["last_saved"] = None
g["save_chat"]()
other = json.loads(open(cf2).read())["messages"] + [{"role": "user", "content": "from phone"}, {"role": "assistant", "content": "phone reply"}]
open(cf2, "w").write(json.dumps({"title": "a", "messages": other}))
g["history"].append({"role": "user", "content": "from keyboard"})
g["save_chat"](merge=False); print("autosave leaves the newer copy alone:", len(json.loads(open(cf2).read())["messages"]) == 4)
g["save_chat"](); got = [m["content"] for m in json.loads(open(cf2).read())["messages"]]
print("both kept:", got == ["a", "b", "from phone", "phone reply", "from keyboard"] and [m["content"] for m in g["history"]] == got)
shutil.rmtree(d)
