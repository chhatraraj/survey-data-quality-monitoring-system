"""
Database Connection

Creates and manages a singleton SQLAlchemy Engine
for the Survey Quality Monitoring System.
"""

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(__name__)

# --------------------------------------------------
# Singleton Engine
# --------------------------------------------------

_engine: Engine | None = None


def get_engine() -> Engine:
    """
    Returns a singleton SQLAlchemy Engine.

    The engine is created only once and reused
    throughout the application.
    """

    global _engine

    if _engine is None:

        logger.info("Creating database engine...")

        _engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            future=True,
        )

    return _engine


# --------------------------------------------------
# Health Check
# --------------------------------------------------

def test_connection() -> bool:
    """
    Tests connectivity to PostgreSQL.

    Returns
    -------
    bool
        True if the connection succeeds.
    """

    try:

        engine = get_engine()

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        logger.info("Database connection successful.")

        return True

    except SQLAlchemyError:

        logger.exception("Database connection failed.")

        return False