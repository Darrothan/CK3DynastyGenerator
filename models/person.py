from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Person:
    name: str
    female: bool
    birth_year: int
    death_year: int
    is_living_at_end: bool
    skip_generation: bool = False
    part_of_dynasty: bool = True

    father: Person | None = None
    mother: Person | None = None
    sppouse: Person | None = None

    # Recordkeeping dates
    date_of_birth: Optional[int] = None
    date_of_death: Optional[int] = None
    date_of_marriage: Optional[int] = None

    # Simulator variables
    mother_age_at_first_child: int = -1

    children: List["Person"] = field(default_factory=list)