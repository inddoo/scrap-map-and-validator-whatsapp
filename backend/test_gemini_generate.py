"""
Test Gemini content generation
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found!")
    exit(1)

print("Testing Gemini 2.5 Flash...")
client = genai.Client(api_key=api_key)
model_name = 'models/gemini-2.5-flash'

try:
    print(f"\nModel: {model_name}")
    print("Generating content...")
    
    response = client.models.generate_content(
        model=model_name,
        contents="Buatkan salam singkat untuk WhatsApp dalam 2 kalimat saja."
    )
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"\nGenerated text:\n{response.text}")
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTrying alternative model: gemini-flash-latest")
    
    try:
        response = client.models.generate_content(
            model='models/gemini-flash-latest',
            contents="Buatkan salam singkat untuk WhatsApp dalam 2 kalimat saja."
        )
        
        print("\n" + "="*60)
        print("✅ SUCCESS with gemini-flash-latest!")
        print("="*60)
        print(f"\nGenerated text:\n{response.text}")
        print("\n" + "="*60)
        print("\n💡 Use 'models/gemini-flash-latest' in gemini_service.py")
        
    except Exception as e2:
        print(f"\n❌ Also failed: {e2}")
