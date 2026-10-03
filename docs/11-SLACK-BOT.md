# Slack Bot Architecture

The Python service accepts weekly metrics over a protected HTTP endpoint and sends them using either a Slack incoming webhook URL or `chat.postMessage`. The bot-token route needs `chat:write` and must be invited to the private channel. Keep the receiver bound to loopback during local work; deploy behind TLS with a production WSGI server, access restrictions, secret management, and health monitoring.

The alternative Make flow uses a Make Custom Webhook and Slack module. Store Slack credentials as Make connections, protect webhook URLs, and configure a safe error route. The local receiver currently has no durable idempotency store; caller retries can create duplicate messages.
