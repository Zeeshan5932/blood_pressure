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
    # First, identify the project root directory 
    project_root = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"Project root: {project_root}")
    
    # Make sure our project root is in sys.path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        logger.info(f"Added project root to sys.path")
    
    # Clear out any existing 'utils' from sys.path to avoid confusion with cv2.utils
    sys.path = [p for p in sys.path if not p.endswith('utils')]
    
    # Import main module from bp_app directory
    logger.info("Importing main module...")
    
    # Print out the current sys.path for debugging
    logger.info(f"sys.path: {sys.path}")
    
    # Try to run the main app
    try:
        # Execute the main.py file directly using a direct reference
        main_file = os.path.join(project_root, "bp_app", "main.py")
        logger.info(f"Executing main file from: {main_file}")
        
        # Use execfile-like behavior to run the main module
        with open(main_file, "r") as f:
            code = compile(f.read(), main_file, 'exec')
            exec(code, globals())
    except Exception as e:
        logger.error(f"Error executing main.py: {str(e)}", exc_info=True)
        st.error("⚠️ Error running the application")
        st.exception(e)
        
        # Show more debug info
        st.info("Debug information:")
        st.code(f"Working directory: {os.getcwd()}")
        st.code(f"Python path: {sys.path}")
        
        # Try to show existing modules for debugging
        try:
            import pkgutil
            modules = [m for _, m, _ in pkgutil.iter_modules()]
            st.code(f"Available modules: {modules[:20]}...")
        except:
            pass
            
except Exception as e:
    logger.error(f"Setup error: {str(e)}", exc_info=True)
    st.error("⚠️ Error setting up the application")
    st.exception(e)
    st.info("Please check that all dependencies are installed correctly via requirements.txt")
