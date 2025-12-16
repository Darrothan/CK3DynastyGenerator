"""
Dynasty metrics and statistics calculation.

Provides functions to calculate comprehensive statistics about a generated dynasty,
including generational breakdowns, age gaps, and character counts.
"""

from typing import List
from models.person import Person
from config.other_constants import DAYS_IN_YEAR
from services.utils import convert_calendar_days_to_years


def has_living_descendant(person: Person) -> bool:
    """
    Check if a person has at least one living descendant (child) at the end of the simulation.
    This does NOT count the person themselves - only their actual descendants.
    
    Args:
        person: The person to check
    
    Returns:
        True if the person has at least one living descendant, False otherwise
    """
    # Check if any child is alive
    for child in person.children:
        if child.is_living_at_end:
            return True
        # Check if this child has living descendants
        if has_living_descendant(child):
            return True
    
    return False


def calculate_dynasty_stats(dynasty: List[List[Person]], end_date: int) -> dict:
    """
    Calculate comprehensive statistics from the dynasty structure.
    
    Args:
        dynasty: List of generations, each containing a list of persons
        end_date: Simulation end date (in absolute days) used to determine character ages
    
    Returns:
        Dictionary containing overall and generation-level statistics
    """
    # Find founder (first person in first non-empty generation)
    founder_name = "Unknown"
    for generation in dynasty:
        if generation:
            founder_name = generation[0].name
            break
    
    stats = {
        "total_generations": len(dynasty),
        "total_people": sum(len(gen) for gen in dynasty),
        "founder_name": founder_name,
        "young_males_count": 0,
        "max_age_gap_overall": 0,
        "total_alive_at_end": 0,
        "generations": [],
    }
    
    total_births = 0
    total_deaths = 0
    
    # Track young males (< 30 years old at end_date) across all generations
    end_year = convert_calendar_days_to_years(end_date)
    
    for gen_idx, generation in enumerate(dynasty):
        if not generation:
            continue
        
        gen_stats = {
            "generation": gen_idx,
            "count": len(generation),
            "males": sum(1 for p in generation if not p.female),
            "females": sum(1 for p in generation if p.female),
            "avg_lifespan": 0,
            "avg_birth_year": 0,
            "avg_death_year": 0,
            "skip_generation_count": sum(1 for p in generation if p.skip_generation),
            "alive_at_end": sum(1 for p in generation if p.is_living_at_end),
        }
        
        if generation:
            gen_stats["avg_lifespan"] = sum(p.death_year - p.birth_year for p in generation) / len(generation)
            gen_stats["avg_birth_year"] = sum(p.birth_year for p in generation) / len(generation)
            gen_stats["avg_death_year"] = sum(p.death_year for p in generation) / len(generation)
        
        # Count children per person
        total_children = sum(len(p.children) for p in generation)
        gen_stats["total_children"] = total_children
        gen_stats["avg_children"] = total_children / len(generation) if generation else 0
        
        # Calculate largest age gap within this generation (span from oldest to youngest)
        if len(generation) > 1:
            birth_years = sorted([p.birth_year for p in generation])
            max_gap = birth_years[-1] - birth_years[0]  # Oldest to youngest
            gen_stats["max_age_gap"] = max_gap
            stats["max_age_gap_overall"] = max(stats["max_age_gap_overall"], max_gap)
        else:
            gen_stats["max_age_gap"] = 0
        
        # Count surviving branches (people with at least one living descendant)
        surviving_branches = sum(1 for p in generation if has_living_descendant(p))
        gen_stats["surviving_branches"] = surviving_branches
        
        # Count young males in this generation
        young_males_in_gen = sum(
            1 for p in generation
            if not p.female and (end_year - p.birth_year) < 30
        )
        gen_stats["young_males_count"] = young_males_in_gen
        stats["young_males_count"] += young_males_in_gen
        
        # Count total alive at end
        stats["total_alive_at_end"] += gen_stats["alive_at_end"]
        
        stats["generations"].append(gen_stats)
        total_births += len(generation)
        total_deaths += len([p for p in generation if p.death_year < 10000])
    
    stats["total_births"] = total_births
    stats["total_deaths"] = total_deaths
    
    return stats


def print_dynasty_stats(stats: dict):
    """Print formatted dynasty statistics with new metrics."""
    print("\n" + "=" * 80)
    print("DYNASTY STATISTICS")
    print("=" * 80)
    
    print(f"\nFounder: {stats['founder_name']}")
    print(f"Total Generations: {stats['total_generations']}")
    print(f"Total Dynasty Members: {stats['total_people']}")
    print(f"Still Alive at End Date: {stats['total_alive_at_end']}")
    print(f"Total Births: {stats['total_births']}")
    print(f"Total Deaths: {stats['total_deaths']}")
    print(f"Young Males (< age 30): {stats['young_males_count']}")
    print(f"Largest Age Gap in Generation: {stats['max_age_gap_overall']} years")
    
    print("\n" + "-" * 80)
    print(f"{'Gen':<5} {'Size':<8} {'Alive':<8} {'Males':<8} {'Females':<10} {'Branches':<10} {'Avg Life':<12} {'Age Gap':<10}")
    print("-" * 80)
    
    for gen_info in stats["generations"]:
        gen = gen_info["generation"]
        size = gen_info["count"]
        alive = gen_info["alive_at_end"]
        males = gen_info["males"]
        females = gen_info["females"]
        branches = gen_info["surviving_branches"]
        avg_life = gen_info["avg_lifespan"]
        age_gap = gen_info["max_age_gap"]
        
        print(f"{gen:<5} {size:<8} {alive:<8} {males:<8} {females:<10} {branches:<10} {avg_life:<12.1f} {age_gap:<10}")
    
    print("=" * 80)


def print_dynasty_tree(dynasty: List[List[Person]], depth: int = 2):
    """Print a simplified dynasty tree structure."""
    print("\n" + "=" * 80)
    print("DYNASTY TREE (limited depth for readability)")
    print("=" * 80)
    
    def print_person(person: Person, indent: int, max_depth: int):
        if indent > max_depth:
            return
        
        prefix = "  " * indent + ("├─ " if indent > 0 else "")
        living = "[D]" if person.death_year < 10000 else "[L]"
        gender = "[M]" if not person.female else "[F]"
        
        print(f"{prefix}{person.name} {gender} ({person.birth_year}-{person.death_year}) {living}")
        
        for child in person.children[:3]:  # Limit to 3 children for readability
            print_person(child, indent + 1, max_depth)
        
        if len(person.children) > 3:
            print(f"{'  ' * (indent + 1)}... and {len(person.children) - 3} more children")
    
    # Find the founder (first person in first non-empty generation)
    founder = None
    for generation in dynasty:
        if generation:
            founder = generation[0]
            break
    
    if founder:
        print_person(founder, 0, depth)
