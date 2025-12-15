"""
Debug test to trace the generation issue.
"""

from services.simulation import generate_dynasty
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from config.sim_config import SimConfig
from config.other_constants import convert_calendar_years_to_days
import random


def main():
    print("Testing dynasty generation with debug output...\n")
    
    # Setup
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 1100
    end_year = 1300  # Longer range for more generations
    male_only_start = 1130
    normal_start = 1160
    
    male_only_start_days = convert_calendar_years_to_days(male_only_start)
    normal_start_days = convert_calendar_years_to_days(normal_start)
    end_days = convert_calendar_years_to_days(end_year)
    
    print(f"Generating dynasty: {birth_year} - {end_year}")
    print(f"  Mainline strategy until: {male_only_start}")
    print(f"  Male-only strategy until: {normal_start}")
    print(f"  Normal strategy after: {normal_start}\n")
    
    # Generate
    rng = random.Random(42)  # Fixed seed for reproducibility
    try:
        dynasty = generate_dynasty(
            birth_year=birth_year,
            male_only_start_date=male_only_start_days,
            normal_start_date=normal_start_days,
            end_date=end_days,
            cfg=cfg,
            rng=rng,
            dynasty_name="Test",
            culture="chinese",
        )
        
        print(f"\nGeneration complete!")
        print(f"Total generations: {len(dynasty)}")
        for i, gen in enumerate(dynasty):
            print(f"  Generation {i}: {len(gen)} people")
            for person in gen[:3]:  # Show first 3
                print(f"    - {person.name} (b. {person.birth_year})")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
