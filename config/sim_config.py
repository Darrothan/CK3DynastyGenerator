from dataclasses import dataclass

from .mortality_config import MortalityConfig
from .fertility_config import FertilityConfig


@dataclass(frozen=True)
class SimConfig:
    mortality: MortalityConfig
    fertility: FertilityConfig
    playable_character_age_max: int = 30  # characters younger than this age can have families generated