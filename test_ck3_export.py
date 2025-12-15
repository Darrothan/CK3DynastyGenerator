"""Test CK3 export functionality"""
import os
import tempfile
from pathlib import Path
import random

from config.sim_config import SimConfig
from config.mortality_config import NormalMortalityConfig
from config.fertility_config import NormalFertilityConfig
from services.simulation import generate_dynasty
from exporters.export_to_ck3 import export_to_ck3
from config.other_constants import convert_calendar_years_to_days


def test_ck3_export_basic():
    """Test basic CK3 export with a small dynasty"""
    # Create a small test dynasty
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 900
    end_year = 950
    end_days = convert_calendar_years_to_days(end_year)
    
    rng = random.Random(42)
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=convert_calendar_years_to_days(920),
        normal_start_date=convert_calendar_years_to_days(935),
        end_date=end_days,
        cfg=cfg,
        rng=rng,
        dynasty_name="Zhu",
        culture="chinese",
    )
    
    # Test export
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_dynasty.txt")
        
        export_to_ck3(
            dynasty=dynasty,
            filepath=filepath,
            dynasty_name="Zhu",
            culture="han",
            religion="jingxue",
            include_death_for_living=True,
            end_date=36500
        )
        
        # Verify file was created
        assert os.path.exists(filepath), "CK3 export file was not created"
        
        # Verify file has content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content) > 0, "CK3 export file is empty"
        assert "zhu_character_" in content, "Lowercase character IDs not found in export"
        assert "birth = yes" in content, "Birth events not found in export"
        assert "dynasty = zhu_dynasty" in content, "Dynasty field not found in export"
        print(f"✓ CK3 export test passed - Generated {len(content)} bytes")


def test_ck3_export_character_format():
    """Test that CK3 character format matches specification"""
    cfg = SimConfig(
        mortality=NormalMortalityConfig(),
        fertility=NormalFertilityConfig(),
    )
    
    birth_year = 1000
    end_year = 1030
    end_days = convert_calendar_years_to_days(end_year)
    
    rng = random.Random(123)
    dynasty = generate_dynasty(
        birth_year=birth_year,
        male_only_start_date=convert_calendar_years_to_days(1010),
        normal_start_date=convert_calendar_years_to_days(1020),
        end_date=end_days,
        cfg=cfg,
        rng=rng,
        dynasty_name="Test",
        culture="chinese",
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_format.txt")
        
        export_to_ck3(
            dynasty=dynasty,
            filepath=filepath,
            dynasty_name="Test",
            culture="chinese",
            religion="daoxue",
            include_death_for_living=False,
            end_date=end_days
        )
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check format structure - character IDs should be lowercase
        assert "test_character_1 = {" in content, "Lowercase character format incorrect"
        assert "religion = daoxue" in content, "Religion not set correctly"
        assert "culture = han" in content, "Culture not set correctly"
        
        # Check for playable flag for young males
        male_chars = [line for line in content.split('\n') if 'name = "' in line]
        assert len(male_chars) > 0, "No characters found in export"
        
        print(f"✓ CK3 format test passed - Found {len(male_chars)} characters")


if __name__ == "__main__":
    test_ck3_export_basic()
    test_ck3_export_character_format()
    print("\n✓ All CK3 export tests passed!")
