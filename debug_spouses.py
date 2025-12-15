import random
from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from services.simulation import generate_dynasty
from config.other_constants import convert_calendar_years_to_days

cfg = SimConfig(
    mortality=NormalMortalityConfig(),
    fertility=NormalFertilityConfig(),
)

birth_year = 1000
end_year = 1050
end_days = convert_calendar_years_to_days(end_year)

rng = random.Random(888)
dynasty = generate_dynasty(
    birth_year=birth_year,
    male_only_start_date=convert_calendar_years_to_days(1010),
    normal_start_date=convert_calendar_years_to_days(1020),
    end_date=end_days,
    cfg=cfg,
    rng=rng,
    dynasty_name='Testing',
    culture='chinese',
)

print('All people in dynasty:')
for gen_idx, generation in enumerate(dynasty):
    print(f'Generation {gen_idx}:')
    for person in generation:
        spouse_name = person.spouse.given_name if person.spouse else "None"
        print(f'  {person.given_name} - dynasty={person.dynasty_name}, spouse={spouse_name}')
