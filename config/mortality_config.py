from dataclasses import dataclass


@dataclass(frozen=True)
class MortalityConfig:
    early_range: tuple[int, int]
    normal_range: tuple[int, int]
    early_probability: float


@dataclass(frozen=True)
class GenerousMortalityConfig(MortalityConfig):
    early_probability: float


@dataclass(frozen=True)
class NormalMortalityConfig(MortalityConfig):
    pass


@dataclass(frozen=True)
class RealisticMortalityConfig(MortalityConfig):
    early_range: tuple[int, int]
    normal_range: tuple[int, int]
    early_probability: float