"""
Test script untuk cek apakah Chrome bisa dibuka dengan Selenium
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys

def test_chrome():
    print("="*60)
    print("TESTING CHROME SELENIUM")
    print("="*60)
    
    print("\n1. Testing basic Chrome...")
    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=options)
        print("✓ Chrome opened successfully!")
        
        print("\n2. Testing navigation...")
        driver.get('https://www.google.com')
        print(f"✓ Navigated to: {driver.current_url}")
        
        print("\n3. Waiting 3 seconds...")
        time.sleep(3)
        
        print("\n4. Closing Chrome...")
        driver.quit()
        print("✓ Chrome closed successfully!")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nChrome Selenium berfungsi dengan baik.")
        print("Anda bisa menggunakan WhatsApp validator.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n" + "="*60)
        print("TROUBLESHOOTING")
        print("="*60)
        print("\n1. Pastikan Chrome terinstall:")
        print("   - Buka: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        print("   - Atau install dari: https://www.google.com/chrome/")
        
        print("\n2. Tutup semua Chrome yang sedang berjalan:")
        print("   - Tekan Ctrl+Shift+Esc (Task Manager)")
        print("   - Cari 'Google Chrome'")
        print("   - Klik kanan > End Task")
        
        print("\n3. Install/Update ChromeDriver:")
        print("   pip install --upgrade selenium")
        
        print("\n4. Coba restart komputer")
        
        print("\n5. Jika masih error, coba:")
        print("   pip uninstall selenium")
        print("   pip install selenium==4.15.0")
        
        return False

if __name__ == '__main__':
    success = test_chrome()
    sys.exit(0 if success else 1)
