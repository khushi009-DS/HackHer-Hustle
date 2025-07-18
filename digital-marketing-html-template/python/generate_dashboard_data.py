import pandas as pd
import json
from collections import Counter

# Load the preprocessed data
df = pd.read_csv("../data/preprocessed_india_job_market.csv")

dashboard_data = {}

# --- 1. Jobs Over Time ---
if 'Posted Date' in df.columns:
    df['Posted Date'] = pd.to_datetime(df['Posted Date'], errors='coerce', dayfirst=True)
    jobs_over_time_series = df['Posted Date'].dt.date.value_counts().sort_index()
    jobs_over_time = {str(date): int(count) for date, count in jobs_over_time_series.items()}
else:
    jobs_over_time = {}
dashboard_data['jobs_over_time'] = jobs_over_time

# --- 2. Top Skills (using one-hot encoded columns) ---
skill_columns = ['aws', 'c++', 'digital marketing', 'excel', 'java', 'machine learning', 'python', 'react', 'sql', 'ui/ux']
top_skills = {skill: int(df[skill].sum()) for skill in skill_columns if skill in df.columns}
dashboard_data['top_skills'] = dict(sorted(top_skills.items(), key=lambda x: x[1], reverse=True))

# --- 3. Job Roles Distribution ---
job_role_prefix = 'Job Title_'
job_roles = {col.replace(job_role_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(job_role_prefix)}
dashboard_data['job_roles'] = dict(sorted(job_roles.items(), key=lambda x: x[1], reverse=True))

# --- 4. Company Popularity ---
company_prefix = 'Company Name_'
company_counts = {col.replace(company_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(company_prefix)}
dashboard_data['companies'] = dict(sorted(company_counts.items(), key=lambda x: x[1], reverse=True))

# --- 5. Locations Heatmap ---
location_prefix = 'Job Location_'
location_counts = {col.replace(location_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(location_prefix)}
dashboard_data['locations'] = dict(sorted(location_counts.items(), key=lambda x: x[1], reverse=True))

# --- 6. Job Type Distribution ---
jobtype_prefix = 'Job Type_'
job_type_counts = {col.replace(jobtype_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(jobtype_prefix)}
dashboard_data['job_types'] = dict(sorted(job_type_counts.items(), key=lambda x: x[1], reverse=True))

# --- 7. Education Requirements ---
edu_prefix = 'Education Requirement_'
edu_counts = {col.replace(edu_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(edu_prefix)}
dashboard_data['education_requirements'] = dict(sorted(edu_counts.items(), key=lambda x: x[1], reverse=True))

# --- 8. Job Portal Distribution ---
portal_prefix = 'Job Portal_'
portal_counts = {col.replace(portal_prefix, ''): int(df[col].sum()) for col in df.columns if col.startswith(portal_prefix)}
dashboard_data['job_portals'] = dict(sorted(portal_counts.items(), key=lambda x: x[1], reverse=True))

# Save to JSON
with open("dashboard_data.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)
