"""Compatibility layer: small adapter that re-exports the project's
core types and helpers from their new locations so older import paths
keep working while the refactor completes.
"""

from models.person import Person
from config.sim_config import SimConfig
from services.simulation import generate_family
from services.utils import draw_age_at_death
from strategies.gen_children_mainline import dynasty_children, family_children
from strategies.base import ChildGenStrategy
from models.generation_type import GenerationType


def pick_strategy(gen_type: GenerationType, cutoff_year: int, reference_year: int) -> ChildGenStrategy:
    if reference_year < cutoff_year:
        return dynasty_children if gen_type == GenerationType.DYNASTY else family_children
    else:
        return family_children


__all__ = [
    "Person",
    "SimConfig",
    "generate_family",
    "draw_age_at_death",
    "dynasty_children",
    "family_children",
    "GenerationType",
    "pick_strategy",
]