from __future__ import annotations
from typing import Optional, List
import random

from config.sim_config import SimConfig
from config.other_constants import DAYS_IN_YEAR, MOTHER_AGE_AT_FIRST_CHILD_PD, FATHER_AGE_OFFSET_PD
from models.person import Person
from services.factory import PersonFactory
from services.utils import generate_calendar_day_in_year, convert_calendar_days_to_years, sample_key_by_weights
# Defer importing strategies to runtime to avoid circular import problems
gen_children_mainline = None
gen_children_normal = None
gen_children_male_only = None
gen_wife = None

def generate_dynasty(
	*,
	birth_year: int,
	male_only_start_date: int,
	normal_start_date: int,
	end_date: int,
	cfg: SimConfig,
	rng: Optional[random.Random] = None,
) -> List[List['Person']]:
	rng = rng or random.Random()
	factory = PersonFactory(cfg=cfg, rng=rng)

	# import strategies here to avoid circular imports at module import time
	from strategies import gen_children_mainline as _gcm, gen_children as _gc, gen_wife as _gw
	global gen_children_mainline, gen_children_male_only, gen_wife
	gen_children_mainline = _gcm.gen_children_mainline
	gen_children_male_only = _gc.gen_children_male_only
	gen_children_normal = _gc.gen_children_normal
	gen_wife = _gw.gen_wife

	founder: Person = factory.create_male(birth_date=generate_calendar_day_in_year(birth_year, rng), end_date=end_date)
	# Outer list is generations, inner list is people in that generation
	dynasty: List[List['Person']] = [[founder]]
	max_generations = 1000  # Limit to prevent infinite loops
	generation = 0

	while generation < len(dynasty) and generation < max_generations:
		next_generation: List[Person] = []
		
		for father in dynasty[generation]:
			if father.skip_generation:
				continue

			if father.date_of_birth < male_only_start_date:
				# Mainline strategy
				father.children = gen_children_mainline(fcfg=cfg.fertility, father=father, end_date=end_date, rng=rng)
			elif father.date_of_birth < normal_start_date:
				# Male-only strategy
				father.children = gen_children_male_only(cfg=cfg, father=father, end_date=end_date, rng=rng)
			else:
				# Normal strategy
				father.children = gen_children_normal(cfg=cfg, father=father, end_date=end_date, rng=rng)
			
			next_generation.extend(father.children)
		
		# Only add the next generation if there are children
		if next_generation:
			dynasty.append(next_generation)
		
		generation += 1

	return dynasty


__all__ = ["generate_dynasty"]