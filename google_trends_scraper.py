import requests
import pandas as pd

def get_ev_trends_rapidapi():
    url = "https://google-trends8.p.rapidapi.com/trendingSearches"
    querystring = {"region_code": "US", "hl": "en-US"}

    headers = {
        "X-RapidAPI-Key": "79713d37e6mshd8b7b32c824c4cep165f13jsn8ff2cdcf7eb3",
        "X-RapidAPI-Host": "google-trends8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise RuntimeError(f"Google Trends API error {response.status_code}: {response.text}")

    data = response.json()
    trends = data.get("trendingSearches", [])

    return pd.DataFrame([
        {"topic": t["title"], "traffic": t.get("formattedTraffic", "N/A")}
        for t in trends
    ])
