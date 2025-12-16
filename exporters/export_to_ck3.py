"""
CK3 History File Exporter

Converts a generated dynasty into a CK3-compatible history file format.
Characters are represented with full genealogy, life events (birth, marriage, death),
and proper CK3 field formatting.
"""

from typing import List, Dict, Tuple
from models.person import Person
from services.utils import convert_calendar_days_to_years
from config.other_constants import DAYS_IN_MONTH, DAYS_IN_YEAR


def convert_absolute_day_to_date(absolute_day: int) -> Tuple[int, int, int]:
    """
    Convert absolute day (days since year 1) to (year, month, day).
    
    Args:
        absolute_day: Days since year 1 (1-indexed)
    
    Returns:
        Tuple of (year, month, day)
    """
    # Convert to 0-indexed
    day_zero_indexed = absolute_day - 1
    
    # Calculate year
    year = day_zero_indexed // DAYS_IN_YEAR + 1
    
    # Days remaining in the year
    days_in_year_remaining = day_zero_indexed % DAYS_IN_YEAR
    
    # Calculate month and day
    month = 1
    days_counted = 0
    for m in range(12):
        if days_counted + DAYS_IN_MONTH[m] > days_in_year_remaining:
            month = m + 1
            day = days_in_year_remaining - days_counted + 1
            break
        days_counted += DAYS_IN_MONTH[m]
    else:
        # Edge case: last day of year
        month = 12
        day = DAYS_IN_MONTH[11]
    
    return year, month, day


def format_ck3_date(year: int, month: int, day: int) -> str:
    """
    Format a date for CK3 (YYYY.M.D format, no leading zeros).
    
    Args:
        year: Year
        month: Month (1-12)
        day: Day (1-31)
    
    Returns:
        Formatted date string like "867.1.1" or "1066.9.15"
    """
    return f"{year}.{month}.{day}"


def build_character_map(dynasty: List[List[Person]]) -> Dict[int, Tuple[Person, str]]:
    """
    Build a map of person object id to (Person, character_id) for lookup.
    Character IDs are numbered sequentially across all generations.
    
    Args:
        dynasty: List of generations
    
    Returns:
        Dictionary mapping id(person) -> (person, character_id)
    """
    character_map = {}
    char_num = 1
    
    for generation in dynasty:
        for person in generation:
            character_map[id(person)] = (person, char_num)
            char_num += 1
    
    return character_map


def export_to_ck3(
    dynasty: List[List[Person]],
    filepath: str,
    dynasty_name: str,
    culture: str,
    religion: str,
    include_death_for_living: bool = False,
    end_date: int = None
) -> None:
    """
    Export a dynasty to a CK3 history file.
    
    Args:
        dynasty: List of generations, each containing Person objects
        filepath: Output file path for the CK3 history file
        dynasty_name: Dynasty/House name (used in character IDs and dynasty field)
        culture: Culture code (e.g., 'han', 'french', 'english')
        religion: Religion code (e.g., 'jingxue', 'catholic', 'daoxue')
        include_death_for_living: If True, add death date (end_date + 1 day) for living characters
        end_date: Simulation end date in absolute days (needed for living character deaths)
    """
    from config.culture_config import get_ck3_culture_code
    
    # Get the CK3 culture code (e.g., "chinese" -> "han")
    ck3_culture = get_ck3_culture_code(culture)
    
    # Format dynasty name for CK3: lowercase with "_dynasty" suffix
    ck3_dynasty_name = f"{dynasty_name.lower()}_dynasty"
    
    # Build character map - includes dynasty members AND their spouses
    character_map = {}
    people_seen = set()
    char_num = 1
    wife_num = 1
    
    # First pass: collect all dynasty members
    for generation in dynasty:
        for person in generation:
            people_seen.add(id(person))
            character_map[id(person)] = (person, char_num, None)  # (person, char_num, wife_num)
            char_num += 1
    
    # Second pass: collect spouses not already in dynasty (these are wives)
    for generation in dynasty:
        for person in generation:
            if person.spouse and id(person.spouse) not in people_seen:
                people_seen.add(id(person.spouse))
                character_map[id(person.spouse)] = (person.spouse, char_num, wife_num)  # Mark as wife
                char_num += 1
                wife_num += 1
    
    # Collect all people with their character IDs (lowercase)
    people_with_ids = []
    for person_id, (person, char_num, wife_num_val) in character_map.items():
        if wife_num_val is not None:
            # This is a wife - use special naming
            character_id = f"{dynasty_name.lower()}_wife_{wife_num_val}"
        else:
            # Regular dynasty member
            character_id = f"{dynasty_name.lower()}_character_{char_num}"
        people_with_ids.append((person, character_id, char_num))
    
    # Generate CK3 entries
    lines = []
    
    for person, character_id, char_num in people_with_ids:
        lines.append(f"{character_id} = {{")
        
        # Name (required)
        lines.append(f"\tname = \"{person.given_name}\"")
        
        # Female flag (optional, only if female)
        if person.female:
            lines.append(f"\tfemale = yes")
        
        # Dynasty (only if part of dynasty) - use lowercase dynasty name with _dynasty suffix
        if person.dynasty_name:
            lines.append(f"\tdynasty = {ck3_dynasty_name}")
        
        # Religion (required)
        lines.append(f"\treligion = {religion}")
        
        # Culture (required, use CK3 culture code)
        lines.append(f"\tculture = {ck3_culture}")
        
        # Father (optional)
        if person.father and id(person.father) in character_map:
            father_person, father_num, father_wife_num = character_map[id(person.father)]
            if father_wife_num is not None:
                father_id = f"{dynasty_name.lower()}_wife_{father_wife_num}"
            else:
                father_id = f"{dynasty_name.lower()}_character_{father_num}"
            lines.append(f"\tfather = {father_id}")
        
        # Mother (optional)
        if person.mother and id(person.mother) in character_map:
            mother_person, mother_num, mother_wife_num = character_map[id(person.mother)]
            if mother_wife_num is not None:
                mother_id = f"{dynasty_name.lower()}_wife_{mother_wife_num}"
            else:
                mother_id = f"{dynasty_name.lower()}_character_{mother_num}"
            lines.append(f"\tmother = {mother_id}")
        
        # Birth event (required)
        if person.date_of_birth:
            birth_year, birth_month, birth_day = convert_absolute_day_to_date(person.date_of_birth)
            birth_date = format_ck3_date(birth_year, birth_month, birth_day)
        else:
            # Fallback to year if no detailed date
            birth_date = format_ck3_date(person.birth_year, 1, 1)
        
        lines.append(f"\t{birth_date} = {{")
        lines.append(f"\t\tbirth = yes")
        
        # Add playable flag for males under 30 at end date
        if not person.female and end_date:
            age_at_end = convert_calendar_days_to_years(end_date) - person.birth_year
            if age_at_end < 30:
                lines.append(f"\t\teffect = {{ add_character_flag = do_not_generate_starting_family }}")
        
        lines.append(f"\t}}")
        
        # Marriage event (optional)
        if person.spouse and person.date_of_marriage and id(person.spouse) in character_map:
            spouse_person, spouse_num, spouse_wife_num = character_map[id(person.spouse)]
            if spouse_wife_num is not None:
                spouse_id = f"{dynasty_name.lower()}_wife_{spouse_wife_num}"
            else:
                spouse_id = f"{dynasty_name.lower()}_character_{spouse_num}"
            
            marriage_year, marriage_month, marriage_day = convert_absolute_day_to_date(person.date_of_marriage)
            marriage_date = format_ck3_date(marriage_year, marriage_month, marriage_day)
            
            lines.append(f"\t{marriage_date} = {{")
            lines.append(f"\t\tadd_spouse = {spouse_id}")
            lines.append(f"\t}}")
        
        # Death event (optional)
        # Check is_living_at_end instead of a date threshold
        if person.date_of_death and not person.is_living_at_end:
            # Character died during simulation
            death_year, death_month, death_day = convert_absolute_day_to_date(person.date_of_death)
            death_date = format_ck3_date(death_year, death_month, death_day)
            
            lines.append(f"\t{death_date} = {{")
            lines.append(f"\t\tdeath = yes")
            lines.append(f"\t}}")
        elif include_death_for_living and person.is_living_at_end and end_date:
            # Living character: add death at end_date + 1 day
            # Calculate the day after end_date
            death_day_absolute = end_date + 1
            death_year, death_month, death_day = convert_absolute_day_to_date(death_day_absolute)
            death_date = format_ck3_date(death_year, death_month, death_day)
            
            lines.append(f"\t{death_date} = {{")
            lines.append(f"\t\tdeath = yes")
            lines.append(f"\t}}")
        
        lines.append("}")
        lines.append("")  # Blank line between characters
    
    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
