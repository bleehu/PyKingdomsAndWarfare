from . import UnitEnums
from .UnitType import UnitType

class Infantry(UnitType):
    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        attack = attack + 1
        defense = defense + 2
        morale = morale + 2
        if experience != UnitEnums.Experience.VETERAN:
            command = command + 1
        if experience == UnitEnums.Experience.VETERAN:
            attacks = attacks + 1
        return attacks, attack, defense, morale, command

    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        attack = attack - 1
        defense = defense - 2
        morale = morale - 2
        if experience != UnitEnums.Experience.ELITE:
            command = command - 1
        if experience == UnitEnums.Experience.ELITE:
            attacks = attacks - 1
        return attacks, attack, defense, morale, command

    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Upgrade a unit's equipment bonuses. This is usually done by spending gold."""
        power = power + 2
        toughness = toughness + 2
        if equipment == UnitEnums.Equipment.HEAVY:
            damage = damage + 1
        return power, toughness, damage

    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Downgrade a unit's equipment bonuses. This is usualy the 'undo' function for upgrading."""
        power = power - 2
        toughness = toughness - 2
        if equipment == UnitEnums.Equipment.SUPER_HEAVY:
            damage = damage - 1
        return power, toughness, damage
