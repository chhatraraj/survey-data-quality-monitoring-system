"""
Survey Quality Monitoring System

Application Entry Point
"""

from sqlalchemy import text

from src.config.settings import settings
from src.config.logging_config import get_logger
from src.database.connection import test_connection
from src.database.session import get_session

logger = get_logger(__name__)


def startup_check() -> None:
    """Run application startup validation."""

    print("=" * 60)
    print("Survey Quality Monitoring System")
    print("=" * 60)

    # -----------------------------------------
    # Configuration
    # -----------------------------------------

    logger.info("Loading configuration...")

    print(f"Environment : {settings.APP_ENV}")
    print(f"Database    : {settings.POSTGRES_DB}")
    print(f"Host        : {settings.POSTGRES_HOST}")

    # -----------------------------------------
    # Database Connection
    # -----------------------------------------

    if not test_connection():
        raise RuntimeError("Unable to connect to PostgreSQL.")

    # -----------------------------------------
    # Session Test
    # -----------------------------------------

    with get_session() as session:

        postgres_version = session.execute(
            text("SELECT version();")
        ).scalar()

        postgis_version = session.execute(
            text("SELECT PostGIS_Version();")
        ).scalar()

    print()
    print("✓ PostgreSQL Connected")
    print(f"PostgreSQL : {postgres_version}")
    print(f"PostGIS    : {postgis_version}")

    print()
    print("✓ System Ready")


if __name__ == "__main__":
    startup_check()