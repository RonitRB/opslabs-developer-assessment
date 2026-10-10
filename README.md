# OpsLabs Developer Assessment

Production-oriented reference implementation for the three assessment workflows: contact enrichment and reporting, YouTube metadata collection, and a Slack incoming webhook.

## What is included

- `task1_make_automation/`: exported Make.com Task 1 blueprint, Airtable schema, Google Docs report template, and operator notes. Reconnect tenant-specific services and set the schedule after importing.
- `task2_youtube_scraper/`: validated YouTube Data API v3 scraper, CSV export, optional Google Sheets append, retry/backoff, and CLI.
- `task3_slack_bot/`: authenticated-by-secret HTTP webhook receiver which validates and formats weekly metrics for Slack.
- `shared/`: environment configuration and structured logging helpers.
- `docs/`: project requirements, architecture, schemas, deployment/runbooks, testing plan, decisions, and known limitations.

## Quick start

1. Python 3.11+ recommended. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`; set only the credentials for integrations you will use. Never commit `.env`.
3. Task 2: `python -m task2_youtube_scraper.scraper --query "python automation" --max-results 10 --csv task2_youtube_scraper/output.csv` (requires `YOUTUBE_API_KEY`). For a video URL, replace `--query` with `--url URL`.
4. Task 3: `python -m task3_slack_bot.slack_bot` then POST `task3_slack_bot/webhook_example.json` to `http://localhost:8000/webhook/weekly-report` with `X-Webhook-Secret` set to `WEBHOOK_SECRET`.
5. Task 1: import `task1_make_automation/make_blueprint.json` into Make.com, remap account connections and resource IDs as needed, then configure the schedule and follow the validation steps in its README and `docs/09-AUTOMATION-FLOWS.md`.

## External service setup

Task 2 YouTube search and Google Sheets append have been live-verified (10 rows written and read back). Task 3's sample report has been delivered through the configured Slack incoming webhook. The project owner reports a successful Task 1 Make Run once across Airtable, Groq, Google Docs, Airtable update, and Slack; scheduled activation/timezone has not been confirmed here. Task 3's Make scenario and the Slack webhook's private-channel destination have not been independently verified. Configure secrets via environment variables and Make connections, never by embedding credentials in blueprints. Task 1 local LLM configuration uses `LLM_PROVIDER=groq` and `GROQ_API_KEY`; Make scenarios should use Make-managed Groq credentials.

## Validation and operational notes

The scraper uses the official YouTube Data API; it does not scrape YouTube HTML. API quota, Google OAuth scopes, Make operation limits, retention, and Slack channel permissions apply. See [docs/13-DEPLOYMENT.md](docs/13-DEPLOYMENT.md) and [docs/12-TESTING.md](docs/12-TESTING.md).

Offline tests: `.venv\Scripts\python.exe -m unittest discover -s tests -v` (10 tests passed on 2026-10-10). These tests validate parsing, CSV formatting, payload validation, and error responses without live credentials. Live checks are documented separately in `docs/12-TESTING.md`.

Architecture: [docs/architecture.mmd](docs/architecture.mmd). Screenshots and Loom recording remain outstanding.
