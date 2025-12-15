"""Quick demo of CK3 export functionality"""
import random
import os

from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from services.simulation import generate_dynasty
from exporters.export_to_ck3 import export_to_ck3
from config.other_constants import convert_calendar_years_to_days


def demo_ck3_export():
    """Generate a small dynasty and export to CK3 format"""
    
    print("=" * 60)
    print("CK3 Dynasty Export Demo")
    print("=" * 60)
    
    # Create configuration
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    # Parameters
    birth_year = 867
    end_year = 900
    end_days = convert_calendar_years_to_days(end_year)
    
    print(f"\nGenerating dynasty from {birth_year} to {end_year}...")
    rng = random.Random(999)
    
    # Generate dynasty
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=convert_calendar_years_to_days(880),
        normal_start_date=convert_calendar_years_to_days(890),
        end_date=end_days,
        cfg=cfg,
        rng=rng,
        dynasty_name="Zhu",
        culture="chinese",
    )
    
    print(f"Generated {len(dynasty)} people in the dynasty")
    
    # Create export directory
    os.makedirs("ck3_exports", exist_ok=True)
    filepath = "ck3_exports/Zhu_demo.txt"
    
    # Export to CK3 format
    print(f"\nExporting to {filepath}...")
    export_to_ck3(
        dynasty=dynasty,
        filepath=filepath,
        dynasty_name="Zhu",
        culture="han",
        religion="jingxue",
        include_death_for_living=True,
        end_date=end_days
    )
    
    print(f"✓ Export complete!")
    
    # Show preview
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    preview_lines = min(30, len(lines))
    
    print(f"\nFirst {preview_lines} lines of output:")
    print("-" * 60)
    for line in lines[:preview_lines]:
        print(line)
    if len(lines) > preview_lines:
        print(f"... ({len(lines) - preview_lines} more lines)")
    print("-" * 60)
    
    print(f"\nTotal file size: {len(content)} bytes")
    print(f"Total characters in export: {len(dynasty)}")
    
    # Count events
    birth_count = content.count("birth = yes")
    marriage_count = content.count("add_spouse")
    death_count = content.count("death = yes")
    
    print(f"\nEvent summary:")
    print(f"  Births: {birth_count}")
    print(f"  Marriages: {marriage_count // 2}")  # Each marriage appears twice
    print(f"  Deaths: {death_count}")


if __name__ == "__main__":
    demo_ck3_export()
