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

- **ImportError**: If you encounter import errors, make sure your project structure matches the one described above.
- **API Key Issues**: Verify your OpenAI API key is correctly set in the appropriate location.
- **OpenCV Issues**: If you encounter issues with OpenCV, try reinstalling with `pip install --force-reinstall opencv-python-headless`.
- **Webcam Access**: For webcam functionality, ensure your browser has permission to access the camera.

## Disclaimer

This app is for demonstration purposes only and does not provide medical advice.
