"""Environment-backed settings; secrets are never logged."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _positive_int(name: str, default: int) -> int:
    try:
        return max(1, int(os.getenv(name, str(default))))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "")
    service_account_file: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON") or os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    spreadsheet_id: str = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    worksheet: str = os.getenv("GOOGLE_SHEETS_WORKSHEET", "Videos")
    webhook_secret: str = os.getenv("WEBHOOK_SECRET", "")
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
    slack_channel_id: str = os.getenv("SLACK_CHANNEL_ID", "")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = _positive_int("PORT", 8000)
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    timeout_seconds: int = _positive_int("REQUEST_TIMEOUT_SECONDS", 20)
    max_retries: int = _positive_int("MAX_RETRIES", 4)


settings = Settings()
