from typing import List
import random

from models.person import Person
from services.factory import PersonFactory
from config.sim_config import SimConfig
from config.other_constants import MOTHER_FERTILITY_WINDOW, CHANCE_OF_SON
from services.utils import sample_key_by_weights, generate_calendar_day_in_year, convert_calendar_days_to_years
from services.children_gen_utils import draw_children_birth_years_exact_k
from strategies.gen_wife import gen_wife


def gen_children(*, cfg: SimConfig, father: Person, end_date: int, rng: random.Random, male_only: bool = False) -> List[Person]:
    children: List[Person] = []
    num_children = sample_key_by_weights(cfg.fertility.num_children_pd, rng)
    mother: Person = gen_wife(father=father, end_date=end_date, mother_age_cfg=cfg, rng=rng)

    fertility_end = min(MOTHER_FERTILITY_WINDOW[1], 
        father.death_year - mother.birth_year, 
        mother.death_year - mother.birth_year)
    children_birthdays: List[int] = draw_children_birth_years_exact_k(rng, 
        num_children, start_age=MOTHER_FERTILITY_WINDOW[0], stop_age=fertility_end)

    factory = PersonFactory(cfg=cfg, rng=rng)
    for birthday in children_birthdays:
        if birthday > end_date:
            break
        if rng.random() < CHANCE_OF_SON:
            children.append(factory.create_male(birth_date=birthday, end_date=end_date, father=father))
        else:
            if not male_only:
                children.append(factory.create_female(birth_date=birthday, end_date=end_date, father=father))
    
    if children_birthdays:
        marriage_year = convert_calendar_days_to_years(children_birthdays[0]) - 1 # Assume marriage one year before first child
        date_of_marriage = generate_calendar_day_in_year(marriage_year, rng)
        father.date_of_marriage = date_of_marriage
        mother.date_of_marriage = date_of_marriage

    return children


"""
This strategy generates only sons.
"""
def gen_children_male_only(*, cfg: SimConfig, father: Person, end_date: int, rng: random.Random) -> List[Person]:
    return gen_children(cfg=cfg, father=father, end_date=end_date, rng=rng, male_only=True)


"""
This strategy generates both sons and daughters normally.
"""
def gen_children_normal(*, cfg: SimConfig, father: Person, end_date: int, rng: random.Random) -> List[Person]:
    return gen_children(cfg=cfg, father=father, end_date=end_date, rng=rng)