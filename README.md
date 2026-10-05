# BXZEX Uncensored AI

A local AI model that lives on your Mac and answers to nobody but you.

No account. No subscription. No filter deciding what you're allowed to ask. It runs on your own machine, in the terminal, and nothing you type, say or show it leaves your laptop. Turn the wifi off and it still works.

I built this for myself, liked it too much to keep it to myself, and now it's free for anyone.

[bxzex.com](https://bxzex.com) · Instagram [@bxzex](https://www.instagram.com/bxzex/)

## What it does

- **Talks to you.** Ask it anything. It doesn't lecture and it doesn't refuse.
- **Goes online when it needs to.** It searches the web and reads pages to get you current answers.
- **Sees images.** Drag a photo or screenshot into the window and ask about it.
- **Makes images.** Ask for a picture, or type `/image`, and it paints one on your Mac in about a minute with no filter in the way. It shows up in the chat and is saved to your Pictures folder.
- **Does things on your Mac.** It can run commands and read or write files. It shows you exactly what it wants to do and waits for your yes first.
- **Listens.** Type `/v`, say what you want, and your words show up at the prompt ready to send.
- **Remembers you.** Tell it something worth keeping and it's still there next week. It all sits in a plain text file you can read, edit or wipe.
- **Comes with skills.** Twenty-nine of them: design, front-end, writing that doesn't sound like a robot, social posts, client proposals, research, debugging, security and more. It pulls in the right one when the job calls for it, and you can write your own.
- **Looks how you want.** Nine color themes. It starts in white fading to blue, like the logo. Pick another during install or switch any time with `/color`.

## Check it before you run it

You shouldn't paste a command from the internet into your terminal on trust, mine included. So here is how to check this one:

- **Scan it.** [Open the installer's report on VirusTotal](https://www.virustotal.com/gui/url/51f215605807510d30794918f552843b22cea998909f6d2f40bc7a7542f0f07c), which runs it past dozens of antivirus engines. You can also go to [virustotal.com](https://www.virustotal.com/gui/home/url) and paste the install address yourself.
- **Read it.** Nothing here is hidden or compiled. The [installer](install.sh) and the [app](bxzex-ai) are plain text files you can open and read top to bottom.
- **Know what it touches.** Everything it installs goes into one folder, `~/.bxzex-ai`, plus a few standard tools from Homebrew. It never asks for your password and there's one command at the bottom of this page that removes all of it.

## What you need

- A Mac with Apple Silicon (M1 or newer) and **24GB of memory or more**
- About 23GB of free disk space
- [Homebrew](https://brew.sh). If you don't have it, their site gives you one line to paste.

## Install

Open the Terminal app and paste this:

```sh
curl -fsSL https://raw.githubusercontent.com/bxzex/bxzex-ai/main/install.sh | bash
```

Pick your color, then let it work. It sets up everything and downloads the AI model, vision, voice, image generation and skills. That's about 21GB, so give it a while on slower internet. If your connection drops, paste the same line again and it picks up where it stopped.

When it says READY, open a new terminal window and type:

```sh
bxzex-ai
```

The first launch takes about a minute while the model loads. After that it stays loaded and opens right away.

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
| `/reset` | Start a fresh conversation. |
| `exit` | Quit. |

Type `/` and it shows you the commands as you go. The whole thing redraws itself when you resize the window.

To show it an image, drag the file into the terminal window and add your question.

You don't have to wait for it to finish. While it's working, type what you forgot to say and press Enter. It gets passed along as a "by the way" and it adjusts.

Press Ctrl-C to stop a reply halfway.

## Images

Type `/image` and describe what you want, or ask in conversation and it writes a detailed prompt for you first. The picture appears in the chat and is saved to `Pictures/BXZEX`. Cmd-click the path to open the full size.

A normal image takes about a minute on a 24GB MacBook Air. Add `hd` for a bigger, sharper one, which takes two to three minutes.

Your Mac can't hold the chat model and the image model at the same time, so it swaps them. You'll see "Making room", then "Painting", and the chat model loads back in while you look at the result.

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

## How fast it is

This is a big model running on a laptop. On a 24GB MacBook Air it writes around three words a second. Short answers land in under a minute. Jobs where it has to look several things up can take a few minutes. A Mac with a Pro or Max chip is quicker.

It's slower than the big online assistants. In exchange, it's private and it's yours.

## Be careful with it

It's uncensored, and when it runs a command it runs it as you, with nothing fencing it in. Read what it's asking before you say yes. It offers an "always" option that stops it asking for the rest of the session. I'd leave that alone unless you're watching.

## Settings

Optional. Set any of these before launching.

| Setting | Default | What it changes |
|---|---|---|
| `BXZEX_VOICE_LANG` | `en` | The language you speak in, like `es`. Use `auto` to let it figure it out. |
| `BXZEX_CTX` | `32768` | How much conversation it can hold at once. |
| `BXZEX_PORT` | `8080` | The local port it uses. |
| `BXZEX_LORA_SCALE` | `0.8` | How strongly image styles are applied. |

The model stays in memory after you quit so the next launch is instant. To shut it down and get that memory back: `pkill llama-server`.

## Remove it

```sh
pkill llama-server
rm -rf ~/.bxzex-ai "$(brew --prefix)/bin/bxzex-ai"
```

## Credits and license

The app, the installer, the skills and the terminal design are © 2026 bxzex. All rights reserved.

It's free to install and use, for anything. What you can't do is copy it, repost it, rebrand it or put out your own version of it. If you want to share it, send people here. The full terms are in [LICENSE](LICENSE).

It runs on open source engines and open models, which are downloaded during install under their own licenses. The DeLorean that flies past during install is ASCII art by mozz.

More of what I build is at [bxzex.com](https://bxzex.com). Say hi on Instagram: [@bxzex](https://www.instagram.com/bxzex/).
