import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Multi-Tech Interview Dashboard", layout="wide")

st.title("📊 Multi-Technology Interview Analytics")

# Load data
df = pd.read_csv("interviews.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("🔍 Filters")

# Technology filter (dynamic)
tech_options = ["All"] + sorted(df["Technology"].unique().tolist())
selected_tech = st.sidebar.selectbox("Technology", tech_options)

# Status filter
status_options = ["All"] + sorted(df["Status"].unique().tolist())
selected_status = st.sidebar.selectbox("Status", status_options)

# Date filter
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

# Apply filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

if selected_tech != "All":
    filtered_df = filtered_df[filtered_df["Technology"] == selected_tech]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]

# ---------------- KPI SECTION ----------------

total = len(filtered_df)
selected = len(filtered_df[filtered_df["Status"] == "Selected"])
rejected = len(filtered_df[filtered_df["Status"] == "Rejected"])
selection_rate = (selected / total) * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Interviews", total)
col2.metric("Selected", selected)
col3.metric("Rejected", rejected)
col4.metric("Selection Rate", f"{selection_rate:.2f}%")

st.divider()

# ---------------- SELECTED LIST ----------------

st.subheader("✅ Selected Candidates")

selected_df = filtered_df[filtered_df["Status"] == "Selected"]

if not selected_df.empty:
    st.dataframe(selected_df)
else:
    st.write("No selected candidates.")

st.divider()

# ---------------- REJECTED LIST ----------------

st.subheader("❌ Rejected Candidates")

rejected_df = filtered_df[filtered_df["Status"] == "Rejected"]

if not rejected_df.empty:
    st.dataframe(rejected_df)
else:
    st.write("No rejected candidates.")

st.divider()

# ---------------- REJECTION REASON ANALYSIS ----------------

if not rejected_df.empty:
    reason_count = rejected_df["Feedback"].value_counts().reset_index()
    reason_count.columns = ["Reason", "Count"]

    fig = px.bar(reason_count, x="Reason", y="Count",
                 title="Rejection Reasons Analysis")
    st.plotly_chart(fig, use_container_width=True)
