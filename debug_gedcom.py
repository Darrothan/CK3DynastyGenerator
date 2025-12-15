"""Debug GEDCOM export issue."""

from services.simulation import generate_dynasty
from config.mortality_config import GenerousMortalityConfig
from config.fertility_config import GenerousFertilityConfig
from config.sim_config import SimConfig
from exporters.export_to_gedcom import export_to_gedcom
import random

# Create config - matching "Generous" preset from wizard
mortality = GenerousMortalityConfig()
fertility = GenerousFertilityConfig()
cfg = SimConfig(mortality=mortality, fertility=fertility)

# Set seed for reproducibility
random.seed(42)

# Generate dynasty with same parameters as test
rng = random.Random()
birth_year = 598
end_year = 867

# Convert years to days (DAYS_IN_YEAR = 365)
DAYS_IN_YEAR = 365
birth_days = (birth_year - 1) * DAYS_IN_YEAR + 1
end_days = (end_year - 1) * DAYS_IN_YEAR + 1
male_only_start_days = (767 - 1) * DAYS_IN_YEAR + 1
normal_start_days = (817 - 1) * DAYS_IN_YEAR + 1

print(f"Generating dynasty from {birth_year} to {end_year}...")
print(f"  Birth days: {birth_days}")
print(f"  End days: {end_days}")

dynasty = generate_dynasty(
    birth_year=birth_days,
    male_only_start_date=male_only_start_days,
    normal_start_date=normal_start_days,
    end_date=end_days,
    cfg=cfg,
    rng=rng,
    dynasty_name='Zhu',
    culture='chinese',
)

print(f"Dynasty generated with {sum(len(g) for g in dynasty)} people")

# Now try to export
filepath = 'test_exports/debug_zhu.ged'
print(f"\nAttempting to export to {filepath}...")

try:
    result = export_to_gedcom(dynasty, filepath, end_year=end_year, culture="chinese", dynasty_name="Zhu")
    print(f"✓ Success! Exported to: {result}")
    
    # Check file size
    import os
    size = os.path.getsize(result)
    print(f"  File size: {size} bytes")
    
except Exception as e:
    import traceback
    print("✗ Error occurred:")
    traceback.print_exc()
    print(f"\nException type: {type(e)}")
    print(f"Exception args: {e.args}")
