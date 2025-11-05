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

def fit_to_container(spec: dict) -> dict:
    """Make the spec fill its container (width & height via CSS)."""
    out = dict(spec)  # don't mutate cached
    # Let container decide width/height; ask Vega-Lite to fit the container.
    out.pop("width", None)
    out.pop("height", None)
    out["autosize"] = {"type": "fit", "contains": "padding"}
    return out

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

# ---------- Global styling to create a 2x2 grid that fits the viewport ----------
st.markdown(
    """
    <style>
      /* Reduce default padding so the two rows fit better */
      .block-container { padding-top: 0.8rem; padding-bottom: 0.8rem; }

      /* Each chart cell aims for ~45vh so two rows fit without scrolling */
      .chartvh { height: 45vh; }
      /* Make the embedded vega container fill that height */
      .chartvh .vega-embed, .chartvh canvas, .chartvh svg { height: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

USE_CONTAINER_WIDTH = True

# ---------- ROW 1: chart4 | chart2 ----------
if ("chart4" in specs) or ("chart2" in specs):
    c1, c2 = st.columns(2)
    if "chart4" in specs:
        with c1:
            st.markdown('<div class="chartvh">', unsafe_allow_html=True)
            st.vega_lite_chart(fit_to_container(specs["chart4"]), use_container_width=USE_CONTAINER_WIDTH)
            st.markdown("</div>", unsafe_allow_html=True)
    if "chart2" in specs:
        with c2:
            st.markdown('<div class="chartvh">', unsafe_allow_html=True)
            st.vega_lite_chart(fit_to_container(specs["chart2"]), use_container_width=USE_CONTAINER_WIDTH)
            st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------- ROW 2: chart1 | chart3 ----------
if ("chart1" in specs) or ("chart3" in specs):
    c3, c4 = st.columns(2)
    if "chart1" in specs:
        with c3:
            st.markdown('<div class="chartvh">', unsafe_allow_html=True)
            st.vega_lite_chart(fit_to_container(specs["chart1"]), use_container_width=USE_CONTAINER_WIDTH)
            st.markdown("</div>", unsafe_allow_html=True)
    if "chart3" in specs:
        with c4:
            st.markdown('<div class="chartvh">', unsafe_allow_html=True)
            st.vega_lite_chart(fit_to_container(specs["chart3"]), use_container_width=USE_CONTAINER_WIDTH)
            st.markdown("</div>", unsafe_allow_html=True)
