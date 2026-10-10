# Deployment and Setup

## Local setup

1. Install Python 3.11+ and run `python -m venv .venv`; activate it.
2. Install `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and configure only required values.
4. Use `python -m task2_youtube_scraper.scraper --help` or `python -m task3_slack_bot.slack_bot`.

## YouTube and Sheets

Enable YouTube Data API v3 in a Google Cloud project and create a restricted API key. For Sheets, create a service account with Sheets scope, share the destination sheet with its service-account email, and set its file path and spreadsheet ID. Protect and rotate the key and JSON credential.

## Slack service

Create a Slack app, grant `chat:write`, install it, invite it into the private channel, and set bot token/channel ID. Configure a strong random webhook secret. Production uses Gunicorn or another WSGI server behind HTTPS and a reverse proxy/firewall; never expose Flask's development server publicly.

## Make Task 1 and Task 3

Create Airtable fields per `task1_make_automation/airtable_schema.json`; authorize Airtable, Groq, Google Docs, and Slack connections. Recreate or map the JSON workflow specifications to current Make modules, test with one record, then set the desired timezone and schedule. Store secrets in Make connections. Activate only after verifying error routes, query filters, channel, and schedule. Local tools that need an LLM should set `LLM_PROVIDER=groq` and `GROQ_API_KEY` in `.env`.

## Operational readiness

Configure alerting for failed runs, API quota, Slack errors, and repeated retries. Define retention/deletion, credential rotation, access review, data residency, and backup. Record deployment URL and owner in the private operational runbook, not source control.
