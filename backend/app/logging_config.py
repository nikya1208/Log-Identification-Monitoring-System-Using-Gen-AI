# C:\Users\NIKHIL\OneDrive\Desktop\logs\backend\app\logging_config.py

import logging

def setup_logging():
    """Configures logging settings for the backend application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("backend")

logger = setup_logging()
