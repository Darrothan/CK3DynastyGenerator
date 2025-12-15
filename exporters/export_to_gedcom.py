"""
GEDCOM export functionality for dynasty generator.

Exports a generated dynasty to GEDCOM 5.5.1 format with all relevant person data.
Includes enhanced fields:
- GIVN/SURN: Split given and surname fields
- _MARNM: Married name for spouses
- Detailed date information (DAY MON YEAR format)
- Age at death notes
- Full family relationships and marriage dates
"""

from datetime import date
from collections import defaultdict
from typing import List, Dict, Set, Optional
from models.person import Person
from config.other_constants import DAYS_IN_YEAR


def convert_absolute_day_to_date(absolute_day: int) -> tuple[int, int, int]:
    """Convert absolute day (CK3 format) to (year, month, day)."""
    from config.other_constants import DAYS_IN_MONTH
    
    year = (absolute_day - 1) // DAYS_IN_YEAR + 1
    day_of_year = (absolute_day - 1) % DAYS_IN_YEAR + 1
    
    month = 1
    for dim in DAYS_IN_MONTH:
        if day_of_year <= dim:
            break
        day_of_year -= dim
        month += 1
    
    return year, month, day_of_year


def format_gedcom_date(year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None) -> Optional[str]:
    """Format a date for GEDCOM output. Returns format like '11 NOV 1998' or 'ABT 1100'."""
    if year is None:
        return None
    
    # Format with approximate if we only have year
    if month is None or day is None:
        return f"ABT {year}"
    
    # Full date format: DAY MON YEAR
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month_name = months[month - 1] if 1 <= month <= 12 else months[0]
    return f"{day} {month_name} {year}"


def collect_people(dynasty: List[List[Person]]) -> List[Person]:
    """
    Flatten dynasty structure into a single list of all people.
    
    Args:
        dynasty: List of generations, each containing a list of persons
    
    Returns:
        Flattened list of all persons in the dynasty
    """
    people = []
    seen: Set[int] = set()
    
    for generation in dynasty:
        for person in generation:
            person_id = id(person)
            if person_id not in seen:
                seen.add(person_id)
                people.append(person)
            
            # Also add spouses (they may not be in the dynasty structure)
            if person.spouse:
                spouse_id = id(person.spouse)
                if spouse_id not in seen:
                    seen.add(spouse_id)
                    people.append(person.spouse)
    
    return people


def export_to_gedcom(
    dynasty: List[List[Person]],
    filepath: str,
    end_year: int = None,
    culture: str = "chinese",
    dynasty_name: str = None,
    source: str = "CK3 Dynasty Generator"
) -> str:
    """
    Export dynasty to GEDCOM 5.5.1 format file.
    
    GEDCOM standard includes the following person fields we support:
    - NAME: Person's name (given and surname)
    - SEX: Male/Female
    - BIRT: Birth date
    - DEAT: Death date
    - MARR: Marriage date
    - FAMS: Family where person is spouse
    - FAMC: Family where person is child
    
    Args:
        dynasty: Dynasty structure to export
        filepath: Path where GEDCOM file will be written
        end_year: If set, exclude deaths beyond this year
        culture: Culture name for naming conventions (e.g., 'chinese', 'english')
        dynasty_name: The dynasty surname to propagate to all members
        source: Source identifier for the GEDCOM file
    
    Returns:
        Path to the created GEDCOM file
    """
    from config.culture_config import get_culture_config
    
    culture_cfg = get_culture_config(culture)
    people = collect_people(dynasty)
    
    # Create ID mappings using object id for hashability
    person_to_index = {id(p): i for i, p in enumerate(people)}
    indi_ids = {id(p): f"@I{i+1}@" for i, p in enumerate(people)}
    
    # Create family IDs and relationships
    fam_ids = {}  # id(person) -> fid
    fam_children = defaultdict(list)  # fid -> list of Person objects
    fam_counter = 0
    
    for person in people:
        if not person.children:
            continue
        fam_counter += 1
        fid = f"@F{fam_counter}@"
        fam_ids[id(person)] = fid
        for child in person.children:
            fam_children[fid].append(child)
    
    # Build relationship maps
    child_famc_map: Dict[int, List[str]] = defaultdict(list)  # id(person) -> [fid]
    father_fams_map: Dict[int, List[str]] = defaultdict(list)  # id(person) -> [fid]
    mother_fams_map: Dict[int, List[str]] = defaultdict(list)  # id(person) -> [fid]
    
    for person_id, fid in fam_ids.items():
        father_fams_map[person_id].append(fid)
        for child in fam_children[fid]:
            child_famc_map[id(child)].append(fid)
            if child.spouse:
                mother_fams_map[id(child.spouse)].append(fid)
    
    # Generate INDI blocks
    indi_blocks: Dict[str, List[str]] = {}
    
    for person in people:
        pid = indi_ids[id(person)]
        
        lines = []
        lines.append(f"0 {pid} INDI")
        
        # Determine surname for this person based on culture conventions
        # Dynasty members (those with dynasty_name set) always use that surname
        if person.dynasty_name:
            surname = person.dynasty_name
        else:
            # Non-dynasty members (spouses from outside)
            # Handle based on culture naming conventions
            surname = ""
            
            # For patrilineal cultures: wives take husband's surname
            if culture_cfg.wives_take_husband_surname and person.female and person.spouse and person.spouse.dynasty_name:
                surname = person.spouse.dynasty_name
            # Otherwise, no surname (no maiden name data stored)
        
        # NAME field (GEDCOM standard: given /surname/)
        given_name = person.given_name
        lines.append(f"1 NAME {given_name} /{surname}/")
        
        # GIVN field (Given Name)
        lines.append(f"2 GIVN {given_name}")
        
        # SURN field (Surname)
        if surname:
            lines.append(f"2 SURN {surname}")
        
        # _MARNM field (Married Name) - for patrilineal cultures where wives took husband's name
        if culture_cfg.wives_take_husband_surname and person.female and person.spouse and person.spouse.dynasty_name and not person.dynasty_name:
            # Wife took husband's dynasty name but originally didn't have it
            lines.append(f"2 _MARNM {person.spouse.dynasty_name}")
        
        # SEX field
        sex = "F" if person.female else "M"
        lines.append(f"1 SEX {sex}")
        
        # BIRT field (Birth Date)
        if person.birth_year is not None:
            lines.append("1 BIRT")
            # Use detailed date if available, otherwise just year
            if person.date_of_birth is not None:
                year, month, day = convert_absolute_day_to_date(person.date_of_birth)
                formatted_date = format_gedcom_date(year, month, day)
            else:
                formatted_date = format_gedcom_date(person.birth_year)
            if formatted_date:
                lines.append(f"2 DATE {formatted_date}")
        
        # DEAT field (Death Date - only if within end_year)
        if person.death_year is not None and (end_year is None or person.death_year <= end_year):
            lines.append("1 DEAT")
            # Use detailed date if available
            if person.date_of_death is not None:
                year, month, day = convert_absolute_day_to_date(person.date_of_death)
                formatted_date = format_gedcom_date(year, month, day)
            else:
                formatted_date = format_gedcom_date(person.death_year)
            if formatted_date:
                lines.append(f"2 DATE {formatted_date}")
        
        # NOTE field - Age at death
        if person.birth_year is not None and person.death_year is not None:
            age_at_death = person.death_year - person.birth_year
            lines.append(f"1 NOTE Age at death: {age_at_death} years")
        
        # MARR field (Marriage Date)
        if person.date_of_marriage is not None:
            year, month, day = convert_absolute_day_to_date(person.date_of_marriage)
            formatted_date = format_gedcom_date(year, month, day)
            if formatted_date:
                lines.append("1 MARR")
                lines.append(f"2 DATE {formatted_date}")
        
        # FAMS field (person as spouse/parent)
        for fid in father_fams_map.get(id(person), []):
            lines.append(f"1 FAMS {fid}")
        for fid in mother_fams_map.get(id(person), []):
            lines.append(f"1 FAMS {fid}")
        
        # FAMC field (person as child)
        for fid in child_famc_map.get(id(person), []):
            lines.append(f"1 FAMC {fid}")
        
        indi_blocks[pid] = lines
    
    # Build GEDCOM output
    today = date.today()
    output = [
        "0 HEAD",
        f"1 SOUR {source}",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
        f"1 DATE {today.strftime('%d %b %Y')}",
        "1 SUBM @SUB1@",
        "0 @SUB1@ SUBM",
        "1 NAME Dynasty Generator",
    ]
    
    # Add individuals in order
    for pid in sorted(indi_blocks, key=lambda s: int(s.strip("@I@"))):
        output.extend(indi_blocks[pid])
    
    # Add families
    for person_id, fid in fam_ids.items():
        # Find the person object from indi_ids
        father = next(p for p in people if id(p) == person_id)
        
        output.append(f"0 {fid} FAM")
        output.append(f"1 HUSB {indi_ids[id(father)]}")
        
        # Add spouse if exists
        if father.spouse:
            output.append(f"1 WIFE {indi_ids[id(father.spouse)]}")
        
        # Add marriage date at family level if available
        if father.date_of_marriage is not None:
            year, month, day = convert_absolute_day_to_date(father.date_of_marriage)
            formatted_date = format_gedcom_date(year, month, day)
            if formatted_date:
                output.append("1 MARR")
                output.append(f"2 DATE {formatted_date}")
        
        # Add children
        for child in fam_children[fid]:
            output.append(f"1 CHIL {indi_ids[id(child)]}")
    
    # Trailer
    output.append("0 TRLR")
    
    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    return filepath
