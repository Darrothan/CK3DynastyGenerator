from __future__ import annotations
from typing import List
import random

from config.mortality_config import MortalityConfig
from config.other_constants import DAYS_IN_YEAR, DAYS_IN_MONTH

# Calendar conversions
def convert_calendar_years_to_days(year: int) -> int:
    return DAYS_IN_YEAR * (year - 1) + 1
def convert_calendar_days_to_years(days: int) -> int:
    return (days - 1) // DAYS_IN_YEAR + 1
def convert_calendar_days_to_CK3_date(days: int) -> str:
    # CK3 date format: "YYYY.MM.DD", where month and day are 1-justified
    year = convert_calendar_days_to_years(days)
    day_of_year = days - convert_calendar_years_to_days(year) + 1

    month = 1
    for dim in DAYS_IN_MONTH:
        if day_of_year <= dim:
            break
        day_of_year -= dim
        month += 1

    return f"{year}.{month}.{day_of_year}"

# Duration conversions
def convert_years_to_days_duration(years: int) -> int:
    return years * DAYS_IN_YEAR
def convert_days_to_years_duration(days: int) -> int:
    return days // DAYS_IN_YEAR


def generate_calendar_day_in_year(year: int, rng: random.Random, start=1, end=DAYS_IN_YEAR) -> int:
    start_day = convert_calendar_years_to_days(year)
    day_of_year = rng.randint(start, end)
    return start_day + day_of_year - 1


def sample_key_by_weights(pd: dict[int, float], rng: random.Random) -> int:
    ks, ws = zip(*pd.items())
    return rng.choices(ks, weights=ws, k=1)[0]


def weighted_sample_without_replacement(ks: List[int], ws: List[float], k: int, rng: random.Random) -> List[int]:
    # simple Efraimidis–Spirakis key sampling
    assert len(ks) == len(ws)
    keys = []
    for i, (x, w) in enumerate(zip(ks, ws)):
        u = rng.random()
        keys.append((u ** (1.0 / w), x))
    keys.sort(reverse=True)
    return [x for _, x in keys[:k]]


def draw_age_at_death(mcfg: MortalityConfig, rng: random.Random) -> int:
    if rng.random() < mcfg.early_probability:
        return rng.randint(*mcfg.early_range)
    return rng.randint(*mcfg.normal_range)