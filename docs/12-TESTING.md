# Testing and Validation Plan

This document records offline validation and defines the remaining live acceptance checks.

## Offline results — 2026-10-03

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -v`

Result: **8 tests passed.** Coverage: supported/invalid YouTube URLs (including CLI error ordering), CSV columns and escaping, valid Slack message formatting, payload validation, unauthorized/invalid webhook requests, and mocked incoming-webhook delivery. No network calls to third-party services or credentials were used.

## Task 2

- Valid URL formats resolve to an 11-character ID; malformed/foreign URLs fail with a clear message.
- API errors distinguish auth/quota from transient failures; retries remain bounded.
- CSV contains the six expected columns, escaped descriptions, ISO date, and numeric view count.
- Optional Sheets append preserves the same column order and requires a valid sheet and shared service account.

## Task 3

- Health endpoint returns success without requiring Slack credentials.
- Wrong/missing secret, wrong content type, malformed JSON, missing fields, booleans, negatives, and oversized input are rejected.
- Valid values format with thousands separators; Slack channel permission/API/network errors return safe failures.
- Caller retry behavior is checked for duplicate delivery.

## Task 1

- Verify one record through Airtable → summary → Docs → Airtable URL/status.
- Force failures at each external module and verify retry, status, and error notification.
- Verify digest timezone/window, count, latest names, private channel, and no duplicate sends after a retry.

Live checks for Airtable, OpenAI, Google Docs/Sheets, Make scheduling, and Slack delivery remain unrun because no account credentials or workspace identifiers are configured. Run these in the target tenant before claiming end-to-end acceptance.
