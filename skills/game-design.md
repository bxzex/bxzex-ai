---
name: game-design
description: Making a game fun and finished: core loop, first 30 seconds, controls, game feel, difficulty, scoring, menus, saving and scope.
---
# Game design that ships

Small but complete beats big and broken. A game that loads, plays for two minutes, and restarts cleanly is better than a huge one that half works. Build the smallest version first, then add.

**Core loop in one sentence.** Write it before any code: "Dodge cars to collect coins and go farther each run." If you cannot say it in one sentence, cut features until you can. Everything you add must feed that loop.

**First 30 seconds**
- The player should be playing within 2 taps from page load. No long intro, no login, no wall of text.
- Teach by doing: the first obstacle or enemy should be easy and obviously safe to fail on.
- One short hint on screen ("Tap to jump") that disappears after the first input.
- First reward within 10 seconds (a point, a coin, a kill, a sound).

**Controls that feel good**
- Input buffering: remember a jump press for about 100 ms and fire it when the player lands.
- Coyote time: allow a jump for about 100 ms after walking off a ledge.
- Variable jump height: cut upward speed when the button is released early.
- Respond on the same frame as the input. Use pointerdown, not click, for touch.
- Make hitboxes slightly smaller than the sprite for the player and slightly larger for pickups.
- Accelerate and decelerate quickly; instant stops feel stiff, slow ones feel slippery.

**Game feel ("juice")**
- Screen shake on big hits: a few frames, small amplitude, decaying fast.
- Hit pause: freeze 40 to 80 ms on impact.
- Particles on jumps, landings, pickups, deaths.
- Squash and stretch on jump and land; flash white on damage.
- Floating score numbers, pop animations on UI counters.
- A sound on every action: jump, land, pickup, hit, click, win, lose. Silence feels broken.
- Keep juice optional-friendly: shake and flashing should be reduced if the user asks (prefers-reduced-motion).

**Difficulty and pacing**
- Ramp slowly: introduce one new thing, let the player master it, then combine.
- Alternate tension and rest; a calm moment after a hard section.
- Cap the speed or spawn rate so it stays beatable. Tune with numbers in one `CONFIG` object at the top.
- Deaths should feel fair: the player can say what they did wrong.

**Scoring**
- Show score and best score always. Reward risk with combos or multipliers that reset on a mistake.
- Show "New best!" on game over and what the player was close to beating.

**Fail fast, restart faster.** Game over to playing again in one tap, under a second. No confirm dialogs. Show score, best, and a big Play Again button.

**Menus and settings**
- Title screen with Play, a mute toggle, and a short how-to-play.
- Pause on Escape/P and when the tab is hidden; resume with a countdown or tap.
- Mute and volume remembered between visits.

**Saving.** Use `localStorage` in try/catch (it can throw in private mode):
```js
const save = (k, v) => { try { localStorage.setItem('mygame:' + k, JSON.stringify(v)); } catch {} };
const load = (k, d) => { try { return JSON.parse(localStorage.getItem('mygame:' + k)) ?? d; } catch { return d; } };
```
Save best score, settings, unlocked levels. Version the save so old data does not crash new code.

**Scope control**
1. Build a playable vertical slice first: title, one level or endless mode, score, game over, restart.
2. Use `update_todos` to list features in priority order; finish one before starting the next.
3. Placeholder shapes first, art later. Cut anything that is not working by the end.

**Verify with test_page.** Open the game as iPhone and Android in portrait and in phone-landscape, plus desktop. Check: it loads, no console errors, no sideways scroll, tap targets are big enough, the HUD is not cut off by notches or the browser bar, and the screenshots look right. Use `steps` such as "click Play", "press Space", "wait 2000" to reach gameplay and the game over screen, then screenshot those too.

**Playtest checklist**
- Can a new player start and understand it without help?
- Does every input produce visible and audible feedback?
- Can you lose, and can you restart instantly?
- Is the first minute easier than the third?
- Does it survive tab switching, resizing, rotating the phone, and mashing every key?
- Does sound start only after the first tap, and does mute work?
