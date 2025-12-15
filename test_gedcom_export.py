"""
Test GEDCOM export functionality.
"""

from services.simulation import generate_dynasty
from exporters.export_to_gedcom import export_to_gedcom
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from config.sim_config import SimConfig
from config.other_constants import convert_calendar_years_to_days
from models.person import Person
import random
import os


def test_gedcom_export():
    """Test that GEDCOM export creates a valid file."""
    # Create test dynasty
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 1100
    end_year = 1150
    
    end_days = convert_calendar_years_to_days(end_year)
    
    rng = random.Random(42)
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=convert_calendar_years_to_days(1120),
        normal_start_date=convert_calendar_years_to_days(1135),
        end_date=end_days,
        cfg=cfg,
        rng=rng,
        dynasty_name="TestDynasty",
        culture="chinese",
    )
    
    # Export to GEDCOM
    os.makedirs('test_exports', exist_ok=True)
    filepath = 'test_exports/test_dynasty.ged'
    
    result = export_to_gedcom(dynasty, filepath, end_year=end_year)
    
    assert os.path.exists(result), f"GEDCOM file not created at {result}"
    
    # Verify file content
    with open(result, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key GEDCOM elements
    assert "0 HEAD" in content, "Missing GEDCOM header"
    assert "SOUR CK3 Dynasty Generator" in content, "Missing source"
    assert "GEDC" in content, "Missing GEDCOM version"
    assert "0 TRLR" in content, "Missing GEDCOM trailer"
    assert "@I" in content, "Missing individual records"
    assert "@F" in content, "Missing family records"
    assert "NAME" in content, "Missing name fields"
    assert "SEX" in content, "Missing sex fields"
    assert "BIRT" in content, "Missing birth fields"
    assert "FAMS" in content or "FAMC" in content, "Missing family relationships"
    
    print(f"[OK] GEDCOM export created successfully at {result}")
    print(f"  File size: {os.path.getsize(result)} bytes")
    
    # Print first few lines
    lines = content.split('\n')[:20]
    print("\n  First 20 lines of GEDCOM file:")
    for line in lines:
        print(f"    {line}")
    
    # Count records
    indi_count = content.count("0 @I")
    fam_count = content.count("0 @F")
    print(f"\n  Records: {indi_count} individuals, {fam_count} families")


def test_gedcom_with_dynasty_names():
    """Test that dynasty names are properly included in GEDCOM."""
    person = Person(
        given_name="John",
        female=False,
        birth_year=1100,
        death_year=1150,
        is_living_at_end=False,
        dynasty_name="Smith"
    )
    
    child = Person(
        given_name="Jane",
        female=True,
        birth_year=1125,
        death_year=1180,
        is_living_at_end=False,
        dynasty_name="Smith"
    )
    
    person.children = [child]
    
    dynasty = [[person], [child]]
    
    os.makedirs('test_exports', exist_ok=True)
    filepath = 'test_exports/test_names.ged'
    export_to_gedcom(dynasty, filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "John /Smith/" in content, "Dynasty name not properly formatted in GEDCOM"
    print("[OK] Dynasty names properly formatted in GEDCOM")


if __name__ == "__main__":
    print("\nTesting GEDCOM export functionality...\n")
    test_gedcom_export()
    print()
    test_gedcom_with_dynasty_names()
    print("\n[OK] All GEDCOM export tests passed!\n")
