"""Regional Breakdown — region selector, bar chart, and KPI table."""

import pandas as pd
import streamlit as st

import data_loader
import style

style.apply_style()

st.title("Regional Breakdown")
st.caption("Compare sales performance across geographic regions.")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df: pd.DataFrame = data_loader.get_data()
all_regions = sorted(df["Region"].unique().tolist())

# ---------------------------------------------------------------------------
# Region selector
# ---------------------------------------------------------------------------
selected_regions = st.multiselect(
    "Select Region(s)",
    options=all_regions,
    default=all_regions,
    help="Choose one or more regions to display.",
)

if not selected_regions:
    st.warning("Select at least one region to view data.")
    st.stop()

filtered = df[df["Region"].isin(selected_regions)]

# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
region_agg = (
    filtered.groupby("Region")
    .agg(
        TotalSales=("SalesAmount", "sum"),
        TotalProfit=("Profit", "sum"),
        TotalQuantity=("Quantity", "sum"),
        AvgOrderValue=("SalesAmount", "mean"),
        OrderCount=("SalesAmount", "count"),
    )
    .sort_values("TotalSales", ascending=False)
    .reset_index()
)

# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------
st.subheader("Total Sales by Region")
st.bar_chart(
    region_agg.set_index("Region")[["TotalSales"]],
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# KPI table
# ---------------------------------------------------------------------------
st.subheader("Regional Metrics")

styled = region_agg.copy()
styled["TotalSales"] = styled["TotalSales"].apply(lambda x: f"${x:,.0f}")
styled["TotalProfit"] = styled["TotalProfit"].apply(lambda x: f"${x:,.0f}")
styled["AvgOrderValue"] = styled["AvgOrderValue"].apply(lambda x: f"${x:,.0f}")
styled["TotalQuantity"] = styled["TotalQuantity"].apply(lambda x: f"{x:,}")

st.dataframe(
    styled.set_index("Region"),
    use_container_width=True,
    column_config={
        "TotalSales": st.column_config.TextColumn("Total Sales"),
        "TotalProfit": st.column_config.TextColumn("Total Profit"),
        "TotalQuantity": st.column_config.TextColumn("Total Quantity"),
        "AvgOrderValue": st.column_config.TextColumn("Avg Order Value"),
        "OrderCount": st.column_config.NumberColumn("Orders"),
    },
)
