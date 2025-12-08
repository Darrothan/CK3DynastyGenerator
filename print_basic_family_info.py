from collections import deque, defaultdict

def print_basic_family_info(person_obj):
    """
    Prints per-generation:
      - total, living, dead
      - largest and smallest age gaps within the generation
        (computed from birth_year differences among individuals in the same gen)

    Also prints overall totals.
    """
    q = deque([(person_obj, 0)])
    gen_total  = defaultdict(int)
    gen_living = defaultdict(int)
    gen_dead   = defaultdict(int)
    gen_birth_years = defaultdict(list)

    visited = set()
    while q:
        p, g = q.popleft()
        if id(p) in visited:
            continue
        visited.add(id(p))

        gen_total[g] += 1
        if getattr(p, "is_living", False):
            gen_living[g] += 1
        else:
            gen_dead[g] += 1

        if hasattr(p, "birth_year") and p.birth_year is not None:
            gen_birth_years[g].append(p.birth_year)

        for child in getattr(p, "children", []):
            q.append((child, g + 1))

    # ---- Per-generation summary ----
    for g in sorted(gen_total.keys()):
        total  = gen_total[g]
        living = gen_living[g]
        dead   = gen_dead[g]
        line = f"Generation {g}: {total} individuals (living: {living}, dead: {dead})"

        years = gen_birth_years.get(g, [])
        if len(years) >= 2:
            years_sorted = sorted(years)
            max_gap = years_sorted[-1] - years_sorted[0]  # oldest vs youngest span in that gen
            # smallest gap = closest birth years among any two in the gen
            min_pair_gap = min(
                years_sorted[i+1] - years_sorted[i]
                for i in range(len(years_sorted) - 1)
            )
            line += f" | age gaps → largest: {max_gap} yrs, smallest: {min_pair_gap} yrs"
        elif len(years) == 1:
            line += " | age gaps → (only one person; no gaps)"
        else:
            line += " | age gaps → (no birth years recorded)"

        print(line)

    # ---- Overall totals ----
    overall_total  = sum(gen_total.values())
    overall_living = sum(gen_living.values())
    overall_dead   = sum(gen_dead.values())
    print(f"\nOverall: {overall_total} individuals (living: {overall_living}, dead: {overall_dead})")
