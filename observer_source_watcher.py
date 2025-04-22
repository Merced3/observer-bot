# observer_source_watcher.py
import json
import os
from observer_fetchers import rss_fetcher
from observer_discord import send_message
from observer_message_format import format_article_message


SOURCES_FILE = "sources.json"
SEEN_FILE = "seen_headlines.json"

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w") as f:
            json.dump({"sources": []}, f, indent=4)

    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    return data.get("sources", [])

def load_seen():
    if not os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "w") as f:
            json.dump({}, f)

    with open(SEEN_FILE, "r") as f:
        return json.load(f)

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=4)

async def check_all_sources(bot):
    print("[Observer] Checking all sources...")  # New: Visual indicator in terminal
    sources = load_sources()
    seen = load_seen()

    for source in sources:
        url = source["url"]
        source_name = source.get("name", "Unknown Source")
        # Detect source type (basic detection for now)
        if url.endswith(".rss") or url.endswith(".xml") or "feed" in url:
            headlines = rss_fetcher.fetch_rss_headlines(url)
        else:
            # Placeholder for other fetchers, scrapers, etc.
            print(f"  [Observer] No fetcher available for: {url}")
            continue

        if not headlines:
            print(f"  [Observer] No headlines found for: {url}")
            continue

        # Initialize if URL has never been seen before
        if url not in seen:
            seen[url] = []

        for article in headlines:
            if article["guid"] not in seen[url]: # Info Wars
                message = format_article_message(article, source_name)
                await send_message(bot, message)
                seen[url].append(article["guid"])
                print(f"  [Observer] New headline posted: {article['title']}")

    save_seen(seen)
    print("[Observer] Finished checking sources.\n")
