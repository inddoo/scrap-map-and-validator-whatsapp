"""
API route handlers
"""
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import csv
import io
import pandas as pd

from scrapers import scrape_google_maps
from core import get_progress, request_stop, update_progress
from .schemas import ScrapeRequest, WAValidationRequest, WAValidationResponse, WAValidationResult

# Thread pool for async execution
executor = ThreadPoolExecutor(max_workers=3)

# Global storage for last scrape results
last_scrape_results = []

# Global WA checker instance
wa_checker = None


async def scrape_maps_handler(request: ScrapeRequest):
    """
    Handle scraping request
    
    Args:
        request: ScrapeRequest with query
        
    Returns:
        dict: Success status, data, and count
    """
    global last_scrape_results
    
    try:
        print(f"Scraping query: {request.query}")
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            scrape_google_maps,
            request.query
        )
        print(f"Scraping completed. Found {len(results)} results")
        
        # Save results for export
        last_scrape_results = results
        
        return {"success": True, "data": results, "count": len(results)}
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def stop_scraping_handler():
    """
    Handle stop scraping request
    
    Returns:
        dict: Success status and message
    """
    try:
        request_stop()
        update_progress(status="stopping", message="Menghentikan scraping...")
        return {"success": True, "message": "Scraping stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def export_csv_handler(request: ScrapeRequest):
    """
    Handle CSV export request
    
    Args:
        request: ScrapeRequest with query (for filename)
        
    Returns:
        StreamingResponse: CSV file download
    """
    global last_scrape_results
    
    try:
        print(f"Exporting CSV for query: {request.query}")
        print(f"Last scrape results count: {len(last_scrape_results)}")
        
        # Debug: print first result
        if last_scrape_results:
            print(f"First result: {last_scrape_results[0]}")
        
        # Check if data exists
        if not last_scrape_results:
            print("ERROR: No data to export!")
            raise HTTPException(
                status_code=400,
                detail="No data to export. Please scrape first."
            )
        
        print(f"Creating CSV with {len(last_scrape_results)} rows...")
        
        # Create CSV with UTF-8 BOM for Excel compatibility
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=['name', 'phone', 'website', 'rating', 'reviews_count', 'category', 
                       'address', 'plus_code', 'hours', 'price_level', 'price_range', 
                       'latitude', 'longitude', 'link']
        )
        writer.writeheader()
        
        # Write rows with error handling
        for idx, row in enumerate(last_scrape_results):
            try:
                writer.writerow(row)
            except Exception as e:
                print(f"Error writing row {idx}: {e}")
                print(f"Row data: {row}")
        
        # Get CSV content and encode
        csv_content = output.getvalue()
        print(f"CSV content preview (first 200 chars): {csv_content[:200]}")
        
        csv_bytes = csv_content.encode('utf-8-sig')  # UTF-8 with BOM
        print(f"CSV content length: {len(csv_bytes)} bytes")
        
        # Clean filename
        safe_query = request.query.replace(' ', '_').replace(',', '').replace('/', '_')
        filename = f"google_maps_{safe_query}.csv"
        print(f"Sending file: {filename}")
        
        # Return as file download
        response = StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        print("Response created successfully!")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during CSV export: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def get_progress_handler():
    """
    Handle progress request
    
    Returns:
        dict: Current progress state
    """
    return get_progress()


async def init_wa_checker_handler():
    """
    Initialize WhatsApp checker - FIXED VERSION
    
    Returns:
        dict: Success status and message
    """
    global wa_checker
    
    try:
        # Import Query checker with logging
        from wa_validator.wa_checker_with_logging import WAQueryChecker
        
        if wa_checker is not None:
            return {"success": True, "message": "WhatsApp checker already initialized"}
        
        print("Initializing WhatsApp checker...", flush=True)
        wa_checker = WAQueryChecker()
        
        loop = asyncio.get_event_loop()
        
        print("Setting up Chrome driver...", flush=True)
        try:
            await loop.run_in_executor(executor, wa_checker.setup_driver)
            print("✓ Chrome driver setup complete", flush=True)
        except Exception as e:
            print(f"Error setup: {e}", flush=True)
            wa_checker = None
            raise HTTPException(status_code=500, detail=f"Gagal setup Chrome: {str(e)}")
        
        print("Starting WhatsApp Web login...", flush=True)
        try:
            login_success = await loop.run_in_executor(executor, wa_checker.login_whatsapp)
            print(f"Login result: {login_success}", flush=True)
        except Exception as e:
            print(f"Error login: {e}", flush=True)
            if wa_checker and wa_checker.driver:
                try:
                    wa_checker.driver.quit()
                except:
                    pass
            wa_checker = None
            raise HTTPException(status_code=500, detail=f"Gagal login: {str(e)}")
        
        if not login_success:
            if wa_checker and wa_checker.driver:
                try:
                    wa_checker.driver.quit()
                except:
                    pass
            wa_checker = None
            raise HTTPException(status_code=500, detail="Login timeout")
        
        return {
            "success": True, 
            "message": "WhatsApp checker ready! Session tersimpan."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        if wa_checker and wa_checker.driver:
            try:
                wa_checker.driver.quit()
            except:
                pass
        wa_checker = None
        
        raise HTTPException(status_code=500, detail=str(e))


async def validate_wa_numbers_handler(request: WAValidationRequest):
    """
    Validate WhatsApp numbers - QUERY METHOD
    Menggunakan Store.QueryExist untuk validasi cepat!
    
    Args:
        request: WAValidationRequest with phone_numbers list
        
    Returns:
        WAValidationResponse: Validation results
    """
    global wa_checker
    
    try:
        if wa_checker is None:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp checker not initialized. Please call /wa/init first."
            )
        
        # Check if still logged in
        if not wa_checker.is_logged_in:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp session expired. Please call /wa/init again to re-login."
            )
        
        print(f"Validating {len(request.phone_numbers)} numbers using Query Method...")
        
        # Gunakan validate_numbers yang sudah batch processing
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            wa_checker.validate_numbers,
            request.phone_numbers
        )
        
        # Check if validation failed (empty results)
        if not results:
            raise HTTPException(
                status_code=400,
                detail="Validation failed. WhatsApp session might be expired. Please call /wa/init again."
            )
        
        # Get summary
        summary = wa_checker.get_summary()
        
        return {
            "success": True,
            "results": results,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error validating: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def validate_wa_csv_handler(file: UploadFile = File(...)):
    """
    Validate WhatsApp numbers from CSV file
    
    Args:
        file: Uploaded CSV file
        
    Returns:
        WAValidationResponse: Validation results
    """
    global wa_checker
    
    try:
        if wa_checker is None:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp checker not initialized. Please call /wa/init first."
            )
        
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Find phone column
        phone_column = None
        for col in df.columns:
            if 'phone' in col.lower() or 'telepon' in col.lower() or 'nomor' in col.lower():
                phone_column = col
                break
        
        if phone_column is None:
            raise HTTPException(
                status_code=400,
                detail=f"Phone column not found. Available columns: {', '.join(df.columns)}"
            )
        
        print(f"Found phone column: {phone_column}")
        print(f"Total rows: {len(df)}")
        
        # Extract phone numbers
        phone_numbers = df[phone_column].dropna().astype(str).tolist()
        
        # Validate using the same handler
        request = WAValidationRequest(phone_numbers=phone_numbers)
        return await validate_wa_numbers_handler(request)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error validating CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def export_wa_results_handler():
    """
    Export WhatsApp validation results to CSV
    
    Returns:
        StreamingResponse: CSV file download
    """
    global wa_checker
    
    try:
        if wa_checker is None or not wa_checker.results:
            raise HTTPException(
                status_code=400,
                detail="No validation results to export. Please validate numbers first."
            )
        
        print(f"Exporting {len(wa_checker.results)} WA validation results...")
        
        # Create CSV
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=['phone', 'clean_phone', 'has_whatsapp', 'is_business', 'business_name', 'status']
        )
        writer.writeheader()
        
        for row in wa_checker.results:
            writer.writerow(row)
        
        csv_content = output.getvalue()
        csv_bytes = csv_content.encode('utf-8-sig')
        
        filename = "wa_validation_results.csv"
        
        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error exporting WA results: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def close_wa_checker_handler():
    """
    Close WhatsApp checker
    
    Returns:
        dict: Success status and message
    """
    global wa_checker
    
    try:
        if wa_checker is None:
            return {"success": True, "message": "WhatsApp checker not initialized"}
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, wa_checker.close)
        wa_checker = None
        
        return {"success": True, "message": "WhatsApp checker closed"}
        
    except Exception as e:
        print(f"Error closing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Global WA sender instance
wa_sender = None


async def send_wa_message_handler(request):
    """
    Send single WhatsApp message
    
    Args:
        request: WASendMessageRequest
        
    Returns:
        dict: Send result
    """
    global wa_checker, wa_sender
    
    try:
        if wa_checker is None or wa_checker.driver is None:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp not initialized. Please call /wa/init first."
            )
        
        # Initialize sender if not exists
        if wa_sender is None:
            from wa_validator.wa_sender import WAAutoSender
            wa_sender = WAAutoSender(wa_checker.driver)
        
        print(f"Sending message to: {request.phone}")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            wa_sender.send_message,
            request.phone,
            request.message,
            request.delay
        )
        
        return {
            "success": True,
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def send_wa_bulk_handler(request):
    """
    Send bulk WhatsApp messages
    
    Args:
        request: WASendBulkRequest
        
    Returns:
        WASendResponse: Send results and summary
    """
    global wa_checker, wa_sender
    
    try:
        if wa_checker is None or wa_checker.driver is None:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp not initialized. Please call /wa/init first."
            )
        
        # Initialize sender if not exists
        if wa_sender is None:
            from wa_validator.wa_sender import WAAutoSender
            wa_sender = WAAutoSender(wa_checker.driver)
        
        print(f"Sending bulk messages to {len(request.phone_numbers)} numbers")
        
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            wa_sender.send_bulk_messages,
            request.phone_numbers,
            request.message,
            request.min_delay,
            request.max_delay,
            request.stop_on_error
        )
        
        summary = wa_sender.get_summary()
        
        return {
            "success": True,
            "results": results,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error sending bulk messages: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def send_wa_personalized_handler(request):
    """
    Send personalized WhatsApp messages
    
    Args:
        request: WASendPersonalizedRequest
        
    Returns:
        WASendResponse: Send results and summary
    """
    global wa_checker, wa_sender
    
    try:
        if wa_checker is None or wa_checker.driver is None:
            raise HTTPException(
                status_code=400,
                detail="WhatsApp not initialized. Please call /wa/init first."
            )
        
        # Initialize sender if not exists
        if wa_sender is None:
            from wa_validator.wa_sender import WAAutoSender
            wa_sender = WAAutoSender(wa_checker.driver)
        
        print(f"Sending personalized messages to {len(request.contacts)} contacts")
        
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            wa_sender.send_personalized_messages,
            request.contacts,
            request.message_template,
            request.min_delay,
            request.max_delay
        )
        
        summary = wa_sender.get_summary()
        
        return {
            "success": True,
            "results": results,
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error sending personalized messages: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
