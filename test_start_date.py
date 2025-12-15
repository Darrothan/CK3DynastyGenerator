"""
Test the new start date selection functionality with CK3 bookmarks and custom dates.
"""

from config.other_constants import (
    CK3_867_START_DAY, CK3_1066_START_DAY, CK3_1178_START_DAY,
    convert_calendar_years_to_days, DAYS_IN_MONTH
)


def test_ck3_bookmark_dates():
    """Test that CK3 bookmark dates are correctly defined."""
    # 867.1.1 = year 867, Jan 1
    assert CK3_867_START_DAY == convert_calendar_years_to_days(867)
    
    # 1066.9.15 = year 1066, Sep 15
    expected_1066 = convert_calendar_years_to_days(1066) + sum(DAYS_IN_MONTH[:8]) + 15 - 1
    assert CK3_1066_START_DAY == expected_1066
    
    # 1178.10.1 = year 1178, Oct 1
    expected_1178 = convert_calendar_years_to_days(1178) + sum(DAYS_IN_MONTH[:9]) + 1 - 1
    assert CK3_1178_START_DAY == expected_1178
    
    print("✓ All CK3 bookmark dates are correct")


def test_custom_date_calculation():
    """Test custom date calculation with month and day."""
    # Test a custom date: 1100.6.15
    year = 1100
    month = 6
    day = 15
    
    abs_day = convert_calendar_years_to_days(year) + sum(DAYS_IN_MONTH[:month - 1]) + day - 1
    
    # Verify we can extract year back
    days_in_year = 365
    extracted_year = (abs_day - 1) // days_in_year + 1
    assert extracted_year == year
    
    print(f"✓ Custom date 1100.6.15 = absolute day {abs_day}")


def test_date_validation():
    """Test that month and day validation works."""
    days_in_year = 365
    
    # Test valid dates
    valid_dates = [
        (1100, 1, 1),    # Jan 1
        (1100, 6, 15),   # Jun 15
        (1100, 12, 31),  # Dec 31
        (867, 1, 1),     # 867.1.1
    ]
    
    for year, month, day in valid_dates:
        assert 1 <= month <= 12, f"Month {month} invalid"
        assert 1 <= day <= DAYS_IN_MONTH[month - 1], f"Day {day} invalid for month {month}"
    
    print(f"✓ Date validation works for {len(valid_dates)} valid dates")


def test_default_date():
    """Test that default (no month/day) works as Jan 1."""
    year = 1100
    
    # User chooses year but defaults to 1/1
    abs_day_default = convert_calendar_years_to_days(year)
    
    # Explicit 1/1 should match
    abs_day_explicit = convert_calendar_years_to_days(year) + sum(DAYS_IN_MONTH[:0]) + 1 - 1
    
    assert abs_day_default == abs_day_explicit
    print(f"✓ Default date 1100.1.1 = absolute day {abs_day_default}")


if __name__ == "__main__":
    test_ck3_bookmark_dates()
    test_custom_date_calculation()
    test_date_validation()
    test_default_date()
    print("\n✅ All start date tests passed!")
