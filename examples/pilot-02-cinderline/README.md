# SearchReady Site Builder — Pilot 02: Cinderline Cycle Studio

**Status:** Isolated, fictional staging website. **Not a released business website or final Skill verification.**

This is a second-business and second-stack acceptance fixture for the unchanged **SearchReady Site Builder candidate v0.2.0**. Pilot 01 covered a fictional home-organizing service with a mostly static site and simulated contact-brief download. Pilot 02 covers a bicycle-repair workshop concept with five distinct HTML routes, accessible navigation and a real **localhost-only Python/SQLite** demo-form pipeline.

## Run on Windows

Open a terminal in the extracted `second_pilot` folder:

```powershell
python app.py --port 8772
```

Open `http://127.0.0.1:8772/index.html`. The server binds to your own computer only. Its default SQLite database is under `data/demo-requests.sqlite`. Only **fictional** inputs should be entered.

The form **saves locally**. It does not email anyone, make an appointment, contact the internet or use payment services.

## Focused tests

The source/HTTP checks were already executed and passed. Do **not** repeat them just for appearance. The remaining acceptance gate is full real-Chrome navigation in the Windows environment where Playwright is available:

```powershell
python tools/test_browser.py
```

It launches its own isolated temporary server/database and should run the 5-page responsive flows without touching any application database. When complete, it writes `evidence/browser-results.json` and screenshots in `evidence/`.

For reproduction only (if a prior environment change or review demands it):

```powershell
python tools/test_pilot.py
python tools/site_preflight.py site --mode staging
python tools/test_render.py
```

## Architecture and safety boundaries

- Standard-library threaded HTTP server and SQLite, zero third-party runtime dependencies.
- Server-side HTML with meaningful copy, unique titles/descriptions, crawlable regular links and HTML-first navigation; all staging routes use `noindex` both in markup and response headers.
- Distinct page themes, responsive CSS, keyboard menu, focus indicators, alt text and reduced-motion preference.
- Local data form with same-origin protection, signed session/CSRF field, input length/content checks, prepared DB insert, HTML escaping, basic throttling and local-only networking. These are **not** a professional external security certification.
- No production hostname, canonicals or production sitemap. No fictional business location, fake review stars, unverifiable awards or false contact delivery. No live LCP/INP/CLS or search rankings claimed.

## Provenance

- Original candidate ZIP SHA-256: `17cb90210d95ad10753739b3db50c15ac5e2a338f1a64e6fb11891cd8dee79a7`.
- Source ZIP was **not modified**. This package is a separate Pilot 02 artifact.
- The source-level preflight tool in `tools/site_preflight.py` is byte-identical to the candidate's matching script.
- See `QA-REPORT.md` and `INDEPENDENT-REVIEW-BRIEF.md` for the evidence boundaries and remaining gates.
