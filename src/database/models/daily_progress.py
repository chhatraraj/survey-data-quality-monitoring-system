from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Double, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class DailyProgress(Base):
    """Represents aggregated daily progress for a project."""

    __tablename__ = "daily_progress"

    progress_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"), nullable=False)
    progress_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed_interviews: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    target_interviews: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_percentage: Mapped[float | None] = mapped_column(Double, nullable=True)
    active_enumerators: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    quality_score: Mapped[float | None] = mapped_column(Double, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    project: Mapped["Project"] = relationship(back_populates="daily_progress")
