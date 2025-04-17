import streamlit as st
import pandas as pd
import os
import sys
import io # Needed for download button

# --- Page Configuration (MUST BE FIRST Streamlit command) ---
st.set_page_config(layout="wide", page_title="Qualitative Coder")

# --- Custom CSS Injection ---
st.markdown("""
<style>
    /* Reduce top padding for the main block */
    .main .block-container {{ padding-top: 1rem; padding-bottom: 1rem; }}
    /* Reduce title font size and top margin */
    h1 {{
        font-size: 1.8rem !important; 
        margin-top: 0 !important; /* Attempt to remove top margin */
        padding-top: 0 !important; /* Attempt to remove top padding */
        margin-bottom: 0.5rem !important; /* Add a small bottom margin for spacing below title */
    }}
</style>
""", unsafe_allow_html=True)

# Add the project root to the Python path to allow importing from src
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import the analysis function AFTER adjusting sys.path
try:
    from src.main import run_analysis_pipeline, DEFAULT_MODEL
except ImportError as e:
    st.error(f"Error importing analysis function: {e}. Ensure backend code is available.")
    st.stop() # Stop execution if import fails

# --- Available Models ---
# Define the models available for selection
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o"] # Add more models as needed

# --- Initialize Session State ---
# Use keys to prevent state reset on rerun if not already initialized
if 'input_df' not in st.session_state: # Store the loaded DataFrame
    st.session_state.input_df = None
if 'results' not in st.session_state:
    st.session_state.results = None # Will store (aggregated_codes, interview_codes)
if 'error' not in st.session_state:
    st.session_state.error = None
if 'running_analysis' not in st.session_state:
    st.session_state.running_analysis = False

# Title appears after config and CSS injection
st.title("Qualitative Coding Assistant")

# --- Create Tabs ---
tab1, tab2 = st.tabs(["🤖 Run Analysis", "📊 View Results"])

# --- Tab 1: Run Analysis ---
with tab1:
    st.header("1. Load Data & Run Analysis")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 5]) # Left column 1/6, right column 5/6

    with col1:
        # --- File Uploader ---
        uploaded_file = st.file_uploader("Upload your interview data (Excel file)", type=["xlsx"])

        # --- Analysis Settings (Model Selection) ---
        selected_model = st.selectbox(
            "Choose the LLM model for analysis:",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL) if DEFAULT_MODEL in AVAILABLE_MODELS else 0,
            disabled=st.session_state.running_analysis # Disable while running
        )

        # --- Analysis Trigger Button ---
        run_button_clicked = st.button("Run Analysis", 
                                    disabled=(st.session_state.input_df is None or st.session_state.running_analysis))

        if uploaded_file is not None:
            # Create a unique key for the uploaded file to check if it's new
            current_file_key = f"{uploaded_file.name}-{uploaded_file.size}"
            
            # Check if this file is different from the last successfully loaded one
            if current_file_key != st.session_state.get('_uploaded_file_key'):
                try:
                    # Read into DataFrame immediately for preview and store in session state
                    st.session_state.input_df = pd.read_excel(uploaded_file)
                    # Store the key of the successfully loaded file
                    st.session_state._uploaded_file_key = current_file_key 
                    st.success(f"File '{uploaded_file.name}' loaded successfully.")
                    # Rerun to update button state immediately after load
                    st.rerun() 
                except Exception as e:
                    st.error(f"Error reading uploaded file: {e}")
                    st.session_state.input_df = None # Reset df on error
                    st.session_state._uploaded_file_key = None # Reset key on error

        # --- Analysis Execution Logic ---
        # Triggered by the button click, but only proceeds if data is loaded
        if run_button_clicked and st.session_state.input_df is not None:
            st.session_state.running_analysis = True
            st.session_state.results = None # Clear previous results
            st.session_state.error = None   # Clear previous errors
            # Use rerun to immediately reflect the spinner and disable button
            st.rerun() 

        # --- Actual Analysis Run (if state is set) ---
        # Separated this logic to run after the rerun triggered by button click
        if st.session_state.running_analysis:
            # Display spinner context outside try/finally so it disappears correctly
            with st.spinner('Processing interviews... This may take a while.'):
                try:
                    st.info(f"Starting analysis using model: {selected_model}...")
                    # Use the DataFrame stored in session state
                    aggregated_codes, interview_codes = run_analysis_pipeline(st.session_state.input_df, model=selected_model)
                    st.session_state.results = (aggregated_codes, interview_codes)
                    st.session_state.error = None # Explicitly clear error on success
                except ImportError:
                    st.session_state.error = "Backend analysis function not available."
                    st.session_state.results = None # Clear results on error
                except Exception as e:
                    st.session_state.error = f"An error occurred during analysis: {e}"
                    st.session_state.results = None # Clear results on error
                finally:
                    st.session_state.running_analysis = False # Analysis finished
                    # Rerun to update UI (remove spinner, show results link, enable buttons)
                    st.rerun()
                 
        # --- Post-Analysis Status Display --- 
        # Display messages *after* the rerun from analysis completion
        if not st.session_state.running_analysis: 
            if st.session_state.results is not None:
                 # Display success message here if results exist and not running
                 st.success("Analysis complete! View results in the 'View Results' tab.")
            elif st.session_state.error is not None:
                 # Display error message here if an error exists and not running
                 st.error(st.session_state.error)
                 
        # Info message if button is disabled because no data is loaded
        if st.session_state.input_df is None:
             st.info("Upload an Excel file to enable the 'Run Analysis' button.")
             
    with col2:
        st.subheader("Data Preview")
        if st.session_state.input_df is not None:
            st.dataframe(st.session_state.input_df, use_container_width=True, hide_index=True)
            st.caption("💡 Double-click a cell to see its full content.")
        else:
            st.info("Upload a file to see the data preview here.")

# --- Tab 2: View Results ---
with tab2:
    st.header("2. View & Download Results")

    if st.session_state.running_analysis:
         st.info("Analysis is currently running...")
    elif st.session_state.results:
        agg_codes_result, int_codes_result = st.session_state.results
        
        # --- Process Results into DataFrames ---
        try:
            # 1. Process aggregated_codes
            processed_agg = []
            for question, codes in agg_codes_result.items():
                for code in codes:
                    processed_agg.append({"Question": question, "Code": code})
            agg_df = pd.DataFrame(processed_agg)

            # 2. Process interview_codes into a matrix
            if not int_codes_result: # Handle empty results
                 int_df = pd.DataFrame(columns=['Question', 'Code'])
            else:
                interview_ids = sorted(list(int_codes_result.keys()))
                matrix_data = []
                for question, codes in agg_codes_result.items():
                    for code in sorted(codes): 
                        row = {"Question": question, "Code": code}
                        for interview_id in interview_ids:
                            interview_data = int_codes_result.get(interview_id, {})
                            question_codes = interview_data.get(question, [])
                            row[interview_id] = "✅" if code in question_codes else "-"
                        matrix_data.append(row)
                
                column_order = ['Question', 'Code'] + interview_ids
                int_df = pd.DataFrame(matrix_data, columns=column_order)

            # --- Display Processed DataFrames ---
            # st.subheader("Aggregated Codes List") # Removed display for aggregated list
            # st.dataframe(agg_df, use_container_width=True) 

            st.subheader("Interview Coding Matrix")
            st.dataframe(int_df, use_container_width=True, hide_index=True)
            st.caption("💡 Double-click a cell to see its full content.")

            # --- Download Button (Excel) ---
            try:
                output = io.BytesIO()
                # Use ExcelWriter to save multiple sheets
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    agg_df.to_excel(writer, sheet_name='Aggregated Codes', index=False)
                    int_df.to_excel(writer, sheet_name='Interview Matrix', index=False)
                
                # It's important to seek(0) after writing to the buffer
                output.seek(0) 
                
                st.download_button(
                    label="📥 Download Results (Excel)",
                    data=output,
                    file_name='coding_results.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except Exception as e:
                st.error(f"Error preparing Excel file for download: {e}")
                
        except Exception as e:
            st.error(f"Could not process or display results. Error: {e}")
            st.warning("The analysis results might not be in the expected dictionary format.")
            st.subheader("Raw Results Data:")
            st.write("Aggregated Codes Result:")
            st.write(agg_codes_result)
            st.write("Interview Codes Result:")
            st.write(int_codes_result)
            
    elif st.session_state.error: # Show error if analysis failed
         st.error(f"Analysis failed: {st.session_state.error}")
    else:
        st.info("Run an analysis from the 'Run Analysis' tab to see results here.")
