---
name: motion-animation
description: Adding purposeful animation and transitions to a web interface that stay smooth and accessible.
---
# Motion and animation

Animate only when it explains something: a panel opening, an item added, a state changing. If removing the animation loses nothing, remove it.

**Durations and easing**
- Small feedback (hover, press, toggle): 100 to 150ms.
- Panels, menus, modals: 200 to 300ms.
- Page or large layout moves: 300 to 500ms, rarely longer.
- Entering things: `ease-out` (`cubic-bezier(0.2, 0, 0, 1)`). Leaving things: `ease-in`, and a bit faster than entering. Never `linear` except for spinners and progress.

**Use CSS first**
```
.card { transition: transform 200ms cubic-bezier(0.2,0,0,1), opacity 200ms; }
.card:hover { transform: translateY(-2px); }
```
Reach for JavaScript only for things CSS cannot do: sequencing from data, scroll-linked effects, gestures, or physics. Use the Web Animations API (`el.animate(...)`) or the project's existing library before adding a new dependency.

**Animate cheap properties.** `transform` and `opacity` run on the GPU. Do not animate `width`, `height`, `top`, `left`, `margin` or `box-shadow` on large areas, because they force layout. To open a panel, animate `transform` or use `grid-template-rows: 0fr` to `1fr`. Use `will-change: transform` only on things that are animating right now.

**Respect reduced motion**
```
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```
Parallax, auto-playing loops and large zooms are the ones that matter most.

**Check**
- Nothing blocks input while animating; users can click during a transition.
- No flash of content on load, and no layout jump when an element appears (reserve its space).
- Looping animations pause when off-screen or can be stopped.
- Test with the browser's Performance panel or by watching for jank on a slow device setting (4x CPU slowdown).

Pitfalls: stagger delays that add up to over a second, bouncing springs on serious interfaces, animating everything on scroll, animations that replay on every re-render.
