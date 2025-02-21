# Qualitative Coding Tool (POC)
This tool automatically codes qualitative interview data using GPT-4-turbo.

## 📂 Project Structure
- `data/` – Stores input (`interviews.xlsx`) and output files.
- `src/` – Contains Python scripts for data processing and LLM interaction.
- `streamlit_app/` – Contains the Streamlit application for visualizing analysis results.
- `tests/` – Unit tests.
- `requirements.txt` – Install dependencies.

## 🚀 How to Run

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the Analysis:
1. Run the analysis script:
   ```bash
   python src/analyze.py
   ```

### Run the Streamlit App:
1. Navigate to the `streamlit_app` directory:
   ```bash
   cd streamlit_app
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 📊 Visualizing Results
The Streamlit app provides an interactive interface to visualize the analysis results. Follow the instructions in the "Run the Streamlit App" section to start the app and explore the results.

## 🧪 Running Tests
To run the unit tests, use the following command:
```bash
pytest tests/
```