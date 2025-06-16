import os
from pathlib import Path
from dotenv import load_dotenv
import openai

print("\n=== ENVIRONMENT TESTING ===\n")

# Get current directory
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

# Construct path to .env file
env_path = Path(current_dir) / '.env'
print(f"Looking for .env file at: {env_path}")
print(f"Does .env file exist: {env_path.exists()}")

# Load environment variables from .env file with verbose output
print("\nLoading .env file...")
env_loaded = load_dotenv(dotenv_path=str(env_path), verbose=True)
print(f"Environment loaded successfully: {env_loaded}")

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

# Check if the key is loaded
if not api_key:
    print("\n❌ API key not found in .env")
else:
    # Only show first and last few characters for security
    masked_key = f"{api_key[:5]}...{api_key[-5:]}" if len(api_key) > 10 else "***"
    print(f"\n✅ API key loaded successfully: {masked_key}")

# Set API key for OpenAI
try:
    openai.api_key = api_key
    print("✅ OpenAI client configured successfully")
except Exception as e:
    print(f"❌ Error configuring OpenAI client: {str(e)}")

# Try a simple request
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("✅ API request successful")
    print("Response:", response['choices'][0]['message']['content'])
except Exception as e:
    print("❌ API request failed:", e)
