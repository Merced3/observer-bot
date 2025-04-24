# observer_source_watcher.py
import json
import os
from observer_discord import send_message
from observer_message_format import format_article_message
from observer_fetchers import rss_fetcher, fmp_fetcher, finnhub_fetcher


SOURCES_FILE = "sources.json"
SEEN_FILE = "seen_headlines.json"
DEBUG = False

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
    if DEBUG: print("  [Observer] Checking all sources...")
    
    sources = load_sources()
    seen = load_seen()

    fetchers = {
        "finnhub.io": lambda: finnhub_fetcher.fetch_finnhub_news(symbol="SPY"),
        "financialmodelingprep": lambda: fmp_fetcher.fetch_fmp_news(symbol="SPY"),
        "rss": lambda url: rss_fetcher.fetch_rss_headlines(url, DEBUG)
    }

    for source in sources:
        url = source["url"]
        source_name = source.get("name", "Unknown Source")
        headlines = []

        # Pick correct fetcher
        if "finnhub.io" in url:
            headlines = fetchers["finnhub.io"]()
        #elif "financialmodelingprep" in url:
            #headlines = fetchers["financialmodelingprep"]()
        elif url.endswith(".rss") or url.endswith(".xml") or "feed" in url:
            headlines = fetchers["rss"](url)
        else:
            #print(f"  [Observer] No fetcher available for: {url}")
            continue

        if not headlines and DEBUG:
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
                if DEBUG: print(f"  [Observer] New headline posted: {article['title']}")

    save_seen(seen)
    if DEBUG: print("  [Observer] Finished checking sources.\n")
