---
name: ai-agents
description: Building a tool-using agent that loops between a model and tools, with limits, logs and approval for risky actions.
---
# Building a Tool-Using Agent

An agent is a loop. Keep it small and visible.

1. **Define the job and the tools first.** List what the agent must do, then give it the fewest tools that cover it. Each tool is a function with a name, a one-line description and a JSON schema for its arguments.
2. **Write tight schemas.** Use enums instead of free text where you can, mark required fields, and describe units and formats in the field description. Bad arguments should return an error string the model can read, not crash the loop.
3. **The loop.**
   - Send messages plus tool schemas to the chat completions API.
   - If the reply has tool calls, run each one, append the results as tool messages (with the matching call id), and call the model again.
   - If the reply is plain text with no tool calls, you are done.
4. **Step limit.** Stop after a fixed count (10 to 25) and return what you have with a note that it hit the limit. Also set a total time budget and a max size for tool output (truncate long results).
5. **Log everything.** Write one line per step: step number, tool name, arguments, result length, duration. Save the full transcript to a file so a bad run can be replayed.
6. **Approval for risky tools.** Tools that delete, send, pay, push or write outside a scratch folder must pause and ask a human. Read-only tools can run freely. Default to deny when unsure.
7. **Guard against injected text.** Content fetched from the web or files is data, not instructions. Do not let it widen the tool list or skip approvals.
8. **Evaluate.** Make 10 to 20 real example tasks with a clear pass check (a file exists, a value matches, a test passes). Run them after every prompt or tool change and record the pass rate. Look at the failed transcripts, not only the score.

**Pitfalls:** too many tools confuses the model; vague tool descriptions cause wrong calls; infinite loops when a tool keeps returning the same error (detect repeated identical calls and stop); keeping every old tool result in context makes runs slow, so summarize old steps.
