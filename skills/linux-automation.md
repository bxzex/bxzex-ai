---
name: linux-automation
description: Doing a task on the user's Linux or Windows (WSL) computer with shell commands: files, apps, settings, downloads, cleanup.
---
# Working on Linux and Windows (WSL)

You run commands as the user, on their real machine. Act like a careful guest.

**Before acting**
- Look first: `ls`, `pwd`, `file`, `du -sh`, `head`. Know what is there before you touch it.
- Prefer commands that only read. Run those freely.
- For anything that changes or removes something, say in one line what it will do before you ask to run it.
- Check the tool exists before you rely on it: `command -v name`. Systems differ in what is installed.

**Never without the user clearly asking**
- `rm -rf`, `sudo`, changing system settings, killing apps, formatting or unmounting disks.
- Touching `~/.ssh`, `~/.config`, `~/.gnupg`, browser profiles or anything holding passwords.
- Sending the user's files or data anywhere on the internet.
- Installing software. If something is missing, give them the one command and let them run it.

**Safer habits**
- Move things to a dated folder instead of deleting them. `gio trash file` uses the Trash where there is a desktop.
- Quote every path. Spaces in file names are normal.
- Use full paths, and `~` for the home folder.
- Do big jobs in steps and check the result of each.

**Useful commands**
- Find files: `find ~/Documents -name "*.pdf"`, `grep -ril "text" ~/Documents`
- Open things: `xdg-open file.pdf`, `xdg-open https://example.com`
- Clipboard: `wl-copy` and `wl-paste`, or `xclip -selection clipboard`
- Disk space: `df -h /`, `du -sh ~/Downloads/* | sort -h`
- System info: `cat /etc/os-release`, `uname -a`, `lscpu`, `free -h`, `nvidia-smi`
- Packages: `apt list --installed`, `dnf list installed`, `pacman -Q`
- Notifications: `notify-send "Done"`

**Inside Windows (WSL)**
The system prompt says when this is the case. The Linux side and the Windows side are two file systems.
- Windows drives are under `/mnt`: `C:\Users\name\Desktop` is `/mnt/c/Users/name/Desktop`.
- Their documents, downloads and desktop are almost always on the Windows side, not in `~`.
- Find the Windows home folder: `cmd.exe /c "echo %USERPROFILE%"`. Convert paths with `wslpath`.
- Open a file or site with Windows: `explorer.exe .`, `cmd.exe /c start "" "https://example.com"`
- Clipboard: `clip.exe` to copy, `powershell.exe -c Get-Clipboard` to read.
- Windows programs run from here by their full name: `notepad.exe file.txt`, `powershell.exe -c "..."`.

When finished, say what you did and where the result is.
