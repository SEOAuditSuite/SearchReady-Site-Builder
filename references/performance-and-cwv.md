# Performance and Core Web Vitals

Design for fast experience, not arbitrary Lighthouse scores. Prefer restrained JS and CSS, responsive images (`srcset`/`sizes`), proper width/height to avoid layout shifts, modern supported formats, local fonts/system fallbacks, long-lived safe caching, lazyload below-the-fold noncritical media, and avoid lazyloading the likely LCP image. Remove unused scripts, heavy icon packs, long main-thread tasks and render-blocking dependencies when appropriate. Keep user-perceived interactivity usable on midrange mobile conditions.

Use actual lab tools (Lighthouse/PageSpeed Insights/DevTools) with identified URL, time, network, device, cache, run count and limitations. Evaluate LCP, INP and CLS using proper **field** measurements where available; INP cannot be certified by one synthetic click. Target 'good' CWV thresholds as guidance: LCP <= 2.5s, INP <= 200ms and CLS <= 0.1 at 75th percentile of real visits; do not label unmeasured field CWV PASS. Compare before/after only for equivalent conditions. Different templates/routes can behave differently, so sample representative pages.

Track resource budgets and evidence by route. Prioritize actual bottlenecks over endless optimization. Avoid false 100/100 score promises, third-party blocking manipulations, hiding content from audits or lowering functionality solely for a score.
