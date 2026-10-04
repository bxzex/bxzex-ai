---
name: python-scripting
description: Writing a Python script to automate a task, process files or crunch data.
---
# Python scripts

- Use only the standard library unless the user already has the package. Check with `python3 -c "import name"` before relying on it.
- Start the file with `#!/usr/bin/env python3` and a one-line docstring saying what it does and how to run it.
- Put the work in functions and call them from `if __name__ == "__main__":`.
- Take inputs from the command line with `argparse`, not edited constants.
- Use `pathlib.Path` for paths and `with open(...)` for files. Always pass `encoding="utf-8"`.
- For CSV use the `csv` module, for JSON the `json` module. Do not parse them by hand.
- Fail loudly with a clear message: say which file or value was the problem.
- Never overwrite the input file. Write to a new one and say where.
- For anything that deletes or renames, add a `--dry-run` that prints what it would do, and run that first.
- Print progress for long jobs so it is clear it has not hung.

After writing it, run it on a small real example and show the output. If it fails, read the full traceback, fix the cause and run it again. Do not hand over a script you have not run.
