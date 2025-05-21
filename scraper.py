import snscrape.modules.twitter as sntwitter
import pandas as pd

def get_ev_tweets(limit=20):
    query = "EV OR electric vehicle OR sustainability lang:en"
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)
    return pd.DataFrame(tweets, columns=["text"])
