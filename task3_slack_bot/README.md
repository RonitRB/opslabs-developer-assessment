# Task 3 — Slack weekly report webhook

## Local run

Set `WEBHOOK_SECRET` and either `SLACK_WEBHOOK_URL` or both `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` in `.env`, then run `python -m task3_slack_bot.slack_bot`. An incoming webhook is bound to its configured channel; the bot-token route needs `chat:write` and must be invited to the private target channel. The service binds to `127.0.0.1` by default. Send `webhook_example.json` as JSON with an `X-Webhook-Secret` header.

```sh
curl -X POST http://127.0.0.1:8000/webhook/weekly-report \
  -H 'Content-Type: application/json' -H 'X-Webhook-Secret: replace-with-a-long-random-secret' \
  --data-binary @task3_slack_bot/webhook_example.json
```

`GET /health` is a minimal liveness endpoint. Invalid content, wrong secrets, missing Slack configuration, API errors, and network errors return explicit HTTP errors without leaking tokens. The service caps request bodies at 16 KB.

## Make.com

For the assessment architecture, a Make Custom Webhook can receive the external payload, use a Slack module to format and post the report, and return a webhook response. The included Make blueprint is a configuration skeleton; connect the private channel and activate scheduling only after importing and validating it in your own Make organization. Store credentials in Make connections. Keep webhook URLs private, rotate them if exposed, and use HTTPS.

## Production deployment

Use a WSGI server (for example Gunicorn), TLS termination, a restricted ingress allowlist or signed request authentication, secret storage, centralized logs, and monitoring. Do not expose Flask's development server to the public internet. Configure retries at the caller with bounded backoff; Slack posting is not exactly-once, so use an idempotency ledger if upstream retries can repeat the same business event.
