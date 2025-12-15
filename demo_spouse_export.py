"""Demo showing non-dynasty spouse inclusion in CK3 export"""
import random
import os

from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from services.simulation import generate_dynasty
from exporters.export_to_ck3 import export_to_ck3
from config.other_constants import convert_calendar_years_to_days


def demo_spouse_export():
    """Demonstrate that non-dynasty spouses are exported"""
    
    print("=" * 70)
    print("CK3 EXPORT - SPOUSE INCLUSION DEMO")
    print("=" * 70)
    print("\nThis demo shows:")
    print("1. Non-dynasty wives are now included in CK3 export")
    print("2. They appear in marriage events but without dynasty field")
    print()
    
    # Create configuration
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    # Parameters - normal generation creates wives
    birth_year = 1000
    end_year = 1050
    end_days = convert_calendar_years_to_days(end_year)
    
    print(f"Generating dynasty from {birth_year} to {end_year}...")
    print("Using normal generation strategy (creates wives)...")
    rng = random.Random(888)
    
    # Generate dynasty - use broader date range for normal strategy
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=convert_calendar_years_to_days(1010),
        normal_start_date=convert_calendar_years_to_days(1020),
        end_date=end_days,
        cfg=cfg,
        rng=rng,
        dynasty_name="Testing",
        culture="chinese",
    )
    
    # Count people and spouses
    dynasty_members = 0
    total_spouses = 0
    non_dynasty_spouses = 0
    
    for generation in dynasty:
        for person in generation:
            if person.part_of_dynasty:
                dynasty_members += 1
            if person.spouse:
                total_spouses += 1
                if not person.spouse.part_of_dynasty:
                    non_dynasty_spouses += 1
    
    print(f"\nDynasty Statistics:")
    print(f"  Dynasty members: {dynasty_members}")
    print(f"  Total characters with spouses: {total_spouses}")
    print(f"  Non-dynasty spouses: {non_dynasty_spouses}")
    
    # Create export directory
    os.makedirs("ck3_exports", exist_ok=True)
    filepath = "ck3_exports/Testing_spouse_demo.txt"
    
    # Export to CK3 format
    print(f"\nExporting to {filepath}...")
    export_to_ck3(
        dynasty=dynasty,
        filepath=filepath,
        dynasty_name="Testing",
        culture="han",
        religion="jingxue",
        include_death_for_living=False,
        end_date=end_days
    )
    
    # Analyze the export
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Count exported characters
    exported_chars = content.count("_character_")
    dynasty_in_export = content.count("dynasty = Testing")
    non_dynasty_in_export = content.count("name =") - dynasty_in_export
    marriage_events = content.count("add_spouse")
    
    print(f"\nExport Analysis:")
    print(f"  Total characters exported: {exported_chars}")
    print(f"  Dynasty members in export: {dynasty_in_export}")
    print(f"  Non-dynasty members in export: {non_dynasty_in_export}")
    print(f"  Marriage events: {marriage_events}")
    
    print(f"\n✓ Export complete!")
    print(f"  Non-dynasty spouses are included (no dynasty field)")
    print(f"  They appear in marriage events as add_spouse targets")
    
    # Show a sample with spouse
    print(f"\nSample (showing character with spouse):")
    print("-" * 70)
    in_sample = False
    sample_lines = 0
    for line in lines:
        if "add_spouse" in line and sample_lines < 30:
            in_sample = True
        if in_sample:
            print(line)
            sample_lines += 1
            if "}" in line and sample_lines > 5:
                break
    print("-" * 70)


if __name__ == "__main__":
    demo_spouse_export()
