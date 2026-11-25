# Implementation and platform choices

Select the simplest stack that fits **real** needs: static HTML/CSS for brochure pages, an appropriate SSR/SSG framework for larger content sites, a real CMS when the owner must edit content, and proper backend/ecommerce systems for transactional behavior. Avoid unnecessary dependencies and proprietary SaaS; respect owner budget and existing codebase. Prefer accessible, maintainable components and small testable files.

Define routes, navigation, metadata API, form integration, image optimization, error pages, redirects and deployment/rollback before scaling. Keep critical crawlable content in initial HTML whenever feasible. Ensure link tags and meta output exist in actual served response; don't assume JS snapshots equal server HTML. Check behavior in production build mode; development server is not proof of deploy readiness.

Use readable configs, environment variables, strict .gitignore for secrets, reproducible install commands and version pins where appropriate. Do not create unsupported scripts or rely on nonexistent connectors. If an existing app has a design system, migrate incrementally rather than rewrite. For integrations, test actual endpoints when authorized; otherwise label BLOCKED and give handover steps.

## Platform-aware design and SEO routing

Honor an explicitly requested platform unless an actual constraint makes it unsuitable. When none is requested, recommend one based on editing needs, catalog/payment complexity, existing site equity, budget, hosting, operational skill and tool access. Explain one tradeoff and ask only for essential approval; do not silently change an existing platform. Record route, actual platform/version, extension/theme choices, SEO-output owner, implementation access and required acceptance evidence.

| Context | Default route | Acceptance boundary |
| --- | --- | --- |
| WordPress business/blog | Native block theme or maintain existing theme/builder | Installable theme/child-theme or approved editor changes; actual WordPress rendering and editing tests |
| Existing Elementor site | Preserve Elementor/theme contracts; use compatible widgets/templates | Test real editor and frontend; no unapproved Pro widgets or subscriptions |
| WooCommerce | WordPress + compatible store/theme integration | Product/catalog/variation/cart/checkout test mode, SEO output and upgrade compatibility |
| Shopify | Existing or new Online Store theme using Liquid, sections and JSON templates | Theme validation and actual authorized store preview; test commerce features with test data |
| Custom static or React/Next.js | Static/SSR/SSG or compatible existing stack | Build, actual served metadata/content, routes, hydration/navigation and deployment checks |

### WordPress and Elementor
Inspect existing core, theme, child theme, active builder and SEO plugin before editing. Use native theme APIs, version-compatible theme.json/blocks or existing builder conventions; preserve wp_head/wp_footer and enqueue assets. Never edit core/vendor files or overwrite a parent theme to make a custom change. Preserve posts, permalinks, media and editor usability. Define one owner for title/meta, canonical, schema, robots and sitemap output (core, plugin or deliberate theme integration); audit actual HTML for conflicting tags and duplicate schema. Do not require an SEO plugin if existing capabilities cover requirements; choose only necessary compatible plugins. Test staging visibility, archive/taxonomy policy, pagination, search results, redirects, mobile navigation, accessibility, image sizes, caching and forms. Verify representative page/post/archive routes and editor functionality in actual WordPress before claiming platform acceptance.

### WooCommerce
Use existing WooCommerce data and template/hooks; avoid recreating order, cart, inventory, checkout or payment systems in a theme. Map categories, products, variants and filters to coherent crawlable routes and canonical policies. Keep price, availability, currency, SKU and applicable product schema truthful and consistent with actual product data; avoid duplicate Product entities from plugins/theme. Distinguish filter combinations from genuine indexable category pages. Test category browsing, product variants, stock states, cart, checkout, tax/shipping and order flow only in authorized test mode. Never use a real payment or customer record for a demo. Confirm plugin/theme version compatibility and backups. Mark unavailable payment/checkout tests BLOCKED.

### Shopify
Use Liquid theme conventions, sections/blocks, JSON templates and supported platform objects; preserve merchant editing and existing app integrations. Do not hand-replace platform-generated canonical, sitemap or robots output by default. Audit final rendered source for conflicting theme/app metadata and structured data, URL consistency and collection/product discovery. Use native SEO fields, approved redirects and truthful product/variant price/availability/currency; review localized markets/hreflang when used. Keep product links crawlable; use native cart/checkout and account capabilities. Respect theme license and plan limitations; do not promise checkout customization unavailable on the plan. Test in a duplicate/unpublished theme or authorized development store, including product variants, collection filters, cart, mobile interactions and checkout in test mode if available. Theme syntax or static mockups are not a Shopify preview PASS. No theme publishing, app install, subscription or live transaction without owner approval.

### Custom frameworks
For JavaScript-heavy sites, use compatible static/server rendering for key content where feasible and verify source/rendered parity, route-level metadata, error statuses, redirects and sitemap output in a production-like build. Use actual browser/network evidence rather than assume search crawlers execute every component. Keep CMS and platform integrations testable and use supported APIs.

### Access fallback
If the actual CMS/store is unavailable, deliver an editable design and implementation package or precise configuration guide and identify the untested platform gates. Do not describe an HTML demo as an installed WordPress theme or Shopify store. Reuse the same visual, SEO and launch gates across platforms; specialize the implementation, not the quality bar.
