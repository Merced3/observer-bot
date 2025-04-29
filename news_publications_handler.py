# news_publication_handler.py

import os
import json
import asyncio
from observer_discord import send_message
from observer_fetchers import rss_fetcher
from observer_message_format import format_article_message
from shared_state import load_seen_sources, save_seen_source

# For RSS fetcher, waiting for more...
SOURCES_FILE = "sources.json"

DEBUG = False  # Set to True for debugging

async def handle_news(bot):
    """
    This function is ment to be ~broad~

    to check all news sources, current and future additions.
    """
    
    while True:
        sources = load_sources()
        seen_sources = load_seen_sources()
        rss_memory = seen_sources.setdefault("rss_memory", {})

        fetchers = {
            "rss": lambda url: rss_fetcher.fetch_rss_headlines(url, DEBUG)
        }

        for source in sources:
            url = source["url"]
            source_name = source.get("name", "Unknown Source")
            headlines = []

            if url.endswith(".rss") or url.endswith(".xml") or "feed" in url:
                headlines = fetchers["rss"](url)
            else:
                continue # future expansion for other sources

            if not headlines and DEBUG:
                print(f"    [handle_news] No headlines found for: {url}")
                continue

            if url not in rss_memory:
                rss_memory[url] = []

            for article in headlines:
                if article["guid"] not in rss_memory[url]:
                    message = format_article_message(article, source_name)
                    await send_message(bot, message)
                    rss_memory[url].append(article["guid"])
                    if DEBUG: print(f"    [handle_news] New headline posted: {article['title']}")

        save_seen_source(seen_sources) # Save back to disk

        await asyncio.sleep(30)

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w") as f:
            json.dump({"sources": []}, f, indent=4)

    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    return data.get("sources", [])
