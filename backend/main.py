"""
FastAPI Main Application
Google Maps Scraper & WhatsApp Business Validator
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from api.routes import (
    scrape_maps_handler,
    stop_scraping_handler,
    export_csv_handler,
    get_progress_handler,
    init_wa_checker_handler,
    validate_wa_numbers_handler,
    validate_wa_csv_handler,
    export_wa_results_handler,
    close_wa_checker_handler
)
from api.schemas import ScrapeRequest, WAValidationRequest

# Initialize FastAPI app
app = FastAPI(
    title="Google Maps Scraper & WA Validator API",
    description="API for scraping Google Maps and validating WhatsApp Business numbers",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Google Maps Scraper & WhatsApp Validator API",
        "version": "1.0.0",
        "endpoints": {
            "scraper": ["/scrape", "/progress", "/stop-scraping", "/export-csv"],
            "wa_validator": ["/wa/init", "/wa/validate", "/wa/validate-csv", "/wa/export", "/wa/close"]
        }
    }


# ============================================================
# GOOGLE MAPS SCRAPER ENDPOINTS
# ============================================================

@app.post("/scrape")
async def scrape_maps(request: ScrapeRequest):
    """Scrape Google Maps for places"""
    return await scrape_maps_handler(request)


@app.get("/progress")
def get_scraping_progress():
    """Get current scraping progress"""
    return get_progress_handler()


@app.post("/stop-scraping")
async def stop_scrape():
    """Stop ongoing scraping"""
    return await stop_scraping_handler()


@app.post("/export-csv")
async def export_csv(request: ScrapeRequest):
    """Export scraping results to CSV"""
    return await export_csv_handler(request)


# ============================================================
# WHATSAPP VALIDATOR ENDPOINTS
# ============================================================

@app.post("/wa/init")
async def init_wa_checker():
    """Initialize WhatsApp checker (scan QR code)"""
    return await init_wa_checker_handler()


@app.post("/wa/validate")
async def validate_wa_numbers(request: WAValidationRequest):
    """Validate WhatsApp numbers"""
    return await validate_wa_numbers_handler(request)


@app.post("/wa/validate-csv")
async def validate_wa_csv(file: UploadFile = File(...)):
    """Validate WhatsApp numbers from CSV file"""
    return await validate_wa_csv_handler(file)


@app.get("/wa/export")
async def export_wa_results():
    """Export WhatsApp validation results to CSV"""
    return await export_wa_results_handler()


@app.post("/wa/close")
async def close_wa_checker():
    """Close WhatsApp checker"""
    return await close_wa_checker_handler()
