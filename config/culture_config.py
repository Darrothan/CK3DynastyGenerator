"""
Culture-specific configuration for name handling and GEDCOM export.

Defines naming conventions and conventions for each supported culture.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CultureConfig:
    """Configuration for a specific culture's naming conventions."""
    
    # Whether spouses take the main dynasty member's surname
    # True = spouses take husband's surname (patrilineal: English, German, etc.)
    # False = spouses keep own names or don't take husband's (Chinese, Vietnamese, etc.)
    wives_take_husband_surname: bool
    
    # Whether to export non-dynasty spouses in GEDCOM
    # True = include all spouses (patrilineal cultures)
    # False = only include spouses who are part of dynasty (matrilineal/patronymic cultures)
    export_non_dynasty_spouses: bool


# Culture configurations
CULTURE_CONFIGS: Dict[str, CultureConfig] = {
    "chinese": CultureConfig(
        wives_take_husband_surname=False,
        export_non_dynasty_spouses=False,
    ),
    "english": CultureConfig(
        wives_take_husband_surname=True,
        export_non_dynasty_spouses=True,
    ),
    "french": CultureConfig(
        wives_take_husband_surname=True,
        export_non_dynasty_spouses=True,
    ),
    "german": CultureConfig(
        wives_take_husband_surname=True,
        export_non_dynasty_spouses=True,
    ),
}


def get_culture_config(culture: str) -> CultureConfig:
    """Get the configuration for a culture. Defaults to English if not found."""
    return CULTURE_CONFIGS.get(culture, CULTURE_CONFIGS["english"])
