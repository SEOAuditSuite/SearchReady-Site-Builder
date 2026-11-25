# Platform verification record — 24 November 2026

**Historical baseline evidence.** The subsequent independent native review and current corrections are recorded in `NATIVE-ACCEPTANCE-DELTA.md`. Historical statuses below are preserved, not the current acceptance verdict.

Baseline: `SearchReady-v0.3.1-SEO-Platform-Integration-Candidate.zip`, SHA256 `b7e411d1cf76628e34e6392e6fb8374f27bd0683ea84aa113a2e388cab33cb38`. ZIP CRC and 142 declared file hashes verified. The original archive was not modified. This lab is separate from the baseline and no existing demo was rebuilt.

| Gate | Status | Evidence |
|---|---|---|
| Native theme source contract | 9/9 PASS | `evidence/source-checks.log`: PHP syntax of all 9 PHP files; native hooks, data retrieval, routes; Shopify layout, JSON/section cross-references, commerce bindings, assets, JS syntax |
| Variant selector browser fixture | 5/5 PASS | `evidence/variant-fixture.json`: actual JavaScript against synthetic DOM; price change, disabled unavailable selection, recovery, no page errors |
| WordPress runtime / editor | BLOCKED | PHP CLI available; WordPress core, usable database driver and server not available; network lookup of WordPress archive failed |
| Shopify Liquid parser / official Theme Check / store preview | BLOCKED | No Shopify CLI or installed Liquid parser; no authorized development store |
| Elementor / WooCommerce | NOT RUN | No installed CMS/extensions |
| Full visual QA, SEO launch audit, checkout/payment, field CWV | NOT RUN | Require real preview and business/site facts; not covered by source/fixture checks |

The first variant fixture attempt exposed an ambiguous test locator (`data-price` on both the displayed amount and options). The display was assigned a distinct `data-current-price` attribute in both the prototype and fixture; the corrected focused test passed. This does not establish native Liquid rendering or commerce behavior. No external API, account change, paid action, production launch or public repository write took place.

## Official implementation references
- https://developer.wordpress.org/themes/releasing-your-theme/required-theme-files/
- https://developer.wordpress.org/themes/advanced-topics/plugin-api-hooks/
- https://developer.wordpress.org/reference/functions/add_theme_support/
- https://shopify.dev/docs/storefronts/themes/architecture/layouts
- https://shopify.dev/docs/storefronts/themes/architecture/templates/json-templates
- https://shopify.dev/docs/storefronts/themes/seo/metadata
- https://shopify.dev/docs/storefronts/themes/architecture/templates/product/overview
- https://shopify.dev/docs/storefronts/themes/tools/theme-check/checks

**Decision:** retain the tested v0.3.1 Skill candidate. Source examples are ready for authorized runtime trials, not final platform acceptance or production deployment. Do not claim equal validation across platforms yet.
