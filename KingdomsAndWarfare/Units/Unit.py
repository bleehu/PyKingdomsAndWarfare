from enum import Enum
from enum import IntEnum
from pdb import set_trace
from typing import Self

from ..Traits import Trait

class Unit:

    class Type(Enum):
        INFANTRY = 1
        ARTILLERY = 2
        CAVALRY = 3
        AERIAL = 4

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

    def __init__(self, 
                 name: str, 
                 description: str = '', 
                 ancestry: str = '', 
                 experience: Experience = Experience.REGULAR,
                 equipment: Equipment = Equipment.LIGHT,
                 tier: Tier = Tier.I,
                 size: int = 6,
                 attacks: int = 1,
                 damage: int = 1,
                 attack: int = 0,
                 defense: int = 10,
                 power: int = 0,
                 toughness: int = 10,
                 morale: int = 0,
                 command: int = 0,
                 traits: list[str] = []):
        self.name = name
        self.description = description
        self.battles = Unit.battles_from_xp(experience)
        self.traits = traits
        self.experience = experience
        self.equipment = equipment
        self.tier = tier
        self.attack = attack
        self.defense = defense
        self.power = power
        self.toughness = toughness
        self.morale = morale
        self.command = command
        self.damage = damage
        self.size = size
        self.attacks = attacks
        self.ancestry = ancestry

    def __eq__(self, __value: Self) -> bool:
        matches = (
            self.name == __value.name
            and self.ancestry == __value.ancestry
            and self.attack == __value.attack
            and self.attacks == __value.attacks
            and self.battles == __value.battles
            and self.command == __value.command
            and self.damage == __value.damage
            and self.defense == __value.defense
            and self.description == __value.description
            and self.equipment == __value.equipment
            and self.experience == __value.experience
            and self.morale == __value.morale
            and self.power == __value.power
            and self.size == __value.size
            and self.tier == __value.tier
            and self.toughness == __value.toughness
            and self.traits == __value.traits
            and self.type == __value.type
        )
        return matches

    def __repr__(self) -> str:
        return f"{self.name}: [{self.experience}, {self.equipment}, {self.ancestry}, {self.Type}] \
            Tier: {self.tier}, \
                ATK: {self.attack} DEF {self.defense} POW {self.power} TOU {self.toughness} \
                MOR {self.morale} COM {self.command}. Size {self.size}. {self.attacks} attacks \
                at {self.damage} each. Traits: {self.traits}."

    def add_trait(self, trait: Trait) -> None:
        """Adds a trait that gives a unit special abilities or weaknesses to the unit.
        Throws an error if more than 4 traits are added."""
        if len(self.traits) < 5:
            self.traits.append(trait)
        else:
            raise Exception("This unit already has 4 traits!")

    def battle(self) -> None:
        """Credits the unit with 1 battle experience and if it has enough experience to
        level up, it does so."""
        self.battles = self.battles + 1
        if self.experience != Unit.Experience.LEVIES:
            if self.battles == 1 or self.battles == 4 or self.battles == 8:
                self.level_up()

    def upgrade(self) -> None:
        if self.experience == Unit.Experience.LEVIES:
            raise CannotUpgradeError("Cannot upgrade Levies")
        if self.equipment == Unit.Equipment.SUPER_HEAVY:
            raise CannotUpgradeError("Cannot upgrade equipment past super-heavy.")
        self.equipment = Unit.Equipment(self.equipment + 1)

    def downgrade(self) -> None:
        if self.experience == Unit.Experience.LEVIES:
            raise CannotUpgradeError("Cannot downgrade Levies")
        if self.equipment == Unit.Equipment.LIGHT:
            raise CannotUpgradeError("Cannot downgrade equipment below Light")
        self.equipment = Unit.Equipment(self.equipment - 1)

    def level_up(self) -> None:
        """Bumps the experience of the unit up one level. Throws an error if
        you try to raise it above super-elite experience."""
        if self.experience == Unit.Experience.LEVIES:
            raise CannotLevelUpError("Cannot level up levies.")
        if self.experience == Unit.Experience.SUPER_ELITE:
            raise CannotLevelUpError("Cannot level up a unit past Super-elite.")
        self.experience = Unit.Experience(self.experience + 1)
        self.battles = Unit.battles_from_xp(self.experience)

    def level_down(self) -> None:
        """Reduces the experience of the unit one level. Usually as an 'undo' for
        leveling up a unit. Throws an error if you try to reduce a unit's level
        below Regular."""
        if self.experience == Unit.Experience.LEVIES:
            raise CannotLevelUpError("Cannot level down levies.")
        if self.experience == Unit.Experience.REGULAR:
            raise CannotLevelUpError("Cannot lower level below regular.")
        self.experience = Unit.Experience(self.experience - 1)
        self.battles = Unit.battles_from_xp(self.experience)

    def to_dict(self) -> dict:
        to_return = {
            "name": self.name,
            "description": self.description,
            "type": str(self.type),
            "battles": self.battles,
            "traits": [],
            "experience": self.experience.name,
            "equipment": self.equipment.name,
            "tier": self.tier,
            "size": self.size,
            "attack": self.attack,
            "defense": self.defense,
            "power": self.power,
            "toughness": self.toughness,
            "morale": self.morale,
            "command": self.command,
            "damage": self.damage,
            "attacks": self.attacks,
            "ancestry": self.ancestry,
        }
        for trait in self.traits:
            to_return["traits"].append(trait.to_dict())
        return to_return
    
    def battles_from_xp(experience: Experience) -> int:
        if experience == Unit.Experience.REGULAR or experience == Unit.Experience.LEVIES:
            return 0
        elif experience == Unit.Experience.VETERAN:
            return 1
        elif experience == Unit.Experience.ELITE:
            return 4
        elif experience == Unit.Experience.SUPER_ELITE:
            return 8
        else:
            raise NoSuchUnitExperienceError("Invalid unit experience detected: " + str(experience))


class CannotUpgradeError(Exception):
    pass


class CannotLevelUpError(Exception):
    pass
