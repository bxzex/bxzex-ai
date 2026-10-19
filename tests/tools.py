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
