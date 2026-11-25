# SearchReady Site Builder — Pilot 02 Focused Review and Remediation

**Date:** 23 November 2026  
**Artifact under review:** SearchReady Pilot 02 (Cinderline Cycle Studio), 26-file validated input ZIP.  
**Original ZIP SHA-256:** `9da28e0587482a5df45622067e5d244d94d9a58a28a6df4376492769010f07f5`  
**Related skill candidate SHA-256:** `17cb90210d95ad10753739b3db50c15ac5e2a338f1a64e6fb11891cd8dee79a7`  
**Scope:** Read-only independent-style examination of supplied source and screenshots, followed by three **minimal fixes in a separate copy**. Original artifact and the skill candidate were not edited. This is not an independent third-party certification; the original authoring assistant also conducted this review pass.

## Evidence and design findings

- **Visual design — positive, source and screenshot inspected.** Distinct editorial bicycle theme, bespoke SVG hero, a considered forest/ivory/terracotta palette, identifiable buttons and hierarchy. Desktop 1440px and mobile 375px home and request screenshots were reviewed. This verifies two captured layouts, not every interaction, device or user's subjective preferences.
- **On-page and technical SEO — source inspection acceptable for staging.** Five separate server routes, descriptive titles and descriptions, one visible H1 per route, ordinary internal anchor links, page-specific copy, and the explicit fictional-business notice. HTML meta robots and `X-Robots-Tag` both enforce `noindex,nofollow`. No unverified canonical domain, fake LocalBusiness schema, fake ratings/address, or release sitemap. This is **correct for an unlaunched fictional demo**, not evidence of public SEO readiness.
- **Form — demo-only by design.** The server stores submissions in local SQLite and explicitly states it does not email or book. CSRF token, same-origin checks when Origin is supplied, input lengths, output escaping and a basic per-IP throttle are present. These do not establish a production security audit.
- **Accessibility — partial only.** Semantic landmarks and labels, a skip link, visible focus rings, Escape-controlled menu, reduced motion and desktop/mobile rendering are present. No full screen-reader, complete color-contrast/state review, or WCAG 2.2 AA conformance test was conducted.
- **Performance — unknown.** Asset structure is small but there is no Lighthouse result or real-user LCP/INP/CLS data. No scores are fabricated.
- **Browser acceptance:** the owner supplied an OpenCode report claiming 80/80 real-Chrome checks PASS on the **original ZIP**. The underlying new Windows screenshots and JSON were not supplied to this reviewer. We accept it as **reported evidence**, not independently re-executed or independently inspected proof. This review does not repeat those 80 checks.

## Original-source findings and targeted changes

| ID | Severity | Finding in original source | Targeted correction | Evidence |
|---|---|---|---|---|
| R01 | Low | `HEAD /index.html` returned 501. Some HTTP tooling expects HEAD to return normal resource headers. | `do_HEAD` delegates to `do_GET`; existing `send_bytes` suppresses body for HEAD. | HTTP 200, same Content-Length, zero body |
| R02 | Medium for robustness; low for localhost demo exposure | Posting more than 8 form fields caused uncaught `ValueError` in `parse_qs` and abrupt connection close rather than a client error. | Catch parser `ValueError`, send HTTP 400. | Malformed POST now HTTP 400, zero saved records |
| R03 | Low accessibility/UX | The global Escape handler always focused the navigation toggle even when the menu was closed, stealing focus from a form field. | Only close/focus when menu is expanded. | Isolated Chromium keyboard checks for both menu states |

## Actual focused regression results

`python tools/test_independent_fixes.py` — **6 PASS, 0 FAIL, 0 BLOCKED**. Evidence: `evidence/reviewer-targeted-results.json`. Scenarios are GET unaffected, HEAD fixed, malformed POST fixed, no DB insertion, closed-menu Escape focus unchanged, open-menu Escape restores button focus. Targeted browser DOM was loaded in Chromium, not a full real-URL navigation replay. The existing PASS suites were deliberately not repeated.

The reviewed copy changes only `app.py`, `site/assets/site.js`, plus **new** review report/test/evidence and a refreshed manifest. Original evidence files were preserved unchanged. Existing staging site snapshots remain `noindex` and are **not** independently deployable form endpoints.

## Release decision

**Pilot 02 reviewed candidate: conditionally acceptable as a staging demo after narrow corrections.**
**SearchReady Skill public release: HOLD pending genuine separate reviewer assessment** of the unchanged Skill candidate and both business-type pilots, especially content/design differences, installation usability and the production-gate wording. Do not imply production site readiness, search rankings, professional penetration testing, or WCAG certification. Real domain/SSL, real form delivery, privacy controls, indexing/canonicals/sitemaps and live performance measurements are **per-site launch dependencies**, not necessarily reasons to block a transparently documented reusable Skill repository indefinitely.

Next action: independent reviewer reads the exact skill candidate, original Pilot 01, and this corrected Pilot 02 with its prior test evidence, then returns only concrete issues with severity, no redundant full testing or unapproved code changes. Publication remains owner-controlled.
