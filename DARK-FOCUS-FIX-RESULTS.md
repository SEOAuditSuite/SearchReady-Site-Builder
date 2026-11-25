> **Completed historical review:** Independent Windows focus-delta acceptance passed on 25 November 2026. See `CURRENT-ACCEPTANCE.md` for the current RELEASE-ready status. No repeat of accepted tests required.

---

## Historical record (superseded status; preserved for provenance)

> **Historical v0.2 D5 evidence only.** Superseded for the changed v0.3 Clearroom/Cinderline surfaces by `V03-FOCUS-REMEDIATION.md`. Independent re-verification of the latest CSS remains pending.

# SearchReady v0.2.0 — Dark-Surface Focus Remediation (D5)

**Date:** 23 November 2026  
**Status:** Focused author remediation; **independent re-review pending, overall release HOLD.**

## Reviewed defect and exact scope

The owner provided an independent review of the previous remediation candidate: **30 PASS / 2 FAIL**. Both failures concerned keyboard-focus outlines against dark CTA backgrounds: Pilot 01 `#183b36` (previous 1.77:1) and Pilot 02 `#20352e` (previous 1.88:1). The earlier blanket claim that D5 was fixed was incomplete. A similarly dark Pilot 01 footer (`#102c26`) is now covered proactively.

No existing functional or cross-browser test suite was repeated. Prior verified D1–D4, D6, D10 checks are unchanged. No business, hosting, sitemap, indexation, or field-performance claims were made.

## Targeted correction

- Preserve teal `#2a635b` keyboard outline on light surfaces.
- Apply a light `#fff7e6` outline on Pilot 01 `.cta-band` and `.footer` focusables and Pilot 02 `.closing` focusables.
- Preserve 3px width and 4px offset; keep the focus indicator plainly visible beside the dark region.
- Extend existing regression scripts to include the two dark CTAs and the dark footer, not only the light page background; allow `test_accessibility_focus.py` to use installed Chrome when `chromium` is absent.

## Narrow evidence actually executed

`python examples/pilot-02-cinderline/tools/test_dark_focus_contrast.py` rendered actual HTML with source CSS using Playwright/Chromium, focused target links and measured **computed** outline/background colors at both 375px and 1440px. This was DOM rendering, not real HTTP navigation.

| Focus target | Measured contrast | Required | Result |
|---|---:|---:|---|
| Pilot 01 dark CTA | 11.47:1 | 3:1 | PASS |
| Pilot 01 dark footer | 13.97:1 | 3:1 | PASS |
| Pilot 02 dark closing CTA | 12.23:1 | 3:1 | PASS |

All three targets were checked at **375px and 1440px**: **6 PASS / 0 FAIL / 0 BLOCKED**. Detailed computed colors, keyboard focus state, ratios and three mobile screenshots: `examples/pilot-02-cinderline/evidence/dark-focus-results.json` and `*-focus-375.png`.

**Scope limitation:** These checks do not establish complete WCAG 2.2 AA conformance, screen-reader announcements, forced-colors/200% zoom behavior, live Chrome URL navigation on the changed build, Lighthouse lab results or field CWV.

## Evidence provenance and release status

Historical owner-reported Windows Chrome results: Pilot 01 **92/92 PASS** and original Pilot 02 **80/80 PASS** on earlier source revisions. Their exact Windows evidence files were not supplied to the authoring environment. The older `browser-results.json` entries marked `BLOCKED` represent a **different cloud environment**, and have been intentionally preserved rather than falsely replaced with PASS.

**HOLD remains** until a separate reviewer verifies this exact ZIP and the remaining bounded release-critical gates. For a public *instruction skill*, production hosting and field CWV are per-site deployment requirements, not facts the author can certify using fictional staging examples. Preserve that distinction.
