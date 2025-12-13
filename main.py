# main.py
from services.simulation import generate_dynasty
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from config.sim_config import SimConfig


# Minimal example SimConfig for quick testing. Replace with real data later.
mcfg = NormalMortalityConfig()
fcfg = NormalFertilityConfig()
cfg = SimConfig(mortality=mcfg, fertility=fcfg)


dynasty = generate_dynasty(
    birth_year=1100,
    male_only_start_date=1130,
    normal_start_date=1160,
    end_date=1200,
    cfg=cfg,
)

print(dynasty)

# want to eventually have the user enter info like start date, patriarch name, etc.