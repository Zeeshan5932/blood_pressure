import os
import sys
import streamlit as st

"""
BP Fuel AI - Main Entry Point
This is the entry point for the BP Fuel AI application. It:
1. Sets up the Python import path for the application
2. Redirects to the main application file
"""

# Show that we're loading
st.set_page_config(page_title="BP Fuel AI", page_icon="❤️")
with st.spinner("Loading BP Fuel AI..."):
    try:
        # Make the project directory structure available for imports
        # This works both locally and on Streamlit Cloud
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ensure current directory is in path
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import and run the main module directly
        # This avoids path issues as we're using the module system
        from bp_app.main import run_app
        run_app()
        
    except Exception as e:
        st.error("❌ Error loading application")
        st.exception(e)
        st.info("Please make sure all dependencies are installed: `pip install -r requirements.txt`")
