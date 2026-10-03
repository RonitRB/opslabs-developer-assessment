# Backend Schema and Architecture

## Components

- `shared.config`: environment-based configuration.
- `shared.logger`: consistent application logging.
- `task2_youtube_scraper.scraper`: input validation, YouTube API calls, normalization, CSV, CLI.
- `task2_youtube_scraper.google_sheets`: optional Sheets append.
- `task3_slack_bot.slack_bot`: Flask health and reporting endpoints, validation, Slack API delivery.
- Make.com owns Task 1 orchestration and scheduled reporting.

## Failure boundaries

Treat API quota/authorization errors as configuration failures, transient transport/429/5xx as bounded retry candidates, and malformed user input as non-retryable. Persist operation IDs and safe errors in Make. Do not retry a non-idempotent Slack post blindly.
