# Native platform acceptance — remediation delta

Date: 24 November 2026

## Independent baseline (owner-provided report)
The original Platform Verification Lab archive is unchanged. The owner supplied an independent acceptance summary, not the raw JSON/screenshot evidence. The reported 34/34 manifest verification and results below are attributed to that review, not a new author-side runtime test.

- WordPress 7.1.5 / PHP 8.4.28 / SQLite / Chrome 158: 262/264 PASS (HTTP 49/49; public sitemap and restore 14/14; browser 184/186; admin 15/15). Native runtime accepted with two minor defects. Actual activation, editing, routing, metadata, keyboard, responsive design and sitemap tested within the reported scope.
- Shopify: official Theme Check exit 1, missing required theme metadata; missing locales directory also reported. No authorized store, so actual Liquid storefront, variants, cart, theme editor, rendered SEO and responsive storefront remain BLOCKED.

## Corrections in this archive

| ID | Change | Author-side verification | Independent status |
|---|---|---|---|
| WP-1 | Responsive comment textarea, form control max width, visible textarea focus | Browser fixture at 320, 375, 768 and 1280 px | Native retest pending |
| WP-2 | Wrapped pagination, 44px minimum width and height, 8px gap at default root font size | Browser fixture checks target dimensions at four widths | Native retest pending |
| SH-1 | Add `theme_support_url` instead of inventing a support email | JSON metadata contract PASS | Official Theme Check pending |
| SH-2 | Add `theme_documentation_url` | JSON metadata contract PASS | Official Theme Check pending |
| SH-3 | Add `locales/en.default.json` and use two translated 404 strings | Locale key resolution PASS | Official Theme Check pending |

Both prototype theme versions are 0.1.1. The `example.com` URLs are reserved placeholders for a fictional staging demonstration. They must be replaced by real approved merchant/theme support and documentation URLs before production delivery. Shopify's official settings schema permits either a support URL or support email, not both: https://shopify.dev/docs/storefronts/themes/architecture/config/settings-schema-json. No checks were suppressed. No full localization claim is made.

## Independent targeted re-verification
1. Extract this ZIP into a fresh directory. Check all manifest sizes and hashes. Preserve the original archive and prior independent evidence.
2. Reuse the existing disposable local WordPress environment. Install the corrected theme there only; confirm version 0.1.1 and clear any stale browser cache. On a real single post with comments enabled, verify textarea stays within the content and no horizontal viewport overflow at 320px; confirm keyboard focus. On a real paginated archive, measure page number link boxes and spacing at 320px and a desktop width. Check navigation works. If the comments pagination is available, check the same CSS there. Record measurements, screenshots and verdicts. Preserve the site's original staging indexing setting.
3. Run official Shopify Theme Check using the installed CLI: `shopify theme check --path shopify/paper-spark` from the package root (or equivalent existing CLI invocation). Capture version, exit code, errors, warnings and locale status. Do not suppress checks, use a live store, or invent a support email. Mark preview and native commerce BLOCKED if access remains unavailable.
4. Recheck the manifest. Write new evidence outside the source directory. Do not rerun unaffected suites, modify the source, purchase anything or publish.

## Lessons for SearchReady integration
Test all native CMS-generated forms (including comments) at 320 CSS pixels, not merely navigation or hand-authored hero layouts. Check pagination and every class of interactive target, not only buttons. On Shopify, check native metadata completeness and default locale presence with the official Theme Check before claiming static acceptance. Treat actual merchant data, admin editing and preview acceptance as separate gates. WordPress core theme success does not certify Elementor or WooCommerce. No production site certification or ranking guarantee.
