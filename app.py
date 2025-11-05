# app.py
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Scientific Visualization Practical work", layout="wide")
st.title("Scientific Visualization Practical work")

# ---------- Helpers ----------
@st.cache_data
def load_spec(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def apply_size(spec: dict, width: int, height: int) -> dict:
    spec = dict(spec)  # avoid mutating cached object
    spec["width"] = int(width)
    spec["height"] = int(height)
    return spec

# ---------- Load JSON specs ----------
paths = {
    "chart1": Path("charts/chart1.json"),
    "chart2": Path("charts/chart2.json"),
    "chart3": Path("charts/chart3.json"),
    "chart4": Path("charts/chart4.json"),
}
specs = {}
for key, p in paths.items():
    if p.exists():
        specs[key] = load_spec(str(p))
    else:
        st.warning(f"Missing file: {p}")

# ---------- Layout ----------
# Row 1: chart4 (left) | chart2 (right)
if "chart4" in specs or "chart2" in specs:
    col1, col2 = st.columns([1, 1])
    with col1:
        if "chart4" in specs:
            spec = apply_size(specs["chart4"], 940, 300)
            st.vega_lite_chart(spec, use_container_width=False)
    with col2:
        if "chart2" in specs:
            spec = apply_size(specs["chart2"], 700, 300)
            st.vega_lite_chart(spec, use_container_width=False)

st.divider()

# Row 2: chart1 (left) | chart3 (right)
if "chart1" in specs or "chart3" in specs:
    col3, col4 = st.columns([1, 2])  # chart3 is wider
    with col3:
        if "chart1" in specs:
            spec = apply_size(specs["chart1"], 900, 300)
            st.vega_lite_chart(spec, use_container_width=False)
    with col4:
        if "chart3" in specs:
            spec = apply_size(specs["chart3"], 50, 200)
            st.vega_lite_chart(spec, use_container_width=False)
