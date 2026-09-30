"""The Aerial unit type: flying units such as griffon riders."""

from . import UnitEnums
from .UnitType import UnitType

class Aerial(UnitType):
    """Flying units. Level up evenly, with extra command.

    Each level: +1 attack, +1 defense, +1 morale, +2 command, and +1 attacks
    on reaching Elite. Each equipment level: +1 power, +1 toughness, and +1
    damage on reaching Super-heavy.
    """

    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after gaining a level: +1 attack, defense, and morale, +2 command, and +1 attacks when going from Veteran to Elite."""
        attack = attack + 1
        defense = defense + 1
        morale = morale + 1
        command = command + 2
        if experience == UnitEnums.Experience.VETERAN:
            attacks = attacks + 1
        return attacks, attack, defense, morale, command

    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after losing a level. Undoes `level_up`."""
        attack = attack - 1
        defense = defense - 1
        morale = morale - 1
        command = command - 2
        if experience == UnitEnums.Experience.ELITE:
            attacks = attacks - 1
        return attacks, attack, defense, morale, command

    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after gaining an equipment level: +1 power and toughness, and +1 damage when going from Heavy to Super-heavy."""
        power = power + 1
        toughness = toughness + 1
        if equipment == UnitEnums.Equipment.HEAVY:
            damage = damage + 1
        return power, toughness, damage

    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after losing an equipment level. Undoes `upgrade`."""
        power = power - 1
        toughness = toughness - 1
        if equipment == UnitEnums.Equipment.SUPER_HEAVY:
            damage = damage - 1
        return power, toughness, damage
