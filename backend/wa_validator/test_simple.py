"""
Simple test script untuk debug WhatsApp checker
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def test_whatsapp_check():
    print("="*60)
    print("SIMPLE WHATSAPP CHECKER TEST")
    print("="*60)
    
    # Setup Chrome
    print("\n1. Setting up Chrome...")
    options = Options()
    user_data_dir = os.path.abspath('./wa_session')
    os.makedirs(user_data_dir, exist_ok=True)
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    print("✓ Chrome opened")
    
    # Login WhatsApp
    print("\n2. Opening WhatsApp Web...")
    driver.get('https://web.whatsapp.com')
    print("✓ WhatsApp Web opened")
    
    print("\n" + "="*60)
    print("SCAN QR CODE SEKARANG!")
    print("="*60)
    
    # Wait for login
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Chat list"]'))
        )
        print("✓ Login berhasil!")
    except:
        print("✗ Login timeout")
        driver.quit()
        return
    
    time.sleep(3)
    
    # Test dengan nomor
    print("\n3. Masukkan nomor untuk test:")
    phone = input("Nomor (contoh: 081234567890): ").strip()
    
    # Clean phone number
    import re
    clean_phone = re.sub(r'\D', '', phone)
    if not clean_phone.startswith('62'):
        if clean_phone.startswith('0'):
            clean_phone = '62' + clean_phone[1:]
        else:
            clean_phone = '62' + clean_phone
    
    print(f"\nCleaned phone: {clean_phone}")
    
    # Open chat
    url = f'https://web.whatsapp.com/send?phone={clean_phone}'
    print(f"\n4. Opening: {url}")
    driver.get(url)
    
    print("\n5. Waiting 10 seconds for page to load...")
    time.sleep(10)
    
    # Get page source
    print("\n6. Analyzing page...")
    page_source = driver.page_source.lower()
    
    # Check for error
    error_keywords = ['invalid', 'tidak valid', 'phone number shared via url is invalid']
    has_error = any(keyword in page_source for keyword in error_keywords)
    
    print(f"\n7. Results:")
    print(f"   Has error message: {has_error}")
    
    if has_error:
        print("   ❌ Nomor TIDAK terdaftar WhatsApp")
    else:
        print("   ✅ Nomor TERDAFTAR WhatsApp")
        
        # Check for business
        business_keywords = ['business account', 'akun bisnis', 'verified business']
        is_business = any(keyword in page_source for keyword in business_keywords)
        
        if is_business:
            print("   💼 WhatsApp BUSINESS")
        else:
            print("   👤 WhatsApp PERSONAL")
    
    # Show current URL
    print(f"\n8. Current URL: {driver.current_url}")
    
    # Show page title
    print(f"9. Page title: {driver.title}")
    
    # Check for specific elements
    print("\n10. Checking elements...")
    try:
        header = driver.find_element(By.CSS_SELECTOR, 'header')
        print(f"    ✓ Header found")
        print(f"    Header text: {header.text[:100]}")
    except:
        print(f"    ✗ Header NOT found")
    
    # Save screenshot
    screenshot_file = f'test_screenshot_{clean_phone}.png'
    driver.save_screenshot(screenshot_file)
    print(f"\n11. Screenshot saved: {screenshot_file}")
    
    # Save page source
    source_file = f'test_source_{clean_phone}.html'
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"12. Page source saved: {source_file}")
    
    print("\n" + "="*60)
    print("TEST SELESAI!")
    print("="*60)
    print("\nSilakan cek:")
    print(f"1. Screenshot: {screenshot_file}")
    print(f"2. Page source: {source_file}")
    print("3. Chrome window (jangan ditutup dulu)")
    
    input("\nTekan Enter untuk tutup Chrome...")
    driver.quit()

if __name__ == '__main__':
    try:
        test_whatsapp_check()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
