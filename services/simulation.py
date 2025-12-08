from __future__ import annotations
from typing import Optional
import random

from config.sim_config import SimConfig
from models.person import Person
from services.factory import PersonFactory


def generate_family(
	*,
	parent_name: str,
	birth_position: int,
	birth_year: int,
	end_year: int,
	cfg: SimConfig,
	child_strategy,
	rng: Optional[random.Random] = None,
) -> Person:
	rng = rng or random.Random()
	factory = PersonFactory(cfg=cfg, rng=rng)

	father = factory.create_male(parent_name, birth_position, birth_year, end_year)
	father.children = child_strategy(father=father, end_year=end_year, cfg=cfg, rng=rng)
	return father


__all__ = ["generate_family"]