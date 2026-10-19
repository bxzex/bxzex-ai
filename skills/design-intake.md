---
name: design-intake
description: The questions to ask before designing or building anything visual, then a one-page brief to confirm.
---
# Design intake

Do not design from a vague request. Ask first, in one message, using ask_user. If the user already answered some of these, skip them. If they say "you decide", pick a default and state it.

**Questions**
1. **Who is it for?** Role, age range, device, how they find it.
2. **What is the one goal?** The single action a visitor should take (book, buy, sign up, call).
3. **Tone.** Three adjectives (calm, bold, technical, warm, playful). Also one word it must not feel like.
4. **Must-haves.** Content, sections, features, brand colors, logo, legal text.
5. **Things to avoid.** Colors, styles, competitors' looks, words, stock imagery.
6. **References.** Two or three sites or screenshots they like, and what exactly they like about each.
7. **Stack and constraints.** Plain HTML, React, Next.js, an existing repo? Hosting, deadline, browser support.
8. **Success measure.** How will we know it worked (more calls, signups, time on task)?

**Before asking**, look around: `list_files .`, read README and package.json, check for an existing style guide or brand assets. Do not ask what the files already answer.

**Then write the brief** and save it to `BRIEF.md` in the project (or show it in chat if the user did not want files):

```
Audience: ...
Goal: ...
Tone: ... (not: ...)
Must include: ...
Avoid: ...
References: ... (take: ...)
Stack: ...
Success: ...
Open questions: ...
```

Ask the user to confirm or correct it in one reply. Keep the brief under 15 lines. Build only after they agree, and check the result against the brief at the end.
