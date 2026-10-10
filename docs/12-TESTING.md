# Testing and Validation Plan

This document records offline validation and defines the remaining live acceptance checks.

## Offline results — 2026-10-10

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -v`

Result: **10 tests passed.** Coverage: supported/invalid YouTube URLs (including CLI error ordering), CSV columns and escaping, API-key redaction from network errors, valid Slack message formatting, payload validation, unauthorized/invalid webhook requests, mocked incoming-webhook delivery, and webhook URL redaction on failures.

## Live result — Task 2 — 2026-10-10

- YouTube Data API keyword search returned 10 videos; `task2_youtube_scraper/output.csv` contains 10 rows and all six expected columns.
- Google Sheets API appended 10 rows to the configured `YouTube Scraper Results` spreadsheet, `Sheet1` worksheet. A read-back confirmed 10 rows and six columns.
- An initial append attempt used the nonexistent `Videos` worksheet and was rejected before writing; the configured worksheet was corrected to `Sheet1`, then the append and read-back succeeded.

## Task 2

- Valid URL formats resolve to an 11-character ID; malformed/foreign URLs fail with a clear message.
- API errors distinguish auth/quota from transient failures; retries remain bounded.
- CSV contains the six expected columns, escaped descriptions, ISO date, and numeric view count.
- Optional Sheets append preserves the same column order and requires a valid sheet and shared service account.

## Task 3

Live delivery check: submitted the assessment's sample metrics through the Flask endpoint using a temporary one-run request secret. The configured Slack incoming webhook returned HTTP 200 (`status=sent`, `delivery=incoming_webhook`). This verifies direct delivery through the incoming webhook, but does not verify a Make.com scenario or independently confirm the webhook's destination channel privacy.

- Health endpoint returns success without requiring Slack credentials.
- Wrong/missing secret, wrong content type, malformed JSON, missing fields, booleans, negatives, and oversized input are rejected.
- Valid values format with thousands separators; Slack channel permission/API/network errors return safe failures.
- Caller retry behavior is checked for duplicate delivery.

## Task 1

Live result — user-reported 2026-10-10: the Make.com scenario was run once and all modules completed successfully for Airtable → Groq → Google Docs → Airtable update → Slack. This result is reported by the project owner; execution history was not independently inspected in this workspace. Scheduled daily delivery still depends on activating the scenario and confirming its timezone.

- Verify one record through Airtable → summary → Docs → Airtable URL/status.
- Force failures at each external module and verify retry, status, and error notification.
- Verify digest timezone/window, count, latest names, private channel, and no duplicate sends after a retry.

Task 1's one-time live run is user-reported above; daily scheduling/activation remains to confirm. Task 3 direct Slack incoming-webhook delivery is verified above, but its Make scenario and private-channel destination are not independently verified.
