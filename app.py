# app.py
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Altair Charts Host", layout="wide")
st.title("Altair Charts Host")

# ---------- Helpers ----------
@st.cache_data
def load_spec(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def apply_size(spec: dict, width: int | None, height: int | None) -> dict:
    # Make a shallow copy so we don't mutate the cache
    spec = dict(spec)
    if width is not None:
        spec["width"] = int(width)
    if height is not None:
        spec["height"] = int(height)
    return spec

# ---------- Inputs ----------
left, right = st.columns(2)

with st.sidebar:
    st.header("Display options")
    w = st.slider("Chart width", 400, 1400, 700, step=10)
    h = st.slider("Chart height", 200, 800, 400, step=10)
    fill_container = st.checkbox("Use container width (overrides width)", value=False)
    show_specs = st.checkbox("Show JSON specs", value=False)

# ---------- Load specs ----------
chart1_path = Path("charts/chart1.json")
chart2_path = Path("charts/chart2.json")

errors = []
spec1 = spec2 = None

if chart1_path.exists():
    spec1 = load_spec(str(chart1_path))
else:
    errors.append(f"Missing file: {chart1_path}")

if chart2_path.exists():
    spec2 = load_spec(str(chart2_path))
else:
    errors.append(f"Missing file: {chart2_path}")

if errors:
    st.error(" • " + "\n • ".join(errors))

# ---------- Render ----------
if spec1:
    spec1_sized = apply_size(spec1, None if fill_container else w, h)
    with left:
        st.subheader("Chart 1")
        st.vega_lite_chart(spec1_sized, use_container_width=fil_
