import argparse
import os
from data_loader import load_excel, save_outputs
from llm_coder import get_codes_from_llm
from processing import process_interviews


#### Todo
# - UI to upload and download results
# - create metadata variables
# - option to disaggregate findings based on given metadata variable
# - generate finding summaries incorporating code/theme prevalence
# - implement local model version

def main():

	# Set up CLI argument parsing
    parser = argparse.ArgumentParser(description="Generate codes for qualitative interview data")
    parser.add_argument('data_path', type=str, help="Path to the excel data file")
    
    args = parser.parse_args()
    
    # Check if input files exist
    if not os.path.exists(args.data_path):
        print(f"Error: The excel file '{args.data_path}' does not exist.")
        return

    #model = "gpt-4o-mini"
    model="gpt-4o"
    #model="o3-mini-2025-01-31"

    print("Loading interview data...")
    df = load_excel(args.data_path)

    print(f"Processing interviews with {model}...")	
    aggregated_codes, interview_codes = process_interviews(df, model, get_codes_from_llm)

    print("Saving results...")
    save_outputs(aggregated_codes, interview_codes, model)
    print("Processing complete. Outputs saved in 'data/outputs'.")

if __name__ == "__main__":
    main()