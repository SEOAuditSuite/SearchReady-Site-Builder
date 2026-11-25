# SearchReady v0.3.1 — Consolidated Reference Guide

For ChatGPT Project uploads. Individual reference files are retained for native skill hosts.

---

## Reference: brand-and-visual-design.md

# Professional visual identity and art direction

Create websites that feel designed for *this* brand. Derive layout, type, color, spacing, shape, photography/illustration style, microinteraction and content hierarchy from the audience and business character. Prefer consistent restraint over predictable decorative gradients, purple glows, giant vague hero claims and card spam.

Set explicit design tokens: color/semantic roles, type scale with responsive clamp where useful, font fallback, spacing rhythm, container/max-width, borders, shadows, radii, motion settings, input/button states and focus ring. Choose legible typography, strong contrast, useful whitespace, clear navigation, readable line length and obvious CTAs. Test 320/375px mobile, tablet and desktop; treat 200% zoom and long localized text as risks. If images are generated, original, licensed or user-supplied, mark provenance/rights; no fabricated screenshots showing nonexistent products.

Build accessible patterns: real buttons for actions, anchors for navigation, meaningful error/success states, explicit loading and disabled states when required. Make mobile menus keyboard operable, closable, with accurate expanded state and no focus traps. Respect prefers-reduced-motion. Test light/dark only if supported. No deceptive cookie banners, fake urgency, intrusive overlays or dark patterns.

Quality bar is qualitative plus evidenced: coherent composition, polished above-the-fold hierarchy, informative sections instead of empty decoration, functional states, mobile readability, and visual consistency across all pages. Images and CSS style alone do not certify conversion performance.


## Category-aware premium design gate (visual refinement v0.3)

A technically correct, responsive page is **not** automatically a compelling brand design. Before drawing a hero or choosing components, identify the site's purpose, audience, emotional goal, expected trust cues, visual references, image/illustration rights, and what must feel *different* from a generic template. Record a compact **art-direction decision**:

1. **Mood:** three specific adjectives (for example *airy / optimistic / organized* rather than "modern"). Choose colors for their meaning and accessible contrast, not from a fixed industry palette.
2. **Typography:** choose deliberate heading/body contrasts, letter spacing and hierarchy. A journal, a children's activity brand and a premium industrial workshop must not share one unexamined serif-and-three-card formula.
3. **Composition:** select an appropriate *layout silhouette*: hero split versus editorial spread versus product-first media versus image-led portfolio. Vary navigation, section cadence, card shapes and relative density based on the task.
4. **Visual language:** choose authentic photography, original illustrations, diagrams or product visuals that directly support the business. Never add unrelated cartoon characters, playful badges or fake trust marks merely to decorate.
5. **Brand-specific components:** specify CTA treatment, imagery, backgrounds, surfaces, radii, iconography and motion. Add a small playful touch where appropriate, but preserve professional trust and accessibility.
6. **Real proof of distinction:** compare the first screen and a complete-page capture against other examples or reference sites. If two unrelated categories feel like theme swaps, revise the art direction before accepting the design.

### Two bounded directions demonstrated in the visual refinement

- **Clearroom (home organization):** light and airy lifestyle direction; white/sky/mint/peach/yellow surfaces, rounded yet spacious components, cheerful original room illustration and generous whitespace. The design should feel welcoming and achievable, not like a dark consulting firm.
- **Cinderline (cycling service):** energetic premium workshop direction; electric blue, dark navy, high-contrast coral and sunshine-yellow, bold athletic headlines, dynamic graphic bicycle art, asymmetric hero field and punchy service cards. Limited playful decals are appropriate; **no false children's services, certifications or appointments**.
- **Margin Atlas (editorial):** retain the quieter reading-first typography, article architecture and subdued palette. Different products should exhibit different visual personalities.

**Quality checks:** judge first-screen hierarchy, content legibility, genuine audience fit, mobile execution, nav/form function, SEO metadata, light/dark focus visibility, reduced motion and whether visuals are original or licensed. Static previews show art direction only; require live HTTP and browser interaction evidence before calling functionality PASS. Owner aesthetic acceptance is qualitative and must not be replaced by automated test counts.

---

## Reference: content-and-information-architecture.md

# Useful content and page architecture

Create a page map from the audience's distinct needs, not keyword stuffing. Define one primary user goal and search intent per page with supporting subtopics and a real conversion path. Homepage explains value plainly; service/product pages answer specific questions; about establishes genuine identity and trust; contact clearly states how contact actually works. Include pricing only if verified; truthful availability and service regions.

Each indexable page should have a distinct descriptive title and coherent H1, credible meta description, clear navigation and relevant internal links. Do not enforce arbitrary character-count "Google limits" or a universal one-H1 rule; avoid duplicated, truncated or generic snippets through human review. Add contextual text, scannable meaningful sections and descriptive link anchors. Do not create dozens of thin location/service variants merely for search. Avoid copying protected or proprietary content from a reference site.

Make all critical text visible and accessible without relying on JS-only postload fetches when reasonable. Image alt describes informative content or is empty for decorative imagery; use captions where valuable. Avoid hidden SEO copy. Add FAQs only when they genuinely answer visitor questions; do not claim FAQ rich results are guaranteed.

For redesigns, map old URL -> new URL and 301/308 where appropriate, update internal links/sitemaps, verify redirects and distinguish canonical from redirect. Search demand/keyword research requires current tools and evidence; never invent search volume or keyword rank.

## Editorial / documentation sites (additional release candidate learning)

For an actual publication, distinguish searchable article HTML from a client-side UI filter. Keep an index/archive with direct crawlable `<a href>` links to meaningful article URLs, verify category names and related reading paths, use descriptive heading levels without unjustified skips, and avoid overpromising reading time. Byline, editorial ownership, experience, external-source citations, publishing/update dates, and schema must be grounded in real supplied facts. Do not automatically infer an author or original research from stylistic copy. Structured-data claims must reflect visible content. During redesign, preserve article permalinks and 301/308 redirects when mapping changes. Require human approval of factual and sensitive editorial claims.

---

## Reference: goal-and-scope.md

# Goal, audience and honest scope

Start from the user's real goal, not a generic landing-page template. Identify: kind of business, core audience geography/language, primary service/product, desired visitor action, preferred platform/budget, actual business credentials/location/contact, brand materials, page inventory, accessibility needs and domain/hosting status. Ask only high-impact unknowns; make reversible decisions independently. For commercial sites, distinguish transactional/lead-gen flows from brochure pages. A CTA must go somewhere real or be explicitly marked as a nonfunctional demo.

Offer a compact, reasoned information architecture and pre-build effort estimate. Make an inventory of pages, components, states and interactions. Avoid blank "coming soon" pages, fabricated team biographies, copied competitor copy or trademark appropriation. Validate information source and imagery license. Label content as VERIFIED OWNER-PROVIDED, DRAFT FOR OWNER REVIEW, or PLACEHOLDER NOT FOR PUBLICATION. A missing production domain cannot be concealed by example.com canonicals.

Provide a concrete acceptance definition: mobile navigation, visible primary action, complete pages, crawlable critical content, truthful SEO metadata, responsive/no-overflow, keyboard and screen reader essentials, measured performance evidence, content authenticity, working forms if requested, and suitable launch gate.

---

## Reference: official-standards.md

# Official standards and references (checked 2026-11-23)

Use official sources for changing rules. Do not claim every best-practice suggestion is a mandatory ranking factor.

- Google Search Essentials: https://developers.google.com/search/docs/essentials
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- People-first content guidance: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Web Vitals: https://web.dev/articles/vitals
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Focus Visible: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible
- W3C Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast

These sources inform requirements. Actual indexation, field performance and conformance must be evaluated with real-world evidence and appropriate audit methods. Dynamic guidance should be rechecked during a production launch.

## Platform and AI-search guidance (checked 2026-11-24)
- Google ecommerce SEO: https://developers.google.com/search/docs/specialty/ecommerce
- Google AI features: https://developers.google.com/search/docs/appearance/ai-features
- Shopify SEO overview: https://help.shopify.com/en/manual/promoting-marketing/seo/seo-overview
- Shopify robots configuration: https://help.shopify.com/en/manual/promoting-marketing/seo/editing-robots-txt
- Shopify international SEO: https://help.shopify.com/en/manual/markets/seo
- WordPress global styles: https://developer.wordpress.org/themes/global-settings-and-styles/
- WooCommerce structured data integration: https://woocommerce.com/document/google-product-feed-expanded-structured-data/
Recheck applicable platform/version documentation before implementation. These sources do not establish actual platform execution or guarantee rankings.

---

## Reference: performance-and-cwv.md

# Performance and Core Web Vitals

Design for fast experience, not arbitrary Lighthouse scores. Prefer restrained JS and CSS, responsive images (`srcset`/`sizes`), proper width/height to avoid layout shifts, modern supported formats, local fonts/system fallbacks, long-lived safe caching, lazyload below-the-fold noncritical media, and avoid lazyloading the likely LCP image. Remove unused scripts, heavy icon packs, long main-thread tasks and render-blocking dependencies when appropriate. Keep user-perceived interactivity usable on midrange mobile conditions.

Use actual lab tools (Lighthouse/PageSpeed Insights/DevTools) with identified URL, time, network, device, cache, run count and limitations. Evaluate LCP, INP and CLS using proper **field** measurements where available; INP cannot be certified by one synthetic click. Target 'good' CWV thresholds as guidance: LCP <= 2.5s, INP <= 200ms and CLS <= 0.1 at 75th percentile of real visits; do not label unmeasured field CWV PASS. Compare before/after only for equivalent conditions. Different templates/routes can behave differently, so sample representative pages.

Track resource budgets and evidence by route. Prioritize actual bottlenecks over endless optimization. Avoid false 100/100 score promises, third-party blocking manipulations, hiding content from audits or lowering functionality solely for a score.

---

## Reference: platform-and-implementation.md

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

---

## Reference: recovery-and-delivery.md

# Durable continuation and handover

For significant projects create or maintain concise `SITE-BRIEF.md`, `PAGE-SEO-MATRIX.md`, `STATUS.md`, `DECISIONS.md`, `QA-LEDGER.md`, and `HANDOVER.md` in the actual editable source repository. Do not overwrite equivalent files with different names. Check git branch, HEAD, dirty state, actual source and prior proof before resuming in a new chat. Preserve previous release/checkpoint, avoid repeated tests without changed risk. A static ChatGPT Project attachment is not automatically rewritten.

Handover: business/site identity, owner-approved goals, supported platforms, repository/commit or archive hash, design tokens, page inventory, exact start/build/deploy commands, asset provenance, content placeholder list, SEO status per route, test evidence, live-domain checks, blocked dependencies, rollback plan, remaining owner approvals and one next safe action. Use the user's language to explain next steps, but maintain professional English in source/deliverables unless requested otherwise.

When the execution environment cannot build/test/host, explain the precise gap and provide the smallest runnable next action; never infer PASS from an instruction or promise asynchronous execution. Public launch, external analytics setup, buying services and account modifications need explicit approval.

---

## Reference: security-privacy-and-forms.md

# Security, privacy and trustworthy conversions

Match controls to actual deployment. For simple static pages: avoid injecting untrusted HTML, remote unknown JS, unsafe target blank links, exposed source maps/secrets and accidental third-party asset calls. For real backends/lead forms: apply HTTPS, server-side validation, output encoding, anti-spam/rate limiting as appropriate, CSRF considerations, safe storage/transmission, notification monitoring and explicit recipient authorization. Never expose credentials in frontend bundles or static files.

Handle contact flows truthfully. A mock success, downloaded local brief or `mailto:` link is NOT an operational form-submission backend. Report exactly what is and is not connected. For user data and cookies, document collection, retention, consent, privacy policy and applicable laws instead of inventing compliance claims. No unapproved analytics, pixels, emails, SMS or CRM integrations.

Use licensed assets and respect copyrights. No fake social proof, unverified seals, cloned proprietary pages or legal templates pretending to be professional legal advice. Avoid public deployment or billing actions without authorization. Security controls need risk-based independent review for sensitive/authenticated/transactional systems; passing a static build is not production security certification.

## Form confirmation and duplicate prevention

For accepted HTML form POSTs, use **Post/Redirect/Get (HTTP 303)** when appropriate so ordinary refresh/back navigation does not resubmit a record. Bind confirmation to a real accepted event; a public `?saved=1` URL must not falsely claim a submission was stored. Where real payments or bookings exist, use server-side idempotency safeguards in addition to PRG. Always test the rejected and accepted paths, accessible inline errors, and confirmation truthfulness; never mark an unconnected demo form as an operational lead inbox.

---

## Reference: seo-intelligence-and-audit.md

# Evidence-led SEO intelligence and audit orchestration

## Start with the site goal, not an SEO score
For every significant BUILD or REDESIGN, identify the offering, audience, language/region, acquisition intent, conversion and factual constraints. Establish a route-to-intent inventory before choosing layouts. For existing sites, preserve proven landing URLs, queries, backlinks and conversions when evidence exists. Separate site changes that are under the agent's control from market competition and ongoing promotion.

## Capability routing (no mandatory paid API)
1. Inspect access to source, actual server, browser, crawl tools and owner-approved data. Prefer existing authorized source/HTTP/browser evidence. Do not request tokens merely because a skill mentions them.
2. If the owner separately supplies BeyondSEO, use its relevant research or audit guidance; if a compatible SEO Audit Suite is accessible, use its documented interfaces in read-only mode first. Neither is bundled or required. Confirm exact version, supported inputs and output coverage before relying on an integration. Never assume that a skill file invokes a tool automatically.
3. For market research use available public search, appropriate competitor sampling and permitted owner exports (GSC/GA4, keyword, crawl, merchant or local business data). Apify or other external services are optional, only with explicit authorization for data access, costs and processing. Do not send private staging data or secrets to them. No credentials in prompts, reports or artifacts.
4. Without tools, produce a source-grounded first-pass plan with explicit unknowns; never invent search volume, difficulty, position, traffic, citations, backlinks or conversions. Distinguish observed fact, estimate with method, hypothesis, and not verified. Note date, locale, device, sample and missing coverage. Synthetic demo keywords are examples, not market research.

## Before build: search intent and page planning
Group observed user needs into navigational, informational, commercial and transactional intents; map each meaningful cluster to an existing or proposed page. Avoid creating nearly identical landing pages, over-optimizing for one phrase, or competing pages with the same purpose. Use competitor observations to find genuine missing information, not copy text, art or brand identity. Record source, date, confidence, decision, primary action and supporting links in the SEO decision ledger. For redesign, retain useful existing URLs where feasible; document redirects and protected content before modifications. For local business, use only owner-confirmed service areas, address, hours and credentials; no fake branches or reviews. For ecommerce, separate category discovery from product purchase and useful buying guides.

## During build: search and visitor quality together
Make critical page content, primary navigation, product/category links and metadata accessible in served HTML where possible. Write natural titles, descriptions, headings and clear next actions. Use descriptive link anchors, contextual related pages, useful original explanations and appropriately sized images. Connect valuable pages through real crawlable links, not invented topic clusters or mass pages. Use truthful, applicable structured data consistent with visible facts; validate syntax and eligibility independently. Establish entity identity from verified business information, consistent naming, genuine expertise/proof and contact details. For sensitive topics use appropriate qualified review, authoritative references and no fabricated credentials.

## AEO, GEO and conversation readiness
Answer genuine customer questions within useful pages with direct, accurate explanations, supporting detail and reliable references when relevant. Use clear terminology and consistent entity relationships. Make useful original evidence easy to find and cite. Check topical coverage, trust signals and clear navigation; do not mandate FAQ markup, hidden text, AI-specific files, mass Q&A pages or unsupported special ranking rules. Treat these as content-quality heuristics, not measurements of AI visibility. Google AI search follows ordinary search foundations; actual inclusion/citations require separate observation. Do not assert visibility in ChatGPT, Google AI Overviews or other systems without direct evidence.

## Delivery audit: inspect, repair, prove
Audit the authorized route inventory, staging/production rules, raw HTML vs rendered DOM where needed, status codes, canonical/redirect/link/sitemap consistency, intentional indexability, title/description uniqueness and quality, headings, media, orphan candidates, structured data, content usefulness, accessibility, conversion journeys, and applicable performance. Keep full-crawl claims distinct from sampled checks. Sitemap-only URLs are candidate orphans until confirmed against the relevant crawl and intended navigation. Treat third-party link failures according to evidence; a blocked response is not automatically a broken page. For each finding record URL, exact observed evidence, expected behavior, impact, priority, revision, owner action and verification state. Repair in-scope confirmed problems; verify affected behavior and necessary regressions. Do not force a perfect numerical score or silently hide blocked findings. A missing production domain, platform login, API or measurement prevents the corresponding claim, not all useful local work.

## Handover and ongoing SEO boundary
Give the owner a short result: built, fixed, verified, unresolved, next action. Provide a detailed ledger separately when useful. Distinguish launch foundations from long-term rankings, indexing, new content, links, reviews, search demand, competition and field measurements. Optional ongoing SEO may be recommended based on actual gaps, but do not buy backlinks, send outreach, change GBP, submit Search Console or purchase services without approval. No guaranteed rankings or AI citations. Refer to official standards and platform rules for current requirements.

---

## Reference: structured-data-and-local-seo.md

# Entity signals, structured data and local SEO

Implement JSON-LD only for types supported by actual visible content and real owner facts. Choose WebSite, Organization, LocalBusiness, Service, Product, BreadcrumbList, Article and other types **only if appropriate**; validate JSON syntax, URL coherence and applicable Google feature-specific guidelines. Google rich results remain discretionary. Never invent review stars, AggregateRating, addresses, opening hours, pricing, author credentials, awards, FAQ eligibility or contact numbers.

For local-service businesses, require verified business name, real location/service area, valid contact, service taxonomy, accurate hours and owner-approved map links before claiming local SEO readiness. Do not create deceptive multi-city landing pages or auto-claim a Google Business Profile; those are separate authorized operations. Maintain consistent NAP when the site legitimately publishes it. Service-area-only brands must not receive fictional street addresses.

For multilingual sites, use language-specific content and accessible navigation; use hreflang only with valid, reciprocal, canonical alternate URLs. Avoid machine-translated low-quality pages. For ecommerce, product data, availability, pricing and merchant feeds must reflect real source of truth; no fake product ratings. Test structured data via source inspection and official validators when available; record external eligibility as unverified.

---

## Reference: technical-seo-and-indexability.md

# Search-engine-friendly technical foundations

Begin with public URL inventory and content intent. Make actual primary content and crawlable links available in meaningful server-rendered or static HTML; if CSR/JS is necessary, inspect raw HTML vs rendered DOM in browser. Give each indexable route appropriate HTTP status, descriptive title, H1, relevant internal links, meta description, stable URLs and media alt, matching language and locale settings where applicable.

**Indexability gate:** staging/demo environments should use appropriate access controls and/or reliable noindex without accidentally propagating to production. Before publishing, inspect both HTML meta robots and X-Robots-Tag; ensure intentional indexable pages are not `noindex`; robots.txt crawl access must allow necessary resources. Important: robots.txt disallow is not a reliable way to prevent indexing. Never install placeholder canonicals or noindex on a real production launch without explicit decision.

**Canonicals and links:** use real absolute canonical URLs only when domain and policy are confirmed; ensure canonical, internal links, redirects, sitemap and hreflang (if any) agree. Avoid self-contradictory URL declarations, chains or orphan pages. Redirect changed indexed URLs with care, using actual server rules and tests. Handle 404 and 410 meaningfully.

**Robots/sitemap:** only populate sitemap with canonical indexable 200 URLs. Generate robots sitemap directive only for verified production domain. Verify that sitemap itself is reachable and valid XML, not merely present as a file. For dynamic applications, use framework-compatible generation, routes and actual server responses. Search Console requires owner-owned property and explicit permission; sitemap submission never guarantees indexing.

**Site language/metadata:** use meaningful `lang`, viewport meta, OG/Twitter previews when useful (not a ranking substitute), descriptive image names and sensible loading. Avoid broad robots blocking, hidden copy, low-value doorway pages, manipulative redirects, arbitrary keyword-density goals and unsupported ranking guarantees.

---

## Reference: ux-accessibility.md

# Responsive user journeys and accessibility

Target WCAG 2.2 AA as a design/verification aspiration, not an automatic certification. Apply semantic landmarks, hierarchy, visible focus, skip links, labels/instructions/errors, descriptive accessible names, keyboard operability, legible typography, appropriate contrast, input target size, no keyboard traps, reduced motion, logical reading order and screen-reader cues. Avoid blanket `aria-*` where native semantics work better.

Check common breakpoints (320, 375, 768, 1024, 1440) and actual long content; no unwanted horizontal scroll, overlapping headers, clipped CTA, or broken tap targets. Prefer actual page browser navigation over screenshots only. Test keyboard Tab/Shift+Tab, Enter/Space, Escape, menu toggle, form errors, focus after modal/route changes, and zoom where tools permit. Automated axe/lighthouse checks can surface issues but cannot prove WCAG conformance; record manual/screen-reader gaps as NOT RUN or BLOCKED.

Contact journeys must be honest: if there is no server/email integration, provide a usable direct contact option approved by owner or label demo clearly, not a fake success toast. For privacy and consent, consult local laws/owner's policy instead of generating legal guarantees.

## Release-focused accessibility requirements

Check **all text roles** (including small hero captions, error text, form notes and focus states) for WCAG AA contrast, not only body text. Test essential form-control boundaries against each adjacent color at 3:1 non-text contrast, and verify a visibly contrasting keyboard focus indicator. Do not let CSS `overflow-x:hidden` mask content clipped below 320 px; inspect focus and layout at 200% zoom when possible.

When server validation rejects form input, list field-specific actionable messages, connect each invalid input to its message with `aria-invalid`/`aria-describedby`, preserve safe input values, and place keyboard focus on an accessible error summary or first invalid field. Confirm the error and success messages are perceivable to keyboard and assistive-technology users. Never label partial keyboard checks a full screen-reader or WCAG 2.2 AA audit.

---

## Reference: verification-and-release-gates.md

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
