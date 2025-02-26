import pandas as pd
from src.processing import process_interviews

def mock_llm(question, answer, existing_codes):
    """Mock function for testing without calling an actual LLM."""
    return ["Example Code 1", "Example Code 2"]

def test_process_interviews():
    mock_data = {
        "Question": ["What challenges do you face?"],
        "Interview 1": ["Access to markets is difficult."],
        "Interview 2": ["We struggle with funding."]
    }
    df = pd.DataFrame(mock_data, index=None)

    aggregated_codes, interview_codes = process_interviews(df, mock_llm)

    assert "What challenges do you face?" in aggregated_codes
    assert "Example Code 1" in aggregated_codes["What challenges do you face?"]
