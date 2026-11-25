# Search-engine-friendly technical foundations

Begin with public URL inventory and content intent. Make actual primary content and crawlable links available in meaningful server-rendered or static HTML; if CSR/JS is necessary, inspect raw HTML vs rendered DOM in browser. Give each indexable route appropriate HTTP status, descriptive title, H1, relevant internal links, meta description, stable URLs and media alt, matching language and locale settings where applicable.

**Indexability gate:** staging/demo environments should use appropriate access controls and/or reliable noindex without accidentally propagating to production. Before publishing, inspect both HTML meta robots and X-Robots-Tag; ensure intentional indexable pages are not `noindex`; robots.txt crawl access must allow necessary resources. Important: robots.txt disallow is not a reliable way to prevent indexing. Never install placeholder canonicals or noindex on a real production launch without explicit decision.

**Canonicals and links:** use real absolute canonical URLs only when domain and policy are confirmed; ensure canonical, internal links, redirects, sitemap and hreflang (if any) agree. Avoid self-contradictory URL declarations, chains or orphan pages. Redirect changed indexed URLs with care, using actual server rules and tests. Handle 404 and 410 meaningfully.

**Robots/sitemap:** only populate sitemap with canonical indexable 200 URLs. Generate robots sitemap directive only for verified production domain. Verify that sitemap itself is reachable and valid XML, not merely present as a file. For dynamic applications, use framework-compatible generation, routes and actual server responses. Search Console requires owner-owned property and explicit permission; sitemap submission never guarantees indexing.

**Site language/metadata:** use meaningful `lang`, viewport meta, OG/Twitter previews when useful (not a ranking substitute), descriptive image names and sensible loading. Avoid broad robots blocking, hidden copy, low-value doorway pages, manipulative redirects, arbitrary keyword-density goals and unsupported ranking guarantees.
