# observer_fetchers/trending_fetcher.py

from pytrends.request import TrendReq
import os
import json
import datetime
from observer_discord import send_message

TRENDING_FILE = "trending_terms.json"
DEBUG = False

def fetch_trending_terms(top_n=10):
    pytrends = TrendReq()

    try:
        trending = pytrends.trending_searches(pn="united_states")
        trending_terms = trending[0].tolist()[:top_n]  # Get top N terms
        return trending_terms
    except Exception as e:
        print(f"    [ERROR] Fetching trending terms: {e}")
        return []

def save_trending_terms(terms):
    if not os.path.exists(TRENDING_FILE):
        with open(TRENDING_FILE, "w") as f:
            json.dump({"terms": []}, f, indent=4)

    with open(TRENDING_FILE, "r") as f:
        data = json.load(f)

    data["terms"].append({
        "date": str(datetime.utcnow()),
        "terms": terms
    })

    with open(TRENDING_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def check_trending(bot):
    trending_terms = fetch_trending_terms()

    if not trending_terms:
        return

    message = "**🔥 Top Trending Search Terms Today:**\n\n"
    for term in trending_terms:
        message += f"• {term}\n"

    await send_message(bot, message)
    save_trending_terms(trending_terms)

    if DEBUG:
        print(f"  [TRENDING] Saved {len(trending_terms)} trending terms.")
