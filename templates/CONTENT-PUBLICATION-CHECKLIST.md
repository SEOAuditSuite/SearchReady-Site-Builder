# Editorial / Content Website Acceptance Checklist

Site identity: [real owner or explicitly fictional demo]  |  Environment: [staging or production]  |  Date: [verified date]

## Content and information architecture
- [ ] Real editorial goal, audience and subject-matter claims are documented.
- [ ] Index/archive and article URLs provide plain HTML content and direct crawlable links.
- [ ] Article hierarchy and in-page navigation have meaningful headings; no avoidable heading gaps.
- [ ] Categories, tags, series and pagination reflect actual content rather than thin or duplicate pages.
- [ ] Article word counts / reading-time labels are truthful when displayed.
- [ ] Byline and credentials are genuine, or intentionally omitted. Publishing dates and update labels are accurate.
- [ ] Sources, licenses, copyright permissions and fact-checking responsibilities are recorded.

## User experience and technical SEO
- [ ] Search/filter UI has a label, keyboard access, understandable empty state and announced results; no false promise of server search.
- [ ] Text legibility, focus contrast, zoom/forced-color behavior and article reading on narrow screens are checked in the actual deployment where possible.
- [ ] Unique descriptive titles, metadata, language, internal links, status codes and media alt are validated.
- [ ] Real-domain canonical, sitemap, robots/noindex and redirects agree *only after* a production origin is confirmed.
- [ ] Any schema is derived from visible, verified publication/author/date information—not invented data.
- [ ] Performance, security/privacy, deployment, rollback and author-approved release gates are documented.

## Evidence ledger
Record each check as PASS / FAIL / BLOCKED / NOT RUN / STALE, with file/revision, environment and evidence path. Distinguish downloaded static screenshots from live URL-browser runs and from field Core Web Vitals. Never turn fictional demo checks into production SEO claims.
