import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interview Dashboard", layout="wide")

st.title("📊 Interview Dashboard")

# Load data
df = pd.read_csv("interviews.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------- TECHNOLOGY SELECTOR ----------------

technologies = sorted(df["Technology"].unique())
selected_tech = st.sidebar.radio("Select Technology", technologies)

# Filter data for selected technology
tech_df = df[df["Technology"] == selected_tech]

st.header(f"📌 {selected_tech} Interview Analytics")

# ---------------- KPI SECTION ----------------

total = len(tech_df)
selected = len(tech_df[tech_df["Status"] == "Selected"])
rejected = len(tech_df[tech_df["Status"] == "Rejected"])
selection_rate = (selected / total) * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Interviews", total)
col2.metric("Selected", selected)
col3.metric("Rejected", rejected)
col4.metric("Selection Rate", f"{selection_rate:.2f}%")

st.divider()

# ---------------- CANDIDATE LIST ----------------

st.subheader("📋 Candidates List")

candidate_names = tech_df["Candidate Name"].unique()

selected_candidate = st.selectbox(
    "Select Candidate to View Details",
    candidate_names
)

candidate_data = tech_df[tech_df["Candidate Name"] == selected_candidate]

st.write(candidate_data[["Date", "Status", "Feedback"]])
