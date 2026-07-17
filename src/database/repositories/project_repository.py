"""Repository helpers for projects."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.database.models.project import Project
from src.database.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for project-related database operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, Project)

    def get_by_code(self, project_code: str) -> Project | None:
        return self.session.query(Project).filter(Project.project_code == project_code).first()

    def get_active_projects(self) -> list[Project]:
        return list(
            self.session.query(Project)
            .filter(Project.status == "Active")
            .all()
        )
