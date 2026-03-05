"""
Test script for AI Gemini integration
Run this to test AI features before using in production
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_api_key():
    """Test if Gemini API key is set"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("   Please add: GEMINI_API_KEY=your_api_key_here")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {api_key[:10]}...")
    return True


def test_gemini_service():
    """Test Gemini service initialization"""
    try:
        from ai import get_gemini_service
        gemini = get_gemini_service()
        print("✅ Gemini service initialized successfully")
        return gemini
    except Exception as e:
        print(f"❌ Failed to initialize Gemini service: {e}")
        return None


def test_message_generation(gemini):
    """Test AI message generation"""
    print("\n" + "="*60)
    print("TEST: AI Message Generation")
    print("="*60)
    
    # Sample data
    template = """Buatkan pesan promosi untuk {name} yang bekerja sebagai {position} di {company}.
Tawarkan layanan IT kami dengan diskon 20%.
Gunakan bahasa profesional tapi ramah."""
    
    data = {
        'phone': '628123456789',
        'name': 'John Doe',
        'company': 'PT ABC Technology',
        'position': 'CEO'
    }
    
    context = "Kami adalah perusahaan IT yang menyediakan jasa pembuatan website dan aplikasi mobile."
    
    try:
        print(f"\nTemplate: {template[:80]}...")
        print(f"Data: {data}")
        print(f"Context: {context[:80]}...")
        print("\nGenerating message...")
        
        message = gemini.generate_personalized_message(
            template=template,
            data=data,
            context=context
        )
        
        print("\n" + "-"*60)
        print("GENERATED MESSAGE:")
        print("-"*60)
        print(message)
        print("-"*60)
        print("\n✅ Message generation successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Message generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_auto_responder(gemini):
    """Test AI auto responder"""
    print("\n" + "="*60)
    print("TEST: AI Auto Responder")
    print("="*60)
    
    incoming_message = "Halo, saya mau tanya harga untuk pembuatan website company profile?"
    
    sender_data = {
        'phone': '628123456789',
        'name': 'John Doe',
        'company': 'PT ABC Technology'
    }
    
    response_prompt = """Anda adalah customer service yang ramah dan profesional.
Jawab pertanyaan tentang harga dengan informatif.
Tawarkan untuk diskusi lebih lanjut via meeting.
Gunakan emoji yang sesuai."""
    
    try:
        print(f"\nIncoming message: {incoming_message}")
        print(f"Sender: {sender_data['name']} from {sender_data['company']}")
        print(f"Response prompt: {response_prompt[:80]}...")
        print("\nGenerating response...")
        
        response = gemini.generate_auto_response(
            incoming_message=incoming_message,
            sender_data=sender_data,
            response_prompt=response_prompt
        )
        
        print("\n" + "-"*60)
        print("GENERATED RESPONSE:")
        print("-"*60)
        print(response)
        print("-"*60)
        print("\n✅ Auto responder successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Auto responder failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bulk_generation(gemini):
    """Test bulk message generation"""
    print("\n" + "="*60)
    print("TEST: Bulk Message Generation")
    print("="*60)
    
    template = "Halo {name}! Kami dari IT Solutions ingin menawarkan diskon spesial untuk {company}. Tertarik? 😊"
    
    contacts = [
        {'phone': '628111', 'name': 'Alice', 'company': 'PT AAA'},
        {'phone': '628222', 'name': 'Bob', 'company': 'CV BBB'},
        {'phone': '628333', 'name': 'Charlie', 'company': 'UD CCC'},
    ]
    
    try:
        print(f"\nTemplate: {template}")
        print(f"Contacts: {len(contacts)}")
        print("\nGenerating messages...")
        
        results = []
        for contact in contacts:
            message = gemini.generate_personalized_message(
                template=template,
                data=contact
            )
            results.append({
                'contact': contact,
                'message': message
            })
            print(f"  ✓ Generated for {contact['name']}")
        
        print("\n" + "-"*60)
        print("SAMPLE GENERATED MESSAGES:")
        print("-"*60)
        for result in results[:2]:
            print(f"\n{result['contact']['name']}:")
            print(result['message'][:100] + "...")
        print("-"*60)
        print(f"\n✅ Bulk generation successful! ({len(results)} messages)")
        return True
        
    except Exception as e:
        print(f"\n❌ Bulk generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🤖 AI GEMINI INTEGRATION TEST")
    print("="*60)
    
    # Test 1: API Key
    if not test_gemini_api_key():
        print("\n❌ Tests aborted - API key not found")
        return
    
    # Test 2: Service initialization
    gemini = test_gemini_service()
    if not gemini:
        print("\n❌ Tests aborted - Service initialization failed")
        return
    
    # Test 3: Message generation
    test_message_generation(gemini)
    
    # Test 4: Auto responder
    test_auto_responder(gemini)
    
    # Test 5: Bulk generation
    test_bulk_generation(gemini)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\nYou can now use AI features in the application.")
    print("See AI_FEATURES_GUIDE.md for usage instructions.\n")


if __name__ == '__main__':
    main()
