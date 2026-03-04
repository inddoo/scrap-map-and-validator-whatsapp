"""
Chrome driver management
"""
import undetected_chromedriver as uc
import os
from config.settings import CHROME_HEADLESS, CHROME_ARGS


def create_chrome_driver():
    """
    Create and configure Chrome driver instance
    
    Returns:
        Chrome driver instance
    """
    options = uc.ChromeOptions()
    
    # Add headless mode if enabled
    if CHROME_HEADLESS:
        options.add_argument('--headless=new')
    
    # Add all configured arguments
    for arg in CHROME_ARGS:
        options.add_argument(arg)
    
    print("Creating Chrome driver...")
    
    try:
        # Method 1: Try with version 145 (match your Chrome)
        print("Trying with Chrome version 145...")
        driver = uc.Chrome(
            options=options,
            version_main=145,  # Match your Chrome version
            use_subprocess=False
        )
        driver.implicitly_wait(10)
        print("✓ Chrome driver created successfully with version 145!")
        return driver
        
    except Exception as e1:
        print(f"Failed with version 145: {e1}")
        
        try:
            # Method 2: Try auto-detect
            print("Trying with auto-detect...")
            driver = uc.Chrome(
                options=options,
                version_main=None,
                use_subprocess=False
            )
            driver.implicitly_wait(10)
            print("✓ Chrome driver created with auto-detect!")
            return driver
            
        except Exception as e2:
            print(f"Failed with auto-detect: {e2}")
            
            try:
                # Method 3: Try without version specification
                print("Trying without version specification...")
                driver = uc.Chrome(
                    options=options,
                    use_subprocess=False
                )
                driver.implicitly_wait(10)
                print("✓ Chrome driver created without version!")
                return driver
                
            except Exception as e3:
                print(f"All methods failed: {e3}")
                
                # Give user clear instructions
                error_msg = """
╔════════════════════════════════════════════════════════════╗
║  CHROME VERSION MISMATCH ERROR                             ║
╚════════════════════════════════════════════════════════════╝

Your Chrome version: 145.0.7632.116
ChromeDriver version: 146

SOLUTION 1 (RECOMMENDED): Update Chrome Browser
1. Open Chrome
2. Click menu (⋮) → Help → About Google Chrome
3. Chrome will auto-update to version 146
4. Restart Chrome
5. Restart this backend

SOLUTION 2: Force ChromeDriver version 145
Run this command:
    pip uninstall undetected-chromedriver
    pip install undetected-chromedriver==3.5.5

SOLUTION 3: Use Selenium with manual ChromeDriver
1. Download ChromeDriver 145 from:
   https://googlechromelabs.github.io/chrome-for-testing/
2. Extract and note the path
3. Update backend/core/driver.py to use that path

After fixing, restart backend with: python run.py
"""
                print(error_msg)
                raise Exception(error_msg)
