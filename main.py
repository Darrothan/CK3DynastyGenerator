"""
CK3 Dynasty Generator - Interactive Wizard

Generates a multi-generation dynasty with customizable parameters and statistics.
"""

from services.simulation import generate_dynasty
from services.dynasty_metrics import calculate_dynasty_stats, print_dynasty_stats, print_dynasty_tree
from services.name_manager import NameManager
from exporters.export_to_gedcom import export_to_gedcom
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
import os


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


def get_culture() -> str:
    """Prompt user to select a culture for name generation."""
    cultures = NameManager.get_available_cultures()
    print("\n--- Dynasty Culture ---")
    for i, culture in enumerate(cultures, 1):
        print(f"{i}. {culture.capitalize()}")
    
    while True:
        try:
            choice = int(input(f"\nSelect culture (1-{len(cultures)}): ").strip())
            if 1 <= choice <= len(cultures):
                return cultures[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(cultures)}.")
        except ValueError:
            print("Please enter a valid number.")


def get_dynasty_name() -> str:
    """Prompt user to enter the dynasty name (surname)."""
    print("\n--- Dynasty Name ---")
    while True:
        name = input("Enter the dynasty surname (e.g., 'Zhu', 'Smith'): ").strip()
        if name:
            return name
        print("Dynasty name cannot be empty. Please try again.")


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


def regenerate_prompt() -> str:
    """
    Ask user if they want to save, regenerate, or exit the dynasty.
    
    Returns:
        'save' - save the dynasty to GEDCOM
        'regenerate' - create another dynasty
        'exit' - exit the program
    """
    while True:
        choice = input("\nWhat would you like to do? (s = save, r = regenerate, e = exit): ").strip().lower()
        if choice == "s":
            return "save"
        elif choice == "r":
            return "regenerate"
        elif choice == "e":
            return "exit"
        else:
            print("Please enter 's', 'r', or 'e'.")


def get_export_filename(dynasty_name: str) -> str:
    """Prompt user for export filename and ensure directory exists."""
    default_name = f"{dynasty_name.replace(' ', '_')}_tree.ged"
    
    while True:
        filename = input(f"\nEnter filename to save GEDCOM (default: {default_name}): ").strip()
        if not filename:
            filename = default_name
        
        # Ensure .ged extension
        if not filename.endswith('.ged'):
            filename += '.ged'
        
        # Create exports directory if it doesn't exist
        os.makedirs('gedcom_exports', exist_ok=True)
        filepath = os.path.join('gedcom_exports', filename)
        
        # Check if file exists and ask for confirmation
        if os.path.exists(filepath):
            overwrite = input(f"\n'{filepath}' already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite == 'y':
                return filepath
            else:
                continue
        else:
            return filepath


def main():
    print("\n" + "=" * 80)
    print("WELCOME TO THE CK3 DYNASTY GENERATOR")
    print("=" * 80)
    
    while True:
        # Get configuration
        cfg = get_config_preset()
        culture = get_culture()
        dynasty_name = get_dynasty_name()
        birth_year, end_year, male_only_start, normal_start = get_dynasty_parameters()
        
        # Convert dates to absolute days for internal use (days since year 1)
        from config.other_constants import DAYS_IN_YEAR, convert_calendar_years_to_days
        male_only_start_days = convert_calendar_years_to_days(male_only_start)
        normal_start_days = convert_calendar_years_to_days(normal_start)
        end_days = convert_calendar_years_to_days(end_year)
        
        print(f"\nGenerating {dynasty_name} dynasty starting {birth_year} and ending {end_year}...")
        
        # Generate the dynasty
        rng = random.Random()
        dynasty = generate_dynasty(
            birth_year=birth_year,
            male_only_start_date=male_only_start_days,
            normal_start_date=normal_start_days,
            end_date=end_days,
            cfg=cfg,
            rng=rng,
            dynasty_name=dynasty_name,
            culture=culture,
        )
        
        # Calculate and print statistics
        stats = calculate_dynasty_stats(dynasty, end_days)
        print_dynasty_stats(stats)
        print_dynasty_tree(dynasty, depth=2)
        
        # Ask what to do next
        choice = regenerate_prompt()
        
        if choice == "save":
            filepath = get_export_filename(dynasty_name)
            try:
                export_to_gedcom(dynasty, filepath, end_year=end_year, culture=culture, dynasty_name=dynasty_name)
                print(f"\n✓ Dynasty saved to: {filepath}")
            except Exception as e:
                import traceback
                print(f"\n✗ Error saving GEDCOM:")
                traceback.print_exc()
        elif choice == "regenerate":
            print("\nRegenerating dynasty...\n")
            continue
        elif choice == "exit":
            print("\nThank you for using the CK3 Dynasty Generator!")
            break


if __name__ == "__main__":
    main()