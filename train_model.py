import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("ev_data.csv")

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("model", MultinomialNB())
])

pipeline.fit(X_train, y_train)

joblib.dump(pipeline.named_steps["model"], "ev_sentiment_model.pkl")
joblib.dump(pipeline.named_steps["tfidf"], "ev_tfidf_vectorizer.pkl")
