# BXZEX Uncensored AI

A local AI model that lives on your own computer and answers to nobody but you. Mac, Linux, and Windows through WSL.

No account. No subscription. No filter deciding what you're allowed to ask. It runs on your own machine, in the terminal, and nothing you type, say or show it leaves your laptop. Turn the wifi off and it still works.

I built this for myself, liked it too much to keep it to myself, and now it's free for anyone.

[bxzex.com](https://bxzex.com) · Instagram [@bxzex](https://www.instagram.com/bxzex/)

## What it does

- **Talks to you.** Ask it anything. It doesn't lecture and it doesn't refuse.
- **Goes online when it needs to.** It searches the web and reads pages to get you current answers.
- **Sees images.** Drag a photo or screenshot into the window and ask about it.
- **Makes images.** Ask for a picture, or type `/image`, and it paints one on your own machine with no filter in the way, in about a minute on a Mac. It shows up in the chat and is saved to your Pictures folder.
- **Does things on your computer.** It can run commands and read or write files. It shows you exactly what it wants to do and waits for your yes first.
- **Listens.** Type `/v`, say what you want, and your words show up at the prompt ready to send.
- **Remembers you.** Tell it something worth keeping and it's still there next week. It all sits in a plain text file you can read, edit or wipe.
- **Comes with skills.** Twenty-nine of them: design, front-end, writing that doesn't sound like a robot, social posts, client proposals, research, debugging, security and more. It pulls in the right one when the job calls for it, and you can write your own.
- **Looks how you want.** Nine color themes. It starts in white fading to blue, like the logo. Pick another during install or switch any time with `/color`.

## Check it before you run it

You shouldn't paste a command from the internet into your terminal on trust, mine included. So here is how to check this one:

- **Scan it.** [Open the installer's report on VirusTotal](https://www.virustotal.com/gui/url/51f215605807510d30794918f552843b22cea998909f6d2f40bc7a7542f0f07c), which runs it past 92 security services. When I scanned it on October 4, 2026, 90 rated it clean. Two reputation services flagged it, which is common for a brand-new install script that hasn't built up a history yet. You can rerun the scan yourself from that page.
- **Read it.** Nothing here is hidden or compiled. The [installer](install.sh) and the [app](bxzex-ai) are plain text files you can open and read top to bottom.
- **Know what it touches.** Everything it installs goes into one folder, `~/.bxzex-ai`, plus a few standard tools from Homebrew. It never asks for your password and there's one command at the bottom of this page that removes all of it.

## What you need

**Mac**
- Apple Silicon (M1 or newer) and **24GB of memory or more**
- About 23GB of free disk space
- [Homebrew](https://brew.sh). If you don't have it, their site gives you one line to paste.

**Linux**
- A 64-bit PC with an NVIDIA graphics card that has **16GB of video memory or more**. Without one it still runs on the processor if you have 24GB of RAM, but slowly.
- About 25GB of free disk space
- `curl` and `python3`, which most systems already have
- For voice, a recording tool. Most desktops have one. If yours doesn't, the installer tells you the one line to add it: `sudo apt install pulseaudio-utils`

**Windows**
- Install WSL first: open PowerShell as administrator, run `wsl --install`, restart, and open Ubuntu. Then follow the Linux steps inside it.
- It knows it's on Windows. Pictures it makes land in your Windows Pictures folder, and you can drag an image in from Explorer like on a Mac.
- For voice, switch the microphone on for desktop apps in Windows settings (Privacy, Microphone).

It will not run on a computer with 8GB or 16GB of memory and no big graphics card. The installer checks and stops if there isn't enough.

Everything works on all three: chat, web search, vision, image generation, voice input, skills, memory, chat history and the shell tools. Linux and Windows support is new, so tell me if something breaks. Image generation on Linux and Windows needs a recent system (Ubuntu 24.04 or similar) and a 64-bit Intel or AMD processor. It uses the graphics card on Linux. Inside Windows it runs on the processor for now, so a picture takes several minutes there.

## Install

Open a terminal and paste this:

```sh
curl -fsSL https://raw.githubusercontent.com/bxzex/bxzex-ai/main/install.sh | bash
```

Pick your color, then let it work. It sets up everything and downloads the AI model, vision, voice, image generation and skills. That's about 21GB on a Mac and 23GB on Linux, so give it a while on slower internet. If your connection drops, paste the same line again and it picks up where it stopped.

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
| `/history` | Your past chats. Pick one and carry on where you left off. |
| `/resume` | Jump straight back into the last chat. |
| `/btw` | Add a note without waiting for an answer, like `/btw the client wants it in Spanish`. |
| `/fast` | Switch fast mode. It's on by default and answers right away. Turn it off when you want it to think a hard question through first. |
| `/think` | Show or hide its thinking when fast mode is off. |
| `/device` | Show whether it runs on your graphics card (GPU) or your processor (CPU). `/device cpu` or `/device gpu` switches and it remembers. |
| `/update` | Get the newest version. |
| `/reset` | Start a fresh conversation. |
| `exit` | Quit. |

Type `/` and it shows you the commands as you go. The whole thing redraws itself when you resize the window.

To show it an image, drag the file into the terminal window and add your question.

You don't have to wait for it to finish. While it's working, type what you forgot to say and press Enter. It gets passed along as a "by the way" and it adjusts.

Press Ctrl-C to stop a reply halfway.

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
- **`chats/`** keeps every conversation, so nothing is lost when you close the window.
- **`skills/`** holds one file per skill. Copy one, change the name and description at the top, write what you want it to know, and it has a new skill.

The skills it ships with:

| Skill | What it's for |
|---|---|
| `ui-design` | Layout, type, color and states for interfaces that look intentional |
| `no-ai-slop` | Stripping out the generic machine-made look before it calls a design done |
| `frontend-build` | Web pages that work when you open the file |
| `landing-page` | Pages built around getting one action from a visitor |
| `accessibility` | Making a page usable by keyboard, screen reader and low vision |
| `react-components` | React components and small apps |
| `human-writing` | Copy, posts and emails that read like a person wrote them |
| `email-writing` | Emails and messages that get an answer |
| `social-posts` | Instagram, TikTok, X and LinkedIn captions in your voice |
| `video-script` | Scripts for Reels, TikTok and Shorts |
| `sales-outreach` | First messages to a client that don't read like spam |
| `client-proposal` | Quotes and scopes of work a client can say yes to |
| `pricing-offers` | What to charge and how to package it |
| `brand-naming` | Names for a business, product or app |
| `seo-basics` | Getting a page found on Google |
| `plan-project` | Turning a vague goal into steps |
| `summarize` | Boiling a long document down for someone with thirty seconds |
| `explain-teach` | Explaining something hard so it sticks |
| `web-research` | Finding current facts and saying where they came from |
| `data-analysis` | Getting an honest answer out of a spreadsheet |
| `debugging` | Finding the real cause before changing anything |
| `code-review` | Catching bugs before they ship |
| `security-check` | Spotting common security mistakes in your own site or app |
| `api-design` | Endpoints that are clear and safe |
| `sql-database` | Tables and queries that return the right rows |
| `python-scripting` | Scripts that automate a job and have been run |
| `bash-scripting` | Shell scripts that don't break on a space |
| `git-workflow` | Committing, branching and undoing without losing work |
| `mac-automation` | Getting things done on your Mac without breaking it |
| `linux-automation` | The same for Linux and Windows. You get whichever one matches your computer. |

## Graphics card or processor

You can run it on either. It uses the graphics card when there is one, because that is much faster: the Mac's own chip, an NVIDIA card, or an AMD or Intel card on Linux. With no card it runs on the processor, which works on any machine with enough memory, only slower.

Type `/device` to see which one it is on. `/device cpu` moves it to the processor, say when a game or a render needs the card, and `/device gpu` moves it back. It reloads the model and remembers your choice.

To set it up for the processor from the start, put `BXZEX_DEVICE=cpu` in front of `bash` on the install line. That works on Mac, Linux and Windows.

## How fast it is

This is a big model running on a laptop. On a 24GB MacBook Air it writes around three words a second. Short answers land in under a minute. Jobs where it has to look several things up can take a few minutes. A Mac with a Pro or Max chip is quicker.

It's slower than the big online assistants. In exchange, it's private and it's yours.

## Use at your own risk

BXZEX AI is provided as is, with no warranty of any kind. You use it entirely at your own risk.

You are responsible for everything you do with it: what you ask it, what it writes, the images it makes, the commands you approve and anything you do with the results. bxzex is not responsible or liable for any of that, or for any loss, damage or legal trouble that comes from using it. Follow the laws where you live. If you don't agree, don't install it.

## Be careful with it

It's uncensored, and when it runs a command it runs it as you, with nothing fencing it in. Read what it's asking before you say yes. It offers an "always" option that stops it asking for the rest of the session. I'd leave that alone unless you're watching.

## Settings

Optional. Set any of these before launching.

| Setting | Default | What it changes |
|---|---|---|
| `BXZEX_VOICE_LANG` | `en` | The language you speak in, like `es`. Use `auto` to let it figure it out. |
| `BXZEX_CTX` | `32768` | How much conversation it can hold at once. |
| `BXZEX_PORT` | `8080` | The local port it uses. |
| `BXZEX_DEVICE` | graphics card | Set to `cpu` to run on the processor for one launch. `/device` saves the choice for good. |
| `BXZEX_LORA_SCALE` | `0.8` | How strongly image styles are applied. |

The model stays in memory after you quit so the next launch is instant. To shut it down and get that memory back: `pkill llama-server`.

## Remove it

```sh
pkill llama-server
rm -rf ~/.bxzex-ai "$(brew --prefix)/bin/bxzex-ai"    # Mac
rm -rf ~/.bxzex-ai ~/.local/bin/bxzex-ai              # Linux
```

## Credits and license

The app, the installer, the skills and the terminal design are © 2026 bxzex. All rights reserved.

It's free to install and use, for anything. What you can't do is copy it, repost it, rebrand it or put out your own version of it. If you want to share it, send people here. The full terms are in [LICENSE](LICENSE).

It runs on open source engines and open models, which are downloaded during install under their own licenses. The DeLorean that flies past during install is ASCII art by mozz.

More of what I build is at [bxzex.com](https://bxzex.com). Say hi on Instagram: [@bxzex](https://www.instagram.com/bxzex/).
