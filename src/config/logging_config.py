"""
Logging Configuration

Provides a centralized logging system for the
Survey Quality Monitoring System.

Logs are written to:
1. Console
2. logs/application.log
"""

import logging
from pathlib import Path


# --------------------------------------------------
# Create logs directory if it doesn't exist
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)


LOG_FILE = LOG_DIR / "application.log"


# --------------------------------------------------
# Configure Logger
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    name : str
        Usually __name__ from the calling module.

    Returns
    -------
    logging.Logger
    """
    return logging.getLogger(name)