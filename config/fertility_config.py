from dataclasses import dataclass

# Shouldn't be used directly
@dataclass(frozen=True)
class FertilityConfig:
    num_children_pd: dict[int, float]

class GenerousFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = {
        3: 0.10,
        4: 0.25,
        5: 0.30,
        6: 0.25,
        7: 0.10,
    }

class NormalFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = {
        2: 0.10,
        3: 0.25,
        4: 0.30,
        5: 0.25,
        6: 0.10,
    }

class RealisticFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = {
        1: 0.10,
        2: 0.25,
        3: 0.30,
        4: 0.25,
        5: 0.10,
    }