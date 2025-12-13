from dataclasses import dataclass, field
import random

from models.person import Person
from config.sim_config import SimConfig
from config.other_constants import FATHER_AGE_OFFSET_PD, DAYS_IN_YEAR
from services.utils import draw_age_at_death, sample_key_by_weights, convert_calendar_years_to_days, convert_calendar_days_to_years, generate_calendar_day_in_year


@dataclass
class PersonFactory:
    cfg: SimConfig
    rng: random.Random = field(default_factory=random.Random)

    def create_person(self, birth_date: int, end_date: int, female: bool = False, father: Person = None, mother: Person = None) -> Person:
        age_at_death = draw_age_at_death(self.cfg.mortality, self.rng)
        birth_year = convert_calendar_days_to_years(birth_date)
        death_year = birth_year + age_at_death

        # Recordkeeping dates
        date_of_death = generate_calendar_day_in_year(death_year, self.rng)
        return Person(
            name="TODO",
            female=female,
            father=father,
            mother=mother,
            birth_year=birth_year,
            death_year=death_year,
            is_living_at_end=(date_of_death > end_date),

            # Recordkeeping dates
            date_of_birth=birth_date,
            date_of_death=date_of_death,
        )

    def create_male(self, birth_date: int, end_date: int, father: Person = None, mother: Person = None) -> Person:
        person = self.create_person(birth_date, end_date, False, father, mother)
        if father is not None and getattr(father, "name", None):
            person.name = f"{father.name}_Son"
        else:
            person.name = "Founder_Son"
        
        # Skip generation for males age 30 or less at end of simulation
        person_age_at_end = end_date - person.date_of_birth
        if person_age_at_end < self.cfg.playable_character_age_max * DAYS_IN_YEAR:
            person.skip_generation = True
        
        return person
    
    def create_female(self, birth_date: int, end_date: int, father: Person = None, mother: Person = None) -> Person:
        person = self.create_person(birth_date, end_date, True, father, mother)
        if father is not None and getattr(father, "name", None):
            person.name = f"{father.name}_Daughter"
        else:
            person.name = "Founder_Daughter"
        person.skip_generation = True
        return person