import streamlit as st
import json
import os
import pandas as pd

# Define paths based on project structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

aggregated_codes_path = os.path.join(DATA_DIR, "aggregated_codes.json")
interview_codes_path = os.path.join(DATA_DIR, "interview_codes.json")

# Load JSON files
with open(aggregated_codes_path, "r") as f:
    aggregated_codes = json.load(f)

with open(interview_codes_path, "r") as f:
    interview_codes = json.load(f)

# Extract interview IDs
interview_ids = list(interview_codes.keys())

# Prepare data for structured display
data = []

for question, all_codes in aggregated_codes.items():
    for code in all_codes:  # Each code gets its own row
        row = {"Question": question, "Code": code}
        
        for interview in interview_ids:
            identified_codes = interview_codes.get(interview, {}).get(question, [])
            row[interview] = "✅" if code in identified_codes else "-"  # Mark presence

        data.append(row)

# Convert to DataFrame for display
df = pd.DataFrame(data)

st.set_page_config(layout="wide")  # Makes the entire page use full width

# Streamlit UI
st.title("Qualitative Coding Review - Matrix View")

st.write("### Coding Matrix (Code-Level Breakdown)")
st.dataframe(df, height=800, width=1200)

st.write("**Legend:**")
st.markdown("- ✅ = Code is identified in the given interview")
