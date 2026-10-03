# Automation Flows

## Task 1 contact processing

Use a manual trigger for acceptance and then a controlled scheduler. Generate synthetic—not real—contact data. Validate email and required fields before writing. Create an Airtable row with `processing` status and idempotency key. Summarize the company with a conservative prompt. Create a Google Doc, then update summary, URL, timestamp, and status. On failure, set status to failed and persist module name, correlation ID, and sanitized error. Retry transient failures up to three times with exponential backoff; avoid duplicating a Doc by checking its idempotency key before recreation.

## Task 1 daily report

Schedule at 07:00 in an explicitly selected timezone. Query only completed records with Doc URLs for the preceding digest window. Report counts and up to five latest distinct company names. Define whether counts are for the prior calendar day or since the previous successful run; calendar-day in the chosen timezone is the default recommendation.

## Task 3

Use Make Custom Webhook → validate all four metric fields → compose a Slack message → post using a Slack connection → return success. Protect the webhook URL, use TLS, add error handling, and limit retries for non-idempotent posts.
