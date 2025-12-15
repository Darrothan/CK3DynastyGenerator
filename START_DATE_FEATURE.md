"""
SUMMARY: Start Date Selection Enhancement

This document describes the new start date selection functionality added to main.py
to support CK3 bookmark dates and custom month/day selection.

PROBLEM:
- Previously, users could only choose start and end years (1/1 default)
- CK3 bookmarks begin at specific dates like 9/15 or 10/1, not always 1/1
- Users had no way to specify exact CK3 bookmark start dates

SOLUTION:
Added get_start_date() function that offers two options:

1. CK3 BOOKMARK DATES (pre-configured):
   - Option 1: 867.1.1   (CK3 game start)
   - Option 2: 1066.9.15 (Norman Conquest)
   - Option 3: 1178.10.1 (Crusades era)

2. CUSTOM DATE (year + optional month/day):
   - Option 4: Manual entry
   - User enters: Year (required), Month (1-12, default 1), Day (1-31, default 1)
   - Validation ensures month/day are valid for the selected month
   - Returns absolute day count for use in generate_dynasty()

IMPLEMENTATION DETAILS:

File: main.py
Function: get_start_date() -> int
  - Imports CK3 bookmark constants from config/other_constants.py
  - Presents 4 menu options to user
  - For bookmarks (1-3): Returns pre-calculated absolute day
  - For custom (4): 
    * Prompts for year, month (with default 1), day (with default 1)
    * Validates month in range [1,12]
    * Validates day in range [1, days_in_month[month-1]]
    * Calculates absolute day using formula:
      abs_day = convert_calendar_years_to_days(year) + sum(DAYS_IN_MONTH[:month-1]) + day - 1
    * Repeats on validation error

Updated main():
  - Now calls get_start_date() after get_dynasty_name()
  - Stores result in start_day_absolute (not currently used, reserved for future)
  - Continues to accept birth_year separately (patriarch birth year)
  - All other parameters (end_year, transition years) handled as before

BACKWARD COMPATIBILITY:
✓ All existing tests pass (5/5)
✓ get_dynasty_parameters() unchanged (still accepts birth year, end year, transitions)
✓ main() still works exactly as before for dynasty generation
✓ start_day_absolute is captured but not used yet (can be integrated later)

EXAMPLES:

User chooses option 1 (867.1.1):
  - Returns CK3_867_START_DAY (absolute day 316091)

User chooses option 2 (1066.9.15):
  - Returns CK3_1066_START_DAY (absolute day 388983)

User chooses option 4 and enters:
  - Year: 1100
  - Month: (press enter for default 1)
  - Day: (press enter for default 1)
  - Returns absolute day 401136 (equivalent to 1100.1.1)

User chooses option 4 and enters:
  - Year: 1100
  - Month: 6
  - Day: 15
  - Returns absolute day 401301 (equivalent to 1100.6.15)

TESTING:
Created test_start_date.py with tests for:
  ✓ CK3 bookmark dates are correct
  ✓ Custom date calculations work
  ✓ Date validation (month 1-12, days per month)
  ✓ Default date behavior (1/1 when not specified)

All tests pass successfully.

FUTURE INTEGRATION:
The start_day_absolute could be used to:
- Adjust founder birth_date to match exact CK3 bookmark start
- Currently founder.date_of_birth is randomized during generation
- Could constrain patriarch to be born on the chosen start date
- Would require changes to generate_dynasty() and factory.create_male()
"""
