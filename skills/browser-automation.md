---
name: browser-automation
description: Driving a real browser with Playwright to open pages, fill forms, click, wait and take screenshots.
---
# Browser automation with Playwright

**Install (Python)**
```
python3 -m venv .venv && . .venv/bin/activate
pip install playwright && playwright install chromium
```
On Linux or WSL missing libraries: `playwright install-deps chromium` (needs sudo).

**Install (Node)**
```
npm i -D playwright && npx playwright install chromium
```

**Minimal script (Python)**
```
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://example.com", wait_until="domcontentloaded")
    page.fill("input[name=email]", "test@example.com")
    page.get_by_role("button", name="Sign up").click()
    page.wait_for_selector("text=Thanks")
    page.screenshot(path="done.png", full_page=True)
    print(page.title())
    browser.close()
```

**Locators.** Prefer `get_by_role`, `get_by_label`, `get_by_text` over brittle CSS paths. Check what is really on the page first: `print(page.content()[:2000])`, or run `playwright codegen URL` (needs a display) to record clicks.

**Waiting.** Never use fixed sleeps. Playwright waits for elements automatically on `click` and `fill`. For results use `page.wait_for_selector`, `page.wait_for_url`, or `page.wait_for_response`. A timeout means the selector is wrong or the page differs from what you expect, so take a screenshot and look.

**Headless vs headed.** Headless is faster and works on servers. Use `headless=False` to watch it when debugging, and `slow_mo=300` to slow it down. WSL needs a display for headed mode.

**Quick screenshot with no script:** `npx playwright screenshot --viewport-size=375,800 https://example.com out.png`.

**Logins.** Save state once after the user logs in themselves: `context.storage_state(path="state.json")`, then reuse it with `browser.new_context(storage_state="state.json")`. Keep `state.json` out of git. Do not type or store the user's passwords in scripts.

**Respect the sites**
- Automate only things the user is allowed to do, on sites that allow it. Read the terms.
- Do not get around CAPTCHAs, rate limits or bot blocks.
- Add pauses between actions, run one browser at a time, and do not spam forms or accounts.

Pitfall: always close the browser (use `with` or try/finally) so processes do not pile up. Check with `pgrep -fl chrom`.
