import openai
import json
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_codes_from_llm(question, answer, existing_codes):
    """Calls the LLM to generate thematic codes for a given interview answer."""
    prompt = f"""
    You are an expert in qualitative data coding.
    Given the following question and interview answer, generate a list of relevant thematic codes.
    If any of the existing codes (provided below) are applicable, do not duplicate them; add new ones if necessary.
    
    Question: {question}
    Answer: {answer}
    Existing Codes: {json.dumps(existing_codes)}

    Return only a JSON array of strings.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are an expert in qualitative data coding."},
                  {"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    try:
        return json.loads(response["choices"][0]["message"]["content"])
    except json.JSONDecodeError:
        return []
