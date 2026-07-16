"""
Daily Progress ORM Model
"""

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Double
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.project import Project


class DailyProgress(Base):
    """
    Stores aggregated daily project progress.
    """

    __tablename__ = "daily_progress"

    daily_progress_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.project_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    progress_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    interviews_completed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    daily_target: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    completion_percentage: Mapped[float] = mapped_column(
        Double,
        nullable=False,
    )

    active_enumerators: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project: Mapped["Project"] = relationship(
        back_populates="daily_progress",
    )

    def __repr__(self) -> str:
        return (
            f"<DailyProgress("
            f"project={self.project_id}, "
            f"date={self.progress_date}, "
            f"completion={self.completion_percentage:.1f}%"
            f")>"
        )