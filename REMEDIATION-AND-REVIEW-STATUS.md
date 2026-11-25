# SearchReady v0.2.0 — Independent Review Response and Release Gates

**Date:** 23 November 2026  
**State:** Corrected candidate for verification. **Public release: HOLD.**

## Source and review identity

- Independent review supplied by the owner: `Independent Review — SearchReady Site Builder v0.2.0 Candidate + Pilot 02 (Cinderline)` (23 November 2026).
- Reviewer read the original 46-file Skill ZIP and Pilot 02 **VERIFIED** ZIP. The reviewer explicitly could not find the later 29-file **Reviewed** ZIP in Downloads. Thus D6, D10 and the parser-hardening issue were observed in an earlier source state, not the already-remediated Reviewed source.
- This combined candidate contains the same Skill foundation with focused changes and `examples/pilot-02-cinderline` sourced from the Reviewed ZIP; the original historical ZIP files were not overwritten.
- The authoring assistant prepared the present remediation. **It is not an independent second sign-off.**

## Finding disposition

| Finding | Severity in reviewer report | Current disposition | Narrow evidence |
|---|---|---|---|
| D1 — 12px hero footnote only 3.38:1 | Medium | **FIXED in Pilot 02**: `#475447` on `#eee9db` = 6.59:1 | `examples/pilot-02-cinderline/evidence/release-fixes-results.json` |
| D2 — control boundaries below 3:1 | Medium | **FIXED**: border `#5b6156` contrasts >=5.07:1 against tested adjacent colors | Same focused evidence |
| D3 — generic server form rejection and missing field announcements | Medium | **FIXED within code**: field-specific messages, `aria-invalid`, `aria-describedby`, linked summary, keyboard focus on summary; **screen-reader user study NOT RUN** | Focused HTTP tests and render-only browser focus results |
| D4 — success POST refresh resubmits | Medium | **FIXED**: 303 Post/Redirect/Get; receipt token associated with signed session; refresh GET did not duplicate row | Isolated SQLite/HTTP tests |
| D5 — focus indicator insufficient on dark CTA surfaces | Medium | **CORRECTED FOR RE-REVIEW**: `#2a635b` on light backgrounds; `#fff7e6` for Pilot 01 dark CTA/footer and Pilot 02 dark closing CTA. Original independent finding: 1.77:1 / 1.88:1. | `DARK-FOCUS-FIX-RESULTS.md`, focused browser and contrast evidence; external re-review still pending |
| D6 — HEAD 501 | Low | **ALREADY FIXED** in source Reviewed ZIP; carried forward | Focused regression on HEAD status |
| D10 — Escape steals focus | Low | **ALREADY FIXED** in source Reviewed ZIP; carried forward | Existing Reviewed 6/6 audit + current guard retained |
| D7, D8, D9, D11–D15 | Low | **DOCUMENTED** as staging limitations or deferred enhancements; do not silently promote to PASS | Previous reviewer report; no live production claim |

## Evidence actually executed in the remediation environment

- `tools/test_release_fixes.py`: **12/12 PASS on prior candidate** — targeted color contrasts, field-specific 422, session-bound confirmation, browser-refresh duplicate prevention, HEAD and Escape guard preservation.
- `tools/test_accessibility_focus.py`: **7/7 PASS on prior candidate** — render-only Chromium focus and error-field styling at 320/375px, Pilot 01 focus outline. It does not count as live-URL browser acceptance or screen-reader certification.
- Affected original Pilot 02 `test_16_valid_demo_submission`: **1/1 PASS** after 303 redirect.
- `examples/pilot-02-cinderline/evidence/reviewer-targeted-results.json` retains the prior 6/6 targeted fix evidence (R01–R03) from the previous author-run pass.

**Not independently verified here:** Windows Chrome real URL-navigation of this newly corrected build, keyboard/screen-reader assistive-technology behavior, Lighthouse lab, field CWV, 200% zoom/forced colors, live hosting or production domain.

## Historical owner-provided results (not copied as newly executed tests)

- Pilot 01: owner shared OpenCode result **92/92 PASS** on original v0.2.0 candidate, Windows local Chrome, 22–23 November 2026.
- Pilot 02: owner shared OpenCode result **80/80 PASS** on the original 26-file `VERIFIED.zip`, Windows local Chrome, 23 November 2026.
- Original packages include older `evidence/browser-results.json` entries marked BLOCKED due to the cloud environment. Those are **historical** and were not rewritten to impersonate a Windows PASS. The complete latest Windows JSON/screenshots were not uploaded in this conversation.
- Source changes since those Windows checks invalidate the **changed form/error/focus states only**. Run focused new Windows checks on this corrected candidate; do not repeat every old page and breakpoint without reason.

## Remaining approval/verification boundary

A transparent public **Skill** could be published after the remaining critical reviewer issues are addressed with evidence and the maintainer accepts an honest scope statement. A production-ready **website** always needs its own verified business facts, domain, hosting, TLS, live form route, privacy treatment, SEO indexability, and performance checks. This candidate's fictional demos remain intentionally `noindex` and local-only; do not fake those launch dependencies.

Before representing the Skill as independently release-ready, obtain a separate reviewer assessment of **this exact updated ZIP**, a focused Windows Chrome check of modified form and focus cases, a bounded accessibility audit (contrast complete, keyboard, 200% zoom, screen reader where available), Lighthouse lab evidence labeled as lab-only, and a materially different site-type sample or appropriately narrow the documented reusability claim. Do not claim 100% WCAG conformance, field CWV results or production security certification from these fixtures.

## 23 November independent re-review: D5 dark-surface regression

The owner supplied a separate reviewer report for the preceding remediation candidate: **30 PASS / 2 FAIL**. Both failures were keyboard focus outlines against dark CTA backgrounds (Pilot 01 `#183b36`, Pilot 02 `#20352e`). The earlier D5 FIXED statement was therefore incomplete. This candidate adds scoped light outlines for both dark CTAs and the Pilot 01 dark footer, while retaining the original teal outline on light surfaces.

The focused contrast/browser evidence is in `DARK-FOCUS-FIX-RESULTS.md` and `examples/pilot-02-cinderline/evidence/dark-focus-results.json`. The independent reviewer has **not yet assessed this updated archive**. Other limitations, including WCAG audit, actual production SEO/hosting and complete updated Windows Chrome PASS evidence, remain unchanged. Historical BLOCKED browser records are preserved as historical environment results, not rewritten as successful executions.
