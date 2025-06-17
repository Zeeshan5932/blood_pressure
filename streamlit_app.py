import os
import sys
import streamlit as st

"""
BP Fuel AI - Main Entry Point
This is the entry point for the BP Fuel AI application. It:
1. Sets up the Python import path for the application
2. Loads environment variables and API keys from Streamlit secrets
3. Redirects to the main application file
"""

# Show that we're loading
st.set_page_config(page_title="BP Fuel AI", page_icon="❤️")

# Automatically load OpenAI API key from Streamlit secrets (if available)
# This handles both Streamlit Cloud and local development with secrets.toml
try:
    if hasattr(st, 'secrets') and 'openai' in st.secrets and st.secrets['openai'].get('api_key'):
        print("Loading API key from Streamlit secrets")
        os.environ["OPENAI_API_KEY"] = st.secrets['openai']['api_key']
        print("API key loaded successfully from Streamlit secrets")
    # No else case - we don't need warning messages here as we'll handle them in the app
except Exception as e:
    print(f"Error loading API key from secrets: {e}")

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
