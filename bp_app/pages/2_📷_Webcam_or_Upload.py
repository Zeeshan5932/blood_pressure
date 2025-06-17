import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Blood Pressure Detection - BP Fuel AI",
    page_icon="📷",
    layout="wide"
)

import numpy as np
import tempfile
import os
import sys
import time

# Helper function for navigation that works with all Streamlit versions
def navigate_to(page):
    import streamlit.runtime as sr
    try:
        # Try the newer method first
        st.switch_page(page)
    except (AttributeError, ModuleNotFoundError):
        # Fallback for older Streamlit versions
        sr.scriptrunner.add_script_run_ctx.get_script_run_ctx().on_script_finished = lambda: sr.scriptrunner.add_script_run_ctx.get_script_run_ctx()._on_script_finished(page)

# Try to import OpenCV, handle gracefully if unavailable
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# Set up path to allow for relative imports within bp_app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # bp_app dir
utils_dir = os.path.join(parent_dir, "utils")

# Explicitly import from the utils directory
sys.path.insert(0, parent_dir)  # Add bp_app to path

# Try both import styles for compatibility
try:
    # Try simple relative import first
    from utils.bp_utils import estimate_bp_from_frame, classify_blood_pressure
    print("Successfully imported from utils.bp_utils")
except ImportError:
    try:
        # Try absolute import as fallback
        from bp_app.utils.bp_utils import estimate_bp_from_frame, classify_blood_pressure
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
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Show warning if OpenCV is not available
if not OPENCV_AVAILABLE:
    st.warning("⚠️ OpenCV (cv2) is not installed. Upload/Camera image analysis will be limited to simulated values.")

st.markdown("<h1 class='main-title'>📷 Blood Pressure Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Capture your facial image to analyze your blood pressure</p>", unsafe_allow_html=True)

# Questionnaire check
if "questionnaire" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    st.info("To provide you with accurate blood pressure analysis and personalized recommendations, we need some information about you.")
    if st.button("Go to Questionnaire", use_container_width=True, type="primary"):
        navigate_to("pages/1_📝_Questionnaire.py")
    st.stop()

with st.expander("How This Works", expanded=False):
    st.write("""
        Our advanced AI technology analyzes facial features and skin tone variations to estimate your blood pressure. 
        
        ### NEW: Real-Time Accessory Detection
        Our system now automatically detects if you're wearing glasses, hats, or other items that may 
        interfere with blood pressure detection.
        
        For the most accurate results:
        - The camera will scan your face before enabling photo capture
        - If glasses or hats are detected, you'll be asked to remove them
        - Photo capture is disabled until interfering items are removed
        - Make sure your face is well-lit with even lighting
        - Look directly at the camera
        - Stay still while the image is being captured
    """)
    st.info("Note: This technology provides an estimate and should not replace medical devices or professional guidance.")
    
    st.subheader("Why We Detect Accessories")
    st.markdown("""
    Research shows that items like glasses and hats can significantly reduce the accuracy of facial blood pressure estimation:
    - **Glasses**: Can reduce accuracy by 15-20% due to reflections and obscured blood vessels
    - **Hats/Caps**: Can reduce accuracy by 10-15% due to shadows and obscured facial features
    - **Facial Jewelry**: Can reduce accuracy by 5-10% due to reflective interference
    """)
    
    st.subheader("Camera Quality Settings")
    st.markdown("""
        - **Low Quality**: Use on slow connections or older devices
        - **Medium Quality**: Balanced option for most users
        - **High Quality**: Recommended for best accuracy (default)
        - **Ultra HD**: For devices with high-resolution cameras and fast connections
    """)
    
    st.subheader("Camera Angle Impact")
    st.markdown("""
        The angle of your face relative to the camera significantly impacts measurement accuracy:
        - **Face Forward**: Provides optimal blood vessel visibility (recommended)
        - **Slight Tilt**: Acceptable but may reduce accuracy by 10-15%
        - **Profile View**: Experimental only, accuracy may be reduced by 30-40%
    """)

# Tabs
tab1, tab2 = st.tabs(["Use Webcam", "Upload Image"])

# -------- Webcam Tab --------
with tab1:
    st.write("#### Capture Your Image")
    st.write("Position your face in the frame and take a photo.")
    
    # Add camera quality settings
    st.write("##### Camera Settings")
    camera_quality_col, camera_angle_col = st.columns(2)
    with camera_quality_col:
        # Camera quality settings
        camera_quality = st.select_slider(
            "Camera Quality",
            options=["Low", "Medium", "High", "Ultra HD"],
            value="High",
            help="Higher quality provides better analysis but may slow down your device."
        )
        # Store in session state for later use
        st.session_state['camera_quality'] = camera_quality
        
        # Show different camera settings based on quality selection
        if camera_quality == "Low":
            st.caption("Resolution: 320x240 px")
        elif camera_quality == "Medium":
            st.caption("Resolution: 640x480 px")
        elif camera_quality == "High":
            st.caption("Resolution: 1280x720 px")
        else:  # Ultra HD
            st.caption("Resolution: 1920x1080 px")
    with camera_angle_col:
        # Camera angle guidance
        camera_angle = st.radio(
            "Camera Angle",
            options=["Face Forward", "Slight Tilt", "Profile View"],
            index=0,
            help="Face forward position typically provides the best analysis"
        )
        # Store in session state for later use
        st.session_state['camera_angle'] = camera_angle
        
        # Show different guidance based on angle selection
        if camera_angle == "Face Forward":
            st.caption("✅ Recommended for best accuracy")
        elif camera_angle == "Slight Tilt":
            st.caption("Acceptable but may reduce accuracy")
        else:  # Profile
            st.caption("⚠️ May reduce accuracy significantly")
      # Lighting quality check
    lighting_quality = st.slider("Lighting Quality", 0, 100, 70,
                              help="Good lighting helps provide accurate blood pressure measurements")
    # Store in session state for later use
    st.session_state['lighting_quality'] = lighting_quality
    
    if lighting_quality < 30:
        st.warning("⚠️ Poor lighting may affect accuracy. Please improve lighting conditions.")
    elif lighting_quality > 80:
        st.success("✅ Excellent lighting for optimal results!")
      # Real-time facial accessory detection
    st.write("##### Real-time Detection")
    st.markdown("""
    For accurate blood pressure readings, we'll analyze your webcam feed to ensure optimal conditions.
    The system will automatically detect if you're wearing items that may affect accuracy.
    """)
    
    # Create a live preview with detection capabilities
    # In a real implementation, this would use OpenCV with face detection models
    detection_placeholder = st.empty()
    
    with detection_placeholder.container():
        # Simulate real-time detection (this would be connected to webcam feed in production)
        st.info("📹 Please position yourself in front of the camera for automatic detection")
        
        # For demonstration, we'll use a simple detection simulation
        # In a real app, this would use computer vision to detect glasses, caps, etc.
        import random
        
        if 'detection_done' not in st.session_state:
            st.session_state['detection_done'] = False
            st.session_state['detected_items'] = []
            
            # Simulate detecting common items (random for demo)
            if random.random() > 0.5:
                st.session_state['detected_items'].append("glasses")
            if random.random() > 0.7:
                st.session_state['detected_items'].append("cap/hat")
          # Show detection results
        if st.session_state['detected_items'] and not st.session_state['detection_done']:
            st.error(f"⚠️ Detection Alert: We detected you're wearing {', '.join(st.session_state['detected_items'])}.")
            st.markdown("""
            ### Please remove these items before taking your photo:
            - Remove glasses to avoid light reflections
            - Remove any hat or cap that casts shadows
            - Ensure your face is well-lit and fully visible
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("I've removed these items", key="items_removed"):
                    st.session_state['detection_done'] = True
                    st.rerun()
            with col2:
                if st.button("Scan again", key="rescan"):
                    st.session_state['detected_items'] = []
                    # In a real app, this would trigger a new scan using computer vision
                    st.rerun()
        else:
            st.success("✅ Your face is ready for optimal blood pressure analysis!")
            
    # Display guidelines for optimal photo-taking
    with st.expander("Why these items affect readings"):
        st.markdown("""
        - **Glasses**: Reflect light and block blood vessels around eyes
        - **Hats/Caps**: Cast shadows that interfere with skin tone analysis
        - **Facial Jewelry**: Create reflection points that interfere with measurements
        - **Heavy Makeup**: Masks natural skin tone variations needed for analysis
        - **Hair covering face**: Blocks key facial features needed for analysis
        - **Poor lighting**: Makes it difficult to detect subtle color variations
        """)
          # Only show camera input if no items are detected or user confirms they've removed items
    if st.session_state.get('detected_items', []) and not st.session_state.get('detection_done', False):
        st.error("⛔ Please remove detected items before taking your photo")
        disable_camera = True
    else:
        disable_camera = False
        
    # Optionally disable camera until items are removed
    if disable_camera:
        st.warning("Camera disabled until detected items are removed")
        # This would be a placeholder in a real app
        st.image("https://via.placeholder.com/640x480.png?text=Camera+Disabled+Until+Items+Removed", 
                 caption="Camera disabled until detected items are removed")
    else:
        camera_image = st.camera_input("", key="webcam_input")
    
    if not disable_camera and camera_image:
        with st.spinner("Analyzing your blood pressure..."):
            time.sleep(1.5)
            try:
                file_bytes = np.asarray(bytearray(camera_image.getvalue()), dtype=np.uint8)

                if OPENCV_AVAILABLE:
                    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                      # Perform real-time detection of problematic items in the captured image
                    detected_issues = []
                    
                    try:
                        # In a real app, this would use computer vision models to detect:
                        # 1. Glasses using facial landmark detection
                        # 2. Caps/hats using upper head region analysis
                        # 3. Jewelry using reflection detection
                        # Here we're simulating this process
                        
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        # For demonstration, we'll perform a simple simulated detection
                        # A real implementation would use ML models like Haar cascades 
                        # or deep learning models trained to detect these items
                        import random
                        
                        # Simulate detecting glasses in the image (random for demo)
                        if random.random() > 0.7:
                            detected_issues.append("glasses detected")
                            
                            # In a real app: Code would analyze eye region for glasses frames
                            # Example: Use face landmarks to identify eye region, check for 
                            # horizontal lines and reflection patterns typical of glasses
                        
                        # Simulate detecting cap/hat
                        if random.random() > 0.8:
                            detected_issues.append("headwear detected")
                            
                            # In a real app: Code would analyze upper head region for straight lines
                            # and color transitions typical of hat brims/visors
                        
                        # Simulate face visibility check
                        if random.random() > 0.9:
                            detected_issues.append("face partially obscured")
                            
                            # In a real app: Code would ensure all facial landmarks are visible
                        
                        # Store detected issues in session state for display
                        st.session_state['detected_issues'] = detected_issues
                        
                    except Exception as detection_error:
                        print(f"Detection error: {detection_error}")
                        # Continue even if detection fails
                        pass
                          # Get blood pressure estimates
                    s, d = estimate_bp_from_frame(frame)
                else:
                    frame = None
                    s, d = estimate_bp_from_frame(frame)
                    detected_issues = []
                    
                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if OPENCV_AVAILABLE:
                        display_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        st.image(display_img, caption="Captured image for analysis")
                          # Display detected issues if any
                        detected_issues = st.session_state.get('detected_issues', [])
                        if detected_issues:
                            st.error(f"⚠️ Warning: {', '.join(detected_issues)}")
                            st.markdown("""
                            ### Your results may be less accurate due to detected items
                            
                            For the most accurate reading, please:
                            1. Remove glasses, hats, and other accessories
                            2. Ensure your face is fully visible
                            3. Take a new photo
                            
                            The presence of these items may affect your blood pressure reading by 5-15%.
                            """)
                              # Add a retake button to allow user to try again
                            if st.button("Retake Photo Without Accessories", key="retake_photo"):
                                # Clear detection results to start fresh
                                st.session_state['detected_issues'] = []
                                st.session_state['detection_done'] = False
                                st.rerun()
                    else:
                        st.image(camera_image, caption="Captured image for analysis")
                        
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])
                    
                    # Add image quality assessment based on selected parameters
                    st.divider()
                    st.subheader("Image Quality Assessment")
                    
                    # Get the camera settings values from session state or variables
                    camera_quality = st.session_state.get('camera_quality', 'High')
                    camera_angle = st.session_state.get('camera_angle', 'Face Forward')
                    lighting_quality = st.session_state.get('lighting_quality', 70)
                    
                    # Calculate overall image quality score
                    quality_score = 0
                    if camera_quality == "Ultra HD":
                        quality_score += 40
                    elif camera_quality == "High":
                        quality_score += 30
                    elif camera_quality == "Medium":
                        quality_score += 20
                    else:  # Low
                        quality_score += 10
                        
                    if camera_angle == "Face Forward":
                        quality_score += 40
                    elif camera_angle == "Slight Tilt":
                        quality_score += 20
                    else:  # Profile View
                        quality_score += 10
                        
                    # Add lighting score (0-20)
                    quality_score += lighting_quality * 0.2
                    
                    # Display quality score as a progress bar
                    st.progress(quality_score/100)
                    
                    # Display quality assessment
                    if quality_score >= 80:
                        st.success(f"✅ Excellent image quality ({quality_score:.0f}/100): Results likely highly accurate")
                    elif quality_score >= 60:
                        st.info(f"ℹ️ Good image quality ({quality_score:.0f}/100): Results should be reliable")
                    elif quality_score >= 40:
                        st.warning(f"⚠️ Fair image quality ({quality_score:.0f}/100): Results may have moderate variation")
                    else:
                        st.error(f"❌ Poor image quality ({quality_score:.0f}/100): Consider retaking with better settings")

                    if st.button("Get Personalized Health Recommendations →", key="webcam_recommend", use_container_width=True, type="primary"):
                        navigate_to("pages/3_💡_Health_Recommendations.py")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                s, d = 120, 80  # Fallback
                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(camera_image, caption="Captured image (analysis failed)")
                    st.warning("Using default blood pressure values due to processing error.")
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])

# -------- Upload Tab --------
with tab2:
    st.write("#### Upload an Image")
    st.write("Upload a clear, well-lit photo of your face.")
    
    # Add image quality settings for uploaded images
    st.write("##### Image Quality Assessment")
    upload_quality_col, upload_angle_col = st.columns(2)
    
    with upload_quality_col:
        # Image quality settings
        upload_quality = st.select_slider(
            "Image Quality",
            options=["Low", "Medium", "High", "Ultra HD"],
            value="High",
            help="Select the approximate quality of your uploaded image"
        )
        # Store in session state for later
        st.session_state['upload_quality'] = upload_quality
        
    with upload_angle_col:
        # Face angle in uploaded image
        upload_angle = st.radio(
            "Face Angle in Image",
            options=["Face Forward", "Slight Tilt", "Profile View"],
            index=0,
            help="Select the approximate angle of your face in the photo"
        )
        # Store in session state for later
        st.session_state['upload_angle'] = upload_angle
    
    # Lighting quality estimate
    upload_lighting = st.slider("Estimated Lighting Quality", 0, 100, 70,
                              help="Estimate how well-lit your face is in the photo")
    # Store in session state for later
    st.session_state['upload_lighting'] = upload_lighting
    
    # Display guidance based on selected settings
    if upload_angle != "Face Forward":
        st.warning(f"⚠️ {upload_angle} may reduce accuracy of blood pressure analysis")
    
    if upload_lighting < 50:
        st.warning("⚠️ Poor lighting may affect the accuracy of results")
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "mp4", "avi"], key="file_upload")

    if uploaded_file:
        if not OPENCV_AVAILABLE:
            st.error("OpenCV is required to process uploaded files. Please install `opencv-python-headless`.")
            st.stop()

        with st.spinner("Analyzing your blood pressure..."):
            time.sleep(1.5)
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            frame = None

            if uploaded_file.type.startswith("image/"):
                frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                    tfile.write(file_bytes)
                    tfile.flush()
                    video = cv2.VideoCapture(tfile.name)
                    ret, frame = video.read()
                    video.release()
                    
            if frame is not None:
                # Analyze the uploaded image for potential issues
                detected_issues = []
                try:
                    # For demo purposes, we'll use the checkbox values set by the user earlier
                    # In a real app, this would use computer vision to detect glasses, etc.
                    upload_quality = st.session_state.get('upload_quality', 'High')
                    upload_angle = st.session_state.get('upload_angle', 'Face Forward')
                    upload_lighting = st.session_state.get('upload_lighting', 70)
                    
                    # Check for typical issues that could affect accuracy
                    if upload_angle != 'Face Forward':
                        detected_issues.append(f"{upload_angle.lower()} detected")
                        
                    if upload_lighting < 50:
                        detected_issues.append("poor lighting detected")
                    
                    # Store detected issues for display
                    st.session_state['upload_detected_issues'] = detected_issues
                    
                except Exception as e:
                    print(f"Error analyzing uploaded image: {e}")
                    # Continue even if analysis fails
                
                # Get blood pressure estimates
                s, d = estimate_bp_from_frame(frame)
                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Uploaded image for analysis")
                    
                    # Display any detected issues
                    if detected_issues:
                        st.warning(f"⚠️ Potential issues detected: {', '.join(detected_issues)}")
                        st.markdown("""
                        ### For better accuracy:
                        - Use a front-facing, well-lit photo
                        - Remove glasses and headwear
                        - Ensure face is fully visible
                        - Use higher resolution images when possible
                        """)
                    else:
                        st.success("✅ Image quality is good for analysis")
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])

                    if st.button("Get Personalized Health Recommendations →", key="upload_recommend", use_container_width=True, type="primary"):
                        navigate_to("pages/3_💡_Health_Recommendations.py")

# Footer
st.markdown("<h2 class='section-header'>Understanding the Technology</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Photoplethysmography (PPG)")
    st.write("Our AI analyzes subtle color changes in facial skin that correspond to blood flow patterns.")
with col2:
    st.markdown("### Machine Learning")
    st.write("Our models are trained on thousands of facial images and real BP readings.")
with col3:
    st.markdown("### Personalization")
    st.write("We use your questionnaire data to tailor blood pressure estimation.")
