# main.py
from strategies.gen_children_mainline import dynasty_children
from services.simulation import generate_family
from config.mortality_config import MortalityConfig
from config.fertility_config import FertilityConfig
from config.sim_config import SimConfig


# Minimal example SimConfig for quick testing. Replace with real data later.
mcfg = MortalityConfig(early_range=(0, 20), normal_range=(40, 80), early_probability=0.1)
fcfg = FertilityConfig(
    father_age_offset_pd={0: 1.0},
    mother_first_child_age_pd={20: 1.0},
    children_attempted_pd={1: 0.7, 2: 0.2, 3: 0.1},
    birth_prob_by_mother_age_pd={age: 1.0 for age in range(20, 41)},
)
cfg = SimConfig(mortality=mcfg, fertility=fcfg)


father = generate_family(
    parent_name="Zhang",
    birth_position=1,
    birth_year=1100,
    end_year=1200,
    cfg=cfg,
    child_strategy=dynasty_children,
)

print(father)

# want to eventually have the user enter info like start date, patriarch name, etc.