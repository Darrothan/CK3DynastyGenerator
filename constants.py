PD_CHILD_BY_MOTHER_AGE = {
    16: 0.0064,
    17: 0.0191,
    18: 0.0383,
    19: 0.0638,
    20: 0.0893,
    21: 0.1084,
    22: 0.1212,
    23: 0.1148,
    24: 0.1021,
    25: 0.0829,
    26: 0.0638,
    27: 0.0510,
    28: 0.0383,
    29: 0.0287,
    30: 0.0223,
    31: 0.0159,
    32: 0.0115,
    33: 0.0077,
    34: 0.0051,
    35: 0.0032,
    36: 0.0019,
    37: 0.0013,
    38: 0.0010,
    39: 0.0006,
    40: 0.0005,
    41: 0.0004,
    42: 0.0003,
    43: 0.0001,
    44: 0.00005,
    45: 0.00001,
}

# THIS IS FOR SMALL-RANGE (100 years) GENERATION OF AN INTERESTING AND LARGE FAMILY
# PD_NOTABLE_MALE_CHILDREN = {
#     1: 0.25,
#     2: 0.45,
#     3: 0.25,
#     4: 0.04,
#     5: 0.01,
# }

# THIS IS FOR MEDIUM-RANGE (200 years), STILL INTERESTING FAMILIES
# PD_NOTABLE_MALE_CHILDREN = {
#     1: 0.40,
#     2: 0.35,
#     3: 0.18,
#     4: 0.05,
#     5: 0.02,
# }

# THIS IS FOR LARGER-RANGE (400+ years), MORE HISTORICALLY PLAUSIBLE FAMILIES
# PD_NOTABLE_MALE_CHILDREN = {
#     1: 0.50,
#     2: 0.30,
#     3: 0.15,
#     4: 0.04,
#     5: 0.01,
# }

# # THIS IS FOR TROUBLED FAMILIES THAT AREN'T AS LUCKY
PD_NOTABLE_MALE_CHILDREN = {
    0: 0.25,   # sometimes no notable sons at all
    1: 0.40,
    2: 0.23,
    3: 0.08,
    4: 0.03,
    5: 0.01,
}


NORMAL_MORTALITY_RANGE = (50, 70)
# EARLY_MORTALITY_RANGE = (20, 49)
# EARLY_MORTALITY_PROBABILITY = 0.25
EARLY_MORTALITY_RANGE = (16, 49)   # some die before or just as they start families
EARLY_MORTALITY_PROBABILITY = 0.45 # almost half die early


PD_MOTHER_AGE_OF_FIRST_CHILD = {
    16: 0.025,
    17: 0.05,
    18: 0.1,
    19: 0.2,
    20: 0.25,
    21: 0.2,
    22: 0.1,
    23: 0.05,
    24: 0.025,
}

PD_FATHER_AVERAGE_AGE_OFFSET = {
    -1: 0.05,
    0: 0.1,
    1: 0.2,
    2: 0.3,
    3: 0.2,
    4: 0.1,
    5: 0.05,
}

# CK3 Specific Constants
DAYS_IN_YEAR = 365
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]   # Will Ignore Leap years for now
# Days will be 1-justified
CK3_867_START_DAY = 867*365 + 1
CK3_1066_START_DAY = 1066*365 + 1
CK3_1178_START_DAY = 1178*365 + 1