---
name: ux-audit
description: Running a full UX review of a page or flow and reporting findings ranked by severity with a fix for each.
---
# UX audit

1. **Get the real thing.** Open the page (or run `npm run dev` and curl it). Read the HTML and CSS with read_file. Review at 375px and 1440px wide.
2. **First impression (5 seconds).** What is this, who is it for, what do I do next? If you cannot answer from the top screen, that is a finding.
3. **Navigation.** Can a visitor reach the main task in two clicks? Is the current page marked? Does the logo link home? Are labels plain words?
4. **Hierarchy.** One primary action per screen. Headings in order (one h1). Is the most important thing the biggest or highest contrast?
5. **Forms.** Every input has a visible label, correct `type` and `autocomplete`. Errors appear next to the field, say what to fix, and keep what the user typed. Required fields marked. Submit button names the action.
6. **Feedback states.** Loading, empty, error and success exist for every data view. Buttons show progress after click.
7. **Mobile.** No horizontal scroll, tap targets 44px or more, text 16px or more, sticky bars not covering content.
8. **Speed.** Run `curl -s -o /dev/null -w "%{time_total}s %{size_download}B\n" URL`. Look for huge images, render-blocking scripts, layout shift.
9. **Accessibility.** Contrast 4.5:1, visible focus ring, alt text, keyboard-only pass with Tab, labels on icon buttons.

**Report format.** Group by severity:
- **Blocker**: users cannot finish the task.
- **Major**: users get confused or slowed.
- **Minor**: polish.

For each finding write: where it is (file and line or page area), what is wrong, why it matters in one sentence, and the exact fix. Put the top three fixes first. Do not pad with praise or vague advice like "improve spacing". Offer to apply the Blocker and Major fixes, then re-check.
