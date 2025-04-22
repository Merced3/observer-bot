# observer_fetchers/fmp_fetcher.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3/stock_news"

def fetch_fmp_news(symbol="SPY", limit=10):
    if not API_KEY:
        print("    [FMP] ❌ No API key found.")
        return []

    url = f"{BASE_URL}?tickers={symbol}&limit={limit}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json()

        clean_articles = []
        for article in articles:
            clean_articles.append({
                "title": article.get("title"),
                "link": article.get("url"),
                "description": article.get("text", ""),
                "pubdate": article.get("publishedDate"),
                "guid": article.get("url"),  # URL is unique
            })

        print(f"    [FMP] ✅ Pulled {len(clean_articles)} articles for {symbol}")
        return clean_articles

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            print("    [FMP] ⚠️ Forbidden (403): The /stock_news endpoint is not available for free tier accounts. Consider upgrading your Financial Modeling Prep plan.")
        else:
            print(f"    [FMP] ❌ HTTP Error: {http_err}")
        return []
    except Exception as e:
        print(f"    [FMP] ❌ Other Error: {e}")
        return []

