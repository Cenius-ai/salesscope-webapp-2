"""Data Explorer — filterable, searchable, sortable sales record table."""

import pandas as pd
import streamlit as st

import data_loader
import style

style.apply_style()

st.title("Data Explorer")
st.caption("Filter, search, and sort the raw sales records.")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
df: pd.DataFrame = data_loader.get_data()

# ---------------------------------------------------------------------------
# Filters row
# ---------------------------------------------------------------------------
col_date, col_region, col_product = st.columns(3)

with col_date:
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

with col_region:
    all_regions = sorted(df["Region"].unique().tolist())
    selected_regions = st.multiselect(
        "Region(s)",
        options=all_regions,
        default=all_regions,
    )

with col_product:
    all_products = sorted(df["Product"].unique().tolist())
    selected_products = st.multiselect(
        "Product(s)",
        options=all_products,
        default=all_products,
    )

# ---------------------------------------------------------------------------
# Search box
# ---------------------------------------------------------------------------
search_term = st.text_input(
    "Search",
    placeholder="Type to search OrderID, Product, Region, or Category…",
)

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
filtered = df.copy()

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["Date"] >= pd.Timestamp(start))
        & (filtered["Date"] <= pd.Timestamp(end))
    ]
elif date_range:
    filtered = filtered[filtered["Date"] >= pd.Timestamp(date_range)]

if selected_regions:
    filtered = filtered[filtered["Region"].isin(selected_regions)]

if selected_products:
    filtered = filtered[filtered["Product"].isin(selected_products)]

if search_term:
    term = search_term.lower()
    mask = (
        filtered["OrderID"].astype(str).str.lower().str.contains(term, na=False)
        | filtered["Product"].str.lower().str.contains(term, na=False)
        | filtered["Region"].str.lower().str.contains(term, na=False)
        | filtered["Category"].str.lower().str.contains(term, na=False)
    )
    filtered = filtered[mask]

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
st.caption(f"{len(filtered):,} of {len(df):,} records match the current filters.")

st.dataframe(
    filtered.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "OrderID": st.column_config.NumberColumn("Order ID", format="%d"),
        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
        "Region": st.column_config.TextColumn("Region"),
        "Product": st.column_config.TextColumn("Product"),
        "Category": st.column_config.TextColumn("Category"),
        "SalesAmount": st.column_config.NumberColumn("Sales (USD)", format="$%.2f"),
        "Quantity": st.column_config.NumberColumn("Qty"),
        "Profit": st.column_config.NumberColumn("Profit (USD)", format="$%.2f"),
    },
)
