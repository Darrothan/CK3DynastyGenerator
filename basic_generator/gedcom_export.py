from datetime import date
from collections import defaultdict

def collect_people(root):
    people, stack, seen = [], [root], set()
    while stack:
        p = stack.pop()
        if id(p) in seen:
            continue
        seen.add(id(p))
        people.append(p)
        stack.extend(reversed(p.children))
    return people

def name_parts(person_name, root_surname=None, keep_suffix=True):
    if keep_suffix:
        given = person_name.replace("_", " ").strip() or "Unknown"
    else:
        given = (person_name.split("_", 1)[0] or "Unknown")
    surname = (root_surname or given) or "Unknown"
    return given, surname

def export_to_gedcom(root, filepath, root_surname=None, source="CK3 Family Generator", end_year=None):
    """Export family tree to GEDCOM. If end_year is set, omit death beyond it."""
    people = collect_people(root)

    indi_ids = {p: f"@I{i+1}@" for i, p in enumerate(people)}

    fam_ids = {}
    fam_children = defaultdict(list)
    fam_counter = 0
    for father in people:
        if not father.children:
            continue
        fam_counter += 1
        fid = f"@F{fam_counter}@"
        fam_ids[father] = fid
        for child in father.children:
            fam_children[fid].append(child)

    # Relationships
    child_famc_map = defaultdict(list)
    father_fams_map = defaultdict(list)
    for father, fid in fam_ids.items():
        father_fams_map[father].append(fid)
        for child in fam_children[fid]:
            child_famc_map[child].append(fid)

    indi_blocks = {}

    for p in people:
        pid = indi_ids[p]
        given, surname = name_parts(p.name, root_surname=root_surname, keep_suffix=True)

        lines = []
        lines.append(f"0 {pid} INDI")
        lines.append(f"1 NAME {given} /{surname}/")
        lines.append("1 SEX M")
        if p.birth_year is not None:
            lines.append("1 BIRT")
            lines.append(f"2 DATE ABT {p.birth_year}")

        # ✅ Only include death date if it's within the simulation end year
        if p.death_year is not None and (end_year is None or p.death_year <= end_year):
            lines.append("1 DEAT")
            lines.append(f"2 DATE ABT {p.death_year}")

        for fid in father_fams_map.get(p, []):
            lines.append(f"1 FAMS {fid}")
        for fid in child_famc_map.get(p, []):
            lines.append(f"1 FAMC {fid}")

        indi_blocks[pid] = lines

    today = date.today()
    out = [
        "0 HEAD",
        f"1 SOUR {source}",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
        f"1 DATE {today.strftime('%d %b %Y')}",
        "1 SUBM @SUB1@",
        "0 @SUB1@ SUBM",
        "1 NAME Generator",
    ]

    for pid in sorted(indi_blocks, key=lambda s: int(s.strip("@I@"))):
        out += indi_blocks[pid]

    for father, fid in fam_ids.items():
        out.append(f"0 {fid} FAM")
        out.append(f"1 HUSB {indi_ids[father]}")
        for child in fam_children[fid]:
            out.append(f"1 CHIL {indi_ids[child]}")

    out.append("0 TRLR")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    return filepath
