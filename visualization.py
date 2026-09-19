import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# AMAZON REVIEWS - DATA VISUALIZATION
# ============================================================

print("=" * 60)
print("AMAZON REVIEWS - DATA VISUALIZATION")
print("=" * 60)

# Database path
DB_PATH = "data/Reviews.sqlite/Reviews.sqlite"

# Output folder
OUTPUT_DIR = Path("charts")
OUTPUT_DIR.mkdir(exist_ok=True)

# Connect to database
conn = sqlite3.connect(DB_PATH)

# Load reviews
df = pd.read_sql_query("SELECT * FROM Reviews", conn)

conn.close()

print("\nDataset loaded successfully!")
print("Total Reviews:", len(df))

# ============================================================
# PREPARATION
# ============================================================

# Convert Time to datetime
df["Date"] = pd.to_datetime(df["Time"], unit="s")

# Extract year
df["Year"] = df["Date"].dt.year

# Calculate review length
df["ReviewLength"] = df["Text"].astype(str).str.len()

# ============================================================
# 1. RATING DISTRIBUTION
# ============================================================

rating_counts = df["Score"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
plt.bar(rating_counts.index, rating_counts.values)
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.title("Amazon Reviews - Rating Distribution")
plt.xticks([1, 2, 3, 4, 5])
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "rating_distribution.png", dpi=300)
plt.close()

print("Saved: charts/rating_distribution.png")

# ============================================================
# 2. RATING PERCENTAGE
# ============================================================

rating_percentage = (
    df["Score"].value_counts(normalize=True).sort_index() * 100
)

plt.figure(figsize=(8, 5))
plt.bar(rating_percentage.index, rating_percentage.values)
plt.xlabel("Rating")
plt.ylabel("Percentage of Reviews")
plt.title("Amazon Reviews - Rating Percentage")
plt.xticks([1, 2, 3, 4, 5])
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "rating_percentage.png", dpi=300)
plt.close()

print("Saved: charts/rating_percentage.png")

# ============================================================
# 3. REVIEWS OVER TIME
# ============================================================

yearly_reviews = df["Year"].value_counts().sort_index()

plt.figure(figsize=(10, 5))
plt.plot(yearly_reviews.index, yearly_reviews.values, marker="o")
plt.xlabel("Year")
plt.ylabel("Number of Reviews")
plt.title("Amazon Reviews - Reviews Over Time")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "reviews_over_time.png", dpi=300)
plt.close()

print("Saved: charts/reviews_over_time.png")

# ============================================================
# 4. AVERAGE RATING OVER TIME
# ============================================================

average_rating_year = df.groupby("Year")["Score"].mean()

plt.figure(figsize=(10, 5))
plt.plot(
    average_rating_year.index,
    average_rating_year.values,
    marker="o"
)
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.title("Amazon Reviews - Average Rating Over Time")
plt.ylim(1, 5)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_rating_over_time.png", dpi=300)
plt.close()

print("Saved: charts/average_rating_over_time.png")

# ============================================================
# 5. TOP 10 PRODUCTS BY REVIEW COUNT
# ============================================================

top_products = df["ProductId"].value_counts().head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(top_products.index, top_products.values)
plt.xlabel("Number of Reviews")
plt.ylabel("Product ID")
plt.title("Top 10 Products by Review Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_10_products.png", dpi=300)
plt.close()

print("Saved: charts/top_10_products.png")

# ============================================================
# 6. REVIEW LENGTH DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 5))
plt.hist(df["ReviewLength"], bins=50)
plt.xlabel("Review Length (Characters)")
plt.ylabel("Number of Reviews")
plt.title("Distribution of Review Length")
plt.xlim(0, 3000)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "review_length_distribution.png", dpi=300)
plt.close()

print("Saved: charts/review_length_distribution.png")

# ============================================================
# 7. HELPFULNESS BY RATING
# ============================================================

helpfulness_by_rating = (
    df.groupby("Score")["HelpfulnessNumerator"].mean()
)

plt.figure(figsize=(8, 5))
plt.bar(
    helpfulness_by_rating.index,
    helpfulness_by_rating.values
)
plt.xlabel("Rating")
plt.ylabel("Average Helpfulness Votes")
plt.title("Average Helpfulness by Rating")
plt.xticks([1, 2, 3, 4, 5])
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "helpfulness_by_rating.png", dpi=300)
plt.close()

print("Saved: charts/helpfulness_by_rating.png")

# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nAll charts have been saved in the 'charts' folder.")