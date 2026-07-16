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

def __repr__(self) -> str:
    return (
        f"<SurveyForm("
        f"id={self.form_id}, "
        f"name='{self.form_name}', "
        f"version='{self.form_version}'"
        f")>"
    )    