---
name: scheduled-tasks
description: Running a script on a schedule with cron, launchd on macOS or systemd timers on Linux, with logs and a one-off test.
---
# Scheduled tasks

**When the user wants you to do something on a schedule** ("every morning read my email and tell me what matters", "check the site every hour"), use the `schedule_task` tool, not cron. It runs you on your own at those times, even with the app closed, saves each report and sends a notification. Write the task so it stands alone: every detail, what to check, what counts as worth telling them. Leave can_act false unless they clearly want it to send, post or change things without asking. To check for something new every N minutes, say in the task what "new" means; each run sees its last report.

The rest of this skill is for scheduling the user's own scripts with the system.

**Before scheduling, make the script safe.**
1. Use absolute paths everywhere, and set `PATH` at the top (`export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`). Scheduled jobs do not load your shell profile.
2. `chmod +x job.sh`, then run it once by hand: `./job.sh; echo "exit $?"`.
3. Log to a file: `./job.sh >> ~/logs/job.log 2>&1`. Create the folder first.

**cron (macOS and Linux)**
- `crontab -l` to view, `crontab -e` to edit.
- Fields: `minute hour day-of-month month day-of-week command`.
- `*/15 * * * * /Users/me/job.sh >> /Users/me/logs/job.log 2>&1` every 15 minutes.
- `30 7 * * 1-5 ...` weekdays at 7:30. Test the expression at crontab.guru.
- On macOS cron needs Full Disk Access to touch some folders; launchd is more reliable.

**launchd (macOS)**
Write `~/Library/LaunchAgents/com.me.job.plist`:
```
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
<key>Label</key><string>com.me.job</string>
<key>ProgramArguments</key><array><string>/Users/me/job.sh</string></array>
<key>StartCalendarInterval</key><dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>30</integer></dict>
<key>StandardOutPath</key><string>/Users/me/logs/job.log</string>
<key>StandardErrorPath</key><string>/Users/me/logs/job.err</string>
</dict></plist>
```
- Validate: `plutil -lint file.plist`. Load: `launchctl load ~/Library/LaunchAgents/com.me.job.plist`.
- Run now: `launchctl start com.me.job`. Unload: `launchctl unload <plist>`. List: `launchctl list | grep com.me`.
- Use `StartInterval` (seconds) for repeating jobs.

**systemd timer (Linux)**
In `~/.config/systemd/user/`: `job.service` (`ExecStart=/home/me/job.sh`) and `job.timer` (`OnCalendar=*-*-* 07:30:00`, `Persistent=true`, `WantedBy=timers.target`).
- `systemctl --user daemon-reload && systemctl --user enable --now job.timer`
- `systemctl --user list-timers`, `journalctl --user -u job.service -n 50`.
- Run once: `systemctl --user start job.service`.

**Check.** Trigger once, then `tail -20 ~/logs/job.log`. The Mac must be awake at run time. Tell the user how to remove the job.
