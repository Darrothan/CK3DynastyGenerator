from typing import List
import random

from models.person import Person
from services.factory import PersonFactory
from config.sim_config import SimConfig
from config.fertility_config import FertilityConfig
from config.mortality_config import MainlineMortalityConfig, NonMainlineMortilityConfig
from config.other_constants import NUM_MAINLINE_CHILD_PD, FATHER_AGE_OFFSET_PD, MOTHER_FERTILITY_WINDOW
from services.utils import sample_key_by_weights
from services.children_gen_utils import draw_children_birth_years_exact_k

"""
This strategy generates only the single surviving line of male heirs.
"""
def gen_children_mainline(*, fcfg: FertilityConfig, father: Person, end_date: int, rng: random.Random) -> List[Person]:
    children: List[Person] = []
    num_children = sample_key_by_weights(fcfg.num_children_pd, rng)
    num_mainline_sons = sample_key_by_weights(NUM_MAINLINE_CHILD_PD, rng)
    father_age_offset = sample_key_by_weights(FATHER_AGE_OFFSET_PD, rng)

    mother_age_at_fathers_death = father.death_year - father.birth_year - father_age_offset
    # In other iterations where there is a mother, we will also need to contend with her own death, but this is easy because it's a stored variable
    fertility_end = min(MOTHER_FERTILITY_WINDOW[1], mother_age_at_fathers_death)  # Account for father's death
    children_birthdays = draw_children_birth_years_exact_k(rng, 
        num_children, start_age=MOTHER_FERTILITY_WINDOW[0], stop_age=fertility_end)
    sons_birthdays = sorted(rng.sample(children_birthdays, k=num_mainline_sons))

    non_main_factory = PersonFactory(cfg=SimConfig(mortality=NonMainlineMortilityConfig, fertility=fcfg), rng=rng)
    main_factory = PersonFactory(cfg=SimConfig(mortality=MainlineMortalityConfig, fertility=fcfg), rng=rng)
    for birthday in sons_birthdays[:-1]:
        if birthday > end_date:
            break
        children.append(non_main_factory.create_male(birth_date=birthday, end_date=end_date, father=father))
    # Last son is the mainline heir
    if sons_birthdays[-1] <= end_date:
        children.append(main_factory.create_male(birth_date=sons_birthdays[-1], end_date=end_date, father=father))
    for child in children[:-1]:
        child.skip_generation = True

    return children