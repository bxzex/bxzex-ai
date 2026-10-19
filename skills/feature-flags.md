---
name: feature-flags
description: Shipping changes behind flags with simple env or database switches, gradual rollout and cleanup.
---
# Feature Flags

A flag lets you deploy code without turning it on.

1. **Start simple.**
   - Env flag: `NEW_CHECKOUT=on`. Fine for all-or-nothing on one environment. Changing it needs a redeploy or restart.
   - Database flag: a `flags` table with `key`, `enabled`, `percent`, `allow_list`. Changes apply without a deploy. Cache reads for 30 to 60 seconds.
   - Use a hosted flag service only when many people need targeting rules and audit logs.
2. **One helper.** Write a single `isEnabled(key, user)` function and use it everywhere. Never scatter raw env checks through the code.
3. **Default off.** If the flag is missing or the lookup fails, return false so the old behavior stays.
4. **Gradual rollout.** Hash a stable id: `hash(flagKey + userId) % 100 < percent`. The same user always gets the same answer. Go 1%, 10%, 50%, 100%, and watch errors and key metrics between steps. For anonymous visitors, use a cookie id.
5. **Internal first.** Add an allow list of staff emails so the team can try it in production before anyone else.
6. **Keep both paths working.** Tests should cover flag on and flag off.
7. **Kill switch.** For risky features, make sure you can turn it off in seconds without a deploy.
8. **Clean up.** When a flag has been at 100% for about two weeks, delete the check, the old code path and the flag row in one commit. Keep a list of flags with owner and date. Find stale ones: `grep -rn "isEnabled(" src | sort`.

**Check:** with the flag off, the old page renders and nothing new runs; with it on for your test user only, the new page renders and others still see the old one.

**Pitfalls:** flags nested inside flags; sending flag names to the browser that reveal unreleased plans; changing the rollout hash mid-rollout, which reshuffles users; flags that live forever and turn into permanent config.
