"""SalesScope — Sales Analytics Dashboard. Entry point for Streamlit multipage app."""

import streamlit as st

import data_loader
import style

st.set_page_config(
    page_title="SalesScope",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

style.apply_style()

# Preload data so every page benefits from the cache warm-up
try:
    data_loader.get_data()
except FileNotFoundError:
    st.error("Sales data CSV not found. Run `python generate_data.py` first.")
    st.stop()

# --- Sidebar branding ---
st.sidebar.markdown(
    """
    <div style="padding: 0.5rem 0 1rem 0;">
        <h1 style="font-family: 'Orbitron', sans-serif; font-weight: 700; font-size: 1.3rem;
                   color: #ffffff; margin: 0; letter-spacing: 0.02em;">
            SalesScope
        </h1>
        <p style="font-family: 'Orbitron', sans-serif; font-size: 0.6rem; color: #5d646a;
                  text-transform: uppercase; letter-spacing: 0.15em; margin: 0.3rem 0 0 0;">
            Analytics Dashboard
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
