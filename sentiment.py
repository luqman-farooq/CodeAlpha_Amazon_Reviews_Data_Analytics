import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

DB_PATH = "data/Reviews.sqlite/Reviews.sqlite"
conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM Reviews", conn)

conn.close()

print("=" * 60)
print("AMAZON REVIEWS - SENTIMENT ANALYSIS")
print("=" * 60)

print("\nTotal Reviews:", len(df))

# ============================================================
# 2. INSTALL / IMPORT VADER
# ============================================================

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except ImportError:
    print("\nNLTK is not installed.")
    print("Run: pip install nltk")
    raise

import nltk

# Download VADER lexicon if needed
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    print("\nDownloading VADER lexicon...")
    nltk.download("vader_lexicon")

# ============================================================
# 3. CREATE SENTIMENT ANALYZER
# ============================================================

sia = SentimentIntensityAnalyzer()

# ============================================================
# 4. COMBINE SUMMARY + REVIEW TEXT
# ============================================================

df["ReviewText"] = (
    df["Summary"].fillna("").astype(str)
    + " "
    + df["Text"].fillna("").astype(str)
)

# ============================================================
# 5. CALCULATE SENTIMENT SCORE
# ============================================================

print("\nCalculating sentiment scores...")

df["SentimentScore"] = df["ReviewText"].apply(
    lambda text: sia.polarity_scores(text)["compound"]
)

# ============================================================
# 6. CLASSIFY SENTIMENT
# ============================================================

def classify_sentiment(score):

    if score >= 0.05:
        return "Positive"

    elif score <= -0.05:
        return "Negative"

    else:
        return "Neutral"


df["Sentiment"] = df["SentimentScore"].apply(
    classify_sentiment
)

# ============================================================
# 7. SENTIMENT SUMMARY
# ============================================================

print("\n--- SENTIMENT DISTRIBUTION ---")

sentiment_counts = (
    df["Sentiment"]
    .value_counts()
)

print(sentiment_counts)

print("\n--- SENTIMENT PERCENTAGE ---")

sentiment_percentage = (
    df["Sentiment"]
    .value_counts(normalize=True)
    * 100
)

for sentiment, percentage in sentiment_percentage.items():

    print(
        f"{sentiment}: {percentage:.2f}%"
    )

# ============================================================
# 8. SENTIMENT BY STAR RATING
# ============================================================

print("\n--- SENTIMENT BY STAR RATING ---")

sentiment_rating = pd.crosstab(
    df["Score"],
    df["Sentiment"]
)

print(sentiment_rating)

# ============================================================
# 9. AVERAGE SENTIMENT BY STAR RATING
# ============================================================

print("\n--- AVERAGE SENTIMENT SCORE BY RATING ---")

average_sentiment_rating = (
    df.groupby("Score")["SentimentScore"]
    .mean()
)

print(
    average_sentiment_rating.round(3)
)

# ============================================================
# 10. CREATE OUTPUT FOLDER
# ============================================================

os.makedirs("sentiment_results", exist_ok=True)

# ============================================================
# 11. SENTIMENT DISTRIBUTION CHART
# ============================================================

plt.figure(figsize=(8, 5))

sentiment_counts.plot(
    kind="bar"
)

plt.title("Amazon Reviews - Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "sentiment_results/sentiment_distribution.png",
    dpi=300
)

plt.show()

# ============================================================
# 12. SENTIMENT PERCENTAGE CHART
# ============================================================

plt.figure(figsize=(8, 5))

sentiment_percentage.plot(
    kind="bar"
)

plt.title("Amazon Reviews - Sentiment Percentage")
plt.xlabel("Sentiment")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "sentiment_results/sentiment_percentage.png",
    dpi=300
)

plt.show()

# ============================================================
# 13. SENTIMENT VS RATING
# ============================================================

sentiment_rating.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Sentiment Distribution by Star Rating")
plt.xlabel("Star Rating")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.savefig(
    "sentiment_results/sentiment_vs_rating.png",
    dpi=300
)

plt.show()

# ============================================================
# 14. SAVE RESULTS TO CSV
# ============================================================

result_columns = [
    "Id",
    "ProductId",
    "UserId",
    "Score",
    "Summary",
    "Text",
    "SentimentScore",
    "Sentiment"
]

df[result_columns].to_csv(
    "sentiment_results/sentiment_results.csv",
    index=False
)

# ============================================================
# 15. SAVE SUMMARY
# ============================================================

summary = pd.DataFrame({
    "Sentiment": sentiment_percentage.index,
    "Percentage": sentiment_percentage.values
})

summary.to_csv(
    "sentiment_results/sentiment_summary.csv",
    index=False
)

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("TASK 4 - SENTIMENT ANALYSIS COMPLETED!")
print("=" * 60)

print("\nFiles created inside 'sentiment_results':")

print("1. sentiment_distribution.png")
print("2. sentiment_percentage.png")
print("3. sentiment_vs_rating.png")
print("4. sentiment_results.csv")
print("5. sentiment_summary.csv")
