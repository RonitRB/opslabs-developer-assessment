# Project Brain

## Current status

- Local source, sample payload, environment template, and documentation have been created.
- Task 2 scraper and Task 3 Flask webhook are implemented but require API keys and have not been exercised against live services.
- Task 1 and Task 3 Make JSON files are tenant-neutral scenario specifications, not native Make.com exports. They need mapping and validation inside a Make organization.
- No external services are connected, no live records were created, and no Loom video was recorded.

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

1. Install dependencies and run local validation.
2. Provision API access, credentials, Airtable and Google resources.
3. Import/recreate Make flows, map modules, and perform end-to-end checks.
4. Choose production host, TLS/ingress, monitoring, retention, and retry/idempotency policy.
5. Record the requested demonstration after live integrations work.

## Known limitations

- No native Make.com scenario export can be generated accurately without a Make tenant and connections.
- Slack receiver does not persist idempotency keys; retries can post duplicates. Make flows need an idempotency ledger before production.
- Synthetic name/email/company generation and OpenAI summarization steps are described but require implementation through Make modules.
- Authentication is a shared secret header; a production deployment should prefer signed timestamped requests or gateway authentication and rotation.
