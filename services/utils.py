from __future__ import annotations
from typing import List
import random

from config.mortality_config import MortalityConfig


def sample_key_by_weights(pd: dict[int, float], rng: random.Random) -> int:
    ks, ws = zip(*pd.items())
    return rng.choices(ks, weights=ws, k=1)[0]


def weighted_sample_without_replacement(ks: List[int], ws: List[float], k: int, rng: random.Random) -> List[int]:
    # simple Efraimidis–Spirakis key sampling
    import math
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