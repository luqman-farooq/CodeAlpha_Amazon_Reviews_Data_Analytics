import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Amazon Reviews Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PATHS
# =========================================================

DB_PATH = Path("data/Reviews.sqlite/Reviews.sqlite")
SENTIMENT_PATH = Path("sentiment_results/sentiment_results.csv")


# =========================================================
# LIGHT THEME CSS
# =========================================================

st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */

.stApp {
    background-color: #f5f7fb;
    color: #1e293b;
}

.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

section[data-testid="stSidebar"] .stRadio label {
    font-weight: 600;
}


/* ================================
   HEADINGS
================================ */

h1 {
    color: #0f172a !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #1e293b !important;
}


/* ================================
   SEARCH BOX
================================ */

.search-title {
    color: #334155;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 9px !important;
    padding: 11px !important;
    font-size: 14px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 1px #f59e0b !important;
}


/* ================================
   KPI CARDS
================================ */

.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px;
    min-height: 135px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
}

.kpi-title {
    color: #64748b;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 9px;
}

.kpi-value {
    color: #0f172a;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.1;
}

.kpi-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}


/* ================================
   EDA CARDS
================================ */

.eda-metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 18px;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
}

.eda-metric-label {
    color: #64748b;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.eda-metric-value {
    color: #0f172a;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
}


/* ================================
   QUALITY CARDS
================================ */

.quality-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 18px;
    min-height: 145px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
}

.quality-label {
    color: #64748b;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
}

.quality-value {
    color: #0f172a;
    font-size: 32px;
    font-weight: 800;
    line-height: 1.1;
}

.quality-note {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}


/* ================================
   SECTION TITLES
================================ */

.section-title {
    color: #0f172a;
    font-size: 22px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 16px;
}


/* ================================
   DATAFRAME
================================ */

div[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}


/* ================================
   DOWNLOAD BUTTON
================================ */

.stDownloadButton button {
    background-color: #f59e0b !important;
    color: #111827 !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}


/* ================================
   INFO
================================ */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* ================================
   FOOTER
================================ */

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 45px;
    padding: 20px;
    border-top: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTION
# =========================================================

def find_column(df, candidates):

    for col in candidates:
        if col in df.columns:
            return col

    lower_map = {
        str(c).lower(): c
        for c in df.columns
    }

    for col in candidates:
        if col.lower() in lower_map:
            return lower_map[col.lower()]

    return None


# =========================================================
# LOAD SQLITE DATA
# =========================================================

@st.cache_data
def load_data():

    if not DB_PATH.exists():
        st.error(
            f"Database not found:\n{DB_PATH}"
        )
        st.stop()

    conn = sqlite3.connect(DB_PATH)

    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table'",
        conn
    )

    if tables.empty:
        conn.close()
        st.error("No table found in SQLite database.")
        st.stop()

    table_name = tables.iloc[0]["name"]

    df = pd.read_sql_query(
        f'SELECT * FROM "{table_name}"',
        conn
    )

    conn.close()

    return df


df = load_data()


# =========================================================
# COLUMN DETECTION
# =========================================================

rating_col = find_column(
    df,
    [
        "Score",
        "score",
        "Rating",
        "rating",
        "Overall",
        "overall"
    ]
)

date_col = find_column(
    df,
    [
        "Time",
        "time",
        "ReviewDate",
        "review_date",
        "Date",
        "date",
        "reviewTime"
    ]
)

product_col = find_column(
    df,
    [
        "ProductId",
        "ProductID",
        "product_id",
        "asin",
        "ASIN"
    ]
)

review_col = find_column(
    df,
    [
        "Text",
        "text",
        "Review",
        "review",
        "ReviewText",
        "reviewText"
    ]
)

summary_col = find_column(
    df,
    [
        "Summary",
        "summary"
    ]
)

helpful_num_col = find_column(
    df,
    [
        "HelpfulnessNumerator",
        "helpful_yes",
        "helpfulness_numerator"
    ]
)

helpful_den_col = find_column(
    df,
    [
        "HelpfulnessDenominator",
        "helpful_total",
        "helpfulness_denominator"
    ]
)

user_col = find_column(
    df,
    [
        "UserId",
        "UserID",
        "user_id"
    ]
)


# =========================================================
# DATA CLEANING
# =========================================================

if rating_col:

    df[rating_col] = pd.to_numeric(
        df[rating_col],
        errors="coerce"
    )


if date_col:

    if str(date_col).lower() == "time":

        df["ParsedDate"] = pd.to_datetime(
            df[date_col],
            unit="s",
            errors="coerce"
        )

    else:

        df["ParsedDate"] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    df["Year"] = df["ParsedDate"].dt.year

else:

    df["Year"] = np.nan


if helpful_num_col:

    df[helpful_num_col] = pd.to_numeric(
        df[helpful_num_col],
        errors="coerce"
    ).fillna(0)


if helpful_den_col:

    df[helpful_den_col] = pd.to_numeric(
        df[helpful_den_col],
        errors="coerce"
    ).fillna(0)


if helpful_num_col and helpful_den_col:

    df["HelpfulnessRatio"] = np.where(
        df[helpful_den_col] > 0,
        df[helpful_num_col] /
        df[helpful_den_col],
        0
    )

else:

    df["HelpfulnessRatio"] = 0


if review_col:

    df["ReviewLength"] = (
        df[review_col]
        .fillna("")
        .astype(str)
        .str.len()
    )

else:

    df["ReviewLength"] = 0


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛒 Amazon Reviews")

st.sidebar.caption(
    "Data Analytics Dashboard"
)

st.sidebar.markdown("---")


page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "EDA",
        "Visualizations",
        "Product Analysis",
        "Sentiment Analysis",
        "Data Quality"
    ]
)


st.sidebar.markdown("---")

st.sidebar.subheader("🔎 Filters")


# =========================================================
# SEARCH
# =========================================================

st.sidebar.markdown(
    '<div class="search-title">🔎 Search Product ID</div>',
    unsafe_allow_html=True
)

product_search = st.sidebar.text_input(
    "Product Search",
    placeholder="Enter Product ID...",
    label_visibility="collapsed"
)


# =========================================================
# RATING FILTER
# =========================================================

if rating_col:

    valid_ratings = sorted(
        df[rating_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_ratings = st.sidebar.multiselect(
        "⭐ Rating",
        options=valid_ratings,
        default=valid_ratings
    )

else:

    selected_ratings = []


# =========================================================
# YEAR FILTER
# =========================================================

if "Year" in df.columns:

    valid_years = sorted(
        df["Year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    selected_years = st.sidebar.multiselect(
        "📅 Year",
        options=valid_years,
        default=valid_years
    )

else:

    selected_years = []


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if rating_col and selected_ratings:

    filtered_df = filtered_df[
        filtered_df[rating_col].isin(
            selected_ratings
        )
    ]


if "Year" in filtered_df.columns and selected_years:

    filtered_df = filtered_df[
        filtered_df["Year"].isin(
            selected_years
        )
    ]


if product_search and product_col:

    filtered_df = filtered_df[
        filtered_df[product_col]
        .astype(str)
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]


# =========================================================
# DOWNLOAD
# =========================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.sidebar.download_button(
    "⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="amazon_reviews_filtered.csv",
    mime="text/csv"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    f"Showing {len(filtered_df):,} records"
)


# =========================================================
# COMMON CHART SETTINGS
# =========================================================

def style_chart(fig):

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            color="#334155"
        ),
        title_font=dict(
            color="#0f172a",
            size=18
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e2e8f0"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e2e8f0"
    )

    return fig


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.title("🛒 Amazon Reviews Analytics Dashboard")

    st.write(
        "Interactive analytics dashboard for Amazon product reviews."
    )

    st.markdown("---")


    # ---------------- KPI CALCULATIONS ----------------

    total_reviews = len(filtered_df)

    if rating_col:
        avg_rating = filtered_df[rating_col].mean()
    else:
        avg_rating = 0

    avg_review_length = (
        filtered_df["ReviewLength"].mean()
    )

    if helpful_num_col and helpful_den_col:

        total_num = filtered_df[
            helpful_num_col
        ].sum()

        total_den = filtered_df[
            helpful_den_col
        ].sum()

        helpfulness = (
            total_num /
            total_den *
            100
            if total_den > 0
            else 0
        )

    else:

        helpfulness = 0


    # ---------------- KPI CARDS ----------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    📊 Total Reviews
                </div>
                <div class="kpi-value">
                    {total_reviews:,}
                </div>
                <div class="kpi-subtitle">
                    Filtered records
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    ⭐ Average Rating
                </div>
                <div class="kpi-value">
                    {avg_rating:.2f}/5
                </div>
                <div class="kpi-subtitle">
                    Average customer score
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    📝 Review Length
                </div>
                <div class="kpi-value">
                    {avg_review_length:.0f}
                </div>
                <div class="kpi-subtitle">
                    Average characters
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    👍 Helpfulness
                </div>
                <div class="kpi-value">
                    {helpfulness:.2f}%
                </div>
                <div class="kpi-subtitle">
                    Helpful vote ratio
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # OVERVIEW CHARTS
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Review Overview</div>',
        unsafe_allow_html=True
    )


    chart1, chart2 = st.columns(2)


    # ---------------- RATING DISTRIBUTION ----------------

    with chart1:

        if rating_col:

            rating_counts = (
                filtered_df[rating_col]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            rating_counts.columns = [
                "Rating",
                "Reviews"
            ]

            fig = px.bar(
                rating_counts,
                x="Rating",
                y="Reviews",
                text="Reviews",
                title="⭐ Reviews by Rating"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # ---------------- RATING PIE ----------------

    with chart2:

        if rating_col:

            pie_data = (
                filtered_df[rating_col]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            pie_data.columns = [
                "Rating",
                "Reviews"
            ]

            fig = px.pie(
                pie_data,
                names="Rating",
                values="Reviews",
                hole=0.45,
                title="🥧 Rating Share"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # =====================================================
    # YEAR TREND
    # =====================================================

    if "Year" in filtered_df.columns:

        year_data = (
            filtered_df
            .dropna(subset=["Year"])
            .groupby("Year")
            .size()
            .reset_index(name="Reviews")
        )

        year_data["Year"] = (
            year_data["Year"]
            .astype(int)
        )

        if len(year_data) > 1:

            fig = px.line(
                year_data,
                x="Year",
                y="Reviews",
                markers=True,
                title="📅 Reviews Trend by Year"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


# =========================================================
# EDA
# =========================================================

elif page == "EDA":

    st.title("📊 Exploratory Data Analysis")

    st.write(
        "Basic structure and quality overview of the dataset."
    )

    st.markdown("---")


    # ---------------- EDA CARDS ----------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="eda-metric-card">
                <div class="eda-metric-label">
                    📊 Rows
                </div>
                <div class="eda-metric-value">
                    {len(filtered_df):,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="eda-metric-card">
                <div class="eda-metric-label">
                    📋 Columns
                </div>
                <div class="eda-metric-value">
                    {len(filtered_df.columns):,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="eda-metric-card">
                <div class="eda-metric-label">
                    ⚠️ Missing Values
                </div>
                <div class="eda-metric-value">
                    {filtered_df.isna().sum().sum():,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="eda-metric-card">
                <div class="eda-metric-label">
                    🔄 Duplicate Rows
                </div>
                <div class="eda-metric-value">
                    {filtered_df.duplicated().sum():,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("---")


    # =====================================================
    # REVIEW LENGTH CHART
    # =====================================================

    if "ReviewLength" in filtered_df.columns:

        st.subheader("📝 Review Length Distribution")

        length_data = filtered_df[
            "ReviewLength"
        ].clip(upper=2000)

        fig = px.histogram(
            length_data,
            nbins=40,
            title="Distribution of Review Length"
        )

        fig.update_layout(
            xaxis_title="Review Length (characters)",
            yaxis_title="Number of Reviews"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


    # =====================================================
    # DATA PREVIEW
    # =====================================================

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )


    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.subheader("📌 Column Information")

    column_info = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": [
            str(filtered_df[c].dtype)
            for c in filtered_df.columns
        ],
        "Missing Values": [
            filtered_df[c].isna().sum()
            for c in filtered_df.columns
        ],
        "Unique Values": [
            filtered_df[c].nunique()
            for c in filtered_df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


# =========================================================
# VISUALIZATIONS
# =========================================================

elif page == "Visualizations":

    st.title("📈 Advanced Visualizations")

    st.write(
        "Detailed charts for ratings, time trends, helpfulness and review behavior."
    )

    st.markdown("---")


    # =====================================================
    # RATING + YEAR
    # =====================================================

    c1, c2 = st.columns(2)


    with c1:

        if rating_col:

            rating_counts = (
                filtered_df[rating_col]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            rating_counts.columns = [
                "Rating",
                "Reviews"
            ]

            fig = px.bar(
                rating_counts,
                x="Rating",
                y="Reviews",
                text="Reviews",
                title="⭐ Rating Distribution"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    with c2:

        if "Year" in filtered_df.columns:

            year_data = (
                filtered_df
                .dropna(subset=["Year"])
                .groupby("Year")
                .size()
                .reset_index(name="Reviews")
            )

            year_data["Year"] = (
                year_data["Year"]
                .astype(int)
            )

            fig = px.line(
                year_data,
                x="Year",
                y="Reviews",
                markers=True,
                title="📅 Reviews Over Time"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # =====================================================
    # AVERAGE RATING BY YEAR
    # =====================================================

    if rating_col and "Year" in filtered_df.columns:

        rating_year = (
            filtered_df
            .dropna(subset=["Year", rating_col])
            .groupby("Year")[rating_col]
            .mean()
            .reset_index()
        )

        rating_year["Year"] = (
            rating_year["Year"]
            .astype(int)
        )

        fig = px.line(
            rating_year,
            x="Year",
            y=rating_col,
            markers=True,
            title="⭐ Average Rating by Year"
        )

        fig.update_layout(
            yaxis_title="Average Rating",
            xaxis_title="Year"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


    # =====================================================
    # HELPFULNESS
    # =====================================================

    if helpful_num_col and helpful_den_col:

        st.subheader("👍 Helpfulness Analysis")

        helpful_sample = filtered_df[
            [
                helpful_num_col,
                helpful_den_col
            ]
        ].copy()

        helpful_sample.columns = [
            "Helpful Votes",
            "Total Votes"
        ]

        helpful_sample = helpful_sample[
            helpful_sample["Total Votes"] > 0
        ]

        if len(helpful_sample) > 0:

            helpful_sample = helpful_sample.sample(
                min(
                    5000,
                    len(helpful_sample)
                ),
                random_state=42
            )

            fig = px.scatter(
                helpful_sample,
                x="Total Votes",
                y="Helpful Votes",
                title="👍 Helpful Votes vs Total Votes",
                opacity=0.6
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # =====================================================
    # REVIEW LENGTH BY RATING
    # =====================================================

    if rating_col:

        length_rating = (
            filtered_df
            .groupby(rating_col)["ReviewLength"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            length_rating,
            x=rating_col,
            y="ReviewLength",
            text_auto=".0f",
            title="📝 Average Review Length by Rating"
        )

        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Average Review Length"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

elif page == "Product Analysis":

    st.title("🛍️ Product Analysis")

    st.write(
        "Product-level review and rating analysis."
    )

    st.markdown("---")


    if product_col:

        if rating_col:

            product_summary = (
                filtered_df
                .groupby(product_col)
                .agg(
                    Reviews=(product_col, "size"),
                    Average_Rating=(
                        rating_col,
                        "mean"
                    )
                )
                .sort_values(
                    "Reviews",
                    ascending=False
                )
                .head(20)
                .reset_index()
            )

        else:

            product_summary = (
                filtered_df
                .groupby(product_col)
                .size()
                .reset_index(
                    name="Reviews"
                )
                .sort_values(
                    "Reviews",
                    ascending=False
                )
                .head(20)
            )


        st.subheader(
            "🔥 Top Products by Review Count"
        )

        st.dataframe(
            product_summary,
            use_container_width=True
        )


        # ---------------- TOP PRODUCTS ----------------

        fig = px.bar(
            product_summary.head(10),
            x="Reviews",
            y=product_col,
            orientation="h",
            title="🏆 Top 10 Products"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


        # ---------------- PRODUCT RATING ----------------

        if rating_col:

            rating_products = (
                product_summary
                .sort_values(
                    "Average_Rating",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                rating_products,
                x="Average_Rating",
                y=product_col,
                orientation="h",
                title="⭐ Top Products by Average Rating"
            )

            fig.update_layout(
                xaxis_title="Average Rating"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    else:

        st.warning(
            "Product ID column was not found."
        )


# =========================================================
# SENTIMENT ANALYSIS
# =========================================================

elif page == "Sentiment Analysis":

    st.title("😊 Sentiment Analysis")

    st.write(
        "Sentiment distribution from the generated sentiment results."
    )

    st.markdown("---")


    if SENTIMENT_PATH.exists():

        sentiment_df = pd.read_csv(
            SENTIMENT_PATH
        )

        st.subheader(
            "📋 Sentiment Results"
        )

        st.dataframe(
            sentiment_df.head(100),
            use_container_width=True
        )


        sentiment_col = find_column(
            sentiment_df,
            [
                "sentiment",
                "Sentiment",
                "label",
                "Label"
            ]
        )


        if sentiment_col:

            sentiment_counts = (
                sentiment_df[
                    sentiment_col
                ]
                .value_counts()
                .reset_index()
            )

            sentiment_counts.columns = [
                "Sentiment",
                "Count"
            ]


            c1, c2 = st.columns(2)


            with c1:

                fig = px.pie(
                    sentiment_counts,
                    names="Sentiment",
                    values="Count",
                    hole=0.45,
                    title="😊 Sentiment Distribution"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True
                )


            with c2:

                fig = px.bar(
                    sentiment_counts,
                    x="Sentiment",
                    y="Count",
                    text="Count",
                    title="📊 Sentiment Counts"
                )

                fig.update_traces(
                    textposition="outside"
                )

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True
                )


        else:

            st.warning(
                "Sentiment column was not found."
            )


    else:

        st.warning(
            "sentiment_results.csv was not found."
        )

        st.info(
            "Place sentiment_results.csv inside "
            "the sentiment_results folder."
        )


# =========================================================
# DATA QUALITY
# =========================================================

elif page == "Data Quality":

    st.title("🧹 Data Quality")

    st.write(
        "Validation checks for ratings, helpfulness values, "
        "missing data and duplicate records."
    )

    st.markdown("---")


    # =====================================================
    # RATING QUALITY
    # =====================================================

    st.markdown(
        '<div class="section-title">⭐ Rating Quality</div>',
        unsafe_allow_html=True
    )


    if rating_col:

        valid_ratings_df = filtered_df[
            filtered_df[rating_col].between(
                1,
                5,
                inclusive="both"
            )
        ]

        valid_rating_count = len(
            valid_ratings_df
        )

        invalid_rating_count = (
            len(filtered_df)
            -
            valid_rating_count
        )

        average_rating = (
            filtered_df[rating_col].mean()
        )


        r1, r2, r3 = st.columns(3)


        with r1:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Valid Ratings
                    </div>
                    <div class="quality-value">
                        {valid_rating_count:,}
                    </div>
                    <div class="quality-note">
                        Ratings between 1 and 5
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with r2:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Invalid Ratings
                    </div>
                    <div class="quality-value">
                        {invalid_rating_count:,}
                    </div>
                    <div class="quality-note">
                        Outside valid range
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with r3:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Average Rating
                    </div>
                    <div class="quality-value">
                        {average_rating:.2f}
                    </div>
                    <div class="quality-note">
                        Average score out of 5
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    else:

        st.warning(
            "Rating column not found."
        )


    # =====================================================
    # HELPFULNESS QUALITY
    # =====================================================

    st.markdown(
        '<div class="section-title">👍 Helpfulness Data Quality</div>',
        unsafe_allow_html=True
    )


    if helpful_num_col and helpful_den_col:

        negative_numerator = (
            filtered_df[helpful_num_col] < 0
        ).sum()

        negative_denominator = (
            filtered_df[helpful_den_col] < 0
        ).sum()

        numerator_greater_denominator = (
            filtered_df[helpful_num_col]
            >
            filtered_df[helpful_den_col]
        ).sum()


        h1, h2, h3 = st.columns(3)


        with h1:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Negative Numerator
                    </div>
                    <div class="quality-value">
                        {negative_numerator:,}
                    </div>
                    <div class="quality-note">
                        Numerator values below zero
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with h2:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Negative Denominator
                    </div>
                    <div class="quality-value">
                        {negative_denominator:,}
                    </div>
                    <div class="quality-note">
                        Denominator values below zero
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with h3:

            st.markdown(
                f"""
                <div class="quality-card">
                    <div class="quality-label">
                        Numerator &gt; Denominator
                    </div>
                    <div class="quality-value">
                        {numerator_greater_denominator:,}
                    </div>
                    <div class="quality-note">
                        Logically inconsistent records
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    else:

        st.warning(
            "Helpfulness columns were not found."
        )


    # =====================================================
    # GENERAL QUALITY
    # =====================================================

    st.markdown(
        '<div class="section-title">🔍 General Data Quality</div>',
        unsafe_allow_html=True
    )


    q1, q2, q3 = st.columns(3)


    with q1:

        missing_values = (
            filtered_df.isna().sum().sum()
        )

        st.markdown(
            f"""
            <div class="quality-card">
                <div class="quality-label">
                    Missing Values
                </div>
                <div class="quality-value">
                    {missing_values:,}
                </div>
                <div class="quality-note">
                    Total missing cells
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with q2:

        duplicate_rows = (
            filtered_df.duplicated().sum()
        )

        st.markdown(
            f"""
            <div class="quality-card">
                <div class="quality-label">
                    Duplicate Rows
                </div>
                <div class="quality-value">
                    {duplicate_rows:,}
                </div>
                <div class="quality-note">
                    Duplicate records
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with q3:

        st.markdown(
            f"""
            <div class="quality-card">
                <div class="quality-label">
                    Total Columns
                </div>
                <div class="quality-value">
                    {len(filtered_df.columns):,}
                </div>
                <div class="quality-note">
                    Dataset attributes
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # QUALITY REPORT
    # =====================================================

    st.markdown(
        '<div class="section-title">📋 Column Quality Report</div>',
        unsafe_allow_html=True
    )


    quality_report = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": [
            str(filtered_df[c].dtype)
            for c in filtered_df.columns
        ],
        "Missing Values": [
            filtered_df[c].isna().sum()
            for c in filtered_df.columns
        ],
        "Unique Values": [
            filtered_df[c].nunique()
            for c in filtered_df.columns
        ]
    })


    st.dataframe(
        quality_report,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🛒 Amazon Reviews Data Analytics Dashboard
        • CodeAlpha Data Analytics Internship
    </div>
    """,
    unsafe_allow_html=True
)