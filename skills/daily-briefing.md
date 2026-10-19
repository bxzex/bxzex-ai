---
name: daily-briefing
description: Producing a short morning briefing from the calendar, notes, weather, news, open tasks and mail counts.
---
# Daily briefing

Goal: one screen the user can read in a minute. Collect what is available, skip what is not, and never invent items.

1. **Date.** `date "+%A %B %d"`.
2. **Calendar.**
   - macOS: `icalBuddy eventsToday` if installed (`brew install ical-buddy`), otherwise `osascript -e 'tell application "Calendar" to get summary of (every event of every calendar whose start date >= (current date) and start date < ((current date) + 1 * days))'`.
   - Linux: `khal list today` or `gcalcli agenda`.
   - Else look for a plan file: `ls ~/notes ~/Documents/*.md`.
3. **Tasks and notes.** Search for open items: `grep -rnE "^\s*- \[ \]|TODO" ~/notes ~/todo.md 2>/dev/null | head -20`. Also check `git status -sb` in the current project.
4. **Weather.** Use web_search for "weather <city> today" (ask once for the city if unknown, then save it in the briefing file). Or `curl -s "wttr.in/CITY?format=3"`.
5. **News.** web_search for 3 headlines on the user's topics. Give source and one line each. No clickbait, no more than 5.
6. **Mail counts.** Only if a CLI exists (`which himalaya mutt notmuch`). Example: `notmuch count tag:unread`. If none, skip it and say nothing.
7. **Write the briefing** in this shape:

```
Tuesday, October 20
Weather: 14C, rain after 3pm
Today: 10:00 standup, 13:00 dentist
Open tasks (3): ship invoice page, reply to Sam, renew domain
Mail: 12 unread
Headlines: ...
Suggested focus: <one task, with a reason>
```

8. Keep it under 15 lines. Save to `~/briefings/YYYY-MM-DD.md` only if the user wants history.

Pitfalls: macOS asks for Calendar permission the first time, tell the user to allow it. Do not read private mail bodies, counts only.
