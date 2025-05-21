import pandas as pd
import snscrape.modules.twitter as sntwitter

def get_ev_tweets(query="EV OR electric vehicle OR sustainability", limit=20):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{query} lang:en").get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)
    return pd.DataFrame(tweets, columns=["text"])
