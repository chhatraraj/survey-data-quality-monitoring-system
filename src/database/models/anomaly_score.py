from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Double, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class AnomalyScore(Base):
    """Represents an anomaly detection score for a survey response."""

    __tablename__ = "anomaly_scores"

    anomaly_score_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("survey_responses.response_id"), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(100), nullable=False)
    anomaly_score: Mapped[float] = mapped_column(Double, nullable=False)
    prediction: Mapped[str] = mapped_column(String(20), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    survey_response: Mapped["SurveyResponse"] = relationship(back_populates="anomaly_scores")
