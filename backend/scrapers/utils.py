"""
Utility functions for scraping operations
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

from core import update_progress
from config.settings import (
    SCROLL_WAIT_TIME,
    SCROLL_MAX_ATTEMPTS,
    SCROLL_NO_CHANGE_THRESHOLD,
    FEED_WAIT_TIME,
    ITEMS_CHECK_ATTEMPTS,
    MIN_ITEMS_BEFORE_SCROLL,
    PRE_SCROLL_WAIT,
    PRE_COLLECT_WAIT
)


def wait_for_results(driver):
    """
    Wait for search results to load
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        bool: True if results loaded, False otherwise
    """
    try:
        print("Waiting for results to load...")
        update_progress(message="Menunggu hasil pencarian...")
        
        # Wait for feed to appear - coba berbagai selector
        feed_found = False
        feed_selectors = [
            'div[role="feed"]',
            'div[role="main"]',
            'div.m6QErb',  # Google Maps container
        ]
        
        for selector in feed_selectors:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"Feed found with selector: {selector}")
                feed_found = True
                break
            except:
                continue
        
        if not feed_found:
            print("ERROR: Feed container not found!")
            return False
        
        time.sleep(3)  # Dikurangi dari 5
        
        # Wait for items to load - coba berbagai selector
        items_found = False
        item_selectors = [
            'a[href*="/maps/place/"]',
            'a[href*="place"]',
            'div[role="article"]',
            'div.Nv2PK',  # Google Maps place card
        ]
        
        for attempt in range(ITEMS_CHECK_ATTEMPTS):
            for selector in item_selectors:
                items = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(items) > 0:
                    print(f"Check {attempt+1}: Found {len(items)} items with selector: {selector}")
                    if len(items) >= MIN_ITEMS_BEFORE_SCROLL:
                        print(f"Items loaded! Found {len(items)} items")
                        items_found = True
                        break
            
            if items_found:
                break
            
            time.sleep(1.5)  # Dikurangi dari 2
        
        # Jika tidak ada items setelah semua attempts
        if not items_found:
            print("ERROR: No items found after all attempts!")
            print("Trying to get page source for debugging...")
            try:
                # Save screenshot
                driver.save_screenshot('debug_no_items_found.png')
                print("Screenshot saved as debug_no_items_found.png")
                
                # Check if there's a "no results" message
                page_text = driver.find_element(By.TAG_NAME, 'body').text
                if 'tidak ditemukan' in page_text.lower() or 'no results' in page_text.lower():
                    print("Google Maps returned 'no results' message")
                    return False
            except:
                pass
            
            return False
        
        update_progress(message="Hasil ditemukan, mulai scroll...")
        time.sleep(PRE_SCROLL_WAIT)
        
        return True
        
    except Exception as e:
        print(f"No results found: {e}")
        try:
            driver.save_screenshot('debug_no_results.png')
            print("Screenshot saved as debug_no_results.png")
        except:
            pass
        return False


def scroll_sidebar(driver):
    """
    Scroll sidebar to load all results
    
    Args:
        driver: Selenium WebDriver instance
    """
    try:
        feed = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        
        print("Scrolling sidebar to load all results...")
        update_progress(message="Scroll sidebar untuk load semua hasil...")
        
        scroll_count = 0
        no_change_count = 0
        previous_height = driver.execute_script('return arguments[0].scrollHeight', feed)
        
        while True:
            # Scroll to bottom
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', feed)
            
            print(f"Scroll {scroll_count + 1}: Menunggu data baru loading...")
            
            # Wait untuk loading data baru setelah scroll
            time.sleep(SCROLL_WAIT_TIME)
            
            scroll_count += 1
            
            # Get new height after scroll and wait
            new_height = driver.execute_script('return arguments[0].scrollHeight', feed)
            
            print(f"Scroll {scroll_count}: height {previous_height} -> {new_height}")
            
            # Check if height changed
            if new_height == previous_height:
                no_change_count += 1
                print(f"Height tidak berubah ({no_change_count}x) - data baru tidak loading")
                
                # Tunggu lebih lama untuk memastikan benar-benar tidak ada data baru
                if no_change_count == 1:
                    print("Tunggu lebih lama untuk memastikan...")
                    time.sleep(SCROLL_WAIT_TIME)  # Extra wait
                    new_height = driver.execute_script('return arguments[0].scrollHeight', feed)
                    if new_height != previous_height:
                        print("Ada data baru setelah tunggu lebih lama!")
                        no_change_count = 0
                        previous_height = new_height
                        continue
                
                # Stop after threshold
                if no_change_count >= SCROLL_NO_CHANGE_THRESHOLD:
                    print(f"Height tidak berubah {SCROLL_NO_CHANGE_THRESHOLD}x berturut-turut, berhenti scroll")
                    update_progress(message=f"Selesai scroll ({scroll_count}x)")
                    break
            else:
                # Reset counter if changed
                no_change_count = 0
                previous_height = new_height
                print(f"✓ Data baru berhasil loading! Height bertambah ke {new_height}")
            
            # Update progress
            if scroll_count % 3 == 0:
                update_progress(message=f"Scroll {scroll_count}x, tinggi: {new_height}px, loading data...")
            
            # Safety limit
            if scroll_count >= SCROLL_MAX_ATTEMPTS:
                print(f"Reached max scroll limit ({SCROLL_MAX_ATTEMPTS})")
                break
                
    except Exception as e:
        print(f"Scroll error: {e}")


def collect_place_urls(driver):
    """
    Collect all place URLs from sidebar
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        list: List of unique place URLs
    """
    try:
        print("Waiting before collecting URLs...")
        time.sleep(PRE_COLLECT_WAIT)
        
        # Try multiple selectors
        selectors = [
            'a[href*="/maps/place/"]',
            'div[role="feed"] a[href*="maps/place"]',
            'a[href*="place"]',
            'div[role="article"] a',
        ]
        
        items = []
        used_selector = None
        
        for selector in selectors:
            items = driver.find_elements(By.CSS_SELECTOR, selector)
            if items:
                print(f"Found {len(items)} items with selector: {selector}")
                used_selector = selector
                break
        
        if not items:
            print("No items found with any selector!")
            # Try alternative: get all links and filter
            all_links = driver.find_elements(By.TAG_NAME, 'a')
            items = [link for link in all_links if '/maps/place/' in link.get_attribute('href') or '']
            if items:
                print(f"Found {len(items)} items using fallback method")
            else:
                driver.save_screenshot('debug_no_items.png')
                return []
        
        # Collect unique hrefs
        all_hrefs = []
        for item in items:
            try:
                href = item.get_attribute('href')
                if href and '/maps/place/' in href and href not in all_hrefs:
                    all_hrefs.append(href)
            except:
                continue
        
        print(f"Collected {len(all_hrefs)} unique place URLs")
        return all_hrefs
        
    except Exception as e:
        print(f"Error collecting URLs: {e}")
        return []


def extract_place_data(driver, href, idx):
    """
    Extract data from a place detail page
    
    Args:
        driver: Selenium WebDriver instance
        href: URL of the place
        idx: Index for debugging
        
    Returns:
        dict: Place data or None if extraction failed
    """
    try:
        # Extract name
        name = _extract_name(driver, idx)
        if not name:
            return None
        
        # Extract all data
        print(f"\n=== Extracting data for: {name} ===")
        rating = _extract_rating(driver)
        phone = _extract_phone(driver)
        website = _extract_website(driver)
        address = _extract_address(driver)
        reviews_count = _extract_reviews_count(driver)
        category = _extract_category(driver)
        hours = _extract_hours(driver)
        plus_code = _extract_plus_code(driver)
        price_level = _extract_price_level(driver)
        price_range = _extract_price_range(driver)
        latitude, longitude = _extract_coordinates(driver, href)
        
        # Debug: Print all extracted data
        print(f"\n=== Extracted Data Summary ===")
        print(f"Name: {name}")
        print(f"Rating: {rating}")
        print(f"Reviews: {reviews_count}")
        print(f"Category: {category}")
        print(f"Phone: {phone}")
        print(f"Website: {website}")
        print(f"Address: {address}")
        print(f"Hours: {hours}")
        print(f"Plus Code: {plus_code}")
        print(f"Price Level: {price_level}")
        print(f"Price Range: {price_range}")
        print(f"Coordinates: {latitude}, {longitude}")
        print(f"Link: {href}")
        print(f"=== End Summary ===\n")
        
        result = {
            "name": name,
            "phone": phone,
            "website": website,
            "rating": rating,
            "reviews_count": reviews_count,
            "category": category,
            "address": address,
            "plus_code": plus_code,
            "hours": hours,
            "price_level": price_level,
            "price_range": price_range,
            "latitude": latitude,
            "longitude": longitude,
            "link": href
        }
        
        print(f"Returning result dict with {len(result)} keys")
        return result
        
    except Exception as e:
        print(f"Error extracting place data: {e}")
        return None


def _extract_name(driver, idx):
    """Extract place name"""
    try:
        # Wait for h1 (dikurangi timeout)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
        )
        time.sleep(1)  # Dikurangi dari 2
        
        # Method 1: From h1 elements
        h1_elements = driver.find_elements(By.CSS_SELECTOR, 'h1')
        for h1 in h1_elements:
            text = h1.text.strip()
            if text and len(text) > 2 and text not in ['Hasil', 'Results', 'Search', 'Cari', 'Maps']:
                print(f"Name (h1): {text}")
                return text
        
        # Method 2: From page title
        page_title = driver.title
        if ' - Google Maps' in page_title:
            name = page_title.split(' - Google Maps')[0].strip()
            print(f"Name (title): {name}")
            return name
        
        # Method 3: From meta tag
        try:
            meta_title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]')
            name = meta_title.get_attribute('content')
            print(f"Name (meta): {name}")
            return name
        except:
            pass
        
        print(f"No valid name found")
        return None
        
    except Exception as e:
        print(f"Name extraction error: {e}")
        try:
            driver.save_screenshot(f'debug_no_name_{idx}.png')
        except:
            pass
        return None


def _extract_rating(driver):
    """Extract place rating"""
    try:
        rating_elem = driver.find_element(By.CSS_SELECTOR, 'div[role="main"] span[aria-label*="bintang"]')
        rating = rating_elem.get_attribute('aria-label')
        print(f"Rating: {rating}")
        return rating
    except:
        try:
            rating_elem = driver.find_element(By.CSS_SELECTOR, 'div[role="main"] span[aria-label*="star"]')
            rating = rating_elem.get_attribute('aria-label')
            print(f"Rating (alt): {rating}")
            return rating
        except:
            print("Rating not found")
            return "Rating tidak tersedia"


def _extract_phone(driver):
    """Extract phone number"""
    try:
        phone_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="phone:tel:"]')
        phone = phone_button.get_attribute('aria-label')
        phone = re.sub(r'^(Telepon|Phone|Nomor telepon):\s*', '', phone)
        print(f"Phone: {phone}")
        return phone
    except:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="elepon"]')
            if buttons:
                phone = buttons[0].get_attribute('aria-label')
                phone = re.sub(r'^(Telepon|Phone|Nomor telepon):\s*', '', phone)
                print(f"Phone (alt): {phone}")
                return phone
        except:
            pass
        print("Phone not found")
        return "Tidak tersedia"


def _extract_website(driver):
    """Extract website URL"""
    try:
        website_link = driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
        website = website_link.get_attribute('href')
        print(f"Website: {website}")
        return website
    except:
        try:
            links = driver.find_elements(By.CSS_SELECTOR, 'div[role="main"] a[href^="http"]')
            for link in links:
                url = link.get_attribute('href')
                if url and 'google.com' not in url and 'gstatic.com' not in url:
                    print(f"Website (alt): {url}")
                    return url
        except:
            pass
        print("Website not found")
        return "Tidak tersedia"


def _extract_address(driver):
    """Extract address"""
    try:
        address_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]')
        address = address_button.get_attribute('aria-label')
        address = re.sub(r'^(Alamat|Address):\s*', '', address)
        print(f"Address: {address}")
        return address
    except:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label]')
            for btn in buttons:
                label = btn.get_attribute('aria-label')
                if label and len(label) > 20 and ('Jl' in label or 'Jalan' in label or 'Street' in label):
                    address = re.sub(r'^(Alamat|Address):\s*', '', label)
                    print(f"Address (alt): {address}")
                    return address
        except:
            pass
        print("Address not found")
        return "Alamat tidak tersedia"


def _extract_reviews_count(driver):
    """Extract number of reviews"""
    try:
        print("Extracting reviews count...")
        
        # Strategy 1: Look for button with review count in aria-label
        try:
            # Indonesian: "1.234 ulasan"
            review_elem = driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="ulasan"]')
            review_text = review_elem.get_attribute('aria-label')
            match = re.search(r'([\d.,]+)\s*ulasan', review_text, re.IGNORECASE)
            if match:
                count = match.group(1).replace('.', '').replace(',', '')
                print(f"✅ Reviews count (Strategy 1 - ID): {count}")
                return count
        except:
            pass
        
        # Strategy 2: English version
        try:
            review_elem = driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="review"]')
            review_text = review_elem.get_attribute('aria-label')
            match = re.search(r'([\d.,]+)\s*review', review_text, re.IGNORECASE)
            if match:
                count = match.group(1).replace('.', '').replace(',', '')
                print(f"✅ Reviews count (Strategy 2 - EN): {count}")
                return count
        except:
            pass
        
        # Strategy 3: Look in rating section - format: "4.5★ (1,234)"
        try:
            # Find all spans in main area
            spans = driver.find_elements(By.CSS_SELECTOR, 'div[role="main"] span')
            for span in spans:
                text = span.text.strip()
                # Match patterns like "(1,234)" or "(1.234)"
                match = re.search(r'\(([\d.,]+)\)', text)
                if match:
                    count = match.group(1).replace('.', '').replace(',', '')
                    # Validate it's a reasonable number (not a price or other number)
                    if len(count) >= 1 and int(count) > 0:
                        print(f"✅ Reviews count (Strategy 3 - parentheses): {count}")
                        return count
        except Exception as e:
            print(f"Strategy 3 error: {e}")
        
        # Strategy 4: Look for specific review button patterns
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[jsaction*="review"], button[data-tab-index="1"]')
            for btn in buttons:
                text = btn.text.strip()
                aria = btn.get_attribute('aria-label') or ''
                combined = text + ' ' + aria
                
                # Match number followed by "ulasan" or "review"
                match = re.search(r'([\d.,]+)\s*(ulasan|review|reviews)', combined, re.IGNORECASE)
                if match:
                    count = match.group(1).replace('.', '').replace(',', '')
                    print(f"✅ Reviews count (Strategy 4 - button): {count}")
                    return count
        except Exception as e:
            print(f"Strategy 4 error: {e}")
        
        # Strategy 5: Look in page text near rating
        try:
            # Find rating element first
            rating_elems = driver.find_elements(By.CSS_SELECTOR, 'span[role="img"]')
            for rating_elem in rating_elems:
                aria = rating_elem.get_attribute('aria-label') or ''
                if 'bintang' in aria.lower() or 'star' in aria.lower():
                    # Look for sibling or nearby elements with review count
                    parent = rating_elem.find_element(By.XPATH, '..')
                    parent_text = parent.text
                    # Match patterns like "1,234" or "1.234" after rating
                    match = re.search(r'[\d.]+\s*[★⭐]\s*\(?([\d.,]+)\)?', parent_text)
                    if match:
                        count = match.group(1).replace('.', '').replace(',', '')
                        print(f"✅ Reviews count (Strategy 5 - near rating): {count}")
                        return count
        except Exception as e:
            print(f"Strategy 5 error: {e}")
        
        # Strategy 6: Look in entire page source as last resort
        try:
            page_text = driver.find_element(By.TAG_NAME, 'body').text
            # Look for pattern: number followed by "ulasan" or "reviews"
            matches = re.findall(r'([\d.,]+)\s*(ulasan|review)', page_text, re.IGNORECASE)
            if matches:
                # Take the first reasonable match
                for match in matches:
                    count = match[0].replace('.', '').replace(',', '')
                    if len(count) >= 1 and int(count) > 0:
                        print(f"✅ Reviews count (Strategy 6 - page text): {count}")
                        return count
        except Exception as e:
            print(f"Strategy 6 error: {e}")
            
    except Exception as e:
        print(f"❌ Error extracting reviews count: {e}")
    
    print("⚠️ Reviews count not found")
    return "0"


def _extract_category(driver):
    """Extract business category/type"""
    try:
        # Category is usually a button near the name
        category_button = driver.find_element(By.CSS_SELECTOR, 'button[jsaction*="category"]')
        category = category_button.text.strip()
        print(f"Category: {category}")
        return category
    except:
        try:
            # Alternative: look for category in specific area
            buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="main"] button.DkEaL')
            if buttons:
                category = buttons[0].text.strip()
                print(f"Category (alt): {category}")
                return category
        except:
            pass
    print("Category not found")
    return "Tidak tersedia"


def _extract_hours(driver):
    """Extract opening hours"""
    try:
        # Click hours button to expand
        hours_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="oh"]')
        hours_text = hours_button.get_attribute('aria-label')
        print(f"Hours: {hours_text}")
        return hours_text
    except:
        try:
            # Alternative: look for hours in various places
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Buka"]')
            if not buttons:
                buttons = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Open"]')
            if buttons:
                hours_text = buttons[0].get_attribute('aria-label')
                print(f"Hours (alt): {hours_text}")
                return hours_text
        except:
            pass
    print("Hours not found")
    return "Tidak tersedia"


def _extract_plus_code(driver):
    """Extract Plus Code"""
    try:
        plus_code_button = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="oloc"]')
        plus_code = plus_code_button.get_attribute('aria-label')
        plus_code = re.sub(r'^(Plus code|Kode plus):\s*', '', plus_code, flags=re.IGNORECASE)
        print(f"Plus Code: {plus_code}")
        return plus_code
    except:
        print("Plus Code not found")
        return "Tidak tersedia"


def _extract_price_level(driver):
    """Extract price level ($ $$ $$$)"""
    try:
        # Price level is usually shown as dollar signs or "Moderate", "Expensive", etc
        price_elem = driver.find_element(By.CSS_SELECTOR, 'span[aria-label*="Price"]')
        price = price_elem.get_attribute('aria-label')
        print(f"Price level: {price}")
        return price
    except:
        try:
            # Look for dollar signs in text
            spans = driver.find_elements(By.CSS_SELECTOR, 'div[role="main"] span')
            for span in spans:
                text = span.text.strip()
                if re.match(r'^\$+$', text):  # Match $, $$, $$$, etc
                    print(f"Price level (alt): {text}")
                    return text
        except:
            pass
    print("Price level not found")
    return "Tidak tersedia"


def _extract_price_range(driver):
    """Extract price range (Rp 50.000 - Rp 100.000)"""
    try:
        print("Extracting price range...")
        
        # Look for price range in various formats
        # Format 1: "Rp 1–25.000 per orang" (2 angka dengan Rp)
        # Format 2: "Rp 25–50 rb" (dengan "rb" atau "ribu")
        # Format 3: "Rp50.000 - Rp100.000" (2 Rp)
        
        # Strategy 1: Look in all text elements
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="main"] button, div[role="main"] span, div[role="main"] div')
        for elem in elements:
            try:
                text = elem.text.strip()
                
                # Pattern 1: "Rp 25–50 rb" or "Rp 25-50 ribu" (with rb/ribu suffix)
                match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+\s*(rb|ribu)', text, re.IGNORECASE)
                if match:
                    price_range = match.group(0)
                    # Add "per orang" if exists
                    if 'per orang' in text.lower():
                        price_range += ' per orang'
                    print(f"✅ Price range (Pattern 1 - with rb/ribu): {price_range}")
                    return price_range
                
                # Pattern 2: "Rp 1–25.000" (single Rp, no rb/ribu)
                match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+(?:\s*per\s*orang)?', text, re.IGNORECASE)
                if match:
                    price_range = match.group(0)
                    print(f"✅ Price range (Pattern 2 - single Rp): {price_range}")
                    return price_range
                
                # Pattern 3: "Rp 50.000 - Rp 100.000" (double Rp)
                match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*Rp\s*[\d.,]+(?:\s*per\s*orang)?', text, re.IGNORECASE)
                if match:
                    price_range = match.group(0)
                    print(f"✅ Price range (Pattern 3 - double Rp): {price_range}")
                    return price_range
                
                # Check aria-label too
                aria_label = elem.get_attribute('aria-label')
                if aria_label:
                    # Pattern 1 in aria-label (with rb/ribu)
                    match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+\s*(rb|ribu)', aria_label, re.IGNORECASE)
                    if match:
                        price_range = match.group(0)
                        if 'per orang' in aria_label.lower():
                            price_range += ' per orang'
                        print(f"✅ Price range (aria - with rb/ribu): {price_range}")
                        return price_range
                    
                    # Pattern 2 in aria-label (single Rp)
                    match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+(?:\s*per\s*orang)?', aria_label, re.IGNORECASE)
                    if match:
                        price_range = match.group(0)
                        print(f"✅ Price range (aria - single Rp): {price_range}")
                        return price_range
                    
                    # Pattern 3 in aria-label (double Rp)
                    match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*Rp\s*[\d.,]+(?:\s*per\s*orang)?', aria_label, re.IGNORECASE)
                    if match:
                        price_range = match.group(0)
                        print(f"✅ Price range (aria - double Rp): {price_range}")
                        return price_range
            except:
                continue
        
        # Strategy 2: Look in entire page text
        try:
            page_text = driver.find_element(By.TAG_NAME, 'body').text
            
            # Pattern 1: With rb/ribu
            match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+\s*(rb|ribu)(?:\s*per\s*orang)?', page_text, re.IGNORECASE)
            if match:
                price_range = match.group(0)
                print(f"✅ Price range (page - with rb/ribu): {price_range}")
                return price_range
            
            # Pattern 2: Single Rp
            match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*[\d.,]+(?:\s*per\s*orang)?', page_text, re.IGNORECASE)
            if match:
                price_range = match.group(0)
                print(f"✅ Price range (page - single Rp): {price_range}")
                return price_range
            
            # Pattern 3: Double Rp
            match = re.search(r'Rp\s*[\d.,]+\s*[-–]\s*Rp\s*[\d.,]+(?:\s*per\s*orang)?', page_text, re.IGNORECASE)
            if match:
                price_range = match.group(0)
                print(f"✅ Price range (page - double Rp): {price_range}")
                return price_range
        except Exception as e:
            print(f"Strategy 2 error: {e}")
            
    except Exception as e:
        print(f"❌ Error extracting price range: {e}")
    
    print("⚠️ Price range not found")
    return "Tidak tersedia"


def _extract_coordinates(driver, href):
    """Extract latitude and longitude from URL or page"""
    try:
        print(f"Extracting coordinates...")
        
        # Strategy 1: From URL (if available)
        print(f"Checking URL: {href[:100]}...")
        match = re.search(r'/@(-?\d+\.?\d*),(-?\d+\.?\d*)', href)
        if match:
            lat = match.group(1)
            lng = match.group(2)
            print(f"✅ Coordinates from URL: {lat}, {lng}")
            return lat, lng
        
        # Strategy 2: From URL with ?q= pattern
        match = re.search(r'\?q=(-?\d+\.?\d*),(-?\d+\.?\d*)', href)
        if match:
            lat = match.group(1)
            lng = match.group(2)
            print(f"✅ Coordinates from URL (q=): {lat}, {lng}")
            return lat, lng
        
        # Strategy 3: From page meta tags
        try:
            # Try og:url meta tag
            meta = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:url"]')
            url = meta.get_attribute('content')
            match = re.search(r'/@(-?\d+\.?\d*),(-?\d+\.?\d*)', url)
            if match:
                lat = match.group(1)
                lng = match.group(2)
                print(f"✅ Coordinates from meta tag: {lat}, {lng}")
                return lat, lng
        except:
            pass  # Silent fail, try next strategy
        
        # Strategy 4: From page source (JavaScript data)
        try:
            page_source = driver.page_source
            
            # Pattern 1: Look for "center":{"lat":X,"lng":Y}
            match = re.search(r'"center":\s*\{\s*"lat":\s*(-?\d+\.?\d*)\s*,\s*"lng":\s*(-?\d+\.?\d*)\s*\}', page_source)
            if match:
                lat = match.group(1)
                lng = match.group(2)
                print(f"✅ Coordinates from page source (center): {lat}, {lng}")
                return lat, lng
            
            # Pattern 2: Look for [lat,lng] array format
            match = re.search(r'\[(-?\d+\.?\d+),\s*(-?\d+\.?\d+)\]', page_source)
            if match:
                lat = match.group(1)
                lng = match.group(2)
                # Validate it's reasonable coordinates for Indonesia
                lat_float = float(lat)
                lng_float = float(lng)
                if -11 <= lat_float <= 6 and 95 <= lng_float <= 141:
                    print(f"✅ Coordinates from page source (array): {lat}, {lng}")
                    return lat, lng
            
            # Pattern 3: Look for data-latitude and data-longitude attributes
            match_lat = re.search(r'data-latitude["\']?\s*[:=]\s*["\']?(-?\d+\.?\d+)', page_source)
            match_lng = re.search(r'data-longitude["\']?\s*[:=]\s*["\']?(-?\d+\.?\d+)', page_source)
            if match_lat and match_lng:
                lat = match_lat.group(1)
                lng = match_lng.group(1)
                print(f"✅ Coordinates from data attributes: {lat}, {lng}")
                return lat, lng
                
        except:
            pass  # Silent fail, try next strategy
        
        # Strategy 5: Try to find in visible text (from screenshot you showed)
        try:
            # Look for pattern like "-6.56248, 110.67180"
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            match = re.search(r'(-?\d+\.\d{4,}),\s*(\d+\.\d{4,})', body_text)
            if match:
                lat = match.group(1)
                lng = match.group(2)
                print(f"✅ Coordinates from visible text: {lat}, {lng}")
                return lat, lng
        except:
            pass  # Silent fail, try next strategy
        
        # Strategy 6: From current URL (might have changed after navigation)
        try:
            current_url = driver.current_url
            if current_url != href:
                print(f"Checking current URL: {current_url[:100]}...")
                match = re.search(r'/@(-?\d+\.?\d*),(-?\d+\.?\d*)', current_url)
                if match:
                    lat = match.group(1)
                    lng = match.group(2)
                    print(f"✅ Coordinates from current URL: {lat}, {lng}")
                    return lat, lng
        except:
            pass  # Silent fail
            
    except Exception as e:
        print(f"❌ Error extracting coordinates: {e}")
    
    print(f"⚠️ Coordinates not found")
    return "Tidak tersedia", "Tidak tersedia"
