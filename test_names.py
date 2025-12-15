"""
Test with ASCII-compatible names to verify functionality.
"""

from services.simulation import generate_dynasty
from services.dynasty_metrics import calculate_dynasty_stats, print_dynasty_stats, print_dynasty_tree
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from config.sim_config import SimConfig
from config.other_constants import convert_calendar_years_to_days
from models.person import Person
import random


def test_name_system():
    """Test that name system works correctly."""
    # Create a person with dynasty name
    person = Person(
        given_name="John",
        female=False,
        birth_year=1100,
        death_year=1150,
        is_living_at_end=False,
        dynasty_name="Smith"
    )
    
    assert person.name == "John Smith", f"Expected 'John Smith', got '{person.name}'"
    assert person.part_of_dynasty == True, "Expected part_of_dynasty to be True"
    
    # Create a person without dynasty name
    person2 = Person(
        given_name="Jane",
        female=True,
        birth_year=1105,
        death_year=1160,
        is_living_at_end=False,
        dynasty_name=None
    )
    
    assert person2.name == "Jane", f"Expected 'Jane', got '{person2.name}'"
    assert person2.part_of_dynasty == False, "Expected part_of_dynasty to be False"
    
    print("✓ Name system works correctly")


def test_dynasty_generation():
    """Test that dynasty generation uses names correctly."""
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 1100
    end_year = 1150
    
    end_days = convert_calendar_years_to_days(end_year)
    
    # Generate dynasty with specified culture and name
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
    
    # Check founder
    founder = dynasty[0][0]
    assert founder.dynasty_name == "TestDynasty", f"Founder dynasty_name should be 'TestDynasty', got {founder.dynasty_name}"
    assert " TestDynasty" in founder.name, f"Founder name should contain ' TestDynasty', got '{founder.name}'"
    
    print(f"✓ Dynasty generation works: Founder is {founder.given_name} {founder.dynasty_name}")
    
    # Check that wives don't have dynasty name
    for generation in dynasty:
        for person in generation:
            if len(person.children) > 0:
                # This person has children, so there's a spouse
                if person.spouse:
                    assert person.spouse.dynasty_name is None, f"Spouse should not have dynasty_name"
    
    print("✓ Spouses correctly have no dynasty name")
    
    # Check stats work
    stats = calculate_dynasty_stats(dynasty, end_days)
    assert stats['founder_name'] == founder.name, f"Stats founder_name mismatch"
    print(f"✓ Metrics correctly identify founder: {stats['founder_name']}")


def test_name_manager():
    """Test that NameManager loads names correctly."""
    from services.name_manager import NameManager
    
    provider = NameManager.load_culture('chinese')
    assert len(provider.male_names) > 0, "Male names list empty"
    assert len(provider.female_names) > 0, "Female names list empty"
    
    rng = random.Random()
    male_name = provider.get_random_male_name(rng)
    female_name = provider.get_random_female_name(rng)
    
    assert isinstance(male_name, str), "Male name should be string"
    assert isinstance(female_name, str), "Female name should be string"
    assert len(male_name) > 0, "Male name should not be empty"
    assert len(female_name) > 0, "Female name should not be empty"
    
    print(f"✓ NameManager loads Chinese names: {male_name} (male), {female_name} (female)")
    
    # Check caching
    provider2 = NameManager.load_culture('chinese')
    assert provider is provider2, "NameManager should cache providers"
    print("✓ NameManager correctly caches providers")


if __name__ == "__main__":
    print("\nTesting name system components...\n")
    test_name_system()
    test_name_manager()
    test_dynasty_generation()
    print("\n✓ All tests passed!\n")
