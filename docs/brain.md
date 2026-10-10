# Project Brain

## Current status

- Local source, sample payload, environment template, and documentation have been created.
- Task 2 scraper is live-verified: 10 YouTube records were fetched to CSV and appended to Google Sheets. Task 3 sample payload was delivered through the configured Slack incoming webhook (HTTP 200).
- Task 1's Make scenario was reported by the project owner as completing a successful Run once across Airtable, Groq, Google Docs, Airtable update, and Slack. Daily activation/timezone needs confirmation. Task 1 and Task 3 JSON files in the repo remain tenant-neutral specifications, not native Make.com exports.
- Task 1 uses Groq as its specified LLM provider; `.env.example` names `LLM_PROVIDER=groq` and `GROQ_API_KEY` for local tooling, while Make should hold secrets in managed connections.
- YouTube/Google Sheets and Task 3 direct incoming-webhook delivery are live-verified. Task 1's successful one-time Make run is owner-reported; scheduled activation/timezone has not been confirmed. Task 3's Make scenario and private-channel destination are not independently verified. No Loom video was recorded.

## Decisions

- Use the official YouTube Data API v3 rather than HTML scraping for stable, policy-aligned metadata access.
- Keep service credentials in environment variables or managed Make connections; never check them into source.
- The Slack receiver binds to loopback by default and expects HTTPS termination and production WSGI hosting when deployed.
- Make scenario files document the complete intended flow but avoid fabricated tenant-specific export metadata.

## Assumptions

- Python 3.11 or later and a workspace with network access to configured APIs.
- Users supply valid OAuth/API credentials, Airtable base/table, Google Sheet, Make organization, and Slack channel IDs.
- The report schedule uses 07:00 in a timezone the operator must choose.
- Generated contacts are synthetic and summaries require review before outreach or publication.

## Next priorities

1. Create and verify the actual Make scenarios and Airtable/Groq/Google Docs/Slack integrations.
2. Capture screenshots and record the requested demonstration after those live integrations work.
3. Commit the implementation files directly into the public GitHub task folders.
4. Choose production host, TLS/ingress, monitoring, retention, and retry/idempotency policy.

## Known limitations

- No native Make.com scenario export can be generated accurately without a Make tenant and connections.
- Slack receiver does not persist idempotency keys; retries can post duplicates. Make flows need an idempotency ledger before production.
- Synthetic name/email/company generation and Groq summarization steps are described but require implementation through Make modules.
- The public GitHub repository currently has the package archive and top-level docs; its task folders still need implementation files committed directly.
- Authentication is a shared secret header; a production deployment should prefer signed timestamped requests or gateway authentication and rotation.
