# logger.py — Sets up application-wide logging

import logging
import os
from datetime import datetime

def setup_logger():
    """Configure and return the application logger."""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Log filename with date stamp
    log_filename = f"logs/email_log_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_filename),    # Write to file
            logging.StreamHandler()                # Also print to terminal
        ]
    )
    
    logger = logging.getLogger("EmailAutomation")
    logger.info("=" * 60)
    logger.info("Email Automation & Reminder System Started")
    logger.info("=" * 60)
    return logger