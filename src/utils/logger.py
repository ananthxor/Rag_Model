import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "RAG_App"):
    """
    Sets up a logger that matches the user's request:
    1. Logs to a file (rag_app.log)
    2. Logs to console
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if setup is called multiple times
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. File Handler (Rotating to save space, 1MB limit, backup 3 files)
    file_handler = RotatingFileHandler('rag_app.log', maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def print_trace(step: str, details: str):
    """
    Prints a highly visible trace log for the user to follow the request flow.
    """
    border = "=" * 60
    print(f"\n{border}")
    print(f"🔍 [TRACE] STEP: {step}")
    print(f"{border}")
    print(f"{details}")
    print(f"{border}\n")

logger = setup_logger()
