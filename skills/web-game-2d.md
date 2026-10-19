---
name: web-game-2d
description: Building 2D browser games with Canvas 2D, Phaser 3 or PixiJS: game loop, input, collisions, sprites, scenes, resizing and performance.
---
# 2D browser games

**Pick the tool**
- Tiny game (one screen, a few dozen objects): plain Canvas 2D in one HTML file. No build step.
- Bigger game (scenes, tilemaps, physics, many sprites, audio): Phaser 3.
- Rendering-heavy (thousands of sprites, effects) where you write your own game logic: PixiJS.
- Versions and APIs change. If unsure, `web_search` or `fetch_page` on the official docs (phaser.io, pixijs.com) before writing code.

**Vite setup (for Phaser or Pixi):** `npm create vite@latest game -- --template vanilla`, then `npm i phaser` (or `pixi.js`), `npm run dev`. Put images and audio in `public/` and load them by absolute path like `/assets/player.png`. `npm run build` outputs `dist/`; use `base: './'` in `vite.config.js` if it will be hosted in a subfolder.

**Fixed-timestep loop.** Update physics at a steady rate, draw once per frame, cap the delta so a hidden tab does not cause a huge jump:
```js
const STEP = 1 / 60;
let last = performance.now(), acc = 0;
function frame(now) {
  acc += Math.min((now - last) / 1000, 0.1); // cap at 100 ms
  last = now;
  while (acc >= STEP) { update(STEP); acc -= STEP; }
  render(acc / STEP); // alpha for interpolation
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```
Phaser and Pixi have their own loops; use their delta and cap it the same way.

**Input**
- Keyboard: track a `keys` set on keydown/keyup, read it in update. Use `event.code` (`KeyW`, `Space`). Call `preventDefault` for arrows and space.
- Mouse and touch: use pointer events (`pointerdown`, `pointermove`, `pointerup`) so one code path handles both. Set `touch-action: none` on the canvas.
- On-screen controls for phones: big buttons (at least 48 px), placed at the thumbs, `pointerdown`/`pointerup` for hold, multi-touch allowed. Show them only on touch devices.
- Gamepad: poll `navigator.getGamepads()` each frame.

**Collisions**
- AABB rectangle overlap: `a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y`.
- Circles: compare squared distance to squared radius sum.
- Tilemaps: convert position to tile index, check the solid tiles around the player; resolve x and y axes separately.
- Phaser Arcade physics: `this.physics.add.collider(player, platforms)` and `overlap` for pickups. Fast objects can tunnel through thin walls; keep speed per frame below the wall thickness.

**Sprites and animation.** Use spritesheets with a fixed frame size. In Phaser: `this.load.spritesheet('hero', 'hero.png', {frameWidth: 32, frameHeight: 32})`, then `anims.create`. In Canvas: `ctx.drawImage(img, fx*32, fy*32, 32, 32, x, y, 32, 32)` and advance the frame by elapsed time, not by frame count.

**Camera.** Follow the player with smoothing (lerp toward the target), clamp to level bounds. Phaser: `cameras.main.startFollow(player, true, 0.1, 0.1)`.

**Scenes.** Keep distinct states: Boot (load assets, show progress), Menu, Play, GameOver. Reset all state when entering Play so restart is clean.

**Resize and sharp pixels**
- Keep a fixed logical size (for example 480x270) and scale to fit; letterbox the rest.
- For crisp canvas: set `canvas.width = cssWidth * devicePixelRatio`, then `ctx.scale(dpr, dpr)`.
- Pixel art: `image-rendering: pixelated;` in CSS and `ctx.imageSmoothingEnabled = false`. In Phaser set `pixelArt: true` and `scale: {mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH}`.
- Handle `resize` and `orientationchange`.

**Pause when hidden.** `document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); })`. Also mute audio and stop timers.

**Performance**
- Object pools for bullets, particles, enemies: reuse instead of `new` and splice.
- No allocations in the loop: no new arrays, objects or closures per frame; no string building.
- Pre-render static backgrounds to an offscreen canvas.
- Draw only what is on screen. Batch sprites from one atlas.

**Verify with test_page.** Open as iPhone and Android in portrait and phone-landscape, iPad, and desktop. Confirm the game starts, there are no console errors, no sideways scroll, controls are reachable, and the canvas fills the screen without blur. Use `steps` like "click Start", "press Space", "wait 2000", then check the screenshots.
