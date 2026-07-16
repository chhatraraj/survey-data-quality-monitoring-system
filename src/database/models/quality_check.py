"""
Quality Check ORM Model
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.utils.enums import SeverityLevel

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.survey_response import SurveyResponse


class QualityCheck(Base):
    """
    Stores rule-based data quality validation results.
    """

    __tablename__ = "quality_checks"

    quality_check_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    response_id: Mapped[int] = mapped_column(
        ForeignKey(
            "survey_responses.response_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    rule_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    severity: Mapped[SeverityLevel] = mapped_column(
        Enum(SeverityLevel),
        nullable=False,
    )

    message: Mapped[str | None] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    response: Mapped["SurveyResponse"] = relationship(
        back_populates="quality_checks",
    )

    def __repr__(self) -> str:
        return (
            f"<QualityCheck("
            f"id={self.quality_check_id}, "
            f"rule='{self.rule_name}', "
            f"severity='{self.severity}'"
            f")>"
        )