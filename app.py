import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Caterlytics",
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

BASE = Path(__file__).resolve().parent

CLEAN = pd.read_csv(
    BASE / "data" / "catering_orders_cleaned.csv",
    parse_dates=["order_date"]
)

BAL = pd.read_csv(
    BASE / "data" / "catering_orders_balanced.csv",
    parse_dates=["order_date"]
)

RAW = pd.read_csv(
    BASE / "data" / "catering_orders_raw.csv"
)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("🍽️ Caterlytics")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Load & Understand Data",
        "Clean Data",
        "Balance Data",
        "Visualize & Analyze"
    ]
)

# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.title("🍽️ Caterlytics")

    st.subheader("Catering Orders — Data Wrangling & Analysis")

    st.write(
        "A Streamlit mini-project demonstrating data loading, inspection, "
        "cleaning, class balancing, visualization, and business-oriented "
        "insights from a catering-order dataset."
    )

    # -----------------------------------------------------
    # PROJECT METRICS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Raw Records",
        len(RAW)
    )

    c2.metric(
        "Clean Records",
        len(CLEAN)
    )

    c3.metric(
        "Clients",
        CLEAN["client_id"].nunique()
    )

    c4.metric(
        "Total Catering Cost",
        f"₹{CLEAN['total_cost'].sum():,.2f}"
    )

    # -----------------------------------------------------
    # WORKFLOW
    # -----------------------------------------------------

    st.markdown("### Project Workflow")

    st.markdown(
        """
        1. **Load & Understand Data** — inspect structure, data types,
           missing values, duplicates and descriptive statistics.

        2. **Clean Data** — standardize fields, parse dates, validate
           costs/statuses and create useful date features.

        3. **Balance Data** — use random oversampling on fulfillment
           status for balanced analytical/modeling data.

        4. **Visualize & Analyze** — study fulfillment status, clients,
           catering costs, time trends and operational patterns.
        """
    )

    st.info(
        "Dataset scope: 150 catering orders, 19 clients, 4 fulfillment "
        "statuses, with order dates from 2020–2024."
    )


# =========================================================
# LOAD & UNDERSTAND DATA
# =========================================================

elif page == "Load & Understand Data":

    st.title("📥 Load & Understand Data")

    st.write(
        "This stage examines the original catering-order dataset before "
        "the cleaning process. It helps identify the structure, quality "
        "and characteristics of the data."
    )

    # -----------------------------------------------------
    # FIRST 5 RECORDS
    # -----------------------------------------------------

    st.markdown("### First 5 Records")

    st.dataframe(
        RAW.head(),
        use_container_width=True
    )

    # -----------------------------------------------------
    # BASIC DATASET METRICS
    # -----------------------------------------------------

    a, b, c, d = st.columns(4)

    a.metric(
        "Rows",
        RAW.shape[0]
    )

    b.metric(
        "Columns",
        RAW.shape[1]
    )

    c.metric(
        "Missing Cells",
        int(RAW.isna().sum().sum())
    )

    d.metric(
        "Duplicate Rows",
        int(RAW.duplicated().sum())
    )

    # -----------------------------------------------------
    # COLUMN NAMES
    # -----------------------------------------------------

    st.markdown("### Column Names")

    st.write(
        list(RAW.columns)
    )

    # -----------------------------------------------------
    # DATA TYPES
    # -----------------------------------------------------

    st.markdown("### Data Types")

    dtype_df = pd.DataFrame({
        "Column": RAW.columns,
        "Data Type": RAW.dtypes.astype(str).values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # MISSING VALUE SUMMARY
    # -----------------------------------------------------

    st.markdown("### Missing-Value Summary")

    miss = pd.DataFrame({
        "Missing Values": RAW.isna().sum(),
        "Missing %": (
            RAW.isna().mean() * 100
        ).round(2)
    })

    st.dataframe(
        miss,
        use_container_width=True
    )

    # -----------------------------------------------------
    # DUPLICATE SUMMARY
    # -----------------------------------------------------

    st.markdown("### Duplicate-Record Summary")

    duplicate_count = int(
        RAW.duplicated().sum()
    )

    if duplicate_count == 0:
        st.success(
            "No exact duplicate records were found in the raw dataset."
        )
    else:
        st.warning(
            f"{duplicate_count} duplicate records were identified."
        )

    # -----------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # -----------------------------------------------------

    st.markdown("### Descriptive Statistics")

    st.write(
        "Descriptive statistics are presented separately for numerical, "
        "categorical and date-related columns so that statistics that are "
        "not applicable to a column are not displayed as None."
    )

    # -----------------------------------------------------
    # NUMERICAL STATISTICS
    # -----------------------------------------------------

    st.markdown("#### Numerical Columns")

    numeric_columns = RAW.select_dtypes(
        include=np.number
    ).columns.tolist()

    if len(numeric_columns) > 0:

        numeric_stats = RAW[numeric_columns].describe().transpose()

        numeric_stats = numeric_stats.rename(
            columns={
                "count": "Count",
                "mean": "Mean",
                "std": "Std. Dev.",
                "min": "Minimum",
                "25%": "25%",
                "50%": "Median",
                "75%": "75%",
                "max": "Maximum"
            }
        )

        numeric_stats = numeric_stats.round(2)

        st.dataframe(
            numeric_stats,
            use_container_width=True
        )

    else:

        st.info(
            "No numerical columns were detected."
        )

    # -----------------------------------------------------
    # CATEGORICAL STATISTICS
    # -----------------------------------------------------

    st.markdown("#### Categorical Columns")

    categorical_columns = RAW.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if len(categorical_columns) > 0:

        categorical_data = []

        for column in categorical_columns:

            series = RAW[column]

            categorical_data.append({
                "Column": column,
                "Count": series.count(),
                "Unique Values": series.nunique(),
                "Most Frequent": (
                    series.mode().iloc[0]
                    if not series.mode().empty
                    else "N/A"
                ),
                "Frequency": (
                    series.value_counts().iloc[0]
                    if not series.value_counts().empty
                    else 0
                )
            })

        categorical_stats = pd.DataFrame(
            categorical_data
        )

        st.dataframe(
            categorical_stats,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No categorical columns were detected."
        )

    # -----------------------------------------------------
    # DATE INFORMATION
    # -----------------------------------------------------

    st.markdown("#### Date Information")

    if "order_date" in RAW.columns:

        date_series = pd.to_datetime(
            RAW["order_date"],
            errors="coerce"
        )

        date_info = pd.DataFrame({
            "Metric": [
                "Valid Dates",
                "Missing Dates",
                "Unique Dates",
                "Earliest Order Date",
                "Latest Order Date"
            ],
            "Value": [
                int(date_series.notna().sum()),
                int(date_series.isna().sum()),
                int(date_series.nunique()),
                (
                    date_series.min().strftime("%Y-%m-%d")
                    if date_series.notna().any()
                    else "N/A"
                ),
                (
                    date_series.max().strftime("%Y-%m-%d")
                    if date_series.notna().any()
                    else "N/A"
                )
            ]
        })

        st.dataframe(
            date_info,
            use_container_width=True,
            hide_index=True
        )

    # -----------------------------------------------------
    # DATA QUALITY OBSERVATION
    # -----------------------------------------------------

    st.markdown("### Data Quality Observation")

    st.info(
        "The raw catering dataset was inspected for missing values, "
        "duplicates, data types, categorical distributions, numerical "
        "statistics and date ranges before proceeding to the cleaning stage."
    )


# =========================================================
# CLEAN DATA
# =========================================================

elif page == "Clean Data":

    st.title("🧹 Clean Data")

    st.markdown("### Cleaning Actions")

    st.markdown(
        """
        - Standardized column names and text values.
        - Converted `order_id` to numeric.
        - Converted `order_date` to datetime.
        - Converted `total_cost` to numeric.
        - Removed exact duplicate rows if present.
        - Validated fulfillment statuses against the expected categories.
        - Checked for missing IDs, dates and costs.
        - Checked for non-positive catering costs.
        - Added `order_year`, `order_month`, `month_name`,
          `day_name` and `order_quarter` for analysis.
        """
    )

    # -----------------------------------------------------
    # CLEANING METRICS
    # -----------------------------------------------------

    a, b, c, d = st.columns(4)

    a.metric(
        "Raw Rows",
        len(RAW)
    )

    b.metric(
        "Clean Rows",
        len(CLEAN)
    )

    b.metric(
        "Clean Rows",
        len(CLEAN)
    )

    c.metric(
        "Exact Duplicates Removed",
        int(RAW.duplicated().sum())
    )

    d.metric(
        "Missing Cells After Cleaning",
        int(CLEAN.isna().sum().sum())
    )

    # -----------------------------------------------------
    # CLEANED DATA
    # -----------------------------------------------------

    st.markdown("### Cleaned Data")

    st.dataframe(
        CLEAN.head(20),
        use_container_width=True
    )

    # -----------------------------------------------------
    # DOWNLOAD CLEANED DATA
    # -----------------------------------------------------

    st.download_button(
        "⬇️ Download Cleaned CSV",
        CLEAN.to_csv(index=False).encode("utf-8"),
        "catering_orders_cleaned.csv",
        "text/csv"
    )


# =========================================================
# BALANCE DATA
# =========================================================

elif page == "Balance Data":

    st.title("⚖️ Balance Data")

    st.write(
        "The target used for balancing is `fulfillment_status`. "
        "The original distribution is intentionally preserved in the "
        "cleaned dataset. A separate balanced dataset is created using "
        "random oversampling so that each fulfillment status has the "
        "same number of records."
    )

    # -----------------------------------------------------
    # ORIGINAL DISTRIBUTION
    # -----------------------------------------------------

    before = (
        CLEAN["fulfillment_status"]
        .value_counts()
        .rename("Original")
    )

    # -----------------------------------------------------
    # BALANCED DISTRIBUTION
    # -----------------------------------------------------

    after = (
        BAL["fulfillment_status"]
        .value_counts()
        .rename("Balanced")
    )

    # -----------------------------------------------------
    # COMPARISON
    # -----------------------------------------------------

    comp = pd.concat(
        [before, after],
        axis=1
    ).fillna(0).astype(int)

    st.markdown("### Original vs Balanced Distribution")

    st.dataframe(
        comp,
        use_container_width=True
    )

    # -----------------------------------------------------
    # VISUAL COMPARISON
    # -----------------------------------------------------

    fig1 = px.bar(
        comp.reset_index().melt(
            id_vars="fulfillment_status",
            var_name="Dataset",
            value_name="Orders"
        ),
        x="fulfillment_status",
        y="Orders",
        color="Dataset",
        barmode="group",
        title="Fulfillment Status: Original vs Balanced"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # -----------------------------------------------------
    # BALANCING RESULT
    # -----------------------------------------------------

    st.success(
        f"Balanced dataset contains {len(BAL)} records."
    )

    st.info(
        "The balanced dataset contains an equal number of records for "
        "each fulfillment status. The original cleaned dataset should "
        "still be used when reporting the real-world distribution of "
        "catering orders."
    )

    # -----------------------------------------------------
    # DOWNLOAD BALANCED DATA
    # -----------------------------------------------------

    st.download_button(
        "⬇️ Download Balanced CSV",
        BAL.to_csv(index=False).encode("utf-8"),
        "catering_orders_balanced.csv",
        "text/csv"
    )


# =========================================================
# VISUALIZE & ANALYZE
# =========================================================

elif page == "Visualize & Analyze":

    st.title("📊 Visualize & Analyze")

    st.write(
        "This section presents visual and statistical analysis of the "
        "cleaned catering-order data."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Orders & Status",
            "Cost & Clients",
            "Time Trends"
        ]
    )

    # =====================================================
    # TAB 1 — ORDERS & STATUS
    # =====================================================

    with tab1:

        status = (
            CLEAN["fulfillment_status"]
            .value_counts()
            .reset_index()
        )

        status.columns = [
            "fulfillment_status",
            "orders"
        ]

        # Pie chart

        fig = px.pie(
            status,
            names="fulfillment_status",
            values="orders",
            hole=0.35,
            title="Fulfillment Status Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Bar chart

        fig2 = px.bar(
            status,
            x="fulfillment_status",
            y="orders",
            title="Orders by Fulfillment Status",
            text="orders"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.markdown(
            "**Observation:** Delivered is the largest fulfillment "
            "category, while Delayed is the smallest. This indicates "
            "that fulfillment outcomes are not equally distributed "
            "in the original dataset."
        )

    # =====================================================
    # TAB 2 — COST & CLIENTS
    # =====================================================

    with tab2:

        client = (
            CLEAN["client_id"]
            .value_counts()
            .reset_index()
        )

        client.columns = [
            "client_id",
            "orders"
        ]

        # Top clients

        fig = px.bar(
            client.head(10),
            x="client_id",
            y="orders",
            title="Top 10 Clients by Number of Orders",
            text="orders"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Average cost by status

        cost_status = (
            CLEAN
            .groupby(
                "fulfillment_status",
                as_index=False
            )["total_cost"]
            .mean()
            .sort_values(
                "total_cost",
                ascending=False
            )
        )

        fig2 = px.bar(
            cost_status,
            x="fulfillment_status",
            y="total_cost",
            title="Average Catering Cost by Fulfillment Status",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # Cost metrics

        c1, c2 = st.columns(2)

        c1.metric(
            "Average Order Cost",
            f"₹{CLEAN['total_cost'].mean():,.2f}"
        )

        c2.metric(
            "Median Order Cost",
            f"₹{CLEAN['total_cost'].median():,.2f}"
        )

    # =====================================================
    # TAB 3 — TIME TRENDS
    # =====================================================

    with tab3:

        yearly = (
            CLEAN
            .groupby("order_year")
            .agg(
                orders=("order_id", "count"),
                total_cost=("total_cost", "sum")
            )
            .reset_index()
        )

        # Orders by year

        fig = px.line(
            yearly,
            x="order_year",
            y="orders",
            markers=True,
            title="Orders by Year"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Cost by year

        fig2 = px.line(
            yearly,
            x="order_year",
            y="total_cost",
            markers=True,
            title="Total Catering Cost by Year"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # Monthly activity

        monthly = (
            CLEAN
            .groupby(
                ["order_year", "order_month"]
            )
            .size()
            .reset_index(
                name="orders"
            )
        )

        monthly["period"] = pd.to_datetime(
            monthly["order_year"].astype(str)
            + "-"
            + monthly["order_month"].astype(str)
            + "-01"
        )

        fig3 = px.bar(
            monthly,
            x="period",
            y="orders",
            title="Monthly Order Activity"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        st.markdown(
            "**Observation:** The yearly and monthly charts help identify "
            "changes in catering-order activity and total catering cost "
            "over time."
        )


# ---------------------------------------------------------
# SIDEBAR FOOTER
# ---------------------------------------------------------

st.sidebar.caption(
    "Caterlytics • Data Wrangling Mini Project"
)
