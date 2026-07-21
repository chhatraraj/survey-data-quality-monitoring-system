"""
Database Seeder.

Creates sample records required for development and testing.
"""

from __future__ import annotations

import logging
from datetime import date

from src.database.models.enumerator import Enumerator
from src.database.models.project import Project
from src.database.models.survey_form import SurveyForm
from src.database.repositories.enumerator_repository import EnumeratorRepository
from src.database.repositories.project_repository import ProjectRepository
from src.database.repositories.survey_form_repository import (
    SurveyFormRepository,
)
from src.database.session import get_session

from src.utils.enums import EnumeratorStatus
from src.utils.enums import ProjectStatus

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Seed the development database with sample records.
    """

    logger.info("=" * 60)
    logger.info("Seeding Development Database")
    logger.info("=" * 60)

    with get_session() as session:

        project_repository = ProjectRepository(session)
        form_repository = SurveyFormRepository(session)
        enumerator_repository = EnumeratorRepository(session)

        #
        # -------------------------------------------------------
        # Project
        # -------------------------------------------------------
        #

        project = project_repository.get_by_field(
            "project_code",
            "DEMO001",
        )

        if project is None:

            project = Project(
                project_code="DEMO001",
                project_name="Survey Quality Demo",
                client_name="Demo Client",
                description="Development project.",
                target_interviews=100,
                start_date=date(2026, 7, 20),
                status=ProjectStatus.PLANNING,
            )

            project_repository.create(
                project,
                commit=False,
            )

            session.flush()

            logger.info("✓ Created demo project.")

        else:
            logger.info("✓ Demo project already exists.")

        #
        # -------------------------------------------------------
        # Survey Form
        # -------------------------------------------------------
        #

        form = form_repository.get_by_field(
            "form_name",
            "Household Survey",
        )

        if form is None:

            form = SurveyForm(
                project_id=project.project_id,
                form_name="Household Survey",
                form_version="v1",
                kobo_form_id="demo_household_form",
            )

            form_repository.create(
                form,
                commit=False,
            )

            session.flush()

            logger.info("✓ Created survey form.")

        else:
            logger.info("✓ Survey form already exists.")

        #
        # -------------------------------------------------------
        # Enumerator 1
        # -------------------------------------------------------
        #

        if not enumerator_repository.exists(
            "employee_code",
            "ENUM001",
        ):

            enumerator_repository.create(
                Enumerator(
                    project_id=project.project_id,
                    employee_code="ENUM001",
                    name="Ram Sharma",
                    district="Kathmandu",
                    province="Bagmati",
                    status=EnumeratorStatus.ACTIVE,
                ),
                commit=False,
            )

            logger.info("✓ Created Enumerator ENUM001.")

        else:
            logger.info("✓ Enumerator ENUM001 already exists.")

        #
        # -------------------------------------------------------
        # Enumerator 2
        # -------------------------------------------------------
        #

        if not enumerator_repository.exists(
            "employee_code",
            "ENUM002",
        ):

            enumerator_repository.create(
                Enumerator(
                    project_id=project.project_id,
                    employee_code="ENUM002",
                    name="Sita Karki",
                    district="Bhaktapur",
                    province="Bagmati",
                    status=EnumeratorStatus.ACTIVE,
                ),
                commit=False,
            )

            logger.info("✓ Created Enumerator ENUM002.")

        else:
            logger.info("✓ Enumerator ENUM002 already exists.")

        #
        # -------------------------------------------------------
        # Commit
        # -------------------------------------------------------
        #

        session.commit()

    logger.info("=" * 60)
    logger.info("Database seeding completed successfully.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()