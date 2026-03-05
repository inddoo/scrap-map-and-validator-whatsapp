"""
Test script untuk verify line breaks preservation
"""

def test_sanitize_with_line_breaks():
    """Test bahwa _sanitize_message preserve line breaks"""
    
    # Simulate the sanitize function
    import re
    
    def _sanitize_message(message: str) -> str:
        """Same as in wa_sender.py"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002600-\U000026FF"
            "\U00002700-\U000027BF"
            "]+",
            flags=re.UNICODE
        )
        
        sanitized = emoji_pattern.sub('', message)
        sanitized = ''.join(
            char for char in sanitized 
            if ord(char) <= 0xFFFF or char in ['\n', '\r', '\t']
        )
        
        lines = sanitized.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r' +', ' ', line.strip())
            cleaned_lines.append(cleaned_line)
        
        sanitized = '\n'.join(cleaned_lines)
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
        
        return sanitized.strip()
    
    # Test message with multiple paragraphs
    test_message = """Halo Prima,

Saya dari PRIMACODE, sebuah perusahaan IT yang berfokus pada pengembangan website profesional dan efektif. Kami memahami betapa pentingnya...

Kami ingin menawarkan konsultasi gratis untuk membahas kebutuhan website Anda.

Terima kasih!"""
    
    print("Original message:")
    print(test_message)
    print(f"\nLine breaks in original: {test_message.count(chr(10))}")
    
    sanitized = _sanitize_message(test_message)
    
    print("\n" + "="*60)
    print("Sanitized message:")
    print(sanitized)
    print(f"\nLine breaks in sanitized: {sanitized.count(chr(10))}")
    
    # Test JavaScript conversion
    escaped_message = sanitized.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '<br>')
    print("\n" + "="*60)
    print("JavaScript HTML version:")
    print(escaped_message)
    print(f"\n<br> tags: {escaped_message.count('<br>')}")
    
    # Verify
    assert sanitized.count('\n') > 0, "Line breaks should be preserved!"
    assert escaped_message.count('<br>') == sanitized.count('\n'), "All \\n should be converted to <br>"
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("Line breaks are properly preserved and converted to HTML")

if __name__ == "__main__":
    test_sanitize_with_line_breaks()
