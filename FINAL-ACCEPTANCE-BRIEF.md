> **Historical checkpoint:** Current status is in `CURRENT-ACCEPTANCE.md`; current reviewer instructions are in `CURRENT-FINAL-ACCEPTANCE-BRIEF.md`. Prior results and pending labels below are preserved for provenance.

# SearchReady Site Builder v0.2.0 — One Consolidated Independent Acceptance

**Status:** Complete consolidated candidate for one independent final review. **Not publicly released.**

## Exact scope and why

The goal is to evaluate a reusable **ChatGPT website-building instruction Skill**, not certify fictional demonstration sites as live businesses. The package contains three distinct examples (a home-organizing service site, a bicycle repair service site, and an editorial journal). Do not invent indexing, Google rankings, real form delivery or certified accessibility.

The author/owner previously reported these Windows Chrome results, **on earlier source revisions**: Pilot 01 92/92 PASS; Pilot 02 80/80 PASS. The corrected Cinderline form/error state was independently checked (30 PASS / 2 dark-focus FAIL) and subsequently corrected in a new package; the later author-side 6/6 dark-focus pass is **not independent sign-off**. Pilot 03 authoring evidence reports 35+35 PASS, with real URL Chrome navigation blocked only in the original cloud environment. Recent focused changes to Pilot 03 passed author-side 11/11 and 5/5 package CI unit checks. **Do not rerun old validated layers just to increase pass counts.**

## Reviewer instructions (one pass, independent, no edits)

1. Extract this **exact** ZIP into a new isolated directory. Record ZIP SHA256, entry count and manifest consistency. Do not edit the original or alter existing customer/business folders.
2. Read `SKILL.md`, `references/`, `REMEDIATION-AND-REVIEW-STATUS.md`, `DARK-FOCUS-FIX-RESULTS.md`, and `CONSOLIDATED-ACCEPTANCE-STATUS.md`. Inspect examples and their evidence provenance.
3. Run **only the missing Pilot 03 live HTTP-browser gate:** `python examples/pilot-03-margin-atlas/tools/test_live_url_only.py` using installed Chrome/Playwright. Save new results to the sibling `<extracted-folder>-review-evidence/pilot-03-margin-atlas/` directory (outside the signed release tree). Earlier in-package blocked evidence is preserved unchanged.
4. Independently check the latest code's **dark CTA/footer focus indicators** in Pilot 01 and Pilot 02, at mobile and desktop sizes. The scoped author script is `python examples/pilot-02-cinderline/tools/test_dark_focus_contrast.py`. Report any genuinely missing focus state; previous independent 1.77:1 / 1.88:1 failures must be measured against the **current** code rather than historical screenshots.
5. Review Pilot 03 editorial site for content authenticity, honest 2-minute reading-time labels, heading structure, keyboard usability, 320px and 200% zoom reading, forced-colours behavior if possible, non-JS article discoverability, journal search feedback and raw-HTML SEO readiness. Distinguish tested, blocked and not run. Do not demand a real canonical/site map for an intentionally noindex fictional demo.
6. Review the package's public GitHub distribution hygiene: no secrets/data, usable Plus Project guide, honest conditional native Skills guide, MIT/other asset rights, versioning/CI, source reproducibility and limitations. Record design/UX strengths and genuine defects with exact file:line references.
7. Optional only if already available without installing anything: Lighthouse lab run against a temporary local URL, clearly labeled **LAB** and not field CWV. If unavailable, `NOT RUN` is accurate.

## Explicit non-goals

- No fourth website and no rebuild/rewrite of prior pilots.
- No repetition of earlier preflight/unit/HTTP/render suites unless a relevant code change invalidates that specific evidence.
- No real user data, public hosting, DNS, Search Console submissions, spending, or new npm/browser installation without authorization.
- No claimed WCAG 2.2 AA certification, screen-reader user study or site-specific production SEO acceptance from static demonstration checks.

## Required output

Provide a concise **independent** acceptance report: exact reviewed archive SHA, verified evidence, new PASS/FAIL/BLOCKED/NOT RUN for only remaining checks, precise severity-ranked defects, release-critical blockers (separate *Skill publish* from *example production launch*), and one `RELEASE` or `HOLD` recommendation for public GitHub distribution. Preserve all results and screenshots in a new reviewer output directory. Never silently replace historical `BLOCKED` JSON with fabricated success.

## Post-review targeted closure (23 November 2026)

The independent reviewer already completed Pilot 03 live Chrome navigation and dark-focus verification and found two bounded source/release defects (Windows CRLF generation and evidence writing into the manifest-controlled directory). Those defects have been corrected. **Do not rerun the full prior acceptance suite.** On Windows, extract the updated candidate in a fresh location; run `python tools/test_editorial_contract.py` and `python tools/check_manifest.py`, and confirm that any future browser evidence scripts save results outside the release tree. Report failures only if they occur. Original reviewer evidence remains external; see `INDEPENDENT-REVIEW-DELTA.md`.
