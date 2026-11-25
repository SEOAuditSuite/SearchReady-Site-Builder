# SearchReady Site Builder — Pilot 03: Margin Atlas

**Type:** Fictional editorial/content publication (deliberately different from the first two local-service websites).  
**Status:** Internal staging demonstration and focused reusability evidence. **Not a public/production site.**

## What this pilot validates

- Content-first information architecture across five pages, including a journal index and two full articles.
- Independent art direction: typographic editorial layout, a custom original abstract SVG map, no stock imagery, and no external fonts, JavaScript CDNs or analytics.
- A mobile-first site design with real navigation, readable long-form text, semantic HTML, a keyboard-accessible menu, and no-JS navigation fallback.
- SEO foundations: route-specific titles/descriptions/H1s, crawlable article/internal links, alt text, source-level staged index policy (`noindex`), no fictional structured data or canonical URL.
- Client-side journal filtering with a polite live status and a visible empty state. Search does not transmit queries.
- Contrast-aware keyboard focus on dark surfaces, reduced-motion styling, and 320–1440px browser layout checks.

## Run locally

From this directory with Python 3.12+:

```sh
python -m http.server 8767 --bind 127.0.0.1 --directory site
```

Then open `http://127.0.0.1:8767/index.html` in a browser. This basic server is only for local demonstration, not production hosting.

## Reproducible tests

```sh
python tools/site_preflight.py site --mode staging
python tools/test_editorial_pilot.py
python tools/test_inline_browser.py
```

`test_editorial_pilot.py` requires `beautifulsoup4` and `playwright` plus Chrome/Chromium; it starts a temporary loopback server and uses a fresh browser. The `test_inline_browser.py` script renders the same HTML/CSS/JS in Chromium without navigation to localhost, explicitly **not** a replacement for an actual HTTP URL browser test.

`build.py` is the original content/site source generator, retained for source provenance. Run it only in a disposable copy if you deliberately wish to regenerate site HTML/CSS/JS. No modifications are needed for normal testing.

## Important production boundaries

This site is fictional and intentionally not indexed; no live origin is confirmed. It has no production canonical, sitemap, analytics, policy pages, hosting/TLS, or measured field Core Web Vitals. Static HTTP status checks and browser render checks do not certify production SEO, WCAG 2.2 AA accessibility, or real search indexing. Do not publicly deploy this demo unchanged.
