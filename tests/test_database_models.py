from src.database.base import Base
from src.database.models import (
    Alert,
    AnomalyScore,
    DailyProgress,
    Enumerator,
    Geofence,
    Project,
    QualityCheck,
    SurveyForm,
    SurveyResponse,
)


def test_database_models_are_importable_and_registered() -> None:
    assert Project.__tablename__ == "projects"
    assert SurveyForm.__tablename__ == "survey_forms"
    assert Enumerator.__tablename__ == "enumerators"
    assert SurveyResponse.__tablename__ == "survey_responses"
    assert Geofence.__tablename__ == "geofences"
    assert QualityCheck.__tablename__ == "quality_checks"
    assert AnomalyScore.__tablename__ == "anomaly_scores"
    assert Alert.__tablename__ == "alerts"
    assert DailyProgress.__tablename__ == "daily_progress"

    expected_tables = {
        "projects",
        "survey_forms",
        "enumerators",
        "survey_responses",
        "geofences",
        "quality_checks",
        "anomaly_scores",
        "alerts",
        "daily_progress",
    }
    assert expected_tables.issubset(set(Base.metadata.tables))
