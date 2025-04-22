import aiohttp
import requests
from bs4 import BeautifulSoup

def fetch_rss_headlines(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'xml')  # Use XML parsing!

        headlines = []
        for item in soup.find_all('item'):
            title_tag = item.find('title')
            if title_tag:
                headlines.append(title_tag.text.strip())
        return headlines

    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []
