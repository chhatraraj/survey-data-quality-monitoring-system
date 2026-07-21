"""
Enumerator ORM Model
"""

from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.utils.enums import EnumeratorStatus

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.project import Project
    from src.database.models.survey_response import SurveyResponse


class Enumerator(Base):
    """
    Represents a field enumerator assigned
    to a survey project.
    """

    __tablename__ = "enumerators"

    enumerator_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    employee_code: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
    )

    province: Mapped[str | None] = mapped_column(
        String(100),
    )

    status: Mapped[EnumeratorStatus] = mapped_column(
        Enum(
            EnumeratorStatus,
            name="enumeratorstatus",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        default=EnumeratorStatus.ACTIVE,
        nullable=False,
    )

    joined_at: Mapped[date | None] = mapped_column(
        Date,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project: Mapped["Project"] = relationship(
        back_populates="enumerators",
    )

    responses: Mapped[list["SurveyResponse"]] = relationship(
        back_populates="enumerator",
    )

    def __repr__(self) -> str:
        return (
            f"<Enumerator("
            f"id={self.enumerator_id}, "
            f"employee='{self.employee_code}', "
            f"name='{self.name}'"
            f")>"
        )