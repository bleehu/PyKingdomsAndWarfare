"""The UnitType base class, which defines how a kind of unit's stats grow."""

from abc import ABCMeta, abstractmethod

from . import UnitEnums

class UnitType(metaclass = ABCMeta):
    """Abstract base for a kind of unit (Infantry, Cavalry, Artillery, Aerial).

    A unit type holds no state. It only defines how a unit's stats change when
    it gains or loses experience or equipment. Subclasses are used as the
    class itself, never instantiated: a `Unit` stores the class in
    `unit_type` and calls these methods on it directly, which is why they take
    no `self`.

    Every method receives the unit's *current* level (before the change) and
    its current stats, and returns the new stats. Each `level_down` must undo
    the matching `level_up`, and each `downgrade` must undo the matching `upgrade`.
    """

    @abstractmethod
    def level_up(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return a unit's stats after gaining one experience level.

        Args:
            experience: The unit's experience before leveling up.
            attacks: Current number of attacks.
            attack: Current attack bonus.
            defense: Current defense.
            morale: Current morale bonus.
            command: Current command bonus.

        Returns:
            The new `(attacks, attack, defense, morale, command)`.
        """
        raise NotImplementedError()

    @abstractmethod
    def level_down(experience: UnitEnums.Experience, attacks: int, attack: int, defense: int, morale: int, command: int) -> tuple[int, int, int, int, int]:
        """Return a unit's stats after losing one experience level. Undoes `level_up`.

        Args:
            experience: The unit's experience before leveling down.
            attacks: Current number of attacks.
            attack: Current attack bonus.
            defense: Current defense.
            morale: Current morale bonus.
            command: Current command bonus.

        Returns:
            The new `(attacks, attack, defense, morale, command)`.
        """
        raise NotImplementedError()

    @abstractmethod
    def upgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return a unit's stats after gaining one equipment level.

        Args:
            equipment: The unit's equipment before upgrading.
            power: Current power bonus.
            toughness: Current toughness.
            damage: Current damage.

        Returns:
            The new `(power, toughness, damage)`.
        """
        raise NotImplementedError()

    @abstractmethod
    def downgrade(equipment: UnitEnums.Equipment, power: int, toughness: int, damage: int) -> tuple[int, int, int]:
        """Return a unit's stats after losing one equipment level. Undoes `upgrade`.

        Args:
            equipment: The unit's equipment before downgrading.
            power: Current power bonus.
            toughness: Current toughness.
            damage: Current damage.

        Returns:
            The new `(power, toughness, damage)`.
        """
        raise NotImplementedError()
