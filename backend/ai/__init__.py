from .gemini_service import GeminiService, get_gemini_service
from .groq_service import GroqService, get_groq_service
import os

# Determine which AI service to use based on available API keys
def get_ai_service():
    """Get available AI service (Groq or Gemini)"""
    groq_key = os.getenv('GROQ_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    # Prefer Groq if available (faster and more quota)
    if groq_key:
        try:
            return get_groq_service()
        except Exception as e:
            print(f"⚠️ Groq service failed to initialize: {e}")
    
    # Fallback to Gemini
    if gemini_key:
        try:
            return get_gemini_service()
        except Exception as e:
            print(f"⚠️ Gemini service failed to initialize: {e}")
    
    raise ValueError("No AI service available. Please set GROQ_API_KEY or GEMINI_API_KEY in .env")

__all__ = ['GeminiService', 'get_gemini_service', 'GroqService', 'get_groq_service', 'get_ai_service']
