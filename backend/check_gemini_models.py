"""
Check available Gemini models for your API key
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit(1)

print(f"✅ API Key: {api_key[:20]}...")
print("\nConfiguring Gemini...")

try:
    genai.configure(api_key=api_key)
    print("✅ Configured successfully\n")
    
    print("Available models:")
    print("="*60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:80]}...")
            print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
