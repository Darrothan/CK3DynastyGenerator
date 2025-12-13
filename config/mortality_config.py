from dataclasses import dataclass

# Shouldn't be used directly
@dataclass(frozen=True)
class MortalityConfig:
    early_range: tuple[int, int]
    normal_range: tuple[int, int]
    early_probability: float

class MainlineMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (-1, -1)
    normal_range: tuple[int, int] = (40, 70)
    early_probability: 0

class NonMainlineMortilityConfig(MortalityConfig):
    early_range: tuple[int, int] = (25, 49)
    normal_range: tuple[int, int] = (50, 70)
    early_probability: 0.80

class GenerousMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (25, 49)
    normal_range: tuple[int, int] = (50, 70)
    early_probability: 0.1

class NormalMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (20, 49)   # some die before or just as they start families
    normal_range: tuple[int, int] = (50, 70)
    early_probability: 0.25

class RealisticMortalityConfig(MortalityConfig):
    early_range: tuple[int, int] = (16, 49)   # some die before or just as they start families
    normal_range: tuple[int, int] = (50, 70)
    early_probability: 0.45 # almost half die early