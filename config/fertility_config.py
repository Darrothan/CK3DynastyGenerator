from dataclasses import dataclass


@dataclass(frozen=True)
class FertilityConfig:
    father_age_offset_pd: dict[int, float]
    mother_first_child_age_pd: dict[int, float]
    children_attempted_pd: dict[int, float]
    birth_prob_by_mother_age_pd: dict[int, float]


@dataclass(frozen=True)
class GenerousFertilityConfig(FertilityConfig):
    children: dict[int, float]
    male_children: dict[int, float]


@dataclass(frozen=True)
class NormalFertilityConfig(FertilityConfig):
    children: dict[int, float]
    male_children: dict[int, float]


@dataclass(frozen=True)
class RealisticFertilityConfig(FertilityConfig):
    children: dict[int, float]
    male_children: dict[int, float]