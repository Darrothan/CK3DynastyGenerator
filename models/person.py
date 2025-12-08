from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Person:
    name: str
    birth_year: int
    death_year: int
    is_living_at_end: bool
    children: List["Person"] = field(default_factory=list)