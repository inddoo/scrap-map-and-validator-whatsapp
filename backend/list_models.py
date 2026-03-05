"""
List available Gemini models
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found!")
    exit(1)

print("Connecting to Gemini API...")
client = genai.Client(api_key=api_key)

print("\n" + "="*60)
print("Available Models:")
print("="*60)

try:
    models = client.models.list()
    for model in models:
        print(f"\n📦 {model.name}")
        if hasattr(model, 'display_name'):
            print(f"   Display: {model.display_name}")
        if hasattr(model, 'description'):
            print(f"   Description: {model.description}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying alternative method...")
    
    # Try direct API call
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        
        for model in models:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', '')
            methods = model.get('supportedGenerationMethods', [])
            
            if 'generateContent' in methods:
                print(f"\n✅ {name}")
                print(f"   Display: {display_name}")
                print(f"   Methods: {', '.join(methods)}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)

print("\n" + "="*60)
