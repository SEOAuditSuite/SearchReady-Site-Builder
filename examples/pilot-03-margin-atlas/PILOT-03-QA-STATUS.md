# SearchReady Site Builder — Pilot 03 Quality and Evidence Record

**Date:** 23 November 2026  
**Pilot:** Margin Atlas — fictional editorial/content publication, five pages  
**Purpose:** Test the Skill's content-site architecture and design versatility beyond local-service landing pages.

## Verified locally

- 5-page staged source SEO preflight: **PASS**, zero errors, one stage info note.
- Reproducible source and actual loopback HTTP checker (`tools/test_editorial_pilot.py`): **35 PASS, 0 FAIL, 1 BLOCKED** (browser-only URL navigation). This includes source metadata, H1/index policy, relative asset/internal links, and actual loopback HTTP 200 delivery of all pages and tested assets.
- Headless Chromium rendering of exact page HTML with original inlined CSS/JS and SVG (`tools/test_inline_browser.py`): **35 PASS, 0 FAIL**. It exercises the five pages across 320/375/768/1024/1440 CSS-pixel widths, mobile menu keyboard control, active-menu Escape focus return, closed-menu Escape focus preservation, journal search filtering/empty state, and dark-background focus color.
- Full-page visual evidence: `evidence/margin-atlas-home-1440.png`, `margin-atlas-home-375.png`, `margin-atlas-journal-375.png`.
- Original visual art: `site/assets/field-map.svg`; fonts and JS/CSS are locally hosted, no network requests for external libraries specified.

## Explicitly blocked/unverified

1. **BLOCKED: Real browser navigation to loopback URLs in this authoring environment**, before any URL-browser assertions. The HTTP transport itself passed. Run the exact pending URL-browser checks in a Windows/Chrome-enabled environment only at final acceptance; do not repeat existing source/HTTP/render checks without a justified change.
2. **NOT RUN: External independent design, accessibility, technical SEO, and security sign-off** for this new third pilot.
3. **NOT RUN: Lighthouse lab performance, automated axe checks, screen-reader, 200% zoom and forced-colors user experience.** These need appropriate capable tooling and bounded human/agent review; do not conflate text and non-text contrast spot checks with WCAG 2.2 AA certification.
4. **BLOCKED by intentional demo scope: Real domain, canonical URLs, sitemap, robots, hosting security, public form delivery, monitoring, field Core Web Vitals, and business authenticity.** These are per-production-site launch requirements, not grounds to invent claims or turn a fictional demo into a public site.
5. A single original editorial pilot does not demonstrate the quality of all possible portfolios, CMSes, redesigns, e-commerce or multilingual sites. Skill should remain stack- and category-neutral, with honest limits.

## Release decision

**HOLD:** Preserve the existing Skill candidate. Before merging this pilot into a GitHub release, run a truly independent visual/source review and, if possible, the one remaining real Chrome HTTP browser gate. Do not claim a full skill-wide certification or regenerate previously PASS evidence.

## Consolidation update (23 November 2026)

After the original 35+35 checks, the Pilot 03 source generator was modified in three targeted ways: truthful `2 MIN READ` labels, a hidden H2 for journal articles, and improved metadata/footer small text. The original 35+35 JSON remains preserved as **historical**. The new `evidence/editorial-delta-results.json` records **11/11 author-side focused PASS**, and new dependency-free CI checks run as `tools/test_editorial_contract.py` (5 tests). Real URL-driven Chrome validation is still pending; run `tools/test_live_url_only.py` only when requested.
