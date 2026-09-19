# Amazon Reviews Data Analytics

## Project Overview

This project analyzes Amazon customer reviews using Python, SQLite, Pandas, Matplotlib, and NLTK. The project was completed as part of the CodeAlpha Data Analytics Internship.

The analysis focuses on three tasks:

* Task 2 — Exploratory Data Analysis (EDA)
* Task 3 — Data Visualization
* Task 4 — Sentiment Analysis

## Dataset

The dataset contains **568,454 Amazon customer reviews** with 10 columns:

* Id
* ProductId
* UserId
* ProfileName
* HelpfulnessNumerator
* HelpfulnessDenominator
* Score
* Time
* Summary
* Text

The SQLite database is stored locally and is excluded from GitHub because of its large size.

## Task 2 — Exploratory Data Analysis

The dataset was analyzed to understand its structure, quality, ratings, review length, helpfulness, product activity, and yearly trends.

### Dataset Summary

| Metric                    |            Result |
| ------------------------- | ----------------: |
| Total Reviews             |           568,454 |
| Total Columns             |                10 |
| Missing Values            |                 0 |
| Duplicate Rows            |                 0 |
| Average Rating            |              4.18 |
| Average Review Length     | 436.22 characters |
| Average Helpfulness Ratio |              0.78 |

### Rating Distribution

| Rating  | Reviews | Percentage |
| ------- | ------: | ---------: |
| 1 Star  |  52,268 |      9.19% |
| 2 Stars |  29,769 |      5.24% |
| 3 Stars |  42,640 |      7.50% |
| 4 Stars |  80,655 |     14.19% |
| 5 Stars | 363,122 |     63.88% |

The majority of reviews have a 5-star rating.

### Yearly Review Trend

The number of reviews increased over time, with the highest number of reviews recorded in **2012**, with 198,659 reviews.

### Product Analysis

The product with the highest number of reviews was:

* Product ID: `B007JFMH8M`
* Number of Reviews: 913

The highest average rating among the analyzed products was:

* Product ID: `B000ED9L9E`
* Average Rating: 4.97
* Number of Reviews: 113

### Data Quality

The dataset contains no missing values and no duplicate records.

Two records were identified where `HelpfulnessNumerator` was greater than `HelpfulnessDenominator`, which can be treated as a small data-quality anomaly.

## Task 3 — Data Visualization

Matplotlib was used to create visualizations for understanding patterns in the Amazon reviews dataset.

### Rating Distribution

![Rating Distribution](charts/rating_distribution.png)

### Rating Percentage

![Rating Percentage](charts/rating_percentage.png)

### Reviews Over Time

![Reviews Over Time](charts/reviews_over_time.png)

### Average Rating Over Time

![Average Rating Over Time](charts/average_rating_over_time.png)

### Top 10 Products by Review Count

![Top 10 Products](charts/top_10_products.png)

### Review Length Distribution

![Review Length Distribution](charts/review_length_distribution.png)

### Helpfulness by Rating

![Helpfulness by Rating](charts/helpfulness_by_rating.png)

## Task 4 — Sentiment Analysis

Sentiment analysis was performed using **NLTK VADER**.

The review `Summary` and `Text` fields were combined and analyzed to calculate sentiment scores.

Reviews were classified into three categories:

* **Positive** — compound sentiment score ≥ 0.05
* **Neutral** — compound sentiment score between -0.05 and 0.05
* **Negative** — compound sentiment score ≤ -0.05

### Sentiment Outputs

The sentiment analysis generated:

* Sentiment distribution chart
* Sentiment percentage chart
* Sentiment vs. rating chart
* Sentiment results CSV file
* Sentiment summary CSV file

### Sentiment Distribution

![Sentiment Distribution](sentiment_results/sentiment_distribution.png)

### Sentiment Percentage

![Sentiment Percentage](sentiment_results/sentiment_percentage.png)

### Sentiment vs Rating

![Sentiment vs Rating](sentiment_results/sentiment_vs_rating.png)

## Key Findings

* The dataset contains 568,454 customer reviews.
* The average customer rating is 4.18 out of 5.
* 5-star reviews represent the largest rating category.
* 2012 contains the highest number of reviews in the dataset.
* The dataset has no missing values or duplicate records.
* Review length varies significantly across customer reviews.
* Helpfulness information provides additional insight into customer engagement.
* Sentiment analysis provides another way to understand customer opinions beyond star ratings.

## Technologies Used

* Python
* Pandas
* SQLite
* Matplotlib
* NLTK
* VADER Sentiment Analysis

## Project Structure

```text
Amazon_Reviews_Project/
│
├── analysis.py
├── visualization.py
├── sentiment.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── charts/
│   ├── rating_distribution.png
│   ├── rating_percentage.png
│   ├── reviews_over_time.png
│   ├── average_rating_over_time.png
│   ├── top_10_products.png
│   ├── review_length_distribution.png
│   └── helpfulness_by_rating.png
│
├── sentiment_results/
│   ├── sentiment_distribution.png
│   ├── sentiment_percentage.png
│   ├── sentiment_vs_rating.png
│   ├── sentiment_summary.csv
│   └── sentiment_results.csv
│
└── data/
    └── Reviews.sqlite/
        └── Reviews.sqlite
```

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Exploratory Data Analysis

```bash
python analysis.py
```

### 3. Generate Visualizations

```bash
python visualization.py
```

### 4. Run Sentiment Analysis

```bash
python sentiment.py
```

## Project Objectives

The main objectives of this project are:

* Perform exploratory data analysis on customer reviews
* Identify rating and review trends
* Analyze product review activity
* Create meaningful data visualizations
* Perform sentiment analysis using NLP
* Understand the relationship between sentiment and star ratings
* Gain practical experience with Python-based data analytics

## Conclusion

This project demonstrates a complete data analytics workflow using a large Amazon reviews dataset. It covers exploratory data analysis, visualization, and sentiment analysis to identify meaningful patterns in customer feedback.

The project provides practical experience in data handling, statistical analysis, visualization, SQLite databases, and Natural Language Processing.

## Internship Information

**Program:** CodeAlpha Data Analytics Internship

**Completed Tasks:**

* Task 2 — Exploratory Data Analysis
* Task 3 — Data Visualization
* Task 4 — Sentiment Analysis
