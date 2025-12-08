from typing import List
import random

from models.person import Person
from config.sim_config import SimConfig
from services.utils import (
    sample_key_by_weights,
    weighted_sample_without_replacement,
    draw_age_at_death,
)


def dynasty_children(*, father: Person, end_year: int, cfg: SimConfig, rng: random.Random) -> List[Person]:
    fcfg = cfg.fertility
    age_offset = sample_key_by_weights(fcfg.father_age_offset_pd, rng)
    mother_first = sample_key_by_weights(fcfg.mother_first_child_age_pd, rng)
    attempted = sample_key_by_weights(fcfg.children_attempted_pd, rng)

    # clamp to mother ages >= first-child age
    clamped = {a:p for a,p in fcfg.birth_prob_by_mother_age_pd.items() if a >= mother_first}

    # sample distinct mother ages (weighted, no replacement)
    ks, ws = list(clamped.keys()), list(clamped.values())
    sampled_mother_ages = weighted_sample_without_replacement(ks, ws, min(attempted, len(ks)), rng)

    # convert to father's ages; chronological
    father_ages = sorted(a + age_offset for a in sampled_mother_ages)

    # births within father’s life and before end_year
    births = []
    for i, fa in enumerate(father_ages, start=1):
        by = father.birth_year + fa
        if by > end_year: break
        # if you want to enforce "before father dies", keep father's death on the Person or pass separately
        child = Person(
            name=f"{father.name}_Son{i}",
            birth_year=by,
            death_year=by + draw_age_at_death(cfg.mortality, rng),
            is_living_at_end=(by + draw_age_at_death(cfg.mortality, rng)) > end_year,
        )
        births.append(child)
    return births

def family_children(*, father: Person, end_year: int, cfg: SimConfig, rng: random.Random) -> List[Person]:
    # identical shape as dynasty_children; if differences are small, call a shared helper with a mode flag.
    return dynasty_children(father=father, end_year=end_year, cfg=cfg, rng=rng)