"""Inject the neobrutalist design system into the Streamlit app.

Committed palette tokens + Orbitron/Exo 2 type.  Hex twin #007eb7 for
chart/canvas/native APIs; never pass raw oklch() to a charting library.
"""

import streamlit as st

# ── Palette (committed token set) ──────────────────────────────────────────
ACCENT_HEX = "#007eb7"          # hex twin of oklch(0.56 0.13 239) — use for charts
PALETTE = {
    "--card":             "#feffff",
    "--ring":             "#007eb7",
    "--muted":            "#e9edf0",
    "--accent":           "#007eb7",
    "--border":           "#dbdfe2",
    "--primary":          "#182127",
    "--on-accent":        "#ffffff",
    "--secondary":        "#e9edf0",
    "--background":       "#f7fbfe",
    "--foreground":       "#0e1318",
    "--on-primary":       "#ffffff",
    "--destructive":      "#c9302d",
    "--on-secondary":     "#0e1318",
    "--on-destructive":   "#ffffff",
    "--card-foreground":   "#0e1318",
    "--muted-foreground":  "#5d646a",
}

# Precomputed token declarations for CSS :root
_TOKEN_LINES = "\n".join(f"    {k}: {v};" for k, v in PALETTE.items())

# ── Fonts ──────────────────────────────────────────────────────────────────
HEADING_FONT = "'Orbitron', sans-serif"
BODY_FONT    = "'Exo 2', sans-serif"
MONO_FONT    = "'Exo 2', monospace"

CSS = f"""
<style>
    /* === Fonts === */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Exo+2:wght@400;500;700&display=swap');

    /* === Token root === */
    :root {{
{_TOKEN_LINES}
    }}

    /* === Base === */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background-color: var(--background);
        color: var(--foreground);
        font-family: {BODY_FONT};
    }}

    /* === Headings — Orbitron === */
    h1, h2, h3, h4, h5, h6 {{
        font-family: {HEADING_FONT};
        font-weight: 700;
        color: var(--foreground);
        letter-spacing: 0.02em;
    }}

    /* === Sidebar === */
    [data-testid="stSidebar"] {{
        background-color: var(--primary);
        border-right: 3px solid #000;
    }}
    [data-testid="stSidebar"] * {{
        color: var(--on-primary);
    }}

    /* === Metric cards (neobrutalist) === */
    [data-testid="stMetric"] {{
        background-color: var(--card);
        border: 3px solid #000;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 4px 4px 0 #000;
        transition: transform 120ms ease, box-shadow 120ms ease;
    }}
    [data-testid="stMetric"]:hover {{
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 #000;
    }}
    [data-testid="stMetric"] label {{
        font-family: {HEADING_FONT};
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--muted-foreground);
    }}
    [data-testid="stMetricValue"] {{
        font-family: {HEADING_FONT};
        font-weight: 700;
        font-size: 2rem;
        color: var(--accent);
    }}

    /* === DataFrames === */
    [data-testid="stDataFrame"] {{
        border: 3px solid #000;
        border-radius: 4px;
        overflow: hidden;
        box-shadow: 4px 4px 0 #000;
    }}
    .stDataFrame table {{
        border-collapse: collapse;
    }}
    .stDataFrame th {{
        background-color: var(--card);
        color: var(--foreground);
        font-family: {HEADING_FONT};
        font-weight: 700;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 3px solid #000;
    }}
    .stDataFrame td {{
        font-family: {BODY_FONT};
        font-size: 0.82rem;
        color: var(--foreground);
    }}

    /* === Buttons === */
    .stButton > button {{
        font-family: {HEADING_FONT};
        font-weight: 700;
        border: 3px solid #000;
        border-radius: 4px;
        background-color: var(--accent);
        color: var(--on-accent);
        box-shadow: 4px 4px 0 #000;
        transition: transform 120ms ease, box-shadow 120ms ease;
    }}
    .stButton > button:hover {{
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0 #000;
    }}
    .stButton > button:active {{
        transform: translate(2px, 2px);
        box-shadow: 0 0 0 #000;
    }}
    .stButton > button:focus-visible {{
        outline: 3px solid var(--ring);
        outline-offset: 3px;
    }}

    /* === Select boxes / multiselect === */
    [data-baseweb="select"] > div {{
        border: 3px solid #000;
        border-radius: 4px;
        background-color: var(--card);
    }}

    /* === Date inputs === */
    [data-testid="stDateInput"] input {{
        border: 3px solid #000;
        border-radius: 4px;
        background-color: var(--card);
        color: var(--foreground);
    }}

    /* === Chart containers === */
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] canvas {{
        background-color: var(--card);
        border: 3px solid #000;
        border-radius: 4px;
        padding: 0.5rem;
        box-shadow: 4px 4px 0 #000;
    }}

    /* === Expander === */
    [data-testid="stExpander"] {{
        border: 3px solid #000;
        border-radius: 4px;
        background-color: var(--card);
        box-shadow: 4px 4px 0 #000;
    }}

    /* === Focus rings === */
    *:focus-visible {{
        outline: 3px solid var(--ring);
        outline-offset: 2px;
    }}

    /* === Scrollbar === */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: var(--muted); }}
    ::-webkit-scrollbar-thumb {{
        background: var(--border);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

    /* === Sticker badge (rotated, one per view) === */
    .neobrutalist-sticker {{
        display: inline-block;
        font-family: {HEADING_FONT};
        font-weight: 700;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.2rem 0.55rem;
        border: 3px solid #000;
        border-radius: 4px;
        background-color: var(--accent);
        color: var(--on-accent);
        box-shadow: 3px 3px 0 #000;
        transform: rotate(-2deg);
    }}

    /* === Reduced motion === */
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
        .stButton > button:hover,
        [data-testid="stMetric"]:hover {{
            transform: none;
        }}
    }}
</style>
"""


def apply_style() -> None:
    """Inject the neobrutalist design CSS into the current page."""
    st.markdown(CSS, unsafe_allow_html=True)
