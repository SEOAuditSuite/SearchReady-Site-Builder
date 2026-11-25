# Evidence-based verification and release gates

Maintain a page/feature matrix with revisions and test evidence. Acceptance layers:

1. **Static:** route list, titles/meta/H1/links/media/language/canonical/robots/schema, content truthfulness; static tests are not a full browser acceptance.
2. **Functional HTTP:** real server on loopback or staging, status, redirects, raw source, actual assets, robots/sitemap (if applicable), canonical consistency, form integration and errors.
3. **Browser:** use accessible Chrome/Chromium/Firefox/mobile emulation to click menu, anchors and CTA; check keyboard, responsive overflow, runtime console/page errors, visual screens, and form flows. Distinguish `set_content()` from URL navigation.
4. **Quality:** accessibility automated checks + meaningful manual review, measured lab performance and field metrics separately, security review proportional to scope.
5. **Launch:** real domain, TLS, indexability/robots/sitemap/metadata, owner-approved true content, real contact channels, policies and consent where applicable, redirects/rollback, Search Console when authorized. Never publish without permission.

Statuses: PASS (tested with evidence), FAIL (observed defect), BLOCKED (needed environment/permission absent), NOT RUN, STALE (prior pass invalidated by a change), INFO. Report a concise release matrix. Re-run only affected checks unless shared infrastructure, schema, routes, auth, or launch policy changed. Independent review should be carried out with the original revision/hash and actual artifacts; do not count two reports by one executing agent as independent tests.

**Release categories:** DRAFT (design not built), STAGING READY (functionality demonstrated on staging with known launch blockers), RELEASE CANDIDATE (all currently available gates passed; any blockers explicit), PRODUCTION READY (all applicable hard gates evidenced and approved for the specific site), LIVE (actual public deployment verified). Do not interpret production ready as guaranteed rankings or legal/WCAG/security certification.

Use `tools/site_preflight.py` as an optional offline source-level triage, never as sole audit. It intentionally cannot prove server headers, mobile browser behavior, real form deliverability, indexing, CWV or accessibility conformance.
