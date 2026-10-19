---
name: web-scraping
description: Collecting public data from websites responsibly, using an API when one exists and a browser only when needed.
---
# Web scraping

1. **Look for an API first.** Check for an official API, a downloadable CSV, an RSS feed or a sitemap. In the browser's network tab, many pages load their data from a JSON URL you can call directly. Also try `curl -s URL/sitemap.xml | head`.
2. **Check the rules.** `curl -s https://site.com/robots.txt` and read the terms page. If scraping is disallowed, or the data is behind a login or is personal information, stop and tell the user. Do not bypass paywalls, CAPTCHAs or blocks.
3. **Try plain requests.**
   ```
   python3 -m venv .venv && . .venv/bin/activate
   pip install requests beautifulsoup4 lxml
   ```
   ```
   import requests
   from bs4 import BeautifulSoup
   r = requests.get(url, headers={"User-Agent": "research-script (contact: you@example.com)"}, timeout=20)
   r.raise_for_status()
   soup = BeautifulSoup(r.text, "lxml")
   rows = [{"name": c.select_one("h2").get_text(strip=True)} for c in soup.select(".card")]
   ```
   Find selectors by saving the HTML (`curl -s URL > page.html`) and reading it, not by guessing.
4. **Headless browser only if needed,** meaning the data does not appear in the raw HTML because JavaScript builds it. Then use Playwright (see browser-automation), wait for the element, and read the text. Look for the underlying JSON request before scraping the rendered page.
5. **Be gentle.** Sleep 1 to 3 seconds between requests, cache pages you already fetched, stop on repeated 429 or 403 responses, and honor any `Crawl-delay`. Fetch only what you need.
6. **Handle messy data.** Strip whitespace, parse numbers and dates into real types, deal with missing fields, deduplicate on a stable key such as an id or URL.
7. **Save it.**
   ```
   import csv, json
   with open("out.csv", "w", newline="", encoding="utf-8") as f:
       w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
   json.dump(rows, open("out.json", "w"), indent=2)
   ```
   Write results as you go on long runs so a crash does not lose everything.
8. **Check.** Count rows, print three samples, compare one against the live page by eye.

Pitfalls: ignoring pagination (follow the next link until none), silent selector breakage that yields empty fields, collecting personal data you do not need, hammering a small site.
