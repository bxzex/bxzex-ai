# BXZEX Uncensored AI

A local AI model that lives on your own computer and answers to nobody but you. Mac, Linux, and Windows through WSL.

No account. No subscription. No filter deciding what you're allowed to ask. It runs on your own machine, in the terminal, and nothing you type, say or show it leaves your laptop. Turn the wifi off and it still works.

I built this for myself, liked it too much to keep it to myself, and now it's free for anyone.

[bxzex.com](https://bxzex.com) · Web version [app.bxzex.com](https://app.bxzex.com) · Instagram [@bxzex](https://www.instagram.com/bxzex/)

## New: the web version

BXZEX AI now also runs in the browser at **[app.bxzex.com](https://app.bxzex.com)**, for when your computer can't run the model or you just want to try it first. It works on a phone too, and you can add it to your home screen like an app.

It is the same model with the same image generation, vision, voice, memory and skills. There's a free plan with a small amount of usage, and Pro for $11 a month if you want more. An account is a username and a password, with no email.

Two things are different from this app, and you should know them before you pick:

- **It isn't private the way this is.** On the web your messages go to a server to be answered. They aren't saved there, but they do leave your device. Here, nothing does.
- **It can't touch your computer.** Running commands and working with your files only happens in this app.

If your machine can run it, this app is still the one with no limits and no bill.

## What it does

- **Talks to you.** Ask it anything. It doesn't lecture and it doesn't refuse.
- **Goes online when it needs to.** It searches the web and reads pages to get you current answers.
- **Sees images.** Drag a photo or screenshot into the window and ask about it.
- **Makes images.** Ask for a picture, or type `/image`, and it paints one on your own machine with no filter in the way, in about a minute on a Mac. It shows up in the chat and is saved to your Pictures folder.
- **Does things on your computer.** It can run commands and read or write files. It shows you exactly what it wants to do and waits for your yes first.
- **Listens.** Type `/v`, say what you want, and your words show up at the prompt ready to send.
- **Remembers you.** Tell it something worth keeping and it's still there next week. It all sits in a plain text file you can read, edit or wipe.
- **Connects to your apps.** Gmail, Calendar, Slack, GitHub, Notion, Drive, Sheets, Instagram, Stripe and 1,600 more, through Composio over MCP. Add it once with `/mcp add`, sign in to an app when it asks, and it can read and act there (it asks before anything that sends, posts or changes). Any other MCP server works the same way.
- **Skills.** Over 100 of them, from design and web apps to games, mobile apps, video and sales. They come from bxzex.com as it needs them, so they're always the newest, and you can add your own.
- **Looks how you want.** Nine color themes. It starts in white fading to blue, like the logo. Pick another during install or switch any time with `/color`.

## Check it before you run it

You shouldn't paste a command from the internet into your terminal on trust, mine included. So here is how to check this one:

- **Scan it.** [Open the installer's report on VirusTotal](https://www.virustotal.com/gui/url/51f215605807510d30794918f552843b22cea998909f6d2f40bc7a7542f0f07c), which runs it past 92 security services. When I scanned it on October 4, 2026, 90 rated it clean. Two reputation services flagged it, which is common for a brand-new install script that hasn't built up a history yet. You can rerun the scan yourself from that page.
- **Read it.** Nothing here is hidden or compiled. The [installer](install.sh) and the [app](bxzex-ai) are plain text files you can open and read top to bottom.
- **Know what it touches.** Everything it installs goes into one folder, `~/.bxzex-ai`, plus a few standard tools from Homebrew. It never asks for your password and there's one command at the bottom of this page that removes all of it.

## What you need

**Mac**
- Apple Silicon (M1 or newer) and **16GB of memory or more**
- About 23GB of free disk space, or 18GB on a 16GB Mac
- [Homebrew](https://brew.sh). If you don't have it, their site gives you one line to paste.

**Linux**
- A 64-bit PC with a graphics card that has **12GB of video memory or more**, or **16GB of RAM** to run it on the processor, which is slower.
- About 25GB of free disk space, or 20GB for the lighter build
- `curl` and `python3`, which most systems already have
- For voice, a recording tool. Most desktops have one. If yours doesn't, the installer tells you the one line to add it: `sudo apt install pulseaudio-utils`

**Windows**
- Install WSL first: open PowerShell as administrator, run `wsl --install`, restart, and open Ubuntu. Then follow the Linux steps inside it.
- It knows it's on Windows. Pictures it makes land in your Windows Pictures folder, and you can drag an image in from Explorer like on a Mac.
- For voice, switch the microphone on for desktop apps in Windows settings (Privacy, Microphone).

**It picks the build that fits your computer.** It's one model in two builds. With 24GB of memory, or a graphics card with 20GB or more, you get the full one. With 16GB of memory, or a 12GB or 16GB graphics card, you get the lighter one: the same model with the same skills, tools, vision, voice and images, packed smaller so it fits. It's a little less sharp on hard questions and remembers about half as much conversation at once. The bar at the bottom says `lite` when that's the one you have. To choose yourself, put `BXZEX_SIZE=full` or `BXZEX_SIZE=lite` in front of `bash` on the install line.

It will not run on a computer with 8GB of memory. The same model can't be made that small and still be worth using. The installer checks and stops if there isn't enough. On a 16GB computer, close your other big apps while it's running.

Everything works on all three: chat, web search, vision, image generation, voice input, skills, memory, chat history and the shell tools. Linux and Windows support is new, so tell me if something breaks. Image generation on Linux and Windows needs a recent system (Ubuntu 24.04 or similar) and a 64-bit Intel or AMD processor. It uses the graphics card on Linux. Inside Windows it runs on the processor for now, so a picture takes several minutes there.

## Install

Open a terminal and paste this:

```sh
curl -fsSL https://raw.githubusercontent.com/bxzex/bxzex-ai/main/install.sh | bash
```

Pick your color, then let it work. It sets up everything and downloads the AI model, vision, voice, and image generation. That's about 21GB on a Mac and 23GB on Linux, so give it a while on slower internet. If your connection drops, paste the same line again and it picks up where it stopped.

When it says READY, open a new terminal window and type:

```sh
bxzex-ai
```

The first launch takes about a minute while the model loads. After that it stays loaded and opens right away.

## Updates

It checks for a new version each time you open it and installs it quietly in the background. When that happens the bar at the bottom says so, and you quit and reopen to use it. Your chats, memory and settings are never touched.

- `/update` checks right now.
- `/update full` runs the installer again when a new version adds something to download. It skips everything you already have.
- Your version is in the bar at the bottom and in `bxzex-ai --version`.
- To turn the automatic check off, launch with `BXZEX_NO_UPDATE=1`.

**If you installed before updates existed.** Version 1.0 has no way to update itself, so nothing I release can reach it. You can tell because there's no version number in the bar at the bottom and `/update` does nothing. Paste the install line from above one more time. It keeps your model, chats and memory, skips everything already downloaded and takes about a minute. From then on it updates by itself.

## Using it

Type and press Enter. For a quick one-off without opening the app: `bxzex-ai "your question"`.

| Type this | And it will |
|---|---|
| `/v` | Listen. Talk, press Enter when you're done, then edit or send what it heard. |
| `/image` | Make a picture. `/image a red fox in snow`. Add `portrait` or `landscape` for the shape and `hd` for more detail. |
| `/color` | Show the color themes and let you pick one. `/color red` jumps straight to it. |
| `/skills` | List what it's been taught. |
| `/memory` | Show what it remembers about you. `/memory clear` wipes it. |
| `/history` | Your past chats. Move with the arrow keys and press Enter to carry on where you left off. |
| `/resume` | Jump straight back into the last chat. |
| `/btw` | Add a note without waiting for an answer, like `/btw the client wants it in Spanish`. |
| `/fast` | Switch fast mode. It's on by default and answers right away. Turn it off when you want it to think a hard question through first. |
| `/think` | Show or hide its thinking when fast mode is off. |
| `/device` | Show whether it runs on your graphics card (GPU) or your processor (CPU). `/device cpu` or `/device gpu` switches and it remembers. |
| `/update` | Get the newest version. |
| `!command` | Run a command yourself, like `!git status`. You see the output and so does it. |
| `@file` | Attach a file to your message, like `what does @app.py do`. |
| `/plan` | Plan mode: it looks around and writes a plan, and changes nothing until you turn it off. Shift+Tab in the box does the same. |
| `/todos` | Its to-do list for the job it's on. On bigger jobs it keeps one and ticks steps off as it goes. |
| `/jobs` | Commands it left running in the background, like a dev server. They stop when you quit. |
| `/context` | How full the chat is. |
| `/rewind` | Go back to an earlier message, change it and send it again, and put back the files it changed after it if you want. Esc twice on an empty line does the same. |
| `/last` | The full output of the last tools it ran (it shows only the first line). Ctrl+O does the same. |
| `/apps` | The apps you can connect. `/apps email` searches them, `/apps connected` shows yours. |
| `/say` | Read its replies out loud. |
| `/schedule` | Tasks it does on its own at set times, even with the app closed. Ask in your own words ("every weekday at 8am, read my Gmail and tell me what's important") and it sets it up; each run's report comes as a notification. Here you read the results, run one now, pause or remove it. |
| `/check` | Open a site or your local app as an iPhone, Android phone, iPad and desktop (Safari's engine for Apple devices), find what breaks (sideways scrolling, buttons too small to tap, tiny text, broken images, console errors) and look at screenshots of each. `/check localhost:5173`, `/check bxzex.com android`. Screenshots are saved in Pictures/BXZEX/checks. The first time, it offers to download the browsers it needs (about 400 MB). |
| `/phone` | Use it from your phone through Telegram: it walks you through making a bot (one minute), then you can write to it from anywhere and it works on your computer. Questions and OKs come as buttons, scheduled reports arrive there, and only your Telegram account can use it. `/phone test`, `/phone off`. |
| `/imessage` | Mac only: text your own number from your iPhone and it answers in that chat from your Mac, with replies starting "BXZEX AI:". Reply yes or no to OK an action. It only reads your chat with yourself, and texting anyone else always asks first and is capped at 20 an hour. Needs Full Disk Access for Python, which it walks you through. `/imessage off`. |
| `/cost` | What the cloud card has cost today, this month and last month, from Modal's own billing. |
| `/export` | Save this chat as a Markdown document in the folder you're in. `/export ~/Desktop` saves it there. |
| `/commit` | It looks at your changes and commits them with a message in your repo's style. `/commit and push` pushes too. |
| `/review` | It reviews your changes (or your branch) for bugs and security holes before you push, worst first, and changes nothing. |
| `/hooks` | Your own commands that run before or after its tools, or when a reply is done. A before-hook that fails blocks the tool. `/hooks add after edit_file|write_file npx prettier --write "$BXZEX_FILE"`. |
| `/notify` | Notifications on or off. When a reply takes 30 seconds or more, or it needs your OK, while you're in another window, you get a notification. |
| `/warm` | Cloud card only: keep it awake during your hours so replies start right away. `/warm 9-18`, `/warm weekdays 9-18`, `/warm off`. Costs about $4 for every hour it stays awake. |
| `/mcp` | Connected tool servers and apps. `/mcp add <name> <url> Header:value` adds one. |
| `/undo` | Put back the last file it wrote or edited. |
| `/compact` | Fold the chat so far into a short summary to make room. |
| `/init` | It looks around the folder you're in and writes a `BXZEX.md` about the project, which it reads every time you work there. |
| `/allow` | Turn "always allow" on or off. Risky commands like `rm` still ask. |
| `/reset` | Start a fresh conversation. `/clear` does the same. |
| `exit` | Quit. |

When it opens it asks where to start: continue from your last save, a new chat, or an earlier one, picked with the arrow keys. Type `/` and it shows you the commands as you go, and Tab finishes the name. Ctrl+V pastes a screenshot from the clipboard. Ctrl+R searches what you sent before. Pasted text keeps its line breaks, and the up arrow brings back what you typed, even from earlier sessions. Looking at files and read-only commands (`ls`, `cat`, `grep`, `git status`) never ask; any change to a file shows you exactly which lines change before you allow it. Press `f` at a question to always allow that kind of command (like `npm test`) or file changes in that folder, kept between sessions; `/allow clear` forgets them. Tables come out as grids and code in color. The whole thing redraws itself when you resize the window.

To show it an image, drag the file into the terminal window and add your question.

On a Mac it can also work in Safari (list your tabs, open pages, read a page, run JavaScript in it, including pages you're signed in to) and in Messages (read recent messages, look people up in Contacts, and send an iMessage or text, which always asks you first). The first time, macOS asks you to allow it.

On the cloud card it can hand research to helpers, and several run at the same time. Helpers only look (read, search, fetch pages, read-only commands) and report back.

You don't have to wait for it to finish. While it's working, type what you forgot to say and press Enter. It gets passed along as a "by the way" and it adjusts.

Press Ctrl-C to stop a reply halfway.

**Long chats.** It can only hold so much conversation at once. When a chat gets close to that, it writes itself a summary of the older part and carries on, keeping your most recent messages word for word. You'll see a line saying so. It can take a few minutes on a laptop, and it's why a very long chat doesn't just stop working.

## Images

Type `/image` and describe what you want, or ask in conversation and it writes a detailed prompt for you first. The picture appears in the chat and is saved to `Pictures/BXZEX`. Cmd-click the path to open the full size (Ctrl-click on Linux and Windows).

A normal image takes about a minute on a 24GB MacBook Air. Add `hd` for a bigger, sharper one, which takes two to three minutes.

Most computers can't hold the chat model and the image model at the same time, so it swaps them. You'll see "Making room", then "Painting", and the chat model loads back in while you look at the result.

It comes with a realistic photo style built in. To change the look, put your own LoRA style files (`.safetensors`) in `~/.bxzex-ai/loras`. Every image uses whatever is in that folder.

To leave image generation out and save about 6GB, install with `BXZEX_IMAGES=0` in front of `bash`.

## Make it yours

Everything it knows about itself lives in four places inside `~/.bxzex-ai`, all plain text:

- **`BXZEX.md`** is its guide. Add your own rules at the bottom ("always answer in Spanish", "I'm a mechanic, keep it practical") and it follows them in every conversation. Put a `BXZEX.md` in any folder and it reads that too when you launch it from there.
- **`memory.md`** is what it has saved about you. One line per thing.
- **`about.md`** is where you tell it who you are. It's read in every chat and never leaves your computer.
- **`tests/`** (in this repo) checks the whole app in a real terminal against a stand-in model: `bash tests/run.sh`.
- **`commands/`** holds your own slash commands: save a prompt as `commands/name.md` and type `/name`.
- **`chats/`** keeps every conversation, so nothing is lost when you close the window.
- **`skills/`** holds one file per skill: a markdown file with a name and description at the top and what it should know below.

The bxzex skills are served from bxzex.com, one at a time as it uses them, and aren't in this repo. `/skills` lists them. Write your own: copy the format of any markdown file with `name:` and `description:` at the top into `~/.bxzex-ai/skills/`, and it uses it.

## Remove it

```sh
pkill llama-server
launchctl bootout gui/$(id -u)/com.bxzex.ai.schedule 2>/dev/null; rm -f ~/Library/LaunchAgents/com.bxzex.ai.schedule.plist   # Mac, if you scheduled tasks
rm -rf ~/.bxzex-ai "$(brew --prefix)/bin/bxzex-ai"    # Mac
crontab -l 2>/dev/null | grep -v 'bxzex-ai schedule' | crontab -    # Linux, if you scheduled tasks
rm -rf ~/.bxzex-ai ~/.local/bin/bxzex-ai              # Linux
```

## Credits and license

The app, the installer, the skills and the terminal design are © 2026 bxzex. All rights reserved.

It's free to install and use, for anything. What you can't do is copy it, repost it, rebrand it or put out your own version of it. If you want to share it, send people here. The full terms are in [LICENSE](LICENSE).

It runs on open source engines and open models, which are downloaded during install under their own licenses. The DeLorean that flies past during install is ASCII art by mozz.

More of what I build is at [bxzex.com](https://bxzex.com). Say hi on Instagram: [@bxzex](https://www.instagram.com/bxzex/).
