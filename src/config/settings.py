"""
Application Configuration

Loads environment variables from the .env file and
provides a centralized configuration object for
the entire application.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Project Root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --------------------------------------------------
# Load .env
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Central configuration for the application.
    """

    # ----------------------------------------------
    # Application
    # ----------------------------------------------

    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # ----------------------------------------------
    # PostgreSQL
    # ----------------------------------------------

    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    # ----------------------------------------------
    # SQLAlchemy Connection URL
    # ----------------------------------------------

    DATABASE_URL = (
        f"postgresql://"
        f"{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/"
        f"{POSTGRES_DB}"
    )


settings = Settings()