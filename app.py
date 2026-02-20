import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interview Analytics Dashboard", layout="wide")

st.title("📊 Interview Analytics Dashboard")

# Load Data
df = pd.read_csv("interviews.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ------------------ SIDEBAR FILTERS ------------------

st.sidebar.header("🔍 Filters")

# Date Filter
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

# Technology Filter
tech_options = ["All"] + list(df["Technology"].unique())
selected_tech = st.sidebar.selectbox("Technology", tech_options)

# Status Filter
status_options = ["All"] + list(df["Status"].unique())
selected_status = st.sidebar.selectbox("Status", status_options)

# Apply Filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

if selected_tech != "All":
    filtered_df = filtered_df[filtered_df["Technology"] == selected_tech]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]

# ------------------ KPI SECTION ------------------

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

# ------------------ MONTHLY TREND ------------------

filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").astype(str)
monthly = filtered_df.groupby("Month").size().reset_index(name="Interviews")

fig1 = px.line(monthly, x="Month", y="Interviews",
               title="📈 Monthly Interview Trend",
               markers=True)
st.plotly_chart(fig1, use_container_width=True)

# ------------------ REJECTION REASONS ------------------

reject_df = filtered_df[filtered_df["Status"] == "Rejected"]

if not reject_df.empty:
    reason_count = reject_df["Feedback"].value_counts().reset_index()
    reason_count.columns = ["Reason", "Count"]

    fig2 = px.bar(reason_count, x="Reason", y="Count",
                  title="❌ Rejection Reasons Analysis")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------ CANDIDATE TABLE ------------------

st.subheader("📋 Candidate Details")

selected_candidate = st.selectbox(
    "Select Candidate to View Feedback",
    filtered_df["Candidate Name"].unique()
)

if selected_candidate:
    candidate_data = filtered_df[
        filtered_df["Candidate Name"] == selected_candidate
    ]
    st.write(candidate_data)
