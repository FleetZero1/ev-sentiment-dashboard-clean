import feedparser
import pandas as pd

def get_news_headlines(keywords, limit=10):
    all_entries = []

    for keyword in keywords:
        query = keyword.replace(" ", "+")
        # Removed specific region/language to make it more global
        url = f"https://news.google.com/rss/search?q={query}+when:7d"
        
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                title = entry.title.strip()
                if title not in all_entries:
                    all_entries.append(title)
        except Exception as e:
            print(f"Error fetching news for keyword '{keyword}': {e}")

    return pd.DataFrame(all_entries, columns=["text"]) if all_entries else pd.DataFrame(columns=["text"])
