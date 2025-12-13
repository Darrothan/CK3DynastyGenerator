from __future__ import annotations
from typing import List
import random

from config.other_constants import CHILD_BY_MOTHER_AGE_PD, MOTHER_FERTILITY_WINDOW, MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS, DAYS_IN_YEAR
from services.utils import convert_years_to_days_duration, convert_calendar_years_to_days

"""
Takes in start and stop ages of the mother and a k number of children to generate and returns a sorted list of absolute birth days for the children.
This mirrors draw_children_birth_years_simple: returns absolute days with proper sibling gap enforcement.
"""
def draw_children_birth_years_exact_k(
    *,
    rng: random.Random,
    k: int,
    start_age: int,
    stop_age: int,
    mother_birth_year: int,
) -> List[int]:
    """
    Draw exactly k child birth ages within [start_age, stop_age], enforcing a minimum
    gap of MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS between sibling births.

    Sampling is exact from the conditional distribution:
      P(S) ∝ ∏_{age in S} CHILD_BY_MOTHER_AGE_PD[age]
    over all valid sets S of size k satisfying the gap constraint.
    """
    if k < 0:
        raise ValueError("k must be >= 0")

    # Build ordered age list and weights for the allowed window.
    ages = [a for a in range(start_age, stop_age + 1) if a in CHILD_BY_MOTHER_AGE_PD and CHILD_BY_MOTHER_AGE_PD[a] > 0.0]
    n = len(ages)

    if k == 0:
        return []

    if n == 0:
        raise ValueError("No ages available in the given window with positive probability.")

    w = [CHILD_BY_MOTHER_AGE_PD[a] for a in ages]

    # Precompute "next index" after taking age i (enforces the gap).
    next_idx = [0] * n
    for i, a in enumerate(ages):
        cutoff = a + MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS
        j = i + 1
        while j < n and ages[j] < cutoff:
            j += 1
        next_idx[i] = j

    # DP[i][t] = total weight of choosing t children from suffix starting at i.
    # Recurrence:
    #   DP[i][t] = DP[i+1][t] + w[i] * DP[next_idx[i]][t-1]
    DP = [[0.0] * (k + 1) for _ in range(n + 1)]
    DP[n][0] = 1.0
    for i in range(n - 1, -1, -1):
        DP[i][0] = 1.0
        for t in range(1, k + 1):
            skip = DP[i + 1][t]
            take = w[i] * DP[next_idx[i]][t - 1]
            DP[i][t] = skip + take

    total = DP[0][k]
    if total == 0.0:
        raise ValueError(
            f"Impossible to place {k} children in [{start_age}, {stop_age}] "
            f"with MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS={MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS}."
        )

    # Sample using the DP as exact choice probabilities.
    chosen: List[int] = []
    i, t = 0, k
    while t > 0 and i < n:
        skip = DP[i + 1][t]
        take = w[i] * DP[next_idx[i]][t - 1]
        denom = skip + take

        # denom should be > 0 here, but guard anyway.
        if denom <= 0.0:
            break

        if rng.random() < (take / denom):
            chosen.append(ages[i])
            i = next_idx[i]
            t -= 1
        else:
            i += 1

    # At this point, we should have exactly k.
    if len(chosen) != k:
        # This should be extremely rare unless floating-point underflow occurs.
        raise RuntimeError(f"Sampling failed: expected {k} children, got {len(chosen)}")

    # Convert ages to actual birth years and then to absolute days with gap enforcement
    birth_years = [mother_birth_year + age for age in sorted(chosen)]
    return generate_birth_days_from_birth_years(birth_years, rng)

"""
Takes in start and stop ages of the mother and a child_multiplier (the approximat number of children to generate) and returns a sortd list of birth days (ages) for the children.
"""
def draw_children_birth_years_simple(
    *, 
    rng: random.Random, 
    child_multiplier: float, 
    start_age: int = MOTHER_FERTILITY_WINDOW[0], 
    stop_age: int = MOTHER_FERTILITY_WINDOW[1]
) -> List[int]:
    """
    Copy, clamp (between start and stop age), and renormalize birth_year_pd
    Iterate over each year and determine whether or not a child is born that year based on probability * child_multiplier
    If a child is born, add that year to the list of birth years
    Then remove that year and the next year from the pd
    Do this until there are no more years left
    """

    birth_year_pd = {age: prob for age, prob in CHILD_BY_MOTHER_AGE_PD.items() if start_age <= age <= stop_age}
    # Normalize
    total_prob = sum(birth_year_pd.values())
    birth_year_pd = {age: prob / total_prob for age, prob in birth_year_pd.items()}

    birth_years: List[int] = []
    available_ages = set(birth_year_pd.keys())

    while available_ages:
        ages = sorted(available_ages)
        probabilities = [birth_year_pd[age] for age in ages]
        chosen_age = rng.choices(ages, weights=probabilities, k=1)[0]

        p_child = min(1.0, birth_year_pd[chosen_age] * child_multiplier)
        if rng.random() < p_child:
            birth_years.append(chosen_age)
            # Enforce minimum gap between siblings
            for age_to_remove in range(chosen_age, chosen_age + MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS):
                available_ages.discard(age_to_remove)
        else:
            available_ages.remove(chosen_age)

    return generate_birth_days_from_birth_years(sorted(birth_years), rng)

"""
Takes in a list of birth years and generates a list of absolute birth days such that no two birth days are less than MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS apart.
"""
def generate_birth_days_from_birth_years(birth_years: List[int], rng: random.Random) -> List[int]:
    birth_years = sorted(birth_years)
    min_gap_days = convert_years_to_days_duration(MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS)
    """
    Generate birth days, making sure they are at least min_gap_days apart
    Iterate over all birth years and randomly assign a day within that year (birth_day_within_year)
    Compare with the previous convert_years_to_days_duration + birth_day_within_year to ensure the gap is maintained
    If not, bubble the currently assigned birth_day_within_year backwards (i.e. swap the two values) in the birth_days_within_year list until either:
    1) the previous birth_year is no longer <= MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS away (it should actually never be LESS -- only equal at minimum)
    2) the current birth_day_within_year >= previous birth_day_within_year
    3) we reach the start of the list
    This ensures that we maintain the minimum gap while still randomizing the birth days within each year
    Finally, return the list of convert_years_to_days_duration + birth_day_within_year values
    """
    
    birth_years = sorted(birth_years)
    n = len(birth_years)

    # 1) assign random day within year
    birth_days_within_year = [rng.randint(1, DAYS_IN_YEAR) for _ in range(n)]

    # 2) find clusters where consecutive years differ by exactly MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS
    clusters: List[tuple[int, int]] = []
    cluster_start: int | None = None

    for i in range(1, n):
        if birth_years[i] - birth_years[i - 1] == MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS:
            if cluster_start is None:
                cluster_start = i - 1  # start cluster at previous index
            # else: we are already in a cluster, keep extending
        else:
            if cluster_start is not None:
                clusters.append((cluster_start, i - 1))
                cluster_start = None

    # close last cluster if it reaches the end
    if cluster_start is not None:
        clusters.append((cluster_start, n - 1))

    # 3) sort days within each cluster, preserving values outside clusters
    for start, end in clusters:
        segment = birth_days_within_year[start : end + 1]
        segment.sort()
        birth_days_within_year[start : end + 1] = segment

    # 4) convert to absolute days
    birth_days: List[int] = []
    for year, day_within_year in zip(birth_years, birth_days_within_year):
        absolute_day = convert_calendar_years_to_days(year) + day_within_year - 1
        birth_days.append(absolute_day)

    return sorted(birth_days)


def calculate_fertility_window(father: 'Person', mother: 'Person', start_age: int, max_age: int) -> tuple[int, int]:
    """
    Calculate the effective fertility window for a mother, accounting for:
    - Maximum fertility age
    - Mother's lifespan
    - Father's lifespan (can't have children after father dies)
    
    Returns (start_age, stop_age) tuple.
    """
    mother_death_age = mother.death_year - mother.birth_year
    father_death_age = father.death_year - mother.birth_year  # father's death in mother's-age years
    
    stop_age_eff = min(max_age, mother_death_age, father_death_age)
    
    return (start_age, stop_age_eff)


def max_children_with_gap(start_age: int, stop_age: int, min_gap_years: int) -> int:
    """
    Calculate maximum number of children that can fit in an age range
    given a minimum gap between siblings.
    """
    if stop_age < start_age:
        return 0
    span = stop_age - start_age
    return 1 + (span // min_gap_years)


def apply_exposure_scaling(rng: random.Random, baseline_k: int, start_age: int, stop_age: int, 
                           full_window_start: int, full_window_end: int) -> int:
    """
    Apply exposure scaling: reduce the number of children proportionally
    if the effective fertility window is smaller than the full window.
    Uses binomial thinning.
    """
    full_years = (full_window_end - full_window_start + 1)
    eff_years = (stop_age - start_age + 1)
    exposure_ratio = eff_years / full_years
    
    # Clamp ratio to [0, 1]
    r = max(0.0, min(1.0, exposure_ratio))
    # Binomial thinning: each potential child survives with probability r
    return sum(1 for _ in range(baseline_k) if rng.random() < r)


def draw_children_with_exposure(
    *,
    rng: random.Random,
    father: 'Person',
    mother: 'Person',
    end_date: int,
    baseline_k: int,
    min_gap_years: int = MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS,
    max_fertility_age: int = MOTHER_FERTILITY_WINDOW[1],
) -> List[int]:
    """
    Draw absolute birth days for children, accounting for:
    - Exposure scaling (reduced fertility if window is constrained)
    - Gap constraint between siblings
    - End date (no children born after simulation ends)
    
    Returns list of absolute birth days.
    """
    start_age = MOTHER_FERTILITY_WINDOW[0]
    start_age_eff, stop_age_eff = calculate_fertility_window(father, mother, start_age, max_fertility_age)
    
    # No exposure => no children
    if stop_age_eff < start_age_eff or baseline_k <= 0:
        return []
    
    # Apply exposure scaling
    k_realized = apply_exposure_scaling(
        rng, baseline_k, start_age_eff, stop_age_eff,
        start_age, max_fertility_age
    )
    
    # Cap by gap constraint feasibility
    k_max = max_children_with_gap(start_age_eff, stop_age_eff, min_gap_years)
    k_realized = min(k_realized, k_max)
    
    if k_realized <= 0:
        return []
    
    # Get birth days with gap enforcement
    return draw_children_birth_years_exact_k(
        rng=rng,
        k=k_realized,
        start_age=start_age_eff,
        stop_age=stop_age_eff,
        mother_birth_year=mother.birth_year,
    )