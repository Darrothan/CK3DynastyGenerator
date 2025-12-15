"""
GEDCOM export functionality for dynasty generator.

Exports a generated dynasty to GEDCOM 5.5.1 format with all relevant person data.
"""

from datetime import date
from collections import defaultdict
from typing import List, Dict, Set
from models.person import Person


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
        source: Source identifier for the GEDCOM file
    
    Returns:
        Path to the created GEDCOM file
    """
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
        
        # NAME field (GEDCOM standard: given /surname/)
        given_name = person.given_name
        surname = person.dynasty_name or ""
        lines.append(f"1 NAME {given_name} /{surname}/")
        
        # SEX field
        sex = "F" if person.female else "M"
        lines.append(f"1 SEX {sex}")
        
        # BIRT field
        if person.birth_year is not None:
            lines.append("1 BIRT")
            lines.append(f"2 DATE ABT {person.birth_year}")
        
        # DEAT field (only if within end_year)
        if person.death_year is not None and (end_year is None or person.death_year <= end_year):
            lines.append("1 DEAT")
            lines.append(f"2 DATE ABT {person.death_year}")
        
        # MARR field
        if person.date_of_marriage is not None:
            # Convert absolute days to year
            from config.other_constants import DAYS_IN_YEAR
            marriage_year = (person.date_of_marriage - 1) // DAYS_IN_YEAR + 1
            lines.append("1 MARR")
            lines.append(f"2 DATE ABT {marriage_year}")
        
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
        
        # Add children
        for child in fam_children[fid]:
            output.append(f"1 CHIL {indi_ids[id(child)]}")
    
    # Trailer
    output.append("0 TRLR")
    
    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    return filepath
