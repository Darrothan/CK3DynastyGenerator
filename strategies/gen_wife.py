import random

from models.person import Person
from config.sim_config import SimConfig
from config.other_constants import MOTHER_AGE_AT_FIRST_CHILD_PD, FATHER_AGE_OFFSET_PD
from services.factory import PersonFactory
from services.utils import (
    sample_key_by_weights,
    generate_calendar_day_in_year,
)


def gen_wife(*, father: Person, end_date: int, cfg: SimConfig, rng: random.Random) -> Person:
    mother_age_at_first_child = sample_key_by_weights(MOTHER_AGE_AT_FIRST_CHILD_PD, rng)
    father_age_offset = sample_key_by_weights(FATHER_AGE_OFFSET_PD, rng)
    mother_birth_year = father.birth_year + father_age_offset
    mother_birthday = generate_calendar_day_in_year(mother_birth_year, rng)

    factory = PersonFactory(cfg=cfg, rng=rng)
    wife: Person = factory.create_female(mother_birthday, end_date=end_date, father=None, mother=None)
    wife.dynasty_name = None  # Wife is not part of the dynasty
    father.spouse = wife
    wife.spouse = father
    wife.mother_age_at_first_child = mother_age_at_first_child

    return wife