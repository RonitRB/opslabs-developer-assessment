# Task 2 — YouTube metadata collector

The scraper uses the official YouTube Data API v3. It accepts either one video URL or a search phrase and writes a UTF-8 CSV with `title`, `channel`, `description`, `publish_date`, `views`, and `url` columns. It can optionally append the same fields to a Google Sheet.

## Configure

1. Enable YouTube Data API v3 in a Google Cloud project and create an API key.
2. Copy the root `.env.example` to `.env` and set `YOUTUBE_API_KEY`.
3. For Sheets output, configure `GOOGLE_SERVICE_ACCOUNT_FILE`, `GOOGLE_SHEETS_SPREADSHEET_ID`, and `GOOGLE_SHEETS_WORKSHEET`. Share the target spreadsheet with the service account email and enable the Google Sheets API.

## Run

From the project root:

```powershell
python -m task2_youtube_scraper.scraper --url "https://youtu.be/VIDEO_ID" --csv task2_youtube_scraper/output.csv
python -m task2_youtube_scraper.scraper --query "python automation" --max-results 10 --csv task2_youtube_scraper/output.csv
python -m task2_youtube_scraper.scraper --query "python automation" --max-results 10 --append-sheets
```

Video URLs must identify a public video. Search returns at most 50 results. Invalid URLs, missing keys, quota/API failures, and unavailable videos produce an actionable error; transient network, 429, and 5xx errors receive bounded retries. A live keyword run has populated `output.csv` with 10 real video records and appended 10 rows to the configured Google Sheet (`Sheet1`). `sample_output.csv` remains illustrative only.

## Validation

Offline tests: `.venv\Scripts\python.exe -m unittest discover -s tests -v`. These test parsing, CSV formatting, and failure handling without contacting YouTube or Google. A live run requires the credentials above.
