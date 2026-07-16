"""
Survey Response ORM Model
"""

from datetime import datetime
from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Double
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class SurveyResponse(Base):
    """
    Represents a single submitted survey interview.
    """

    __tablename__ = "survey_responses"

    response_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    form_id: Mapped[int] = mapped_column(
        ForeignKey("survey_forms.form_id", ondelete="CASCADE"),
        nullable=False,
    )

    enumerator_id: Mapped[int] = mapped_column(
        ForeignKey("enumerators.enumerator_id", ondelete="CASCADE"),
        nullable=False,
    )

    submission_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    interview_duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
    )

    latitude: Mapped[float | None] = mapped_column(
        Double,
    )

    longitude: Mapped[float | None] = mapped_column(
        Double,
    )

    location: Mapped[object | None] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
        )
    )

    household_id: Mapped[str | None] = mapped_column(
        String(100),
    )

    respondent_age: Mapped[int | None] = mapped_column(
        Integer,
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
    )

    device_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    raw_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<SurveyResponse("
            f"id={self.response_id}, "
            f"household='{self.household_id}', "
            f"enumerator={self.enumerator_id}"
            f")>"
        )