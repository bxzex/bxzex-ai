---
name: refactor-simplify
description: Simplifying or cleaning up working code safely, with behavior kept identical.
---
# Refactor and simplify

A refactor changes structure, not behavior. If behavior must change, that is a separate step.

1. **Get a baseline.** Run the tests and the build now and write down the result. If there are no tests, write a few that pin down the current behavior of the code you will touch (see the testing skill) or at least save sample outputs to compare.
2. **Read before you cut.** Open the target file fully. Find every caller: `grep -rn "functionName" --include=*.py --include=*.ts .` Also check for dynamic uses (strings, config files, exports, reflection).
3. **Commit a clean starting point** so each step can be undone with `git diff` or `git checkout -- file`.
4. **Work in small steps,** one kind of change at a time, running tests after each:
   - Delete dead code: unused functions, variables, imports, commented-out blocks. Confirm with grep that nothing references them.
   - Rename vague names (`data`, `tmp`, `doStuff`) to what they hold or do. Rename in all places at once.
   - Flatten nesting with early returns.
   - Extract a function when a block has a clear name and is used twice or is hard to read inline.
   - Merge duplicated code, but only when the copies really mean the same thing.
   - Replace clever one-liners with plain code.
5. **Do not mix in** new features, formatting of untouched files, dependency upgrades or style changes across the repo. They hide real changes in the diff.
6. **Run the checks after every step:** tests, linter, type checker, build. If something fails, undo that step and make it smaller.
7. **Review the diff** with `git diff --stat` and `git diff`. Every changed line should be explainable as "same behavior, simpler".

Pitfalls:
- Removing code that looks unused but is called by name from a template or config.
- Changing a function signature that other packages or scripts call.
- Making an abstraction for a single use. Three similar lines beat a premature helper.
- Changing error messages, log text or output formats that something else parses.

Finish by telling the user what you removed, renamed and merged, and the test result before and after.
