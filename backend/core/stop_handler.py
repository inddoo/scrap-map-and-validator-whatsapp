"""
Stop signal handler for scraping operations
"""

# Global flag untuk stop scraping
_should_stop = False


def should_stop():
    """
    Check if scraping should stop
    
    Returns:
        bool: True if stop signal received
    """
    return _should_stop


def request_stop():
    """Set flag to stop scraping"""
    global _should_stop
    _should_stop = True
    print("Stop signal received!")


def reset_stop_flag():
    """Reset stop flag to allow new scraping"""
    global _should_stop
    _should_stop = False
