# BXZEX Uncensored AI — Local Model

An AI that lives on your Mac and answers to nobody but you.

No account. No subscription. No filter deciding what you're allowed to ask. It runs on your own machine, in the terminal, and nothing you type, say or show it ever leaves your laptop. Turn the wifi off and it still works.

I built this for myself, liked it too much to keep it, and I'm giving it away free.

— bxzex · [bxzex.com](https://bxzex.com) · Instagram [@bxzex](https://www.instagram.com/bxzex/)

## What it does

- **Talks to you.** Ask it anything. It doesn't lecture and it doesn't refuse.
- **Goes online when it needs to.** It searches the web and reads pages to get you current answers.
- **Sees images.** Drag a photo or screenshot into the window and ask about it.
- **Does things on your Mac.** It can run commands and read or write files. It shows you exactly what it wants to do and waits for your yes first.
- **Listens.** Type `/v`, say what you want, and your words show up at the prompt ready to send.
- **Remembers you.** Tell it something worth keeping and it's still there next week. It all sits in a plain text file you can read, edit or wipe.
- **Comes with skills.** Twenty-nine of them: design, front-end, writing that doesn't sound like a robot, social posts, client proposals, research, debugging, security and more. It pulls the right one in when the job calls for it, and you can write your own.
- **Looks how you want.** Nine color themes. It starts in white fading to blue, like the logo. Pick another during install or switch any time with `/color`.

## What you need

- A Mac with Apple Silicon (M1 or newer) and **24GB of memory or more**
- About 17GB of free disk space
- [Homebrew](https://brew.sh). If you don't have it, their site gives you one line to paste.

## Install

Open the Terminal app and paste this:

```sh
curl -fsSL https://raw.githubusercontent.com/bxzex/bxzex-ai/main/install.sh | bash
```

Pick your color, then let it work. It sets up everything it needs and downloads the model, which is about 15GB, so give it a while on slower internet. If your connection drops, paste the same line again and it picks up where it stopped.

When it says READY, open a new terminal window and type:

```sh
bxzex-ai
```

The first launch takes about a minute while the model loads. After that it stays loaded and opens right away.

## Using it

Type and press Enter. That's really it. For a quick one-off without opening the app: `bxzex-ai "your question"`.

| Type this | And it will |
|---|---|
| `/v` | Listen. Talk, press Enter when you're done, then edit or send what it heard. |
| `/color` | Show the color themes and let you pick one. `/color blue` jumps straight to it. |
| `/skills` | List what it's been taught. |
| `/btw` | Add a note without waiting for an answer, like `/btw the client wants it in Spanish`. |
| `/memory` | Show what it remembers about you. `/memory clear` wipes it. |
| `/history` | Your past chats. Pick one and carry on where you left off. |
| `/resume` | Jump straight back into the last chat. |
| `/fast` | Switch fast mode. It's on by default and answers right away. Turn it off when you want it to think a hard question through first. |
| `/think` | Show or hide its thinking when fast mode is off. |
| `/reset` | Start a fresh conversation. |
| `exit` | Quit. |

Type `/` and it shows you the commands as you go. The whole thing redraws itself when you resize the window.

To show it an image, drag the file into the terminal window and add your question.

You don't have to wait for it to finish. While it's working, just type what you forgot to say and press Enter. It gets passed along as a "by the way" and it adjusts.

Press Ctrl-C to stop a reply halfway.

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
| `frontend-build` | Web pages that actually work when you open the file |
| `landing-page` | Pages built around getting one action from a visitor |
| `accessibility` | Making a page usable by keyboard, screen reader and low vision |
| `human-writing` | Copy, posts and emails that read like a person wrote them |
| `social-posts` | Instagram, TikTok, X and LinkedIn captions in your voice |
| `client-proposal` | Quotes and scopes of work a client can say yes to |
| `summarize` | Boiling a long document down for someone with thirty seconds |
| `web-research` | Finding current facts and saying where they came from |
| `data-analysis` | Getting an honest answer out of a spreadsheet |
| `debugging` | Finding the real cause before changing anything |
| `code-review` | Catching bugs before they ship |
| `security-check` | Spotting common security mistakes in your own site or app |
| `python-scripting` | Scripts that automate a job and have actually been run |
| `git-workflow` | Committing, branching and undoing without losing work |
| `mac-automation` | Getting things done on your Mac without breaking it |
| `email-writing` | Emails and messages that get an answer |
| `sales-outreach` | First messages to a client that don't read like spam |
| `video-script` | Scripts for Reels, TikTok and Shorts |
| `brand-naming` | Names for a business, product or app |
| `pricing-offers` | What to charge and how to package it |
| `seo-basics` | Getting a page found on Google |
| `plan-project` | Turning a vague goal into steps |
| `explain-teach` | Explaining something hard so it sticks |
| `react-components` | React components and small apps |
| `api-design` | Endpoints that are clear and safe |
| `sql-database` | Tables and queries that return the right rows |
| `bash-scripting` | Shell scripts that don't break on a space |

## How fast it is

This is a big model running on a laptop, not a data center. On a 24GB MacBook Air it writes around three words a second. Short answers land in under a minute. Jobs where it has to look several things up can take a few minutes. A Mac with a Pro or Max chip is quicker.

That's the trade. It's slower, and it's yours.

## Be careful with it

It's uncensored, and when it runs a command it runs it as you, with nothing fencing it in. So read what it's asking before you say yes. It offers an "always" option that stops it asking for the rest of the session. I'd leave that alone unless you're watching.

## Settings

Optional. Set any of these before launching.

| Setting | Default | What it changes |
|---|---|---|
| `BXZEX_VOICE_LANG` | `en` | The language you speak in, like `es`. Use `auto` to let it figure it out. |
| `BXZEX_CTX` | `32768` | How much conversation it can hold at once. |
| `BXZEX_PORT` | `8080` | The local port it uses. |

The model stays in memory after you quit so the next launch is instant. To shut it down and get that memory back: `pkill llama-server`.

## Remove it

```sh
pkill llama-server
rm -rf ~/.bxzex-ai "$(brew --prefix)/bin/bxzex-ai"
```

## Credits

The app, the installer, the skills and the terminal design are © 2026 bxzex. All rights reserved.

It's free to install and use, for anything. What you can't do is copy it, repost it, rebrand it or put out your own version of it. If you want to share it, send people here. The full terms are in [LICENSE](LICENSE).

It stands on good open source work: [llama.cpp](https://github.com/ggml-org/llama.cpp) runs the model and [whisper.cpp](https://github.com/ggerganov/whisper.cpp) does the listening. The model is open-weight and is downloaded during install under its own license. The DeLorean that flies past during install is ASCII art by mozz, the one on the start screen is braille art, and the logo is set in the TheDraw font Bio Hazard.

More of what I build is at [bxzex.com](https://bxzex.com). Say hi on Instagram: [@bxzex](https://www.instagram.com/bxzex/).
