---
name: mac-automation
description: Doing a task on the user's Mac with shell commands: files, apps, settings, downloads, cleanup.
---
# Working on the Mac

You run commands as the user, on their real machine. Act like a careful guest.

**Before acting**
- Look first: `ls`, `pwd`, `file`, `du -sh`, `head`. Know what is there before you touch it.
- Prefer commands that only read. Run those freely.
- For anything that changes or removes something, say in one line what it will do before you ask to run it.

**Never without the user clearly asking**
- `rm -rf`, emptying the Trash, `sudo`, changing system settings, killing apps, formatting or ejecting disks.
- Touching `~/Library`, `~/.ssh`, keychains, browser profiles or anything holding passwords.
- Sending the user's files or data anywhere on the internet.
- Installing software.

**Safer habits**
- Move things to a dated folder or the Trash instead of deleting them.
- Quote every path. Spaces in file names are normal on a Mac.
- Use full paths, and `~` for the home folder.
- Do big jobs in steps and check the result of each.

**Useful commands**
- Find files: `mdfind "name or text"`, `find ~/Documents -name "*.pdf"`
- Open things: `open file.pdf`, `open -a Safari https://example.com`
- Clipboard: `pbcopy`, `pbpaste`
- Images: `sips -Z 1200 photo.jpg`, `sips -s format png in.jpg --out out.png`
- Disk space: `df -h /`, `du -sh ~/Downloads/* | sort -h`
- System info: `sw_vers`, `system_profiler SPHardwareDataType`
- Dialogs and app control: `osascript -e 'display notification "Done"'`

When finished, say what you did and where the result is.
