# BXZEX Uncensored AI — Local Model

An AI that lives on your Mac and answers to nobody but you.

No account. No subscription. No filter deciding what you're allowed to ask. It runs on your own machine, in the terminal, and nothing you type, say or show it ever leaves your laptop. Turn the wifi off and it still works.

I built this for myself, liked it too much to keep it, and I'm giving it away free.

— Brian · [bxzex.com](https://bxzex.com) · Instagram [@bxzex](https://www.instagram.com/bxzex/)

## What it does

- **Talks to you.** Ask it anything. It doesn't lecture and it doesn't refuse.
- **Goes online when it needs to.** It searches the web and reads pages to get you current answers.
- **Sees images.** Drag a photo or screenshot into the window and ask about it.
- **Does things on your Mac.** It can run commands and read or write files. It shows you exactly what it wants to do and waits for your yes first.
- **Listens.** Type `/v`, say what you want, and your words show up at the prompt ready to send.
- **Looks how you want.** Nine color themes. Pick one during install or switch any time with `/color`.

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
| `/fast` | Switch fast mode. It's on by default and answers right away. Turn it off when you want it to think a hard question through first. |
| `/think` | Show or hide its thinking when fast mode is off. |
| `/reset` | Start a fresh conversation. |
| `exit` | Quit. |

To show it an image, drag the file into the terminal window and add your question.

Press Ctrl-C to stop a reply halfway.

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

The app, the installer and the terminal design are © 2026 bxzex (Brian Ochoa), released under the MIT license. Use it, share it, build on it. Just keep the copyright notice with it.

It stands on good open source work: [llama.cpp](https://github.com/ggml-org/llama.cpp) runs the model and [whisper.cpp](https://github.com/ggerganov/whisper.cpp) does the listening. The model is open-weight and is downloaded during install under its own license. The DeLorean in the loading screen is ASCII art by mozz.

More of what I build is at [bxzex.com](https://bxzex.com). Say hi on Instagram: [@bxzex](https://www.instagram.com/bxzex/).
