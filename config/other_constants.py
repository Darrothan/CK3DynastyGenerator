"""Project constants and simple calendar helpers.

Keep small calendar helpers here to avoid circular imports with
`services.utils` which also needs constants from this module.
"""

# simple helper (kept local to avoid circular imports)
def convert_calendar_years_to_days(year: int) -> int:
    return DAYS_IN_YEAR * (year - 1) + 1

# This is based off 1925 data so it's not super accurate for medieval times
# MOTHER_FERTILITY_WINDOW = (16, 45)
# CHILD_BY_MOTHER_AGE_PD = {
#     16: 0.0064, 17: 0.0191, 18: 0.0383, 19: 0.0638,
#     20: 0.0893, 21: 0.1084, 22: 0.1212, 23: 0.1148,
#     24: 0.1021, 25: 0.0829, 26: 0.0638, 27: 0.0510,
#     28: 0.0383, 29: 0.0287, 30: 0.0223, 31: 0.0159,
#     32: 0.0115, 33: 0.0077, 34: 0.0051, 35: 0.0032,
#     36: 0.0019, 37: 0.0013, 38: 0.0010, 39: 0.0006,
#     40: 0.0005, 41: 0.0004, 42: 0.0003, 43: 0.0001,
#     44: 0.00005, 45: 0.00001,
# }
# This is a more accurate distribution for medieval times, but may not work with CK3's 16+ starting age for marriage
MOTHER_FERTILITY_WINDOW = (14, 39)
CHILD_BY_MOTHER_AGE_PD = {
    14: 0.010, 15: 0.025, 16: 0.055, 17: 0.090,
    18: 0.125, 19: 0.145, 20: 0.140, 21: 0.125,
    22: 0.100, 23: 0.075, 24: 0.050, 25: 0.030,
    26: 0.020, 27: 0.015, 28: 0.010, 29: 0.007,
    30: 0.005, 31: 0.004, 32: 0.003, 33: 0.002,
    34: 0.0015, 35: 0.001, 36: 0.0007, 37: 0.0004,
    38: 0.0002, 39: 0.0001
}
NUM_MAINLINE_CHILD_PD = {
    1: 0.8,
    2: 0.1975,
    3: 0.025,
}
MINIMUM_GAP_BETWEEN_SIBLINGS_YEARS = 2

MOTHER_AGE_AT_FIRST_CHILD_PD = { age: prob for age, prob in CHILD_BY_MOTHER_AGE_PD.items()}

FATHER_AGE_OFFSET_PD = {
    -1: 0.05, 0: 0.1, 1: 0.2, 2: 0.3,
    3: 0.2, 4: 0.1, 5: 0.05,
}

# MOTHER_AGE_OF_MARRIAGE_PD = {
#     16: 0.3, 17: 0.25, 18: 0.20, 19: 0.1,
#     20: 0.06, 21: 0.03, 22: 0.01,
#}

# CK3 Specific Constants
DAYS_IN_YEAR = 365
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]   # Will Ignore Leap years for now
# Days will be 1-justified
# 867.1.1
CK3_867_START_DAY = convert_calendar_years_to_days(867)
# 1066.9.15
CK3_1066_START_DAY = convert_calendar_years_to_days(1066) + sum(DAYS_IN_MONTH[:8]) + 15 - 1
# 867.10.1
CK3_1178_START_DAY = convert_calendar_years_to_days(1178) + sum(DAYS_IN_MONTH[:9]) + 1 - 1

CHANCE_OF_SON = 0.51