"""
Simple runner script for the API server
"""
import uvicorn
from config.settings import API_HOST, API_PORT

if __name__ == "__main__":
    print("=" * 60)
    print("🗺️  Google Maps Scraper & WhatsApp Validator API")
    print("=" * 60)
    print(f"Starting server at http://{API_HOST}:{API_PORT}")
    print("Press CTRL+C to stop")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
        log_level="info"
    )
