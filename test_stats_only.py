"""
Quick test of metrics functions without full generation.
"""

from services.dynasty_metrics import calculate_dynasty_stats, print_dynasty_stats, print_dynasty_tree
from config.other_constants import convert_calendar_years_to_days
from models.person import Person


# Create minimal test dynasty
founder = Person(
    given_name="Founder",
    female=False,
    birth_year=1100,
    death_year=1150,
    is_living_at_end=False,
    dynasty_name="Test",
)

child1 = Person(
    given_name="Founder_Son1",
    female=False,
    birth_year=1130,
    death_year=1180,
    is_living_at_end=False,
    dynasty_name="Test",
)

child2 = Person(
    given_name="Founder_Daughter1",
    female=True,
    birth_year=1135,
    death_year=1170,
    is_living_at_end=False,
    dynasty_name="Test",
)

founder.children = [child1, child2]

# Minimal dynasty structure [gen0 (empty), gen1 (founder), gen2 (children)]
dynasty = [[], [founder], [child1, child2]]

# End date for metrics (year 1200)
end_date = convert_calendar_years_to_days(1200)

print("Testing stats and tree functions...\n")

# Test stats
stats = calculate_dynasty_stats(dynasty, end_date)
print_dynasty_stats(stats)

# Test tree
print_dynasty_tree(dynasty, depth=3)

print("\nTest completed successfully!")
