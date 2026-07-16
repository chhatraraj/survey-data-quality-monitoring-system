"""
Project ORM Model
"""

from datetime import date
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class Project(Base):
    """
    Represents a survey project.
    """

    __tablename__ = "projects"

    project_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    project_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    project_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    target_interviews: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Planning"
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

def __repr__(self) -> str:
    return (
        f"<Project("
        f"id={self.project_id}, "
        f"name='{self.project_name}', "
        f"code='{self.project_code}'"
        f")>"
    )