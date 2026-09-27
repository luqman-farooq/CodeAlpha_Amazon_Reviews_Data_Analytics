
````markdown
# 🛒 Amazon Reviews Data Analytics Dashboard

An interactive **Amazon Reviews Data Analytics Dashboard** developed using Python, Streamlit, Pandas, NumPy, SQLite, and Plotly.

This project was developed as part of the **CodeAlpha Data Analytics Internship** and focuses on exploratory data analysis, data visualization, product analysis, sentiment analysis, and data-quality assessment of a large Amazon customer reviews dataset.

---

## 📌 Project Overview

Amazon customer reviews contain valuable information about customer satisfaction, product popularity, review behavior, helpfulness, and sentiment.

This project transforms a large Amazon Reviews dataset into an interactive analytics dashboard where users can explore the data through:

- Interactive filters
- KPI cards
- Data-quality checks
- Interactive Plotly charts
- Product-level analysis
- Sentiment analysis
- Review trends
- Downloadable filtered data

The project combines data analysis with an interactive **Streamlit dashboard** to make the results easier to explore and understand.

---

## 📊 Dashboard

The main application is built with **Streamlit**.

The dashboard contains the following sections:

```text
Overview
│
├── EDA
│
├── Visualizations
│
├── Product Analysis
│
├── Sentiment Analysis
│
└── Data Quality
````

Users can navigate between these sections using the sidebar.

---

## 🏠 Overview

The Overview section provides a quick summary of the review dataset.

### Key Performance Indicators

The dashboard displays:

* Total Reviews
* Average Rating
* Average Review Length
* Helpfulness Percentage

### Overview Visualizations

Interactive charts include:

* Rating Distribution
* Rating Share
* Reviews Trend by Year

These visualizations provide a quick understanding of customer rating patterns and review activity.

---

## 🔎 Exploratory Data Analysis

The EDA section provides detailed information about the dataset structure and quality.

### EDA Metrics

* Number of Rows
* Number of Columns
* Missing Values
* Duplicate Rows

### Additional Analysis

The dashboard also provides:

* Review Length Distribution
* Dataset Preview
* Column Information
* Data Types
* Basic statistical information

---

## 📈 Data Visualizations

Interactive visualizations are created using **Plotly**.

### Visualizations Included

1. Rating Distribution
2. Reviews Over Time
3. Average Rating by Year
4. Helpful Votes vs Total Votes
5. Average Review Length by Rating

The charts are interactive and support features such as hover information, zooming, and filtering.

---

## 📦 Product Analysis

The Product Analysis section focuses on product-level review behavior.

### Analysis Includes

* Top products by review count
* Top products by average rating
* Product ID search
* Product-based filtering

Users can enter a Product ID in the sidebar to analyze a specific product.

---

## 😊 Sentiment Analysis

Sentiment analysis is included to understand the emotional tone of customer reviews.

The project uses sentiment results generated from customer review text.

### Sentiment Categories

Reviews can be classified into:

* Positive
* Neutral
* Negative

The dashboard displays:

* Sentiment distribution
* Sentiment counts
* Sentiment visualization

Sentiment results are loaded from:

```text
sentiment_results/sentiment_results.csv
```

---

## 🧹 Data Quality Analysis

The Data Quality section evaluates the reliability and consistency of the dataset.

### Rating Quality

The dashboard checks:

* Valid Ratings
* Invalid Ratings
* Average Rating

### Helpfulness Data Quality

The dashboard checks:

* Negative Helpfulness Numerator
* Negative Helpfulness Denominator
* Helpfulness Numerator greater than Denominator

### General Data Quality

The dashboard checks:

* Missing Values
* Duplicate Rows
* Total Columns

A detailed column-quality report is also provided.

---

## 🎛️ Interactive Filters

The dashboard provides several filters through the sidebar.

### Available Filters

* Product ID Search
* Rating
* Year

All dashboard analysis updates according to the selected filters.

Users can also download the filtered dataset as a CSV file.

---

## 🗃️ Dataset

The project uses the **Amazon Fine Food Reviews dataset**.

The dataset contains information such as:

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

The original dataset contains approximately **568,454 customer reviews**.

The dataset is stored locally in SQLite format.

> The complete database file is not included in the GitHub repository because of its large file size.

---

## 🧹 Data Processing

The application performs several data-processing steps before analysis.

### Processing Steps

1. Load review data from SQLite.
2. Detect relevant dataset columns.
3. Convert ratings to numeric values.
4. Convert review timestamps into readable dates.
5. Extract review years.
6. Calculate helpfulness ratios.
7. Calculate review length.
8. Handle missing numeric values.
9. Detect duplicate records.
10. Perform data-quality checks.

---

## 📊 Key Analytical Questions

The dashboard helps answer questions such as:

* What is the average customer rating?
* How are ratings distributed?
* How has review activity changed over time?
* Which products receive the most reviews?
* Which products have high average ratings?
* How helpful are customer reviews?
* Does review length vary by rating?
* Are there invalid ratings?
* Are there duplicate records?
* What is the sentiment distribution?
* How can the quality of the review data be assessed?

---

## 📁 Project Structure

```text
Amazon_Reviews_Project/
│
├── app.py
├── analysis.py
├── visualization.py
├── sentiment.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── Reviews.sqlite/
│       └── Reviews.sqlite
│
└── sentiment_results/
    └── sentiment_results.csv
```

---

## 🛠️ Technologies Used

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Application and data processing   |
| Streamlit  | Interactive dashboard             |
| Pandas     | Data cleaning and analysis        |
| NumPy      | Numerical operations              |
| SQLite     | Data storage and database loading |
| Plotly     | Interactive visualizations        |
| NLTK       | Natural Language Processing       |
| VADER      | Sentiment Analysis                |

---

## ▶️ How to Run the Dashboard

### 1. Clone the Repository

```bash
git clone https://github.com/luqman-farooq/CodeAlpha_Amazon_Reviews_Data_Analytics.git
```

### 2. Open the Project Folder

```bash
cd CodeAlpha_Amazon_Reviews_Data_Analytics
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

Alternatively:

```bash
python -m streamlit run app.py
```

The Streamlit application will open in the browser.

---

## 📥 Download Filtered Data

The dashboard provides a **Download Filtered CSV** feature.

Users can:

1. Search for a Product ID.
2. Select specific ratings.
3. Select specific years.
4. Apply the filters.
5. Download the filtered dataset as a CSV file.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Understand the structure of Amazon customer review data.
2. Perform exploratory data analysis.
3. Analyze customer rating patterns.
4. Identify review activity trends.
5. Analyze product-level review behavior.
6. Analyze review helpfulness.
7. Study review length.
8. Perform sentiment analysis.
9. Identify potential data-quality issues.
10. Create interactive data visualizations.
11. Build a user-friendly analytics dashboard.
12. Gain practical experience working with a large real-world dataset.

---

## 📌 Internship Tasks

This project was completed as part of the:

**CodeAlpha Data Analytics Internship**

### Completed Tasks

* **Task 2 — Exploratory Data Analysis**
* **Task 3 — Data Visualization**
* **Task 4 — Sentiment Analysis**

The final project combines these tasks into an interactive Streamlit analytics dashboard.

---

## 💡 Key Insights

The exploratory analysis identified several important patterns in the dataset:

* The dataset contains approximately **568,454 reviews**.
* The average customer rating is approximately **4.18 / 5**.
* 5-star reviews form the largest rating category.
* 4- and 5-star reviews represent the majority of the dataset.
* Review activity increased significantly during the later years covered by the dataset.
* Product-level review counts vary considerably.
* Helpfulness information can be used to understand customer interaction with reviews.
* Data-quality checks can identify unusual helpfulness records.
* Customer review text can be analyzed to identify sentiment.

> Dashboard metrics may change when filters are applied because the dashboard recalculates the analysis for the selected data.

---

## 🔮 Future Improvements

Possible future enhancements include:

* Advanced NLP analysis
* Word cloud visualization
* Topic modeling
* Review keyword analysis
* Product category analysis
* Monthly review trends
* Advanced sentiment classification
* Sentiment vs rating analysis inside the dashboard
* Additional product KPIs
* Streamlit Cloud deployment
* Automated dashboard reporting

---

## 🧑‍💻 Author

**Luqman Farooq**

Amazon Reviews Data Analytics Project

**CodeAlpha Data Analytics Internship**

---

## 🏁 Conclusion

This project demonstrates a complete data analytics workflow using a large real-world Amazon Reviews dataset.

The project combines:

```text
Data Loading
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Data Quality Analysis
      ↓
Data Visualization
      ↓
Product Analysis
      ↓
Sentiment Analysis
      ↓
Interactive Streamlit Dashboard
```

The final dashboard provides an interactive way to explore customer ratings, review activity, product performance, review helpfulness, sentiment, and overall data quality.

The project provided practical experience with **Python, Pandas, NumPy, SQLite, Plotly, Streamlit, NLTK, and VADER sentiment analysis**.

---

## ⭐ Project Repository

**Repository Name:** `CodeAlpha_Amazon_Reviews_Data_Analytics`

**Project Type:** Data Analytics / NLP / Interactive Dashboard

**Internship:** CodeAlpha Data Analytics Internship

````
