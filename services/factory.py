from dataclasses import dataclass, field
import random

from models.person import Person
from config.sim_config import SimConfig
from services.utils import draw_age_at_death


@dataclass
class PersonFactory:
    cfg: SimConfig
    rng: random.Random = field(default_factory=random.Random)

    def create_male(self, parent_name: str, birth_position: int, birth_year: int, end_year: int) -> Person:
        age_at_death = draw_age_at_death(self.cfg.mortality, self.rng)
        death_year = birth_year + age_at_death
        return Person(
            name=f"{parent_name}_Son{birth_position}",
            birth_year=birth_year,
            death_year=death_year,
            is_living_at_end=(death_year > end_year),
        )