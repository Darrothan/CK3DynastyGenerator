from dataclasses import dataclass, field


# Shouldn't be used directly
@dataclass(frozen=True)
class FertilityConfig:
    num_children_pd: dict[int, float]


@dataclass(frozen=True)
class GenerousFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = field(default_factory=lambda: {
        3: 0.10,
        4: 0.25,
        5: 0.30,
        6: 0.25,
        7: 0.10,
    })


@dataclass(frozen=True)
class NormalFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = field(default_factory=lambda: {
        2: 0.10,
        3: 0.25,
        4: 0.30,
        5: 0.25,
        6: 0.10,
    })


@dataclass(frozen=True)
class RealisticFertilityConfig(FertilityConfig):
    num_children_pd: dict[int, float] = field(default_factory=lambda: {
        1: 0.10,
        2: 0.25,
        3: 0.30,
        4: 0.25,
        5: 0.10,
    })