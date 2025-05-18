import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

print("\nAvailable Gemini Models for Your API Key:")
for m in models:
    print("-", m.name)
