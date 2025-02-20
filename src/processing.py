def process_interviews(df, llm_function):
    """Processes all interviews, generating codes for each question."""
    question_col = df.columns[0]  # First column contains the questions
    interview_cols = df.columns[1:]  # Other columns contain interview answers

    aggregated_codes = {}
    interview_codes = {interview: {} for interview in interview_cols}

    for _, row in df.iterrows():
        question = row[question_col]
        aggregated_codes.setdefault(question, [])

        for interview in interview_cols:
            answer = row[interview]
            existing_codes = aggregated_codes[question]
            codes = llm_function(question, answer, existing_codes)

            # Merge new codes with existing ones
            for code in codes:
                if code not in aggregated_codes[question]:
                    aggregated_codes[question].append(code)

            # Store codes per interview
            interview_codes[interview][question] = codes

    return aggregated_codes, interview_codes
