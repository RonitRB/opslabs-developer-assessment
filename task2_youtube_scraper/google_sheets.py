"""Optional Google Sheets writer using a service account with least privilege."""
from __future__ import annotations

from dataclasses import asdict

from shared.config import settings
from task2_youtube_scraper.scraper import Video


def append_videos(videos: list[Video]) -> int:
    if not settings.service_account_file or not settings.spreadsheet_id:
        raise RuntimeError("Set GOOGLE_SERVICE_ACCOUNT_FILE and GOOGLE_SHEETS_SPREADSHEET_ID before using --append-sheets.")
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file(settings.service_account_file, scopes=scopes)
    service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
    values = [[r["title"], r["channel"], r["description"], r["publish_date"], r["views"], r["url"]] for r in map(asdict, videos)]
    if not values:
        return 0
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=settings.spreadsheet_id,
            range=f"'{settings.worksheet}'!A:F",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()
    except HttpError as exc:
        status = getattr(exc.resp, "status", "unknown")
        if status == 403:
            reason = "Check that the service account has Editor access and the Sheets API is enabled."
        elif status == 400:
            reason = "Check the configured worksheet name and column range."
        else:
            reason = "Check Google API availability and retry."
        raise RuntimeError(f"Google Sheets append failed (HTTP {status}). {reason}") from exc
    return int(result.get("updates", {}).get("updatedRows", len(values)))
