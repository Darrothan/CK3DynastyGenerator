#!/usr/bin/env python3
"""
DEMO: Start Date Selection Feature

This script demonstrates the new start date selection functionality
without requiring full user interaction.
"""

from config.other_constants import (
    CK3_867_START_DAY, CK3_1066_START_DAY, CK3_1178_START_DAY,
    convert_calendar_years_to_days, DAYS_IN_MONTH
)


def demo_start_date_feature():
    """Demonstrate the start date selection feature."""
    
    print("=" * 80)
    print("CK3 DYNASTY GENERATOR - START DATE FEATURE DEMO")
    print("=" * 80)
    
    print("\n--- CK3 Bookmark Dates ---\n")
    
    # Option 1: 867.1.1
    print("Option 1: 867.1.1 (CK3 Game Start)")
    print(f"  Absolute Day: {CK3_867_START_DAY}")
    print(f"  Format: Year 867, January 1st")
    
    # Option 2: 1066.9.15
    print("\nOption 2: 1066.9.15 (Norman Conquest)")
    print(f"  Absolute Day: {CK3_1066_START_DAY}")
    print(f"  Format: Year 1066, September 15th")
    
    # Option 3: 1178.10.1
    print("\nOption 3: 1178.10.1 (Crusades Era)")
    print(f"  Absolute Day: {CK3_1178_START_DAY}")
    print(f"  Format: Year 1178, October 1st")
    
    print("\n" + "=" * 80)
    print("--- Custom Date Examples ---\n")
    
    # Custom example 1: 1100.1.1 (default month/day)
    print("User Input: Year=1100, Month=(default 1), Day=(default 1)")
    custom_day_1 = convert_calendar_years_to_days(1100) + sum(DAYS_IN_MONTH[:0]) + 1 - 1
    print(f"  Date: 1100.1.1")
    print(f"  Absolute Day: {custom_day_1}\n")
    
    # Custom example 2: 1100.6.15
    print("User Input: Year=1100, Month=6, Day=15")
    custom_day_2 = convert_calendar_years_to_days(1100) + sum(DAYS_IN_MONTH[:5]) + 15 - 1
    print(f"  Date: 1100.6.15")
    print(f"  Absolute Day: {custom_day_2}\n")
    
    # Custom example 3: 900.12.31
    print("User Input: Year=900, Month=12, Day=31")
    custom_day_3 = convert_calendar_years_to_days(900) + sum(DAYS_IN_MONTH[:11]) + 31 - 1
    print(f"  Date: 900.12.31")
    print(f"  Absolute Day: {custom_day_3}\n")
    
    print("=" * 80)
    print("FEATURE BENEFITS:")
    print("=" * 80)
    print("""
✓ Supports exact CK3 bookmark start dates
  - Users can select 867.1.1, 1066.9.15, or 1178.10.1 from a menu
  - No manual calculation needed

✓ Custom date support
  - Users can enter any year + optional month/day
  - Defaults to 1/1 if month/day not specified
  - Validates month (1-12) and day (1-28/29/30/31)

✓ Proper date handling
  - Calculates absolute days (CK3 day count) from calendar dates
  - Accounts for different month lengths (28-31 days)
  - Compatible with existing generate_dynasty() function

✓ User-friendly interface
  - Clear menu with descriptions
  - Input validation with helpful error messages
  - Defaults make simple selection easy
    """)
    
    print("=" * 80)
    print("\nTo use this feature, run: python main.py")
    print("When prompted, choose option 1-4 for start date selection")
    print("=" * 80)


if __name__ == "__main__":
    demo_start_date_feature()
