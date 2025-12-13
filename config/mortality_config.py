from dataclasses import dataclass

# Shouldn't be used directly
@dataclass(frozen=True)
class MortalityConfig:
    early_range: tuple[int, int]
    normal_range: tuple[int, int]
    early_probability: float

from dataclasses import dataclass


@dataclass(frozen=True)
class MainlineMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (-1, -1)
    normal_range: tuple[int, int] = (40, 70)
    early_probability: float = 0.0


@dataclass(frozen=True)
class NonMainlineMortilityConfig(MortalityConfig):
    early_range: tuple[int, int] = (25, 49)
    normal_range: tuple[int, int] = (50, 70)
    early_probability: float = 0.80


@dataclass(frozen=True)
class GenerousMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (25, 49)
    normal_range: tuple[int, int] = (50, 70)
    early_probability: float = 0.1


@dataclass(frozen=True)
class NormalMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (20, 49)   # some die before or just as they start families
    normal_range: tuple[int, int] = (50, 70)
    early_probability: float = 0.25


@dataclass(frozen=True)
class RealisticMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (16, 49)   # some die before or just as they start families
    normal_range: tuple[int, int] = (50, 70)
    early_probability: float = 0.45 # almost half die early