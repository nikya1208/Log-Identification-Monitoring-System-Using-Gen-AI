# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\utils.py

from datetime import datetime

def get_timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def format_log_message(level: str, message: str) -> str:
    """Formats a log message with a timestamp."""
    return f"[{get_timestamp()}] {level.upper()}: {message}"
