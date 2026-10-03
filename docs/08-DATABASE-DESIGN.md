# Database Design

## Airtable `Contacts`

| Field | Type | Purpose |
| --- | --- | --- |
| Name | Single line text | Synthetic contact name; primary field |
| Email | Email | Generated contact email |
| Company | Single line text | Company used in enrichment |
| Summary | Long text | AI-produced company summary |
| Google Doc URL | URL | Created report link |
| Created Date | Date/time | UTC creation timestamp |
| Status | Single select | pending, processing, complete, failed |
| Idempotency Key | Single line text | Prevent duplicate generation on retries |

## Google Sheets `Videos`

Header order: `Title`, `Channel`, `Description`, `Publish Date`, `Views`, `URL`. Store view counts numerically and publication timestamps in ISO 8601 UTC format.

Google Docs are one document per completed contact, based on `task1_make_automation/company_report_template.md`.
