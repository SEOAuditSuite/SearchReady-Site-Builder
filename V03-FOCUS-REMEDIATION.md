> **Completed historical review:** Independent Windows focus-delta acceptance passed on 25 November 2026. See `CURRENT-ACCEPTANCE.md` for the current RELEASE-ready status. No repeat of accepted tests required.

---

## Historical record (superseded status; preserved for provenance)

# v0.3.1 D5 current-surface remediation — 25 November 2026

**HOLD only for independent re-verification of the changed focus states.**

## Inherited independent acceptance (owner-supplied report)
The exact consolidated candidate was reviewed without modifying it: manifest 185/185; package 8/8; integration 7/7; embedded platform lab 38/38; audit fixture 2/2. Fresh-agent A/B/C behavior passed (WordPress / Shopify / stay on WordPress, distinct art direction, native SEO ownership, URL preservation and 301s, truthful unavailable-tool fallbacks). Nine pages at four widths, 36 real HTTP Chrome loads: zero overflow/console errors/broken links/external requests, one visible H1 and noindex each; mobile navigation and local demo form journeys passed. Visual separation passed. Raw independent evidence remains on the owner's Windows PC, not supplied here. No previous passing suite was repeated.

The reviewer identified a narrow HOLD: 32 Clearroom footer observations, 4 Cinderline dark/coral card observations, 10 Cinderline skip-link observations and stale D5 coverage. Prior dark-footer evidence is historical; it cannot establish contrast on the new mint footer.

## Correction and author evidence
- Clearroom: remove old cream footer override; explicitly use #185d95 on #eaf9f8 (6.386:1).
- Cinderline: cream #fff7e6 on navy #111b39 (15.890:1), navy on coral #ff744d (6.338:1) and yellow #ffe36d (13.278:1).
- Cinderline skip link crosses yellow strip and navy header; a 4px navy outline at zero offset and 8px cream shadow create two distinct contrasting bands. Inner vs yellow 11.509:1, outer vs navy 15.890:1, bands vs each other 15.890:1. Explicit forced-colors system outline fallback added (not independently tested in forced-colors mode).
- Two targeted standard-library tests PASS: contrast pairs and current selector contract. CI includes these two tests. `tools/test_focus_v03.py` traverses actual Tab order with expanded mobile menus across all nine pages at 320/375/1440, compares computed focus colors to adjacent ancestor backgrounds (gradient stops included), verifies both skip-link colors and saves samples outside the package. It is not a full pixel audit; inspect representative screenshots and the skip link edges in independent Chrome.
- Author Chromium **offline DOM: 384 PASS / 0 FAIL / 0 BLOCKED; 27/27 page traversal counts match visible controls**. Source HTML, CSS, JS rendered inlined. Real localhost HTTP navigation attempted separately: **BLOCKED by ERR_BLOCKED_BY_ADMINISTRATOR**; zero live checks completed in the author environment. Original independent live passes apply to previous CSS. Raw author JSON and representative 375px screenshots are in `visual-review/v03-focus-author/`; historical D5 evidence unchanged. New script defaults to real local HTTP static source; no form POSTs, no public host.

## Remaining gate
On Windows, repeat only the corrected focus checks, real-URL all-focus scan and integrity. No fresh-agent rerun, native platform rerun, SEO audit rerun, new demos, installs, or publication needed for this correction. See CURRENT-FINAL-ACCEPTANCE-BRIEF.md. Prior native Shopify storefront/Elementor/WooCommerce/external tool runtime and production launch limitations remain. No WCAG certification or ranking guarantee.
