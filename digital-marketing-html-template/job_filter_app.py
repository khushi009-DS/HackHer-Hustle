import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("preprocessed_india_job_market.csv")

df = load_data()

# Extract filters from column names
domain_options = [col.replace("Job Title_", "") for col in df.columns if col.startswith("Job Title_")]
skill_options = [col for col in ["python", "sql", "java", "excel", "aws", "c++", "react", "machine learning", "ui/ux", "digital marketing"] if col in df.columns]
location_options = [col.replace("Job Location_", "") for col in df.columns if col.startswith("Job Location_")]

# Sidebar filters
st.sidebar.header("Filter Jobs")
selected_domains = st.sidebar.multiselect("Select Job Roles", domain_options)
selected_skills = st.sidebar.multiselect("Select Required Skills", skill_options)
selected_locations = st.sidebar.multiselect("Select Job Locations", location_options)

# Filtering function
def filter_jobs(domains=None, skills=None, locations=None):
    filtered_df = df.copy()

    if domains:
        domain_cols = [f"Job Title_{d}" for d in domains]
        filtered_df = filtered_df[filtered_df[domain_cols].any(axis=1)]

    if skills:
        filtered_df = filtered_df[(filtered_df[skills].sum(axis=1) == len(skills))]

    if locations:
        location_cols = [f"Job Location_{loc}" for loc in locations]
        filtered_df = filtered_df[filtered_df[location_cols].any(axis=1)]

    return filtered_df

# Apply filters
result_df = filter_jobs(
    domains=selected_domains,
    skills=selected_skills,
    locations=selected_locations
)

# Display results
st.title("Job Finder")
st.write(f"### {len(result_df)} Jobs Found")
st.dataframe(result_df[[
    "Posted Date", "Company Size", "Average Salary (LPA)", "Experience (Years)", "Number of Applicants"
] + [f"Job Title_{d}" for d in selected_domains if f"Job Title_{d}" in result_df.columns] 
  + selected_skills 
  + [f"Job Location_{loc}" for loc in selected_locations if f"Job Location_{loc}" in result_df.columns]])
