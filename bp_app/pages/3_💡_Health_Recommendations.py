import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Health Recommendations - BP Fuel AI",
    page_icon="💡",
    layout="wide"
)

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Import utilities for API key handling
from utils.bp_utils import get_openai_api_key

# Set up a more robust environment variable loading process
print("Health Recommendations page: Initializing API key handling")

# First, try to load directly from environment
api_key_found = False
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    api_key_found = True
    print("Health Recommendations page: API key already found in environment variables")
else:
    # Load environment variables using the robust function from bp_utils
    print("Health Recommendations page: Attempting to load API key from all sources")
    api_key = get_openai_api_key()
    api_key_found = bool(api_key)

# Try loading from .env file in multiple locations as a fallback
if not api_key_found:
    print("Health Recommendations page: Trying multiple .env file locations")
    # Try multiple possible locations for the .env file
    possible_locations = [
        Path(__file__).parent.parent.parent / '.env',  # project root
        Path(__file__).parent.parent / '.env',         # bp_app directory
        Path.cwd() / '.env',                          # current working directory
    ]
    
    for env_path in possible_locations:
        print(f"Health Recommendations page: Looking for .env file at: {env_path}")
        if env_path.exists():
            print(f"Health Recommendations page: Found .env file at: {env_path}")
            try:
                # Force reload the environment variables
                load_dotenv(dotenv_path=str(env_path), override=True)
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    api_key_found = True
                    print(f"Health Recommendations page: Successfully loaded API key from {env_path}")
                    break
            except Exception as e:
                print(f"Health Recommendations page: Error loading .env file: {str(e)}")
    
# Final check for Streamlit secrets as a last resort
if not api_key_found and hasattr(st, 'secrets'):
    try:
        if 'openai' in st.secrets and st.secrets['openai'].get('api_key'):
            os.environ["OPENAI_API_KEY"] = st.secrets['openai']['api_key']
            api_key = st.secrets['openai']['api_key']
            api_key_found = True
            print("Health Recommendations page: Successfully loaded API key from Streamlit secrets")
    except Exception as e:
        print(f"Health Recommendations page: Error accessing Streamlit secrets: {str(e)}")

# Log final status
if api_key_found:
    masked_key = f"{api_key[:3]}...{api_key[-3:]}" if api_key and len(api_key) > 6 else "***"
    print(f"Health Recommendations page: Final status - API key found: {masked_key}")
else:
    print("Health Recommendations page: Final status - API key NOT found in any location")

# Try to import OpenCV, but don't fail if it's not available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    # We'll handle missing OpenCV gracefully as we're mainly using it for display in this page

# Set up path to allow for relative imports within bp_app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # bp_app dir
utils_dir = os.path.join(parent_dir, "utils")

# Explicitly import from the utils directory
sys.path.insert(0, parent_dir)  # Add bp_app to path

# Try both import styles for compatibility
try:
    # Try simple relative import first
    from utils.bp_utils import classify_blood_pressure, get_openai_recommendations, get_default_recommendations
    print("Successfully imported from utils.bp_utils")
except ImportError:
    try:
        # Try absolute import as fallback
        from bp_app.utils.bp_utils import classify_blood_pressure, get_openai_recommendations, get_default_recommendations
        print("Successfully imported from bp_app.utils.bp_utils")
    except ImportError as e:
        # Show helpful error information
        print(f"Import error: {str(e)}")
        print(f"Python path: {sys.path}")
        print(f"Parent directory: {parent_dir}")
        print(f"Utils directory: {utils_dir}")
        print(f"Current directory: {current_dir}")
        # Re-raise to show the error in the UI
        raise

# Load custom CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>💡 Health Recommendations</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Personalized recommendations based on your blood pressure</p>", unsafe_allow_html=True)

# Check for session state data
if 'questionnaire' not in st.session_state or 'bp_result' not in st.session_state:
    st.warning("Please complete the questionnaire and blood pressure detection first!")
    st.markdown("""
    <div class="info-card">
        <h2>How to get your recommendations:</h2>
        <ol>
            <li>First, fill out the questionnaire in the 📝 Questionnaire page</li>
            <li>Then, get your blood pressure reading in the 📷 Webcam or Upload page</li>
            <li>Come back to this page for your personalized recommendations</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Display blood pressure reading
q = st.session_state['questionnaire']
systolic, diastolic = st.session_state['bp_result']

bp_classification = classify_blood_pressure(systolic, diastolic)

# Convert questionnaire data to the format expected by the AI recommendation function
user_info = {
    "age": q.get('age', 30),
    "gender": q.get('gender', 'Not specified'),
    "weight": q.get('weight', 'Not specified'),
    "height": q.get('height', 'Not specified'),
    "medical_conditions": q.get('prev_conditions', []),
    "medications": q.get('medications', []),
    "activity_level": q.get('exercise', 'moderate'),
    "diet": q.get('diet', 'Not specified')
}

# Display blood pressure results in a card
st.markdown(f"""
<div class="info-card">
    <h2>Your Blood Pressure Reading</h2>
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 2.5rem; font-weight: bold; color: {bp_classification['color']};">
            {systolic}/{diastolic} <span style="font-size: 1.2rem;">mmHg</span>
        </div>
        <div style="margin-left: 30px; padding-left: 30px; border-left: 1px solid #e0e0e0;">
            <div style="font-weight: bold; font-size: 1.3rem; color: {bp_classification['color']};">{bp_classification['category']}</div>
            <div>{bp_classification['description']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Setup progress tabs to show the user what's happening
tab1, tab2 = st.tabs(["AI-Powered Recommendations", "What This Means"])

with tab1:
    with st.container():
        st.markdown("<h2 class='section-header'>Your Personalized Health Plan</h2>", unsafe_allow_html=True)        # Check API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Try one more time with the utility function if needed
        if not api_key:
            api_key = get_openai_api_key()
            api_key_found = bool(api_key)
        
        # Only show success icon if API key is found, don't show warnings
        if api_key_found:
            st.sidebar.success("✅ Using AI-powered recommendations")
        
        # Generate recommendations based on API key availability
        if not api_key:
            # Use default recommendations without showing warnings
            print("API key not found, using default recommendations")
            recommendations = get_default_recommendations(bp_classification["category"])
            
            # Optional: Users who need to debug can expand this section
            with st.expander("Advanced: API Configuration"):
                st.info("Using standard recommendations. For personalized AI recommendations, an OpenAI API key is needed.")
                
                # Check if Streamlit secrets is configured correctly
                if hasattr(st, 'secrets'):
                    if 'openai' in st.secrets:
                        if 'api_key' in st.secrets['openai']:
                            if st.secrets['openai']['api_key']:
                                st.success("API key found in Streamlit secrets but not accessible. Try restarting the app.")
                            else:
                                st.warning("API key in Streamlit secrets is empty.")
                        else:
                            st.warning("'api_key' missing from 'openai' section in secrets.")
                    else:
                        st.warning("'openai' section missing from secrets configuration.")
                else:
                    st.warning("Streamlit secrets are not available.")
              # Use default recommendations since we can't use OpenAI
            recommendations = get_default_recommendations(bp_classification["category"])
        else:
            st.success("✅ Using OpenAI API for personalized recommendations")
            # Create a spinner while recommendations are generating
            with st.spinner("Generating personalized AI recommendations based on your data..."):
                # We'll use asyncio to handle the async OpenAI call
                try:
                    # Make sure we set the API key correctly for OpenAI
                    os.environ["OPENAI_API_KEY"] = api_key
                    
                    # Create a new asyncio event loop for the OpenAI API call
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Log that we're about to call OpenAI
                    print("Health Recommendations page: Calling OpenAI API for recommendations")
                    recommendations = loop.run_until_complete(get_openai_recommendations(bp_classification, user_info))
                    
                    # Check if there was an error with the OpenAI call
                    if "error" in recommendations:
                        st.warning(f"OpenAI API error: {recommendations['error']}")
                        print(f"Health Recommendations page: OpenAI API error: {recommendations['error']}")
                        # Fallback to default recommendations
                        recommendations = get_default_recommendations(bp_classification["category"])
                    else:
                        print("Health Recommendations page: Successfully got OpenAI recommendations")
                        
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"Error generating OpenAI recommendations: {error_msg}")
                    print(f"Health Recommendations page: Exception during OpenAI call: {error_msg}")
                    
                    # Show detailed error information
                    with st.expander("Error Details"):
                        st.code(error_msg)
                        import traceback
                        st.code(traceback.format_exc())
                    
                    # Fallback to default recommendations
                    recommendations = get_default_recommendations(bp_classification["category"])
        
        # Display the diet recommendations
        st.markdown("""
        <div class="recommendation-card">
            <h3 class="recommendation-header">🥗 Diet Recommendations</h3>
        """, unsafe_allow_html=True)
        
        for item in recommendations["diet"]:
            st.markdown(f"- {item}")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display the exercise recommendations
        st.markdown("""
        <div class="recommendation-card">
            <h3 class="recommendation-header">🏃‍♂️ Exercise Recommendations</h3>
        """, unsafe_allow_html=True)
        
        for item in recommendations["exercise"]:
            st.markdown(f"- {item}")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display the lifestyle recommendations
        st.markdown("""
        <div class="recommendation-card">
            <h3 class="recommendation-header">🧘‍♀️ Lifestyle Recommendations</h3>
        """, unsafe_allow_html=True)
        
        for item in recommendations["lifestyle"]:
            st.markdown(f"- {item}")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add a disclaimer
        st.markdown("""
        <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; font-size: 0.9rem;">
            <strong>Disclaimer:</strong> These recommendations are generated for informational purposes only and do not constitute medical advice. 
            Always consult with a healthcare professional before making significant changes to your diet, exercise routine, or medication.
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="info-card">
        <h2>Understanding Your Blood Pressure Reading</h2>
        
        <h3>What is {bp_classification['category']}?</h3>
        <p>{bp_classification['description']}</p>
        
        <h3>What This Means For You</h3>
        <p>Blood pressure categories help determine the level of care needed. Your reading is classified as <span class="{bp_classification['class']}">{bp_classification['category']}</span>, which indicates a {bp_classification['risk_level']} risk level for cardiovascular issues.</p>
        
        <h3>Next Steps</h3>
    """, unsafe_allow_html=True)
    
    if bp_classification['alert']:
        st.markdown("""
        <p>Based on your blood pressure reading, it's important to:</p>
        <ul>
            <li>Follow up with a healthcare provider soon</li>
            <li>Monitor your blood pressure regularly</li>
            <li>Follow the personalized recommendations provided</li>
        </ul>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p>Based on your blood pressure reading, it's important to:</p>
        <ul>
            <li>Continue monitoring your blood pressure periodically</li>
            <li>Maintain a healthy lifestyle</li>
            <li>Follow the personalized recommendations provided</li>        </ul>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add educational content about blood pressure using Streamlit native components
    with st.expander("Blood Pressure Education", expanded=True):
        st.subheader("What is Blood Pressure?")
        st.write("Blood pressure is the force of blood pushing against the walls of your arteries. It's measured using two numbers:")
        st.write("- **Systolic** (top number): The pressure when your heart beats")
        st.write("- **Diastolic** (bottom number): The pressure when your heart rests between beats")
        
        st.subheader("Blood Pressure Categories")
        
        # Using a Pandas DataFrame for better table presentation if available, otherwise use a simple list
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
            
            bp_categories = pd.DataFrame({
                "Category": ["Low Blood Pressure", "Normal", "Elevated", "Hypertension Stage 1", 
                            "Hypertension Stage 2", "Hypertensive Crisis"],
                "Systolic (mmHg)": ["Lower than 90", "Less than 120", "120-129", "130-139", 
                                "140 or higher", "Higher than 180"],
                "Diastolic (mmHg)": ["Lower than 60", "Less than 80", "Less than 80", "80-89", 
                                    "90 or higher", "Higher than 120"]
            })
            
            # Display the table with Streamlit's built-in table styling
            st.table(bp_categories)
            
        except ImportError:
            # Fallback if pandas is not available
            st.warning("Pandas is not installed. Displaying simplified blood pressure categories.")
            
            st.write("**Low Blood Pressure**: Systolic < 90 mmHg | Diastolic < 60 mmHg")
            st.write("**Normal**: Systolic < 120 mmHg | Diastolic < 80 mmHg")
            st.write("**Elevated**: Systolic 120-129 mmHg | Diastolic < 80 mmHg")
            st.write("**Hypertension Stage 1**: Systolic 130-139 mmHg | Diastolic 80-89 mmHg")
            st.write("**Hypertension Stage 2**: Systolic ≥ 140 mmHg | Diastolic ≥ 90 mmHg")
            st.write("**Hypertensive Crisis**: Systolic > 180 mmHg | Diastolic > 120 mmHg")

# Add a PDF download button
with st.expander("Download your personalized health plan"):
    st.write("Generate a PDF with your personalized recommendations to save or print.")
    
    if st.button("Generate PDF Report"):
        st.info("This feature would generate a downloadable PDF with all your personalized recommendations and blood pressure information.")
        # In a real application, you would generate a PDF here

# Add a tracking section
st.markdown("<h2 class='section-header'>Track Your Progress</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="info-card">
    <p>Regular tracking of your blood pressure can help you see trends and the effectiveness of lifestyle changes.</p>
    <p>Set a reminder to check your blood pressure and come back to update your readings.</p>
</div>
""", unsafe_allow_html=True)

# Create columns for the calendar
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3>Blood Pressure Log</h3>", unsafe_allow_html=True)
    st.line_chart({
        'Systolic': [120, 118, 122, 119, systolic],
        'Diastolic': [80, 79, 82, 78, diastolic]
    })

with col2:
    st.markdown("<h3>Set a Reminder</h3>", unsafe_allow_html=True)
    reminder_date = st.date_input("Next check-up date")
    reminder_time = st.time_input("Reminder time")
    
    if st.button("Set Reminder"):
        st.success(f"Reminder set for {reminder_date} at {reminder_time}!")
        # In a real app, this would set an actual reminder
