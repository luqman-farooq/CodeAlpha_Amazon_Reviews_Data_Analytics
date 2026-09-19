\# Amazon Reviews Data Analytics



\## Project Overview



This project was developed as part of the \*\*CodeAlpha Data Analytics Internship\*\*. The project analyzes a large Amazon Reviews dataset to discover patterns in customer ratings, review behavior, product performance, helpfulness, and sentiment.



The project focuses on three data analytics tasks:



\* \*\*Task 2 — Exploratory Data Analysis (EDA)\*\*

\* \*\*Task 3 — Data Visualization\*\*

\* \*\*Task 4 — Sentiment Analysis\*\*



\## Dataset



The dataset contains \*\*568,454 Amazon reviews\*\* with 10 columns:



\* `Id`

\* `ProductId`

\* `UserId`

\* `ProfileName`

\* `HelpfulnessNumerator`

\* `HelpfulnessDenominator`

\* `Score`

\* `Time`

\* `Summary`

\* `Text`



The dataset is stored locally in SQLite format.



> The original dataset is not included in this repository because of its large file size.



\## Task 2 — Exploratory Data Analysis



The EDA analyzes the structure and quality of the dataset.



\### Analysis Performed



\* Dataset dimensions and column information

\* Missing value analysis

\* Duplicate record analysis

\* Statistical summary

\* Rating distribution

\* Average rating

\* Review length analysis

\* Helpfulness ratio

\* Reviews by year

\* Most-reviewed products

\* Product average ratings

\* Low-rating and high-rating review percentages

\* Basic anomaly checks



\### Main Script



```text

analysis.py

```



\## Task 3 — Data Visualization



Several visualizations were created to make the findings easier to understand.



\### Visualizations



\* Rating Distribution

\* Rating Percentage

\* Reviews Over Time

\* Average Rating Over Time

\* Top 10 Products by Review Count

\* Review Length Distribution

\* Helpfulness by Rating



All visualization outputs are stored in:



```text

charts/

```



\### Main Script



```text

visualization.py

```



\## Task 4 — Sentiment Analysis



Sentiment analysis was performed using \*\*NLTK VADER (Valence Aware Dictionary and sEntiment Reasoner)\*\*.



The review summary and review text were combined and analyzed to calculate a sentiment score.



Reviews were classified into:



\* Positive

\* Neutral

\* Negative



The analysis also compares sentiment with the corresponding star rating.



\### Sentiment Outputs



The following files are generated:



```text

sentiment\_results/

├── sentiment\_distribution.png

├── sentiment\_percentage.png

├── sentiment\_vs\_rating.png

├── sentiment\_results.csv

└── sentiment\_summary.csv

```



\### Main Script



```text

sentiment.py

```



\## Technologies Used



\* Python

\* Pandas

\* Matplotlib

\* SQLite

\* NLTK

\* VADER Sentiment Analysis

\* Jupyter Notebook / Python environment



\## Project Structure



```text

Amazon\_Reviews\_Project/

│

├── analysis.py

├── visualization.py

├── sentiment.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── charts/

│   ├── rating\_distribution.png

│   ├── rating\_percentage.png

│   ├── reviews\_over\_time.png

│   ├── average\_rating\_over\_time.png

│   ├── top\_10\_products.png

│   ├── review\_length\_distribution.png

│   └── helpfulness\_by\_rating.png

│

├── sentiment\_results/

│   ├── sentiment\_distribution.png

│   ├── sentiment\_percentage.png

│   ├── sentiment\_vs\_rating.png

│   └── sentiment\_summary.csv

│

├── notebooks/

│

└── data/

&#x20;   └── Amazon Reviews Dataset

```



\## How to Run



\### 1. Install dependencies



```bash

pip install -r requirements.txt

```



\### 2. Run Exploratory Data Analysis



```bash

python analysis.py

```



\### 3. Generate Visualizations



```bash

python visualization.py

```



\### 4. Run Sentiment Analysis



```bash

python sentiment.py

```



\## Key Objectives



The main objectives of this project are:



1\. Understand the structure and quality of Amazon review data.

2\. Identify patterns in customer ratings and review activity.

3\. Analyze product-level review behavior.

4\. Visualize important trends and distributions.

5\. Analyze customer sentiment using NLP techniques.

6\. Compare sentiment patterns with star ratings.



\## Conclusion



This project demonstrates a complete data analytics workflow using a large real-world review dataset. It combines data cleaning, exploratory analysis, visualization, and natural language processing to extract meaningful information from customer reviews.



The project provides practical experience with \*\*Python, Pandas, Matplotlib, SQLite, and NLP-based sentiment analysis\*\*.



