import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DATABASE CONNECTION
# ============================================================

DB_PATH = r"C:\Users\DELL\Desktop\Amazon_Reviews_Project\data\Reviews.sqlite\Reviews.sqlite"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM Reviews", conn)

conn.close()

print("Dataset loaded successfully!")
print("Rows:", len(df))

# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

import os

os.makedirs("charts", exist_ok=True)

# ============================================================
# 1. RATING DISTRIBUTION
# ============================================================

rating_counts = df["Score"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

rating_counts.plot(kind="bar")

plt.title("Amazon Reviews - Rating Distribution")
plt.xlabel("Star Rating")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/rating_distribution.png", dpi=300)
plt.show()

# ============================================================
# 2. RATING PERCENTAGE
# ============================================================

rating_percentage = (
    df["Score"].value_counts(normalize=True)
    .sort_index() * 100
)

plt.figure(figsize=(8, 5))

rating_percentage.plot(kind="bar")

plt.title("Percentage of Reviews by Rating")
plt.xlabel("Star Rating")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/rating_percentage.png", dpi=300)
plt.show()

# ============================================================
# 3. REVIEWS OVER TIME
# ============================================================

df["Date"] = pd.to_datetime(
    df["Time"],
    unit="s",
    errors="coerce"
)

df["Year"] = df["Date"].dt.year

yearly_reviews = df["Year"].value_counts().sort_index()

plt.figure(figsize=(10, 5))

yearly_reviews.plot(kind="line", marker="o")

plt.title("Amazon Reviews Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Reviews")

plt.grid(True)

plt.tight_layout()
plt.savefig("charts/reviews_over_time.png", dpi=300)
plt.show()

# ============================================================
# 4. AVERAGE RATING BY YEAR
# ============================================================

yearly_rating = (
    df.groupby("Year")["Score"]
    .mean()
)

plt.figure(figsize=(10, 5))

yearly_rating.plot(kind="line", marker="o")

plt.title("Average Rating Over Time")
plt.xlabel("Year")
plt.ylabel("Average Rating")

plt.tight_layout()
plt.savefig("charts/average_rating_over_time.png", dpi=300)
plt.show()

# ============================================================
# 5. TOP 10 MOST REVIEWED PRODUCTS
# ============================================================

top_products = (
    df["ProductId"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_products.plot(kind="barh")

plt.title("Top 10 Most Reviewed Products")
plt.xlabel("Number of Reviews")
plt.ylabel("Product ID")

plt.tight_layout()
plt.savefig("charts/top_10_products.png", dpi=300)
plt.show()

# ============================================================
# 6. REVIEW LENGTH DISTRIBUTION
# ============================================================

df["ReviewLength"] = (
    df["Text"]
    .fillna("")
    .astype(str)
    .str.len()
)

plt.figure(figsize=(9, 5))

plt.hist(df["ReviewLength"], bins=50)

plt.title("Distribution of Review Length")
plt.xlabel("Review Length (Characters)")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("charts/review_length_distribution.png", dpi=300)
plt.show()

# ============================================================
# 7. HELPFULNESS VS RATING
# ============================================================

df["HelpfulnessRatio"] = (
    df["HelpfulnessNumerator"]
    / df["HelpfulnessDenominator"].replace(0, pd.NA)
)

helpfulness_by_rating = (
    df.groupby("Score")["HelpfulnessRatio"]
    .mean()
)

plt.figure(figsize=(8, 5))

helpfulness_by_rating.plot(
    kind="bar"
)

plt.title("Average Helpfulness Ratio by Rating")
plt.xlabel("Star Rating")
plt.ylabel("Average Helpfulness Ratio")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("charts/helpfulness_by_rating.png", dpi=300)
plt.show()

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("TASK 3 - DATA VISUALIZATION COMPLETED!")
print("=" * 60)

print("\nCharts saved inside the 'charts' folder:")
print("1. rating_distribution.png")
print("2. rating_percentage.png")
print("3. reviews_over_time.png")
print("4. average_rating_over_time.png")
print("5. top_10_products.png")
print("6. review_length_distribution.png")
print("7. helpfulness_by_rating.png")
