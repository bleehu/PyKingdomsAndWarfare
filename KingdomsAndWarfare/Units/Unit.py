"""The Unit class: a single military unit card, its stats, and how those stats change."""

from pdb import set_trace
from warnings import warn
from typing import Self
from random import randint

from . import UnitEnums
from .UnitType import UnitType
from ..Traits import Trait

class Unit:
    """A military unit card: its identity, stats, experience, equipment, and traits.

    Stat changes from leveling and equipment upgrades are delegated to the
    unit's `unit_type` (Infantry, Cavalry, Artillery, or Aerial).

    Attributes:
        name: Display name of the unit.
        unit_type: The UnitType class that decides how this unit's stats grow.
        description: Flavor text for the unit.
        ancestry: The unit's ancestry, e.g. "Human" or "Dwarf".
        experience: Current experience level.
        equipment: Current equipment level.
        tier: Power tier of the unit.
        battles: Number of battles the unit has fought.
        size: Full strength of the unit.
        casualties: Remaining strength. Starts equal to `size` and goes
            down as the unit takes hits.
        attacks: Number of attacks the unit makes each turn.
        damage: Extra casualties dealt when an attack also passes its power test.
        attack: Bonus added to attack rolls.
        defense: Target number enemies must meet to hit this unit.
        power: Bonus added to power rolls.
        toughness: Target number enemy power rolls must meet to deal extra damage.
        morale: Bonus to morale tests.
        command: Bonus to command tests.
        traits: Special abilities or weaknesses attached to the unit.
    """

    def __init__(self, 
                 name: str, 
                 unit_type: type[UnitType],
                 description: str = '', 
                 ancestry: str = '', 
                 experience: UnitEnums.Experience = UnitEnums.Experience.REGULAR,
                 equipment: UnitEnums.Equipment = UnitEnums.Equipment.LIGHT,
                 tier: UnitEnums.Tier = UnitEnums.Tier.I,
                 size: int = 6,
                 attacks: int = 1,
                 damage: int = 1,
                 attack: int = 0,
                 defense: int = 10,
                 power: int = 0,
                 toughness: int = 10,
                 morale: int = 0,
                 command: int = 0,
                 traits: list[Trait] = []):
        """Create a unit at full strength.

        Only `name` and `unit_type` are required. Every other stat defaults to
        a baseline Tier I, Regular, Light-equipment unit of size 6. `battles`
        is set to match the starting experience.

        Args:
            name: Display name of the unit.
            unit_type: The UnitType class, e.g. `Infantry`. Pass the class itself, not an instance.
            description: Flavor text for the unit.
            ancestry: The unit's ancestry.
            experience: Starting experience level.
            equipment: Starting equipment level.
            tier: Power tier of the unit.
            size: Full strength. The unit starts with no losses.
            attacks: Number of attacks per turn.
            damage: Extra casualties dealt on a successful power test.
            attack: Bonus to attack rolls.
            defense: Target number enemies must meet to hit this unit.
            power: Bonus to power rolls.
            toughness: Target number enemy power rolls must meet.
            morale: Bonus to morale tests.
            command: Bonus to command tests.
            traits: Traits to attach to the unit.
        """
        self.name = name
        self.unit_type = unit_type
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
        self.casualties = size
        self.attacks = attacks
        self.ancestry = ancestry

    def __eq__(self, __value: Self) -> bool:
        """Return True if every stat, trait, and identifying field matches `__value`."""
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
            and self.casualties == __value.casualties
            and self.tier == __value.tier
            and self.toughness == __value.toughness
            and self.traits == __value.traits
            and self.unit_type == __value.unit_type
        )
        return matches

    def __repr__(self) -> str:
        """Return a one-line summary of the unit's stats, for debugging."""
        return f"{self.name}: [{self.experience}, {self.equipment}, {self.ancestry}, {self.unit_type}] \
            Tier: {self.tier}, \
                ATK: {self.attack} DEF {self.defense} POW {self.power} TOU {self.toughness} \
                MOR {self.morale} COM {self.command}. Casualties/Size {self.casualties}/{self.size}. {self.attacks} attacks \
                at {self.damage} each. Traits: {self.traits}."

    def add_trait(self, trait: Trait) -> None:
        """Attach a trait to the unit.

        Args:
            trait: The special ability or weakness to add.

        Raises:
            Exception: If the unit already has five traits.
        """
        if len(self.traits) < 5:
            self.traits.append(trait)
        else:
            raise Exception("This unit already has 4 traits!")

    def battle(self) -> None:
        """Record one battle fought, leveling the unit up when it reaches a milestone.

        A unit levels up on its 1st, 4th, and 8th battle, becoming Veteran,
        Elite, and Super-elite. Levies gain battles but never level up.
        """
        self.battles = self.battles + 1
        if self.experience != UnitEnums.Experience.LEVIES:
            if self.battles == 1 or self.battles == 4 or self.battles == 8:
                self.level_up()

    def upgrade(self) -> None:
        """Raise the unit's equipment one level and apply the matching stat bonuses.

        Raises:
            CannotUpgradeError: If the unit is Levies or already has
                Super-heavy equipment.
        """
        if self.experience == UnitEnums.Experience.LEVIES:
            raise CannotUpgradeError("Cannot upgrade Levies")
        if self.equipment == UnitEnums.Equipment.SUPER_HEAVY:
            raise CannotUpgradeError("Cannot upgrade equipment past super-heavy.")
        self.power, self.toughness, self.damage = self.unit_type.upgrade(self.equipment, self.power, self.toughness, self.damage)
        self.equipment = UnitEnums.Equipment(self.equipment + 1)

    def downgrade(self) -> None:
        """Lower the unit's equipment one level and remove the matching stat bonuses.

        This is the undo for `upgrade`.

        Raises:
            CannotUpgradeError: If the unit is Levies or already has
                Light equipment.
        """
        if self.experience == UnitEnums.Experience.LEVIES:
            raise CannotUpgradeError("Cannot downgrade Levies")
        if self.equipment == UnitEnums.Equipment.LIGHT:
            raise CannotUpgradeError("Cannot downgrade equipment below Light")
        self.power, self.toughness, self.damage = self.unit_type.downgrade(self.equipment, self.power, self.toughness, self.damage)
        self.equipment = UnitEnums.Equipment(self.equipment - 1)

    def level_up(self) -> None:
        """Raise the unit's experience one level and apply the matching stat bonuses.

        `battles` is reset to the minimum count for the new experience level.

        Raises:
            CannotLevelUpError: If the unit is Levies or already Super-elite.
        """
        if self.experience == UnitEnums.Experience.LEVIES:
            raise CannotLevelUpError("Cannot level up levies.")
        if self.experience == UnitEnums.Experience.SUPER_ELITE:
            raise CannotLevelUpError("Cannot level up a unit past Super-elite.")
        self.attacks, self.attack, self.defense, self.morale, self.command = \
            self.unit_type.level_up(self.experience, self.attacks, self.attack, self.defense, self.morale, self.command)
        self.experience = UnitEnums.Experience(self.experience + 1)
        self.battles = Unit.battles_from_xp(self.experience)

    def level_down(self) -> None:
        """Lower the unit's experience one level and remove the matching stat bonuses.

        This is the undo for `level_up`. `battles` is reset to the minimum
        count for the new experience level.

        Raises:
            CannotLevelUpError: If the unit is Levies or already Regular.
        """
        if self.experience == UnitEnums.Experience.LEVIES:
            raise CannotLevelUpError("Cannot level down levies.")
        if self.experience == UnitEnums.Experience.REGULAR:
            raise CannotLevelUpError("Cannot lower level below regular.")
        self.attacks, self.attack, self.defense, self.morale, self.command = \
            self.unit_type.level_down(self.experience, self.attacks, self.attack, self.defense, self.morale, self.command)
        self.experience = UnitEnums.Experience(self.experience - 1)
        self.battles = Unit.battles_from_xp(self.experience)

    def attack_unit(self, target: "Unit", attack_roll: int, power_roll: int):
        """Resolve one attack against `target`, reducing its remaining strength.

        If `attack_roll + attack` meets the target's defense, the target loses
        1. If `power_roll + power` then also meets the target's toughness, it
        loses `damage` more. A miss does nothing. The caller supplies the
        rolls, so dice can be real, simulated, or fixed for tests.

        Args:
            target: The unit being attacked.
            attack_roll: The raw die result for the attack test.
            power_roll: The raw die result for the power test.

        Warns:
            UserWarning: If a unit attacks itself (or an identical unit).
        """
        if(self == target):
            warn(f"Unit {self.name} is attacking itself!")
        attack_score = attack_roll + self.attack
        if (attack_score >= target.defense):
            target.casualties = target.casualties - 1
            power_score = power_roll + self.power
            if (power_score >= target.toughness):
                target.casualties = target.casualties - self.damage
    
    def get_diminished(self):
        """Return True if the unit's remaining strength (`casualties`) is at least half its `size`."""
        return self.casualties * 2 >= self.size


    def to_dict(self) -> dict:
        """Serialize the unit to a JSON-friendly dict.

        Enums are stored by name, the unit type by its class name, and traits
        as nested dicts. Use `UnitFactory.unit_from_dict` to read it back.
        """
        to_return = {
            "name": self.name,
            "description": self.description,
            "type": self.unit_type.__qualname__,
            "battles": self.battles,
            "traits": [],
            "experience": self.experience.name,
            "equipment": self.equipment.name,
            "tier": self.tier,
            "size": self.size,
            "casualties": self.casualties,
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

    def battles_from_xp(experience: UnitEnums.Experience) -> int:
        """Return the minimum number of battles a unit needs for an experience level.

        Call this on the class: `Unit.battles_from_xp(experience)`.

        Args:
            experience: The experience level to look up.

        Returns:
            0 for Levies and Regular, 1 for Veteran, 4 for Elite, and 8 for Super-elite.
        """
        if experience == UnitEnums.Experience.REGULAR or experience == UnitEnums.Experience.LEVIES:
            return 0
        elif experience == UnitEnums.Experience.VETERAN:
            return 1
        elif experience == UnitEnums.Experience.ELITE:
            return 4
        elif experience == UnitEnums.Experience.SUPER_ELITE:
            return 8
        else:
            raise NoSuchUnitExperienceError("Invalid unit experience detected: " + str(experience))


class CannotUpgradeError(Exception):
    """Raised when a unit's equipment cannot be raised or lowered any further."""
    pass


class CannotLevelUpError(Exception):
    """Raised when a unit's experience cannot be raised or lowered any further."""
    pass
