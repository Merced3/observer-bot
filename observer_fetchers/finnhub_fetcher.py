# observer_fetchers/finnhub_fetcher.py

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1/company-news"

def fetch_finnhub_news(symbol="SPY", days_back=2):
    if not FINNHUB_API_KEY:
        print("    [FINNHUB] ❌ No API key found.")
        return []

    # Calculate date range
    today = datetime.utcnow()
    from_date = (today - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    url = f"{BASE_URL}?symbol={symbol}&from={from_date}&to={to_date}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json()

        clean_articles = []
        for article in articles:
            #print(article)
            clean_article = {
                "title": article.get("headline"),
                "link": article.get("url"),
                "pubdate": datetime.utcfromtimestamp(article.get("datetime", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "guid": article.get("id"),
            }
            if article.get("summary"):
                clean_article["description"] = article.get("summary")

            clean_articles.append(clean_article)

        print(f"    [FINNHUB] ✅ Pulled {len(clean_articles)} articles for {symbol}")
        return clean_articles

    except requests.exceptions.HTTPError as http_err:
        print(f"    [FINNHUB] ❌ HTTP Error: {http_err}")
        return []
    except Exception as e:
        print(f"    [FINNHUB] ❌ Other Error: {e}")
        return []
