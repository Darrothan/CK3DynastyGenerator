"""
Test the new metrics functionality.
"""

from services.simulation import generate_dynasty
from services.dynasty_metrics import calculate_dynasty_stats, print_dynasty_stats, print_dynasty_tree
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from config.sim_config import SimConfig
from config.other_constants import convert_calendar_years_to_days
import random


def main():
    print("Testing new dynasty metrics...\n")
    
    # Setup
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 1100
    end_year = 1200
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
    rng = random.Random(42)
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=male_only_start_days,
        normal_start_date=normal_start_days,
        end_date=end_days,
        cfg=cfg,
        rng=rng,
    )
    
    # Calculate and display metrics
    stats = calculate_dynasty_stats(dynasty, end_days)
    print_dynasty_stats(stats)
    print_dynasty_tree(dynasty, depth=2)
    
    print("\nMetrics test completed!")


if __name__ == "__main__":
    main()
