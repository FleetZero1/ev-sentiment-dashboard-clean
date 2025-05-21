import streamlit as st
st.set_page_config(page_title="Global Energy Transition Dashboard", layout="wide")



import joblib
import pandas as pd
import spacy
import string

from reddit_scraper import get_reddit_posts
from news_scraper import get_news_headlines
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 2 minutes
st_autorefresh(interval=120000, key="refresh")

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Load sentiment model and vectorizer
model = joblib.load("ev_sentiment_model.pkl")
vectorizer = joblib.load("ev_tfidf_vectorizer.pkl")

# Global post-oil energy transition keywords
global_keywords = [
    "energy transition", "post-oil world", "fossil fuel phase-out", "net zero",
    "decarbonization", "carbon neutrality", "climate change", "climate crisis",
    "clean energy", "global warming", "electric vehicles", "EV market", "BYD",
    "Tesla", "Rivian", "NIO", "battery range", "lithium mining",
    "solid-state batteries", "EV charging stations", "public chargers",
    "fast charging", "supercharger network", "battery swap stations",
    "charging infrastructure", "solar energy", "wind energy", "offshore wind",
    "green hydrogen", "blue hydrogen", "renewable diesel", "synthetic fuels",
    "biofuels", "natural gas", "LNG", "propane", "hybrid vehicles",
    "hydrogen fuel cells", "smart grid", "energy storage", "battery recycling",
    "vehicle-to-grid", "grid modernization", "energy resilience", "microgrids"
]

# Preprocessing with SpaCy
def preprocess(text):
    doc = nlp(text)
    return ' '.join([token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text.lower() not in string.punctuation])

# Predict sentiment
def predict_sentiment(texts):
    cleaned = [preprocess(t) for t in texts]
    vectors = vectorizer.transform(cleaned)
    return model.predict(vectors)

# UI
st.title("🌍 Global Energy Sentiment Dashboard")

st.markdown("""
This dashboard tracks global public sentiment about the transition away from oil,
including electric vehicles, charging infrastructure, renewable energy, and alternative fuels.

**Data Sources:**
- 🧵 Reddit posts from global subreddits (e.g., r/electricvehicles, r/renewableenergy, r/sustainability)
- 📰 News headlines from Google News using global keywords
""")

# --- Reddit Section ---
st.header("🧵 User Reviews")
if st.button("Fetch Reddit Posts"):
    reddit_df = get_reddit_posts(limit=20, keywords=global_keywords)
    if not reddit_df.empty:
        reddit_df["sentiment"] = ["✅ Positive" if p == 1 else "⚠️ Negative" for p in predict_sentiment(reddit_df["text"])]
        st.dataframe(reddit_df)
        st.bar_chart(reddit_df["sentiment"].value_counts())

        csv = reddit_df.to_csv(index=False)
        st.download_button("📥 Download Reddit Data", data=csv, file_name="global_reddit_sentiment.csv", mime="text/csv")
    else:
        st.warning("No User Reviews found.")

# --- News Section ---
st.header("📰 Global News Headlines")
if st.button("Fetch News"):
    news_df = get_news_headlines(global_keywords, limit=5)  # 5 per keyword
    if not news_df.empty:
        news_df["sentiment"] = ["✅ Positive" if p == 1 else "⚠️ Negative" for p in predict_sentiment(news_df["text"])]
        st.dataframe(news_df)
        st.bar_chart(news_df["sentiment"].value_counts())

        csv = news_df.to_csv(index=False)
        st.download_button("📥 Download News Data", data=csv, file_name="global_news_sentiment.csv", mime="text/csv")
    else:
        st.warning("No news headlines found.")
