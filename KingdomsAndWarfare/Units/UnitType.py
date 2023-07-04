from abc import ABCMeta, abstractmethod

from . import UnitEnums

class UnitType(metaclass = ABCMeta):
    @abstractmethod
    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        raise NotImplementedError()

    @abstractmethod
    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        raise NotImplementedError()

    @abstractmethod
    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        raise NotImplementedError()

    @abstractmethod
    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        raise NotImplementedError()
