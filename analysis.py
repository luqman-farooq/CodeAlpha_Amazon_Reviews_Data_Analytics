
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

DB_PATH = r"C:\Users\DELL\Desktop\Amazon_Reviews_Project\data\Reviews.sqlite\Reviews.sqlite"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM Reviews", conn)

conn.close()

print("=" * 60)
print("AMAZON REVIEWS - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\n--- DATASET OVERVIEW ---")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

# ============================================================
# 3. FIRST AND LAST RECORDS
# ============================================================

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- LAST 5 ROWS ---")
print(df.tail())

# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n--- MISSING VALUES ---")

missing = df.isnull().sum()

print(missing)

print("\nMissing Percentage:")

missing_percentage = (df.isnull().sum() / len(df)) * 100

print(missing_percentage.round(2))

# ============================================================
# 5. DUPLICATE RECORDS
# ============================================================

print("\n--- DUPLICATE RECORDS ---")

duplicate_count = df.duplicated().sum()

print("Duplicate Rows:", duplicate_count)

# ============================================================
# 6. STATISTICAL SUMMARY
# ============================================================

print("\n--- STATISTICAL SUMMARY ---")

print(df.describe())

# ============================================================
# 7. RATING ANALYSIS
# ============================================================

print("\n--- RATING ANALYSIS ---")

rating_counts = df["Score"].value_counts().sort_index()

print(rating_counts)

print("\nAverage Rating:", round(df["Score"].mean(), 2))

print("Minimum Rating:", df["Score"].min())

print("Maximum Rating:", df["Score"].max())

# ============================================================
# 8. RATING PERCENTAGE
# ============================================================

rating_percentage = (rating_counts / len(df)) * 100

print("\nRating Percentage:")

for rating, percentage in rating_percentage.items():
    print(f"{rating} Stars: {percentage:.2f}%")

# ============================================================
# 9. REVIEW LENGTH ANALYSIS
# ============================================================

print("\n--- REVIEW LENGTH ANALYSIS ---")

df["ReviewLength"] = df["Text"].fillna("").astype(str).str.len()

print("Average Review Length:", round(df["ReviewLength"].mean(), 2))

print("Minimum Review Length:", df["ReviewLength"].min())

print("Maximum Review Length:", df["ReviewLength"].max())

print("\nReview Length Statistics:")

print(df["ReviewLength"].describe())

# ============================================================
# 10. HELPFULNESS ANALYSIS
# ============================================================

print("\n--- HELPFULNESS ANALYSIS ---")

print(
    "Average Helpfulness Numerator:",
    round(df["HelpfulnessNumerator"].mean(), 2)
)

print(
    "Average Helpfulness Denominator:",
    round(df["HelpfulnessDenominator"].mean(), 2)
)

# Avoid division by zero
df["HelpfulnessRatio"] = (
    df["HelpfulnessNumerator"]
    / df["HelpfulnessDenominator"].replace(0, pd.NA)
)

print(
    "Average Helpfulness Ratio:",
    round(df["HelpfulnessRatio"].mean(), 2)
)

# ============================================================
# 11. YEARLY REVIEW ANALYSIS
# ============================================================

print("\n--- YEARLY REVIEW ANALYSIS ---")

df["Date"] = pd.to_datetime(df["Time"], unit="s", errors="coerce")

df["Year"] = df["Date"].dt.year

yearly_reviews = df["Year"].value_counts().sort_index()

print(yearly_reviews)

# ============================================================
# 12. TOP PRODUCTS BY REVIEW COUNT
# ============================================================

print("\n--- TOP 10 PRODUCTS BY REVIEW COUNT ---")

top_products = df["ProductId"].value_counts().head(10)

print(top_products)

# ============================================================
# 13. TOP PRODUCTS BY AVERAGE RATING
# ============================================================

print("\n--- PRODUCTS WITH HIGH AVERAGE RATING ---")

product_rating = (
    df.groupby("ProductId")
    .agg(
        AverageRating=("Score", "mean"),
        ReviewCount=("Score", "count")
    )
)

# Only include products with at least 100 reviews
reliable_product_rating = product_rating[
    product_rating["ReviewCount"] >= 100
].sort_values(
    "AverageRating",
    ascending=False
)

print(reliable_product_rating.head(10))

# ============================================================
# 14. LOW RATING REVIEWS
# ============================================================

print("\n--- LOW RATING REVIEWS ---")

low_rating = df[df["Score"] <= 2]

print("Number of Low Rating Reviews:", len(low_rating))

print(
    "Percentage of Low Rating Reviews:",
    round((len(low_rating) / len(df)) * 100, 2),
    "%"
)

# ============================================================
# 15. HIGH RATING REVIEWS
# ============================================================

print("\n--- HIGH RATING REVIEWS ---")

high_rating = df[df["Score"] >= 4]

print("Number of High Rating Reviews:", len(high_rating))

print(
    "Percentage of High Rating Reviews:",
    round((len(high_rating) / len(df)) * 100, 2),
    "%"
)

# ============================================================
# 16. ANOMALY CHECKS
# ============================================================

print("\n--- ANOMALY CHECKS ---")

print("Scores below 1:", (df["Score"] < 1).sum())

print("Scores above 5:", (df["Score"] > 5).sum())

print(
    "Negative Helpfulness Values:",
    (df["HelpfulnessNumerator"] < 0).sum()
)

print(
    "Helpfulness Numerator > Denominator:",
    (
        df["HelpfulnessNumerator"]
        > df["HelpfulnessDenominator"]
    ).sum()
)

# ============================================================
# 17. VISUALIZATION 1 — RATING DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

rating_counts.plot(kind="bar")

plt.title("Amazon Reviews - Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("rating_distribution.png", dpi=300)
plt.show()

# ============================================================
# 18. VISUALIZATION 2 — YEARLY REVIEWS
# ============================================================

plt.figure(figsize=(10, 5))

yearly_reviews.plot(kind="line", marker="o")

plt.title("Amazon Reviews Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("reviews_over_time.png", dpi=300)
plt.show()

# ============================================================
# 19. VISUALIZATION 3 — REVIEW LENGTH
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(df["ReviewLength"], bins=50)

plt.title("Distribution of Review Length")
plt.xlabel("Review Length (Characters)")
plt.ylabel("Number of Reviews")

plt.tight_layout()
plt.savefig("review_length_distribution.png", dpi=300)
plt.show()

# ============================================================
# 20. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nCharts saved:")
print("1. rating_distribution.png")
print("2. reviews_over_time.png")
print("3. review_length_distribution.png")
