import pandas as pd
import json

def load_excel(file_path):
    """
    Loads the Excel file into a DataFrame.
    
    Expected Excel structure:
      - Row 0: The first cell is unused or a header; cells 1...n contain interview IDs.
      - Rows 1...m: Column 0 contains the question text; columns 1...n contain responses.
    """
    return pd.read_excel(file_path, header=None)

def save_outputs(aggregated_codes, interview_codes):
    """
    Saves outputs in both CSV and JSON formats.
    """
    # Save aggregated codes: each question with its aggregated codes
    agg_data = [(question, "; ".join(codes)) for question, codes in aggregated_codes.items()]
    pd.DataFrame(agg_data, columns=["Question", "Aggregated Codes"]).to_csv("data/aggregated_codes.csv", index=False)

    # Save interview-specific codes: each interview's responses by question
    # Create a DataFrame where each row is a question and each column is an interview.
    output = {"Question": list(aggregated_codes.keys())}
    for interview_id, q_codes in interview_codes.items():
        # Align order of questions using the aggregated_codes keys
        codes_list = []
        for question in aggregated_codes.keys():
            # Join codes with a semicolon if there are any, otherwise leave blank.
            codes = q_codes.get(question, [])
            codes_list.append("; ".join(codes))
        output[interview_id] = codes_list
    pd.DataFrame(output).to_csv("data/interview_codes.csv", index=False)

    # Also save as JSON files
    with open("data/aggregated_codes.json", "w") as f:
        json.dump(aggregated_codes, f, indent=4)
    with open("data/interview_codes.json", "w") as f:
        json.dump(interview_codes, f, indent=4)
