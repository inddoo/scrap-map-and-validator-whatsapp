"""
Example: WhatsApp Auto Sender Usage
Contoh penggunaan fitur auto sender
"""
import requests
import time

# Base URL
BASE_URL = "http://localhost:8000"


def example_1_single_message():
    """
    Example 1: Kirim pesan tunggal
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Send Single Message")
    print("="*60)
    
    data = {
        "phone": "628123456789",  # Ganti dengan nomor Anda
        "message": "Halo! Ini pesan test dari auto sender.",
        "delay": 5
    }
    
    response = requests.post(f"{BASE_URL}/wa/send", json=data)
    result = response.json()
    
    print(f"Success: {result['success']}")
    print(f"Status: {result['result']['status']}")
    print(f"Message Sent: {result['result']['message_sent']}")


def example_2_bulk_messages():
    """
    Example 2: Kirim pesan massal (bulk)
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Send Bulk Messages")
    print("="*60)
    
    data = {
        "phone_numbers": [
            "628123456789",  # Ganti dengan nomor valid
            "628987654321",
            "628555666777"
        ],
        "message": "🎉 PROMO SPESIAL!\n\nDiskon 50% untuk semua produk!\nKunjungi: www.toko.com",
        "min_delay": 5,
        "max_delay": 10,
        "stop_on_error": False
    }
    
    response = requests.post(f"{BASE_URL}/wa/send-bulk", json=data)
    result = response.json()
    
    print(f"Success: {result['success']}")
    print(f"\nSummary:")
    print(f"  Total: {result['summary']['total']}")
    print(f"  Sent: {result['summary']['sent']}")
    print(f"  Failed: {result['summary']['failed']}")
    print(f"  Success Rate: {result['summary']['sent_percent']}%")
    
    print(f"\nResults:")
    for r in result['results']:
        print(f"  {r['phone']}: {r['status']}")


def example_3_personalized_messages():
    """
    Example 3: Kirim pesan personal dengan template
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Send Personalized Messages")
    print("="*60)
    
    data = {
        "contacts": [
            {
                "phone": "628123456789",
                "name": "John Doe",
                "company": "ABC Corp",
                "product": "Laptop"
            },
            {
                "phone": "628987654321",
                "name": "Jane Smith",
                "company": "XYZ Ltd",
                "product": "Smartphone"
            }
        ],
        "message_template": """Halo {name} dari {company}! 👋

Terima kasih sudah tertarik dengan {product}.

Ada yang bisa kami bantu?

Hubungi kami untuk info lebih lanjut!""",
        "min_delay": 5,
        "max_delay": 10
    }
    
    response = requests.post(f"{BASE_URL}/wa/send-personalized", json=data)
    result = response.json()
    
    print(f"Success: {result['success']}")
    print(f"\nSummary:")
    print(f"  Total: {result['summary']['total']}")
    print(f"  Sent: {result['summary']['sent']}")
    print(f"  Failed: {result['summary']['failed']}")
    
    print(f"\nResults:")
    for r in result['results']:
        contact = r.get('contact', {})
        print(f"  {contact.get('name', 'Unknown')}: {r['status']}")


def example_4_from_csv():
    """
    Example 4: Kirim pesan dari data CSV
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Send Messages from CSV Data")
    print("="*60)
    
    # Simulasi data dari CSV
    import csv
    import io
    
    csv_data = """name,phone,company
John Doe,628123456789,ABC Corp
Jane Smith,628987654321,XYZ Ltd
Bob Johnson,628555666777,DEF Inc"""
    
    # Parse CSV
    contacts = []
    reader = csv.DictReader(io.StringIO(csv_data))
    for row in reader:
        contacts.append(row)
    
    # Kirim pesan personal
    data = {
        "contacts": contacts,
        "message_template": "Halo {name} dari {company}!\n\nIni pesan khusus untuk Anda.",
        "min_delay": 5,
        "max_delay": 10
    }
    
    response = requests.post(f"{BASE_URL}/wa/send-personalized", json=data)
    result = response.json()
    
    print(f"Success: {result['success']}")
    print(f"Total contacts from CSV: {len(contacts)}")
    print(f"Messages sent: {result['summary']['sent']}")


def example_5_with_validation():
    """
    Example 5: Validasi dulu, baru kirim pesan
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Validate Then Send")
    print("="*60)
    
    # Step 1: Validasi nomor
    print("\nStep 1: Validating numbers...")
    validate_data = {
        "phone_numbers": [
            "81234567890",  # Format: angka setelah +62
            "87654321098",
            "85556667777"
        ]
    }
    
    response = requests.post(f"{BASE_URL}/wa/validate", json=validate_data)
    validation_result = response.json()
    
    # Step 2: Filter hanya yang punya WhatsApp
    valid_numbers = [
        r['clean_phone'] 
        for r in validation_result['results'] 
        if r['has_whatsapp']
    ]
    
    print(f"Valid numbers: {len(valid_numbers)} out of {len(validate_data['phone_numbers'])}")
    
    if len(valid_numbers) == 0:
        print("No valid numbers to send messages to!")
        return
    
    # Step 3: Kirim pesan ke nomor yang valid
    print("\nStep 2: Sending messages to valid numbers...")
    send_data = {
        "phone_numbers": valid_numbers,
        "message": "Halo! Ini pesan untuk nomor yang valid.",
        "min_delay": 5,
        "max_delay": 10
    }
    
    response = requests.post(f"{BASE_URL}/wa/send-bulk", json=send_data)
    send_result = response.json()
    
    print(f"Messages sent: {send_result['summary']['sent']}")


def main():
    """
    Main function - pilih example yang ingin dijalankan
    """
    print("\n" + "="*60)
    print("WhatsApp Auto Sender - Examples")
    print("="*60)
    print("\nPastikan:")
    print("1. Backend sudah running (python run.py)")
    print("2. WhatsApp sudah diinit (/wa/init)")
    print("3. Ganti nomor dengan nomor valid Anda")
    print("="*60)
    
    # Uncomment example yang ingin dijalankan:
    
    # example_1_single_message()
    # example_2_bulk_messages()
    # example_3_personalized_messages()
    # example_4_from_csv()
    # example_5_with_validation()
    
    print("\n✅ Done! Uncomment example yang ingin dijalankan.")


if __name__ == "__main__":
    main()
