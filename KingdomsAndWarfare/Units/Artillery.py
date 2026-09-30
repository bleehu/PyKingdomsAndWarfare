"""The Artillery unit type: siege engines and ranged war machines."""

from . import UnitEnums
from .UnitType import UnitType

class Artillery(UnitType):
    """Siege engines and war machines. Level up with a focus on attack.

    Each level: +2 attack, +1 defense, +1 morale, +1 command, and +1 attacks
    on reaching Veteran. Each equipment level: +1 power and +1 toughness.
    Damage never changes with equipment.
    """

    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after gaining a level: +2 attack, +1 defense, morale, and command, and +1 attacks when going from Regular to Veteran."""
        attack = attack + 2
        defense = defense + 1
        morale = morale + 1
        command = command + 1
        if experience == UnitEnums.Experience.REGULAR:
            attacks = attacks + 1
        return attacks, attack, defense, morale, command

    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return stats after losing a level. Undoes `level_up`."""
        attack = attack - 2
        defense = defense - 1
        morale = morale - 1
        command = command - 1
        if experience == UnitEnums.Experience.VETERAN:
            attacks = attacks - 1
        return attacks, attack, defense, morale, command

    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after gaining an equipment level: +1 power and toughness."""
        power = power + 1
        toughness = toughness + 1
        return power, toughness, damage

    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return stats after losing an equipment level. Undoes `upgrade`."""
        power = power - 1
        toughness = toughness - 1
        return power, toughness, damage
