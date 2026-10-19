---
name: react-performance
description: Fixing slow React apps by measuring first, then cutting re-renders, needless effects and large bundles.
---
# React Performance

Measure, then fix. Most apps are slow for a few specific reasons.

1. **Measure.** Open React DevTools Profiler, record the slow interaction, and look at what rendered and why. For load time, run `npx vite build` or `npx next build` and read the bundle sizes.
2. **Fix state placement.** State that changes often (typing, hover) should live in the smallest component that needs it. Move it down, or pass children as props so the heavy parts do not re-render.
3. **Memo only where measured.** `React.memo`, `useMemo` and `useCallback` help when a child is expensive and its props are stable. Otherwise they add cost and noise. If a project uses the React Compiler, skip most manual memoizing.
4. **Keys.** Use a stable id from the data, never the array index for lists that reorder or change. A changing key remounts the component and loses state.
5. **Cut needless effects.** If a value can be computed from props or state during render, compute it there instead of `useEffect` plus `setState`. Handle clicks in event handlers, not effects. Reset state with a `key` on the component.
6. **Effects that remain.** List every dependency, return a cleanup that removes listeners and aborts fetches, and expect effects to run twice in dev strict mode.
7. **Data fetching.** Fetch on the server where the framework allows it. On the client use a data library with caching and request dedupe instead of raw `useEffect` fetches. Avoid waterfalls: start independent requests together with `Promise.all`.
8. **Code splitting.** Lazy load heavy, rarely used parts: `const Chart = lazy(() => import('./Chart'))` inside `<Suspense fallback={...}>`. In Next.js use `next/dynamic`. Split by route first.
9. **Long lists.** Over a few hundred rows, use virtualization (`@tanstack/react-virtual`). Debounce search inputs by about 200 ms.
10. **Images and fonts.** Set width and height, lazy load below the fold, serve modern formats.

**Check:** profile again after each change and compare the number and duration of renders. Keep only changes that helped.

**Pitfalls:** new object or function props created inline passed to memoized children; context values that change on every render; huge libraries imported for one function.
