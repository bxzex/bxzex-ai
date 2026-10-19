---
name: ux-critique
description: Giving an honest designer's opinion on a page or screen when someone asks what you think of it.
---
# UX critique

This is an opinion, not a checklist audit. Be direct and kind, and always give reasons.

1. **Look first.** Read the code with read_file, or screenshot it if a headless browser exists (`npx playwright screenshot URL out.png`). Look at the top screen on mobile and desktop before you form a view.
2. **Ask what it is trying to do.** If the purpose is unclear, use ask_user once. Otherwise infer it from the page and say your assumption.
3. **Write exactly this structure:**

**Three things that work**
Name the specific element (the headline, the spacing around the form, the photo) and why it works for this audience. Skip generic praise like "clean design".

**Three things that do not**
Name the element, say what the visitor experiences because of it, and what to do instead. Rank the worst first. Examples: a headline that describes the company instead of the benefit, a low-contrast button, five competing calls to action.

**One bigger move**
A single change that would improve the page more than all small fixes together. It might be cutting half the sections, rewriting the headline around the customer's problem, or replacing stock imagery with real work. Explain the reasoning and what it costs.

**Rules**
- Judge against the page's goal, not your taste. A loud page can be right for a loud brand.
- Every claim needs evidence you can point to.
- No hedging chains ("it might perhaps be worth considering"). Say what you think.
- Do not edit files unless asked. Finish by offering to apply the bigger move.
