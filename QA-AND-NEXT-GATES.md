> **Historical checkpoint:** Current status is in `CURRENT-ACCEPTANCE.md`; current reviewer instructions are in `CURRENT-FINAL-ACCEPTANCE-BRIEF.md`. Prior results and pending labels below are preserved for provenance.

> **Historical initial-candidate QA record:** Preserved as originally written. For the current three-pilot review candidate, use `CONSOLIDATED-ACCEPTANCE-STATUS.md` and `FINAL-ACCEPTANCE-BRIEF.md` instead.

# SearchReady Site Builder — Candidate v0.2.0 Verification Record

**Date:** 2026-11-23  
**Status:** SKILL CANDIDATE / PILOT STAGING ACCEPTANCE PARTIAL — **NOT** A PUBLIC FINAL RELEASE

## Source boundary

The earlier Pilot 01 QA document (2026-11-18) was reviewed: 62/62 limited browser render checks, 174/174 DOM checks and 6/6 offline tests were *reported*. Live HTTP-browser navigation and production validation were not performed there. Its original draft ZIP and pilot ZIP were inaccessible as raw source bytes in this environment, so this candidate must not be represented as a file-level patch or backward-compatible regression verification of that earlier draft.

## New deliverables

- Native-style `SKILL.md` with explicit launch/SEO/design gates.
- 12 standalone specialist references and combined ChatGPT Project reference guide.
- Plain-language guides for Project setup and conditional native Skills availability.
- Offline source-level preflight, narrow unit/validation tests, project templates.
- Fresh independent fictional four-page pilot: Clearroom home-organizing demo, with SVG illustration, local CSS/JS, responsive navigation and local-only demo brief download.

## Tests actually run

| Layer | Result | Exact scope |
| --- | --- | --- |
| Skill package rules and reference wiring | **7/7 PASS** | `python tools/validate_package.py`; names, paths, docs, references, safeguards |
| Offline source audit unit tests | **9/9 PASS** | `python tools/test_site_preflight.py`; valid staging and error detection for missing SEO/indexing/assets |
| Pilot source SEO preflight | **PASS: 4 pages, 0 errors** | `python tools/site_preflight.py pilot/site --mode staging`; correct deliberate `noindex`, unique titles/descriptions, H1, local links/assets |
| Real loopback HTTP transport | **9/9 PASS** | `python tools/test_http_pilot.py`; HTML routes plus CSS/JS/SVG read over 127.0.0.1 via actual HTTP |
| Browser-rendered responsive/interactions | **88/88 PASS** | `python tools/test_render_pilot.py`; actual installed Chromium; 4 pages × 5 viewport widths with unchanged inlined local HTML/CSS/JS/SVG, mobile menu, Escape, form validation and local download |
| Browser URL navigation (HTTP through Playwright) | **BLOCKED** | Attempted `test_browser_pilot.py`; Chromium `ERR_BLOCKED_BY_ADMINISTRATOR` for loopback URL, before any page checks. Not a product functional failure, but no browser URL acceptance evidence here. |

## Evidence retained

- `pilot/evidence/static_preflight.json`
- `pilot/evidence/http-results.json`
- `pilot/evidence/render-results.json`
- `pilot/evidence/browser-results.json` — blocked attempt recorded without changing earlier results
- `pilot/evidence/home-desktop-1440.png`, `home-mobile-375.png`, `contact-mobile-375.png`
- Source files and reproducible scripts in `tools/` and `pilot/site/`.

## Actual known blockers / no unsupported claims

1. Real browser URL navigation to local HTTP must be run in an unblocked environment (e.g., Windows OpenCode + installed Chrome); don't repeat existing passed static or DOM-render tests.
2. Pilot is **fictional** and explicitly `noindex`; there is no verified domain, canonical URL, production sitemap, live lead inbox, tracking policy, real business info or actual public hosting. This is intentional; do not change the demo into a public website.
3. Field LCP/INP/CLS unmeasured; lab performance not run. No WCAG 2.2 AA certification or professional security audit.
4. Source-to-rendered-browser differences were not independently audited against a production server. No outside independent UX reviewer or different business/stack second pilot yet.
5. Native installation/activation in ChatGPT workspace is NOT verified; Project reference method remains available wherever Projects are supported.

## Next focused action

Run exactly the outstanding real HTTP-browser journey through `python tools/test_browser_pilot.py` on Windows with working Python Playwright/Google Chrome; record results and screenshots. Existing source preflight, HTTP and render tests should not be repeated unless affected by changes. Then run a genuinely different second-business/stack pilot and independent design/SEO/UX review. Only after those gates and any necessary fixes should the owner approve a GitHub public release.
