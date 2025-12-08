from typing import Protocol, List
import random

from models.person import Person
from config.sim_config import SimConfig


class ChildGenStrategy(Protocol):
    def __call__(self, *, father: Person, end_year: int, cfg: SimConfig, rng: random.Random) -> List[Person]: ...