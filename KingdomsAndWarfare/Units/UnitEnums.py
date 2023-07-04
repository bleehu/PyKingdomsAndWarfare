from enum import Enum
from enum import IntEnum

class Tier(IntEnum):
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5

class Experience(IntEnum):
    LEVIES = 1
    REGULAR = 2
    VETERAN = 3
    ELITE = 4
    SUPER_ELITE = 5

class Equipment(IntEnum):
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3
    SUPER_HEAVY = 4
