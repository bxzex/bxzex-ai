---
name: bash-scripting
description: Writing a shell script or a one-line command to automate something in the terminal.
---
# Shell scripts

- Start with `#!/bin/bash` and `set -euo pipefail` so it stops on errors instead of ploughing on.
- Quote every variable: `"$file"`, `"$@"`. Unquoted paths break on spaces.
- Use `$(command)`, not backticks.
- Check what you need exists: `command -v ffmpeg >/dev/null || { echo "ffmpeg is required"; exit 1; }`
- Give variables clear names. Put settings at the top.
- Loop over files safely: `for f in *.jpg; do ...; done`. Never parse the output of `ls`.
- Use `mktemp` for temporary files and clean them up with `trap 'rm -f "$tmp"' EXIT`.
- Send errors to stderr: `echo "problem" >&2`.
- On a Mac the default bash is old (3.2). Avoid associative arrays and `${var,,}`. `sed -i` needs an empty argument: `sed -i '' ...`.

**Safety**
- Anything that deletes or overwrites: print what it would do first, or add a `--dry-run`.
- Never `rm -rf "$dir/"` with a variable that could be empty. Check it first.
- Do not pipe a download straight into a shell without reading it.

**Before handing it over**
- Run `bash -n script.sh` to check the syntax.
- Run it on a small test case and show the output.
- Tell the user how to run it: `chmod +x script.sh && ./script.sh`.

If the job needs real data handling, parsing JSON or more than about fifty lines, write it in Python instead.
