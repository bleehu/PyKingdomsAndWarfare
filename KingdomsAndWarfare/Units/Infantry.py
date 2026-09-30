"""The Infantry unit type: foot soldiers."""

from . import UnitEnums
from .UnitType import UnitType

class Infantry(UnitType):
    """Foot soldiers. Level up with a focus on defense and morale.

    Each level: +1 attack, +2 defense, +2 morale, and +1 command, except on
    reaching Elite, where they gain +1 attacks instead of command. Each
    equipment level: +2 power, +2 toughness, and +1 damage on reaching Super-heavy.
    """

    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after gaining a level: +1 attack, +2 defense and morale, and +1 command, or +1 attacks instead of command when going from Veteran to Elite."""
        attack = attack + 1
        defense = defense + 2
        morale = morale + 2
        if experience != UnitEnums.Experience.VETERAN:
            command = command + 1
        if experience == UnitEnums.Experience.VETERAN:
            attacks = attacks + 1
        return attacks, attack, defense, morale, command

    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after losing a level. Undoes `level_up`."""
        attack = attack - 1
        defense = defense - 2
        morale = morale - 2
        if experience != UnitEnums.Experience.ELITE:
            command = command - 1
        if experience == UnitEnums.Experience.ELITE:
            attacks = attacks - 1
        return attacks, attack, defense, morale, command

    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after gaining an equipment level: +2 power and toughness, and +1 damage when going from Heavy to Super-heavy."""
        power = power + 2
        toughness = toughness + 2
        if equipment == UnitEnums.Equipment.HEAVY:
            damage = damage + 1
        return power, toughness, damage

    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after losing an equipment level. Undoes `upgrade`."""
        power = power - 2
        toughness = toughness - 2
        if equipment == UnitEnums.Equipment.SUPER_HEAVY:
            damage = damage - 1
        return power, toughness, damage
