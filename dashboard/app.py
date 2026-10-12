

from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_DIR / "reports"

st.set_page_config(page_title="Mutual Fund Analytics", layout="wide")
st.title("Mutual Fund Analytics Dashboard")
st.write("Data Analyst Internship Project")

col1, col2, col3 = st.columns(3)
col1.metric("Fund Master Records", "40")
col2.metric("NAV History Records", "46,000")
col3.metric("Unmatched AMFI Codes", "0")

st.info(
    "These figures describe the supplied datasets. "
    "Matching AMFI codes does not independently verify live scheme names."
)

st.header("Explore Reports")

csv_files = sorted(REPORT_DIR.glob("*.csv"))

if csv_files:
    selected = st.selectbox("Select a CSV report", csv_files, format_func=lambda p: p.name)
    df = pd.read_csv(selected)
    st.write(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    st.dataframe(df, use_container_width=True)

    
numeric_cols = df.select_dtypes(include="number").columns.tolist()

# Avoid plotting identifier columns
chart_cols = [
    col for col in numeric_cols
    if not col.lower().endswith(("_code", "_id"))
]

if chart_cols:
    chart_col = st.selectbox("Select a column for a chart", chart_cols)
    st.bar_chart(df[chart_col])
else:
    st.info("No suitable numeric columns available for a chart in this report.")

else:
    st.warning("No CSV reports found.")

st.header("Charts")

images = sorted(REPORT_DIR.glob("*.png"))
for i in range(0, len(images), 2):
    cols = st.columns(2)
    for col, image_path in zip(cols, images[i:i + 2]):
        with col:
            st.subheader(image_path.stem.replace("_", " ").title())
            st.image(str(image_path), use_container_width=True)

st.caption("Educational analysis only; not investment advice.")
