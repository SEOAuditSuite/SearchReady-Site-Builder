# Responsive user journeys and accessibility

Target WCAG 2.2 AA as a design/verification aspiration, not an automatic certification. Apply semantic landmarks, hierarchy, visible focus, skip links, labels/instructions/errors, descriptive accessible names, keyboard operability, legible typography, appropriate contrast, input target size, no keyboard traps, reduced motion, logical reading order and screen-reader cues. Avoid blanket `aria-*` where native semantics work better.

Check common breakpoints (320, 375, 768, 1024, 1440) and actual long content; no unwanted horizontal scroll, overlapping headers, clipped CTA, or broken tap targets. Prefer actual page browser navigation over screenshots only. Test keyboard Tab/Shift+Tab, Enter/Space, Escape, menu toggle, form errors, focus after modal/route changes, and zoom where tools permit. Automated axe/lighthouse checks can surface issues but cannot prove WCAG conformance; record manual/screen-reader gaps as NOT RUN or BLOCKED.

Contact journeys must be honest: if there is no server/email integration, provide a usable direct contact option approved by owner or label demo clearly, not a fake success toast. For privacy and consent, consult local laws/owner's policy instead of generating legal guarantees.

## Release-focused accessibility requirements

Check **all text roles** (including small hero captions, error text, form notes and focus states) for WCAG AA contrast, not only body text. Test essential form-control boundaries against each adjacent color at 3:1 non-text contrast, and verify a visibly contrasting keyboard focus indicator. Do not let CSS `overflow-x:hidden` mask content clipped below 320 px; inspect focus and layout at 200% zoom when possible.

When server validation rejects form input, list field-specific actionable messages, connect each invalid input to its message with `aria-invalid`/`aria-describedby`, preserve safe input values, and place keyboard focus on an accessible error summary or first invalid field. Confirm the error and success messages are perceivable to keyboard and assistive-technology users. Never label partial keyboard checks a full screen-reader or WCAG 2.2 AA audit.
