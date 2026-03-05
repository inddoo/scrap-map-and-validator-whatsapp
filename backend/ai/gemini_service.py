"""
Gemini AI Service for message generation and auto-responder
"""
import os
from google import genai
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize new Google GenAI client
        self.client = genai.Client(api_key=api_key)
        # Use Gemini Flash Latest - automatically uses the latest stable flash model
        # This has better quota limits and avoids model-specific quota issues
        self.model_name = 'models/gemini-flash-latest'
    
    def generate_personalized_message(
        self, 
        template: str, 
        data: Dict[str, str],
        context: Optional[str] = None
    ) -> str:
        """
        Generate personalized message based on template and CSV data
        
        Args:
            template: Message template or instruction
            data: Dictionary containing CSV row data (name, company, etc.)
            context: Additional context for message generation
        
        Returns:
            Generated personalized message
        """
        # Build prompt for Gemini
        context_section = ""
        if context:
            context_section = f"Konteks tambahan: {context}"
        
        prompt = f"""Kamu adalah asisten yang membantu membuat pesan WhatsApp yang personal dan profesional.

Data penerima:
{self._format_data(data)}

Template/Instruksi:
{template}

{context_section}

Buatkan pesan WhatsApp yang:
1. Personal dan menyapa nama penerima
2. Sesuai dengan data yang diberikan
3. Profesional namun ramah
4. Terstruktur dengan paragraf yang jelas (gunakan line break antar paragraf)
5. Tidak terlalu panjang (maksimal 3-4 paragraf)
6. JANGAN gunakan emoji atau karakter khusus
7. Gunakan teks biasa saja

Format:
- Salam pembuka (1 baris)
- [baris kosong]
- Paragraf 1: Perkenalan/konteks
- [baris kosong]
- Paragraf 2: Penawaran/isi utama
- [baris kosong]
- Paragraf 3: Call to action/penutup

Berikan HANYA teks pesan, tanpa penjelasan tambahan."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "resource_exhausted" in error_msg:
                print(f"⚠️ Gemini API quota exceeded! Using fallback template.")
                print(f"   Error: {e}")
                print(f"   Tip: Quota resets in 24 hours or upgrade to paid plan.")
            else:
                print(f"Error generating message: {e}")
            # Fallback to simple template replacement
            return self._simple_template_replace(template, data)
    
    def generate_auto_response(
        self,
        incoming_message: str,
        sender_data: Dict[str, str],
        response_prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate auto response based on incoming message
        
        Args:
            incoming_message: Message received from contact
            sender_data: Data about the sender (from CSV)
            response_prompt: Instructions for how to respond
            conversation_history: Previous messages in conversation
        
        Returns:
            Generated response message
        """
        # Build conversation context
        history_text = ""
        if conversation_history:
            history_text = "\n".join([
                f"{'Saya' if msg['role'] == 'bot' else 'Mereka'}: {msg['message']}"
                for msg in conversation_history[-5:]  # Last 5 messages
            ])
        
        # Build prompt parts
        history_section = ""
        if history_text:
            history_section = f"Riwayat percakapan:\n{history_text}\n"
        
        prompt = f"""Kamu adalah asisten WhatsApp Business yang membantu merespons pesan pelanggan.

Data pelanggan:
{self._format_data(sender_data)}

Petunjuk responden:
{response_prompt}

{history_section}
Pesan masuk dari pelanggan:
"{incoming_message}"

Buatkan balasan yang:
1. Sesuai dengan petunjuk responden yang diberikan
2. Menjawab pertanyaan atau merespons pesan dengan tepat
3. Personal dan menyebut nama pelanggan jika relevan
4. Profesional namun ramah
5. Singkat dan jelas
6. JANGAN gunakan emoji atau karakter khusus
7. Gunakan teks biasa saja

Berikan HANYA teks balasan, tanpa penjelasan tambahan."""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "resource_exhausted" in error_msg:
                print(f"⚠️ Gemini API quota exceeded for auto-responder!")
                print(f"   Using default response.")
            else:
                print(f"Error generating response: {e}")
            return "Terima kasih atas pesan Anda. Kami akan segera merespons."
    
    def _format_data(self, data: Dict[str, str]) -> str:
        """Format data dictionary for prompt"""
        return "\n".join([f"- {key}: {value}" for key, value in data.items() if value])
    
    def _simple_template_replace(self, template: str, data: Dict[str, str]) -> str:
        """Simple fallback template replacement"""
        message = template
        for key, value in data.items():
            placeholder = "{" + key + "}"
            message = message.replace(placeholder, value)
            placeholder_upper = "{" + key.upper() + "}"
            message = message.replace(placeholder_upper, value)
        return message


# Singleton instance
_gemini_service = None

def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
