from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class SurveyResponse(Base):
    """Represents a completed survey interview."""

    __tablename__ = "survey_responses"

    response_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"), nullable=False)
    form_id: Mapped[int] = mapped_column(ForeignKey("survey_forms.form_id"), nullable=False)
    enumerator_id: Mapped[int] = mapped_column(ForeignKey("enumerators.enumerator_id"), nullable=False)
    submission_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    interview_duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Double, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Double, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    household_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    respondent_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    project: Mapped["Project"] = relationship(back_populates="survey_responses")
    survey_form: Mapped["SurveyForm"] = relationship(back_populates="survey_responses")
    enumerator: Mapped["Enumerator"] = relationship(back_populates="survey_responses")
    quality_checks: Mapped[list["QualityCheck"]] = relationship(back_populates="survey_response", cascade="all, delete-orphan")
    anomaly_scores: Mapped[list["AnomalyScore"]] = relationship(back_populates="survey_response", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="survey_response", cascade="all, delete-orphan")
