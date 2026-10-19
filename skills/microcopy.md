---
name: microcopy
description: Writing or fixing the small text in an interface: buttons, labels, helper text, empty states, errors, loading and success messages.
---
# Microcopy

Small text decides whether people feel guided or lost. Make each string say what happened and what to do next.

**Find the strings first.** `grep -rnE "Submit|Error|Something went wrong|Loading|No (data|results)" src/` and read the matches.

**Buttons**
- Verb plus object: "Save changes", "Send invoice", "Create account". Never "Submit", "OK", "Click here".
- Destructive buttons name the loss: "Delete project". Cancel is "Keep editing" if cancel is ambiguous.

**Labels and helper text**
- Labels are nouns, always visible ("Email address"). Placeholders show an example, not the label.
- Helper text says the rule before the mistake: "At least 8 characters."

**Errors** (three parts: what happened, why if known, how to fix)
- Bad: "Invalid input." Good: "That email is missing an @. Check it and try again."
- Never blame the user. Never show raw codes without a plain sentence next to them.
- Put it next to the field. Keep what they typed.

**Empty states**
- Say what goes here and give the first action: "No invoices yet. Create your first invoice."

**Loading and success**
- Loading: say what is happening ("Saving...", "Finding nearby stores") and only show it after about 300ms.
- Success: confirm the result with specifics: "Invoice 1042 sent to ana@example.com."

**Style**
- Sentence case. Short words. Under 8 words where possible.
- Same term for the same thing everywhere (pick "project" or "workspace", not both).
- No exclamation marks, no "Oops", no jokes on error screens.

**Output.** Give a before and after table of each string with the file and line, then apply the edits with edit_file.
