# Qualitative Coding Tool (POC)

This tool automates the process of coding qualitative interview transcripts using the GPT-4-turbo language model. It aims to identify key themes, sentiments, or other specified codes within interview text data.

## 🎯 Purpose & Goal
The primary goal is to accelerate the qualitative analysis process by providing an initial layer of automated coding. Researchers can then review and refine these automated codes.

## 📂 Project Structure
- `data/` – Stores input data and generated output files.
  - Input: Expects `interviews.xlsx` (see format below).
  - Output: Coded data (e.g., `coded_interviews.xlsx`), analysis summaries.
- `src/` – Contains the core Python logic:
  - `main.py`: The main script to run the analysis pipeline.
  - `data_loader.py`: Handles loading data from input files.
  - `processing.py`: Contains data preprocessing steps.
  - `llm_coder.py`: Manages interaction with the OpenAI API.
  - `preprocessing_tool/`: Additional preprocessing utilities.
- `streamlit_app/` – Contains the Streamlit web application (`app.py`) for visualizing results.
- `tests/` – Unit tests for the application components (`test_*.py`).
- `requirements.txt` – Python package dependencies.
- `.env` – Configuration file for API keys (see Configuration section).
- `.gitignore` – Specifies intentionally untracked files for Git.

## ⚙️ Configuration
Before running, create a `.env` file in the project root directory with your OpenAI API key:
```env
OPENAI_API_KEY='your_api_key_here'
```
The application uses `python-dotenv` to load this key.

## 💾 Input Data Format
The tool expects an input Excel file (`.xlsx`) provided via a command-line argument. This file should contain at least the following columns:
- `InterviewID`: A unique identifier for each interview.
- `Transcript`: The full text of the interview transcript.
*(Add any other required or expected columns here)*

## 📈 Workflow
The main analysis script (`src/main.py`) performs the following steps:
1. **Parse Arguments:** Reads the input file path provided via the command line.
2. **Load Data:** Reads the specified Excel file.
3. **Preprocess Text:** Cleans and prepares the transcript text for analysis.
4. **Code Interviews:** Sends transcript segments to the OpenAI API (GPT-4-turbo) with specific coding prompts.
5. **Process Results:** Aggregates the codes received from the LLM.
6. **Save Output:** Saves the coded data and any generated analysis to the `data/` directory (e.g., `coded_interviews.xlsx`).

## 🚀 How to Run

### 1. Setup Environment
- Ensure you have Python 3.x installed.
- Create a virtual environment (recommended):
  ```bash
  python -m venv qual_coder_env
  source qual_coder_env/bin/activate  # On Windows use `qual_coder_env\Scripts\activate`
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Create and populate the `.env` file as described in the Configuration section.
- Prepare your input Excel file (e.g., `my_interviews.xlsx`).

### 2. Run the Analysis
Execute the main script from the project root directory, passing the path to your input Excel file as an argument (replace `path/to/your/interviews.xlsx` with the actual path):
```bash
python src/main.py path/to/your/interviews.xlsx
```
Check the `data/` directory for output files.

### 3. Run the Streamlit App (Optional)
To visualize results (if implemented):
```bash
streamlit run streamlit_app/app.py
```

## 📊 Visualizing Results
The Streamlit app (`streamlit_app/app.py`) provides an interactive interface to visualize the analysis results. Follow the instructions in the "Run the Streamlit App" section to start the app.

## 🧪 Running Tests
To run the unit tests, execute the following command from the project root directory:
```bash
pytest tests/
```