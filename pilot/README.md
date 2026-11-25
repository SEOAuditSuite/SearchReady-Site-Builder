# Clearroom — Fictional Home Organization Website Pilot

This is an **original, fictional, local-only service-business demonstration** to validate SearchReady's design, navigation and SEO fundamentals. Not a functioning paid business or verified production website.

Pages: `index.html`, `services.html`, `process.html`, `contact.html`.

All routes deliberately contain `noindex,nofollow` and no real-domain canonicals or XML sitemap. Do **not** publish without replacing the fictional content, obtaining a verified domain, connecting an owner-approved real contact method, and completing a production readiness review.

The contact page downloads a text brief locally; nothing is transmitted. It is not an email/CRM integration.

Local preview:

```bash
cd pilot/site
python -m http.server 8767 --bind 127.0.0.1
```

Check with `python tools/site_preflight.py pilot/site --mode staging`. The test harness runs real HTTP + headless Chromium only if browser automation is installed and executable in its environment. No background server runs after this handover.
