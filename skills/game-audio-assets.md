---
name: game-audio-assets
description: Sound, music and art for games: Web Audio unlock, Howler.js, retro SFX, free licensed assets, atlases, drawing in code and compression.
---
# Game audio and assets

**Audio must unlock on a gesture.** Browsers block sound until the user taps or clicks. Start audio from the first Play tap:
```js
let ctx;
function unlockAudio() {
  ctx ??= new (window.AudioContext || window.webkitAudioContext)();
  if (ctx.state === 'suspended') ctx.resume();
}
addEventListener('pointerdown', unlockAudio, {once: true});
addEventListener('keydown', unlockAudio, {once: true});
```
iOS Safari also mutes Web Audio when the silent switch is on for some setups; do not rely on sound alone to communicate anything.

**Howler.js** (`npm i howler`) is the easy path for SFX and music: `new Howl({src: ['jump.ogg', 'jump.m4a']})`, `.play()`, `.volume()`, `Howler.mute(true)`. Audio sprites put many sounds in one file: `sprite: {jump: [0, 300], coin: [400, 250]}` then `play('jump')`. Check howlerjs.com docs if unsure about options.

**Retro SFX without files.** Generate jsfxr-style sounds in code with an oscillator and a quick envelope:
```js
function beep(freq = 440, dur = 0.1, type = 'square', vol = 0.15) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = type; o.frequency.setValueAtTime(freq, ctx.currentTime);
  o.frequency.exponentialRampToValueAtTime(freq * 2, ctx.currentTime + dur);
  g.gain.setValueAtTime(vol, ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
  o.connect(g).connect(ctx.destination); o.start(); o.stop(ctx.currentTime + dur);
}
```
Rising pitch for pickups, falling for hits, noise bursts for explosions. Vary pitch slightly each play (plus or minus 5 percent) so repeats do not grate.

**Music**
- Use a loop that is seamless (cut at a beat; ogg loops cleaner than mp3, which adds padding).
- Keep music quieter than SFX (about 0.3 vs 0.7).
- Duck music briefly under big sounds or on pause: lower gain over 200 ms.
- Stop or lower music when the tab is hidden.

**Settings.** Mute toggle always visible; save music and SFX volume in `localStorage` (try/catch) and apply on load.

**Free assets and licenses**
- Kenney (kenney.nl) is CC0: no credit needed. Good for sprites, UI, sounds, 3D models.
- OpenGameArt: each asset has its own license (CC0, CC-BY, CC-BY-SA, GPL). Read it every time.
- CC-BY needs credit. CC-BY-SA requires sharing changes under the same license. Avoid non-commercial licenses if the game may be monetized.
- Keep a `CREDITS.md`: asset name, author, source URL, license. Add credits on the game's about screen when required.
- Do not use ripped assets from commercial games or unlicensed images from search.

**Sprite sheets and atlases.** Pack many images into one texture to cut requests and draw calls. TexturePacker is paid with a free tier; free options are free-tex-packer, `spritesmith`, or ImageMagick `magick montage`. Phaser and Pixi read the JSON atlas format. Keep frame sizes consistent and leave 1 to 2 px padding to avoid edge bleeding.

**Drawing assets in code.** When nothing fits, draw with SVG or Canvas: simple shapes, gradients, a limited palette of 4 to 6 colors, consistent outline width. Render to an offscreen canvas once and reuse it as a sprite. Consistent simple art looks better than mixed styles.

**Fonts.** Load with `@font-face` or Google Fonts, use `font-display: swap`, and wait for `document.fonts.ready` before drawing text on canvas. Pixel or display fonts for titles, a readable sans for small HUD text.

**Compression**
- Images: WebP (or AVIF) for backgrounds; PNG for tiny pixel art. `magick in.png -quality 80 out.webp`.
- 3D textures: KTX2 (Basis) via `toktx` or gltf-transform.
- Audio: ogg Vorbis plus m4a (AAC) or mp3 fallback, since Safari support for ogg varies. `ffmpeg -i in.wav -c:a libvorbis -q:a 4 out.ogg` and `-c:a aac -b:a 96k out.m4a`.
- Mono for SFX, 96 to 128 kbps for music. Aim for a first load under a few MB.

**Verify with test_page.** Load the game on iPhone and Android, portrait and phone-landscape. Check there are no console errors or 404s for missing images, sounds and fonts, the first tap starts audio without errors, and the screenshots show art that is sharp and not stretched.
