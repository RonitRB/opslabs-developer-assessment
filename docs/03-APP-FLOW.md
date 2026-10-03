# Application Flow

## Task 1

Trigger → generate synthetic contact → validate → Airtable create → AI company summary → create Google Doc from template → update Airtable with summary and URL → scheduled digest queries completed records → aggregate → Slack.

## Task 2

CLI URL or query → validate input → YouTube API search/details → normalize fields → write UTF-8 CSV → optionally append rows to Google Sheets.

## Task 3

JSON POST + shared secret → validate schema → format report → Slack API post → return delivery status. Invalid authorization, JSON, schema, or downstream Slack configuration returns a 4xx/5xx response.

Failure routes should retain a correlation/idempotency key and safe error context, then alert an operator after bounded retries.
