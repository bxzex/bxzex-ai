---
name: new-skill
description: Writing a new skill file for this assistant so it can be loaded later with use_skill.
---
# Writing a new skill

Skills are plain markdown files the assistant loads on demand. Users keep their own in `~/.bxzex-ai/skills/`. Files placed there are available in every session.

**Format**
```
---
name: kebab-name
description: One sentence saying when to use it.
---
# Title
Instructions.
```
- `name` must match the filename without `.md`.
- The description is what gets matched against a task, so lead with the situation ("Use when deploying...") and keep it to one sentence.

**What makes one useful**
1. **A narrow job.** One topic, one outcome. Split a skill that covers two jobs.
2. **Numbered steps** in the order a person would do them.
3. **Exact commands** with real flags, not "run the build tool". Say what output means success.
4. **Checks.** Tell the assistant how to verify its own work (a curl, a test, a file listing).
5. **Pitfalls.** The 3 to 6 mistakes that actually happen, each with the fix.
6. **Short.** 1200 to 2600 characters. If it needs more, it is two skills.
7. **Plain words.** No filler, no hype. Write like a colleague explaining over a desk.

**Steps to make one**
1. Do the task by hand once, and note which commands worked and which failed.
2. Create the folder if needed: `mkdir -p ~/.bxzex-ai/skills`.
3. Write the file with write_file at `~/.bxzex-ai/skills/<name>.md`.
4. Check the format: `head -4 ~/.bxzex-ai/skills/<name>.md` shows `---`, `name:`, `description:`, `---`. Run `wc -c` and stay in range.
5. **Test it.** Start a fresh session, give a realistic task, and make sure the assistant calls `use_skill` with your name and follows the steps. If it skips the skill, improve the description. If it misfollows, make the step clearer.
6. Remove anything personal such as keys, emails and paths before sharing a skill.
