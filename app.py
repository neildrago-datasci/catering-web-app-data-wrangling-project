
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Caterlytics", page_icon="🍽️", layout="wide")

BASE = Path(__file__).resolve().parent
CLEAN = pd.read_csv(BASE / "data" / "catering_orders_cleaned.csv", parse_dates=["order_date"])
BAL = pd.read_csv(BASE / "data" / "catering_orders_balanced.csv", parse_dates=["order_date"])
RAW = pd.read_csv(BASE / "data" / "catering_orders_raw.csv")

st.sidebar.title("🍽️ Caterlytics")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Load & Understand Data", "Clean Data", "Balance Data", "Visualize & Analyze"]
)

if page == "Home":
    st.title("🍽️ Caterlytics")
    st.subheader("Catering Orders — Data Wrangling & Analysis")
    st.write(
        "A Streamlit mini-project demonstrating data loading, inspection, cleaning, "
        "class balancing, visualization, and business-oriented insights from a catering-order dataset."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Raw Records", len(RAW))
    c2.metric("Clean Records", len(CLEAN))
    c3.metric("Clients", CLEAN["client_id"].nunique())
    c4.metric("Total Catering Cost", f"₹{CLEAN['total_cost'].sum():,.2f}")
    st.markdown("### Project workflow")
    st.markdown(
        "1. **Load & Understand Data** — inspect structure, types, missing values and duplicates.\n"
        "2. **Clean Data** — standardize fields, parse dates, validate costs/statuses and create useful date features.\n"
        "3. **Balance Data** — use random oversampling on fulfillment status for balanced analytical/modeling data.\n"
        "4. **Visualize & Analyze** — study status, clients, cost, time trends and operational patterns."
    )
    st.info("Dataset scope: 150 catering orders, 19 clients, 4 fulfillment statuses, with order dates from 2020–2024.")

elif page == "Load & Understand Data":
    st.title("📥 Load & Understand Data")
    st.markdown("### First 5 records")
    st.dataframe(RAW.head(), use_container_width=True)
    a,b,c,d = st.columns(4)
    a.metric("Rows", RAW.shape[0])
    b.metric("Columns", RAW.shape[1])
    c.metric("Missing Cells", int(RAW.isna().sum().sum()))
    d.metric("Duplicate Rows", int(RAW.duplicated().sum()))
    st.markdown("### Column names")
    st.write(list(RAW.columns))
    st.markdown("### Data types")
    st.dataframe(pd.DataFrame({"Column": RAW.columns, "Data Type": RAW.dtypes.astype(str).values}), use_container_width=True)
    st.markdown("### Missing-value summary")
    miss = pd.DataFrame({"Missing Values": RAW.isna().sum(), "Missing %": (RAW.isna().mean()*100).round(2)})
    st.dataframe(miss, use_container_width=True)
    st.markdown("### Descriptive statistics")
    st.dataframe(RAW.describe(include="all").transpose(), use_container_width=True)

elif page == "Clean Data":
    st.title("🧹 Clean Data")
    st.markdown("### Cleaning actions")
    st.markdown(
        "- Standardized column names and text values.\n"
        "- Converted `order_id` to numeric, `order_date` to datetime, and `total_cost` to numeric.\n"
        "- Removed exact duplicate rows if present.\n"
        "- Validated fulfillment statuses against the four expected categories.\n"
        "- Checked for missing IDs/dates/costs and non-positive costs.\n"
        "- Added `order_year`, `order_month`, `month_name`, `day_name`, and `order_quarter` for analysis."
    )
    a,b,c,d = st.columns(4)
    a.metric("Raw rows", len(RAW))
    b.metric("Clean rows", len(CLEAN))
    c.metric("Exact duplicates removed", int(RAW.duplicated().sum()))
    d.metric("Missing cells after cleaning", int(CLEAN.isna().sum().sum()))
    st.markdown("### Cleaned data")
    st.dataframe(CLEAN.head(20), use_container_width=True)
    st.download_button(
        "⬇️ Download Cleaned CSV",
        CLEAN.to_csv(index=False).encode("utf-8"),
        "catering_orders_cleaned.csv",
        "text/csv"
    )

elif page == "Balance Data":
    st.title("⚖️ Balance Data")
    st.write(
        "The target used for balancing is `fulfillment_status`. The original distribution is intentionally preserved "
        "in the cleaned dataset; a separate balanced dataset is created using random oversampling so that each status "
        "has the same number of records."
    )
    before = CLEAN["fulfillment_status"].value_counts().rename("Original")
    after = BAL["fulfillment_status"].value_counts().rename("Balanced")
    comp = pd.concat([before, after], axis=1).fillna(0).astype(int)
    st.dataframe(comp, use_container_width=True)
    fig1 = px.bar(comp.reset_index().melt(id_vars="fulfillment_status", var_name="Dataset", value_name="Orders"),
                  x="fulfillment_status", y="Orders", color="Dataset", barmode="group",
                  title="Fulfillment Status: Original vs Balanced")
    st.plotly_chart(fig1, use_container_width=True)
    st.info("Balanced data contains 288 rows: 72 records per fulfillment status. Use the balanced file for fair class-based analysis/modeling; use the cleaned file for real-world distribution reporting.")
    st.download_button(
        "⬇️ Download Balanced CSV",
        BAL.to_csv(index=False).encode("utf-8"),
        "catering_orders_balanced.csv",
        "text/csv"
    )

elif page == "Visualize & Analyze":
    st.title("📊 Visualize & Analyze")
    tab1, tab2, tab3 = st.tabs(["Orders & Status", "Cost & Clients", "Time Trends"])
    with tab1:
        status = CLEAN["fulfillment_status"].value_counts().reset_index()
        status.columns = ["fulfillment_status", "orders"]
        fig = px.pie(status, names="fulfillment_status", values="orders", hole=.35, title="Fulfillment Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.bar(status, x="fulfillment_status", y="orders", title="Orders by Fulfillment Status", text="orders")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Observation:** Delivered is the largest category, while Delayed is the smallest. The original data is therefore imbalanced across fulfillment outcomes.")
    with tab2:
        client = CLEAN["client_id"].value_counts().reset_index()
        client.columns = ["client_id", "orders"]
        fig = px.bar(client.head(10), x="client_id", y="orders", title="Top 10 Clients by Number of Orders", text="orders")
        st.plotly_chart(fig, use_container_width=True)
        cost_status = CLEAN.groupby("fulfillment_status", as_index=False)["total_cost"].mean().sort_values("total_cost", ascending=False)
        fig2 = px.bar(cost_status, x="fulfillment_status", y="total_cost", title="Average Catering Cost by Fulfillment Status", text_auto=".2f")
        st.plotly_chart(fig2, use_container_width=True)
        st.metric("Average Order Cost", f"₹{CLEAN['total_cost'].mean():,.2f}")
        st.metric("Median Order Cost", f"₹{CLEAN['total_cost'].median():,.2f}")
    with tab3:
        yearly = CLEAN.groupby("order_year").agg(orders=("order_id","count"), total_cost=("total_cost","sum")).reset_index()
        fig = px.line(yearly, x="order_year", y="orders", markers=True, title="Orders by Year")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = px.line(yearly, x="order_year", y="total_cost", markers=True, title="Total Catering Cost by Year")
        st.plotly_chart(fig2, use_container_width=True)
        monthly = CLEAN.groupby(["order_year","order_month"]).size().reset_index(name="orders")
        monthly["period"] = pd.to_datetime(monthly["order_year"].astype(str) + "-" + monthly["order_month"].astype(str) + "-01")
        fig3 = px.bar(monthly, x="period", y="orders", title="Monthly Order Activity")
        st.plotly_chart(fig3, use_container_width=True)

st.sidebar.caption("Caterlytics • Data Wrangling Mini Project")
