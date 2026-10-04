---
name: react-components
description: Writing or fixing React components and small React apps.
---
# React

First read the project: which React version, TypeScript or not, how styles are done, which libraries are already there. Match what exists.

**Components**
- Function components and hooks.
- One job per component. If a file passes about 150 lines, split it.
- Props in, events out. Name handlers `onSomething`.
- Derive values during render instead of storing them in state. State is only for what the user can change.
- Keep state as low in the tree as it can live.

**Hooks**
- Only at the top level. Never inside conditions or loops.
- `useEffect` is for syncing with the outside world: fetching, subscriptions, timers. Not for computing values from props.
- Every effect lists all the values it uses, and cleans up what it starts.
- Reach for `useMemo` and `useCallback` only when you have measured a problem.

**Lists and forms**
- Stable, unique `key` on list items. Never the array index when the list can change.
- Controlled inputs. A `label` for every field.

**States**
- Every data view handles loading, empty and error. Build all three.
- Disable the submit button while a request is in flight.

**Quality**
- No `any` in TypeScript without a reason.
- Semantic HTML and keyboard access, same as any page.
- Do not add a dependency for something ten lines of code can do.

Run the type check and the build, and fix what they report, before saying it works. For the look, load ui-design and no-ai-slop.
