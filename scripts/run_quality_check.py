"""
Integration test for the Quality Engine.
"""

import logging

from src.database.session import get_session
from src.database.repositories.survey_response_repository import (
    SurveyResponseRepository,
)
from src.core.dependencies import create_quality_service

logger = logging.getLogger(__name__)


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    logger.info("Starting quality validation...")

    with get_session() as session:

        response_repository = SurveyResponseRepository(session)

        quality_service = create_quality_service(session)

        responses = response_repository.get_all()

        if not responses:
            logger.info("No survey responses found.")
            return

        for response in responses:

            logger.info(
                "Validating response %s",
                response.response_id,
            )

            results = quality_service.validate(response)

            for result in results:

                if result.passed:
                    logger.info(
                        "PASS | %s",
                        result.rule_name,
                    )
                else:
                    logger.warning(
                        "FAIL | %s | %s",
                        result.rule_name,
                        result.message,
                    )

    logger.info("Quality validation completed.")


if __name__ == "__main__":
    main()