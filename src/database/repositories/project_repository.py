"""
Repository for Project model.

Provides project-specific database operations.
"""

from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.project import Project
from src.database.repositories.base_repository import BaseRepository
from src.utils.enums import ProjectStatus


class ProjectRepository(BaseRepository[Project]):
    """
    Repository responsible for Project database operations.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository.
        """
        super().__init__(session, Project)

    # ---------------------------------------------------------
    # Project Queries
    # ---------------------------------------------------------

    def get_by_code(self, project_code: str) -> Project | None:
        """
        Retrieve a project using its unique project code.
        """

        stmt = (
            select(Project)
            .where(Project.project_code == project_code)
        )

        return self.session.scalar(stmt)

    def get_active_projects(self) -> list[Project]:
        """
        Retrieve all active projects.
        """

        stmt = (
            select(Project)
            .where(
                Project.status == ProjectStatus.ACTIVE,
                Project.is_deleted.is_(False),
            )
            .order_by(Project.project_name)
        )

        return list(self.session.scalars(stmt))

    def get_by_client(self, client_name: str) -> list[Project]:
        """
        Retrieve all projects belonging to a client.
        """

        stmt = (
            select(Project)
            .where(
                Project.client_name == client_name,
                Project.is_deleted.is_(False),
            )
            .order_by(Project.project_name)
        )

        return list(self.session.scalars(stmt))

    # ---------------------------------------------------------
    # Soft Delete
    # ---------------------------------------------------------

    def soft_delete(self, project: Project) -> Project:
        """
        Soft delete a project.

        The project remains in the database but is marked as deleted.
        """

        project.is_deleted = True
        project.deleted_at = datetime.now(UTC)

        self.session.commit()
        self.session.refresh(project)

        return project

    def restore(self, project: Project) -> Project:
        """
        Restore a previously soft-deleted project.
        """

        project.is_deleted = False
        project.deleted_at = None

        self.session.commit()
        self.session.refresh(project)

        return project          