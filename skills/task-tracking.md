---
name: task-tracking
description: Keeping a todo list with update_todos on multi-step work so progress stays clear and nothing is forgotten.
---
# Tracking Tasks with update_todos

Use the list for work that has several steps or touches several files. Skip it for a one-command job.

1. **Write the list early.** Before the first change, break the job into 3 to 8 steps. Each step is a concrete action with a result you can check:
   - Good: "Add /api/health route and test with curl", "Update README install section".
   - Too vague: "Fix the backend". Too small: "open file".
2. **Order by dependency.** Put the step that unblocks others first. Put verification (build, tests, curl) as its own last step so it does not get skipped.
3. **One in progress at a time.** Set exactly one item to in progress when you start it. If you are juggling two, you are not tracking, you are guessing.
4. **Tick off as you finish**, right after the step is verified, not in a batch at the end. A step is done only when you have seen it work (command output, test pass, page loads).
5. **Add what you discover.** If you find a missing config, a failing test or a needed migration, add it as a new step instead of holding it in your head. Remove a step if it turns out unnecessary, and say so.
6. **Keep it honest.** If a step is blocked (needs the user, a login, a secret), mark it clearly and move to the next independent step. Do not mark blocked work as done.
7. **Resend the full list on every update.** The tool replaces the whole list, so include every item with its current state.
8. **Finish with a check.** Before the final reply, read the list: nothing should be pending or in progress without a reason. Mention leftover items to the user.

**Example start:** 1 Read current routes (in progress), 2 Write the new route, 3 Add tests, 4 Run build and tests, 5 Summarize changes.

**Pitfalls:** a list of 20 tiny items (merge them); never updating it so it lies; marking a step done after writing code but before running it; rewriting step names every update.
