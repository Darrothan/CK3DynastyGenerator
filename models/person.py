from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Person:
    given_name: str
    female: bool
    birth_year: int
    death_year: int
    is_living_at_end: bool
    
    # Optional fields with defaults
    dynasty_name: str | None = None
    skip_generation: bool = False

    father: Person | None = None
    mother: Person | None = None
    spouse: Person | None = None

    # Recordkeeping dates
    date_of_birth: Optional[int] = None
    date_of_death: Optional[int] = None
    date_of_marriage: Optional[int] = None

    # Simulator variables
    mother_age_at_first_child: int = -1

    children: List["Person"] = field(default_factory=list)

    @property
    def name(self) -> str:
        """Return full name combining given name and dynasty name."""
        if self.dynasty_name:
            return f"{self.given_name} {self.dynasty_name}"
        return self.given_name
    
    @property
    def part_of_dynasty(self) -> bool:
        """Check if person is part of the main dynasty."""
        return self.dynasty_name is not None