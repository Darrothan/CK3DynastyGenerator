import random
from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import GenerousFertilityConfig
from services.simulation import generate_dynasty
from config.other_constants import convert_calendar_years_to_days

cfg = SimConfig(
    mortality=NormalMortalityConfig(),
    fertility=GenerousFertilityConfig(),  # More children = higher chance of reaching normal strategy
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

print('All people in dynasty (showing spouses):')
total = 0
for gen_idx, generation in enumerate(dynasty):
    print(f'\nGeneration {gen_idx}:')
    for person in generation:
        spouse_name = person.spouse.given_name if person.spouse else "None"
        dynasty_status = "DYNASTY" if person.dynasty_name else "non-dynasty"
        print(f'  {person.given_name} ({dynasty_status}) -> spouse: {spouse_name}')
        total += 1

print(f'\nTotal people: {total}')
