import argparse
import os
import pandas as pd
from .data_loader import load_excel, save_outputs
from .llm_coder import get_codes_from_llm
from .processing import process_interviews

# Define the default model
DEFAULT_MODEL = "gpt-4o" 

#### Todo
# - UI to upload and download results
# - create metadata variables
# - option to disaggregate findings based on given metadata variable
# - generate finding summaries incorporating code/theme prevalence
# - implement local model version

def run_analysis_pipeline(input_df: pd.DataFrame, model: str):
    """
    Runs the qualitative coding pipeline on the input DataFrame.

    Args:
        input_df: DataFrame containing interview data (e.g., 'InterviewID', 'Transcript').
        model: The identifier for the language model to use.

    Returns:
        A tuple containing:
        - aggregated_codes: DataFrame or structure with aggregated results.
        - interview_codes: DataFrame or structure with detailed results per interview.
    """
    print(f"Processing interviews with {model}...") # Keep prints for feedback
    aggregated_codes, interview_codes = process_interviews(input_df, model, get_codes_from_llm)
    print("Processing complete.") 
    return aggregated_codes, interview_codes

def main_cli():
    """Handles Command Line Interface execution."""
    # Set up CLI argument parsing
    parser = argparse.ArgumentParser(description="Generate codes for qualitative interview data")
    parser.add_argument('data_path', type=str, help="Path to the excel data file")
    parser.add_argument('--model', type=str, default=DEFAULT_MODEL, 
                        help=f"LLM model to use (default: {DEFAULT_MODEL})")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.data_path):
        print(f"Error: The excel file '{args.data_path}' does not exist.")
        return

    print("Loading interview data...")
    df = load_excel(args.data_path)

    # Call the refactored pipeline function
    aggregated_codes, interview_codes = run_analysis_pipeline(df, args.model)

    print("Saving results...")
    # Save results for the CLI version
    save_outputs(aggregated_codes, interview_codes, args.model) 
    print("Processing complete. Outputs saved in 'data/outputs'.") # Assuming save_outputs saves there

if __name__ == "__main__":
    main_cli()