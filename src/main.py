from data_loader import load_excel, save_outputs
from llm_coder import get_codes_from_llm
from processing import process_interviews

def main():
    print("Loading interview data...")
    df = load_excel("data/interviews.xlsx")

    print("Processing interviews with LLM...")
    aggregated_codes, interview_codes = process_interviews(df, get_codes_from_llm)

    print("Saving results...")
    save_outputs(aggregated_codes, interview_codes)
    print("Processing complete. Outputs saved in 'data/'.")

if __name__ == "__main__":
    main()