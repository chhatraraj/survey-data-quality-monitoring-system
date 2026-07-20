"""
Survey Form ORM Model
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.project import Project
    from src.database.models.survey_response import SurveyResponse


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

    # Class Relationships
    project: Mapped["Project"] = relationship(
        back_populates="forms"
    )

    responses: Mapped[list["SurveyResponse"]] = relationship(
        back_populates="form",
        cascade="all, delete-orphan",
    )

    # Instance Methods
    def __repr__(self) -> str:
        return (
            f"<SurveyForm("
            f"id={self.form_id}, "
            f"name='{self.form_name}', "
            f"version='{self.form_version}'"
            f")>"
        )