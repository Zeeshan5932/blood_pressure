import os
import sys
import streamlit as st

# Print the current working directory for debugging
st.write(f"Current working directory: {os.getcwd()}")

# Add the bp_app directory to the path using robust path handling
bp_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bp_app")
sys.path.append(bp_app_path)

# Import the main module from bp_app
try:
    # Instead of executing the file, we'll import the bp_app as a module
    # This is safer and more reliable for Streamlit Cloud
    
    # First make sure our utils module can be found
    utils_path = os.path.join(bp_app_path, "utils")
    if utils_path not in sys.path:
        sys.path.append(utils_path)
    
    # Then import and run our main module
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", os.path.join(bp_app_path, "main.py"))
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)
except Exception as e:
    st.error(f"Error running the application: {e}")
    st.exception(e)  # This will show the full stack trace
    st.info("Please check that all dependencies are installed correctly via requirements.txt")
