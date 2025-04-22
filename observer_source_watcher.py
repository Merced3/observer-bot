import json
import os
import asyncio
from observer_fetchers import rss_fetcher
from observer_discord import send_message

SOURCES_FILE = "sources.json"
SEEN_FILE = "seen_headlines.json"

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w") as f:
            json.dump({"sources": []}, f, indent=4)

    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    return [source["url"] for source in data["sources"]]

def load_seen():
    if not os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "w") as f:
            json.dump({}, f)
    with open(SEEN_FILE, "r") as f:
        return json.load(f)

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=4)

async def check_all_sources():
    sources = load_sources()
    seen = load_seen()

    for url in sources:
        if url.endswith(".rss") or "feed" in url:
            headlines = rss_fetcher.fetch_rss_headlines(url)
        else:
            # Placeholder for future source types (API fetchers, scrapers)
            continue

        if not headlines:
            continue

        if url not in seen:
            seen[url] = []

        for headline in headlines:
            if headline not in seen[url]:
                await send_message(f"📰 {headline}")
                seen[url].append(headline)

    save_seen(seen)
