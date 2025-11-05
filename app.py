# app.py
import streamlit as st
import altair as alt
import json
from pathlib import Path

st.set_page_config(page_title="Altair Chart Host", layout="wide")
st.title("Altair Chart Host")

# ---------- Load pre-saved chart ----------
@st.cache_data
def load_chart(path: str):
    """Load an Altair/Vega-Lite JSON chart spec from file."""
    with open(path, "r") as f:
        spec = json.load(f)
    # Rebuild an Altair chart object from the JSON
    return alt.Chart.from_dict(spec)

# Path to your chart JSON (relative to repo root)
chart_path = Path("charts/chart1.json")

if chart_path.exists():
    chart = load_chart(chart_path)
    st.altair_chart(chart, use_container_width=True)
    with st.expander("View Vega-Lite spec"):
        st.json(chart.to_dict())
else:
    st.error(f"Chart file not found: {chart_path}")
    st.info("Make sure charts/chart1.json is committed to your repository.")
