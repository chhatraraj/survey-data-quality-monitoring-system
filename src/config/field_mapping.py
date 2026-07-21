"""
Survey mapping configuration loader.
"""

from pathlib import Path

import yaml


_CONFIG_FILE = (
    Path(__file__).resolve()
    .parents[2]
    / "config"
    / "survey_mapping.yaml"
)


def load_field_mapping() -> dict[str, str]:
    """
    Load survey field mapping configuration.
    """

    with _CONFIG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    return config["survey_response"]["fields"]