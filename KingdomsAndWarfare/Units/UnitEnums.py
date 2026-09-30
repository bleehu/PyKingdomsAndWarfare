"""Enums for a unit's tier, experience, and equipment levels.

All are IntEnums ordered from weakest to strongest, so raising or lowering a
level is `Enum(value + 1)` or `Enum(value - 1)`.
"""

from enum import Enum
from enum import IntEnum

class Tier(IntEnum):
    """A unit's power tier, from I (weakest) to V (strongest)."""
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5

class Experience(IntEnum):
    """A unit's experience level.

    Levies are untrained conscripts that can never level up. Other units
    start at Regular and advance through battle.
    """
    LEVIES = 1
    REGULAR = 2
    VETERAN = 3
    ELITE = 4
    SUPER_ELITE = 5

class Equipment(IntEnum):
    """A unit's equipment level, from Light to Super-heavy."""
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3
    SUPER_HEAVY = 4
