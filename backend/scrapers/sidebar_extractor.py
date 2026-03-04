"""
Extract data directly from sidebar without opening detail pages
Much faster than opening each place individually
"""
from selenium.webdriver.common.by import By
import time
import re


def extract_from_sidebar(driver):
    """
    Extract data directly from sidebar items
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        list: List of place data extracted from sidebar
    """
    results = []
    
    try:
        print("Extracting data from sidebar...")
        
        # Wait a bit for all items to be ready
        time.sleep(3)
        
        # Find all place cards in sidebar - try multiple strategies
        items = []
        
        # Strategy 1: Find by feed container
        try:
            feed = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            # Get direct children that are likely place cards
            items = feed.find_elements(By.XPATH, './div/div[@jsaction]')
            if len(items) > 5:
                print(f"Strategy 1: Found {len(items)} items via feed > div > div[@jsaction]")
        except Exception as e:
            print(f"Strategy 1 failed: {e}")
        
        # Strategy 2: Find all links with place URLs
        if len(items) < 5:
            try:
                links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
                # Get parent containers
                items = []
                seen = set()
                for link in links:
                    try:
                        # Go up to find the card container
                        parent = link.find_element(By.XPATH, './ancestor::div[@jsaction][1]')
                        parent_id = parent.get_attribute('data-index') or str(id(parent))
                        if parent_id not in seen:
                            items.append(parent)
                            seen.add(parent_id)
                    except:
                        continue
                if len(items) > 5:
                    print(f"Strategy 2: Found {len(items)} items via link parents")
            except Exception as e:
                print(f"Strategy 2 failed: {e}")
        
        # Strategy 3: Find by class name
        if len(items) < 5:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')
                if len(items) > 5:
                    print(f"Strategy 3: Found {len(items)} items via class Nv2PK")
            except Exception as e:
                print(f"Strategy 3 failed: {e}")
        
        if not items or len(items) < 3:
            print(f"ERROR: Not enough items found ({len(items)}). Sidebar extraction failed.")
            # Save screenshot for debugging
            try:
                driver.save_screenshot('debug_sidebar_no_items.png')
                print("Screenshot saved: debug_sidebar_no_items.png")
            except:
                pass
            return results
        
        print(f"Processing {len(items)} items from sidebar...")
        
        for idx, item in enumerate(items):
            try:
                data = extract_item_data(item, idx)
                if data:
                    results.append(data)
                    if len(results) % 10 == 0:
                        print(f"✓ Extracted {len(results)} places so far...")
                    elif len(results) <= 5:
                        print(f"✓ Extracted {len(results)}: {data['name']}")
            except Exception as e:
                print(f"Error extracting item {idx}: {e}")
                continue
        
        print(f"\n=== Total extracted from sidebar: {len(results)} ===")
        return results
        
    except Exception as e:
        print(f"Error in sidebar extraction: {e}")
        import traceback
        traceback.print_exc()
        return results


def extract_item_data(item, idx):
    """
    Extract data from a single sidebar item
    
    Args:
        item: Selenium WebElement
        idx: Index for debugging
        
    Returns:
        dict: Place data or None
    """
    try:
        # Get the link - try multiple selectors
        link = None
        link_elem = None
        link_selectors = [
            'a[href*="/maps/place/"]',
            'a[href*="place"]',
            'a[href*="maps"]',
            'a'
        ]
        
        for selector in link_selectors:
            try:
                link_elem = item.find_element(By.CSS_SELECTOR, selector)
                link = link_elem.get_attribute('href')
                if link and '/maps/place/' in link:
                    break
            except:
                continue
        
        if not link or '/maps/place/' not in link:
            print(f"Item {idx}: No valid link found, skipping")
            return None
        
        # Get name - try multiple selectors
        name = None
        name_selectors = [
            'div.fontHeadlineSmall',
            'div.qBF1Pd',
            'div[class*="fontHeadline"]',
            'div[class*="title"]',
            'a[aria-label]',
        ]
        
        for selector in name_selectors:
            try:
                name_elem = item.find_element(By.CSS_SELECTOR, selector)
                name = name_elem.text.strip()
                if name and len(name) > 2:
                    break
            except:
                continue
        
        # Fallback: get from aria-label of link
        if not name and link_elem:
            try:
                name = link_elem.get_attribute('aria-label')
                if name:
                    name = name.strip()
            except:
                pass
        
        # Last fallback: get any text from item
        if not name:
            try:
                name = item.text.strip().split('\n')[0]
            except:
                pass
        
        if not name or len(name) < 2:
            print(f"Item {idx}: No valid name found, skipping")
            return None
        
        # Get rating
        rating = "Rating tidak tersedia"
        reviews_count = "0"
        try:
            rating_elem = item.find_element(By.CSS_SELECTOR, 'span[role="img"][aria-label*="bintang"]')
            rating_text = rating_elem.get_attribute('aria-label')
            rating = rating_text
            # Try to extract review count from nearby text
            try:
                parent = rating_elem.find_element(By.XPATH, '..')
                text = parent.text
                match = re.search(r'\(?([\d.,]+)\)?', text)
                if match:
                    reviews_count = match.group(1).replace('.', '').replace(',', '')
            except:
                pass
        except:
            try:
                rating_elem = item.find_element(By.CSS_SELECTOR, 'span[aria-label*="star"]')
                rating_text = rating_elem.get_attribute('aria-label')
                rating = rating_text
                # Try to extract review count
                try:
                    parent = rating_elem.find_element(By.XPATH, '..')
                    text = parent.text
                    match = re.search(r'\(?([\d.,]+)\)?', text)
                    if match:
                        reviews_count = match.group(1).replace('.', '').replace(',', '')
                except:
                    pass
            except:
                pass
        
        # Get category - usually shown in sidebar
        category = "Tidak tersedia"
        try:
            category_elem = item.find_element(By.CSS_SELECTOR, 'span.W4Efsd:first-of-type')
            category = category_elem.text.strip()
            if not category or len(category) > 50:  # Too long, probably not category
                category = "Tidak tersedia"
        except:
            pass
        
        # Get address - usually in the description area
        address = "Alamat tidak tersedia"
        try:
            # Try to find address in various places
            text_elements = item.find_elements(By.CSS_SELECTOR, 'div.W4Efsd span')
            for elem in text_elements:
                text = elem.text.strip()
                # Address usually contains "Jl" or is longer text
                if text and (len(text) > 20 or 'Jl' in text or 'Jalan' in text):
                    address = text
                    break
        except:
            pass
        
        # Phone and website usually not available in sidebar
        # Would need to open detail page for these
        
        # Extract coordinates from link
        latitude = "Tidak tersedia"
        longitude = "Tidak tersedia"
        try:
            # Try multiple patterns
            match = re.search(r'/@(-?\d+\.?\d*),(-?\d+\.?\d*)', link)
            if not match:
                match = re.search(r'\?q=(-?\d+\.?\d*),(-?\d+\.?\d*)', link)
            if not match:
                match = re.search(r'/place/[^/]+/@(-?\d+\.?\d*),(-?\d+\.?\d*)', link)
            
            if match:
                latitude = match.group(1)
                longitude = match.group(2)
                print(f"Coordinates extracted: {latitude}, {longitude}")
        except Exception as e:
            print(f"Error extracting coordinates: {e}")
        
        return {
            "name": name,
            "phone": "Tidak tersedia (sidebar)",
            "website": "Tidak tersedia (sidebar)",
            "rating": rating,
            "reviews_count": reviews_count,
            "category": category,
            "address": address,
            "plus_code": "Tidak tersedia (sidebar)",
            "hours": "Tidak tersedia (sidebar)",
            "price_level": "Tidak tersedia (sidebar)",
            "price_range": "Tidak tersedia (sidebar)",
            "latitude": latitude,
            "longitude": longitude,
            "link": link
        }
        
    except Exception as e:
        print(f"Error extracting item data: {e}")
        return None


def extract_from_sidebar_with_hover(driver):
    """
    Extract data from sidebar with hover to get more info
    Slightly slower but gets more data
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        list: List of place data
    """
    from selenium.webdriver.common.action_chains import ActionChains
    
    results = []
    
    try:
        print("Extracting data from sidebar with hover...")
        
        # Find all place links
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
        print(f"Found {len(links)} place links")
        
        actions = ActionChains(driver)
        
        for idx, link in enumerate(links):
            try:
                # Hover over the link to show more info
                actions.move_to_element(link).perform()
                time.sleep(0.5)  # Wait for hover info
                
                # Get parent container
                parent = link.find_element(By.XPATH, './ancestor::div[contains(@class, "Nv2PK") or @jsaction]')
                
                # Extract data
                data = extract_item_data(parent, idx)
                if data:
                    results.append(data)
                    print(f"✓ Extracted {len(results)}: {data['name']}")
                    
            except Exception as e:
                print(f"Error with hover extraction {idx}: {e}")
                continue
        
        return results
        
    except Exception as e:
        print(f"Error in hover extraction: {e}")
        return results
