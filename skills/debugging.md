---
name: debugging
description: Something is broken (code, a command, a build, a config) and the cause is not yet known.
---
# Debugging

Find the cause before you change anything.

1. **Get the real error.** Run the thing and read the whole message, including the first error, not just the last line. Read the log file if there is one.
2. **Reproduce it** with the smallest command that still fails.
3. **Look at what is actually there.** Read the file, print the value, check the version, list the directory. Do not reason from what should be true.
4. **One guess at a time.** State the guess, state what you would see if it were right, then check exactly that.
5. **Change one thing**, then run it again. If it did not help, undo it before trying the next idea.
6. **Confirm the fix** by running the original failing command, not a different one.

Common causes worth checking early: wrong working directory, wrong version of a tool, a missing environment variable, a stale cache or build, a typo in a path, a port already in use, file permissions.

Rules:
- Never say it is fixed until you have seen it work.
- Do not delete, reset or reinstall things to make an error go away unless the user agrees.
- If you are stuck after three attempts, stop and tell the user what you tried and what you saw.
