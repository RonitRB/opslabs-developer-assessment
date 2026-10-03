# YouTube Scraper Design

The collector calls the official YouTube Data API v3. URL parsing recognizes watch, short, embed, live, and youtu.be formats, then validates the 11-character ID. Keyword mode calls `search.list` followed by `videos.list` to obtain current view counts and detailed metadata. API results are normalized to six columns, with UTC publication timestamps and numeric views.

Network and transient server/rate-limit failures use bounded backoff. Invalid URLs, inaccessible videos, quota/credential errors, and empty results are reported clearly. Search consumes API quota; use small result limits and monitor the Google Cloud quota dashboard. HTML scraping is intentionally not used.
