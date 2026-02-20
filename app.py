import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Technology Wise Dashboard", layout="wide")

st.title("📊 Technology Wise Interview Analytics")

# Load data
df = pd.read_csv("interviews.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.divider()

# ---------------- TECHNOLOGY WISE KPI ----------------

technologies = sorted(df["Technology"].unique())

for tech in technologies:
    tech_df = df[df["Technology"] == tech]
    
    total = len(tech_df)
    selected = len(tech_df[tech_df["Status"] == "Selected"])
    rejected = len(tech_df[tech_df["Status"] == "Rejected"])
    selection_rate = (selected / total) * 100 if total > 0 else 0
    
    st.subheader(f"📌 {tech} Interviews Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Interviews", total)
    col2.metric("Selected", selected)
    col3.metric("Rejected", rejected)
    col4.metric("Selection Rate", f"{selection_rate:.2f}%")
    
    st.divider()
