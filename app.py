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

def apply_size(spec: dict, width: int | None, height: int | None) -> dict:
    spec = dict(spec)  # avoid mutating cached object
    if width is not None:
        spec["width"] = int(width)
    if height is not None:
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

# Layout sizing (no sidebar controls)
USE_CONTAINER_WIDTH = True
ROW1_HEIGHT = 480  # bigger row
ROW2_HEIGHT = 340  # smaller row

# ---------- ROW 1: chart4 | chart3 ----------
if "chart4" in specs or "chart3" in specs:
    c1, c2 = st.columns(2)
    if "chart4" in specs:
        with c1:
            spec = apply_size(specs["chart4"], None if USE_CONTAINER_WIDTH else 600, ROW1_HEIGHT)
            st.vega_lite_chart(spec, use_container_width=USE_CONTAINER_WIDTH)
    if "chart3" in specs:
        with c2:
            spec = apply_size(specs["chart3"], None if USE_CONTAINER_WIDTH else 600, ROW1_HEIGHT)
            st.vega_lite_chart(spec, use_container_width=USE_CONTAINER_WIDTH)

st.divider()

# ---------- ROW 2: chart1 | chart2 ----------
if "chart1" in specs or "chart2" in specs:
    c3, c4 = st.columns(2)
    if "chart1" in specs:
        with c3:
            spec = apply_size(specs["chart1"], None if USE_CONTAINER_WIDTH else 600, ROW2_HEIGHT)
            st.vega_lite_chart(spec, use_container_width=USE_CONTAINER_WIDTH)
    if "chart2" in specs:
        with c4:
            spec = apply_size(specs["chart2"], None if USE_CONTAINER_WIDTH else 600, ROW2_HEIGHT)
            st.vega_lite_chart(spec, use_container_width=USE_CONTAINER_WIDTH)
