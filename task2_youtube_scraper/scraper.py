"""Collect YouTube metadata through the official YouTube Data API v3."""
from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

from shared.config import settings
from shared.logger import get_logger

API = "https://www.googleapis.com/youtube/v3"
log = get_logger(__name__)


class ScraperError(Exception):
    """Expected, user-correctable API or input error."""


@dataclass
class Video:
    title: str
    channel: str
    description: str
    publish_date: str
    views: int
    url: str


def extract_video_id(url: str) -> str:
    """Accept standard watch, youtu.be, shorts, embed and live URLs."""
    try:
        parsed = urlparse(url.strip())
    except ValueError as exc:
        raise ScraperError("Invalid video URL.") from exc
    host = (parsed.hostname or "").lower().removeprefix("www.")
    video_id = ""
    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        else:
            match = re.match(r"^/(?:shorts|embed|live)/([^/?#]+)", parsed.path)
            if match:
                video_id = match.group(1)
    elif host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id or ""):
        raise ScraperError("Unrecognized or invalid YouTube video URL. Supply a public video URL with an 11-character video ID.")
    return video_id


def _get(endpoint: str, params: dict) -> dict:
    params = {**params, "key": settings.youtube_api_key}
    for attempt in range(settings.max_retries):
        try:
            response = requests.get(f"{API}/{endpoint}", params=params, timeout=settings.timeout_seconds)
        except requests.RequestException as exc:
            if attempt + 1 == settings.max_retries:
                # Request exception strings may include the full query URL, which contains
                # the API key. Keep details useful without exposing request parameters.
                raise ScraperError(
                    f"YouTube API request failed after retries ({type(exc).__name__}). "
                    "Check network connectivity and retry."
                ) from exc
            time.sleep(min(2 ** attempt, 16))
            continue
        if response.status_code == 200:
            return response.json()
        if response.status_code == 429 or response.status_code >= 500:
            if attempt + 1 < settings.max_retries:
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = min(max(float(retry_after), 0), 30) if retry_after else min(2 ** attempt, 16)
                except ValueError:
                    delay = min(2 ** attempt, 16)
                time.sleep(delay)
                continue
        try:
            reason = response.json().get("error", {}).get("message", response.text[:300])
        except ValueError:
            reason = response.text[:300]
        if response.status_code in (400, 401, 403):
            raise ScraperError(f"YouTube API rejected the request ({response.status_code}): {reason}. Check API key, quota, and YouTube Data API v3 access.")
        raise ScraperError(f"YouTube API returned HTTP {response.status_code}: {reason}")
    raise ScraperError("YouTube API request failed after retries.")


def _map_video(item: dict) -> Video:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    video_id = item.get("id", "")
    return Video(
        title=snippet.get("title", ""),
        channel=snippet.get("channelTitle", ""),
        description=snippet.get("description", ""),
        publish_date=snippet.get("publishedAt", ""),
        views=int(stats.get("viewCount", 0)),
        url=f"https://www.youtube.com/watch?v={video_id}",
    )


def fetch_video(video_id: str) -> list[Video]:
    data = _get("videos", {"part": "snippet,statistics", "id": video_id})
    items = data.get("items", [])
    if not items:
        raise ScraperError("Video was not found or is unavailable to the API (it may be private, deleted, or region restricted).")
    return [_map_video(item) for item in items]


def search_videos(query: str, max_results: int = 10) -> list[Video]:
    if not query.strip():
        raise ScraperError("Search keyword cannot be empty.")
    if not 1 <= max_results <= 50:
        raise ScraperError("max_results must be between 1 and 50.")
    found = _get("search", {"part": "snippet", "type": "video", "q": query.strip(), "maxResults": max_results})
    ids = [x.get("id", {}).get("videoId") for x in found.get("items", [])]
    ids = [x for x in ids if x]
    if not ids:
        return []
    details = _get("videos", {"part": "snippet,statistics", "id": ",".join(ids)})
    return [_map_video(item) for item in details.get("items", [])]


def write_csv(videos: list[Video], path: str | Path) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(Video.__dataclass_fields__)
    with out.open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(asdict(v) for v in videos)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="One YouTube video URL")
    source.add_argument("--query", help="Search keyword")
    parser.add_argument("--max-results", type=int, default=10, help="Search result count (1-50); default 10")
    parser.add_argument("--csv", default="task2_youtube_scraper/output.csv", help="Output CSV path")
    parser.add_argument("--append-sheets", action="store_true", help="Also append rows to configured Google Sheet")
    args = parser.parse_args(argv)
    try:
        video_id = extract_video_id(args.url) if args.url else None
        if not settings.youtube_api_key:
            raise ScraperError("YOUTUBE_API_KEY is required. Copy .env.example to .env and set it.")
        if args.url:
            videos = fetch_video(video_id)
        else:
            videos = search_videos(args.query, args.max_results)
        write_csv(videos, args.csv)
        log.info("Saved %d video rows to %s", len(videos), args.csv)
        if args.append_sheets:
            from task2_youtube_scraper.google_sheets import append_videos
            appended = append_videos(videos)
            print(f"Appended {appended} row(s) to Google Sheets")
        print(f"Saved {len(videos)} video(s) to {args.csv}")
        return 0
    except (ScraperError, OSError, RuntimeError) as exc:
        log.error("Scrape failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
