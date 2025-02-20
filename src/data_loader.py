import pandas as pd
import json

def load_excel(file_path):
    """Loads the Excel file into a Pandas DataFrame."""
    return pd.read_excel(file_path)

def save_outputs(aggregated_codes, interview_codes):
    """Saves outputs in both CSV and JSON formats."""
    pd.DataFrame(aggregated_codes.items(), columns=["Question", "Codes"]).to_csv("data/aggregated_codes.csv", index=False)
    pd.DataFrame(interview_codes).to_csv("data/interview_codes.csv", index=False)

    with open("data/aggregated_codes.json", "w") as f:
        json.dump(aggregated_codes, f, indent=4)
    with open("data/interview_codes.json", "w") as f:
        json.dump(interview_codes, f, indent=4)