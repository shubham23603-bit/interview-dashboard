import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interview Dashboard", layout="wide")

st.title("📊 Interview Analytics Dashboard")

# Load CSV file
df = pd.read_csv("interviews.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- KPI SECTION ----------------

total = len(df)
selected = len(df[df["Status"] == "Selected"])
rejected = len(df[df["Status"] == "Rejected"])
selection_rate = (selected / total) * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Interviews", total)
col2.metric("Selected", selected)
col3.metric("Rejected", rejected)
col4.metric("Selection Rate", f"{selection_rate:.2f}%")

st.divider()

# ---------------- SELECTED LIST ----------------

st.subheader("✅ Selected Candidates")

selected_df = df[df["Status"] == "Selected"]

if not selected_df.empty:
    st.dataframe(selected_df[["Date", "Candidate Name", "Technology", "Feedback"]])
else:
    st.write("No selected candidates.")

st.divider()

# ---------------- REJECTED LIST ----------------

st.subheader("❌ Rejected Candidates")

rejected_df = df[df["Status"] == "Rejected"]

if not rejected_df.empty:
    st.dataframe(rejected_df[["Date", "Candidate Name", "Technology", "Feedback"]])
else:
    st.write("No rejected candidates.")

st.divider()

# ---------------- REJECTION REASON CHART ----------------

if not rejected_df.empty:
    reason_count = rejected_df["Feedback"].value_counts().reset_index()
    reason_count.columns = ["Reason", "Count"]

    fig = px.bar(reason_count, x="Reason", y="Count",
                 title="Rejection Reasons Analysis")
    st.plotly_chart(fig, use_container_width=True)
