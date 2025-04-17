import pandas as pd

def process_interviews(df, model, llm_function):
    """
    Processes the interview data to generate codes.
    
    The DataFrame is expected to have:
      - Row 0: Interview IDs (columns 1...n); column 0 can be empty or a header.
      - Rows 1...m: Column 0 contains questions; columns 1...n contain responses.
    
    Returns:
      - aggregated_codes: { question_text: [code1, code2, ...] }
      - interview_codes: { interview_id: { question_text: [code1, code2, ...] } }
    """
    # Extract interview IDs from the first row (excluding first column)
    interview_ids = df.iloc[0, 1:].tolist()
    
    # Extract questions from the first column starting at row 1
    questions = df.iloc[1:, 0].tolist()
    
    # Extract responses: rows 1 onward, columns 1 onward
    responses = df.iloc[1:, 1:].values

    # Initialize dictionaries to store outputs
    aggregated_codes = {}  # Maps each question to its aggregated codes
    interview_codes = {interview_id: {} for interview_id in interview_ids}

    # Iterate over each question and corresponding responses
    for row_idx, question in enumerate(questions):
        aggregated_codes[question] = []
        for col_idx, interview_id in enumerate(interview_ids):
            response = responses[row_idx, col_idx]
            if pd.isna(response):
                continue  # Skip empty responses
            
            # Get existing aggregated codes for this question
            existing_codes = aggregated_codes[question]
            
            # Generate codes using the LLM function
            codes = llm_function(question, response, existing_codes, model)

            print(f"Question: \n {question} \n\n")
            print(f"Response: \n {response} \n\n")
            print(f"Identified codes in response: \n {codes} \n\n")

            # Add any new codes to the aggregated list (avoid duplicates)
            for code in codes:
                if code not in aggregated_codes[question]:
                    aggregated_codes[question].append(code)

            # Store codes specific to this interview and question
            interview_codes[interview_id][question] = codes

    return aggregated_codes, interview_codes
