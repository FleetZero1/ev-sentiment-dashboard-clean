import pandas as pd
import requests

def get_reddit_posts(subreddits=["electricvehicles", "sustainability", "renewableenergy", "climate", "energy"], limit=20, keywords=None):
    posts = []

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit}"
        headers = {"User-agent": "EVSentimentApp/0.1"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            json_data = response.json()

            for item in json_data["data"]["children"]:
                post_data = item["data"]
                title = post_data.get("title", "")
                body = post_data.get("selftext", "")
                full_text = f"{title} {body}".strip()

                # Filter by keywords if provided
                if not keywords or any(kw.lower() in full_text.lower() for kw in keywords):
                    posts.append(full_text)

        except Exception as e:
            print(f"Error fetching from subreddit {sub}: {e}")

    return pd.DataFrame(posts, columns=["text"]) if posts else pd.DataFrame(columns=["text"])
