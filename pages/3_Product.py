"""Product Performance — horizontal bar chart, profit-vs-quantity scatter, and sortable KPI table."""

import pandas as pd
import streamlit as st

import data_loader
import style

style.apply_style()

st.title("Product Performance")
st.caption("Analyze revenue, profit, and margins by product line.")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df: pd.DataFrame = data_loader.get_data()

product_agg = (
    df.groupby("Product")
    .agg(
        TotalSales=("SalesAmount", "sum"),
        TotalQuantity=("Quantity", "sum"),
        TotalProfit=("Profit", "sum"),
        OrderCount=("SalesAmount", "count"),
    )
    .reset_index()
)
product_agg["MarginPct"] = (
    (product_agg["TotalProfit"] / product_agg["TotalSales"] * 100).round(1)
)

# Sort by sales descending for charts
product_agg = product_agg.sort_values("TotalSales", ascending=True)

# ---------------------------------------------------------------------------
# Horizontal bar chart
# ---------------------------------------------------------------------------
st.subheader("Total Sales by Product")
st.bar_chart(
    product_agg.set_index("Product")[["TotalSales"]],
    use_container_width=True,
    horizontal=True,
)

# ---------------------------------------------------------------------------
# Scatter plot — profit vs quantity
# ---------------------------------------------------------------------------
st.subheader("Profit vs Quantity by Product")
scatter_data = product_agg.set_index("Product")[["TotalQuantity", "TotalProfit"]].copy()
scatter_data = scatter_data.rename(
    columns={"TotalQuantity": "Quantity", "TotalProfit": "Profit"}
)
st.scatter_chart(
    scatter_data,
    x="Quantity",
    y="Profit",
    size="Quantity",
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# Sortable KPI table
# ---------------------------------------------------------------------------
st.subheader("Product KPIs")

table_data = product_agg.sort_values("TotalSales", ascending=False).copy()
table_data["TotalSales"] = table_data["TotalSales"].apply(lambda x: f"${x:,.0f}")
table_data["TotalProfit"] = table_data["TotalProfit"].apply(lambda x: f"${x:,.0f}")
table_data["MarginPct"] = table_data["MarginPct"].apply(lambda x: f"{x}%")
table_data["TotalQuantity"] = table_data["TotalQuantity"].apply(lambda x: f"{x:,}")

st.dataframe(
    table_data.set_index("Product"),
    use_container_width=True,
    column_config={
        "TotalSales": st.column_config.TextColumn("Sales"),
        "TotalQuantity": st.column_config.TextColumn("Quantity"),
        "TotalProfit": st.column_config.TextColumn("Profit"),
        "MarginPct": st.column_config.TextColumn("Margin %"),
        "OrderCount": st.column_config.NumberColumn("Orders"),
    },
)
