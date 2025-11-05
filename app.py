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
    spec = dict(spec)  # avoid mutating cached object
    if width is not None:
        spec["width"] = int(width)
    if height is not None:
        spec["height"] = int(height)
    return spec

# ---------- Sidebar controls (shared) ----------
with st.sidebar:
    st.header("Display options")
    w_row1 = st.slider("Row 1 width (each col)", 350, 1200, 600, step=10)
    h_row1 = st.slider("Row 1 height", 200, 800, 380, step=10)
    w_row2 = st.slider("Row 2 width", 400, 1600, 1200, step=10)
    h_row2 = st.slider("Row 2 height", 200, 900, 420, step=10)
    fill_container = st.checkbox("Use container width (ignore width values)", value=False)
    show_specs = st.checkbox("Show JSON specs", value=False)

# ---------- Load JSON specs ----------
paths = {
    "chart1": Path("charts/chart1.json"),
    "chart2": Path("charts/chart2.json"),
    "chart4": Path("charts/chart4.json"),  # NEW chart on a new row
}
specs = {}
for key, p in paths.items():
    if p.exists():
        specs[key] = load_spec(str(p))
    else:
        st.warning(f"Missing file: {p}")

# ---------- ROW 1: two charts side-by-side ----------
if "chart1" in specs or "chart2" in specs:
    c1, c2 = st.columns(2)
    if "chart1" in specs:
        with c1:
            st.subheader("Chart 1")
            spec = apply_size(specs["chart1"], None if fill_container else w_row1, h_row1)
            st.vega_lite_chart(spec, use_container_width=fill_container)
    if "chart2" in specs:
        with c2:
            st.subheader("Chart 2")
            spec = apply_size(specs["chart2"], None if fill_container else w_row1, h_row1)
            st.vega_lite_chart(spec, use_container_width=fill_container)

st.divider()

# ---------- ROW 2: one full-width chart (Chart 3) ----------
if "chart4" in specs:
    st.subheader("Chart 4")
    spec = apply_size(specs["chart4"], None if fill_container else w_row2, h_row2)
    st.vega_lite_chart(spec, use_container_width=fill_container)

# --- If you prefer 3 charts in the second row, uncomment this block ---
# if all(k in specs for k in ("chart1","chart2","chart3")):
#     st.markdown("### Row 2 (three columns example)")
#     r2c1, r2c2, r2c3 = st.columns(3)
#     for col, key in zip((r2c1, r2c2, r2c3), ("chart1","chart2","chart3")):
#         with col:
#             spec = apply_size(specs[key], None if fill_container else int(w_row2/3), h_row2)
#             st.vega_lite_chart(spec, use_container_width=fill_container)

# ---------- Optional: show raw specs ----------
if show_specs:
    st.divider()
    st.subheader("Vega-Lite JSON")
    cols = st.columns(3)
    for col, key in zip(cols, ("chart1","chart2","chart4")):
        with col:
            st.caption(f"{key}.json")
            st.json(specs.get(key, {"error": "not loaded"}))
