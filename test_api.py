import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Testing API Connection
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Hello Gemini! Test connection successful.")
    print(response.text)
else:
    print("Error: Please set your GEMINI_API_KEY in the .env file first to run this test.")
