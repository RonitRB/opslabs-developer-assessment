"""HTTP receiver for weekly metrics; forwards validated payloads to Slack."""
from __future__ import annotations

import hmac
from typing import Any

from flask import Flask, jsonify, request
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError, SlackRequestError

from shared.config import settings
from shared.logger import get_logger

log = get_logger(__name__)
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
FIELDS = ("leads_contacted", "replied", "meetings_booked", "positive_replies")
MAX_METRIC = 2_147_483_647


def validate_payload(payload: Any) -> dict[str, int]:
    if not isinstance(payload, dict):
        raise ValueError("JSON body must be an object.")
    normalized: dict[str, int] = {}
    for field in FIELDS:
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > MAX_METRIC:
            raise ValueError(f"{field} must be an integer between 0 and {MAX_METRIC}.")
        normalized[field] = value
    return normalized


def format_report(metrics: dict[str, int]) -> str:
    return "*Weekly Report*\n\n" + "\n".join([
        f"Leads Contacted: {metrics['leads_contacted']:,}",
        f"Replies: {metrics['replied']:,}",
        f"Meetings Booked: {metrics['meetings_booked']:,}",
        f"Positive Replies: {metrics['positive_replies']:,}",
    ])


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/webhook/weekly-report")
def weekly_report():
    expected = settings.webhook_secret
    supplied = request.headers.get("X-Webhook-Secret", "")
    if not expected or not hmac.compare_digest(supplied.encode(), expected.encode()):
        return jsonify({"error": "unauthorized"}), 401
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415
    try:
        metrics = validate_payload(request.get_json(silent=False))
    except Exception as exc:
        # Flask may raise BadRequest for malformed JSON; do not return parser internals.
        return jsonify({"error": str(exc) if isinstance(exc, ValueError) else "Malformed JSON body."}), 400
    if not settings.slack_webhook_url and (not settings.slack_bot_token or not settings.slack_channel_id):
        log.error("Slack delivery is not configured")
        return jsonify({"error": "Slack delivery is not configured."}), 503
    try:
        if settings.slack_webhook_url:
            response = requests.post(
                settings.slack_webhook_url,
                json={"text": format_report(metrics), "unfurl_links": False, "unfurl_media": False},
                timeout=settings.timeout_seconds,
            )
            response.raise_for_status()
            return jsonify({"status": "sent", "delivery": "incoming_webhook"}), 200
        response = WebClient(token=settings.slack_bot_token, timeout=settings.timeout_seconds).chat_postMessage(
            channel=settings.slack_channel_id,
            text=format_report(metrics),
            unfurl_links=False,
            unfurl_media=False,
        )
        return jsonify({"status": "sent", "channel": response.get("channel"), "ts": response.get("ts")}), 200
    except SlackApiError as exc:
        code = exc.response.get("error", "unknown")
        log.error("Slack API rejected report: %s", code)
        status = 429 if exc.response.status_code == 429 else 502
        return jsonify({"error": "Slack rejected the report.", "code": code}), status
    except SlackRequestError:
        log.exception("Slack request failed")
        return jsonify({"error": "Slack could not be reached."}), 502
    except requests.RequestException as exc:
        # Exception strings can contain the webhook URL, which embeds its secret.
        log.error("Slack incoming webhook request failed (%s)", type(exc).__name__)
        return jsonify({"error": "Slack could not be reached."}), 502


if __name__ == "__main__":
    if not settings.webhook_secret:
        raise SystemExit("WEBHOOK_SECRET must be configured before starting the webhook service.")
    # Bind loopback by default. Use a production WSGI server behind TLS for deployment.
    app.run(host=settings.host, port=settings.port, debug=False)
