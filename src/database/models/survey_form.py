"""
Survey Form ORM Model
"""

from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from src.database.models.project import Project
    from src.database.models.survey_response import SurveyResponse

forms: Mapped[list["SurveyForm"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)

enumerators: Mapped[list["Enumerator"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)

responses: Mapped[list["SurveyResponse"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)

geofences: Mapped[list["Geofence"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)

alerts: Mapped[list["Alert"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)

daily_progress: Mapped[list["DailyProgress"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)
class SurveyForm(Base):
    """
    Represents a survey form belonging to a project.
    """

    __tablename__ = "survey_forms"

    form_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    form_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    form_version: Mapped[str | None] = mapped_column(
        String(50),
    )

    kobo_form_id: Mapped[str | None] = mapped_column(
        String(255),
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
    back_populates="forms"
)

responses: Mapped[list["SurveyResponse"]] = relationship(
    back_populates="form",
    cascade="all, delete-orphan",
)

def __repr__(self) -> str:
    return (
        f"<SurveyForm("
        f"id={self.form_id}, "
        f"name='{self.form_name}', "
        f"version='{self.form_version}'"
        f")>"
    )    