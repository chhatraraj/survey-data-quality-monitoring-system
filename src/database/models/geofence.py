"""
Geofence ORM Model
"""

from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class Geofence(Base):
    """
    Represents a geographic survey boundary.
    """

    __tablename__ = "geofences"

    geofence_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.project_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    geofence_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    area: Mapped[object] = mapped_column(
        Geography(
            geometry_type="POLYGON",
            srid=4326,
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<Geofence("
            f"id={self.geofence_id}, "
            f"name='{self.geofence_name}'"
            f")>"
        )