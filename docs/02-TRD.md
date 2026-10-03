# Technical Requirements

## Runtime

- Python 3.11+ recommended.
- Dependencies are declared in the root and task-level requirements files.
- `.env.example` lists runtime settings; production should use a managed secret store.

## Integrations

- YouTube Data API v3 for search and video details.
- Google Sheets API with service-account access for optional append.
- Airtable, OpenAI, Google Docs, and Slack via Make.com connections for Task 1.
- Slack Web API `chat.postMessage` in the local Task 3 service.

## Reliability and security

- HTTP timeout, bounded exponential retry for network, 429, and transient 5xx API failures.
- Validate IDs, payload types, row boundaries, and maximum request size.
- Never log full request headers, API keys, or Slack tokens.
- Production ingress must use TLS, restricted access, secret rotation, monitoring, and an idempotency strategy.

## Data retention

Keep only requested metadata and generated contact fields. Define retention and deletion windows in the target services before live use. Avoid storing unnecessary private or personal data.
