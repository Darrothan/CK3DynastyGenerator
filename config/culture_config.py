"""
Culture-specific configuration for name handling and exports.

Defines naming conventions for each supported culture.
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
    
    # CK3 culture code (may differ from the culture name used internally)
    # e.g., "chinese" -> "han" in CK3, but most others map directly
    ck3_culture_code: str = None  # If None, uses the culture name directly


# Culture configurations
CULTURE_CONFIGS: Dict[str, CultureConfig] = {
    "chinese": CultureConfig(
        wives_take_husband_surname=False,
        ck3_culture_code="han",
    ),
    "english": CultureConfig(
        wives_take_husband_surname=True,
        ck3_culture_code="english",
    ),
    "french": CultureConfig(
        wives_take_husband_surname=True,
        ck3_culture_code="french",
    ),
    "german": CultureConfig(
        wives_take_husband_surname=True,
        ck3_culture_code="german",
    ),
}


def get_culture_config(culture: str) -> CultureConfig:
    """Get the configuration for a culture. Defaults to English if not found."""
    return CULTURE_CONFIGS.get(culture, CULTURE_CONFIGS["english"])


def get_ck3_culture_code(culture: str) -> str:
    """Get the CK3 culture code for a culture."""
    config = get_culture_config(culture)
    return config.ck3_culture_code or culture
