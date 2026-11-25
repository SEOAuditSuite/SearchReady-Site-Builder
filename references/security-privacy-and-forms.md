# Security, privacy and trustworthy conversions

Match controls to actual deployment. For simple static pages: avoid injecting untrusted HTML, remote unknown JS, unsafe target blank links, exposed source maps/secrets and accidental third-party asset calls. For real backends/lead forms: apply HTTPS, server-side validation, output encoding, anti-spam/rate limiting as appropriate, CSRF considerations, safe storage/transmission, notification monitoring and explicit recipient authorization. Never expose credentials in frontend bundles or static files.

Handle contact flows truthfully. A mock success, downloaded local brief or `mailto:` link is NOT an operational form-submission backend. Report exactly what is and is not connected. For user data and cookies, document collection, retention, consent, privacy policy and applicable laws instead of inventing compliance claims. No unapproved analytics, pixels, emails, SMS or CRM integrations.

Use licensed assets and respect copyrights. No fake social proof, unverified seals, cloned proprietary pages or legal templates pretending to be professional legal advice. Avoid public deployment or billing actions without authorization. Security controls need risk-based independent review for sensitive/authenticated/transactional systems; passing a static build is not production security certification.

## Form confirmation and duplicate prevention

For accepted HTML form POSTs, use **Post/Redirect/Get (HTTP 303)** when appropriate so ordinary refresh/back navigation does not resubmit a record. Bind confirmation to a real accepted event; a public `?saved=1` URL must not falsely claim a submission was stored. Where real payments or bookings exist, use server-side idempotency safeguards in addition to PRG. Always test the rejected and accepted paths, accessible inline errors, and confirmation truthfulness; never mark an unconnected demo form as an operational lead inbox.
