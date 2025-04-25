# rss_fetcher.py
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import SSLError, ConnectionError

def fetch_rss_headlines(url, verbose=False, retries=3, backoff=5):
    attempt = 0
    while attempt < retries:
        try:
            if verbose:
                print(f"    [FETCH] Attempt {attempt+1}: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'xml')
            headlines = []

            for item in soup.find_all('item'):
                title_tag = item.find('title')
                link_tag = item.find('link')
                guid_tag = item.find('guid')
                description_tag = item.find('description')
                pubdate_tag = item.find('pubDate')

                if title_tag and link_tag:
                    headlines.append({
                        "title": title_tag.text.strip(),
                        "link": link_tag.text.strip(),
                        "guid": guid_tag.text.strip() if guid_tag else link_tag.text.strip(),
                        "description": description_tag.text.strip() if description_tag else "No description available.",
                        "pubdate": pubdate_tag.text.strip() if pubdate_tag else "No publish date available."
                    })

            if verbose:
                print(f"    [FETCH] Retrieved {len(headlines)} headlines.")
            return headlines

        except (SSLError, ConnectionError) as ssl_err:
            print(f"    [WARN] SSL/Connection error while fetching RSS: {ssl_err}")
        except Exception as e:
            print(f"    [ERROR] Fetching RSS: {e}")

        attempt += 1
        time.sleep(backoff * attempt)

    print(f"    [FAIL] Could not fetch RSS from {url} after {retries} attempts.")
    return []