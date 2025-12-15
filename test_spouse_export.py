import random
import os
from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import GenerousFertilityConfig
from services.simulation import generate_dynasty
from exporters.export_to_ck3 import export_to_ck3
from config.other_constants import convert_calendar_years_to_days

cfg = SimConfig(
    mortality=NormalMortalityConfig(),
    fertility=GenerousFertilityConfig(),
)

birth_year = 900
end_year = 970
end_days = convert_calendar_years_to_days(end_year)

rng = random.Random(555)
dynasty = generate_dynasty(
    birth_year=birth_year,
    male_only_start_date=convert_calendar_years_to_days(920),
    normal_start_date=convert_calendar_years_to_days(940),
    end_date=end_days,
    cfg=cfg,
    rng=rng,
    dynasty_name='TestDyn',
    culture='chinese',
)

os.makedirs('ck3_exports', exist_ok=True)
filepath = 'ck3_exports/TestDyn_with_spouse.txt'

export_to_ck3(
    dynasty=dynasty,
    filepath=filepath,
    dynasty_name='TestDyn',
    culture='han',
    religion='jingxue',
    include_death_for_living=True,
    end_date=end_days
)

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(content)
