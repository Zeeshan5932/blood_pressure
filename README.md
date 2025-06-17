# BP Fuel AI - Blood Pressure Management System

A Streamlit application that estimates blood pressure using computer vision and provides AI-powered personalized health recommendations.

## Features

- Webcam-based blood pressure estimation
- Comprehensive health questionnaire
- AI-powered personalized health recommendations using OpenAI
- Interactive and modern user interface
- Educational blood pressure information
- Health tracking tools

## Requirements

- Python 3.9+ (3.11 recommended)
- OpenCV
- Streamlit 1.27.0+
- NumPy
- OpenAI API key
- python-dotenv

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/BP-Fuel-AI.git
   cd BP-Fuel-AI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - For local development:
     - Create a `.env` file in the project root directory
     - Add your OpenAI API key to the `.env` file:
       ```
       OPENAI_API_KEY=your_openai_api_key_here
       ```
   - For Streamlit Cloud deployment:
     - Add the API key in the Streamlit Cloud dashboard under "Settings" > "Secrets"
     - Use this format:
       ```toml
       [openai]
       api_key = "your_openai_api_key_here"
       ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Navigate through the application:
   - Fill out the health questionnaire
   - Get your blood pressure reading using webcam or by uploading an image
   - View personalized AI-generated health recommendations
   
3. Allow webcam access when prompted for blood pressure detection

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository

2. Connect your repository to Streamlit Cloud

3. Configure the deployment:
   - Set the main file path to `streamlit_app.py`
   - Add your OpenAI API key in the "Secrets" section
   - Use the format specified in the Installation section
   
4. Deploy the app

## Project Structure

```
BP-Fuel-AI/
├── .streamlit/              # Streamlit configuration
│   ├── config.toml          # Configuration for Streamlit
│   └── secrets.toml         # Local secrets for development
│
├── bp_app/                  # Main application code
│   ├── assets/              # CSS and other static assets
│   │   └── styles.css       # Custom styles for the app
│   │
│   ├── pages/               # Streamlit pages
│   │   ├── __init__.py      # Makes the directory a Python package
│   │   ├── 1_📝_Questionnaire.py
│   │   ├── 2_📷_Webcam_or_Upload.py
│   │   └── 3_💡_Health_Recommendations.py
│   │
│   ├── utils/               # Utility functions
│   │   ├── __init__.py      # Makes the directory a Python package
│   │   └── bp_utils.py      # Blood pressure utility functions
│   │
│   ├── __init__.py          # Makes the directory a Python package
│   └── main.py              # Main application code
│
├── .env                     # Environment variables (local only, not committed)
├── .gitignore               # Files to ignore in Git
├── packages.txt             # System-level dependencies for Streamlit Cloud
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python runtime specification
└── streamlit_app.py         # Entry point for the application
```

## Troubleshooting

### OpenAI API Key Issues

If you see the error: "⚠️ OpenAI API key not found. Using default recommendations instead.", follow these steps:

#### For Local Development:

1. Create a `.env` file in the project root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Alternatively, create a `.streamlit/secrets.toml` file:
   ```toml
   [openai]
   api_key = "your_openai_api_key_here"
   ```
   You can copy the template from `secrets.toml.template`

3. Make sure you have installed all requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Restart the Streamlit app

#### For Streamlit Cloud Deployment:

1. In your Streamlit Cloud dashboard, go to "Settings" > "Secrets"

2. Add your OpenAI API key in this format:
   ```toml
   [openai]
   api_key = "your_openai_api_key_here"
   ```

3. Save your secrets and redeploy the app

### Import Errors

If you see any import errors:

1. Make sure your project structure matches exactly:
   ```
   BP-Fuel-AI/
   ├── bp_app/
   │   ├── __init__.py  # Important!
   │   ├── utils/
   │   │   ├── __init__.py  # Important!
   │   │   └── bp_utils.py
   ```

2. Try running with debug output:
   ```bash
   streamlit run streamlit_app.py --logger.level=debug
   ```

### OpenCV Issues

If OpenCV is causing problems:

1. Try reinstalling with:
   ```bash
   pip uninstall opencv-python opencv-python-headless
   pip install opencv-python-headless==4.6.0.66
   ```

2. Make sure your system has the necessary dependencies (on Linux):
   ```bash
   apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
   ```

### Webcam Access

For webcam functionality, ensure your browser has permission to access the camera.

## Disclaimer

This app is for demonstration purposes only and does not provide medical advice.
