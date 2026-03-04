"""
Google Maps scraper implementation
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from urllib.parse import quote

from core import (
    create_chrome_driver, 
    get_progress, 
    update_progress,
    should_stop,
    reset_stop_flag
)
from config.settings import (
    SCROLL_WAIT_TIME,
    SCROLL_MAX_ATTEMPTS,
    SCROLL_NO_CHANGE_THRESHOLD,
    INITIAL_PAGE_LOAD_TIME,
    FEED_WAIT_TIME,
    ITEMS_CHECK_ATTEMPTS,
    MIN_ITEMS_BEFORE_SCROLL,
    PRE_SCROLL_WAIT,
    PRE_COLLECT_WAIT,
    DETAIL_PAGE_LOAD_TIME,
    DETAIL_PAGE_EXTRA_WAIT,
    DELAY_BETWEEN_REQUESTS,
    SCRAPE_MODE
)
from .utils import (
    wait_for_results,
    scroll_sidebar,
    collect_place_urls,
    extract_place_data
)
from .query_normalizer import build_search_query, get_alternative_queries
from .sidebar_extractor import extract_from_sidebar


def scrape_google_maps(query: str):
    """
    Scrape all Google Maps results for a given query
    
    Args:
        query: Search query string
        
    Returns:
        list: List of dictionaries containing place data
    """
    reset_stop_flag()
    results = []
    driver = None
    
    try:
        print(f"Starting scrape for: {query}")
        update_progress(status="running", current=0, total=0, message="Memulai scraping...")
        
        # Normalize query
        # Extract category and location from query
        parts = query.split(' ', 1)
        if len(parts) == 2:
            category, location = parts
            optimized_query = build_search_query(category, location)
            print(f"Original query: {query}")
            print(f"Optimized query: {optimized_query}")
            query = optimized_query
        
        # Create driver
        print("Starting Chrome...")
        update_progress(message="Membuka Chrome...")
        driver = create_chrome_driver()
        
        # Navigate to search URL
        encoded_query = quote(query)
        search_url = f"https://www.google.com/maps/search/{encoded_query}/"
        print(f"Opening URL: {search_url}")
        update_progress(message=f"Membuka Google Maps: {query}")
        
        driver.get(search_url)
        time.sleep(INITIAL_PAGE_LOAD_TIME)
        
        # Wait for results to load
        if not wait_for_results(driver):
            print("ERROR: No results found for query!")
            update_progress(
                status="error",
                message=f"Tidak ada hasil untuk query: {query}"
            )
            return results
        
        # Scroll sidebar to load all results
        scroll_sidebar(driver)
        
        # Check scraping mode
        if SCRAPE_MODE == "sidebar":
            print("=== SIDEBAR MODE: Extracting data from sidebar (FAST) ===")
            results = extract_from_sidebar(driver)
            print(f"Sidebar extraction complete: {len(results)} places")
            
        else:
            print("=== DETAIL MODE: Opening each place for full data (SLOW) ===")
            # Collect all place URLs
            all_hrefs = collect_place_urls(driver)
            
            if not all_hrefs:
                print("No place URLs found!")
                return results
            
            print(f"Collected {len(all_hrefs)} unique place URLs")
            update_progress(total=len(all_hrefs), message=f"Ditemukan {len(all_hrefs)} tempat, mulai extract data...")
            
            # Process each URL
            count = 0
            for idx, href in enumerate(all_hrefs):
                # Check stop flag
                if should_stop():
                    print("Scraping stopped by user!")
                    update_progress(
                        status="stopped", 
                        message=f"Dihentikan oleh user. Berhasil scrape {count} tempat."
                    )
                    break
                
                try:
                    print(f"\n=== Processing {idx+1}/{len(all_hrefs)} ===")
                    print(f"Opening: {href}")
                    update_progress(
                        current=idx+1,
                        current_place=f"Membuka tempat {idx+1}/{len(all_hrefs)}...",
                        message=f"Progress: {idx+1}/{len(all_hrefs)}"
                    )
                    
                    # Check if driver still alive
                    try:
                        driver.current_url
                    except:
                        print("Driver crashed, restarting...")
                        try:
                            driver.quit()
                        except:
                            pass
                        driver = create_chrome_driver()
                        time.sleep(3)
                    
                    # Open URL
                    try:
                        driver.get(href)
                        time.sleep(DETAIL_PAGE_LOAD_TIME)
                        time.sleep(DETAIL_PAGE_EXTRA_WAIT)
                    except Exception as e:
                        print(f"Failed to open URL: {e}")
                        continue
                    
                    # Extract place data
                    place_data = extract_place_data(driver, href, idx)
                    
                    if place_data:
                        results.append(place_data)
                        count += 1
                        print(f"✓ Successfully extracted {count}/{len(all_hrefs)}: {place_data['name']}")
                        update_progress(
                            current=idx+1,
                            current_place=place_data['name'],
                            message=f"✓ Berhasil: {place_data['name']} ({count} tempat)"
                        )
                    
                    # Delay between requests (dikurangi untuk lebih cepat)
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    
                except Exception as e:
                    print(f"Error processing URL {idx}: {e}")
                    continue
        
        print(f"\n=== FINAL: Total results: {len(results)} ===")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            try:
                print("Closing browser...")
                driver.quit()
            except:
                print("Browser already closed")
    
    print(f"\n=== SCRAPING COMPLETE ===")
    print(f"Total extracted: {len(results)} places")
    
    if should_stop():
        update_progress(status="stopped", message=f"Selesai (dihentikan). Total: {len(results)} tempat")
    else:
        update_progress(status="completed", message=f"Selesai! Total: {len(results)} tempat")
    
    return results
