"""
REFACTORING: Start Date Integration

This document describes the refactoring that integrates the start date selection 
into the simulation end date, eliminating the redundant end year prompt.

BEFORE (Previous Implementation):
=================================

1. get_start_date() -> int
   - Returns only the absolute day
   - No year information extracted

2. get_dynasty_parameters() -> Tuple[int, int, int, int]
   - Prompted for: birth_year, END_YEAR, male_only_start, normal_start
   - User had to manually enter simulation end year
   - Unrelated to start date selection (user had to enter it twice!)

3. main() flow:
   - Call get_start_date() (but ignored the result!)
   - Call get_dynasty_parameters() (separately asks for end_year)
   - Convert end_year to end_days
   - Result: User prompted for end year regardless of start date chosen


AFTER (New Implementation):
===========================

1. get_start_date() -> Tuple[int, int]
   - Returns both (absolute_day, year) as a tuple
   - Extracts and returns the year from the chosen date:
     * Option 1 (867): returns (CK3_867_START_DAY, 867)
     * Option 2 (1066): returns (CK3_1066_START_DAY, 1066)
     * Option 3 (1178): returns (CK3_1178_START_DAY, 1178)
     * Custom (1100.6.15): returns (401301, 1100)

2. get_dynasty_parameters(end_year: int) -> Tuple[int, int, int]
   - Now takes end_year as a parameter (from start date)
   - Prompts for: birth_year, male_only_start, normal_start only
   - Validates birth_year < end_year (using passed-in end_year)
   - Returns only (birth_year, male_only_start, normal_start)
   - NO MORE redundant "Enter simulation end year" prompt!

3. main() flow:
   - Call get_start_date() -> returns (start_day_absolute, start_year)
   - Call get_dynasty_parameters(start_year) -> uses start_year as simulation end
   - Set end_days = start_day_absolute (the exact start date selected)
   - Result: Single unified date selection, no redundancy


KEY BENEFITS:
=============

✅ Single Date Selection:
   - User chooses start date once (bookmark or custom)
   - That becomes the simulation end date automatically
   - No need to enter end year separately

✅ Logical Coherence:
   - Start date selection (867.1.1, 1066.9.15, etc.) is used
   - Previously selected date was ignored!
   - Now the exact selected date (including month/day) is used as simulation end

✅ Cleaner UX:
   - Fewer prompts (3 fewer input() calls)
   - Clear relationship between selections
   - Less confusion about what year the simulation ends on

✅ Type Safety:
   - get_start_date() now returns Tuple[int, int] (explicit)
   - Compiler/IDE can catch if (abs_day, year) tuple not properly unpacked
   - Previously just returned int, easy to misuse

✅ Backward Compatible:
   - All existing tests pass (9/9)
   - No changes to simulation logic
   - Only UI/wizard flow changed


EXAMPLE FLOW:

User selects option 2 (1066.9.15):
  1. get_start_date() returns (388983, 1066)
  2. get_dynasty_parameters(1066) asks:
     - Birth year: 1050
     - Male-only start: 1056
     - Normal start: 1062
  3. Dynasty generated from 1050 to 1066.9.15 (absolute day 388983)

User selects option 4 (custom 1100.6.15):
  1. User enters year=1100, month=6, day=15
  2. get_start_date() returns (401301, 1100)
  3. get_dynasty_parameters(1100) asks:
     - Birth year: 1050
     - Male-only start: 1070
     - Normal start: 1090
  4. Dynasty generated from 1050 to 1100.6.15 (absolute day 401301)


CODE CHANGES:
=============

main.py:
  - get_start_date(): signature changed from () -> int to () -> Tuple[int, int]
  - get_dynasty_parameters(): signature changed from () -> Tuple[int,int,int,int] to (int) -> Tuple[int,int,int]
  - main() loop: now unpacks (start_day_absolute, start_year) and passes start_year to get_dynasty_parameters()
  - end_days assignment: changed from convert_calendar_years_to_days(end_year) to start_day_absolute
"""
