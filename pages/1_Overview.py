"""Overview — KPI cards, revenue line chart, top-products bar, and region bar chart."""

import pandas as pd
import streamlit as st

import data_loader
import style

style.apply_style()

st.title("Overview")
st.caption("High-level sales metrics, trends, and breakdowns.")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df: pd.DataFrame = data_loader.get_data()

total_sales = df["SalesAmount"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0

# ---------------------------------------------------------------------------
# KPI row — four cards
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Order Value", f"${avg_order_value:,.0f}")
col4.metric("Total Orders", f"{total_orders:,}")

# ---------------------------------------------------------------------------
# Line chart — sales over time (monthly)
# ---------------------------------------------------------------------------
st.subheader("Sales Over Time")

monthly = (
    df.set_index("Date")
    .resample("M")["SalesAmount"]
    .sum()
    .reset_index()
)
monthly["Month"] = monthly["Date"].dt.strftime("%b %Y")
st.line_chart(monthly.set_index("Month")[["SalesAmount"]], use_container_width=True)

# ---------------------------------------------------------------------------
# Two side-by-side bar charts
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Top 5 Products")
    top5 = (
        df.groupby("Product")["SalesAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.bar_chart(top5, use_container_width=True)

with right:
    st.subheader("Sales by Region")
    region_sales = df.groupby("Region")["SalesAmount"].sum().sort_values(ascending=False)
    st.bar_chart(region_sales, use_container_width=True)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.caption(
    f"Data range: {df['Date'].min().strftime('%b %d, %Y')} → "
    f"{df['Date'].max().strftime('%b %d, %Y')}  ·  "
    f"{len(df):,} records"
)
