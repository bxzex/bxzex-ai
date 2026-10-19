---
name: media-ffmpeg
description: Converting, trimming, compressing and editing video, audio and images with ffmpeg and ImageMagick.
---
# Media with ffmpeg and ImageMagick

Install: `brew install ffmpeg imagemagick` on macOS, `sudo apt install ffmpeg imagemagick` on Debian, Ubuntu or WSL. Check with `ffmpeg -version`. Inspect any file first: `ffprobe -hide_banner file.mp4`.

Always write to a new filename. Add `-n` (never overwrite) or `-y` (overwrite) on purpose.

**Video**
- Convert to MP4 that plays everywhere: `ffmpeg -i in.mov -c:v libx264 -crf 23 -preset medium -c:a aac -movflags +faststart out.mp4`
- Smaller file: raise `-crf` (28 is small, 18 is near lossless).
- Resize to 720p high: `-vf scale=-2:720`
- Trim without re-encoding: `ffmpeg -ss 00:00:10 -to 00:00:25 -i in.mp4 -c copy clip.mp4` (cuts land on keyframes; re-encode for exact cuts).
- Remove audio: `-an`. Change speed 2x: `-vf "setpts=0.5*PTS" -af atempo=2`.
- Join clips: write `list.txt` with lines `file 'a.mp4'` then `ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4`.

**Audio**
- Extract: `ffmpeg -i in.mp4 -vn -c:a libmp3lame -q:a 2 out.mp3`
- Convert to WAV: `ffmpeg -i in.mp3 out.wav`
- Normalize loudness: `-af loudnorm`

**GIF** (good quality in two passes):
```
ffmpeg -i in.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,palettegen" pal.png
ffmpeg -i in.mp4 -i pal.png -lavfi "fps=12,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" out.gif
```
Keep GIFs short. For web, an MP4 or WebM is far smaller.

**Images**
- Resize: `magick in.jpg -resize 1200x out.jpg` (older installs use `convert`).
- Convert: `magick in.png out.webp`. Quality: `-quality 82`.
- Strip metadata and shrink: `magick in.jpg -strip -quality 80 out.jpg`.

**Batch loops**
```
mkdir -p out
for f in *.mov; do ffmpeg -n -i "$f" -c:v libx264 -crf 24 -c:a aac "out/${f%.mov}.mp4"; done
for f in *.png; do magick "$f" -resize 1600x "out/${f%.png}.jpg"; done
```
Quote every filename; spaces break unquoted loops.

**Check:** `ffprobe` the result for duration, size and codecs, compare `ls -lh` before and after, and play a few seconds if you can. Pitfall: `-ss` placed after `-i` is slow but exact, before `-i` is fast.
