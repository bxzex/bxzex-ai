#!/bin/bash
# BXZEX Uncensored AI
# Copyright (c) 2026 bxzex. All rights reserved. · https://bxzex.com
# Free to use. Not to be copied, modified, rebranded or redistributed. See LICENSE.
#
#   curl -fsSL https://raw.githubusercontent.com/bxzex/bxzex-ai/main/install.sh | bash
#
# Safe to run again: finished downloads are skipped and interrupted ones resume.
set -euo pipefail

REPO="https://raw.githubusercontent.com/bxzex/bxzex-ai/main"
WEIGHTS="https://huggingface.co/bartowski/orcarouter_Qwen3.8-27B-Uncensored-GGUF/resolve/main"
BXZEX_HOME="${BXZEX_HOME:-$HOME/.bxzex-ai}"
LOG="$BXZEX_HOME/install.log"

R=$'\033[0m'; D=$'\033[2m'; B=$'\033[1m'
A=$'\033[38;5;39m'   # accent, replaced once a color is picked
COLORS="blue red orange gold green cyan purple pink white"
SKILLS="accessibility api-design bash-scripting brand-naming client-proposal code-review data-analysis debugging email-writing explain-teach frontend-build git-workflow human-writing landing-page mac-automation no-ai-slop plan-project pricing-offers python-scripting react-components sales-outreach security-check seo-basics social-posts sql-database summarize ui-design video-script web-research"
code_for() { case "$1" in blue) echo 39;; red) echo 196;; orange) echo 208;; gold) echo 220;; green) echo 46;; cyan) echo 51;;
             purple) echo 141;; pink) echo 205;; white) echo 255;; *) echo 39;; esac; }

ok()   { printf '  %s✓%s %s\n' "$A" "$R" "$*"; }
note() { printf '  %s%s%s\n' "$D" "$*" "$R"; }
die()  { printf '\033[?25h\n  %s✗ %s%s\n' "$A" "$*" "$R" >&2; exit 1; }
trap 'printf "\033[?25h"' EXIT

# curl | bash leaves stdin as the script itself, so questions go to the terminal directly
ask() {   # prompt -> reply on stdout, empty when there is no terminal or BXZEX_YES=1
  [ "${BXZEX_YES:-}" = 1 ] && return 0
  [ -r /dev/tty ] || return 0
  printf '%s' "$1" > /dev/tty
  local reply; IFS= read -r reply < /dev/tty || true
  printf '%s' "$reply"
}

pick_color() {
  local choice="${BXZEX_COLOR:-}" i=1 name
  if [ -z "$choice" ] && [ ! -f "$BXZEX_HOME/config.json" ]; then
    printf '  Pick your color:\n\n'
    for name in $COLORS; do
      printf '   %s%d%s  \033[38;5;%sm████  %s%s\n' "$D" "$i" "$R" "$(code_for "$name")" "$name" "$R"; i=$((i+1))
    done
    printf '\n'
    choice="$(ask "  number or name (Enter for blue): ")"
    case "$choice" in [1-9]) choice="$(echo $COLORS | cut -d' ' -f"$choice")";; esac
  fi
  [ -n "$choice" ] || return 0
  case " $COLORS " in *" $choice "*) ;; *) choice=blue;; esac
  A=$'\033[38;5;'"$(code_for "$choice")m"
  printf '{"color": "%s"}\n' "$choice" > "$BXZEX_HOME/config.json"
  ok "color set to $choice (change it any time with /color)"
}

# run a command with a little car driving back and forth until it finishes
drive() {   # label, command...
  local label="$1"; shift
  "$@" >>"$LOG" 2>&1 &
  local pid=$! i=0 k bars="▁▂▃▅▆▇▆▅▃▂" row
  printf '\033[?25l'
  while kill -0 "$pid" 2>/dev/null; do
    row=""
    for ((k = 0; k < 12; k++)); do row+="${bars:$(( (i + k * 3 + RANDOM % 2) % 10 )):1}"; done
    printf '\r\033[K  %s%s%s  %s' "$A" "$row" "$R" "$label"
    i=$((i + 1)); sleep 0.08
  done
  printf '\r\033[K\033[?25h'
  if wait "$pid"; then ok "$label"; else tail -15 "$LOG" >&2; die "$label failed. Full log: $LOG"; fi
}

size_of() { stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || echo 0; }

download() {   # url, destination, label
  local url="$1" dest="$2" label="$3" total pid t0 from have
  [ -f "$dest" ] && { ok "$label"; return; }
  total="$(curl -sIL "$url" | tr -d '\r' | awk 'tolower($1)=="content-length:" {n=$2} END {print n+0}')"
  from="$(size_of "$dest.part")"; t0="$(date +%s)"
  curl -fL -C - -s -o "$dest.part" "$url" &
  pid=$!
  printf '\033[?25l'
  while kill -0 "$pid" 2>/dev/null; do
    have="$(size_of "$dest.part")"
    awk -v h="$have" -v t="$total" -v f="$from" -v s="$(( $(date +%s) - t0 ))" -v a="$A" -v r="$R" -v d="$D" -v l="$label" 'BEGIN {
      w = 28; p = (t > 0) ? h / t : 0; if (p > 1) p = 1; fill = int(p * w); bar = ""
      for (i = 0; i < w; i++) bar = bar ((i < fill) ? "█" : (i == fill) ? "►" : "─")
      rate = (s > 0) ? (h - f) / s : 0
      eta = (rate > 0 && t > h) ? (t - h) / rate : 0
      left = (eta >= 3600) ? sprintf("%dh%02dm", eta / 3600, (eta % 3600) / 60) : (eta >= 60) ? sprintf("%dm", eta / 60 + 1) : sprintf("%ds", eta)
      printf "\r\033[K  %s%s%s %3d%%  %s%.1f of %.1f GB · %.0f MB/s · %s left%s  %s", a, bar, r, p * 100, d, h / 1e9, t / 1e9, rate / 1e6, left, r, l
    }'
    sleep 0.5
  done
  printf '\r\033[K\033[?25h'
  wait "$pid" || die "$label did not finish downloading. Run the installer again and it picks up where it stopped."
  mv "$dest.part" "$dest"
  ok "$label"
}

# ---- checks ----
OS="$(uname -s)"; ARCH="$(uname -m)"
case "$OS" in
  Darwin) [ "$ARCH" = arm64 ] || die "On a Mac this needs Apple Silicon (M1 or newer)." ;;
  Linux)  case "$ARCH" in x86_64|aarch64|arm64) ;; *) die "This needs a 64-bit Intel, AMD or ARM computer." ;; esac ;;
  *)      die "This runs on macOS and Linux. On Windows, install WSL first (wsl --install), open Ubuntu, and run this there." ;;
esac
command -v curl >/dev/null || die "curl is required."
command -v python3 >/dev/null || die "python3 is required. On a Mac run: xcode-select --install. On Linux: sudo apt install python3"
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' || die "python3 3.9 or newer is required."
mkdir -p "$BXZEX_HOME/bin" "$BXZEX_HOME/models" "$BXZEX_HOME/skills"
: > "$LOG"

# ---- the app (first, so it can draw the logo) ----
src="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" && pwd)"
[ -f "$src/install.sh" ] && [ -f "$src/bxzex-ai" ] || src=""
fetch() {   # path inside the repo, destination
  if [ -n "$src" ]; then cp "$src/$1" "$2"; else curl -fsSL -o "$2" "$REPO/$1"; fi
}
for f in bxzex-ai bxzex-server; do fetch "$f" "$BXZEX_HOME/bin/$f"; chmod +x "$BXZEX_HOME/bin/$f"; done
for k in $SKILLS; do fetch "skills/$k.md" "$BXZEX_HOME/skills/$k.md"; done

python3 "$BXZEX_HOME/bin/bxzex-ai" --logo || true
printf '\n   %sU N C E N S O R E D   ·   L O C A L   A I%s\n' "$B" "$R"
printf '   %shttps://bxzex.com · instagram.com/bxzex%s\n\n' "$D" "$R"
note "Free to use, at your own risk. You are responsible for what you do with it. Terms: github.com/bxzex/bxzex-ai"
printf '\n'
pick_color
python3 "$BXZEX_HOME/bin/bxzex-ai" --flyby || true
ok "app"
ok "skills"

if [ "$OS" = Darwin ]; then ram=$(( $(sysctl -n hw.memsize) / 1073741824 ))
else ram=$(( $(awk '/MemTotal/ {print $2}' /proc/meminfo) / 1048576 )); fi
vram=0
if [ "$OS" = Linux ] && command -v nvidia-smi >/dev/null 2>&1; then
  vram=$(( $(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | sort -n | tail -1 || echo 0) / 1024 ))
fi
if [ "$ram" -lt 23 ] && [ "$vram" -lt 15 ]; then
  note "This computer has ${ram}GB of memory. The model wants about 17GB, so it may be very slow or fail to load."
  case "$(ask "  Install anyway? [y/N] ")" in y|Y|yes) ;; *) [ "${BXZEX_YES:-}" = 1 ] || die "stopped";; esac
fi

# ---- engines ----
if [ "$OS" = Darwin ]; then
  command -v brew >/dev/null || die "Homebrew is required. Install it from https://brew.sh and run this again."
  for pair in "llama.cpp:chat engine" "whisper-cpp:voice engine" "ffmpeg:audio tools"; do
    pkg="${pair%%:*}"; label="${pair#*:}"
    if brew list "$pkg" >/dev/null 2>&1; then ok "$label"
    else HOMEBREW_NO_AUTO_UPDATE=1 drive "$label" brew install "$pkg"; fi
  done
else
  # Linux: a ready-built engine matched to the graphics card, kept inside our own folder
  eng="$BXZEX_HOME/engine"; tag="${BXZEX_ENGINE_TAG:-b11401}"
  case "$ARCH" in x86_64) cpu=x64 ;; *) cpu=arm64 ;; esac
  if [ "$vram" -gt 0 ] && [ "$cpu" = x64 ]; then kind="cuda-12.8-$cpu"
  elif ls /usr/share/vulkan/icd.d/*.json /etc/vulkan/icd.d/*.json >/dev/null 2>&1; then kind="vulkan-$cpu"
  else kind="$cpu"; fi
  kind="${BXZEX_ENGINE:-$kind}"
  if [ -f "$eng/.$tag-$kind" ]; then ok "chat engine"
  else
    rm -rf "$eng"; mkdir -p "$eng"
    base="https://github.com/ggml-org/llama.cpp/releases/download/$tag"
    download "$base/llama-$tag-bin-ubuntu-$kind.tar.gz" "$eng/engine.tar.gz" "chat engine"
    tar -xzf "$eng/engine.tar.gz" -C "$eng" && rm -f "$eng/engine.tar.gz"
    case "$kind" in cuda-*)
      download "$base/cudart-llama-$tag-bin-ubuntu-$kind.tar.gz" "$eng/runtime.tar.gz" "graphics runtime"
      tar -xzf "$eng/runtime.tar.gz" -C "$eng" && rm -f "$eng/runtime.tar.gz" ;;
    esac
    [ -n "$(find "$eng" -name llama-server -type f | head -1)" ] || die "The chat engine did not unpack correctly."
    touch "$eng/.$tag-$kind"
  fi
  [ "$kind" = "$cpu" ] && note "No supported graphics card found, so it will run on the processor. That works, but slowly."
  # the engine needs a few standard system libraries; say exactly which if any are missing
  srv="$(find "$eng" -name llama-server -type f | head -1)"
  missing="$(LD_LIBRARY_PATH="$(dirname "$srv"):$eng" ldd "$srv" 2>/dev/null | awk '/not found/ {print $1}' | sort -u | tr '\n' ' ')"
  case "$missing" in *libgomp*)
    if [ "$(id -u)" = 0 ] && command -v apt-get >/dev/null; then drive "system library" apt-get install -y libgomp1
    else die "One system library is missing. Run this, then run the installer again:  sudo apt install libgomp1"; fi
    missing="$(LD_LIBRARY_PATH="$(dirname "$srv"):$eng" ldd "$srv" 2>/dev/null | awk '/not found/ {print $1}' | sort -u | tr '\n' ' ')" ;;
  esac
  [ -z "$missing" ] || die "The chat engine needs system libraries that are not installed: $missing"
fi

# ---- the model ----
m="$BXZEX_HOME/models"
if [ ! -f "$m/bxzex-model.gguf" ]; then
  free="$(df -Pk "$HOME" | awk 'NR==2 {print int($4 / 1048576)}')"
  need=24; [ "$OS" = Darwin ] || need=18
  [ "$free" -ge "$need" ] || [ -n "${BXZEX_MODEL_URL:-}" ] || die "Not enough disk space: the downloads need about $((need - 1))GB and ${free}GB is free."
  note "Downloading the AI model. It is about 15GB, so this is the long part."
fi
download "${BXZEX_MODEL_URL:-$WEIGHTS/orcarouter_Qwen3.8-27B-Uncensored-Q3_K_M.gguf}" "$m/bxzex-model.gguf"  "AI model"
[ -n "${BXZEX_MODEL_URL:-}" ] || download "$WEIGHTS/mmproj-orcarouter_Qwen3.8-27B-Uncensored-f16.gguf"  "$m/bxzex-vision.gguf" "vision"
if [ "$OS" = Darwin ]; then
  download "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin" "$m/bxzex-voice.bin" "voice"
else
  note "Voice input and image generation are Mac-only for now. Everything else works here."
fi

# ---- image generation (Mac only; set BXZEX_IMAGES=0 to skip) ----
if [ "$OS" = Darwin ] && [ "${BXZEX_IMAGES:-1}" != 0 ]; then
  brew list uv >/dev/null 2>&1 || command -v uv >/dev/null || HOMEBREW_NO_AUTO_UPDATE=1 drive "image tools" brew install uv
  if [ -x "$HOME/.local/bin/mflux-generate-z-image-turbo" ] || command -v mflux-generate-z-image-turbo >/dev/null; then ok "image engine"
  else drive "image engine" uv tool install --python 3.12 mflux; fi
  if [ -f "$m/bxzex-image/.done" ]; then ok "image generation"
  else
    note "Downloading image generation, about 5.5GB."
    drive "image generation" uvx --from huggingface_hub hf download mflux-community/z-image-turbo-mflux-q4 --local-dir "$m/bxzex-image"
    touch "$m/bxzex-image/.done"
  fi
  mkdir -p "$BXZEX_HOME/loras"
  download "https://github.com/bxzex/bxzex-ai/releases/download/assets/bxzex-image-style.safetensors" "$BXZEX_HOME/loras/bxzex-image-style.safetensors" "image style"
fi

if [ "$OS" = Darwin ]; then bindir="$(brew --prefix)/bin"; else bindir="$HOME/.local/bin"; mkdir -p "$bindir"; fi
ln -sf "$BXZEX_HOME/bin/bxzex-ai" "$bindir/bxzex-ai"
ok "command added"
case ":$PATH:" in *":$bindir:"*) ;; *)
  for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    [ -f "$rc" ] && ! grep -q '.local/bin' "$rc" && printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$rc"
  done ;;
esac

python3 "$BXZEX_HOME/bin/bxzex-ai" --car || true
printf '\n  %s%sREADY.%s Open a new terminal window and type: %sbxzex-ai%s\n' "$B" "$A" "$R" "$B" "$R"
printf '  %shttps://bxzex.com · instagram.com/bxzex · © 2026 bxzex%s\n\n' "$D" "$R"
