"""
Database Session

Creates SQLAlchemy sessions that are used by the
application to interact with PostgreSQL.
"""

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from src.database.connection import get_engine


# --------------------------------------------------
# Session Factory
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=get_engine(),
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# --------------------------------------------------
# Context Manager
# --------------------------------------------------

@contextmanager
def get_session() -> Session:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

