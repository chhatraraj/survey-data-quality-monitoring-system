"""
Machine Learning Anomaly Score ORM Model
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Double
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import Base
from src.utils.enums import MLAlgorithm

if TYPE_CHECKING:
    from src.database.models.survey_response import SurveyResponse


class AnomalyScore(Base):
    """
    Stores machine learning anomaly detection results
    for survey responses.
    """

    __tablename__ = "anomaly_scores"

    anomaly_score_id: Mapped[int] = mapped_column(
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

    algorithm: Mapped[MLAlgorithm] = mapped_column(
        Enum(
            MLAlgorithm,
            name="mlalgorithm",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    anomaly_score: Mapped[float] = mapped_column(
        Double,
        nullable=False,
    )

    prediction: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    response: Mapped["SurveyResponse"] = relationship(
        back_populates="anomaly_scores",
    )

    def __repr__(self) -> str:
        return (
            f"<AnomalyScore("
            f"id={self.anomaly_score_id}, "
            f"algorithm='{self.algorithm}', "
            f"score={self.anomaly_score:.3f}, "
            f"prediction={self.prediction}"
            f")>"
        )