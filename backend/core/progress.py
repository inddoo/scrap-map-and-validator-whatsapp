"""
Progress tracking for scraping operations
"""

# Global progress tracking
_scraping_progress = {
    "status": "idle",  # idle, running, completed, stopped, error
    "current": 0,
    "total": 0,
    "current_place": "",
    "message": ""
}


def get_progress():
    """
    Get current scraping progress
    
    Returns:
        dict: Copy of current progress state
    """
    return _scraping_progress.copy()


def update_progress(status=None, current=None, total=None, current_place=None, message=None):
    """
    Update scraping progress
    
    Args:
        status: Status of scraping (idle, running, completed, stopped, error)
        current: Current item number
        total: Total items to process
        current_place: Name of current place being scraped
        message: Progress message
    """
    global _scraping_progress
    
    if status is not None:
        _scraping_progress["status"] = status
    if current is not None:
        _scraping_progress["current"] = current
    if total is not None:
        _scraping_progress["total"] = total
    if current_place is not None:
        _scraping_progress["current_place"] = current_place
    if message is not None:
        _scraping_progress["message"] = message


def reset_progress():
    """Reset progress to initial state"""
    global _scraping_progress
    _scraping_progress = {
        "status": "idle",
        "current": 0,
        "total": 0,
        "current_place": "",
        "message": ""
    }
