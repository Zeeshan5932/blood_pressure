import os
import sys
import streamlit as st

# Configure logging to help debug issues
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting BP Fuel AI application")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Streamlit version: {st.__version__}")

# Set up paths in a way that works for both local and cloud
try:
    # Handle both absolute and relative paths for cloud deployment
    bp_app_dir = "bp_app"  # Default to relative path for cloud
    if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bp_app")):
        bp_app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bp_app")
        logger.info(f"Using absolute path for bp_app: {bp_app_dir}")
    else:
        logger.info(f"Using relative path for bp_app: {bp_app_dir}")
    
    # Add paths to sys.path
    sys.path.insert(0, bp_app_dir)
    utils_dir = os.path.join(bp_app_dir, "utils")
    sys.path.insert(0, utils_dir)
    logger.info(f"Updated sys.path with: {bp_app_dir} and {utils_dir}")
    
    # Import main module - this redirects to bp_app/main.py
    main_path = os.path.join(bp_app_dir, "main.py")
    logger.info(f"Importing main module from: {main_path}")
    
    # To make sure we catch all errors
    try:
        with open(main_path, "r") as f:
            exec(f.read())
    except Exception as e:
        logger.error(f"Error executing main.py: {str(e)}", exc_info=True)
        st.error(f"Error running the application: {str(e)}")
        st.exception(e)
except Exception as e:
    logger.error(f"Setup error: {str(e)}", exc_info=True)
    st.error(f"Error setting up the application: {str(e)}")
    st.exception(e)
    st.info("Please check that all dependencies are installed correctly via requirements.txt")
