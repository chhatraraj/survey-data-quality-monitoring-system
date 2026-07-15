"""
Database Connection

Creates a SQLAlchemy Engine that is shared across
the entire application.
"""

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.config.settings import settings
from src.config.logging_config import get_logger


logger = get_logger(__name__)


# --------------------------------------------------
# Create SQLAlchemy Engine
# --------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

def test_connection() -> bool:
    """
    Tests whether the application can connect
    to PostgreSQL.

    Returns
    -------
    bool
        True if successful.
    """

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        logger.info("Database connection successful.")

        return True

    except SQLAlchemyError as error:

        logger.exception("Database connection failed.")

        return False