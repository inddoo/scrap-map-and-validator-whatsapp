"""
Test message sanitization with line breaks
"""
import re

def sanitize_message(message: str) -> str:
    """Remove emojis and characters outside BMP but preserve line breaks"""
    
    # Remove emojis using regex pattern
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "]+",
        flags=re.UNICODE
    )
    
    # Remove emojis
    sanitized = emoji_pattern.sub('', message)
    
    # Filter characters with code points > 0xFFFF (outside BMP)
    # BUT preserve newlines, carriage returns, and tabs
    sanitized = ''.join(
        char for char in sanitized 
        if ord(char) <= 0xFFFF or char in ['\n', '\r', '\t']
    )
    
    # Clean up excessive spaces on each line, but preserve line breaks
    lines = sanitized.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove excessive spaces within line
        cleaned_line = re.sub(r' +', ' ', line.strip())
        cleaned_lines.append(cleaned_line)
    
    # Join with newlines, remove excessive empty lines (max 2 consecutive)
    sanitized = '\n'.join(cleaned_lines)
    sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
    
    return sanitized.strip()


# Test cases with line breaks
test_messages = [
    "Halo! 👋\nSelamat datang 😊\nKami dari PT ABC",
    
    """Halo Pak John!

Kami dari PT ABC ingin menawarkan:
- Produk A
- Produk B
- Produk C

Terima kasih! 🙏""",
    
    "Promo spesial 🎉\n\nDiskon 20%\n\nHubungi kami sekarang!",
]

print("="*60)
print("MESSAGE SANITIZATION TEST (WITH LINE BREAKS)")
print("="*60)

for i, msg in enumerate(test_messages, 1):
    print(f"\n{i}. Original:")
    print("   ---")
    print(msg)
    print("   ---")
    
    sanitized = sanitize_message(msg)
    print(f"\n   Sanitized:")
    print("   ---")
    print(sanitized)
    print("   ---")
    
    if msg != sanitized:
        print(f"   ⚠️ Characters removed (emojis)")
    else:
        print(f"   ✅ No changes needed")
    
    # Check if line breaks preserved
    original_lines = msg.count('\n')
    sanitized_lines = sanitized.count('\n')
    print(f"   Line breaks: {original_lines} → {sanitized_lines}")

print("\n" + "="*60)
print("✅ All tests completed")
print("="*60)
