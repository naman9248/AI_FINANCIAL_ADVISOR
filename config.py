import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY is not set. Please set it in your .env file.")

# Other configuration variables can be added here
APP_TITLE = "AI Financial Advisor"
APP_DESCRIPTION = "Your personal AI-powered financial assistant."
