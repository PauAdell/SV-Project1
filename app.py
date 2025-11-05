# app.py
import streamlit as st
import altair as alt

st.set_page_config(page_title="Altair Chart Host", layout="wide")
st.title("Altair Chart Host")

chart = None
error_text = None

# Try to import a function from your own script that returns an Altair chart
# Create a file called chart_module.py with a function `build_chart()` that returns alt.Chart
try:
    from chart_module import build_chart  # <- you provide this
    chart = build_chart()
except Exception as e:
    error_text = str(e)

if chart is None:
    import pandas as pd
    st.info(
        "Couldn’t import your chart from `chart_module.build_chart()`.\n"
        "Showing a small demo chart instead."
        + (f"\n\nDetails: {error_text}" if error_text else "")
    )
    # --- Demo chart ---
    df = pd.DataFrame({"x": list(range(30))})
    df["y"] = (df["x"] * 1.3).round(2)
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("x:Q", title="X"),
            y=alt.Y("y:Q", title="Y"),
            tooltip=["x", "y"],
        )
        .properties(height=400)
        .interactive()
    )

# Render your Altair chart
st.altair_chart(chart, use_container_width=True)

# Optional: show the Vega-Lite spec (helps debug)
with st.expander("View Vega-Lite spec"):
    st.json(chart.to_dict())

