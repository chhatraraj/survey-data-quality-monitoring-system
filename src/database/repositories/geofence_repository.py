"""Repository helpers for geofences."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.geofence import Geofence
from src.database.repositories.base_repository import BaseRepository


class GeofenceRepository(BaseRepository[Geofence]):
    """Repository for geofence operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, Geofence)

    def get_by_project(self, project_id: int) -> list[Geofence]:
        return list(
            self.session.query(Geofence)
            .filter(Geofence.project_id == project_id)
            .all()
        )
