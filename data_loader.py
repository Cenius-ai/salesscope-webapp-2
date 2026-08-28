"""Shared data loader — reads the sales CSV into a cached pandas DataFrame."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "data" / "sales_data.csv"


@st.cache_data(ttl=3600)
def get_data() -> pd.DataFrame:
    """Return the full sales dataset with parsed dates and typed columns."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Sales data file not found at {DATA_PATH}. "
            "Run `python generate_data.py` first."
        )
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["Date"],
        dtype={
            "OrderID": "int64",
            "Region": "string",
            "Product": "string",
            "Category": "string",
            "SalesAmount": "float64",
            "Quantity": "int64",
            "Profit": "float64",
        },
    )
    return df
