"""
CK3 Dynasty Generator - Interactive Wizard

Generates a multi-generation dynasty with customizable parameters and statistics.
"""

from services.simulation import generate_dynasty
from services.dynasty_metrics import calculate_dynasty_stats, print_dynasty_stats, print_dynasty_tree
from config.mortality_config import (
    NormalMortalityConfig,
    GenerousMortalityConfig,
    RealisticMortalityConfig,
)
from config.fertility_config import (
    NormalFertilityConfig,
    GenerousFertilityConfig,
    RealisticFertilityConfig,
)
from config.sim_config import SimConfig
from typing import Tuple
import random


def get_config_preset() -> SimConfig:
    """Present user with preset config options."""
    print("\n--- Dynasty Configuration Preset ---")
    print("1. Normal (balanced mortality & fertility)")
    print("2. Generous (high fertility, low mortality)")
    print("3. Realistic (high early mortality, moderate fertility)")
    
    while True:
        choice = input("\nSelect preset (1-3): ").strip()
        if choice == "1":
            return SimConfig(
                mortality=NormalMortalityConfig(),
                fertility=NormalFertilityConfig(),
            )
        elif choice == "2":
            return SimConfig(
                mortality=GenerousMortalityConfig(),
                fertility=GenerousFertilityConfig(),
            )
        elif choice == "3":
            return SimConfig(
                mortality=RealisticMortalityConfig(),
                fertility=RealisticFertilityConfig(),
            )
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_dynasty_parameters() -> Tuple[int, int, int, int]:
    """Collect start year, end year, and strategy transition dates from user."""
    print("\n--- Dynasty Time Parameters ---")
    
    while True:
        try:
            birth_year = int(input("Enter patriarch birth year (e.g., 1100): "))
            end_year = int(input("Enter simulation end year (e.g., 1200): "))
            if birth_year >= end_year:
                print("Birth year must be before end year. Try again.")
                continue
            
            print("\nStrategy transitions:")
            print("  - Before 'male_only_start': mainline strategy (only male heirs)")
            print("  - Before 'normal_start': male-only strategy (sons only)")
            print("  - After 'normal_start': normal strategy (mixed children)")
            
            male_only_start = int(input(f"Male-only strategy starts (year between {birth_year} and {end_year}): "))
            normal_start = int(input(f"Normal strategy starts (year between {male_only_start} and {end_year}): "))
            
            if not (birth_year <= male_only_start <= normal_start <= end_year):
                print("Dates must be in order. Try again.")
                continue
            
            return birth_year, end_year, male_only_start, normal_start
        except ValueError:
            print("Please enter valid integer years.")


def regenerate_prompt() -> bool:
    """Ask user if they want to regenerate the dynasty."""
    while True:
        choice = input("\nGenerate another dynasty? (y/n): ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Please enter 'y' or 'n'.")


def main():
    print("\n" + "=" * 80)
    print("WELCOME TO THE CK3 DYNASTY GENERATOR")
    print("=" * 80)
    
    while True:
        # Get configuration
        cfg = get_config_preset()
        birth_year, end_year, male_only_start, normal_start = get_dynasty_parameters()
        
        # Convert dates to absolute days for internal use (days since year 1)
        # For now, keep it simple: 1 day = 1 day, and we'll convert years to days
        from config.other_constants import DAYS_IN_YEAR, convert_calendar_years_to_days
        male_only_start_days = convert_calendar_years_to_days(male_only_start)
        normal_start_days = convert_calendar_years_to_days(normal_start)
        end_days = convert_calendar_years_to_days(end_year)
        
        print(f"\nGenerating dynasty starting {birth_year} and ending {end_year}...")
        
        # Generate the dynasty
        rng = random.Random()
        dynasty = generate_dynasty(
            birth_year=birth_year,
            male_only_start_date=male_only_start_days,
            normal_start_date=normal_start_days,
            end_date=end_days,
            cfg=cfg,
            rng=rng,
        )
        
        # Calculate and print statistics
        stats = calculate_dynasty_stats(dynasty, end_days)
        print_dynasty_stats(stats)
        print_dynasty_tree(dynasty, depth=2)
        
        # Ask to regenerate or exit
        if not regenerate_prompt():
            print("\nThank you for using the CK3 Dynasty Generator!")
            break


if __name__ == "__main__":
    main()