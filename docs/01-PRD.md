# Product Requirements

## Users

An assessment reviewer should be able to understand the architecture, inspect the code, set credentials, execute the local scraper and webhook, and configure the Make scenarios in a tenant.

## Functional requirements

1. Task 1 generates a valid synthetic contact, creates an Airtable record, summarizes its company with an AI service, creates a Google Doc, updates the Airtable record, and sends a 07:00 daily Slack digest.
2. Task 2 accepts either one YouTube URL or a search phrase, returns the required metadata, handles malformed/unavailable input clearly, and writes CSV plus optional Google Sheets rows.
3. Task 3 accepts a JSON metrics object, validates all required non-negative integer values, and sends a readable weekly report to the configured Slack channel.
4. All tasks document configuration, error handling, retries, scheduling, and credential management.

## Non-functional requirements

- Secrets are not committed or included in logs.
- API calls have explicit timeouts and bounded retries where safe.
- Invalid input fails with actionable messages and suitable HTTP/CLI status.
- Workflows are modular and operationally observable.
- Data collection is limited to requested public metadata and synthetic contact data.

## Acceptance evidence

Source and sample payloads are included. Live acceptance requires configured external accounts, successful end-to-end runs, and saved run evidence; this package alone does not establish those external results.
