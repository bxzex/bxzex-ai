---
name: code-review
description: Reviewing code or a diff for bugs and problems before it ships.
---
# Code review

Read all of it before judging any of it. Understand what the change is for.

**Look for, in this order**
1. **Wrong behavior.** Does it do what it claims? Walk through it with a real input, then an empty one, then a huge one, then a malformed one.
2. **Edges.** Null or missing values, empty lists, zero, negative numbers, duplicate entries, off-by-one in loops and slices.
3. **Failure paths.** What happens when the network call fails, the file is missing, the user double-clicks? Are errors swallowed silently?
4. **Security.** User input reaching SQL, a shell, HTML or a file path without being checked. Secrets in code or logs. Missing permission checks.
5. **Data safety.** Anything that deletes, overwrites or migrates. Is it reversible?
6. **Concurrency.** Two requests at once, shared state, race between check and use.
7. **Clarity.** Names that lie, dead code, a function doing three jobs, a comment that disagrees with the code.

**How to report**
- Most serious first. For each: the file and line, what goes wrong, a concrete input that triggers it, and a suggested fix.
- Separate "this is a bug" from "I would do it differently". Say which is which.
- If you did not run it, say so. Do not claim something is broken unless you can show the path that breaks it.
- If it is fine, say it is fine. Do not invent problems to look thorough.
