import random
import constants

def weighted_sample_without_replacement(population, weights, k):
    """Pick up to k distinct items with weights; no replacement."""
    items = list(population)
    w = list(weights)
    chosen = []
    for _ in range(min(k, len(items))):
        idx = random.choices(range(len(items)), weights=w, k=1)[0]
        chosen.append(items.pop(idx))
        w.pop(idx)
    return chosen

class MalePerson:
    def __init__(self, parent_name, birth_position, birth_year, END_YEAR):
        self.name = f"{parent_name}_Son{birth_position}"
        self.birth_year = birth_year

        # lifespan
        self.age_at_death = (
            random.randint(*constants.EARLY_MORTALITY_RANGE)
            if random.random() < constants.EARLY_MORTALITY_PROBABILITY
            else random.randint(*constants.NORMAL_MORTALITY_RANGE)
        )
        self.death_year = birth_year + self.age_at_death
        self.is_living = self.death_year > END_YEAR  # keep or change to >= per your definition

        # father–mother age offset
        self.age_offset = random.choices(
            population=list(constants.PD_FATHER_AVERAGE_AGE_OFFSET.keys()),
            weights=list(constants.PD_FATHER_AVERAGE_AGE_OFFSET.values()),
            k=1
        )[0]

        # mother’s age at first child
        wife_age_of_first_child = random.choices(
            population=list(constants.PD_MOTHER_AGE_OF_FIRST_CHILD.keys()),
            weights=list(constants.PD_MOTHER_AGE_OF_FIRST_CHILD.values()),
            k=1
        )[0]

        # how many kids attempted
        number_of_children_attempted = random.choices(
            population=list(constants.PD_NOTABLE_MALE_CHILDREN.keys()),
            weights=list(constants.PD_NOTABLE_MALE_CHILDREN.values()),
            k=1
        )[0]

        # fertility ages ≥ first-child age
        clamped = {
            age: p for age, p in constants.PD_CHILD_BY_MOTHER_AGE.items()
            if age >= wife_age_of_first_child
        }

        # sample mother ages (weighted, no replacement)
        sampled_mother_ages = weighted_sample_without_replacement(
            population=list(clamped.keys()),
            weights=list(clamped.values()),
            k=number_of_children_attempted
        )

        # convert to father's ages, chronological
        father_ages_at_birth = sorted(age + self.age_offset for age in sampled_mother_ages)

        # drop births after father's death or after END_YEAR
        father_ages_at_birth = [
            a for a in father_ages_at_birth
            if a <= self.age_at_death and (self.birth_year + a) <= END_YEAR
        ]

        # spawn children
        self.children = [
            MalePerson(
                parent_name=self.name,
                birth_position=i + 1,
                birth_year=self.birth_year + a,
                END_YEAR=END_YEAR
            )
            for i, a in enumerate(father_ages_at_birth)
        ]

    def __str__(self):
        return f"MalePerson(name={self.name}, birth_year={self.birth_year}, death_year={self.death_year}, is_living={self.is_living}, children_count={len(self.children)})"