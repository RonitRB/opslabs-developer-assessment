# API Specification

## Local webhook

### `GET /health`

Returns `200 {"status":"ok"}` for liveness.

### `POST /webhook/weekly-report`

Headers: `Content-Type: application/json`, `X-Webhook-Secret: <configured secret>`.

Body: integer, non-negative fields `leads_contacted`, `replied`, `meetings_booked`, `positive_replies`. Booleans, strings, missing values, negatives, and values above 2,147,483,647 are rejected.

Success returns `200 {"status":"sent","channel":"…","ts":"…"}`. Errors return 400 malformed/schema, 401 unauthorized, 415 wrong content type, 502 Slack/network failure, or 503 missing Slack configuration. Body size is capped at 16 KB.

## Scraper CLI

Use exactly one of `--url` or `--query`. `--max-results` accepts 1–50. `--csv` selects output location. `--append-sheets` enables the optional Sheets integration. Expected failures exit with status 2.
