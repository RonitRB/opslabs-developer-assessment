"""Offline tests for validation and CSV behavior; no API credentials required."""
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from task2_youtube_scraper.scraper import ScraperError, Video, _get, extract_video_id, main, write_csv
from task3_slack_bot.slack_bot import app, format_report, validate_payload


class YouTubeScraperTests(unittest.TestCase):
    def test_supported_video_urls(self):
        samples = [
            "https://www.youtube.com/watch?v=abcdefghijk",
            "https://youtu.be/abcdefghijk?t=10",
            "https://youtube.com/shorts/abcdefghijk",
            "https://youtube.com/embed/abcdefghijk",
            "https://youtube.com/live/abcdefghijk",
        ]
        for url in samples:
            with self.subTest(url=url):
                self.assertEqual(extract_video_id(url), "abcdefghijk")

    def test_invalid_url_is_actionable(self):
        for url in ("not a url", "https://example.com/watch?v=abcdefghijk", "https://youtu.be/short"):
            with self.subTest(url=url), self.assertRaisesRegex(ScraperError, "invalid|Unrecognized"):
                extract_video_id(url)

    @patch("task2_youtube_scraper.scraper.settings")
    def test_cli_reports_invalid_url_before_missing_credentials(self, mock_settings):
        mock_settings.youtube_api_key = ""
        with patch("builtins.print") as printer:
            code = main(["--url", "not a url"])
        self.assertEqual(code, 2)
        self.assertIn("invalid", printer.call_args.args[0].lower())

    def test_csv_output_has_six_columns_and_row(self):
        row = Video("Title", "Channel", "Description, quoted", "2025-01-01T00:00:00Z", 12, "https://youtu.be/abcdefghijk")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nested" / "videos.csv"
            write_csv([row], path)
            with path.open(encoding="utf-8-sig", newline="") as fp:
                rows = list(csv.DictReader(fp))
            self.assertEqual(list(rows[0]), ["title", "channel", "description", "publish_date", "views", "url"])
            self.assertEqual(rows[0]["description"], "Description, quoted")
            self.assertEqual(rows[0]["views"], "12")

    @patch("task2_youtube_scraper.scraper.settings")
    @patch("task2_youtube_scraper.scraper.requests.get")
    def test_network_error_does_not_expose_api_key(self, mock_get, mock_settings):
        mock_settings.youtube_api_key = "private-test-key"
        mock_settings.max_retries = 1
        mock_settings.timeout_seconds = 1
        mock_get.side_effect = requests.ConnectionError(
            "failed URL https://example.invalid/?key=private-test-key"
        )
        with self.assertRaises(ScraperError) as error:
            _get("search", {})
        self.assertNotIn("private-test-key", str(error.exception))
        self.assertIn("Check network connectivity", str(error.exception))


class SlackWebhookTests(unittest.TestCase):
    def setUp(self):
        self.metrics = {"leads_contacted": 2345, "replied": 56, "meetings_booked": 4, "positive_replies": 12}

    def test_valid_payload_and_format(self):
        self.assertEqual(validate_payload(self.metrics), self.metrics)
        report = format_report(self.metrics)
        self.assertIn("Leads Contacted: 2,345", report)
        self.assertIn("Positive Replies: 12", report)

    def test_rejects_missing_negative_boolean_and_string_values(self):
        invalid_payloads = [
            {},
            {**self.metrics, "replied": -1},
            {**self.metrics, "replied": True},
            {**self.metrics, "replied": "56"},
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                validate_payload(payload)

    @patch("task3_slack_bot.slack_bot.settings")
    def test_endpoint_rejects_bad_secret_and_schema(self, mock_settings):
        mock_settings.webhook_secret = "expected-secret"
        client = app.test_client()
        wrong_secret = client.post("/webhook/weekly-report", json=self.metrics, headers={"X-Webhook-Secret": "wrong"})
        self.assertEqual(wrong_secret.status_code, 401)
        invalid_schema = client.post("/webhook/weekly-report", json={**self.metrics, "replied": -1}, headers={"X-Webhook-Secret": "expected-secret"})
        self.assertEqual(invalid_schema.status_code, 400)

    @patch("task3_slack_bot.slack_bot.requests.post")
    @patch("task3_slack_bot.slack_bot.settings")
    def test_endpoint_delivers_via_incoming_webhook(self, mock_settings, mock_post):
        mock_settings.webhook_secret = "expected-secret"
        mock_settings.slack_webhook_url = "https://example.invalid/services/test"
        mock_settings.timeout_seconds = 5
        mock_post.return_value.raise_for_status.return_value = None
        response = app.test_client().post(
            "/webhook/weekly-report",
            json=self.metrics,
            headers={"X-Webhook-Secret": "expected-secret"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "sent")
        self.assertIn("Leads Contacted: 2,345", mock_post.call_args.kwargs["json"]["text"])

    @patch("task3_slack_bot.slack_bot.requests.post")
    @patch("task3_slack_bot.slack_bot.settings")
    def test_failed_incoming_webhook_does_not_log_url_secret(self, mock_settings, mock_post):
        mock_settings.webhook_secret = "expected-secret"
        mock_settings.slack_webhook_url = "https://example.invalid/services/test"
        mock_settings.timeout_seconds = 5
        mock_post.side_effect = requests.ConnectionError(
            "failed URL https://example.invalid/services/sensitive-webhook-token"
        )
        with self.assertLogs("task3_slack_bot.slack_bot", level="ERROR") as captured:
            response = app.test_client().post(
                "/webhook/weekly-report",
                json=self.metrics,
                headers={"X-Webhook-Secret": "expected-secret"},
            )
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("sensitive-webhook-token", "\n".join(captured.output))


if __name__ == "__main__":
    unittest.main()
