from dataclasses import dataclass

from .mortality_config import MortalityConfig
from .fertility_config import FertilityConfig


@dataclass(frozen=True)
class SimConfig:
    mortality: MortalityConfig
    fertility: FertilityConfig