import requests
from bs4 import BeautifulSoup

def fetch_rss_headlines(url, source_name):
    try:
        #print(f"    [FETCH] Trying to pull RSS feed from: {url}")
        response = requests.get(url)
        response.raise_for_status()

        #print("    [FETCH] RSS feed pulled successfully.")
        soup = BeautifulSoup(response.text, 'xml')  # Use XML parsing!

        headlines = []
        for item in soup.find_all('item'):
            title_tag = item.find('title')
            link_tag = item.find('link')
            guid_tag = item.find('guid')
            description_tag = item.find('description')
            pubdate_tag = item.find('pubDate')

            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = link_tag.text.strip()
                guid = guid_tag.text.strip() if guid_tag else link
                description = description_tag.text.strip() if description_tag else "No description available."
                pubdate = pubdate_tag.text.strip() if pubdate_tag else "No publish date available."

                # Save as a dictionary instead of tuple
                headlines.append({
                    "title": title,
                    "link": link,
                    "guid": guid,
                    "description": description,
                    "pubdate": pubdate
                })

        print(f"    [{source_name}] Found {len(headlines)} headlines.")
        return headlines

    except Exception as e:
        print(f"    [ERROR] Fetching RSS: {e}")
        return []