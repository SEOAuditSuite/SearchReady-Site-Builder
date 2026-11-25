# SearchReady v0.3.1 — Platform verification lab

**Status: platform remediation candidate. Independent baseline WordPress runtime: 262/264 PASS; Shopify official Theme Check: FAIL (two schema errors and missing locale directory). Targeted corrections are implemented; native re-verification pending.** This is an add-on evidence package for the unchanged SEO & Platform Integration Candidate, not a new Skill version or release approval.

## WordPress: Fieldnote Learning
A classic theme prototype for an educational resource website. It uses WordPress-managed posts, pages, menus, search, archive/pagination and editing rather than hardcoded fictional business data. Core/plugin metadata ownership is preserved; an approved SEO configuration is necessary for descriptions and applicable schema. Install the `fieldnote-learning` folder only into a disposable staging WordPress instance. Set a site title, description, menu, sample posts/pages and images, disable indexing in staging, and verify actual output. No Elementor or WooCommerce implementation is included.

## Shopify: Paper Spark
A small-catalog native Liquid theme prototype with editable homepage text and featured collection, native product, collection, cart, page and 404 templates. Uses Shopify-provided title, description and canonical fields and native cart/checkout routes. The product picker is for a bounded small catalog; high-variant support, variant media, localization, theme-editor refresh, accessibility, structured data, and all other full-store requirements are not accepted by this lab. It is not a complete Theme Store submission. No checkout customization, fake payment implementation or invented reviews. Theme files may be zipped with `layout/`, `sections/`, `templates/`, `assets/`, `snippets/`, `config/`, and `locales/` at the theme ZIP root for authorized unpublished preview after Theme Check. Do not activate/publish in a live store.

## Reproduce the checks
From the root of this lab, run `python tools/test_platform_source.py` (Python 3, PHP CLI and Node.js). For the variant JavaScript fixture, run `python tools/test_variant_fixture.py` with Python Playwright and a locally available Chromium. Results are printed; redirect output outside the lab directory to preserve the manifest. The latter runs the real script against synthetic HTML, not a Shopify rendering. A missing runtime is not a pass.

## Focused re-verification after remediation
Read `NATIVE-ACCEPTANCE-DELTA.md`. Reuse the disposable WordPress installation and already installed Shopify CLI; do not repeat unchanged suites. Run `python tools/test_platform_delta.py` for the CSS browser fixture and schema/locale contract. The fixture is not a substitute for native WordPress rendering. Shopify support/documentation URLs under `example.com` are reserved staging placeholders, not actual support services; replace with real approved URLs before merchant delivery.

## Native acceptance (when available)
- WordPress: verify activation on the actual version, frontend and admin editing, page/post/archive/search/404, menu, canonical/title/description uniqueness, robots/sitemap, representative mobile and keyboard states. Check plugin SEO ownership. Do not infer Elementor/WooCommerce compatibility from core theme activation.
- Shopify: run official Theme Check, open an authorized unpublished preview with fictional products/variants; verify theme editor, rendered metadata/structured data, collection/product links, stock and prices, cart updates and checkout only in authorized test mode. No paid subscription or live order.
- Elementor and WooCommerce: separate compatibility gates when a real installed platform and approved extensions are available. No execution claimed.
- Existing visual redesign: independent real URL-navigation acceptance remains pending from v0.3. No earlier PASS suites need repeating.

## Design and SEO decisions
Fieldnote Learning: educational/editorial brand, clear resource hierarchy, editor-owned content, bright warm yellow and violet. Paper Spark: cheerful stationery retail, lively accent colors, browsable product grid, real catalog data as source of truth. These are source-level design implementations, not independently approved visual previews. No search volumes, competitor claims, rankings or customer reviews invented. Keyword mapping and native-platform SEO audit must use the actual business/catalog/domain, approved research and available tools. BeyondSEO and SEO Audit Suite remain optional, not bundled or invoked automatically.
