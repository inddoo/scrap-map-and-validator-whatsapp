"""
Groq AI Service for message generation and auto-responder
Fast and free alternative to Gemini
"""
import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class GroqService:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Available Groq models (in priority order)
        self.available_models = [
            'llama-3.1-70b-versatile',   # Best quality
            'llama-3.1-8b-instant',      # Fastest
            'mixtral-8x7b-32768',        # Good balance
            'gemma2-9b-it',              # Efficient
        ]
        
        self.current_model = None
    
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
        # Build prompt
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

        # Try each model until one succeeds
        last_error = None
        
        for model_name in self.available_models:
            try:
                print(f"  Trying Groq model: {model_name}")
                
                response = requests.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content'].strip()
                    
                    # Success! Remember this model
                    if self.current_model != model_name:
                        self.current_model = model_name
                        print(f"  ✓ Using Groq model: {model_name}")
                    
                    return message
                else:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get('error', {}).get('message', str(response.status_code))
                    print(f"  ⚠️ {model_name}: {error_msg}, trying next...")
                    last_error = Exception(error_msg)
                    continue
                    
            except Exception as e:
                print(f"  ⚠️ {model_name}: Error - {e}, trying next...")
                last_error = e
                continue
        
        # All models failed, use fallback
        print(f"⚠️ All Groq models failed! Using fallback template.")
        print(f"   Last error: {last_error}")
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
        
        # Build prompt with better context
        sender_name = sender_data.get('name', 'Pelanggan')
        
        history_section = ""
        if history_text:
            history_section = f"\nRiwayat percakapan sebelumnya:\n{history_text}\n"
        
        prompt = f"""Kamu adalah asisten WhatsApp yang cerdas dan responsif. Tugasmu adalah membalas pesan dari pelanggan dengan cara yang natural dan membantu.

PENTING: Baca dan pahami pesan pelanggan dengan baik, lalu berikan respons yang RELEVAN dan SPESIFIK terhadap apa yang mereka tanyakan atau katakan.

Informasi pelanggan:
- Nama: {sender_name}
- Nomor: {sender_data.get('phone', 'Unknown')}

Panduan respons Anda:
{response_prompt}
{history_section}
Pesan dari {sender_name}:
"{incoming_message}"

INSTRUKSI PENTING:
1. BACA pesan pelanggan dengan teliti
2. PAHAMI apa yang mereka tanyakan atau butuhkan
3. JAWAB secara spesifik dan relevan terhadap pesan mereka
4. Jika mereka bertanya, JAWAB pertanyaannya
5. Jika mereka menyapa, BALAS sapaannya dengan ramah
6. Jika mereka minta informasi, BERIKAN informasi yang diminta
7. Gunakan nama pelanggan untuk personalisasi
8. Singkat, jelas, dan natural (seperti chat biasa)
9. JANGAN gunakan emoji
10. JANGAN berikan jawaban template/generic yang tidak relevan

Balas SEKARANG dengan respons yang tepat dan natural:"""

        # Try each model until one succeeds
        last_error = None
        
        for model_name in self.available_models:
            try:
                print(f"    🤖 Generating response with {model_name}...")
                print(f"    📩 Incoming: {incoming_message[:80]}...")
                
                response = requests.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": "Kamu adalah asisten WhatsApp yang cerdas, responsif, dan natural. Selalu baca pesan dengan teliti dan berikan respons yang spesifik dan relevan. Jangan pernah memberikan jawaban template yang generic."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.8,  # Lebih kreatif dan natural
                        "max_tokens": 500,
                        "top_p": 0.9
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content'].strip()
                    
                    # Success! Remember this model
                    if self.current_model != model_name:
                        self.current_model = model_name
                        print(f"    ✓ Auto-responder using Groq model: {model_name}")
                    
                    print(f"    💬 Generated: {message[:80]}...")
                    return message
                else:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get('error', {}).get('message', str(response.status_code))
                    print(f"    ⚠️ {model_name} failed: {error_msg}")
                    last_error = Exception(error_msg)
                    continue
                    
            except Exception as e:
                last_error = e
                continue
        
        # All models failed
        print(f"⚠️ All Groq models failed for auto-responder! Using default response.")
        print(f"   Last error: {last_error}")
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
_groq_service = None


def get_groq_service() -> GroqService:
    """Get or create Groq service instance"""
    global _groq_service
    if _groq_service is None:
        _groq_service = GroqService()
    return _groq_service
