from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Alert(Base):
    """Represents a generated alert linked to a survey response."""

    __tablename__ = "alerts"

    alert_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    response_id: Mapped[int | None] = mapped_column(ForeignKey("survey_responses.response_id"), nullable=True)
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Open")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    survey_response: Mapped["SurveyResponse"] = relationship(back_populates="alerts")
