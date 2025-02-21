from openai import OpenAI
import json
import os

client = OpenAI()

def get_codes_from_llm(question, answer, existing_codes):
    
    """
    
    Calls the OpenAI Chat Completions API using the new client syntax to generate thematic codes 
    for a given interview answer. The prompt includes the question, answer, and any existing codes.
    
    """

    # Define the JSON Schema
    json_schema = {
        "name": "code_schema",
        "schema": {
            "type": "object",
            "properties": {
                "thematic_codes": {
                    "description" : "the codes identified in the data",
                    "type": "array",
                    "items": {"type": "string"}
                },
                "additionalProperties": False
            },
        }
    }

    few_shot_examples = (
    "Here are a few examples:\n\n"
    "Example 1:\n"
    "Question: Who in your organization is primarily responsible for managing disruptions in global trade?\n"
    "Answer: Our supply chain manager takes the lead on handling trade disruptions. They coordinate with suppliers, negotiate alternative shipping routes, and ensure that we have contingency plans in place. However, our finance team also plays a key role, as they monitor currency fluctuations and adjust our purchasing strategies accordingly. The leadership team steps in when major strategic decisions are needed.\n"
    "Existing Codes: [\"Supply Chain Manager\"]\n"
    "Expected Output: [\"Supply Chain Manager\", \"Finance Team\", \"Leadership Team\"]\n\n"
    "Example 2:\n"
    "Question: How have recent economic challenges affected your household’s access to essential resources?\n"
    "Answer: Over the past year, prices for basic goods like food and electricity have increased significantly, making it difficult for us to afford everything we need. We’ve had to cut back on fresh produce and rely more on cheaper, processed foods. Public transportation costs have also risen, so we now walk more often instead of taking the bus. Our children’s education expenses, like school materials and fees, are harder to manage, so we’ve had to prioritize essentials over extracurricular activities.\n"
    "Existing Codes: [\"Rising Cost of Living\", \"Reduced Use of Public Transportation\"]\n"
    "Expected Output: [\"Rising Cost of Living\", \"Reduced Use of Public Transportation\", \"Reduced Food Quality\", \"Household Budget Adjustments\"]\n\n"
)

    prompt = (
        "You are an expert in qualitative data coding. "
        "Given the following question and interview answer, follow these steps:\n\n"
        "1. Review the list of existing codes provided. \n"
        "2. Read the interview answer carefully and note any additional themes or topics not covered by the existing codes.\n"
        "3. Return a union of the relevant existing codes and any new codes you identified.\n\n"
        "Important Rules:\n"
        "- Only return codes that specifically answer the question and match the type of information requested.\n"
        "- Do not include codes that describe general information unrelated to the question's focus.\n\n"
        + few_shot_examples +
        "Now apply this to the following: "
        f"Question: {question}\n"
        f"Answer: {answer}\n"
        f"Existing Codes: {json.dumps(existing_codes)}\n\n"
        f"Return the response in the specified JSON format."
    )

    # Using the new syntax from the official docs
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model identifier
        #model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are an expert in qualitative data coding."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_schema", "json_schema": json_schema},
    )
    
    try:
        data = json.loads(response.choices[0].message.content)
        return data.get("thematic_codes", [])
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        print("Response content:", response.choices[0].message.content)
        return []