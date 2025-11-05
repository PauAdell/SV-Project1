import streamlit as st, json

st.set_page_config(page_title="Altair Chart Host", layout="wide")
st.title("Altair Chart Host")

with open("charts/chart1_inline.json", "r") as f:
    spec = json.load(f)

# Render the raw Vega-Lite spec
st.vega_lite_chart(spec, use_container_width=True)

with st.expander("Spec"):
    st.json(spec)