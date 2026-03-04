"""
Configuration settings for the scraper application
"""

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:5173"]

# Scraper Settings
SCROLL_WAIT_TIME = 4  # seconds (ditambah untuk memberi waktu loading data baru)
SCROLL_MAX_ATTEMPTS = 100
SCROLL_NO_CHANGE_THRESHOLD = 2  # stop after 2 consecutive no-changes

# Scraping Mode
SCRAPE_MODE = "detail"  # "sidebar" (cepat, data terbatas) atau "detail" (lambat, data lengkap)
# sidebar: Ambil data dari sidebar saja (nama, rating, alamat, link) - SANGAT CEPAT
# detail: Buka setiap tempat untuk data lengkap (+ phone, website, hours, dll) - LAMBAT tapi LENGKAP

# Page Load Settings
INITIAL_PAGE_LOAD_TIME = 5  # seconds
FEED_WAIT_TIME = 15  # seconds
ITEMS_CHECK_ATTEMPTS = 5
MIN_ITEMS_BEFORE_SCROLL = 3
PRE_SCROLL_WAIT = 2  # seconds
PRE_COLLECT_WAIT = 3  # seconds (ditambah untuk koneksi lambat)
DETAIL_PAGE_LOAD_TIME = 4  # seconds
DETAIL_PAGE_EXTRA_WAIT = 1  # seconds
DELAY_BETWEEN_REQUESTS = 1  # seconds

# Extraction Settings
EXTRACTION_TIMEOUT = 10  # seconds - max time to extract one place
SKIP_ON_TIMEOUT = True  # Skip place if extraction takes too long

# Chrome Settings
CHROME_HEADLESS = False  # Set to True for headless mode
CHROME_ARGS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--start-maximized',
    '--disable-blink-features=AutomationControlled',
    '--lang=id-ID'
]
